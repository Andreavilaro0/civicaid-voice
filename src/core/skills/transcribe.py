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
    """Return truthy value when transcription is enabled and Gemini key is available."""
    if not config.WHISPER_ON:
        return None
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
        import base64
        from google import genai
        client = genai.Client(api_key=config.GEMINI_API_KEY)

        # Encode audio bytes to base64 for the new SDK
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                genai.types.Content(
                    parts=[
                        genai.types.Part(
                            inline_data=genai.types.Blob(
                                mime_type=mime_type, data=audio_b64
                            )
                        ),
                        genai.types.Part(
                            text=(
                                "Transcribe this audio exactly as spoken. "
                                "Reply ONLY with the transcription, nothing else. "
                                "Also detect the language and prepend it as a tag like [es] or [fr]."
                            )
                        ),
                    ]
                )
            ],
            config=genai.types.GenerateContentConfig(
                max_output_tokens=300, temperature=0.1,
            ),
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
