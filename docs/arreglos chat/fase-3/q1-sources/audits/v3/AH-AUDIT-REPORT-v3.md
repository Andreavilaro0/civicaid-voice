# Anti-Hallucination Audit v3 -- Biblioteca Oficial v0

**Date:** 2026-02-18
**Auditor:** Claude Code (Opus 4.6), 5-Agent Anti-Hallucination Pipeline v3
**Repo:** /Users/andreaavila/Documents/hakaton/civicaid-voice
**Scope:** All Q1/Q1.1 documentation, data files, scripts, schemas, tests
**Mode:** STRICT READ-ONLY (zero source files modified)
**Previous audits:** v1 (50 claims, CONDITIONAL PASS), v2 (185 claims, CONDITIONAL PASS)

---

## 1. Executive Summary

**Final Verdict: CONDITIONAL PASS**

This is the strictest audit iteration to date: 301 claims extracted and evaluated (up from 50 in v1 and 185 in v2), with a dedicated Semantic Red Team agent (A5) added to probe inflated language. The overall verdict is a three-layer assessment:

| Layer | Verdict | Basis |
|-------|---------|-------|
| **Data layer** | **STRONG PASS** | All 4 validation scripts pass, both JSON Schemas valid, 5/5 unit tests pass, 64/64 source entries conform to schema, 0 phantom files, 0 fabricated URLs, 0 duplicate IDs, 0 blocklist/allowlist overlap |
| **Documentation layer** | **FAIL** | 20 CONTRADICTED claims, 18 drifts (14 inherited from post-fix propagation failure), 79 semantic inflations including systemic misuse of "verified" (80+ instances with 0 HTTP evidence) |
| **URL layer** | **155/156 COVERED** | 1 NOT_COVERED domain: `oficinavirtual.cordoba.es` (local-cordoba catalogo_url) |

The data artifacts (registry.yaml, local_seed.yaml, allowlist.yaml, blocklist.yaml, canonical_rules.yaml, schemas, scripts, tests) are accurate and internally consistent. The documentation layer has significant staleness and semantic inflation that, if left unaddressed, would mislead a reader into believing URLs were HTTP-tested when they were only researched, and that all post-forensic issues were fully resolved when 14+ stale claims remain.

**Hallucination Risk:** Data fabrication = 0/100 (none). Documentation accuracy = 25/100 (stale). Semantic inflation = 62/100 (MEDIUM-HIGH). Weighted composite = CONDITIONAL PASS.

---

## 2. Methodology

Five agents operated in strict read-only mode across the entire Q1/Q1.1 corpus:

### A1: Claim Extractor
- Extracted 238 factual/structural claims (C-001 through C-238) from all documentation, data files, scripts, schemas, and prior audit reports
- Each claim tagged with `claim_type` (COUNT, STRUCTURE, BEHAVIOR, CROSSREF, SEMANTIC), `source_file`, `source_locator`, and `expected_evidence` (FILE, CMD, or BOTH)

### A2: Evidence Verifier
- Ran 54 reproducible verification checks with saved outputs (preflight.txt, g1-registry.txt through g6-ruff.txt, ground-truth-counts.txt)
- Each check executed against live data files and scripts
- Ground truth reference computed independently from YAML/JSON data files

### A3: Drift Reconciler
- Compared all numeric claims across 4+ documents against ground truth computed from data files
- Identified 18 drifts (DRIFT-01 through DRIFT-18) with root cause analysis
- Produced FIX-PLAN.md with exact old-to-new text replacements for each drift

### A4: Policy/Schema Deep Verifier
- Phantom file check: 32 referenced file paths verified (32/32 FOUND)
- URL allowlist compliance: 156 URLs extracted from registry.yaml + local_seed.yaml, each domain checked against allowlist tiers and pattern rules
- Deep schema analysis: SourceRegistry.v1 (7 required fields, 2 conditional rules, 5 enums) and ProcedureDoc.v1 (13 required fields, 4 oneOf constructs, 3 pattern constraints)
- Duplicate ID check, blocklist/allowlist overlap check, sample validation

