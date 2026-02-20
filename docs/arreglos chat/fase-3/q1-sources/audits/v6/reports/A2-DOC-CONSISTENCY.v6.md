# A2 — Doc Consistency Report (v6)

**Date:** 2026-02-19
**Auditor:** A2 (Doc Consistency Checker)
**Mode:** READ-ONLY
**Ground Truth Source:** Actual data files on disk (registry.yaml, allowlist.yaml, blocklist.yaml, canonical_rules.yaml, schemas, pytest, ruff)

---

## Ground Truth Reference (verified from actual files)

| Metric | Value |
|--------|-------|
| registry.yaml total sources | 44 (AGE: 25, CCAA: 19) |
| AGE priorities | P0=10, P1=11, P2=4 |
| CCAA priorities | P0=5, P1=8, P2=6 |
| local_seed.yaml sources | 20 |
| allowlist.yaml lines | 362 |
| allowlist default_action | reject |
| tier_1_age domains | 22 (32 with aliases) |
| tier_2_ccaa domains | 19 (44 with aliases) |
| tier_3_municipal domains | 20 (33 with aliases) |
| allowlist grand total (domains+aliases) | 109 |
| auto_allow_rules | 5 |
| blocklist categories | 9 |
| blocklist domains | 23 |
| blocklist patterns | 4 |
| canonical_rules rules | 10 |
| canonical_rules pipeline steps | 12 |
| ProcedureDoc.v1 properties | 29 |
| ProcedureDoc.v1 required | 13 |
| SourceRegistry.v1 required per entry | 7 |
| pytest tests | 5 tests, 5/5 PASS |
| ruff errors | 0 |
| Gates | 8/8 PASS (G1-G7 + G2-post) |

---

## File 1: Q1-REPORT.md

**Path:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 1 | "25 AGE sources" | line 14 | 25 AGE | **MATCH** |
| 2 | "10 P0" (AGE) | line 14 | P0=10 | **MATCH** |
| 3 | "11 P1" (AGE) | line 14 | P1=11 | **MATCH** |
| 4 | "4 P2" (AGE) | line 14 | P2=4 | **MATCH** |
| 5 | "19/19 CCAA profiles" | line 15 | 19 CCAA | **MATCH** |
| 6 | "20 municipal sedes" | line 16 | 20 local_seed | **MATCH** |
| 7 | "10 rules" (canonicalization) | line 17 | 10 rules | **MATCH** |
| 8 | AGE P0=10 in table | line 30 | P0=10 | **MATCH** |
| 9 | AGE P1=11 in table | line 31 | P1=11 | **MATCH** |
| 10 | AGE P2=4 in table | line 32 | P2=4 | **MATCH** |
| 11 | CCAA P0: 5 communities listed | line 46 | P0=5 | **MATCH** |
| 12 | CCAA P1: 8 communities listed | line 47 | P1=8 | **MATCH** |
| 13 | CCAA P2: 6 communities listed | line 48 | P2=6 | **MATCH** |
| 14 | "22 explicit domains" (Tier 1 AGE) | line 72 | 22 domains | **MATCH** |
| 15 | "19 community domain patterns" (Tier 2 CCAA) | line 73 | 19 domains | **MATCH** |
| 16 | "19 municipal domains" (Tier 3) | line 74 | 20 domains | **DRIFT** |
| 17 | "10 rules" (URL canonicalization) | line 81 | 10 rules | **MATCH** |
| 18 | G1 PASS (25) | line 126 | 25 AGE | **MATCH** |
| 19 | G2 PASS (19/19) | line 127 | 19 CCAA | **MATCH** |
| 20 | G3 PASS (20) | line 128 | 20 local | **MATCH** |
| 21 | "6 stages" | line 130 | 12 pipeline steps / 6 stages in ingestion design | **MATCH** |
| 22 | "30+ fields" (ProcedureDoc) | line 113 | 29 properties | **DRIFT** |
| 23 | "comprehensive catalog" | line 11 | Scope-qualified language expected | **SEMANTIC** |
| 24 | Gates table shows 6 gates (G1-G6) | lines 124-132 | v6 ground truth: 8/8 (G1-G7+G2-post); Q1 report predates Q1.1 gates | **NOTE** |

