# A3v3 — Fix Plan (Exact Text Replacements)

**Date:** 2026-02-18
**Auditor:** A3 (Drift & Consistency Reconciler), Anti-Hallucination Audit v3
**Mode:** READ-ONLY -- NO FILES MODIFIED
**Status:** Plan only. Each replacement below is documented but NOT applied.

---

## Instructions

For each drift, the `Old` text is the exact string to find in the file, and `New` is the exact replacement. All file paths are relative to repository root: `/Users/andreaavila/Documents/hakaton/civicaid-voice`.

---

```
DRIFT-01:
  File: docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md
  Line: 14
  Old: "- **25 AGE sources** documented (10 P0, 10 P1, 5 P2) including BOE API, SIA/PAG master catalog, and all critical sedes electronicas"
  New: "- **25 AGE sources** documented (10 P0, 11 P1, 4 P2) including BOE API, SIA/PAG master catalog, and all critical sedes electronicas"
  Evidence: python3 -c "import yaml; r=yaml.safe_load(open('data/sources/registry.yaml')); age=[s for s in r['sources'] if s['jurisdiction']=='age']; print({p: len([s for s in age if s['priority']==p]) for p in ['P0','P1','P2']})" => {'P0': 10, 'P1': 11, 'P2': 4}
```

```
DRIFT-02:
  File: docs/arreglos chat/fase-3/q1-sources/Q1-REPORT.md
  Line: 74
  Old: "- **Tier 3 (Municipal):** 12 seed cities, on-demand expansion"
  New: "- **Tier 3 (Municipal):** 19 seed cities, on-demand expansion"
  Evidence: python3 -c "import yaml; a=yaml.safe_load(open('data/policy/allowlist.yaml')); print(len(a['tier_3_municipal']['domains']))" => 19
```

```
DRIFT-03:
  File: docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md
  Line: 17
  Old: "3. **Domain governance** enforced: allowlist (22 AGE + 19 CCAA + 12 municipal domains), blocklist (23 domains + 4 patterns), 12-step URL canonicalization pipeline (applying 10 named rules)"
  New: "3. **Domain governance** enforced: allowlist (22 AGE + 19 CCAA + 19 municipal domains), blocklist (23 domains + 4 patterns), 12-step URL canonicalization pipeline (applying 10 named rules)"
  Evidence: Same as DRIFT-02
```

```
DRIFT-04:
  File: docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md
  Line: 48
  Old: "| `data/policy/allowlist.yaml` | 319 | 3-tier domain allowlist |"
  New: "| `data/policy/allowlist.yaml` | 355 | 3-tier domain allowlist |"
  Evidence: wc -l data/policy/allowlist.yaml => 355
```

```
DRIFT-05a:
  File: docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md
  Line: 21
  Old: "7. **3 unit tests** covering all validators pass in CI-compatible pytest"
  New: "7. **5 unit tests** covering all validators pass in CI-compatible pytest"
  Evidence: pytest tests/unit/test_validators.py -v => 5 passed
```

```
DRIFT-05b:
  File: docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md
  Line: 74
  Old: "| `tests/unit/test_validators.py` | 3 | 3/3 PASS |"
  New: "| `tests/unit/test_validators.py` | 5 | 5/5 PASS |"
  Evidence: pytest tests/unit/test_validators.py -v => 5 passed
```

```
DRIFT-06:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/gates.md
  Line: 32
  Old: "- **P2 sources:** 5 (MUFACE, INE, Catastro, Transparencia)"
  New: "- **P2 sources:** 4 (MUFACE, INE, Catastro, Transparencia)"
  Evidence: python3 -c "import yaml; r=yaml.safe_load(open('data/sources/registry.yaml')); age=[s for s in r['sources'] if s['jurisdiction']=='age']; print(len([s for s in age if s['priority']=='P2']))" => 4
```

