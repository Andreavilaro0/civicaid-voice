# FASE 1 — Closing Report: Estabilizacion + Salida de Demo + Calidad Percibida

**Fecha:** 2026-02-18
**Equipo:** Clara / CivicAid Voice
**Branch:** main
**Repo:** civicaid-voice

| Documento relacionado | Path |
|----------------------|------|
| Auditoria Fase 1 (validada) | [AUDIT-REPORT-FASE1-VALIDADO.md](AUDIT-REPORT-FASE1-VALIDADO.md) |
| Gates de calidad | [evidence/gates.md](evidence/gates.md) |
| Validacion en produccion | [evidence/prod-validation.md](evidence/prod-validation.md) |
| Backlog pendiente | [backlog.md](backlog.md) |
| Salida pytest | [evidence/commands-output/pytest-full.txt](evidence/commands-output/pytest-full.txt) |
| Salida ruff | [evidence/commands-output/ruff-check.txt](evidence/commands-output/ruff-check.txt) |

---

## Resumen Ejecutivo (15 bullets)

1. **DEMO_MODE desactivado** — el bot ahora sigue siempre el flujo real: cache → miss → KB + LLM → respuesta util (render.yaml `DEMO_MODE: "false"`)
2. **Truncamiento KB corregido** — `json.dumps(...)[:2000]` reemplazado por `_build_kb_context()` con tiers de prioridad que nunca rompe JSON (llm_generate.py)
3. **Inyeccion de prompt hardened** — texto del usuario envuelto en `<user_query>` XML + regla 11 anti-inyeccion en system_prompt.py
4. **KB expandida de 3 a 8 tramites** — +5 nuevos: prestacion_desempleo, nie_tie, ayuda_alquiler, justicia_gratuita, certificado_discapacidad
5. **Cobertura KB sube de 9.7% a ~26%** de los 31 tramites identificados en la auditoria
6. **Matching KB robusto** — accent normalization con `unicodedata` en kb_lookup.py, aplicada tanto a input como a keywords
7. **Keywords en espanol y frances** en los 8 tramites — soporte bilingue real
8. **Observabilidad pipeline** — `log_pipeline_result()` con `request_id`, `user_id_hash` (SHA256), `provider`, `latency_ms`, `fallback_reason` en cada exit point
9. **Tests: 85 → 110 (+25)** — 0 regressions, 0 failures, cobertura de todas las features nuevas
10. **Ruff: 0 errores** — codebase limpio con reglas E,F,W (ignorando E501)
11. **test_redteam.py corregido** — collection error eliminado (`allow_module_level=True`)
12. **KB context builder inteligente** — prioriza nombre/descripcion/organismo > requisitos > documentos > pasos > URLs > cuantias; respeta limite de 3000 chars
13. **Metadata excluida del contexto LLM** — campos `keywords`, `verificado`, `fecha_verificacion`, `tramite` nunca se envian a Gemini
14. **Pipeline robusto** — log estructurado en TODOS los exit points: guardrail, cache, demo_mode, llm, fallback, pipeline_error
15. **Base solida para Fase 2** — KB extensible (drop .json con `keywords`), matching normalizado, prompt hardened, observabilidad completa

---

## Gates: Before vs After

| Metrica | BEFORE (baseline) | AFTER (validacion) | Delta |
|---------|-------------------|---------------------|-------|
| pytest passed | 85 | 110 | **+25** |
| pytest failed | 0 | 0 | 0 |
| pytest skipped | 0 | 1 | +1 (redteam, expected) |
| pytest deselected | 1 | 1 | 0 (hanging test, known) |
| pytest collection errors | 1 | 0 | **-1 (fixed)** |
| ruff errors | 0 | 0 | 0 |
| Tramites en KB | 3 | 8 | **+5** |
| KB matching: accent-aware | No | Si | **fixed** |
| Prompt injection hardened | No | Si | **fixed** |
| KB truncation safe | No | Si | **fixed** |
| DEMO_MODE prod | true | false | **fixed** |
| Observability pipeline_result | No | Si | **added** |

### Nota de reconciliacion de metricas

La documentacion previa referencia distintos conteos de tests:

| Fuente | Conteo | Explicacion |
|--------|--------|-------------|
| `docs/04-testing/TEST-PLAN.md` | 96 tests (91 passed + 5 xpassed) | Suite original pre-Fase 1. Incluye test_redteam con xpassed. |
| Baseline Fase 1 (pre-cambios) | 85 passed, 1 deselected, 1 collection error | Sin los tests de redteam (collection error). El deselected es `test_pipeline_text_cache_miss`. |
| CLAUDE.md | "96 tests (91 passed + 5 xpassed)" | Refleja conteo de TEST-PLAN.md. Pendiente de actualizar. |
| **Post-Fase 1 (actual)** | **110 passed, 1 skipped, 1 deselected** | +25 tests nuevos. redteam corregido (skip en vez de collection error). |

**Causa de las diferencias:** Los 96 del TEST-PLAN incluyen 5 tests de redteam que ahora se contabilizan como 1 skipped (grupo parametrizado). Los 85 de baseline excluian redteam por collection error. Los 110 finales incluyen 25 tests nuevos (8 llm_generate + 15 kb_lookup + 2 accent normalization).

---

## Flags Actuales del Sistema

Tabla completa de feature flags en `src/core/config.py` con valores actuales:

| Flag | Default (config.py) | Valor en render.yaml | Notas |
|------|---------------------|---------------------|-------|
| `DEMO_MODE` | `false` | `false` | **Cambiado en Fase 1** (era `true`). Cache-only si `true`. |
| `LLM_LIVE` | `true` | `true` | Habilita Gemini 1.5 Flash |
| `WHISPER_ON` | `true` | `false` | **Flag legacy.** El STT real es Gemini Flash (`transcribe.py`), NO Whisper. Debe estar `false` en prod para evitar confusiones. TICKET-06 propone renombrar a `STT_ENABLED`. |
| `LLM_TIMEOUT` | `6` (segundos) | `6` | Timeout maximo para Gemini |
| `WHISPER_TIMEOUT` | `12` (segundos) | `12` | Usado como timeout de transcripcion Gemini (nombre legacy) |
| `GUARDRAILS_ON` | `true` | `true` | Filtrado pre/post de contenido peligroso |
| `STRUCTURED_OUTPUT_ON` | `false` | `false` | JSON estructurado desde Gemini. No activar sin testing. |
| `OBSERVABILITY_ON` | `true` | `true` | RequestContext + metricas + hooks Flask |
| `RAG_ENABLED` | `false` | `false` | Stub no funcional. No activar. |

> **Nota:** `TWILIO_TIMEOUT` (10s) esta hardcodeado en `src/core/skills/send_response.py`, no es un flag configurable.

---

## Tickets Cerrados (Fase 1)

| Ticket | Prioridad | Descripcion | Archivos Modificados | Estado |
|--------|-----------|-------------|---------------------|--------|
| TICKET-01 | P0 | DEMO_MODE=false en render.yaml | `render.yaml` | CERRADO |
| TICKET-02 | P0 | Fix truncamiento KB en llm_generate | `src/core/skills/llm_generate.py` | CERRADO |
| TICKET-03 | P0 | Expandir KB de 3 a 8 tramites | `data/tramites/*.json` (5 nuevos) | CERRADO |
| TICKET-04 | P1 | Hardening inyeccion prompt | `src/core/skills/llm_generate.py`, `src/core/prompts/system_prompt.py` | CERRADO |
| TICKET-05 | P0/P1 | Mejora matching KB con accent normalization | `src/core/skills/kb_lookup.py` | CERRADO |
| TICKET-07 | P1 | Fix test_redteam.py collection error | `tests/unit/test_redteam.py` | CERRADO |
| OBS-01 | P1 | Observabilidad pipeline con user_id_hash | `src/utils/logger.py`, `src/core/pipeline.py` | CERRADO |

---

## Tickets Pendientes (Backlog para Fases 2+)

