#!/usr/bin/env bash
set -euo pipefail
echo "=== Structured Outputs Verification ==="
echo "1. Checking pydantic import..."
python3 -c "from pydantic import BaseModel; print('OK: pydantic available')"
echo "2. Checking structured model..."
python3 -c "from src.core.models_structured import ClaraStructuredResponse; print('OK: ClaraStructuredResponse imports')"
echo "3. Checking parse function..."
python3 -c "
from src.core.models_structured import parse_structured_response
import json
test_json = json.dumps({'intent':'informacion','language':'es','tramite':'imv','summary':'El IMV es una ayuda.','steps':['Paso 1'],'required_docs':['DNI'],'warnings':[],'sources':['https://seg-social.es'],'disclaimer':'Orientativo.'})
parsed, display = parse_structured_response(test_json)
assert parsed is not None, 'Parse failed'
assert parsed.tramite == 'imv'
print(f'OK: parsed tramite={parsed.tramite}')
"
echo "4. Checking fallback on bad JSON..."
python3 -c "
from src.core.models_structured import parse_structured_response
parsed, display = parse_structured_response('This is not JSON at all')
assert parsed is None, 'Should have failed'
assert display == 'This is not JSON at all', 'Should return original text'
print('OK: fallback works')
"
echo "5. Running tests..."
pytest tests/ -q
echo "=== Structured Outputs: ALL CHECKS PASSED ==="