### A5: Semantic Red Team
- Extracted 63 semantic entries (SEM-001 through SEM-063) targeting inflated language
- Analyzed usage of "verified" (80+ occurrences, 3 distinct meanings, only 1 with evidence), "comprehensive" (0.25% municipal coverage), "PASS" (concealing limited test scope), "3/3" (concealing 4.7% denominator), "all" (overgeneralizing), "resolved" (without propagation), "covers/coverage" (implying completeness)
- Assigned overall semantic risk score: 62/100 (MEDIUM-HIGH)

---

## 3. Claims Summary

### 3.1 By Status

| Status | Count | % |
|--------|------:|---:|
| VERIFIED | 195 | 64.8% |
| CONTRADICTED | 20 | 6.6% |
| SEMANTIC_FLAG | 79 | 26.2% |
| UNVERIFIED | 7 | 2.3% |
| **TOTAL** | **301** | **100.0%** |

### 3.2 By Claim Type

| Claim Type | Count | Description |
|------------|------:|-------------|
| COUNT | 120 | Numeric claims (line counts, source counts, test counts, domain counts) |
| SEMANTIC | 79 | Language-level claims ("verified", "comprehensive", "PASS", "all", etc.) |
| STRUCTURE | 38 | Structural claims (file existence, field presence, schema conformance) |
| CROSSREF | 34 | Cross-document consistency claims (same fact in 2+ documents) |
| BEHAVIOR | 30 | Runtime/behavioral claims (script outputs, API responses, test results) |
| **TOTAL** | **301** | |

### 3.3 Status x Type Breakdown

| Status | COUNT | STRUCTURE | BEHAVIOR | CROSSREF | SEMANTIC |
|--------|------:|----------:|---------:|---------:|---------:|
| VERIFIED | 107 | 38 | 22 | 28 | 0 |
| CONTRADICTED | 13 | 0 | 1 | 6 | 0 |
| SEMANTIC_FLAG | 0 | 0 | 0 | 0 | 79 |
| UNVERIFIED | 0 | 0 | 7 | 0 | 0 |

---

## 4. Contradictions (CONTRADICTED)

20 claims are CONTRADICTED. All are documentation-layer issues where report text diverged from the actual data files. Zero data-level fabrications were found.

### 4.1 Root Cause 1: Post-Fix Documentation Propagation Failure (14 drifts)

The forensic audit (AUDIT-01 through AUDIT-10) fixed data and code artifacts but did NOT propagate numeric changes back to report files. This single root cause accounts for 11 of 18 drifts and the majority of contradictions.

| Claim ID | File | Claimed | Actual | Drift |
|----------|------|---------|--------|-------|
| C-034 | Q1-REPORT.md line 75 | Tier 3 Municipal: 12 seed cities | 19 domains in tier_3_municipal | DRIFT-02 |
| C-071 | Q1.1-REPORT.md line 17 | 22 AGE + 19 CCAA + 12 municipal | 22 + 19 + 19 municipal | DRIFT-03 |
| C-085 | Q1.1-REPORT.md line 48 | allowlist.yaml 319 lines | 355 lines | DRIFT-04 |
| C-078 | Q1.1-REPORT.md line 21 | 3 unit tests | 5 unit tests (5/5 PASS) | DRIFT-05a |
| C-091 | Q1.1-REPORT.md line 74 | 3 tests, 3/3 PASS | 5 tests, 5/5 PASS | DRIFT-05b |
| C-108 | Q1.1-REPORT.md line 138 | pytest: 3 passed | 5 passed | DRIFT-05 |
| C-124 | gates.md line 54 | Tier 3: 12 initial seed cities | 19 domains | DRIFT-10 |
| C-125 | gates.md line 55 | Blocklist: 8 categories | 9 categories | DRIFT-09 |
| C-141 | gates.md line 138 | pytest: 3 passed | 5 passed | DRIFT-08 |
| C-164 | PS-SCHEMA-VERIFY (DRIFT-01) | 12 municipal domains | 19 | DRIFT-03 |
| C-165 | PS-SCHEMA-VERIFY (DRIFT-02) | 3 unit tests | 5 | DRIFT-05 |
| C-206 | FORENSIC-AUDIT line 84 | tier_3_municipal = 12 | 19 | DRIFT-12 |
| C-219 | CROSSREF: Q1.1 vs PS-SCHEMA | 3 tests vs 5 tests | 5 tests | DRIFT-05 |
| C-220 | CROSSREF: Q1.1 vs PS-SCHEMA | 12 municipal vs 19 | 19 | DRIFT-03 |

