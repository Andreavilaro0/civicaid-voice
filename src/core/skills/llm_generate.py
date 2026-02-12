"""Generate response using Gemini Flash with system prompt + KB context."""

import json
import time
from src.core.models import LLMResponse, KBContext
from src.core.config import config
from src.core.prompts.system_prompt import build_prompt
from src.core.prompts.templates import get_template
from src.utils.logger import log_llm, log_error
from src.utils.timing import timed


@timed("llm_generate")
def llm_generate(
    user_text: str,
    language: str,
    kb_context: KBContext | None,
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
        kb_str = json.dumps(kb_context.datos, ensure_ascii=False, indent=2)[:2000]

    system = build_prompt(kb_context=kb_str, language=language)

    # Structured output instruction (opt-in)
    prompt_text = f"{system}\n\nPregunta del usuario: {user_text}"
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
