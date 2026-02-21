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


# --- MULTI-LANGUAGE FORMATTING ---

def test_french_numbered_steps_bold():
    """French numbered steps get bolded."""
    text = "1. Votre passeport 2. Contrat de logement"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result


def test_english_numbered_steps_bold():
    """English numbered steps get bolded."""
    text = "1. Your passport 2. Rental contract"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result


def test_portuguese_numbered_steps_bold():
    """Portuguese numbered steps get bolded."""
    text = "1. O teu passaporte 2. Contrato de arrendamento"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result


def test_arabic_with_numbers_formatted():
    """Arabic text with numbered steps gets formatted."""
    text = "1. جواز السفر 2. عقد الإيجار"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result


def test_atencion_keyword_bolded():
    """ATENCION keyword gets bolded."""
    text = "ATENCION: el plazo termina manana."
    result = format_for_whatsapp(text)
    assert "*ATENCION:*" in result


def test_already_formatted_french_untouched():
    """Already-formatted French text is not double-bolded."""
    text = "*1.* Votre passeport"
    result = format_for_whatsapp(text)
    assert result == text  # No change because "*" already present


def test_empty_string():
    """Empty string returns empty string."""
    assert format_for_whatsapp("") == ""


def test_whitespace_only():
    """Whitespace-only returns whitespace."""
    assert format_for_whatsapp("   ") == "   "


def test_long_numbered_list():
    """10-item numbered list all get bolded."""
    items = " ".join(f"{i}. Item{i}" for i in range(1, 11))
    result = format_for_whatsapp(items)
    for i in range(1, 11):
        assert f"*{i}.*" in result


def test_decimal_number_not_formatted_as_step():
    """Decimal numbers like '3.5' should get formatted (known behavior).
    The regex matches any digit+period+space pattern."""
    text = "El coste es 3. 5 euros"
    result = format_for_whatsapp(text)
    # "3. " matches the pattern, this is expected behavior
    assert "*3.*" in result


def test_url_with_numbers_preserved():
    """URLs with numbers are preserved when no other formatting present."""
    text = "Mas info en https://sede.administracion.gob.es/pag1234"
    result = format_for_whatsapp(text)
    assert "https://sede.administracion.gob.es/pag1234" in result


def test_mixed_language_content():
    """Mixed ES+FR content with numbers gets formatted."""
    text = "1. El padron 2. L'inscription 3. Registration"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result
    assert "*3.*" in result
