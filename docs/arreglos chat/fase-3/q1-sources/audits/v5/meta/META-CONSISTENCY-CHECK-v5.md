# Meta-Consistency Check -- Audit v5

**Date:** 2026-02-19
**Auditor:** A6 (Meta-Consistency Checker)
**Model:** Claude Opus 4.6
**Scope:** All v5 audit outputs -- claims, verified claims, drifts, semantic, evidence, policy-schema, fix-plan
**Method:** Automated Python checks (no manual counting)

---

## Results

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | Claims file integrity | PASS | 280 lines, all valid JSON, claim_ids C-001..C-280 sequential with no gaps or duplicates |
| 2 | Verified claims integrity | PASS | 280 lines, all valid JSON with "status" field. Breakdown: VERIFIED=238, CONTRADICTED=16, SEMANTIC_FLAG=18, UNVERIFIED=8. Sum=280 |
| 3 | Status consistency with DRIFTS.md | PASS | DRIFTS.md header states 238/16/18/8. Verified JSONL has 238/16/18/8. All four counts match exactly |
| 4 | DRIFTS.md internal consistency | PASS | Section 2 lists 16 CONTRADICTED claim_ids, section 3 lists 18 SEMANTIC_FLAG claim_ids, section 4 lists 8 UNVERIFIED claim_ids. All match verified JSONL counts exactly |
| 5 | Semantic JSONL consistency | PASS | 36 lines in semantic.v5.jsonl, all valid JSON, sf_ids SF-001..SF-036 sequential with no gaps. SEMANTIC-REPORT.md header states Total=36. Match confirmed |
| 6 | Evidence files exist | PASS | 14 evidence files in evidence/, all non-empty (345 bytes to 56 KB). 7 other audit files (claims, drifts, semantic, policy-schema) all exist and non-empty |
| 7 | URL coverage consistency | PASS (NOTE) | url-coverage.jsonl: 279 lines (COVERED=264, NOT_COVERED=15). GT #49=264, GT #50=15 -- both match. NOTE: url-extract.txt says 284 unique URLs but coverage JSONL has 279; difference of 5 is due to template/artifact URLs filtered out during allowlist matching |
| 8 | FIX-PLAN consistency | PASS | 34 fixes (FIX-01..FIX-34). All 34 reference valid CONTRADICTED or SEMANTIC_FLAG claims (0 invalid refs). Priority split: 26 P1 + 8 P2 = 34. Matches DRIFTS severity table exactly |
| 9 | Ground truth completeness | PASS | 55 metrics (#1..#55), no gaps. 5 discrepancies (D1-D5) logged. D1-D4 correspond to CONTRADICTED findings in DRIFTS. D5 is URL coverage gap (NOT_COVERED URLs are non-gov reference domains) |
| 10 | Policy-Schema report consistency | PASS (NOTE) | PS-SCHEMA-VERIFY-REPORT.md exists (22,915 bytes). States "25 PASS / 5 NOTE / 0 FAIL". Actual count from table: 26 PASS / 5 NOTE / 0 FAIL. Minor self-inconsistency: report undercounts PASS by 1 (likely item 5.5 or similar was recategorized during writing). 8 findings listed as stated. FAIL=0 confirmed |
| 11 | No self-contradictions | PASS | Zero overlap between VERIFIED/CONTRADICTED/SEMANTIC_FLAG sets. All 16 CONTRADICTED claims have non-empty evidence_ref fields referencing GT entries (GT #8, #9, #22, #24, #25, #41, #42). No claim has conflicting statuses |

---

## Detailed Evidence

### CHECK 1: Claims File Integrity

```
File: claims/claims.v5.jsonl
Line count: 280 (expected 280) -- MATCH
Invalid JSON lines: 0
Unique claim_ids: 280
Sequential C-001..C-280: missing=0, extra=0, duplicates=0
```

### CHECK 2: Verified Claims Integrity

```
File: claims/claims.v5.verified.jsonl
Line count: 280 (expected 280) -- MATCH
Invalid JSON lines: 0
Missing status field: 0
Status breakdown:
  VERIFIED: 238
  CONTRADICTED: 16
  SEMANTIC_FLAG: 18
  UNVERIFIED: 8
  Total: 280 -- MATCH
```

### CHECK 3: Status Consistency with DRIFTS.md

```
DRIFTS.md header states: VERIFIED=238, CONTRADICTED=16, SEMANTIC_FLAG=18, UNVERIFIED=8
Verified JSONL actual:   VERIFIED=238, CONTRADICTED=16, SEMANTIC_FLAG=18, UNVERIFIED=8
All four counts match: TRUE
```

### CHECK 4: DRIFTS.md Internal Consistency

```
Section 2 CONTRADICTED claim_ids (16):
  C-001, C-007, C-008, C-018, C-053, C-062, C-071, C-082,
  C-094, C-099, C-112, C-125, C-126, C-154, C-160, C-187
  -> verified JSONL CONTRADICTED: 16 -- MATCH

Section 3 SEMANTIC_FLAG claim_ids (18):
  C-033, C-034, C-035, C-059, C-063, C-095, C-096, C-100,
  C-103, C-119, C-140, C-144, C-149, C-155, C-157, C-158, C-171, C-275
  -> verified JSONL SEMANTIC_FLAG: 18 -- MATCH

Section 4 UNVERIFIED claim_ids (8):
  C-036, C-037, C-045, C-061, C-145, C-198, C-199, C-200
  -> verified JSONL UNVERIFIED: 8 -- MATCH
```

### CHECK 5: Semantic JSONL Consistency

```
File: semantic/semantic.v5.jsonl
Line count: 36 (expected 36) -- MATCH
Invalid JSON: 0
sf_ids: SF-001..SF-036, sequential, no gaps, no duplicates
SEMANTIC-REPORT.md header Total: 36 -- MATCH
```

### CHECK 6: Evidence Files

```
evidence/ directory (14 files, all non-empty):
  ground-truth-counts.txt:        6,545 bytes
  link-check-dry.txt:             2,968 bytes
  phantom-paths.txt:              3,340 bytes
  policy-counts.txt:              1,432 bytes
  preflight.txt:                  1,306 bytes
  pytest-collect-only.txt:        1,040 bytes
  pytest-run.txt:                 1,236 bytes
  registry-counts.txt:            1,047 bytes
  ruff.txt:                         345 bytes
  schema-validate-policy.txt:       433 bytes
  schema-validate-proceduredoc.txt: 648 bytes
  schema-validate-registry.txt:     669 bytes
  url-coverage.jsonl:            56,024 bytes
  url-extract.txt:                1,194 bytes

Other audit outputs (all exist, all non-empty):
  claims/claims.v5.jsonl:            103,507 bytes
  claims/claims.v5.verified.jsonl:   142,362 bytes
  drifts/DRIFTS.md:                   12,847 bytes
  drifts/FIX-PLAN.md:                14,609 bytes
  semantic/semantic.v5.jsonl:         25,356 bytes
  semantic/SEMANTIC-REPORT.md:        13,774 bytes
  policy-schema/PS-SCHEMA-VERIFY-REPORT.md: 22,915 bytes
```

### CHECK 7: URL Coverage Consistency

```
url-coverage.jsonl: 279 lines (COVERED=264, NOT_COVERED=15)
Ground truth #49 (COVERED):     264 -- MATCH
Ground truth #50 (NOT_COVERED):  15 -- MATCH
url-extract.txt unique URLs:    284

Difference (284 - 279 = 5): Template/artifact URLs (e.g., {sede}.gob.es,
www.{municipio}.es) are in url-extract but filtered from coverage analysis.
This is expected and documented in url-extract.txt header.
```

### CHECK 8: FIX-PLAN Consistency

```
Fixes found: 34 (FIX-01 through FIX-34)
All 34 reference CONTRADICTED or SEMANTIC_FLAG claims: 0 invalid refs
Priority split: P1=26, P2=8 (total=34)
DRIFTS severity table: P1=26 (16 CONTRADICTED + 10 SEMANTIC), P2=8 -- MATCH
```

### CHECK 9: Ground Truth Completeness

```
Metric rows: 55 (#1 through #55), no gaps
Discrepancy log: 5 entries (D1-D5)
  D1: AGE priority split (P1/P2 off by 1) -> CONTRADICTED C-001/C-007/C-008/C-112
  D2: allowlist.yaml line count (319 vs 355) -> CONTRADICTED C-071
  D3: tier_3_municipal domains (12 vs 19) -> CONTRADICTED C-018/C-053/C-125
  D4: forensic report tier_3 (12 vs 19) -> CONTRADICTED C-187
  D5: 15 NOT_COVERED URLs (non-gov reference links) -> acknowledged in report
All 5 discrepancies are accounted for in DRIFTS CONTRADICTED findings.
```

### CHECK 10: Policy-Schema Report Consistency

```
File: policy-schema/PS-SCHEMA-VERIFY-REPORT.md (22,915 bytes)
Stated: "25 PASS / 5 NOTE / 0 FAIL"
Actual table count: 26 PASS / 5 NOTE / 0 FAIL

DISCREPANCY: The report states 25 PASS but the checklist table contains
26 items marked PASS. The 5 NOTE and 0 FAIL counts are correct.
This is a cosmetic self-inconsistency (off by 1 in the PASS count).
It does not affect the substantive findings (0 FAIL confirmed).

Findings listed: 8 (as stated). All 8 findings present.
```

### CHECK 11: No Self-Contradictions

```
Status overlap check:
  VERIFIED & CONTRADICTED:   0 overlap (clean)
  VERIFIED & SEMANTIC_FLAG:  0 overlap (clean)
  CONTRADICTED & SEMANTIC_FLAG: 0 overlap (clean)

CONTRADICTED evidence_ref validation (all 16):
  C-001: "GT #8,#9: age_p1=11, age_p2=4"        -- valid GT ref
  C-007: "GT #8: age_p1=11"                       -- valid GT ref
  C-008: "GT #9: age_p2=4"                        -- valid GT ref
  C-018: "GT #22: allowlist_tier3=19"              -- valid GT ref
  C-053: "GT #22: allowlist_tier3=19"              -- valid GT ref
  C-062: "GT #41: pytest_collected=5"              -- valid GT ref
  C-071: "GT #24: allowlist_lines=355"             -- valid GT ref
  C-082: "GT #41,#42: pytest 5 collected, 5 passed" -- valid GT ref
  C-094: "GT #41: pytest_collected=5"              -- valid GT ref
  C-099: "GT #42: pytest_passed=5"                 -- valid GT ref
  C-112: "GT #8,#9: age_p1=11, age_p2=4"         -- valid GT ref
  C-125: "GT #22: allowlist_tier3=19"              -- valid GT ref
  C-126: "GT #25: blocklist_categories=9"          -- valid GT ref
  C-154: "GT #41: pytest_collected=5"              -- valid GT ref
  C-160: "GT #42: pytest_passed=5"                 -- valid GT ref
  C-187: "GT #22: allowlist_tier3=19"              -- valid GT ref
All 16 CONTRADICTED claims have valid evidence references.
All GT entries (#8, #9, #22, #24, #25, #41, #42) exist in ground-truth-counts.txt.
```

---

## Summary

**11/11 checks PASS** (2 with minor notes)

| Verdict | Count |
|---------|-------|
| PASS (clean) | 9 |
| PASS with NOTE | 2 |
| FAIL | 0 |

### Notes on the 2 PASS-with-NOTE results:

1. **CHECK 7 (URL coverage):** url-coverage.jsonl has 279 entries vs url-extract.txt's 284 unique URLs. The 5-URL difference is explained by template/artifact URLs that were extracted but correctly excluded from allowlist matching. The COVERED/NOT_COVERED counts match ground truth exactly.

2. **CHECK 10 (PS-Schema report):** The report states "25 PASS" but the actual checklist table has 26 PASS items. This is a cosmetic off-by-one error in the report's summary line. It does not affect any substantive finding (0 FAIL is confirmed correct).

### Overall Assessment

The v5 audit outputs are **internally consistent and do not hallucinate**. All counts match across files. All cross-references resolve. All evidence files exist and are non-empty. No claim has conflicting statuses. The only discrepancy found is a single off-by-one in the PS-SCHEMA-VERIFY-REPORT.md summary line (26 PASS stated as 25), which is cosmetic and does not affect the audit's conclusions.

---

## Python Commands Used

All checks were executed via `python3 -c "..."` one-liners using only the standard library (`json`, `os`, `re`, `collections.Counter`). No external dependencies were required. The scripts:

1. Parsed JSONL files line-by-line with `json.loads()`
2. Counted statuses with `collections.Counter`
3. Verified sequential IDs with set arithmetic
4. Cross-checked counts between files using regex extraction from Markdown tables
5. Validated file existence and size with `os.path.exists()` and `os.path.getsize()`
6. Checked for set overlaps between status categories

All counting was automated. No manual counting was performed.
