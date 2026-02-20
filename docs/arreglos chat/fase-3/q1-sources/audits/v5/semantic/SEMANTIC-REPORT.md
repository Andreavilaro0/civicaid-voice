# Semantic Inflation Red Team Report (v5)

**Agent:** A5 -- SKEPTIC / Semantic Inflation Red Team
**Date:** 2026-02-19
**Scope:** All Q1/Q1.1 Biblioteca Oficial v0 documentation
**Mode:** READ-ONLY adversarial audit
**Model:** claude-opus-4-6

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 6 |
| HIGH     | 17 |
| MEDIUM   | 10 |
| LOW      | 0 |
| **Total** | **36** |

The Q1/Q1.1 documentation suffers from **systematic semantic inflation** in three main patterns:

1. **"Verified" used 15+ times when no HTTP verification was performed.** The word "verified" appears across 6 different files to describe URLs that were only researched and documented from official directories. The Q1 report itself acknowledges "No actual HTTP validation of URLs" as Gap G1, yet the word "verified" persists throughout the documentation without qualification.

2. **Denominator concealment in fractions.** "3/3 URLs OK" (from a 100+ URL registry), "19/19 CCAA" (one shallow entry per community), "20/20 municipal URLs" (out of 8,131 municipalities = 0.25%). These fractions are technically accurate but create a false impression of completeness.

3. **"All" / "fully" / "complete" applied to partial work.** "Fully validated" (only schema-validated), "all passing" (one script crashes), "all validators covered" (link_check.py has no unit test), "comprehensive catalog" (25 sources from a universe of thousands).

These patterns are not isolated typos -- they form a consistent rhetorical tendency that would mislead a reader (a judge, a stakeholder, a new team member) into believing the project is further along in validation and coverage than it actually is.

---

## Detailed Findings by File

### Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md (8 findings)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-001 | 11 | CRITICAL | "delivers a fully validated, machine-readable foundation" | "Fully validated" = only schema-validated. No HTTP, no content verification. |
| SF-002 | 11 | HIGH | "All Q1 research...has been converted" | 9 research .md files (4,448 lines) remain as markdown, not converted. |
| SF-003 | 15 | HIGH | "validated against JSON Schema" | Readers may infer URL validation. Only structural format was checked. |
| SF-004 | 19 | CRITICAL | "all executable, all passing" | link_check.py crashes at URL 12/18 in live mode (forensic audit F-01). |
| SF-005 | 21 | HIGH | "3 unit tests covering all validators" | Only happy-path tests; link_check.py has no unit test; "all" is false. |
| SF-006 | 22 | CRITICAL | "All 6 gates passed" | G4 was found MISLEADING by the forensic audit (live crash). |
| SF-007 | 20 | CRITICAL | "live test: 3/3 URLs OK" | 3/3 from 100+ URLs. Denominator concealment. |
| SF-008 | 93 | CRITICAL | "G4...PASS...3/3 URLs OK" | Gate table repeats the misleading G4 PASS without caveat. |
| SF-033 | 74 | MEDIUM | "3/3 PASS" (test count) | Stale if AUDIT-04 fix applied (should be 5/5); temporal confusion. |
| SF-034 | 5 | MEDIUM | "validated artifacts for Clara's RAG pipeline" | RAG pipeline does not exist yet (RAG_ENABLED=false). |

### Q1-REPORT.md (6 findings)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-009 | 11 | HIGH | "a comprehensive catalog" | 25 AGE sources from thousands; 20/8,131 municipalities. Seed, not comprehensive. |
| SF-010 | 14 | MEDIUM | "all critical sedes electronicas" | No criteria define "critical." Unverifiable absolutism. |
| SF-011 | 16 | CRITICAL | "20 municipal sedes verified" | Q1 report itself says "No actual HTTP validation" (line 140). |
| SF-012 | 58 | HIGH | "Manual curation, verified URLs" | Same unperformed HTTP verification, in a method column. |
| SF-013 | 129 | HIGH | "Allowlist complete...PASS" | Forensic audit found 14 coverage gaps. "Complete" is false. |
| SF-014 | 133 | MEDIUM | "All 4 abort conditions cleared" | A3 flagged as "CONCERN" by forensic audit. |
| SF-015 | 4 | MEDIUM | "Status: COMPLETE" | All validation deferred to Q2. Research is complete; the layer is not. |
| SF-035 | 42 | MEDIUM | "19/19 CCAA profiles" | "Profile" implies depth; actual entries are shallow (one URL + priority). |

