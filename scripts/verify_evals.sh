#!/usr/bin/env bash
set -euo pipefail
echo "=== Evals Verification ==="
python3 -c "from src.utils.eval_runner import load_eval_cases; cases = load_eval_cases('data/evals'); total = sum(len(c) for c in cases.values()); print(f'OK: {len(cases)} eval sets, {total} total cases')"
python3 scripts/run_evals.py
pytest tests/unit/test_evals.py -q
echo "=== Evals: ALL CHECKS PASSED ==="
