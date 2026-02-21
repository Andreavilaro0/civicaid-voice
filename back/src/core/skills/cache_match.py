"""Match user input against demo_cache.json entries by keywords."""

import unicodedata

from src.core.models import CacheEntry, CacheResult, InputType
from src.utils.timing import timed


def _normalize(text: str) -> str:
    """Normalize text: lowercase, strip accents, collapse whitespace."""
    text = text.lower().strip()
    # Remove accents (é→e, ñ→n, etc.) for more forgiving matching
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _score_entry(entry: CacheEntry, text_norm: str) -> float:
    """Score a cache entry against normalized text. Returns 0.0 if no match."""
    if entry.match_mode != "any_keyword" or not entry.patterns:
        return 0.0
    matches = sum(1 for p in entry.patterns if _normalize(p) in text_norm)
    return matches / len(entry.patterns) if matches > 0 else 0.0


@timed("cache_match")
def cache_match(
    text: str,
    idioma: str,
    input_type: InputType,
    cache_entries: list[CacheEntry],
) -> CacheResult:
    """Find best matching cache entry. Returns CacheResult."""

    # Image demo shortcut
    if input_type == InputType.IMAGE:
        for entry in cache_entries:
            if entry.match_mode == "image_demo":
                return CacheResult(hit=True, entry=entry, score=1.0)

    text_norm = _normalize(text)
    if not text_norm:
        return CacheResult(hit=False)

    # Pass 1: match with language filter (preferred)
    best_entry = None
    best_score = 0.0

    for entry in cache_entries:
        if entry.idioma not in (idioma, "any"):
            continue
        score = _score_entry(entry, text_norm)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry:
        return CacheResult(hit=True, entry=best_entry, score=best_score)

    # Pass 2: match ignoring language (handles langdetect misclassification)
    for entry in cache_entries:
        score = _score_entry(entry, text_norm)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry:
        return CacheResult(hit=True, entry=best_entry, score=best_score)

    return CacheResult(hit=False)
