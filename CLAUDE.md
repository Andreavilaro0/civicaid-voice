# CivicAid Voice / Clara — Contexto para Claude Code

## Proyecto

**Clara** es un asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar tramites de servicios sociales (IMV, Empadronamiento, Tarjeta Sanitaria). Soporta texto, audio (Whisper) e imagenes. Responde en espanol y frances.

- **Hackathon:** OdiseIA4Good — UDIT (Feb 2026)
- **Repo:** /Users/andreaavila/Documents/hakaton/civicaid-voice
- **Stack:** Python 3.11, Flask, Twilio WhatsApp, Whisper base, Gemini 1.5 Flash, Docker, Render
- **Estado:** Fase 1 MVP — codigo completo, tests 32/32, deploy pendiente

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
    pipeline.py             # Orquestador de 10 skills
    twilio_client.py        # Wrapper Twilio REST
    skills/                 # 10 skills atomicas
    prompts/                # system_prompt.py, templates.py
  utils/
    logger.py               # Logging estructurado
    timing.py               # Decorador timing
data/
  cache/demo_cache.json     # 8 respuestas pre-calculadas + 6 MP3s
  tramites/*.json           # 3 KBs (IMV, empadronamiento, tarjeta_sanitaria)
tests/
  unit/ (21 tests)          # cache, config, detect_input, detect_lang, kb_lookup
  integration/ (7 tests)    # pipeline, twilio_stub, webhook
  e2e/ (4 tests)            # demo_flows
```

## Feature Flags

| Flag | Default | Efecto |
|------|---------|--------|
| DEMO_MODE | false | Cache-only, skip LLM tras cache miss |
| LLM_LIVE | true | Habilita Gemini |
| WHISPER_ON | true | Habilita transcripcion audio |
| LLM_TIMEOUT | 6 | Segundos max Gemini |
| WHISPER_TIMEOUT | 12 | Segundos max Whisper |

## Documentacion

| Documento | Path |
|-----------|------|
| Plan Fase 1 (ejecutable) | docs/01-phases/FASE1-IMPLEMENTACION-MVP.md |
| Plan Maestro (Fase 0) | docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md |
| Arquitectura + diagramas | docs/02-architecture/ARCHITECTURE.md |
| Runbook Demo | docs/03-runbooks/RUNBOOK-DEMO.md |
| Test Plan (T1-T10) | docs/04-testing/TEST-PLAN.md |
| Deploy Render | docs/05-ops/RENDER-DEPLOY.md |
| Notion OS | docs/06-integrations/NOTION-OS.md |
| Evidence Ledger | docs/07-evidence/PHASE-1-EVIDENCE.md |
| Phase Status (semaforo) | docs/07-evidence/PHASE-STATUS.md |
| Close Checklist | docs/07-evidence/PHASE-CLOSE-CHECKLIST.md |
| Executive Summary | docs/00-EXECUTIVE-SUMMARY.md |

## Scripts

| Script | Uso |
|--------|-----|
| scripts/run-local.sh | Correr app local (venv + deps + Flask) |
| scripts/phase_close.sh | Generar reporte de cierre: `./scripts/phase_close.sh 1 [RENDER_URL]` |
| scripts/populate_notion.sh | Poblar 3 DBs de Notion (33 entries) |
| scripts/tmux_team_up.sh | Setup de paneles tmux |

## Notion

- **Backlog DB:** 304c5a0f-372a-81de-92a8-f54c03b391c0
- **KB Tramites DB:** 304c5a0f-372a-81ff-9d45-c785e69f7335
- **Testing DB:** 304c5a0f-372a-810d-8767-d77efbd46bb2
- **Token:** Configurado en ~/.mcp.json (NOTION_TOKEN)
- **Estado:** DBs vacias — ejecutar `bash scripts/populate_notion.sh` para poblar 33 entries
- **MCP:** Requiere reinicio de Claude Code tras cambiar token en ~/.mcp.json

## Agent Teams (6 paneles)

El proyecto usa un modelo de 6 agentes especializados con un lead en modo delegate-only:

| # | Nombre | Scope | Skills/MCP |
|---|--------|-------|------------|
| 1 | DevOps/Infra | Dockerfile, render.yaml, scripts/* | docker-expert, github-actions-creator, devops-engineer |
| 2 | Backend/Pipeline | src/core/*, src/routes/*, src/app.py | general-purpose |
| 3 | QA/Testing | tests/**, .github/**, pyproject.toml | general-purpose |
| 4 | Notion Ops | docs/06-integrations/*, Notion MCP | notion-ops, notion-knowledge-capture |
| 5 | Docs/Architecture | docs/01-03/* | general-purpose |
| 6 | Release/PM | docs/01-phases/FASE1*, docs/07-evidence/* | general-purpose |

**Regla:** El lead solo coordina y sintetiza. Todo trabajo lo hacen los teammates. Ningun teammate edita fuera de su scope.

## Fixes Aplicados (Fase 1 Hardening)

1. DEMO_MODE implementado en pipeline.py (era dead code)
2. WHISPER_ON short-circuit para audio
3. Twilio REST timeout (10s) en send_response.py
4. NumMedia safe parsing (try/except) en webhook.py
5. Silent thread death protection en pipeline.py
6. Twilio webhook signature validation (RequestValidator) en webhook.py
7. Docker build fix (setuptools<75 + --no-build-isolation para whisper)
8. .dockerignore creado
9. Unused import time removido de logger.py

## Estado Actual de Gates

| Gate | Estado | Evidencia |
|------|--------|-----------|
| G0 Tooling | PASS | Skills, agents, MCP, Notion DBs |
| G1 Texto | PASS (codigo) | 32/32 tests, ruff clean, cache-first OK. PENDING: deploy |
| G2 Audio | PASS (codigo) | Pipeline completo, timeouts, feature flags. PENDING: test real |
| G3 Demo | PENDING | Falta: deploy Render, Twilio webhook, rehearsal |

## Bloqueantes

1. **Notion DBs vacias** — Ejecutar `bash scripts/populate_notion.sh` (token ya configurado, requiere reinicio MCP)
2. **Deploy Render** — Push a GitHub, trigger deploy, verificar /health
3. **Twilio webhook** — Configurar URL en Twilio console
4. **Demo rehearsal** — Ejecutar WOW 1 + WOW 2 en vivo

## Comandos Rapidos

```bash
# Tests
pytest tests/ -v --tb=short

# Lint
ruff check src/ tests/ --select E,F,W --ignore E501

# Local
bash scripts/run-local.sh

# Docker
docker build -t civicaid-voice:test . && docker run -p 5000:5000 --env-file .env civicaid-voice:test

# Health
curl http://localhost:5000/health | python3 -m json.tool

# Cierre de fase
./scripts/phase_close.sh 1 https://civicaid-voice.onrender.com

# Poblar Notion
bash scripts/populate_notion.sh
```

## Equipo Humano

| Persona | Rol |
|---------|-----|
| Robert | Backend lead, pipeline, demo presenter |
| Marcos | Routes, Twilio, deploy, audio pipeline |
| Lucas | KB research, testing, demo assets |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordination |
