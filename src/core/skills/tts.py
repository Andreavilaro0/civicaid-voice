"""Text-to-Speech using gTTS — convert LLM response to MP3 for WhatsApp audio."""

import hashlib
import os
from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "cache")


@timed("tts")
def text_to_audio(text: str, language: str = "es") -> str | None:
    """Convert text to MP3 using gTTS. Returns public URL or None on failure."""
    if not config.AUDIO_BASE_URL:
        return None

    # Map language codes to gTTS-compatible codes
    lang_map = {"es": "es", "fr": "fr", "en": "en"}
    tts_lang = lang_map.get(language, "es")

    # Deterministic filename based on content hash (avoids duplicates)
    text_hash = hashlib.md5(f"{text}:{tts_lang}".encode()).hexdigest()[:12]
    filename = f"tts_{text_hash}.mp3"
    filepath = os.path.join(_CACHE_DIR, filename)

    # Return cached file if it already exists
    if os.path.exists(filepath):
        return f"{config.AUDIO_BASE_URL.rstrip('/')}/{filename}"

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        tts.save(filepath)
        return f"{config.AUDIO_BASE_URL.rstrip('/')}/{filename}"
    except Exception as e:
        log_error("tts", str(e))
        return None
