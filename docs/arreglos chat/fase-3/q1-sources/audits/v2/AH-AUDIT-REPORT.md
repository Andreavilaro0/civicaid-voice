# AH-AUDIT-REPORT v2 — Anti-Hallucination Audit

**Date:** 2026-02-18
**Mode:** STRICT READ-ONLY (zero files modified)
**Auditor:** Claude Opus 4.6 (5 parallel agents + lead consolidation)
**Scope:** Q1 + Q1.1 Biblioteca Oficial v0 + v1 audit artifacts
**Repository:** /Users/andreaavila/Documents/hakaton/civicaid-voice
**Agents:** A1 (Claim Extractor, 158 claims), A2 (Evidence Verifier, 32 checks), A3 (Consistency Reconciler, 14 drifts), A4 (Policy/Schema Deep Verifier, 14/14 pass), A5 (Skeptic Red Team, 27 semantic entries)

---

## 1. Executive Summary

### Claim Status Distribution

| Status | Count | % |
|--------|-------|---|
| VERIFIED | 131 | 70.8% |
| CONTRADICTED | 15 | 8.1% |
| UNVERIFIED | 1 | 0.5% |
| SEMANTIC_FLAG | 38 | 20.5% |
| **Total** | **185** | 100% |

### High-Risk Areas

1. **SEMANTIC INFLATION (38 flags):** The word "verified" appears 12 times across reports and always means "research-verified" (someone browsed the site and typed the URL), NEVER "HTTP-verified" (automated 200 check). The project's own `assumptions-gaps.md` (G1) explicitly states: "No actual HTTP validation of URLs performed." Every use of "verified URLs" is misleading.

2. **DOCUMENTATION DRIFT (14 drifts, 15 contradictions):** All contradictions are documentation-not-updated-after-data-changes. Zero data fabrications. Root cause: forensic audit (AUDIT-01 through AUDIT-10) fixed data/code artifacts but did NOT update the report text that references those artifacts.

3. **DENOMINATOR CONCEALMENT:** "3/3 URLs OK" appears in 3 documents. The actual denominator is 64 portal_urls (or 157 total URLs). The notation creates false impression of comprehensive validation when only 4.7% was tested.

4. **NEW vs v1:** This v2 audit found **9 additional drifts** that v1 missed:
   - DRIFT-02: Q1-REPORT "12 seed cities" vs 19 (Q1-REPORT was not audited in v1)
   - DRIFT-04: Q1.1 allowlist "319 lines" vs 355 (completely new)
   - DRIFT-07: gates.md P1 count "10" vs 11 (v1 only caught P2)
   - DRIFT-09: gates.md "8 categories" vs 9 (completely new)
   - DRIFT-10: Forensic audit internal "3/3" vs "5/5" inconsistency
   - DRIFT-11: "All 10 resolved" behavioral drift (docs still stale)
   - DRIFT-12: Three-way disagreement on municipal domain count
   - DRIFT-13: Three-way disagreement on test count
   - DRIFT-14: Cross-doc false consistency (Q1-REPORT + gates.md agree on wrong P1/P2)

### Verdict Preview

**CONDITIONAL PASS** — Core data artifacts are accurate and schema-validated. Documentation has 15 stale numeric claims and 38 semantic inflation issues. Zero data-level fabrications. Zero phantom files. Zero invented URLs.

---

## 2. VERIFIED Claims Summary (Top 15)

| # | Claim | Type | Evidence |
|---|-------|------|----------|
| 1 | 44 sources in registry.yaml (25 AGE + 19 CCAA) | COUNT | `validate_source_registry.py` exit 0 |
| 2 | 20 sources in local_seed.yaml | COUNT | same script, exit 0 |
| 3 | AGE P0 = 10, CCAA P0 = 5, Total P0 = 15 | COUNT | Python yaml count |
| 4 | 19/19 CCAA profiles in registry | COUNT | validator output |
| 5 | Allowlist: tier_1=22, tier_2=19, tier_3=19, default=reject | COUNT | Python yaml count |
| 6 | Blocklist: 9 categories, 23 domains, 4 patterns | COUNT | Python yaml count |
| 7 | Canonical: 10 rules, 12 pipeline steps, 17 tracking, 7 session | COUNT | Python yaml count |
| 8 | Research docs: 9 files, 4,448 total lines (each individually verified) | COUNT | `wc -l` exact match |
| 9 | ProcedureDoc schema: 296 lines, Draft 2020-12 | STRUCTURE | `wc -l` + JSON inspection |
| 10 | ProcedureDoc sample: completeness 0.86, base_legal populated | BEHAVIOR | validator script output |
| 11 | All 4 validators pass with exit 0 | BEHAVIOR | Direct execution |
| 12 | 5/5 pytest tests pass | BEHAVIOR | `pytest -v` output |
| 13 | ruff lint: zero errors | BEHAVIOR | `ruff check` output |
| 14 | All 64 portal_urls traceable to research docs (61 exact, 3 subdomain) | CROSSREF | A5 URL traceability |
| 15 | Zero phantom files (30+ referenced paths all exist) | STRUCTURE | A5 phantom check |

