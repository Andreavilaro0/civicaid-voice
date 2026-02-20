# ProcedureDoc Normalization Schema

> **Scope:** Canonical data schema for normalized government procedure documents in Clara's knowledge base.
> **Status:** Research / Design (no code changes)
> **Date:** 2026-02-18
> **Related:** `ingestion-playbook.md`, `extraction-spec.md`

---

## Overview

Every procedure ingested into Clara's KB is normalized into a **ProcedureDoc** -- a JSON document that follows a consistent schema regardless of the original source format (HTML, PDF, BOE XML). This schema is a superset of the current `data/tramites/*.json` format, meaning existing curated files remain valid without modification.

---

## ProcedureDoc v1 Schema

```json
{
  "version": 1,

  "id": "age-sepe-prestacion-desempleo",
  "nombre": "Prestacion por Desempleo (Paro)",
  "nombre_alternativo": ["Paro", "Cobrar el paro", "Prestacion contributiva por desempleo"],

  "source_url": "https://www.sepe.es/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html",
  "source_urls": [
    "https://www.sepe.es/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html",
    "https://sede.sepe.gob.es/portalSede/flows/tramiteSolicitud"
  ],
  "source_type": "age",

  "organismo": "SEPE (Servicio Publico de Empleo Estatal)",
  "organismo_abrev": "SEPE",

  "territorio": {
    "nivel": "estatal",
    "ccaa": null,
    "municipio": null,
    "provincia": null
  },

  "canal": "mixto",

  "descripcion": "Prestacion economica para personas que han perdido su empleo...",
  "requisitos": ["..."],
  "documentos_necesarios": ["..."],
  "plazos": "15 dias habiles desde la situacion legal de desempleo",
  "tasas": null,
  "base_legal": ["Real Decreto Legislativo 8/2015", "Ley 31/1984"],

  "como_solicitar": {
    "online": "Sede electronica del SEPE con certificado digital o cl@ve",
    "presencial": "Oficinas de prestaciones del SEPE con cita previa",
    "telefono": "919 26 79 70 (cita previa) / 901 119 999 (informacion)"
  },

  "donde_solicitar": {
    "urls": ["https://sede.sepe.gob.es/portalSede/flows/tramiteSolicitud"],
    "direcciones": ["Oficinas de prestaciones del SEPE (ver directorio en sepe.es)"],
    "cita_previa_url": "https://sede.sepe.gob.es/portalSede/flows/tramiteCitaPrevia"
  },

  "keywords": ["paro", "desempleo", "sepe", "prestacion desempleo", "cobrar paro"],
  "tags": ["empleo", "prestacion-contributiva", "sepe", "seguridad-social"],

  "idioma": "es",
  "idiomas_disponibles": ["es"],

  "extracted_at": "2026-02-18T10:00:00Z",
  "verified_at": "2026-02-18T10:00:00Z",
  "verified_by": "manual",

  "content_hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
  "word_count": 1250,
  "completeness_score": 0.92,

  "version": 1
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | integer | Yes | Schema version. Always `1` for this spec. |
| `id` | string | Yes | Globally unique slug: `{source_type}-{organismo_abrev}-{nombre_slug}` |
| `nombre` | string | Yes | Full procedure name as displayed to user |
| `nombre_alternativo` | string[] | No | Colloquial or alternative names |
| `source_url` | string (URI) | Yes | Primary canonical URL |
| `source_urls` | string[] (URI) | No | All URLs contributing to this document |
| `source_type` | enum | Yes | `"age"` / `"ccaa"` / `"local"` / `"boe"` |
| `organismo` | string | Yes | Full name of responsible body |
| `organismo_abrev` | string | No | Abbreviation (SEPE, INSS, etc.) |
| `territorio.nivel` | enum | Yes | `"estatal"` / `"autonomico"` / `"local"` |
| `territorio.ccaa` | string or null | No | Lowercase slug if autonomico/local |
| `territorio.municipio` | string or null | No | Lowercase slug if local |
| `territorio.provincia` | string or null | No | Lowercase slug if local |
| `canal` | enum | Yes | `"electronico"` / `"presencial"` / `"mixto"` |
| `descripcion` | string | Yes | 1-3 sentence summary |
| `requisitos` | string[] | Recommended | Eligibility requirements |
| `documentos_necesarios` | string[] | Recommended | Documents the user must provide |
| `plazos` | string or object | No | Deadlines and timeframes |
| `tasas` | string or null | No | Fees or costs |
| `base_legal` | string[] | No | Legal references (BOE IDs, law names) |
| `como_solicitar` | object or list | Recommended | How to apply (online/presencial/telefono) |
| `donde_solicitar.urls` | string[] | No | URLs to start the procedure |
| `donde_solicitar.direcciones` | string[] | No | Physical addresses |
| `donde_solicitar.cita_previa_url` | string or null | No | Appointment booking URL |
| `keywords` | string[] | Yes | Search keywords for `kb_lookup.py` |
| `tags` | string[] | No | Classification tags for filtering |
| `idioma` | string | Yes | Primary language: `"es"`, `"ca"`, `"eu"`, `"gl"` |
| `idiomas_disponibles` | string[] | No | All available languages |
| `extracted_at` | string (ISO 8601) | Yes | When content was extracted |
| `verified_at` | string (ISO 8601) or null | No | When content was last verified |
| `verified_by` | string or null | No | `"manual"` or `"auto"` |
| `content_hash` | string | Yes | SHA-256 of normalized text body |
| `word_count` | integer | Yes | Total words across all text fields |
| `completeness_score` | float | Yes | 0.0 to 1.0 (see calculation below) |

---

## Completeness Score Calculation

The `completeness_score` measures how many expected fields are filled, weighted by importance to the end user.

### Field Weights

```python
SCORED_FIELDS = {
    "nombre":               1.0,   # Must know what the procedure is called
    "descripcion":          1.0,   # Must know what it does
    "requisitos":           1.0,   # Must know if they qualify
    "documentos_necesarios": 1.0,  # Must know what to bring
    "como_solicitar":       1.0,   # Must know how to apply
    "organismo":            0.8,   # Should know who handles it
    "plazos":               0.6,   # Should know deadlines
    "fuente_url":           0.5,   # Should have source for trust
    "donde_solicitar":      0.4,   # Helpful to know where
    "tasas":                0.3,   # Helpful to know cost
    "base_legal":           0.3,   # Nice to have legal refs
    "donde_solicitar":      0.3,   # Direct link to start
    "telefono":             0.2,   # Nice to have phone
    "datos_importantes":    0.2,   # Nice to have tips
}
# Maximum possible weight: 8.6
```

### Calculation

```python
def calculate_completeness(doc: dict) -> float:
    total_weight = sum(SCORED_FIELDS.values())
    filled_weight = 0.0

    for field_name, weight in SCORED_FIELDS.items():
        value = doc.get(field_name)
        if value is not None and value != [] and value != "" and value != {}:
            filled_weight += weight

    return round(filled_weight / total_weight, 2)
