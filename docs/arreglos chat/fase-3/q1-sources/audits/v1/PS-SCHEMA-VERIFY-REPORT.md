# PS-SCHEMA-VERIFY-REPORT — Anti-Hallucination Audit

**Date:** 2026-02-18
**Mode:** READ-ONLY
**Auditor:** Claude Code (5 simulated agents: A1 Claim Extractor, A2 Evidence Verifier, A3 Consistency Reconciler, A4 Policy/Schema Deep Verifier, A5 Skeptic Red Team)
**Scope:** Q1 + Q1.1 Biblioteca Oficial v0 artifacts
**Repository:** /Users/andreaavila/Documents/hakaton/civicaid-voice

---

## 1. Executive Summary (12 bullets, each referencing claim_id)

1. (C-01, C-02, C-03) 64 total sources verified: 44 in registry.yaml + 20 in local_seed.yaml. VERIFIED.
2. (C-04, C-05, C-06) Priority breakdown: 10 AGE P0, 5 CCAA P0, 15 total P0. VERIFIED.
3. (C-07) All 19/19 CCAA communities covered. VERIFIED.
4. (C-08, C-09) Allowlist: 22 AGE domains + 19 CCAA domains. VERIFIED.
5. (C-41) CONTRADICTED: Q1.1 report says "12 municipal domains" but actual is 19 (post-AUDIT-03 drift).
6. (C-42, C-45) CONTRADICTED: Q1.1 report says "3 unit tests" but actual is 5/5 PASS. Gates.md expected output also stale ("3 passed" vs "5 passed").
7. (C-43, C-44) CONTRADICTED: Q1 report claims AGE P1=10, P2=5 but actual P1=11, P2=4. Gates.md lists 4 P2 names but says "5".
8. (C-17, C-18, C-19) All 4 validation scripts pass with exit code 0. VERIFIED.
9. (C-20, C-50) Link checker runs live without crash (AUDIT-01 fix confirmed). 3/3 OK.
10. (C-23 through C-32) All 9 research docs line counts match exactly. Total: 4,448. VERIFIED.
11. (C-46, C-47) UNVERIFIED: No HTTP validation of 20 municipal URLs or BOE API (research-only phase).
12. (C-36, C-16) ProcedureDoc sample has base_legal populated and completeness 0.86. VERIFIED.

---

## 2. Claims Ledger

### 2.1 VERIFIED Claims (40 claims)

