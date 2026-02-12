# Guardrails — Safety Layer for Clara

## Overview

Clara includes a pre/post safety layer that protects users and ensures responsible AI behavior. Guardrails run **before** processing user input (pre-check) and **after** generating LLM output (post-check).

## Architecture

```
User Input -> [PRE-CHECK] -> Pipeline (cache/KB/LLM) -> [POST-CHECK] -> User
                 |                                           |
                 v                                           v
          Block harmful input                     Add disclaimers
          Return helpline info                    Redact PII
```

## Feature Flag

| Flag | Env Var | Default | Effect |
|------|---------|---------|--------|
| GUARDRAILS_ON | `GUARDRAILS_ON` | `true` | Enable/disable all guardrails |

When `GUARDRAILS_ON=false`, all checks are bypassed and input/output passes through unchanged.

## Pre-Check Rules

The pre-check runs on user input **before** any pipeline processing. If a blocked pattern is detected, the pipeline returns immediately with a safe response (helpline number, etc.).

| Category | Patterns | Response |
|----------|----------|----------|
| self_harm | suicid, matarme, hacerme dano, autolesion | Helpline 024 / 112 |
| violence | bomba, explosivo, arma, terroris | Emergency 112 |
| illegal | hackear, robar identidad, falsificar documento | Legal professional referral |

## Post-Check Rules

The post-check runs on LLM output **before** sending to the user.

### Legal/Medical Disclaimer
If the response mentions legal or medical terms (abogado, legal, medico, tratamiento, etc.), a disclaimer is appended:

> IMPORTANTE: Esta informacion es orientativa y no constituye asesoramiento legal ni medico. Consulte con un profesional cualificado o visite las fuentes oficiales para su caso concreto.

### PII Redaction
Sensitive data patterns are redacted from LLM output to prevent echoing back user PII:

| Pattern | Type | Replacement |
|---------|------|-------------|
| `\b\d{8}[A-Z]\b` | DNI | `[DNI REDACTADO]` |
| `\b[XYZ]\d{7}[A-Z]\b` | NIE | `[NIE REDACTADO]` |
| `\b\d{3}[-.]?\d{3}[-.]?\d{3}\b` | Phone | `[phone REDACTADO]` |

## How to Extend

### Adding a new blocked pattern
Edit `BLOCKED_PATTERNS` in `src/core/guardrails.py`:

```python
BLOCKED_PATTERNS = [
    ...
    (r'\bnew_pattern\b', 'category_name', 'Response message to user.'),
]
```

### Adding a new PII pattern
Edit `PII_PATTERNS` in `src/core/guardrails.py`:

```python
PII_PATTERNS = [
    ...
    (r'regex_pattern', 'PII_TYPE'),
]
```

## NeMo Guardrails (Future)

For production, consider integrating NVIDIA NeMo Guardrails for:
- Topical rails (keep conversation on-topic)
- Jailbreak detection
- Fact-checking rails
- Multi-turn conversation safety

The current regex-based approach is a lightweight MVP suitable for the hackathon demo, designed to be replaced by NeMo or similar frameworks in production.

## Testing

```bash
# Run guardrails unit tests
pytest tests/unit/test_guardrails.py -v

# Run full verification script
bash scripts/verify_guardrails.sh
```

## Files

| File | Purpose |
|------|---------|
| `src/core/guardrails.py` | Pre-check and post-check logic |
| `src/core/config.py` | `GUARDRAILS_ON` flag |
| `src/core/pipeline.py` | Integration points (pre/post) |
| `tests/unit/test_guardrails.py` | Unit tests (16 tests) |
| `scripts/verify_guardrails.sh` | Verification script |
