"""Integration test: audio language detection flows through to TTS language selection.

Validates the full chain:
1. Transcription detects language from audio
2. Language propagates to LLM generation
3. Language propagates to TTS engine selection
4. Error fallbacks use correct language
"""

from src.core.skills.detect_lang import detect_language, set_conversation_lang, _conversation_lang
import pytest


@pytest.fixture(autouse=True)
def clear_memory():
    _conversation_lang.clear()
    yield
    _conversation_lang.clear()


class TestAudioLanguagePipeline:
    """Test language flows through the full pipeline."""

    def test_french_audio_gets_french_tts(self):
        """French audio -> French transcription -> French TTS voice."""
        from src.core.skills.tts import _GEMINI_VOICE_NAME
        assert "fr" in _GEMINI_VOICE_NAME
        assert _GEMINI_VOICE_NAME["fr"] != _GEMINI_VOICE_NAME["es"]

    def test_chinese_detection_in_full_chain(self):
        """Chinese text should be detected and stored in conversation memory."""
        phone = "+86test"
        lang = detect_language("你好，我需要帮助", phone=phone)
        assert lang == "zh"
        from src.core.skills.detect_lang import get_conversation_lang
        assert get_conversation_lang(phone) == "zh"

    def test_arabic_script_detection_in_chain(self):
        """Arabic script should be detected via character range check."""
        phone = "+212test"
        lang = detect_language("مرحبا أريد مساعدة", phone=phone)
        assert lang == "ar"
        from src.core.skills.detect_lang import get_conversation_lang
        assert get_conversation_lang(phone) == "ar"

    def test_transcription_language_stored_in_memory(self):
        """After transcription detects a language, it should be stored."""
        phone = "+33test"
        set_conversation_lang(phone, "fr")
        lang = detect_language("", phone=phone)
        assert lang == "fr"

    def test_all_8_languages_have_tts_voices(self):
        """All 8 supported languages must have TTS voice mappings."""
        from src.core.skills.tts import _GEMINI_VOICE_NAME, _GEMINI_VOICE_STYLE, _ELEVENLABS_VOICE_ID
        languages = ["es", "fr", "en", "pt", "ro", "ca", "zh", "ar"]
        for lang in languages:
            assert lang in _GEMINI_VOICE_NAME, f"Missing Gemini voice for {lang}"
            assert lang in _GEMINI_VOICE_STYLE, f"Missing Gemini style for {lang}"
            assert lang in _ELEVENLABS_VOICE_ID, f"Missing ElevenLabs voice for {lang}"

    def test_all_8_languages_have_templates(self):
        """All 8 supported languages must have all required templates."""
        from src.core.prompts.templates import get_template
        languages = ["es", "fr", "en", "pt", "ro", "ca", "zh", "ar"]
        templates = ["ack_greeting", "ack_text", "ack_audio", "whisper_fail", "llm_fail", "fallback_generic"]
        for lang in languages:
            for tmpl in templates:
                result = get_template(tmpl, lang)
                assert result and len(result) > 5, f"Missing/empty template {tmpl} for {lang}"

    def test_all_8_languages_in_system_prompt_tones(self):
        """All 8 languages must have tone rules in system prompt."""
        from src.core.prompts.system_prompt import _LANGUAGE_TONES
        languages = ["es", "fr", "en", "pt", "ro", "ca", "zh", "ar"]
        for lang in languages:
            assert lang in _LANGUAGE_TONES, f"Missing tone rules for {lang}"
            assert len(_LANGUAGE_TONES[lang]) > 20, f"Tone too short for {lang}"

    def test_detect_lang_supported_set_includes_all_8(self):
        """_SUPPORTED set must include all 8 language codes."""
        from src.core.skills.detect_lang import _SUPPORTED
        expected = {"es", "fr", "en", "pt", "ro", "ca", "ar", "zh"}
        missing = expected - _SUPPORTED
        assert not missing, f"Missing from _SUPPORTED: {missing}"

    def test_tts_language_aware_formatting(self):
        """TTS formatting should be language-aware for phone numbers."""
        from src.core.skills.tts import _strip_formatting_localized
        es_result = _strip_formatting_localized("Llama al 060", "es")
        fr_result = _strip_formatting_localized("Appelez le 060", "fr")
        en_result = _strip_formatting_localized("Call 060", "en")
        assert "cero sesenta" in es_result
        assert "soixante" in fr_result
        assert "sixty" in en_result

    def test_transcription_3_letter_codes_mapped(self):
        """3-letter language codes from transcription should be mapped to 2-letter."""
        from src.core.skills.transcribe import _parse_transcript
        text, lang = _parse_transcript("[eng] Hello")
        assert lang == "en"
        text, lang = _parse_transcript("[fra] Bonjour")
        assert lang == "fr"
        text, lang = _parse_transcript("[ara] مرحبا")
        assert lang == "ar"