### 4.2 Root Cause 2: BOE Source Priority Reclassification (5 drifts)

When Q1 research (markdown) was converted to Q1.1 implementation (YAML), `age-boe-sumarios` was reclassified from implicit P0 ("BOE x3") to explicit P1. Research documents were never updated.

| Claim ID | File | Claimed | Actual | Drift |
|----------|------|---------|--------|-------|
| C-006 | Q1-REPORT.md line 14 | AGE P1=10 | P1=11 | DRIFT-01 |
| C-007 | Q1-REPORT.md line 14 | AGE P2=5 | P2=4 | DRIFT-01 |
| C-018 | Q1-REPORT.md line 31 | AGE P1=10 | P1=11 | DRIFT-01 |
| C-019 | Q1-REPORT.md line 32 | AGE P2=5 | P2=4 | DRIFT-01 |
| C-171 | PS-SCHEMA-VERIFY line 43 | gates.md 8 vs actual 9 categories | 9 categories | DRIFT-09 |
| C-221 | CROSSREF: gates.md vs PS-SCHEMA | 8 vs 9 categories | 9 | DRIFT-09 |

### 4.3 Fix Reference

All 20 contradictions have exact text replacements documented in `drifts/FIX-PLAN.md`. Each replacement specifies the file path, line number, old string, and new string.

---

## 5. Semantic Inflation Analysis

Agent A5 (Semantic Red Team) evaluated the corpus for inflated language that overstates confidence, scope, or validation level. 63 semantic entries were cataloged in `semantic/semantic.jsonl` and analyzed in `semantic/SEMANTIC-REPORT.md`.

### 5.1 Overall Risk Score: 62/100 (MEDIUM-HIGH)

### 5.2 Key Findings

**"verified" (80+ occurrences, 31 HIGH severity):**
The word "verified" carries three distinct meanings in the corpus, only one of which has machine evidence:
1. **schema-validated** -- scripts confirm YAML/JSON conforms to JSON Schema. This is supported.
2. **research-verified** -- URLs were found during web research. NO HTTP HEAD/GET was ever run. This is the dominant usage (31 HIGH instances).
3. **HTTP-verified** -- implies live connectivity testing. Zero occurrences of this actually happened during Q1.

The gaps document (`assumptions-gaps.md` line 24) explicitly states: "No actual HTTP validation of URLs performed (research-only constraint)" -- yet "verified" is used 30+ times in other documents to describe these same URLs. This is a direct internal contradiction.

**"comprehensive" (1 HIGH):**
Q1-REPORT.md line 11 calls the catalog "comprehensive" despite covering only 64 sources and 20 of 8,131 municipalities (0.25% municipal coverage).

**"PASS" (3 HIGH, 5 MEDIUM):**
Gate G4 ("Link checker smoke test: PASS, 3/3 URLs OK") is the highest-risk instance. Only 3 of 64 portal_urls were tested (4.7%). The forensic audit itself identified G4 as MISLEADING, but the original documents (Q1.1-REPORT.md line 93, gates.md line 108) still say unqualified "PASS."

