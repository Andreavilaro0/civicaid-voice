"""Rules-based verification of LLM response. NOT an LLM agent — deterministic code."""

from src.core.models import KBContext


def verify_response(response_text: str, kb_context: KBContext | None) -> str:
    """Verify and patch LLM response with rules-based checks."""
    # 1. Ensure official URL is present if we have KB context
    if kb_context and kb_context.fuente_url and kb_context.fuente_url not in response_text:
        response_text += f"\n\nMás información: {kb_context.fuente_url}"

    # 2. Enforce word limit (200 words, hard cap at 250)
    words = response_text.split()
    if len(words) > 250:
        response_text = " ".join(words[:200]) + "..."

    return response_text
