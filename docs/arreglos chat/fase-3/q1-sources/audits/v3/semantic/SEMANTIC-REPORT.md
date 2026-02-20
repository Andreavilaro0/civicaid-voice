# A5 Semantic Inflation Audit Report (v3)

**Date:** 2026-02-18
**Auditor:** A5 (Semantic Inflation Red Team)
**Scope:** All Q1/Q1.1 documentation + data layer
**Mode:** READ-ONLY

---

## Overall Semantic Risk Score: 62/100 (MEDIUM-HIGH)

The documentation is technically rigorous in many areas but systematically inflates confidence through the use of "verified" (without HTTP evidence), "comprehensive" (with 0.25% municipal coverage), "PASS" (concealing limited test scope), and "3/3" (concealing that 64 URLs exist but only 3 were tested). The Forensic Audit Report partially addresses some issues but itself introduces new semantic inflation ("All 10 audit findings have been resolved" without propagation evidence).

---

## a) "verified" Analysis

### Summary

"Verified" appears 80+ times across the corpus. The word carries three distinct meanings, only one of which (schema-validated) has actual machine evidence. The other two meanings (research-verified, HTTP-verified) lack reproducible proof.

### Occurrences

| # | File | Line | Context | Actual Meaning | Severity | Recommendation |
|---|------|------|---------|----------------|----------|----------------|
| 1 | Q1-REPORT.md | 16 | "20 municipal sedes verified" | research-verified: URLs were found during web research, NOT tested via HTTP | HIGH | Replace with "researched" or "cataloged" |
| 2 | Q1-REPORT.md | 58 | "Manual curation, verified URLs" | research-verified: same as above | HIGH | Replace with "researched URLs" |
| 3 | ccaa.md | 4 | "profiled with verified URLs" | research-verified: 19 CCAA URLs found during research, zero HTTP checks | HIGH | Replace with "documented URLs" |
| 4 | local.md | 6 | "verified sede electronica URLs" | research-verified | HIGH | Replace with "documented sede electronica URLs" |
| 5 | local.md | 18 | "verified with real sede URLs" | research-verified | HIGH | Replace with "documented with researched sede URLs" |
| 6-25 | local.md | 22-41 | "Verified" in Status column (x20 cities) | research-verified: NO HTTP HEAD/GET was run against these 20 URLs | HIGH | Replace with "Researched" or "URL documented" |
| 26 | gates.md | 11 | "20 cities, all verified" | research-verified: gate criteria says "verified" but no HTTP was run | HIGH | Replace with "20 cities, all documented" |
| 27 | gates.md | 45 | "all with verified sede URLs" | research-verified | HIGH | Replace with "all with documented sede URLs" |
| 28 | gates.md | 92 | "Municipal URLs verified: 20" | research-verified | HIGH | Replace with "Municipal URLs documented: 20" |
| 29 | references.md | 30 | "Sedes Electronicas (Verified)" | Section header implying HTTP verification | HIGH | Replace with "Sedes Electronicas (Researched)" |
| 30 | references.md | 39 | "complete list with verified URLs" | research-verified | HIGH | Replace with "complete list with documented URLs" |
| 31 | references.md | 63 | "Municipal URLs verified: 20/20" | research-verified | HIGH | Replace with "Municipal URLs documented: 20/20" |
| 32 | Q1.1-REPORT.md | 11 | "fully validated, machine-readable" | schema-validated (scripts pass), NOT HTTP-validated | MEDIUM | Replace with "schema-validated" |
| 33 | local_seed.yaml | 32 | "URLs verified from local.md" | Comment claims verification; no HTTP evidence | HIGH | Replace with "URLs transcribed from local.md" |
| 34 | allowlist.md | 123 | "must be verified manually" | Correct usage -- prescriptive, not claiming done | LOW | OK as-is (prescriptive) |
| 35 | allowlist.md | 136 | "User-generated, unverified" | Correct usage -- accurate description | LOW | OK as-is |

**Schema-field uses of "verified" (verified_at, verified_by in ProcedureDoc schema):** These are schema field names, not claims. They are acceptable as data model fields. Found in normalization-schema.md lines 71-72, 115-116, 201-202, 249-250, 347-348, 455-456, 574-575, and proceduredoc.sample.json lines 113-114. These are LOW severity.

