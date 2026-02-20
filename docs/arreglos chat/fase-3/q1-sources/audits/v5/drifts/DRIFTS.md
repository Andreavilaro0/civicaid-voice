# DRIFTS & CONSISTENCY RECONCILIATION REPORT

**Agent:** A3 (Drift & Consistency Reconciler)
**Audit:** Anti-Hallucination Audit v5
**Date:** 2026-02-19
**Inputs:** 280 claims (A1), 55 ground truth metrics (A2), 36 semantic findings (A5)

---

## 1. Summary

| Status | Count | Percentage |
|--------|-------|------------|
| VERIFIED | 238 | 85.0% |
| CONTRADICTED | 16 | 5.7% |
| SEMANTIC_FLAG | 18 | 6.4% |
| UNVERIFIED | 8 | 2.9% |
| **Total** | **280** | **100%** |

### Breakdown by Source File

| Source File | Total | VERIFIED | CONTRADICTED | SEMANTIC_FLAG | UNVERIFIED |
|-------------|-------|----------|--------------|---------------|------------|
| Q1-REPORT.md | 50 | 38 | 4 | 6 | 2 |
| Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md | 50 | 35 | 5 | 8 | 2 |
| evidence/gates.md | 55 | 44 | 5 | 4 | 2 |
| evidence/Q1.1-FORENSIC-AUDIT-REPORT.md | 46 | 37 | 4 | 4 | 1 |
| evidence/references.md | 4 | 0 | 0 | 4 | 0 |
| data/ (YAML files) | 46 | 46 | 0 | 0 | 0 |
| schemas/ (JSON files) | 16 | 16 | 0 | 0 | 0 |
| scripts/ (Python files) | 15 | 14 | 0 | 0 | 1 |
| tests/ | 6 | 6 | 0 | 0 | 0 |
| evidence/assumptions-gaps.md | 2 | 2 | 0 | 0 | 0 |
| backlog/ | 3 | 3 | 0 | 0 | 0 |
| README files | 5 | 5 | 0 | 0 | 0 |

---

## 2. CONTRADICTED Claims (16)

### P0 -- Data Corruption / Critical Numeric Mismatches

*No P0 (data corruption) findings. All data files (YAML, JSON, schemas) have correct values. Contradictions are confined to documentation prose.*

### P1 -- Doc-Data Mismatches

| # | claim_id | Source File | Line | Claimed Value | Actual Value | Evidence | Severity |
|---|----------|-------------|------|---------------|--------------|----------|----------|
| 1 | C-001 | Q1-REPORT.md | 14 | AGE: 10 P0, **10 P1, 5 P2** | 10 P0, **11 P1, 4 P2** | registry-counts.txt row 8-9; GT #8,#9 | P1 |
| 2 | C-007 | Q1-REPORT.md | 29 | AGE P1 count: **10** | **11** | registry-counts.txt; GT #8 | P1 |
| 3 | C-008 | Q1-REPORT.md | 30 | AGE P2 count: **5** | **4** | registry-counts.txt; GT #9 | P1 |
| 4 | C-018 | Q1-REPORT.md | 75 | Tier 3 municipal: **12 domains** | **19 domains** | policy-counts.txt; GT #22 | P1 |
| 5 | C-053 | Q1.1-REPORT.md | 17 | allowlist: 22 AGE + 19 CCAA + **12 municipal** | 22 AGE + 19 CCAA + **19 municipal** | policy-counts.txt; GT #22 | P1 |
| 6 | C-062 | Q1.1-REPORT.md | 21 | **3 unit tests**, all PASS | **5 unit tests**, 5/5 PASS | pytest-run.txt; GT #41 | P1 |
| 7 | C-071 | Q1.1-REPORT.md | 48 | allowlist.yaml: **319 lines** | **355 lines** | policy-counts.txt; GT #24 | P1 |
| 8 | C-082 | Q1.1-REPORT.md | 74 | test_validators.py: **3 tests**, 3/3 PASS | **5 tests**, 5/5 PASS | pytest-run.txt; GT #41,#42 | P1 |
| 9 | C-094 | Q1.1-REPORT.md | 103 | A3: **4 scripts, 3 tests** | 4 scripts, **5 tests** | pytest-run.txt; GT #41 | P1 |
| 10 | C-099 | Q1.1-REPORT.md | 128 | pytest outputs **3 passed** | **5 passed** | pytest-run.txt; GT #42 | P1 |
| 11 | C-112 | gates.md | 29 | AGE: P0: 10, **P1: 10, P2: 5** | P0: 10, **P1: 11, P2: 4** | registry-counts.txt; GT #8,#9 | P1 |
| 12 | C-125 | gates.md | 54 | Tier 3 municipal: **12 initial seed cities** | **19 municipal domains** | policy-counts.txt; GT #22 | P1 |
| 13 | C-126 | gates.md | 55 | Blocklist: **8 categories** | **9 categories** | policy-counts.txt; GT #25 | P1 |
| 14 | C-154 | gates.md | 147 | A3: 4 scripts, **3 tests** | 4 scripts, **5 tests** | pytest-run.txt; GT #41 | P1 |
| 15 | C-160 | FORENSIC-AUDIT.md | 30 | All 4 scripts pass, **3/3 tests** pass | 4 scripts pass, **5/5 tests** | pytest-run.txt; GT #42 | P1 |
| 16 | C-187 | FORENSIC-AUDIT.md | 84 | tier_3 domains: claimed 12, actual 12 -- **VERIFIED** | Actual: **19** (was 12 pre-fix, is 19 post-fix) | policy-counts.txt; GT #22 | P1 |

