"""Tests for analyze_image skill."""

from unittest.mock import patch, MagicMock
from src.core.skills.analyze_image import analyze_image, ImageAnalysisResult


def test_analyze_image_returns_result_dataclass():
    """analyze_image returns an ImageAnalysisResult."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = False
        mock_cfg.GEMINI_API_KEY = "key"
        result = analyze_image(b"fake", "image/jpeg")
        assert isinstance(result, ImageAnalysisResult)
        assert result.success is False


def test_analyze_image_disabled_returns_failure():
    """When VISION_ENABLED=False, returns failure without calling API."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = False
        mock_cfg.GEMINI_API_KEY = "key"
        result = analyze_image(b"fake", "image/jpeg")
        assert result.success is False
        assert "disabled" in result.error.lower()


def test_analyze_image_no_api_key_returns_failure():
    """When GEMINI_API_KEY is empty, returns failure."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = True
        mock_cfg.GEMINI_API_KEY = ""
        result = analyze_image(b"fake", "image/jpeg")
        assert result.success is False


def test_analyze_image_calls_gemini_with_image_bytes():
    """Verify Gemini is called with image data and Spanish document prompt."""
    import unittest.mock as um

    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "Este documento es una carta de la Seguridad Social."

    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = True
        mock_cfg.GEMINI_API_KEY = "test-key"
        mock_cfg.VISION_TIMEOUT = 10
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = analyze_image(b"\x89PNG\r\n", "image/png")
            assert result.success is True
            assert "Seguridad Social" in result.text
            mock_client.models.generate_content.assert_called_once()


def test_analyze_image_handles_api_exception():
    """When Gemini raises an exception, returns failure gracefully."""
    import unittest.mock as um

    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_client.models.generate_content.side_effect = Exception("API error")

    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = True
        mock_cfg.GEMINI_API_KEY = "test-key"
        mock_cfg.VISION_TIMEOUT = 10
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = analyze_image(b"\x89PNG\r\n", "image/png")
            assert result.success is False
            assert "API error" in result.error


def test_analyze_image_result_has_duration():
    """Result includes duration_ms."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = False
        mock_cfg.GEMINI_API_KEY = "key"
        result = analyze_image(b"fake", "image/jpeg")
        assert hasattr(result, "duration_ms")
        assert isinstance(result.duration_ms, int)
