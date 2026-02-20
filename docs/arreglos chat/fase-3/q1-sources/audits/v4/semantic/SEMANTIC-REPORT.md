# Semantic Inflation Report — Audit v4

> **Date:** 2026-02-18
> **Auditor:** A5 — Semantic Inflation Red Team
> **Scope:** 9 documentation files in Q1/Q1.1 artifact set
> **Mode:** READ-ONLY

---

## Summary

- **Total occurrences found:** 28
- **By severity:** CRITICAL: 2 / HIGH: 9 / MEDIUM: 11 / LOW: 6
- **Files affected:**
  - `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` (4 findings)
  - `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` (7 findings)
  - `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` (7 findings)
  - `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` (5 findings)
  - `docs/arreglos chat/fase-3/q1-sources/evidence/references.md` (4 findings)
  - `docs/arreglos chat/fase-3/q1-sources/evidence/assumptions-gaps.md` (0 findings)
  - `data/sources/README.md` (0 findings)
  - `data/policy/README.md` (0 findings)
  - `schemas/README.md` (1 finding)

---

## Findings

### SF-001: "comprehensive catalog" in Q1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 11
- **Original text:** "a comprehensive catalog of official Spanish government sources at all three administrative levels"
- **Problem:** 64 sources cataloged out of potentially thousands of government endpoints. Municipal coverage is 20 out of 8,131 municipalities (0.25%). "Comprehensive" implies near-total coverage, which is false.
- **Severity:** HIGH
- **Suggested replacement:** "a foundational catalog of official Spanish government sources at all three administrative levels"

### SF-002: "verified" URLs in Q1-REPORT.md (local table)
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 58
- **Original text:** "Manual curation, verified URLs"
- **Problem:** No HTTP validation was performed on any URL. The gaps document (assumptions-gaps.md, line 24) explicitly states "No actual HTTP validation of URLs performed (research-only)." Using "verified" implies HTTP testing.
- **Severity:** HIGH
- **Suggested replacement:** "Manual curation, research-documented URLs"

### SF-003: "Allowlist complete" in Q1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 129
- **Original text:** "Allowlist complete (3 tiers + blocklist)"
- **Problem:** The forensic audit (F-03) found 14 allowlist coverage gaps where registry URLs would be REJECTED by the allowlist-first policy. "Complete" implies no gaps exist.
- **Severity:** MEDIUM
- **Suggested replacement:** "Allowlist structured (3 tiers + blocklist; 14 gap fixes pending)"

### SF-004: "20 municipal sedes verified" in Q1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Line:** 16
- **Original text:** "20 municipal sedes verified (Tier 1 top cities by population)"
- **Problem:** Same as SF-002. "Verified" without qualifier implies HTTP validation. Only research-level documentation was done.
- **Severity:** HIGH
- **Suggested replacement:** "20 municipal sedes documented (Tier 1 top cities by population)"

### SF-005: "fully validated" in Q1.1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 11
- **Original text:** "The Biblioteca Oficial v0 delivers a fully validated, machine-readable foundation"
- **Problem:** Validation was schema-level only (JSON Schema validation scripts pass). No HTTP validation of URLs, no content validation of extracted data, no end-to-end pipeline validation. "Fully validated" implies all validation dimensions were covered.
- **Severity:** CRITICAL
- **Suggested replacement:** "The Biblioteca Oficial v0 delivers a schema-validated, machine-readable foundation"

### SF-006: "All Q1 research" in Q1.1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 11
- **Original text:** "All Q1 research (AGE, CCAA, municipal sources) has been converted into structured YAML registries"
- **Problem:** The 9 research markdown files (4,448 lines) contain far more detail than what was converted into YAML. The YAML registries capture source metadata (URLs, priorities, access methods) but not the full research content (extraction strategies, CMS analysis, disambiguation logic, etc.). "All" overstates the conversion scope.
- **Severity:** MEDIUM
- **Suggested replacement:** "Core Q1 source metadata (AGE, CCAA, municipal sources) has been converted into structured YAML registries"

