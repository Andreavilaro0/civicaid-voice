"""Look up office info (address, phone, appointment URL) by city and tramite."""

import json
import os
import unicodedata

from src.utils.logger import log_error

_OFICINAS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "oficinas.json")

_OFICINAS: dict = {}

# Generic fallback when city is not in the directory
_GENERIC_FALLBACK: dict = {
    "oficina": "Oficina de informacion de tu ayuntamiento",
    "direccion": "Consulta en tu ayuntamiento local",
    "telefono": "060 (informacion general de la Administracion)",
    "horario": "Lunes a viernes 9:00 a 14:00",
    "cita_previa_url": "https://administracion.gob.es",
    "sede_url": "https://administracion.gob.es",
}


def _normalize(text: str) -> str:
    text = text.lower().strip()
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _load_oficinas() -> None:
    global _OFICINAS
    if not os.path.isfile(_OFICINAS_PATH):
        return
    try:
        with open(_OFICINAS_PATH, "r", encoding="utf-8") as f:
            _OFICINAS = json.load(f)
    except Exception as e:
        log_error("office_lookup_load", str(e))


# Load on import
_load_oficinas()


def office_lookup(city: str, tramite: str | None) -> dict | None:
    """Look up office info for a city + tramite combination.

    Args:
        city: Municipality name (e.g. "madrid", "barcelona").
        tramite: Tramite key (e.g. "empadronamiento", "imv"). Can be None.

    Returns:
        Dict with office info (oficina, direccion, telefono, horario,
        cita_previa_url, sede_url) or None if no city is provided.
    """
    if not city:
        return None

    city_norm = _normalize(city)
    city_data = _OFICINAS.get(city_norm)

    if not city_data:
        return _GENERIC_FALLBACK

    if not tramite:
        # Return the first available tramite's office info for this city
        first_key = next(iter(city_data), None)
        return city_data[first_key] if first_key else _GENERIC_FALLBACK

    tramite_norm = _normalize(tramite)
    office = city_data.get(tramite_norm)
    if office:
        return office

    return _GENERIC_FALLBACK
