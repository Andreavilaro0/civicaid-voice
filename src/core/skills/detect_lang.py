"""Detect language of text using langdetect with Spanish keyword hints."""

from langdetect import detect, LangDetectException
from src.utils.timing import timed

# Keywords that strongly indicate Spanish — covers tramites vocabulary
_ES_KEYWORDS = {
    "hola", "que", "como", "ayuda", "necesito", "quiero", "gracias",
    "imv", "empadronamiento", "empadron", "padron", "tarjeta", "sanitaria",
    "tramite", "cita", "previa", "medico", "seguridad", "social",
    "buenas", "buenos", "dias", "tardes", "noches",
}

# Keywords that strongly indicate French
_FR_KEYWORDS = {
    "bonjour", "salut", "merci", "comment", "aide", "besoin",
    "carte", "mairie", "inscrire", "inscription", "domicile",
}


def _keyword_hint(text: str) -> str | None:
    """Check for language-specific keywords. Returns lang code or None."""
    words = set(text.lower().split())
    es_hits = len(words & _ES_KEYWORDS)
    fr_hits = len(words & _FR_KEYWORDS)
    if es_hits > 0 and es_hits >= fr_hits:
        return "es"
    if fr_hits > 0 and fr_hits > es_hits:
        return "fr"
    return None


@timed("detect_lang")
def detect_language(text: str) -> str:
    """Detect language code. Uses keyword hints for short/ambiguous text."""
    if not text or len(text.strip()) < 3:
        return "es"

    # For short text (<40 chars), prefer keyword detection over langdetect
    hint = _keyword_hint(text)
    if hint and len(text.strip()) < 40:
        return hint

    try:
        lang = detect(text)
        # langdetect often confuses es with pt/it/ca — use hint as tiebreaker
        if lang in ("pt", "it", "ca", "gl") and hint == "es":
            return "es"
        return lang
    except LangDetectException:
        return hint or "es"
