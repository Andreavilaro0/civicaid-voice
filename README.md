# Clara — CivicAid Voice

> Asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar tramites de servicios sociales.

**Hackathon:** OdiseIA4Good — UDIT (Feb 2026)
**Estado:** Fase 1 MVP en progreso

---

## Que es Clara

Clara es un chatbot de WhatsApp que responde preguntas sobre:
- **Ingreso Minimo Vital (IMV)** — prestacion economica
- **Empadronamiento** — registro municipal
- **Tarjeta Sanitaria** — acceso a sanidad publica

Soporta texto, audio (via Whisper) e imagenes. Responde en espanol y frances.

## Arquitectura

```
Usuario WhatsApp → Twilio → Flask /webhook → TwiML ACK (< 1s)
                                            → Background Thread:
                                              cache_match → HIT → Twilio REST → Usuario
                                              cache_match → MISS → KB + Gemini → Twilio REST → Usuario
```

Patron **TwiML ACK**: respuesta HTTP 200 inmediata, procesamiento en hilo de fondo, envio final via Twilio REST API.

Ver documentacion completa en [`docs/02-architecture/ARCHITECTURE.md`](docs/02-architecture/ARCHITECTURE.md).

## Quick Start

### Requisitos
- Python 3.11+
- ffmpeg (`brew install ffmpeg` / `apt-get install ffmpeg`)

### Local macOS (sin audio)

```bash
git clone https://github.com/YOUR-ORG/civicaid-voice.git
cd civicaid-voice
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # ligero, sin torch/whisper
cp .env.example .env              # Rellenar con claves reales
```

Texto, cache y LLM funcionan sin whisper. Audio queda deshabilitado (`whisper_loaded: false` en `/health`).

### Audio opcional (macOS)

```bash
INSTALL_AUDIO=1 ./scripts/run-local.sh
# o manualmente:
pip install "setuptools<75" wheel
pip install --no-build-isolation -r requirements-audio.txt
```

Si la instalacion falla, el servidor arranca igual (solo texto).

> **Nota:** En Docker/Render, whisper se instala siempre via Dockerfile. No necesitas hacer nada extra.

### Variables de entorno (.env)

```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_SANDBOX_FROM=whatsapp:+14155238886
GEMINI_API_KEY=AIzaxxxxxxxx
DEMO_MODE=true          # Cache-first para demo
LLM_LIVE=true           # Habilitar Gemini
WHISPER_ON=true          # Habilitar transcripcion audio
LLM_TIMEOUT=6            # Segundos
WHISPER_TIMEOUT=12       # Segundos
AUDIO_BASE_URL=https://civicaid-voice.onrender.com/static/cache
```

### Correr local

```bash
python -m src.app
# → http://localhost:5000/health
```

### Correr tests

```bash
pytest tests/ -v --tb=short
# 32 tests: 21 unit + 7 integration + 4 e2e
```

### Docker

```bash
docker build -t civicaid-voice .
docker run -p 5000:5000 --env-file .env civicaid-voice
```

## Estructura del Proyecto

```
civicaid-voice/
├── src/
│   ├── app.py                  # Flask entry point
│   ├── routes/                 # webhook, health, static_files
│   ├── core/
│   │   ├── config.py           # Feature flags
│   │   ├── models.py           # 8 dataclasses
│   │   ├── cache.py            # demo_cache.json loader
│   │   ├── pipeline.py         # Orchestrator
│   │   ├── skills/             # 9 atomic skills
│   │   └── prompts/            # System prompt + templates
│   └── utils/                  # Logger + timing
├── data/
│   ├── cache/                  # demo_cache.json + 6 MP3s
│   └── tramites/               # 3 KB JSONs (IMV, empadronamiento, tarjeta)
├── tests/                      # 32 tests (unit/integration/e2e)
├── docs/                       # Documentacion completa
├── scripts/                    # Scripts de operacion
├── Dockerfile                  # Python 3.11 + ffmpeg + gunicorn
├── render.yaml                 # Render Blueprint
├── requirements.txt            # Core dependencies (9 packages)
└── requirements-audio.txt      # Whisper/audio (optional on macOS, always in Docker)
```

## Deploy (Render)

Ver [`docs/05-ops/RENDER-DEPLOY.md`](docs/05-ops/RENDER-DEPLOY.md) para guia completa.

Resumen:
1. Crear Web Service en Render → conectar GitHub → Docker
2. Configurar env vars
3. Deploy → verificar `/health`
4. Configurar Twilio webhook → `https://URL/webhook` POST
5. cron-job.org → `https://URL/health` cada 8 min

## Documentacion

| Documento | Ruta |
|---|---|
| Plan Maestro (Fase 0) | [`docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md`](docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md) |
| Implementacion MVP (Fase 1) | [`docs/01-phases/FASE1-IMPLEMENTACION-MVP.md`](docs/01-phases/FASE1-IMPLEMENTACION-MVP.md) |
| Arquitectura + diagramas | [`docs/02-architecture/`](docs/02-architecture/) |
| Runbook Demo | [`docs/03-runbooks/RUNBOOK-DEMO.md`](docs/03-runbooks/RUNBOOK-DEMO.md) |
| Plan de Tests (T1-T10) | [`docs/04-testing/TEST-PLAN.md`](docs/04-testing/TEST-PLAN.md) |
| Deploy Render | [`docs/05-ops/RENDER-DEPLOY.md`](docs/05-ops/RENDER-DEPLOY.md) |
| Notion OS | [`docs/06-integrations/NOTION-OS.md`](docs/06-integrations/NOTION-OS.md) |
| Estado de Fases | [`docs/07-evidence/PHASE-STATUS.md`](docs/07-evidence/PHASE-STATUS.md) |

## Equipo

| Persona | Rol |
|---|---|
| Robert | Backend lead, pipeline, demo presenter |
| Marcos | Routes, Twilio, deploy, audio pipeline |
| Lucas | KB research, testing, demo assets |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordination |

## Licencia

Proyecto de hackathon. Uso educativo.
