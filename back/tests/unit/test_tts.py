"""Tests for TTS skill — dual engine (Gemini + gTTS)."""

from unittest.mock import patch, MagicMock


def test_text_to_audio_returns_none_without_audio_base_url():
    """No AUDIO_BASE_URL = no TTS."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.AUDIO_BASE_URL = ""
        from src.core.skills.tts import text_to_audio
        assert text_to_audio("necesito ayuda con mi tramite", "es") is None


def test_text_to_audio_gtts_returns_url():
    """gTTS engine returns a URL when successful."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gtts") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gtts"
        mock_gtts.return_value = "/tmp/fake.mp3"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda con mi tramite", "es")
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
        result = text_to_audio("necesito ayuda con mi tramite", "es")
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
        result = text_to_audio("necesito ayuda con mi tramite", "es")
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
        result = text_to_audio("necesito ayuda con mi tramite", "es")
        assert result is not None


def test_synthesize_gemini_no_api_key():
    """No API key = None."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = ""
        from src.core.skills.tts import _synthesize_gemini
        assert _synthesize_gemini("hola", "es") is None


def test_gemini_voice_names_exist():
    """All 3 languages have voice names. ES uses Aoede (warm, Clara voice)."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    assert _GEMINI_VOICE_NAME["es"] == "Aoede"  # Updated: warm Clara voice
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
    """Text pre-processing adds micro-pauses and strips formatting."""
    from src.core.skills.tts import _prepare_text_for_tts
    # Parenthetical explanations get pause
    result = _prepare_text_for_tts("el padron (registro en tu ciudad)")
    assert "..." in result
    # Numbered steps are stripped for natural speech
    result = _prepare_text_for_tts("1. Tu pasaporte")
    assert "Tu pasaporte" in result
    assert not result.strip().startswith("1.")


# ---------------------------------------------------------------------------
# New tests: ElevenLabs engine, triple fallback, voice mapping, truncation
# ---------------------------------------------------------------------------


def test_elevenlabs_engine_returns_url_when_successful():
    """ElevenLabs engine returns a URL when _synthesize_elevenlabs succeeds."""
    fake_mp3 = b"\xff\xfb\x90\x00" + b"\x00" * 100  # fake MP3 bytes
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value=fake_mp3), \
         patch("os.path.exists", return_value=False), \
         patch("builtins.open", MagicMock()):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda con mi tramite", "es")
        assert result is not None
        assert result.startswith("http://localhost/cache/")
        assert result.endswith(".mp3")


def test_elevenlabs_fallback_to_gemini_then_gtts():
    """Triple fallback: elevenlabs fails -> gemini fails -> gtts succeeds."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value=None) as mock_el, \
         patch("src.core.skills.tts._synthesize_gemini", return_value=None) as mock_gem, \
         patch("src.core.skills.tts._synthesize_gtts", return_value="/tmp/f.mp3") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda con mi tramite", "es")

        # All three engines attempted in order
        mock_el.assert_called_once()
        mock_gem.assert_called_once()
        mock_gtts.assert_called_once()
        # Final result comes from gTTS
        assert result is not None
        assert result.endswith(".mp3")


def test_elevenlabs_falls_to_gemini_when_elevenlabs_fails():
    """When elevenlabs fails, Gemini is tried next and succeeds."""
    fake_wav = b"RIFF" + b"\x00" * 100
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value=None) as mock_el, \
         patch("src.core.skills.tts._synthesize_gemini", return_value=fake_wav) as mock_gem, \
         patch("os.path.exists", return_value=False), \
         patch("builtins.open", MagicMock()):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda con mi tramite", "es")

        mock_el.assert_called_once()
        mock_gem.assert_called_once()
        assert result is not None
        assert result.endswith(".wav")


def test_all_engines_failing_returns_none():
    """When all three engines fail, text_to_audio returns None."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value=None), \
         patch("src.core.skills.tts._synthesize_gemini", return_value=None), \
         patch("src.core.skills.tts._synthesize_gtts", return_value=None), \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda con mi tramite", "es")
        assert result is None


def test_voice_name_mapping_includes_es_fr_en():
    """_GEMINI_VOICE_NAME has entries for at least es, fr, en."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    for lang in ("es", "fr", "en"):
        assert lang in _GEMINI_VOICE_NAME
        assert isinstance(_GEMINI_VOICE_NAME[lang], str)
        assert len(_GEMINI_VOICE_NAME[lang]) > 0


def test_elevenlabs_voice_id_mapping_includes_es_fr_en():
    """_ELEVENLABS_VOICE_ID has entries for at least es, fr, en."""
    from src.core.skills.tts import _ELEVENLABS_VOICE_ID
    for lang in ("es", "fr", "en"):
        assert lang in _ELEVENLABS_VOICE_ID
        assert isinstance(_ELEVENLABS_VOICE_ID[lang], str)
        assert len(_ELEVENLABS_VOICE_ID[lang]) > 0


def test_truncate_for_tts_short_text_unchanged():
    """Text under _TTS_MAX_WORDS is returned unchanged."""
    from src.core.skills.tts import _truncate_for_tts
    short = "Hola, esto es una prueba corta."
    assert _truncate_for_tts(short) == short


def test_truncate_for_tts_long_text_is_cut():
    """Text longer than _TTS_MAX_WORDS is truncated."""
    from src.core.skills.tts import _truncate_for_tts, _TTS_MAX_WORDS
    # Build text with more words than the limit
    words = ["palabra"] * (_TTS_MAX_WORDS + 20)
    long_text = " ".join(words)
    result = _truncate_for_tts(long_text)
    assert len(result.split()) <= _TTS_MAX_WORDS


def test_truncate_for_tts_prefers_sentence_boundary():
    """Truncation prefers ending at a sentence boundary (period or question mark)."""
    from src.core.skills.tts import _truncate_for_tts, _TTS_MAX_WORDS
    # Build text where a period falls PAST the halfway mark of the truncated window.
    # We need >_TTS_MAX_WORDS total words, with a period well past the midpoint.
    # e.g. 35 words + period + 20 filler words  (55 total, period at word 35)
    prefix_words = ["palabra"] * (_TTS_MAX_WORDS - 10)
    suffix_words = ["extra"] * 20
    sentence = " ".join(prefix_words) + ". " + " ".join(suffix_words)
    result = _truncate_for_tts(sentence)
    # The period is past the halfway mark, so truncation should cut there
    assert result.endswith(".")


def test_synthesize_elevenlabs_no_api_key():
    """No ELEVENLABS_API_KEY means _synthesize_elevenlabs returns None."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.ELEVENLABS_API_KEY = ""
        from src.core.skills.tts import _synthesize_elevenlabs
        assert _synthesize_elevenlabs("hola", "es") is None


def test_synthesize_elevenlabs_exception_returns_none():
    """If the ElevenLabs SDK raises an exception, return None gracefully."""
    mock_client = MagicMock()
    mock_client.text_to_speech.convert.side_effect = Exception("API down")
    mock_elevenlabs_cls = MagicMock(return_value=mock_client)

    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch.dict("sys.modules", {"elevenlabs": MagicMock(ElevenLabs=mock_elevenlabs_cls)}):
        mock_cfg.ELEVENLABS_API_KEY = "fake-key"
        from src.core.skills.tts import _synthesize_elevenlabs
        # Should not raise; returns None
        assert _synthesize_elevenlabs("hola", "es") is None


# ---------------------------------------------------------------------------
# Multi-language TTS tests: voice selection, text prep, truncation per language
# ---------------------------------------------------------------------------


def test_gemini_voice_fr_is_different_from_es():
    """FR voice should be different from ES voice."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    assert _GEMINI_VOICE_NAME["fr"] != _GEMINI_VOICE_NAME["es"]


def test_gemini_voice_en_exists_and_valid():
    """EN voice should exist and be a non-empty string."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    assert "en" in _GEMINI_VOICE_NAME
    assert isinstance(_GEMINI_VOICE_NAME["en"], str)
    assert len(_GEMINI_VOICE_NAME["en"]) > 0


def test_gemini_style_es_mentions_clara():
    """ES voice style must mention Clara persona."""
    from src.core.skills.tts import _GEMINI_VOICE_STYLE
    assert "Clara" in _GEMINI_VOICE_STYLE["es"]


def test_gemini_style_fr_mentions_clara():
    """FR voice style must mention Clara persona."""
    from src.core.skills.tts import _GEMINI_VOICE_STYLE
    assert "Clara" in _GEMINI_VOICE_STYLE["fr"]


def test_gemini_style_en_mentions_clara():
    """EN voice style must mention Clara persona."""
    from src.core.skills.tts import _GEMINI_VOICE_STYLE
    assert "Clara" in _GEMINI_VOICE_STYLE["en"]


def test_elevenlabs_voice_id_es_nonempty():
    """ES ElevenLabs voice ID is a non-empty string."""
    from src.core.skills.tts import _ELEVENLABS_VOICE_ID
    assert len(_ELEVENLABS_VOICE_ID["es"]) > 5


def test_elevenlabs_voice_id_fr_nonempty():
    """FR ElevenLabs voice ID is a non-empty string."""
    from src.core.skills.tts import _ELEVENLABS_VOICE_ID
    assert len(_ELEVENLABS_VOICE_ID["fr"]) > 5


def test_elevenlabs_voice_id_en_nonempty():
    """EN ElevenLabs voice ID is a non-empty string."""
    from src.core.skills.tts import _ELEVENLABS_VOICE_ID
    assert len(_ELEVENLABS_VOICE_ID["en"]) > 5


def test_prepare_text_french_parenthetical():
    """French parenthetical explanations get micro-pause."""
    from src.core.skills.tts import _prepare_text_for_tts
    result = _prepare_text_for_tts("le padron (inscription a la mairie)")
    assert "..." in result


def test_prepare_text_portuguese_numbered_steps():
    """Portuguese numbered steps are stripped."""
    from src.core.skills.tts import _prepare_text_for_tts
    result = _prepare_text_for_tts("1. O teu passaporte")
    assert "O teu passaporte" in result
    assert not result.strip().startswith("1.")


def test_truncate_french_long_text():
    """Truncation works on French long text."""
    from src.core.skills.tts import _truncate_for_tts, _TTS_MAX_WORDS
    words = ["parole"] * (_TTS_MAX_WORDS + 20)
    long_text = " ".join(words)
    result = _truncate_for_tts(long_text)
    assert len(result.split()) <= _TTS_MAX_WORDS


def test_truncate_english_prefers_sentence_boundary():
    """Truncation on English text prefers sentence boundary."""
    from src.core.skills.tts import _truncate_for_tts, _TTS_MAX_WORDS
    prefix = ["word"] * (_TTS_MAX_WORDS - 10)
    suffix = ["extra"] * 20
    sentence = " ".join(prefix) + ". " + " ".join(suffix)
    result = _truncate_for_tts(sentence)
    assert result.endswith(".")
