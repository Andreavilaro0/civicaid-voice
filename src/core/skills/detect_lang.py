"""Detect language of text using langdetect."""

from langdetect import detect, LangDetectException
from src.utils.timing import timed


@timed("detect_lang")
def detect_language(text: str) -> str:
    """Detect language code. Returns 'es' as fallback."""
    if not text or len(text.strip()) < 3:
        return "es"
    try:
        return detect(text)
    except LangDetectException:
        return "es"
