"""Territory detection for Spanish CCAA and municipalities.

Detects autonomous community or city references in user queries
so that search results can be filtered by territory.
"""

import unicodedata
from typing import Optional


# ── CCAA map ─────────────────────────────────────────────────────────

CCAA_MAP: dict[str, str] = {
    # Madrid
    "madrid": "madrid",
    "comunidad de madrid": "madrid",
    "cam": "madrid",
    # Cataluna
    "cataluna": "cataluna",
    "catalunya": "cataluna",
    "cat": "cataluna",
    # Andalucia
    "andalucia": "andalucia",
    # Valencia
    "valencia": "valencia",
    "comunitat valenciana": "valencia",
    "comunidad valenciana": "valencia",
    "cv": "valencia",
    # Galicia
    "galicia": "galicia",
    # Pais Vasco
    "pais vasco": "pais_vasco",
    "euskadi": "pais_vasco",
    "euskal herria": "pais_vasco",
    # Castilla y Leon
    "castilla y leon": "castilla_y_leon",
    "cyl": "castilla_y_leon",
    # Castilla-La Mancha
    "castilla la mancha": "castilla_la_mancha",
    "clm": "castilla_la_mancha",
    # Canarias
    "canarias": "canarias",
    "islas canarias": "canarias",
    # Aragon
    "aragon": "aragon",
    # Extremadura
    "extremadura": "extremadura",
    # Baleares
    "baleares": "baleares",
    "islas baleares": "baleares",
    "illes balears": "baleares",
    # Murcia
    "murcia": "murcia",
    "region de murcia": "murcia",
    # Asturias
    "asturias": "asturias",
    "principado de asturias": "asturias",
    # Navarra
    "navarra": "navarra",
    "comunidad foral de navarra": "navarra",
    # Cantabria
    "cantabria": "cantabria",
    # La Rioja
    "la rioja": "la_rioja",
    "rioja": "la_rioja",
}


# ── City map ─────────────────────────────────────────────────────────

CITY_MAP: dict[str, dict[str, str]] = {
    # Madrid
    "madrid": {"ccaa": "madrid", "municipio": "madrid"},
    "alcala de henares": {"ccaa": "madrid", "municipio": "alcala de henares"},
    "mostoles": {"ccaa": "madrid", "municipio": "mostoles"},
    "fuenlabrada": {"ccaa": "madrid", "municipio": "fuenlabrada"},
    "leganes": {"ccaa": "madrid", "municipio": "leganes"},
    "getafe": {"ccaa": "madrid", "municipio": "getafe"},
    "alcorcon": {"ccaa": "madrid", "municipio": "alcorcon"},
    "torrejon de ardoz": {"ccaa": "madrid", "municipio": "torrejon de ardoz"},
    "parla": {"ccaa": "madrid", "municipio": "parla"},
    # Cataluna
    "barcelona": {"ccaa": "cataluna", "municipio": "barcelona"},
    "hospitalet": {"ccaa": "cataluna", "municipio": "hospitalet de llobregat"},
    "hospitalet de llobregat": {"ccaa": "cataluna", "municipio": "hospitalet de llobregat"},
    "badalona": {"ccaa": "cataluna", "municipio": "badalona"},
    "terrassa": {"ccaa": "cataluna", "municipio": "terrassa"},
    "sabadell": {"ccaa": "cataluna", "municipio": "sabadell"},
    "tarragona": {"ccaa": "cataluna", "municipio": "tarragona"},
    "lleida": {"ccaa": "cataluna", "municipio": "lleida"},
    "girona": {"ccaa": "cataluna", "municipio": "girona"},
    # Andalucia
    "sevilla": {"ccaa": "andalucia", "municipio": "sevilla"},
    "malaga": {"ccaa": "andalucia", "municipio": "malaga"},
    "cordoba": {"ccaa": "andalucia", "municipio": "cordoba"},
    "granada": {"ccaa": "andalucia", "municipio": "granada"},
    "jerez": {"ccaa": "andalucia", "municipio": "jerez de la frontera"},
    "jerez de la frontera": {"ccaa": "andalucia", "municipio": "jerez de la frontera"},
    "almeria": {"ccaa": "andalucia", "municipio": "almeria"},
    "huelva": {"ccaa": "andalucia", "municipio": "huelva"},
    "cadiz": {"ccaa": "andalucia", "municipio": "cadiz"},
    "jaen": {"ccaa": "andalucia", "municipio": "jaen"},
    # Valencia
    "valencia": {"ccaa": "valencia", "municipio": "valencia"},
    "alicante": {"ccaa": "valencia", "municipio": "alicante"},
    "elche": {"ccaa": "valencia", "municipio": "elche"},
    "castellon": {"ccaa": "valencia", "municipio": "castellon de la plana"},
    # Pais Vasco
    "bilbao": {"ccaa": "pais_vasco", "municipio": "bilbao"},
    "vitoria": {"ccaa": "pais_vasco", "municipio": "vitoria-gasteiz"},
    "san sebastian": {"ccaa": "pais_vasco", "municipio": "san sebastian"},
    "donostia": {"ccaa": "pais_vasco", "municipio": "san sebastian"},
    # Aragon
    "zaragoza": {"ccaa": "aragon", "municipio": "zaragoza"},
    "huesca": {"ccaa": "aragon", "municipio": "huesca"},
    "teruel": {"ccaa": "aragon", "municipio": "teruel"},
    # Galicia
    "vigo": {"ccaa": "galicia", "municipio": "vigo"},
    "a coruna": {"ccaa": "galicia", "municipio": "a coruna"},
    "coruna": {"ccaa": "galicia", "municipio": "a coruna"},
    "ourense": {"ccaa": "galicia", "municipio": "ourense"},
    "santiago de compostela": {"ccaa": "galicia", "municipio": "santiago de compostela"},
    "lugo": {"ccaa": "galicia", "municipio": "lugo"},
    "pontevedra": {"ccaa": "galicia", "municipio": "pontevedra"},
    # Castilla y Leon
    "valladolid": {"ccaa": "castilla_y_leon", "municipio": "valladolid"},
    "burgos": {"ccaa": "castilla_y_leon", "municipio": "burgos"},
    "salamanca": {"ccaa": "castilla_y_leon", "municipio": "salamanca"},
    "leon": {"ccaa": "castilla_y_leon", "municipio": "leon"},
    # Canarias
    "las palmas": {"ccaa": "canarias", "municipio": "las palmas de gran canaria"},
    "santa cruz de tenerife": {"ccaa": "canarias", "municipio": "santa cruz de tenerife"},
    "tenerife": {"ccaa": "canarias", "municipio": "santa cruz de tenerife"},
    # Baleares
    "palma": {"ccaa": "baleares", "municipio": "palma de mallorca"},
    "palma de mallorca": {"ccaa": "baleares", "municipio": "palma de mallorca"},
    # Murcia
    "murcia": {"ccaa": "murcia", "municipio": "murcia"},
    "cartagena": {"ccaa": "murcia", "municipio": "cartagena"},
    # Asturias
    "oviedo": {"ccaa": "asturias", "municipio": "oviedo"},
    "gijon": {"ccaa": "asturias", "municipio": "gijon"},
    # Navarra
    "pamplona": {"ccaa": "navarra", "municipio": "pamplona"},
    # Cantabria
    "santander": {"ccaa": "cantabria", "municipio": "santander"},
    # La Rioja
    "logrono": {"ccaa": "la_rioja", "municipio": "logrono"},
    # Extremadura
    "badajoz": {"ccaa": "extremadura", "municipio": "badajoz"},
    "caceres": {"ccaa": "extremadura", "municipio": "caceres"},
    "merida": {"ccaa": "extremadura", "municipio": "merida"},
    # Castilla-La Mancha
    "toledo": {"ccaa": "castilla_la_mancha", "municipio": "toledo"},
    "albacete": {"ccaa": "castilla_la_mancha", "municipio": "albacete"},
    "ciudad real": {"ccaa": "castilla_la_mancha", "municipio": "ciudad real"},
    "guadalajara": {"ccaa": "castilla_la_mancha", "municipio": "guadalajara"},
}


