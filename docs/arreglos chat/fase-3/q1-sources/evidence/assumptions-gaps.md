# Q1 Assumptions and Gaps

> Date: 2026-02-18

## Assumptions

| # | Assumption | Impact if wrong | Mitigation |
|---|-----------|-----------------|------------|
| A1 | Government `.gob.es` domains are stable and rarely change | Broken links, stale content | Link health checker (Q2) |
| A2 | BOE API is free and will remain without auth requirements | Would need to find alternative legislation source | Monitor API changes, cache locally |
| A3 | trafilatura can extract useful content from most government HTML pages | Poor extraction quality | Fallback to readability-lxml + site-specific parsers |
| A4 | 1 req/sec rate limiting is sufficient for all government domains | Could get blocked or too slow | Per-domain config, monitor for 429s |
| A5 | ProcedureDoc v1 schema covers the essential fields for Clara's use cases | Missing fields discovered during extraction | Schema is versioned, can add fields in v2 |
| A6 | Spanish (Castellano) version is available for all key procedure pages | Some CCAA content only in regional language | langdetect + flag for manual translation |
| A7 | Municipal sede electronica URLs follow predictable patterns | Can't auto-discover some sedes | DIR3 + PAG directory as fallback |
| A8 | The existing KB format (data/tramites/*.json) will coexist with ProcedureDoc | Migration complexity | Backward compatibility designed into schema |
| A9 | CCAA sede electronica structures are consistent enough for automated extraction | Each CCAA has different CMS/layout | Site-specific extraction rules where needed |
| A10 | Vulnerable users primarily need AGE + CCAA procedures (municipal is secondary) | Municipal procedures (empadronamiento) are actually critical | Top 20 cities covered in Tier 1 |

## Gaps

| # | Gap | Severity | Resolution plan |
|---|-----|----------|-----------------|
| G1 | No actual HTTP validation of URLs performed (research-only) | High | First Q2 task: automated URL health check |
| G2 | BOE API response format not tested with real requests | Medium | Q2-ING-04: BOE API integration test |
| G3 | SIA/PAG catalog page structure not analyzed in detail | Medium | Q2-ING-09: crawl test of PAG procedure pages |
| G4 | CCAA sede electronica page layouts not analyzed for extraction | Medium | Q2-ING-10: extraction test per P0 CCAA |
| G5 | No sitemap.xml verification for any domain | Medium | Q2-LINK-02: sitemap discovery across all registries |
| G6 | robots.txt compliance not checked for any domain | Medium | Q2-ING-01: respect robots.txt in fetch stage |
| G7 | Content quality of existing KB tramites not evaluated against ProcedureDoc schema | Low | Q2-ING-08: migration + completeness scoring |
| G8 | No performance benchmarks for extraction pipeline | Low | Q2: establish baseline processing times |
| G9 | DIR3 dataset not downloaded or analyzed | Medium | Q2: download and parse DIR3 for municipal lookup |
| G10 | Import@ss and Carpeta Ciudadana content inaccessible (auth-required) | Low | Document what users can do, not extract content |
| G11 | Some CCAA URLs may have changed since last verification | Medium | Automated check in Q2 |
| G12 | No cost estimate for embedding/vector infrastructure | Medium | Q2-VEC-01: evaluate model options and costs |
| G13 | Tier 2-3 municipal URLs not individually verified | Medium | Q3: automated verification + DIR3 cross-reference |

## Risk Register

| Risk | Probability | Impact | Status |
|------|------------|--------|--------|
| Government website restructuring breaks links | Medium | Medium | Mitigated by health checker design |
| BOE API changes or adds auth | Low | High | Cache locally, monitor for changes |
| Extraction quality too low for automated pipeline | Medium | High | Fallback to LLM-assisted extraction (Q3) |
| Vector search quality insufficient for Clara's needs | Medium | High | Hybrid retrieval (vector + keyword) planned |
| CCAA content in regional languages only | Low | Medium | Language detection + Spanish preference |
| Municipal sede platforms too heterogeneous | Medium | Medium | Site-specific rules + Diputacion fallback |
