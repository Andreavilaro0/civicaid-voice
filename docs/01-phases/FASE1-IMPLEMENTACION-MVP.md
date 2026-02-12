# FASE 1 — Implementacion MVP "Clara" (WhatsApp-First)

> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good — UDIT
> **Fecha inicio:** 2026-02-12
> **Objetivo:** MVP funcional: WA texto + WA audio + cache-first + logs + health + deploy Render.
>
> **Documentos relacionados:**
> [Plan Maestro (Fase 0)](./FASE0-PLAN-MAESTRO-FINAL.md) |
> [Arquitectura](../02-architecture/ARCHITECTURE.md) |
> [Runbook Demo](../03-runbooks/RUNBOOK-DEMO.md)

---

## 1. Alcance

### Que es "MVP listo"

| # | Condicion | Verificacion |
|---|---|---|
| 1 | WhatsApp texto funciona | "Que es el IMV?" → ACK + respuesta cache |
| 2 | WhatsApp audio funciona | Nota de voz → ACK + transcripcion + respuesta |
| 3 | Cache-first activo | DEMO_MODE=true → respuestas en <2s |
| 4 | Logs estructurados | [ACK], [CACHE], [WHISPER], [LLM], [REST] en logs |
| 5 | Health endpoint | GET /health → JSON con estado de componentes |
| 6 | Deploy estable | Render + cron cada 8 min + cold start <15s |

### Que queda FUERA

- Base de datos relacional (JSON suficiente para 3 tramites)
- Multi-user avanzado (stateless por mensaje)
- Embeddings/RAG (keyword matching suficiente)
- gTTS en vivo (solo audios pre-generados)

---

## 2. Arquitectura

### 2.1 Patron TwiML ACK

```
POST /webhook → Parsear → TwiML ACK (HTTP 200, <1s) → Background Thread
                                                       → cache/whisper/gemini
                                                       → Twilio REST API → Usuario
```

### 2.2 Pipeline de 10 Skills

```
detect_input → [audio?] fetch_media → convert_audio → transcribe
            → detect_lang → cache_match
                           → [HIT]  → send_response (cache)
                           → [MISS] → kb_lookup → llm_generate → verify → send_response (llm)
```

### 2.3 Feature Flags

| Flag | Tipo | Default | Efecto |
|---|---|---|---|
| DEMO_MODE | bool | false | Prioriza cache, audios pre-hosted |
| LLM_LIVE | bool | true | Habilita llamadas a Gemini |
| WHISPER_ON | bool | true | Habilita transcripcion audio |
| LLM_TIMEOUT | int | 6 | Segundos max para Gemini |
| WHISPER_TIMEOUT | int | 12 | Segundos max para Whisper |
| AUDIO_BASE_URL | str | "" | Base URL para MP3 publicos |

### 2.4 Timeouts y Fallbacks

| Skill | Timeout | Fallback |
|---|---|---|
| fetch_media | 5s | "Escribe tu pregunta" |
| convert_ogg_to_wav | 3s | "Escribe tu pregunta" |
| transcribe_whisper | 12s (enforced via ThreadPoolExecutor) | "No pude entender tu audio" |
| detect_language | - | Default "es" |
| cache_match | - | CacheResult(hit=False) |
| llm_generate | 6s (via request_options) | Respuesta generica con URLs oficiales |
| send_final_message | 5s | Retry x1, luego silencio |

Ver diagramas Mermaid en [`docs/02-architecture/`](../02-architecture/).

---

## 3. Como se usa agent-development (Subagentes)

### Subagentes del proyecto (.claude/agents/)

