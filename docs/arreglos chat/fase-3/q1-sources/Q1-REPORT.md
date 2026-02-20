# Q1/4 Report — RAG Source-of-Truth Layer

> **Date:** 2026-02-18
> **Status:** RESEARCH COMPLETE (documentation only -- validation, HTTP checks, and API testing deferred to Q2)
> **Scope:** First quarter of 4-quarter RAG universal system for Spanish government procedures

---

## Executive Summary

Q1 establishes the knowledge foundation for Clara's RAG system: a comprehensive catalog of official Spanish government sources at all three administrative levels (central, regional, local), plus the technical specifications for ingesting, normalizing, and governing that content.

**Key deliverables:**
- **25 AGE sources** documented (10 P0, 11 P1, 4 P2) including BOE API, SIA/PAG master catalog, and all critical sedes electronicas
- **19/19 CCAA profiles** with sede electronica URLs, procedure catalogs, and priority rankings
- **20 municipal sedes** verified (Tier 1 top cities by population), plus 4-tier coverage strategy for 8,131 municipalities
- **Domain governance** framework: 3-tier allowlist, blocklist, canonicalization (10 rules), and link health checker spec
- **Ingestion pipeline** design: 6-stage process (discovery → fetch → extract → normalize → store → index) with ProcedureDoc v1 schema

**No src/ production code was written.** All Q1 output is research documentation (Q1.1 added validation scripts and data artifacts) that feeds directly into Q2 implementation.

---

## Source Registries

### AGE (Central Government) — 25 Sources

| Priority | Count | Examples |
|----------|-------|---------|
| P0 (Essential) | 10 | SIA/PAG, BOE (API), SEPE, Seg Social, AEAT, Extranjeria, IMV |
| P1 (Important) | 11 | Clave, DGT, IMSERSO, MIVAU, Min. Justicia, datos.gob.es |
| P2 (Secondary) | 4 | MUFACE, INE (API), Catastro (API), Transparencia |

**Top APIs discovered:**
- BOE REST API — daily summaries, consolidated legislation (no auth, XML/JSON)
- INE JSON API — statistical data, IPREM/SMI thresholds
- datos.gob.es CKAN API — national open data catalog
- Catastro SOAP/WFS — property data

Full details: [`source-registry/age.md`](source-registry/age.md)

### CCAA (Autonomous Communities) — 19/19

| Priority | Communities |
|----------|-----------|
| P0 (Critical) | Madrid, Cataluna, Andalucia, Comunitat Valenciana, Canarias |
| P1 (Medium) | Pais Vasco, Castilla y Leon, Castilla-La Mancha, Galicia, Murcia, Aragon, Illes Balears, Extremadura |
| P2 (Lower) | Asturias, Navarra, Cantabria, La Rioja, Ceuta, Melilla |

Co-official languages noted: Catalan (4 CCAA), Basque (2), Galician (1), Valencian (1), Aranes (1).

Full details: [`source-registry/ccaa.md`](source-registry/ccaa.md)

### Local (Municipal) — 4-Tier Strategy

| Tier | Coverage | Method | Count |
|------|----------|--------|-------|
| Tier 1 (P0) | Top 20 cities | Manual curation, verified URLs | 20 cities |
| Tier 2 (P1) | Provincial capitals + cities 21-50 | Semi-automated via DIR3/PAG | ~50 cities |
| Tier 3 (P2) | Cities >50k inhabitants | Automated with validation | ~100 cities |
| Tier 4 (deferred) | Remaining ~7,900 municipalities | Directory fallback (DIR3, Diputaciones) | n/a |

**Disambiguation strategy:** Bot asks municipality only for municipal-level procedures (empadronamiento, IBI, etc.). Decision tree + fallback chain documented.

Full details: [`source-registry/local.md`](source-registry/local.md)

---

## Link Governance

### Domain Allowlist
- **Tier 1 (AGE):** `*.gob.es` auto-allowed + 22 explicit domains
- **Tier 2 (CCAA):** 19 community domain patterns
- **Tier 3 (Municipal):** 20 municipal domains, on-demand expansion
- **Blocklist:** Commercial sites, SEO farms, forums, social media, unofficial aggregators
- **Default policy:** REJECT (allowlist-first)

Full details: [`link-governance/allowlist.md`](link-governance/allowlist.md)

### URL Canonicalization
10 rules covering: HTTPS normalization, trailing slashes, tracking param stripping, fragment removal, www normalization, case handling, redirect following, session param stripping, pagination, language variants.

Full details: [`link-governance/canonicalization.md`](link-governance/canonicalization.md)

### Link Health Checker
Automated monitoring: daily (P0), weekly (P1), monthly (P2). HTTP HEAD + SSL check + content hash comparison. Alert after 3 consecutive failures, remove after 7 days down.