| claim_id | claim_text | claim_type | status | evidence_file | evidence_excerpt | reproducible_check | notes |
|----------|-----------|------------|--------|---------------|------------------|--------------------|-------|
| C-01 | "44 sources in registry.yaml (25 AGE + 19 CCAA)" | COUNT | VERIFIED | data/sources/registry.yaml | `python3 scripts/validate_source_registry.py` -> "PASS (44 sources)" | `python3 scripts/validate_source_registry.py` | 25 AGE + 19 CCAA = 44 |
| C-02 | "20 sources in local_seed.yaml" | COUNT | VERIFIED | data/sources/local_seed.yaml | same script -> "PASS (20 sources)" | `python3 scripts/validate_source_registry.py` | 20 local municipality sources |
| C-03 | "64 total sources across registries" | COUNT | VERIFIED | data/sources/registry.yaml, data/sources/local_seed.yaml | 44 + 20 = 64 | Arithmetic sum of C-01 and C-02 | Trivial derivation |
| C-04 | "AGE P0 = 10 sources" | COUNT | VERIFIED | data/sources/registry.yaml | python count -> 10 | `grep -c 'priority: P0' registry.yaml` (AGE section) | Counted within AGE block |
| C-05 | "CCAA P0 = 5 sources" | COUNT | VERIFIED | data/sources/registry.yaml | python count -> 5 | `grep -c 'priority: P0' registry.yaml` (CCAA section) | Counted within CCAA block |
| C-06 | "Total P0 = 15" | COUNT | VERIFIED | data/sources/registry.yaml | 10 + 5 = 15 | Arithmetic sum of C-04 and C-05 | Trivial derivation |
| C-07 | "19/19 CCAA profiles in registry" | COUNT | VERIFIED | data/sources/registry.yaml | validator -> CCAA: 19 | `python3 scripts/validate_source_registry.py` | All 19 autonomous communities present |
| C-08 | "Allowlist tier_1_age = 22 domains" | COUNT | VERIFIED | data/policy/allowlist.yaml | python count -> 22 | `python3 -c "import yaml; d=yaml.safe_load(open('data/policy/allowlist.yaml')); print(len(d['tier_1_age']['domains']))"` | 22 AGE-level domains |
| C-09 | "Allowlist tier_2_ccaa = 19 domains" | COUNT | VERIFIED | data/policy/allowlist.yaml | python count -> 19 | `python3 -c "import yaml; d=yaml.safe_load(open('data/policy/allowlist.yaml')); print(len(d['tier_2_ccaa']['domains']))"` | 19 CCAA-level domains |
| C-10 | "Blocklist: 9 categories, 23 domains, 4 patterns" | COUNT | VERIFIED | data/policy/blocklist.yaml | python count -> 9 categories, 23 domains, 4 patterns | `python3 -c "import yaml; ..."` | Structure matches claim |
| C-11 | "10 canonicalization rules" | COUNT | VERIFIED | data/policy/canonical_rules.yaml | python count -> 10 | `python3 -c "import yaml; d=yaml.safe_load(open('data/policy/canonical_rules.yaml')); print(len(d['rules']))"` | 10 named canonicalization rules |
| C-12 | "12 pipeline steps" | COUNT | VERIFIED | data/policy/canonical_rules.yaml | python count -> 12 | `python3 -c "import yaml; d=yaml.safe_load(open('data/policy/canonical_rules.yaml')); print(len(d['pipeline']))"` | 12 pipeline steps in order |
| C-13 | "17 tracking params to strip" | COUNT | VERIFIED | data/policy/canonical_rules.yaml | python count -> 17 | Count of tracking_params list items | UTM and analytics params |
| C-14 | "7 session params to strip" | COUNT | VERIFIED | data/policy/canonical_rules.yaml | python count -> 7 | Count of session_params list items | Session/token params |
| C-15 | "ProcedureDoc schema = 296 lines" | COUNT | VERIFIED | schemas/ProcedureDoc.v1.schema.json | `wc -l` -> 296 | `wc -l schemas/ProcedureDoc.v1.schema.json` | Exact line count match |
| C-16 | "ProcedureDoc completeness = 0.86" | COUNT | VERIFIED | scripts/validate_proceduredoc_schema.py output | completeness: 0.86 | `python3 scripts/validate_proceduredoc_schema.py` | Score computed from filled fields ratio |
| C-17 | "registry.yaml validates against schema" | BEHAVIOR | VERIFIED | scripts/validate_source_registry.py | exit code 0 | `python3 scripts/validate_source_registry.py; echo $?` -> 0 | All entries conform to SourceRegistry schema |
| C-18 | "Policy files all validate" | BEHAVIOR | VERIFIED | scripts/validate_policy.py | exit code 0 | `python3 scripts/validate_policy.py; echo $?` -> 0 | allowlist, blocklist, canonical_rules all pass |
| C-19 | "ProcedureDoc sample validates" | BEHAVIOR | VERIFIED | scripts/validate_proceduredoc_schema.py | exit code 0 | `python3 scripts/validate_proceduredoc_schema.py; echo $?` -> 0 | Sample JSON validates against schema |
| C-20 | "Link checker smoke works (no crash)" | BEHAVIOR | VERIFIED | scripts/link_check.py | 3/3 OK live test | `python3 scripts/link_check.py --smoke` | No exceptions, graceful handling |
| C-21 | "All 6 Q1 gates PASS" | CROSSREF | VERIFIED | gates.md | All criteria met | Cross-reference gates.md checklist against evidence | All gate conditions satisfied |
| C-22 | "All 4 abort conditions cleared" | CROSSREF | VERIFIED | gates.md | Abort conditions section | Cross-reference abort conditions | No abort triggers found |
| C-23 | "Research docs total = 4,448 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/*.md | `wc -l` -> 4448 | `wc -l docs/arreglos\ chat/fase-3/q1-sources/*.md` | Sum of all 9 research docs |
| C-24 | "age.md = 518 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/age.md | `wc -l` -> 518 | `wc -l age.md` | Exact match |
| C-25 | "ccaa.md = 665 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/ccaa.md | `wc -l` -> 665 | `wc -l ccaa.md` | Exact match |
| C-26 | "local.md = 403 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/local.md | `wc -l` -> 403 | `wc -l local.md` | Exact match |
| C-27 | "allowlist.md = 229 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/allowlist.md | `wc -l` -> 229 | `wc -l allowlist.md` | Exact match |
| C-28 | "canonicalization.md = 322 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/canonicalization.md | `wc -l` -> 322 | `wc -l canonicalization.md` | Exact match |
| C-29 | "link-checking-spec.md = 545 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/link-checking-spec.md | `wc -l` -> 545 | `wc -l link-checking-spec.md` | Exact match |
| C-30 | "ingestion-playbook.md = 446 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/ingestion-playbook.md | `wc -l` -> 446 | `wc -l ingestion-playbook.md` | Exact match |
| C-31 | "extraction-spec.md = 739 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/extraction-spec.md | `wc -l` -> 739 | `wc -l extraction-spec.md` | Exact match |
| C-32 | "normalization-schema.md = 581 lines" | COUNT | VERIFIED | docs/arreglos chat/fase-3/q1-sources/normalization-schema.md | `wc -l` -> 581 | `wc -l normalization-schema.md` | Exact match |
| C-33 | "default_action: reject in allowlist" | STRUCTURE | VERIFIED | data/policy/allowlist.yaml:3 | `default_action: reject` | `head -5 data/policy/allowlist.yaml` | Reject-by-default policy confirmed |
| C-34 | "default_action: reject in blocklist" | STRUCTURE | VERIFIED | data/policy/blocklist.yaml:4 | `default_action: reject` | `head -5 data/policy/blocklist.yaml` | Reject-by-default policy confirmed |
| C-35 | "No src/ files touched in Q1.1" | STRUCTURE | VERIFIED | file listing | No src/ modifications | `git log --name-only` for Q1.1 commits | Data/docs only phase |
| C-36 | "base_legal populated in ProcedureDoc sample" | STRUCTURE | VERIFIED | data/samples/proceduredoc.sample.json:59-62 | base_legal field present and non-empty | `python3 -c "import json; d=json.load(open('...')); print(d['base_legal'])"` | Contains legal reference strings |
| C-37 | "SourceRegistry schema uses Draft 2020-12" | STRUCTURE | VERIFIED | schemas/SourceRegistry.v1.schema.json:1 | `"$schema": "https://json-schema.org/draft/2020-12/schema"` | `head -1 schemas/SourceRegistry.v1.schema.json` | Draft 2020-12 confirmed |
| C-38 | "ProcedureDoc schema uses Draft 2020-12" | STRUCTURE | VERIFIED | schemas/ProcedureDoc.v1.schema.json:1 | `"$schema": "https://json-schema.org/draft/2020-12/schema"` | `head -1 schemas/ProcedureDoc.v1.schema.json` | Draft 2020-12 confirmed |
| C-39 | "registry.yaml = ~800 lines" | COUNT | VERIFIED | data/sources/registry.yaml | `wc -l` -> 799 | `wc -l data/sources/registry.yaml` | 799 lines, ~800 is accurate |
| C-40 | "local_seed.yaml = 413 lines" | COUNT | VERIFIED | data/sources/local_seed.yaml | `wc -l` -> 413 | `wc -l data/sources/local_seed.yaml` | Exact match |

