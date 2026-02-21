"""Tests: greeting detection works for all 8 languages.

Verifies is_greeting detects greetings from _GREETING_WORDS set.
Known limitation: is_greeting does not strip punctuation or accents.
"""

import pytest
from src.core.prompts.templates import is_greeting


class TestGreetingDetected:
    """Greetings that match _GREETING_WORDS are detected."""

    GREETINGS = [
        # Spanish
        "Hola",
        "Buenas",
        "buenas tardes",
        "buenas noches",
        "que tal",
        "ey",
        # French
        "Bonjour",
        "salut",
        "bonsoir",
        # English
        "Hello",
        "hi",
        "hey",
        "start",
        "help",
        # Portuguese
        "ola",
        "oi",
        "bom dia",
        # Romanian
        "Buna",
        "buna ziua",
        # Catalan
        "bon dia",
        # Chinese
        "你好",
        "nihao",
        # Arabic (transliterated)
        "salam",
        "marhaba",
        "ahlan",
        # Generic triggers
        "join",
        "empezar",
        "ayuda",
    ]

    @pytest.mark.parametrize("g", GREETINGS)
    def test_greeting_detected(self, g):
        assert is_greeting(g), f"'{g}' should be detected as greeting"


class TestNotGreeting:
    """Non-greeting messages are not detected as greetings."""

    NOT_GREETINGS = [
        "¿Cómo me empadrono?",
        "Necesito el IMV",
        "What documents do I need for the NIE application process?",
        "NIE X1234567A",
        "Quiero información sobre el desempleo y las ayudas disponibles",
        "Comment obtenir la carte de santé en Espagne pour ma famille?",
    ]

    @pytest.mark.parametrize("q", NOT_GREETINGS)
    def test_not_greeting(self, q):
        assert not is_greeting(q), f"'{q}' should NOT be a greeting"


class TestGreetingMaxWordLimit:
    """Messages with more than 4 words are never greetings."""

    LONG = [
        "hola quiero saber como pido ayuda",
        "hello I need help with the registration",
        "bonjour je veux savoir comment faire",
    ]

    @pytest.mark.parametrize("q", LONG)
    def test_long_messages_not_greeting(self, q):
        assert not is_greeting(q)


class TestGreetingPunctuationLimitation:
    """Known limitation: is_greeting does not strip punctuation."""

    PUNCTUATED = [
        "hola!",
        "Hello!",
        "Bonjour!",
        "¡Hola!",
    ]

    @pytest.mark.parametrize("g", PUNCTUATED)
    @pytest.mark.xfail(reason="is_greeting doesn't strip punctuation — known limitation")
    def test_punctuation_not_stripped(self, g):
        assert is_greeting(g)


class TestGreetingAccentLimitation:
    """Known limitation: is_greeting does not normalize accents."""

    ACCENTED = [
        "Olá",       # Portuguese with accent (set has "ola")
        "buenos días",  # Spanish with accent (set has "buenos dias")
    ]

    @pytest.mark.parametrize("g", ACCENTED)
    @pytest.mark.xfail(reason="is_greeting doesn't normalize accents — known limitation")
    def test_accents_not_normalized(self, g):
        assert is_greeting(g)


class TestGreetingCaseInsensitive:
    """Greetings are case-insensitive (lowered before checking)."""

    CASES = [
        "HOLA",
        "BONJOUR",
        "HELLO",
        "HI",
        "OLA",
    ]

    @pytest.mark.parametrize("g", CASES)
    def test_case_insensitive(self, g):
        assert is_greeting(g), f"'{g}' should match case-insensitively"
