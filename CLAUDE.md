# CivicAid Voice / Clara — Contexto para Claude Code

## Proyecto

**Clara** es un asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar ayudas, definiciones, links y procesos del gobierno espanol. Soporta texto, audio (Whisper) e imagenes. Responde en espanol y frances.

- **Hackathon:** OdiseIA4Good — UDIT (Feb 2026)
- **Repo:** /Users/andreaavila/Documents/hakaton/civicaid-voice
- **Stack:** Python 3.11, Flask, Twilio WhatsApp, Whisper base, Gemini 1.5 Flash, Docker, Render
- **KB:** Extensible — cualquier .json en data/tramites/ con campo "keywords" se carga automaticamente
- **Estado:** Fases 0-3 cerradas, Fase 4 en curso

## Arquitectura

```
Usuario WhatsApp -> Twilio -> Flask /webhook -> TwiML ACK (<1s)
                                             -> Background Thread:
                                               cache_match -> HIT -> Twilio REST -> Usuario
                                               cache_match -> MISS -> KB + Gemini -> Twilio REST -> Usuario
```

Patron **TwiML ACK**: respuesta HTTP 200 inmediata, procesamiento en hilo de fondo, envio final via Twilio REST API.

## Estructura del Codigo

```
src/
  app.py                    # Flask entry point — create_app()
  routes/
    webhook.py              # POST /webhook — Twilio, con signature validation
    health.py               # GET /health — healthcheck
    static_files.py         # GET /static/cache/* — servir MP3s
  core/
    config.py               # Feature flags (DEMO_MODE, LLM_LIVE, WHISPER_ON, timeouts)
    models.py               # 8 dataclasses (IncomingMessage, CacheEntry, FinalResponse, etc.)
    cache.py                # Carga demo_cache.json
    pipeline.py             # Orquestador de 11 skills
    twilio_client.py        # Wrapper Twilio REST
    guardrails.py           # Capa de seguridad pre/post
    models_structured.py    # Salidas JSON estructuradas
    retriever.py            # RAG stub (futuro)
    skills/                 # 11 skills atomicas (incl. tts.py)
    prompts/                # system_prompt.py, templates.py
  utils/
    logger.py               # Logging estructurado
    eval_runner.py           # Runner de evaluaciones
    timing.py               # Decorador timing
    observability.py         # RequestContext + hooks Flask
data/
  cache/demo_cache.json     # 8 respuestas pre-calculadas + 6 MP3s
  evals/*.json              # 5 archivos de evaluacion
  tramites/*.json           # 3 KBs (IMV, empadronamiento, tarjeta_sanitaria)
tests/
  unit/ (85 tests)          # cache, config, detect_input, detect_lang, kb_lookup, guardrails, evals, redteam, retriever, structured_outputs, observability, transcribe
  integration/ (7 tests)    # pipeline, twilio_stub, webhook
  e2e/ (4 tests)            # demo_flows
  # Total: 96 tests (91 passed + 5 xpassed)
```

## Feature Flags (config.py)

| Flag | Default | Efecto |
|------|---------|--------|
| DEMO_MODE | false | Cache-only, skip LLM tras cache miss |
| LLM_LIVE | true | Habilita Gemini |
| WHISPER_ON | true | Habilita transcripcion audio |
| LLM_TIMEOUT | 6 | Segundos max Gemini |
| WHISPER_TIMEOUT | 12 | Segundos max Whisper |
| GUARDRAILS_ON | true | Habilita guardrails de contenido |
| STRUCTURED_OUTPUT_ON | false | Habilita salida estructurada JSON |
| OBSERVABILITY_ON | true | Habilita metricas y trazas |
| RAG_ENABLED | false | Habilita RAG (stub, pendiente implementacion) |

> **Nota:** TWILIO_TIMEOUT (10s) esta hardcodeado en `src/core/skills/send_response.py`, no es un flag en config.py.

## Documentacion

| Documento | Path |
|-----------|------|
| Resumen Ejecutivo | docs/00-EXECUTIVE-SUMMARY.md |
| Indice de Documentacion | docs/00-DOCS-INDEX.md |
| Fase 4 — Ideacion | docs/01-phases/FASE4-IDEACION.md |
| Fase 4 — Plan | docs/01-phases/FASE4-PLAN.md |
| Fase 4 — Arquitectura | docs/01-phases/FASE4-PLAN-ARQUITECTURA.md |
| Arquitectura + diagramas | docs/02-architecture/ARCHITECTURE.md |
| Observabilidad | docs/02-architecture/OBSERVABILITY.md |
| Propuesta Arq Fase 4 | docs/02-architecture/FASE4-ARCHITECTURE-PROPOSAL.md |
| Runbook Demo | docs/03-runbooks/RUNBOOK-DEMO.md |
| Test Plan (T1-T10) | docs/04-testing/TEST-PLAN.md |
| Framework de Evals | docs/04-testing/EVALS.md |
| Deploy Render | docs/05-ops/RENDER-DEPLOY.md |
| Observability Quickstart | docs/05-ops/OBSERVABILITY-QUICKSTART.md |
| Guia Twilio | docs/06-integrations/TWILIO-SETUP-GUIDE.md |
| Notion OS | docs/06-integrations/NOTION-OS.md |
| Guardrails | docs/06-integrations/GUARDRAILS.md |
| Structured Outputs | docs/06-integrations/STRUCTURED_OUTPUTS.md |
| RAG Opcional | docs/06-integrations/RAG_OPTIONAL.md |
| Guia Jueces | docs/06-integrations/JUDGES-QUICK-EVAL.md |
| Tono y Voz Clara | docs/08-marketing/CLARA-TONE-VOICE-GUIDE.md |
| Narrativa Jueces | docs/08-marketing/NARRATIVA-JUECES-FASE4.md |
| UX y Accesibilidad | docs/08-ux/PHASE4-UX-ACCESSIBILITY-ANALYSIS.md |
| Doc Tecnico Sprint 3 | docs/09-academic/Sprint3_DocTecnico.md |
| Presentacion Sprint 3 | docs/09-academic/Sprint3_Presentacion.md |

## Scripts

| Script | Uso |
|--------|-----|
| scripts/run-local.sh | Correr app local (venv + deps + Flask) |
| scripts/run_evals.py | Runner de evaluaciones (16 casos, 4 sets) |

## Notion

- **Backlog DB:** 304c5a0f-372a-81de-92a8-f54c03b391c0
- **KB Tramites DB:** 304c5a0f-372a-81ff-9d45-c785e69f7335
- **Testing DB:** 304c5a0f-372a-810d-8767-d77efbd46bb2
- **Token:** Configurado en ~/.mcp.json (NOTION_TOKEN)
- **Estado:** 81 entradas pobladas (43 Backlog + 12 KB Tramites + 26 Testing)

## Comandos Rapidos

```bash
# Tests
pytest tests/ -v --tb=short

# Lint
ruff check src/ tests/ --select E,F,W --ignore E501

# Local
bash scripts/run-local.sh

# Docker
docker build -t civicaid-voice . && docker run -p 10000:10000 --env-file .env civicaid-voice

# Health
curl http://localhost:5000/health | python3 -m json.tool

# Evals
python scripts/run_evals.py
```

## Equipo Humano

| Persona | Rol |
|---------|-----|
| Robert | Backend lead, pipeline, demo presenter |
| Marcos | Routes, Twilio, deploy, audio pipeline |
| Lucas | KB research, testing, demo assets |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordination |
