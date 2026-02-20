# DRIFTS.v6.md — Remaining Doc-vs-Data Inconsistencies

**Audit:** v6
**Date:** 2026-02-19
**Branch:** fix/fase3-full-pass

---

## Root Cause

The v5 fix phase added `sede.grancanaria.com` as a new tier_3_municipal entry and added aliases (`www.sepe.es`, `jccm.es`, `www.jccm.es`) to existing entries. This grew the allowlist from 355 to 362 lines and tier_3_municipal from 19 to 20 domains. However, several documentation files still reference the pre-fix counts.

---

## Drift Items

### DRIFT-01: tier_3_municipal count (19 → 20)

**Ground truth:** `allowlist.yaml` tier_3_municipal has 20 domains (verified by parsing).

| File | Line | Current Text | Should Be |
|------|------|-------------|-----------|
| Q1-REPORT.md | 74 | "19 municipal domains" | "20 municipal domains" |
| Q1.1-REPORT.md | 17 | "19 municipal domains" | "20 municipal domains" |
| gates.md | 54 | "19 municipal domains" | "20 municipal domains" |
| FULLPASS-CLOSING-REPORT.md | 32 | "tier_3_municipal: 12 → 19 domains" | "tier_3_municipal: 12 → 20 domains" |

**Priority:** P1 (numeric inaccuracy)

### DRIFT-02: allowlist line count (355 → 362)

**Ground truth:** `allowlist.yaml` has 362 lines (verified by `wc -l`).

| File | Line | Current Text | Should Be |
|------|------|-------------|-----------|
| Q1.1-REPORT.md | 48 | "355" | "362" |
| FULLPASS-CLOSING-REPORT.md | 33 | "allowlist lines: 319 → 355" | "allowlist lines: 319 → 362" |

**Priority:** P1 (numeric inaccuracy)

### DRIFT-03: URL coverage scope (informational)

The FULLPASS-CLOSING-REPORT.md references URL coverage numbers computed with an informal scope:
- "Before: 264 COVERED / 15 NOT_COVERED"
- "After: 268 COVERED / 11 NOT_COVERED"

v6 establishes two formal scopes:
- **Enforcement:** 125 URLs, 125 COVERED, 0 NOT_COVERED
- **Docs+Data:** 261 URLs (256 analyzable), 249 COVERED, 7 NOT_COVERED (all non-gov)

**Action:** Add a clarifying note to FULLPASS report (not a numeric fix — the old numbers were accurate for their scope).

**Priority:** P2 (scope clarification, not factual error)

---

## Summary

| Priority | Count | Items |
|----------|-------|-------|
| P1 | 2 | DRIFT-01, DRIFT-02 |
| P2 | 1 | DRIFT-03 |
| **Total** | **3** | |

All drifts are documentation-only. No data file or script changes needed.
