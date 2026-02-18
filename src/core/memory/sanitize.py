"""Sanitize memory content before injecting into LLM prompt."""

import re
from typing import Optional

# PII patterns to redact from memory before injection
_PII_PATTERNS = [
    (re.compile(r'\b\d{8}[A-Z]\b'), '[DNI_REDACTED]'),
    (re.compile(r'\b[XYZ]\d{7}[A-Z]\b'), '[NIE_REDACTED]'),
    (re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{3}\b'), '[PHONE_REDACTED]'),
    (re.compile(r'\b[A-Z]{2}\d{2}\s?\d{4}\s?\d{4}\s?\d{2}\s?\d{10}\b'), '[IBAN_REDACTED]'),
]


def escape_xml_tags(text: str) -> str:
    """Escape < and > to prevent tag injection in LLM prompts."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sanitize_for_prompt(text: Optional[str]) -> str:
    """Sanitize text for safe injection into prompt: escape tags + redact PII."""
    if not text:
        return ""
    result = escape_xml_tags(text)
    for pattern, replacement in _PII_PATTERNS:
        result = pattern.sub(replacement, result)
    return result
