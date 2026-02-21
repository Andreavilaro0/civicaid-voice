"""Detect memory-related commands from user input."""

import re
import unicodedata
from enum import Enum
from typing import Optional


class MemoryCommand(Enum):
    FORGET = "forget"
    OPT_IN_YES = "opt_in_yes"
    OPT_IN_NO = "opt_in_no"


def _normalize(text: str) -> str:
    """Lowercase, strip, remove accents."""
    text = text.lower().strip()
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


_FORGET_PATTERNS = [
    re.compile(r"^olvida\s+mis\s+datos$"),
    re.compile(r"^borra\s+mis\s+datos$"),
    re.compile(r"^elimina\s+mis\s+datos$"),
    re.compile(r"^oublie\s+mes\s+donnees$"),
    re.compile(r"^forget\s+my\s+data$"),
    re.compile(r"^delete\s+my\s+data$"),
]

_YES_PATTERNS = [
    re.compile(r"^si$"),
    re.compile(r"^oui$"),
    re.compile(r"^yes$"),
    re.compile(r"^vale$"),
    re.compile(r"^ok$"),
    re.compile(r"^claro$"),
]

_NO_PATTERNS = [
    re.compile(r"^no$"),
    re.compile(r"^non$"),
    re.compile(r"^nah$"),
]


def detect_memory_command(text: str) -> Optional[MemoryCommand]:
    """Detect if user text is a memory command. Returns None for normal messages."""
    norm = _normalize(text)

    for pattern in _FORGET_PATTERNS:
        if pattern.match(norm):
            return MemoryCommand.FORGET

    # Only detect yes/no for short messages (<=2 words) to avoid false positives
    if len(norm.split()) <= 2:
        for pattern in _YES_PATTERNS:
            if pattern.match(norm):
                return MemoryCommand.OPT_IN_YES
        for pattern in _NO_PATTERNS:
            if pattern.match(norm):
                return MemoryCommand.OPT_IN_NO

    return None
