"""Generate response using Gemini Flash with system prompt + KB context."""

import json
import time
from src.core.models import LLMResponse, KBContext
from src.core.config import config
from src.core.prompts.system_prompt import build_prompt
from src.core.prompts.templates import get_template
from src.utils.logger import log_llm, log_error
from src.utils.timing import timed
from src.core.memory.sanitize import escape_xml_tags

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


def _build_grounded_context(kb_context: KBContext, max_chunks: int = 4) -> str:
    """Build grounded context with numbered chunks and source URLs."""
    if not kb_context.chunks_used:
        return ""

    lines = ["CHUNKS RECUPERADOS:"]
    for i, chunk in enumerate(kb_context.chunks_used[:max_chunks], 1):
        # Sanitize chunk content to prevent prompt injection via [Cn] spoofing
        content = chunk.get('content_preview', '')
        content = escape_xml_tags(content)  # P0-3: escape XML tags
        content = content.replace('[C', '[​C')  # zero-width space breaks tag pattern
        section = chunk.get('section_name', '').replace('[', '(').replace(']', ')')
        lines.append(f"[C{i}] Seccion: {section} | "
                     f"Tramite: {chunk.get('procedure_id', '')} | "
                     f"Score: {chunk.get('score', 0):.2f}")
        lines.append(f"Contenido: {content}")
        if chunk.get('source_url'):
            url = escape_xml_tags(chunk['source_url'])  # P0-2: escape XML tags
            url = url.replace('[C', '[​C')  # P0-2: zero-width space defense
            lines.append(f"Fuente: {url}")
        lines.append("")  # blank line between chunks

    return "\n".join(lines)


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

    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    json_str = escape_xml_tags(json_str)
    return json_str


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

    # Build grounded context if available
    chunks_block = ""
    if kb_context and kb_context.chunks_used:
        from src.core.config import config as cfg
        if getattr(cfg, 'RAG_GROUNDED_PROMPTING', False):
            max_chunks = getattr(cfg, 'RAG_MAX_CHUNKS_IN_PROMPT', 4)
            chunks_block = _build_grounded_context(kb_context, max_chunks)

    system = build_prompt(
        kb_context=kb_str, language=language,
        memory_profile=memory_profile,
        memory_summary=memory_summary,
        memory_case=memory_case,
        chunks_block=chunks_block,
    )

    # Structured output instruction (opt-in)
    safe_user_text = escape_xml_tags(user_text)  # P0-1: prevent XML tag injection
    prompt_text = f"{system}\n\n<user_query>\n{safe_user_text}\n</user_query>"
    if config.STRUCTURED_OUTPUT_ON:
        prompt_text += (
            '\n\nIMPORTANT: Respond ONLY with valid JSON matching this schema: '
            '{"intent":"string","language":"string","tramite":"string|null",'
            '"summary":"string","steps":["string"],"required_docs":["string"],'
            '"warnings":["string"],"sources":["string"],"disclaimer":"string"}'
        )

    start = time.time()
    try:
        from google import genai
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt_text,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=500,
                temperature=0.3,
            ),
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
