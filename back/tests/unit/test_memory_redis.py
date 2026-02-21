"""Tests for RedisStore — all Redis calls are mocked."""

import json
from unittest.mock import MagicMock, patch


def _make_store():
    """Build a RedisStore with a mocked Redis client."""
    with patch("redis.Redis.from_url") as mock_from_url:
        mock_client = MagicMock()
        mock_from_url.return_value = mock_client
        from src.core.memory.backends.redis_store import RedisStore
        store = RedisStore(url="redis://fake:6379/0", ttl_days=30)
    return store, mock_client


def test_get_miss():
    """get() returns None when key is absent."""
    store, mock_client = _make_store()
    mock_client.get.return_value = None
    assert store.get("user1") is None
    mock_client.get.assert_called_once_with("clara:mem:user1")


def test_get_hit():
    """get() deserializes stored JSON into MemoryState."""
    from src.core.memory.models import new_memory_state
    store, mock_client = _make_store()
    state = new_memory_state()
    state.profile_name = "Ana"
    mock_client.get.return_value = json.dumps(state.to_dict())
    result = store.get("user1")
    assert result is not None
    assert result.profile_name == "Ana"


def test_upsert_calls_setex():
    """upsert() calls setex with correct key, TTL, and JSON."""
    from src.core.memory.models import new_memory_state
    store, mock_client = _make_store()
    state = new_memory_state()
    store.upsert("user1", state)
    mock_client.setex.assert_called_once()
    args = mock_client.setex.call_args
    assert args[0][0] == "clara:mem:user1"
    assert args[0][1] == 30 * 86400
    parsed = json.loads(args[0][2])
    assert parsed["version"] == 1


def test_forget_calls_delete():
    """forget() calls delete on the correct key."""
    store, mock_client = _make_store()
    store.forget("user1")
    mock_client.delete.assert_called_once_with("clara:mem:user1")


def test_health_ok():
    """health() returns True when ping succeeds."""
    store, mock_client = _make_store()
    mock_client.ping.return_value = True
    assert store.health() is True


def test_health_fail():
    """health() returns False when ping raises."""
    store, mock_client = _make_store()
    mock_client.ping.side_effect = ConnectionError("down")
    assert store.health() is False
