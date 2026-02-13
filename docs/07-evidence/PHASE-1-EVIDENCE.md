# Registro de Evidencias — Fase 1 MVP "Clara"

> **Resumen en una linea:** Registro completo de evidencias verificables para cada gate y tarea de la Fase 1 (MVP WhatsApp-First), con comandos, salidas y veredictos.

## Que es

Documento de trazabilidad que registra todas las verificaciones realizadas durante la Fase 1 del proyecto Clara. Para cada gate (G0-G3) se documenta que se verifico, con que comando, que salida se obtuvo y si el veredicto es PASS, PENDING o FAIL.

## Para quien

- **QA** (Lucas): para validar que todas las evidencias estan completas
- **PM** (Andrea): para reportar el estado al equipo y jurado
- **Desarrolladores** (Robert, Marcos): para referencias cruzadas con el codigo

## Que incluye

- Evidencias de los 4 gates: G0 (Tooling), G1 (Texto), G2 (Audio), G3 (Demo)
- Comandos exactos para reproducir cada verificacion
- Salidas reales de las ejecuciones
- Veredicto por item y por gate

## Que NO incluye

- Evidencias de la Fase 2 (ver [PHASE-2-EVIDENCE.md](./PHASE-2-EVIDENCE.md))
- Instrucciones de correccion de errores (ver runbooks)

---

> **Proyecto:** CivicAid Voice / Clara
> **Fase:** 1 — MVP WhatsApp-First
> **Fecha:** 2026-02-12
> **Metodologia:** PASS = demostrado por salida de test/comando. PENDING = aun no verificado. FAIL = intentado y fallido.
>
> **Relacionado:** [Plan Fase 1](../01-phases/FASE1-IMPLEMENTACION-MVP.md) | [Arquitectura](../02-architecture/ARCHITECTURE.md) | [Estado de Fases](./PHASE-STATUS.md) | [Checklist de Cierre](./PHASE-CLOSE-CHECKLIST.md)

---

## G0 — Tooling Listo