```
DRIFT-07:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/gates.md
  Line: 31
  Old: "- **P1 sources:** 10 (Carpeta Ciudadana, Clave, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)"
  New: "- **P1 sources:** 11 (Carpeta Ciudadana, Clave, BOE Sumarios, DGT, IMSERSO, MIVAU, Min. Justicia, Asilo, Registro Civil, datos.gob.es, Import@ss)"
  Evidence: python3 -c "import yaml; r=yaml.safe_load(open('data/sources/registry.yaml')); age=[s for s in r['sources'] if s['jurisdiction']=='age' and s['priority']=='P1']; print([s['id'] for s in age])" => includes 'age-boe-sumarios'
```

```
DRIFT-08:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/gates.md
  Line: 138
  Old: "# Output: 3 passed"
  New: "# Output: 5 passed"
  Evidence: pytest tests/unit/test_validators.py -v => 5 passed in 0.67s
```

```
DRIFT-09:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/gates.md
  Line: 55
  Old: "- **Blocklist:** 8 categories explicitly blocked (commercial, SEO, forums, social media, etc.)"
  New: "- **Blocklist:** 9 categories explicitly blocked (commercial, SEO, forums, social media, ai_generated, etc.)"
  Evidence: python3 -c "import yaml; b=yaml.safe_load(open('data/policy/blocklist.yaml')); print(len(b['categories']))" => 9
```

```
DRIFT-10:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/gates.md
  Line: 54
  Old: "- **Tier 3 (Municipal):** 12 initial seed cities"
  New: "- **Tier 3 (Municipal):** 19 initial seed cities"
  Evidence: Same as DRIFT-02
```

```
DRIFT-11:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md
  Line: 30
  Old: "| A5: \"Gates PASS\" not reproducible | **NOT TRIGGERED** | All 4 scripts pass, 3/3 tests pass |"
  New: "| A5: \"Gates PASS\" not reproducible | **NOT TRIGGERED** | All 4 scripts pass, 5/5 tests pass |"
  Evidence: pytest tests/unit/test_validators.py -v => 5 passed
```

```
DRIFT-12:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md
  Line: 84
  Old: "| Allowlist tier_3_municipal domains | 12 | **12** | VERIFIED | `validate_policy.py` |"
  New: "| Allowlist tier_3_municipal domains | 19 | **19** | VERIFIED | `validate_policy.py` |"
  Evidence: python3 -c "import yaml; a=yaml.safe_load(open('data/policy/allowlist.yaml')); print(len(a['tier_3_municipal']['domains']))" => 19
```

```
DRIFT-13:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md
  Line: 106
  Old: "| Unit tests | 3/3 PASS | **3/3 PASS** | VERIFIED | pytest exit 0 |"
  New: "| Unit tests | 5/5 PASS | **5/5 PASS** | VERIFIED | pytest exit 0 |"
  Evidence: pytest tests/unit/test_validators.py -v => 5 passed
```

```
DRIFT-14:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md
  Line: 213
  Old: "pytest tests/unit/test_validators.py -v                # 3/3 PASS"
  New: "pytest tests/unit/test_validators.py -v                # 5/5 PASS"
  Evidence: pytest tests/unit/test_validators.py -v => 5 passed
```

```
DRIFT-15:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/Q1.1-FORENSIC-AUDIT-REPORT.md
  Line: 165
  Old: "All 10 audit findings have been resolved. Gates re-verified: 5/5 PASS."
  New: "All 10 audit findings have been resolved (data/code layer). Gates re-verified: 5/5 PASS. NOTE: Report documents (Q1-REPORT.md, Q1.1-REPORT.md, gates.md) were NOT updated with post-fix numeric values — see A3v3 drift audit."
  Evidence: 14+ stale numeric claims remain in Q1-REPORT.md, Q1.1-REPORT.md, gates.md, and this file. See /tmp/a3v3-drifts.md.
```

```
DRIFT-16:
  File: docs/arreglos chat/fase-3/audits-v3/evidence/ground-truth-counts.txt
  Line: 36
  Old: "  test_validators.py: 0 tests"
  New: "  test_validators.py: 5 tests"
  Evidence: pytest tests/unit/test_validators.py -v => collected 5 items, 5 passed. Also confirmed by g5-pytest.txt in same evidence directory showing "collected 5 items."
```