```

### Current KB Completeness Estimates

| Tramite | Estimated Score | Key Missing Fields |
|---------|----------------|--------------------|
| prestacion_desempleo | 0.90 | tasas, base_legal |
| imv | 0.82 | tasas, base_legal, donde_solicitar |
| empadronamiento | 0.78 | plazos, tasas, base_legal |
| tarjeta_sanitaria | 0.72 | plazos, tasas, base_legal |
| nie_tie | 0.88 | tasas (partial), base_legal |
| ayuda_alquiler | 0.85 | base_legal |
| certificado_discapacidad | 0.88 | tasas |
| justicia_gratuita | 0.88 | -- |

Average: ~0.84. The pipeline should aim for >= 0.70 for auto-ingested procedures.

---

## Backward Compatibility with `data/tramites/*.json`

The ProcedureDoc schema is a **strict superset** of the existing format. Every field in the current JSON files maps directly:

| Current Field | ProcedureDoc Field | Notes |
|---------------|-------------------|-------|
| `keywords` | `keywords` | Identical |
| `tramite` | derived from `id` | Filename key; also kept as legacy field |
| `nombre` | `nombre` | Identical |
| `organismo` | `organismo` | Identical |
| `descripcion` | `descripcion` | Identical |
| `requisitos` | `requisitos` | Identical (list of strings) |
| `documentos` | `documentos_necesarios` | Renamed for clarity |
| `como_solicitar` | `como_solicitar` | Same structure accepted |
| `plazos` | `plazos` | String or object both valid |
| `cuantias` / `cuantias_2024` | kept as extended field | Flexible structure |
| `duracion` | kept as extended field | Flexible structure |
| `datos_importantes` | kept as extended field | list of strings |
| `fuente_url` | `source_url` (primary) | Also kept as legacy `fuente_url` |
| `telefono` | kept as extended field | String |
| `verificado` | maps to `verified_by != null` | Boolean kept for compat |
| `fecha_verificacion` | `verified_at` | ISO 8601 conversion |

### Why No Changes to `kb_lookup.py` Are Needed

The existing `kb_lookup.py` reads only:
1. `keywords` (for matching) -- present in ProcedureDoc
2. `tramite` (via filename) -- ProcedureDoc files use the same naming
3. The full JSON dict (passed to LLM as context) -- all fields pass through

Since ProcedureDoc is a superset, `kb_lookup.py` works without modification. New fields are simply additional context for the LLM.

---

## Field Validation Rules

### Required Fields -- Reject if Missing

| Field | Format Constraint |
|-------|------------------|
| `id` | Lowercase alphanumeric + hyphens: `^[a-z0-9-]+$` |
| `nombre` | Non-empty string, minimum 3 characters |
| `source_url` | Valid HTTPS URI |
| `source_type` | One of: `age`, `ccaa`, `local`, `boe` |
| `keywords` | Non-empty array, at least 1 element |
| `descripcion` | Non-empty string, minimum 10 characters |
| `idioma` | One of: `es`, `ca`, `eu`, `gl`, `en` |
| `extracted_at` | ISO 8601 datetime string |
| `content_hash` | 64-character hex string (SHA-256) |
| `word_count` | Integer >= 0 |
| `completeness_score` | Float 0.0 to 1.0 |
| `version` | Integer, must equal `1` |

### Optional Fields -- Validate Format if Present

| Field | Format Constraint |
|-------|------------------|
| `nombre_alternativo` | Array of non-empty strings |
| `source_urls` | Array of valid HTTPS URIs |
| `organismo_abrev` | Uppercase string, 2-10 characters |
| `territorio.nivel` | One of: `estatal`, `autonomico`, `local` |
| `territorio.ccaa` | Lowercase slug if nivel is `autonomico` or `local` |
| `canal` | One of: `electronico`, `presencial`, `mixto` |
| `requisitos` | Array of strings |
| `documentos_necesarios` | Array of strings |
| `base_legal` | Array of strings |
| `tags` | Array of lowercase slugs |
| `idiomas_disponibles` | Array of language codes |
| `verified_at` | ISO 8601 datetime or null |
| `verified_by` | `"manual"` or `"auto"` or null |

---

## Example: Fully Normalized ProcedureDoc for Prestacion por Desempleo

```json
{
  "version": 1,
  "id": "age-sepe-prestacion-desempleo",
  "nombre": "Prestacion por Desempleo (Paro)",
  "nombre_alternativo": [
    "Paro",
    "Cobrar el paro",
    "Prestacion contributiva por desempleo",
    "Chomage"
  ],

  "source_url": "https://www.sepe.es/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html",
  "source_urls": [
    "https://www.sepe.es/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html",
    "https://sede.sepe.gob.es/portalSede/flows/tramiteSolicitud"
  ],
  "source_type": "age",

  "organismo": "SEPE (Servicio Publico de Empleo Estatal)",
  "organismo_abrev": "SEPE",

  "territorio": {
    "nivel": "estatal",
    "ccaa": null,
    "municipio": null,
    "provincia": null
  },

  "canal": "mixto",

  "descripcion": "Prestacion economica para personas que han perdido su empleo de forma involuntaria y han cotizado un minimo de 360 dias en los ultimos 6 anos. Cubre una parte del salario anterior durante un periodo proporcional al tiempo cotizado.",

  "requisitos": [
    "Estar afiliado y en situacion de alta (o asimilada) en la Seguridad Social en un regimen que contemple la prestacion por desempleo",
    "Encontrarse en situacion legal de desempleo (despido, fin de contrato temporal, ERE, etc.)",
    "Haber cotizado un minimo de 360 dias dentro de los 6 anos anteriores a la situacion legal de desempleo",
    "No haber cumplido la edad ordinaria de jubilacion",
    "Estar inscrito como demandante de empleo en el SEPE y mantener dicha inscripcion durante todo el periodo de prestacion",
    "Suscribir el compromiso de actividad (buscar empleo activamente y aceptar colocacion adecuada)",
    "No estar realizando trabajo por cuenta ajena a jornada completa ni por cuenta propia"
  ],

  "documentos_necesarios": [
    "DNI o NIE en vigor",
    "Certificado de empresa (lo emite el empleador y suele llegar al SEPE de forma telematica)",
    "Documento de afiliacion a la Seguridad Social (numero de afiliacion)",
    "Justificante de inscripcion como demandante de empleo (DARDE)",
    "Documento bancario con el numero de cuenta (IBAN) donde cobrar la prestacion",
    "Libro de familia o documento acreditativo de hijos a cargo (si aplica, para incremento de cuantia minima)"
  ],

  "plazos": "15 dias habiles desde la situacion legal de desempleo (ultimo dia de trabajo efectivo). Si se solicita fuera de plazo, se pierde un dia de prestacion por cada dia de retraso.",

  "tasas": null,

  "base_legal": [
    "Real Decreto Legislativo 8/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley General de la Seguridad Social (arts. 262-282)",
    "Ley 31/1984, de 2 de agosto, de proteccion por desempleo"
  ],

  "como_solicitar": {
    "online": "Sede electronica del SEPE (sede.sepe.gob.es). Tramite 'Solicitud de prestacion contributiva'. Requiere certificado digital, cl@ve permanente o DNI electronico.",
    "presencial": "Oficinas de prestaciones del SEPE. Solicitar cita previa en sede.sepe.gob.es o llamando al 919 26 79 70. Cita previa obligatoria.",
    "telefono": "Llamar al 919 26 79 70 para solicitar cita previa. Informacion general: 901 119 999."
  },

  "donde_solicitar": {
    "urls": [
      "https://sede.sepe.gob.es/portalSede/flows/tramiteSolicitud"
    ],
    "direcciones": [
      "Oficinas de prestaciones del SEPE (consultar directorio en sepe.es)"
    ],
    "cita_previa_url": "https://sede.sepe.gob.es/portalSede/flows/tramiteCitaPrevia"
  },

  "keywords": [
    "paro", "desempleo", "sepe", "prestacion desempleo", "cobrar paro",
    "despido", "cotizacion", "demandante empleo", "inem",
    "subsidio desempleo", "chomage", "allocation chomage"
  ],
  "tags": [
    "empleo", "prestacion-contributiva", "sepe", "seguridad-social",
    "despido", "fin-contrato"
  ],

  "idioma": "es",
  "idiomas_disponibles": ["es"],

  "extracted_at": "2026-02-18T10:00:00Z",
  "verified_at": "2026-02-18T10:00:00Z",
  "verified_by": "manual",

  "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "word_count": 1250,
  "completeness_score": 0.92,

  "version": 1
}
```

---

## Migration Path from Current KB Format to ProcedureDoc

### Step 1: Audit Existing Files

Inventory all 8 files in `data/tramites/` and map each field to the ProcedureDoc schema (see backward compatibility table above).

### Step 2: Generate ProcedureDoc Versions

For each existing file, produce a ProcedureDoc by:
1. Copying all existing fields as-is (they remain valid).
2. Adding new required fields: `id`, `version`, `source_url` (from `fuente_url`), `source_type`, `territorio`, `canal`, `idioma`, `extracted_at`, `content_hash`, `word_count`, `completeness_score`.
3. Renaming `documentos` to `documentos_necesarios` (keep `documentos` as alias).
4. Adding `organismo_abrev` extracted from `organismo`.
5. Computing `completeness_score` via the formula above.

### Step 3: Store in Parallel

```
data/
  tramites/                     # <-- UNCHANGED, existing 8 files
    prestacion_desempleo.json
    imv.json
    ...
  ingested/                     # <-- NEW, pipeline output
    procedures/
      age-sepe-prestacion-desempleo.json
      age-inss-imv.json
      ...
```

Both directories are valid sources for `kb_lookup.py`. The existing `data/tramites/` files take priority for the same procedure (manually verified > auto-extracted).

### Step 4: Migration Script (Pseudocode)

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime

TRAMITES_DIR = Path("data/tramites")
OUTPUT_DIR = Path("data/ingested/procedures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Map organismo text to abbreviation and source_type
ORG_MAP = {
    "SEPE": {"abrev": "SEPE", "source_type": "age", "nivel": "estatal"},
    "Seguridad Social": {"abrev": "INSS", "source_type": "age", "nivel": "estatal"},
    "Ayuntamiento": {"abrev": None, "source_type": "local", "nivel": "local"},
    # ... extend as needed
}

def migrate_tramite(filepath: Path) -> dict:
    with open(filepath) as f:
        old = json.load(f)

    tramite = old.get("tramite", filepath.stem)
    organismo = old.get("organismo", "")
    org_info = lookup_org(organismo)

    # Build new ProcedureDoc
    doc = {
        "version": 1,
        "id": f"{org_info['source_type']}-{org_info['abrev'] or 'unknown'}-{tramite}".lower(),
        "nombre": old.get("nombre", ""),
        "nombre_alternativo": [],
        "source_url": old.get("fuente_url", ""),
        "source_urls": [old.get("fuente_url", "")],
        "source_type": org_info["source_type"],
        "organismo": organismo,
        "organismo_abrev": org_info["abrev"],
        "territorio": {
            "nivel": org_info["nivel"],
            "ccaa": None,
            "municipio": None,
            "provincia": None,
        },
        "canal": detect_canal(old),
        "descripcion": old.get("descripcion", ""),
        "requisitos": old.get("requisitos", []),
        "documentos_necesarios": flatten_documentos(old),
        "plazos": old.get("plazos"),
        "tasas": None,
        "base_legal": [],
        "como_solicitar": old.get("como_solicitar", old.get("como_hacerlo_madrid", "")),
        "donde_solicitar": {
            "urls": [old.get("fuente_url", "")],
            "direcciones": [],
            "cita_previa_url": None,
        },
        "keywords": old.get("keywords", []),
        "tags": [],
        "idioma": "es",
        "idiomas_disponibles": ["es"],
        "extracted_at": datetime.utcnow().isoformat() + "Z",
        "verified_at": old.get("fecha_verificacion"),
        "verified_by": "manual" if old.get("verificado") else None,
        "content_hash": compute_hash(old),
        "word_count": count_words(old),
        "completeness_score": calculate_completeness(doc),
    }

    # Preserve legacy fields for backward compat
    for legacy_field in ["cuantias", "cuantias_2024", "duracion",
                         "datos_importantes", "telefono", "tramite",
                         "fuente_url", "verificado", "fecha_verificacion"]:
        if legacy_field in old:
            doc[legacy_field] = old[legacy_field]

    return doc

def flatten_documentos(old: dict) -> list[str]:
    """Handle both list and dict formats of documentos field."""
    docs = old.get("documentos", old.get("documentos_necesarios", []))
    if isinstance(docs, list):
        return docs
    if isinstance(docs, dict):
        result = []
        for category, items in docs.items():
            for item in items:
                result.append(f"[{category}] {item}")
        return result
    return []

def detect_canal(old: dict) -> str:
    como = old.get("como_solicitar", [])
    if isinstance(como, list):
        vias = [c.get("via", "").lower() for c in como]
        has_online = any("online" in v for v in vias)
        has_presencial = any("presencial" in v for v in vias)
        if has_online and has_presencial:
            return "mixto"
        if has_online:
            return "electronico"
        return "presencial"
    return "mixto"

def compute_hash(doc: dict) -> str:
    text = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def count_words(doc: dict) -> int:
    text_fields = ["descripcion", "requisitos", "datos_importantes"]
    total = 0
    for field in text_fields:
        val = doc.get(field, "")
        if isinstance(val, str):
            total += len(val.split())
        elif isinstance(val, list):
            total += sum(len(str(item).split()) for item in val)
    return total
```

### Step 5: Validate and Deploy

1. Run migration script on all 8 files.
2. Validate each output against the JSON Schema (see below).
3. Verify `kb_lookup.py` loads both `data/tramites/` and `data/ingested/procedures/` correctly.
4. Run existing eval suite to confirm no regressions.

---

## JSON Schema for Validation

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ProcedureDoc v1",
  "type": "object",
  "required": [
    "version", "id", "nombre", "source_url", "source_type",
    "descripcion", "keywords", "idioma", "extracted_at",
    "content_hash", "word_count", "completeness_score"
  ],
  "properties": {
    "version": { "type": "integer", "const": 1 },
    "id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
    "nombre": { "type": "string", "minLength": 3 },
    "nombre_alternativo": { "type": "array", "items": { "type": "string" } },
    "source_url": { "type": "string", "format": "uri" },
    "source_urls": { "type": "array", "items": { "type": "string", "format": "uri" } },
    "source_type": { "type": "string", "enum": ["age", "ccaa", "local", "boe"] },
    "organismo": { "type": "string" },
    "organismo_abrev": { "type": "string" },
    "territorio": {
      "type": "object",
      "properties": {
        "nivel": { "type": "string", "enum": ["estatal", "autonomico", "local"] },
        "ccaa": { "type": ["string", "null"] },
        "municipio": { "type": ["string", "null"] },
        "provincia": { "type": ["string", "null"] }
      }
    },
    "canal": { "type": "string", "enum": ["electronico", "presencial", "mixto"] },
    "descripcion": { "type": "string", "minLength": 10 },
    "requisitos": { "type": "array", "items": { "type": "string" } },
    "documentos_necesarios": { "type": "array", "items": { "type": "string" } },
    "plazos": {},
    "tasas": { "type": ["string", "null"] },
    "base_legal": { "type": "array", "items": { "type": "string" } },
    "como_solicitar": {},
    "donde_solicitar": {
      "type": "object",
      "properties": {
        "urls": { "type": "array", "items": { "type": "string" } },
        "direcciones": { "type": "array", "items": { "type": "string" } },
        "cita_previa_url": { "type": ["string", "null"] }
      }
    },
    "keywords": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "tags": { "type": "array", "items": { "type": "string" } },
    "idioma": { "type": "string", "enum": ["es", "ca", "eu", "gl", "en"] },
    "idiomas_disponibles": { "type": "array", "items": { "type": "string" } },
    "extracted_at": { "type": "string", "format": "date-time" },
    "verified_at": { "type": ["string", "null"], "format": "date-time" },
    "verified_by": { "type": ["string", "null"] },
    "content_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "word_count": { "type": "integer", "minimum": 0 },
    "completeness_score": { "type": "number", "minimum": 0, "maximum": 1 }
  }
}
```
