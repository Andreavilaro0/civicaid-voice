"""Load demo_cache.json at startup and expose cache matching."""

import json
import os
from src.core.models import CacheEntry, CacheResult, InputType
from src.core.skills.cache_match import cache_match
from src.utils.logger import log_error

_CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache", "demo_cache.json")
_entries: list[CacheEntry] = []


def load_cache() -> int:
    """Load demo_cache.json into memory. Returns number of entries loaded."""
    global _entries
    try:
        with open(_CACHE_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        _entries = [
            CacheEntry(
                id=e["id"],
                patterns=e["patterns"],
                match_mode=e["match_mode"],
                idioma=e["idioma"],
                respuesta=e["respuesta"],
                audio_file=e.get("audio_file"),
            )
            for e in raw
        ]
        return len(_entries)
    except Exception as e:
        log_error("load_cache", str(e))
        _entries = []
        return 0


def match(text: str, idioma: str, input_type: InputType) -> CacheResult:
    """Match text against cache entries."""
    return cache_match(text, idioma, input_type, _entries)


def get_entry_count() -> int:
    return len(_entries)
