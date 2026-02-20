# FASE 1, Q1 — Prompt de Implementacion Completo

> **Para:** Claude Code (agent mode o multiagent)
> **Skill requerida:** `nextjs-developer`, `frontend-developer`, `react-expert`, `twilio-communications`
> **Fecha:** 19 Feb 2026

---

## CONTEXTO DEL PROYECTO

Eres un ingeniero senior implementando la capa frontend de **Clara**, un asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana (inmigrantes, mayores, personas con baja alfabetizacion digital) a navegar tramites del gobierno espanol. Clara ya tiene un backend funcional en Flask desplegado en Render. Tu trabajo es construir la web app responsive y mejorar el canal WhatsApp.

### Stack Backend Existente (NO MODIFICAR excepto donde se indica)
- **Python 3.11, Flask** en `src/app.py`
- **Twilio WhatsApp** sandbox en `src/routes/webhook.py`
- **Pipeline de 11 skills** en `src/core/pipeline.py`: guardrails -> audio -> language detection -> memory -> cache -> KB -> LLM (Gemini 1.5 Flash) -> verify -> structured output -> TTS (gTTS) -> send response
- **Modelos** en `src/core/models.py`: `IncomingMessage`, `InputType` (TEXT/AUDIO/IMAGE), `FinalResponse`, `CacheResult`, `KBContext`, `LLMResponse`
- **Config** en `src/core/config.py`: singleton `config` con feature flags (DEMO_MODE, LLM_LIVE, WHISPER_ON, GUARDRAILS_ON, etc.)
- **Deploy:** Docker + Render, puerto 5000
- **Base URL actual:** La que este en `.env` como `AUDIO_BASE_URL`

### Arquitectura de Comunicacion Actual
```
Usuario WhatsApp -> Twilio -> Flask POST /webhook -> TwiML ACK (<1s)
                                                  -> Background Thread -> pipeline.process(msg)
                                                  -> Twilio REST API -> Usuario WhatsApp
```

---

## DECISION ARQUITECTONICA: COMO CONECTAR FRONT Y BACK

### Enfoque elegido: Nuevo endpoint `/api/chat` en el Flask existente

**Por que esta decision y no otras:**

| Opcion | Pros | Contras | Veredicto |
|--------|------|---------|-----------|
| **A) Nuevo `/api/chat` en Flask** | Reutiliza todo el pipeline, 1 solo backend, ya desplegado | Necesita CORS, nueva ruta | ELEGIDA |
| B) Next.js llama a Gemini directo | Frontend independiente | Duplica logica de guardrails, KB, verify, prompts | NO — duplicacion |
| C) Next.js con API routes propias | Full-stack JS | Reescribir pipeline entero en JS | NO — tiempo de hackathon |
| D) WebSockets | Real-time | Sobre-ingenieria para hackathon | NO — complejidad innecesaria |

### Contrato de la API a crear

**Archivo a crear:** `src/routes/api_chat.py`

**Endpoint:** `POST /api/chat`

**Request (JSON):**
```json
{
  "text": "Que es el IMV?",
  "language": "es",
  "input_type": "text",
  "audio_base64": null,
  "image_base64": null,
  "session_id": "web_abc123"
}
```

**Response (JSON):**
```json
{
  "response": "El Ingreso Minimo Vital es una ayuda mensual...",
  "audio_url": "https://backend-url/static/cache/tts_abc123.mp3",
  "source": "llm",
  "language": "es",
  "duration_ms": 1200,
  "sources": [
    {"name": "Seguridad Social", "url": "https://www.seg-social.es"}
  ]
}
```

**Endpoint:** `GET /api/health`
```json
{"status": "ok", "version": "1.0", "features": {"whisper": true, "llm": true}}
```

---

## PARTE 1: BACKEND — Nueva ruta API (antes del frontend)

### Tarea 1.1: Crear `src/routes/api_chat.py`

