# Clara — CivicAid Voice

> **Resumen en una linea:** Asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar ayudas, definiciones, links y procesos del gobierno espanol, respondiendo en su idioma con texto y audio.

## Que es

Clara es un **chatbot de WhatsApp** que orienta sobre el gobierno espanol:

- **Ayudas** — Prestaciones, subsidios y programas sociales disponibles
- **Definiciones** — Explicacion clara de conceptos administrativos y legales
- **Links** — Enlaces directos a webs oficiales y formularios
- **Procesos** — Guia paso a paso de tramites y gestiones gubernamentales

Soporta texto, audio (via Gemini/Whisper) e imagenes. Responde en 2 idiomas: espanol y frances.

## Para quien

- **Personas vulnerables en Espana:** inmigrantes, mayores, personas en riesgo de exclusion social.
- **Jurado del hackathon OdiseIA4Good:** Para evaluar el proyecto.
- **Desarrolladores:** Para contribuir o extender la funcionalidad.

## Que incluye

- Pipeline de 11 skills para procesamiento de mensajes.
- 8 respuestas precalculadas en cache para demo.
- 26 feature flags configurables (12 nuevos en Q4).
- RAG con busqueda hibrida (BM25 + vector) sobre PostgreSQL + pgvector.
- 8 tramites en base de conocimiento (IMV, empadronamiento, tarjeta sanitaria, NIE/TIE, paro, alquiler, discapacidad, justicia gratuita).
- 469+ tests automatizados (443 unit + 26 integration).
- Documentacion completa ([ver indice](docs/00-DOCS-INDEX.md)).

## Que NO incluye

- Interfaz web (solo WhatsApp).
- Soporte multiusuario persistente (sin sesiones).

---

**Hackathon:** OdiseIA4Good — UDIT | **Fecha:** Febrero 2026 | **Estado:** Fase 4 completada

## Arquitectura

```
Usuario WhatsApp > Twilio > Flask /webhook > TwiML ACK (< 1s)
                                            > Hilo de fondo:
                                              cache_match > HIT > Twilio REST > Usuario
                                              cache_match > MISS > KB + Gemini > Twilio REST > Usuario
```

Patron **TwiML ACK**: respuesta HTTP 200 inmediata, procesamiento en hilo de fondo, envio final via Twilio REST API.

Documentacion completa de arquitectura: [docs/02-architecture/ARCHITECTURE.md](docs/02-architecture/ARCHITECTURE.md)

---

## Inicio Rapido (5 pasos)

### Requisitos Previos

- **Python 3.11+**
- **ffmpeg** (`brew install ffmpeg` en macOS / `apt-get install ffmpeg` en Linux)
- Cuenta de **Twilio** (sandbox gratuito)
- Clave API de **Google Gemini**

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/YOUR-ORG/civicaid-voice.git
cd civicaid-voice
```

### Paso 2: Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instala las 10 dependencias core (Flask, Twilio, Gemini, gTTS, langdetect, etc.). Texto, cache y LLM funcionan sin Whisper. El audio queda deshabilitado (`whisper_loaded: false` en `/health`).

### Paso 4: Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con las claves reales:

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

### Paso 5: Ejecutar

```bash
bash scripts/run-local.sh
# O directamente:
python -m src.app
# > http://localhost:5000/health
```

---

## Audio Opcional (macOS)

En macOS, Whisper se puede instalar manualmente si se necesita transcripcion local:

```bash
INSTALL_AUDIO=1 ./scripts/run-local.sh
# O manualmente:
pip install "setuptools<75" wheel
pip install --no-build-isolation -r requirements-audio.txt
```

Si la instalacion falla, el servidor arranca igual (solo texto).

> **Nota:** En Docker/Render, la configuracion de audio se maneja automaticamente. No es necesario hacer nada extra.

---

## Tests

```bash
# Ejecutar los 96 tests
pytest tests/ -v --tb=short

# Ejecucion rapida
pytest tests/ -q

# Solo tests unitarios
pytest tests/unit/ -v

# Solo tests de integracion
pytest tests/integration/ -v

# Solo tests end-to-end
pytest tests/e2e/ -v
```

Resultado esperado: **96 tests** (91 passed + 5 xpassed).

---

## Lint

```bash
ruff check src/ tests/ --select E,F,W --ignore E501
```

---

## Docker

```bash
# Construir imagen
docker build -t civicaid-voice .

# Ejecutar contenedor
docker run -p 10000:10000 --env-file .env civicaid-voice

# Verificar salud
curl http://localhost:10000/health | python3 -m json.tool
```

El Dockerfile usa Python 3.11, gunicorn con 1 worker, y expone el puerto 10000 (compatible con Render). En local sin Docker, el puerto por defecto es 5000.

---

## Deploy en Render

Guia completa: [docs/05-ops/RENDER-DEPLOY.md](docs/05-ops/RENDER-DEPLOY.md)

Resumen:

1. Crear Web Service en Render > conectar GitHub > Docker
2. Configurar variables de entorno (puerto 10000)
3. Deploy > verificar `/health`
4. Configurar Twilio webhook > `https://URL/webhook` POST
5. Configurar cron en cron-job.org > `https://URL/health` cada 14 minutos

---

## Estructura del Proyecto