---

## 3. CONTRADICTED Claims (15 items, exact conflict evidence)

### 3.1 Numeric Count Contradictions (9 items)

| # | Document | Line | Claimed | Actual | Command | DRIFT |
|---|----------|------|---------|--------|---------|-------|
| 1 | Q1-REPORT.md | 14 | AGE "10 P1, 5 P2" | P1=11, P2=4 | `python3 -c "import yaml; ..."` count by priority | DRIFT-01 |
| 2 | Q1-REPORT.md | 74 | "12 seed cities" in allowlist | 19 tier_3_municipal | `python3 -c` count tier_3 | DRIFT-02 |
| 3 | Q1.1-REPORT.md | 17 | "12 municipal domains" | 19 domains | same command | DRIFT-03 |
| 4 | Q1.1-REPORT.md | 48 | allowlist "319 lines" | 355 lines | `wc -l allowlist.yaml` | DRIFT-04 |
| 5 | Q1.1-REPORT.md | 21,74 | "3 unit tests" / "3/3 PASS" | 5 tests, 5/5 PASS | `pytest -v` | DRIFT-05 |
| 6 | gates.md | 32 | "P2 sources: 5" | 4 P2 sources | yaml count | DRIFT-06 |
| 7 | gates.md | 31 | "P1 sources: 10" | 11 P1 sources | yaml count | DRIFT-07 |
| 8 | gates.md | 138 | "Output: 3 passed" | "5 passed" | `pytest -v` | DRIFT-08 |
| 9 | gates.md | 55 | "8 categories blocked" | 9 categories | yaml count | DRIFT-09 |

### 3.2 Internal Document Contradictions (3 items)

| # | Document | Lines | Contradiction | DRIFT |
|---|----------|-------|--------------|-------|
| 10 | FORENSIC-AUDIT.md | 30,106,213 vs 165,175 | Says "3/3 tests" in early sections, "5/5 PASS" in fixes section | DRIFT-10 |
| 11 | FORENSIC-AUDIT.md | 84 | Claims Ledger says "tier_3: 12 VERIFIED" but AUDIT-03 added 7 more → 19 | DRIFT-12 |
| 12 | FORENSIC-AUDIT.md | 165 | "All 10 findings resolved" but 9+ stale claims remain in docs | DRIFT-11 |

### 3.3 Cross-Document False Consistency (3 items)

| # | Documents | What Happened | DRIFT |
|---|-----------|--------------|-------|
| 13 | Q1-REPORT + gates.md | Both agree on P1=10, P2=5 — both wrong (P1=11, P2=4). Mutual consistency is false reassurance. | DRIFT-14 |
| 14 | Q1.1-REPORT + FORENSIC Claims Ledger | Both say "12 municipal domains" — both wrong (actual 19). FORENSIC verified at 12, then added 7 via AUDIT-03 without updating own ledger. | DRIFT-12 |
| 15 | Q1.1-REPORT + gates.md | Both say "3 tests" — both wrong (actual 5). AUDIT-04 added 2 tests but neither doc updated. | DRIFT-13 |

---

## 4. UNVERIFIED Claims (evidence missing, Q2 plan)

| # | Claim | Why Unverified | Q2 Resolution |
|---|-------|---------------|---------------|
| 1 | "20 municipal sede URLs verified" | NO HTTP 200 checks performed; "verified" = research-verified only. assumptions-gaps.md G1 confirms this. | Q2-LINK-01: Run `link_check.py` against all local_seed URLs, preserve JSONL evidence. |
| 2 | "BOE REST API: no auth, XML/JSON" | No live API test in repo. Endpoints respond (200/404) but no data request evidence. | Q2-ING-04: BOE API integration test with real requests. |
| 3 | "3/3 URLs OK avg 229ms" | Timing data is ephemeral — no preserved log artifact. Run itself is not reproducible offline. | Preserve JSONL output as evidence artifact after each run. |
| 4 | "Forensic audit: 325 claims extracted" | Report says 325 but only ~30 are shown in ledger. Full extraction not preserved. | Either publish full 325-claim ledger or correct the count. |

