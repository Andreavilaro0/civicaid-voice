"""Transcribe audio using Gemini Flash (replaces local Whisper for Render free tier).

Improvements (2026-02-23):
- Enhanced prompt with noise/accent context for vulnerable populations
- MIME type normalization (WhatsApp sends "audio/ogg; codecs=opus")
- Retry with superior model on first failure
- Higher token limit for longer voice messages
- Domain-aware transcription (trámites, ayudas sociales)
"""

import time
from src.core.models import TranscriptResult
from src.core.config import config
from src.utils.logger import log_whisper, log_error
from src.utils.timing import timed

# ── MIME normalization map ──
# WhatsApp and browsers send compound MIME types that Gemini may not recognize.
_MIME_NORMALIZE = {
    "audio/ogg; codecs=opus": "audio/ogg",
    "audio/ogg;codecs=opus": "audio/ogg",
    "audio/webm;codecs=opus": "audio/webm",
    "audio/webm; codecs=opus": "audio/webm",
    "audio/mp4; codecs=opus": "audio/mp4",
    "audio/mp4;codecs=opus": "audio/mp4",
    "audio/mpeg": "audio/mpeg",
    "audio/amr": "audio/amr",
}

# ── Transcription prompt ──
# Context-rich prompt handles: accents, background noise, mixed languages, trámites vocabulary.
_TRANSCRIPTION_PROMPT = (
    "You are a transcription assistant for a social services helpline in Spain. "
    "The callers are often immigrants or vulnerable people who may speak with strong accents "
    "(Latin American, North African, Sub-Saharan, Eastern European, Chinese) "
    "or mix languages (Spanish + French, Spanish + Arabic, Spanish + Portuguese, Spanish + Romanian). "
    "Common topics include: IMV (Ingreso Mínimo Vital), empadronamiento, tarjeta sanitaria, "
    "NIE, TIE, asilo, refugio, ayudas sociales, Seguridad Social, padrón, cita previa.\n\n"
    "INSTRUCTIONS:\n"
    "1. Transcribe the audio EXACTLY as spoken, preserving the original words even if grammar is imperfect.\n"
    "2. If the audio has background noise, do your best to extract the speech.\n"
    "3. Detect the primary language spoken and prepend it as a tag: [es], [fr], [ar], [pt], [ro], [zh], [en], [ca].\n"
    "4. If the speaker mixes languages, use the DOMINANT language as the tag.\n"
    "5. Reply ONLY with the language tag followed by the transcription. Nothing else.\n"
    "6. If you truly cannot understand ANY words, respond with: [unknown]\n\n"
    "Example outputs:\n"
    "[es] Hola, necesito ayuda con el empadronamiento\n"
    "[fr] Bonjour, je voudrais savoir comment obtenir la carte sanitaire\n"
    "[ar] مرحبا، أريد معلومات عن الإقامة"
)

# Map 3-letter ISO 639-2 codes to our 2-letter codes
_LANG_3_TO_2 = {
    "eng": "en", "fra": "fr", "spa": "es", "por": "pt",
    "ron": "ro", "cat": "ca", "zho": "zh", "ara": "ar",
    "chi": "zh", "fre": "fr",  # ISO 639-2 bibliographic variants
}

# ── Models: primary (fast) and fallback (stronger for difficult audio) ──
_PRIMARY_MODEL = "gemini-2.0-flash"
_FALLBACK_MODEL = "gemini-2.5-flash"


def _normalize_mime(mime_type: str) -> str:
    """Normalize compound MIME types to base MIME type Gemini accepts."""
    normalized = _MIME_NORMALIZE.get(mime_type)
    if normalized:
        return normalized
    # Strip anything after semicolon as fallback
    if ";" in mime_type:
        return mime_type.split(";")[0].strip()
    return mime_type


def load_whisper_model():
    """No-op — Gemini API needs no local model."""
    pass


def get_whisper_model():
    """Return truthy value when transcription is enabled and Gemini key is available."""
    if not config.WHISPER_ON:
        return None
    return "gemini" if config.GEMINI_API_KEY else None


def _call_gemini(audio_b64: str, mime_type: str, model: str) -> str:
    """Call Gemini with audio and return raw text response."""
    from google import genai
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=model,
        contents=[
            genai.types.Content(
                parts=[
                    genai.types.Part(
                        inline_data=genai.types.Blob(
                            mime_type=mime_type, data=audio_b64
                        )
                    ),
                    genai.types.Part(text=_TRANSCRIPTION_PROMPT),
                ]
            )
        ],
        config=genai.types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.2,
        ),
    )
    return response.text.strip()


def _parse_transcript(raw: str) -> tuple[str, str]:
    """Parse language tag and text from raw Gemini output.

    Returns (text, language). Handles:
    - [es] Hola mundo
    - [unknown]
    - Plain text without tag
    """
    if raw == "[unknown]" or raw.startswith("[unknown]"):
        return "", "unknown"

    if raw.startswith("[") and "]" in raw[:6]:
        tag_end = raw.index("]")
        language = raw[1:tag_end].lower().strip()
        text = raw[tag_end + 1:].strip()
        # Validate language tag is reasonable (2-3 chars)
        if len(language) <= 3 and language.isalpha():
            # Map 3-letter codes to 2-letter
            language = _LANG_3_TO_2.get(language, language)
            return text, language

    # No valid tag found — assume Spanish
    return raw, "es"


@timed("transcribe")
def transcribe(audio_bytes: bytes, mime_type: str = "audio/ogg") -> TranscriptResult:
    """Transcribe audio bytes using Gemini Flash with retry on failure.

    Pipeline:
    1. Normalize MIME type
    2. Try primary model (gemini-2.0-flash — fast)
    3. On failure or empty result, retry with fallback model (gemini-2.5-flash — stronger)
    4. Parse language tag and return TranscriptResult
    """
    if not config.GEMINI_API_KEY:
        return TranscriptResult(
            text="", language="es", duration_ms=0,
            success=False, error="No Gemini API key"
        )

    start = time.time()
    mime_type = _normalize_mime(mime_type)

    try:
        import base64
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        # ── Attempt 1: Primary model (fast) ──
        raw = ""
        try:
            raw = _call_gemini(audio_b64, mime_type, _PRIMARY_MODEL)
        except Exception as e1:
            log_error("transcribe_primary", f"{_PRIMARY_MODEL}: {e1}")

        text, language = _parse_transcript(raw)

        # ── Attempt 2: Fallback model if primary failed or returned empty ──
        if not text or language == "unknown":
            try:
                raw_fallback = _call_gemini(audio_b64, mime_type, _FALLBACK_MODEL)
                text_fb, lang_fb = _parse_transcript(raw_fallback)
                if text_fb:
                    text = text_fb
                    language = lang_fb
                    log_whisper(True, 0, f"[fallback:{_FALLBACK_MODEL}] {text[:50]}")
            except Exception as e2:
                log_error("transcribe_fallback", f"{_FALLBACK_MODEL}: {e2}")

        elapsed = int((time.time() - start) * 1000)

        if not text:
            log_whisper(False, elapsed)
            return TranscriptResult(
                text="", language="es", duration_ms=elapsed,
                success=False, error="Could not transcribe audio"
            )

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