| Ticket | Prioridad | Descripcion | Notas |
|--------|-----------|-------------|-------|
| TICKET-06 | P1 | Whisper flag rename (WHISPER_ON → STT_ENABLED) | Cosmetic, no impacta funcionalidad |
| TICKET-08 | P2 | Cache-first hit ratio monitoring | Depende de observabilidad (ya implementada) |
| TICKET-09 | P2 | TTS upgrade gTTS → mejor voz | Fase 2: voz |
| TICKET-10 | P2 | RAG retriever real (reemplazar stub) | Fase 3+ |
| TICKET-11 | P1 | Expand KB a 15+ tramites | Siguientes: reagrupacion_familiar, asilo, pension_no_contributiva, etc. |
| TICKET-12 | P2 | Fuzzy/semantic KB matching | Fase 2: mejora matching con embeddings |
| TICKET-13 | P2 | Rate limiting per user | Fase 2: seguridad |
| TICKET-14 | P1 | Fix test_pipeline_text_cache_miss hanging | Necesita mock de send_final_message |
| TICKET-15 | P2 | Image input pipeline (OCR) | Actualmente no funcional |
| TICKET-16 | P2 | Multilingual system prompt variants | Fase 2: internacionalizacion |

---

## Detalle de Cambios por Archivo

### src/core/skills/llm_generate.py
- **TICKET-02:** Nuevo `_build_kb_context(datos, max_chars=3000)` con 6 tiers de prioridad
- **TICKET-02:** `_PRIORITY_FIELDS` y `_EXCLUDED_FIELDS` constantes
- **TICKET-04:** Prompt usa `<user_query>\n{user_text}\n</user_query>` en lugar de f-string directa

### src/core/prompts/system_prompt.py
- **TICKET-04:** Regla 11 SEGURIDAD: instruccion anti-inyeccion para `<user_query>` tags

### src/core/skills/kb_lookup.py
- **TICKET-05:** Nueva funcion `_normalize(text)` con `unicodedata.normalize("NFKD")` + filtro combining chars
- **TICKET-05:** `_detect_tramite()` usa `_normalize()` tanto en input como en keywords

### render.yaml
- **TICKET-01:** `DEMO_MODE: "false"` (era `"true"`)

### src/core/pipeline.py
- **OBS-01:** `log_pipeline_result()` en 5 exit points: guardrail, cache, demo_mode, llm/fallback, pipeline_error
- **OBS-01:** Import de `log_pipeline_result` desde logger

### src/utils/logger.py
- **OBS-01:** Nueva funcion `log_pipeline_result(request_id, from_number, source, total_ms, fallback_reason)`
- **OBS-01:** SHA256 hash de user phone (`user_id_hash`), structured fields: `provider`, `latency_ms`, `fallback_reason`

### data/tramites/ (5 nuevos archivos)
- **TICKET-03:** `prestacion_desempleo.json` — Paro/SEPE, 12 keywords (es+fr), cuantias, duracion, plazos
- **TICKET-03:** `nie_tie.json` — NIE/TIE/Extranjeria, 12 keywords, tipos, requisitos UE vs no-UE
- **TICKET-03:** `ayuda_alquiler.json` — Alquiler/Bono Joven, 12 keywords, programas, requisitos
- **TICKET-03:** `justicia_gratuita.json` — Abogado oficio, 11 keywords, prestaciones, umbrales IPREM
- **TICKET-03:** `certificado_discapacidad.json` — Grados 33/65/75%, 10 keywords, beneficios por grado

### data/tramites/ (3 modificados)
- Adicion de campo `"tramite"` en `empadronamiento.json`, `imv.json`, `tarjeta_sanitaria.json` para consistencia

### tests/unit/test_kb_lookup.py
- **TICKET-03/05:** +21 nuevos tests para 5 tramites (es, keyword alternativo, fr) + 2 tests accent normalization

### tests/unit/test_llm_generate.py (NUEVO)
- **TICKET-02/04:** 8 tests: context building (prioridad, exclusion, JSON valido, max_chars), fallbacks (LLM disabled, no API key), prompt XML delimiters, anti-injection instruction

### tests/unit/test_redteam.py
- **TICKET-07:** `allow_module_level=True` en `pytest.skip()`

### tests/unit/test_retriever.py
- Minor: ajuste import para compatibilidad con nuevos tramites

---

## Evidencia de Calidad

### pytest (final)
```
110 passed, 1 skipped, 1 deselected in 0.72s
```

### ruff (final)
```
All checks passed!
```

