# Ingestion Pipeline Playbook

> **Scope:** Q1 design document -- pipeline architecture for ingesting Spanish government procedure documents into Clara's knowledge base.
> **Status:** Research / Design (no code changes)
> **Owner:** Ingestion Agent
> **Date:** 2026-02-18
> **Depends on:** AGE Source Registry, CCAA Source Registry, Link Governance
> **Feeds into:** Q2 -- vector embeddings + semantic search

---

## Overview

Clara currently serves 8 procedures from hand-curated JSON files in `data/tramites/`. This playbook defines how to scale from 8 to 200+ procedures by automating document discovery, fetching, extraction, normalization, and storage -- while keeping the system compatible with the existing `kb_lookup.py` keyword-matching retriever and the `retriever.py` abstraction layer.

The pipeline produces **ProcedureDoc JSON files** (see `normalization-schema.md`) that drop into `data/tramites/` and are automatically picked up by `_load_all_tramites()` on next restart.

```
Discovery --> Fetch --> Extract --> Normalize --> Store --> Index Metadata
   |            |          |            |           |           |
sitemaps    HTTP GET    HTML/PDF    ProcedureDoc   JSON      keyword
RSS feeds   rate-limit  BOE XML     schema        files     index
APIs        retry       forms       cleaning      raw       metadata
crawl       cache       OCR flag    lang detect   archive   tags
seeds
```

---

## Stage 1: Discovery

### 1.1 Sitemaps

Most sedes electronicas publish `sitemap.xml` at their root. This is the primary discovery mechanism.

| Source Type | Sitemap Pattern | Example |
|---|---|---|
| AGE Ministerios | `https://{sede}.gob.es/sitemap.xml` | `sede.sepe.gob.es/sitemap.xml` |
| CCAA sedes | `https://{sede}.{ccaa}.es/sitemap.xml` | `sede.comunidad.madrid/sitemap.xml` |
| Ayuntamientos | `https://www.{municipio}.es/sitemap.xml` | `www.madrid.es/sitemap.xml` |
| BOE | `https://www.boe.es/sitemap.xml` | Standard XML sitemap |

**Process:**
1. Fetch `sitemap.xml` (may reference sitemap index files linking to sub-sitemaps)
2. Parse with `xml.etree.ElementTree` or `lxml`
3. Filter URLs by path patterns that indicate procedures (e.g., `/tramites/`, `/procedimientos/`, `/servicios/`)
4. Extract `<lastmod>` for change detection
5. Store discovered URLs in a `discovery_queue` JSON

**Frequency:** Weekly scan for new URLs, daily check of `<lastmod>` for changes.

### 1.2 RSS Feeds

Some sources publish RSS feeds for new or updated procedures.

| Source | Feed URL | Content |
|---|---|---|
| BOE | `https://www.boe.es/rss/` | New publications by section |
| Some CCAA | Varies by community | New procedures/convocatorias |
| SIA Catalog | Not RSS, but API-based | Updated procedure registry |

**Process:**
1. Poll RSS feeds daily
2. Parse with `feedparser` library
3. Extract entry URLs and publication dates
4. Cross-reference with existing URL index to detect new content
5. Add new URLs to discovery queue

### 1.3 API Catalogs

Structured data sources that provide procedure metadata directly.

| API | Description | Format |
|---|---|---|
| SIA (Sistema de Informacion Administrativa) | National catalog of all AGE procedures | REST JSON |
| PAG (Punto de Acceso General) | administracion.gob.es procedure listings | HTML + structured data |
| BOE Open Data | `https://boe.es/datosabiertos/` | XML/JSON |
| datos.gob.es | Open data portal | CKAN API |

**Process for SIA/PAG:**
1. Query the SIA API for procedure listings by organism
2. Extract procedure metadata (name, organism, territory, status)
3. Follow links to the canonical sede electronica page for full content
4. Store API response as supplementary metadata