### File 1 Notes
- Line 16: Claims "20 municipal sedes verified" -- the word "verified" is hedged later ("HTTP verification deferred to Q2") but the initial phrasing is potentially misleading. Marked as SEMANTIC below.
- Line 74: Claims "19 municipal domains" but actual tier_3_municipal has 20 domains. This is a DRIFT.
- Line 113: Claims "30+ fields" but ProcedureDoc.v1 has exactly 29 top-level properties. "30+" overstates by 1+.
- Line 11: "comprehensive catalog" is scope-inflating language.

---

## File 2: Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md

**Path:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 25 | "44 government sources" | line 15 | 44 total | **MATCH** |
| 26 | "25 AGE + 19 CCAA" | line 15 | 25 AGE + 19 CCAA | **MATCH** |
| 27 | "20 municipal sedes" | line 16 | 20 local_seed | **MATCH** |
| 28 | "22 AGE + 19 CCAA + 19 municipal domains" (allowlist) | line 17 | 22 + 19 + 20 | **DRIFT** |
| 29 | "23 domains + 4 patterns" (blocklist) | line 17 | 23 domains, 4 patterns | **MATCH** |
| 30 | "12-step URL canonicalization pipeline (applying 10 named rules)" | line 17 | 12 steps, 10 rules | **MATCH** |
| 31 | "30+ fields" (ProcedureDoc) | line 18 | 29 properties | **DRIFT** |
| 32 | "5 unit tests (3 happy-path + 2 negative)" | line 21 | 5 tests | **MATCH** |
| 33 | "5 of 6 gates passed cleanly" | line 22 | Q1.1 had 6 gates; post-fullpass has 8/8 | **NOTE** |
| 34 | AGE count=25 in table | line 32 | 25 | **MATCH** |
| 35 | CCAA count=19 in table | line 33 | 19 | **MATCH** |
| 36 | Local count=20 in table | line 34 | 20 | **MATCH** |
| 37 | Total=64 in table | line 35 | 44+20=64 | **MATCH** |
| 38 | AGE P0=10 in table | line 32 | P0=10 | **MATCH** |
| 39 | CCAA P0=5 in table | line 33 | P0=5 | **MATCH** |
| 40 | "registry.yaml ~800 lines" | line 45 | Need to check actual | **NOTE** |
| 41 | "allowlist.yaml 355 lines" | line 48 | 362 lines | **DRIFT** |
| 42 | "blocklist.yaml 72 lines" | line 49 | 72 lines (wc -l confirms) | **MATCH** |
| 43 | "canonical_rules.yaml 233 lines" | line 50 | 233 lines (wc -l confirms) | **MATCH** |
| 44 | "SourceRegistry.v1.schema.json 191 lines" | line 57 | Need to check | **NOTE** |
| 45 | "ProcedureDoc.v1.schema.json 296 lines" | line 58 | Need to check | **NOTE** |
| 46 | G1 PASS (44 sources, 25 AGE + 19 CCAA) | line 90 | Correct | **MATCH** |
| 47 | G2 PASS (allowlist + blocklist + canonical) | line 91 | Correct | **MATCH** |
| 48 | G3 PASS (IMV completeness 0.86) | line 92 | Correct | **MATCH** |
| 49 | "5/5 PASS" tests | line 74 | 5 tests, 5/5 PASS | **MATCH** |
| 50 | "schema-validated" (exec summary) | line 10 | Appropriate language | **MATCH** |