**Forensic Audit uses of "VERIFIED":** The Q1.1-FORENSIC-AUDIT-REPORT.md uses "VERIFIED" 30+ times. The forensic audit DID run validation scripts and verify file existence, so this usage is MEDIUM risk -- it is accurate for schema validation and file counts but some entries (like file line counts) are just wc -l which is mechanical, while the "VERIFIED" label implies deeper validation.

### Critical Finding

The Q1 gaps document (assumptions-gaps.md) line 24 explicitly states: **"No actual HTTP validation of URLs performed (research-only constraint)"** -- yet the word "verified" is used 30+ times across other documents to describe these same URLs. This is a direct contradiction. The gaps document is honest; the other documents inflate.

---

## b) "complete"/"comprehensive" Analysis

### Occurrences

| # | File | Line | Context | Actual Meaning | Severity | Recommendation |
|---|------|------|---------|----------------|----------|----------------|
| 1 | Q1-REPORT.md | 4 | "Status: COMPLETE" | Phase status -- phase is finished, not that coverage is complete | LOW | OK as-is (phase status) |
| 2 | Q1-REPORT.md | 11 | "comprehensive catalog of official Spanish government sources" | 64 sources cataloged out of potentially thousands; 20 out of 8,131 municipalities = 0.25% | HIGH | Replace with "initial catalog" or "foundational catalog" |
| 3 | Q1-REPORT.md | 129 | "Allowlist complete (3 tiers + blocklist)" | Allowlist has structural completeness (3 tiers exist) but F-03 found 14 coverage gaps | MEDIUM | Replace with "Allowlist structured (3 tiers + blocklist)" |
| 4 | Q1.1-REPORT.md | 4 | "Status: COMPLETE" | Phase status | LOW | OK as-is |
| 5 | ccaa.md | 4 | "Complete -- all 19 communities" | Accurate: 19/19 profiled. But "complete" implies exhaustive procedure coverage, when only URLs were documented | MEDIUM | Replace with "All 19 communities profiled" |
| 6 | ccaa.md | 416 | "Phase 3 -- Coverage complete" | Future aspiration, not a current claim | LOW | OK as-is (roadmap) |
| 7 | references.md | 33 | "complete list with URLs" | Means "the full list is in age.md" -- acceptable cross-reference | LOW | OK as-is |
| 8 | references.md | 36 | "complete list with URLs" | Same as above | LOW | OK as-is |
| 9 | references.md | 39 | "complete list with verified URLs" | Combines two inflated terms | HIGH | Replace with "full documented list" |
| 10 | gates.md | 12 | "Allowlist complete" | Same as Q1-REPORT.md item | MEDIUM | Same recommendation |
| 11 | local.md | 172 | "Complete list of all 8,131 municipalities" | Referring to INE data, not CivicAid's data. Accurate for INE. | LOW | OK as-is (describes external dataset) |
| 12 | link-checking-spec.md | 150 | "last complete check cycle" | Technical field name -- acceptable | LOW | OK as-is |
| 13 | Q1.1-REPORT.md | 11 | "fully validated" | See "verified" section. Schema-validated but not HTTP-validated | MEDIUM | Replace with "schema-validated" |

---

## c) "official" Analysis

### Occurrences

| # | File | Line | Context | Actual Meaning | Severity | Recommendation |
|---|------|------|---------|----------------|----------|----------------|
| 1 | Q1-REPORT.md | 11 | "official Spanish government sources" | Means "gov-domain sources" -- accurate, these are .gob.es domains | LOW | OK as-is |
| 2 | age.md | 4 | "official Spanish central government sources" | Same -- gov-domain | LOW | OK as-is |
| 3 | age.md | 17 | "Official state gazette" | BOE is literally the Official State Gazette by law | LOW | OK as-is (legally accurate) |
| 4 | age.md | 116 | "Official gazette + API" | Same | LOW | OK as-is |
| 5 | age.md | 118 | "ALL official state publications" | BOE does publish all official state publications by law | LOW | OK as-is |
| 6 | Q1.1-REPORT.md | 1 | "Biblioteca Oficial" | Title uses "Oficial" to mean "from government sources" | LOW | OK as-is |
| 7 | local.md | 69 | "official sede electronica URL" | Means "the actual gov URL" -- acceptable | LOW | OK as-is |
| 8 | local.md | 154 | "Official Directories" | Section title -- accurate, DIR3 is an official directory | LOW | OK as-is |
| 9 | local.md | 164 | "official sede electronica" | Same as above | LOW | OK as-is |
| 10 | local.md | 201 | "Official registry of all local entities" | REL is literally an official registry | LOW | OK as-is |
| 11 | allowlist.md | 11 | "official government information" | Policy statement -- prescriptive, accurate | LOW | OK as-is |
| 12 | allowlist.md | 47 | "(only if official)" | Conditional inclusion note -- cautious | LOW | OK as-is |
| 13 | allowlist.md | 140 | "Appear official but are not" | Warning about unofficial sites -- good practice | LOW | OK as-is |
| 14 | allowlist.md | 165 | "official government entity" | Validation checklist item | LOW | OK as-is |
| 15 | allowlist.md | 212 | "answer from official sources only" | Policy statement | LOW | OK as-is |
| 16 | sources/README.md | 3 | "official Spanish government sources" | Descriptor -- means gov-domain | LOW | OK as-is |

