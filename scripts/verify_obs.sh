#!/usr/bin/env bash
set -euo pipefail
echo "=== Observability Verification ==="
echo "1. Checking observability module..."
python3 -c "from src.utils.observability import RequestContext, get_context, set_context; print('OK: observability module imports')"
echo "2. Checking request_id generation..."
python3 -c "
from src.utils.observability import RequestContext
ctx = RequestContext()
assert len(ctx.request_id) == 36, 'UUID length wrong'
print(f'OK: request_id={ctx.request_id}')
"
echo "3. Checking timing tracking..."
python3 -c "
from src.utils.observability import RequestContext
ctx = RequestContext()
ctx.add_timing('cache', 50)
ctx.add_timing('llm', 200)
assert ctx.timings == {'cache': 50, 'llm': 200}
print(f'OK: timings={ctx.timings}')
"
echo "4. Running tests..."
pytest tests/ -q
echo "=== Observability: ALL CHECKS PASSED ==="