### 2.2 CONTRADICTED Claims (5 claims)

| claim_id | claim_text | claim_type | status | evidence_file | evidence_excerpt | reproducible_check | notes |
|----------|-----------|------------|--------|---------------|------------------|--------------------|-------|
| C-41 | "Q1.1 report: allowlist has '12 municipal domains'" | COUNT | CONTRADICTED | Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md:17 | "12 municipal domains" | Count tier_3_municipal in allowlist.yaml -> 19 | Post-AUDIT-03 drift; 7 domains added but report not updated |
| C-42 | "Q1.1 report: '3 unit tests'" | COUNT | CONTRADICTED | Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md:21 | "3 unit tests" | `python3 -m pytest tests/ -v` -> 5/5 PASS | Post-AUDIT-04 drift; 2 negative tests added |
| C-43 | "Q1 report: AGE 'P1=10, P2=5'" | COUNT | CONTRADICTED | Q1-REPORT.md:14 | "10 P0, 10 P1, 5 P2" | Count P1/P2 in AGE section of registry.yaml -> P1=11, P2=4 | Priority reassignment between research and implementation |
| C-44 | "Gates.md: '5 P2 AGE sources'" | COUNT | CONTRADICTED | gates.md:32 | "P2 sources: 5 (MUFACE, INE, Catastro, Transparencia)" | Count P2 in registry.yaml -> 4 | Lists 4 names but says "5" |
| C-45 | "Gates.md Q1.1: expected '3 passed'" | COUNT | CONTRADICTED | gates.md:138 | `# Output: 3 passed` | `python3 -m pytest tests/ -v` -> 5 passed | Same root cause as C-42; gates.md not updated |

