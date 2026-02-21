"""Tests: error and fallback templates exist and follow tone rules for all 5 languages."""

import re
import pytest
from src.core.prompts.templates import get_template, TEMPLATES


LANGUAGES = ["es", "fr", "en", "pt", "ar"]
ERROR_KEYS = ["vision_fail", "whisper_fail", "llm_fail", "fallback_generic"]


class TestErrorTemplatesExist:
    """Every error template must exist for all 5 supported languages."""

    @pytest.mark.parametrize("key", ERROR_KEYS)
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_template_exists_and_nonempty(self, key, lang):
        result = get_template(key, lang)
        assert result, f"Missing: {key}/{lang}"
        assert len(result) > 20, f"Too short: {key}/{lang} = '{result}'"


class TestErrorTemplatesOfferAlternative:
    """Error templates must offer the user an alternative action (E-V-I pattern)."""

    @pytest.mark.parametrize("key", ["vision_fail", "whisper_fail", "llm_fail"])
    def test_es_offers_alternative(self, key):
        text = get_template(key, "es")
        assert any(w in text.lower() for w in ["puedes", "intentar", "escribeme"]), \
            f"{key}/es must offer alternative"

    @pytest.mark.parametrize("key", ["vision_fail", "whisper_fail", "llm_fail"])
    def test_fr_offers_alternative(self, key):
        text = get_template(key, "fr")
        assert any(w in text.lower() for w in ["pouvez", "reessayer", "reessayez", "ecrivez"]), \
            f"{key}/fr must offer alternative"

    @pytest.mark.parametrize("key", ["vision_fail", "whisper_fail", "llm_fail"])
    def test_en_offers_alternative(self, key):
        text = get_template(key, "en")
        assert any(w in text.lower() for w in ["can", "try", "type"]), \
            f"{key}/en must offer alternative"


class TestErrorTemplatesNoEmoji:
    """ACK and error templates must NOT contain emoji (Fase 5 rule)."""

    @pytest.mark.parametrize("key", ERROR_KEYS + ["ack_text", "ack_audio", "ack_image"])
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_no_emoji(self, key, lang):
        text = get_template(key, lang)
        if not text:
            pytest.skip(f"No template for {key}/{lang}")
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U0001f900-\U0001f9FF"
            "]+", flags=re.UNICODE
        )
        assert not emoji_pattern.search(text), \
            f"Emoji found in {key}/{lang}: '{text}'"


class TestMemoryTemplatesExist:
    """Memory templates must exist for es, fr, en."""

    MEMORY_KEYS = [
        "memory_optin_ask", "memory_optin_confirmed",
        "memory_optin_declined", "memory_forgotten",
    ]

    @pytest.mark.parametrize("key", MEMORY_KEYS)
    @pytest.mark.parametrize("lang", ["es", "fr", "en"])
    def test_memory_template_exists(self, key, lang):
        result = get_template(key, lang)
        assert result, f"Missing: {key}/{lang}"
        assert len(result) > 10, f"Too short: {key}/{lang}"


class TestGetTemplateFallback:
    """get_template falls back to Spanish for unknown languages."""

    def test_unknown_lang_falls_back_to_es(self):
        es = get_template("ack_text", "es")
        xx = get_template("ack_text", "xx")
        assert xx == es

    def test_unknown_key_returns_empty(self):
        result = get_template("nonexistent_key", "es")
        assert result == ""


class TestAckTemplatesAllLanguages:
    """All ACK templates exist for all 5 languages and are non-trivial."""

    ACK_KEYS = ["ack_greeting", "ack_text", "ack_audio", "ack_image"]

    @pytest.mark.parametrize("key", ACK_KEYS)
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_ack_exists_and_long_enough(self, key, lang):
        result = get_template(key, lang)
        assert result, f"Missing: {key}/{lang}"
        assert len(result) > 15, f"Too short: {key}/{lang}"

    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_ack_greeting_mentions_clara(self, lang):
        result = get_template("ack_greeting", lang)
        assert "Clara" in result or "كلارا" in result, f"ack_greeting/{lang} should mention Clara"

    @pytest.mark.parametrize("key", ACK_KEYS)
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_ack_no_urls(self, key, lang):
        result = get_template(key, lang)
        assert "http" not in result.lower(), f"ACK {key}/{lang} should not contain URLs"


