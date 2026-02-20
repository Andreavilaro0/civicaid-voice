# Q1: Backend API Endpoint — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Tiempo estimado:** 15-25 min con multi-agentes

---

## PROMPT

### ROL Y SKILLS

Eres un ingeniero backend senior ejecutando la tarea Q1 del plan de Fase 1 de Clara. **Antes de escribir una sola linea de codigo**, activa las siguientes skills en orden de prioridad:

**Skills OBLIGATORIAS (invoca con `/skill-name`):**

| Skill | Cuando usarla | Fase |
|-------|---------------|------|
| `/executing-plans` | Gobierna toda la ejecucion — sigue este prompt como plan paso a paso | TODA |
| `/test-driven-development` | Escribe TODOS los tests ANTES de la implementacion | Fase Testing |
| `/python-pro` | Codigo Python idiomatico, type hints, docstrings minimas | Fase Implementacion |
| `/api-designer` | Diseno del contrato REST, status codes, error handling | Fase Implementacion |
| `/owasp-security` | Validacion de inputs, CORS seguro, sin injection | Fase Seguridad |
| `/verification-before-completion` | Checklist final antes del commit | Fase Final |

**Skills RECOMENDADAS (usa si detectas problemas):**

| Skill | Cuando usarla |
|-------|---------------|
| `/test-fixing` | Si algun test falla y no es obvio por que |
| `/systematic-debugging` | Si hay errores de import o runtime |
| `/code-review` | Auto-review antes del commit |
| `/secure-code-guardian` | Si tocas validacion de inputs o CORS |
| `/coverage-analysis` | Para verificar que los tests cubren todos los paths |
| `/webapp-testing` | Para patrones especificos de testing Flask |
| `/modern-python` | Si necesitas patrones Python 3.11+ |
| `/fullstack-guardian` | Para validar que el endpoint es compatible con el frontend futuro |
| `/render-deploy` | Si necesitas verificar compatibilidad con el deploy en Render |

### ESTRATEGIA MULTI-AGENTE

Usa el **Task tool** para lanzar agentes en paralelo donde sea posible. Estrategia recomendada:

```
FASE 1 — Lectura (paralelo):
  Agente A (Explore): Lee y resume todos los archivos backend relevantes
  Agente B (Explore): Lee y resume tests existentes + requirements.txt

FASE 2 — Implementacion (secuencial):
  Tu (principal): Escribe tests -> implementacion -> modificaciones

FASE 3 — Verificacion (paralelo):
  Agente C (Bash): Ejecuta pytest tests/unit/test_api_chat.py -v
  Agente D (Bash): Ejecuta pytest tests/ --tb=short (suite completa)
  Agente E (Bash): Ejecuta ruff check src/routes/api_chat.py --select E,F,W --ignore E501
```

**Para lanzar agentes paralelos usa este patron:**
```
Task tool con subagent_type="Explore" para lectura
Task tool con subagent_type="Bash" para comandos
Task tool con subagent_type="general-purpose" para tareas complejas
```

---

### CONTEXTO DEL PROYECTO

**Clara** es un asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana (inmigrantes, mayores, personas con baja alfabetizacion digital) a navegar tramites del gobierno espanol. Ya tiene un backend funcional en Flask desplegado en Render.

**Tu trabajo:** Crear un endpoint REST API (`POST /api/chat` y `GET /api/health`) para que un frontend Next.js (que se construira despues) pueda comunicarse con el pipeline existente. Es SOLO backend Python — no toques nada de frontend.

### ARQUITECTURA EXISTENTE

```
Usuario WhatsApp -> Twilio -> Flask POST /webhook -> TwiML ACK (<1s)
                                                  -> Background Thread -> pipeline.process(msg)
                                                  -> Twilio REST API -> Usuario WhatsApp

[NUEVO — tu trabajo]:
Frontend Next.js -> POST /api/chat -> Flask -> pipeline sincrono -> JSON response -> Frontend
```

**Diferencia clave:** El webhook de Twilio es asincrono (TwiML ACK + hilo de fondo). Tu endpoint `/api/chat` es **sincrono** — recibe request, procesa, devuelve JSON. Reutiliza las mismas skills del pipeline pero sin hilos de fondo.

### STACK Y ARCHIVOS EXISTENTES