### SF-007: "3/3 URLs OK" in Q1.1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 20
- **Original text:** "live test: 3/3 URLs OK (avg 229ms)"
- **Problem:** The actual denominator is 64 portal URLs across registry.yaml + local_seed.yaml (or 157 total URLs if counting all URL fields). Testing 3 out of 64 is 4.7% coverage. The "3/3" notation creates a false impression of completeness. Additionally, the forensic audit found the link checker crashes at URL 12/18 during extended testing.
- **Severity:** CRITICAL
- **Suggested replacement:** "live smoke test: 3/64 URLs checked OK (4.7% coverage, avg 229ms)"

### SF-008: "3/3 PASS" in Q1.1-REPORT.md tests table
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 74
- **Original text:** "| `tests/unit/test_validators.py` | 3 | 3/3 PASS |"
- **Problem:** After the forensic audit fix (AUDIT-04), 2 negative tests were added, making the actual count 5 tests. This line is stale -- it still says 3/3 when the current state is 5/5.
- **Severity:** MEDIUM
- **Suggested replacement:** "| `tests/unit/test_validators.py` | 5 | 5/5 PASS |"

### SF-009: "all executable, all passing" in Q1.1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 19
- **Original text:** "4 validation scripts (`validate_source_registry.py`, `validate_policy.py`, `validate_proceduredoc_schema.py`, `link_check.py`) -- all executable, all passing"
- **Problem:** The forensic audit found that link_check.py crashes on line ~111 (NoneType when status_code is None) at URL 12/18 during smoke test. "All passing" was true only for limited dry-run scenarios but false for live extended runs. The crash bug was later fixed (AUDIT-01), but the phrasing remains misleadingly absolute.
- **Severity:** MEDIUM
- **Suggested replacement:** "4 validation scripts -- all executable, all passing schema validation (link_check.py smoke-tested on 3 URLs)"

### SF-010: "PASS" for G4 in Q1.1-REPORT.md gate table
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 93
- **Original text:** "| G4 | Link checker smoke test | PASS | 3/3 URLs OK, JSONL generated |"
- **Problem:** The forensic audit reclassified G4 as "PARTIAL" / "MISLEADING" because the live checker crashed at URL 12/18. A bare "PASS" conceals that only 4.7% of URLs were tested and that the tool had a crash bug.
- **Severity:** HIGH
- **Suggested replacement:** "| G4 | Link checker smoke test | PASS (smoke, 3/64 URLs = 4.7%) | 3 URLs OK, JSONL generated |"

### SF-011: "verified sede electronica URLs" in gates.md (G3 criteria)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 11
- **Original text:** "Local coverage strategy includes at least 20 cities with verified sede electronica URLs"
- **Problem:** Gate criteria uses "verified" but no HTTP verification was performed. The gaps document explicitly says "No actual HTTP validation of URLs performed."
- **Severity:** HIGH
- **Suggested replacement:** "Local coverage strategy includes at least 20 cities with documented sede electronica URLs"

### SF-012: "20 cities, all verified" in gates.md (G3 result)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 11
- **Original text:** "**PASS** (20 cities, all verified)"
- **Problem:** Same as SF-011. "All verified" without HTTP evidence is misleading.
- **Severity:** HIGH
- **Suggested replacement:** "**PASS** (20 cities, all research-documented)"

### SF-013: "Allowlist complete" in gates.md (G4)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 12
- **Original text:** "Domain allowlist covers all 3 tiers (AGE, CCAA, Municipal) with explicit blocklist"
- **Problem:** The forensic audit found 14 allowlist coverage gaps. "Covers all 3 tiers" implies full coverage within each tier, but 5 registry URLs and 9 local_seed URLs would be rejected.
- **Severity:** MEDIUM
- **Suggested replacement:** "Domain allowlist covers all 3 tiers structurally (AGE, CCAA, Municipal) with explicit blocklist"

### SF-014: "all with verified sede electronica URLs" in gates.md (G3 evidence)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 45
- **Original text:** "**Tier 1 cities:** 20 (all with verified sede electronica URLs)"
- **Problem:** Same "verified" inflation. Research-documented, not HTTP-verified.
- **Severity:** HIGH
- **Suggested replacement:** "**Tier 1 cities:** 20 (all with research-documented sede electronica URLs)"

