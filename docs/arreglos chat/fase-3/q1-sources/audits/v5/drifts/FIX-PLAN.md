# FIX-PLAN: Anti-Hallucination Audit v5

**Agent:** A3 (Drift & Consistency Reconciler)
**Date:** 2026-02-19
**Total Fixes Required:** 34 (16 CONTRADICTED + 18 SEMANTIC_FLAG)
**Fix Types:** All doc-only (no data or code changes needed)

> **IMPORTANT:** Do NOT apply these fixes. This is a plan only for review.

---

## Priority P1 -- Doc-Data Mismatches (26 fixes)

### FIX-01: Q1-REPORT.md -- AGE Priority Split Error
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 14
- **claim_ids:** C-001
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `25 AGE sources documented (10 P0, 10 P1, 5 P2)`
- **New text:** `25 AGE sources documented (10 P0, 11 P1, 4 P2)`

### FIX-02: Q1-REPORT.md -- AGE P1 Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 29
- **claim_ids:** C-007
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `P1 (Important) count: 10`
- **New text:** `P1 (Important) count: 11`

### FIX-03: Q1-REPORT.md -- AGE P2 Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 30
- **claim_ids:** C-008
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `P2 (Secondary) count: 5`
- **New text:** `P2 (Secondary) count: 4`

### FIX-04: Q1-REPORT.md -- Tier 3 Municipal Domain Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 75
- **claim_ids:** C-018
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Tier 3 (Municipal): 12 seed cities, on-demand expansion`
- **New text:** `Tier 3 (Municipal): 19 municipal domains, on-demand expansion`

### FIX-05: Q1.1-REPORT.md -- Municipal Domain Count in Allowlist Summary
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 17
- **claim_ids:** C-053
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `allowlist (22 AGE + 19 CCAA + 12 municipal domains)`
- **New text:** `allowlist (22 AGE + 19 CCAA + 19 municipal domains)`

### FIX-06: Q1.1-REPORT.md -- Unit Test Count (bullet)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 21
- **claim_ids:** C-062
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `3 unit tests covering all validators pass in CI-compatible pytest`
- **New text:** `5 unit tests (3 happy-path + 2 negative) covering schema validators pass in CI-compatible pytest`

### FIX-07: Q1.1-REPORT.md -- Allowlist Line Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 48
- **claim_ids:** C-071
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `allowlist.yaml: 319 lines`
- **New text:** `allowlist.yaml: 355 lines`

### FIX-08: Q1.1-REPORT.md -- Test Count in Table
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 74
- **claim_ids:** C-082
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `| \`tests/unit/test_validators.py\` | 3 | 3/3 PASS |`
- **New text:** `| \`tests/unit/test_validators.py\` | 5 | 5/5 PASS |`

### FIX-09: Q1.1-REPORT.md -- A3 Abort Condition Test Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 103
- **claim_ids:** C-094
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `A3 - Reproducible validation scripts: CLEAR (4 scripts, 3 tests)`
- **New text:** `A3 - Reproducible validation scripts: CLEAR (4 scripts, 5 tests)`

### FIX-10: Q1.1-REPORT.md -- pytest Output Claim
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 128
- **claim_ids:** C-099
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `pytest tests/unit/test_validators.py -v outputs 3 passed`
- **New text:** `pytest tests/unit/test_validators.py -v outputs 5 passed`

### FIX-11: gates.md -- AGE Priority Split
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 29
- **claim_ids:** C-112
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `AGE: 25 sources documented, P0: 10, P1: 10, P2: 5`
- **New text:** `AGE: 25 sources documented, P0: 10, P1: 11, P2: 4`

### FIX-12: gates.md -- Tier 3 Municipal Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 54
- **claim_ids:** C-125
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Tier 3 (Municipal): 12 initial seed cities`
- **New text:** `Tier 3 (Municipal): 19 municipal domains`

### FIX-13: gates.md -- Blocklist Category Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 55
- **claim_ids:** C-126
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Blocklist: 8 categories explicitly blocked`
- **New text:** `Blocklist: 9 categories explicitly blocked`

