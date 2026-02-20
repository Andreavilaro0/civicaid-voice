# Fix Plan -- Audit v4 (DOC-ONLY, DO NOT APPLY)

**Date:** 2026-02-18
**Auditor:** A3 (Drift & Consistency Reconciler), Anti-Hallucination Audit v4
**Mode:** READ-ONLY -- NO FILES MODIFIED
**Status:** Plan only. Each replacement below is documented but NOT applied.
**Repository:** /Users/andreaavila/Documents/hakaton/civicaid-voice

---

## Instructions

For each drift, the `Current text` is the exact string found in the file, and `Replacement` is the exact text to use. All file paths are relative to repository root.

---

## FIX-01: AGE P1/P2 split in Q1-REPORT

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Location:** line 14
- **Current text:** `- **25 AGE sources** documented (10 P0, 10 P1, 5 P2) including BOE API, SIA/PAG master catalog, and all critical sedes electronicas`
- **Replacement:** `- **25 AGE sources** documented (10 P0, 11 P1, 4 P2) including BOE API, SIA/PAG master catalog, and all critical sedes electronicas`
- **Linked drift:** DRIFT-01
- **Priority:** P0

---

## FIX-02: Municipal domain count in Q1-REPORT

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Location:** line 74
- **Current text:** `- **Tier 3 (Municipal):** 12 seed cities, on-demand expansion`
- **Replacement:** `- **Tier 3 (Municipal):** 19 municipal domains, on-demand expansion`
- **Linked drift:** DRIFT-02
- **Priority:** P1

---

## FIX-03: Municipal domain count in Q1.1-REPORT bullet #3

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Location:** line 17
- **Current text:** `3. **Domain governance** enforced: allowlist (22 AGE + 19 CCAA + 12 municipal domains), blocklist (23 domains + 4 patterns), 12-step URL canonicalization pipeline (applying 10 named rules)`
- **Replacement:** `3. **Domain governance** enforced: allowlist (22 AGE + 19 CCAA + 19 municipal domains), blocklist (23 domains + 4 patterns), 12-step URL canonicalization pipeline (applying 10 named rules)`
- **Linked drift:** DRIFT-03
- **Priority:** P1

---

## FIX-04: Allowlist line count in Q1.1-REPORT

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Location:** line 48
- **Current text:** `| \`data/policy/allowlist.yaml\` | 319 | 3-tier domain allowlist |`
- **Replacement:** `| \`data/policy/allowlist.yaml\` | 355 | 3-tier domain allowlist |`
- **Linked drift:** DRIFT-04
- **Priority:** P1

---

## FIX-05a: Unit test count in Q1.1-REPORT (bullet)

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Location:** line 21
- **Current text:** `7. **3 unit tests** covering all validators pass in CI-compatible pytest`
- **Replacement:** `7. **5 unit tests** covering all validators pass in CI-compatible pytest`
- **Linked drift:** DRIFT-05
- **Priority:** P0

---

## FIX-05b: Unit test count in Q1.1-REPORT (table)

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`
- **Location:** line 74
- **Current text:** `| \`tests/unit/test_validators.py\` | 3 | 3/3 PASS |`
- **Replacement:** `| \`tests/unit/test_validators.py\` | 5 | 5/5 PASS |`
- **Linked drift:** DRIFT-05
- **Priority:** P0

---

## FIX-06a: Phantom path -- ingested/procedures

- **File:** `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md`
- **Location:** line 107
- **Current text:** `- **Store:** \`data/ingested/procedures/<id>.json\` + \`data/ingested/raw/<domain>/<hash>\` + \`catalog.json\``
- **Replacement:** `- **Store:** \`data/ingested/procedures/<id>.json\` + \`data/ingested/raw/<domain>/<hash>\` + \`catalog.json\` (Q2 planned, not yet created)`
- **Linked drift:** DRIFT-06
- **Priority:** P0

---

## FIX-07: Gates.md AGE P1 count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Location:** line 31
- **Current text:** `- **P1 sources:** 10 (Carpeta Ciudadana, Clave, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)`
- **Replacement:** `- **P1 sources:** 11 (Carpeta Ciudadana, Clave, BOE Sumarios, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)`
- **Linked drift:** DRIFT-07
- **Priority:** P2

---

## FIX-08: Gates.md AGE P2 count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Location:** line 32
- **Current text:** `- **P2 sources:** 5 (MUFACE, INE, Catastro, Transparencia)`
- **Replacement:** `- **P2 sources:** 4 (MUFACE, INE, Catastro, Transparencia)`
- **Linked drift:** DRIFT-08
- **Priority:** P2

---

## FIX-09: Gates.md blocklist categories

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Location:** line 55
- **Current text:** `- **Blocklist:** 8 categories explicitly blocked (commercial, SEO, forums, social media, etc.)`
- **Replacement:** `- **Blocklist:** 9 categories explicitly blocked (commercial, SEO, forums, social media, ai_generated, etc.)`
- **Linked drift:** DRIFT-09
- **Priority:** P2

---