### evidence/gates.md (5 findings)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-017 | 11 | HIGH | "verified sede electronica URLs...PASS (all verified)" | No HTTP verification was performed. |
| SF-018 | 45 | HIGH | "all with verified sede electronica URLs" | Same inflation, reinforced by repetition. |
| SF-019 | 88 | HIGH | "Gates passed: 6/6" | G4 was MISLEADING per forensic audit. |
| SF-020 | 92 | HIGH | "Municipal URLs verified: 20" | Third repetition of "verified" without HTTP evidence. |
| SF-021 | 108 | CRITICAL | "G4: Link checker works...PASS (3/3 URLs OK)" | Link checker crashes at URL 12/18. "Works" is overstated. |

### evidence/Q1.1-FORENSIC-AUDIT-REPORT.md (5 findings)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-022 | 165 | HIGH | "All 10 audit findings have been resolved" | Unclear if fixes propagated to report prose. Some original misleading text remains. |
| SF-023 | 14 | MEDIUM | "Hallucination Risk Score: 12/100 (LOW)" | No disclosed methodology. Subjective impression as quantitative metric. |
| SF-024 | 12 | MEDIUM | "the vast majority are VERIFIED" | Only ~30 of 325 claims individually checked. "Vast majority" is unsubstantiated. |
| SF-025 | 26 | HIGH | "6/6 gates...all VERIFIED" | Contradicts own finding on line 103 (G4 = PARTIAL/MISLEADING). |
| SF-036 | 213 | MEDIUM | "pytest...# 3/3 PASS" | Should be 5/5 if AUDIT-04 was resolved. Internal inconsistency. |

### evidence/references.md (4 findings)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-026 | 30 | HIGH | "Sedes Electronicas (Verified)" | Section header implies HTTP verification. None performed. |
| SF-027 | 39 | HIGH | "complete list with verified URLs" | 20/8,131 = 0.25%. Neither "complete" nor "verified." |
| SF-028 | 63 | HIGH | "Municipal URLs verified: 20/20 (Tier 1)" | Denominator concealment: 20/8,131, not 20/20. |
| SF-029 | 33 | MEDIUM | "complete list with URLs" (AGE) | 25 sources is curated, not complete. |

### source-registry/ccaa.md (1 finding)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-030 | 4 | HIGH | "Complete -- all 19...verified URLs" | "Complete" and "verified" both inflated. |

### source-registry/local.md (2 findings)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-031 | 6 | HIGH | "verified sede electronica URLs and procedure catalogs" | URLs not HTTP-verified; catalogs not indexed, only linked. |
| SF-032 | 18 | HIGH | "Each has been verified with real sede electronica URLs" | Conflates "URLs are real" with "URLs are verified." |

### Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md (additional)

| ID | Line | Severity | Original Text (truncated) | Problem |
|----|------|----------|---------------------------|---------|
| SF-016 | 4 | MEDIUM | "Status: COMPLETE" | Missing post-audit caveat present in Q1 report. |

---

## Top 5 Most Impactful Findings

### 1. SF-001 / SF-004 / SF-006: "Fully validated" + "all passing" + "All 6 gates passed" (CRITICAL x3)

**Impact:** The Q1.1 executive summary (the most-read section of the report) contains three CRITICAL semantic inflations in adjacent bullets. A reader scanning only the executive summary would conclude: (a) all artifacts are fully validated, (b) all scripts work, (c) all gates passed cleanly. The forensic audit contradicts all three: validation is schema-only, link_check.py crashes, and G4 is MISLEADING.

**Why it matters:** This is the section shown to judges, stakeholders, and new team members. It sets the tone for all downstream trust decisions.

### 2. SF-007 / SF-008 / SF-021: "3/3 URLs OK" denominator concealment (CRITICAL x3)

**Impact:** The fraction "3/3" appears in the Q1.1 report, the gate results table, and the Q1.1 gates file. The true denominator is 100+ URLs across 64 sources. Testing 3 and reporting 100% pass rate is statistically meaningless and creates a false impression of validated infrastructure. The forensic audit found the tool crashes at URL 12/18, meaning even 18 URLs could not be fully checked.

**Why it matters:** A "3/3 PASS" looks like a gate that could be trusted. It is actually a minimal smoke test on <3% of the URL corpus.

### 3. SF-011 / SF-017 / SF-020 / SF-026 / SF-030 / SF-031 / SF-032: Systematic "verified" inflation (6 HIGH + 1 CRITICAL)

