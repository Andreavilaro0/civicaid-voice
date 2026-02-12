# Structured Outputs — Pipeline LLM de Clara

> **Resumen en una linea:** Los Structured Outputs anaden validacion JSON con schema Pydantic a las respuestas de Gemini, con fallback seguro si el parseo falla.

## Vision general

Los Structured Outputs anaden una capa opcional de validacion de schema JSON a las respuestas del LLM (Gemini Flash) de Clara. Cuando estan habilitados, el LLM devuelve un objeto `ClaraStructuredResponse` validado que luego se formatea en texto limpio para el usuario.

**Feature flag:** `STRUCTURED_OUTPUT_ON` (por defecto: `false` — impacto cero cuando esta desactivado)

## Arquitectura

```
Consulta usuario -> llm_generate (prompt + instruccion schema JSON)
                 -> Gemini Flash -> texto JSON bruto
                 -> verify_response (verificaciones basadas en reglas)
                 -> parse_structured_response -> ClaraStructuredResponse (Pydantic)
                 -> display_text (resumen formateado + pasos + docs + avisos)
                 -> send_final_message
```

Cuando la flag esta desactivada, el pipeline no cambia — `parse_structured_response` nunca se ejecuta.

## Schema: ClaraStructuredResponse

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| `intent` | string | si | Intencion del usuario: informacion, requisitos, pasos, documentos, otro |
| `language` | string | si | Idioma de respuesta: es, fr, en, ar |
| `tramite` | string\|null | no | Tramite: imv, empadronamiento, tarjeta_sanitaria |
| `summary` | string | si | Resumen breve de 1-2 frases |
| `steps` | list[string] | no | Pasos ordenados si aplica |
| `required_docs` | list[string] | no | Documentos requeridos |
| `warnings` | list[string] | no | Avisos o advertencias importantes |
| `sources` | list[string] | no | URLs de fuentes oficiales |
| `disclaimer` | string | no | Disclaimer legal (tiene valor por defecto) |

## Fallback seguro

Si el LLM devuelve JSON invalido o la respuesta no coincide con el schema, `parse_structured_response` retorna `(None, original_text)` — se usa el texto original sin estructura con cero interrupciones.

## Activacion

```bash
export STRUCTURED_OUTPUT_ON=true
```

O en `.env`:
```
STRUCTURED_OUTPUT_ON=true
```

## Archivos

| Archivo | Proposito |
|---------|-----------|
| `src/core/models_structured.py` | Modelo Pydantic + funcion de parseo |
| `src/core/config.py` | Flag `STRUCTURED_OUTPUT_ON` |
| `src/core/skills/llm_generate.py` | Inyeccion de schema JSON en el prompt |
| `src/core/pipeline.py` | Paso de parseo despues de verify |
| `tests/unit/test_structured_outputs.py` | 10 tests unitarios |
| `scripts/verify_structured.sh` | Script de verificacion |

## Tests

```bash
pytest tests/unit/test_structured_outputs.py -v
```

10 tests que cubren: validacion del modelo, valores por defecto, campos requeridos, parseo JSON, parseo de bloques de codigo markdown, fallback con JSON invalido, formateo de display y verificacion de flag por defecto.

## Referencias

- [Structured Outputs y Guardrails (guia completa)](../05-ops/STRUCTURED-OUTPUTS-GUARDRAILS.md)
- [Integracion del Toolkit](../02-architecture/TOOLKIT-INTEGRATION.md)
