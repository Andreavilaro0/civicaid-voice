"""Redis-backed MemoryStore for production use."""

from __future__ import annotations

import json
from typing import Optional

import redis

from src.core.memory.models import MemoryState
from src.core.memory.store import MemoryStore

_KEY_PREFIX = "clara:mem:"


class RedisStore(MemoryStore):
    """Redis-backed MemoryStore. Keys: clara:mem:<user_id>, JSON values, TTL via setex."""

    def __init__(self, url: str = "redis://localhost:6379/0", ttl_days: int = 30) -> None:
        self._client = redis.Redis.from_url(url, decode_responses=True)
        self._ttl_seconds = ttl_days * 86400

    def get(self, user_id: str) -> Optional[MemoryState]:
        raw = self._client.get(f"{_KEY_PREFIX}{user_id}")
        if raw is None:
            return None
        return MemoryState.from_dict(json.loads(raw))

    def upsert(self, user_id: str, state: MemoryState) -> None:
        self._client.setex(
            f"{_KEY_PREFIX}{user_id}",
            self._ttl_seconds,
            json.dumps(state.to_dict()),
        )

    def forget(self, user_id: str) -> None:
        self._client.delete(f"{_KEY_PREFIX}{user_id}")

    def health(self) -> bool:
        try:
            return self._client.ping()
        except Exception:
            return False
