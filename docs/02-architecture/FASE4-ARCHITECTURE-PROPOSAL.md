# Fase 4 "Humana" -- Propuesta de Arquitectura para Clara

> **Resumen en una linea:** Analisis exhaustivo de 3 arquitecturas candidatas para la Fase 4 de Clara, con investigacion web, diagramas ASCII, presupuesto de RAM, gestion de estado conversacional, feature flags y estrategia de mitigacion de cold starts.

> **Fecha:** 2026-02-13
> **Autor:** Agent 5 — Systems Architect
> **Estado:** PROPUESTA (pendiente de validacion por el equipo)

---

## Indice

1. [Investigacion Web — Hallazgos Clave](#1-investigacion-web--hallazgos-clave)
2. [Propuesta de 3 Arquitecturas](#2-propuesta-de-3-arquitecturas)
3. [Seleccion de Arquitectura Recomendada](#3-seleccion-de-arquitectura-recomendada)
4. [5 Diagramas ASCII (F1 a F4 + Pipeline Detallado)](#4-5-diagramas-ascii-f1-a-f4--pipeline-detallado)
5. [Sistema de Gestion de Estado](#5-sistema-de-gestion-de-estado)
6. [Feature Flags para Fase 4](#6-feature-flags-para-fase-4)
7. [Mitigacion de Cold Starts](#7-mitigacion-de-cold-starts)
8. [Presupuesto de RAM](#8-presupuesto-de-ram)
9. [Fuentes y Referencias](#9-fuentes-y-referencias)

---

## 1. Investigacion Web -- Hallazgos Clave

### 1.1 Monolito vs Microservicios para Bots en Entornos Restringidos

**Conclusion: MONOLITO es la opcion correcta para 512MB RAM.**

Los microservicios introducen overhead de red, duplicacion de runtimes y complejidad operacional que no se justifica con un solo endpoint `/webhook` y 512MB de RAM. Un monolito con buen diseno modular interno (el patron actual de Clara con skills) ofrece las ventajas de separacion de responsabilidades sin el coste de RAM de procesos separados.

Referencia: [Atlassian - Microservices vs Monolith](https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith) | [The New Stack - Operational Comparison](https://thenewstack.io/microservices/microservices-vs-monoliths-an-operational-comparison/)

### 1.2 Clasificacion de Intenciones sin Modelos Pesados

**Estrategia recomendada: Cascada Regex -> Keywords -> fastText comprimido.**

| Estrategia | RAM | Latencia | Precision | Complejidad |
|------------|-----|----------|-----------|-------------|
| Regex + keywords | ~0 MB | <1ms | Media-baja | Baja |
| fastText comprimido | 5-20 MB | <1ms | Alta | Media |
| fastText completo | 500+ MB | <1ms | Muy alta | Media |
| Modelo transformer | 200+ MB | 50-100ms | Muy alta | Alta |

Para Clara, la cascada en 3 niveles es optima:
1. **Regex** para intenciones explicitas ("quiero solicitar el IMV", "necesito empadronarme")
2. **Keywords ponderados** para deteccion de tramite (ya implementado en `kb_lookup.py`)
3. **fastText comprimido** (~20MB) como fallback para clasificacion ambigua

Referencia: [Label Your Data - Intent Classification 2025](https://labelyourdata.com/articles/machine-learning/intent-classification) | [FastText - Meta AI](https://ai.meta.com/tools/fasttext/) | [DataCamp - Intent with Regex](https://campus.datacamp.com/courses/building-chatbots-in-python/understanding-natural-language?ex=2)

### 1.3 Gestion de Estado Conversacional

**Estrategia recomendada: dict en memoria con TTL (hackathon) + SQLite opcional (persistencia).**

| Almacenamiento | Latencia | Persistencia | RAM | Complejidad |
|---------------|----------|-------------|-----|-------------|
| dict en memoria | ~0ms | No | Variable | Nula |
| SQLite | ~1ms | Si | ~5MB | Baja |
| Redis | ~1ms | Parcial | Externo | Media |
| PostgreSQL | ~5ms | Si | Externo | Alta |

Redis requiere un servicio externo (coste adicional en Render). SQLite es el punto medio perfecto: persistencia real, cero dependencias externas, < 5MB de footprint.

Referencia: [Kevin de Bree - Chatbot Persistent Memory SQLite](https://medium.com/@kpdebree/solving-chatbot-amnesia-building-an-ai-agent-with-persistent-memory-using-python-openai-and-b9ec166c298a) | [Redis - Real-Time Chatbots](https://redis.io/blog/redis-as-the-engine-behind-real-time-intelligent-chatbots/)

### 1.4 TTS Open-Source: Estrategias de Servicio

**Conclusion: Pre-generacion + gTTS on-demand. Piper y Kokoro NO caben en 512MB.**

| Motor TTS | RAM en runtime | Calidad | Idiomas (es/fr/ar) | Viable en 512MB |
|-----------|---------------|---------|---------------------|-----------------|
| gTTS (Google TTS) | ~0 MB (API web) | Media | es, fr, ar | SI |
| Piper TTS (onnx) | ~500 MB | Alta | es (limitado), fr | NO |
| Kokoro-82M | ~200-300 MB | Alta | en (otros limitado) | AJUSTADO |
| MMS (Meta) | ~300+ MB | Media | es, fr, ar | NO |
| edge-tts (Microsoft) | ~0 MB (API web) | Alta | es, fr, ar | SI |

**Estrategia optima para 512MB:**
- **Pre-generacion:** Audios pregrabados en MP3 para las ~20 respuestas mas comunes de los flujos guiados (patron actual ampliado).
- **On-demand:** gTTS o edge-tts para respuestas LLM dinamicas. Ambos son APIs web gratuitas sin modelo local.
- **Futuro (si se sube a 1GB):** Piper TTS con modelos `low` (~50MB modelo, ~200MB runtime).

Referencia: [Inferless - 12 Best Open-Source TTS Models 2025](https://www.inferless.com/learn/comparing-different-text-to-speech---tts--models-part-2) | [Piper TTS GitHub](https://github.com/rhasspy/piper) | [Kokoro-82M HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) | [BentoML - Best Open-Source TTS 2026](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)

### 1.5 Restricciones de Render Free Tier

| Restriccion | Valor | Impacto |
|-------------|-------|---------|
| RAM | 512 MB | Limite duro. OOM = crash |
| CPU | 0.1 vCPU | Procesamiento lento en CPU |
| Sleep despues de inactividad | 15 minutos | Requiere keep-alive |
| Cold start | 30-50 segundos | Primera peticion lenta |
| Horas mensuales | 750 h (31 dias) | Suficiente para 24/7 con keep-alive |
| Ancho de banda | 100 GB/mes | Suficiente |
| Disco efimero | Si | Los archivos TTS se pierden al reiniciar |

Referencia: [Render Community - Free Tier](https://community.render.com/t/the-free-instance-type-e-g-512mb-ram-0-1-cpu/39044) | [FreeTiers - Render Infographic](https://www.freetiers.com/directory/render) | [Render Community - Sleep Behavior](https://community.render.com/t/do-web-services-on-a-free-tier-go-to-sleep-after-some-time-inactive/3303)

### 1.6 Patrones de Tareas en Background para Flask

**Conclusion: `threading.Thread` (patron actual) es suficiente para el hackathon.**

| Patron | Overhead RAM | Complejidad | Dependencias | Fiabilidad |
|--------|-------------|-------------|-------------|------------|
| `threading.Thread` | ~0 MB | Nula | Ninguna | Baja (daemon=True pierde tareas) |
| `concurrent.futures.ThreadPoolExecutor` | ~2 MB | Baja | Ninguna | Media (pool controlado) |
| RQ (Redis Queue) | +50 MB (Redis) | Media | Redis externo | Alta |
| Celery | +100 MB (broker) | Alta | RabbitMQ/Redis | Muy alta |
| Huey | +30 MB (Redis) | Media | Redis | Alta |

**Recomendacion Fase 4:** Migrar de `threading.Thread` a `ThreadPoolExecutor(max_workers=4)` para controlar el numero maximo de hilos y evitar que picos de trafico agoten la memoria. No requiere dependencias externas.

Referencia: [Miguel Grinberg - Flask Background Jobs](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs) | [DevProPortal - Celery vs RQ vs Dramatiq 2025](https://devproportal.com/languages/python/python-background-tasks-celery-rq-dramatiq-comparison-2025/) | [Flask Docs - Celery](https://flask.palletsprojects.com/en/stable/patterns/celery/)

### 1.7 Audio en WhatsApp via Twilio

**Hallazgo critico: Solo archivos OGG se reproducen nativamente en WhatsApp.** Los MP3 aparecen como archivo descargable.

| Formato | Reproduccion en WhatsApp | Limite |
|---------|--------------------------|--------|
| OGG (opus) | Nativa (burbuja de audio) | 16 MB |
| MP3 | Descargable (no inline) | 16 MB |
| WAV | Descargable | 16 MB |

**Accion para Fase 4:** Convertir la generacion TTS a formato OGG/opus para que el audio se reproduzca nativamente en WhatsApp como mensaje de voz.

Los archivos deben servirse desde una URL publica accesible por HTTPS. Opciones:
1. **Ruta estatica de Flask** (patron actual: `/static/cache/`)
2. **Twilio Assets** — CDN gratuito de Twilio para media estatico
3. **Render static** — servir desde el mismo contenedor

Referencia: [Twilio - WhatsApp Media Guidance](https://www.twilio.com/docs/whatsapp/guidance-whatsapp-media-messages) | [Twilio - Accepted MIME Types](https://www.twilio.com/docs/messaging/guides/accepted-mime-types) | [Twilio - Assets](https://www.twilio.com/docs/serverless/functions-assets/assets)

---

## 2. Propuesta de 3 Arquitecturas

---

### Arquitectura A: "Monolito Conversacional Extendido"

**Descripcion:** Evolucion natural del monolito actual. Se anaden estado conversacional, clasificacion de intenciones y flujos guiados como skills adicionales dentro del pipeline existente. Sin dependencias externas nuevas.

```
+======================================================================+
|                    ARQUITECTURA A: MONOLITO EXTENDIDO                 |
+======================================================================+

  Usuario WhatsApp
       |
       v
  [Twilio Cloud]
       |
       v POST /webhook
  +------------------------------------------------------------+
  |  FLASK APP (monolito)                    512 MB RAM total  |
  |                                                            |
  |  +------------------+     +---------------------------+    |
  |  | webhook.py       |     | ThreadPoolExecutor(4)     |    |
  |  | TwiML ACK <1s    |---->| pipeline_v2.process()     |    |
  |  +------------------+     +---------------------------+    |
  |                                  |                         |
  |                                  v                         |
  |  +-------------------------------------------------------+ |
  |  |              PIPELINE v2 (15 skills)                   | |
  |  |                                                        | |
  |  |  [guardrail_pre] --> [detect_input]                    | |
  |  |       |                    |                           | |
  |  |       v                    v                           | |
  |  |  [session_load] --> [AUDIO: fetch+transcribe]          | |
  |  |       |                    |                           | |
  |  |       v                    v                           | |
  |  |  [detect_lang] --> [intent_classify]                   | |
  |  |                         |                              | |
  |  |          +--------------+---------------+              | |
  |  |          v              v               v              | |
  |  |     [cache_match]  [kb_lookup]  [guided_flow_step]     | |
  |  |          |              |               |              | |
  |  |          v              v               v              | |
  |  |     [SEND si HIT] [llm_generate] [state_update]       | |
  |  |                        |               |              | |
  |  |                        v               v              | |
  |  |                   [verify] --> [guardrail_post]        | |
  |  |                        |                              | |
  |  |                        v                              | |
  |  |                   [tts_generate]                       | |
  |  |                        |                              | |
  |  |                        v                              | |
  |  |                   [session_save]                       | |
  |  |                        |                              | |
  |  |                        v                              | |
  |  |                   [send_response]                      | |
  |  +-------------------------------------------------------+ |
  |                                                            |
  |  +-------------------+  +----------------+  +----------+   |
  |  | ConversationStore |  | demo_cache.json|  | KB .json |   |
  |  | (dict + TTL)      |  | (8 entradas)   |  | (3 tram) |   |
  |  +-------------------+  +----------------+  +----------+   |
  +------------------------------------------------------------+
       |
       v Twilio REST API
  [Twilio Cloud] --> Usuario WhatsApp
```

**Estimacion de RAM:**

| Componente | RAM (MB) |
|------------|----------|
| Python 3.11 runtime | 30 |
| Flask + dependencias | 25 |
| Pipeline + skills | 10 |
| ConversationStore (100 sesiones) | 5 |
| demo_cache + KB JSON | 2 |
| gTTS (on-demand, sin modelo) | 0 |
| langdetect | 5 |
| Twilio SDK | 10 |
| google-generativeai SDK | 15 |
| Overhead GC + buffers | 30 |
| **Total estimado** | **~132 MB** |

**Estimacion de latencia:**

| Escenario | Latencia estimada |
|-----------|-------------------|
| Cache HIT (texto) | 50-100 ms |
| Cache MISS + LLM (texto) | 2-6 s |
| Audio + LLM | 4-12 s |
| Flujo guiado (step ya calculado) | 100-200 ms |

**Tabla de Pros/Contras:**

| Pros | Contras |
|------|---------|
| Minimo cambio respecto a F3 | Estado se pierde al reiniciar (dict en memoria) |
| Cero dependencias nuevas | ThreadPoolExecutor no persiste tareas |
| Bajo consumo de RAM (~132 MB) | Sin persistencia real de sesion |
| Facil de testear (todo in-process) | Escalado limitado a 1 instancia |
| Deploy identico al actual | Flujos guiados complejos pueden complicar pipeline.py |

**Estrategia de feature flags:**
- Nuevos flags se anaden al dataclass `Config` existente.
- `GUIDED_FLOWS_ON`, `INTENT_CLASSIFIER_ON` controlan las nuevas skills.
- Backward-compatible: con flags desactivados, se comporta exactamente como Fase 3.

**Cadena de fallback:**
```
intent_classify FALLO --> keyword match (actual)
guided_flow FALLO --> llm_generate (actual)
session_load FALLO --> sesion nueva (sin historial)
tts FALLO --> solo texto (actual)
llm_generate FALLO --> fallback template (actual)
```

---

### Arquitectura B: "Monolito con SQLite State + Intent Engine"

**Descripcion:** Monolito como en A, pero con SQLite para persistencia de estado conversacional, y un motor de intenciones basado en reglas + fastText comprimido. La persistencia permite retomar conversaciones tras cold starts.

```
+======================================================================+
|              ARQUITECTURA B: MONOLITO + SQLite + INTENT              |
+======================================================================+

  Usuario WhatsApp
       |
       v
  [Twilio Cloud]
       |
       v POST /webhook
  +------------------------------------------------------------+
  |  FLASK APP (monolito)                    512 MB RAM total  |
  |                                                            |
  |  +------------------+     +---------------------------+    |
  |  | webhook.py       |     | ThreadPoolExecutor(4)     |    |
  |  | TwiML ACK <1s    |---->| pipeline_v2.process()     |    |
  |  +------------------+     +---------------------------+    |
  |                                  |                         |
  |       +------+------+------+-----+-------+                 |
  |       v      v      v      v             v                 |
  |  +---------+----+-------+--------+  +-----------+          |
  |  |PIPELINE v2   |       |        |  | INTENT    |          |
  |  |15 skills     |       |        |  | ENGINE    |          |
  |  |(mismo que A) |       |        |  |           |          |
  |  |              |       |        |  | 1. regex  |          |
  |  |              |       |        |  | 2. kw     |          |
  |  |              |       |        |  | 3. fastTx |          |
  |  +---------+----+-------+--------+  +-----------+          |
  |            |                              |                |
  |            v                              v                |
  |  +-------------------------------------------------------+ |
  |  |                   SQLite (state.db)                    | |
  |  |                                                        | |
  |  |  sessions:                                             | |
  |  |    phone_hash TEXT PK                                  | |
  |  |    state_json TEXT                                     | |
  |  |    tramite TEXT                                        | |
  |  |    step INTEGER                                        | |
  |  |    language TEXT                                        | |
  |  |    updated_at REAL                                     | |
  |  |    created_at REAL                                     | |
  |  |                                                        | |
  |  |  conversation_log:                                     | |
  |  |    id INTEGER PK AUTOINCREMENT                         | |
  |  |    phone_hash TEXT                                     | |
  |  |    role TEXT (user|assistant)                           | |
  |  |    content TEXT                                        | |
  |  |    timestamp REAL                                      | |
  |  +-------------------------------------------------------+ |
  |                                                            |
  |  +----------------+  +----------+  +-----------+           |
  |  | demo_cache.json|  | KB .json |  | fastText  |           |
  |  | (8+ entradas)  |  | (3 tram) |  | (~20 MB)  |           |
  |  +----------------+  +----------+  +-----------+           |
  +------------------------------------------------------------+
       |
       v Twilio REST API
  [Twilio Cloud] --> Usuario WhatsApp

  [Disco efimero: /tmp/state.db]
  (Se pierde al reiniciar Render free tier — pero se recrea vacio)
```

**Estimacion de RAM:**

| Componente | RAM (MB) |
|------------|----------|
| Python 3.11 runtime | 30 |
| Flask + dependencias | 25 |
| Pipeline + skills | 10 |
| SQLite (in-process, shared cache) | 8 |
| fastText comprimido (intent model) | 20 |
| demo_cache + KB JSON | 2 |
| gTTS (on-demand) | 0 |
| langdetect | 5 |
| Twilio SDK | 10 |
| google-generativeai SDK | 15 |
| Overhead GC + buffers | 30 |
| **Total estimado** | **~155 MB** |

**Estimacion de latencia:**

| Escenario | Latencia estimada |
|-----------|-------------------|
| Cache HIT (texto) | 50-100 ms |
| Cache MISS + intent + LLM (texto) | 2-7 s |
| Audio + intent + LLM | 4-13 s |
| Flujo guiado (step desde SQLite) | 2-5 ms |
| Intent classify (regex+kw) | <1 ms |
| Intent classify (fastText) | <2 ms |

**Tabla de Pros/Contras:**

| Pros | Contras |
|------|---------|
| Persistencia de estado (sobrevive a reinicios de hilo) | SQLite en disco efimero de Render se pierde al reiniciar |
| Intent engine rapido y preciso | fastText comprimido requiere entrenamiento previo (+20MB) |
| Historial de conversacion para contexto LLM | Mas complejidad en el setup |
| Permite retomar flujos guiados | SQLite no soporta escrituras concurrentes bien |
| Logging de conversacion para analytics | Necesita migracion de schema |

**A VALIDAR:** El disco efimero de Render free tier persiste entre requests pero NO entre deploys o restarts del contenedor. Para un hackathon esto es aceptable (sesiones duran minutos, no dias), pero para produccion se necesitaria un volumen persistente o base de datos externa.

**Estrategia de feature flags:**
- Mismos flags que A, mas:
  - `STATE_BACKEND=memory|sqlite` — permite alternar entre dict y SQLite.
  - `FASTTEXT_INTENT_ON=false` — carga el modelo de fastText solo si esta activado.
- Backward-compatible con Fase 3.

**Cadena de fallback:**
```
fastText FALLO --> keyword match --> regex match
SQLite FALLO --> dict en memoria (degradacion graceful)
session_load FALLO --> sesion nueva
guided_flow FALLO --> llm_generate
tts FALLO --> solo texto
llm_generate FALLO --> fallback template
```

---

### Arquitectura C: "Monolito Event-Driven con Pre-generacion Agresiva"

**Descripcion:** Enfoque radicalmente diferente: pre-generar TODAS las respuestas posibles de los flujos guiados (texto + audio) en build time, convirtiendo los flujos guiados en un grafo estatico navegable. El LLM solo interviene para preguntas fuera de los flujos predefinidos.

```
+======================================================================+
|           ARQUITECTURA C: PRE-GENERACION + GRAFO ESTATICO            |
+======================================================================+

  FASE DE BUILD (offline, en CI/CD o local):
  +-----------------------------------------------------------+
  |                                                           |
  |  [flow_definitions/*.yaml] --> [build_flows.py]           |
  |       |                            |                      |
  |       v                            v                      |
  |  [Gemini 1.5 Flash]        [gTTS / edge-tts]             |
  |  Genera texto para          Genera OGG para               |
  |  cada paso de cada          cada respuesta                 |
  |  flujo guiado               pregenerada                    |
  |       |                            |                      |
  |       v                            v                      |
  |  [data/flows/               [data/flows/                  |
  |   imv_flow.json              imv_step1.ogg                |
  |   empad_flow.json            imv_step2.ogg                |
  |   ts_flow.json]              ...]                         |
  +-----------------------------------------------------------+

  RUNTIME (512 MB Render):
  +------------------------------------------------------------+
  |  FLASK APP                               512 MB RAM total  |
  |                                                            |
  |  +------------------+     +---------------------------+    |
  |  | webhook.py       |     | ThreadPoolExecutor(4)     |    |
  |  | TwiML ACK <1s    |---->| pipeline_v2.process()     |    |
  |  +------------------+     +---------------------------+    |
  |                                  |                         |
  |                                  v                         |
  |  +-------------------------------------------------------+ |
  |  |              PIPELINE v2 (13 skills)                   | |
  |  |                                                        | |
  |  |  [guardrail_pre]                                       | |
  |  |       |                                                | |
  |  |       v                                                | |
  |  |  [detect_input] --> [AUDIO: fetch+transcribe]          | |
  |  |       |                    |                           | |
  |  |       v                    v                           | |
  |  |  [session_load] --> [detect_lang]                      | |
  |  |       |                                                | |
  |  |       v                                                | |
  |  |  [flow_router]                                         | |
  |  |       |                                                | |
  |  |   +---+---+                                            | |
  |  |   v       v                                            | |
  |  |  EN      FUERA                                         | |
  |  |  FLUJO   DE FLUJO                                      | |
  |  |   |       |                                            | |
  |  |   v       v                                            | |
  |  |  [flow   [cache -->  kb_lookup -->                     | |
  |  |   step]   match]     llm_generate -->                  | |
  |  |   |       |          verify]                           | |
  |  |   |       |             |                              | |
  |  |   v       v             v                              | |
  |  |  [resp.  [guardrail_post]                              | |
  |  |   pre-        |                                        | |
  |  |   generada]   v                                        | |
  |  |   |      [tts on-demand]                               | |
  |  |   |           |                                        | |
  |  |   +-----+-----+                                        | |
  |  |         v                                              | |
  |  |    [session_save]                                       | |
  |  |         |                                              | |
  |  |         v                                              | |
  |  |    [send_response]                                      | |
  |  +-------------------------------------------------------+ |
  |                                                            |
  |  +------------------+  +----------+  +------------------+  |
  |  | flows/*.json     |  | KB .json |  | ConversationStore|  |
  |  | (pregenerado)    |  | (3 tram) |  | (dict + TTL)     |  |
  |  | + OGG/MP3 audio  |  |          |  |                  |  |
  |  +------------------+  +----------+  +------------------+  |
  +------------------------------------------------------------+
       |
       v Twilio REST API
  [Twilio Cloud] --> Usuario WhatsApp
```

**Estimacion de RAM:**

| Componente | RAM (MB) |
|------------|----------|
| Python 3.11 runtime | 30 |
| Flask + dependencias | 25 |
| Pipeline + skills | 10 |
| ConversationStore (100 sesiones) | 5 |
| Flow graphs (3 tramites x ~50KB) | 1 |
| demo_cache + KB JSON | 2 |
| Pre-generated audio index | 1 |
| gTTS (on-demand para LLM fallback) | 0 |
| langdetect | 5 |
| Twilio SDK | 10 |
| google-generativeai SDK | 15 |
| Overhead GC + buffers | 30 |
| **Total estimado** | **~134 MB** |

**Estimacion de latencia:**

| Escenario | Latencia estimada |
|-----------|-------------------|
| Flujo guiado (step pregenerado) | 10-50 ms |
| Flujo guiado con audio pregenerado | 10-50 ms |
| Fuera de flujo + cache HIT | 50-100 ms |
| Fuera de flujo + LLM | 2-6 s |
| Audio transcripcion + flujo | 4-12 s |

**Tabla de Pros/Contras:**

| Pros | Contras |
|------|---------|
| Latencia ultra-baja para flujos guiados | Requiere paso de build separado |
| Audio pregenerado en formato OGG | Respuestas estaticas (no personalizadas) |
| Minimo consumo de RAM en runtime | Mas archivos en el repo (audios) |
| Sin dependencia de Gemini para flujos comunes | Cambiar un flujo requiere re-build |
| Funciona offline (flujos guiados) | Complejidad del build script |
| Fiabilidad maxima para la demo | Menos flexibilidad que LLM on-demand |

**Estrategia de feature flags:**
- `GUIDED_FLOWS_ON=true` — activa el router de flujos.
- `PREGENERATED_AUDIO_ON=true` — usa audio pregenerado en vez de gTTS on-demand.
- `LLM_LIVE=true` — LLM solo para preguntas fuera de flujo.
- `FLOW_DEFINITIONS_PATH=data/flows/` — ruta a las definiciones de flujo.

**Cadena de fallback:**
```
flow_router FALLO --> cache_match --> llm_generate
flujo guiado step FALLO --> llm_generate para ese paso
audio pregenerado NO EXISTE --> gTTS on-demand --> solo texto
session_load FALLO --> sesion nueva, flujo desde paso 1
Gemini FALLO --> fallback template
```

---

## 3. Seleccion de Arquitectura Recomendada

### Recomendacion: ARQUITECTURA C — "Monolito con Pre-generacion + Grafo Estatico"

**Justificacion:**

| Criterio | Peso | A (Extendido) | B (SQLite+Intent) | C (Pre-gen) |
|----------|------|----------------|--------------------|--------------|
| RAM en 512MB | 25% | 132 MB (OK) | 155 MB (OK) | 134 MB (OK) |
| Latencia flujos guiados | 20% | 100-200 ms | 2-5 ms | 10-50 ms |
| Fiabilidad demo | 20% | Media | Media-Alta | MUY ALTA |
| Complejidad implementacion | 15% | Baja | Media-Alta | Media |
| Persistencia estado | 10% | No | Parcial (efimero) | No |
| Experiencia usuario | 10% | Buena | Buena | Excelente |

**Por que C y no las otras:**

1. **Fiabilidad de demo (criterio numero 1 en hackathon):** Las respuestas pregeneradas NUNCA fallan. No hay latencia de API, no hay riesgo de timeout, no hay riesgo de respuestas incoherentes del LLM. Esto es exactamente lo que hizo que la demo de Fase 3 funcionara (cache-first), pero extendido a flujos completos.

2. **Latencia:** Un usuario siguiendo un flujo guiado de empadronamiento recibe respuesta en 10-50ms con audio OGG nativo que se reproduce en la burbuja de WhatsApp. Esto es una experiencia de "app nativa", no de "chatbot lento".

3. **RAM:** Es la mas eficiente en runtime (~134 MB). El trabajo pesado (generacion de texto + audio) se hace en build time, no en runtime.

4. **Escalabilidad de contenido:** Anadir un nuevo tramite es crear un YAML, correr el build script, y hacer deploy. El build script usa Gemini + gTTS una vez, y las respuestas quedan fijadas.

5. **El LLM sigue disponible** para preguntas fuera de flujo. No perdemos la capacidad generativa de Clara, solo la optimizamos donde es predecible.

**Riesgos y mitigaciones:**

| Riesgo | Mitigacion |
|--------|------------|
| Respuestas pregeneradas suenan "roboticas" | Prompt cuidadoso en build time; tono humano |
| Build script complejo | Script bien documentado, idempotente |
| Tamano del repo crece con audios | .gitignore los OGG; solo commitear JSONs de flujo |
| Estado en memoria se pierde | Aceptable para hackathon; flujos cortos (3-5 pasos) |
| Disco efimero pierde TTS dinamico | Se regenera on-demand; flujos guiados son estaticos |

---

## 4. 5 Diagramas ASCII (F1 a F4 + Pipeline Detallado)

### Diagrama 1: Fase 1 (MVP) -- Lo que se construyo

```
+================================================================+
|                DIAGRAMA 1: FASE 1 — MVP                        |
|                32 tests | 14 tareas D1.x                      |
+================================================================+

  Usuario WhatsApp
       |
       | texto / audio / imagen
       v
  [Twilio Cloud]
       |
       v POST /webhook
  +------------------------------------------+
  |  FLASK /webhook                          |
  |  +------------------------------------+  |
  |  | 1. Validar firma Twilio            |  |
  |  | 2. Parsear Body, From, NumMedia    |  |
  |  | 3. detect_input_type               |  |
  |  | 4. TwiML ACK --> HTTP 200 (<1s)    |  |
  |  | 5. threading.Thread(pipeline)      |  |
  |  +------------------------------------+  |
  +------------------------------------------+
       |                    |
       | TwiML ACK         | Background Thread
       v                    v
  [Twilio --> User]    +---------------------------+
  "Un momento..."      | PIPELINE (11 skills)      |
                       |                           |
                       | [detect_input]             |
                       |      |                    |
                       |  +---+---+                |
                       |  v       v                |
                       | TEXT    AUDIO              |
                       |  |      |                 |
                       |  |   [fetch_media]        |
                       |  |   [convert_audio]      |
                       |  |   [transcribe(Whisper)] |
                       |  |      |                 |
                       |  +--+---+                 |
                       |     v                     |
                       | [detect_lang]             |
                       |     |                     |
                       |     v                     |
                       | [cache_match]             |
                       |     |                     |
                       |  +--+--+                  |
                       |  v     v                  |
                       | HIT   MISS                |
                       |  |     |                  |
                       |  |  [kb_lookup]           |
                       |  |  [llm_generate]        |
                       |  |  [verify_response]     |
                       |  |     |                  |
                       |  +--+--+                  |
                       |     v                     |
                       | [send_response]           |
                       | (Twilio REST)             |
                       +---------------------------+
                             |
                             v
                       [Twilio --> User]
                       Respuesta completa

  COMPONENTES FASE 1:
  +------------------+  +----------+  +---------------+
  | demo_cache.json  |  | KB JSONs |  | config.py     |
  | 8 entradas       |  | 3 tram.  |  | 5 flags       |
  +------------------+  +----------+  +---------------+
  | models.py: 8 dataclasses                          |
  | prompts/: system_prompt + templates (es/fr)       |
  | logger.py, timing.py                              |
  +---------------------------------------------------+
```

---

### Diagrama 2: Fase 2 (Hardening) -- Lo que se anadio

```
+================================================================+
|           DIAGRAMA 2: FASE 2 — HARDENING & DEPLOY              |
|           93 tests (+61) | 6 gates P2.1-P2.6                  |
+================================================================+

  CAMBIOS SOBRE FASE 1 (marcados con [+NEW] y [~MOD]):

  +------------------------------------------+
  |  FLASK /webhook                          |
  |  +------------------------------------+  |
  |  | [~MOD] RequestValidator (firma)    |  |
  |  | [~MOD] NumMedia safe parsing       |  |
  |  | [~MOD] Silent thread death protect |  |
  |  +------------------------------------+  |
  +------------------------------------------+

  PIPELINE:
  +------------------------------------------+
  | [~MOD] transcribe.py:                    |
  |   Whisper base --> Gemini transcripcion  |
  |   (ahorra ~290 MB RAM)                  |
  |                                          |
  | [+NEW] guardrails.py:                    |
  |   pre_check (blocklist, PII)            |
  |   post_check (disclaimer, PII redact)   |
  |                                          |
  | [+NEW] models_structured.py:             |
  |   ClaraStructuredResponse               |
  |   parse_structured_response()           |
  |                                          |
  | [+NEW] tts.py:                           |
  |   gTTS on-demand con hash caching       |
  |                                          |
  | [+NEW] observability.py:                 |
  |   RequestContext, request_id, timings    |
  +------------------------------------------+

  [+NEW] CONFIG FLAGS (5 -> 9):
  +------------------------------------------+
  | GUARDRAILS_ON = true                     |
  | STRUCTURED_OUTPUT_ON = false             |
  | OBSERVABILITY_ON = true                  |
  | RAG_ENABLED = false                      |
  | AUDIO_BASE_URL (para TTS)               |
  +------------------------------------------+

  [+NEW] DEPLOY:
  +------------------------------------------+
  | Dockerfile (Python 3.11 + gunicorn)      |
  | render.yaml (16 env vars)               |
  | .dockerignore                            |
  | Puerto: 10000 (Render) / 5000 (local)  |
  +------------------------------------------+

  [+NEW] DOCS (29 archivos):
  +------------------------------------------+
  | ARCHITECTURE.md, OBSERVABILITY.md        |
  | RENDER-DEPLOY.md, TWILIO-SETUP-GUIDE.md |
  | RUNBOOK-PHASE2.md, TEST-PLAN.md         |
  | NOTION-OS.md + 81 entradas en 3 DBs     |
  +------------------------------------------+

  [+NEW] SEGURIDAD:
  +------------------------------------------+
  | Escaneo de secretos (11 patrones, 0 hit)|
  | .env en .gitignore (4 patrones)         |
  | render.yaml sync:false para secretos    |
  +------------------------------------------+
```

---

### Diagrama 3: Fase 3 (Demo) -- Lo que se anadio

```
+================================================================+
|              DIAGRAMA 3: FASE 3 — DEMO EN VIVO                 |
|              96 tests (+3) | 7 gates P3.1-P3.Q7               |
+================================================================+

  CAMBIOS SOBRE FASE 2:

  [+NEW] TWILIO REAL:
  +------------------------------------------+
  | Sandbox configurado                      |
  | Signature validation activa (403)        |
  | Checklist paso a paso                    |
  | Test real via WhatsApp completado        |
  +------------------------------------------+

  [+NEW] OPS:
  +------------------------------------------+
  | cron-job.org cada 14 min --> /health     |
  | Runbook 8 escenarios de incidente        |
  | /health devuelve 8 componentes           |
  | Avg latencia: 166ms                      |
  +------------------------------------------+

  [+NEW] QA DEEP AUDIT:
  +------------------------------------------+
  | phase3_verify.sh (7 pasos)               |
  | 12 contradicciones detectadas            |
  | 11 corregidas                            |
  | Conteos alineados: 96 tests, 11 skills  |
  +------------------------------------------+

  [+NEW] LOGGING JSON:
  +------------------------------------------+
  | JSONFormatter                            |
  | request_id en cada linea                 |
  | Timings por stage en JSON                |
  | Demo-grade logging                       |
  +------------------------------------------+

  [+NEW] DEMO ASSETS:
  +------------------------------------------+
  | 6 MP3s pregrabados (es x 3, fr x 2, 1)  |
  | demo_cache.json (8 entradas)             |
  | Guion 6-8 min                            |
  | WOW 1 (texto) + WOW 2 (audio)           |
  | 1-pager ejecutivo                        |
  +------------------------------------------+

  ESTADO FINAL FASE 3:
  +------------------------------------------+
  | 96/96 tests PASS                         |
  | 9 feature flags + 1 hardcoded            |
  | 11 skills en pipeline                    |
  | 81 entradas Notion                       |
  | Deploy Render verificado                 |
  | Todos los gates PASS                     |
  +------------------------------------------+
```

---

### Diagrama 4: Fase 4 (Humana) -- Arquitectura C Completa

```
+================================================================+
|          DIAGRAMA 4: FASE 4 "HUMANA" — ARQUITECTURA C          |
|          Monolito Pre-gen + Grafo Estatico                     |
+================================================================+

  === FASE DE BUILD (CI/CD o local) ===

  flow_definitions/
  +-------------------+     +-------------------+
  | imv_flow.yaml     |     | build_flows.py    |
  | empad_flow.yaml   |---->| (script offline)  |
  | ts_flow.yaml      |     |                   |
  +-------------------+     +--------+----------+
                                     |
                    +----------------+----------------+
                    v                                 v
            [Gemini 1.5 Flash]                [gTTS / edge-tts]
            Genera texto                       Genera OGG audio
            para cada paso                     para cada respuesta
                    |                                 |
                    v                                 v
            data/flows/                        data/flows/audio/
            +------------------+               +------------------+
            | imv_flow.json    |               | imv_s1_es.ogg    |
            | empad_flow.json  |               | imv_s2_es.ogg    |
            | ts_flow.json     |               | imv_s1_fr.ogg    |
            |                  |               | empad_s1_es.ogg  |
            | Cada JSON tiene: |               | ...              |
            |  steps[]         |               | (~20-40 archivos)|
            |  transitions{}   |               +------------------+
            |  responses{}     |
            |  audio_refs{}    |
            +------------------+

  === RUNTIME (Render 512 MB) ===

  Usuario WhatsApp (es/fr/ar)
       |
       | texto / audio
       v
  [Twilio Cloud]
       |
       v POST /webhook
  +--------------------------------------------------------------+
  |  FLASK APP                                  ~134 MB RAM      |
  |                                                              |
  |  +-------------------+     +----------------------------+    |
  |  | webhook.py        |     | ThreadPoolExecutor(4)      |    |
  |  | Validar firma     |     | Limite: 4 hilos max        |    |
  |  | Parsear request   |     |                            |    |
  |  | TwiML ACK <1s     |---->| pipeline_v2.process(msg)   |    |
  |  +-------------------+     +----------------------------+    |
  |                                    |                         |
  |                                    v                         |
  |  +----------------------------------------------------------+|
  |  |               PIPELINE v2 (~15 skills)                   ||
  |  |                                                          ||
  |  |  +================+                                      ||
  |  |  | GUARDRAIL PRE  |  blocklist, PII, self-harm          ||
  |  |  +================+                                      ||
  |  |         | safe                                           ||
  |  |         v                                                ||
  |  |  +================+                                      ||
  |  |  | DETECT INPUT   |  TEXT / AUDIO                        ||
  |  |  +================+                                      ||
  |  |         |                                                ||
  |  |     +---+--------+                                       ||
  |  |     v            v                                       ||
  |  |   TEXT         AUDIO                                     ||
  |  |     |         [fetch_media]                              ||
  |  |     |         [transcribe via Gemini]                    ||
  |  |     |            |                                       ||
  |  |     +-----+------+                                       ||
  |  |           v                                              ||
  |  |  +================+                                      ||
  |  |  | DETECT LANG    |  es / fr / ar                        ||
  |  |  +================+                                      ||
  |  |           |                                              ||
  |  |           v                                              ||
  |  |  +================+                                      ||
  |  |  | SESSION LOAD   |  Cargar estado del usuario           ||
  |  |  +================+  (por phone_hash)                    ||
  |  |           |                                              ||
  |  |           v                                              ||
  |  |  +================+                                      ||
  |  |  | FLOW ROUTER    |  Decidir: EN FLUJO / FUERA          ||
  |  |  +================+                                      ||
  |  |        |                |                                ||
  |  |        v                v                                ||
  |  |   EN FLUJO         FUERA DE FLUJO                        ||
  |  |        |                |                                ||
  |  |        v                v                                ||
  |  |  +-----------+   +---------------------------+           ||
  |  |  | FLOW STEP |   | INTENT CLASSIFY           |           ||
  |  |  | Navegar   |   | regex -> kw -> Gemini     |           ||
  |  |  | grafo     |   +---------------------------+           ||
  |  |  | estatico  |          |                                ||
  |  |  | Obtener   |          v                                ||
  |  |  | respuesta |   +---------------------------+           ||
  |  |  | pregener. |   | CACHE MATCH               |           ||
  |  |  | + audio   |   | --> KB LOOKUP             |           ||
  |  |  | OGG/MP3   |   | --> LLM GENERATE          |           ||
  |  |  +-----------+   | --> VERIFY                |           ||
  |  |        |         | --> GUARDRAIL POST        |           ||
  |  |        |         | --> TTS ON-DEMAND         |           ||
  |  |        |         +---------------------------+           ||
  |  |        |                |                                ||
  |  |        +--------+-------+                                ||
  |  |                 v                                        ||
  |  |  +================+                                      ||
  |  |  | SESSION SAVE   |  Actualizar estado                   ||
  |  |  +================+                                      ||
  |  |                 |                                        ||
  |  |                 v                                        ||
  |  |  +================+                                      ||
  |  |  | SEND RESPONSE  |  Twilio REST + media_url             ||
  |  |  +================+                                      ||
  |  +----------------------------------------------------------+|
  |                                                              |
  |  +--------------+  +----------+  +-----------+  +--------+  |
  |  | flows/*.json |  | KB .json |  | ConvStore |  | cache  |  |
  |  | + audio/     |  | 3 tram.  |  | dict+TTL  |  | .json  |  |
  |  +--------------+  +----------+  +-----------+  +--------+  |
  +--------------------------------------------------------------+
       |
       v Twilio REST API
  [Twilio Cloud]
       |
       v
  Usuario WhatsApp
  (texto + audio OGG nativo en burbuja)
```

---

### Diagrama 5: Fase 4 Pipeline Detallado -- Cada Skill con Inputs/Outputs

```
+================================================================+
|     DIAGRAMA 5: PIPELINE v2 DETALLADO — INPUTS / OUTPUTS      |
+================================================================+

  IncomingMessage
  {from_number, body, media_url, media_type, input_type, timestamp, request_id}
       |
       v
  +=================================================================+
  | SKILL 1: guardrail_pre                                         |
  | IN:  text (str)                                                |
  | OUT: GuardrailResult {safe: bool, reason: str, modified: str}  |
  | FLAG: GUARDRAILS_ON                                            |
  | FALLO: safe=True (pass-through)                                |
  +=================================================================+
       | safe=True
       v
  +=================================================================+
  | SKILL 2: detect_input                                          |
  | IN:  num_media (int), media_type (str)                         |
  | OUT: InputType (TEXT | AUDIO | IMAGE)                          |
  | FLAG: ninguno                                                  |
  | FALLO: InputType.TEXT (default)                                |
  +=================================================================+
       |
       +--- TEXT ---+----------- AUDIO --------+
       |            |                           |
       |            v                           |
       |  +===========================================+
       |  | SKILL 3: fetch_media                      |
       |  | IN:  media_url (str)                      |
       |  | OUT: bytes (audio raw)                    |
       |  | TIMEOUT: 10s                              |
       |  | FALLO: None --> fallback "whisper_fail"   |
       |  +===========================================+
       |            |
       |            v
       |  +===========================================+
       |  | SKILL 4: transcribe                       |
       |  | IN:  audio_bytes (bytes), mime_type (str) |
       |  | OUT: TranscriptResult {text, language,     |
       |  |      duration_ms, success, error}         |
       |  | FLAG: WHISPER_ON                           |
       |  | TIMEOUT: WHISPER_TIMEOUT (12s)            |
       |  | FALLO: fallback "whisper_fail"            |
       |  +===========================================+
       |            |
       +-----+------+
             v
  +=================================================================+
  | SKILL 5: detect_lang                                           |
  | IN:  text (str)                                                |
  | OUT: language (str: "es" | "fr" | "ar")                        |
  | LOGICA: keyword_hint -> langdetect -> fallback "es"            |
  | FLAG: ninguno                                                  |
  | FALLO: "es"                                                    |
  | [+F4] Anadir keywords arabes si ARABIC_ON=true                |
  +=================================================================+
             |
             v
  +=================================================================+
  | SKILL 6: session_load                [+NEW F4]                 |
  | IN:  phone_hash (str: hash de from_number)                     |
  | OUT: ConversationState {                                       |
  |        phone_hash, tramite, step, language,                    |
  |        history[], guided_active, updated_at                    |
  |      }                                                         |
  | FLAG: GUIDED_FLOWS_ON                                          |
  | STORAGE: dict con TTL 30 min                                   |
  | FALLO: ConversationState nueva (step=0, guided=False)          |
  +=================================================================+
             |
             v
  +=================================================================+
  | SKILL 7: flow_router                 [+NEW F4]                 |
  | IN:  text (str), state (ConversationState), language (str)     |
  | OUT: FlowDecision {                                            |
  |        in_flow: bool,                                          |
  |        flow_name: str | None,                                  |
  |        step_num: int,                                          |
  |        user_intent: str ("start_imv"|"next"|"docs"|"free")    |
  |      }                                                         |
  | LOGICA:                                                        |
  |   1. Si state.guided_active --> "EN FLUJO"                     |
  |   2. Si regex match "quiero solicitar IMV" --> iniciar flujo   |
  |   3. Si keyword match tramite --> ofrecer flujo                |
  |   4. Else --> "FUERA DE FLUJO"                                 |
  | FLAG: GUIDED_FLOWS_ON                                          |
  | FALLO: FUERA DE FLUJO (usa pipeline clasico)                   |
  +=================================================================+
             |
      +------+------+
      v             v
  EN FLUJO     FUERA DE FLUJO
      |             |
      v             |
  +=============+   |
  | SKILL 8a:   |   |
  | flow_step   |   |
  | [+NEW F4]   |   |
  |             |   |
  | IN:  flow   |   |
  |  .json,     |   |
  |  step_num,  |   |
  |  user_input |   |
  | OUT:        |   |
  |  FlowStep { |   |
  |   text,     |   |
  |   audio_url,|   |
  |   next_step,|   |
  |   options[],|   |
  |   complete  |   |
  |  }          |   |
  | FALLO:      |   |
  |  llm_gen    |   |
  +=============+   |
      |             |
      |             v
      |    +===========================================+
      |    | SKILL 8b: cache_match (existente)         |
      |    | IN:  text, idioma, input_type             |
      |    | OUT: CacheResult {hit, entry, score}      |
      |    +===========================================+
      |         |
      |     +---+---+
      |     v       v
      |    HIT    MISS
      |     |       |
      |     |       v
      |     |  +===========================================+
      |     |  | SKILL 9: intent_classify  [+NEW F4]      |
      |     |  | IN:  text (str), language (str)           |
      |     |  | OUT: Intent {                             |
      |     |  |   name: str,                              |
      |     |  |   confidence: float,                      |
      |     |  |   tramite: str | None,                    |
      |     |  |   method: "regex"|"keyword"|"gemini"      |
      |     |  | }                                         |
      |     |  | CASCADA:                                  |
      |     |  |   1. regex patterns --> confidence 1.0    |
      |     |  |   2. keyword score --> confidence 0.7-0.9 |
      |     |  |   3. Gemini mini-call --> confidence var   |
      |     |  | FLAG: INTENT_CLASSIFIER_ON                |
      |     |  | FALLO: Intent(name="unknown",conf=0)      |
      |     |  +===========================================+
      |     |       |
      |     |       v
      |     |  +===========================================+
      |     |  | SKILL 10: kb_lookup (existente mejorado)  |
      |     |  | IN:  text, intent, language               |
      |     |  | OUT: KBContext {tramite, datos, url, ok}   |
      |     |  +===========================================+
      |     |       |
      |     |       v
      |     |  +===========================================+
      |     |  | SKILL 11: llm_generate (existente)        |
      |     |  | IN:  text, KBContext, language,            |
      |     |  |      conversation_history (1-3 turnos)    |
      |     |  | OUT: LLMResponse {text, lang, ms, ok}     |
      |     |  | FLAG: LLM_LIVE                            |
      |     |  | TIMEOUT: LLM_TIMEOUT (6s)                |
      |     |  +===========================================+
      |     |       |
      |     +---+---+
      |         v
      |    +===========================================+
      |    | SKILL 12: verify_response (existente)     |
      |    | IN:  response_text, KBContext              |
      |    | OUT: verified_text (str)                   |
      |    +===========================================+
      |         |
      |         v
      |    +===========================================+
      |    | SKILL 13: guardrail_post (existente)      |
      |    | IN:  response_text (str)                  |
      |    | OUT: safe_text (str) con disclaimers      |
      |    | FLAG: GUARDRAILS_ON                        |
      |    +===========================================+
      |         |
      |         v
      |    +===========================================+
      |    | SKILL 14: tts_generate                    |
      |    | IN:  text (str), language (str)            |
      |    | OUT: audio_url (str | None)               |
      |    | LOGICA:                                   |
      |    |   1. Buscar audio pregenerado por hash    |
      |    |   2. Si no existe: gTTS on-demand         |
      |    |   3. Formato: OGG (pref) o MP3            |
      |    | FLAG: TTS_ENGINE (gtts|edge-tts|none)     |
      |    | FALLO: None (solo texto)                  |
      |    +===========================================+
      |         |
      +----+----+
           v
  +=================================================================+
  | SKILL 15: session_save               [+NEW F4]                 |
  | IN:  state (ConversationState), user_text, response_text       |
  | OUT: void                                                      |
  | LOGICA:                                                        |
  |   1. Actualizar step, updated_at                               |
  |   2. Append a history (max 5 turnos)                           |
  |   3. Si TTL expirado: limpiar sesion                           |
  | FLAG: GUIDED_FLOWS_ON                                          |
  | FALLO: silencioso (no bloquea respuesta)                       |
  +=================================================================+
           |
           v
  +=================================================================+
  | SKILL 16: send_response (existente mejorado)                   |
  | IN:  FinalResponse {to_number, body, media_url, source, ms}   |
  | OUT: bool (enviado con exito)                                  |
  | LOGICA:                                                        |
  |   1. Twilio REST create message                                |
  |   2. Si falla con media: retry sin media                       |
  |   3. Log REST con source y timing                              |
  | TIMEOUT: 10s (hardcoded)                                       |
  | FALLO: log_error, return False                                 |
  +=================================================================+
           |
           v
  [Twilio REST API --> WhatsApp --> Usuario]
```

---

## 5. Sistema de Gestion de Estado

### 5.1 Schema de ConversationState

```python
@dataclass
class ConversationState:
    """Estado de la conversacion de un usuario."""
    phone_hash: str           # SHA-256 del numero (GDPR: no almacenar numeros)
    tramite: str | None       # "imv" | "empadronamiento" | "tarjeta_sanitaria" | None
    step: int                 # Paso actual en el flujo guiado (0 = no en flujo)
    language: str             # Idioma detectado: "es" | "fr" | "ar"
    guided_active: bool       # True si el usuario esta en un flujo guiado
    history: list[dict]       # Ultimos N turnos [{role: "user"|"assistant", text: str}]
    intent_stack: list[str]   # Stack de intenciones (para nested questions)
    created_at: float         # Timestamp de creacion
    updated_at: float         # Timestamp de ultima actualizacion
    metadata: dict            # Datos extra (docs entregados, etc.)
```

### 5.2 Almacenamiento

**Para hackathon: dict en memoria con TTL.**

```python
import time
import hashlib
from threading import Lock

class ConversationStore:
    """Almacen thread-safe de estados conversacionales con TTL."""

    def __init__(self, ttl_seconds: int = 1800):  # 30 min TTL
        self._store: dict[str, ConversationState] = {}
        self._lock = Lock()
        self._ttl = ttl_seconds

    def _hash_phone(self, phone: str) -> str:
        return hashlib.sha256(phone.encode()).hexdigest()[:16]

    def get(self, phone: str) -> ConversationState | None:
        key = self._hash_phone(phone)
        with self._lock:
            state = self._store.get(key)
            if state and (time.time() - state.updated_at) > self._ttl:
                del self._store[key]
                return None
            return state

    def save(self, phone: str, state: ConversationState) -> None:
        key = self._hash_phone(phone)
        state.updated_at = time.time()
        with self._lock:
            self._store[key] = state

    def cleanup(self) -> int:
        """Eliminar sesiones expiradas. Retorna cantidad eliminada."""
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._store.items()
                       if (now - v.updated_at) > self._ttl]
            for k in expired:
                del self._store[k]
            return len(expired)

    def count(self) -> int:
        with self._lock:
            return len(self._store)
```

**Para persistencia ligera (opcional, post-hackathon): SQLite.**

```sql
-- state.db (en /tmp/ para Render free tier)
CREATE TABLE IF NOT EXISTS sessions (
    phone_hash TEXT PRIMARY KEY,
    state_json TEXT NOT NULL,
    tramite TEXT,
    step INTEGER DEFAULT 0,
    language TEXT DEFAULT 'es',
    updated_at REAL NOT NULL,
    created_at REAL NOT NULL
);

CREATE INDEX idx_sessions_updated ON sessions(updated_at);

CREATE TABLE IF NOT EXISTS conversation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_hash TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user' | 'assistant'
    content TEXT NOT NULL,
    timestamp REAL NOT NULL,
    FOREIGN KEY (phone_hash) REFERENCES sessions(phone_hash)
);
```

### 5.3 Ciclo de Vida de Sesion

```
CREAR                ACTUALIZAR              EXPIRAR
  |                      |                      |
  v                      v                      v
+----------+     +---------------+     +----------------+
| Primer   |     | Cada mensaje  |     | TTL > 30 min   |
| mensaje  |     | del usuario:  |     | sin actividad: |
| del user |     |               |     |                |
| Estado:  |     | - update step |     | - Eliminar de  |
|  step=0  |     | - append hist |     |   store        |
|  guided= |     | - update lang |     | - Proxima msg  |
|   False  |     | - update ts   |     |   = sesion     |
|  hist=[] |     |               |     |   nueva        |
+----------+     +---------------+     +----------------+
     |                   |                     ^
     v                   v                     |
  [Si detecta     [Si step==last        [cleanup() corre
   tramite:        de flujo:             cada 5 min via
   guided=True,    guided=False,         timer thread]
   step=1]         step=0]
```

### 5.4 Flujos Guiados como Maquina de Estados

Cada tramite se define como un grafo de estados en un archivo JSON pregenerado:

```json
{
  "tramite": "imv",
  "version": "2026-02",
  "total_steps": 5,
  "steps": {
    "1": {
      "id": "intro",
      "text_es": "El Ingreso Minimo Vital (IMV) es una prestacion de la Seguridad Social...",
      "text_fr": "Le Revenu Minimum Vital (IMV) est une prestation de la Securite Sociale...",
      "audio_es": "flows/audio/imv_s1_es.ogg",
      "audio_fr": "flows/audio/imv_s1_fr.ogg",
      "options": ["requisitos", "solicitar", "documentos"],
      "transitions": {
        "requisitos": 2,
        "solicitar": 3,
        "documentos": 4,
        "default": 2
      }
    },
    "2": {
      "id": "requisitos",
      "text_es": "Para solicitar el IMV necesitas cumplir estos requisitos...",
      "text_fr": "Pour demander le IMV, vous devez remplir ces conditions...",
      "audio_es": "flows/audio/imv_s2_es.ogg",
      "audio_fr": "flows/audio/imv_s2_fr.ogg",
      "options": ["solicitar", "documentos", "volver"],
      "transitions": {
        "solicitar": 3,
        "documentos": 4,
        "volver": 1,
        "default": 3
      }
    }
  }
}
```

**Navegacion del grafo:**
1. El usuario envia "quiero solicitar el IMV".
2. `flow_router` detecta intent "start_imv", crea sesion con step=1.
3. `flow_step` busca step 1 en `imv_flow.json`, devuelve texto + audio + opciones.
4. El usuario responde "documentos".
5. `flow_router` ve `guided_active=True`, pasa a `flow_step`.
6. `flow_step` busca la transicion "documentos" desde step 1 --> step 4.
7. Devuelve texto + audio del paso 4.

**Palabras clave de control de flujo:**
- "volver" / "retour" --> paso anterior
- "salir" / "quitter" --> salir del flujo (guided_active=False)
- "menu" / "inicio" --> step 1 del flujo actual
- Cualquier otra cosa --> `transitions.default` o `llm_generate` si no hay default

---

## 6. Feature Flags para Fase 4

### 6.1 Nuevos Flags

| # | Flag | Tipo | Default | Descripcion |
|---|------|------|---------|-------------|
| 10 | `GUIDED_FLOWS_ON` | bool | `false` | Activa flujos guiados con estado |
| 11 | `INTENT_CLASSIFIER_ON` | bool | `false` | Activa clasificacion de intenciones (regex+kw+Gemini) |
| 12 | `TTS_ENGINE` | str | `"gtts"` | Motor TTS: "gtts", "edge-tts", "none" |
| 13 | `ARABIC_ON` | bool | `false` | Activa soporte para arabe (detect_lang + templates) |
| 14 | `SESSION_TTL` | int | `1800` | TTL de sesiones en segundos (30 min default) |
| 15 | `MAX_HISTORY_TURNS` | int | `3` | Numero maximo de turnos en historial conversacional |
| 16 | `PREGENERATED_AUDIO_ON` | bool | `true` | Usar audio pregenerado para flujos guiados |
| 17 | `FLOW_DEFINITIONS_PATH` | str | `"data/flows/"` | Ruta a las definiciones de flujo JSON |
| 18 | `THREAD_POOL_SIZE` | int | `4` | Tamano del ThreadPoolExecutor |

### 6.2 Tabla Completa de Flags (Fase 3 + Fase 4)

| # | Flag | F3 | F4 | Cambio |
|---|------|----|----|--------|
| 1 | DEMO_MODE | false | false | Sin cambio |
| 2 | LLM_LIVE | true | true | Sin cambio |
| 3 | WHISPER_ON | true | true | Sin cambio |
| 4 | LLM_TIMEOUT | 6 | 6 | Sin cambio |
| 5 | WHISPER_TIMEOUT | 12 | 12 | Sin cambio |
| 6 | GUARDRAILS_ON | true | true | Sin cambio |
| 7 | STRUCTURED_OUTPUT_ON | false | false | Sin cambio |
| 8 | OBSERVABILITY_ON | true | true | Sin cambio |
| 9 | RAG_ENABLED | false | false | Sin cambio |
| 10 | GUIDED_FLOWS_ON | N/A | false | NUEVO |
| 11 | INTENT_CLASSIFIER_ON | N/A | false | NUEVO |
| 12 | TTS_ENGINE | N/A | "gtts" | NUEVO |
| 13 | ARABIC_ON | N/A | false | NUEVO |
| 14 | SESSION_TTL | N/A | 1800 | NUEVO |
| 15 | MAX_HISTORY_TURNS | N/A | 3 | NUEVO |
| 16 | PREGENERATED_AUDIO_ON | N/A | true | NUEVO |
| 17 | FLOW_DEFINITIONS_PATH | N/A | "data/flows/" | NUEVO |
| 18 | THREAD_POOL_SIZE | N/A | 4 | NUEVO |

### 6.3 Estrategia de Migracion

1. **Backward compatible:** Con TODOS los flags nuevos en sus valores default, el sistema se comporta EXACTAMENTE como Fase 3. Los flags nuevos estan desactivados por defecto.

2. **Activacion incremental:**
   - Sprint 1: `GUIDED_FLOWS_ON=true` + `SESSION_TTL=1800`
   - Sprint 2: `INTENT_CLASSIFIER_ON=true`
   - Sprint 3: `ARABIC_ON=true`
   - Sprint 4: `TTS_ENGINE=edge-tts` (mejor calidad) + `PREGENERATED_AUDIO_ON=true`

3. **No se elimina ningun flag de Fase 3.** Los flags existentes siguen funcionando como siempre.

### 6.4 Interacciones entre Flags

```
GUIDED_FLOWS_ON=false --> flow_router siempre retorna FUERA_DE_FLUJO
                          (pipeline clasico F3)

GUIDED_FLOWS_ON=true + DEMO_MODE=true  --> Flujos guiados activos,
                                           pero fuera de flujo = cache-only

GUIDED_FLOWS_ON=true + LLM_LIVE=false  --> Flujos guiados activos (pregenerado),
                                           fuera de flujo = fallback template

INTENT_CLASSIFIER_ON=true + GUIDED_FLOWS_ON=false --> Intent se usa para
                                                       mejorar kb_lookup,
                                                       pero sin flujos guiados

ARABIC_ON=true --> Anade keywords arabes a detect_lang,
                   templates arabes en templates.py,
                   flujos guiados en arabe (si existen)

PREGENERATED_AUDIO_ON=true + TTS_ENGINE=none --> Solo audio pregenerado,
                                                  sin fallback a TTS on-demand

TTS_ENGINE=none --> Sin TTS, solo texto
                    (ahorra latencia si el usuario prefiere texto)
```

### 6.5 Combinaciones Tipicas para Fase 4

| Escenario | GUIDED_ FLOWS | INTENT_ CLASSIFIER | TTS_ ENGINE | ARABIC | Descripcion |
|-----------|--------------|-------------------|-------------|--------|-------------|
| Demo F4 basica | true | false | gtts | false | Flujos guiados sin intent engine |
| Demo F4 completa | true | true | edge-tts | true | Todo activado |
| Regresion F3 | false | false | gtts | false | Identico a Fase 3 |
| Solo cache | false | false | none | false | Cache-only sin audio |
| Produccion full | true | true | gtts | true | Todo activado, TTS fiable |

---

## 7. Mitigacion de Cold Starts

### 7.1 UptimeRobot (Free Tier)

**Configuracion recomendada:**

| Parametro | Valor |
|-----------|-------|
| Tipo de monitor | HTTP(s) |
| URL | `https://civicaid-voice.onrender.com/health` |
| Intervalo | 5 minutos |
| Timeout del monitor | 30 segundos |
| Alert contacts | Email del equipo |

**Pasos:**
1. Crear cuenta en [uptimerobot.com](https://uptimerobot.com) (gratis, hasta 50 monitores).
2. Crear nuevo monitor tipo "HTTP(s)".
3. URL: `https://civicaid-voice.onrender.com/health`
4. Intervalo: 5 minutos (el minimo del free tier).
5. Activar alertas por email para downtime.

**Alternativa actual:** cron-job.org cada 14 min (ya configurado en Fase 3). UptimeRobot es mas fiable y tiene mejor dashboard.

**Nota:** Render free tier duerme tras 15 min de inactividad. Con pings cada 5 min, el servicio permanece despierto indefinidamente dentro del limite de 750 horas/mes.

Referencia: [UptimeRobot - Keep Alive](https://uptimerobot.com/keep-alive/) | [Sergei Liski - Run Full-Time on Render Free](https://sergeiliski.medium.com/how-to-run-a-full-time-app-on-renders-free-tier-without-it-sleeping-bec26776d0b9)

### 7.2 Graceful Cold Start Handler

Cuando Render despierta el contenedor tras un cold start, hay un periodo de 30-50 segundos donde el servicio no esta listo. Se propone:

```python
# En src/app.py

import time

_BOOT_TIME = time.time()
_READY = False

def create_app():
    app = Flask(__name__)

    # ... registrar blueprints ...

    # Cargar datos al arrancar
    from src.core.cache import load_cache
    entries = load_cache()

    # Cargar flows si GUIDED_FLOWS_ON
    if config.GUIDED_FLOWS_ON:
        from src.core.flows import load_flows
        load_flows()

    global _READY
    _READY = True
    boot_ms = int((time.time() - _BOOT_TIME) * 1000)
    logger.info(f"[BOOT] Clara ready in {boot_ms}ms")

    return app
```

```python
# En src/routes/health.py (mejorado)

@health_bp.route("/health", methods=["GET"])
def health():
    from src.app import _READY, _BOOT_TIME

    status = "ready" if _READY else "booting"
    uptime_s = int(time.time() - _BOOT_TIME)

    return jsonify({
        "status": status,
        "uptime_seconds": uptime_s,
        "version": "0.4.0",
        # ... resto de componentes ...
    }), 200 if _READY else 503
```

### 7.3 Estrategia de Pre-carga

| Componente | Momento de carga | Impacto en boot |
|------------|-----------------|-----------------|
| demo_cache.json | Al arrancar (ya implementado) | ~10ms |
| KB JSONs (3 tramites) | Al arrancar (ya implementado) | ~5ms |
| Flow JSONs (3 flujos) | Al arrancar (nuevo) | ~10ms |
| Audio index (hash -> filepath) | Al arrancar (nuevo) | ~5ms |
| langdetect | Primera llamada (lazy) | ~50ms |
| gTTS | Primera llamada (lazy, sin modelo) | ~0ms |
| Gemini SDK | Primera llamada (lazy) | ~100ms |
| ThreadPoolExecutor | Al arrancar (nuevo) | ~1ms |
| ConversationStore | Al arrancar (nuevo) | ~0ms |

**Tiempo estimado de boot total:** < 200ms para datos estaticos. El primer request que use Gemini tendra ~100ms extra de inicializacion del SDK.

**A VALIDAR:** El cold start de Render incluye el tiempo de iniciar el contenedor Docker + Gunicorn + la app Flask. Los 30-50 segundos son de la infra de Render, no de la app. La app en si arranca en <1s.

---

## 8. Presupuesto de RAM

### 8.1 Desglose Detallado (Arquitectura C)

| Componente | RAM Base (MB) | RAM Pico (MB) | Notas |
|------------|--------------|---------------|-------|
| **Python 3.11 runtime** | 28 | 32 | Interprete + stdlib |
| **Flask framework** | 8 | 12 | Werkzeug + Jinja2 + routing |
| **Gunicorn (1 worker)** | 5 | 8 | Master + worker overhead |
| **Twilio SDK** | 8 | 12 | twilio + httplib2 + requests |
| **google-generativeai SDK** | 12 | 18 | Proto buffers + grpc (lazy) |
| **langdetect** | 4 | 6 | Profiles cargados en memoria |
| **gTTS** | 2 | 4 | Minimal; HTTP call externo |
| **dotenv + dataclasses** | 1 | 1 | Negligible |
| **Pipeline code (skills)** | 3 | 5 | Importaciones + logica |
| **ConversationStore (100 sesiones)** | 2 | 8 | ~80 bytes/sesion base; pico con historial |
| **Flow graphs (3 JSONs)** | 1 | 1 | ~50KB por flujo |
| **demo_cache.json** | 1 | 1 | 8 entradas, ~15KB |
| **KB JSONs (3 tramites)** | 1 | 1 | ~20KB por tramite |
| **Audio file I/O buffer** | 0 | 5 | Solo durante TTS generation |
| **Request handling (per-request)** | 0 | 3 | Headers, form data, response |
| **Thread pool (4 threads)** | 2 | 8 | Stack por thread ~2MB (compartido) |
| **GC overhead + fragmentation** | 15 | 25 | ~15-20% overhead tipico Python |
| **OS + container overhead** | 20 | 25 | Alpine/Debian slim |
| | | | |
| **TOTAL ESTIMADO** | **~113 MB** | **~175 MB** | |
| **Margen de seguridad (30%)** | | **~228 MB** | |
| **Limite Render** | | **512 MB** | |
| **Margen libre** | | **~284 MB** | |

### 8.2 Comparacion con Alternativas que NO Caben

| Componente alternativo | RAM adicional | Viable en 512MB |
|----------------------|---------------|-----------------|
| Whisper base (local) | +290 MB | AJUSTADO (total ~465 MB, sin margen) |
| Piper TTS (runtime) | +500 MB | NO |
| Kokoro-82M (ONNX) | +200-300 MB | AJUSTADO |
| fastText completo (pre-trained) | +500 MB | NO |
| fastText comprimido | +20 MB | SI (total ~195 MB) |
| Redis (in-process) | +50 MB | SI pero innecesario |
| SQLite (in-process) | +5 MB | SI |
| Celery worker | +100 MB | AJUSTADO |

### 8.3 Escenarios de RAM

| Escenario | RAM Estimada | Viable |
|-----------|-------------|--------|
| Arq. C base (sin audio local, sin fastText) | ~175 MB pico | SI (64% libre) |
| Arq. C + fastText comprimido (20MB) | ~195 MB pico | SI (62% libre) |
| Arq. C + SQLite | ~180 MB pico | SI (65% libre) |
| Arq. C + Whisper base local | ~465 MB pico | RIESGO (9% libre) |
| Arq. C + Piper TTS | >675 MB pico | NO (excede limite) |

### 8.4 Recomendacion de Presupuesto

```
+================================================================+
|           PRESUPUESTO DE RAM — FASE 4 (512 MB)                 |
+================================================================+

  [################.........................] 175 / 512 MB (34%)

  Asignado:
    Python + Flask + Gunicorn      :  41 MB  [########]
    SDKs (Twilio + Gemini)         :  30 MB  [######]
    Librerias (langdetect, gTTS)   :   7 MB  [#]
    Pipeline + Skills              :   8 MB  [##]
    Datos (cache, KB, flows)       :   4 MB  [#]
    Estado conversacional          :   8 MB  [##]
    Thread pool (4 hilos)          :   8 MB  [##]
    OS + container                 :  25 MB  [#####]
    GC + buffers                   :  25 MB  [#####]
    I/O temporal                   :   5 MB  [#]
    -----------------------------------------
    SUBTOTAL PICO                  : 161 MB
    Margen seguridad (+10%)        :  14 MB
    TOTAL ASIGNADO                 : 175 MB

  Reserva disponible:
    Para futuras features          : 337 MB  [libre]

  MAXIMO ABSOLUTO (OOM threshold)  : 480 MB  (dejar 32 MB para OS)
```

---

## 9. Fuentes y Referencias

### Monolito vs Microservicios
- [Atlassian - Microservices vs Monolith](https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith)
- [The New Stack - Operational Comparison](https://thenewstack.io/microservices/microservices-vs-monoliths-an-operational-comparison/)
- [GeeksforGeeks - Monolithic vs Microservices](https://www.geeksforgeeks.org/software-engineering/monolithic-vs-microservices-architecture/)

### Intent Classification
- [Label Your Data - Intent Classification 2025](https://labelyourdata.com/articles/machine-learning/intent-classification)
- [FastText - Meta AI](https://ai.meta.com/tools/fasttext/)
- [fastText - Text Classification Tutorial](https://fasttext.cc/docs/en/supervised-tutorial.html)
- [DataCamp - Intent Classification with Regex](https://campus.datacamp.com/courses/building-chatbots-in-python/understanding-natural-language?ex=2)
- [Medium - Intent Classification in <1ms](https://medium.com/@durgeshrathod.777/intent-classification-in-1ms-how-we-built-a-lightning-fast-classifier-with-embeddings-db76bfb6d964)
- [Meta Engineering - FastText on Smaller Devices](https://engineering.fb.com/2017/05/02/ml-applications/expanded-fasttext-library-now-fits-on-smaller-memory-devices/)

### Conversation State Management
- [Kevin de Bree - Chatbot Persistent Memory SQLite](https://medium.com/@kpdebree/solving-chatbot-amnesia-building-an-ai-agent-with-persistent-memory-using-python-openai-and-b9ec166c298a)
- [Redis - Real-Time Chatbots](https://redis.io/blog/redis-as-the-engine-behind-real-time-intelligent-chatbots/)
- [Redis - AI Agent Memory](https://redis.io/blog/ai-agent-memory-stateful-systems/)

### TTS Open Source
- [Inferless - 12 Best Open-Source TTS Models 2025](https://www.inferless.com/learn/comparing-different-text-to-speech---tts--models-part-2)
- [Piper TTS - GitHub](https://github.com/rhasspy/piper)
- [Kokoro-82M - HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)
- [BentoML - Best Open-Source TTS 2026](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)
- [kokoro-onnx - GitHub](https://github.com/thewh1teagle/kokoro-onnx)

### Render Free Tier
- [Render Community - Free Instance Type](https://community.render.com/t/the-free-instance-type-e-g-512mb-ram-0-1-cpu/39044)
- [FreeTiers - Render Infographic](https://www.freetiers.com/directory/render)
- [Render Community - Sleep Behavior](https://community.render.com/t/do-web-services-on-a-free-tier-go-to-sleep-after-some-time-inactive/3303)
- [Render Community - RAM Clarification](https://community.render.com/t/clarification-on-free-tier-instance-ram-allocation/26734)

### Flask Background Tasks
- [Miguel Grinberg - Flask Background Jobs](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs)
- [DevProPortal - Celery vs RQ vs Dramatiq 2025](https://devproportal.com/languages/python/python-background-tasks-celery-rq-dramatiq-comparison-2025/)
- [Flask Docs - Background Tasks with Celery](https://flask.palletsprojects.com/en/stable/patterns/celery/)
- [Judoscale - Choosing Python Task Queue](https://judoscale.com/blog/choose-python-task-queue)

### Twilio WhatsApp Media
- [Twilio - WhatsApp Media Guidance](https://www.twilio.com/docs/whatsapp/guidance-whatsapp-media-messages)
- [Twilio - Accepted MIME Types](https://www.twilio.com/docs/messaging/guides/accepted-mime-types)
- [Twilio - Assets](https://www.twilio.com/docs/serverless/functions-assets/assets)
- [Twilio - Send/Receive Media WhatsApp Python](https://www.twilio.com/docs/whatsapp/tutorial/send-and-receive-media-messages-whatsapp-python)

### Whisper Memory
- [OpenAI Whisper - Memory Requirements Discussion](https://github.com/openai/whisper/discussions/5)
- [Whisper.cpp - README](https://github.com/ggml-org/whisper.cpp/blob/master/README.md)

### Cold Start Prevention
- [UptimeRobot - Keep Alive](https://uptimerobot.com/keep-alive/)
- [Sergei Liski - Run Full-Time on Render Free Tier](https://sergeiliski.medium.com/how-to-run-a-full-time-app-on-renders-free-tier-without-it-sleeping-bec26776d0b9)
- [Saurav - Fix Render Cold Start](https://medium.com/@sauravhldr/fix-render-com-free-tier-slow-initial-load-cold-start-problem-using-free-options-and-easy-steps-c0b6c7af8276)
- [Prajwal - Keep Render Apps Alive 24/7](https://medium.com/@prajju.18gryphon/keep-your-render-free-apps-alive-24-7-41aa85d71256)

---

## Apendice A: Items Marcados "A VALIDAR"

| ID | Claim | Razon de incertidumbre | Como validar |
|----|-------|----------------------|--------------|
| V1 | Piper TTS ~500MB runtime | Solo fuente: issue #484 de GitHub | Medir con `memory_profiler` en contenedor |
| V2 | Kokoro-82M ~200-300MB RAM CPU | Estimacion basada en tamano ONNX, no medido | Cargar modelo y medir RSS |
| V3 | fastText comprimido ~20MB | Dependiente del tamano del vocabulario entrenado | Entrenar modelo y medir |
| V4 | Cold start Render 30-50s | Varia segun hora y carga de la plataforma | Medir con UptimeRobot logs |
| V5 | gTTS/edge-tts sin modelo local | gTTS usa API web de Google Translate; edge-tts usa Edge API | Verificar que no cachea modelo localmente |
| V6 | Solo OGG se reproduce nativo en WhatsApp | Segun docs Twilio 2024; podria cambiar | Probar envio de MP3 vs OGG en sandbox |
| V7 | ThreadPoolExecutor(4) ~8MB | Estimacion de stack por thread; depende de la carga | Medir con `tracemalloc` bajo carga |
| V8 | SQLite disco efimero persiste entre requests | Render no documenta esto explicitamente para free tier | Probar escritura + lectura tras 10 min |

---

## Apendice B: Glosario

| Termino | Definicion |
|---------|-----------|
| ACK | Acknowledgement — respuesta HTTP inmediata antes del procesamiento |
| Cold start | Tiempo que tarda Render en despertar un servicio dormido |
| Flow graph | Grafo dirigido de pasos de un flujo guiado (maquina de estados) |
| Intent | Intencion del usuario detectada a partir de su mensaje |
| KB | Knowledge Base — base de conocimiento en archivos JSON |
| OGG | Formato de audio que WhatsApp reproduce nativamente en burbuja |
| Pre-generacion | Generar respuestas y audio en build time (offline) en vez de runtime |
| Session | Estado conversacional de un usuario, identificado por hash de telefono |
| Skill | Funcion atomica del pipeline que transforma datos de entrada en salida |
| TTL | Time To Live — duracion maxima de una sesion antes de expirar |
| TwiML | Twilio Markup Language — XML para respuestas a Twilio |

---

> **Siguiente paso:** Presentar este documento al equipo para validacion. Tras aprobacion, crear tickets en Notion para cada componente nuevo de Fase 4 y asignar a los teammates correspondientes.
