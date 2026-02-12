# Arquitectura de Clara — Asistente Conversacional por WhatsApp

## 1. Resumen

**Clara** es un asistente conversacional diseñado para poblaciones vulnerables en España — personas migrantes, refugiadas y en situación de exclusión social — que necesitan orientación sobre trámites administrativos esenciales. Clara opera exclusivamente a través de **WhatsApp**, el canal de comunicación más accesible para estas comunidades, y proporciona guía paso a paso sobre tres trámites fundamentales:

- **Ingreso Mínimo Vital (IMV)** — Prestación económica de la Seguridad Social para personas en situación de vulnerabilidad económica.
- **Empadronamiento** — Inscripción en el padrón municipal, requisito previo para acceder a servicios públicos.
- **Tarjeta Sanitaria** — Documento que acredita el derecho a la asistencia sanitaria pública.

Clara acepta **texto, audio e imágenes** como entrada, responde en el idioma detectado del usuario (español, inglés, francés, árabe, ucraniano, entre otros), y devuelve tanto texto como audio pregrabado o generado por TTS para maximizar la accesibilidad.

---

## 2. Patrón TwiML ACK + Respuesta Asíncrona

El patrón arquitectónico central de Clara resuelve una restricción crítica de la integración con Twilio: **Twilio exige una respuesta HTTP en menos de 15 segundos**, pero el pipeline completo (transcripción de audio + consulta LLM) puede tardar entre 4 y 18 segundos.

### Flujo del patrón:

1. **Twilio envía un POST** al endpoint `/webhook` de Flask con los datos del mensaje (Body, From, NumMedia, MediaUrl, MediaContentType).
2. **Flask responde inmediatamente** (en menos de 1 segundo) con un **HTTP 200** que incluye un cuerpo **TwiML XML** con un mensaje de acknowledgement:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <Response>
       <Message>Un momento, estoy procesando tu consulta...</Message>
   </Response>
   ```
3. **Antes de retornar**, Flask lanza un **`threading.Thread`** que ejecuta el pipeline completo de 10 skills en segundo plano.
4. **El hilo de background** procesa el mensaje (transcripción, detección de idioma, búsqueda en caché, consulta al LLM, verificación) y al finalizar envía la respuesta definitiva al usuario mediante la **Twilio REST API** (`client.messages.create`).

### Ventajas:

- El usuario recibe feedback inmediato ("Un momento...") mientras Clara procesa.
- No hay riesgo de timeout de Twilio.
- El pipeline puede tomar el tiempo necesario para transcribir audio y generar respuestas de calidad.

---

## 3. Stack Tecnológico

| Componente | Tecnología | Justificación |
|---|---|---|
| **Lenguaje** | Python 3.11 | Ecosistema ML maduro, tipado con dataclasses |
| **Framework web** | Flask | Ligero, suficiente para un webhook único |
| **Canal** | Twilio WhatsApp Sandbox | Integración rápida para hackathon, sin necesidad de Business API |
| **Transcripción** | Whisper `base` (OpenAI) | Modelo local, multilingüe, sin coste por API |
| **LLM** | Gemini 1.5 Flash (Google) | Rápido, económico, ventana de contexto amplia |
| **Detección de idioma** | `langdetect` | Librería ligera, soporta los idiomas objetivo |
| **Text-to-Speech** | gTTS (Google TTS) | Gratuito, múltiples idiomas |
| **Base de conocimiento** | JSON estático | Sin dependencias externas, editable, versionable |
| **Despliegue** | Render (free tier) + Docker | CI/CD automático desde GitHub, SSL incluido |
| **Contenedorización** | Docker | Entorno reproducible, incluye ffmpeg para audio |

---

## 4. Módulos del Proyecto

```
civicaid-voice/
├── src/
│   ├── app.py                  # Punto de entrada Flask — create_app() + blueprints
│   │
│   ├── routes/
│   │   ├── webhook.py          # POST /webhook — entrada principal de Twilio
│   │   ├── health.py           # GET /health — healthcheck para Render
│   │   └── static_files.py     # GET /static/cache/* — servir audios .mp3
│   │
│   ├── core/
│   │   ├── config.py           # Variables de entorno y feature flags (dataclass Config)
│   │   ├── cache.py            # Carga demo_cache.json + delega matching a cache_match
│   │   ├── pipeline.py         # Orquestador del pipeline de 10 skills
│   │   ├── models.py           # Dataclasses: IncomingMessage, CacheEntry, FinalResponse, etc.
│   │   ├── twilio_client.py    # Wrapper de Twilio REST API (delega a send_response)
│   │   │
│   │   ├── skills/
│   │   │   ├── detect_input.py     # Skill 1: Detectar tipo de entrada (texto/audio/imagen)
│   │   │   ├── fetch_media.py      # Skill 2: Descargar media desde Twilio (con auth)
│   │   │   ├── convert_audio.py    # Skill 3: Convertir .ogg a .wav con ffmpeg
│   │   │   ├── transcribe.py       # Skill 4: Transcribir audio con Whisper base
│   │   │   ├── detect_lang.py      # Skill 5: Detectar idioma con langdetect
│   │   │   ├── cache_match.py      # Skill 6: Buscar coincidencia en caché por keywords
│   │   │   ├── kb_lookup.py        # Skill 7: Buscar contexto en base de conocimiento JSON
│   │   │   ├── llm_generate.py     # Skill 8: Generar respuesta con Gemini 1.5 Flash
│   │   │   ├── verify_response.py  # Skill 9: Verificar calidad y seguridad de respuesta
│   │   │   └── send_response.py    # Skill 10: Enviar respuesta final por Twilio REST
│   │   │
│   │   └── prompts/
│   │       ├── system_prompt.py    # Prompt del sistema para Gemini
│   │       └── templates.py        # Plantillas de ACK, fallback y errores (es/fr/en)
│   │
│   └── utils/
│       ├── logger.py           # Logging estructurado con contexto de sesión
│       └── timing.py           # Decorador para medir tiempos de ejecución
│
├── data/
│   ├── cache/
│   │   ├── demo_cache.json     # Respuestas precalculadas para demo (8 entradas)
│   │   └── *.mp3               # 6 audios pregrabados (es × 3 trámites + fr × 2 + vision)
│   │
│   └── tramites/
│       ├── imv.json            # Base de conocimiento: Ingreso Mínimo Vital
│       ├── empadronamiento.json # Base de conocimiento: Empadronamiento
│       └── tarjeta_sanitaria.json # Base de conocimiento: Tarjeta Sanitaria
│
├── tests/
│   ├── unit/
│   │   ├── test_cache.py           # Tests de coincidencia de caché
│   │   ├── test_config.py          # Tests de configuración y feature flags
│   │   ├── test_detect_input.py    # Tests de detección de tipo de entrada
│   │   ├── test_detect_lang.py     # Tests de detección de idioma
│   │   └── test_kb_lookup.py       # Tests de búsqueda en KB
│   ├── integration/
│   │   ├── test_pipeline.py        # Tests del pipeline completo
│   │   ├── test_twilio_stub.py     # Tests con stub de Twilio
│   │   └── test_webhook.py         # Tests de integración del webhook
│   └── e2e/
│       └── test_demo_flows.py      # Tests end-to-end de flujos de demo
│
├── Dockerfile
├── render.yaml
├── pyproject.toml
└── requirements.txt
```

---

## 5. Pipeline de 10 Skills

El pipeline es una cadena secuencial de 10 skills especializadas. Cada skill recibe el contexto acumulado y lo enriquece para la siguiente. El orquestador (`pipeline.py`) ejecuta las skills en orden y gestiona errores con fallbacks.

```
detect_input → fetch_media → convert_audio → transcribe → detect_lang
     → cache_match → kb_lookup → llm_generate → verify_response → send_response
```

| # | Skill | Entrada | Salida | Timeout | Notas |
|---|---|---|---|---|---|
| 1 | `detect_input` | IncomingMessage | input_type (TEXT/AUDIO/IMAGE) | — | Examina NumMedia y MediaContentType |
| 2 | `fetch_media` | MediaUrl | bytes (.ogg) | 10s | Solo si input_type=AUDIO/IMAGE. Usa auth de Twilio |
| 3 | `convert_audio` | bytes .ogg | bytes .wav | 5s | Usa ffmpeg. Solo si AUDIO |
| 4 | `transcribe` | bytes .wav | TranscriptResult | 12s | Whisper base. Solo si AUDIO y WHISPER_ON=true |
| 5 | `detect_lang` | texto | idioma (es/en/fr/ar/uk) | — | langdetect. Fallback: "es" |
| 6 | `cache_match` | texto + idioma | CacheResult | — | Búsqueda por keywords normalizados |
| 7 | `kb_lookup` | texto + trámite detectado | KBContext | — | Solo si cache MISS. Extrae secciones relevantes del JSON |
| 8 | `llm_generate` | texto + KBContext + idioma | LLMResponse | 6s | Solo si cache MISS. Gemini 1.5 Flash |
| 9 | `verify_response` | LLMResponse | LLMResponse (validada) | — | Verifica longitud, idioma, ausencia de alucinaciones |
| 10 | `send_response` | FinalResponse | mensaje enviado | 10s | Twilio REST API. Incluye texto + URL de audio si disponible |

### Flujo condicional:

- **Texto**: Skills 1 → 5 → 6 → (7 → 8 → 9 si MISS) → 10
- **Audio**: Skills 1 → 2 → 3 → 4 → 5 → 6 → (7 → 8 → 9 si MISS) → 10
- **Imagen**: Skills 1 → 2 → 6 (match de demo para imagen) → 10

---

## 6. Dataclasses

Todas las estructuras de datos están definidas como `dataclasses` de Python para garantizar tipado, inmutabilidad donde corresponda, y claridad en las interfaces entre skills.

```python
class InputType(Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"

@dataclass
class IncomingMessage:
    """Mensaje entrante parseado desde el POST de Twilio."""
    from_number: str                    # Número del remitente (whatsapp:+34...)
    body: str                           # Texto del mensaje (vacío si es audio)
    media_url: Optional[str] = None     # URL del primer adjunto
    media_type: Optional[str] = None    # MIME type (audio/ogg, image/jpeg)
    input_type: InputType = InputType.TEXT  # Tipo detectado por detect_input
    timestamp: float = 0.0             # Epoch del momento de recepción

@dataclass
class AckResponse:
    """TwiML XML devuelto como HTTP 200 inmediato."""
    message: str              # Texto del ACK (localizado)
    twiml_xml: str            # XML completo de TwiML

@dataclass
class TranscriptResult:
    """Resultado de la transcripción de audio con Whisper."""
    text: str                 # Texto transcrito
    language: str             # Idioma detectado por Whisper
    duration_ms: int          # Milisegundos de procesamiento
    success: bool             # True si la transcripción fue exitosa
    error: Optional[str] = None  # Mensaje de error si falló

@dataclass
class CacheEntry:
    """Entrada individual en demo_cache.json."""
    id: str                   # Identificador único (ej: "ahmed_empadronamiento_fr")
    patterns: List[str]       # Keywords para matching (ej: ["inscrire", "mairie"])
    match_mode: str           # "any_keyword" | "image_demo"
    idioma: str               # Idioma de la respuesta: "fr" | "es" | "any"
    respuesta: str            # Texto completo de la respuesta
    audio_file: Optional[str] = None  # Nombre del .mp3 asociado

@dataclass
class CacheResult:
    """Resultado de la búsqueda en caché."""
    hit: bool                           # True si se encontró coincidencia
    entry: Optional[CacheEntry] = None  # Entrada encontrada (None si miss)
    score: float = 0.0                  # Puntuación de coincidencia (0.0-1.0)

@dataclass
class KBContext:
    """Contexto extraído de la base de conocimiento para el LLM."""
    tramite: str              # Nombre del trámite identificado
    datos: dict = {}          # Datos estructurados del JSON del trámite
    fuente_url: str = ""      # URL oficial de referencia
    verificado: bool = False  # Si los datos están verificados oficialmente

@dataclass
class LLMResponse:
    """Respuesta generada por Gemini."""
    text: str                 # Texto de la respuesta
    language: str             # Idioma de la respuesta
    duration_ms: int          # Milisegundos de generación
    from_cache: bool          # True si se usó caché en vez de LLM
    success: bool             # True si la generación fue exitosa
    error: Optional[str] = None  # Mensaje de error si falló

@dataclass
class FinalResponse:
    """Respuesta final enviada al usuario por Twilio REST."""
    to_number: str                     # Número destino (whatsapp:+34...)
    body: str                          # Texto de la respuesta
    media_url: Optional[str] = None    # URL del audio MP3 (pre-hosted)
    source: str = "cache"              # Origen: "cache" | "llm" | "fallback"
    total_ms: int = 0                  # Tiempo total de procesamiento en ms
```

---

## 7. Feature Flags

Las feature flags permiten controlar el comportamiento de Clara sin cambiar código, especialmente útil para alternar entre modo demo y modo producción.

| Flag | Tipo | Default | Descripción |
|---|---|---|---|
| `DEMO_MODE` | `bool` | `true` | Activa el modo demo: prioriza respuestas de caché, usa audios pregrabados |
| `LLM_LIVE` | `bool` | `true` | Habilita las llamadas al LLM (Gemini). Si es `false`, solo responde desde caché |
| `WHISPER_ON` | `bool` | `true` | Habilita la transcripción de audio con Whisper. Si es `false`, los audios se ignoran |
| `LLM_TIMEOUT` | `int` | `6` (segundos) | Timeout máximo para la llamada a Gemini 1.5 Flash |
| `WHISPER_TIMEOUT` | `int` | `12` (segundos) | Timeout máximo para la transcripción con Whisper base |
| `AUDIO_BASE_URL` | `str` | URL de Render | URL base para servir los archivos de audio .mp3 pregrabados |

### Combinaciones típicas:

- **Demo en hackathon**: `DEMO_MODE=true`, `LLM_LIVE=true`, `WHISPER_ON=true` — Caché primero, LLM como fallback.
- **Solo caché**: `DEMO_MODE=true`, `LLM_LIVE=false` — Sin dependencia de APIs externas.
- **Producción completa**: `DEMO_MODE=false`, `LLM_LIVE=true`, `WHISPER_ON=true` — Pipeline completo sin priorizar caché.

---

## 8. Decisiones de Diseño

### 8.1 ¿Por qué caché primero? (Cache-first para fiabilidad en demo)

En un contexto de hackathon, la fiabilidad de la demo es crítica. Las APIs externas (Gemini, Whisper) pueden fallar, tener latencia variable o devolver respuestas inconsistentes. El enfoque **cache-first** garantiza que los escenarios de demo más comunes (preguntas sobre IMV, empadronamiento, tarjeta sanitaria en español, inglés y francés) siempre producen una respuesta inmediata, consistente y con audio pregrabado. El LLM solo interviene cuando la caché no tiene una respuesta adecuada.

### 8.2 ¿Por qué sin base de datos? (JSON suficiente para 3 trámites)

Clara maneja información sobre exactamente **3 trámites administrativos**. La base de conocimiento completa cabe en menos de 50 KB de JSON. Introducir una base de datos (PostgreSQL, SQLite, Redis) añadiría:

- Complejidad de configuración y conexión.
- Dependencia adicional en el despliegue.
- Overhead innecesario para un volumen de datos tan reducido.

Los archivos JSON son **versionables en Git**, editables con cualquier editor, y se cargan en memoria al inicio de la aplicación. Para el alcance actual (3 trámites, ~20 preguntas frecuentes), esta solución es óptima.

### 8.3 ¿Por qué una sola llamada al LLM? (No multi-agente)

Arquitecturas multi-agente (un agente para clasificar, otro para responder, otro para verificar) multiplican la latencia y el coste. Clara usa **una única llamada a Gemini 1.5 Flash** con un prompt que incluye:

- El system prompt con las instrucciones del rol.
- El contexto relevante de la base de conocimiento (KBContext).
- El mensaje del usuario.

El modelo recibe todo lo necesario para generar una respuesta completa en una sola invocación. La verificación posterior (Skill 9) es una validación programática local, no otra llamada al LLM.

### 8.4 ¿Por qué Whisper base? (Restricciones de RAM en Render free)

El tier gratuito de Render asigna **512 MB de RAM**. Los modelos de Whisper tienen estos requisitos:

| Modelo | Parámetros | RAM requerida |
|---|---|---|
| `tiny` | 39M | ~150 MB |
| `base` | 74M | ~290 MB |
| `small` | 244M | ~960 MB |
| `medium` | 769M | ~3 GB |

**Whisper `base`** es el modelo más grande que cabe en memoria junto con la aplicación Flask y sus dependencias (~200 MB adicionales). Ofrece un buen equilibrio entre precisión multilingüe y consumo de recursos. El modelo `tiny` sacrifica demasiada calidad en idiomas como árabe y ucraniano; `small` excede la memoria disponible.

---

## 9. Diagramas

La documentación visual de la arquitectura se encuentra en tres archivos Mermaid ubicados junto a este documento:

### 9.1 Diagrama de Secuencia: Patrón TwiML ACK + REST

**Archivo**: [`sequence-wa-ack-rest.mmd`](./sequence-wa-ack-rest.mmd)

Muestra el flujo temporal completo desde que el usuario envía un mensaje en WhatsApp hasta que recibe la respuesta final. Ilustra el patrón de doble respuesta: ACK inmediato vía TwiML y respuesta completa vía Twilio REST API. Incluye el camino alternativo para entrada de audio (fetch, conversión, transcripción) y la bifurcación entre cache HIT y cache MISS.

### 9.2 Diagrama de Flujo de Datos

**Archivo**: [`dataflow.mmd`](./dataflow.mmd)

Representa el flujo de datos a través del pipeline de 10 skills como un flowchart. Muestra cómo los tres tipos de entrada (texto, audio, imagen) convergen en el pipeline y cómo se ramifican según los resultados de la caché. Útil para entender las decisiones condicionales del sistema.

### 9.3 Diagrama de Componentes

**Archivo**: [`components.mmd`](./components.mmd)

Vista estática de la arquitectura mostrando todos los módulos del sistema, sus agrupaciones lógicas (routes, core, skills, data) y las dependencias entre componentes internos y servicios externos (Twilio, Whisper, Gemini). Útil para entender la estructura del código y las integraciones.

---

## 10. Referencias Rápidas

| Recurso | Ubicación |
|---|---|
| Punto de entrada | [`src/app.py`](../../src/app.py) — `create_app()` registra blueprints |
| Configuración | [`src/core/config.py`](../../src/core/config.py) — dataclass `Config` con feature flags |
| Pipeline | [`src/core/pipeline.py`](../../src/core/pipeline.py) — orquestador `process()` |
| Skills (10) | [`src/core/skills/*.py`](../../src/core/skills/) |
| Plantillas | [`src/core/prompts/templates.py`](../../src/core/prompts/templates.py) — ACK, fallback, errores |
| Base de conocimiento | [`data/tramites/*.json`](../../data/tramites/) — 3 trámites |
| Caché de demo | [`data/cache/demo_cache.json`](../../data/cache/demo_cache.json) — 8 entradas |
| Tests | [`tests/`](../../tests/) — unit, integration, e2e |
| Dockerfile | [`Dockerfile`](../../Dockerfile) |
| Despliegue | Render (free tier) con [`render.yaml`](../../render.yaml) y auto-deploy desde `main` |
| Plan maestro | [`docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md`](../01-phases/FASE0-PLAN-MAESTRO-FINAL.md) |
| Implementación MVP | [`docs/01-phases/FASE1-IMPLEMENTACION-MVP.md`](../01-phases/FASE1-IMPLEMENTACION-MVP.md) |
| Runbook demo | [`docs/03-runbooks/RUNBOOK-DEMO.md`](../03-runbooks/RUNBOOK-DEMO.md) |
