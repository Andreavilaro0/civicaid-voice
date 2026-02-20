"""Query synonym expansion for Spanish government acronyms and terms.

Expands acronyms (IMV, NIE, SEPE, etc.) into their full Spanish names
so that BM25 tsvector matching can find relevant chunks.
"""

import unicodedata


SYNONYMS: dict[str, str] = {
    # Acronyms
    "imv": "ingreso minimo vital prestacion economica",
    "nie": "numero de identidad de extranjero",
    "tie": "tarjeta de identidad de extranjero",
    "sepe": "servicio publico de empleo estatal",
    "tsi": "tarjeta sanitaria individual",
    "ccaa": "comunidades autonomas",
    "age": "administracion general del estado",
    "dni": "documento nacional de identidad",
    "oac": "oficina de atencion al ciudadano empadronamiento padron",
    "iprem": "indicador publico renta efectos multiples ingreso minimo vital",
    "darde": "demanda de empleo tarjeta desempleo sepe paro",
    "mivau": "ministerio vivienda agenda urbana ayuda alquiler",
    "aeat": "agencia tributaria hacienda renta declaracion",
    # Common terms
    "paro": "prestacion por desempleo",
    "empadronamiento": "alta en el padron municipal registro",
    "alquiler joven": "bono alquiler joven ayuda al alquiler vivienda",
    "discapacidad": "certificado de discapacidad grado reconocimiento",
    "justicia gratuita": "asistencia juridica gratuita turno de oficio abogado",
    # Reverse mappings: full names → acronym + related terms
    "ingreso minimo vital": "imv prestacion economica pobreza seguridad social",
    "tarjeta sanitaria": "tsi asistencia sanitaria medico",
    "prestacion por desempleo": "paro sepe empleo cotizacion",
    "numero de identidad de extranjero": "nie extranjeria residencia",
    "tarjeta de identidad de extranjero": "tie extranjeria residencia",
    "certificado de discapacidad": "grado reconocimiento valoracion",
    "bono alquiler": "alquiler joven ayuda vivienda",
    "asistencia juridica gratuita": "justicia gratuita turno oficio abogado",
}


def _remove_accents(text: str) -> str:
    """Strip diacritics from text (e.g. 'nino' from 'nino')."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")


def normalize_query(query: str) -> str:
    """Lowercase and remove accents from *query*."""
    return _remove_accents(query.lower())


def expand_query(query: str) -> str:
    """Expand synonym keys found in *query*, keeping the original tokens.

    Multi-word keys (e.g. "alquiler joven") are checked first so they
    take precedence over single-word keys.
    """
    normalized = normalize_query(query)

    # Sort multi-word keys first (longer keys first) so they match before
    # their individual words.
    multi_word = sorted(
        ((k, v) for k, v in SYNONYMS.items() if " " in k),
        key=lambda kv: len(kv[0]),
        reverse=True,
    )
    single_word = {k: v for k, v in SYNONYMS.items() if " " not in k}

    expanded = normalized

    # Phase 1: multi-word expansion (append expansion after the match)
    for key, expansion in multi_word:
        if key in expanded:
            expanded = expanded.replace(key, f"{key} {expansion}", 1)

    # Phase 2: single-word expansion
    tokens = expanded.split()
    result: list[str] = []
    for token in tokens:
        result.append(token)
        if token in single_word:
            result.append(single_word[token])

    return " ".join(result)