**Note:** Items 2-4 are classified UNVERIFIED because no in-repo evidence exists for them. They are not necessarily false — they simply cannot be confirmed READ-ONLY.

---

## 5. Drift Taxonomy

### Distribution

| Type | Count | Description |
|------|-------|-------------|
| documentation_drift | 13 | Report text not updated after data/code changes |
| behavioral_drift | 1 | "All resolved" claim contradicted by stale docs |
| data_drift | 0 | No cases where data files changed after docs and docs were correct |

### Systemic Root Cause

All 14 drifts share **one systemic root cause:** the forensic audit (AUDIT-01 through AUDIT-10) fixed data and code artifacts but did NOT propagate numeric changes back to report files. This created a two-layer staleness:

- **Layer 1 (data fixes, DONE):** allowlist.yaml +7 domains, test_validators.py +2 tests, link_check.py crash fix, proceduredoc base_legal filled, blocklist +1 category
- **Layer 2 (doc propagation, NOT DONE):** Q1-REPORT.md, Q1.1-REPORT.md, gates.md, and even sections of the forensic audit itself were never updated

### Full Drift Table

| DRIFT | Severity | Claimed | Actual | File:Line | Type |
|-------|----------|---------|--------|-----------|------|
| DRIFT-01 | P1 | AGE P1=10, P2=5 | P1=11, P2=4 | Q1-REPORT:14 | documentation_drift |
| DRIFT-02 | P1 | 12 seed cities | 19 domains | Q1-REPORT:74 | documentation_drift |
| DRIFT-03 | P1 | 12 municipal domains | 19 domains | Q1.1-REPORT:17 | documentation_drift |
| DRIFT-04 | P1 | 319 lines | 355 lines | Q1.1-REPORT:48 | documentation_drift |
| DRIFT-05 | P1 | 3 unit tests | 5 tests | Q1.1-REPORT:21,74 | documentation_drift |
| DRIFT-06 | P2 | 5 P2 sources | 4 sources | gates.md:32 | documentation_drift |
| DRIFT-07 | P2 | 10 P1 sources | 11 sources | gates.md:31 | documentation_drift |
| DRIFT-08 | P2 | 3 passed | 5 passed | gates.md:138 | documentation_drift |
| DRIFT-09 | P2 | 8 categories | 9 categories | gates.md:55 | documentation_drift |
| DRIFT-10 | P2 | 3/3 internally | 5/5 actual | FORENSIC:30,106,213 | documentation_drift |
| DRIFT-11 | P0 | "All 10 resolved" | 9+ stale claims remain | FORENSIC:165 | behavioral_drift |
| DRIFT-12 | P1 | 12 verified (3-way) | 19 actual | FORENSIC:84 | documentation_drift |
| DRIFT-13 | P2 | 3/3 PASS (3-way) | 5/5 PASS | Multiple | documentation_drift |
| DRIFT-14 | P2 | P1=10,P2=5 (agreed) | P1=11,P2=4 | Q1+gates cross-doc | documentation_drift |

---

## 6. Semantic Closure Analysis

### "verified" (12 occurrences — ALL research-verified, ZERO HTTP-verified)

Every use of "verified" in relation to URLs means someone manually browsed a government website and typed the URL into a markdown document. **No automated HTTP 200 check was ever performed.** The project's own `assumptions-gaps.md` (Gap G1, line 24) confirms: "No actual HTTP validation of URLs performed (research-only constraint)."

**Affected files:** Q1-REPORT.md (lines 16, 58), ccaa.md (lines 4, 660), local.md (lines 18, 22-41), gates.md (lines 11, 45, 92), references.md (lines 30, 39), local_seed.yaml (line 32)

**Recommendation:** Replace every "verified URLs" with "research-documented URLs (HTTP validation pending Q2)" or "manually cataloged URLs."

### "official" (5 occurrences — ACCEPTABLE)

All uses correctly mean "belonging to government entities" (.gob.es, .es domains). No claim implies government endorsement of CivicAid. No change needed.

### "comprehensive" / "complete" / "all" (6 occurrences — PARTIALLY MISLEADING)

- "comprehensive catalog" (Q1-REPORT:11) — covers 64 sources but misses 8,111/8,131 municipalities (99.75% gap at local level)
- "at all three administrative levels" (Q1-REPORT:11) — technically true but conceals 0.25% municipal coverage
- "all critical sedes" (Q1-REPORT:14) — circular: "critical" = P0 by self-definition
- "Allowlist complete" (Q1-REPORT:129) — structural completeness only, not domain coverage

