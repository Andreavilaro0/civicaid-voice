# Gates Results (Post-Fix)
Date: 2026-02-19

| Gate | Command | Exit Code | Result | Evidence |
|------|---------|-----------|--------|----------|
| G1 | `validate_source_registry.py` | 0 | PASS | evidence/validate-registry.txt |
| G2 | `validate_policy.py` | 0 | PASS | evidence/validate-policy.txt |
| G3 | `validate_proceduredoc_schema.py proceduredoc.sample.json` | 0 | PASS | evidence/validate-proceduredoc.txt |
| G4 | `pytest tests/unit/test_validators.py --collect-only` | 0 | PASS (5 collected) | evidence/pytest-collect-only.txt |
| G5 | `pytest tests/unit/test_validators.py -v` | 0 | PASS (5/5 passed) | evidence/pytest-run.txt |
| G6 | `ruff check scripts/ tests/ --select E,F,W --ignore E501` | 0 | PASS | evidence/ruff.txt |
| G7 | `link_check.py --dry-run --limit 10` | 0 | PASS (8 URLs) | evidence/link-check-dry.txt |
| G2-post | `validate_policy.py` (re-run after allowlist update) | 0 | PASS | evidence/validate-policy-post.txt |

**Summary: 7/7 gates PASS** (plus post-fix policy re-validation also PASS)

## Details

### G1 — Source Registry Validation
- `registry.yaml`: 44 sources (AGE: 25, CCAA: 19, Local: 0)
- `local_seed.yaml`: 20 sources (AGE: 0, CCAA: 0, Local: 20)

### G2 — Policy Validation
- `allowlist.yaml`: PASS
- `blocklist.yaml`: PASS
- `canonical_rules.yaml`: PASS

### G3 — ProcedureDoc Schema Validation
- Sample: `proceduredoc.sample.json`
- id: `age-inss-ingreso-minimo-vital`
- nombre: Ingreso Minimo Vital
- completeness: 0.86

### G4 — Pytest Collection
- 5 tests collected in `test_validators.py`
- Classes: TestValidateSourceRegistry, TestValidatePolicy, TestValidateProcedureDoc

### G5 — Pytest Execution
- 5/5 tests passed in 0.89s
- All validator tests green

### G6 — Ruff Lint
- Zero errors/warnings on `scripts/` and `tests/`

### G7 — Link Check (Dry Run)
- 8 URLs identified across registries
- All from `.gob.es` / `.boe.es` domains

### G2-post — Policy Re-Validation
- Re-run 30s after initial gates to capture any allowlist updates by A3
- All 3 policy files still PASS
