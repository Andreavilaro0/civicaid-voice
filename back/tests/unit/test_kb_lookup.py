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
    result = kb_lookup("cual es la capital de francia", "es")
    assert result is None


def test_kb_lookup_accent_insensitive():
    """Query without accents matches keywords that have accents."""
    # "ingreso minimo" (no accent) should match "ingreso mínimo" (with accent)
    result = kb_lookup("ingreso minimo", "es")
    assert result is not None
    assert result.tramite == "imv"


def test_kb_lookup_mixed_accents():
    """Query with accents matches keywords without accents and vice versa."""
    result = kb_lookup("información sobre el ingreso mínimo vital", "es")
    assert result is not None
    assert result.tramite == "imv"


# --- New tramites: prestacion_desempleo ---


def test_kb_lookup_prestacion_desempleo():
    """Find prestacion desempleo by 'paro' keyword."""
    result = kb_lookup("quiero cobrar el paro", "es")
    assert result is not None
    assert result.tramite == "prestacion_desempleo"
    assert result.fuente_url != ""
    assert result.verificado is True


def test_kb_lookup_desempleo_sepe():
    """Find prestacion desempleo by 'desempleo sepe'."""
    result = kb_lookup("prestacion desempleo del sepe", "es")
    assert result is not None
    assert result.tramite == "prestacion_desempleo"


def test_kb_lookup_desempleo_french():
    """Find prestacion desempleo by French keyword 'chomage'."""
    result = kb_lookup("je veux demander le chomage", "fr")
    assert result is not None
    assert result.tramite == "prestacion_desempleo"


# --- New tramites: nie_tie ---


def test_kb_lookup_nie():
    """Find NIE/TIE by 'nie' keyword."""
    result = kb_lookup("como consigo el nie", "es")
    assert result is not None
    assert result.tramite == "nie_tie"
    assert result.fuente_url != ""
    assert result.verificado is True


def test_kb_lookup_extranjeria():
    """Find NIE/TIE by 'extranjeria' keyword."""
    result = kb_lookup("tengo cita en extranjeria", "es")
    assert result is not None
    assert result.tramite == "nie_tie"


def test_kb_lookup_nie_french():
    """Find NIE/TIE by French keyword 'carte sejour'."""
    result = kb_lookup("comment obtenir la carte sejour", "fr")
    assert result is not None
    assert result.tramite == "nie_tie"


# --- New tramites: ayuda_alquiler ---


def test_kb_lookup_ayuda_alquiler():
    """Find ayuda alquiler by 'ayuda alquiler' keyword."""
    result = kb_lookup("necesito ayuda para pagar el alquiler", "es")
    assert result is not None
    assert result.tramite == "ayuda_alquiler"
    assert result.fuente_url != ""
    assert result.verificado is True


def test_kb_lookup_bono_joven():
    """Find ayuda alquiler by 'bono joven' keyword."""
    result = kb_lookup("como pido el bono joven alquiler", "es")
    assert result is not None
    assert result.tramite == "ayuda_alquiler"


def test_kb_lookup_alquiler_french():
    """Find ayuda alquiler by French keyword 'aide logement'."""
    result = kb_lookup("aide logement en espagne", "fr")
    assert result is not None
    assert result.tramite == "ayuda_alquiler"


# --- New tramites: justicia_gratuita ---


def test_kb_lookup_justicia_gratuita():
    """Find justicia gratuita by 'abogado gratis' keyword."""
    result = kb_lookup("necesito un abogado gratis", "es")
    assert result is not None
    assert result.tramite == "justicia_gratuita"
    assert result.fuente_url != ""
    assert result.verificado is True


def test_kb_lookup_turno_oficio():
    """Find justicia gratuita by 'turno oficio' keyword."""
    result = kb_lookup("necesito un abogado de turno oficio", "es")
    assert result is not None
    assert result.tramite == "justicia_gratuita"


def test_kb_lookup_justicia_french():
    """Find justicia gratuita by French keyword 'avocat gratuit'."""
    result = kb_lookup("je cherche un avocat gratuit", "fr")
    assert result is not None
    assert result.tramite == "justicia_gratuita"


# --- New tramites: certificado_discapacidad ---


def test_kb_lookup_certificado_discapacidad():
    """Find certificado discapacidad by 'discapacidad' keyword."""
    result = kb_lookup("como solicitar certificado de discapacidad", "es")
    assert result is not None
    assert result.tramite == "certificado_discapacidad"
    assert result.fuente_url != ""
    assert result.verificado is True


def test_kb_lookup_minusvalia():
    """Find certificado discapacidad by 'minusvalia' keyword."""
    result = kb_lookup("tengo minusvalia y quiero el certificado", "es")
    assert result is not None
    assert result.tramite == "certificado_discapacidad"


def test_kb_lookup_discapacidad_french():
    """Find certificado discapacidad by French keyword 'handicap'."""
    result = kb_lookup("certificat handicap en espagne", "fr")
    assert result is not None
    assert result.tramite == "certificado_discapacidad"
