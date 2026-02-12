"""Transcribe audio using Gemini Flash (replaces local Whisper for Render free tier)."""

import time
from src.core.models import TranscriptResult
from src.core.config import config
from src.utils.logger import log_whisper, log_error
from src.utils.timing import timed


def load_whisper_model():
    """No-op — Gemini API needs no local model."""
    pass


def get_whisper_model():
    """Return truthy value when Gemini key is available (for health check)."""
    return "gemini" if config.GEMINI_API_KEY else None


@timed("transcribe")
def transcribe(audio_bytes: bytes, mime_type: str = "audio/ogg") -> TranscriptResult:
    """Transcribe audio bytes using Gemini Flash. Returns TranscriptResult."""
    if not config.GEMINI_API_KEY:
        return TranscriptResult(
            text="", language="es", duration_ms=0,
            success=False, error="No Gemini API key"
        )

    start = time.time()
    try:
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            [
                {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": mime_type, "data": audio_bytes}},
                        {"text": (
                            "Transcribe this audio exactly as spoken. "
                            "Reply ONLY with the transcription, nothing else. "
                            "Also detect the language and prepend it as a tag like [es] or [fr]."
                        )},
                    ],
                }
            ],
            generation_config={"max_output_tokens": 300, "temperature": 0.1},
            request_options={"timeout": config.WHISPER_TIMEOUT},
        )

        elapsed = int((time.time() - start) * 1000)
        raw = response.text.strip()

        # Parse language tag [xx] if present
        language = "es"
        text = raw
        if raw.startswith("[") and "]" in raw[:5]:
            tag_end = raw.index("]")
            language = raw[1:tag_end].lower().strip()
            text = raw[tag_end + 1:].strip()

        log_whisper(True, elapsed, text)
        return TranscriptResult(
            text=text, language=language, duration_ms=elapsed, success=True
        )
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        log_whisper(False, elapsed)
        log_error("transcribe_gemini", str(e))
        return TranscriptResult(
            text="", language="es", duration_ms=elapsed,
            success=False, error=str(e)
        )
