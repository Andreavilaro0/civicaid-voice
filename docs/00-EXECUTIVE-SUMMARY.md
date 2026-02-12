# CivicAid Voice / Clara — Executive Summary

> **Hackathon:** OdiseIA4Good — UDIT | **Fecha:** Febrero 2026
> **Equipo:** Robert, Marcos, Lucas, Daniel, Andrea

---

## What is Clara?

Clara is a **WhatsApp chatbot** that helps vulnerable populations in Spain — immigrants, elderly, and people at risk of social exclusion — navigate essential government paperwork. Clara speaks the user's language, understands voice notes, and translates bureaucracy into plain human language.

## Que es Clara?

Clara es un **chatbot de WhatsApp** que ayuda a poblaciones vulnerables en Espana — inmigrantes, mayores y personas en riesgo de exclusion social — a navegar tramites administrativos esenciales. Clara habla el idioma del usuario, entiende notas de voz, y traduce la burocracia a lenguaje humano.

---

## Key Differentiators / Diferenciadores clave

| # | Feature | Description |
|---|---------|-------------|
| 1 | **WhatsApp-native** | Zero app downloads. Works where users already are (95% penetration in Spain) |
| 2 | **Voice-first** | Audio in, audio out. Critical for low digital literacy populations |
| 3 | **Multilingual** | Automatic language detection. Spanish, French, English, and more |
| 4 | **Verified information** | Responses grounded in official government data, not hallucinations |

## Impact / Impacto

- **3.2M immigrants** + **9.5M elderly** in Spain face bureaucratic barriers
- **40% of immigrants** don't complete paperwork due to language barriers
- Clara reduces that barrier to **zero** — responds in the user's language

## Technical Architecture / Arquitectura tecnica

```
WhatsApp → Twilio → Flask (Render) → Pipeline of 10 skills → Twilio REST → User
                     ↓
              ACK in <1s ("Un momento...")
                     ↓ (background thread)
              detect_input → fetch_media → transcribe (Whisper)
              → detect_lang → cache_match → kb_lookup → llm_generate (Gemini)
              → verify → send_response
```

- **Cache-first**: Demo scenarios always respond in <2s from pre-computed answers
- **Graceful degradation**: 5 fallback levels, from LLM timeout to offline video backup
- **Zero cost**: Gemini free tier, Whisper local model, Render free tier, Twilio sandbox

## Demo Flow (3 min) / Flujo de demo

| Time | What happens | Technical route |
|------|-------------|-----------------|
| 0:00 | Introduction — the problem of bureaucratic exclusion | — |
| 0:30 | **WOW 1:** Maria asks "Que es el IMV?" via WhatsApp text → instant response with text + audio | Cache hit → <2s |
| 1:15 | Transition — introducing Ahmed, a French-speaking immigrant | — |
| 1:30 | **WOW 2:** Ahmed sends a voice note in French asking about empadronamiento → response in French with audio | Whisper STT → detect lang → KB → Gemini → ~10s |
| 2:30 | Closing — scalability, zero cost, real impact | — |

Full script with fallback procedures: [`RUNBOOK-DEMO.md`](./03-runbooks/RUNBOOK-DEMO.md)

## Covered Procedures / Tramites cubiertos

| Tramite | Description |
|---------|-------------|
| **Ingreso Minimo Vital (IMV)** | Social Security income for vulnerable individuals |
| **Empadronamiento** | Municipal registration — prerequisite for public services |
| **Tarjeta Sanitaria** | Public healthcare card |

## Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11 |
| Web framework | Flask |
| Messaging | Twilio WhatsApp Sandbox |
| Speech-to-text | Whisper `base` (local) |
| LLM | Gemini 1.5 Flash |
| Language detection | `langdetect` |
| Deployment | Render (Docker) |
| Knowledge base | JSON files (3 tramites) |

## Documentation Map / Mapa de documentacion

| Document | Description | Path |
|----------|-------------|------|
| **This file** | Executive summary for reviewers | `docs/00-EXECUTIVE-SUMMARY.md` |
| **Plan Maestro** | Original project plan (Fase 0) | [`docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md`](./01-phases/FASE0-PLAN-MAESTRO-FINAL.md) |
| **Implementacion MVP** | Phase 1 implementation tracker | [`docs/01-phases/FASE1-IMPLEMENTACION-MVP.md`](./01-phases/FASE1-IMPLEMENTACION-MVP.md) |
| **Architecture** | Full technical architecture | [`docs/02-architecture/ARCHITECTURE.md`](./02-architecture/ARCHITECTURE.md) |
| **Diagrams** | Mermaid diagrams (components, dataflow, sequence) | [`docs/02-architecture/*.mmd`](./02-architecture/) |
| **Runbook Demo** | Minute-by-minute demo script with fallbacks | [`docs/03-runbooks/RUNBOOK-DEMO.md`](./03-runbooks/RUNBOOK-DEMO.md) |

---

> **To run locally:** `pip install -r requirements.txt && python -m src.app`
>
> **To run tests:** `pytest tests/ -v`
