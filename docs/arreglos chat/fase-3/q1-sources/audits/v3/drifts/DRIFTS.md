# A3v3 — Drift & Consistency Taxonomy

**Date:** 2026-02-18
**Auditor:** A3 (Drift & Consistency Reconciler), Anti-Hallucination Audit v3
**Mode:** STRICT READ-ONLY
**Repository:** /Users/andreaavila/Documents/hakaton/civicaid-voice

---

## Ground Truth Reference (computed from data files)

| Data File | Key Metric | Actual Value |
|-----------|-----------|--------------|
| registry.yaml | Total sources | 44 (25 AGE + 19 CCAA) |
| registry.yaml | AGE priority | P0=10, P1=11, P2=4 |
| registry.yaml | CCAA priority | P0=5, P1=8, P2=6 |
| registry.yaml | Lines | 799 |
| local_seed.yaml | Sources | 20 |
| local_seed.yaml | Lines | 413 |
| allowlist.yaml | Domains | 22 (tier_1) + 19 (tier_2) + 19 (tier_3) = 60 |
| allowlist.yaml | Lines | 355 |
| allowlist.yaml | default_action | reject |
| blocklist.yaml | Categories/Domains/Patterns | 9 / 23 / 4 |
| blocklist.yaml | Lines | 72 |
| canonical_rules.yaml | Rules / Pipeline steps | 10 / 12 |
| canonical_rules.yaml | Lines | 233 |
| ProcedureDoc.v1.schema.json | Lines | 296 |
| ProcedureDoc sample | Completeness | 0.86 |
| test_validators.py | Test count | 5 (5/5 PASS) |

---

## Drift Inventory

### DRIFT-01: Q1-REPORT AGE P1/P2 Split
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 14
- **Claimed:** "25 AGE sources documented (10 P0, 10 P1, 5 P2)"
- **Actual:** P0=10, P1=11, P2=4 (total still 25)
- **Root cause:** `age-boe-sumarios` (BOE Sumarios Diarios) is P1 in registry.yaml, but was grouped under "BOE x3" as P0 in the research phase. When the machine-readable registry was created, it was correctly assigned P1, but Q1-REPORT was never updated.

### DRIFT-02: Q1-REPORT Municipal Domain Count in Allowlist
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 74
- **Claimed:** "Tier 3 (Municipal): 12 seed cities, on-demand expansion"
- **Actual:** 19 domains in tier_3_municipal (7 added by AUDIT-03)
- **Root cause:** Forensic audit (AUDIT-03) added 7 municipal domains to allowlist.yaml but did not propagate the change back to Q1-REPORT.md.

### DRIFT-03: Q1.1-REPORT Municipal Domain Count
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` line 17
- **Claimed:** "allowlist (22 AGE + 19 CCAA + 12 municipal domains)"
- **Actual:** tier_3_municipal has 19 domains (not 12)
- **Root cause:** Same as DRIFT-02. AUDIT-03 added 7 domains to data file but Q1.1-REPORT bullet #3 was not updated.

### DRIFT-04: Q1.1-REPORT Allowlist Line Count
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` line 48
- **Claimed:** "`data/policy/allowlist.yaml` | 319 | 3-tier domain allowlist"
- **Actual:** allowlist.yaml is 355 lines (`wc -l` = 355)
- **Root cause:** After AUDIT-03 added 7 municipal domains + 4 CCAA aliases, the file grew from ~319 to 355 lines. The Q1.1-REPORT artifact table was not updated.