```
civicaid-voice/
├── src/
│   ├── app.py                    # Punto de entrada Flask — create_app()
│   ├── routes/
│   │   ├── webhook.py            # POST /webhook — entrada de Twilio
│   │   ├── health.py             # GET /health — 8 componentes
│   │   └── static_files.py       # GET /static/cache/* — audios MP3
│   ├── core/
│   │   ├── config.py             # 9 feature flags
│   │   ├── models.py             # 8 dataclasses
│   │   ├── cache.py              # Carga demo_cache.json
│   │   ├── pipeline.py           # Orquestador de 11 skills
│   │   ├── guardrails.py         # Capa de seguridad pre/post
│   │   ├── skills/               # 11 skills atomicas
│   │   └── prompts/              # System prompt + plantillas
│   └── utils/
│       ├── logger.py             # 7 funciones de logging con tags
│       ├── timing.py             # Decorador @timed
│       └── observability.py      # RequestContext + hooks Flask
├── data/
│   ├── cache/                    # demo_cache.json (8 entradas) + 6 MP3s
│   └── tramites/                 # 3 KBs JSON (IMV, empadronamiento, tarjeta)
├── tests/                        # 96 tests (unit/integration/e2e)
├── docs/                         # 29 documentos (ver indice)
├── scripts/                      # Scripts de operacion
├── Dockerfile                    # Python 3.11 + gunicorn (puerto 10000)
├── render.yaml                   # Render Blueprint
├── pyproject.toml                # Configuracion proyecto + ruff + pytest
├── requirements.txt              # 10 dependencias core
└── requirements-audio.txt        # Whisper/audio (opcional en macOS)
```

---

## Feature Flags

| # | Flag | Default | Descripcion |
|---|------|---------|-------------|
| 1 | `DEMO_MODE` | `false` | Modo demo: cache-only, skip LLM tras cache miss |
| 2 | `LLM_LIVE` | `true` | Habilitar llamadas a Gemini |
| 3 | `WHISPER_ON` | `true` | Habilitar transcripcion de audio |
| 4 | `LLM_TIMEOUT` | `6` | Timeout en segundos para Gemini |
| 5 | `WHISPER_TIMEOUT` | `12` | Timeout en segundos para transcripcion |
| 6 | `AUDIO_BASE_URL` | `""` | URL base para audios MP3 |
| 7 | `OBSERVABILITY_ON` | `true` | Habilitar request_id y logs [OBS] |
| 8 | `GUARDRAILS_ON` | `true` | Habilitar capa de seguridad pre/post |
| 9 | `STRUCTURED_OUTPUT_ON` | `false` | Habilitar salidas JSON estructuradas |
| 10 | `RAG_ENABLED` | `false` | Habilitar vector store (stub, futuro) |

---

## Modulos Opcionales del Toolkit

| Modulo | Flag | Default | Archivo | Documentacion |
|--------|------|---------|---------|---------------|
| Observabilidad | `OBSERVABILITY_ON` | `true` | `src/utils/observability.py` | [OBSERVABILITY.md](docs/02-architecture/OBSERVABILITY.md) |
| Guardrails | `GUARDRAILS_ON` | `true` | `src/core/guardrails.py` | [GUARDRAILS.md](docs/06-integrations/GUARDRAILS.md) |
| Structured Outputs | `STRUCTURED_OUTPUT_ON` | `false` | `src/core/models_structured.py` | [STRUCTURED_OUTPUTS.md](docs/06-integrations/STRUCTURED_OUTPUTS.md) |
| RAG (vector store) | `RAG_ENABLED` | `false` | `src/core/retriever.py` | [RAG_OPTIONAL.md](docs/06-integrations/RAG_OPTIONAL.md) |

---

## Verificacion

```bash
# Todos los tests
pytest tests/ -q

# Suite de evaluacion
python scripts/run_evals.py

# Health check local
curl http://localhost:5000/health | python3 -m json.tool
```

---

## Documentacion

Indice completo: [docs/00-DOCS-INDEX.md](docs/00-DOCS-INDEX.md)

| Documento | Ruta |
|-----------|------|
| Resumen Ejecutivo | [docs/00-EXECUTIVE-SUMMARY.md](docs/00-EXECUTIVE-SUMMARY.md) |
| Indice de Documentacion | [docs/00-DOCS-INDEX.md](docs/00-DOCS-INDEX.md) |
| Arquitectura + diagramas | [docs/02-architecture/ARCHITECTURE.md](docs/02-architecture/ARCHITECTURE.md) |
| Observabilidad | [docs/02-architecture/OBSERVABILITY.md](docs/02-architecture/OBSERVABILITY.md) |
| Runbook Demo | [docs/03-runbooks/RUNBOOK-DEMO.md](docs/03-runbooks/RUNBOOK-DEMO.md) |
| Plan de Tests (T1-T10) | [docs/04-testing/TEST-PLAN.md](docs/04-testing/TEST-PLAN.md) |
| Deploy en Render | [docs/05-ops/RENDER-DEPLOY.md](docs/05-ops/RENDER-DEPLOY.md) |
| Guia de Twilio | [docs/06-integrations/TWILIO-SETUP-GUIDE.md](docs/06-integrations/TWILIO-SETUP-GUIDE.md) |
| Notion OS | [docs/06-integrations/NOTION-OS.md](docs/06-integrations/NOTION-OS.md) |
| Fase 4 — Plan | [docs/01-phases/FASE4-PLAN.md](docs/01-phases/FASE4-PLAN.md) |

---

## Equipo

| Persona | Rol |
|---------|-----|
| Robert | Backend lead, pipeline, presentador de demo |
| Marcos | Routes, Twilio, deploy, pipeline de audio |
| Lucas | Investigacion KB, testing, assets de demo |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordinacion |

---

## Licencia

Proyecto de hackathon OdiseIA4Good — UDIT (Febrero 2026). Uso educativo.
