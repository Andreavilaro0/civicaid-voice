# Structured Outputs — Clara LLM Pipeline

## Overview

Structured outputs add optional JSON schema enforcement to Clara's Gemini LLM responses. When enabled, the LLM returns a validated `ClaraStructuredResponse` object that is then formatted into clean display text for the user.

**Feature flag:** `STRUCTURED_OUTPUT_ON` (default: `false` — zero impact when off)

## Architecture

```
User query -> llm_generate (prompt + JSON schema instruction)
           -> Gemini Flash -> raw JSON text
           -> verify_response (rules-based checks)
           -> parse_structured_response -> ClaraStructuredResponse (Pydantic)
           -> display_text (formatted summary + steps + docs + warnings)
           -> send_final_message
```

When the flag is off, the pipeline is unchanged — `parse_structured_response` is never called.

## Schema: ClaraStructuredResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `intent` | string | yes | User intent: informacion, requisitos, pasos, documentos, otro |
| `language` | string | yes | Response language: es, fr, en, ar |
| `tramite` | string\|null | no | Tramite: imv, empadronamiento, tarjeta_sanitaria |
| `summary` | string | yes | Brief 1-2 sentence answer |
| `steps` | list[string] | no | Ordered steps if applicable |
| `required_docs` | list[string] | no | Required documents |
| `warnings` | list[string] | no | Important warnings or caveats |
| `sources` | list[string] | no | Official source URLs |
| `disclaimer` | string | no | Legal disclaimer (has default) |

## Graceful Fallback

If the LLM returns invalid JSON or the response doesn't match the schema, `parse_structured_response` returns `(None, original_text)` — the original unstructured text is used with zero breakage.

## Enabling

```bash
export STRUCTURED_OUTPUT_ON=true
```

Or in `.env`:
```
STRUCTURED_OUTPUT_ON=true
```

## Files

| File | Purpose |
|------|---------|
| `src/core/models_structured.py` | Pydantic model + parse function |
| `src/core/config.py` | `STRUCTURED_OUTPUT_ON` flag |
| `src/core/skills/llm_generate.py` | JSON schema prompt injection |
| `src/core/pipeline.py` | Parse step after verify |
| `tests/unit/test_structured_outputs.py` | 10 unit tests |
| `scripts/verify_structured.sh` | Verification script |

## Tests

```bash
pytest tests/unit/test_structured_outputs.py -v
```

10 tests covering: model validation, defaults, required field enforcement, JSON parsing, markdown code block parsing, fallback on invalid JSON, display formatting, and flag default verification.
