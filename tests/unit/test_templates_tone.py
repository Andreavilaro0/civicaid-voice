"""Tests: templates match Clara E-V-I tone."""

from src.core.prompts.templates import get_template, TEMPLATES


def test_all_templates_have_es_fr_en():
    """Every template key has ES, FR, and EN versions."""
    for key, langs in TEMPLATES.items():
        assert "es" in langs, f"{key} missing 'es'"
        assert "fr" in langs, f"{key} missing 'fr'"
        assert "en" in langs, f"{key} missing 'en'"


def test_error_templates_offer_alternative():
    """Error templates should always offer an alternative action."""
    error_keys = ["vision_fail", "whisper_fail", "llm_fail"]
    for key in error_keys:
        es = get_template(key, "es")
        assert any(word in es.lower() for word in ["puedes", "intentar", "alternativa"]), \
            f"{key}/es should offer alternative"


def test_ack_templates_not_empty():
    """ACK templates should be non-empty for all languages."""
    ack_keys = ["ack_text", "ack_audio", "ack_image"]
    for key in ack_keys:
        for lang in ["es", "fr", "en"]:
            val = get_template(key, lang)
            assert len(val) > 5, f"{key}/{lang} is too short or empty"


def test_closing_template_is_warm():
    """Closing template should feel warm and encouraging."""
    es = get_template("closing", "es")
    assert "suerte" in es.lower() or "animo" in es.lower() or "mucho" in es.lower()
