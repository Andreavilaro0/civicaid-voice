"""Orchestrator: receives IncomingMessage, executes skills in order, sends response."""

import time
import threading
from src.core.models import (
    IncomingMessage, InputType, FinalResponse, CacheResult,
    TranscriptResult, KBContext, LLMResponse,
)
from src.core import cache
from src.core.config import config
from src.core.skills.detect_lang import detect_language
from src.core.skills.kb_lookup import kb_lookup  # noqa: F401 — kept for backward compat
from src.core.retriever import get_retriever
from src.core.skills.analyze_image import analyze_image
from src.core.skills.llm_generate import llm_generate
from src.core.skills.verify_response import verify_response
from src.core.skills.send_response import send_final_message
from src.core.prompts.templates import get_template
from src.core.memory.user_hash import derive_user_id
from src.core.memory.store import get_store
from src.core.memory.models import new_memory_state
from src.core.memory.commands import detect_memory_command, MemoryCommand
from src.core.memory.sanitize import sanitize_for_prompt
from src.core.memory.update import update_memory_after_response
from src.utils.logger import log_cache, log_error, log_memory, log_observability, log_pipeline_result
from src.utils.observability import get_context

# ── Inactivity follow-up + goodbye tracking ──
# {phone_number: {"timestamp": float, "language": str, "timer": Timer, "goodbye_timer": Timer|None}}
_user_activity: dict[str, dict] = {}
_activity_lock = threading.Lock()
FOLLOWUP_DELAY = 300  # 5 minutes
GOODBYE_DELAY = 180   # 3 minutes after follow-up


def _schedule_followup(phone: str, language: str) -> None:
    """Schedule a follow-up message after FOLLOWUP_DELAY seconds of inactivity."""
    with _activity_lock:
        # Cancel previous timers (both followup and goodbye)
        prev = _user_activity.get(phone)
        if prev:
            if prev.get("timer"):
                prev["timer"].cancel()
            if prev.get("goodbye_timer"):
                prev["goodbye_timer"].cancel()
        # Schedule new timer
        timer = threading.Timer(FOLLOWUP_DELAY, _send_followup_if_idle, args=[phone, language, time.time()])
        timer.daemon = True
        timer.start()
        _user_activity[phone] = {"timestamp": time.time(), "language": language, "timer": timer, "goodbye_timer": None}


def _send_followup_if_idle(phone: str, language: str, scheduled_at: float) -> None:
    """Send follow-up only if user hasn't sent anything since scheduled_at."""
    with _activity_lock:
        entry = _user_activity.get(phone)
        if not entry or entry["timestamp"] > scheduled_at:
            return  # User sent a message after this was scheduled
    try:
        if config.WHATSAPP_PROVIDER == "meta":
            from src.core.skills.send_response_meta import send_followup
            send_followup(phone, language)
        else:
            # Twilio: send plain text follow-up
            from src.core.skills.send_response_meta import FOLLOWUP, FOLLOWUP_SPEECH
            followup_text = FOLLOWUP.get(language, FOLLOWUP["es"])
            response = FinalResponse(
                to_number=phone, body=followup_text,
                source="followup", total_ms=0,
            )
            send_final_message(response)
            _send_audio_async(phone, FOLLOWUP_SPEECH.get(language, FOLLOWUP_SPEECH["es"]), language)
    except Exception as e:
        log_error("followup_timer", str(e))

    # Schedule goodbye after follow-up
    _schedule_goodbye(phone, language)


def _schedule_goodbye(phone: str, language: str) -> None:
    """Schedule a goodbye message after GOODBYE_DELAY seconds post-follow-up."""
    with _activity_lock:
        entry = _user_activity.get(phone)
        if not entry:
            return
        # Cancel previous goodbye timer if any
        if entry.get("goodbye_timer"):
            entry["goodbye_timer"].cancel()
        goodbye_timer = threading.Timer(GOODBYE_DELAY, _send_goodbye_if_idle, args=[phone, language, time.time()])
        goodbye_timer.daemon = True
        goodbye_timer.start()
        entry["goodbye_timer"] = goodbye_timer


