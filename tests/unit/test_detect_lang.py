"""Test T5: Language detection."""

from src.core.skills.detect_lang import detect_language


def test_t5_detect_french():
    """T5: Detect French language."""
    result = detect_language("Bonjour, comment faire pour s'inscrire?")
    assert result == "fr"


def test_detect_spanish():
    """Detect Spanish language."""
    result = detect_language("Hola, necesito información sobre el IMV")
    assert result == "es"


def test_detect_short_text_defaults():
    """Short text defaults to Spanish."""
    result = detect_language("hi")
    assert result == "es"


def test_detect_empty_defaults():
    """Empty text defaults to Spanish."""
    result = detect_language("")
    assert result == "es"
