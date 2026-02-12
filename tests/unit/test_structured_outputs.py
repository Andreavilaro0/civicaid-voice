"""Tests for structured output models and parsing — src/core/models_structured.py."""

import json
import pytest
from src.core.models_structured import ClaraStructuredResponse, parse_structured_response


# --- Fixtures ---

VALID_DATA = {
    "intent": "informacion",
    "language": "es",
    "tramite": "imv",
    "summary": "El IMV es una prestacion economica.",
    "steps": ["Paso 1: Reunir documentos", "Paso 2: Solicitar cita"],
    "required_docs": ["DNI/NIE", "Certificado de empadronamiento"],
    "warnings": ["El plazo puede variar segun comunidad autonoma"],
    "sources": ["https://www.seg-social.es/imv"],
    "disclaimer": "Orientativo.",
}


# --- Model validation tests ---

def test_structured_response_model_validation():
    """ClaraStructuredResponse accepts valid data and sets fields correctly."""
    resp = ClaraStructuredResponse(**VALID_DATA)
    assert resp.intent == "informacion"
    assert resp.language == "es"
    assert resp.tramite == "imv"
    assert resp.summary == "El IMV es una prestacion economica."
    assert len(resp.steps) == 2
    assert len(resp.required_docs) == 2
    assert len(resp.warnings) == 1
    assert len(resp.sources) == 1
    assert resp.disclaimer == "Orientativo."


def test_structured_response_defaults():
    """ClaraStructuredResponse uses defaults for optional list fields."""
    minimal = ClaraStructuredResponse(intent="otro", language="fr", summary="Bonjour")
    assert minimal.tramite is None
    assert minimal.steps == []
    assert minimal.required_docs == []
    assert minimal.warnings == []
    assert minimal.sources == []
    assert "orientativa" in minimal.disclaimer.lower() or "informacion" in minimal.disclaimer.lower()


def test_structured_response_rejects_missing_required():
    """ClaraStructuredResponse raises ValidationError when required fields are missing."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ClaraStructuredResponse()  # missing intent, language, summary


# --- parse_structured_response tests ---

def test_parse_valid_json():
    """parse_structured_response correctly parses valid JSON."""
    raw = json.dumps(VALID_DATA)
    parsed, display = parse_structured_response(raw)
    assert parsed is not None
    assert parsed.tramite == "imv"
    assert "El IMV es una prestacion economica." in display
    assert "Paso 1" in display
    assert "DNI/NIE" in display
    assert "Orientativo." in display


def test_parse_invalid_json_fallback():
    """parse_structured_response returns (None, original) for non-JSON text."""
    raw = "Hola, necesito ayuda con el IMV"
    parsed, display = parse_structured_response(raw)
    assert parsed is None
    assert display == raw


def test_parse_markdown_json_block():
    """parse_structured_response handles ```json ... ``` blocks."""
    raw = "```json\n" + json.dumps(VALID_DATA) + "\n```"
    parsed, display = parse_structured_response(raw)
    assert parsed is not None
    assert parsed.intent == "informacion"
    assert "El IMV es una prestacion economica." in display


def test_parse_generic_code_block():
    """parse_structured_response handles ``` ... ``` blocks (no json tag)."""
    raw = "```\n" + json.dumps(VALID_DATA) + "\n```"
    parsed, display = parse_structured_response(raw)
    assert parsed is not None
    assert parsed.tramite == "imv"


def test_parse_partial_json_fallback():
    """parse_structured_response returns fallback for partial/invalid JSON."""
    raw = '{"intent": "informacion", "language": "es"'  # missing closing brace
    parsed, display = parse_structured_response(raw)
    assert parsed is None
    assert display == raw


def test_parse_display_no_steps():
    """Display text omits steps section when steps list is empty."""
    data = VALID_DATA.copy()
    data["steps"] = []
    data["required_docs"] = []
    data["warnings"] = []
    data["sources"] = []
    raw = json.dumps(data)
    parsed, display = parse_structured_response(raw)
    assert parsed is not None
    assert "Pasos:" not in display
    assert "Documentos necesarios:" not in display


def test_flag_off_no_impact():
    """STRUCTURED_OUTPUT_ON defaults to false — zero impact when off."""
    from src.core.config import Config
    cfg = Config()
    assert cfg.STRUCTURED_OUTPUT_ON is False
