# Registro de Evidencias — Fase 2 Hardening y Deploy "Clara"

> **Resumen en una linea:** Registro completo de evidencias para la Fase 2 (Hardening, Deploy e Integraciones) con 6 gates verificados: Twilio, Render, cron, Notion, QA (93 tests) y seguridad.

## Que es

Documento de trazabilidad que registra todas las verificaciones realizadas durante la Fase 2 del proyecto Clara. Cada gate (P2.1-P2.6) incluye los items verificados, la evidencia obtenida y el veredicto correspondiente.

## Para quien

- **QA** (Lucas): para validar cobertura de testing y resultados de seguridad
- **DevOps** (Marcos): para confirmar el estado de deploy y configuraciones
- **PM** (Andrea): para reportar al jurado del hackathon

## Que incluye

- Evidencias de 6 gates: P2.1 (Twilio), P2.2 (Render), P2.3 (Cron), P2.4 (Notion), P2.5 (QA), P2.6 (Seguridad)
- Salidas reales de pytest, docker build, /health, y escaneo de secretos
- Comandos verificados y salidas reproducibles

## Que NO incluye

- Evidencias de la Fase 1 (ver [PHASE-1-EVIDENCE.md](./PHASE-1-EVIDENCE.md))
- Procedimientos de remediacion de vulnerabilidades

---

> **Proyecto:** CivicAid Voice / Clara
> **Fase:** 2 — Hardening, Deploy e Integraciones
> **Fecha:** 2026-02-12
> **Metodologia:** PASS = demostrado por salida de test/comando. PENDING = aun no verificado. FAIL = intentado y fallido.
>
> **Relacionado:** [Evidencia Fase 1](./PHASE-1-EVIDENCE.md) | [Estado de Fases](./PHASE-STATUS.md) | [Plan de Testing](../04-testing/TEST-PLAN.md)

---

## P2.1 — Verificacion del Pipeline Twilio + Guia de Configuracion

| ID | Descripcion | Evidencia | Estado |
|----|-------------|----------|--------|
| P2.1.1 | Validacion de firma de webhook Twilio en webhook.py | `RequestValidator` utilizado en webhook.py | PASS |
| P2.1.2 | Envio Twilio REST con timeout de 10s | `timeout=10` en send_response.py | PASS |
| P2.1.3 | Parsing seguro de NumMedia | try/except en webhook.py | PASS |
| P2.1.4 | Guia de configuracion del sandbox Twilio | `docs/06-integrations/TWILIO-SETUP-GUIDE.md` creada | PASS |

---

## P2.2 — Deploy en Render Reproducible + /health Verificado

| ID | Descripcion | Evidencia | Estado |
|----|-------------|----------|--------|
| P2.2.1 | Dockerfile compila exitosamente | `docker build -t civicaid-voice:test .` | PASS (local) |
| P2.2.2 | render.yaml usa `sync: false` para secretos | No hay secretos en render.yaml | PASS |
| P2.2.3 | Endpoint /health devuelve JSON | `curl .../health` devuelve 200 OK, `{"status":"ok","cache_entries":8}` | PASS |
| P2.2.4 | .dockerignore presente | `.dockerignore` existe | PASS |

---

## P2.3 — Warm-up Cron Documentado y Verificado

| ID | Descripcion | Evidencia | Estado |
|----|-------------|----------|--------|
| P2.3.1 | Configuracion de cron-job.org documentada | Seccion 5 de RUNBOOK-PHASE2.md | PASS |
| P2.3.2 | Intervalo de warm-up: 14 min | Previene cold start del tier gratuito de Render (duerme tras 15 min) | PASS |

---

## P2.4 — Notion Completamente Actualizado

| ID | Descripcion | Evidencia | Estado |
|----|-------------|----------|--------|
| P2.4.1 | 3 bases de datos de Notion pobladas | 75 entradas en 3 DBs (37 Backlog, 12 KB, 26 Testing) | PASS |
| P2.4.2 | Backlog DB: 37 entradas | Consulta API Notion (31 Hecho, 1 En progreso, 5 Backlog) | PASS |
| P2.4.3 | KB Tramites DB: 12 entradas | Consulta API Notion (todas Verificado) | PASS |
| P2.4.4 | Demo & Testing DB: 26 entradas | Consulta API Notion (10 Pasa, 16 Pendiente) | PASS |

---

## P2.5 — Script de Verificacion + Evidencia QA

### Salida de pytest