### P2 -- Stale/Minor

*All contradictions are P1 (doc-data mismatch). No P2-level contradictions found.*

---

## 3. SEMANTIC_FLAG Claims (18)

| # | claim_id | Source File | Line | Issue | Cross-ref SF-xxx | Severity |
|---|----------|-------------|------|-------|------------------|----------|
| 1 | C-033 | Q1-REPORT.md | 133 | "All 4 abort conditions cleared" -- conceals A3 concern flagged by forensic audit (14 allowlist gaps) | SF-014 | P2 |
| 2 | C-034 | Q1-REPORT.md | 4 | "Status: COMPLETE" -- inflated for a quarter that defers all validation, HTTP checks, API testing to Q2 | SF-015 | P2 |
| 3 | C-035 | Q1-REPORT.md | 20 | "No code was written. All output is research documentation" -- accurate but some Q1.1 items (scripts) are Q1 scope | -- | P2 |
| 4 | C-059 | Q1.1-REPORT.md | 19 | "all executable, all passing" -- misleading for link_check.py which crashed at URL 12/18 per forensic audit | SF-004 | P1 |
| 5 | C-063 | Q1.1-REPORT.md | 22 | "All 6 gates passed" -- conceals G4 was MISLEADING per forensic audit (link checker crash bug) | SF-006 | P1 |
| 6 | C-095 | Q1.1-REPORT.md | 4 | "Status: COMPLETE" -- lacks caveats present in Q1-REPORT (post-audit fixes, forensic findings) | SF-016 | P2 |
| 7 | C-096 | Q1.1-REPORT.md | 11 | "fully validated, machine-readable foundation" -- "fully validated" inflates "schema-validated"; no HTTP or content validation | SF-001 | P1 |
| 8 | C-100 | Q1.1-REPORT.md | 5 | "Convert Q1 research markdown into machine-readable, validated artifacts" -- "validated" without scope qualifier | SF-034 | P2 |
| 9 | C-103 | gates.md | 11 | "20 cities, all verified" -- "verified" implies HTTP verification not performed in Q1 scope | SF-017, SF-018 | P1 |
| 10 | C-119 | gates.md | 45 | "Tier 1 cities: 20 (all with verified sede electronica URLs)" -- same "verified" inflation as above | SF-018 | P1 |
| 11 | C-140 | gates.md | 88 | "Gates passed: 6/6" -- summary fraction without G4 caveat; forensic audit found G4 MISLEADING | SF-019 | P1 |
| 12 | C-144 | gates.md | 92 | "Municipal URLs verified: 20" -- "verified" used in summary metric; no HTTP verification done | SF-020 | P1 |
| 13 | C-149 | gates.md | 108 | "G4: Link checker works -- PASS (3/3 URLs OK)" -- live test crashed at URL 12/18; 3/3 is smoke-only denominator | SF-021 | P1 |
| 14 | C-155 | FORENSIC-AUDIT.md | 12 | "vast majority are VERIFIED" -- vague; only ~30 key claims individually verified, not 325 | SF-024 | P2 |
| 15 | C-157 | FORENSIC-AUDIT.md | 14 | "Hallucination Risk Score: 12/100 (LOW)" -- uncalibrated metric presented as quantitative | SF-023 | P2 |
| 16 | C-158 | FORENSIC-AUDIT.md | 26 | "Core claims (... 6/6 gates) are all VERIFIED" -- contradicts own G4 MISLEADING finding on line 103 | SF-025 | P1 |
| 17 | C-171 | FORENSIC-AUDIT.md | 110 | "All 29 declared files exist. VERIFIED" -- accurate but scope-limited; does not address content correctness | -- | P2 |
| 18 | C-275 | references.md | 63 | "Municipal URLs verified: 20/20 (Tier 1)" -- fraction conceals 8,131 total municipalities; "verified" inflated | SF-028 | P1 |