# ── Detection logic ──────────────────────────────────────────────────

def _remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")


def _normalize(text: str) -> str:
    return _remove_accents(text.lower())


def _extract_bigrams(words: list[str]) -> list[str]:
    """Return all consecutive 2-word, 3-word, and 4-word n-grams."""
    ngrams: list[str] = []
    for n in (4, 3, 2):
        for i in range(len(words) - n + 1):
            ngrams.append(" ".join(words[i : i + n]))
    return ngrams


def detect_territory(query: str) -> Optional[dict]:
    """Detect a Spanish territory reference in *query*.

    Checks for "en <territory>" patterns first, then falls back to
    n-gram and single-word matching against CITY_MAP and CCAA_MAP.

    Returns:
        {"nivel": "municipal", "ccaa": "...", "municipio": "..."} for cities,
        {"nivel": "ccaa", "ccaa": "..."} for autonomous communities,
        or None if no territory is detected.
    """
    normalized = _normalize(query)
    words = normalized.split()

    # Phase 1: "en <territory>" pattern — higher confidence
    for i, word in enumerate(words):
        if word == "en" and i + 1 < len(words):
            # Try progressively shorter suffixes
            for end in range(len(words), i, -1):
                candidate = " ".join(words[i + 1 : end])
                if candidate in CITY_MAP:
                    info = CITY_MAP[candidate]
                    return {"nivel": "municipal", "ccaa": info["ccaa"], "municipio": info["municipio"]}
                if candidate in CCAA_MAP:
                    return {"nivel": "ccaa", "ccaa": CCAA_MAP[candidate]}

    # Phase 2: n-gram matching (cities first, then CCAA)
    ngrams = _extract_bigrams(words)
    for ngram in ngrams:
        if ngram in CITY_MAP:
            info = CITY_MAP[ngram]
            return {"nivel": "municipal", "ccaa": info["ccaa"], "municipio": info["municipio"]}
    for ngram in ngrams:
        if ngram in CCAA_MAP:
            return {"nivel": "ccaa", "ccaa": CCAA_MAP[ngram]}

    # Phase 3: single-word matching
    for word in words:
        if word in CITY_MAP:
            info = CITY_MAP[word]
            return {"nivel": "municipal", "ccaa": info["ccaa"], "municipio": info["municipio"]}
    for word in words:
        if word in CCAA_MAP:
            return {"nivel": "ccaa", "ccaa": CCAA_MAP[word]}

    return None