### DRIFT-05: Q1.1-REPORT Test Count (two locations)
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` lines 21, 74
- **Claimed:** Line 21: "3 unit tests covering all validators pass in CI-compatible pytest"; Line 74: "tests/unit/test_validators.py | 3 | 3/3 PASS"
- **Actual:** test_validators.py has 5 tests (5/5 PASS). The two negative tests were added by AUDIT-04.
- **Root cause:** AUDIT-04 added 2 negative tests. Q1.1-REPORT was not updated in either location.

### DRIFT-06: Gates.md AGE P2 Count
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 32
- **Claimed:** "P2 sources: 5 (MUFACE, INE, Catastro, Transparencia)"
- **Actual:** 4 P2 sources. The text claims "5" but lists only 4 names: MUFACE, INE, Catastro, Transparencia.
- **Root cause:** Count label is wrong (says 5, names 4). The 5th entry was likely age-boe-sumarios which was reassigned to P1 during implementation. The count was not updated, nor was a 5th name added.

### DRIFT-07: Gates.md AGE P1 Count
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 31
- **Claimed:** "P1 sources: 10 (Carpeta Ciudadana, Clave, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)"
- **Actual:** 11 P1 sources. The missing source is `age-boe-sumarios` (BOE Sumarios Diarios).
- **Root cause:** Same root cause as DRIFT-06. BOE Sumarios was reclassified from P0 (research) to P1 (implementation) but gates.md still groups it under BOE x3 as P0 on line 30.

### DRIFT-08: Gates.md Pytest Expected Output
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 138
- **Claimed:** "# Output: 3 passed"
- **Actual:** `5 passed` (5/5 PASS)
- **Root cause:** Same as DRIFT-05. AUDIT-04 added 2 tests; gates.md expected output was not updated.

### DRIFT-09: Gates.md Blocklist Categories Count
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 55
- **Claimed:** "8 categories explicitly blocked (commercial, SEO, forums, social media, etc.)"
- **Actual:** 9 categories in blocklist.yaml (the 9th is `ai_generated` with empty domain list)
- **Root cause:** `ai_generated` category has `domains: []` and may have been added after gates.md was written, or was excluded from the count because it has zero domains.

### DRIFT-10: Gates.md Municipal Seed Count
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 54
- **Claimed:** "Tier 3 (Municipal): 12 initial seed cities"
- **Actual:** 19 domains in tier_3_municipal
- **Root cause:** Same root cause as DRIFT-02 and DRIFT-03. AUDIT-03 fix not propagated.

### DRIFT-11: FORENSIC-AUDIT Abort Condition A5 Test Count
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 30
- **Claimed:** "All 4 scripts pass, 3/3 tests pass"
- **Actual:** 5/5 tests pass
- **Root cause:** This line was written before AUDIT-04 added 2 negative tests, and was never updated in the early section even though the "Fixes Applied" section on line 175 correctly states "5/5 PASS."

### DRIFT-12: FORENSIC-AUDIT Claims Ledger Municipal Count
- **Type:** documentation_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 84
- **Claimed:** "Allowlist tier_3_municipal domains | 12 | **12** | VERIFIED"
- **Actual:** 19 domains in tier_3_municipal
- **Root cause:** The Claims Ledger was written pre-AUDIT-03. The forensic audit itself added 7 domains (AUDIT-03) but did not update its own Claims Ledger table.

### DRIFT-13: FORENSIC-AUDIT Gate Claims Unit Test Count
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 106
- **Claimed:** "Unit tests | 3/3 PASS | **3/3 PASS** | VERIFIED"
- **Actual:** 5/5 PASS
- **Root cause:** Same as DRIFT-11. The Gate Claims table was not updated after AUDIT-04.

### DRIFT-14: FORENSIC-AUDIT Commands Section Stale
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 213
- **Claimed:** "pytest tests/unit/test_validators.py -v                # 3/3 PASS"
- **Actual:** 5/5 PASS
- **Root cause:** Verification commands section was written before AUDIT-04 and not updated.

### DRIFT-15: FORENSIC-AUDIT "All 10 Resolved" Behavioral Contradiction
- **Type:** behavioral_drift
- **Severity:** P0
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 165
- **Claimed:** "All 10 audit findings have been resolved."
- **Actual:** Data/code fixes were applied, but report documents (Q1-REPORT, Q1.1-REPORT, gates.md, and even the FORENSIC-AUDIT itself) were NOT updated. At least 14 stale claims remain across 4 documents.
- **Root cause:** The forensic audit defined "resolved" as "code/data fix applied" but did not include a documentation propagation step. This created Layer 2 staleness (docs not updated after Layer 1 data fixes).

### DRIFT-16: V3 Evidence Ground-Truth Test Count
- **Type:** data_drift
- **Severity:** P1
- **Documents:** `docs/arreglos chat/fase-3/audits-v3/evidence/ground-truth-counts.txt` line 36
- **Claimed:** "test_validators.py: 0 tests"
- **Actual:** 5 tests (5/5 PASS as confirmed by g5-pytest.txt in the same evidence directory)
- **Root cause:** The preflight ground-truth counting script likely failed to parse test functions from test_validators.py (possibly looking for `def test_` at top level but missing class-based methods), producing a false "0 tests" count. This contradicts g5-pytest.txt line 6 in the same evidence directory which shows "collected 5 items" and "5 passed."

### DRIFT-17: Gates.md P0 Source Listing Includes P1 Source
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 30
- **Claimed:** "P0 sources: 10 (SIA, PAG, Sede PAG, BOE x3, SEPE, Seg Social, AEAT, Extranjeria, IMV)"
- **Actual:** "BOE x3" implies 3 BOE sources at P0, but only `age-boe-diario` (P0) and `age-boe-legislacion` (P0) are P0. `age-boe-sumarios` is P1 in registry.yaml. The P0 count of 10 is correct only if BOE x3 means 3 P0 sources, but there are only 2 BOE P0 sources.
- **Root cause:** This is consistent with DRIFT-06 and DRIFT-07. When BOE Sumarios was set as P1, the "BOE x3" shorthand became misleading. The P0 count of 10 is still correct (the 10th P0 is `age-inclusion-imv`), but "BOE x3" overcounts BOE P0 sources by 1. The shorthand should be "BOE x2" (diario + legislacion consolidated) plus age-boe-sumarios listed under P1.

### DRIFT-18: Cross-Document False Consistency (Q1-REPORT + gates.md agree on wrong P1/P2)
- **Type:** documentation_drift
- **Severity:** P2
- **Documents:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 14 + `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` lines 31-32
- **Claimed:** Both Q1-REPORT.md and gates.md agree on AGE P1=10, P2=5
- **Actual:** P1=11, P2=4
- **Root cause:** Both documents were written during the research phase before the machine-readable registry diverged. Their mutual agreement creates false reassurance of accuracy.

---

## Drift Summary Statistics

| Type | Count |
|------|-------|
| documentation_drift | 16 |
| behavioral_drift | 1 |
| data_drift | 1 |
| **Total** | **18** |

| Severity | Count |
|----------|-------|
| P0 | 1 (DRIFT-15) |
| P1 | 8 (DRIFT-01, -02, -03, -04, -05, -11, -12, -16) |
| P2 | 9 (DRIFT-06, -07, -08, -09, -10, -13, -14, -17, -18) |

---

## Systemic Root Causes

### RC-1: Post-Fix Documentation Propagation Failure
**Affects:** DRIFT-02, -03, -04, -05, -08, -10, -11, -12, -13, -14, -15 (11 drifts)

The forensic audit (AUDIT-01 through AUDIT-10) fixed data and code artifacts but did NOT propagate numeric changes back to report files. This is the single largest root cause, responsible for 11 of 18 drifts.

### RC-2: Research-to-Implementation Priority Divergence
**Affects:** DRIFT-01, -06, -07, -17, -18 (5 drifts)

When the Q1 research (markdown) was converted to Q1.1 implementation (YAML), `age-boe-sumarios` was reclassified from implicit P0 ("BOE x3") to explicit P1. The research documents were never updated to reflect the final priority assignment.

### RC-3: Preflight Script Bug
**Affects:** DRIFT-16 (1 drift)

The v3 ground-truth counting script produced a false "0 tests" count for test_validators.py, likely because it searched for top-level `def test_` functions but missed class-based test methods.

---

*Generated by A3v3 (Drift & Consistency Reconciler), 2026-02-18*
*Mode: STRICT READ-ONLY -- zero files modified*