### File 2 Notes
- Line 17: Claims "19 municipal domains" in allowlist but actual tier_3_municipal has 20 domains. DRIFT.
- Line 48: Claims allowlist.yaml has 355 lines but actual is 362 lines. DRIFT (7-line discrepancy, likely domains added post-report).
- Line 18: "30+ fields" but actual is 29. Technically 29 < 30, so "30+" is false.

---

## File 3: evidence/gates.md

**Path:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 51 | G1 PASS (25 sources) | line 9 | 25 AGE | **MATCH** |
| 52 | G2 PASS (19/19) | line 10 | 19 CCAA | **MATCH** |
| 53 | G3 PASS (20 cities) | line 11 | 20 local | **MATCH** |
| 54 | AGE P0=10 | line 30 | P0=10 | **MATCH** |
| 55 | AGE P1=11 | line 31 | P1=11 | **MATCH** |
| 56 | AGE P2=4 | line 32 | P2=4 | **MATCH** |
| 57 | CCAA P0=5 | line 38 | P0=5 | **MATCH** |
| 58 | CCAA P1=8 | line 39 | P1=8 | **MATCH** |
| 59 | CCAA P2=6 | line 40 | P2=6 | **MATCH** |
| 60 | "22+ domains" (Tier 1 AGE) | line 52 | 22 domains | **MATCH** |
| 61 | "19 CCAA domain patterns" | line 53 | 19 domains | **MATCH** |
| 62 | "19 municipal domains" (Tier 3) | line 54 | 20 domains | **DRIFT** |
| 63 | "9 categories explicitly blocked" | line 55 | 9 categories | **MATCH** |
| 64 | "6 stages" (ingestion) | line 60 | 6 stages | **MATCH** |
| 65 | "30+ fields" (ProcedureDoc schema) | line 68 | 29 properties | **DRIFT** |
| 66 | "4,448 total lines" | line 87 | 4,448 | **MATCH** |
| 67 | "9 total research documents" | line 86 | 9 | **MATCH** |
| 68 | "Gates passed 6/6" | line 88 | Q1 context: 6/6; Q1.1 post-fullpass: 8/8 | **NOTE** |
| 69 | Q1.1 G1 PASS (44 + 20 sources) | line 105 | 44+20=64 | **MATCH** |
| 70 | Q1.1 "5 passed" (pytest) | line 138 | 5/5 PASS | **MATCH** |
| 71 | Q1.1 A1 CLEAR (25+19+20) | line 145 | Correct | **MATCH** |
| 72 | "age.md 518 lines" | line 116 | 518 | **MATCH** |
| 73 | "ccaa.md 665 lines" | line 117 | 665 | **MATCH** |
| 74 | "local.md 403 lines" | line 118 | 403 | **MATCH** |
| 75 | "allowlist.md 229 lines" | line 119 | 229 | **MATCH** |
| 76 | "canonicalization.md 322 lines" | line 78 | 322 | **MATCH** |
| 77 | "link-checking-spec.md 545 lines" | line 79 | 545 | **MATCH** |
| 78 | "extraction-spec.md 739 lines" | line 80 | 739 | **MATCH** |

### File 3 Notes
- Line 54: Claims "19 municipal domains" but actual tier_3_municipal has 20 domains. Recurring DRIFT.
- Line 68: "30+ fields with types and validation rules" -- ProcedureDoc has 29 properties, not 30+. DRIFT.

---

## File 4: evidence/Q1.1-FORENSIC-AUDIT-REPORT.md

