"""MemoryState dataclass — canonical per-user memory schema."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone


@dataclass
class MemoryState:
    """Per-user memory blob stored by MemoryStore backends."""

    # schema
    version: int = 1

    # consent
    consent_opt_in: bool = False
    consent_set_at: str = ""

    # profile
    profile_name: str = ""
    profile_language: str = ""
    profile_locale: str = ""

    # preferences
    pref_verbosity: str = "normal"
    pref_tone: str = "friendly"
    pref_audio: bool = False

    # current case
    current_case_tramite: str = ""
    current_case_intent: str = ""
    current_case_updated_at: str = ""

    # slots
    slots: dict = field(default_factory=dict)

    # conversation summary
    conversation_summary: str = ""

    # timestamps
    updated_at: str = ""
    expires_at: str = ""

    def to_dict(self) -> dict:
        """Serialize to plain dict (JSON-safe)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> MemoryState:
        """Deserialize from dict, ignoring unknown keys."""
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})


def new_memory_state(ttl_days: int = 30) -> MemoryState:
    """Factory: create a fresh MemoryState with timestamps set."""
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=ttl_days)
    return MemoryState(
        updated_at=now.isoformat(),
        expires_at=expires.isoformat(),
    )
