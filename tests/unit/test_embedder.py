"""Tests for Gemini embedding wrapper."""

from unittest.mock import MagicMock, patch

import pytest


def _make_mock_client():
    """Create a mock genai.Client with embed_content returning 768-dim vectors."""
    mock_client = MagicMock()
    return mock_client


def _embed_response(values):
    """Create a mock embed_content response."""
    mock_embedding = MagicMock()
    mock_embedding.values = values
    mock_response = MagicMock()
    mock_response.embeddings = [mock_embedding]
    return mock_response


class TestEmbedText:
    """Tests for embed_text function."""

    @patch("src.core.rag.embedder._client")
    @patch("src.core.rag.embedder._request_timestamps")
    def test_embed_text_returns_768_floats(self, mock_timestamps, mock_client):
        mock_timestamps.__len__ = lambda self: 0
        mock_timestamps.__bool__ = lambda self: False

        mock_client.models.embed_content.return_value = _embed_response([0.1] * 768)
        from src.core.rag.embedder import embed_text

        result = embed_text("test query")
        assert len(result) == 768
        assert all(isinstance(v, float) for v in result)
        mock_client.models.embed_content.assert_called_once()

    @patch("src.core.rag.embedder._client")
    @patch("src.core.rag.embedder._request_timestamps")
    def test_embed_text_passes_correct_params(self, mock_timestamps, mock_client):
        mock_timestamps.__len__ = lambda self: 0
        mock_timestamps.__bool__ = lambda self: False

        mock_client.models.embed_content.return_value = _embed_response([0.5] * 768)
        from src.core.rag.embedder import embed_text

        embed_text("consulta sobre IMV")
        call_kwargs = mock_client.models.embed_content.call_args
        assert call_kwargs[1]["contents"] == "consulta sobre IMV" or call_kwargs.kwargs.get("contents") == "consulta sobre IMV"
        assert "model" in call_kwargs[1] or "model" in call_kwargs.kwargs

    @patch("src.core.rag.embedder._client")
    @patch("src.core.rag.embedder.time")
    @patch("src.core.rag.embedder._request_timestamps")
    def test_embed_text_retries_on_error(self, mock_timestamps, mock_time, mock_client):
        mock_timestamps.__len__ = lambda self: 0
        mock_timestamps.__bool__ = lambda self: False
        mock_time.monotonic.return_value = 100.0
        mock_time.sleep = MagicMock()

        # First call raises, second succeeds
        mock_client.models.embed_content.side_effect = [
            Exception("API rate limit"),
            _embed_response([0.2] * 768),
        ]
        from src.core.rag.embedder import embed_text

        result = embed_text("retry test")
        assert len(result) == 768
        assert mock_client.models.embed_content.call_count == 2

    @patch("src.core.rag.embedder._client")
    @patch("src.core.rag.embedder.time")
    @patch("src.core.rag.embedder._request_timestamps")
    def test_embed_text_raises_after_max_retries(self, mock_timestamps, mock_time, mock_client):
        mock_timestamps.__len__ = lambda self: 0
        mock_timestamps.__bool__ = lambda self: False
        mock_time.monotonic.return_value = 100.0
        mock_time.sleep = MagicMock()

        mock_client.models.embed_content.side_effect = Exception("persistent failure")
        from src.core.rag.embedder import embed_text

        with pytest.raises(RuntimeError, match="failed after"):
            embed_text("will fail")
        assert mock_client.models.embed_content.call_count == 3


class TestEmbedBatch:
    """Tests for embed_batch function."""

    @patch("src.core.rag.embedder._client")
    @patch("src.core.rag.embedder._request_timestamps")
    def test_embed_batch_returns_correct_count(self, mock_timestamps, mock_client):
        mock_timestamps.__len__ = lambda self: 0
        mock_timestamps.__bool__ = lambda self: False

        mock_client.models.embed_content.return_value = _embed_response([0.3] * 768)
        from src.core.rag.embedder import embed_batch

        texts = ["text one", "text two", "text three"]
        results = embed_batch(texts)
        assert len(results) == 3
        assert all(len(v) == 768 for v in results)

    @patch("src.core.rag.embedder._client")
    def test_embed_batch_empty_returns_empty(self, mock_client):
        from src.core.rag.embedder import embed_batch

        results = embed_batch([])
        assert results == []
        mock_client.models.embed_content.assert_not_called()
