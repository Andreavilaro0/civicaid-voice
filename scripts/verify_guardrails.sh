#!/usr/bin/env bash
set -euo pipefail
echo "=== Guardrails Verification ==="
echo "1. Checking guardrails module..."
python3 -c "from src.core.guardrails import pre_check, post_check, GuardrailResult; print('OK: guardrails imports')"
echo "2. Checking pre_check blocks dangerous input..."
python3 -c "
from src.core.guardrails import pre_check
result = pre_check('quiero hacerme daño')
assert not result.safe, 'Should be blocked'
assert result.reason == 'self_harm'
assert '024' in result.modified_text
print(f'OK: blocked self_harm, response includes helpline')
"
echo "3. Checking pre_check allows safe input..."
python3 -c "
from src.core.guardrails import pre_check
result = pre_check('Que es el IMV?')
assert result.safe, 'Should be safe'
print('OK: safe input passes')
"
echo "4. Checking post_check adds disclaimer..."
python3 -c "
from src.core.guardrails import post_check
result = post_check('Deberias consultar un abogado para esto.')
assert 'IMPORTANTE' in result
assert 'asesoramiento legal' in result
print('OK: legal disclaimer added')
"
echo "5. Checking post_check redacts PII..."
python3 -c "
from src.core.guardrails import post_check
result = post_check('Tu DNI es 12345678A y tu NIE es X1234567B')
assert '12345678A' not in result
assert 'X1234567B' not in result
assert 'REDACTADO' in result
print('OK: PII redacted')
"
echo "6. Running tests..."
pytest tests/ -q
echo "=== Guardrails: ALL CHECKS PASSED ==="
