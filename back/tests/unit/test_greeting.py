"""Tests for is_greeting() — edge cases and all 5 languages."""

import pytest
from src.core.prompts.templates import is_greeting


class TestGreetingBasic:
    """Basic greeting detection per language."""

    @pytest.mark.parametrize("text", ["Hola", "hola", "buenas", "que tal"])
    def test_es_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["Bonjour", "bonjour", "salut"])
    def test_fr_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["Hello", "hello", "hi", "hey", "help"])
    def test_en_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["Ola", "ola", "oi"])
    def test_pt_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["salam", "marhaba", "ahlan"])
    def test_ar_greetings(self, text):
        assert is_greeting(text)


class TestGreetingPunctuation:
    """Greetings with punctuation — documents known limitation."""

    @pytest.mark.parametrize("text", ["Hola!", "Hello?", "Bonjour!"])
    @pytest.mark.xfail(reason="is_greeting doesn't strip punctuation — known limitation")
    def test_punctuation_not_stripped(self, text):
        assert is_greeting(text)


class TestGreetingNonGreeting:
    """Non-greeting messages should NOT be detected as greetings."""

    @pytest.mark.parametrize("text", [
        "Necesito informacion sobre el IMV",
        "Que documentos necesito para el empadronamiento",
        "Como pedir cita previa",
        "NIE X1234567A",
    ])
    def test_not_greetings(self, text):
        assert not is_greeting(text)


class TestGreetingEdgeCases:
    """Edge cases for greeting detection."""

    def test_empty_string(self):
        assert not is_greeting("")

    def test_whitespace_only(self):
        assert not is_greeting("   ")

    def test_long_message_not_greeting(self):
        """Long message (>4 words) containing 'hola' is NOT a greeting."""
        assert not is_greeting("Hola necesito mucha ayuda con mis tramites urgentes")

    def test_four_word_with_greeting(self):
        """4-word message with greeting word IS a greeting."""
        assert is_greeting("Hola necesito ayuda urgente")

    def test_start_keyword(self):
        """'start' is a WhatsApp join keyword, treated as greeting."""
        assert is_greeting("start")

    def test_join_keyword(self):
        """'join' is a WhatsApp keyword, treated as greeting."""
        assert is_greeting("join")