### SF-015: "PASS (3/3 URLs OK)" in gates.md (Q1.1 G4)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 108
- **Original text:** "**PASS** (3/3 URLs OK)"
- **Problem:** Same denominator concealment as SF-007. 3 out of 64 URLs tested (4.7%). The notation "3/3" makes it appear all targets were tested.
- **Severity:** HIGH
- **Suggested replacement:** "**PASS** (smoke: 3/64 URLs tested OK, 4.7% coverage)"

### SF-016: "All 6 gates passed" in gates.md summary
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 88
- **Original text:** "Gates passed | 6/6"
- **Problem:** G4 was later reclassified as PARTIAL/MISLEADING by the forensic audit. Presenting "6/6" without caveat conceals the G4 issue.
- **Severity:** MEDIUM
- **Suggested replacement:** "Gates passed | 6/6 (G4 with caveats -- see forensic audit)"

### SF-017: "Municipal URLs verified | 20" in gates.md summary
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Line:** 92
- **Original text:** "Municipal URLs verified | 20"
- **Problem:** Same "verified" without HTTP evidence pattern.
- **Severity:** MEDIUM
- **Suggested replacement:** "Municipal URLs documented | 20"

### SF-018: "All 10 audit findings have been resolved" in Forensic Audit Report
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 165
- **Original text:** "All 10 audit findings have been resolved. Gates re-verified: 5/5 PASS."
- **Problem:** The fixes were applied to data/code files (registry.yaml, link_check.py, allowlist.yaml, etc.) but the downstream documentation (Q1-REPORT.md, Q1.1-REPORT.md, gates.md) was NOT updated with corrected values. At least 14 stale claims remain across those documents. "Resolved" implies fully propagated resolution.
- **Severity:** MEDIUM
- **Suggested replacement:** "All 10 audit findings have been addressed in source data/code files. Gates re-verified: 5/5 PASS. NOTE: downstream report documents were not updated with post-fix values."

### SF-019: "VERIFIED" for gate claims in Forensic Audit Report
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 26
- **Original text:** "Core claims (44 sources, 25 AGE, 19 CCAA, 20 local, 6/6 gates) are all VERIFIED"
- **Problem:** "6/6 gates" is listed as "all VERIFIED" but the same report on line 103 marks G4 as "PARTIAL" / "MISLEADING". Internal contradiction within the same document.
- **Severity:** MEDIUM
- **Suggested replacement:** "Core claims (44 sources, 25 AGE, 19 CCAA, 20 local) are VERIFIED; gates 5/6 VERIFIED + G4 PARTIAL"

### SF-020: "3/3 tests pass" in Forensic Audit Report (A5 abort condition)
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 30
- **Original text:** "All 4 scripts pass, 3/3 tests pass"
- **Problem:** After AUDIT-04 fix (same report, line 175), 2 negative tests were added making it 5/5. This line was not updated, creating an internal inconsistency within the same document.
- **Severity:** LOW
- **Suggested replacement:** "All 4 scripts pass, 5/5 tests pass"

### SF-021: "pytest exit 0" as sole evidence for "3/3 PASS" in Forensic Audit Report
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 213
- **Original text:** "pytest tests/unit/test_validators.py -v                # 3/3 PASS"
- **Problem:** Same staleness as SF-020. After AUDIT-04, actual count is 5/5.
- **Severity:** LOW
- **Suggested replacement:** "pytest tests/unit/test_validators.py -v                # 5/5 PASS"

### SF-022: All 10 "RESOLVED" tickets in Forensic Audit Report
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Line:** 192-201
- **Original text:** All 10 rows marked "RESOLVED"
- **Problem:** The code/data-layer fixes were applied, but marking tickets as "RESOLVED" implies full resolution including documentation propagation. At least 14 downstream stale claims were not updated.
- **Severity:** MEDIUM
- **Suggested replacement:** Mark as "RESOLVED (source)" or add a column "Doc propagation: PENDING"

### SF-023: "complete list with verified URLs" in references.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/references.md`
- **Line:** 39
- **Original text:** "See `source-registry/local.md` for complete list with verified URLs."
- **Problem:** Combines two inflated terms: "complete" (only 20 of 8,131 municipalities) and "verified" (no HTTP validation). Double inflation.
- **Severity:** HIGH
- **Suggested replacement:** "See `source-registry/local.md` for the full Tier 1 seed list with documented URLs."

