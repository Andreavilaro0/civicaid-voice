# Eval Framework

## Overview

Automated evaluation suite for Clara's response quality. Tests cache responses and KB lookups against expected content patterns.

## Structure

```
data/evals/
  imv_evals.json              # 5 cases — IMV queries
  empadronamiento_evals.json  # 5 cases — empadronamiento queries
  tarjeta_evals.json          # 3 cases — tarjeta sanitaria queries
  safety_evals.json           # 3 cases — safety/off-topic queries

src/utils/eval_runner.py      # Eval engine (load, run, report)
scripts/run_evals.py          # CLI runner
tests/unit/test_evals.py      # Unit tests for eval framework
```

## Eval Case Format

```json
{
  "id": "imv_01",
  "query": "Que es el IMV?",
  "language": "es",
  "expected_contains": ["IMV", "Ingreso Minimo"],
  "expected_not_contains": ["empadronamiento"],
  "expected_tramite": "imv"
}
```

- `expected_contains`: case-insensitive substrings that MUST appear in the response
- `expected_not_contains`: case-insensitive substrings that MUST NOT appear
- `expected_tramite`: metadata for classification (not checked by runner)

## Running Evals

```bash
# Run eval suite
python3 scripts/run_evals.py

# Run eval unit tests
pytest tests/unit/test_evals.py -v
```

## Scoring

- Each case gets a score from 0.0 to 1.0 based on checks passed / total checks
- A case passes only if ALL checks pass (score = 1.0)
- Reports show per-set and overall pass rates