**"3/3" denominator concealment (4 HIGH):**
The pattern "3/3 URLs OK" appears 4 times across 3 files. The true denominator is 64 portal_urls. Reporting "3/3" instead of "3/64" conceals that only 4.7% of URLs were smoke-tested. This is the single highest-risk semantic inflation pattern.

**"All resolved" (MEDIUM):**
The forensic audit claims "All 10 audit findings have been resolved" (line 165) but did not propagate numeric changes to downstream documents. At least 14 stale claims remain across Q1-REPORT.md, Q1.1-REPORT.md, gates.md, and the forensic audit report itself.

### 5.3 Severity Distribution

| Category | HIGH | MEDIUM | LOW |
|----------|-----:|-------:|----:|
| "verified" (URL) | 31 | 2 | 4+ |
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

Note: "official" usage is CLEAN across the corpus -- it consistently means "government-domain" or "legally designated," never "endorsed by CivicAid."

---

## 6. URL Allowlist Compliance

Agent A4 extracted all `portal_url`, `sede_url`, `catalogo_url`, and `api_url` fields from `registry.yaml` (44 sources) and `local_seed.yaml` (20 sources), then checked each URL's domain against the 3-tier allowlist plus pattern rules.

### 6.1 Summary

| Metric | Value |
|--------|-------|
| Total URL entries extracted | 156 |
| Unique domains | 67 |
| COVERED (by explicit tier or pattern) | 155 |
| NOT_COVERED | 1 |

### 6.2 NOT_COVERED Domain

| Source ID | URL | Domain | Recommendation |
|-----------|-----|--------|----------------|
| local-cordoba | `https://oficinavirtual.cordoba.es/catalogo-de-tramites-y-servicios` | `oficinavirtual.cordoba.es` | Add as alias under `cordoba.es` in tier_3_municipal |

**Analysis:** The allowlist has `cordoba.es` in tier_3_municipal but only the base domain and `sede.cordoba.es` as alias. The subdomain `oficinavirtual.cordoba.es` is not explicitly covered. Under strict enforcement, this URL would be rejected.

### 6.3 Additional Ambiguities

A4 also identified 5 portal_url domains using `.es` TLD that are NOT explicitly listed in any allowlist tier (`muface.es`, `imserso.es`, `ine.es`/`servicios.ine.es`, `jccm.es`). Their `.gob.es` sede counterparts ARE covered, so only the portal_url path would be affected under strict enforcement.

### 6.4 Machine-Readable Output

Full URL audit saved to: `url-audit/url-coverage.jsonl` (156 entries)

---

## 7. Drift Inventory & Fix Plan

Agent A3 identified 18 drifts between documentation claims and data-file ground truth.

### 7.1 Severity Distribution

| Severity | Count | Drift IDs |
|----------|------:|-----------|
| P0 (Critical) | 1 | DRIFT-15: Behavioral drift -- "All 10 audit findings have been resolved" is misleading without propagation evidence |
| P1 (High) | 8 | DRIFT-01, -02, -03, -04, -05, -11, -12, -16 |
| P2 (Low) | 9 | DRIFT-06, -07, -08, -09, -10, -13, -14, -17, -18 |
| **Total** | **18** | |

### 7.2 Type Distribution

| Type | Count |
|------|------:|
| documentation_drift | 16 |
| behavioral_drift | 1 |
| data_drift | 1 |
| **Total** | **18** |

### 7.3 Systemic Root Causes

**RC-1: Post-Fix Documentation Propagation Failure** (11 drifts)
Affects: DRIFT-02, -03, -04, -05, -08, -10, -11, -12, -13, -14, -15.
The forensic audit fixed data/code artifacts but did NOT propagate numeric changes back to report files. This is the single largest root cause.

**RC-2: Research-to-Implementation Priority Divergence** (5 drifts)
Affects: DRIFT-01, -06, -07, -17, -18.
When Q1 research (markdown) was converted to Q1.1 implementation (YAML), `age-boe-sumarios` was reclassified from implicit P0 to explicit P1. Research documents were never updated.

