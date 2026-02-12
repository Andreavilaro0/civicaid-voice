"""Test T4: KB lookup."""

from src.core.skills.kb_lookup import kb_lookup


def test_t4_kb_lookup_empadronamiento():
    """T4: Find empadronamiento tramite."""
    result = kb_lookup("necesito empadronarme", "es")
    assert result is not None
    assert result.tramite == "empadronamiento"
    assert result.fuente_url != ""
    assert result.verificado is True


def test_kb_lookup_imv():
    """Find IMV tramite."""
    result = kb_lookup("informacion sobre el ingreso minimo vital", "es")
    assert result is not None
    assert result.tramite == "imv"


def test_kb_lookup_tarjeta():
    """Find tarjeta sanitaria."""
    result = kb_lookup("como conseguir la tarjeta sanitaria", "es")
    assert result is not None
    assert result.tramite == "tarjeta_sanitaria"


def test_kb_lookup_no_match():
    """No match for unrelated query."""
    result = kb_lookup("que tiempo hace hoy", "es")
    assert result is None