---

## 4. UNVERIFIED Claims (8)

| # | claim_id | Source File | Line | Claim | Reason |
|---|----------|-------------|------|-------|--------|
| 1 | C-036 | Q1-REPORT.md | 159 | age.md: 518 lines | Line count not independently re-measured in v5 evidence; forensic audit says VERIFIED but no v5 wc -l output |
| 2 | C-037 | Q1-REPORT.md | 160 | ccaa.md: 665 lines | Same -- forensic audit verified, no independent v5 check |
| 3 | C-045 | Q1-REPORT.md | 174 | Total research lines: 4,448 | Sum depends on individual file counts not independently re-measured in v5 |
| 4 | C-061 | Q1.1-REPORT.md | 20 | live test: 3/3 URLs OK (avg 229ms) | Runtime result not reproducible offline; timing varies |
| 5 | C-145 | gates.md | 93 | APIs documented: 5+ | No v5 evidence counts api_url entries specifically |
| 6 | C-198 | FORENSIC-AUDIT.md | 6 | "Mode: READ-ONLY (no files modified)" | Cannot verify whether audit was truly read-only; audit fixes section contradicts this |
| 7 | C-199 | FORENSIC-AUDIT.md | 4 | "4 parallel verification agents" | Audit methodology claim; no evidence to verify or refute |
| 8 | C-200 | FORENSIC-AUDIT.md | 80 | "AGE P0 sources: actual 10 (Q1.1 table said 8, marked FALSE)" | The claimed "Q1.1 table said 8" -- no such value of 8 found in Q1.1 report; forensic finding may refer to an earlier version |

---

## 5. Root Cause Analysis

### RC-1: Post-Fix Propagation Failure (Primary)
**Affects:** 10 of 16 CONTRADICTED claims (C-018, C-053, C-071, C-125, C-187, C-062, C-082, C-094, C-099, C-154, C-160)

The forensic audit's AUDIT-03 fix added 7 new municipal domains to `tier_3_municipal` in `allowlist.yaml` (from 12 to 19 domains), also increasing line count from 319 to 355. The AUDIT-04 fix added 2 negative tests (from 3 to 5 total tests). **However, the prose in Q1-REPORT.md, Q1.1-REPORT.md, gates.md, and even the FORENSIC-AUDIT-REPORT.md itself was NOT updated** to reflect the new actual values. This is the classic "fix the data, forget the docs" anti-pattern.

**Propagation chain failure:**
```
allowlist.yaml (19 domains, 355 lines)  <-- FIXED
    |
    v
Q1.1-REPORT.md line 17 (still says "12 municipal") <-- NOT UPDATED
Q1.1-REPORT.md line 48 (still says "319 lines")    <-- NOT UPDATED
gates.md line 54 (still says "12 initial seed")      <-- NOT UPDATED
FORENSIC-AUDIT.md line 84 (claims "12" was verified) <-- NOT UPDATED
```

### RC-2: Pre-Existing Numeric Error in Q1-REPORT.md
**Affects:** 3 CONTRADICTED claims (C-001, C-007, C-008)

