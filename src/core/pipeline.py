"""Orchestrator: receives IncomingMessage, executes skills in order, sends response."""

import time
from src.core.models import (
    IncomingMessage, InputType, FinalResponse, CacheResult,
    TranscriptResult, KBContext, LLMResponse,
)
from src.core import cache
from src.core.config import config
from src.core.skills.detect_lang import detect_language
from src.core.skills.kb_lookup import kb_lookup  # noqa: F401 — kept for backward compat
from src.core.retriever import get_retriever
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
            transcript: TranscriptResult = transcribe(media_bytes, mime_type)

            if not transcript.success or not transcript.text:
                _send_fallback(msg, "whisper_fail", start)
                return

            text = transcript.text
            language = transcript.language

        # --- DETECT LANGUAGE (for text input) ---
        if msg.input_type == InputType.TEXT:
            language = detect_language(text)

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

        # --- KB LOOKUP (via retriever chain) ---
        kb_context: KBContext | None = get_retriever().retrieve(text, language)

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

        # --- LLM GENERATE ---
        llm_resp: LLMResponse = llm_generate(
            text, language, kb_context,
            memory_profile=memory_profile_str,
            memory_summary=memory_summary_str,
            memory_case=memory_case_str,
        )

        # --- VERIFY ---
        verified_text = verify_response(llm_resp.text, kb_context)

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

        # --- MEMORY UPDATE (post-response) ---
        if config.MEMORY_ENABLED and memory_store and memory and memory.consent_opt_in:
            if kb_context:
                tramite_key = kb_context.tramite
            memory = update_memory_after_response(memory, text, verified_text, tramite_key, language)
            memory_store.upsert(user_id, memory)
            log_memory(msg.request_id, user_id, config.MEMORY_BACKEND,
                        hit=True, write=True, size_bytes=len(str(memory.to_dict())),
                        latency_ms=0)

        # --- TTS: convert response to audio ---
        audio_url = None
        try:
            from src.core.skills.tts import text_to_audio
            audio_url = text_to_audio(verified_text, language)
        except Exception as tts_err:
            log_error("tts", str(tts_err))

        # --- SEND FINAL ---
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
            media_url=audio_url,
            source="llm" if llm_resp.success else "fallback",
            total_ms=elapsed_ms,
        )
        send_final_message(response)

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
    language = detect_language(msg.body) if msg.body else "es"
    elapsed_ms = int((time.time() - start) * 1000)
    fallback_text = get_template(template_key, language)
    response = FinalResponse(
        to_number=msg.from_number,
        body=fallback_text,
        source="fallback",
        total_ms=elapsed_ms,
    )
    send_final_message(response)
