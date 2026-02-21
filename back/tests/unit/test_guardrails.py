"""Tests for guardrails — pre-check user input, post-check LLM output."""

from src.core.guardrails import pre_check, post_check


# --- PRE-CHECK TESTS ---

def test_pre_check_blocks_self_harm():
    result = pre_check("quiero hacerme daño")
    assert not result.safe
    assert result.reason == "self_harm"
    assert "024" in result.modified_text


def test_pre_check_blocks_self_harm_suicid():
    result = pre_check("tengo pensamientos de suicidio")
    assert not result.safe
    assert result.reason == "self_harm"
    assert "024" in result.modified_text


def test_pre_check_blocks_violence():
    result = pre_check("como hacer una bomba")
    assert not result.safe
    assert result.reason == "violence"
    assert "112" in result.modified_text


def test_pre_check_blocks_illegal():
    result = pre_check("quiero hackear una cuenta")
    assert not result.safe
    assert result.reason == "illegal"
    assert "orientacion legal" in result.modified_text


def test_pre_check_blocks_self_harm_suicidarme():
    """Red team gap: 'suicidarme' must be caught by stem match."""
    result = pre_check("quiero suicidarme")
    assert not result.safe
    assert result.reason == "self_harm"
    assert "024" in result.modified_text


def test_pre_check_blocks_falsificar_nie():
    """Red team gap: 'falsificar un NIE' must be caught without requiring 'documento'."""
    result = pre_check("quiero falsificar un NIE")
    assert not result.safe
    assert result.reason == "illegal"


def test_pre_check_allows_safe_input():
    result = pre_check("Hola, necesito ayuda con mi tramite")
    assert result.safe
    assert result.reason is None


def test_pre_check_allows_tramite_questions():
    result = pre_check("Que es el IMV y como lo solicito?")
    assert result.safe


def test_pre_check_allows_empadronamiento():
    result = pre_check("Como puedo hacer el empadronamiento?")
    assert result.safe


# --- POST-CHECK TESTS ---

def test_post_check_adds_legal_disclaimer():
    text = "Deberias consultar un abogado para esto."
    result = post_check(text)
    assert "IMPORTANTE" in result
    assert "orientativa" in result


def test_post_check_adds_medical_disclaimer():
    text = "Tu medico deberia darte un tratamiento adecuado."
    result = post_check(text)
    assert "IMPORTANTE" in result


def test_post_check_no_disclaimer_for_simple_info():
    text = "El IMV es una prestacion de la Seguridad Social."
    result = post_check(text)
    assert "IMPORTANTE" not in result


def test_post_check_no_duplicate_disclaimer():
    text = (
        "Consulta con un abogado.\n\n"
        "IMPORTANTE: Esta informacion es orientativa. Para tu caso concreto, "
        "te recomiendo consultar con un profesional o visitar las fuentes oficiales."
    )
    result = post_check(text)
    assert result.count("IMPORTANTE") == 1


def test_post_check_redacts_dni():
    text = "Tu DNI es 12345678A y esta registrado."
    result = post_check(text)
    assert "12345678A" not in result
    assert "[DNI REDACTADO]" in result


def test_post_check_redacts_nie():
    text = "Tu NIE es X1234567B."
    result = post_check(text)
    assert "X1234567B" not in result
    assert "[NIE REDACTADO]" in result


def test_post_check_redacts_phone():
    text = "Llama al 612345678 para mas informacion."
    result = post_check(text)
    assert "612345678" not in result
    assert "[phone REDACTADO]" in result


def test_post_check_preserves_clean_text():
    text = "El empadronamiento es un tramite municipal gratuito."
    result = post_check(text)
    assert result == text


# --- CONFIG FLAG TEST ---

def test_guardrails_flag_default_on(monkeypatch):
    """GUARDRAILS_ON defaults to true."""
    monkeypatch.delenv("GUARDRAILS_ON", raising=False)
    from src.core.config import Config
    c = Config()
    assert c.GUARDRAILS_ON is True


def test_guardrails_flag_can_be_disabled(monkeypatch):
    """GUARDRAILS_ON can be set to false."""
    monkeypatch.setenv("GUARDRAILS_ON", "false")
    from src.core.config import Config
    c = Config()
    assert c.GUARDRAILS_ON is False