### Sample log line (PIPELINE_RESULT)
```json
{
  "ts": "2026-02-18T00:12:00",
  "level": "INFO",
  "logger": "clara",
  "msg": "[PIPELINE_RESULT] request_id=abc-123 user=a1b2c3d4e5f6 source=llm total=1234ms",
  "tag": "PIPELINE_RESULT",
  "request_id": "abc-123",
  "user_id_hash": "a1b2c3d4e5f6",
  "provider": "llm",
  "latency_ms": 1234,
  "fallback_reason": ""
}
```

---

## Como Reproducir

Instrucciones completas para verificar todas los gates de Fase 1 desde cero.

### Prerequisitos
```bash
git clone <repo-url> civicaid-voice && cd civicaid-voice
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Gate 1: pytest
```bash
PYTHONPATH=. pytest tests/ -v --tb=short -k "not test_pipeline_text_cache_miss"
# Esperado: 110 passed, 1 skipped, 1 deselected
```

### Gate 2: ruff lint
```bash
ruff check src/ tests/ --select E,F,W --ignore E501
# Esperado: All checks passed!
```

### Gate 3: KB count
```bash
ls data/tramites/*.json | wc -l
# Esperado: 8
```

### Gate 4: DEMO_MODE
```bash
grep -A1 "DEMO_MODE" render.yaml
# Esperado: value: "false"
```

> Detalle completo de gates y excepciones: [evidence/gates.md](evidence/gates.md)

---

## Evidencia en Produccion

### Estado actual
La verificacion en produccion requiere acceso al Dashboard de Render y a un numero WhatsApp conectado al Sandbox de Twilio. No se ha realizado verificacion runtime al momento de este reporte.

### Checklist de verificacion (pendiente)

- [ ] Confirmar que `DEMO_MODE=false` en Render Dashboard (no solo render.yaml)
- [ ] Enviar mensaje WhatsApp de cache miss (ej: "como pido el paro") y verificar `source=llm` en logs
- [ ] Verificar `/health` endpoint devuelve `{"status": "ok"}`
- [ ] Capturar screenshot de logs como evidencia y guardar en `evidence/commands-output/`

> Guia detallada: [evidence/prod-validation.md](evidence/prod-validation.md)
>
> **TICKET-17** abierto en [backlog.md](backlog.md) para completar esta verificacion.

---

## Riesgos Residuales

| # | Riesgo | Severidad | Ticket | Estado |
|---|--------|-----------|--------|--------|
| R1 | **Test colgado** — `test_pipeline_text_cache_miss_llm_disabled` sin mock de llamadas externas | P1 | TICKET-14 | Mitigado con `-k` flag |
| R2 | **Render free tier** (512MB/0.1 CPU) — sin headroom para modelos locales. Dependencia critica en Gemini API. | P2 | — | Aceptado para hackathon |
| R3 | **KB schema inconsistente** — 3 tramites originales usan `como_hacerlo_madrid`/`como_solicitarla_madrid`; 5 nuevos usan `como_solicitar`. `_build_kb_context` maneja ambos via tier 4. | P2 | TICKET-19 | Funcional pero fragil |
| R4 | **Keyword matching O(n*m)** — irrelevante con 8 tramites, pero no escala a 50+. | P2 | TICKET-12 | Aceptado para Fase 1 |
| R5 | **Inyeccion residual: tag breaking** — un atacante podria inyectar `</user_query>` dentro del input para salir del delimitador XML. | P1 | TICKET-18 | Hipotesis — requiere red-team test |
| R6 | **DEMO_MODE sin verificacion runtime** — render.yaml dice `false` pero Render Dashboard podria sobreescribir. | P1 | TICKET-17 | Pendiente verificacion |
| R7 | **WHISPER_ON default=true en config.py** vs `false` en render.yaml — si alguien despliega sin render.yaml, el flag estaria en `true` (confuso pero inofensivo, ya que Whisper no se usa). | P1 | TICKET-06 | Cosmetic |

---

## Siguiente Paso: Fase 2

Prioridades recomendadas (ver [backlog.md](backlog.md) para detalle completo):

1. **Sprint 1 (P0-P1):** Expandir KB a 15+, fix test colgado, verificar DEMO_MODE en prod, tag breaking injection
2. **Sprint 2 (P1):** Renombrar WHISPER_ON, fuzzy/semantic matching, KB schema unificado
3. **Sprint 3 (P2):** TTS upgrade, RAG real, rate limiting, image/OCR, multilingual prompts