### 2.3 UNVERIFIED Claims (5 claims)

| claim_id | claim_text | claim_type | status | evidence_file | evidence_excerpt | reproducible_check | notes |
|----------|-----------|------------|--------|---------------|------------------|--------------------|-------|
| C-46 | "20 municipal sede URLs verified" | BEHAVIOR | UNVERIFIED | — | No HTTP evidence | No HTTP request logs preserved | Research-verified only, not HTTP-verified |
| C-47 | "BOE REST API: no auth, XML/JSON" | BEHAVIOR | UNVERIFIED | — | No API test evidence | No curl/requests logs preserved | Claimed in research docs but not tested |
| C-48 | "Link checker 3/3 URLs OK avg 229ms" | BEHAVIOR | UNVERIFIED | — | Specific run not preserved | Run not reproducible without network | Timing data is ephemeral |
| C-49 | "Forensic audit: 325 claims extracted" | COUNT | UNVERIFIED | FORENSIC-AUDIT-REPORT.md | "325 claims extracted" | Only ~30 claims shown in report | Full extraction not preserved |
| C-50 | "link_check.py crash fixed" | BEHAVIOR | VERIFIED | scripts/link_check.py | Safe pattern: try/except around requests | `python3 scripts/link_check.py --smoke` | Reclassified from UNVERIFIED after live test confirmed fix |

---

## 3. Contradictions and Drifts

### DRIFT-01: Q1.1 Report Municipal Domain Count (C-41)

- **Report says:** "12 municipal domains" (Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md, line 17)
- **Actual:** 19 domains in data/policy/allowlist.yaml tier_3_municipal
- **Root cause:** AUDIT-03 (forensic audit) added 7 municipal domains to allowlist.yaml, but Q1.1 report bullet #3 was not updated.
- **Impact:** Medium -- report is stale, could confuse downstream consumers.

### DRIFT-02: Q1.1 Report Test Count (C-42)

- **Report says:** "3 unit tests" (Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md, line 21, and table line 74)
- **Actual:** 5 tests (5/5 PASS)
- **Root cause:** AUDIT-04 added 2 negative test cases, but report not updated.
- **Impact:** Low -- understates test coverage.

### DRIFT-03: Q1.1 Gates.md Expected Output (C-45)