| Subagente | Archivo | Proposito | Herramientas | Cuando usarlo | Cuando NO usarlo |
|---|---|---|---|---|---|
| **notion-ops** | `.claude/agents/notion-ops.md` | Gestion de Notion: crear DBs, popular datos, actualizar estados | MCP notionApi, Read, Write | Setup workspace, crear vistas, mover tareas | Codigo Python, Twilio, deploy |
| **ci-bot** | `.claude/agents/ci-bot.md` | GitHub Actions CI/CD | Skill github-actions-creator, Read, Write | Crear/modificar ci.yml, debug CI | Tests locales, deploy, Notion |
| **twilio-integrator** | `.claude/agents/twilio-integrator.md` | Twilio sandbox, webhooks, payloads | Skill twilio-communications, Bash | Configurar sandbox, generar TwiML, debug delivery | Audio processing, Notion, CI |

### Agents globales (~/.claude/agents/)

| Agent | Proposito | Cuando usarlo |
|---|---|---|
| **devops-engineer** | Render deploy, cron, Docker, /health | Deploy, troubleshooting infra, optimizar Dockerfile |
| **machine-learning-engineer** | Whisper optimization, inference, RAM | Whisper >12s, Render sin RAM, optimizar model |

### Como invocar un subagente

Desde Claude Code, usar el Task tool:

```
Task(subagent_type="general-purpose", prompt="[contexto del .claude/agents/notion-ops.md] + [tarea especifica]")
```

### Validacion de salida de subagentes

1. **notion-ops**: Verificar que los DB IDs se guardaron en `project-settings.json`
2. **ci-bot**: Verificar que `ci.yml` es YAML valido y el workflow corre en GitHub
3. **twilio-integrator**: Verificar que el webhook responde con TwiML a un POST de prueba
4. **devops-engineer**: Verificar que `/health` retorna JSON OK tras deploy
5. **machine-learning-engineer**: Verificar que Whisper carga en <30s y transcribe en <WHISPER_TIMEOUT

### Reglas de uso

1. Un subagente = una responsabilidad. No mezclar.
2. Leer el `.md` del subagente antes de invocarlo (tiene contexto y restricciones).
3. Los subagentes del proyecto se commitean al repo. Los globales no.
4. Los subagentes no se comunican entre si. El flujo lo orquesta Claude Code.

---

## 4. Plan de Ejecucion

### Gate 0: Tooling Ready (pre-requisito)

| # | Criterio | Estado |
|---|---|---|
| G0.1 | 15 skills instaladas | ✅ |
| G0.2 | 5 agents globales + 3 proyecto | ✅ |
| G0.3 | NOTION_TOKEN configurado | ✅ |
| G0.4 | GITHUB_TOKEN | ⚠️ Pendiente |
| G0.5 | .env con valores reales | ⚠️ Pendiente |
| G0.6 | Notion OS (3 DBs) | ✅ |

### Dia 1: Infraestructura + WA Texto

