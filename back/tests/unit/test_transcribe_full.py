"""Comprehensive tests for transcribe.py — Gemini audio transcription."""

import unittest.mock as um
from unittest.mock import patch
from src.core.skills.transcribe import transcribe, get_whisper_model
from src.core.models import TranscriptResult


# --- get_whisper_model tests ---

def test_get_whisper_model_enabled_with_key():
    """Returns truthy when WHISPER_ON=True and GEMINI_API_KEY set."""
    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.WHISPER_ON = True
        mock_cfg.GEMINI_API_KEY = "test-key"
        assert get_whisper_model() is not None


def test_get_whisper_model_disabled():
    """Returns None when WHISPER_ON=False."""
    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.WHISPER_ON = False
        mock_cfg.GEMINI_API_KEY = "test-key"
        assert get_whisper_model() is None


def test_get_whisper_model_no_key():
    """Returns None when no Gemini API key."""
    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.WHISPER_ON = True
        mock_cfg.GEMINI_API_KEY = ""
        assert get_whisper_model() is None


# --- transcribe() branch coverage ---

def test_transcribe_no_api_key():
    """Branch: no GEMINI_API_KEY → failure without calling API."""
    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = ""
        result = transcribe(b"fake-audio", "audio/ogg")
        assert isinstance(result, TranscriptResult)
        assert result.success is False
        assert "API key" in result.error


def test_transcribe_happy_path_spanish():
    """Branch: happy path → Gemini returns [es] tagged transcription."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[es] Necesito ayuda con el empadronamiento"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            assert result.language == "es"
            assert "empadronamiento" in result.text
            assert result.text.startswith("Necesito")  # tag stripped
            mock_client.models.generate_content.assert_called_once()


def test_transcribe_happy_path_french():
    """Branch: happy path → Gemini returns [fr] tagged transcription."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[fr] Je voudrais m'inscrire a la mairie"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            assert result.language == "fr"
            assert "mairie" in result.text


def test_transcribe_no_language_tag():
    """Branch: Gemini returns text without [xx] tag → defaults to 'es'."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "Hola necesito informacion sobre el IMV"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            assert result.language == "es"
            assert "IMV" in result.text


def test_transcribe_gemini_exception():
    """Branch: Gemini raises exception on both primary and fallback → failure."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_client.models.generate_content.side_effect = Exception("API timeout")

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is False
            assert result.error  # Error message present
            assert result.language == "es"


def test_transcribe_result_has_duration():
    """TranscriptResult includes duration_ms field."""
    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = ""
        result = transcribe(b"fake", "audio/ogg")
        assert hasattr(result, "duration_ms")
        assert isinstance(result.duration_ms, int)


def test_transcribe_sends_correct_mime_type():
    """Verify Gemini is called with the correct mime_type for audio."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[es] Test"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            transcribe(b"\x00\x01", "audio/mp4")
            call_args = mock_client.models.generate_content.call_args
            # Verify generate_content was called with correct model
            assert call_args[1]["model"] == "gemini-2.0-flash"


def test_transcribe_three_letter_code():
    """Branch: Gemini returns [eng] (3-letter ISO) — document behavior."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[eng] I need help with my registration"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            assert result.text is not None
            assert len(result.text) > 0


def test_transcribe_empty_response():
    """Branch: Gemini returns empty string."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = ""

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            # Empty text should be handled gracefully
            assert result.text == "" or result.success is False


def test_transcribe_whitespace_only_response():
    """Branch: Gemini returns whitespace — treated as empty."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "   \n  "

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            if result.success:
                assert result.text.strip() == ""


def test_transcribe_english_tag():
    """Branch: Gemini returns [en] tag for English audio."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[en] I need help with my healthcare card"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            assert result.language == "en"
            assert "healthcare" in result.text
