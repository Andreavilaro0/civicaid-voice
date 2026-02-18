"""MemoryStore ABC — pluggable backend interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.core.memory.models import MemoryState


class MemoryStore(ABC):
    """Abstract base for memory persistence backends."""

    @abstractmethod
    def get(self, user_id: str) -> Optional[MemoryState]:
        """Return MemoryState for user, or None if missing/expired."""

    @abstractmethod
    def upsert(self, user_id: str, state: MemoryState) -> None:
        """Create or overwrite the user's MemoryState."""

    @abstractmethod
    def forget(self, user_id: str) -> None:
        """Delete all memory for a user (right-to-forget)."""

    @abstractmethod
    def health(self) -> bool:
        """Return True if the backend is reachable."""


def get_store(backend: str = "dev", **kwargs) -> MemoryStore:
    """Factory: return a MemoryStore instance by backend name."""
    if backend == "dev":
        from src.core.memory.backends.dev import InMemoryStore
        return InMemoryStore()
    elif backend == "redis":
        from src.core.memory.backends.redis_store import RedisStore
        return RedisStore(**kwargs)
    else:
        raise ValueError(f"Unknown memory backend: {backend}")
