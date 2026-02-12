"""Look up tramite info from JSON knowledge base files."""

import json
import os
from src.core.models import KBContext
from src.utils.logger import log_error
from src.utils.timing import timed

_KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "tramites")

# Keywords that map to each tramite
_TRAMITE_KEYWORDS = {
    "imv": ["imv", "ingreso minimo", "ingreso mínimo", "renta minima", "ayuda economica", "prestacion", "604"],
    "empadronamiento": ["empadron", "padron", "padrón", "registrar", "domicilio", "municipio", "censo", "inscrire", "mairie"],
    "tarjeta_sanitaria": ["tarjeta sanitaria", "tarjeta salud", "sanidad", "medico", "médico", "carte santé", "docteur", "seguro medico"],
}


def _detect_tramite(text: str) -> str | None:
    """Detect which tramite the text is about."""
    text_lower = text.lower()
    best_tramite = None
    best_count = 0
    for tramite, keywords in _TRAMITE_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
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
