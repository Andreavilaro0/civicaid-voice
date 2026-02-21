"""Tests: language detection works on realistic questions per language.

Verifies detect_language returns correct language code for real
questions in all 8 supported languages (es, fr, en, pt, ro, ca, zh, ar).
"""

import pytest
from src.core.skills.detect_lang import detect_language, _conversation_lang


@pytest.fixture(autouse=True)
def clear_conversation_memory():
    """Reset conversation memory between tests."""
    _conversation_lang.clear()
    yield
    _conversation_lang.clear()


class TestSpanishDetection:
    """Spanish questions detected correctly."""

    CASES = [
        "Necesito ayuda con el IMV",
        "Hola, quiero información sobre el empadronamiento",
        "¿Cómo pido el padrón?",
        "Quiero pedir la tarjeta sanitaria",
        "Necesito cita previa para el médico",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_spanish(self, q):
        assert detect_language(q) == "es"


class TestFrenchDetection:
    """French questions detected correctly."""

    CASES = [
        "Bonjour, j'ai besoin d'aide pour m'inscrire",
        "Merci beaucoup pour votre aide",
        "Salut, je ne comprends pas les démarches",
        "J'ai besoin d'aide pour le NIE",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_french(self, q):
        assert detect_language(q) == "fr"


class TestEnglishDetection:
    """English questions detected correctly."""

    CASES = [
        "Hello, I need help with my registration",
        "How do I register at the town hall?",
        "I need help with my residency permit please",
        "What documents do I need for the NIE?",
        "Can you help me with the health card?",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_english(self, q):
        assert detect_language(q) == "en"


class TestPortugueseDetection:
    """Portuguese questions detected correctly."""

    CASES = [
        "Preciso de ajuda com o registo",
        "Obrigado pela ajuda",
        "Não tenho documentos, posso ir ao médico?",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_portuguese(self, q):
        assert detect_language(q) == "pt"


class TestRomanianDetection:
    """Romanian questions detected correctly."""

    CASES = [
        "Am nevoie de ajutor cu programarea",
        "Buna, vreau sa ma inregistrez",
        "Multumesc pentru ajutor",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_romanian(self, q):
        assert detect_language(q) == "ro"


class TestChineseDetection:
    """Chinese questions detected correctly (CJK character detection)."""

    CASES = [
        "我需要办理居留证",
        "如何申请最低收入保障？",
        "我需要医疗卡，怎么办？",
        "你好，我需要帮助",
        "请问怎么去市政厅登记？",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_chinese(self, q):
        assert detect_language(q) == "zh"


class TestArabicDetection:
    """Arabic questions detected via transliterated keywords."""

    CASES = [
        "salam, musaada",
        "marhaba, shukran",
        "ahlan",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_arabic(self, q):
        assert detect_language(q) == "ar"


class TestCatalanDetection:
    """Catalan questions detected correctly."""

    CASES = [
        "Necessito la targeta sanitària sisplau",
    ]

    @pytest.mark.parametrize("q", CASES)
    def test_detect_catalan(self, q):
        assert detect_language(q) == "ca"


class TestAmbiguousInputDefaultsToSpanish:
    """Short or ambiguous inputs default to Spanish."""

    AMBIGUOUS = ["IMV", "ok", "si", "1", "hola"]

    @pytest.mark.parametrize("q", AMBIGUOUS)
    def test_ambiguous_defaults_es(self, q):
        detected = detect_language(q)
        assert detected == "es", f"'{q}' should default to 'es', got '{detected}'"


class TestVeryShortTextDefaultsToSpanish:
    """Text shorter than 3 characters defaults to Spanish."""

    SHORT = ["ok", "si", "1", "no", "?"]

    @pytest.mark.parametrize("q", SHORT)
    def test_very_short_defaults_es(self, q):
        detected = detect_language(q)
        assert detected == "es"


class TestConversationMemoryPreserved:
    """Phone-based conversation memory preserves detected language."""

    def test_french_remembered(self):
        detect_language("Bonjour, j'ai besoin d'aide", phone="+33612345678")
        # Second short message should remember French
        result = detect_language("ok", phone="+33612345678")
        assert result == "fr"

    def test_english_remembered(self):
        detect_language("Hello, I need help please", phone="+44712345678")
        result = detect_language("ok", phone="+44712345678")
        assert result == "en"
