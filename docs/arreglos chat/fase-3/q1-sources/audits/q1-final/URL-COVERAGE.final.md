# URL Coverage Audit — Q1 Final Close-Out

**Generated:** 2026-02-19 13:00
**Verdict:** PASS
**Auditor:** A4 (automated)

---

## Scope A — Enforcement (data files only)

**Files scanned:** 5

| Metric | Count |
|--------|------:|
| Raw URL matches | 184 |
| Template/artifact URLs skipped | 0 |
| Bare protocol skipped | 0 |
| Example domain skipped | 3 |
| **Unique analyzable URLs** | **149** |
| COVERED | 149 |
| NOT_COVERED | 0 |
| GOV_NOT_COVERED | 0 |
| NON_GOV_REF | 0 |

### Tier Breakdown (covered URLs)

| Tier | Count |
|------|------:|
| T1 (AGE) | 55 |
| T2 (CCAA) | 66 |
| T3 (Municipal) | 28 |

### GOV_NOT_COVERED: 0 (PASS)

### NON_GOV_REF: 0

### Skipped Example Domain URLs

- `http://example.es`
- `https://example.gob.es/tramite%20con%20espacios`
- `https://example.gob.es/tramite`

---

## Scope B — Docs+Data (enforcement + q1-sources/*.md)

**Files scanned:** 22

| Metric | Count |
|--------|------:|
| Raw URL matches | 559 |
| Template/artifact URLs skipped | 3 |
| Bare protocol skipped | 1 |
| Example domain skipped | 3 |
| **Unique analyzable URLs** | **268** |
| COVERED | 257 |
| NOT_COVERED | 11 |
| GOV_NOT_COVERED | 0 |
| NON_GOV_REF | 11 |

### Tier Breakdown (covered URLs)

| Tier | Count |
|------|------:|
| T1 (AGE) | 109 |
| T2 (CCAA) | 118 |
| T3 (Municipal) | 30 |

### GOV_NOT_COVERED: 0 (PASS)

### NON_GOV_REF (informational)

These are non-government reference URLs found in the data/docs.
They are not expected to be on the allowlist.

| # | Domain | URL |
|---|--------|-----|
| 1 | `trafilatura.readthedocs.io` | `https://trafilatura.readthedocs.io/` |
| 2 | `github.com` | `https://github.com/jsvine/pdfplumber` |
| 3 | `github.com` | `https://github.com/buriy/python-readability` |
| 4 | `github.com` | `https://github.com/Mimino666/langdetect` |
| 5 | `docs.ckan.org` | `https://docs.ckan.org/en/latest/api/` |
| 6 | `github.com` | `https://github.com/civicaid;` |
| 7 | `json-schema.org` | `https://json-schema.org/draft/2020-12/schema` |
| 8 | `github.com` | `https://github.com/civicaid-voice` |
| 9 | `ropenspain.github.io` | `https://ropenspain.github.io/CatastRo/` |
| 10 | `help.unhcr.org` | `https://help.unhcr.org/spain/` |
| 11 | `github.com` | `https://github.com/datosgobes` |

### Skipped Template URLs

- `https://{sede}.gob.es/sitemap.xml`
- `https://www.{municipio}.es/sitemap.xml`
- `https://{sede}.{ccaa}.es/sitemap.xml`

### Skipped Example Domain URLs

- `http://example.es`
- `https://example.gob.es/tramite%20con%20espacios`
- `https://example.gob.es/tramite`

---

## Critical Check Summary

| Scope | GOV_NOT_COVERED | Status |
|-------|---------------:|--------|
| Scope A (Enforcement) | 0 | PASS |
| Scope B (Docs+Data) | 0 | PASS |

**Overall verdict:** PASS