### SF-024: "Municipal URLs verified | 20/20 (Tier 1)" in references.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/references.md`
- **Line:** 63
- **Original text:** "Municipal URLs verified | 20/20 (Tier 1) | This research"
- **Problem:** "Verified" without HTTP evidence. The 20/20 notation is accurate (20 out of 20 Tier 1 cities) but "verified" is inflated.
- **Severity:** MEDIUM
- **Suggested replacement:** "Municipal URLs documented | 20/20 (Tier 1) | This research"

### SF-025: "complete list with URLs" for AGE in references.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/references.md`
- **Line:** 33
- **Original text:** "See `source-registry/age.md` for complete list with URLs."
- **Problem:** "Complete list" is acceptable as a cross-reference to the full file, but could be read as "complete coverage of all AGE sources" when only 25 were cataloged. Mild inflation.
- **Severity:** LOW
- **Suggested replacement:** "See `source-registry/age.md` for the full 25-source catalog with URLs."

### SF-026: "complete list with URLs" for CCAA in references.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/references.md`
- **Line:** 36
- **Original text:** "See `source-registry/ccaa.md` for complete list with URLs."
- **Problem:** Same as SF-025. 19/19 CCAA is actually complete for communities, but "complete" could be read as "all CCAA procedures/URLs."
- **Severity:** LOW
- **Suggested replacement:** "See `source-registry/ccaa.md` for the full 19-community catalog with URLs."

### SF-027: "Status: COMPLETE" in Q1.1-REPORT.md
- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Line:** 4
- **Original text:** "**Status:** COMPLETE"
- **Problem:** As a phase status indicator this is acceptable -- the Q1.1 work phase is finished. However, without qualification it could be read as "the biblioteca is complete" when it is a v0 seed. Low risk because "v0" is in the title.
- **Severity:** LOW
- **Suggested replacement:** "**Status:** COMPLETE (Q1.1 scope delivered)"

### SF-028: "validate_proceduredoc_schema.py" sample path in schemas/README.md
- **File:** `schemas/README.md`
- **Line:** 16
- **Original text:** "python3 scripts/validate_proceduredoc_schema.py data/tramites/imv.json"
- **Problem:** The example implies `data/tramites/imv.json` validates against ProcedureDoc.v1 schema, but existing tramites files use the legacy format, not ProcedureDoc v1. Only the specially crafted `proceduredoc.sample.json` validates. Running the shown command would likely fail or give misleading results.
- **Severity:** LOW
- **Suggested replacement:** "python3 scripts/validate_proceduredoc_schema.py \"docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json\""

---

## Replacement Plan

