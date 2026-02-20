# GATES-RESULTS.v6.md — Post-Fix Gate Verification

**Date:** 2026-02-19
**Branch:** fix/fase3-full-pass
**Commit:** deb42a9688cec73c820fbe4265845a370bc72600

---

## Gate Results

| Gate | Command | Result | Evidence |
|------|---------|--------|----------|
| G1 Registry | `python3 scripts/validate_source_registry.py` | **PASS** | 44 + 20 sources |
| G2 Policy | `python3 scripts/validate_policy.py` | **PASS** | allowlist + blocklist + canonical |
| G3 ProcedureDoc | `python3 scripts/validate_proceduredoc_schema.py "...proceduredoc.sample.json"` | **PASS** | completeness 0.86 |
| G4 Tests collected | `pytest tests/unit/test_validators.py --collect-only` | **PASS** | 5 tests |
| G5 Tests pass | `pytest tests/unit/test_validators.py -v` | **PASS** | 5/5, 0.59s |
| G6 Lint | `ruff check scripts/ tests/ --select E,F,W --ignore E501` | **PASS** | 0 errors |
| G7 Link checker | `python3 scripts/link_check.py --dry-run --limit 10` | **PASS** | 8 URLs |

**7/7 gates PASS**

---

## Gate Output (verbatim)

### G1: Registry Validation
```
=== Source Registry Validation ===
  registry.yaml: PASS (44 sources — AGE: 25, CCAA: 19, Local: 0)
  local_seed.yaml: PASS (20 sources — AGE: 0, CCAA: 0, Local: 20)
PASS: All source registry files valid.
```

### G2: Policy Validation
```
=== Policy Validation ===
  allowlist.yaml: PASS
  blocklist.yaml: PASS
  canonical_rules.yaml: PASS
PASS: All policy files valid.
```

### G3: ProcedureDoc Validation
```
PASS: proceduredoc.sample.json valid against ProcedureDoc v1
  id: age-inss-ingreso-minimo-vital
  nombre: Ingreso Minimo Vital
  completeness: 0.86
```

### G4+G5: Tests
```
tests/unit/test_validators.py::TestValidateSourceRegistry::test_validates PASSED [ 20%]
tests/unit/test_validators.py::TestValidatePolicy::test_validates PASSED [ 40%]
tests/unit/test_validators.py::TestValidateProcedureDoc::test_sample_validates PASSED [ 60%]
tests/unit/test_validators.py::TestValidateProcedureDoc::test_invalid_proceduredoc_rejected PASSED [ 80%]
tests/unit/test_validators.py::TestValidateProcedureDoc::test_missing_file_rejected PASSED [100%]
5 passed in 0.59s
```

### G6: Lint
```
All checks passed!
```

### G7: Link Checker (dry-run)
```
Link checker: 8 URLs (smoke=False, limit=10)
  [age-sia] https://administracion.gob.es/pag_Home/espanaAdmon/SIA.html
  [age-pag] https://administracion.gob.es/
  [age-pag] https://sede.administracion.gob.es/
  [age-carpeta-ciudadana] https://carpetaciudadana.gob.es/
  [age-clave] https://clave.gob.es/
  [age-boe-diario] https://www.boe.es/
  [age-boe-diario] https://boe.es/datosabiertos/api/boe/sumario/
  [age-boe-legislacion] https://www.boe.es/buscar/legislacion.php
Dry run complete. 8 URLs would be checked.
```

---

## URL Coverage (v6 formal scopes)

### Enforcement Scope (data files only)
- URLs: 125
- COVERED: 125 (100%)
- NOT_COVERED: 0
- **GOV COVERAGE: PASS**

### Docs+Data Scope (all md + data)
- URLs: 261 (256 analyzable after 5 template/artifact skips)
- COVERED: 249 (97.3%)
- NOT_COVERED: 7 (all non-gov: github.com, docs.ckan.org, json-schema.org, etc.)
- **GOV COVERAGE: PASS**

---

*Generated 2026-02-19 by Audit v6*