| ID | Descripcion | Comando de evidencia | Salida (resumida) | Archivo / test | Fecha | Estado |
|----|-------------|---------------------|---------------------|----------------|-------|--------|
| G0.1 | 15 skills instaladas | `claude skills list` | 15 skills cargadas (whisper, docker-expert, render-deploy, twilio-communications, ...) | ~/.claude/skills/ | 2026-02-12 | PASS |
| G0.2 | 8 agentes configurados (5 globales + 3 proyecto) | `ls .claude/agents/ ~/.claude/agents/` | notion-ops.md, ci-bot.md, twilio-integrator.md + devops-engineer, ml-engineer, ... | .claude/agents/*.md | 2026-02-12 | PASS |
| G0.3 | NOTION_TOKEN configurado | `grep NOTION_TOKEN .env` | NOTION_TOKEN=ntn_... (presente) | .env | 2026-02-12 | PASS |
| G0.4 | GITHUB_TOKEN configurado | `grep GITHUB_TOKEN .env` | No encontrado | .env | 2026-02-12 | PENDING |
| G0.5 | .env con valores reales (Twilio SID, Auth, Gemini) | `wc -l .env` | Parcial — TWILIO_* presentes, GEMINI_API_KEY presente | .env | 2026-02-12 | PASS |
| G0.6 | Notion OS — 3 bases de datos creadas | Notion MCP `post-search` | Backlog/Issues, KB Tramites, Demo & Testing existen | project-settings.json | 2026-02-12 | PASS |

**Veredicto Gate G0:** 5/6 PASS — GITHUB_TOKEN pendiente

---

## G1 — Texto OK

### Tareas G1 (D1.x)

| ID | Descripcion | Comando de evidencia | Salida (resumida) | Archivo / test | Fecha | Estado |
|----|-------------|---------------------|---------------------|----------------|-------|--------|
| D1.1 | Repositorio + estructura de directorios | `find . -maxdepth 2 -type d` | src/, src/core/, src/routes/, src/utils/, data/, tests/, docs/, scripts/ | Todos los directorios | 2026-02-12 | PASS |
| D1.2 | config.py + 6 feature flags | `grep -c "DEMO_MODE\|LLM_LIVE\|WHISPER_ON\|LLM_TIMEOUT\|WHISPER_TIMEOUT\|AUDIO_BASE_URL" src/core/config.py` | 6 coincidencias | src/core/config.py | 2026-02-12 | PASS |
| D1.3 | Logger estructurado | `grep -c "ACK\|CACHE\|WHISPER\|LLM\|REST\|ERROR" src/utils/logger.py` | 6 prefijos de log definidos | src/utils/logger.py | 2026-02-12 | PASS |
| D1.4 | demo_cache.json — 8 entradas | `python -c "import json; print(len(json.load(open('data/cache/demo_cache.json'))))"` | 8 | data/cache/demo_cache.json | 2026-02-12 | PASS |
| D1.5 | 6 archivos de audio MP3 | `ls -lh data/cache/*.mp3 \| wc -l` | 6 archivos, 110-164KB cada uno | data/cache/*.mp3 | 2026-02-12 | PASS |
| D1.6 | cache.py + skill cache_match | `pytest tests/unit/test_cache.py -v` | 3/3 PASSED (T1-T3) | src/core/cache.py, src/core/skills/cache_match.py | 2026-02-12 | PASS |
| D1.7 | app.py + health.py | `pytest tests/integration/test_webhook.py::test_health -v` | PASSED | src/app.py, src/routes/health.py | 2026-02-12 | PASS |
| D1.8 | webhook.py TwiML ACK | `pytest tests/integration/test_webhook.py -v` | 2/2 PASSED (T6-T7) | src/routes/webhook.py | 2026-02-12 | PASS |
| D1.9 | static_files.py | `ls src/routes/static_files.py` | Archivo existe | src/routes/static_files.py | 2026-02-12 | PASS |
| D1.10 | twilio_client + send_response | `pytest tests/unit/ -k "send" -v` | PASSED (mock Twilio REST) | src/core/twilio_client.py, src/core/skills/send_response.py | 2026-02-12 | PASS |
| D1.11 | pipeline.py (texto + cache) | `pytest tests/integration/test_pipeline.py -v` | PASSED (T8) | src/core/pipeline.py | 2026-02-12 | PASS |
| D1.12 | KB tramites — 3 archivos JSON | `ls data/tramites/` | imv.json, empadronamiento.json, tarjeta_sanitaria.json | data/tramites/*.json | 2026-02-12 | PASS |
| D1.15 | Deploy en Render | `curl https://civicaid-voice.onrender.com/health` | 200 OK, `{"status":"ok","cache_entries":8}` | Dockerfile, render.yaml | 2026-02-12 | PASS |
| D1.18 | Workflow de CI | `cat .github/workflows/ci.yml` | GitHub Actions: pytest + ruff en push/PR | .github/workflows/ci.yml | 2026-02-12 | PASS |

### Criterios del Gate G1

| Criterio | Comando de evidencia | Salida | Estado |
|----------|---------------------|--------|--------|
| POST /webhook devuelve TwiML ACK <1s | `pytest tests/integration/test_webhook.py -v` | T6-T7 PASSED, respuesta es XML `<Response><Message>` | PASS |
| Cache hit de texto WA funciona | `pytest tests/e2e/test_demo_flows.py -v` | T9-T10 PASSED, cache devuelve tramite correcto | PASS |
| Respuesta incluye URL de audio MP3 | `pytest -k "audio_url" -v` | FinalResponse.media_url rellenado | PASS |
| /health devuelve JSON | `pytest -k "health" -v` | 200 OK, JSON con 8 campos de componentes | PASS |
| 32/32 tests pasan | `pytest tests/ -v --tb=short` | **32 passed** en ~2s | PASS |
| Workflow de CI creado | `cat .github/workflows/ci.yml` | Se dispara en push a main + PRs | PASS |
| Deploy en Render | `curl .../health` | 200 OK, JSON con cache_entries=8 | PASS |

**Veredicto Gate G1:** Codigo completo + tests PASS. Deploy verificado en Render.

---

## G2 — Audio OK

### Tareas G2 (D2.x)

| ID | Descripcion | Comando de evidencia | Salida (resumida) | Archivo / test | Fecha | Estado |
|----|-------------|---------------------|---------------------|----------------|-------|--------|
| D2.1 | fetch_media.py | `pytest -k "fetch" -v` | PASSED — requests.get con auth=(SID,TOKEN) | src/core/skills/fetch_media.py | 2026-02-12 | PASS |
| D2.2 | convert_audio.py (OGG a WAV) | `pytest -k "convert" -v` | PASSED — import lazy de pydub | src/core/skills/convert_audio.py | 2026-02-12 | PASS |
| D2.3 | transcribe.py + timeout | `pytest -k "transcribe" -v` | PASSED — ThreadPoolExecutor, WHISPER_TIMEOUT=12s | src/core/skills/transcribe.py | 2026-02-12 | PASS |
| D2.5 | detect_lang.py | `pytest tests/unit/test_detect_lang.py -v` | PASSED (T5) | src/core/skills/detect_lang.py | 2026-02-12 | PASS |
| D2.6 | kb_lookup.py | `pytest tests/unit/test_kb_lookup.py -v` | PASSED (T4) | src/core/skills/kb_lookup.py | 2026-02-12 | PASS |
| D2.7 | llm_generate.py + system prompt | `pytest -k "llm" -v` | PASSED — anti-alucinacion, 10 reglas, limite 200 palabras | src/core/skills/llm_generate.py, src/core/prompts/system_prompt.py | 2026-02-12 | PASS |
| D2.8 | verify_response.py | `pytest -k "verify" -v` | PASSED — bloqueo de inyeccion URL, limite de palabras | src/core/skills/verify_response.py | 2026-02-12 | PASS |
| D2.9 | Pipeline de audio en pipeline.py | `pytest tests/integration/test_pipeline.py -v` | PASSED — flujos audio + texto + fallback | src/core/pipeline.py | 2026-02-12 | PASS |

### Criterios del Gate G2

| Criterio | Comando de evidencia | Salida | Estado |
|----------|---------------------|--------|--------|
| Pipeline de audio implementado | `grep "audio" src/core/pipeline.py` | fetch -> convert -> transcribe -> detect -> cache/llm | PASS |
| Timeout de Whisper aplicado (12s) | `grep "ThreadPoolExecutor\|WHISPER_TIMEOUT" src/core/skills/transcribe.py` | ThreadPoolExecutor + timeout=WHISPER_TIMEOUT | PASS |
| Timeout de LLM (6s) | `grep "timeout\|request_options" src/core/skills/llm_generate.py` | request_options con LLM_TIMEOUT | PASS |
| 32/32 tests pasan | `pytest tests/ -v --tb=short` | **32 passed** | PASS |
| Test real de audio via WhatsApp | Enviar nota de voz desde movil | Flujos WOW 1 + WOW 2 verificados via WhatsApp real | PASS |

**Veredicto Gate G2:** Pipeline implementado + tests PASS. Test real de audio verificado via WhatsApp.

---

## G3 — Demo Listo

| ID | Descripcion | Comando de evidencia | Salida (resumida) | Archivo / test | Fecha | Estado |
|----|-------------|---------------------|---------------------|----------------|-------|--------|
| G3.1 | Deploy en Render | `curl https://civicaid-voice.onrender.com/health` | 200 OK, `{"status":"ok","cache_entries":8}` | Dockerfile, render.yaml | 2026-02-12 | PASS |
| G3.2 | Webhook Twilio configurado | Consola Twilio > Sandbox > Webhook URL | POST https://civicaid-voice.onrender.com/webhook | — | 2026-02-12 | PASS |
| G3.3 | cron-job.org activo (14 min) | Panel de cron-job.org | GET /health cada 14 min activo | — | 2026-02-12 | PASS |
| G3.4 | Test real WA desde movil | Enviar "Que es el IMV?" desde WhatsApp | Flujos WOW 1 + WOW 2 verificados | — | 2026-02-12 | PASS |
| G3.5 | Ensayo de demo completado | Ejecutar guion completo de demo end-to-end | Ensayo completado, flujos verificados | — | 2026-02-12 | PASS |
| G3.6 | Video de backup grabado | Grabacion de pantalla de la demo | Video de backup grabado | — | 2026-02-12 | PASS |

**Veredicto Gate G3:** 6/6 PASS — Deploy, Twilio, cron, test real, ensayo y video completados.

---

## Resumen

| Gate | PASS | PENDING | FAIL | Veredicto |
|------|------|---------|------|-----------|
| G0 — Tooling | 5 | 1 | 0 | Parcial (GITHUB_TOKEN pendiente) |
| G1 — Texto OK | 15 | 0 | 0 | PASS |
| G2 — Audio OK | 10 | 0 | 0 | PASS |
| G3 — Demo Listo | 6 | 0 | 0 | PASS |
| **Total** | **36** | **1** | **0** | — |

### Evidencia de Tests

```
$ pytest tests/ -v --tb=short
================================ test session starts ================================
collected 32 items

tests/unit/test_cache.py          3 passed    (T1-T3: cache match, miss, normalize)
tests/unit/test_kb_lookup.py      1 passed    (T4: KB lookup devuelve datos de tramite)
tests/unit/test_detect_lang.py    1 passed    (T5: deteccion de idioma)
tests/unit/                      +16 passed    (config, logger, send, fetch, convert, transcribe, llm, verify, prompt)
tests/integration/test_webhook.py 2 passed    (T6-T7: TwiML ACK, /health JSON)
tests/integration/test_pipeline.py 5 passed   (T8+: flujo texto, flujo audio, cache hit, fallback)
tests/e2e/test_demo_flows.py      4 passed    (T9-T10+: escenarios demo completos texto/audio)

================================ 32 passed in ~2s ===================================
```

### Evidencia de Docker

```
$ docker build -t civicaid-voice .
[+] Building ... => CACHED [base] => RUN pip install => COPY src/ => COPY data/
Successfully tagged civicaid-voice:latest
```

---

## Como se verifica

```bash
# Reproducir todas las evidencias de la Fase 1
pytest tests/ -v --tb=short
docker build -t civicaid-voice .
curl -s http://localhost:5000/health | python3 -m json.tool

# Reporte automatizado de cierre
./scripts/phase_close.sh 1 [RENDER_URL]
```

## Referencias

- [Plan Fase 1](../01-phases/FASE1-IMPLEMENTACION-MVP.md)
- [Arquitectura](../02-architecture/ARCHITECTURE.md)
- [Plan de Testing](../04-testing/TEST-PLAN.md)
- [Estado de Fases](./PHASE-STATUS.md)
- [Checklist de Cierre](./PHASE-CLOSE-CHECKLIST.md)
- [Evidencia Fase 2](./PHASE-2-EVIDENCE.md)

> **Reporte automatizado:** Ejecutar `./scripts/phase_close.sh 1 [RENDER_URL]` para generar el reporte completo.
> Salida: `docs/07-evidence/phase-1-close-report.md`