- **Report says:** `# Output: 3 passed` (gates.md, line 138)
- **Actual:** `5 passed`
- **Root cause:** Same as DRIFT-02.
- **Impact:** Low -- copy-paste from gates will fail to match.

### DRIFT-04: Q1 Report AGE P1/P2 Split (C-43)

- **Report says:** "10 P0, 10 P1, 5 P2" = 25 (Q1-REPORT.md, line 14)
- **Actual:** P0=10, P1=11, P2=4 = 25
- **Root cause:** age-boe-sumarios is P1 in registry.yaml but was likely categorized as P2 during Q1 research. Total is still 25 but split differs.
- **Impact:** Medium -- priority assignments mismatch between research and implementation.

### DRIFT-05: Gates.md P2 Count (C-44)

- **Report says:** "P2 sources: 5 (MUFACE, INE, Catastro, Transparencia)" (gates.md, line 32)
- **Actual:** 4 P2 sources, and only 4 names listed despite claiming 5
- **Root cause:** Count typo -- lists 4 names but says "5".
- **Impact:** Low -- the named sources are correct, only the count label is off.

---

## 4. What is Verified vs What is NOT

### FULLY VERIFIED (high confidence)

- Source counts (25 AGE, 19 CCAA, 20 local, 64 total)
- All 4 validation scripts execute and pass (exit 0)
- 5/5 pytest tests pass
- Schema files are valid JSON Schema Draft 2020-12
- ProcedureDoc sample validates with completeness 0.86, base_legal populated
- All 9 research doc line counts match exactly (4,448 total)
- Policy structure: reject-by-default, 3-tier allowlist, blocklist with 9 categories
- Canonical rules: 10 named rules, 12 pipeline steps
- link_check.py runs without crash (AUDIT-01 fix confirmed)

### NOT VERIFIED (needs Q2 work)

- No HTTP validation of any municipal sede URL (20 cities claimed "verified" = research-verified, not HTTP-verified)
- No live BOE API test (endpoints respond but no data requests)
- No HTTP validation of CCAA sede URLs
- No robots.txt compliance check for any domain
- No sitemap.xml verification for any domain
- DIR3 dataset not downloaded or parsed
- Content quality of existing KB tramites not evaluated against ProcedureDoc schema

---

## 5. Missing Checks (Proposed Commands)

```bash
# CHECK-01: HTTP validate all P0 URLs in registry.yaml (smoke)
python3 scripts/link_check.py --smoke --limit 50 --output /tmp/p0_check.jsonl

# CHECK-02: HTTP validate all local_seed.yaml URLs
python3 scripts/link_check.py --limit 100 --output /tmp/local_check.jsonl

# CHECK-03: Verify allowlist covers all registry URLs
python3 -c "
import yaml
# Load registry URLs, extract domains, check against allowlist domains
# Report any domain NOT covered by allowlist tiers
"

# CHECK-04: Validate existing tramites against ProcedureDoc schema
for f in data/tramites/*.json; do
  python3 scripts/validate_proceduredoc_schema.py "\$f"
done

# CHECK-05: BOE API smoke test
curl -s 'https://boe.es/datosabiertos/api/boe/sumario/20260218' | head -20

# CHECK-06: Verify line counts claimed in Q1.1 report table match reality
wc -l data/sources/registry.yaml data/sources/local_seed.yaml data/policy/*.yaml schemas/*.json

# CHECK-07: Cross-reference allowlist domains vs local_seed municipalities
python3 -c "
import yaml
# For each local_seed source, check that its portal domain is in tier_3_municipal
"

# CHECK-08: Run full test suite
python3 -m pytest tests/ -v --tb=short
```

---

## 6. Recommendations (Documentation Only, No Code Changes)

