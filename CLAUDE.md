# CivicAid Voice / Clara — Contexto para Claude Code

## Proyecto

**Clara** es un asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar ayudas, definiciones, links y procesos del gobierno espanol. Soporta texto, audio (Whisper) e imagenes. Responde en espanol y frances.

- **Hackathon:** OdiseIA4Good — UDIT (Feb 2026)
- **Repo:** /Users/andreaavila/Documents/hakaton/civicaid-voice
- **Stack:** Python 3.11, Flask, Twilio WhatsApp, Whisper base, Gemini 2.5 Flash, Docker, Render
- **KB:** Extensible — cualquier .json en data/tramites/ con campo "keywords" se carga automaticamente
- **RAG:** PostgreSQL + pgvector, hybrid BM25+vector search, fallback chain, response cache
- **Tono:** Fase 5 completada — Clara habla como amiga del ayuntamiento (E-V-I pattern, sin emoji en ACKs)
- **Frontend:** `front/` (React + Vite, port 5173) — unico frontend activo
- **Estado (2026-02-23):** Fases 0-5 completadas, Fase 3 Q1-Q4 RAG completada (FULL PASS). clara-web/ eliminado, front/ es el unico frontend

## Arquitectura

```
Usuario WhatsApp -> Twilio -> Flask /webhook -> TwiML ACK (<1s)
                                             -> Background Thread:
                                               cache_match -> HIT -> Twilio REST -> Usuario
                                               cache_match -> MISS -> get_retriever() -> Gemini -> Twilio REST
                                                                      |
                                                              FallbackRetriever:
                                                                PGVector (hybrid BM25+vector)
                                                                -> JSON KB (keyword matching)
                                                                -> Directory (last resort)
```

Patron **TwiML ACK**: respuesta HTTP 200 inmediata, procesamiento en hilo de fondo, envio final via Twilio REST API.

## Estructura del Repo

```
civicaid-voice/
├── back/                          # Backend Python (Flask + Twilio + Gemini)
│   ├── src/                       # Codigo fuente
│   ├── data/                      # Knowledge base, evals, cache
│   ├── scripts/                   # Utilidades CLI
│   ├── tests/                     # Tests (unit, integration, evals, e2e)
│   ├── schemas/                   # JSON schemas
│   ├── Dockerfile, docker-compose.yml
│   ├── requirements.txt, pyproject.toml
│   └── render.yaml (rootDir: back)
├── front/                         # Frontend React + Vite (port 5173)
├── clase/                         # Material escolar
│   ├── presentacion/              # Pitch, demos HTML, PPTX, PDF, guion
│   └── design/                    # Branding, mockups, videos, marketing
├── docs/                          # Documentacion tecnica
├── CLAUDE.md
├── README.md
└── .gitignore
```

## Estructura del Backend (back/)

```
back/
  src/
    app.py                    # Flask entry point — create_app()
    routes/
      webhook.py              # POST /webhook — Twilio, con signature validation
      health.py               # GET /health — healthcheck
      static_files.py         # GET /static/cache/* — servir MP3/WAV/OGG (dynamic MIME)
      admin.py                # Admin endpoints (rag-metrics, staleness, satisfaction)
    core/
      config.py               # Feature flags (50 flags: DEMO_MODE, LLM_LIVE, VISION_*, TTS_*, RAG_*, MEMORY_*, etc.)
      models.py               # 8 dataclasses (IncomingMessage, CacheEntry, FinalResponse, KBContext, etc.)
      cache.py                # Carga demo_cache.json
      pipeline.py             # Orquestador de 12 skills — uses get_retriever().retrieve()
      twilio_client.py        # Wrapper Twilio REST
      guardrails.py           # Capa de seguridad pre/post
      models_structured.py    # Salidas JSON estructuradas
      retriever.py            # Singleton retriever factory (FallbackRetriever, PGVector, JSON, Directory)
      skills/                 # 13 skills atomicas (incl. tts.py, analyze_image.py, whatsapp_format.py)
      prompts/                # system_prompt.py, templates.py
      rag/                    # RAG infrastructure (Q2-Q4)
    utils/
      logger.py, eval_runner.py, timing.py, observability.py, rag_eval.py, rag_metrics.py
  data/
    cache/demo_cache.json     # 8 respuestas pre-calculadas + 6 MP3s
    evals/*.json              # Eval sets + reports (236 queries, P@3=86%)
    tramites/*.json           # 8 KBs (IMV, empadronamiento, tarjeta_sanitaria, NIE/TIE, etc.)
    policy/                   # Allowlist, blocklist, canonical rules
    sources/                  # Source registry (44 fuentes), local seed (20 cities)
  scripts/
    run_ingestion.py, check_drift.py, check_boe.py, run_rag_eval.py, init_db.py
  tests/
    unit/ (~500 tests), integration/ (~40 tests), evals/, e2e/ (4 tests)
```