### 1.4 Crawling (Fallback)

For sites without sitemaps or APIs, use polite depth-limited crawling.

**Rules:**
- Respect `robots.txt` -- always check before crawling
- Maximum depth: 3 levels from seed URL
- Maximum pages per domain per session: 500
- Stay within the same domain (no external link following)
- Detect and skip duplicate content (URL normalization + content hashing)
- Identify procedure pages by URL patterns and content markers (e.g., "Requisitos", "Documentacion necesaria", "Plazo")

**Crawl politeness:**
- 1 request per second per domain (configurable, default conservative)
- Identify with `User-Agent: CivicAid-Clara/1.0 (+https://github.com/civicaid; research-only)`
- Honor `Crawl-delay` from `robots.txt`

### 1.5 Manual Seed List

The initial 8 tramites already in the KB serve as the seed:

| File | Procedure | Source URL |
|---|---|---|
| `prestacion_desempleo.json` | Prestacion por Desempleo | sepe.es |
| `imv.json` | Ingreso Minimo Vital | seg-social.es |
| `empadronamiento.json` | Empadronamiento | madrid.es |
| `tarjeta_sanitaria.json` | Tarjeta Sanitaria | comunidad.madrid |
| `nie_tie.json` | NIE/TIE | inclusion.gob.es |
| `ayuda_alquiler.json` | Ayuda al Alquiler | mivau.gob.es |
| `certificado_discapacidad.json` | Certificado Discapacidad | comunidad.madrid |
| `justicia_gratuita.json` | Justicia Gratuita | mjusticia.gob.es |

These already have `fuente_url` fields pointing to the official source page. They serve as ground truth for validating the extraction pipeline -- any automated extraction of these pages should produce results consistent with the existing curated data.

---

## Stage 2: Fetch

### 2.1 HTTP Configuration

```yaml
fetch_config:
  user_agent: "CivicAid-Clara/1.0 (+https://github.com/civicaid; research-only)"
  timeout_connect: 30   # seconds
  timeout_read: 60      # seconds
  max_retries: 3
  retry_backoff_base: 2  # exponential: 2s, 4s, 8s
  max_redirects: 5
  verify_ssl: true
```

### 2.2 Rate Limiting

- **Default:** 1 request per second per domain
- **Configurable per domain** in a `rate_limits.yaml` file for domains that require slower access
- Implement via `time.sleep()` between requests to same domain, or use a token-bucket approach
- Separate queues per domain so one slow domain does not block others

### 2.3 Retry Policy

| HTTP Status | Action |
|---|---|
| 200 | Success -- proceed to extraction |
| 301/302 | Follow redirect (up to 5 hops) |
| 304 | Not Modified -- skip extraction, content unchanged |
| 403 | Log warning, backoff 60s, retry once, then skip |
| 429 | Read `Retry-After` header, wait, retry (max 3 times) |
| 5xx | Retry with exponential backoff (2s, 4s, 8s), then skip |
| Timeout | Retry once with doubled timeout, then skip |

### 2.4 Conditional Requests

To avoid re-fetching unchanged content:

1. On first fetch, store `ETag` and `Last-Modified` response headers alongside the raw content
2. On subsequent fetches, send `If-None-Match` (with stored ETag) and `If-Modified-Since` (with stored Last-Modified)
3. If server returns 304 Not Modified, skip extraction
4. If server does not support conditional requests, use content hashing (SHA-256 of response body) to detect changes

### 2.5 Raw Storage

Store every raw response for provenance:

```
data/raw/
  {domain}/
    {url_hash}.html        # raw HTML body
    {url_hash}.meta.json   # headers, status code, ETag, Last-Modified, fetched_at
    {url_hash}.pdf         # raw PDF (if applicable)
```

- `url_hash` = SHA-256 of the canonical URL (first 16 hex chars)
- Keep last 2 versions for diff detection
- Total raw storage estimate: ~500 MB for 200 procedures (HTML is small, PDFs can be larger)

---

## Stage 3: Extract

Detailed in `extraction-spec.md`. Summary of document types and tools:

| Document Type | Primary Tool | Fallback | Output |
|---|---|---|---|
| HTML web pages | `trafilatura` | `beautifulsoup4` | Clean markdown |
| PDF with text | `pdfplumber` | `pymupdf` (fitz) | Text + tables as markdown |
| PDF scanned | Flag for OCR | Deferred to Q2 | Placeholder with flag |
| BOE XML | `xml.etree` | `lxml` | Structured text |
| HTML forms | `beautifulsoup4` | -- | Field list + labels |
| PDF forms | `pdfplumber` | `pymupdf` | Field list + labels |
| DOCX/ODT | `python-docx` | `odfpy` | Clean text |

### 3.1 Content Quality Check (post-extraction)

After extracting text, run a basic quality check:

- **Minimum word count:** 50 words (below this, likely an error page or redirect)
- **Language check:** Detect language with `langdetect` -- should be `es` (or `ca`, `eu`, `gl` for regional content)
- **Structure markers:** Presence of key terms like "requisitos", "documentacion", "plazo", "solicitar" -- at least 2 of these should appear for a procedure page
- **Encoding:** Verify UTF-8, fix mojibake if detected

---

## Stage 4: Normalize

Transform raw extracted text into the **ProcedureDoc** schema (see `normalization-schema.md`).

### 4.1 Section Detection

Procedures on Spanish government sites follow common structural patterns. Use heuristic heading detection:

| Section | Common Headings Found in Source Pages |
|---|---|
| `nombre` | Page `<h1>`, `<title>`, "Denominacion del tramite" |
| `descripcion` | "Objeto", "Descripcion", "En que consiste", "Que es" |
| `requisitos` | "Requisitos", "Quien puede solicitarlo", "Beneficiarios" |
| `documentos_necesarios` | "Documentacion", "Documentos necesarios", "Que necesitas" |
| `plazos` | "Plazo", "Cuando solicitarlo", "Plazos de presentacion" |
| `tasas` | "Tasas", "Coste", "Precio", "Gratuito" |
| `como_solicitar` | "Como solicitarlo", "Tramitacion", "Donde presentar" |
| `donde_solicitar` | "Lugar de presentacion", "Oficinas", "Presencial" |
| `base_legal` | "Normativa", "Legislacion", "Base legal", "Regulacion" |

**Algorithm:**
1. Split extracted text at headings (markdown `##` or `###`)
2. Match heading text (lowercased, accent-stripped) against the patterns above
3. Map matched sections to ProcedureDoc fields
4. Content that does not match any pattern goes into a `datos_adicionales` overflow field

### 4.2 Metadata Detection

Extract metadata from the page and URL:

| Field | Detection Method |
|---|---|
| `organismo` | From page header/logo, breadcrumb, or URL domain |
| `territorio.nivel` | From URL domain: `.gob.es` = estatal, `.ccaa.es` = autonomico, `.municipio.es` = local |
| `territorio.ccaa` | From URL domain or explicit text on page |
| `canal` | Detect "sede electronica" (electronico), "presencial" keywords, or both (mixto) |
| `idioma` | `langdetect` on extracted text body |

### 4.3 Text Cleaning

1. **Whitespace:** Collapse multiple spaces/newlines into single space; preserve paragraph breaks
2. **Encoding:** Normalize to UTF-8 NFC; fix common mojibake patterns (`Ã±` -> `n`, `Ã©` -> `e`, etc.)
3. **Unicode:** Normalize to NFC form (consistent with `_normalize()` in `kb_lookup.py` which uses NFKD for search)
4. **HTML entities:** Decode any remaining `&amp;`, `&nbsp;`, etc.
5. **Boilerplate removal:** Strip repeated legal disclaimers, accessibility statements, cookie notices
6. **Deduplication:** If the same paragraph appears multiple times (common in CMS-generated pages), keep only the first occurrence

