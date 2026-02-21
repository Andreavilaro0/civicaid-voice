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