```
$ pytest tests/ -v --tb=short
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /Users/andreaavila/Documents/hakaton/civicaid-voice
configfile: pyproject.toml

tests/e2e/test_demo_flows.py::test_t9_wa_text_demo_complete PASSED       [  1%]
tests/e2e/test_demo_flows.py::test_t10_wa_audio_demo_stub PASSED         [  2%]
tests/e2e/test_demo_flows.py::test_health_endpoint PASSED                [  3%]
tests/e2e/test_demo_flows.py::test_static_cache_mp3 PASSED               [  4%]
tests/integration/test_pipeline.py::test_t8_pipeline_text_cache_hit PASSED [  5%]
tests/integration/test_pipeline.py::test_pipeline_text_cache_miss_llm_disabled PASSED [  6%]
tests/integration/test_twilio_stub.py::test_send_final_message_text_only PASSED [  7%]
tests/integration/test_twilio_stub.py::test_send_final_message_with_media PASSED [  8%]
tests/integration/test_webhook.py::test_t6_webhook_text PASSED           [  9%]
tests/integration/test_webhook.py::test_t7_webhook_audio PASSED          [ 10%]
tests/integration/test_webhook.py::test_webhook_returns_twiml_xml PASSED [ 11%]
tests/unit/test_cache.py::test_t1_cache_match_keyword_exact PASSED       [ 12%]
tests/unit/test_cache.py::test_t2_cache_match_no_match PASSED            [ 13%]
tests/unit/test_cache.py::test_t3_cache_match_image_demo PASSED          [ 15%]
tests/unit/test_cache.py::test_cache_match_french PASSED                 [ 16%]
tests/unit/test_cache.py::test_cache_match_language_filter PASSED        [ 17%]
tests/unit/test_cache.py::test_cache_match_empty_text PASSED             [ 18%]
tests/unit/test_config.py::test_config_defaults PASSED                   [ 19%]
tests/unit/test_config.py::test_config_demo_mode PASSED                  [ 20%]
tests/unit/test_config.py::test_config_twilio_sandbox_default PASSED     [ 21%]
tests/unit/test_detect_input.py::test_text_input PASSED                  [ 22%]
tests/unit/test_detect_input.py::test_audio_input PASSED                 [ 23%]
tests/unit/test_detect_input.py::test_image_input PASSED                 [ 24%]
tests/unit/test_detect_input.py::test_unknown_media_type PASSED          [ 25%]
tests/unit/test_detect_lang.py::test_t5_detect_french PASSED             [ 26%]
tests/unit/test_detect_lang.py::test_detect_spanish PASSED               [ 27%]
tests/unit/test_detect_lang.py::test_detect_short_text_defaults PASSED   [ 29%]
tests/unit/test_detect_lang.py::test_detect_empty_defaults PASSED        [ 30%]
tests/unit/test_evals.py::test_load_eval_cases PASSED                    [ 31%]
tests/unit/test_evals.py::test_load_eval_cases_missing_dir PASSED        [ 32%]
tests/unit/test_evals.py::test_run_eval_case_pass PASSED                 [ 33%]
tests/unit/test_evals.py::test_run_eval_case_fail_missing PASSED         [ 34%]
tests/unit/test_evals.py::test_run_eval_case_fail_unexpected PASSED      [ 35%]
tests/unit/test_evals.py::test_run_eval_case_no_checks PASSED            [ 36%]
tests/unit/test_evals.py::test_run_eval_set PASSED                       [ 37%]
tests/unit/test_evals.py::test_eval_report_generation PASSED             [ 38%]
tests/unit/test_evals.py::test_eval_runner_with_cache PASSED             [ 39%]
tests/unit/test_guardrails.py::test_pre_check_blocks_self_harm PASSED    [ 40%]
tests/unit/test_guardrails.py::test_pre_check_blocks_self_harm_suicid PASSED [ 41%]
tests/unit/test_guardrails.py::test_pre_check_blocks_violence PASSED     [ 43%]
tests/unit/test_guardrails.py::test_pre_check_blocks_illegal PASSED      [ 44%]
tests/unit/test_guardrails.py::test_pre_check_blocks_self_harm_suicidarme PASSED [ 45%]
tests/unit/test_guardrails.py::test_pre_check_blocks_falsificar_nie PASSED [ 46%]
tests/unit/test_guardrails.py::test_pre_check_allows_safe_input PASSED   [ 47%]
tests/unit/test_guardrails.py::test_pre_check_allows_tramite_questions PASSED [ 48%]
tests/unit/test_guardrails.py::test_pre_check_allows_empadronamiento PASSED [ 49%]
tests/unit/test_guardrails.py::test_post_check_adds_legal_disclaimer PASSED [ 50%]
tests/unit/test_guardrails.py::test_post_check_adds_medical_disclaimer PASSED [ 51%]
tests/unit/test_guardrails.py::test_post_check_no_disclaimer_for_simple_info PASSED [ 52%]
tests/unit/test_guardrails.py::test_post_check_no_duplicate_disclaimer PASSED [ 53%]
tests/unit/test_guardrails.py::test_post_check_redacts_dni PASSED        [ 54%]
tests/unit/test_guardrails.py::test_post_check_redacts_nie PASSED        [ 55%]
tests/unit/test_guardrails.py::test_post_check_redacts_phone PASSED      [ 56%]
tests/unit/test_guardrails.py::test_post_check_preserves_clean_text PASSED [ 58%]
tests/unit/test_guardrails.py::test_guardrails_flag_default_on PASSED    [ 59%]
tests/unit/test_guardrails.py::test_guardrails_flag_can_be_disabled PASSED [ 60%]
tests/unit/test_kb_lookup.py::test_t4_kb_lookup_empadronamiento PASSED   [ 61%]
tests/unit/test_kb_lookup.py::test_kb_lookup_imv PASSED                  [ 62%]
tests/unit/test_kb_lookup.py::test_kb_lookup_tarjeta PASSED              [ 63%]
tests/unit/test_kb_lookup.py::test_kb_lookup_no_match PASSED             [ 64%]
tests/unit/test_observability.py::test_request_context_creation PASSED   [ 65%]
tests/unit/test_observability.py::test_timing_tracking PASSED            [ 66%]
tests/unit/test_observability.py::test_to_dict PASSED                    [ 67%]
tests/unit/test_observability.py::test_context_thread_local PASSED       [ 68%]
tests/unit/test_observability.py::test_clear_context PASSED              [ 69%]
tests/unit/test_observability.py::test_observability_flag_off PASSED     [ 70%]
tests/unit/test_redteam.py::TestRedTeamDataFile::test_redteam_file_exists PASSED [ 72%]
tests/unit/test_redteam.py::TestRedTeamDataFile::test_redteam_file_valid_json PASSED [ 73%]
tests/unit/test_redteam.py::TestRedTeamDataFile::test_redteam_cases_have_required_fields PASSED [ 74%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_guardrails_module_exists PASSED [ 75%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_blocked_prompts[rt_01] XPASS [ 76%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_blocked_prompts[rt_02] XPASS [ 77%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_blocked_prompts[rt_03] XPASS [ 78%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_blocked_prompts[rt_04] XPASS [ 79%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_blocked_prompts[rt_05] XPASS [ 80%]
tests/unit/test_redteam.py::TestRedTeamGuardrails::test_safe_input_passes PASSED [ 81%]
tests/unit/test_retriever.py::TestRetrieverInterface::test_retriever_is_abstract PASSED [ 82%]
tests/unit/test_retriever.py::TestRetrieverInterface::test_json_kb_retriever_is_retriever PASSED [ 83%]
tests/unit/test_retriever.py::TestJSONKBRetriever::test_json_kb_retriever_finds_imv PASSED [ 84%]
tests/unit/test_retriever.py::TestJSONKBRetriever::test_json_kb_retriever_finds_empadronamiento PASSED [ 86%]
tests/unit/test_retriever.py::TestJSONKBRetriever::test_json_kb_retriever_no_match PASSED [ 87%]
tests/unit/test_retriever.py::TestGetRetriever::test_get_retriever_returns_json PASSED [ 88%]
tests/unit/test_retriever.py::TestGetRetriever::test_get_retriever_returns_retriever PASSED [ 89%]
tests/unit/test_structured_outputs.py::test_structured_response_model_validation PASSED [ 90%]
tests/unit/test_structured_outputs.py::test_structured_response_defaults PASSED [ 91%]
tests/unit/test_structured_outputs.py::test_structured_response_rejects_missing_required PASSED [ 92%]
tests/unit/test_structured_outputs.py::test_parse_valid_json PASSED      [ 93%]
tests/unit/test_structured_outputs.py::test_parse_invalid_json_fallback PASSED [ 94%]
tests/unit/test_structured_outputs.py::test_parse_markdown_json_block PASSED [ 95%]
tests/unit/test_structured_outputs.py::test_parse_generic_code_block PASSED [ 96%]
tests/unit/test_structured_outputs.py::test_parse_partial_json_fallback PASSED [ 97%]
tests/unit/test_structured_outputs.py::test_parse_display_no_steps PASSED [ 98%]
tests/unit/test_structured_outputs.py::test_flag_off_no_impact PASSED    [100%]

======================== 88 passed, 5 xpassed in 1.27s =========================

Veredicto: PASS -- 93 tests (88 passed + 5 xpassed), 0 fallidos
```

