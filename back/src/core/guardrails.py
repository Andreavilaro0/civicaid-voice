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

# --- DISCLAIMER: Always appended for legal/medical topics (multilingual) ---
LEGAL_DISCLAIMERS = {
    "es": "\n\nIMPORTANTE: Esta informacion es orientativa. Para tu caso concreto, te recomiendo consultar con un profesional o visitar las fuentes oficiales.",
    "en": "\n\nIMPORTANT: This information is for guidance only. For your specific case, I recommend consulting a professional or visiting official sources.",
    "fr": "\n\nIMPORTANT: Ces informations sont indicatives. Pour votre cas specifique, je vous recommande de consulter un professionnel ou de visiter les sources officielles.",
    "pt": "\n\nIMPORTANTE: Esta informacao e orientativa. Para o seu caso concreto, recomendo consultar um profissional ou visitar as fontes oficiais.",
    "ro": "\n\nIMPORTANT: Aceste informatii sunt orientative. Pentru cazul dvs. concret, va recomand sa consultati un profesionist sau sa vizitati sursele oficiale.",
    "ca": "\n\nIMPORTANT: Aquesta informacio es orientativa. Per al teu cas concret, et recomano consultar amb un professional o visitar les fonts oficials.",
    "zh": "\n\n重要提示：此信息仅供参考。对于您的具体情况，建议咨询专业人士或访问官方来源。",
    "ar": "\n\nمهم: هذه المعلومات إرشادية فقط. لحالتك المحددة، أنصحك باستشارة متخصص أو زيارة المصادر الرسمية.",
}

# Clara's own domain — always allowed, never replaced
_CLARA_DOMAINS = {"andreavilaro0.github.io"}

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


def post_check(response_text: str, language: str = "es") -> str:
    """Check and modify LLM output BEFORE sending to user."""
    result = response_text

    # Add legal disclaimer if legal/medical topics detected (in user's language)
    disclaimer = LEGAL_DISCLAIMERS.get(language, LEGAL_DISCLAIMERS["es"])
    if LEGAL_TRIGGERS.search(result) and disclaimer not in result:
        result += disclaimer

    # Check for PII in response (should not be echoed back)
    for pattern, pii_type in PII_PATTERNS:
        if re.search(pattern, result):
            result = re.sub(pattern, f'[{pii_type} REDACTADO]', result)

    # Validate URLs in final response against domain policy
    from src.core.config import config
    if config.DOMAIN_VALIDATION_ON:
        from src.core.domain_validator import extract_urls, is_domain_approved
        _FALLBACK_URL = "https://administracion.gob.es"
        for url in extract_urls(result):
            # Skip Clara's own domain (info-legal page, etc.)
            if any(d in url for d in _CLARA_DOMAINS):
                continue
            if not is_domain_approved(url):
                result = result.replace(url, _FALLBACK_URL)

    return result