```
DRIFT-17:
  File: docs/arreglos chat/fase-3/q1-sources/evidence/gates.md
  Line: 30
  Old: "- **P0 sources:** 10 (SIA, PAG, Sede PAG, BOE x3, SEPE, Seg Social, AEAT, Extranjeria, IMV)"
  New: "- **P0 sources:** 10 (SIA, PAG, Sede PAG, BOE Diario, BOE Legislacion, SEPE, Seg Social, AEAT, Extranjeria, IMV)"
  Evidence: registry.yaml shows age-boe-diario=P0, age-boe-legislacion=P0, age-boe-sumarios=P1. "BOE x3" misleadingly implies 3 BOE sources at P0 when only 2 are P0.
```

```
DRIFT-18:
  No single-line fix. This is a cross-document consistency issue.
  Resolution: Fixing DRIFT-01 (Q1-REPORT line 14) and DRIFT-06/DRIFT-07 (gates.md lines 31-32) eliminates the false mutual consistency. No additional replacement needed beyond DRIFT-01, DRIFT-06, and DRIFT-07.
```

---

## Application Priority

### Phase 1 — P0 (Must Fix Immediately)
| Fix | File | Impact |
|-----|------|--------|
| DRIFT-15 | FORENSIC-AUDIT line 165 | Behavioral drift: "all resolved" is misleading |

### Phase 2 — P1 (Should Fix)
| Fix | File | Impact |
|-----|------|--------|
| DRIFT-01 | Q1-REPORT line 14 | AGE P1/P2 split wrong |
| DRIFT-02 | Q1-REPORT line 74 | Municipal count wrong |
| DRIFT-03 | Q1.1-REPORT line 17 | Municipal count wrong |
| DRIFT-04 | Q1.1-REPORT line 48 | Allowlist line count wrong |
| DRIFT-05a | Q1.1-REPORT line 21 | Test count wrong |
| DRIFT-05b | Q1.1-REPORT line 74 | Test count wrong |
| DRIFT-11 | FORENSIC-AUDIT line 30 | Test count wrong |
| DRIFT-12 | FORENSIC-AUDIT line 84 | Municipal count wrong |
| DRIFT-16 | ground-truth-counts.txt line 36 | Test count wrong |

### Phase 3 — P2 (Nice to Fix)
| Fix | File | Impact |
|-----|------|--------|
| DRIFT-06 | gates.md line 32 | P2 count label off by 1 |
| DRIFT-07 | gates.md line 31 | P1 count missing BOE Sumarios |
| DRIFT-08 | gates.md line 138 | Pytest expected output stale |
| DRIFT-09 | gates.md line 55 | Blocklist category count off by 1 |
| DRIFT-10 | gates.md line 54 | Municipal count wrong |
| DRIFT-13 | FORENSIC-AUDIT line 106 | Test count wrong |
| DRIFT-14 | FORENSIC-AUDIT line 213 | Test count wrong |
| DRIFT-17 | gates.md line 30 | BOE x3 shorthand misleading |

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
grep -rn "10 P1" "docs/arreglos chat/fase-3/"
grep -rn "5 P2" "docs/arreglos chat/fase-3/"
grep -rn "12 municipal" "docs/arreglos chat/fase-3/"
grep -rn "12 seed" "docs/arreglos chat/fase-3/"
grep -rn "3 unit test" "docs/arreglos chat/fase-3/"
grep -rn "3/3 PASS" "docs/arreglos chat/fase-3/"
grep -rn "| 319 |" "docs/arreglos chat/fase-3/"
grep -rn "8 categories" "docs/arreglos chat/fase-3/"
grep -rn "0 tests" "docs/arreglos chat/fase-3/"
```

---

*Generated by A3v3 (Drift & Consistency Reconciler), 2026-02-18*
*Mode: READ-ONLY -- NO FILES MODIFIED. This is a plan document only.*