**Impact:** The word "verified" appears in relation to URLs at least 15 times across 6 files. Not once does it mean HTTP-verified. The Q1 report itself admits "No actual HTTP validation of URLs" as the #1 gap. This is the single most pervasive semantic inflation pattern in the documentation.

**Why it matters:** If someone reads "verified URLs" and deploys the registry to a production system, they will discover broken links, 403 errors, and API stubs. The word "verified" creates operational trust that does not exist.

### 4. SF-009 / SF-027 / SF-028 / SF-029: "Complete" / "comprehensive" for partial coverage

**Impact:** The project covers 25 AGE sources (from a universe of thousands), 19 CCAA entries (one per community, no procedure depth), and 20/8,131 municipalities (0.25%). Calling this "comprehensive" or "complete" misrepresents the actual coverage ratio by orders of magnitude.

**Why it matters:** A stakeholder reading "comprehensive catalog" may not fund the Q2/Q3 work needed to achieve actual comprehensive coverage, believing it already exists.

### 5. SF-022 / SF-025 / SF-033 / SF-036: Temporal confusion and internal contradictions

**Impact:** The forensic audit claims "All 10 findings resolved" and "6/6 gates VERIFIED" in its abort condition table, but its own gate claims table shows G4 as MISLEADING. The test count is 3/3 in the Q1.1 report but should be 5/5 post-fix. These contradictions mean no single document can be trusted as the current source of truth.

**Why it matters:** When the audit report that is supposed to establish truth contains internal contradictions, the entire verification chain is undermined.

---

## Recommendations

### R1: Global find-and-replace for "verified" (addresses 12 findings)

Replace all instances of "verified" in reference to URLs with either:
- "research-documented" (if the URL was found in a government directory)
- "HTTP-verified" (only after actual HTTP HEAD checks pass)

Create a glossary in the project docs defining these terms.

### R2: Add explicit denominators to all fractions (addresses 5 findings)

Every fraction in the documentation should show the true denominator:
- "3/3 URLs OK" should become "3/100+ URLs sampled OK"
- "20/20 municipal URLs" should become "20/8,131 municipalities (Tier 1 seed)"
- "19/19 CCAA" should note "one entry per community; procedure catalogs not indexed"

### R3: Qualify all gate PASS results with scope (addresses 6 findings)

Each gate result should state:
- What was tested (schema validation, dry-run, live test)
- What was NOT tested (HTTP liveness, content accuracy, edge cases)
- Any caveats from the forensic audit

### R4: Replace "fully validated" and "complete" with precise terms (addresses 4 findings)

- "fully validated" should become "schema-validated"
- "COMPLETE" status should become "RESEARCH COMPLETE" or "ARTIFACTS COMPLETE (validation pending Q2)"
- "comprehensive catalog" should become "seed catalog" or "curated catalog"

### R5: Resolve temporal inconsistencies (addresses 4 findings)

The forensic audit report, Q1.1 report, and gates.md contain contradictory numbers (3/3 vs 5/5 tests, 6/6 vs 5/6+1 gates). Designate ONE file as the canonical post-audit source of truth and update all others to reference it.

### R6: Add a "Limitations" section to Q1.1 executive summary

The executive summary is the most visible part of the report and currently contains zero caveats. Add a 3-bullet "Key Limitations" subsection immediately after the "10 Key Bullets":
1. No URLs have been HTTP-verified (deferred to Q2)
2. Link checker passed smoke test only (3 URLs); full registry untested
3. Coverage is a seed layer: 25/thousands AGE, 19 CCAA entries, 20/8,131 municipalities

---

## Methodology

This audit was performed by reading every line of the 9 specified files (plus supporting files discovered via cross-references). Each sentence was evaluated against the question: "Could a reasonable reader be misled about the project's actual state?" Findings were classified by severity based on the gap between what the text implies and what the evidence supports.

The audit was adversarial by design. Where charitable and skeptical readings were both possible, the skeptical reading was chosen. This is intentional: the purpose is to surface all potential misleading language, not to give the benefit of the doubt.

**Files audited:** 9 primary + 3 supporting (backlog, ccaa.md header, local.md detail)
**Total findings:** 36
**Pattern coverage:** All 10 target patterns were searched; 8 of 10 yielded findings.
- Patterns with findings: "verified", "complete/comprehensive", "PASS", "all/fully", "resolved", "validated", fractions/denominators, temporal confusion
- Patterns without findings: "tested" (adequately qualified in most uses), no LOW-severity findings identified (all issues were at least MEDIUM)