```python
"""POST /api/chat — REST API for web frontend. Reuses existing pipeline synchronously."""

import time
import base64
import tempfile
import os
import logging
from flask import Blueprint, request, jsonify
from src.core.config import config
from src.core.models import IncomingMessage, InputType, KBContext, LLMResponse
from src.core import cache
from src.core.skills.detect_lang import detect_language
from src.core.skills.kb_lookup import kb_lookup
from src.core.skills.llm_generate import llm_generate
from src.core.skills.verify_response import verify_response
from src.core.prompts.templates import get_template

logger = logging.getLogger("clara")
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    language = data.get("language", "es")
    input_type_str = data.get("input_type", "text")
    audio_b64 = data.get("audio_base64")
    session_id = data.get("session_id", "")

    if not text and not audio_b64:
        return jsonify({"error": "text or audio_base64 required"}), 400

    start = time.time()

    # --- Audio transcription ---
    if input_type_str == "audio" and audio_b64:
        try:
            from src.core.skills.transcribe import transcribe
            audio_bytes = base64.b64decode(audio_b64)
            from src.core.models import TranscriptResult
            transcript: TranscriptResult = transcribe(audio_bytes, "audio/webm")
            if transcript.success and transcript.text:
                text = transcript.text
                language = transcript.language
            else:
                return jsonify({"error": "audio_transcription_failed"}), 422
        except Exception as e:
            logger.error("API audio error: %s", e)
            return jsonify({"error": "audio_processing_error"}), 500

    # --- Guardrails pre-check ---
    if config.GUARDRAILS_ON:
        from src.core.guardrails import pre_check
        guard = pre_check(text)
        if not guard.safe:
            elapsed = int((time.time() - start) * 1000)
            return jsonify({
                "response": guard.modified_text or "No puedo ayudar con ese tema.",
                "source": "guardrail", "language": language,
                "duration_ms": elapsed, "audio_url": None, "sources": []
            })

    # --- Detect language ---
    if input_type_str == "text":
        language = detect_language(text)

    # --- Cache match ---
    cache_result = cache.match(text, language, InputType.TEXT)
    if cache_result.hit and cache_result.entry:
        elapsed = int((time.time() - start) * 1000)
        audio_url = None
        if cache_result.entry.audio_file and config.AUDIO_BASE_URL:
            audio_url = f"{config.AUDIO_BASE_URL.rstrip('/')}/{cache_result.entry.audio_file}"
        return jsonify({
            "response": cache_result.entry.respuesta,
            "source": "cache", "language": language,
            "duration_ms": elapsed, "audio_url": audio_url, "sources": []
        })

    # --- Demo mode ---
    if config.DEMO_MODE:
        elapsed = int((time.time() - start) * 1000)
        return jsonify({
            "response": get_template("fallback_generic", language),
            "source": "fallback", "language": language,
            "duration_ms": elapsed, "audio_url": None, "sources": []
        })

    # --- KB + LLM ---
    kb_context = kb_lookup(text, language)
    llm_resp = llm_generate(text, language, kb_context)
    verified = verify_response(llm_resp.text, kb_context)

    if config.STRUCTURED_OUTPUT_ON:
        from src.core.models_structured import parse_structured_response
        parsed, display = parse_structured_response(verified)
        if parsed:
            verified = display

    if config.GUARDRAILS_ON:
        from src.core.guardrails import post_check
        verified = post_check(verified)

    # --- TTS ---
    audio_url = None
    try:
        from src.core.skills.tts import text_to_audio
        audio_url = text_to_audio(verified, language)
    except Exception:
        pass

    # --- Build sources ---
    sources = []
    if kb_context and kb_context.fuente_url:
        sources.append({"name": kb_context.tramite, "url": kb_context.fuente_url})

    elapsed = int((time.time() - start) * 1000)
    return jsonify({
        "response": verified,
        "source": "llm" if llm_resp.success else "fallback",
        "language": language,
        "duration_ms": elapsed,
        "audio_url": audio_url,
        "sources": sources,
    })


@api_bp.route("/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "ok",
        "features": {
            "whisper": config.WHISPER_ON,
            "llm": config.LLM_LIVE,
            "guardrails": config.GUARDRAILS_ON,
            "demo_mode": config.DEMO_MODE,
        }
    })
```

### Tarea 1.2: Registrar blueprint y CORS en `src/app.py`

Agregar al `create_app()`:
```python
# Despues de los otros blueprint registers:
from src.routes.api_chat import api_bp
app.register_blueprint(api_bp)

# CORS para el frontend
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Instalar dependencia: `pip install flask-cors` y agregar a `requirements.txt`.

### Tarea 1.3: Variables de entorno nuevas

Agregar a `.env`:
```
FRONTEND_URL=http://localhost:3000
```

---

## PARTE 2: FRONTEND — Next.js Web App

### Scaffolding

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice
npx create-next-app@latest clara-web --typescript --tailwind --app --src-dir --no-eslint
cd clara-web
npm install react-aria-components next-intl
```

### Estructura de archivos a crear

```
clara-web/
  src/
    app/
      layout.tsx          # Root layout con fonts + metadata
      page.tsx            # Pantalla de Bienvenida
      chat/
        page.tsx          # Interfaz de Chat principal
      globals.css         # Tailwind + custom tokens
    components/
      ui/
        Button.tsx        # Boton accesible 64x64px
        ChatBubble.tsx    # Burbuja Clara vs Usuario
        LanguageSelector.tsx  # Toggle ES/FR
        LoadingState.tsx  # "Clara esta buscando..."
        AudioPlayer.tsx   # Reproductor con velocidad
      VoiceRecorder.tsx   # Grabacion toggle mic
      DocumentUpload.tsx  # Subida de foto
      ChatInput.tsx       # Campo texto + 3 botones
      MessageList.tsx     # Lista de mensajes con scroll
      Header.tsx          # Header del chat
    lib/
      api.ts              # Cliente HTTP para /api/chat
      types.ts            # TypeScript interfaces
      constants.ts        # Colores, sizes, URLs
    messages/
      es.json             # Strings en espanol
      fr.json             # Strings en frances
  public/
    icons/                # Iconos Clara
    manifest.json         # PWA manifest
  tailwind.config.ts      # Paleta Clara
  next.config.ts          # Config next-intl
```
