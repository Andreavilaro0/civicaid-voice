"""Safety guardrails for Clara — pre-check user input, post-check LLM output.
Controlled by GUARDRAILS_ON flag. When off, all checks return safe/unchanged."""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class GuardrailResult:
    safe: bool
    reason: Optional[str] = None
    modified_text: Optional[str] = None


# --- BLOCKLIST: Topics Clara should not engage with ---
BLOCKED_PATTERNS = [
    (r'\b(suicid\w*|matarme|hacerme da[nñ]o|autolesion\w*)\b', 'self_harm',
     'Entiendo que estas pasando por un momento muy dificil. No estas solo/a. '
     'Llama al 024 (linea de atencion a la conducta suicida) o al 112. Hay personas preparadas para ayudarte.'),
    (r'\b(bomba|explosivo|armas?|terroris\w*)\b', 'violence',
     'No puedo ayudar con ese tema. Si hay una emergencia, llama al 112.'),
    (r'\b(hackear|robar identidad|falsificar)\b', 'illegal',
     'No puedo ayudar con eso. Si necesitas orientacion legal gratuita, llama al 060 o pide un abogado de oficio en tu juzgado mas cercano.'),
]

# --- DISCLAIMER: Always appended for legal/medical topics ---
LEGAL_DISCLAIMER = (
    "\n\nIMPORTANTE: Esta informacion es orientativa. Para tu caso concreto, "
    "te recomiendo consultar con un profesional o visitar las fuentes oficiales."
)

LEGAL_TRIGGERS = re.compile(
    r'\b(abogado|legal|juridic|demanda|denuncia|juicio|medic|diagnostic|receta|tratamiento)\b',
    re.IGNORECASE
)

# --- PII patterns to warn about ---
PII_PATTERNS = [
    (r'\b\d{8}[A-Z]\b', 'DNI'),          # Spanish DNI
    (r'\b[XYZ]\d{7}[A-Z]\b', 'NIE'),     # Spanish NIE
    (r'\b\d{3}[-.]?\d{3}[-.]?\d{3}\b', 'phone'),  # Phone number
]


def pre_check(user_text: str) -> GuardrailResult:
    """Check user input BEFORE processing. Returns safe=False if blocked."""
    text_lower = user_text.lower()
    for pattern, category, response in BLOCKED_PATTERNS:
        if re.search(pattern, text_lower):
            return GuardrailResult(safe=False, reason=category, modified_text=response)
    return GuardrailResult(safe=True)


def post_check(response_text: str) -> str:
    """Check and modify LLM output BEFORE sending to user."""
    result = response_text

    # Add legal disclaimer if legal/medical topics detected
    if LEGAL_TRIGGERS.search(result) and LEGAL_DISCLAIMER not in result:
        result += LEGAL_DISCLAIMER

    # Check for PII in response (should not be echoed back)
    for pattern, pii_type in PII_PATTERNS:
        if re.search(pattern, result):
            result = re.sub(pattern, f'[{pii_type} REDACTADO]', result)

    return result
