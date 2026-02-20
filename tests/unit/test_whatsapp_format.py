"""Tests for WhatsApp response formatting."""

from src.core.skills.whatsapp_format import format_for_whatsapp


def test_bold_numbered_steps():
    """Numbered steps get bold markers."""
    text = "Para pedirlo necesitas: 1. Tu pasaporte 2. Contrato de alquiler"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result


def test_bold_ojo_warning():
    """OJO warnings get bold."""
    text = "OJO: el plazo es hasta el 15 de marzo."
    result = format_for_whatsapp(text)
    assert "*OJO:*" in result or "*OJO*" in result


def test_bold_important_keywords():
    """Key action words get bold."""
    text = "IMPORTANTE: necesitas llevar tu DNI."
    result = format_for_whatsapp(text)
    assert "*IMPORTANTE:*" in result


def test_no_double_bold():
    """Already-bolded text should not get double-bolded."""
    text = "*1.* Tu pasaporte"
    result = format_for_whatsapp(text)
    assert "**1.**" not in result


def test_preserves_plain_text():
    """Plain text without special markers should be unchanged."""
    text = "Hola, puedo ayudarte con tramites."
    result = format_for_whatsapp(text)
    assert result == text


def test_url_not_mangled():
    """URLs should not be modified by formatting."""
    text = "Mas info: https://administracion.gob.es"
    result = format_for_whatsapp(text)
    assert "https://administracion.gob.es" in result
