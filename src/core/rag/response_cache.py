"""Response cache for RAG retrieval results.

Redis primary, in-memory LRU fallback. Transparent to caller.
Controlled by RAG_CACHE_ENABLED / RAG_CACHE_BACKEND / RAG_CACHE_TTL."""

import hashlib
import json
import logging
import time
from collections import OrderedDict
from typing import Optional

from src.core.models import KBContext

logger = logging.getLogger(__name__)


def _serialize(ctx: KBContext) -> str:
    """Serialize KBContext to JSON string."""
    return json.dumps({
        "tramite": ctx.tramite,
        "datos": ctx.datos,
        "fuente_url": ctx.fuente_url,
        "verificado": ctx.verificado,
        "chunks_used": ctx.chunks_used,
    })


def _deserialize(raw: str) -> KBContext:
    """Deserialize JSON string to KBContext."""
    d = json.loads(raw)
    return KBContext(
        tramite=d["tramite"],
        datos=d.get("datos", {}),
        fuente_url=d.get("fuente_url", ""),
        verificado=d.get("verificado", False),
        chunks_used=d.get("chunks_used", []),
    )


class ResponseCache:
    """Cache for RAG retrieval results. Redis primary, LRU fallback."""

    def __init__(
        self,
        backend: str = "redis",
        redis_url: str = "",
        ttl: int = 3600,
        max_memory_items: int = 256,
    ):
        self.backend = backend
        self.ttl = ttl
        self._redis = None
        self._memory_cache: OrderedDict = OrderedDict()
        self._max_memory = max_memory_items

        # Stats
        self._hits = 0
        self._misses = 0
        self._evictions = 0

        if backend == "redis" and redis_url:
            try:
                import redis as _redis_mod
                self._redis = _redis_mod.Redis.from_url(
                    redis_url, decode_responses=True,
                )
                self._redis.ping()
                logger.info("ResponseCache: Redis connected at %s", redis_url)
            except Exception as exc:
                logger.warning(
                    "ResponseCache: Redis unavailable (%s), falling back to memory",
                    exc,
                )
                self._redis = None

    # ------------------------------------------------------------------
    # Key generation
    # ------------------------------------------------------------------

    @staticmethod
    def _cache_key(query: str, language: str) -> str:
        """Generate cache key from normalized query + language."""
        normalized = query.strip().lower()
        digest = hashlib.sha256(f"{normalized}:{language}".encode()).hexdigest()[:16]
        return f"rag:cache:{digest}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, query: str, language: str) -> Optional[KBContext]:
        """Get cached result. Returns None on miss."""
        key = self._cache_key(query, language)

        # Try Redis first
        if self._redis:
            try:
                raw = self._redis.get(key)
                if raw is not None:
                    self._hits += 1
                    return _deserialize(raw)
            except Exception as exc:
                logger.warning("ResponseCache Redis get failed: %s", exc)
                self._redis = None  # degrade to memory

        # Memory fallback
        entry = self._memory_cache.get(key)
        if entry is not None:
            stored_time, raw = entry
            if time.monotonic() - stored_time < self.ttl:
                self._memory_cache.move_to_end(key)
                self._hits += 1
                return _deserialize(raw)
            else:
                # Expired
                del self._memory_cache[key]

        self._misses += 1
        return None

    def put(self, query: str, language: str, result: KBContext) -> None:
        """Cache a result with TTL."""
        key = self._cache_key(query, language)
        raw = _serialize(result)

        # Try Redis
        if self._redis:
            try:
                self._redis.setex(key, self.ttl, raw)
                return
            except Exception as exc:
                logger.warning("ResponseCache Redis put failed: %s", exc)
                self._redis = None

        # Memory fallback
        if key in self._memory_cache:
            self._memory_cache.move_to_end(key)
        self._memory_cache[key] = (time.monotonic(), raw)

        # Evict oldest if over limit
        while len(self._memory_cache) > self._max_memory:
            self._memory_cache.popitem(last=False)
            self._evictions += 1

    def invalidate(self, procedure_id: str) -> int:
        """Invalidate all cache entries for a procedure. Returns count removed."""
        count = 0

        # Redis: scan for matching values (no key pattern, must scan values)
        if self._redis:
            try:
                cursor = "0"
                while True:
                    cursor, keys = self._redis.scan(
                        cursor=cursor, match="rag:cache:*", count=100,
                    )
                    for k in keys:
                        raw = self._redis.get(k)
                        if raw and f'"tramite": "{procedure_id}"' in raw:
                            self._redis.delete(k)
                            count += 1
                    if cursor == 0 or cursor == "0":
                        break
            except Exception as exc:
                logger.warning("ResponseCache Redis invalidate failed: %s", exc)

        # Memory: iterate and remove matching
        to_remove = []
        for k, (_, raw) in self._memory_cache.items():
            if f'"tramite": "{procedure_id}"' in raw:
                to_remove.append(k)
        for k in to_remove:
            del self._memory_cache[k]
            count += 1

        return count

    def invalidate_all(self) -> None:
        """Clear entire cache."""
        if self._redis:
            try:
                cursor = "0"
                while True:
                    cursor, keys = self._redis.scan(
                        cursor=cursor, match="rag:cache:*", count=100,
                    )
                    if keys:
                        self._redis.delete(*keys)
                    if cursor == 0 or cursor == "0":
                        break
            except Exception as exc:
                logger.warning("ResponseCache Redis flush failed: %s", exc)

        self._memory_cache.clear()

    def stats(self) -> dict:
        """Return cache stats: hits, misses, size, backend."""
        size = len(self._memory_cache)
        if self._redis:
            try:
                cursor, keys = self._redis.scan(
                    cursor=0, match="rag:cache:*", count=1000,
                )
                size = len(keys)
            except Exception:
                pass

        return {
            "hits": self._hits,
            "misses": self._misses,
            "evictions": self._evictions,
            "size": size,
            "backend": "redis" if self._redis else "memory",
        }
