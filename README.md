# Clara — CivicAid Voice

> **Resumen en una linea:** Asistente conversacional multicanal (Web + WhatsApp) que ayuda a personas vulnerables en Espana a navegar ayudas y tramites del gobierno espanol, en 8 idiomas, con texto y voz.

**Demo en vivo:** [https://andreavilaro0.github.io/civicaid-voice/](https://andreavilaro0.github.io/civicaid-voice/)

## Que es

Clara es un **asistente conversacional** accesible por web y WhatsApp que orienta sobre el gobierno espanol:

- **Ayudas** — Prestaciones, subsidios y programas sociales disponibles
- **Definiciones** — Explicacion clara de conceptos administrativos y legales
- **Links** — Enlaces directos a webs oficiales y formularios
- **Procesos** — Guia paso a paso de tramites y gestiones gubernamentales

Soporta texto, audio (via Gemini/ElevenLabs) e imagenes. Responde en **8 idiomas**: espanol, ingles, frances, portugues, rumano, catalan, chino y arabe.

## Para quien

- **Personas vulnerables en Espana:** inmigrantes, mayores, personas en riesgo de exclusion social.
- **Jurado del hackathon OdiseIA4Good:** Para evaluar el proyecto.
- **Desarrolladores:** Para contribuir o extender la funcionalidad.

## Que incluye

### Frontend Web (React)
- Landing page multilingue con 6 secciones (problema, personas, guia, plan, exito, CTA)
- Chat interactivo con texto, voz y subida de documentos
- Mascota 3D animada (Spline) con estados reactivos (idle/greeting/thinking/talking)
- 5 paginas: Home, Chat, Como Usar, Quienes Somos, Futuro
- 8 idiomas con traduccion completa
- Desplegado en GitHub Pages

### Backend (Python/Flask)
- Pipeline de 13 skills para procesamiento de mensajes
- 8 respuestas precalculadas en cache para demo
- 50 feature flags configurables
- RAG con busqueda hibrida (BM25 + vector) sobre PostgreSQL + pgvector
- 8 tramites en base de conocimiento (IMV, empadronamiento, tarjeta sanitaria, NIE/TIE, paro, alquiler, discapacidad, justicia gratuita)
- TTS con ElevenLabs (voz Sara Martin)
- 469+ tests automatizados (443 unit + 26 integration)
- Desplegado en Render

---

**Hackathon:** OdiseIA4Good — UDIT | **Fecha:** Febrero 2026 | **Estado:** Fases 0-5 completadas

## Arquitectura

```
                      ┌─────────────────────────────────────┐
                      │         Frontend (React)             │
                      │   GitHub Pages / Vite / Tailwind     │
                      │   8 idiomas, voz, chat, mascota 3D   │
                      └──────────────┬──────────────────────┘
                                     │ HTTPS
                      ┌──────────────▼──────────────────────┐
                      │         Backend (Flask)               │
                      │   Render / Docker / Gunicorn          │
                      │   Pipeline: 13 skills + Gemini 2.5    │
                      └──────────────┬──────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
      ┌───────▼───────┐    ┌────────▼────────┐    ┌───────▼───────┐
      │   WhatsApp     │    │   Knowledge     │    │   TTS          │
      │   (Meta API)   │    │   Base (JSON)   │    │   (ElevenLabs) │
      └───────────────┘    └─────────────────┘    └───────────────┘
```

## Inicio Rapido

### Frontend (React)

```bash
cd front
npm install
npm run dev
# > http://localhost:5173
```

Para desplegar en GitHub Pages:

```bash
cd front
npm run deploy
# > https://andreavilaro0.github.io/civicaid-voice/
```

### Backend (Python)

```bash
cd back
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Editar con claves reales
bash scripts/run-local.sh
# > http://localhost:5000/health
```

Variables de entorno necesarias:

```bash
GEMINI_API_KEY=AIzaxxxxxxxx
ELEVENLABS_API_KEY=xxxxxxxx
# Para WhatsApp (opcional):
META_WHATSAPP_TOKEN=xxxxxxxx
META_PHONE_NUMBER_ID=xxxxxxxx
```

---

## Estructura del Proyecto

```
civicaid-voice/
├── front/                         # Frontend React (Vite + Tailwind)
│   ├── src/
│   │   ├── pages/                 # 5 paginas (Home, Chat, ComoUsar, QuienesSomos, Futuro)
│   │   ├── components/            # 20 componentes (chat, welcome, UI)
│   │   ├── hooks/                 # 4 hooks (useChat, useAudioPlayer, useAudioRecorder, useMascotState)
│   │   ├── contexts/              # MascotContext (estado de la mascota 3D)
│   │   └── lib/                   # API client, i18n, types, constants
│   ├── index.html
│   └── package.json
├── back/                          # Backend Python (Flask + Gemini)
│   ├── src/
│   │   ├── app.py                 # Punto de entrada Flask
│   │   ├── routes/                # webhook, health, admin, static_files
│   │   ├── core/
│   │   │   ├── config.py          # 50 feature flags
│   │   │   ├── pipeline.py        # Orquestador de 13 skills
│   │   │   ├── guardrails.py      # Seguridad pre/post
│   │   │   ├── skills/            # 13 skills (LLM, TTS, vision, etc.)
│   │   │   └── prompts/           # System prompt + plantillas
│   │   └── utils/                 # logger, timing, observability
│   ├── data/
│   │   ├── cache/                 # Respuestas pre-calculadas + MP3s
│   │   └── tramites/              # 8 KBs JSON
│   ├── tests/                     # 469+ tests
│   ├── Dockerfile
│   └── render.yaml
├── clase/                         # Material escolar (presentacion, branding)
├── docs/                          # Documentacion tecnica
├── CLAUDE.md                      # Contexto para Claude Code
└── README.md
```

---

## Tests

```bash
# Backend
cd back && pytest tests/ -v --tb=short

# Frontend (build check)
cd front && npm run build
```

---

## Deploy

| Componente | Plataforma | URL |
|------------|-----------|-----|
| Frontend | GitHub Pages | [andreavilaro0.github.io/civicaid-voice](https://andreavilaro0.github.io/civicaid-voice/) |
| Backend | Render | civicaid-voice.onrender.com |
| WhatsApp | Meta Cloud API | Via webhook |

---

## Tech Stack

| Capa | Tecnologia |
|------|-----------|
| Frontend | React 19, TypeScript 5.9, Vite 7, Tailwind 4, Spline 3D |
| Backend | Python 3.11, Flask, Gemini 2.5 Flash, ElevenLabs |
| Infra | GitHub Pages (front), Render/Docker (back) |
| WhatsApp | Meta Cloud API |
| Base de conocimiento | JSON (8 tramites), RAG con pgvector (opcional) |

---

## Equipo

| Persona | Rol |
|---------|-----|
| Robert | Backend lead, pipeline, presentador de demo |
| Marcos | Routes, Twilio, deploy, pipeline de audio |
| Lucas | Investigacion KB, testing, assets de demo |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordinacion, frontend |

---

## Documentacion

Indice completo: [docs/00-DOCS-INDEX.md](docs/00-DOCS-INDEX.md)

---

## Licencia

Proyecto de hackathon OdiseIA4Good — UDIT (Febrero 2026). Uso educativo.