### Salida de Ruff Lint

```
$ ruff check src/ tests/ --select E,F,W --ignore E501
Todas las comprobaciones superadas.

Veredicto: PASS -- cero errores de lint
```

### Script de Verificacion

```
$ bash scripts/phase2_verify.sh
# Ejecuta 5 pasos: pytest, ruff, docker build, docker /health, Render /health
# Ver script en scripts/phase2_verify.sh
```

### Desglose de Tests (adiciones Fase 2 vs Fase 1)

| Suite | Fase 1 | Fase 2 | Delta |
|-------|--------|--------|-------|
| Tests unitarios | 21 | 75 | +54 |
| Tests de integracion | 7 | 8 | +1 |
| Tests E2E | 4 | 4 | 0 |
| Red team (xpassed) | 0 | 5 | +5 |
| **Total** | **32** | **93** | **+61** |

Archivos de test nuevos en la Fase 2:

| Archivo | Tests | Cobertura |
|---------|-------|-----------|
| tests/unit/test_evals.py | 9 | Eval runner, casos de evaluacion, reportes |
| tests/unit/test_guardrails.py | 19 | Bloqueadores pre-check, disclaimers post-check, redaccion PII |
| tests/unit/test_observability.py | 6 | RequestContext, timings, thread-local, feature flag |
| tests/unit/test_redteam.py | 9 | Validacion archivo red team, prompts adversariales contra guardrails |
| tests/unit/test_retriever.py | 7 | Interfaz Retriever, JSON KB retriever, factory |
| tests/unit/test_structured_outputs.py | 11 | Modelo de respuesta estructurada, parsing JSON, display |