| Componente | Archivo | Que hace |
|------------|---------|----------|
| Flask app | `src/app.py` | Entry point, `create_app()`, registra 5 blueprints |
| Config | `src/core/config.py` | Dataclass frozen con feature flags (DEMO_MODE, LLM_LIVE, WHISPER_ON, GUARDRAILS_ON, STRUCTURED_OUTPUT_ON, AUDIO_BASE_URL) |
| Modelos | `src/core/models.py` | `InputType` (TEXT/AUDIO/IMAGE), `CacheEntry`, `CacheResult`, `KBContext`, `LLMResponse`, `TranscriptResult` |
| Cache | `src/core/cache.py` | `load_cache()` carga `demo_cache.json`, `match(text, lang, input_type)` retorna `CacheResult` |
| Detect lang | `src/core/skills/detect_lang.py` | `detect_language(text)` retorna `"es"` o `"fr"` |
| KB lookup | `src/core/skills/kb_lookup.py` | `kb_lookup(text, language)` retorna `KBContext` |
| LLM | `src/core/skills/llm_generate.py` | `llm_generate(text, language, kb_context)` retorna `LLMResponse` |
| Verify | `src/core/skills/verify_response.py` | `verify_response(text, kb_context)` retorna string |
| TTS | `src/core/skills/tts.py` | `text_to_audio(text, language)` retorna URL string |
| Transcribe | `src/core/skills/transcribe.py` | `transcribe(audio_bytes, mime_type)` retorna `TranscriptResult` |
| Guardrails | `src/core/guardrails.py` | `pre_check(text)` retorna `GuardrailResult(.safe, .modified_text)`, `post_check(text)` retorna string |
| Templates | `src/core/prompts/templates.py` | `get_template(key, language)` retorna string |
| Structured | `src/core/models_structured.py` | `parse_structured_response(text)` retorna `(parsed, display)` |
| Tests | `tests/` | 182 tests pasando — NO rompas ninguno |
| Blueprints | `src/app.py` lineas 32-44 | `health_bp`, `webhook_bp`, `static_bp`, `forget_bp`, `admin_bp` |
| Dependencies | `requirements.txt` | flask, gunicorn, twilio, pydub, google-genai, langdetect, requests, python-dotenv, gTTS, pydantic, redis, sqlalchemy, psycopg2-binary, pgvector |

### CONTRATO API (SAGRADO — no lo cambies)

**Request:** `POST /api/chat`
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

**Response:** (TODOS estos campos son obligatorios, siempre)
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

**Health:** `GET /api/health`
```json
{"status": "ok", "features": {"whisper": true, "llm": true, "guardrails": true, "demo_mode": false}}
```

**Error responses:**
- `400` — `{"error": "text or audio_base64 required"}` si falta input
- `422` — `{"error": "audio_transcription_failed"}` si falla transcripcion
- `500` — `{"error": "audio_processing_error"}` si falla procesamiento audio

---

## EJECUCION PASO A PASO

### PASO 0: Lectura del codebase (usa agentes paralelos)

**Lanza DOS agentes Explore en paralelo:**

**Agente A — Backend core:**
```
Lee y resume: src/app.py, src/core/config.py, src/core/models.py, src/core/cache.py,
src/core/skills/detect_lang.py, src/core/skills/kb_lookup.py, src/core/skills/llm_generate.py,
src/core/skills/verify_response.py, src/core/skills/tts.py, src/core/skills/transcribe.py,
src/core/guardrails.py, src/core/prompts/templates.py, src/core/models_structured.py
```

**Agente B — Tests y deps:**
```
Lee y resume: requirements.txt, lista de archivos en tests/unit/, cualquier test existente
que importe de src/routes/ para entender el patron de testing usado.
```

**Espera** a que ambos agentes terminen antes de continuar. Confirma que entiendes:
1. Como `create_app()` registra blueprints (patron Import + register_blueprint)
2. Las firmas exactas de las funciones que vas a importar
3. Los modelos exactos que usa cada funcion (CacheResult, KBContext, LLMResponse, etc.)
4. El patron de testing existente (pytest fixtures, mocks)

---

### PASO 1: Agregar `flask-cors` a `requirements.txt`

**Skill activa:** `/api-designer` (CORS es parte del diseno de la API)

