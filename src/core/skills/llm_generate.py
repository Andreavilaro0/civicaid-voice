"""Generate response using Gemini Flash with system prompt + KB context."""

import json
import time
from src.core.models import LLMResponse, KBContext
from src.core.config import config
from src.core.prompts.system_prompt import build_prompt
from src.core.prompts.templates import get_template
from src.utils.logger import log_llm, log_error
from src.utils.timing import timed

# Fields in priority order for KB context building
_PRIORITY_FIELDS = [
    # Tier 1: always include
    ["nombre", "descripcion", "organismo"],
    # Tier 2: always include
    ["requisitos"],
    # Tier 3: always include
    ["documentos"],
    # Tier 4: how-to (any that exist)
    ["como_solicitar", "como_hacerlo_madrid", "como_solicitarla_madrid", "proceso"],
    # Tier 5: always include
    ["fuente_url", "telefono"],
    # Tier 6: include if space
    ["cuantias_2024", "plazos", "datos_importantes", "quien_tiene_derecho"],
]

# Metadata fields to never include
_EXCLUDED_FIELDS = {"keywords", "verificado", "fecha_verificacion", "tramite"}


def _build_kb_context(datos: dict, max_chars: int = 3000) -> str:
    """Build KB context string prioritizing important fields.

    Iterates through field tiers in priority order, including each tier
    only if it fits within max_chars. Always returns valid JSON.
    """
    result: dict = {}
    for tier in _PRIORITY_FIELDS:
        tier_data: dict = {}
        for field in tier:
            if field in datos and field not in _EXCLUDED_FIELDS:
                tier_data[field] = datos[field]
        if not tier_data:
            continue
        candidate = {**result, **tier_data}
        candidate_str = json.dumps(candidate, ensure_ascii=False, indent=2)
        if len(candidate_str) <= max_chars:
            result = candidate
        # else: skip this tier, it doesn't fit

    return json.dumps(result, ensure_ascii=False, indent=2)


@timed("llm_generate")
def llm_generate(
    user_text: str,
    language: str,
    kb_context: KBContext | None,
    memory_profile: str = "",
    memory_summary: str = "",
    memory_case: str = "",
) -> LLMResponse:
    """Call Gemini Flash to generate a response. Returns LLMResponse."""
    if not config.LLM_LIVE or not config.GEMINI_API_KEY:
        fallback = get_template("fallback_generic", language)
        return LLMResponse(
            text=fallback, language=language, duration_ms=0,
            from_cache=False, success=False, error="LLM disabled or no API key"
        )

    # Build KB context string
    kb_str = "No hay contexto disponible."
    if kb_context:
        kb_str = _build_kb_context(kb_context.datos)

    system = build_prompt(
        kb_context=kb_str, language=language,
        memory_profile=memory_profile,
        memory_summary=memory_summary,
        memory_case=memory_case,
    )

    # Structured output instruction (opt-in)
    prompt_text = f"{system}\n\n<user_query>\n{user_text}\n</user_query>"
    if config.STRUCTURED_OUTPUT_ON:
        prompt_text += (
            '\n\nIMPORTANT: Respond ONLY with valid JSON matching this schema: '
            '{"intent":"string","language":"string","tramite":"string|null",'
            '"summary":"string","steps":["string"],"required_docs":["string"],'
            '"warnings":["string"],"sources":["string"],"disclaimer":"string"}'
        )

    start = time.time()
    try:
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            [{"role": "user", "parts": [{"text": prompt_text}]}],
            generation_config={"max_output_tokens": 500, "temperature": 0.3},
            request_options={"timeout": config.LLM_TIMEOUT},
        )
        elapsed = int((time.time() - start) * 1000)
        text = response.text.strip()
        log_llm(True, elapsed, "gemini")
        return LLMResponse(
            text=text, language=language, duration_ms=elapsed,
            from_cache=False, success=True
        )
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        log_llm(False, elapsed, "gemini")
        log_error("llm_generate", str(e))
        fallback = get_template("llm_fail", language)
        return LLMResponse(
            text=fallback, language=language, duration_ms=elapsed,
            from_cache=False, success=False, error=str(e)
        )
