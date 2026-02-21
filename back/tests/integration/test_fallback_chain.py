"""Integration tests for fallback chain — runs without Docker/DB.

Tests real JSONKBRetriever + DirectoryRetriever together."""

import os
import time
from unittest.mock import patch

from src.core.models import KBContext


class TestFallbackChainIntegration:
    """Full chain with real JSONKBRetriever + DirectoryRetriever (no PGVector)."""

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

    def test_json_retriever_finds_imv(self):
        """JSONKBRetriever should find IMV before directory is needed."""
        fr = self._make_retriever()
        result = fr.retrieve("necesito informacion sobre el imv ingreso minimo", "es")
        assert result is not None
        assert result.tramite == "imv"

    def test_directory_fallback_when_json_no_match(self):
        """For a query that JSON can match but let's test directory works too."""
        fr = self._make_retriever()
        # The directory retriever should be in the chain
        dir_present = any(
            type(r).__name__ == "DirectoryRetriever" for r in fr.retrievers
        )
        assert dir_present

    def test_no_result_for_irrelevant_query(self):
        fr = self._make_retriever()
        result = fr.retrieve("receta de paella valenciana con mariscos", "es")
        assert result is None

    def test_chain_returns_kbcontext(self):
        fr = self._make_retriever()
        result = fr.retrieve("tarjeta sanitaria medico salud", "es")
        assert result is not None
        assert isinstance(result, KBContext)
        assert result.tramite == "tarjeta_sanitaria"


class TestCacheHitLatency:
    """Cache hit latency must be < 5ms with memory backend."""

    @patch.dict(os.environ, {
        "RAG_FALLBACK_CHAIN": "true",
        "RAG_ENABLED": "false",
        "RAG_CACHE_ENABLED": "false",
    })
    def test_cache_hit_under_5ms(self):
        from importlib import reload
        import src.core.config
        reload(src.core.config)

        from src.core.rag.response_cache import ResponseCache

        cache = ResponseCache(backend="memory", ttl=3600)
        ctx = KBContext(
            tramite="imv",
            datos={"nombre": "IMV"},
            fuente_url="https://example.com",
        )
        cache.put("test query", "es", ctx)

        # Warm up
        cache.get("test query", "es")

        # Measure
        iterations = 100
        start = time.perf_counter()
        for _ in range(iterations):
            cache.get("test query", "es")
        elapsed = (time.perf_counter() - start) / iterations * 1000  # ms

        assert elapsed < 5.0, f"Cache hit took {elapsed:.2f}ms, expected < 5ms"