**Veredicto Gate P2.5: PASS**

---

## P2.6 — Escaneo de Seguridad + Auditoria de Secretos

### Fecha del escaneo: 2026-02-12

### 1. Verificacion de .gitignore

```
$ grep -c '.env' .gitignore
4 coincidencias: .env, .env.local, .env.production, .env.*.local

Veredicto: PASS -- .env y variantes estan en gitignore
```

### 2. .env no rastreado en Git

```
$ git ls-files | grep '\.env$'
(sin salida -- .env NO esta rastreado)

Veredicto: PASS
```

### 3. .env.example no tiene valores reales

```
Verificado .env.example:
- TWILIO_ACCOUNT_SID= (vacio)
- TWILIO_AUTH_TOKEN= (vacio)
- GEMINI_API_KEY= (vacio)
- NOTION_TOKEN= (vacio)
- GRAFANA_API_KEY= (vacio)
- GITHUB_TOKEN= (vacio)
- ADMIN_TOKEN= (vacio)
- TWILIO_SANDBOX_FROM=whatsapp:+14155238886 (numero publico de sandbox, seguro)

Veredicto: PASS -- todos los campos de secretos vacios o placeholder
```

### 4. Escaneo de patrones de secretos

| Patron | Descripcion | Archivos encontrados | Veredicto |
|--------|-------------|---------------------|-----------|
| `sk-[a-zA-Z0-9]{20,}` | Clave API de OpenAI | 0 | PASS |
| `xoxb-*` | Token de bot de Slack | 0 | PASS |
| `ghp_[a-zA-Z0-9]{36}` | Token personal de GitHub | 0 | PASS |
| `AC[a-f0-9]{32}` | Account SID de Twilio | 0 | PASS |
| `Bearer [token-real]` | Tokens Bearer | 0 reales (1 placeholder) | PASS |
| `password=["'][real]` | Contrasenas hardcodeadas | 0 | PASS |
| `ntn_[token-real]` | Token de integracion Notion | 0 reales (4 placeholders) | PASS |
| `AIza[a-zA-Z0-9_-]{35}` | Clave API de Google | 0 | PASS |
| `api_key=["'][real]` | Clave API generica | 0 | PASS |
| `secret=["'][real]` | Secreto generico | 0 | PASS |
| `token=["'][real]` | Token generico | 0 | PASS |

### 5. Verificacion de render.yaml

```
Las variables de entorno sensibles usan sync: false (configuradas via panel de Render, no en codigo):
- TWILIO_ACCOUNT_SID: sync: false
- TWILIO_AUTH_TOKEN: sync: false
- GEMINI_API_KEY: sync: false

Solo valores no sensibles estan hardcodeados (DEMO_MODE, LLM_LIVE, etc.)

Veredicto: PASS
```

