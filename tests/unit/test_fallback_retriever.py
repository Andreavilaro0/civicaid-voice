"""Tests for FallbackRetriever in src/core/retriever.py."""

import os
from unittest.mock import MagicMock, patch

from src.core.models import KBContext


def _make_ctx(tramite: str = "imv") -> KBContext:
    return KBContext(
        tramite=tramite,
        datos={"nombre": "Test"},
        fuente_url="https://example.com",
        verificado=True,
    )


# ---------------------------------------------------------------------------
# FallbackRetriever with mocked retrievers
# ---------------------------------------------------------------------------

class TestFallbackRetrieverChain:
    """Test fallback chain with all retrievers mocked."""

    @patch.dict(os.environ, {
        "RAG_FALLBACK_CHAIN": "true",
        "RAG_ENABLED": "false",
        "RAG_CACHE_ENABLED": "false",
    })
    def _make_retriever(self):
        """Build FallbackRetriever with patched config."""
        # Must reimport to pick up patched env
        from importlib import reload
        import src.core.config
        reload(src.core.config)
        from src.core.retriever import FallbackRetriever
        return FallbackRetriever()

    def test_first_retriever_succeeds(self):
        fr = self._make_retriever()
        # Replace retrievers with mocks
        mock1 = MagicMock()
        mock1.retrieve.return_value = _make_ctx("imv")
        mock2 = MagicMock()
        fr.retrievers = [mock1, mock2]

        result = fr.retrieve("que es el imv", "es")
        assert result is not None
        assert result.tramite == "imv"
        mock2.retrieve.assert_not_called()

    def test_fallback_first_fails_second_succeeds(self):
        fr = self._make_retriever()
        mock1 = MagicMock()
        mock1.retrieve.return_value = None
        mock2 = MagicMock()
        mock2.retrieve.return_value = _make_ctx("empadronamiento")
        mock3 = MagicMock()
        fr.retrievers = [mock1, mock2, mock3]

        result = fr.retrieve("padron", "es")
        assert result is not None
        assert result.tramite == "empadronamiento"
        mock3.retrieve.assert_not_called()

    def test_fallback_first_two_fail_directory_succeeds(self):
        fr = self._make_retriever()
        mock1 = MagicMock()
        mock1.retrieve.return_value = None
        mock2 = MagicMock()
        mock2.retrieve.return_value = None
        mock3 = MagicMock()
        mock3.retrieve.return_value = _make_ctx("nie_tie")
        fr.retrievers = [mock1, mock2, mock3]

        result = fr.retrieve("nie", "es")
        assert result is not None
        assert result.tramite == "nie_tie"

    def test_all_retrievers_fail_returns_none(self):
        fr = self._make_retriever()
        mock1 = MagicMock()
        mock1.retrieve.return_value = None
        mock2 = MagicMock()
        mock2.retrieve.return_value = None
        fr.retrievers = [mock1, mock2]

        result = fr.retrieve("receta tortilla", "es")
        assert result is None

    def test_retriever_exception_continues_chain(self):
        fr = self._make_retriever()
        mock1 = MagicMock()
        mock1.retrieve.side_effect = RuntimeError("DB down")
        mock2 = MagicMock()
        mock2.retrieve.return_value = _make_ctx("imv")
        fr.retrievers = [mock1, mock2]

        result = fr.retrieve("imv", "es")
        assert result is not None
        assert result.tramite == "imv"


# ---------------------------------------------------------------------------
# Cache integration
# ---------------------------------------------------------------------------

class TestFallbackRetrieverCache:

    @patch.dict(os.environ, {
        "RAG_FALLBACK_CHAIN": "true",
        "RAG_ENABLED": "false",
        "RAG_CACHE_ENABLED": "false",
    })
    def _make_retriever(self):
        from importlib import reload
        import src.core.config
        reload(src.core.config)
        from src.core.retriever import FallbackRetriever
        return FallbackRetriever()

    def test_cache_hit_on_second_call(self):
        fr = self._make_retriever()
        # Add a mock cache
        from src.core.rag.response_cache import ResponseCache
        fr.cache = ResponseCache(backend="memory", ttl=3600)

        mock_ret = MagicMock()
        mock_ret.retrieve.return_value = _make_ctx("imv")
        fr.retrievers = [mock_ret]

        # First call — miss, hits retriever
        r1 = fr.retrieve("imv query", "es")
        assert r1 is not None
        assert mock_ret.retrieve.call_count == 1

        # Second call — cache hit, no retriever call
        r2 = fr.retrieve("imv query", "es")
        assert r2 is not None
        assert mock_ret.retrieve.call_count == 1  # still 1

    def test_cache_disabled_no_caching(self):
        fr = self._make_retriever()
        assert fr.cache is None  # RAG_CACHE_ENABLED=false

        mock_ret = MagicMock()
        mock_ret.retrieve.return_value = _make_ctx("imv")
        fr.retrievers = [mock_ret]

        fr.retrieve("q", "es")
        fr.retrieve("q", "es")
        assert mock_ret.retrieve.call_count == 2


# ---------------------------------------------------------------------------
# get_retriever factory
# ---------------------------------------------------------------------------

class TestGetRetrieverFactory:

    @patch.dict(os.environ, {
        "RAG_FALLBACK_CHAIN": "false",
        "RAG_ENABLED": "false",
    })
    def test_fallback_chain_disabled_returns_json(self):
        from importlib import reload
        import src.core.config
        reload(src.core.config)
        from src.core.retriever import get_retriever, reset_retriever, JSONKBRetriever
        reset_retriever()
        r = get_retriever()
        reset_retriever()
        assert isinstance(r, JSONKBRetriever)

    @patch.dict(os.environ, {
        "RAG_FALLBACK_CHAIN": "true",
        "RAG_ENABLED": "false",
        "RAG_CACHE_ENABLED": "false",
    })
    def test_fallback_chain_enabled_returns_fallback(self):
        from importlib import reload
        import src.core.config
        reload(src.core.config)
        from src.core.retriever import get_retriever, reset_retriever, FallbackRetriever
        reset_retriever()
        r = get_retriever()
        reset_retriever()
        assert isinstance(r, FallbackRetriever)

    @patch.dict(os.environ, {
        "RAG_FALLBACK_CHAIN": "true",
        "RAG_ENABLED": "true",
        "RAG_DB_URL": "postgresql://fake",
        "RAG_CACHE_ENABLED": "false",
    })
    def test_pgvector_init_failure_graceful(self):
        """If PGVector fails to init, chain still works via JSON + Directory."""
        from importlib import reload
        import src.core.config
        reload(src.core.config)
        from src.core.retriever import FallbackRetriever

        fr = FallbackRetriever()
        # PGVector should have failed (no real DB), chain should have JSON + Directory
        type_names = [type(r).__name__ for r in fr.retrievers]
        assert "JSONKBRetriever" in type_names
        assert "DirectoryRetriever" in type_names
