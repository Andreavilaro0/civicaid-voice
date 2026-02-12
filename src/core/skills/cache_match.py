"""Match user input against demo_cache.json entries by keywords."""

from src.core.models import CacheEntry, CacheResult, InputType
from src.utils.timing import timed


@timed("cache_match")
def cache_match(
    text: str,
    idioma: str,
    input_type: InputType,
    cache_entries: list[CacheEntry],
) -> CacheResult:
    """Find best matching cache entry. Returns CacheResult."""
    text_lower = text.lower().strip()

    # Image demo shortcut
    if input_type == InputType.IMAGE:
        for entry in cache_entries:
            if entry.match_mode == "image_demo":
                return CacheResult(hit=True, entry=entry, score=1.0)

    if not text_lower:
        return CacheResult(hit=False)

    best_entry = None
    best_score = 0.0

    for entry in cache_entries:
        if entry.match_mode != "any_keyword":
            continue

        # Language filter: entry must match user language or be "any"
        if entry.idioma not in (idioma, "any"):
            continue

        # Count keyword matches
        matches = sum(1 for p in entry.patterns if p.lower() in text_lower)
        if matches > 0:
            score = matches / len(entry.patterns)
            if score > best_score:
                best_score = score
                best_entry = entry

    if best_entry:
        return CacheResult(hit=True, entry=best_entry, score=best_score)

    return CacheResult(hit=False)