| Tarea | Owner | Estado | Archivo principal |
|---|---|---|---|
| D1.1 Crear repo + estructura | Robert | ✅ | Toda la estructura |
| D1.2 config.py + 6 flags | Robert | ✅ | src/core/config.py |
| D1.3 logger.py | Robert | ✅ | src/utils/logger.py |
| D1.4 demo_cache.json 8 entries | Robert | ✅ | data/cache/demo_cache.json |
| D1.5 6 audios MP3 (gTTS) | Robert | ✅ | data/cache/*.mp3 |
| D1.6 cache.py + cache_match.py | Robert | ✅ | src/core/cache.py, skills/cache_match.py |
| D1.7 app.py + health.py | Marcos | ✅ | src/app.py, routes/health.py |
| D1.8 webhook.py TwiML ACK | Marcos | ✅ | src/routes/webhook.py |
| D1.9 static_files.py | Marcos | ✅ | src/routes/static_files.py |
| D1.10 twilio_client.py + send | Marcos | ✅ | src/core/twilio_client.py, skills/send_response.py |
| D1.11 pipeline.py (texto+cache) | Marcos | ✅ | src/core/pipeline.py |
| D1.12-13 JSONs tramites | Lucas | ✅ | data/tramites/*.json |
| D1.15 Deploy Render | Marcos | ⏳ Pendiente | Dockerfile, render.yaml |
| D1.18 CI workflow | Robert | ✅ | .github/workflows/ci.yml |

### Gate 1: Texto OK

| Criterio | Estado |
|---|---|
| POST /webhook retorna TwiML ACK <1s | ✅ Implementado |
| WA texto cache hit funciona | ✅ Tests pasan |
| Respuesta incluye audio MP3 | ✅ media_url en FinalResponse |
| /health retorna JSON | ✅ Implementado + testeado |
| Tests T1-T8 pasan | ✅ 32/32 |
| CI workflow creado | ✅ |
| Deploy Render | ⏳ Pendiente |

### Dia 2: Audio Pipeline + Whisper + LLM

| Tarea | Owner | Estado | Archivo |
|---|---|---|---|
| D2.1 fetch_media.py | Marcos | ✅ | skills/fetch_media.py |
| D2.2 convert_audio.py | Marcos | ✅ | skills/convert_audio.py |
| D2.3 transcribe.py + timeout | Marcos | ✅ | skills/transcribe.py |
| D2.5 detect_lang.py | Robert | ✅ | skills/detect_lang.py |
| D2.6 kb_lookup.py | Robert | ✅ | skills/kb_lookup.py |
| D2.7 llm_generate.py + prompt | Robert | ✅ | skills/llm_generate.py |
| D2.8 verify_response.py | Robert | ✅ | skills/verify_response.py |
| D2.9 Audio pipeline en pipeline.py | Marcos | ✅ | src/core/pipeline.py |

### Gate 2: Audio OK

| Criterio | Estado |
|---|---|
| Audio pipeline implementado | ✅ |
| Whisper timeout enforced (12s) | ✅ ThreadPoolExecutor |
| LLM timeout (6s) | ✅ request_options |
| Tests pasan | ✅ 32/32 |
| Test real con audio | ⏳ Requiere deploy |

### Dia 3: Endurecimiento + Demo

| Tarea | Estado |
|---|---|
| Fallbacks completos | ✅ Implementado |
| Feature flags probados | ⏳ Requiere deploy |
| Demo rehearsal | ⏳ |
| Video backup | ⏳ |
| README.md | ✅ |

---

## 5. Verificacion

### Comando para correr tests

```bash
# Desde la raiz del proyecto:
pytest tests/ -v --tb=short

# Tests especificos:
pytest tests/unit/test_cache.py -v          # T1-T3
pytest tests/unit/test_kb_lookup.py -v      # T4
pytest tests/unit/test_detect_lang.py -v    # T5
pytest tests/integration/test_webhook.py -v # T6-T7
pytest tests/integration/test_pipeline.py -v # T8
pytest tests/e2e/test_demo_flows.py -v      # T9-T10
```

### Comando para probar /health local

```bash
python -m src.app &
curl http://localhost:5000/health | python -m json.tool
```

### Script de cierre de fase

```bash
./scripts/phase_close.sh 1 https://civicaid-voice.onrender.com
# Genera: docs/07-evidence/phase-1-close-report.md
```

---

## 6. Procedimiento de Cierre de Fase

Al cerrar Fase N:

1. **Docs**: Actualizar `PHASE-STATUS.md` + escribir `PHASE-N-EVIDENCE.md`
2. **Notion**: Actualizar Phase Releases DB + mover tareas a Hecho + registrar latencias
3. **GitHub**: Commit + push + tag `phase-N-vX.Y` + cerrar issues
4. **Visuales**: Actualizar Mermaid si hubo cambios de arquitectura
5. **Logs**: Ejecutar `./scripts/phase_close.sh N [URL]` y guardar output en `docs/07-evidence/logs/`

Ver checklist completo en [`docs/07-evidence/PHASE-CLOSE-CHECKLIST.md`](../07-evidence/PHASE-CLOSE-CHECKLIST.md).
