"""Tests for src/core/rag/response_cache.py — memory backend, key gen, TTL, eviction."""

import time
from unittest.mock import MagicMock

from src.core.models import KBContext
from src.core.rag.response_cache import ResponseCache, _serialize, _deserialize


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_ctx(tramite: str = "imv") -> KBContext:
    return KBContext(
        tramite=tramite,
        datos={"nombre": "Ingreso Minimo Vital", "organismo": "Seg Social"},
        fuente_url="https://example.com/imv",
        verificado=True,
        chunks_used=[{"chunk_id": "c1", "score": 0.9}],
    )


def _memory_cache(**kwargs) -> ResponseCache:
    """Create a memory-only cache (no Redis)."""
    return ResponseCache(backend="memory", **kwargs)


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------

class TestCacheKeyGeneration:
    def test_same_query_same_key(self):
        k1 = ResponseCache._cache_key("que es el imv", "es")
        k2 = ResponseCache._cache_key("que es el imv", "es")
        assert k1 == k2

    def test_different_query_different_key(self):
        k1 = ResponseCache._cache_key("que es el imv", "es")
        k2 = ResponseCache._cache_key("como pedir el paro", "es")
        assert k1 != k2

    def test_different_language_different_key(self):
        k1 = ResponseCache._cache_key("que es el imv", "es")
        k2 = ResponseCache._cache_key("que es el imv", "fr")
        assert k1 != k2

    def test_key_normalized_case_insensitive(self):
        k1 = ResponseCache._cache_key("Que Es El IMV", "es")
        k2 = ResponseCache._cache_key("que es el imv", "es")
        assert k1 == k2

    def test_key_prefix(self):
        k = ResponseCache._cache_key("test", "es")
        assert k.startswith("rag:cache:")


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

class TestSerialization:
    def test_round_trip(self):
        ctx = _make_ctx()
        raw = _serialize(ctx)
        restored = _deserialize(raw)
        assert restored.tramite == ctx.tramite
        assert restored.datos == ctx.datos
        assert restored.fuente_url == ctx.fuente_url
        assert restored.verificado == ctx.verificado
        assert restored.chunks_used == ctx.chunks_used


# ---------------------------------------------------------------------------
# Memory backend: put + get
# ---------------------------------------------------------------------------

class TestMemoryBackend:
    def test_put_get_hit(self):
        cache = _memory_cache()
        ctx = _make_ctx()
        cache.put("que es el imv", "es", ctx)
        result = cache.get("que es el imv", "es")
        assert result is not None
        assert result.tramite == "imv"

    def test_get_miss(self):
        cache = _memory_cache()
        result = cache.get("something", "es")
        assert result is None

    def test_ttl_expiration(self):
        cache = _memory_cache(ttl=1)
        ctx = _make_ctx()
        cache.put("query", "es", ctx)

        # Manually expire by manipulating stored time
        key = ResponseCache._cache_key("query", "es")
        _, raw = cache._memory_cache[key]
        cache._memory_cache[key] = (time.monotonic() - 10, raw)

        result = cache.get("query", "es")
        assert result is None

    def test_lru_eviction(self):
        cache = _memory_cache(max_memory_items=2)
        cache.put("q1", "es", _make_ctx("imv"))
        cache.put("q2", "es", _make_ctx("empadronamiento"))
        cache.put("q3", "es", _make_ctx("nie_tie"))

        # q1 should have been evicted
        assert cache.get("q1", "es") is None
        assert cache.get("q2", "es") is not None
        assert cache.get("q3", "es") is not None
        assert cache._evictions >= 1


# ---------------------------------------------------------------------------
# Invalidation
# ---------------------------------------------------------------------------

class TestInvalidation:
    def test_invalidate_by_procedure_id(self):
        cache = _memory_cache()
        cache.put("q1", "es", _make_ctx("imv"))
        cache.put("q2", "es", _make_ctx("empadronamiento"))

        count = cache.invalidate("imv")
        assert count == 1
        assert cache.get("q1", "es") is None
        assert cache.get("q2", "es") is not None

    def test_invalidate_all(self):
        cache = _memory_cache()
        cache.put("q1", "es", _make_ctx("imv"))
        cache.put("q2", "es", _make_ctx("empadronamiento"))

        cache.invalidate_all()
        assert cache.get("q1", "es") is None
        assert cache.get("q2", "es") is None


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_tracking(self):
        cache = _memory_cache()
        ctx = _make_ctx()
        cache.put("q", "es", ctx)

        cache.get("q", "es")       # hit
        cache.get("miss", "es")    # miss

        stats = cache.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["backend"] == "memory"
        assert stats["size"] == 1


# ---------------------------------------------------------------------------
# Redis fallback
# ---------------------------------------------------------------------------

class TestRedisFallback:
    def test_redis_unavailable_falls_back_to_memory(self):
        cache = ResponseCache(
            backend="redis",
            redis_url="redis://nonexistent:6379",
            ttl=3600,
        )
        # Should have fallen back to memory (no _redis)
        assert cache._redis is None

        # Should still work with memory
        ctx = _make_ctx()
        cache.put("q", "es", ctx)
        result = cache.get("q", "es")
        assert result is not None
        assert result.tramite == "imv"

    def test_redis_runtime_failure_degrades(self):
        cache = _memory_cache()
        # Simulate a redis object that fails
        mock_redis = MagicMock()
        mock_redis.get.side_effect = ConnectionError("connection lost")
        cache._redis = mock_redis

        # put something in memory first
        ctx = _make_ctx()
        cache._memory_cache[ResponseCache._cache_key("q", "es")] = (
            time.monotonic(), _serialize(ctx),
        )

        # get should fail on Redis, degrade, then succeed from memory
        result = cache.get("q", "es")
        assert result is not None
        assert cache._redis is None  # degraded
