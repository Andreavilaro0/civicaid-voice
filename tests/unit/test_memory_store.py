"""Tests for MemoryStore abstraction + InMemoryStore dev backend."""

from datetime import datetime, timedelta, timezone


def test_get_miss():
    """get() returns None for unknown user."""
    from src.core.memory.backends.dev import InMemoryStore
    store = InMemoryStore()
    assert store.get("unknown_user") is None


def test_upsert_and_get():
    """upsert then get returns the same state."""
    from src.core.memory.backends.dev import InMemoryStore
    from src.core.memory.models import new_memory_state
    store = InMemoryStore()
    state = new_memory_state(ttl_days=30)
    state.profile_name = "Ana"
    store.upsert("user1", state)
    result = store.get("user1")
    assert result is not None
    assert result.profile_name == "Ana"


def test_forget():
    """forget() removes user data."""
    from src.core.memory.backends.dev import InMemoryStore
    from src.core.memory.models import new_memory_state
    store = InMemoryStore()
    store.upsert("user1", new_memory_state())
    store.forget("user1")
    assert store.get("user1") is None


def test_forget_nonexistent():
    """forget() on missing user does not raise."""
    from src.core.memory.backends.dev import InMemoryStore
    store = InMemoryStore()
    store.forget("no_such_user")  # should not raise


def test_health():
    """InMemoryStore.health() always returns True."""
    from src.core.memory.backends.dev import InMemoryStore
    store = InMemoryStore()
    assert store.health() is True


def test_ttl_expired():
    """get() returns None when memory has expired."""
    from src.core.memory.backends.dev import InMemoryStore
    from src.core.memory.models import MemoryState
    store = InMemoryStore()
    expired = MemoryState(
        updated_at=datetime.now(timezone.utc).isoformat(),
        expires_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
    )
    store.upsert("user1", expired)
    assert store.get("user1") is None


def test_isolation():
    """Different users have independent memory."""
    from src.core.memory.backends.dev import InMemoryStore
    from src.core.memory.models import new_memory_state
    store = InMemoryStore()
    s1 = new_memory_state()
    s1.profile_name = "Ana"
    s2 = new_memory_state()
    s2.profile_name = "Luis"
    store.upsert("user1", s1)
    store.upsert("user2", s2)
    assert store.get("user1").profile_name == "Ana"
    assert store.get("user2").profile_name == "Luis"
