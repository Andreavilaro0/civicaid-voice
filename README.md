# Clara — CivicAid Voice

**Clara is a voice and chat assistant that helps people in Spain understand public aid and government procedures. It works on the web and on WhatsApp, in 8 languages, with text, voice and images.**

**Live demo:** [andreavilaro0.github.io/civicaid-voice](https://andreavilaro0.github.io/civicaid-voice/)

> The backend runs on Render. The first request after a quiet period can take around 20–30 seconds while the server wakes up.

---

## The problem

Government procedures in Spain are hard to follow. The information is spread across many official websites, it uses legal language, and it is almost always in Spanish only.

This is a real barrier for the people who need help the most: migrants, older people, and people at risk of social exclusion. Many of them use WhatsApp every day but not complex websites, and some prefer to speak instead of type.

## What Clara does

You ask Clara a question in your own language, by text or by voice. Clara answers in simple words and explains:

- **Aid** — benefits and social programmes you may be able to get (for example, the Ingreso Mínimo Vital).
- **Procedures** — step-by-step guides (for example, registering your address, getting a NIE/TIE, or a health card).
- **Definitions** — what administrative and legal terms mean.
- **Links** — direct links to the official websites and forms.

Main features:

- **Two channels:** a web chat and WhatsApp (Meta Cloud API; Twilio is also supported).
- **8 languages:** Spanish, English, French, Portuguese, Romanian, Catalan, Chinese and Arabic.
- **Voice in and voice out:** audio messages are transcribed, and answers can be read aloud with ElevenLabs.
- **Images:** you can send a photo of an official document and Clara explains what it says.
- **Curated knowledge base:** 23 Spanish procedures stored as JSON files in `back/data/tramites/`.
- **Guardrails:** safety checks before and after the AI model writes an answer.

## Architecture

```
   Web (React)                      WhatsApp
   GitHub Pages                     Meta Cloud API / Twilio
        │                                 │
        │ HTTPS  /api/chat                │ webhook
        └───────────────┬─────────────────┘
                        ▼
              Backend (Python · Flask)
              Docker on Render
                        │
        message pipeline (one step after another):
        detect input → detect language → transcribe audio
        → knowledge base lookup → Gemini answer
        → verify answer → text-to-speech → send
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Gemini 2.5      Knowledge base    ElevenLabs
   Flash (LLM)     (23 JSON files)   (voice)
```

How a message flows:

1. The user writes or sends audio from the web or from WhatsApp.
2. The backend detects the type of input and the language, and transcribes audio if needed.
3. It finds the matching procedure in the knowledge base.
4. Gemini writes an answer using that information, and the answer goes through the guardrails.
5. The backend sends the answer back as text, and as audio if needed.

The pipeline steps live in `back/src/core/skills/`, and the orchestrator is `back/src/core/pipeline.py`.

A hybrid RAG search (BM25 + vectors on PostgreSQL/pgvector) is also implemented, but it is **turned off in production** (`RAG_ENABLED=false` in `render.yaml`). Production uses the curated JSON knowledge base instead.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Spline (3D mascot) |
| Backend | Python 3.11, Flask, Gunicorn, Docker |
| AI | Google Gemini 2.5 Flash (answers, audio, images), ElevenLabs (text-to-speech) |
| Messaging | WhatsApp via Meta Cloud API and Twilio |
| Data | JSON knowledge base; optional PostgreSQL + pgvector for RAG |
| Hosting | GitHub Pages (frontend), Render (backend) |
| Tests | pytest (backend) |

## Run it locally

### Frontend

```bash
cd front
npm install
npm run dev
# open http://localhost:5173
```

To point the web app to your own backend, set `VITE_API_URL` (for example `http://localhost:5000`).

### Backend

```bash
cp .env.example back/.env   # then add your own API keys
cd back
bash scripts/run-local.sh
# health check: http://localhost:5000/health
```

The script creates a virtual environment, installs `requirements.txt` and starts Flask on port 5000.

The main environment variables are:

```bash
GEMINI_API_KEY=...
ELEVENLABS_API_KEY=...
# Optional, for WhatsApp:
META_WHATSAPP_TOKEN=...
META_PHONE_NUMBER_ID=...
```

See `.env.example` for the full list.

### Tests

```bash
cd back && pytest tests/ -v --tb=short   # backend
cd front && npm run build                # frontend build check
```

## Project structure

```
civicaid-voice/
├── front/            # React web app (pages, chat, 3D mascot, translations)
├── back/
│   ├── src/
│   │   ├── app.py            # Flask entry point
│   │   ├── routes/           # web chat API, WhatsApp webhooks, health
│   │   └── core/             # pipeline, skills, guardrails, prompts, config
│   ├── data/tramites/        # knowledge base (23 procedures)
│   ├── tests/                # pytest suite
│   └── Dockerfile
├── docs/             # technical docs and design notes (in Spanish)
├── clase/            # class material (presentation, branding)
└── render.yaml       # Render deployment config
```

## Current status and known limitations

- The web demo and the backend are deployed and working.
- The backend has more than 1,200 automated tests. **Some tests currently fail** and CI is red. The main causes are a database driver mismatch in `requirements.txt` (`psycopg2` installed, `psycopg` 3 expected) and tests that were not updated when the knowledge base grew.
- The keyword search in the knowledge base is too permissive: some off-topic questions still match a procedure.
- The public API endpoints do not have rate limiting yet, and the WhatsApp webhooks do not verify request signatures yet.

## Hackathon context

Clara was built for **OdiseIA4Good 2026** (UDIT, February 2026), a 48-hour hackathon with more than 300 participants, focused on using AI for social good. After the hackathon the project kept growing (more procedures, more tests, WhatsApp through Meta).

## Team

| Person | Role |
|---|---|
| **Andrea Ávila** | **Team lead · full-stack: built the backend and the frontend end to end** — Python/Flask backend and message pipeline, React/TypeScript frontend, Gemini and ElevenLabs integration, WhatsApp, deployment |
| Robert | Team member |
| Marcos | Team member |
| Lucas | Team member |
| Daniel | Team member |

> Built with AI-assisted development (Claude); architecture, review and validation by the author.

## Documentation

Full index (in Spanish): [docs/00-DOCS-INDEX.md](docs/00-DOCS-INDEX.md)

## License

Hackathon project for OdiseIA4Good — UDIT (February 2026). For educational use.
