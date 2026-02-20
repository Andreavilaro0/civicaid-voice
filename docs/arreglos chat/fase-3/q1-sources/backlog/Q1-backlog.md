# Q1 Backlog — Source-of-Truth Layer

> Status: Q1 COMPLETE (research-only, no code)
> Date: 2026-02-18

## Completed (Q1)

- [x] AGE Source Registry — 25 sources documented with URLs, priority, access methods
- [x] CCAA Source Registry — All 19 communities profiled with sede electronica, catalogs, priorities
- [x] Local Coverage Strategy — 4-tier approach, top 20 cities with verified URLs, disambiguation strategy
- [x] Domain Allowlist — 3-tier allowlist + blocklist + review process
- [x] URL Canonicalization Policy — 10 rules + pipeline pseudocode + edge cases
- [x] Link Health Checker Spec — check types, scheduling, alert thresholds, pseudocode
- [x] Ingestion Playbook — 6-stage pipeline (discovery/fetch/extract/normalize/store/index)
- [x] Extraction Specification — HTML/PDF/BOE XML handlers, quality scoring, error handling
- [x] ProcedureDoc Normalization Schema — v1 JSON schema, completeness scoring, migration path
- [x] Q1 Report + Evidence + Backlogs

## Open Items (carry to Q2)

| ID | Title | Priority | Notes |
|----|-------|----------|-------|
| Q1-CARRY-01 | Verify all 25 AGE URLs are live (automated check) | High | Run HTTP HEAD against all URLs in age.md |
| Q1-CARRY-02 | Verify all 19 CCAA sede URLs are live | High | Same for ccaa.md |
| Q1-CARRY-03 | Verify all 20 municipal sede URLs are live | High | Same for local.md top 20 |
| Q1-CARRY-04 | BOE API integration test | Medium | Fetch one day's sumario, validate XML parsing |
| Q1-CARRY-05 | SIA/PAG catalog scrape test | Medium | Crawl 10 procedure pages, validate extraction |
| Q1-CARRY-06 | Populate datos.gob.es dataset links | Low | DIR3, INE municipal registry downloads |
| Q1-CARRY-07 | Cross-validate allowlist vs KB fuente_url | Medium | Ensure all existing KB URLs are in allowlist |

## Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Some CCAA sede URLs may have changed since research | Medium | Automated URL health check in Q2 |
| BOE API rate limits undocumented | Low | Conservative 1 req/sec default |
| Municipal sede URLs are unstable (platform migrations) | Medium | Quarterly health checks + fallback to Diputacion |
| Some CCAA content only in co-official language | Low | Language detection + prefer Spanish version |
| No actual crawl/fetch testing done (research-only) | Medium | First Q2 task: validate pipeline against real pages |