**Verdict:** "Official" usage is CLEAN across the corpus. It consistently means "government-domain" or "legally designated," never "endorsed by CivicAid." No inflation detected.

---

## d) "all"/"every" Analysis

### High-Severity Occurrences

| # | File | Line | Context | Actual Scope | Severity | Recommendation |
|---|------|------|---------|--------------|----------|----------------|
| 1 | Q1-REPORT.md | 11 | "at all three administrative levels" | Only 20/8131 municipalities at local level = 0.25% coverage | HIGH | Replace with "across all three administrative tiers (seed coverage)" |
| 2 | Q1-REPORT.md | 14 | "all critical sedes electronicas" | Which are "all critical"? Undefined set. P0 count is 10. | MEDIUM | Replace with "key sedes electronicas" |
| 3 | Q1-REPORT.md | 133 | "All 4 abort conditions cleared" | Accurate (4 specific conditions defined and checked) | LOW | OK as-is |
| 4 | Q1.1-REPORT.md | 11 | "All Q1 research" | Accurate -- all Q1 docs were converted | LOW | OK as-is |
| 5 | Q1.1-REPORT.md | 19 | "all executable, all passing" | Accurate -- 4 scripts, all pass | LOW | OK as-is |
| 6 | Q1.1-REPORT.md | 22 | "All 6 gates passed" | Accurate for defined gates; but G4 was later found to be MISLEADING by forensic audit | MEDIUM | Should note "All 6 defined gates passed (G4 with caveats)" |
| 7 | gates.md | 10 | "All 17 autonomous communities + 2 autonomous cities" | Accurate: 19/19 | LOW | OK as-is |
| 8 | gates.md | 11 | "all verified" | See "verified" section -- inflated | HIGH | See verified recommendation |
| 9 | gates.md | 21 | "All 19/19 covered" | Accurate | LOW | OK as-is |
| 10 | Forensic Audit | 110 | "All 29 declared files exist" | Auditor confirmed each file | LOW | OK as-is |
| 11 | Forensic Audit | 165 | "All 10 audit findings have been resolved" | Claims resolution but no evidence of propagation to downstream consumers | MEDIUM | Should say "All 10 findings addressed in source files" |
| 12 | age.md | 48 | "ALL administrative procedures" | Describing SIA scope (legally mandated) -- accurate for SIA | LOW | OK as-is (describes external system) |
| 13 | age.md | 62 | "ALL public administrations" | Describing PAG scope -- accurate for PAG's mandate | LOW | OK as-is |
| 14 | age.md | 118 | "ALL official state publications" | Describing BOE scope -- legally accurate | LOW | OK as-is |
| 15 | age.md | 233 | "ALL immigration procedures" | Describing Extranjeria scope -- accurate for the portal | LOW | OK as-is |

---

## e) "PASS" Without Qualification Analysis

### Occurrences

