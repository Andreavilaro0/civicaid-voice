"""Format Clara responses for WhatsApp rich text (bold, italic)."""

import re


def format_for_whatsapp(text: str) -> str:
    """Apply WhatsApp-compatible formatting to Clara's response.

    - Bold numbered steps: "1." -> "*1.*"
    - Bold warning keywords: OJO, IMPORTANTE
    - Does NOT modify URLs or already-formatted text.
    """
    # Skip if already has WhatsApp formatting
    if "*" in text:
        return text

    # Bold numbered steps: "1. " -> "*1.* "
    result = re.sub(r'(\d+)\.\s', r'*\1.* ', text)

    # Bold warning keywords
    result = re.sub(r'\b(OJO|IMPORTANTE|ATENCION):', r'*\1:*', result)

    return result