## FIX-10: Gates.md municipal seed count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Location:** line 54
- **Current text:** `- **Tier 3 (Municipal):** 12 initial seed cities`
- **Replacement:** `- **Tier 3 (Municipal):** 19 initial seed cities`
- **Linked drift:** DRIFT-10
- **Priority:** P2

---

## FIX-11: Gates.md pytest expected output

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Location:** line 138
- **Current text:** `# Output: 3 passed`
- **Replacement:** `# Output: 5 passed`
- **Linked drift:** DRIFT-11
- **Priority:** P2

---

## FIX-12: Gates.md Q1.1 abort A3 test count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/gates.md`
- **Location:** line 147
- **Current text:** `| A3 | Reproducible validation scripts | CLEAR (4 scripts, 3 tests) |`
- **Replacement:** `| A3 | Reproducible validation scripts | CLEAR (4 scripts, 5 tests) |`
- **Linked drift:** DRIFT-12
- **Priority:** P2

---

## FIX-13: FORENSIC-AUDIT abort A5 test count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Location:** line 30
- **Current text:** `| A5: "Gates PASS" not reproducible | **NOT TRIGGERED** | All 4 scripts pass, 3/3 tests pass |`
- **Replacement:** `| A5: "Gates PASS" not reproducible | **NOT TRIGGERED** | All 4 scripts pass, 5/5 tests pass |`
- **Linked drift:** DRIFT-13
- **Priority:** P1

---

## FIX-14: FORENSIC-AUDIT Claims Ledger municipal count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Location:** line 84
- **Current text:** `| Allowlist tier_3_municipal domains | 12 | **12** | VERIFIED | \`validate_policy.py\` |`
- **Replacement:** `| Allowlist tier_3_municipal domains | 19 | **19** | VERIFIED | \`validate_policy.py\` |`
- **Linked drift:** DRIFT-14
- **Priority:** P1

---

## FIX-15: FORENSIC-AUDIT Gate Claims unit test count

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Location:** line 106
- **Current text:** `| Unit tests | 3/3 PASS | **3/3 PASS** | VERIFIED | pytest exit 0 |`
- **Replacement:** `| Unit tests | 5/5 PASS | **5/5 PASS** | VERIFIED | pytest exit 0 |`
- **Linked drift:** DRIFT-15
- **Priority:** P2

---

## FIX-16: FORENSIC-AUDIT commands section pytest comment

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Location:** line 213
- **Current text:** `pytest tests/unit/test_validators.py -v                # 3/3 PASS`
- **Replacement:** `pytest tests/unit/test_validators.py -v                # 5/5 PASS`
- **Linked drift:** DRIFT-16
- **Priority:** P2

---

## FIX-17: FORENSIC-AUDIT "All 10 resolved" behavioral caveat

- **File:** `docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md`
- **Location:** line 165
- **Current text:** `All 10 audit findings have been resolved. Gates re-verified: 5/5 PASS.`
- **Replacement:** `All 10 audit findings have been resolved (data/code layer). Gates re-verified: 5/5 PASS. NOTE: Report documents (Q1-REPORT.md, Q1.1-REPORT.md, gates.md, README.md) were NOT updated with post-fix numeric values -- see Audit v4 drift report.`
- **Linked drift:** DRIFT-17
- **Priority:** P1

---

## FIX-18: Fase-3 README.md test count

- **File:** `docs/arreglos chat/fase-3/README.md`
- **Location:** line 76
- **Current text:** `- 3 tests unitarios — 3/3 PASS`
- **Replacement:** `- 5 tests unitarios — 5/5 PASS`
- **Linked drift:** DRIFT-18
- **Priority:** P1

---

## FIX-19: URL coverage gap (allowlist additions OR documentation)