| # | File | Line | Context | What Was Actually Tested | Severity | Recommendation |
|---|------|------|---------|--------------------------|----------|----------------|
| 1 | Q1-REPORT.md | 126 | "G1: **PASS** (25)" | Schema count validation -- accurate | LOW | OK as-is |
| 2 | Q1-REPORT.md | 127 | "G2: **PASS** (19/19)" | Schema count validation -- accurate | LOW | OK as-is |
| 3 | Q1-REPORT.md | 128 | "G3: **PASS** (20)" | Research-only count check -- no HTTP validation | MEDIUM | Add qualifier: "PASS (20 documented, HTTP pending Q2)" |
| 4 | Q1-REPORT.md | 129 | "G4: **PASS**" | Allowlist exists -- but 14 gaps found later | MEDIUM | Should note "PASS (structural; coverage gaps addressed in Q1.1)" |
| 5 | Q1-REPORT.md | 130 | "G5: **PASS** (6 stages)" | Playbook documented -- accurate | LOW | OK as-is |
| 6 | Q1-REPORT.md | 131 | "G6: **PASS**" | Schema documented -- accurate | LOW | OK as-is |
| 7 | Q1.1-REPORT.md | 74 | "3/3 PASS" | 3 happy-path unit tests passed; no negative tests at time of writing | MEDIUM | Note "3/3 PASS (happy-path only)" |
| 8 | Q1.1-REPORT.md | 90 | "G1: PASS" | validate_source_registry.py exit 0 -- accurate | LOW | OK as-is |
| 9 | Q1.1-REPORT.md | 91 | "G2: PASS" | validate_policy.py exit 0 -- accurate | LOW | OK as-is |
| 10 | Q1.1-REPORT.md | 92 | "G3: PASS" | validate_proceduredoc_schema.py exit 0 -- accurate | LOW | OK as-is |
| 11 | Q1.1-REPORT.md | 93 | "G4: PASS, 3/3 URLs OK" | **CRITICAL**: Only 3 URLs tested out of 64 total (4.7%). Forensic audit found script crashes at URL 12/18 in live mode. | HIGH | Must say "G4: PASS (smoke, 3/64 URLs, dry-run only)" |
| 12 | Q1.1-REPORT.md | 94-95 | "G5: PASS", "G6: PASS" | Visual check / file existence -- accurate | LOW | OK as-is |
| 13 | gates.md | 9-14 | All 6 Q1 gates "PASS" | See individual items above | See above | See above |
| 14 | gates.md | 88 | "Gates passed: 6/6" | Summary -- same caveats | MEDIUM | Add footnote |
| 15 | gates.md | 105-110 | All 6 Q1.1 gates "PASS" | Same as Q1.1-REPORT items | See above | See above |
| 16 | gates.md | 108 | "PASS (3/3 URLs OK)" | Same G4 issue | HIGH | Same as #11 |
| 17 | Forensic Audit | 30 | "All 4 scripts pass, 3/3 tests pass" | Accurate at time of audit | LOW | OK |
| 18 | Forensic Audit | 103 | "PASS (3/3) -> PARTIAL -> MISLEADING" | The forensic audit CORRECTLY identifies G4 as misleading | LOW | Good -- this is the correction |
| 19 | Forensic Audit | 165 | "Gates re-verified: 5/5 PASS" | After fixes -- but which 5? G4 was partial. | MEDIUM | Should specify which 5 gates and note G4 caveats remain |
| 20 | Forensic Audit | 175 | "Total: 5/5 PASS" | Refers to unit tests (5 after adding 2 negative tests) -- accurate | LOW | OK as-is |

---

## f) "3/3" and "N/N" Denominator Concealment Analysis

### Occurrences