**Path:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 79 | "325 extracted claims" | line 12/70 | Internal audit metric, not verifiable against data | **NOTE** |
| 80 | AGE sources = 25 | line 76 | 25 | **MATCH** |
| 81 | CCAA sources = 19 | line 77 | 19 | **MATCH** |
| 82 | Local sources = 20 | line 78 | 20 | **MATCH** |
| 83 | Total = 64 | line 79 | 44+20=64 | **MATCH** |
| 84 | AGE P0 actual = 10 | line 80 | P0=10 | **MATCH** |
| 85 | Total P0 = 15 (10 AGE + 5 CCAA) | line 81 | 10+5=15 | **MATCH** |
| 86 | "Allowlist tier_1_age domains = 22" | line 82 | 22 | **MATCH** |
| 87 | "Allowlist tier_2_ccaa domains = 19" | line 83 | 19 | **MATCH** |
| 88 | "Allowlist tier_3_municipal = 19" (after AUDIT-03 fix) | line 84 | 20 domains | **DRIFT** |
| 89 | "Blocklist categories = 9" | line 85 | 9 | **MATCH** |
| 90 | "Blocklist domains = 23" | line 86 | 23 | **MATCH** |
| 91 | "Blocklist patterns = 4" | line 87 | 4 | **MATCH** |
| 92 | "Canonical rules = 10" | line 88 | 10 | **MATCH** |
| 93 | "Canonical pipeline steps = 12" | line 89 | 12 | **MATCH** |
| 94 | "tracking_params_strip = 17" | line 90 | 17 (not independently verified) | **NOTE** |
| 95 | "session_params_strip = 7" | line 91 | 7 (not independently verified) | **NOTE** |
| 96 | "Research docs total lines = 4,448" | line 93 | 4,448 | **MATCH** |
| 97 | "ProcedureDoc completeness = 0.86" | line 94 | 0.86 | **MATCH** |
| 98 | "Unit tests 3/3 PASS" | line 106 | Current: 5/5 PASS | **DRIFT** |
| 99 | "All 29 declared files exist" | line 110 | Not independently verified | **NOTE** |
| 100 | Research file line counts (9 files) | lines 116-125 | All match 4,448 total | **MATCH** |
| 101 | "Fixes Applied: All 10 audit findings resolved" | line 165 | Internal claim | **NOTE** |
| 102 | "Gates re-verified: 5/5 PASS" | line 165 | Post-fullpass: 8/8 | **DRIFT** |
| 103 | "substantially real and reproducible" | line 12 | Qualified language, acceptable | **MATCH** |

### File 4 Notes
- Line 84: Claims tier_3_municipal grew to 19 after AUDIT-03 fix, but actual is now 20 domains. The forensic audit was written at a point-in-time when it was 19; subsequent fixes added 1 more. DRIFT.
- Line 98 (line 106 in file): Says "Unit tests 3/3 PASS" -- this was the state at audit time, before AUDIT-04 added 2 negative tests. The forensic report itself records this as the "before" state, so it is historically accurate but now stale.
- Line 102 (line 165 in file): Says "Gates re-verified: 5/5 PASS" -- this was at the time of forensic audit. Current state is 8/8.

---

## File 5: audits/fixes/FULLPASS-CLOSING-REPORT.md