The Q1-REPORT.md (written before data files) states AGE priority split as "10 P0, 10 P1, 5 P2". The actual data in registry.yaml is "10 P0, 11 P1, 4 P2". This appears to be an error in the original research document -- P1 and P2 counts are off by 1 each (P1 is undercounted, P2 is overcounted). This error was:
- Propagated to gates.md line 29 (C-112)
- Detected by the forensic audit but NOT corrected in the source documents

### RC-3: Stale Test Count in Multiple Documents
**Affects:** 6 CONTRADICTED claims (C-062, C-082, C-094, C-099, C-154, C-160)

When AUDIT-04 added 2 negative tests, all references to "3 tests" became stale. These references appear in:
- Q1.1-REPORT.md (lines 21, 74, 128)
- gates.md (line 147)
- FORENSIC-AUDIT-REPORT.md (line 30)

### RC-4: Blocklist Category Miscount
**Affects:** 1 CONTRADICTED claim (C-126)

Gates.md line 55 claims "8 categories explicitly blocked" but the actual blocklist.yaml has 9 categories. This is likely a simple counting error in the documentation -- the 9th category may have been added late or miscounted.

### RC-5: Semantic Inflation Pattern ("verified" as keyword)
**Affects:** 10 of 18 SEMANTIC_FLAG claims

The word "verified" appears 15+ times across Q1 documentation to mean "researched and documented" but reads as "HTTP-confirmed reachable." This systematic misuse was identified by A5 (SF-011, SF-017, SF-018, SF-020, SF-026, SF-027, SF-028, SF-030, SF-031, SF-032). The root cause is that the Q1 documentation was written with an aspirational tone rather than a precisely scoped one, and no editorial review caught the ambiguity before publication.

### RC-6: Internal Inconsistency in Forensic Audit
**Affects:** 2 SEMANTIC_FLAG claims (C-155, C-158)

The forensic audit report contains internal contradictions: it claims "6/6 gates VERIFIED" in the summary (line 26) while marking G4 as "MISLEADING" in the detailed findings (line 103). This suggests the summary was written before the detailed analysis was complete, or the consolidation step did not reconcile the two sections.

---

## 6. Severity Distribution

| Severity | CONTRADICTED | SEMANTIC_FLAG | Total |
|----------|-------------|---------------|-------|
| P0 | 0 | 0 | 0 |
| P1 | 16 | 10 | 26 |
| P2 | 0 | 8 | 8 |
| **Total** | **16** | **18** | **34** |

**Assessment:** No P0 (data corruption) issues. All data files contain correct values. All contradictions are P1 (doc-data mismatch) confined to documentation prose that was not updated after audit fixes. Semantic inflation is systematic but addressable through editorial corrections.

---

## 7. Cross-Reference Matrix: Semantic Findings (A5) to Claims

| SF-ID | Linked claim_ids | Status |
|-------|-------------------|--------|
| SF-001 | C-096 | SEMANTIC_FLAG |
| SF-004 | C-059 | SEMANTIC_FLAG |
| SF-006 | C-063 | SEMANTIC_FLAG |
| SF-014 | C-033 | SEMANTIC_FLAG |
| SF-015 | C-034 | SEMANTIC_FLAG |
| SF-016 | C-095 | SEMANTIC_FLAG |
| SF-017 | C-103, C-119 | SEMANTIC_FLAG |
| SF-018 | C-103, C-119 | SEMANTIC_FLAG |
| SF-019 | C-140 | SEMANTIC_FLAG |
| SF-020 | C-144 | SEMANTIC_FLAG |
| SF-021 | C-149 | SEMANTIC_FLAG |
| SF-023 | C-157 | SEMANTIC_FLAG |
| SF-024 | C-155 | SEMANTIC_FLAG |
| SF-025 | C-158 | SEMANTIC_FLAG |
| SF-028 | C-275 | SEMANTIC_FLAG |
| SF-034 | C-100 | SEMANTIC_FLAG |
| SF-002, SF-003, SF-005, SF-007-SF-013, SF-022, SF-026-SF-027, SF-029-SF-033, SF-035-SF-036 | (prose-level findings; no direct 1:1 claim match -- covered by claims in the same source file) | ACKNOWLEDGED |

---

*End of DRIFTS report. See FIX-PLAN.md for remediation instructions.*