| # | File | Line | Context | Hidden Denominator | Severity | Recommendation |
|---|------|------|---------|-------------------|----------|----------------|
| 1 | Q1.1-REPORT.md | 20 | "3/3 URLs OK (avg 229ms)" | 3 of 64 total portal_urls (4.7%). Smoke test used --limit parameter | HIGH | Must say "3/64 URLs smoke-tested OK" |
| 2 | Q1.1-REPORT.md | 21 | "3 unit tests covering all validators" | 3 tests for 4 validators. "all validators" is technically false (link_check not tested). Later upgraded to 5. | MEDIUM | Should say "3 tests covering 3 of 4 validators" |
| 3 | Q1.1-REPORT.md | 74 | "3/3 PASS" | 3 happy-path-only tests | MEDIUM | "3/3 PASS (happy-path; no negative tests)" |
| 4 | Q1.1-REPORT.md | 93 | "3/3 URLs OK, JSONL generated" | 3 of 64 total URLs | HIGH | "3/64 URLs smoke-tested OK" |
| 5 | gates.md | 88 | "6/6 gates passed" | Accurate denominator for defined gates, but G4 was misleading | MEDIUM | "6/6 defined gates passed (G4 with caveats)" |
| 6 | gates.md | 89 | "4/4 abort conditions cleared" | Accurate -- 4 defined conditions | LOW | OK as-is |
| 7 | gates.md | 91 | "19/19 CCAA profiles" | Accurate -- 19 is the real total | LOW | OK as-is |
| 8 | gates.md | 108 | "PASS (3/3 URLs OK)" | Same as #1 | HIGH | Same fix needed |
| 9 | references.md | 62 | "19/19" | Accurate | LOW | OK as-is |
| 10 | references.md | 63 | "20/20 (Tier 1)" | 20 of 20 Tier 1 cities documented -- accurate for Tier 1 scope but implies broader validation | MEDIUM | "20/20 Tier 1 documented (HTTP check pending)" |
| 11 | Q1-REPORT.md | 15 | "19/19 CCAA profiles" | Accurate | LOW | OK as-is |
| 12 | Q1-REPORT.md | 127 | "19/19" | Accurate | LOW | OK as-is |
| 13 | local.md | 300 | "20/20 cities indexed" | Future success criteria -- prescriptive | LOW | OK as-is |
| 14 | Forensic Audit | 14 | "12/100" | Hallucination risk score -- denominator is explicit | LOW | OK as-is |
| 15 | Forensic Audit | 29 | "7/11 checked OK" | Honest -- states that only 11 of 18 were checked before crash | LOW | Good transparency |
| 16 | Forensic Audit | 106 | "3/3 PASS" | Refers to unit tests -- accurate count | LOW | OK as-is |
| 17 | Forensic Audit | 131 | "11/18 P0 URLs before crash" | Honest reporting | LOW | Good |
| 18 | Forensic Audit | 165 | "5/5 PASS" | Refers to unit tests after fix -- accurate | LOW | OK as-is |

**Critical Pattern:** The "3/3 URLs OK" appears 4 times across 3 files (Q1.1-REPORT.md x2, gates.md x1, Forensic Audit flags it once). The actual denominator is 64 portal_urls across the registry. Testing 3/64 = 4.7% and reporting "3/3" conceals the true scope. This is the single highest-risk semantic inflation pattern in the corpus.

---

## g) "covers"/"coverage" Analysis

### Occurrences

| # | File | Line | Context | Actual Coverage | Severity | Recommendation |
|---|------|------|---------|----------------|----------|----------------|
| 1 | Q1-REPORT.md | 16 | "4-tier coverage strategy for 8,131 municipalities" | Only 20 are actually documented. Strategy exists for the rest but no data. | MEDIUM | OK as-is (says "strategy" not "coverage") |
| 2 | Q1-REPORT.md | 130 | "Ingestion playbook covers 4+ stages" | Accurate -- playbook documents 6 stages | LOW | OK as-is |
| 3 | Q1.1-REPORT.md | 28 | "Source Coverage" (section header) | Table header -- neutral | LOW | OK as-is |
| 4 | Q1.1-REPORT.md | 101 | "Registry covers AGE+CCAA+Local" | 25+19+20=64 sources. "Covers" implies completeness but it is a seed. | MEDIUM | Replace with "Registry includes AGE+CCAA+Local" |
| 5 | gates.md | 12 | "Domain allowlist covers all 3 tiers" | Structural coverage (tiers exist) but 14 domain gaps found | MEDIUM | "Domain allowlist structured across all 3 tiers" |
| 6 | gates.md | 13 | "Ingestion playbook covers 4 stages" | Accurate | LOW | OK as-is |
| 7 | gates.md | 21 | "CCAA registry covers fewer than 10" | Abort condition definition -- accurate | LOW | OK as-is |
| 8 | gates.md | 145 | "Registry covers AGE+CCAA+Local" | Same as #4 | MEDIUM | Same recommendation |
| 9 | local.md | 6 | "Covers ~30% of Spain's population" | Tier 1 cities by population -- statistically plausible | LOW | OK as-is (qualified with ~) |
| 10 | local.md | 1 | "Local Government Coverage Strategy" | Title -- "strategy" not "coverage claim" | LOW | OK as-is |
| 11 | backlog/Q2Q3Q4-backlog.md | 73 | "Production-ready RAG with ... full coverage" | Q4 goal statement -- aspirational | MEDIUM | Should say "expanded coverage" not "full coverage" |
| 12 | backlog/Q2Q3Q4-backlog.md | 84 | "Full CCAA coverage" | Q4 backlog item -- aspirational | MEDIUM | Should say "Complete CCAA coverage (19 communities, P1+P2)" |
| 13 | backlog/Q2Q3Q4-backlog.md | 94 | "Fallback chain covers 95%+ of municipality queries" | Q4 exit criteria -- aspirational/measurable | LOW | OK as-is (it is a target metric) |
| 14 | allowlist.md | 101 | "Clara's coverage areas" | Scoping statement | LOW | OK as-is |
| 15 | local_seed.yaml | 8 | "coverage_pct: ~30%" | Data field -- qualified with ~ | LOW | OK as-is |