Abre `requirements.txt` con **Read**, luego usa **Edit** para agregar al final:

```
flask-cors==5.0.*
```

Ejecuta con **Bash**:
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && pip install flask-cors
```

**Verificacion:** El output debe mostrar "Successfully installed flask-cors-5.0.x"

---

### PASO 2: Crear tests PRIMERO (TDD)

**Skill activa:** `/test-driven-development` + `/webapp-testing`

Crea `tests/unit/test_api_chat.py` con **Write**:

```python
"""Tests for POST /api/chat and GET /api/health API endpoints.

Covers: health check, input validation, cache hit flow, response contract,
CORS preflight, and audio error handling.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestApiHealth:
    """GET /api/health endpoint tests."""

    def test_returns_200_with_status_ok(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"

    def test_includes_feature_flags(self, client):
        resp = client.get("/api/health")
        data = resp.get_json()
        assert "features" in data
        for key in ("whisper", "llm", "guardrails", "demo_mode"):
            assert key in data["features"], f"Missing feature flag: {key}"


class TestApiChatValidation:
    """Input validation tests for POST /api/chat."""

    def test_rejects_empty_body(self, client):
        resp = client.post("/api/chat", json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["error"] == "text or audio_base64 required"

    def test_rejects_blank_text(self, client):
        resp = client.post("/api/chat", json={"text": "   "})
        assert resp.status_code == 400

    def test_rejects_null_text_no_audio(self, client):
        resp = client.post("/api/chat", json={"text": None, "audio_base64": None})
        assert resp.status_code == 400


class TestApiChatCacheHit:
    """Tests for the cache-hit happy path."""

    def test_cache_hit_returns_response(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(
                    respuesta="El IMV es una ayuda mensual de la Seguridad Social.",
                    audio_file=None,
                )
            )
            resp = client.post("/api/chat", json={"text": "Que es el IMV?"})
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["response"] == "El IMV es una ayuda mensual de la Seguridad Social."
            assert data["source"] == "cache"

    def test_cache_hit_includes_audio_url_when_available(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"), \
             patch("src.routes.api_chat.config") as mock_config:
            mock_config.GUARDRAILS_ON = False
            mock_config.AUDIO_BASE_URL = "https://example.com/static/cache"
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(
                    respuesta="Respuesta con audio.",
                    audio_file="imv_es.mp3",
                )
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            assert data["audio_url"] == "https://example.com/static/cache/imv_es.mp3"


class TestApiChatContract:
    """Verifica que la respuesta tenga TODOS los campos del contrato API."""

    def test_response_has_all_required_keys(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(respuesta="Test.", audio_file=None)
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            required_keys = {"response", "source", "language", "duration_ms", "audio_url", "sources"}
            assert required_keys.issubset(data.keys()), f"Faltan keys: {required_keys - data.keys()}"

    def test_sources_is_always_a_list(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(respuesta="Test.", audio_file=None)
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            assert isinstance(data["sources"], list)

    def test_duration_ms_is_non_negative_integer(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(respuesta="Test.", audio_file=None)
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            assert isinstance(data["duration_ms"], int)
            assert data["duration_ms"] >= 0


class TestApiChatCORS:
    """CORS configuration tests."""

    def test_cors_preflight_succeeds(self, client):
        resp = client.options("/api/chat", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        })
        assert resp.status_code in (200, 204)


class TestApiChatAudio:
    """Audio input handling tests."""

    def test_rejects_failed_transcription(self, client):
        with patch("src.routes.api_chat.config") as mock_config:
            mock_config.GUARDRAILS_ON = False
            with patch("src.core.skills.transcribe.transcribe") as mock_transcribe:
                mock_transcribe.return_value = MagicMock(success=False, text="")
                resp = client.post("/api/chat", json={
                    "input_type": "audio",
                    "audio_base64": "dGVzdA==",
                })
                assert resp.status_code == 422
```

**Ejecuta los tests para verificar que FALLAN** (el modulo no existe aun):
```bash
pytest tests/unit/test_api_chat.py -v 2>&1 | head -30
```

**Resultado esperado:** `ModuleNotFoundError: No module named 'src.routes.api_chat'` o similar. Esto confirma que TDD funciona — los tests fallan porque la implementacion no existe.

---

### PASO 3: Crear `src/routes/api_chat.py`

**Skills activas:** `/python-pro` + `/api-designer` + `/owasp-security`

Crea el archivo con **Write**:

```python
"""POST /api/chat — REST API for web frontend.