**Recommendation:** Replace "comprehensive" with "structured" or "extensive." Add "(seed coverage at local level)" where municipal coverage is implied.

### "3/3 URLs OK" (3 occurrences — DENOMINATOR CONCEALED)

- Q1.1-REPORT:20, Q1.1-REPORT:93, gates.md:108
- Denominator the reader infers: 3 (all URLs tested)
- Actual denominator: 64 portal_urls, or 157 total URLs
- Coverage: 4.7% of portal_urls

**Recommendation:** Replace with "3/64 sampled URLs OK" or "smoke test: 3 P0 URLs spot-checked."

---

## 7. Reproducible Command Log

All commands executed against: `REPO=/Users/andreaavila/Documents/hakaton/civicaid-voice`, `VENV=$REPO/.venv/bin/python3`

### Validators (all PASS)

```bash
$VENV $REPO/scripts/validate_source_registry.py
# Output: PASS (44 sources — AGE: 25, CCAA: 19, Local: 0)
#         PASS (20 sources — AGE: 0, CCAA: 0, Local: 20)

$VENV $REPO/scripts/validate_policy.py
# Output: allowlist PASS, blocklist PASS, canonical_rules PASS

$VENV $REPO/scripts/validate_proceduredoc_schema.py \
  "$REPO/docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"
# Output: PASS, id=age-inss-ingreso-minimo-vital, completeness=0.86

$VENV $REPO/scripts/link_check.py --smoke --limit 5 --dry-run
# Output: 3 URLs listed, dry run complete

$VENV -m pytest $REPO/tests/unit/test_validators.py -v --tb=short
# Output: 5 passed in 0.59s

$VENV -m ruff check $REPO/scripts/ --select E,F,W --ignore E501
# Output: All checks passed!
```

### Ground Truth Counts

```bash
# Registry priorities
$VENV -c "import yaml; r=yaml.safe_load(open('$REPO/data/sources/registry.yaml')); \
  by_j_p={}; \
  [by_j_p.update({f'{s[\"jurisdiction\"]}-{s[\"priority\"]}': by_j_p.get(f'{s[\"jurisdiction\"]}-{s[\"priority\"]}',0)+1}) for s in r['sources']]; \
  print(by_j_p)"
# Output: {'age-P0': 10, 'age-P1': 11, 'age-P2': 4, 'ccaa-P0': 5, 'ccaa-P1': 8, 'ccaa-P2': 6}

# Allowlist domain counts
$VENV -c "import yaml; a=yaml.safe_load(open('$REPO/data/policy/allowlist.yaml')); \
  print('tier_1:', len(a['tier_1_age']['domains']), \
        'tier_2:', len(a['tier_2_ccaa']['domains']), \
        'tier_3:', len(a['tier_3_municipal']['domains']))"
# Output: tier_1: 22 tier_2: 19 tier_3: 19

# Blocklist
$VENV -c "import yaml; b=yaml.safe_load(open('$REPO/data/policy/blocklist.yaml')); \
  print('categories:', len(b['categories']), \
        'domains:', sum(len(c.get('domains',[])) for c in b['categories']), \
        'patterns:', len(b.get('patterns',[])))"
# Output: categories: 9 domains: 23 patterns: 4

# File line counts
wc -l $REPO/data/sources/registry.yaml $REPO/data/sources/local_seed.yaml \
  $REPO/data/policy/allowlist.yaml $REPO/data/policy/blocklist.yaml \
  $REPO/data/policy/canonical_rules.yaml
# Output: 799 + 413 + 355 + 72 + 233

# Research doc total
wc -l "$REPO/docs/arreglos chat/fase-3/q1-sources/source-registry/"*.md \
      "$REPO/docs/arreglos chat/fase-3/q1-sources/link-governance/"*.md \
      "$REPO/docs/arreglos chat/fase-3/q1-sources/ingestion/"*.md
# Output: 518+665+403+229+322+545+446+739+581 = 4448 total
```

---

## 8. "No Hallucination" Sign-Off Checklist

### Data-Level Checks (all PASS)

- [x] All source counts reproducible via scripts (44+20=64 verified)
- [x] All 4 validation scripts pass exit 0 (schema-validated)
- [x] All research doc line counts match exactly (4,448 total)
- [x] All 30+ referenced file paths exist (zero phantom files)
- [x] All 64 portal_urls traceable to research docs (zero fabricated URLs)
- [x] ProcedureDoc sample validates (completeness 0.86, base_legal populated)
- [x] Link checker runs without crash (AUDIT-01 fix confirmed)
- [x] Policy default_action = reject in both allowlist and blocklist
- [x] Zero overlap between allowlist and blocklist domains
- [x] All 10 canonical rules referenced in 12-step pipeline
- [x] All 44 registry entries have required fields (zero duplicates)
- [x] All 20 local_seed entries have required fields (zero duplicates)
- [x] 5/5 pytest tests pass
- [x] ruff lint: zero errors