1. **Update Q1.1 report bullet #3**: Change "12 municipal domains" to "19 municipal domains" (matches post-AUDIT-03 state).
2. **Update Q1.1 report line 21**: Change "3 unit tests" to "5 unit tests" (matches post-AUDIT-04 state).
3. **Update Q1.1 report table (line 74)**: Change "3 | 3/3 PASS" to "5 | 5/5 PASS".
4. **Update gates.md Q1.1 (line 138)**: Change `# Output: 3 passed` to `# Output: 5 passed`.
5. **Update Q1-REPORT.md line 14**: Change "10 P1, 5 P2" to "11 P1, 4 P2" (or add note explaining divergence from registry.yaml).
6. **Update gates.md line 32**: Change "5" to "4" for P2 count, or add the 5th P2 source name if intended.
7. **Add HTTP smoke evidence**: Run link_check.py against all registries and preserve JSONL output as an evidence artifact.
8. **Document forensic audit resolution**: Q1.1-FORENSIC-AUDIT-REPORT.md says "All 10 findings resolved" but 5 drift items show the report itself was not updated. Add a "post-fix documentation sweep" step.
9. **Preserve test outputs**: Keep pytest and validator outputs as evidence artifacts alongside reports.
10. **Add version metadata**: Reports should include a `last_updated` field that changes when the report is edited post-factum.

---

## 7. Issues (Priority P0/P1/P2)

| # | Priority | Title | Affected Files | Resolution |
|---|----------|-------|---------------|------------|
| ISS-01 | P1 | Q1.1 report stale: "12 municipal domains" should be 19 | Q1.1-REPORT.md:17 | Update bullet #3 |
| ISS-02 | P1 | Q1.1 report stale: "3 unit tests" should be 5 | Q1.1-REPORT.md:21,74 | Update count and table |
| ISS-03 | P1 | Gates.md Q1.1 expected output stale: "3 passed" should be "5 passed" | gates.md:138 | Update expected output |
| ISS-04 | P1 | Q1 report AGE P1/P2 split does not match registry.yaml | Q1-REPORT.md:14 | Update or annotate |
| ISS-05 | P2 | Gates.md P2 count "5" should be "4" | gates.md:32 | Fix count |
| ISS-06 | P2 | No HTTP smoke evidence artifact preserved | evidence/ | Run link_check, save JSONL |
| ISS-07 | P2 | No cross-check: allowlist domains vs registry URLs | -- | Run CHECK-03 |
| ISS-08 | P2 | Existing tramites/*.json not validated against ProcedureDoc v1 | data/tramites/ | Run CHECK-04 |
| ISS-09 | P2 | Forensic audit says "all resolved" but reports have drift | FORENSIC-AUDIT-REPORT.md | Add documentation sweep step |
| ISS-10 | P2 | No version/last_updated metadata in reports | All reports | Add field |

---

## 8. Sign-Off Checklist

Conditions for declaring 'NO HALLUCINATION':

- [x] All source counts reproducible via scripts (C-01 through C-07)
- [x] All validation scripts pass exit 0 (C-17, C-18, C-19)
- [x] All file existence claims verified (29 files)
- [x] All research doc line counts match (C-23 through C-32, total 4,448)
- [x] ProcedureDoc sample validates with correct completeness (C-16)
- [x] base_legal populated (C-36)
- [x] Link checker does not crash (C-50)
- [x] Policy default_action = reject (C-33, C-34)
- [ ] **BLOCKED**: Q1.1 report has 5 stale claims (DRIFT-01 through DRIFT-05)
- [ ] **BLOCKED**: No HTTP validation evidence for municipal URLs (C-46)
- [ ] **BLOCKED**: Gates.md expected outputs do not match current reality (C-45)

**VERDICT: CONDITIONAL PASS**

Core data is accurate and reproducible. 5 report-level drift items and 0 data-level fabrications found. No URLs invented, no phantom files, no falsified counts in YAML/JSON data. The hallucination risk is in stale documentation, not in the underlying artifacts.

**Sign-off recommendation:** Fix ISS-01 through ISS-05 (documentation updates only, ~15 minutes), then re-run this audit to achieve full PASS.

---

*Generated by PS-SCHEMA-VERIFY audit, 2026-02-18*
*Machine-readable companion: claims.jsonl*
