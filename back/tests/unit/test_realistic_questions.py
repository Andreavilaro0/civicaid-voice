"""Tests: realistic user questions hit correct KB entries.

Verifies kb_lookup finds correct tramite for natural questions across
8 tramites and multiple languages (where keywords exist in the KB).
"""

import pytest
from src.core.skills.kb_lookup import kb_lookup


# ── IMV ────────────────────────────────────────────────────────

class TestIMVQuestions:
    """Real questions about Ingreso Minimo Vital."""

    QUESTIONS = [
        ("¿Qué es el ingreso mínimo vital?", "es"),
        ("¿Cómo pido el IMV?", "es"),
        ("¿Cuánto se cobra de ingreso mínimo?", "es"),
        ("Me denegaron el IMV, ¿qué hago?", "es"),
        ("Soy madre soltera sin trabajo, ¿puedo pedir el IMV?", "es"),
        ("¿Qué documentos necesito para el ingreso mínimo vital?", "es"),
        ("¿Cómo solicito la prestación del IMV?", "es"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_imv_question(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "imv"


# ── Empadronamiento ────────────────────────────────────────────

class TestEmpadronamientoQuestions:
    """Real questions about municipal registration."""

    QUESTIONS = [
        ("¿Cómo me empadrono?", "es"),
        ("Necesito el padrón, ¿qué hago?", "es"),
        ("¿Puedo empadronarme sin contrato de alquiler?", "es"),
        ("¿Dónde saco el certificado de empadronamiento?", "es"),
        ("Soy sin techo, ¿puedo registrarme en el padrón?", "es"),
        ("¿Cada cuánto hay que renovar el padrón?", "es"),
        ("Necesito registrarme en el censo municipal", "es"),
        # French (keywords: inscrire, mairie)
        ("Comment m'inscrire à la mairie?", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_empadronamiento(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "empadronamiento"


# ── Tarjeta Sanitaria ──────────────────────────────────────────

class TestTarjetaSanitariaQuestions:
    """Real questions about health card."""

    QUESTIONS = [
        ("¿Cómo saco la tarjeta sanitaria?", "es"),
        ("Necesito un médico, ¿cómo consigo la tarjeta de sanidad?", "es"),
        ("¿Dónde pido cita con el médico?", "es"),
        ("Mi hijo necesita vacunas, ¿necesita tarjeta sanitaria?", "es"),
        ("Estoy embarazada y necesito tarjeta sanitaria", "es"),
        ("¿Cómo consigo el seguro médico?", "es"),
        # French (keywords: docteur, carte sante)
        ("J'ai besoin d'un docteur, comment avoir la carte santé?", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_tarjeta_sanitaria(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "tarjeta_sanitaria"


# ── NIE / TIE ──────────────────────────────────────────────────

class TestNIETIEQuestions:
    """Real questions about foreigner ID."""

    QUESTIONS = [
        ("¿Cómo saco el NIE?", "es"),
        ("Necesito el TIE, ¿qué documentos necesito?", "es"),
        ("Se me venció el NIE, ¿qué hago?", "es"),
        ("¿Dónde pido cita para extranjería?", "es"),
        ("Soy de la UE, ¿necesito NIE o TIE?", "es"),
        ("Necesito el permiso de residencia", "es"),
        ("Perdí mis papeles de residencia", "es"),
        # English (keyword: nie)
        ("How do I get a NIE number in Spain?", "en"),
        # French (keyword: nie)
        ("Comment obtenir le NIE en Espagne?", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_nie_tie(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "nie_tie"


# ── Desempleo ──────────────────────────────────────────────────

class TestDesempleoQuestions:
    """Real questions about unemployment benefits."""

    QUESTIONS = [
        ("¿Cómo pido el paro?", "es"),
        ("¿Cuánto tiempo tengo para pedir el desempleo?", "es"),
        ("¿Cuánto cobro de paro?", "es"),
        ("¿Puedo trabajar mientras cobro el paro?", "es"),
        ("Me despidieron, ¿cómo pido el paro?", "es"),
        ("Necesito pedir cita en el SEPE", "es"),
        # French (keyword: chomage)
        ("Comment obtenir le chômage en Espagne?", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_desempleo(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "prestacion_desempleo"


# ── Ayuda Alquiler ─────────────────────────────────────────────

class TestAyudaAlquilerQuestions:
    """Real questions about rental assistance."""

    QUESTIONS = [
        ("¿Hay ayudas para pagar el alquiler?", "es"),
        ("¿Qué es el bono alquiler joven?", "es"),
        ("No puedo pagar el alquiler, ¿qué hago?", "es"),
        ("Necesito ayuda para mi vivienda", "es"),
        ("¿Cómo pido el bono joven de alquiler?", "es"),
        # French (keyword: loyer, aide au loyer)
        ("Comment obtenir une aide au loyer?", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_ayuda_alquiler(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "ayuda_alquiler"


# ── Discapacidad ───────────────────────────────────────────────

class TestDiscapacidadQuestions:
    """Real questions about disability certificate."""

    QUESTIONS = [
        ("¿Cómo saco el certificado de discapacidad?", "es"),
        ("Tengo una enfermedad crónica, ¿puedo pedir la discapacidad?", "es"),
        ("¿Qué beneficios tiene el grado de discapacidad?", "es"),
        ("¿Cómo solicito la valoración de discapacidad?", "es"),
        # French (keyword: handicap)
        ("Comment obtenir le certificat de handicap?", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_discapacidad(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "certificado_discapacidad"


# ── Justicia Gratuita ──────────────────────────────────────────

class TestJusticiaGratuitaQuestions:
    """Real questions about free legal aid."""

    QUESTIONS = [
        ("Necesito un abogado gratis", "es"),
        ("¿Cómo pido justicia gratuita?", "es"),
        ("¿Tengo derecho a abogado de oficio?", "es"),
        ("¿Cómo solicito asistencia jurídica gratuita?", "es"),
        # French (keyword: avocat gratuit)
        ("J'ai besoin d'un avocat gratuit", "fr"),
    ]

    @pytest.mark.parametrize("q,lang", QUESTIONS,
                             ids=[q[:40] for q, _ in QUESTIONS])
    def test_justicia_gratuita(self, q, lang):
        result = kb_lookup(q, lang)
        assert result is not None, f"No KB match for: '{q}'"
        assert result.tramite == "justicia_gratuita"


# ── No-match (vague questions without tramite keywords) ────────

class TestNoMatchReturnsNone:
    """Questions without tramite keywords return None."""

    QUESTIONS = [
        "No tengo dinero para comer esta semana",
        "Estoy desesperado y no sé qué hacer",
        "¿Cuál es la capital de Francia?",
        "Hello, how are you?",
        "Me siento sola en este país",
    ]

    @pytest.mark.parametrize("q", QUESTIONS)
    def test_no_kb_match(self, q):
        result = kb_lookup(q, "es")
        assert result is None, f"Should not match any tramite: '{q}'"