| # | File | Line | Original | Replacement | Severity |
|---|------|------|----------|-------------|----------|
| SF-001 | Q1-REPORT.md | 11 | "comprehensive catalog" | "foundational catalog" | HIGH |
| SF-002 | Q1-REPORT.md | 58 | "verified URLs" | "research-documented URLs" | HIGH |
| SF-003 | Q1-REPORT.md | 129 | "Allowlist complete" | "Allowlist structured" | MEDIUM |
| SF-004 | Q1-REPORT.md | 16 | "20 municipal sedes verified" | "20 municipal sedes documented" | HIGH |
| SF-005 | Q1.1-REPORT.md | 11 | "fully validated" | "schema-validated" | CRITICAL |
| SF-006 | Q1.1-REPORT.md | 11 | "All Q1 research" | "Core Q1 source metadata" | MEDIUM |
| SF-007 | Q1.1-REPORT.md | 20 | "3/3 URLs OK" | "3/64 URLs checked OK (4.7% coverage)" | CRITICAL |
| SF-008 | Q1.1-REPORT.md | 74 | "3 \| 3/3 PASS" | "5 \| 5/5 PASS" | MEDIUM |
| SF-009 | Q1.1-REPORT.md | 19 | "all executable, all passing" | "all executable, all passing schema validation (link_check.py smoke-tested on 3 URLs)" | MEDIUM |
| SF-010 | Q1.1-REPORT.md | 93 | "PASS \| 3/3 URLs OK" | "PASS (smoke, 3/64 = 4.7%) \| 3 URLs OK" | HIGH |
| SF-011 | gates.md | 11 | "verified sede electronica URLs" | "documented sede electronica URLs" | HIGH |
| SF-012 | gates.md | 11 | "all verified" | "all research-documented" | HIGH |
| SF-013 | gates.md | 12 | "covers all 3 tiers" | "covers all 3 tiers structurally" | MEDIUM |
| SF-014 | gates.md | 45 | "all with verified sede electronica URLs" | "all with research-documented sede electronica URLs" | HIGH |
| SF-015 | gates.md | 108 | "PASS (3/3 URLs OK)" | "PASS (smoke: 3/64 URLs, 4.7%)" | HIGH |
| SF-016 | gates.md | 88 | "6/6" | "6/6 (G4 with caveats)" | MEDIUM |
| SF-017 | gates.md | 92 | "Municipal URLs verified" | "Municipal URLs documented" | MEDIUM |
| SF-018 | FORENSIC-AUDIT-REPORT.md | 165 | "All 10...resolved" | "All 10...addressed in source files; doc propagation pending" | MEDIUM |
| SF-019 | FORENSIC-AUDIT-REPORT.md | 26 | "6/6 gates...all VERIFIED" | "5/6 VERIFIED + G4 PARTIAL" | MEDIUM |
| SF-020 | FORENSIC-AUDIT-REPORT.md | 30 | "3/3 tests pass" | "5/5 tests pass" | LOW |
| SF-021 | FORENSIC-AUDIT-REPORT.md | 213 | "# 3/3 PASS" | "# 5/5 PASS" | LOW |
| SF-022 | FORENSIC-AUDIT-REPORT.md | 192-201 | "RESOLVED" x10 | "RESOLVED (source)" x10 | MEDIUM |
| SF-023 | references.md | 39 | "complete list with verified URLs" | "full Tier 1 seed list with documented URLs" | HIGH |
| SF-024 | references.md | 63 | "Municipal URLs verified" | "Municipal URLs documented" | MEDIUM |
| SF-025 | references.md | 33 | "complete list with URLs" | "full 25-source catalog with URLs" | LOW |
| SF-026 | references.md | 36 | "complete list with URLs" | "full 19-community catalog with URLs" | LOW |
| SF-027 | Q1.1-REPORT.md | 4 | "COMPLETE" | "COMPLETE (Q1.1 scope delivered)" | LOW |
| SF-028 | schemas/README.md | 16 | "data/tramites/imv.json" | "evidence/samples/proceduredoc.sample.json" | LOW |

---

## Severity Distribution

| Keyword | CRITICAL | HIGH | MEDIUM | LOW |
|---------|----------|------|--------|-----|
| "verified" (no HTTP) | 0 | 7 | 2 | 0 |
| "comprehensive" | 0 | 1 | 0 | 0 |
| "fully validated" | 1 | 0 | 0 | 0 |
| "complete" | 0 | 0 | 1 | 3 |
| "3/3" (denominator) | 1 | 1 | 1 | 1 |
| "all" (overgeneralized) | 0 | 0 | 2 | 0 |
| "resolved" (partial) | 0 | 0 | 3 | 0 |
| "PASS" (narrow criteria) | 0 | 0 | 1 | 0 |
| other | 0 | 0 | 1 | 2 |
| **Total** | **2** | **9** | **11** | **6** |

---

## Risk Assessment

The two CRITICAL findings (SF-005 and SF-007) are the most dangerous because they appear in the executive summary of Q1.1-REPORT.md -- the first thing a reader sees. A stakeholder reading "fully validated" and "3/3 URLs OK" would reasonably conclude that HTTP validation was performed and all targets were tested, when in reality:

1. Validation is schema-only (JSON Schema Draft 2020-12 structural checks)
2. Only 3 out of 64 URLs (4.7%) were smoke-tested via HTTP
3. The link checker tool crashed during extended testing

The HIGH findings (9 total) cluster around the word "verified" used for URLs that were only research-documented. This pattern appears across 4 different files, creating a consistent but misleading impression of HTTP-level verification.

The MEDIUM findings (11 total) are mostly staleness issues where post-forensic-audit fixes changed the ground truth but the documentation was not updated, plus some "resolved"/"all" overgeneralizations.

The LOW findings (6 total) are minor wording choices that could be improved but are unlikely to materially mislead a reader.
