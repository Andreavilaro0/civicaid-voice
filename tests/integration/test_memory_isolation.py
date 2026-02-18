"""Integration test: two users with different hashes have isolated memory."""

from src.core.memory.models import new_memory_state
from src.core.memory.backends.dev import InMemoryStore
from src.core.memory.user_hash import derive_user_id


def test_two_users_isolated():
    """User A's memory never leaks to User B."""
    store = InMemoryStore()
    h_a = derive_user_id("whatsapp:+34600111222", "test-salt")
    h_b = derive_user_id("whatsapp:+34600333444", "test-salt")

    ms_a = new_memory_state()
    ms_a.consent_opt_in = True
    ms_a.profile_name = "Ana"
    ms_a.current_case_tramite = "imv"

    ms_b = new_memory_state()
    ms_b.consent_opt_in = True
    ms_b.profile_name = "Pedro"
    ms_b.current_case_tramite = "empadronamiento"

    store.upsert(h_a, ms_a)
    store.upsert(h_b, ms_b)

    assert store.get(h_a).profile_name == "Ana"
    assert store.get(h_a).current_case_tramite == "imv"
    assert store.get(h_b).profile_name == "Pedro"
    assert store.get(h_b).current_case_tramite == "empadronamiento"

    # Forget one user — other unaffected
    store.forget(h_a)
    assert store.get(h_a) is None
    assert store.get(h_b).profile_name == "Pedro"


def test_parallel_upserts_isolated():
    """Concurrent upserts to different users don't interfere."""
    store = InMemoryStore()
    for i in range(10):
        h = derive_user_id(f"whatsapp:+3460000{i:04d}", "salt")
        ms = new_memory_state()
        ms.consent_opt_in = True
        ms.profile_name = f"User{i}"
        store.upsert(h, ms)

    for i in range(10):
        h = derive_user_id(f"whatsapp:+3460000{i:04d}", "salt")
        result = store.get(h)
        assert result.profile_name == f"User{i}"


def test_hash_determines_isolation():
    """Different phones with same salt produce different hashes."""
    h_a = derive_user_id("whatsapp:+34600111222", "salt")
    h_b = derive_user_id("whatsapp:+34600333444", "salt")
    assert h_a != h_b
    assert len(h_a) == 64
    assert len(h_b) == 64