### FIX-14: gates.md -- A3 Test Count
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 147
- **claim_ids:** C-154
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Q1.1 A3: Reproducible validation scripts — CLEAR (4 scripts, 3 tests)`
- **New text:** `Q1.1 A3: Reproducible validation scripts — CLEAR (4 scripts, 5 tests)`

### FIX-15: FORENSIC-AUDIT.md -- Test Count in Scripts Summary
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 30
- **claim_ids:** C-160
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `All 4 scripts pass, 3/3 tests pass`
- **New text:** `All 4 scripts pass, 5/5 tests pass`

### FIX-16: FORENSIC-AUDIT.md -- Tier 3 Domain Verification
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 84
- **claim_ids:** C-187
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Allowlist tier_3_municipal domains: claimed 12, actual 12 — VERIFIED`
- **New text:** `Allowlist tier_3_municipal domains: claimed 12, actual 19 — CONTRADICTED (grew from 12 to 19 after AUDIT-03 fix)`

### FIX-17: Q1.1-REPORT.md -- "all passing" for Validation Scripts (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 19
- **claim_ids:** C-059
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `all executable, all passing`
- **New text:** `all executable; 3 schema validators pass; link_check.py passes in dry-run/smoke mode (3 URLs tested, full registry not yet scanned)`

### FIX-18: Q1.1-REPORT.md -- "All 6 gates passed" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 22
- **claim_ids:** C-063
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `All 6 gates passed (G1-G6), all 4 abort conditions cleared (A1-A4)`
- **New text:** `5 of 6 gates passed cleanly (G1-G3, G5-G6); G4 (link checker) passed in smoke/dry-run mode only. All 4 abort conditions cleared (A1-A4).`

### FIX-19: Q1.1-REPORT.md -- "fully validated" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 11
- **claim_ids:** C-096
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `fully validated, machine-readable foundation`
- **New text:** `schema-validated, machine-readable foundation`

### FIX-20: gates.md -- "all verified" for Local Cities (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 11
- **claim_ids:** C-103
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `PASS (20 cities, all verified)`
- **New text:** `PASS (20 cities, all research-documented; HTTP verification deferred to Q2)`

### FIX-21: gates.md -- "verified sede electronica URLs" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 45
- **claim_ids:** C-119
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Tier 1 cities: 20 (all with verified sede electronica URLs)`
- **New text:** `Tier 1 cities: 20 (all with research-documented sede electronica URLs; HTTP verification pending Q2)`

### FIX-22: gates.md -- "Gates passed: 6/6" Without Caveat (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 88
- **claim_ids:** C-140
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `| Gates passed | 6/6 |`
- **New text:** `| Gates passed | 6/6 (G4 limited to smoke/dry-run; see forensic audit) |`

### FIX-23: gates.md -- "Municipal URLs verified" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 92
- **claim_ids:** C-144
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `| Municipal URLs verified | 20 |`
- **New text:** `| Municipal URLs documented | 20 (HTTP verification pending Q2) |`

### FIX-24: gates.md -- G4 "Link checker works" PASS (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 108
- **claim_ids:** C-149
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `| **G4: Link checker works** | \`link_check.py\` runs smoke test and generates JSONL output | **PASS** (3/3 URLs OK) |`
- **New text:** `| **G4: Link checker runs** | \`link_check.py\` runs smoke test (3 URLs) and generates JSONL output | **PASS (smoke only)** -- full-registry live test had crash bug (fixed post-audit) |`

### FIX-25: FORENSIC-AUDIT.md -- "6/6 gates all VERIFIED" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 26
- **claim_ids:** C-158
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `Core claims (44 sources, 25 AGE, 19 CCAA, 20 local, 6/6 gates) are all VERIFIED`
- **New text:** `Core claims (44 sources, 25 AGE, 19 CCAA, 20 local) are VERIFIED; gates are 5/6 clean PASS + G4 partial (see F-01)`

