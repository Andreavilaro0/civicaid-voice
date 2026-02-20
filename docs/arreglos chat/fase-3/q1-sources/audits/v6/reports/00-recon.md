# 00-RECON — Audit v6 Reconnaissance Report

**Project:** CivicAid/Clara — Biblioteca Oficial v0
**Date:** 2026-02-19
**Branch:** fix/fase3-full-pass
**Commit:** deb42a9688cec73c820fbe4265845a370bc72600
**Auditor:** Claude Code (Opus 4.6)

---

## Purpose

Audit v6 resolves the URL coverage scope discrepancy discovered between v5 and the post-fix analysis:
- v5 evidence: 284 URLs / 15 NOT_COVERED (enforcement-only scope)
- Post-fix evidence: 292 URLs / 74 NOT_COVERED (broader docs+data scope)

v6 establishes **two formal scopes** as the canonical single source of truth.

---

## Environment

| Item | Value |
|------|-------|
| Python | 3.11.8 |
| OS | Darwin 25.0.0 (arm64) |
| jsonschema | 4.26.0 |
| pytest | 9.0.2 |
| ruff | 0.15.0 |
| PyYAML | 6.0.3 |

---

## Artifact Inventory

### Data Files

| File | Size | Key Metrics |
|------|------|-------------|
| data/sources/registry.yaml | 799 lines | 44 sources (25 AGE + 19 CCAA) |
| data/sources/local_seed.yaml | 413 lines | 20 local sources |
| data/policy/allowlist.yaml | 362 lines | 22+19+20 domains across 3 tiers |
| data/policy/blocklist.yaml | 72 lines | 9 categories, 23 domains, 4 patterns |
| data/policy/canonical_rules.yaml | 233 lines | 10 rules, 12 pipeline steps |

### Schemas

| File | Properties | Required |
|------|-----------|----------|
| schemas/ProcedureDoc.v1.schema.json | 29 | 13 |
| schemas/SourceRegistry.v1.schema.json | 18 (in $defs/SourceEntry) | 7 per entry |

### Scripts & Tests

| File | Status |
|------|--------|
| scripts/validate_source_registry.py | PASS |
| scripts/validate_policy.py | PASS |
| scripts/validate_proceduredoc_schema.py | PASS (completeness 0.86) |
| scripts/link_check.py | PASS (dry-run, 8 URLs) |
| tests/unit/test_validators.py | 5/5 PASS (0.60s) |
| ruff check | 0 errors |

### Documentation Files (post-fix from v5)

| File | Fixes Applied (v5) |
|------|-------------------|
| Q1-REPORT.md | 7 |
| Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md | 11 |
| evidence/gates.md | 10 |
| evidence/Q1.1-FORENSIC-AUDIT-REPORT.md | 6 |
| evidence/references.md | 1 |

---

## Ground Truth v6

Extracted programmatically from actual data files:

```
registry.yaml: 44 total sources
  AGE: 25 (P0=10, P1=11, P2=4)
  CCAA: 19 (P0=5, P1=8, P2=6)
local_seed.yaml: 20 sources

allowlist.yaml:
  default_action: reject
  tier_1_age: 22 domains (32 with aliases)
  tier_2_ccaa: 19 domains (44 with aliases)
  tier_3_municipal: 20 domains (33 with aliases)
  grand_total: 109 domains+aliases
  auto_allow_rules: 5
  lines: 362

blocklist.yaml: 9 categories, 23 domains, 4 patterns
canonical_rules.yaml: 10 rules, 12 pipeline steps
ProcedureDoc schema: 29 properties, 13 required
SourceRegistry schema: 7 required per entry

pytest: 5 tests, 5/5 PASS
ruff: 0 errors
Gates: 8/8 PASS
```

---

## URL Coverage v6 (Dual Scope)

### Scope 1: ENFORCEMENT (data files only)

Files scanned: `data/sources/registry.yaml`, `data/sources/local_seed.yaml`, `data/policy/allowlist.yaml`, `data/policy/blocklist.yaml`, `data/policy/canonical_rules.yaml`

| Metric | Value |
|--------|-------|
| Unique URLs extracted | 125 |
| COVERED | 125 |
| NOT_COVERED | 0 |
| GOV NOT_COVERED | 0 |
| Coverage rate | 100.0% |

**Verdict: PASS** — All enforcement-scope URLs are covered by the allowlist.

### Scope 2: DOCS+DATA (all markdown + data)

Files scanned: All `.md` files under `docs/arreglos chat/fase-3/q1-sources/` + all data files.

| Metric | Value |
|--------|-------|
| Unique URLs extracted | 261 |
| Artifact/Template (skipped) | 5 |
| Analyzable URLs | 256 |
| COVERED | 249 |
| NOT_COVERED | 7 |
| GOV NOT_COVERED | 0 |
| NON_GOV NOT_COVERED | 7 |
| Coverage rate | 97.3% |

**Verdict: PASS** — All government URLs are covered. 7 non-gov URLs (github.com, docs.ckan.org, json-schema.org, etc.) are correctly NOT in the allowlist.

### Resolution of v5-vs-postfix discrepancy

| Source | URLs | NOT_COVERED | Explanation |
|--------|------|-------------|-------------|
| v5 (url-coverage.jsonl) | 284 | 15 | Informal scope — mixed data+some docs |
| post-fix (url-coverage-postfix.txt) | 292 | 74 | Informal scope — all .md + data, no URL cleaning |
| **v6 enforcement** | **125** | **0** | Formal scope — data files only |
| **v6 docs+data** | **261** | **7** | Formal scope — all md+data, cleaned URLs |

The discrepancy is fully explained by:
1. **Scope difference:** v5 included some but not all markdown files
2. **URL cleaning:** v5/postfix didn't strip backticks, template URLs, or markdown artifacts
3. **Deduplication:** v6 properly deduplicates after normalization

---

## Preliminary Findings

### Known Drifts (to verify in A2)

| Item | Doc Claim | Ground Truth | Status |
|------|-----------|-------------|--------|
| allowlist lines | 355 (FULLPASS report) | 362 | DRIFT |
| tier_3_municipal | 19 (FULLPASS report) | 20 | DRIFT |
| URL coverage | "268 COVERED / 11 NOT_COVERED" (FULLPASS) | 125/0 (enforcement) or 249/7 (docs+data) | SCOPE_CHANGED |

### New v6 Observations

1. **tier_3_municipal count increased from 19 to 20** — sede.grancanaria.com was added during the fix phase but the FULLPASS report counted it under the 19 total (off-by-one).
2. **Allowlist grew from 355 to 362 lines** — Adding 4 domains with their YAML structure added 7 more lines than the report estimated.
3. **URL coverage needs formal scoping** — Previous reports mixed scopes, creating apparent contradictions. v6 resolves this definitively.

---

## Next Steps

1. **A2: Doc Consistency** — Verify every numeric claim in docs against v6 ground truth
2. **A4: Claims/Meta** — Re-verify key claims and produce DRIFTS.v6.md + FIX-PLAN.v6.md
3. **Apply minimal fixes** — Update only the 2-3 remaining drifts
4. **Close** — Write GATES-RESULTS.v6.md and AH-AUDIT-REPORT-v6.md

---

*Generated by Audit v6 recon phase, 2026-02-19*