---

## h) Additional Dangerous Terms

### "fully validated"

| # | File | Line | Context | Severity | Recommendation |
|---|------|------|---------|----------|----------------|
| 1 | Q1.1-REPORT.md | 11 | "fully validated, machine-readable foundation" | Schema-validated only, NOT HTTP-validated. "Fully" is the dangerous amplifier. | HIGH | Replace with "schema-validated, machine-readable foundation" |

### "resolved" without propagation evidence

| # | File | Line | Context | Severity | Recommendation |
|---|------|------|---------|----------|----------------|
| 1 | Forensic Audit | 165 | "All 10 audit findings have been resolved" | Claims resolution in same session but no evidence that downstream consumers (other docs citing wrong numbers) were also updated | MEDIUM | Should say "All 10 findings addressed in source files; downstream propagation pending verification" |
| 2 | Forensic Audit | 192-201 | All 10 tickets marked "RESOLVED" | Same concern | MEDIUM | Same recommendation |

### "production-ready"

| # | File | Line | Context | Severity | Recommendation |
|---|------|------|---------|----------|----------------|
| 1 | Q2Q3Q4-backlog.md | 73 | "Production-ready RAG" | Q4 goal -- aspirational, not a current claim | LOW | OK as-is (future goal) |

### "no issues" / "no problems"

No occurrences found. CLEAN.

### "fully tested"

No occurrences found. CLEAN.

---

## Summary Risk Matrix

| Category | Occurrences (HIGH) | Occurrences (MEDIUM) | Occurrences (LOW) |
|----------|-------------------|---------------------|-------------------|
| "verified" (URL) | 31 | 2 | 4+ (schema fields) |
| "comprehensive" | 1 | 0 | 0 |
| "complete" | 0 | 3 | 6 |
| "official" | 0 | 0 | 16 |
| "PASS" | 3 | 5 | 12 |
| "3/3" denominator | 4 | 2 | 10 |
| "covers/coverage" | 0 | 5 | 10 |
| "all/every" | 1 | 3 | 11 |
| "fully validated" | 1 | 0 | 0 |
| "resolved" | 0 | 2 | 0 |
| **TOTALS** | **41** | **22** | **69+** |

---

## Top 5 Remediation Priorities

1. **Replace all 31 instances of "verified" for URLs with "documented" or "researched"** -- these URLs have ZERO HTTP evidence; the gaps document explicitly states this.

2. **Change "3/3 URLs OK" to "3/64 URLs smoke-tested OK"** in Q1.1-REPORT.md (x2) and gates.md (x1) -- the denominator concealment is the most dangerous single pattern.

3. **Change "comprehensive catalog" to "foundational catalog"** in Q1-REPORT.md -- 64 sources with 0.25% municipal coverage is not comprehensive.

4. **Change "fully validated" to "schema-validated"** in Q1.1-REPORT.md -- the word "fully" implies HTTP validation which did not occur.

5. **Add explicit caveats to G4 PASS** everywhere it appears -- the forensic audit identified it as MISLEADING but the original documents still say unqualified "PASS."

---

## Conclusion

The documentation is honest in its gaps document (assumptions-gaps.md) and the forensic audit correctly identified the G4 link checker issue. However, the primary reports (Q1-REPORT.md, Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md, gates.md) systematically use inflated language that overstates the validation level. A reader of Q1-REPORT.md alone would believe all 64 URLs were HTTP-tested and verified, when in reality zero URLs were HTTP-tested during Q1 (and only 3 were smoke-tested during Q1.1, with the script crashing on the 12th of 18 P0 URLs).

The "verified" inflation is structural: it permeates the vocabulary of 5+ documents and would require a systematic find-and-replace to remediate.
