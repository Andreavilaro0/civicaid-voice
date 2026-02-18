"""Look up tramite info from JSON knowledge base files.

Loads ALL .json files from data/tramites/ and matches by keywords.
To add a new tramite, just drop a .json file with a 'keywords' field."""

import json
import os
import unicodedata
from src.core.models import KBContext
from src.utils.logger import log_error
from src.utils.timing import timed


def _normalize(text: str) -> str:
    """Normalize text: lowercase, strip, remove accents."""
    text = text.lower().strip()
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

_KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "tramites")

# Built dynamically from all JSON files in data/tramites/
_TRAMITE_KEYWORDS: dict[str, list[str]] = {}


def _load_all_tramites() -> None:
    """Scan data/tramites/ and build keyword index from every .json file."""
    global _TRAMITE_KEYWORDS
    _TRAMITE_KEYWORDS = {}

    if not os.path.isdir(_KB_DIR):
        return

    for filename in os.listdir(_KB_DIR):
        if not filename.endswith(".json"):
            continue
        tramite_id = filename.replace(".json", "")
        filepath = os.path.join(_KB_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                datos = json.load(f)
            keywords = datos.get("keywords", [])
            if not keywords:
                # Fallback: use tramite name split by underscore
                keywords = tramite_id.replace("_", " ").split()
            _TRAMITE_KEYWORDS[tramite_id] = keywords
        except Exception as e:
            log_error("kb_load_tramite", f"{filename}: {e}")


# Load on import
_load_all_tramites()


def _detect_tramite(text: str) -> str | None:
    """Detect which tramite the text is about."""
    text_norm = _normalize(text)
    best_tramite = None
    best_count = 0
    for tramite, keywords in _TRAMITE_KEYWORDS.items():
        count = sum(1 for kw in keywords if _normalize(kw) in text_norm)
        if count > best_count:
            best_count = count
            best_tramite = tramite
    return best_tramite


@timed("kb_lookup")
def kb_lookup(text: str, language: str) -> KBContext | None:
    """Look up KB data for a tramite. Returns KBContext or None."""
    tramite = _detect_tramite(text)
    if not tramite:
        return None

    json_path = os.path.join(_KB_DIR, f"{tramite}.json")
    if not os.path.exists(json_path):
        return None

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return KBContext(
            tramite=tramite,
            datos=datos,
            fuente_url=datos.get("fuente_url", ""),
            verificado=datos.get("verificado", False),
        )
    except Exception as e:
        log_error("kb_lookup", str(e))
        return None
