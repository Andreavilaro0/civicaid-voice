"""Post-response memory update: summary, case, slots, PII redaction."""

import re
from datetime import datetime, timezone
from src.core.memory.models import MemoryState

_PII_PATTERNS = [
    re.compile(r'\b\d{8}[A-Z]\b'),       # DNI
    re.compile(r'\b[XYZ]\d{7}[A-Z]\b'),  # NIE
    re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{3}\b'),  # Phone
]


def _contains_pii(text: str) -> bool:
    """Check if text contains PII patterns."""
    return any(p.search(text) for p in _PII_PATTERNS)


def _truncate_summary(summary: str, max_lines: int = 8) -> str:
    """Keep only the last max_lines of the summary."""
    lines = summary.strip().split("\n")
    if len(lines) > max_lines:
        lines = lines[-max_lines:]
    return "\n".join(lines)


def update_memory_after_response(
    state: MemoryState,
    user_text: str,
    response_text: str,
    tramite_key: str | None,
    language: str,
) -> MemoryState:
    """Update memory state after a pipeline response. Returns updated state."""
    if not state.consent_opt_in:
        return state

    now = datetime.now(timezone.utc).isoformat()
    state.updated_at = now

    # Update language if detected
    if language and language != "es":
        state.profile_language = language

    # Update current case
    if tramite_key:
        state.current_case_tramite = tramite_key
        state.current_case_updated_at = now

    # Append to conversation summary (redact PII first)
    safe_text = user_text if not _contains_pii(user_text) else "[mensaje con datos personales]"
    summary_line = f"- Usuario pregunto: {safe_text[:80]}"
    if tramite_key:
        summary_line += f" (tramite: {tramite_key})"
    if state.conversation_summary:
        state.conversation_summary += "\n" + summary_line
    else:
        state.conversation_summary = summary_line
    state.conversation_summary = _truncate_summary(state.conversation_summary)

    return state
