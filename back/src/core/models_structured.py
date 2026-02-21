"""Pydantic models for structured LLM output — optional, controlled by STRUCTURED_OUTPUT_ON flag."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field


class ClaraStructuredResponse(BaseModel):
    """Structured response schema for Clara's LLM output."""
    intent: str = Field(description="User intent: informacion, requisitos, pasos, documentos, otro")
    language: str = Field(description="Response language: es, fr, en, ar")
    tramite: Optional[str] = Field(default=None, description="Tramite: imv, empadronamiento, tarjeta_sanitaria, or null")
    summary: str = Field(description="Brief 1-2 sentence answer")
    steps: List[str] = Field(default_factory=list, description="Ordered steps if applicable")
    required_docs: List[str] = Field(default_factory=list, description="Required documents")
    warnings: List[str] = Field(default_factory=list, description="Important warnings or caveats")
    sources: List[str] = Field(default_factory=list, description="Official source URLs")
    disclaimer: str = Field(
        default="Esta informacion es orientativa. Consulte fuentes oficiales para confirmar.",
        description="Legal disclaimer",
    )


def parse_structured_response(raw_text: str) -> tuple[ClaraStructuredResponse | None, str]:
    """Try to parse LLM output as structured JSON. Returns (parsed, display_text).
    If parsing fails, returns (None, original_text) — zero breakage."""
    try:
        text = raw_text.strip()
        # Handle markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)
        parsed = ClaraStructuredResponse(**data)

        # Build display text from structured data
        display = parsed.summary
        if parsed.steps:
            display += "\n\nPasos:\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(parsed.steps))
        if parsed.required_docs:
            display += "\n\nDocumentos necesarios:\n" + "\n".join(f"  - {d}" for d in parsed.required_docs)
        if parsed.warnings:
            display += "\n\n" + "\n".join(f"Aviso: {w}" for w in parsed.warnings)
        if parsed.sources:
            display += "\n\n" + "\n".join(f"Mas info: {s}" for s in parsed.sources)
        display += f"\n\n{parsed.disclaimer}"

        return parsed, display
    except (json.JSONDecodeError, Exception):
        return None, raw_text