def _send_goodbye_if_idle(phone: str, language: str, scheduled_at: float) -> None:
    """Send goodbye only if user hasn't sent anything since the follow-up."""
    with _activity_lock:
        entry = _user_activity.get(phone)
        if not entry or entry["timestamp"] > scheduled_at:
            return  # User sent a message after follow-up
    try:
        if config.WHATSAPP_PROVIDER == "meta":
            from src.core.skills.send_response_meta import send_goodbye
            send_goodbye(phone, language)
        else:
            # Twilio: send plain text goodbye
            from src.core.skills.send_response_meta import GOODBYE, GOODBYE_SPEECH
            goodbye_text = GOODBYE.get(language, GOODBYE["es"])
            response = FinalResponse(
                to_number=phone, body=goodbye_text,
                source="goodbye", total_ms=0,
            )
            send_final_message(response)
            _send_audio_async(phone, GOODBYE_SPEECH.get(language, GOODBYE_SPEECH["es"]), language)
    except Exception as e:
        log_error("goodbye_timer", str(e))

    # Clean up history and activity
    try:
        from src.core.conversation_history import clear_history
        clear_history(phone)
    except Exception:
        pass
    with _activity_lock:
        _user_activity.pop(phone, None)


def _send_audio_async(to_number: str, text: str, language: str) -> None:
    """Generate TTS and send audio as a separate message (non-blocking)."""
    def _do_tts():
        try:
            from src.core.skills.tts import text_to_audio
            audio_url = text_to_audio(text, language)
            if audio_url:
                if config.WHATSAPP_PROVIDER == "meta":
                    from src.core.skills.send_response_meta import send_audio_only
                    send_audio_only(to_number, audio_url)
                else:
                    response = FinalResponse(
                        to_number=to_number, body="", media_url=audio_url,
                        source="tts", total_ms=0,
                    )
                    send_final_message(response)
        except Exception as e:
            log_error("async_tts", str(e))

    t = threading.Thread(target=_do_tts, daemon=True)
    t.start()


def _build_media_url(audio_file: str | None) -> str | None:
    """Build public URL for cached audio file."""
    if not audio_file or not config.AUDIO_BASE_URL:
        return None
    return f"{config.AUDIO_BASE_URL.rstrip('/')}/{audio_file}"