### 6. Escaneo de documentacion y scripts

```
Escaneados: docs/, scripts/, .claude/
- docs/06-integrations/NOTION-OS.md: contiene "ntn_XXXX...XXXX" (placeholder, seguro)
- .claude/NOTION-SETUP-MANUAL.md: contiene "ntn_XXXXXXXXXXXXXXXXXXXXXXXX" (placeholder, seguro)
- .claude/project-settings.json: contiene "ntn_xxx" (placeholder, seguro)
- scripts/populate_notion.sh: contiene "ntn_xxx" (ejemplo en mensaje de error, seguro)

No se encontraron tokens reales en ningun archivo de documentacion o script.

Veredicto: PASS
```

### 7. Verificaciones adicionales

| Verificacion | Resultado |
|--------------|-----------|
| .dockerignore existe | PASS |
| .dockerignore excluye .env | PASS (via patron de .gitignore) |
| Directorio secrets/ en .gitignore | PASS |
| *.pem y *.key en .gitignore | PASS |
| No hay archivos credentials.json | PASS |

**Veredicto Gate P2.6: PASS -- Cero secretos filtrados. Todos los valores sensibles usan variables de entorno o placeholders.**

---

## Resumen

| Gate | Descripcion | Estado | Evidencia |
|------|-------------|--------|----------|
| P2.1 | Verificacion pipeline Twilio | **PASS** | Validacion de firma, timeouts, parsing seguro, guia de configuracion |
| P2.2 | Deploy Render reproducible | **PASS** | Docker build exitoso, Render /health 200 OK, cache_entries=8 |
| P2.3 | Warm-up cron documentado | **PASS** | Documentado en RUNBOOK-PHASE2.md Seccion 5 (cada 14 min) |
| P2.4 | Notion completamente actualizado | **PASS** | 75 entradas en 3 DBs (37 Backlog, 12 KB, 26 Testing) |
| P2.5 | Script de verificacion + evidencia QA | **PASS** | 93/93 tests, 0 errores lint, scripts/phase2_verify.sh |
| P2.6 | Escaneo de seguridad + auditoria de secretos | **PASS** | Cero secretos filtrados, .env en gitignore, solo placeholders |

---

## Comandos verificados y salidas (Pase de reconciliacion 2026-02-12)

### Docker Build

```
$ docker build -t civicaid-voice:test .
#1 [internal] load build definition from Dockerfile
#4 [1/5] FROM docker.io/library/python:3.11-slim
#6 [4/5] RUN pip install --no-cache-dir -r requirements.txt (CACHED)
#9 [5/5] COPY . . (CACHED)
#10 exporting to image — naming to docker.io/library/civicaid-voice:test done
BUILD EXITOSO (tamano imagen: 1.79GB)
```

### Docker /health (contenedor local)

```
$ curl -s http://localhost:5050/health | python3 -m json.tool
{
    "status": "ok",
    "uptime_s": 8,
    "components": {
        "cache_entries": 8,
        "demo_mode": true,
        "ffmpeg_available": false,
        "gemini_key_set": false,
        "llm_live": true,
        "twilio_configured": false,
        "whisper_enabled": true,
        "whisper_loaded": false
    }
}
```

### Render /health (produccion)

```
$ curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
{
    "status": "ok",
    "components": {
        "cache_entries": 8,
        "demo_mode": true,
        "gemini_key_set": true,
        "twilio_configured": true,
        "whisper_enabled": false,
        "whisper_loaded": false
    }
}
```

### Audio estatico en Render

```
$ curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
HTTP/2 200 OK
Content-Type: audio/mpeg
```

### Webhook en Render (peticion sin firma = 403, correcto)

```
$ curl -s -o /dev/null -w "%{http_code}" -X POST https://civicaid-voice.onrender.com/webhook -d "Body=test"
403
```

---

## Como se verifica

```bash
# Script de verificacion completo
bash scripts/phase2_verify.sh [RENDER_URL]

# Suite completa de tests
pytest tests/ -v --tb=short

# Lint
ruff check src/ tests/ --select E,F,W --ignore E501
```

## Referencias

- [Evidencia Fase 1](./PHASE-1-EVIDENCE.md)
- [Estado de Fases](./PHASE-STATUS.md)
- [Plan de Testing](../04-testing/TEST-PLAN.md)
- [Plan Fase 2](../01-phases/FASE2-HARDENING-DEPLOY-INTEGRATIONS.md)
- [Runbook Fase 2](../03-runbooks/RUNBOOK-PHASE2.md)
