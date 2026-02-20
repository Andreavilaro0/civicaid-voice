# GATES-RESULTS.final.md — Q1 Close-Out Gate Verification

**Date:** 2026-02-19
**Branch:** fix/fase3-full-pass
**Commit:** deb42a9688cec73c820fbe4265845a370bc72600
**Python:** 3.11.8

---

## Results

| Gate | Command | Exit | Result |
|------|---------|------|--------|
| G1 | `python3 scripts/validate_source_registry.py` | 0 | **PASS** (44 + 20 sources) |
| G2 | `python3 scripts/validate_policy.py` | 0 | **PASS** (allowlist + blocklist + canonical) |
| G3 | `python3 scripts/validate_proceduredoc_schema.py <sample>` | 0 | **PASS** (completeness 0.86) |
| G4 | `pytest tests/unit/test_validators.py --collect-only` | 0 | **PASS** (5 tests collected) |
| G5 | `pytest tests/unit/test_validators.py -v` | 0 | **PASS** (5/5, 0.60s) |
| G6 | `ruff check scripts/ tests/ --select E,F,W --ignore E501` | 0 | **PASS** (0 errors) |
| G7 | `python3 scripts/link_check.py --dry-run --limit 10` | 0 | **PASS** (8 URLs, dry-run) |

**7/7 gates PASS** (all exit code 0)

---

## Verbatim Output

See `COMMANDS-AND-OUTPUTS.log` in this directory for full gate execution output with timestamps.

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

### G3: ProcedureDoc
```
PASS: proceduredoc.sample.json valid against ProcedureDoc v1
  id: age-inss-ingreso-minimo-vital
  nombre: Ingreso Minimo Vital
  completeness: 0.86
```

### G4+G5: Tests
```
tests/unit/test_validators.py::TestValidateSourceRegistry::test_validates PASSED
tests/unit/test_validators.py::TestValidatePolicy::test_validates PASSED
tests/unit/test_validators.py::TestValidateProcedureDoc::test_sample_validates PASSED
tests/unit/test_validators.py::TestValidateProcedureDoc::test_invalid_proceduredoc_rejected PASSED
tests/unit/test_validators.py::TestValidateProcedureDoc::test_missing_file_rejected PASSED
5 passed in 0.60s
```

### G6: Lint
```
All checks passed!
```

### G7: Link Checker
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

*Generated 2026-02-19 by Q1 Final Close-Out audit*
