"""Tests for post-response memory update."""

from src.core.memory.models import new_memory_state
from src.core.memory.update import update_memory_after_response


def test_update_sets_tramite():
    """Update sets current_case_tramite from kb_context."""
    ms = new_memory_state()
    ms.consent_opt_in = True
    updated = update_memory_after_response(
        ms, user_text="como pido el paro", response_text="Para solicitar...",
        tramite_key="prestacion_desempleo", language="es",
    )
    assert updated.current_case_tramite == "prestacion_desempleo"


def test_update_appends_summary():
    """Update builds conversation summary."""
    ms = new_memory_state()
    ms.consent_opt_in = True
    updated = update_memory_after_response(
        ms, user_text="info sobre IMV", response_text="El IMV es...",
        tramite_key="imv", language="es",
    )
    assert len(updated.conversation_summary) > 0


def test_update_preserves_profile():
    """Update does not overwrite existing profile."""
    ms = new_memory_state()
    ms.consent_opt_in = True
    ms.profile_name = "Maria"
    updated = update_memory_after_response(
        ms, user_text="test", response_text="test", tramite_key=None, language="es",
    )
    assert updated.profile_name == "Maria"


def test_update_redacts_pii_from_slots():
    """PII is not stored in summary."""
    ms = new_memory_state()
    ms.consent_opt_in = True
    updated = update_memory_after_response(
        ms, user_text="mi DNI es 12345678A",
        response_text="test", tramite_key=None, language="es",
    )
    assert "12345678A" not in updated.conversation_summary


def test_update_no_consent_returns_unchanged():
    """If no consent, memory is not updated."""
    ms = new_memory_state()
    ms.consent_opt_in = False
    updated = update_memory_after_response(
        ms, user_text="test", response_text="test",
        tramite_key="imv", language="es",
    )
    assert updated.current_case_tramite == ""
    assert updated.conversation_summary == ""
