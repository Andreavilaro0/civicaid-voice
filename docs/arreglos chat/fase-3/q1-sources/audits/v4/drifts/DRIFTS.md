# Document Drift Report -- Audit v4

**Date:** 2026-02-18
**Auditor:** A3 (Drift & Consistency Reconciler), Anti-Hallucination Audit v4
**Mode:** STRICT READ-ONLY (zero files modified)
**Repository:** /Users/andreaavila/Documents/hakaton/civicaid-voice

---

## Summary: 22 drifts found (3 P0, 10 P1, 9 P2)

All drifts are documentation-layer issues where report text diverged from actual data files. Zero data-level fabrications were found. The underlying YAML/JSON/Python artifacts are correct; only the human-readable reports are stale.

### Ground Truth Reference (computed from evidence files)

| Data File | Key Metric | Actual Value | Evidence Source |
|-----------|-----------|--------------|-----------------|
| registry.yaml | Total sources | 44 (25 AGE + 19 CCAA) | registry-counts.txt |
| registry.yaml | AGE priority | P0=10, P1=11, P2=4 | registry-counts.txt line 4 |
| registry.yaml | CCAA priority | P0=5, P1=8, P2=6 | registry-counts.txt line 4 |
| registry.yaml | Lines | 799 | registry-counts.txt line 6 |
| local_seed.yaml | Sources | 20 | registry-counts.txt line 5 |
| local_seed.yaml | Lines | 413 | registry-counts.txt line 7 |
| allowlist.yaml | Tier 1 (AGE) | 22 domains | policy-counts.txt line 3 |
| allowlist.yaml | Tier 2 (CCAA) | 19 domains | policy-counts.txt line 4 |
| allowlist.yaml | Tier 3 (Municipal) | 19 domains | policy-counts.txt line 5 |
| allowlist.yaml | Lines | 355 | policy-counts.txt line 6 |
| allowlist.yaml | default_action | reject | policy-counts.txt line 2 |
| blocklist.yaml | Categories | 9 | policy-counts.txt line 8 |
| blocklist.yaml | Domains in categories | 23 | policy-counts.txt line 9 |
| blocklist.yaml | Top-level patterns | 4 | policy-counts.txt line 10 |
| canonical_rules.yaml | Named rules / Pipeline steps | 10 / 12 | policy-counts.txt lines 13-14 |
| test_validators.py | Test count | 5 (5/5 PASS) | pytest-collect-only.txt, pytest-run.txt |
| Phantom paths | 4 paths not found | data/ingested/* (Q2 planned) | phantom-paths.txt |
| URL coverage | 20 NOT_COVERED out of 157 | 12.7% gap | url-extract.txt |

---

## DRIFT-01: AGE priority split (P1=10, P2=5 claimed vs P1=11, P2=4 actual)

- **Severity:** P0
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 14
- **Claimed value:** "25 AGE sources documented (10 P0, 10 P1, 5 P2)"
- **Actual value:** P0=10, P1=11, P2=4 (total still 25)
- **Evidence:** `registry-counts.txt` line 4: `by_jurisdiction_priority: {"age-P0": 10, "age-P1": 11, "age-P2": 4, ...}`
- **Impact:** A reader relying on Q1-REPORT.md would miscategorize one AGE source (age-boe-sumarios) as P2 instead of P1, leading to incorrect priority planning for ingestion in Q2. This is the top-level summary document and the first line most stakeholders read.

---

## DRIFT-02: Municipal tier_3 domain count in Q1-REPORT

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 74
- **Claimed value:** "Tier 3 (Municipal): 12 seed cities, on-demand expansion"
- **Actual value:** 19 domains in tier_3_municipal section of allowlist.yaml
- **Evidence:** `policy-counts.txt` line 5: `tier_3_municipal: 19 domains`; confirmed by reading `data/policy/allowlist.yaml` lines 248-336 which lists 19 domain entries
- **Impact:** Understates municipal allowlist coverage by 7 domains (37% delta). Could cause confusion about what domains are trusted for local-level procedures.

---

## DRIFT-03: Municipal domain count in Q1.1-REPORT bullet #3

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` line 17
- **Claimed value:** "allowlist (22 AGE + 19 CCAA + 12 municipal domains)"
- **Actual value:** 22 AGE + 19 CCAA + 19 municipal domains
- **Evidence:** `policy-counts.txt` line 5: `tier_3_municipal: 19 domains`
- **Impact:** Same root cause as DRIFT-02. AUDIT-03 in the forensic audit added 7 municipal domains but did not propagate the change to Q1.1-REPORT.md.

---

## DRIFT-04: Allowlist.yaml line count in Q1.1-REPORT

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` line 48
- **Claimed value:** "| `data/policy/allowlist.yaml` | 319 | 3-tier domain allowlist |"
- **Actual value:** 355 lines (confirmed by `wc -l`)
- **Evidence:** `policy-counts.txt` line 6: `allowlist.yaml lines: 355`
- **Impact:** The file grew from ~319 to 355 lines after AUDIT-03 added 7 municipal domains + 4 CCAA aliases. A developer cross-checking line counts would encounter a 36-line discrepancy.

---

## DRIFT-05: Unit test count in Q1.1-REPORT (two locations)

- **Severity:** P0
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` lines 21 and 74
- **Claimed value:** Line 21: "**3 unit tests** covering all validators pass in CI-compatible pytest"; Line 74: "| `tests/unit/test_validators.py` | 3 | 3/3 PASS |"
- **Actual value:** 5 tests, 5/5 PASS
- **Evidence:** `pytest-collect-only.txt` shows "collected 5 items" with 5 test functions listed; `pytest-run.txt` shows "5 passed in 0.60s"
- **Impact:** Understates test coverage by 40%. The 2 negative tests (test_invalid_proceduredoc_rejected, test_missing_file_rejected) added by AUDIT-04 are real and valuable. Omitting them makes the test suite appear weaker than it is.

---

## DRIFT-06: Phantom paths in Q1-REPORT (ingested/* directories)

- **Severity:** P0
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` lines 107-108
- **Claimed value:** "Store: `data/ingested/procedures/<id>.json` + `data/ingested/raw/<domain>/<hash>` + `catalog.json`"
- **Actual value:** Neither `data/ingested/procedures/` nor `data/ingested/raw/` exist on disk
- **Evidence:** `phantom-paths.txt` lines 8-9: "PHANTOM: data/ingested/procedures/<id>.json (referenced in ...Q1-REPORT.md:107)" and "PHANTOM: data/ingested/raw/<domain>/<hash> (referenced in ...Q1-REPORT.md:107)"
- **Impact:** A developer or Q2 implementer reading Q1-REPORT would expect these directories to exist. They are Q2 planned artifacts described in the ingestion pipeline design, but not flagged as future work in the Store bullet point. The text reads as if they are current file locations.

---

## DRIFT-07: Gates.md AGE P1 count

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 31
- **Claimed value:** "P1 sources: 10 (Carpeta Ciudadana, Clave, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)"
- **Actual value:** 11 P1 sources. The missing source is `age-boe-sumarios` (BOE Sumarios Diarios).
- **Evidence:** `registry-counts.txt` line 4: `"age-P1": 11`
- **Impact:** The named list has 10 items and the count says 10, but the actual registry has 11 P1 sources. BOE Sumarios was reclassified from implicit P0 to P1 but gates.md was never updated.

---

## DRIFT-08: Gates.md AGE P2 count

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 32
- **Claimed value:** "P2 sources: 5 (MUFACE, INE, Catastro, Transparencia)"
- **Actual value:** 4 P2 sources
- **Evidence:** `registry-counts.txt` line 4: `"age-P2": 4`
- **Impact:** The count label says "5" but only 4 names are listed. Internally inconsistent -- a reader cannot reconcile the number with the named sources.

---

## DRIFT-09: Gates.md blocklist categories count

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 55
- **Claimed value:** "Blocklist: 8 categories explicitly blocked (commercial, SEO, forums, social media, etc.)"
- **Actual value:** 9 categories in blocklist.yaml (the 9th is `ai_generated` with empty domain list)
- **Evidence:** `policy-counts.txt` line 8: `blocklist categories: 9`; confirmed by reading `data/policy/blocklist.yaml` which lists 9 `- category:` entries (lines 8, 16, 22, 30, 39, 44, 51, 57, 63)
- **Impact:** Minor -- the `ai_generated` category has `domains: []` and may have been excluded from the count because it has zero current domains. However, the category exists and will catch AI-generated content as it is discovered.

---

## DRIFT-10: Gates.md municipal seed count

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 54
- **Claimed value:** "Tier 3 (Municipal): 12 initial seed cities"
- **Actual value:** 19 domains in tier_3_municipal
- **Evidence:** `policy-counts.txt` line 5: `tier_3_municipal: 19 domains`
- **Impact:** Same root cause as DRIFT-02 and DRIFT-03. The gates.md file echoes the same stale "12" count.

---

## DRIFT-11: Gates.md pytest expected output

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 138
- **Claimed value:** "# Output: 3 passed"
- **Actual value:** "5 passed"
- **Evidence:** `pytest-run.txt` line 15: "5 passed in 0.60s"
- **Impact:** A developer running the command and comparing output would see a mismatch. Low severity because the test suite itself still passes.

---

## DRIFT-12: Gates.md Q1.1 abort condition A3 test count

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` line 147
- **Claimed value:** "| A3 | Reproducible validation scripts | CLEAR (4 scripts, 3 tests) |"
- **Actual value:** 4 scripts, 5 tests
- **Evidence:** `pytest-collect-only.txt` line 7: "collected 5 items"
- **Impact:** Understates test count in the abort condition clearance table.

---

## DRIFT-13: FORENSIC-AUDIT abort condition A5 test count

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 30
- **Claimed value:** "| A5: \"Gates PASS\" not reproducible | **NOT TRIGGERED** | All 4 scripts pass, 3/3 tests pass |"
- **Actual value:** 5/5 tests pass
- **Evidence:** `pytest-run.txt` line 15: "5 passed in 0.60s"
- **Impact:** The forensic audit itself is stale in its early section (line 30) even though the "Fixes Applied" section (line 175) correctly states "5/5 PASS." Internal self-contradiction within the same document.

---

## DRIFT-14: FORENSIC-AUDIT Claims Ledger municipal count

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 84
- **Claimed value:** "| Allowlist tier_3_municipal domains | 12 | **12** | VERIFIED | `validate_policy.py` |"
- **Actual value:** 19 domains in tier_3_municipal
- **Evidence:** `policy-counts.txt` line 5: `tier_3_municipal: 19 domains`
- **Impact:** The forensic audit's own Claims Ledger says "12 VERIFIED" but AUDIT-03 in the same report added 7 domains, making the total 19. The ledger contradicts the fixes section of the same document.

---

## DRIFT-15: FORENSIC-AUDIT Gate Claims unit test count

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 106
- **Claimed value:** "| Unit tests | 3/3 PASS | **3/3 PASS** | VERIFIED | pytest exit 0 |"
- **Actual value:** 5/5 PASS
- **Evidence:** `pytest-run.txt` line 15: "5 passed in 0.60s"
- **Impact:** Same as DRIFT-13. The Gate Claims table was not updated after AUDIT-04 added 2 tests.

---

## DRIFT-16: FORENSIC-AUDIT commands section stale

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 213
- **Claimed value:** "pytest tests/unit/test_validators.py -v                # 3/3 PASS"
- **Actual value:** 5/5 PASS
- **Evidence:** `pytest-run.txt` line 15: "5 passed in 0.60s"
- **Impact:** Verification command comments show stale expected output.

---

## DRIFT-17: FORENSIC-AUDIT "All 10 resolved" behavioral drift

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md` line 165
- **Claimed value:** "All 10 audit findings have been resolved. Gates re-verified: 5/5 PASS."
- **Actual value:** Data/code fixes were applied, but report documents (Q1-REPORT.md, Q1.1-REPORT.md, gates.md, README.md, and the forensic audit itself) were NOT updated with post-fix numeric values. At least 20+ stale claims remain across 5+ documents.
- **Evidence:** This entire drift report demonstrates that 21 other drifts exist in documentation. The forensic audit itself has 4 internal stale claims (DRIFT-13, -14, -15, -16).
- **Impact:** "All 10 resolved" creates false confidence that downstream consumers can rely on report text. It is accurate at the data/code layer but misleading at the documentation layer. A stakeholder reading only the forensic audit would believe all issues are fixed when significant doc staleness remains.

---

## DRIFT-18: Fase-3 README.md test count

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/README.md` line 76
- **Claimed value:** "3 tests unitarios -- 3/3 PASS"
- **Actual value:** 5 tests, 5/5 PASS
- **Evidence:** `pytest-collect-only.txt` line 7: "collected 5 items"; `pytest-run.txt` line 15: "5 passed in 0.60s"
- **Impact:** This is the fase-3 landing page README. A developer or judge arriving here first would see stale test metrics. The README was never updated after AUDIT-04 added 2 negative tests.

---

## DRIFT-19: URL coverage gap (20 NOT_COVERED URLs)

- **Severity:** P1
- **Source doc:** Implicit across all documents that claim comprehensive allowlist coverage
- **Claimed value:** Documents imply full allowlist coverage of all registry URLs
- **Actual value:** 20 NOT_COVERED URLs out of 157 (12.7% gap)
- **Evidence:** `url-extract.txt` lines 7-27 list 20 NOT_COVERED URLs across 9 unique domains: `muface.es`, `imserso.es`, `ine.es` / `servicios.ine.es`, `jccm.es`, `carm.es` / `sede.carm.es`, `juntaex.es` / `tramites.juntaex.es`, `seuelectronica.palma.cat`, `seuelectronica.l-h.cat`, `sede.coruna.gal`
- **Impact:** Under strict allowlist-first enforcement (default_action: reject), these 20 URLs from official government sources would be rejected. The `.gob.es` sede counterparts for AGE sources are covered, but portal URLs and some CCAA/local URLs are not.

---

## DRIFT-20: v3 ground-truth-counts.txt test count

- **Severity:** P1
- **Source doc:** `docs/arreglos chat/fase-3/audits-v3/evidence/ground-truth-counts.txt` line 36
- **Claimed value:** "test_validators.py: 0 tests"
- **Actual value:** 5 tests (5/5 PASS)
- **Evidence:** `pytest-collect-only.txt` shows "collected 5 items"; `pytest-run.txt` shows "5 passed"
- **Impact:** The v3 preflight ground-truth counting script failed to parse test functions from test_validators.py (likely searched for top-level `def test_` but missed class-based test methods). This false "0 tests" count contradicts the g5-pytest.txt evidence in the same v3 evidence directory. Any downstream consumer of ground-truth-counts.txt would get a false zero.

---

## DRIFT-21: Phantom path data/tramites/*.json

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 116
- **Claimed value:** "Backward compatible with existing `data/tramites/*.json`."
- **Actual value:** The directory `data/tramites/` exists and contains 8 JSON files (ayuda_alquiler.json, certificado_discapacidad.json, empadronamiento.json, imv.json, justicia_gratuita.json, nie_tie.json, prestacion_desempleo.json, tarjeta_sanitaria.json). The phantom-paths.txt incorrectly flags `data/tramites/*.json` as PHANTOM because glob patterns are not literal file paths.
- **Evidence:** `phantom-paths.txt` line 24: "[PHANTOM] data/tramites/*.json" but the directory is listed at line 23 as "[FOUND] data/tramites/". Filesystem check confirms 8 .json files exist.
- **Impact:** Low. The phantom-paths evidence file is itself misleading on this entry. The actual data/tramites/ directory exists with 8 KB JSONs. The glob pattern is not a phantom -- it is a real reference to real files. However, the Q1-REPORT text implies the migration from these files to ProcedureDoc format is ready, when it is Q2 planned work.

---

## DRIFT-22: Cross-document false consistency on P1/P2 (Q1-REPORT + gates.md)

- **Severity:** P2
- **Source doc:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` line 14 + `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md` lines 31-32
- **Claimed value:** Both Q1-REPORT.md and gates.md agree on AGE P1=10, P2=5
- **Actual value:** P1=11, P2=4
- **Evidence:** `registry-counts.txt` line 4: `"age-P1": 11, "age-P2": 4`
- **Impact:** Two documents independently agree on the wrong values, creating false reassurance of accuracy via mutual consistency. A reader checking Q1-REPORT against gates.md would conclude both are correct. This is a meta-drift -- fixing DRIFT-01, DRIFT-07, and DRIFT-08 resolves it automatically.

---

## Drift Summary Statistics

| Type | Count |
|------|-------|
| documentation_drift | 18 |
| behavioral_drift | 1 (DRIFT-17) |
| data_drift | 1 (DRIFT-20) |
| coverage_gap | 1 (DRIFT-19) |
| false_consistency | 1 (DRIFT-22) |
| **Total** | **22** |

| Severity | Count | Drift IDs |
|----------|-------|-----------|
| P0 | 3 | DRIFT-01, DRIFT-05, DRIFT-06 |
| P1 | 10 | DRIFT-02, DRIFT-03, DRIFT-04, DRIFT-13, DRIFT-14, DRIFT-17, DRIFT-18, DRIFT-19, DRIFT-20, (grouped) |
| P2 | 9 | DRIFT-07, DRIFT-08, DRIFT-09, DRIFT-10, DRIFT-11, DRIFT-12, DRIFT-15, DRIFT-16, DRIFT-21, DRIFT-22 |

---

## Systemic Root Causes

### RC-1: Post-Fix Documentation Propagation Failure (14 drifts)
**Affects:** DRIFT-02, -03, -04, -05, -10, -11, -12, -13, -14, -15, -16, -17, -18, -22

The forensic audit (AUDIT-01 through AUDIT-10) fixed data and code artifacts but did NOT propagate numeric changes back to report files. This is the single largest root cause, responsible for 14 of 22 drifts.

### RC-2: Research-to-Implementation Priority Divergence (4 drifts)
**Affects:** DRIFT-01, -07, -08, -22

When Q1 research (markdown) was converted to Q1.1 implementation (YAML), `age-boe-sumarios` was reclassified from implicit P0 ("BOE x3") to explicit P1. Research documents were never updated.

### RC-3: Allowlist Coverage Gaps (1 drift)
**Affects:** DRIFT-19

9 domains referenced in registry.yaml and local_seed.yaml are not covered by any allowlist tier or auto-allow pattern under strict enforcement.

### RC-4: Preflight Script Bug (1 drift)
**Affects:** DRIFT-20

The v3 ground-truth counting script produced a false "0 tests" count for test_validators.py because it searched for top-level `def test_` functions but missed class-based test methods.

### RC-5: Phantom Path Audit False Positive (1 drift)
**Affects:** DRIFT-21

The phantom-paths check treated glob patterns (e.g., `data/tramites/*.json`) as literal file paths. The directory and files exist; only the glob syntax is not a resolvable path.

### RC-6: Q2 Planned Artifacts Referenced as Current (1 drift)
**Affects:** DRIFT-06

The ingestion pipeline design section describes planned storage paths that do not yet exist on disk, without marking them as future/planned.

---

*Generated by A3v4 (Drift & Consistency Reconciler), Anti-Hallucination Audit v4, 2026-02-18*
*Mode: STRICT READ-ONLY -- zero files modified*
