# Doc Drift Fixes Applied

Date: 2026-02-19
Total: 34 fixes (26 P1 + 8 P2)

## Summary

All 34 doc-drift fixes from the FIX-PLAN have been applied across 5 markdown files. Fixes correct numeric mismatches, semantic overstatements, and precision gaps identified during forensic audit cross-referencing.

## Changes

| Fix# | File | Status | Old (truncated) | New (truncated) |
|------|------|--------|-----------------|-----------------|
| FIX-01 | Q1-REPORT.md | APPLIED | 25 AGE sources documented (10 P0, 10 P1, 5 P2) | 25 AGE sources documented (10 P0, 11 P1, 4 P2) |
| FIX-02 | Q1-REPORT.md | APPLIED | P1 (Important) count: 10 | P1 (Important) count: 11 |
| FIX-03 | Q1-REPORT.md | APPLIED | P2 (Secondary) count: 5 | P2 (Secondary) count: 4 |
| FIX-04 | Q1-REPORT.md | APPLIED | Tier 3 (Municipal): 12 seed cities, on-demand expansion | Tier 3 (Municipal): 19 municipal domains, on-demand expansion |
| FIX-05 | Q1.1-REPORT.md | APPLIED | allowlist (22 AGE + 19 CCAA + 12 municipal domains) | allowlist (22 AGE + 19 CCAA + 19 municipal domains) |
| FIX-06 | Q1.1-REPORT.md | ADAPTED | **3 unit tests** covering all validators... | **5 unit tests** (3 happy-path + 2 negative) covering schema validators... |
| FIX-07 | Q1.1-REPORT.md | APPLIED | allowlist.yaml: 319 | allowlist.yaml: 355 |
| FIX-08 | Q1.1-REPORT.md | APPLIED | test_validators.py \| 3 \| 3/3 PASS | test_validators.py \| 5 \| 5/5 PASS |
| FIX-09 | Q1.1-REPORT.md | ADAPTED | A3 - Reproducible validation/gates \| CLEAR \| 4 scripts, all runnable, 3 pytest tests | A3 - Reproducible validation/gates \| CLEAR \| 4 scripts, all runnable, 5 pytest tests |
| FIX-10 | gates.md | ADAPTED | # Output: 3 passed (in gates.md commands section) | # Output: 5 passed |
| FIX-11 | gates.md | APPLIED | P1 sources: 10 ... P2 sources: 5 | P1 sources: 11 ... P2 sources: 4 |
| FIX-12 | gates.md | APPLIED | Tier 3 (Municipal): 12 initial seed cities | Tier 3 (Municipal): 19 municipal domains |
| FIX-13 | gates.md | APPLIED | Blocklist: 8 categories explicitly blocked | Blocklist: 9 categories explicitly blocked |
| FIX-14 | gates.md | APPLIED | A3 \| Reproducible validation scripts \| CLEAR (4 scripts, 3 tests) | A3 \| Reproducible validation scripts \| CLEAR (4 scripts, 5 tests) |
| FIX-15 | FORENSIC-AUDIT.md | APPLIED | All 4 scripts pass, 3/3 tests pass | All 4 scripts pass, 5/5 tests pass |
| FIX-16 | FORENSIC-AUDIT.md | ADAPTED | tier_3_municipal domains \| 12 \| **12** \| VERIFIED | tier_3_municipal domains \| 12 \| **19** \| CONTRADICTED (grew from 12 to 19 after AUDIT-03 fix) |
| FIX-17 | Q1.1-REPORT.md | APPLIED | all executable, all passing | all executable; 3 schema validators pass; link_check.py passes in dry-run/smoke mode... |
| FIX-18 | Q1.1-REPORT.md | ADAPTED | **All 6 gates passed** (G1-G6), all 4 abort conditions cleared | **5 of 6 gates passed cleanly** (G1-G3, G5-G6); G4 passed in smoke/dry-run mode only... |
| FIX-19 | Q1.1-REPORT.md | APPLIED | fully validated, machine-readable foundation | schema-validated, machine-readable foundation |
| FIX-20 | gates.md | APPLIED | PASS (20 cities, all verified) | PASS (20 cities, all research-documented; HTTP verification deferred to Q2) |
| FIX-21 | gates.md | APPLIED | Tier 1 cities: 20 (all with verified sede electronica URLs) | Tier 1 cities: 20 (all with research-documented sede electronica URLs; HTTP verification pending Q2) |
| FIX-22 | gates.md | APPLIED | Gates passed \| 6/6 | Gates passed \| 6/6 (G4 limited to smoke/dry-run; see forensic audit) |
| FIX-23 | gates.md | APPLIED | Municipal URLs verified \| 20 | Municipal URLs documented \| 20 (HTTP verification pending Q2) |
| FIX-24 | gates.md | APPLIED | G4: Link checker works \| ... \| PASS (3/3 URLs OK) | G4: Link checker runs \| ... \| PASS (smoke only) -- full-registry live test had crash bug |
| FIX-25 | FORENSIC-AUDIT.md | APPLIED | Core claims (44 sources, 25 AGE, 19 CCAA, 20 local, 6/6 gates) are all VERIFIED | Core claims (...20 local) are VERIFIED; gates are 5/6 clean PASS + G4 partial |
| FIX-26 | references.md | APPLIED | Municipal URLs verified \| 20/20 (Tier 1) | Municipal URLs documented \| 20/8,131 (Tier 1 seed cities; 0.25% of all municipalities) |
| FIX-27 | Q1-REPORT.md | APPLIED | All 4 abort conditions cleared. | All 4 abort conditions cleared (A3 flagged as concern in forensic audit due to 14 allowlist coverage gaps). |
| FIX-28 | Q1-REPORT.md | APPLIED | Status: COMPLETE (research-only, no code changes) | Status: RESEARCH COMPLETE (documentation only -- validation, HTTP checks, and API testing deferred to Q2) |
| FIX-29 | Q1-REPORT.md | APPLIED | No code was written. All output is research documentation | No src/ production code was written. All Q1 output is research documentation (Q1.1 added validation scripts and data artifacts) |
| FIX-30 | Q1.1-REPORT.md | APPLIED | **Status:** COMPLETE | **Status:** COMPLETE (post-audit fixes applied; see FORENSIC-AUDIT-REPORT for 10 resolved findings) |
| FIX-31 | Q1.1-REPORT.md | APPLIED | Convert Q1 research markdown into machine-readable, validated artifacts | Convert Q1 research markdown into machine-readable, schema-validated artifacts |
| FIX-32 | FORENSIC-AUDIT.md | APPLIED | the vast majority are VERIFIED | the ~30 most critical claims were individually verified...; remaining claims were not individually audited |
| FIX-33 | FORENSIC-AUDIT.md | APPLIED | Hallucination Risk Score: 12/100 (LOW) | Hallucination Risk Assessment: LOW -- Core data claims are accurate; discrepancies found in secondary metrics... |
| FIX-34 | FORENSIC-AUDIT.md | APPLIED | All 29 declared files exist. VERIFIED | All 29 declared files exist (structural check). VERIFIED. (Content correctness verified separately in claims ledger.) |

