"""Rules-based verification of LLM response. NOT an LLM agent — deterministic code."""

import logging

from src.core.models import KBContext

logger = logging.getLogger(__name__)


def verify_response(response_text: str, kb_context: KBContext | None) -> str:
    """Verify and patch LLM response with rules-based checks."""
    from src.core.config import config

    # 1. Validate fuente_url domain before adding it
    official_url = ""
    if kb_context and kb_context.fuente_url:
        if config.DOMAIN_VALIDATION_ON:
            from src.core.domain_validator import is_domain_approved
            if is_domain_approved(kb_context.fuente_url):
                official_url = kb_context.fuente_url
            else:
                logger.warning(
                    "fuente_url domain not approved, omitting: %s",
                    kb_context.fuente_url,
                )
        else:
            official_url = kb_context.fuente_url

    # 2. Scan LLM text for URLs and replace unapproved ones
    if config.DOMAIN_VALIDATION_ON:
        from src.core.domain_validator import extract_urls, is_domain_approved as _approved
        for url in extract_urls(response_text):
            if not _approved(url):
                replacement = official_url or "https://administracion.gob.es"
                logger.warning("Replacing unapproved URL in response: %s -> %s", url, replacement)
                response_text = response_text.replace(url, replacement)

    # 3. Ensure official URL is present if we have KB context
    if official_url and official_url not in response_text:
        response_text += f"\n\nMás información: {official_url}"

    # 4. Enforce word limit (400 words soft, hard cap at 500)
    words = response_text.split()
    if len(words) > 500:
        response_text = " ".join(words[:400]) + "..."

    return response_text
