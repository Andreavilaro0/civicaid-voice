"""Orchestrator: receives IncomingMessage, executes skills in order, sends response."""

import time
import os
from src.core.models import (
    IncomingMessage, InputType, FinalResponse, CacheResult,
    TranscriptResult, KBContext, LLMResponse,
)
from src.core import cache
from src.core.config import config
from src.core.skills.detect_lang import detect_language
from src.core.skills.kb_lookup import kb_lookup
from src.core.skills.llm_generate import llm_generate
from src.core.skills.verify_response import verify_response
from src.core.skills.send_response import send_final_message
from src.core.prompts.templates import get_template
from src.utils.logger import log_cache, log_error


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

    try:
        # --- AUDIO PIPELINE ---
        if msg.input_type == InputType.AUDIO and msg.media_url:
            if not config.WHISPER_ON:
                _send_fallback(msg, "whisper_fail", start)
                return

            from src.core.skills.fetch_media import fetch_media
            from src.core.skills.convert_audio import convert_ogg_to_wav
            from src.core.skills.transcribe import transcribe

            media_bytes = fetch_media(msg.media_url)
            if media_bytes is None:
                _send_fallback(msg, "whisper_fail", start)
                return

            wav_path = convert_ogg_to_wav(media_bytes)
            if wav_path is None:
                _send_fallback(msg, "whisper_fail", start)
                return

            transcript: TranscriptResult = transcribe(wav_path)
            # Clean up temp file
            try:
                os.remove(wav_path)
            except OSError:
                pass

            if not transcript.success or not transcript.text:
                _send_fallback(msg, "whisper_fail", start)
                return

            text = transcript.text
            language = transcript.language

        # --- DETECT LANGUAGE (for text input) ---
        if msg.input_type == InputType.TEXT:
            language = detect_language(text)

        # --- CACHE MATCH ---
        cache_result: CacheResult = cache.match(text, language, msg.input_type)

        if cache_result.hit and cache_result.entry:
            elapsed_ms = int((time.time() - start) * 1000)
            log_cache(True, cache_result.entry.id, elapsed_ms)
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
            fallback_text = get_template("fallback_generic", language)
            response = FinalResponse(
                to_number=msg.from_number,
                body=fallback_text,
                source="fallback",
                total_ms=elapsed_ms,
            )
            send_final_message(response)
            return

        # --- KB LOOKUP ---
        kb_context: KBContext | None = kb_lookup(text, language)

        # --- LLM GENERATE ---
        llm_resp: LLMResponse = llm_generate(text, language, kb_context)

        # --- VERIFY ---
        verified_text = verify_response(llm_resp.text, kb_context)

        # --- SEND FINAL ---
        elapsed_ms = int((time.time() - start) * 1000)
        response = FinalResponse(
            to_number=msg.from_number,
            body=verified_text,
            source="llm" if llm_resp.success else "fallback",
            total_ms=elapsed_ms,
        )
        send_final_message(response)

    except Exception as e:
        log_error("pipeline", str(e))
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
