"""Rules-based verification of LLM response. NOT an LLM agent — deterministic code."""

from src.core.models import KBContext


def verify_response(response_text: str, kb_context: KBContext | None) -> str:
    """Verify and patch LLM response with rules-based checks."""
    # 1. Ensure official URL is present if we have KB context
    if kb_context and kb_context.fuente_url and kb_context.fuente_url not in response_text:
        response_text += f"\n\nMás información: {kb_context.fuente_url}"

    # 2. Enforce word limit (400 words soft, hard cap at 500)
    # Previous 200-word cap was truncating steps + links.
    # TTS has its own 45-word limit — text responses need room for full info.
    words = response_text.split()
    if len(words) > 500:
        response_text = " ".join(words[:400]) + "..."

    return response_text
