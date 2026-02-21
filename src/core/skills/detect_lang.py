"""Detect language of text using langdetect with keyword hints."""

from langdetect import detect, LangDetectException
from src.utils.timing import timed

# Only UNAMBIGUOUS keywords per language (no shared words like "como", "que")
_ES_KEYWORDS = {
    "hola", "necesito", "quiero", "gracias", "ayuda",
    "imv", "empadronamiento", "empadron", "padron", "tarjeta", "sanitaria",
    "tramite", "cita", "previa", "medico", "seguridad", "social",
    "buenas", "buenos", "noches",
}

_FR_KEYWORDS = {
    "bonjour", "salut", "merci", "besoin", "demarche",
    "mairie", "inscrire", "inscription", "domicile", "papiers",
    "oui", "non", "pourquoi", "quand",
}

_EN_KEYWORDS = {
    "hello", "hi", "hey", "help", "need", "want", "please", "thanks",
    "thank", "how", "what", "where", "when", "why", "the", "is", "are",
    "my", "can", "could", "would", "should", "about", "with",
    "registration", "appointment", "document", "benefits",
    "i", "you", "your", "do", "does", "have",
}

_PT_KEYWORDS = {
    "ola", "oi", "obrigado", "obrigada", "preciso",
    "onde", "registo", "consulta", "por favor",
    "nao", "sim", "tenho", "posso", "quero",
}

_AR_KEYWORDS = {
    "salam", "marhaba", "shukran", "musaada", "ahlan",
}

# Supported language codes — map langdetect output to our codes
_SUPPORTED = {"es", "fr", "en", "pt", "ar"}


def _keyword_hint(text: str) -> str | None:
    """Check for language-specific keywords. Returns lang code or None."""
    words = set(text.lower().split())
    scores = {
        "es": len(words & _ES_KEYWORDS),
        "fr": len(words & _FR_KEYWORDS),
        "en": len(words & _EN_KEYWORDS),
        "pt": len(words & _PT_KEYWORDS),
        "ar": len(words & _AR_KEYWORDS),
    }
    best = max(scores, key=scores.get)
    # Require at least 1 hit, and best must win by margin for short text
    if scores[best] == 0:
        return None
    # If there's a tie between es and another, don't force es
    second = sorted(scores.values(), reverse=True)[1]
    if scores[best] == second and best == "es":
        # Tie — let langdetect decide
        return None
    return best


@timed("detect_lang")
def detect_language(text: str) -> str:
    """Detect language code. Trusts langdetect for longer text, keywords for short."""
    if not text or len(text.strip()) < 3:
        return "es"

    hint = _keyword_hint(text)

    # For very short text (<30 chars), prefer keyword detection
    if hint and len(text.strip()) < 30:
        return hint

    try:
        lang = detect(text)
        # Map to supported languages
        if lang in _SUPPORTED:
            return lang
        # langdetect sometimes returns "ca" (Catalan) or "gl" (Galician) for Spanish
        if lang in ("ca", "gl"):
            return "es"
        # For other unsupported languages, use keyword hint or default
        return hint or "es"
    except LangDetectException:
        return hint or "es"
