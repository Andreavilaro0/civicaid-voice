"""Tests for TTS skill — dual engine (Gemini + gTTS)."""

from unittest.mock import patch, MagicMock
import os


def test_text_to_audio_returns_none_without_audio_base_url():
    """No AUDIO_BASE_URL = no TTS."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.AUDIO_BASE_URL = ""
        from src.core.skills.tts import text_to_audio
        assert text_to_audio("hola", "es") is None


def test_text_to_audio_gtts_returns_url():
    """gTTS engine returns a URL when successful."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gtts") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gtts"
        mock_gtts.return_value = "/tmp/fake.mp3"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        assert result is not None
        assert result.startswith("http://localhost/cache/")
        assert result.endswith(".mp3")


def test_text_to_audio_gemini_returns_url():
    """Gemini engine returns a URL when successful."""
    fake_wav = b"RIFF" + b"\x00" * 100  # Minimal WAV-like bytes
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gemini", return_value=fake_wav), \
         patch("os.path.exists", return_value=False), \
         patch("builtins.open", MagicMock()):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gemini"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        assert result is not None
        assert result.startswith("http://localhost/cache/")
        assert result.endswith(".wav")


def test_text_to_audio_gemini_fallback_to_gtts():
    """If Gemini fails, falls back to gTTS."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gemini", return_value=None), \
         patch("src.core.skills.tts._synthesize_gtts", return_value="/tmp/f.mp3") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gemini"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        mock_gtts.assert_called_once()
        assert result is not None
        assert result.endswith(".mp3")


def test_text_to_audio_cached_file_returns_url():
    """Cached file returns URL without re-synthesizing."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("os.path.exists", return_value=True):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gtts"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        assert result is not None


def test_synthesize_gemini_no_api_key():
    """No API key = None."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = ""
        from src.core.skills.tts import _synthesize_gemini
        assert _synthesize_gemini("hola", "es") is None


def test_gemini_voice_names_exist():
    """All 3 languages have voice names. ES uses Sulafat (Warm)."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    assert _GEMINI_VOICE_NAME["es"] == "Sulafat"  # Documented as "Warm"
    assert "fr" in _GEMINI_VOICE_NAME
    assert "en" in _GEMINI_VOICE_NAME


def test_gemini_voice_styles_are_detailed():
    """All 3 languages have detailed voice style prompts with Clara persona."""
    from src.core.skills.tts import _GEMINI_VOICE_STYLE
    for lang in ("es", "fr", "en"):
        assert lang in _GEMINI_VOICE_STYLE
        assert "Clara" in _GEMINI_VOICE_STYLE[lang]
        # Style prompts should be detailed (>100 chars), not just 1 sentence
        assert len(_GEMINI_VOICE_STYLE[lang]) > 100


def test_prepare_text_for_tts():
    """Text pre-processing adds micro-pauses for natural delivery."""
    from src.core.skills.tts import _prepare_text_for_tts
    # Parenthetical explanations get pause
    result = _prepare_text_for_tts("el padron (registro en tu ciudad)")
    assert "..." in result
    # Numbered steps get pause
    result = _prepare_text_for_tts("1. Tu pasaporte")
    assert "... " in result
