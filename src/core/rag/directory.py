"""Last-resort fallback retriever — static directory of tramites.

Loads data from data/tramites/*.json at import time and provides keyword-based
retrieval returning minimal KBContext with official URLs."""

import json
import logging
import os
import unicodedata
from typing import Optional

from src.core.models import KBContext

logger = logging.getLogger(__name__)

_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "tramites",
)

# Each entry: {"nombre", "descripcion", "organismo", "fuente_url", "telefono", "keywords"}
DIRECTORY: dict[str, dict] = {}


def _normalize(text: str) -> str:
    """Lowercase, strip accents."""
    text = text.lower().strip()
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _build_directory() -> dict[str, dict]:
    """Build directory from data/tramites/*.json files."""
    directory: dict[str, dict] = {}
    data_dir = os.path.normpath(_DATA_DIR)

    if not os.path.isdir(data_dir):
        logger.warning("Directory data path not found: %s", data_dir)
        return directory

    for filename in sorted(os.listdir(data_dir)):
        if not filename.endswith(".json"):
            continue
        tramite_id = filename.replace(".json", "")
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                datos = json.load(f)
            directory[tramite_id] = {
                "nombre": datos.get("nombre", ""),
                "descripcion": datos.get("descripcion", ""),
                "organismo": datos.get("organismo", ""),
                "fuente_url": datos.get("fuente_url", ""),
                "telefono": datos.get("telefono", ""),
                "keywords": datos.get("keywords", []),
            }
        except Exception as exc:
            logger.warning("Failed to load %s: %s", filename, exc)

    return directory


# Build at import time
DIRECTORY = _build_directory()


class DirectoryRetriever:
    """Last-resort retriever using static directory with keyword matching."""

    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        """Keyword-match against directory. Returns KBContext with minimal info."""
        query_norm = _normalize(query)
        best_id: Optional[str] = None
        best_count = 0

        for tramite_id, info in DIRECTORY.items():
            keywords = info.get("keywords", [])
            count = sum(1 for kw in keywords if _normalize(kw) in query_norm)
            if count > best_count:
                best_count = count
                best_id = tramite_id

        if not best_id:
            return None

        info = DIRECTORY[best_id]
        return KBContext(
            tramite=best_id,
            datos={
                "nombre": info["nombre"],
                "descripcion": info["descripcion"],
                "organismo": info["organismo"],
                "telefono": info.get("telefono", ""),
                "source": "directory_fallback",
            },
            fuente_url=info["fuente_url"],
            verificado=False,
        )