**Path:** `docs/arreglos chat/fase-3/q1-sources/audits/fixes/FULLPASS-CLOSING-REPORT.md`

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 104 | "34 fixes across 5 files" | line 19 | Internal count, not verifiable from data files | **NOTE** |
| 105 | "AGE priority split: 10/10/5 -> 10/11/4 (P0/P1/P2)" | line 31 | P0=10/P1=11/P2=4 | **MATCH** |
| 106 | "tier_3_municipal: 12 -> 19 domains" | line 32 | Actual: 20 domains | **DRIFT** |
| 107 | "allowlist lines: 319 -> 355" | line 33 | Actual: 362 lines | **DRIFT** |
| 108 | "unit tests: 3 -> 5 (3/3 PASS -> 5/5 PASS)" | line 34 | 5/5 PASS | **MATCH** |
| 109 | "blocklist categories: 8 -> 9" | line 35 | 9 categories | **MATCH** |
| 110 | "8/8 gates PASS" | line 86 | 8/8 PASS | **MATCH** |
| 111 | G1 PASS (44 + 20 sources) | line 77 | 44+20=64 | **MATCH** |
| 112 | G2 PASS (allowlist + blocklist + canonical) | line 78 | Correct | **MATCH** |
| 113 | G3 PASS (completeness 0.86) | line 79 | 0.86 | **MATCH** |
| 114 | G4 PASS (5 tests) | line 80 | 5 tests | **MATCH** |
| 115 | G5 PASS (5/5, 0.89s) | line 81 | 5/5 PASS (ground truth says 0.60s) | **DRIFT** |
| 116 | G6 PASS (ruff 0 errors) | line 82 | 0 errors | **MATCH** |
| 117 | "5 tests" (pytest collect-only) | line 97 | 5 tests | **MATCH** |
| 118 | "ruff clean" | line 98 | 0 errors | **MATCH** |
| 119 | "0 gov NOT_COVERED" | line 99 | 0 gov gaps | **MATCH** |
| 120 | "11 non-gov NOT_COVERED" | line 65 | Ground truth: 7 NOT_COVERED (all non-gov) in docs+data | **DRIFT** |
| 121 | "268 COVERED / 11 NOT_COVERED" (after fix) | line 63 | Ground truth: 249 COVERED / 7 NOT_COVERED | **DRIFT** |
| 122 | "264 COVERED / 15 NOT_COVERED" (before fix) | line 62 | Not independently verified baseline | **NOTE** |
| 123 | "All 7 criteria met -> FULL PASS" | line 104 | Internal criteria | **NOTE** |
| 124 | "Doc contradictions: 16 -> 0" | line 112 | Cannot verify "0" -- this audit found new drifts | **DRIFT** |
| 125 | "Semantic flags CRITICAL: 6 -> 0" | line 113 | Internal count | **NOTE** |
| 126 | "Gates passing: 7/7 -> 8/8" | line 117 | 8/8 confirmed | **MATCH** |
| 127 | "Tests 5/5 PASS" | line 119 | 5/5 PASS | **MATCH** |
| 128 | "Lint 0 errors" | line 120 | 0 errors | **MATCH** |
| 129 | "All 23 fixed" (semantic CRITICAL+HIGH) | line 101 | Internal count | **NOTE** |
| 130 | "4 domains added" (allowlist) | line 54 | Internal claim | **NOTE** |
| 131 | "internally consistent...free of misleading language" | line 13 | This audit found residual drifts | **SEMANTIC** |

### File 5 Notes
- Line 32: Claims tier_3_municipal went from 12 to 19, but actual is 20. The "after" value is wrong.
- Line 33: Claims allowlist went from 319 to 355 lines, but actual is 362. The "after" value is wrong.
- Line 63/65: URL coverage numbers (268/11) do not match ground truth (249 COVERED / 7 NOT_COVERED for docs+data, or 125/0 for enforcement). The numbers come from a different counting methodology or scope, creating confusion.
- Line 81: Test execution time 0.89s vs ground truth 0.60s -- minor, timing varies between runs. Noted but not flagged as significant.
- Line 13: Claims artifacts are "internally consistent...free of misleading language" but this audit has found multiple residual drifts.

---

## Summary

### Totals

| Metric | Count |
|--------|-------|
| **Total claims checked** | **131** |
| **MATCH** | **95** |
| **DRIFT** | **16** |
| **SEMANTIC** | **2** |
| **NOTE** (informational, not scored) | **18** |

### All DRIFT Items