def process(msg: IncomingMessage) -> None:
    """Main pipeline — runs in background thread after ACK."""
    start = time.time()
    text = msg.body
    language = "es"
    ctx = get_context()

    try:
        # --- GREETING DETECTION → Welcome flow ---
        cmd_text = text.strip().lower().replace("/", "")
        is_greeting = cmd_text in (
            "hola", "hi", "hello", "hey",          # es / en
            "salut", "bonjour",                      # fr
            "oi", "ola", "olá",                      # pt
            "buna", "bună",                          # ro
            "bon dia",                               # ca
            "你好", "nihao",                          # zh
            "مرحبا", "أهلا", "سلام",                 # ar (script)
            "salam", "marhaba", "ahlan",             # ar (romanized)
            "start", "inicio",                       # commands
        )
        is_restart = cmd_text in ("menu", "reiniciar", "restart", "clear", "borrar", "reset")

        if is_greeting or is_restart:
            lang_detected = detect_language(text, phone=msg.from_number) if text else "es"
            if config.WHATSAPP_PROVIDER == "meta":
                from src.core.skills.send_response_meta import send_welcome
                send_welcome(msg.from_number, lang_detected)
            else:
                elapsed_ms = int((time.time() - start) * 1000)
                response = FinalResponse(
                    to_number=msg.from_number,
                    body=(
                        "👋 *Hola, soy Clara.*\n\n"
                        "Te ayudo con trámites sociales en España.\n\n"
                        "1️⃣ ¿Qué es el IMV?\n"
                        "2️⃣ Empadronamiento\n"
                        "3️⃣ Tarjeta sanitaria\n"
                        "4️⃣ NIE/TIE\n\n"
                        "Escribe tu pregunta o elige un número."
                    ),
                    source="welcome",
                    total_ms=elapsed_ms,
                )
                send_final_message(response)
            return

        # --- INTERACTIVE BUTTON REPLIES (Meta) ---
        if text.startswith("btn_"):
            button_map = {
                "btn_imv": "¿Qué es el IMV?",
                "btn_empadronamiento": "¿Cómo me empadrono?",
                "btn_salud": "¿Cómo saco la tarjeta sanitaria?",
                "btn_continue": "",  # Continue = do nothing
                "btn_restart": "RESTART",
            }
            mapped = button_map.get(text, text)
            if mapped == "":
                return  # "Seguir conversación" = do nothing
            if mapped == "RESTART":
                lang_detected = detect_language("", phone=msg.from_number)
                if config.WHATSAPP_PROVIDER == "meta":
                    from src.core.skills.send_response_meta import send_welcome
                    send_welcome(msg.from_number, lang_detected)
                return
            text = mapped

        # --- GUARDRAILS PRE-CHECK ---
        if config.GUARDRAILS_ON:
            from src.core.guardrails import pre_check
            guard_result = pre_check(text)
            if not guard_result.safe:
                elapsed_ms = int((time.time() - start) * 1000)
                log_pipeline_result(msg.request_id, msg.from_number, "guardrail", elapsed_ms)
                response = FinalResponse(
                    to_number=msg.from_number,
                    body=guard_result.modified_text or "No puedo ayudar con ese tema.",
                    source="guardrail",
                    total_ms=elapsed_ms,
                )
                send_final_message(response)
                return

        # --- AUDIO PIPELINE (Gemini transcription) ---
        if msg.input_type == InputType.AUDIO and msg.media_url:
            from src.core.skills.fetch_media import fetch_media
            from src.core.skills.transcribe import transcribe

            media_bytes = fetch_media(msg.media_url)
            if media_bytes is None:
                _send_fallback(msg, "whisper_fail", start)
                return

            mime_type = msg.media_type or "audio/ogg"
            # Pass conversation's last known language as hint for better detection
            from src.core.skills.detect_lang import get_conversation_lang
            lang_hint = get_conversation_lang(msg.from_number) if msg.from_number else None
            transcript: TranscriptResult = transcribe(media_bytes, mime_type, language_hint=lang_hint)

            if not transcript.success or not transcript.text:
                _send_fallback(msg, "whisper_fail", start)
                return

            text = transcript.text
            language = transcript.language
            # Remember detected audio language for future ACKs
            from src.core.skills.detect_lang import set_conversation_lang
            set_conversation_lang(msg.from_number, language)

        # --- DETECT LANGUAGE (for text input) ---
        if msg.input_type == InputType.TEXT:
            language = detect_language(text, phone=msg.from_number)

        # --- MEMORY BLOCK ---
        memory = None
        user_id = ""
        memory_store = None
        tramite_key = None  # Will be set after kb_lookup

        if config.MEMORY_ENABLED:
            import os
            user_id = derive_user_id(msg.from_number, config.MEMORY_SECRET_SALT)
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            memory_store = get_store(config.MEMORY_BACKEND, redis_url=redis_url)
            memory = memory_store.get(user_id) or new_memory_state(ttl_days=config.MEMORY_TTL_DAYS)

            # Check for forget command
            cmd = detect_memory_command(text)
            if cmd == MemoryCommand.FORGET:
                memory_store.forget(user_id)
                elapsed_ms = int((time.time() - start) * 1000)
                log_pipeline_result(msg.request_id, msg.from_number, "memory_forget", elapsed_ms)
                response = FinalResponse(
                    to_number=msg.from_number,
                    body=get_template("memory_forgotten", language),
                    source="memory_forget",
                    total_ms=elapsed_ms,
                )
                send_final_message(response)
                return

            # Check opt-in state
            if not memory.consent_opt_in and not config.MEMORY_OPTIN_DEFAULT:
                if cmd == MemoryCommand.OPT_IN_YES:
                    memory.consent_opt_in = True
                    memory.consent_set_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    memory_store.upsert(user_id, memory)
                    elapsed_ms = int((time.time() - start) * 1000)
                    response = FinalResponse(
                        to_number=msg.from_number,
                        body=get_template("memory_optin_confirmed", language),
                        source="memory_optin",
                        total_ms=elapsed_ms,
                    )
                    send_final_message(response)
                    return
                elif cmd == MemoryCommand.OPT_IN_NO:
                    memory.consent_opt_in = False
                    memory.consent_set_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    memory_store.upsert(user_id, memory)
                    elapsed_ms = int((time.time() - start) * 1000)
                    response = FinalResponse(
                        to_number=msg.from_number,
                        body=get_template("memory_optin_declined", language),
                        source="memory_optin",
                        total_ms=elapsed_ms,
                    )
                    send_final_message(response)
                    return
                elif memory.consent_set_at == "":
                    # First contact -- ask for consent
                    elapsed_ms = int((time.time() - start) * 1000)
                    response = FinalResponse(
                        to_number=msg.from_number,
                        body=get_template("memory_optin_ask", language),
                        source="memory_optin",
                        total_ms=elapsed_ms,
                    )
                    send_final_message(response)
                    return

        # --- CACHE MATCH ---
        cache_result: CacheResult = cache.match(text, language, msg.input_type)

        if cache_result.hit and cache_result.entry:
            elapsed_ms = int((time.time() - start) * 1000)
            log_cache(True, cache_result.entry.id, elapsed_ms)
            log_pipeline_result(msg.request_id, msg.from_number, "cache", elapsed_ms)
            if ctx:
                ctx.add_timing("cache", elapsed_ms)
                ctx.add_timing("total", elapsed_ms)
                log_observability(ctx)
            response = FinalResponse(
                to_number=msg.from_number,
                body=cache_result.entry.respuesta,
                media_url=_build_media_url(cache_result.entry.audio_file),
                source="cache",
                total_ms=elapsed_ms,
            )
            send_final_message(response)
            return

        log_cache(False, ms=int((time.time() - start) * 1000))

        # --- DEMO_MODE: cache-only, skip LLM ---
        if config.DEMO_MODE:
            elapsed_ms = int((time.time() - start) * 1000)
            log_pipeline_result(msg.request_id, msg.from_number, "fallback", elapsed_ms, fallback_reason="demo_mode")
            fallback_text = get_template("fallback_generic", language)
            response = FinalResponse(
                to_number=msg.from_number,
                body=fallback_text,
                source="fallback",
                total_ms=elapsed_ms,
            )
            send_final_message(response)
            return

        # --- IMAGE PIPELINE (Gemini vision) ---
        if msg.input_type == InputType.IMAGE and msg.media_url:
            from src.core.skills.fetch_media import fetch_media

            media_bytes = fetch_media(msg.media_url)
            if media_bytes is None:
                _send_fallback(msg, "vision_fail", start)
                return

            vision_result = analyze_image(media_bytes, msg.media_type or "image/jpeg", language=language)

            if vision_result.success and vision_result.text:
                elapsed_ms = int((time.time() - start) * 1000)
                log_pipeline_result(msg.request_id, msg.from_number, "vision", elapsed_ms)
                if ctx:
                    ctx.add_timing("vision", vision_result.duration_ms)
                    ctx.add_timing("total", elapsed_ms)
                    log_observability(ctx)
                response = FinalResponse(
                    to_number=msg.from_number,
                    body=vision_result.text,
                    source="vision",
                    total_ms=elapsed_ms,
                )
                send_final_message(response)
                return
            else:
                _send_fallback(msg, "vision_fail", start)
                return

        # --- KB LOOKUP (via retriever chain) ---
        kb_context: KBContext | None = get_retriever().retrieve(text, language)

        # --- OFFICE LOOKUP (location-specific info) ---
        from src.core.rag.territory import detect_territory
        from src.core.skills.office_lookup import office_lookup

        territory = detect_territory(text)
        office_info = None
        if territory and territory.get("municipio") and kb_context:
            office_info = office_lookup(territory["municipio"], kb_context.tramite)

        # --- BUILD MEMORY CONTEXT ---
        memory_profile_str = ""
        memory_summary_str = ""
        memory_case_str = ""
        if config.MEMORY_ENABLED and memory and memory.consent_opt_in:
            profile_parts = []
            if memory.profile_name:
                profile_parts.append(f"Nombre: {memory.profile_name}")
            if memory.profile_language:
                profile_parts.append(f"Idioma: {memory.profile_language}")
            memory_profile_str = sanitize_for_prompt(", ".join(profile_parts)) if profile_parts else ""
            memory_summary_str = sanitize_for_prompt(memory.conversation_summary)
            case_parts = []
            if memory.current_case_tramite:
                case_parts.append(f"tramite={memory.current_case_tramite}")
            if memory.current_case_intent:
                case_parts.append(f"intent={memory.current_case_intent}")
            memory_case_str = sanitize_for_prompt(", ".join(case_parts)) if case_parts else ""

        # --- CONVERSATION HISTORY ---
        from src.core.conversation_history import get_history, add_message as add_history
        history = get_history(msg.from_number)
        add_history(msg.from_number, "user", text)

        # --- LLM GENERATE ---
        llm_resp: LLMResponse = llm_generate(
            text, language, kb_context,
            memory_profile=memory_profile_str,
            memory_summary=memory_summary_str,
            memory_case=memory_case_str,
            office_info=office_info,
            conversation_history=history,
        )

        # --- VERIFY ---
        verified_text = verify_response(llm_resp.text, kb_context)

        # --- SAVE MODEL RESPONSE TO HISTORY ---
        add_history(msg.from_number, "model", verified_text)

        # --- STRUCTURED OUTPUT (optional) ---
        if config.STRUCTURED_OUTPUT_ON:
            from src.core.models_structured import parse_structured_response
            parsed, display_text = parse_structured_response(verified_text)
            if parsed:
                verified_text = display_text

        # --- GUARDRAILS POST-CHECK ---
        if config.GUARDRAILS_ON:
            from src.core.guardrails import post_check
            verified_text = post_check(verified_text)

        # --- WHATSAPP FORMATTING ---
        from src.core.skills.whatsapp_format import format_for_whatsapp
        verified_text = format_for_whatsapp(verified_text)

        # --- MEMORY UPDATE (post-response) ---
        if config.MEMORY_ENABLED and memory_store and memory and memory.consent_opt_in:
            if kb_context:
                tramite_key = kb_context.tramite
            memory = update_memory_after_response(memory, text, verified_text, tramite_key, language)
            memory_store.upsert(user_id, memory)
            log_memory(msg.request_id, user_id, config.MEMORY_BACKEND,
                        hit=True, write=True, size_bytes=len(str(memory.to_dict())),
                        latency_ms=0)

        # --- SEND TEXT IMMEDIATELY (don't wait for TTS) ---
        elapsed_ms = int((time.time() - start) * 1000)
        if llm_resp.success:
            log_pipeline_result(msg.request_id, msg.from_number, "llm", elapsed_ms)
        else:
            log_pipeline_result(msg.request_id, msg.from_number, "fallback", elapsed_ms,
                                fallback_reason=llm_resp.error or "")
        if ctx:
            ctx.add_timing("total", elapsed_ms)
            log_observability(ctx)
        response = FinalResponse(
            to_number=msg.from_number,
            body=verified_text,
            media_url=None,  # Text first, audio follows async
            source="llm" if llm_resp.success else "fallback",
            total_ms=elapsed_ms,
        )
        send_final_message(response)

        # --- TTS: generate and send audio in background ---
        _send_audio_async(msg.from_number, verified_text, language)

        # --- SCHEDULE FOLLOW-UP (5 min inactivity) ---
        _schedule_followup(msg.from_number, language)

    except Exception as e:
        log_error("pipeline", str(e))
        elapsed_ms = int((time.time() - start) * 1000)
        log_pipeline_result(msg.request_id, msg.from_number, "fallback", elapsed_ms,
                            fallback_reason="pipeline_error")
        try:
            _send_fallback(msg, "llm_fail", start)
        except Exception as fallback_err:
            log_error("pipeline_fallback", str(fallback_err))


def _send_fallback(msg: IncomingMessage, template_key: str, start: float) -> None:
    """Send a fallback response when something fails."""
    language = detect_language(msg.body, phone=msg.from_number) if msg.body else \
        detect_language("", phone=msg.from_number)
    elapsed_ms = int((time.time() - start) * 1000)
    fallback_text = get_template(template_key, language)
    response = FinalResponse(
        to_number=msg.from_number,
        body=fallback_text,
        source="fallback",
        total_ms=elapsed_ms,
    )
    send_final_message(response)