## File Summary

| File | Fixes Applied | Fix IDs |
|------|--------------|---------|
| Q1-REPORT.md | 7 | FIX-01 to FIX-04, FIX-27 to FIX-29 |
| Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md | 11 | FIX-05 to FIX-10, FIX-17 to FIX-19, FIX-30, FIX-31 |
| evidence/gates.md | 10 | FIX-10 to FIX-14, FIX-20 to FIX-24 |
| evidence/Q1.1-FORENSIC-AUDIT-REPORT.md | 6 | FIX-15, FIX-16, FIX-25, FIX-32 to FIX-34 |
| evidence/references.md | 1 | FIX-26 |

## Adaptation Notes

- **FIX-06**: Plan text `"3 unit tests covering..."` matched as `"**3 unit tests** covering..."` (markdown bold markers)
- **FIX-09**: Plan text targeted `"A3 - Reproducible validation scripts: CLEAR (4 scripts, 3 tests)"` -- actual file used table format with different separator; adapted to match table row
- **FIX-10**: Plan said target was Q1.1-REPORT.md but `"# Output: 3 passed"` was found in gates.md commands section; applied there
- **FIX-16**: Plan text used em-dash format `"claimed 12, actual 12 — VERIFIED"` -- actual file used table format `| 12 | **12** | VERIFIED |`; adapted to table format
- **FIX-18**: Plan text `"All 6 gates passed"` matched as `"**All 6 gates passed**"` (markdown bold markers)