### 4.4 Language Detection

Use `langdetect` or `lingua-py` to tag the primary language:

| Code | Language | Where Found |
|---|---|---|
| `es` | Castellano | All AGE, most CCAA, most local |
| `ca` | Catalan/Valenciano | Cataluna, Baleares, Valencia |
| `eu` | Euskera | Pais Vasco, Navarra |
| `gl` | Gallego | Galicia |
| `en` | English | Some AGE pages have English versions |

If a page is bilingual (common in Cataluna, Pais Vasco), tag the dominant language and note the secondary language in metadata.

### 4.5 Keyword Generation

Auto-generate `keywords` field (compatible with `kb_lookup.py`'s keyword matching):

1. Extract from `nombre` field: split into meaningful terms
2. Include `organismo` name and common abbreviations (e.g., "SEPE", "IMV")
3. Include colloquial terms people use to search (e.g., "paro" for "prestacion por desempleo")
4. Include the `tramite` ID slug itself
5. For known tramites, supplement with manually curated synonyms

---

## Stage 5: Store

### 5.1 Directory Structure

```
data/
  tramites/                    # <-- ProcedureDoc JSON files (production)
    prestacion_desempleo.json  #     existing curated files
    imv.json
    ...
    {new_tramite_id}.json      #     new auto-ingested files
  raw/                         # <-- raw fetched content (provenance)
    {domain}/
      {url_hash}.html
      {url_hash}.meta.json
  extracted/                   # <-- intermediate extracted text (debugging)
    {tramite_id}.extracted.json
  ingestion/                   # <-- pipeline state and logs
    discovery_queue.json
    fetch_log.json
    ingestion_catalog.json
```

### 5.2 ProcedureDoc JSON Format

Files in `data/tramites/` follow the ProcedureDoc schema from `normalization-schema.md`. Key compatibility requirements:

- **Must have `keywords` field** (list of strings) -- this is how `kb_lookup.py` discovers the file
- **Must have `tramite` field** (string) -- used as the lookup key
- **Must have `nombre` field** (string) -- displayed to users
- **Must have `fuente_url` field** (string) -- source attribution
- File name must match `tramite` field value: `{tramite}.json`

### 5.3 Ingestion Catalog

A single `ingestion_catalog.json` tracks all ingested documents:

```json
{
  "last_updated": "2026-02-18T12:00:00Z",
  "total_documents": 42,
  "documents": [
    {
      "tramite_id": "prestacion_desempleo",
      "source_url": "https://www.sepe.es/...",
      "source_domain": "sepe.es",
      "source_type": "age",
      "extracted_at": "2026-02-15T10:30:00Z",
      "last_verified_at": "2026-02-18T10:30:00Z",
      "content_hash": "a1b2c3d4...",
      "word_count": 1250,
      "section_count": 8,
      "completeness_score": 0.85,
      "verification_status": "manual",
      "ingestion_method": "seed"
    }
  ]
}
```

---

## Stage 6: Index Metadata (Pre-Vector)

### 6.1 Keyword Index

Maintains compatibility with the current `kb_lookup.py` system:

- Every `data/tramites/*.json` file with a `keywords` field is auto-loaded by `_load_all_tramites()` at import time
- The `_detect_tramite()` function matches user queries against these keywords using accent-normalized substring matching
- **No changes needed** to `kb_lookup.py` -- new JSON files are picked up automatically

### 6.2 Metadata Tags for Filtering

The ingestion catalog enables filtering by:

- **Territory:** `estatal`, `autonomico` (with CCAA), `local` (with municipio)
- **Organism:** SEPE, Seguridad Social, Ayuntamiento de Madrid, etc.
- **Procedure type:** prestacion, certificado, inscripcion, solicitud, etc.
- **Channel:** presencial, electronico, mixto
- **Language:** es, ca, eu, gl

This filtering capability bridges to Q2 where the `VectorRetriever` (currently stubbed in `retriever.py`) will use these metadata tags as pre-filters before semantic search.

### 6.3 Bridge to Q2 Vector Search

The current `retriever.py` defines the `Retriever` ABC with a `JSONKBRetriever` and a commented-out `VectorRetriever`. The ingestion pipeline feeds both:

1. **Q1 (now):** ProcedureDoc JSON files feed `JSONKBRetriever` via `kb_lookup.py`
2. **Q2 (next):** The same JSON files will be embedded into a FAISS/ChromaDB index, and `VectorRetriever` will be implemented
3. **Transition:** The `get_retriever()` factory in `retriever.py` will switch based on `config.RAG_ENABLED` flag

---

## Pipeline Orchestration

### Scheduling

| Task | Frequency | Trigger |
|---|---|---|
| Sitemap scan | Weekly | Cron / scheduled task |
| RSS poll | Daily | Cron / scheduled task |
| Re-fetch known URLs | Weekly | Conditional requests (ETag/Last-Modified) |
| Full re-extraction | Monthly | Force re-process all stored raw content |
| Manual seed addition | On demand | Developer adds URL to seed list |

### Error Handling

| Error | Action | Recovery |
|---|---|---|
| Fetch fails (network) | Retry 3x with backoff, then mark URL as `fetch_failed` | Retry next cycle |
| Extraction produces empty text | Mark as `extraction_failed`, log URL and HTTP status | Manual review queue |
| Schema validation fails | Store extracted text but mark as `normalization_failed` | Manual mapping review |
| Duplicate content detected | Skip, log as `duplicate` with reference to existing document | No action needed |
| Language is not Spanish | Store with correct language tag, skip if language is unexpected | Review for multilingual pages |

### Quality Metrics

Track per ingestion run:

- Documents discovered (new URLs found)
- Documents fetched (successful HTTP 200)
- Documents extracted (non-empty text output)
- Documents normalized (valid ProcedureDoc JSON produced)
- Documents stored (written to `data/tramites/`)
- Completeness score distribution (histogram of field coverage)
- Errors by category (fetch, extract, normalize)

---

## Dependencies and Tools

### Python Libraries

| Library | Purpose | Stage |
|---|---|---|
| `requests` | HTTP fetching | Fetch |
| `trafilatura` | Main content extraction from HTML | Extract |
| `beautifulsoup4` | HTML parsing fallback, form extraction | Extract |
| `pdfplumber` | PDF text and table extraction | Extract |
| `pymupdf` (fitz) | Fast PDF text extraction | Extract |
| `feedparser` | RSS feed parsing | Discovery |
| `langdetect` | Language detection | Normalize |
| `python-docx` | DOCX extraction (if encountered) | Extract |
| `lxml` | XML parsing (BOE, sitemaps) | Discovery, Extract |
| `hashlib` | Content hashing (SHA-256) | Fetch, Store |

### External Services

| Service | Usage | Auth |
|---|---|---|
| SIA API | Procedure catalog queries | Public (no auth) |
| BOE Open Data | Structured legal text | Public (no auth) |
| datos.gob.es | Open data catalog | Public (API key optional) |

---

## Security and Compliance

- **No PII processing:** Procedure documents are public information; no personal data is ingested
- **robots.txt compliance:** Always check and honor robots.txt directives
- **Rate limiting:** Conservative defaults (1 req/s) to avoid overloading government servers
- **Attribution:** Every ProcedureDoc includes `fuente_url` and `source_domain` for source attribution
- **Cache control:** Respect `Cache-Control` and `Expires` headers
- **No credential storage:** All sources are public; no login or API keys for government sites
- **Data retention:** Raw content retained for provenance; extracted content versioned with timestamps