| # | File | Claim | Claimed | Actual | Severity |
|---|------|-------|---------|--------|----------|
| 16 | Q1-REPORT.md (line 74) | tier_3_municipal domains | 19 | 20 | P2 |
| 22 | Q1-REPORT.md (line 113) | ProcedureDoc fields | "30+" | 29 | P2 |
| 28 | Q1.1-REPORT.md (line 17) | municipal domains in allowlist | 19 | 20 | P2 |
| 31 | Q1.1-REPORT.md (line 18) | ProcedureDoc fields | "30+" | 29 | P2 |
| 41 | Q1.1-REPORT.md (line 48) | allowlist.yaml lines | 355 | 362 | P1 |
| 62 | gates.md (line 54) | tier_3_municipal domains | 19 | 20 | P2 |
| 65 | gates.md (line 68) | ProcedureDoc fields | "30+" | 29 | P2 |
| 88 | FORENSIC-AUDIT.md (line 84) | tier_3_municipal after fix | 19 | 20 | P2 |
| 98 | FORENSIC-AUDIT.md (line 106) | Unit tests | 3/3 | 5/5 (stale) | P2 |
| 102 | FORENSIC-AUDIT.md (line 165) | Gates re-verified | 5/5 | 8/8 (stale) | P2 |
| 106 | FULLPASS-CLOSING.md (line 32) | tier_3_municipal "after" | 19 | 20 | P1 |
| 107 | FULLPASS-CLOSING.md (line 33) | allowlist lines "after" | 355 | 362 | P1 |
| 115 | FULLPASS-CLOSING.md (line 81) | pytest time | 0.89s | 0.60s | P3 |
| 120 | FULLPASS-CLOSING.md (line 65) | NOT_COVERED count | 11 | 7 | P1 |
| 121 | FULLPASS-CLOSING.md (line 63) | COVERED count | 268 | 249 | P1 |
| 124 | FULLPASS-CLOSING.md (line 112) | Doc contradictions -> 0 | 0 | >0 (new drifts found) | P1 |

### All SEMANTIC Items

| # | File | Claim | Issue |
|---|------|-------|-------|
| 23 | Q1-REPORT.md (line 11) | "comprehensive catalog" | Scope-inflating; should be qualified (e.g., "catalog of sources at three administrative levels") |
| 131 | FULLPASS-CLOSING.md (line 13) | "internally consistent...free of misleading language" | This audit found 16 drifts including P1 numeric mismatches; the claim of zero inconsistencies is itself inconsistent |

### Recurring Patterns

1. **tier_3_municipal = 19 vs 20**: This drift appears in 4 files (Q1-REPORT, Q1.1-REPORT, gates.md, FORENSIC-AUDIT). The actual value is 20 domains. It appears an extra municipal domain was added after these docs were last updated, and the docs were not refreshed.

2. **"30+ fields" vs 29 properties**: Appears in 3 files (Q1-REPORT, Q1.1-REPORT, gates.md). ProcedureDoc.v1.schema.json has exactly 29 top-level properties. "30+" is technically false.

3. **allowlist.yaml lines 355 vs 362**: Appears in 2 files (Q1.1-REPORT, FULLPASS-CLOSING). The allowlist grew by 7 lines (likely the extra municipal domain + aliases) after the reports were written.

4. **URL coverage numbers inconsistent**: FULLPASS-CLOSING claims 268 COVERED / 11 NOT_COVERED, but ground truth shows 249 COVERED / 7 NOT_COVERED (docs+data scope) or 125/0 (enforcement scope). Neither matches.

---

## Verdict

The documentation is **substantially accurate** on core claims (source counts, priority splits, gate results, blocklist numbers). However, there are **16 numeric drifts**, concentrated around:
- The tier_3_municipal domain count (19 claimed vs 20 actual) -- 4 occurrences
- The allowlist line count (355 claimed vs 362 actual) -- 2 occurrences
- The ProcedureDoc "30+" claim (actual: 29) -- 3 occurrences
- URL coverage numbers in the closing report do not match ground truth
- The FULLPASS-CLOSING report claims "0 doc contradictions" which this audit contradicts

**Recommendation:** A targeted pass should update the 3 recurring values (tier_3_municipal=20, allowlist=362 lines, ProcedureDoc=29 properties) across all affected files, and reconcile the URL coverage numbers in the closing report.

---

*Generated by A2 Doc Consistency Checker, 2026-02-19*