**RC-3: Preflight Script Bug** (1 drift)
Affects: DRIFT-16.
The v3 ground-truth counting script produced a false "0 tests" count for test_validators.py, likely because it searched for top-level `def test_` functions but missed class-based test methods. The actual count is 5 tests (confirmed by g5-pytest.txt showing "collected 5 items").

### 7.4 Fix Plan Reference

All 18 drifts have exact text replacements documented in `drifts/FIX-PLAN.md`. The plan is organized into three phases:

- **Phase 1 -- P0:** 1 replacement (DRIFT-15, FORENSIC-AUDIT line 165)
- **Phase 2 -- P1:** 9 replacements (DRIFT-01 through -05, -11, -12, -16)
- **Phase 3 -- P2:** 8 replacements (DRIFT-06 through -10, -13, -14, -17)

DRIFT-18 (cross-document false consistency) requires no separate fix -- it is resolved automatically when DRIFT-01, -06, and -07 are applied.

---

## 8. Recommendations

### Priority 1: IMMEDIATE

1. **Apply FIX-PLAN.md** -- Execute all 18 text replacements documented in `drifts/FIX-PLAN.md`. Start with the P0 fix (DRIFT-15: add propagation caveat to "All 10 audit findings have been resolved"), then P1, then P2. Estimated effort: 30 minutes manual or scriptable via sed.

### Priority 2: HIGH

2. **Add `oficinavirtual.cordoba.es` to allowlist** -- Add as alias under the `cordoba.es` entry in `tier_3_municipal` within `data/policy/allowlist.yaml`. This closes the only NOT_COVERED URL gap.

3. **Replace "verified" with "documented" for research-only URLs** -- Across 31 HIGH-severity instances in Q1-REPORT.md, local.md (20 city status columns), gates.md, references.md, and local_seed.yaml. The gaps document already states "no HTTP validation performed" -- the other documents should use consistent language. Recommended replacements:
   - "verified" (URL context) --> "documented" or "researched"
   - "fully validated" --> "schema-validated"
   - "comprehensive catalog" --> "foundational catalog"

### Priority 3: MEDIUM

4. **Add pre-commit hook to detect count/number drifts** -- After any data file change (YAML/JSON), automatically grep report markdown files for stale numeric values. This would have prevented 11 of 18 drifts.

5. **Fix ground-truth-counts.txt test_validators.py entry** -- Line 36 shows "test_validators.py: 0 tests" but the actual count is 5 tests (confirmed by g5-pytest.txt). The preflight script's test-counting logic should be updated to handle class-based test methods.

### Priority 4: LOW

6. **Add explicit G4 caveats** -- Everywhere G4 is reported as "PASS" (Q1.1-REPORT.md line 93, gates.md line 108), add qualifier: "PASS (smoke, 3/64 URLs, dry-run only)". The forensic audit identified G4 as MISLEADING but the original documents were never updated.

7. **Consider adding 5 `.es` portal domains to allowlist** -- `muface.es`, `imserso.es`, `ine.es`, `servicios.ine.es`, and `jccm.es` are not explicitly listed. Their `.gob.es` sede counterparts are covered, but strict enforcement would reject the portal URLs.

---

## Appendix A: Evidence Files

All evidence files are located under `docs/arreglos chat/fase-3/audits-v3/` relative to the repository root.

### A2 Evidence (Reproducible Verification Outputs)

