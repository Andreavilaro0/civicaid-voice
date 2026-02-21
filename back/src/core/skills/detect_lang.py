"""Detect language of text using langdetect with keyword hints."""

import re
from langdetect import detect, LangDetectException
from src.utils.timing import timed

# Simple per-phone-number language memory (survives within process)
_conversation_lang: dict[str, str] = {}

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

_RO_KEYWORDS = {
    "buna", "multumesc", "ajutor", "nevoie",
    "programare", "inregistrare", "vreau", "trebuie",
}

_CA_KEYWORDS = {
    "bon dia", "bona tarda", "gracies", "necessito",
    "tramit", "empadronament", "targeta", "sisplau",
}

_ZH_KEYWORDS = {
    "你好", "帮助", "需要", "谢谢", "请问", "怎么", "什么", "哪里",
}

_AR_KEYWORDS = {
    "salam", "marhaba", "shukran", "musaada", "ahlan",
}

# Supported language codes — map langdetect output to our codes
_SUPPORTED = {"es", "fr", "en", "pt", "ro", "ca", "ar"}


def _strip_punctuation(text: str) -> str:
    """Remove punctuation so 'What?' matches 'what'."""
    return re.sub(r'[^\w\s]', '', text)


def _keyword_hint(text: str) -> str | None:
    """Check for language-specific keywords. Returns lang code or None."""
    lower = _strip_punctuation(text).lower()
    words = set(lower.split())

    # Chinese detection: check for CJK characters directly
    if any('\u4e00' <= c <= '\u9fff' for c in text):
        return "zh"

    scores = {
        "es": len(words & _ES_KEYWORDS),
        "fr": len(words & _FR_KEYWORDS),
        "en": len(words & _EN_KEYWORDS),
        "pt": len(words & _PT_KEYWORDS),
        "ro": len(words & _RO_KEYWORDS),
        "ca": sum(1 for kw in _CA_KEYWORDS if kw in lower),
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


def get_conversation_lang(phone: str) -> str:
    """Get last known language for a phone number. Defaults to 'es'."""
    return _conversation_lang.get(phone, "es")


def set_conversation_lang(phone: str, lang: str) -> None:
    """Remember the detected language for a phone number."""
    _conversation_lang[phone] = lang


@timed("detect_lang")
def detect_language(text: str, phone: str = "") -> str:
    """Detect language code. Trusts langdetect for longer text, keywords for short.

    If phone is provided, remembers the language for future ACKs.
    """
    if not text or len(text.strip()) < 3:
        # No text — use conversation memory or default
        lang = get_conversation_lang(phone) if phone else "es"
        return lang

    hint = _keyword_hint(text)

    # For very short text (<30 chars), prefer keyword detection
    if hint and len(text.strip()) < 30:
        if phone:
            set_conversation_lang(phone, hint)
        return hint

    try:
        lang = detect(text)
        # Map Chinese variants to "zh"
        if lang in ("zh-cn", "zh-tw"):
            if phone:
                set_conversation_lang(phone, "zh")
            return "zh"
        # Map to supported languages (es, fr, en, pt, ro, ca, ar)
        if lang in _SUPPORTED:
            if phone:
                set_conversation_lang(phone, lang)
            return lang
        # langdetect sometimes returns "gl" (Galician) for Spanish
        if lang == "gl":
            if phone:
                set_conversation_lang(phone, "es")
            return "es"
        # For other unsupported languages, use keyword hint or default
        result = hint or "es"
        if phone:
            set_conversation_lang(phone, result)
        return result
    except LangDetectException:
        result = hint or "es"
        if phone:
            set_conversation_lang(phone, result)
        return result
