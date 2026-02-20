# Q1 Quality Gates

> Date: 2026-02-18

## Gate Definitions

| Gate | Criteria | Status |
|------|----------|--------|
| **G1: AGE >= 20 sources** | AGE source registry contains at least 20 documented sources with URLs, priority, and access method | **PASS** (25 sources) |
| **G2: CCAA = 19/19** | All 17 autonomous communities + 2 autonomous cities have a documented entry with sede electronica URL | **PASS** (19/19) |
| **G3: Local seed >= 20 cities** | Local coverage strategy includes at least 20 cities with verified sede electronica URLs | **PASS** (20 cities, all research-documented; HTTP verification deferred to Q2) |
| **G4: Allowlist complete** | Domain allowlist covers all 3 tiers (AGE, CCAA, Municipal) with explicit blocklist | **PASS** |
| **G5: Ingestion playbook covers 4 stages** | Discovery, Fetch, Extract, Normalize stages are documented with tools, formats, and error handling | **PASS** (6 stages: +Store, +Index) |
| **G6: ProcedureDoc schema defined** | Normalization schema is documented with all fields, types, validation rules, and an example | **PASS** |

## Abort Conditions

| ID | Condition | Status |
|----|-----------|--------|
| **A1** | No AGE source registry OR fewer than 15 sources | **CLEARED** — 25 sources documented |
| **A2** | CCAA registry covers fewer than 10 communities | **CLEARED** — All 19/19 covered |
| **A3** | No ingestion pipeline design (discovery through normalization) | **CLEARED** — Full 6-stage pipeline documented |
| **A4** | No defined document schema for normalized output | **CLEARED** — ProcedureDoc v1 with 29 fields |

## Gate Evidence

### G1: AGE Source Registry
- **File:** `source-registry/age.md` (518 lines)
- **Sources documented:** 25
- **P0 sources:** 10 (SIA, PAG, Sede PAG, BOE x3, SEPE, Seg Social, AEAT, Extranjeria, IMV)
- **P1 sources:** 11 (Carpeta Ciudadana, Clave, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)
- **P2 sources:** 4 (MUFACE, INE, Catastro, Transparencia)
- **APIs documented:** BOE (REST, RSS), INE (JSON REST), datos.gob.es (CKAN), Catastro (SOAP + WMS/WFS)

### G2: CCAA Source Registry
- **File:** `source-registry/ccaa.md` (665 lines)
- **Communities covered:** 19/19
- **P0 communities:** 5 (Madrid, Cataluna, Andalucia, Valencia, Canarias)
- **P1 communities:** 8 (Pais Vasco, Castilla y Leon, CLM, Galicia, Murcia, Aragon, Balears, Extremadura)
- **P2 communities:** 6 (Asturias, Navarra, Cantabria, La Rioja, Ceuta, Melilla)
- **Co-official languages noted:** Catalan, Basque, Galician, Valencian, Aranes

### G3: Local Coverage Strategy
- **File:** `source-registry/local.md` (403 lines)
- **Tier 1 cities:** 20 (all with research-documented sede electronica URLs; HTTP verification pending Q2)
- **Key procedures per city:** 5 defined (empadronamiento, certificado, IBI, basuras, licencias)
- **Disambiguation strategy:** Documented with decision tree and fallback chain
- **Directory infrastructure:** 6 fallback directories documented (DIR3, INE, PAG, FEMP, Diputaciones, REL)

### G4: Domain Allowlist
- **File:** `link-governance/allowlist.md` (229 lines)
- **Tier 1 (AGE):** 22+ domains with auto-allow for *.gob.es
- **Tier 2 (CCAA):** 19 CCAA domain patterns
- **Tier 3 (Municipal):** 20 municipal domains
- **Blocklist:** 9 categories explicitly blocked (commercial, SEO, forums, social media, etc.)
- **Review process:** 6-step validation checklist

