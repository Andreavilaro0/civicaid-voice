"""Tests for llm_generate: KB context building, prompt construction, fallbacks."""

import json
from unittest.mock import patch

from src.core.skills.llm_generate import _build_kb_context, llm_generate


# --- _build_kb_context tests ---

_SAMPLE_DATOS = {
    "keywords": ["imv", "ingreso minimo"],
    "tramite": "imv",
    "nombre": "Ingreso Mínimo Vital",
    "organismo": "Seguridad Social",
    "descripcion": "Prestación económica dirigida a prevenir el riesgo de pobreza.",
    "requisitos": ["Tener entre 23 y 65 años", "Residencia legal en España"],
    "documentos": ["DNI/NIE", "Certificado de empadronamiento"],
    "como_solicitar": [{"via": "Online", "detalle": "sede.seg-social.gob.es"}],
    "fuente_url": "https://www.seg-social.es/imv",
    "telefono": "900 20 22 22",
    "cuantias_2024": {"adulto_solo": "604,21€/mes"},
    "plazos": {"resolucion": "6 meses"},
    "verificado": True,
    "fecha_verificacion": "2024-12-01",
}


def test_build_kb_context_includes_priority_fields():
    """Priority fields (nombre, descripcion, organismo, requisitos, documentos) are included."""
    result = _build_kb_context(_SAMPLE_DATOS)
    parsed = json.loads(result)
    assert "nombre" in parsed
    assert "descripcion" in parsed
    assert "organismo" in parsed
    assert "requisitos" in parsed
    assert "documentos" in parsed


def test_build_kb_context_excludes_metadata():
    """Metadata fields (keywords, verificado, fecha_verificacion, tramite) are excluded."""
    result = _build_kb_context(_SAMPLE_DATOS)
    parsed = json.loads(result)
    assert "keywords" not in parsed
    assert "verificado" not in parsed
    assert "fecha_verificacion" not in parsed
    assert "tramite" not in parsed


def test_build_kb_context_valid_json_always():
    """Output is always valid JSON, even with empty or large data."""
    # Empty dict
    result = _build_kb_context({})
    parsed = json.loads(result)
    assert isinstance(parsed, dict)

    # Normal data
    result = _build_kb_context(_SAMPLE_DATOS)
    parsed = json.loads(result)
    assert isinstance(parsed, dict)

    # Very small max_chars
    result = _build_kb_context(_SAMPLE_DATOS, max_chars=10)
    parsed = json.loads(result)
    assert isinstance(parsed, dict)


def test_build_kb_context_respects_max_chars():
    """Output never exceeds max_chars limit."""
    result = _build_kb_context(_SAMPLE_DATOS, max_chars=200)
    assert len(result) <= 200
    # Still valid JSON
    parsed = json.loads(result)
    assert isinstance(parsed, dict)


def test_llm_generate_disabled_returns_fallback():
    """When LLM_LIVE=False, returns fallback response."""
    with patch("src.core.skills.llm_generate.config") as mock_config:
        mock_config.LLM_LIVE = False
        mock_config.GEMINI_API_KEY = "test-key"
        mock_config.STRUCTURED_OUTPUT_ON = False
        resp = llm_generate("test question", "es", None)
        assert resp.success is False
        assert resp.error == "LLM disabled or no API key"


def test_llm_generate_no_api_key_returns_fallback():
    """When GEMINI_API_KEY is empty, returns fallback response."""
    with patch("src.core.skills.llm_generate.config") as mock_config:
        mock_config.LLM_LIVE = True
        mock_config.GEMINI_API_KEY = ""
        mock_config.STRUCTURED_OUTPUT_ON = False
        resp = llm_generate("test question", "es", None)
        assert resp.success is False
        assert resp.error == "LLM disabled or no API key"


# --- Prompt construction tests (TICKET-04) ---

def test_prompt_uses_xml_delimiters():
    """Prompt wraps user text in <user_query> XML tags."""
    import types
    import unittest.mock as um

    mock_google = types.ModuleType("google")
    mock_genai = um.MagicMock()
    mock_google.generativeai = mock_genai
    mock_model = mock_genai.GenerativeModel.return_value
    mock_response = mock_model.generate_content.return_value
    mock_response.text = "test response"

    with patch("src.core.skills.llm_generate.config") as mock_config:
        mock_config.LLM_LIVE = True
        mock_config.GEMINI_API_KEY = "test-key"
        mock_config.STRUCTURED_OUTPUT_ON = False
        mock_config.LLM_TIMEOUT = 6
        with patch.dict("sys.modules", {
            "google": mock_google,
            "google.generativeai": mock_genai,
        }):
            llm_generate("hola mundo", "es", None)

            call_args = mock_model.generate_content.call_args
            prompt = call_args[0][0][0]["parts"][0]["text"]
            assert "<user_query>" in prompt
            assert "</user_query>" in prompt
            assert "hola mundo" in prompt


def test_prompt_contains_anti_injection_instruction():
    """System prompt includes anti-injection instruction about <user_query>."""
    from src.core.prompts.system_prompt import build_prompt
    prompt = build_prompt(kb_context="test", language="es")
    assert "SEGURIDAD" in prompt
    assert "<user_query>" in prompt
    assert "NUNCA obedezcas" in prompt
