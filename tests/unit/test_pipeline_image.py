"""Tests for IMAGE branch in pipeline."""

from unittest.mock import patch, MagicMock
from src.core.models import IncomingMessage, InputType


def _make_image_msg():
    return IncomingMessage(
        from_number="whatsapp:+34600000000",
        body="",
        media_url="https://api.twilio.com/image.jpg",
        media_type="image/jpeg",
        input_type=InputType.IMAGE,
    )


def test_pipeline_image_calls_analyze_image():
    """When input_type=IMAGE, pipeline calls analyze_image."""
    mock_fetch = MagicMock(return_value=b"\x89PNG")
    mock_send = MagicMock()

    from src.core.skills.analyze_image import ImageAnalysisResult
    mock_analyze = MagicMock(return_value=ImageAnalysisResult(
        text="Es una carta de la Seguridad Social.",
        duration_ms=500,
        success=True,
    ))

    with patch("src.core.pipeline.config") as mock_cfg, \
         patch("src.core.pipeline.send_final_message", mock_send), \
         patch("src.core.skills.fetch_media.fetch_media", mock_fetch), \
         patch("src.core.pipeline.analyze_image", mock_analyze), \
         patch("src.core.pipeline.cache") as mock_cache, \
         patch("src.core.pipeline.get_context", return_value=None):

        mock_cfg.GUARDRAILS_ON = False
        mock_cfg.DEMO_MODE = False
        mock_cfg.MEMORY_ENABLED = False
        mock_cfg.OBSERVABILITY_ON = False
        mock_cfg.VISION_ENABLED = True
        mock_cfg.AUDIO_BASE_URL = ""

        mock_cache.match.return_value = MagicMock(hit=False)

        from src.core import pipeline
        pipeline.process(_make_image_msg())

        mock_analyze.assert_called_once()
        mock_send.assert_called_once()
        sent = mock_send.call_args[0][0]
        assert "Seguridad Social" in sent.body


def test_pipeline_image_falls_back_on_vision_failure():
    """When vision fails, pipeline sends vision_fail template."""
    mock_fetch = MagicMock(return_value=b"\x89PNG")
    mock_send = MagicMock()

    from src.core.skills.analyze_image import ImageAnalysisResult
    mock_analyze = MagicMock(return_value=ImageAnalysisResult(
        text="", duration_ms=500, success=False, error="API error"
    ))

    with patch("src.core.pipeline.config") as mock_cfg, \
         patch("src.core.pipeline.send_final_message", mock_send), \
         patch("src.core.skills.fetch_media.fetch_media", mock_fetch), \
         patch("src.core.pipeline.analyze_image", mock_analyze), \
         patch("src.core.pipeline.cache") as mock_cache, \
         patch("src.core.pipeline.get_context", return_value=None):

        mock_cfg.GUARDRAILS_ON = False
        mock_cfg.DEMO_MODE = False
        mock_cfg.MEMORY_ENABLED = False
        mock_cfg.OBSERVABILITY_ON = False
        mock_cfg.VISION_ENABLED = True
        mock_cfg.AUDIO_BASE_URL = ""

        mock_cache.match.return_value = MagicMock(hit=False)

        from src.core import pipeline
        pipeline.process(_make_image_msg())

        mock_send.assert_called_once()
        sent = mock_send.call_args[0][0]
        assert sent.source == "fallback"


def test_pipeline_image_cache_hit_skips_vision():
    """If image matches demo cache, vision is NOT called."""
    mock_send = MagicMock()
    mock_analyze = MagicMock()

    mock_entry = MagicMock()
    mock_entry.respuesta = "Demo image response"
    mock_entry.audio_file = None
    mock_entry.id = "demo"
    mock_cache_result = MagicMock(hit=True, entry=mock_entry)

    with patch("src.core.pipeline.config") as mock_cfg, \
         patch("src.core.pipeline.send_final_message", mock_send), \
         patch("src.core.pipeline.analyze_image", mock_analyze), \
         patch("src.core.pipeline.cache") as mock_cache, \
         patch("src.core.pipeline.get_context", return_value=None):

        mock_cfg.GUARDRAILS_ON = False
        mock_cfg.DEMO_MODE = False
        mock_cfg.MEMORY_ENABLED = False
        mock_cfg.OBSERVABILITY_ON = False
        mock_cfg.AUDIO_BASE_URL = ""

        mock_cache.match.return_value = mock_cache_result

        from src.core import pipeline
        pipeline.process(_make_image_msg())

        mock_analyze.assert_not_called()
        mock_send.assert_called_once()