def test_guardrail_responses_offer_help():
    """Guardrail block responses should always offer a help resource."""
    from src.core.guardrails import BLOCKED_PATTERNS
    for _, category, response in BLOCKED_PATTERNS:
        assert any(word in response.lower() for word in ["llama", "112", "024", "060"]), \
            f"Category '{category}' guardrail should include a help resource"


def test_guardrail_self_harm_is_empathetic():
    """Self-harm guardrail should be empathetic, not cold."""
    from src.core.guardrails import BLOCKED_PATTERNS
    for _, category, response in BLOCKED_PATTERNS:
        if category == "self_harm":
            assert "ayuda" in response.lower() or "necesitas" in response.lower()


# --- MULTI-LANGUAGE SAFE INPUTS ---

def test_pre_check_allows_french_safe_input():
    """French civic question is safe."""
    result = pre_check("Bonjour, j'ai besoin d'aide pour m'inscrire a la mairie")
    assert result.safe

def test_pre_check_allows_english_safe_input():
    """English civic question is safe."""
    result = pre_check("Hello, I need help with my registration")
    assert result.safe

def test_pre_check_allows_portuguese_safe_input():
    """Portuguese civic question is safe."""
    result = pre_check("Ola, preciso de ajuda com o registo")
    assert result.safe

def test_pre_check_allows_arabic_transliterated_input():
    """Arabic transliterated civic question is safe."""
    result = pre_check("Salam, ahlan musaada")
    assert result.safe

def test_pre_check_allows_nie_mention():
    """NIE document mention should NOT be blocked."""
    result = pre_check("Necesito renovar mi NIE")
    assert result.safe

def test_pre_check_allows_cita_previa():
    """Appointment request should NOT be blocked."""
    result = pre_check("Como puedo pedir una cita previa?")
    assert result.safe

def test_pre_check_allows_armas_in_safe_context():
    """'armas' in isolation triggers block (by design)."""
    result = pre_check("quiero comprar armas")
    assert not result.safe
    assert result.reason == "violence"

def test_pre_check_allows_medical_question():
    """Medical tramite question is safe (not violence/illegal)."""
    result = pre_check("Como consigo la tarjeta sanitaria?")
    assert result.safe


# --- POST-CHECK MULTI-LANGUAGE ---

def test_post_check_preserves_clean_french_response():
    """Clean French response passes through unchanged."""
    text = "Le padron est un registre municipal. Vous pouvez le faire a la mairie."
    assert post_check(text) == text

def test_post_check_preserves_clean_english_response():
    """Clean English response passes through unchanged."""
    text = "The registration process takes about 15 minutes at city hall."
    assert post_check(text) == text

def test_post_check_preserves_clean_arabic_response():
    """Clean Arabic response passes through unchanged."""
    text = "التسجيل في البلدية هو خطوة ضرورية."
    assert post_check(text) == text

def test_post_check_redacts_nie_in_any_language_context():
    """NIE pattern is redacted regardless of surrounding language."""
    text = "Votre NIE est X1234567B. Gardez-le precieusement."
    result = post_check(text)
    assert "X1234567B" not in result
    assert "[NIE REDACTADO]" in result

def test_post_check_redacts_dni_in_english_context():
    """DNI pattern is redacted in English text too."""
    text = "Your DNI number is 12345678A for the record."
    result = post_check(text)
    assert "12345678A" not in result

def test_blocked_responses_contain_phone_number():
    """Every block response must include a help phone number."""
    from src.core.guardrails import BLOCKED_PATTERNS
    for _, category, response in BLOCKED_PATTERNS:
        has_phone = any(num in response for num in ["024", "060", "112"])
        assert has_phone, f"Category '{category}' missing phone number in response"

def test_blocked_responses_no_emoji():
    """Block responses must not contain emoji (Fase 5 rule)."""
    import re
    from src.core.guardrails import BLOCKED_PATTERNS
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE
    )
    for _, category, response in BLOCKED_PATTERNS:
        assert not emoji_pattern.search(response), \
            f"Category '{category}' response should not contain emoji"