Reutiliza el pipeline existente de Clara de forma sincrona.
No duplica logica — importa directamente las skills existentes.
"""

import time
import base64
import logging
from flask import Blueprint, request, jsonify
from src.core.config import config
from src.core.models import InputType
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

    if not text and not audio_b64:
        return jsonify({"error": "text or audio_base64 required"}), 400

    start = time.time()

    # --- Audio transcription (si envian audio desde el frontend) ---
    if input_type_str == "audio" and audio_b64:
        try:
            from src.core.skills.transcribe import transcribe
            audio_bytes = base64.b64decode(audio_b64)
            transcript = transcribe(audio_bytes, "audio/webm")
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

    # --- Demo mode (solo cache, sin LLM) ---
    if config.DEMO_MODE:
        elapsed = int((time.time() - start) * 1000)
        return jsonify({
            "response": get_template("fallback_generic", language),
            "source": "fallback", "language": language,
            "duration_ms": elapsed, "audio_url": None, "sources": []
        })

    # --- KB lookup + LLM generate ---
    kb_context = kb_lookup(text, language)
    llm_resp = llm_generate(text, language, kb_context)
    verified = verify_response(llm_resp.text, kb_context)

    # --- Structured output (opcional) ---
    if config.STRUCTURED_OUTPUT_ON:
        from src.core.models_structured import parse_structured_response
        parsed, display = parse_structured_response(verified)
        if parsed:
            verified = display

    # --- Guardrails post-check ---
    if config.GUARDRAILS_ON:
        from src.core.guardrails import post_check
        verified = post_check(verified)

    # --- TTS (text-to-speech, best-effort) ---
    audio_url = None
    try:
        from src.core.skills.tts import text_to_audio
        audio_url = text_to_audio(verified, language)
    except Exception:
        pass

    # --- Build sources list ---
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

---

### PASO 4: Modificar `src/app.py`

**Skill activa:** `/python-pro`

Abre `src/app.py` con **Read** primero, luego usa **Edit** (NO Write) para hacer dos cambios:

**Cambio A — Registrar blueprint:** Despues de la linea `app.register_blueprint(admin_bp)`, agrega:

```python
    from src.routes.api_chat import api_bp
    app.register_blueprint(api_bp)
```

**Cambio B — Habilitar CORS:** Inmediatamente despues del cambio A, agrega:

```python
    # CORS for web frontend API
    import os
    from flask_cors import CORS
    frontend_origins = os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
    CORS(app, resources={r"/api/*": {"origins": frontend_origins}})
```

**CRITICO:** Ambos cambios van DENTRO de `create_app()`, antes del `return app`. No muevas ni modifiques ninguna otra linea.

---

### PASO 5: Ejecutar tests (usa agentes paralelos)

**Skill activa:** `/verification-before-completion`

**Lanza TRES comandos en paralelo con el Task tool (subagent_type="Bash"):**

**Comando 1 — Tests nuevos:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && pytest tests/unit/test_api_chat.py -v
```
**Esperado:** Todos los tests PASAN (12+ tests).

**Comando 2 — Suite completa:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && pytest tests/ -v --tb=short 2>&1 | tail -30
```
**Esperado:** 182+ tests pasando, 0 failed. Los tests nuevos se suman al total.

**Comando 3 — Lint:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && ruff check src/routes/api_chat.py --select E,F,W --ignore E501
```
**Esperado:** Sin errores.

**Si algun test falla:** Activa `/test-fixing` + `/systematic-debugging`. Lee el traceback completo, identifica la causa raiz, corrige y re-ejecuta. NO hagas commit hasta que todo pase.

---

### PASO 6: Test manual con curl (opcional, solo si el servidor puede levantarse)

```bash
# En una terminal aparte: bash scripts/run-local.sh
# Luego en otra:

# Health check
curl -s http://localhost:5000/api/health | python3 -m json.tool

# Chat — cache hit
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Que es el IMV?"}' | python3 -m json.tool

# Validation — 400
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

# CORS preflight
curl -s -X OPTIONS http://localhost:5000/api/chat \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" -v 2>&1 | grep -i "access-control"
```

**Nota:** Si no puedes levantar el servidor (deps pesadas como Whisper), los unit tests con mocks son suficientes. No bloquees el progreso por esto.

---

### PASO 7: Auto-review de seguridad

**Skill activa:** `/owasp-security` + `/code-review`

Antes del commit, revisa mentalmente:

- [ ] **Input validation:** `text` se stripea, se rechaza vacio. `audio_base64` se decodifica con try/except.
- [ ] **No SQL injection:** No hay queries SQL directas.
- [ ] **No command injection:** No hay `os.system()`, `subprocess`, ni `eval()`.
- [ ] **CORS restrictivo:** Solo origenes de `FRONTEND_URL`, no `*` en produccion.
- [ ] **Error handling:** Excepciones de audio capturadas, no leakean stack traces al usuario.
- [ ] **No secrets en codigo:** Ninguna API key hardcodeada.
- [ ] **Lazy imports:** Los imports pesados (transcribe, guardrails, tts, structured) son lazy dentro de la funcion para evitar cargar Whisper/Gemini si no se necesitan.

---

### PASO 8: Commit

**Skill activa:** `/verification-before-completion`

```bash
git add src/routes/api_chat.py src/app.py requirements.txt tests/unit/test_api_chat.py
git commit -m "feat: add REST API endpoint POST /api/chat for web frontend

- New blueprint: api_bp with /api/chat (POST) and /api/health (GET)
- Reuses existing pipeline: cache -> guardrails -> detect_lang -> KB -> LLM -> verify -> TTS
- CORS enabled for frontend origin via FRONTEND_URL env var
- Response contract: {response, audio_url, source, language, duration_ms, sources[]}
- 12 new tests, all existing 182 tests still passing
- TDD: tests written first, implementation second

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE A USAR

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Read** | Antes de modificar cualquier archivo | OBLIGATORIO — nunca edites sin leer primero |
| **Write** | Para crear `api_chat.py` y `test_api_chat.py` | Archivos nuevos |
| **Edit** | Para modificar `src/app.py` y `requirements.txt` | NO reescribas, solo edita las lineas necesarias |
| **Bash** | Para `pip install`, `pytest`, `curl`, `git commit` | Comandos de terminal |
| **Glob** | Para verificar estructura antes de crear archivos | Ej: `tests/unit/test_*.py` |
| **Grep** | Para buscar patrones si necesitas entender imports | Ej: buscar `register_blueprint` |
| **Task** | Para lanzar agentes paralelos en Paso 0 y Paso 5 | `subagent_type="Explore"` o `"Bash"` |

## RESTRICCIONES ABSOLUTAS

1. **NO modifiques** ningun archivo excepto `src/app.py` y `requirements.txt`
2. **NO dupliques** logica — importa y reutiliza las skills existentes
3. **NO rompas** los 182 tests existentes
4. **NO uses** imports circulares — los lazy imports son intencionales
5. **NO agregues** dependencias que no sean `flask-cors`
6. **Sigue TDD:** tests ANTES de implementacion, siempre
7. **El contrato JSON es sagrado:** `{response, audio_url, source, language, duration_ms, sources[]}`
8. **NO hagas commit** si algun test falla

## DEFINICION DE TERMINADO

- [ ] `flask-cors==5.0.*` agregado a `requirements.txt` e instalado
- [ ] `tests/unit/test_api_chat.py` creado con 12+ tests (escritos ANTES de la implementacion)
- [ ] `src/routes/api_chat.py` creado con `POST /api/chat` y `GET /api/health`
- [ ] `src/app.py` modificado: blueprint registrado + CORS habilitado
- [ ] Todos los tests nuevos pasan: `pytest tests/unit/test_api_chat.py -v`
- [ ] Todos los tests existentes siguen pasando: `pytest tests/ --tb=short`
- [ ] Lint limpio: `ruff check src/routes/api_chat.py`
- [ ] Review de seguridad completado (checklist OWASP)
- [ ] Commit con mensaje descriptivo

---

> **Siguiente paso despues de completar Q1:** El prompt Q2 creara el scaffolding de `clara-web/` con Next.js 14.