| File | Description |
|------|-------------|
| `evidence/preflight.txt` | Environment snapshot: Python 3.11.8, repo root, file tree, skills detection |
| `evidence/g1-registry.txt` | Output of `validate_source_registry.py` (44+20 sources, PASS) |
| `evidence/g2-policy.txt` | Output of `validate_policy.py` (allowlist, blocklist, canonical_rules: all PASS) |
| `evidence/g3-proceduredoc.txt` | Output of `validate_proceduredoc_schema.py` (PASS, completeness 0.86) |
| `evidence/g4-linkcheck-dryrun.txt` | Output of `link_check.py --dry-run` |
| `evidence/g5-pytest.txt` | Output of `pytest tests/unit/test_validators.py -v` (5 passed) |
| `evidence/g6-ruff.txt` | Output of `ruff check` (lint clean) |
| `evidence/ground-truth-counts.txt` | Computed counts from all data files (registry, allowlist, blocklist, canonical, schemas, tests) |
| `evidence/a4-deep-verification.md` | A4 full report: phantom file check, URL allowlist compliance, deep schema analysis |

### A3 Drift Files

| File | Description |
|------|-------------|
| `drifts/DRIFTS.md` | 18 drifts with root cause analysis, severity, affected files |
| `drifts/FIX-PLAN.md` | Exact old-to-new text replacements for all 18 drifts |

### A5 Semantic Files

| File | Description |
|------|-------------|
| `semantic/SEMANTIC-REPORT.md` | Full semantic inflation analysis across 8 categories |
| `semantic/semantic.jsonl` | 63 semantic entries in machine-readable JSONL |

### A4 URL Audit

| File | Description |
|------|-------------|
| `url-audit/url-coverage.jsonl` | 156 URL entries with coverage status (155 COVERED, 1 NOT_COVERED) |

### Claims File

| File | Description |
|------|-------------|
| `claims.v3.jsonl` | 301 claims with final statuses (195 VERIFIED, 20 CONTRADICTED, 79 SEMANTIC_FLAG, 7 UNVERIFIED) |

---

## Appendix B: Verification Commands

All commands assume the repository root as working directory and the project virtual environment is activated.

```bash
# G1: Source Registry Validation
python3 scripts/validate_source_registry.py
# Expected: PASS (44 sources -- AGE: 25, CCAA: 19, Local: 0)
#           PASS (20 sources -- AGE: 0, CCAA: 0, Local: 20)

# G2: Policy Validation
python3 scripts/validate_policy.py
# Expected: allowlist.yaml: PASS, blocklist.yaml: PASS, canonical_rules.yaml: PASS

# G3: ProcedureDoc Schema Validation
python3 scripts/validate_proceduredoc_schema.py \
  "docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"
# Expected: PASS: proceduredoc.sample.json valid against ProcedureDoc v1
#           completeness: 0.86

# G5: Unit Tests
pytest tests/unit/test_validators.py -v
# Expected: 5 passed (3 happy-path + 2 negative tests)

# G6: Lint Check
ruff check scripts/ tests/unit/test_validators.py --select E,F,W --ignore E501
# Expected: All checks passed!

# Post-Fix Drift Detection (run after applying FIX-PLAN.md)
grep -rn "10 P1" "docs/arreglos chat/fase-3/"
grep -rn "5 P2" "docs/arreglos chat/fase-3/"
grep -rn "12 municipal" "docs/arreglos chat/fase-3/"
grep -rn "12 seed" "docs/arreglos chat/fase-3/"
grep -rn "3 unit test" "docs/arreglos chat/fase-3/"
grep -rn "3/3 PASS" "docs/arreglos chat/fase-3/"
grep -rn "| 319 |" "docs/arreglos chat/fase-3/"
grep -rn "8 categories" "docs/arreglos chat/fase-3/"
grep -rn "0 tests" "docs/arreglos chat/fase-3/"
# Expected: Zero matches after all fixes applied
```

---

*Generated by Claude Code (Opus 4.6), 5-Agent Anti-Hallucination Pipeline v3*
*Date: 2026-02-18*
*Mode: STRICT READ-ONLY -- zero source files modified*
*Claims: 301 (195 VERIFIED, 20 CONTRADICTED, 79 SEMANTIC_FLAG, 7 UNVERIFIED)*