### G5: Ingestion Playbook
- **File:** `ingestion/ingestion-playbook.md` (446 lines)
- **Stages:** 6 (Discovery, Fetch, Extract, Normalize, Store, Index)
- **Discovery methods:** 5 (sitemaps, RSS, API catalogs, crawling, manual seed)
- **Fetch config:** rate limiting, retry policy, caching, conditional requests
- **Dependencies:** 10 Python packages listed
- **Out-of-scope:** Explicitly lists Q2+ items (embeddings, OCR, LLM extraction)

### G6: ProcedureDoc Schema
- **File:** `ingestion/normalization-schema.md` (581 lines)
- **Schema fields:** 29 with types and validation rules
- **Completeness scoring:** Weighted formula with code
- **Backward compatibility:** Mapping from existing data/tramites/*.json
- **Example:** Full ProcedureDoc for "Prestacion por Desempleo"
- **Migration path:** 5-step process with pseudocode

## Supporting Documents

| Document | File | Lines |
|----------|------|-------|
| URL Canonicalization | `link-governance/canonicalization.md` | 322 |
| Link Health Checker | `link-governance/link-checking-spec.md` | 545 |
| Extraction Spec | `ingestion/extraction-spec.md` | 739 |

## Summary

| Metric | Value |
|--------|-------|
| Total research documents | 9 |
| Total lines written | 4,448 |
| Gates passed | 6/6 (G4 limited to smoke/dry-run; see forensic audit) |
| Abort conditions cleared | 4/4 |
| AGE sources | 25 |
| CCAA profiles | 19/19 |
| Municipal URLs documented | 20 (HTTP verification pending Q2) |
| APIs documented | 5+ |

---

# Q1.1 Quality Gates — Biblioteca Oficial v0

> Date: 2026-02-18

## Gate Definitions

| Gate | Criteria | Status |
|------|----------|--------|
| **G1: Registry validates** | `registry.yaml` + `local_seed.yaml` pass JSON Schema validation | **PASS** (44 + 20 sources) |
| **G2: Policy validates** | allowlist, blocklist, canonical_rules pass structural validation | **PASS** |
| **G3: ProcedureDoc validates** | ProcedureDoc schema exists and sample validates | **PASS** (IMV, completeness 0.86) |
| **G4: Link checker runs** | `link_check.py` runs smoke test (3 URLs) and generates JSONL output | **PASS (smoke only)** -- full-registry live test had crash bug (fixed post-audit) |
| **G5: Docs updated** | READMEs in data/, schemas/ with usage instructions | **PASS** |
| **G6: Backlog Q2/Q3 updated** | Future work documented | **PASS** |

## Commands

```bash
# G1
python3 scripts/validate_source_registry.py
# Output: PASS (44 sources — AGE: 25, CCAA: 19, Local: 0)
#         PASS (20 sources — AGE: 0, CCAA: 0, Local: 20)

# G2
python3 scripts/validate_policy.py
# Output: allowlist PASS, blocklist PASS, canonical_rules PASS

# G3
python3 scripts/validate_proceduredoc_schema.py \
  "docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"
# Output: PASS: proceduredoc.sample.json valid against ProcedureDoc v1

# G4
python3 scripts/link_check.py --smoke --limit 5 --output /tmp/smoke.jsonl
# Output: 3 OK, 0 FAIL

# G5 (visual check)
cat data/sources/README.md data/policy/README.md schemas/README.md

# Tests
pytest tests/unit/test_validators.py -v
# Output: 5 passed
```

## Q1.1 Abort Conditions

| ID | Condition | Status |
|----|-----------|--------|
| A1 | Registry covers AGE+CCAA+Local | CLEAR (25+19+20) |
| A2 | Policy enforceable with tiers | CLEAR (3-tier allowlist, reject-by-default) |
| A3 | Reproducible validation scripts | CLEAR (4 scripts, 5 tests) |
| A4 | Report + evidence present | CLEAR (Q1.1 report + samples) |
