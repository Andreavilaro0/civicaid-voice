"""Tests for memory-aware prompt building."""

from src.core.prompts.system_prompt import build_prompt


def test_build_prompt_without_memory():
    """build_prompt works without memory (backwards compat)."""
    p = build_prompt(kb_context="test", language="es")
    assert "Clara" in p
    assert "MEMORIA DEL USUARIO" not in p


def test_build_prompt_with_memory():
    """build_prompt includes memory blocks when provided."""
    p = build_prompt(
        kb_context="test",
        language="es",
        memory_profile="Nombre: Maria, Idioma: es",
        memory_summary="Pregunto sobre IMV",
        memory_case="tramite=imv, intent=requisitos",
    )
    assert "<memory_profile>" in p
    assert "Maria" in p
    assert "<memory_summary>" in p
    assert "IMV" in p
    assert "<memory_case>" in p
    assert "imv" in p


def test_build_prompt_memory_security_rule():
    """System prompt contains memory anti-injection rule."""
    p = build_prompt(
        kb_context="test",
        language="es",
        memory_profile="test",
    )
    assert "memory_" in p
    assert "instrucciones" in p.lower() or "datos" in p.lower()