## Feature Flags (config.py)

| Flag | Default | Efecto |
|------|---------|--------|
| DEMO_MODE | false | Cache-only, skip LLM tras cache miss |
| LLM_LIVE | true | Habilita Gemini |
| WHISPER_ON | true | Habilita transcripcion audio |
| GUARDRAILS_ON | true | Habilita guardrails de contenido |
| VISION_ENABLED | true | Habilita analisis de imagenes via Gemini Vision |
| TTS_ENGINE | "gtts" | Motor TTS: "gtts" (robotico) o "gemini" (voz calida Clara) |
| STRUCTURED_OUTPUT_ON | false | Habilita salida estructurada JSON |
| OBSERVABILITY_ON | true | Habilita metricas y trazas |
| RAG_ENABLED | false | Habilita RAG pipeline (PGVector hybrid search) |
| RAG_FALLBACK_CHAIN | true | FallbackRetriever: PGVector -> JSON -> Directory |
| RAG_CACHE_ENABLED | false | Response cache (memory LRU / Redis) |
| RAG_METRICS_ENABLED | true | RAG observability metrics |
| RAG_INGESTION_ENABLED | false | Automated ingestion pipeline |
| RAG_DRIFT_CHECK_ENABLED | false | Content drift detection |
| RAG_BOE_MONITOR_ENABLED | false | BOE RSS monitor |
| MEMORY_ENABLED | false | User memory/personalization |

> **Nota:** TWILIO_TIMEOUT (10s) esta hardcodeado en `back/src/core/skills/send_response.py`, no es un flag en config.py.

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
| Fase 5 — Voz Clara | docs/01-phases/fase5-voz-clara/FASE5-VOZ-CLARA.md |
| Referencia System Prompt | docs/CLARA-SYSTEM-PROMPT.md |
| Verificacion Fase 5 | docs/plans/evidence/VERIFY-BACK-FRONT-REPORT.md |
| Auditoria Post-Q4 | docs/plans/evidence/audit-report-2026-02-20-post-q4.md |

## Scripts (back/scripts/)

| Script | Uso |
|--------|-----|
| back/scripts/run-local.sh | Correr app local (venv + deps + Flask) |
| back/scripts/run_evals.py | Runner de evaluaciones (16 casos, 4 sets) |
| back/scripts/run_ingestion.py | CLI ingestion runner (--all, --dry-run, --force) |
| back/scripts/check_drift.py | CLI drift detection (--all, --stale, --json) |
| back/scripts/check_boe.py | CLI BOE monitor (--check, --json) |
| back/scripts/run_rag_eval.py | RAG eval runner (P@K, MRR, BM25) |
| back/scripts/init_db.py | PostgreSQL table initialization |

## Notion

- **Backlog DB:** 304c5a0f-372a-81de-92a8-f54c03b391c0
- **KB Tramites DB:** 304c5a0f-372a-81ff-9d45-c785e69f7335
- **Testing DB:** 304c5a0f-372a-810d-8767-d77efbd46bb2
- **Token:** Configurado en ~/.mcp.json (NOTION_TOKEN)
- **Estado:** 81 entradas pobladas (43 Backlog + 12 KB Tramites + 26 Testing)

## Comandos Rapidos

```bash
# Tests (desde back/)
cd back && pytest tests/ -v --tb=short

# Lint (desde back/)
cd back && ruff check src/ tests/ scripts/ --select E,F,W --ignore E501

# Local (desde back/)
cd back && bash scripts/run-local.sh

# Docker (PostgreSQL + pgvector for RAG) — desde back/
cd back && docker compose up -d
cd back && python scripts/init_db.py

# Docker (app) — desde back/
cd back && docker build -t civicaid-voice . && docker run -p 10000:10000 --env-file ../.env civicaid-voice

# Health
curl http://localhost:5000/health | python3 -m json.tool

# Frontend (front/ — React + Vite)
cd front && npm run dev

# RAG Ingestion
cd back && python scripts/run_ingestion.py --all --dry-run

# RAG Eval (requires Docker DB)
cd back && python scripts/run_rag_eval.py

# Admin metrics
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:5000/admin/rag-metrics
```

## Welcome Page — Estado Actual (2026-02-23)

- **Frontend unico:** `front/` (React + Vite, port 5173) — `clara-web/` fue eliminado
- **Audio de bienvenida:** `front/public/audio/welcome-multilingual.mp3` (unico archivo, multilingue)
- Build limpio, frontend funcional

## Equipo Humano

| Persona | Rol |
|---------|-----|
| Robert | Backend lead, pipeline, demo presenter |
| Marcos | Routes, Twilio, deploy, audio pipeline |
| Lucas | KB research, testing, demo assets |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordination |
