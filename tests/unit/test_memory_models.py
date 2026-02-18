"""Tests for MemoryState schema and user_hash."""

import json


def test_new_memory_state_defaults():
    """new_memory_state returns MemoryState with sane defaults."""
    from src.core.memory.models import new_memory_state
    m = new_memory_state()
    assert m.version == 1
    assert m.consent_opt_in is False
    assert m.pref_verbosity == "normal"
    assert m.slots == {}
    assert m.updated_at != ""
    assert m.expires_at != ""


def test_memory_state_serializable():
    """MemoryState.to_dict returns a plain dict."""
    from src.core.memory.models import new_memory_state
    m = new_memory_state()
    d = m.to_dict()
    assert isinstance(d, dict)
    assert d["version"] == 1


def test_memory_state_json_valid():
    """to_dict output is valid JSON."""
    from src.core.memory.models import new_memory_state
    m = new_memory_state()
    raw = json.dumps(m.to_dict())
    parsed = json.loads(raw)
    assert parsed["version"] == 1


def test_derive_user_id_stable():
    """Same phone + salt always produces same hash."""
    from src.core.memory.user_hash import derive_user_id
    h1 = derive_user_id("+34600111222", "salt1")
    h2 = derive_user_id("+34600111222", "salt1")
    assert h1 == h2
    assert len(h1) == 64


def test_derive_user_id_different_salt():
    """Different salt produces different hash."""
    from src.core.memory.user_hash import derive_user_id
    h1 = derive_user_id("+34600111222", "salt1")
    h2 = derive_user_id("+34600111222", "salt2")
    assert h1 != h2


def test_derive_user_id_different_phones():
    """Different phones produce different hashes."""
    from src.core.memory.user_hash import derive_user_id
    h1 = derive_user_id("+34600111222", "salt")
    h2 = derive_user_id("+34600333444", "salt")
    assert h1 != h2


def test_derive_user_id_no_pii():
    """Hash does not contain the original phone number."""
    from src.core.memory.user_hash import derive_user_id
    phone = "+34600111222"
    h = derive_user_id(phone, "salt")
    assert phone not in h
    assert "34600111222" not in h
