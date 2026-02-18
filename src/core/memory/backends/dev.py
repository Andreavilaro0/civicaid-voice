"""In-memory (dict) backend — for development and testing."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from src.core.memory.models import MemoryState
from src.core.memory.store import MemoryStore


class InMemoryStore(MemoryStore):
    """Dict-backed MemoryStore. Data lives only in process memory."""

    def __init__(self) -> None:
        self._data: dict[str, str] = {}  # user_id -> JSON string

    def get(self, user_id: str) -> Optional[MemoryState]:
        raw = self._data.get(user_id)
        if raw is None:
            return None
        state = MemoryState.from_dict(json.loads(raw))
        # TTL check
        if state.expires_at:
            expires = datetime.fromisoformat(state.expires_at)
            if datetime.now(timezone.utc) > expires:
                del self._data[user_id]
                return None
        return state

    def upsert(self, user_id: str, state: MemoryState) -> None:
        self._data[user_id] = json.dumps(state.to_dict())

    def forget(self, user_id: str) -> None:
        self._data.pop(user_id, None)

    def health(self) -> bool:
        return True