### Documentation-Level Checks (BLOCKED)

- [ ] **BLOCKED:** 15 stale numeric claims across Q1-REPORT, Q1.1-REPORT, gates.md, FORENSIC-AUDIT (DRIFT-01 through DRIFT-14)
- [ ] **BLOCKED:** 12 instances of "verified" meaning research-verified, not HTTP-verified (semantic inflation)
- [ ] **BLOCKED:** "3/3 URLs OK" denominator conceals 95.3% untested coverage
- [ ] **BLOCKED:** "comprehensive catalog" misleading at municipal level (0.25% coverage)
- [ ] **BLOCKED:** Forensic audit claims "all 10 resolved" but docs remain stale (DRIFT-11)

---

## 9. Verdict

### CONDITIONAL PASS

**Hallucination Risk Score: 18/100 (LOW)**

| Category | Score | Evidence |
|----------|-------|----------|
| Data fabrication | 0/100 | Zero invented URLs, files, or counts |
| Schema validity | 0/100 | All schemas validate, all entries conform |
| Documentation drift | 25/100 | 15 stale claims, all traceable to post-fix propagation failure |
| Semantic inflation | 35/100 | "verified" misused 12 times, "comprehensive" overreaches, "3/3" misleading |
| Test coverage | 15/100 | Tests verify tooling works but not data correctness |
| **Weighted average** | **18/100** | Data = 0 (weight 50%), Docs = 25 (weight 25%), Semantics = 35 (weight 15%), Tests = 15 (weight 10%) |

### To Achieve FULL PASS

**Minimal documentation updates needed (no code changes):**

1. Q1-REPORT.md line 14: "10 P1, 5 P2" → "11 P1, 4 P2"
2. Q1-REPORT.md line 74: "12 seed cities" → "19 seed cities"
3. Q1.1-REPORT.md line 17: "12 municipal domains" → "19 municipal domains"
4. Q1.1-REPORT.md line 48: "319" → "355"
5. Q1.1-REPORT.md lines 21, 74: "3 unit tests" → "5 unit tests", "3/3" → "5/5"
6. gates.md line 31: P1 count "10" → "11"
7. gates.md line 32: P2 count "5" → "4"
8. gates.md line 55: "8 categories" → "9 categories"
9. gates.md line 138: "3 passed" → "5 passed"
10. FORENSIC-AUDIT.md lines 30, 106, 213: "3/3" → "5/5"
11. FORENSIC-AUDIT.md line 84: tier_3 "12" → "19"
12. All "verified URLs" → "research-documented URLs (HTTP validation pending Q2)"
13. Q1-REPORT.md line 11: "comprehensive" → "structured" or "extensive"
14. All "3/3 URLs OK" → "3/64 sampled URLs OK (smoke test)"

---

## 10. Comparison: v1 Audit vs v2 Audit

| Metric | v1 (PS-SCHEMA-VERIFY) | v2 (this report) |
|--------|----------------------|-------------------|
| Total claims | 50 | 185 |
| VERIFIED | 41 | 131 |
| CONTRADICTED | 5 | 15 |
| UNVERIFIED | 4 | 1 (+ 3 behavioral) |
| SEMANTIC_FLAG | 0 | 38 |
| Drifts found | 5 | 14 |
| New drifts not in v1 | — | 9 (DRIFT-02,04,07,09,10,11,12,13,14) |
| Semantic analysis | None | 27 entries |
| URL traceability | Not checked | 64/64 checked (61 exact) |
| Phantom file check | Not checked | 30+ files confirmed |
| Deep schema checks | Partial | 14/14 pass |
| Blocklist/allowlist overlap | Not checked | 0 overlap confirmed |
| Domain coverage analysis | Not checked | 100% of registry URLs in allowlist |
| Verdict | CONDITIONAL PASS | CONDITIONAL PASS |
| Hallucination Risk | 15/100 | 18/100 (higher due to semantic flags) |

---

*Generated by Anti-Hallucination Audit v2, 2026-02-18*
*Machine-readable companion: claims.jsonl (185 claims)*
*Agent outputs: A3 drifts (14), A4 reproducibility (14/14 pass), A5 red team (semantic closure)*