- **File:** `data/policy/allowlist.yaml` (if adding domains) OR `docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md` (if documenting as known gap)
- **Location:** Various
- **Current text:** N/A (missing entries)
- **Replacement:** One of two options:
  - **Option A (Preferred): Add missing domains to allowlist.yaml.** Add to tier_1_age: `muface.es`, `imserso.es`, `ine.es`. Add to tier_2_ccaa under existing entries as aliases: `jccm.es` (under castillalamancha.es), `carm.es` / `sede.carm.es` (under murciaregion.es -- note: `carm.es` already added as alias). Add to tier_3_municipal: `seuelectronica.palma.cat` (under palma.es or as new entry), `seuelectronica.l-h.cat` (new entry for L'Hospitalet), `sede.coruna.gal` (new entry for A Coruna).
  - **Option B: Document as known gaps** by adding a "Known Coverage Gaps" section to Q1-REPORT.md listing the 9 domains and their status.
- **Linked drift:** DRIFT-19
- **Priority:** P1

---

## FIX-20: v3 ground-truth-counts.txt test count

- **File:** `docs/arreglos chat/fase-3/audits-v3/evidence/ground-truth-counts.txt`
- **Location:** line 36
- **Current text:** `  test_validators.py: 0 tests`
- **Replacement:** `  test_validators.py: 5 tests`
- **Linked drift:** DRIFT-20
- **Priority:** P1

---

## FIX-21: No single-line fix needed

- **File:** N/A
- **Location:** N/A
- **Current text:** N/A
- **Replacement:** N/A -- DRIFT-21 is a false positive in phantom-paths.txt. The `data/tramites/*.json` glob references 8 real files. No documentation change needed. The phantom-paths check should be updated to handle glob patterns.
- **Linked drift:** DRIFT-21
- **Priority:** P2 (informational only)

---

## FIX-22: No separate fix needed

- **File:** N/A
- **Location:** N/A
- **Current text:** N/A
- **Replacement:** N/A -- DRIFT-22 (cross-document false consistency) is resolved automatically when FIX-01 (Q1-REPORT line 14), FIX-07 (gates.md line 31), and FIX-08 (gates.md line 32) are applied.
- **Linked drift:** DRIFT-22
- **Priority:** P2 (meta-drift, auto-resolved)

---

## Application Priority

### Phase 1 -- P0 (Must Fix Immediately)

| Fix | File | Line | Impact |
|-----|------|------|--------|
| FIX-01 | Q1-REPORT.md | 14 | AGE P1/P2 split wrong -- top-level summary |
| FIX-05a | Q1.1-REPORT.md | 21 | Test count understated (3 vs 5) |
| FIX-05b | Q1.1-REPORT.md | 74 | Test count table understated (3/3 vs 5/5) |
| FIX-06a | Q1-REPORT.md | 107 | Phantom paths not marked as Q2 planned |

### Phase 2 -- P1 (Should Fix)

| Fix | File | Line | Impact |
|-----|------|------|--------|
| FIX-02 | Q1-REPORT.md | 74 | Municipal count wrong (12 vs 19) |
| FIX-03 | Q1.1-REPORT.md | 17 | Municipal count wrong (12 vs 19) |
| FIX-04 | Q1.1-REPORT.md | 48 | Allowlist line count wrong (319 vs 355) |
| FIX-13 | FORENSIC-AUDIT.md | 30 | Test count wrong in abort conditions |
| FIX-14 | FORENSIC-AUDIT.md | 84 | Municipal count wrong in Claims Ledger |
| FIX-17 | FORENSIC-AUDIT.md | 165 | "All resolved" misleading without caveat |
| FIX-18 | README.md (fase-3) | 76 | Test count wrong in landing page |
| FIX-19 | allowlist.yaml or Q1-REPORT.md | Various | URL coverage gap -- 9 domains |
| FIX-20 | ground-truth-counts.txt | 36 | Test count wrong in evidence file |

### Phase 3 -- P2 (Nice to Fix)

| Fix | File | Line | Impact |
|-----|------|------|--------|
| FIX-07 | gates.md | 31 | P1 count missing BOE Sumarios |
| FIX-08 | gates.md | 32 | P2 count label off by 1 |
| FIX-09 | gates.md | 55 | Blocklist category count off by 1 |
| FIX-10 | gates.md | 54 | Municipal count wrong (12 vs 19) |
| FIX-11 | gates.md | 138 | Pytest expected output stale |
| FIX-12 | gates.md | 147 | Abort condition test count stale |
| FIX-15 | FORENSIC-AUDIT.md | 106 | Gate Claims test count stale |
| FIX-16 | FORENSIC-AUDIT.md | 213 | Command comment test count stale |

### No Action Required

| Fix | Reason |
|-----|--------|
| FIX-21 | False positive in phantom-paths check -- no doc change needed |
| FIX-22 | Auto-resolved by FIX-01, FIX-07, FIX-08 |

---

## Verification Commands (Post-Fix)

After applying all replacements, run these to confirm consistency:

```bash
# Verify all ground-truth counts still hold
python3 scripts/validate_source_registry.py
python3 scripts/validate_policy.py
python3 scripts/validate_proceduredoc_schema.py \
  "docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"
pytest tests/unit/test_validators.py -v

# Grep for remaining stale values across all docs
grep -rn "10 P1" "docs/arreglos chat/fase-3/q1-sources/"
grep -rn "5 P2" "docs/arreglos chat/fase-3/q1-sources/"
grep -rn "12 municipal" "docs/arreglos chat/fase-3/"
grep -rn "12 seed" "docs/arreglos chat/fase-3/"
grep -rn "3 unit test" "docs/arreglos chat/fase-3/"
grep -rn "3/3 PASS" "docs/arreglos chat/fase-3/q1-sources/"
grep -rn "| 319 |" "docs/arreglos chat/fase-3/"
grep -rn "8 categories" "docs/arreglos chat/fase-3/q1-sources/"
grep -rn "0 tests" "docs/arreglos chat/fase-3/audits-v3/"
# Expected: Zero matches in source documents after all fixes applied
# (Audit reports referencing "claimed X" in their own text are acceptable)
```

---

*Generated by A3v4 (Drift & Consistency Reconciler), Anti-Hallucination Audit v4, 2026-02-18*
*Mode: READ-ONLY -- NO FILES MODIFIED. This is a plan document only.*