### FIX-26: references.md -- "Municipal URLs verified: 20/20" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/references.md`
- **Line:** 63
- **claim_ids:** C-275
- **Priority:** P1
- **Type:** doc-only
- **Old text:** `| Municipal URLs verified | 20/20 (Tier 1) | This research |`
- **New text:** `| Municipal URLs documented | 20/8,131 (Tier 1 seed cities; 0.25% of all municipalities) | This research |`

---

## Priority P2 -- Stale/Minor/Semantic Tone (8 fixes)

### FIX-27: Q1-REPORT.md -- "All 4 abort conditions cleared" Without Caveat (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 133
- **claim_ids:** C-033
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `All 4 abort conditions cleared.`
- **New text:** `All 4 abort conditions cleared (A3 flagged as concern in forensic audit due to 14 allowlist coverage gaps).`

### FIX-28: Q1-REPORT.md -- "Status: COMPLETE" Without Scope Qualifier (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 4
- **claim_ids:** C-034
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `Status: COMPLETE (research-only, no code changes)`
- **New text:** `Status: RESEARCH COMPLETE (documentation only -- validation, HTTP checks, and API testing deferred to Q2)`

### FIX-29: Q1-REPORT.md -- "No code was written" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 20
- **claim_ids:** C-035
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `No code was written. All output is research documentation`
- **New text:** `No src/ production code was written. All Q1 output is research documentation (Q1.1 added validation scripts and data artifacts)`

### FIX-30: Q1.1-REPORT.md -- "Status: COMPLETE" Without Caveats (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 4
- **claim_ids:** C-095
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `**Status:** COMPLETE`
- **New text:** `**Status:** COMPLETE (post-audit fixes applied; see FORENSIC-AUDIT-REPORT for 10 resolved findings)`

### FIX-31: Q1.1-REPORT.md -- "validated artifacts" in Goal Statement (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 5
- **claim_ids:** C-100
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `Convert Q1 research markdown into machine-readable, validated artifacts`
- **New text:** `Convert Q1 research markdown into machine-readable, schema-validated artifacts`

### FIX-32: FORENSIC-AUDIT.md -- "vast majority are VERIFIED" (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 12
- **claim_ids:** C-155
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `the vast majority are VERIFIED`
- **New text:** `the ~30 most critical claims were individually verified (counts, file existence, schema validation, gates); remaining claims were not individually audited`

### FIX-33: FORENSIC-AUDIT.md -- Uncalibrated Risk Score (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 14
- **claim_ids:** C-157
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `Hallucination Risk Score: 12/100 (LOW)`
- **New text:** `Hallucination Risk Assessment: LOW -- Core data claims are accurate; discrepancies found in secondary metrics and one crash bug (qualitative assessment, not a calibrated metric)`

### FIX-34: FORENSIC-AUDIT.md -- "All 29 declared files exist" Scope Note (Semantic)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 110
- **claim_ids:** C-171
- **Priority:** P2
- **Type:** doc-only
- **Old text:** `All 29 declared files exist. VERIFIED`
- **New text:** `All 29 declared files exist (structural check). VERIFIED. (Content correctness verified separately in claims ledger.)`

---

## Summary by File

| File | Fix Count | P1 | P2 |
|------|-----------|----|----|
| Q1-REPORT.md | 6 | 4 | 2 |
| Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md | 10 | 8 | 2 |
| evidence/gates.md | 9 | 9 | 0 |
| evidence/Q1.1-FORENSIC-AUDIT-REPORT.md | 6 | 2 | 4 |
| evidence/references.md | 1 | 1 | 0 |
| **Total** | **34** (2 overlap on same file+line) | **26** | **8** |

---

## Recommended Execution Order

1. **Batch 1 (P1 numeric corrections):** FIX-01 through FIX-16 -- These are objective numeric corrections with clear old/new values. Apply with find-and-replace; verify with grep.
2. **Batch 2 (P1 semantic corrections):** FIX-17 through FIX-26 -- These require editorial judgment to ensure replacement text reads naturally in context.
3. **Batch 3 (P2 tone/scope corrections):** FIX-27 through FIX-34 -- Lower priority; can be batched with the next documentation refresh.

---

*End of FIX-PLAN. No fixes should be applied without human review.*
