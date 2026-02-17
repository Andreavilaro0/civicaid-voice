# Sprint 3 — Presentacion (8 slides)

> Contenido slide-ready para copiar a Canva/PowerPoint.
> Estilo: fondo oscuro, cards coloridas, tipografia bold.

---

## SLIDE 1 — Portada

### CivicAid Voice / Clara

**"Traducimos la burocracia a tu lengua"**

Asistente WhatsApp de tramites sociales para personas vulnerables en Espana

| 3.2M inmigrantes | 9.5M mayores 65 | 4.5M exclusion | 78% WhatsApp |
|:-:|:-:|:-:|:-:|

**Equipo:** Robert Promes (PM) - Marcos - Daniel - Andrea - Lucas

UDIT — Taller de Proyectos II — Dr. Gustavo Bermejo Martin
13 de febrero de 2026

---

## SLIDE 2 — Que hace Clara

### 01 Funcionalidades

**4 funcionalidades CORE desplegadas:**

| Icono | Funcionalidad | Detalle |
|:-----:|--------------|---------|
| 💬 | Chat multilingue | Espanol + Frances, deteccion automatica |
| 🎙️ | Voz STT + TTS | Audio in (Gemini) + Audio out (gTTS) |
| ⚡ | Cache inteligente | 8 respuestas en <2 segundos |
| 🔧 | Pipeline 11 skills | Orquestador modular y resiliente |

**Calidad:**
- Guardrails de seguridad (6 red team tests, 100% bloqueo)
- 96 tests automatizados
- Observabilidad con JSON logs

**Proximo Sprint:** Lector de documentos + Canal web

---

## SLIDE 3 — Arquitectura

### 02 Stack 100% gratuito

```
WhatsApp → Twilio → Flask (Render) → TwiML ACK (<1s)
                                         ↓
                                   Background Thread
                                         ↓
                          Cache HIT? → SI → Twilio REST → Usuario
                                  ↓ NO
                          KB → Gemini Flash → Verify → gTTS
                                         ↓
                                   Twilio REST → Usuario
```

**Stack:**

| Capa | Tecnologia |
|------|-----------|
| Canal | WhatsApp (Twilio Sandbox) |
| Servidor | Flask + Gunicorn (Render free) |
| LLM | Gemini 1.5 Flash (free tier) |
| Audio | Gemini (STT) + gTTS (TTS) |
| KB | 3 JSONs (IMV, empadronamiento, tarjeta) |
| Container | Docker (Python 3.11-slim) |

**Coste total: 0 EUR/mes**

---

## SLIDE 4 — Flujo paso a paso

### 03 Procesos

**Flujo A — Texto WhatsApp (6 pasos)**

1. Usuario escribe en WhatsApp
2. Twilio POST → /webhook
3. Validacion de firma (seguridad)
4. TwiML ACK (<1 segundo)
5. Cache match → KB → Gemini → Verify → gTTS
6. Respuesta via Twilio REST

**Tiempo: <2s (cache) | 4-8s (LLM)**

---

**Flujo B — Audio WhatsApp (8 pasos)**

1. Usuario envia audio
2. Twilio POST → /webhook (con MediaUrl)
3. Validacion de firma
4. TwiML ACK (<1 segundo)
5. Descarga audio + Gemini transcripcion
6. Deteccion de idioma
7. Cache → KB → Gemini → Verify
8. gTTS audio + Twilio REST

**Tiempo: 6-12s**

---

## SLIDE 5 — Ventajas y limitaciones

### 04-05 Pros y contras

**VENTAJAS**

| # | Ventaja |
|---|---------|
| 1 | Accesible: WhatsApp + audio (sin leer/escribir) |
| 2 | Multilingue: ES + FR nativos |
| 3 | Gratis: 0 EUR/mes infraestructura |
| 4 | Rapido: <2s con cache inteligente |

**LIMITACIONES (con mitigacion)**

| # | Limitacion | Mitigacion |
|---|-----------|------------|
| 1 | KB estatica (3 tramites) | RAG preparado, extensible |
| 2 | 2 idiomas probados | Extensible por config |
| 3 | Twilio Sandbox | Migracion trivial (1 variable) |
| 4 | Canal web en desarrollo | Sprint 4 (WhatsApp es prioridad) |

> Todas las limitaciones son del prototipo, no de la arquitectura.

---

## SLIDE 6 — Prototipo y escalabilidad

### 06-07 Producto real + futuro

**URL en produccion:** https://civicaid-voice.onrender.com

**Estado actual:**
- /health → 8 componentes OK
- 96/96 tests PASS
- Docker containerizado
- Cron warm-up cada 14 min

**Escalabilidad:**

| Aspecto | Hoy (0 EUR) | Futuro (~200 EUR) |
|---------|-------------|-------------------|
| Servidor | Render free | GCP Cloud Run |
| LLM | Gemini Flash free | Gemini Pro fine-tuned |
| KB | 3 JSONs | RAG + vector DB |
| Idiomas | 2 | 6+ |
| Canales | WhatsApp | WhatsApp + Web + Telegram |
| Users | ~10 | 10,000+ |

---

## SLIDE 7 — Puntos destacables

### 08 Lo que nos hace diferentes

**3 personas reales:**

- **Maria** (ES) — IMV: "Como solicito el ingreso minimo?" → Respuesta completa en <3s
- **Ahmed** (FR) — Empadronamiento: Audio en frances → Respuesta en frances + audio
- **Laura** (ES) — Tarjeta sanitaria: "Necesito la tarjeta" → Pasos + telefonos

**Datos INE:**
3.2M inmigrantes | 9.5M mayores 65 | 4.5M exclusion | 78% WhatsApp

**Momento WOW:**
1. Texto: respuesta en <3 segundos con info verificada
2. Audio: frances → transcripcion + respuesta en frances

**Sprint 3 en numeros:**
0 EUR | 1 canal | 2 idiomas | 3 tramites | 96 tests | 11 skills

---

## SLIDE 8 — Scrum + Criterios del jurado

### Sprint Review + Evaluacion

**Checkpoints:**

| Sprint | Estado |
|--------|--------|
| S1 (30 Ene) Planificacion | COMPLETADO |
| S2 (6 Feb) Doc + repo | COMPLETADO |
| S3 (13 Feb) MVP + doc v2 | HOY |
| S4 (20 Feb) Demo final | PROXIMO |

**Cambios vs Sprint 2:** Web → Sprint 4 | Whisper → Gemini | HuggingFace → Render | 4 idiomas → 2 probados | Mockup → Producto real

**Cruce con criterios del jurado:**

| Criterio | Peso | Evidencia clave |
|----------|------|-----------------|
| Innovacion | 30% | Pipeline 11 skills + TwiML ACK + guardrails + evals |
| Impacto Social | 30% | WhatsApp audio para no alfabetizados + multilingue |
| Viabilidad | 20% | Desplegado, 96 tests, 0 EUR, Docker |
| Presentacion | 20% | Demo en vivo + WOW texto + WOW audio frances |

---

**Equipo:** Robert - Marcos - Daniel - Andrea - Lucas
**Repo:** github.com/civicaid-voice
**UDIT — Taller de Proyectos II — 2026**