Full details: [`link-governance/link-checking-spec.md`](link-governance/link-checking-spec.md)

---

## Ingestion Pipeline

### 6-Stage Design

```
Discovery --> Fetch --> Extract --> Normalize --> Store --> Index
  sitemaps    HTTP GET   trafilatura  ProcedureDoc  JSON files  keyword +
  RSS/API     rate-limit pdfplumber   schema v1     raw archive metadata
  crawl       retry/cache BOE XML     section split catalog     (Q2: vectors)
```

- **Discovery:** sitemaps, RSS, API catalogs (SIA/PAG, BOE), polite crawling, manual seed list
- **Fetch:** 1 req/sec default, conditional requests (ETag/If-Modified-Since), retry with backoff
- **Extract:** trafilatura (HTML), pdfplumber (PDF), custom BOE XML parser. Quality gates: min 50 words, language check, encoding, structure
- **Normalize:** Section detection via Spanish heading patterns, metadata inference from domain/breadcrumbs, text cleaning, deduplication
- **Store:** `data/ingested/procedures/<id>.json` + `data/ingested/raw/<domain>/<hash>` + `catalog.json`
- **Index:** Keyword-based (extends current kb_lookup.py), metadata tags for filtering. Bridges to Q2 vector embeddings.

Full details: [`ingestion/ingestion-playbook.md`](ingestion/ingestion-playbook.md), [`ingestion/extraction-spec.md`](ingestion/extraction-spec.md)

### ProcedureDoc v1 Schema

29 fields covering: identification, source metadata, territory, content sections (descripcion, requisitos, documentos, plazos, tasas, base_legal, como_solicitar, donde_solicitar), keywords, language, provenance, quality metrics.

Backward compatible with existing `data/tramites/*.json`. Migration path documented with pseudocode.

Full details: [`ingestion/normalization-schema.md`](ingestion/normalization-schema.md)

---

## Gates

| Gate | Criteria | Status |
|------|----------|--------|
| G1 | AGE >= 20 sources | **PASS** (25) |
| G2 | CCAA = 19/19 | **PASS** (19/19) |
| G3 | Local seed >= 20 cities | **PASS** (20) |
| G4 | Allowlist complete (3 tiers + blocklist) | **PASS** |
| G5 | Ingestion playbook covers 4+ stages | **PASS** (6 stages) |
| G6 | ProcedureDoc schema defined | **PASS** |

All 4 abort conditions cleared (A3 flagged as concern in forensic audit due to 14 allowlist coverage gaps). See [`evidence/gates.md`](evidence/gates.md).

---

## Gaps and Risks

**Top gaps (carry to Q2):**
1. No actual HTTP validation of URLs (research-only constraint)
2. BOE API not tested with real requests
3. CCAA page layouts not analyzed for extraction compatibility
4. DIR3 dataset not downloaded or parsed
5. No cost estimate for vector infrastructure

**Top risks:**
- Government website restructuring could break links (mitigated by health checker)
- Extraction quality may vary across government CMS platforms (mitigated by fallback chain)
- Municipal sede platforms are heterogeneous (mitigated by Diputacion fallback)

Full details: [`evidence/assumptions-gaps.md`](evidence/assumptions-gaps.md)

---

## Deliverables

| File | Path | Lines |
|------|------|-------|
| AGE Source Registry | `source-registry/age.md` | 518 |
| CCAA Source Registry | `source-registry/ccaa.md` | 665 |
| Local Coverage Strategy | `source-registry/local.md` | 403 |
| Domain Allowlist | `link-governance/allowlist.md` | 229 |
| URL Canonicalization | `link-governance/canonicalization.md` | 322 |
| Link Health Checker | `link-governance/link-checking-spec.md` | 545 |
| Ingestion Playbook | `ingestion/ingestion-playbook.md` | 446 |
| Extraction Spec | `ingestion/extraction-spec.md` | 739 |
| Normalization Schema | `ingestion/normalization-schema.md` | 581 |
| Q1 Backlog | `backlog/Q1-backlog.md` | — |
| Q2/Q3/Q4 Backlog | `backlog/Q2Q3Q4-backlog.md` | — |
| References | `evidence/references.md` | — |
| Assumptions & Gaps | `evidence/assumptions-gaps.md` | — |
| Quality Gates | `evidence/gates.md` | — |
| **This report** | `Q1-REPORT.md` | — |
| **Total research lines** | — | **4,448** |

---

## Next Steps (Q2)

1. **Automated URL health check** against all registries (validate research)
2. **Implement fetch + extract stages** (trafilatura + pdfplumber)
3. **BOE API integration** (daily monitoring)
4. **Migrate existing 8 KB tramites** to ProcedureDoc format
5. **Choose embedding model** and set up vector store
6. **Ingest top 20 AGE procedure pages** from real sources
7. **Upgrade retriever.py** from keyword to vector search