class TestClosingTemplatesAllLanguages:
    """Closing template exists for all 5 languages."""

    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_closing_exists(self, lang):
        result = get_template("closing", lang)
        assert result, f"Missing closing/{lang}"
        assert len(result) > 20

    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_closing_offers_continued_help(self, lang):
        result = get_template("closing", lang).lower()
        # Each language should offer to help again
        help_words = {
            "es": ["aqui", "duda"],
            "fr": ["la", "question"],
            "en": ["here", "anything"],
            "pt": ["aqui", "duvida"],
            "ar": ["هنا", "سؤال"],
        }
        assert any(w in result for w in help_words[lang]), \
            f"closing/{lang} should offer continued help"


class TestFrenchTemplatesUseFormal:
    """French templates must use 'vous' (formal), never 'tu'."""

    ALL_TEMPLATE_KEYS = [k for k in TEMPLATES.keys()]

    @pytest.mark.parametrize("key", ALL_TEMPLATE_KEYS)
    def test_fr_uses_vous_not_tu(self, key):
        result = get_template(key, "fr")
        if not result:
            pytest.skip(f"No FR template for {key}")
        # Check for "tu " (with space) or "tu'" to avoid matching "tout" etc.
        words = result.lower().split()
        # "tu" as standalone word is informal
        assert "tu" not in words, \
            f"{key}/fr should use 'vous', found 'tu' in: '{result}'"


class TestPortugueseTemplatesEuropean:
    """Portuguese templates should use European Portuguese forms."""

    @pytest.mark.parametrize("key", ["ack_greeting", "ack_text", "ack_audio", "ack_image"])
    def test_pt_has_european_hints(self, key):
        result = get_template(key, "pt")
        if not result:
            pytest.skip(f"No PT template for {key}")
        # European Portuguese: "podes", "Da-me", "te" (not "voce")
        eu_hints = ["podes", "da-me", "-te", "conta-me", "-me"]
        assert any(h in result.lower() for h in eu_hints), \
            f"{key}/pt should have European Portuguese forms"


class TestArabicTemplatesHaveScript:
    """Arabic templates must contain Arabic script characters."""

    AR_KEYS = ["ack_greeting", "ack_text", "ack_audio", "ack_image",
               "vision_fail", "whisper_fail", "llm_fail", "fallback_generic", "closing"]

    @pytest.mark.parametrize("key", AR_KEYS)
    def test_ar_contains_arabic_script(self, key):
        import re
        result = get_template(key, "ar")
        assert result, f"Missing: {key}/ar"
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        assert arabic_pattern.search(result), \
            f"{key}/ar should contain Arabic script characters"


class TestErrorTemplatesHaveHelpResource:
    """Error templates must include a help resource in every language."""

    ERROR_KEYS = ["vision_fail", "whisper_fail", "llm_fail"]

    @pytest.mark.parametrize("key", ERROR_KEYS)
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_error_has_help_resource(self, key, lang):
        result = get_template(key, lang)
        if not result:
            pytest.skip(f"No template for {key}/{lang}")
        # Should contain at least one help mechanism
        help_resources = ["060", "112", "administracion.gob.es", "reessay", "try", "intentar",
                          "envoyer", "enviar", "send", "escribir", "ecri", "type",
                          "tentar", "novo", "enviar",  # PT retry words
                          "إرسال", "أخرى", "المحاولة"]  # AR retry words
        assert any(r in result.lower() for r in help_resources), \
            f"{key}/{lang} should include a help resource or retry suggestion"
