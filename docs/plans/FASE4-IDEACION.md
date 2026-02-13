# Fase 4 "Humana" — Documento de Ideacion Consolidado

> **Para Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Disenar la Fase 4 de CivicAid Voice / Clara con flujos guiados conversacionales, soporte para arabe, pre-generacion de respuestas y audio, y una experiencia que funcione 100% con herramientas open source y gratuitas dentro de 512MB RAM.

**Architecture:** Monolito Pre-generacion + Grafo Estatico. Todas las respuestas de flujos guiados se generan offline (texto + audio OGG). En runtime el pipeline navega un grafo estatico para flujos guiados y usa LLM solo para preguntas fuera de flujo. Estado conversacional en memoria con TTL.

**Tech Stack:** Python 3.11, Flask, Twilio WhatsApp, gTTS/edge-tts, Gemini 1.5 Flash, Docker, Render Free Tier (512MB)

**Fecha:** 2026-02-13
**Autores:** Equipo de 8 agentes especializados + Sintetizador
**Estado:** PROPUESTA CONSOLIDADA — pendiente de aprobacion

**Restriccion critica:** TODO debe ser OPEN SOURCE + GRATUITO + LOCAL. Cero APIs de pago. Render free tier (512MB RAM, 0.1 vCPU).

---

## Indice

- [A) Resumen Ejecutivo](#a-resumen-ejecutivo)
- [B) 3 Arquitecturas Candidatas](#b-3-arquitecturas-candidatas)
- [C) Decision Final](#c-decision-final)
- [D) Backlog Fase 4](#d-backlog-fase-4)
- [E) Plan de Tests](#e-plan-de-tests)
- [F) Plan Notion OS](#f-plan-notion-os)
- [G) Diagramas por Fase](#g-diagramas-por-fase)
- [H) Narrativa para Jueces + Elevator Pitch](#h-narrativa-para-jueces--elevator-pitch)
- [Anexo: Fuentes y Referencias](#anexo-fuentes-y-referencias)
- [Anexo: Items A VALIDAR](#anexo-items-a-validar)

---

## A) Resumen Ejecutivo

### Que es Clara

Clara es una asistente de WhatsApp que ayuda a personas vulnerables en Espana — inmigrantes y mayores — a entender y completar tramites de servicios sociales. Le hablas o le escribes en tu idioma y Clara responde con informacion verificada del gobierno, paso a paso, con texto y audio.

### Estado actual (fin de Fase 3)

| Metrica | Valor |
|---------|-------|
| Tests automatizados | 96 (91 passed + 5 xpassed) |
| Skills en pipeline | 11 |
| Feature flags | 9 |
| Tramites cubiertos | 3 (IMV, Empadronamiento, Tarjeta Sanitaria) |
| Idiomas | 2 (espanol, frances) |
| Entradas Notion | 81 (43 Backlog + 12 KB + 26 Testing) |
| Cache pre-calculado | 8 entradas texto + 6 MP3 |
| Deploy | Render verificado, /health operativo |
| Gates | 22/22 PASS |

### Que anade Fase 4

| Feature nueva | Descripcion en lenguaje humano |
|---------------|-------------------------------|
| Flujos guiados | Clara lleva al usuario paso a paso por un tramite, como un formulario hablado |
| Estado conversacional | Clara recuerda en que paso estabas si mandas otro mensaje |
| Pre-generacion de respuestas | Las respuestas de los flujos se preparan offline, asi son instantaneas |
| Audio OGG nativo | Los audios se reproducen directamente en la burbuja de WhatsApp (no como archivo descargable) |
| Soporte arabe (stub) | Deteccion de arabe + templates basicos, listo para ampliar |
| Intent classification | Clara entiende mejor que quiere el usuario (regex + keywords + LLM fallback) |
| ThreadPoolExecutor | Control del numero maximo de hilos para evitar saturacion |
| Nuevo WOW 3: foto de carta | El usuario manda foto de una carta del gobierno y Clara la explica |

### Restriccion de RAM — Resolucion de conflicto

**Conflicto detectado:** El Agent 1 (Voice) recomendo Piper TTS con estimacion de ~100MB RAM. El Agent 5 (Architecture) demostro que Piper TTS requiere ~500MB en runtime (fuente: GitHub issue #484), lo cual NO cabe en 512MB.

**Resolucion:** Se descarta Piper TTS para runtime. La estrategia de TTS es:
1. **Pre-generacion offline** (en CI/CD o maquina local): gTTS o edge-tts generan OGGs para todas las respuestas de flujos guiados
2. **On-demand en runtime**: gTTS o edge-tts (ambas son APIs web gratuitas, 0MB de modelo local)
3. **Futuro (si se sube a 1GB)**: Piper TTS con modelos `low`

### Presupuesto de RAM

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

## B) 3 Arquitecturas Candidatas

---

### Arquitectura A: "Monolito Conversacional Extendido"

**Idea:** Evolucion directa del monolito actual. Se anaden estado conversacional (dict en memoria), clasificacion de intenciones y flujos guiados como skills adicionales dentro del pipeline. Sin dependencias nuevas.

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
  |  PIPELINE v2 (15 skills):                                  |
  |  guardrail_pre -> detect_input -> [AUDIO: fetch+transcr.]  |
  |  -> session_load -> detect_lang -> intent_classify          |
  |  -> flow_router:                                           |
  |      EN FLUJO -> flow_step -> state_update -> SEND         |
  |      FUERA -> cache -> kb_lookup -> llm -> verify          |
  |               -> guardrail_post -> tts -> session_save     |
  |               -> send_response                             |
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

| Metrica | Valor |
|---------|-------|
| RAM estimada | ~132 MB |
| Latencia flujo guiado | 100-200 ms |
| Fiabilidad demo | Media |
| Complejidad | Baja |
| Persistencia estado | No (se pierde al reiniciar) |

| Pros | Contras |
|------|---------|
| Minimo cambio respecto a F3 | Estado en memoria se pierde al reiniciar |
| Cero dependencias nuevas | Sin audio pregenerado (TTS on-demand para todo) |
| Bajo consumo de RAM | Latencia alta en flujos (depende de gTTS cada vez) |
| Facil de testear | Flujos guiados sin audio nativo OGG |

---

### Arquitectura B: "Monolito + SQLite + Intent Engine"

**Idea:** Monolito con SQLite para persistencia de estado y un motor de intenciones regex + keywords + fastText comprimido (~20MB). La persistencia permite retomar conversaciones tras cold starts.

```
+======================================================================+
|              ARQUITECTURA B: MONOLITO + SQLite + INTENT              |
+======================================================================+

  Usuario WhatsApp
       |
       v POST /webhook
  +------------------------------------------------------------+
  |  FLASK APP (monolito)                    512 MB RAM total  |
  |                                                            |
  |  PIPELINE v2 (15 skills) + INTENT ENGINE:                  |
  |  guardrail_pre -> detect_input -> [AUDIO]                  |
  |  -> session_load(SQLite) -> detect_lang                    |
  |  -> intent_classify(regex -> kw -> fastText)               |
  |  -> flow_router -> EN/FUERA FLUJO                          |
  |                                                            |
  |  +-------------------------------------------------------+ |
  |  |                   SQLite (state.db)                    | |
  |  |  sessions: phone_hash, state_json, tramite, step...   | |
  |  |  conversation_log: id, phone_hash, role, content...   | |
  |  +-------------------------------------------------------+ |
  |                                                            |
  |  +----------------+  +----------+  +-----------+           |
  |  | demo_cache.json|  | KB .json |  | fastText  |           |
  |  | (8+ entradas)  |  | (3 tram) |  | (~20 MB)  |           |
  |  +----------------+  +----------+  +-----------+           |
  +------------------------------------------------------------+
```

| Metrica | Valor |
|---------|-------|
| RAM estimada | ~155 MB |
| Latencia flujo guiado | 2-5 ms |
| Fiabilidad demo | Media-Alta |
| Complejidad | Media-Alta |
| Persistencia estado | Parcial (disco efimero de Render) |

| Pros | Contras |
|------|---------|
| Persistencia de estado (sobrevive entre requests) | SQLite en disco efimero se pierde al reiniciar container |
| Intent engine rapido y preciso | fastText comprimido requiere entrenamiento previo (+20MB RAM) |
| Historial para contexto LLM | Mas complejidad en setup y migracion |
| Logging de conversacion para analytics | SQLite no soporta bien escrituras concurrentes |

**A VALIDAR:** El disco efimero de Render persiste entre requests pero NO entre deploys. Para hackathon es aceptable.

---

### Arquitectura C: "Pre-generacion + Grafo Estatico" (RECOMENDADA)

**Idea:** Enfoque radicalmente diferente. PRE-GENERAR todas las respuestas de los flujos guiados (texto + audio OGG) en build time, convirtiendo los flujos en un grafo estatico navegable. El LLM solo interviene para preguntas fuera de flujo.

```
+======================================================================+
|           ARQUITECTURA C: PRE-GENERACION + GRAFO ESTATICO            |
+======================================================================+

  === FASE DE BUILD (offline, en CI/CD o maquina local) ===

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
            Genera texto para                  Genera OGG audio
            cada paso de cada                  para cada respuesta
            flujo guiado (una vez)             pregenerada
                    |                                 |
                    v                                 v
            data/flows/                        data/flows/audio/
            +------------------+               +------------------+
            | imv_flow.json    |               | imv_s1_es.ogg    |
            | empad_flow.json  |               | imv_s2_es.ogg    |
            | ts_flow.json     |               | imv_s1_fr.ogg    |
            |                  |               | ...              |
            | Cada JSON tiene: |               | (~20-40 archivos)|
            |  steps[]         |               +------------------+
            |  transitions{}   |
            |  responses{}     |
            |  audio_refs{}    |
            +------------------+

  === RUNTIME (Render 512 MB) ===

  Usuario WhatsApp (es/fr/ar)
       |
       v
  [Twilio Cloud]
       |
       v POST /webhook
  +--------------------------------------------------------------+
  |  FLASK APP                                  ~134 MB RAM      |
  |                                                              |
  |  +-------------------+     +----------------------------+    |
  |  | webhook.py        |     | ThreadPoolExecutor(4)      |    |
  |  | TwiML ACK <1s     |---->| pipeline_v2.process(msg)   |    |
  |  +-------------------+     +----------------------------+    |
  |                                    |                         |
  |  PIPELINE v2 (~15 skills):                                   |
  |                                                              |
  |  [guardrail_pre] -> [detect_input] -> [AUDIO: fetch+transc] |
  |       -> [detect_lang] -> [session_load]                     |
  |       -> [flow_router]                                       |
  |            |                    |                             |
  |        EN FLUJO            FUERA DE FLUJO                    |
  |            |                    |                             |
  |       [flow_step]          [cache_match]                     |
  |       (resp. pre-          [kb_lookup]                       |
  |        generada            [llm_generate]                    |
  |        + audio OGG)        [verify]                          |
  |            |               [guardrail_post]                  |
  |            |               [tts on-demand]                   |
  |            +-------+--------+                                |
  |                    v                                         |
  |              [session_save] -> [send_response]               |
  |                                                              |
  |  +--------------+  +----------+  +-----------+  +--------+  |
  |  | flows/*.json |  | KB .json |  | ConvStore |  | cache  |  |
  |  | + audio/     |  | 3 tram.  |  | dict+TTL  |  | .json  |  |
  |  +--------------+  +----------+  +-----------+  +--------+  |
  +--------------------------------------------------------------+
       |
       v Twilio REST API
  [Twilio Cloud] --> Usuario WhatsApp
  (texto + audio OGG nativo en burbuja)
```

| Metrica | Valor |
|---------|-------|
| RAM estimada | ~134 MB (pico ~175 MB) |
| Latencia flujo guiado | 10-50 ms (pre-generado) |
| Latencia fuera de flujo + LLM | 2-6 s |
| Fiabilidad demo | MUY ALTA |
| Complejidad | Media |
| Persistencia estado | No (dict en memoria, aceptable para hackathon) |

| Pros | Contras |
|------|---------|
| Latencia ultra-baja para flujos guiados | Requiere paso de build separado |
| Audio OGG nativo en WhatsApp | Respuestas estaticas (no personalizadas) |
| Minimo consumo de RAM en runtime | Mas archivos en el repo (audios) |
| Sin dependencia de Gemini para flujos comunes | Cambiar un flujo requiere re-build |
| Funciona offline para flujos guiados | Complejidad del build script |
| Fiabilidad maxima para la demo | Menos flexibilidad que LLM on-demand |

---

## C) Decision Final

### Arquitectura seleccionada: C — "Pre-generacion + Grafo Estatico"

**Tabla comparativa:**

| Criterio | Peso | A (Extendido) | B (SQLite+Intent) | C (Pre-gen) |
|----------|------|----------------|--------------------|-------------|
| RAM en 512MB | 25% | 132 MB | 155 MB | 134 MB |
| Latencia flujos guiados | 20% | 100-200 ms | 2-5 ms | 10-50 ms |
| Fiabilidad demo | 20% | Media | Media-Alta | **MUY ALTA** |
| Complejidad implementacion | 15% | Baja | Media-Alta | Media |
| Persistencia estado | 10% | No | Parcial | No |
| Experiencia usuario (audio) | 10% | Buena | Buena | **Excelente** |

### Por que C y no las otras

1. **Fiabilidad de demo (criterio #1 en hackathon):** Las respuestas pregeneradas NUNCA fallan. No hay latencia de API, no hay riesgo de timeout, no hay respuestas incoherentes del LLM. Es exactamente el patron que hizo funcionar la demo de Fase 3 (cache-first), pero extendido a flujos completos.

2. **Latencia:** Un usuario siguiendo un flujo guiado recibe respuesta en 10-50ms con audio OGG nativo que se reproduce en la burbuja de WhatsApp. Experiencia de "app nativa".

3. **RAM:** La mas eficiente en runtime (~134 MB). El trabajo pesado (generacion de texto + audio) se hace en build time.

4. **Escalabilidad de contenido:** Anadir un nuevo tramite = crear un YAML + correr build script + deploy. Sin cambios de codigo.

5. **El LLM sigue disponible** para preguntas fuera de flujo. No perdemos capacidad generativa, solo la optimizamos donde es predecible.

### Riesgos y mitigaciones

| Riesgo | Mitigacion |
|--------|------------|
| Respuestas pregeneradas suenan "roboticas" | Prompt cuidadoso en build time; tono Clara |
| Build script complejo | Script documentado, idempotente |
| Tamano del repo crece con audios | .gitignore los OGG; solo commitear JSONs |
| Estado en memoria se pierde | Aceptable para hackathon; flujos cortos (3-5 pasos) |
| Disco efimero pierde TTS dinamico | Se regenera on-demand; flujos guiados son estaticos |

### Herramientas explicadas (cada una en lenguaje humano)

| Herramienta | Que es | Que hace en Clara | Licencia | Coste |
|-------------|--------|-------------------|----------|-------|
| **Python 3.11** | Lenguaje de programacion. Es como el "idioma" en el que esta escrito todo el codigo de Clara. | Todo el sistema esta escrito en Python | PSF (libre) | Gratis |
| **Flask** | Un framework web. Es como una centralita telefonica: recibe llamadas (mensajes) y las dirige al sitio correcto. | Recibe los mensajes de Twilio y devuelve respuestas | BSD (libre) | Gratis |
| **Twilio** | Un servicio que conecta aplicaciones con WhatsApp. Es el "cartero" que lleva y trae mensajes. | Envia y recibe mensajes de WhatsApp | N/A | Free tier |
| **Gemini 1.5 Flash** | Un modelo de inteligencia artificial de Google. Es el "cerebro" que entiende preguntas complejas y genera respuestas. | Genera respuestas para preguntas fuera de flujo | Gratis (API) | Gratis |
| **gTTS** | Google Text-to-Speech. Convierte texto escrito en una voz que puedes escuchar. | Genera los audios que Clara envia por WhatsApp | MIT (libre) | Gratis |
| **edge-tts** | Motor de voz de Microsoft Edge. Igual que gTTS pero con voces de mayor calidad. | Alternativa a gTTS para generar audios | MIT (libre) | Gratis |
| **Whisper** | Un "oido digital" creado por OpenAI. Escucha audio y lo convierte en texto escrito. | Transcribe los mensajes de voz que mandan los usuarios | MIT (libre) | Gratis |
| **Docker** | Una "caja" que empaqueta todo el codigo y sus dependencias para que funcione igual en cualquier ordenador. | Empaqueta Clara para que se pueda desplegar en la nube | Apache 2.0 | Gratis |
| **Render** | Un servicio de hosting en la nube. Es el "apartamento" donde Clara vive en internet. | Ejecuta Clara 24/7 accesible desde WhatsApp | N/A | Free tier |
| **langdetect** | Una libreria que detecta en que idioma esta escrito un texto. | Detecta si el usuario escribe en espanol, frances o arabe | Apache 2.0 | Gratis |
| **Notion MCP** | Conexion con Notion para gestionar el workspace del proyecto. | Sincroniza tareas, documentacion y metricas | N/A | Free tier |

### Numeros coherentes (estado tras Fase 4)

| Metrica | Fase 3 | Fase 4 (proyectado) | Delta |
|---------|--------|---------------------|-------|
| Tests | 96 | ~265 | +169 |
| Skills | 11 | ~16 | +5 |
| Feature flags | 9 | 18 | +9 |
| Tramites | 3 | 3 (mismos, con flujos guiados) | 0 |
| Idiomas | 2 | 2 + arabe (stub) | +1 stub |
| Entradas Notion | 81 | ~155 | +74 |
| Cache texto | 8 | 8 + flujos pregenerados | +~20 |
| Archivos audio | 6 MP3 | 6 MP3 + ~30 OGG | +~30 |
| RAM pico | ~130 MB | ~175 MB | +45 MB |

---

## D) Backlog Fase 4

### D.1 Sprint 1: Fundamentos (estado + flujos basicos)

| # | Tarea | Exit Criteria | Evidencia |
|---|-------|---------------|-----------|
| F4-01 | Crear `ConversationState` dataclass en `src/core/models.py` | Dataclass con phone_hash, tramite, step, language, guided_active, history, intent_stack, created_at, updated_at, metadata | Test unitario pasa |
| F4-02 | Crear `ConversationStore` en `src/core/conversation.py` | Clase thread-safe con get/save/cleanup/count, TTL 30 min | 5 tests unitarios pasan |
| F4-03 | Crear skill `session_load` en `src/core/skills/session_load.py` | Carga estado por phone_hash, retorna nuevo si no existe | 3 tests |
| F4-04 | Crear skill `session_save` en `src/core/skills/session_save.py` | Guarda estado actualizado, limita historial a MAX_HISTORY_TURNS | 3 tests |
| F4-05 | Crear `flow_definitions/imv_flow.yaml` | Flujo IMV con 5 pasos, transiciones, opciones, texto es/fr | Archivo YAML valido |
| F4-06 | Crear `flow_definitions/empad_flow.yaml` | Flujo Empadronamiento con 4 pasos | Archivo YAML valido |
| F4-07 | Crear `flow_definitions/ts_flow.yaml` | Flujo Tarjeta Sanitaria con 4 pasos | Archivo YAML valido |
| F4-08 | Crear skill `flow_router` en `src/core/skills/flow_router.py` | Decide EN FLUJO / FUERA DE FLUJO basado en estado + regex + keywords | 6 tests |
| F4-09 | Crear skill `flow_step` en `src/core/skills/flow_step.py` | Navega grafo estatico, retorna texto + audio_url + opciones + next_step | 5 tests |
| F4-10 | Crear `build_flows.py` (script offline) | Lee YAMLs, genera JSONs con texto por idioma, genera OGGs con gTTS | Script ejecutable, genera archivos |
| F4-11 | Integrar skills nuevas en `pipeline_v2.py` | Pipeline completo con 15+ skills, backward-compatible con F3 | Tests de integracion pasan |
| F4-12 | Anadir 9 feature flags nuevos a `config.py` | GUIDED_FLOWS_ON, INTENT_CLASSIFIER_ON, TTS_ENGINE, ARABIC_ON, SESSION_TTL, MAX_HISTORY_TURNS, PREGENERATED_AUDIO_ON, FLOW_DEFINITIONS_PATH, THREAD_POOL_SIZE | Test de config pasa |

### D.2 Sprint 2: Audio OGG + Intent + Calidad

| # | Tarea | Exit Criteria | Evidencia |
|---|-------|---------------|-----------|
| F4-13 | Migrar `tts.py` para generar OGG ademas de MP3 | Soporte para formato OGG via pydub o ffmpeg | 3 tests |
| F4-14 | Actualizar `send_response.py` para enviar media_url con OGG | Audio OGG se reproduce en burbuja WhatsApp | Test integracion |
| F4-15 | Crear skill `intent_classify` en `src/core/skills/intent_classify.py` | Cascada regex -> keywords -> Gemini mini-call | 8 tests |
| F4-16 | Migrar `threading.Thread` a `ThreadPoolExecutor` en `webhook.py` | Pool controlado de 4 workers max | 2 tests |
| F4-17 | Implementar `cleanup_timer` en `conversation.py` | Thread daemon que limpia sesiones expiradas cada 5 min | 2 tests |
| F4-18 | Anadir keywords arabes a `detect_lang.py` (stub) | Deteccion basica de arabe si ARABIC_ON=true | 3 tests |
| F4-19 | Crear templates arabe en `prompts/templates.py` | Templates basicos para respuestas en arabe | 2 tests |
| F4-20 | Implementar Adaptive Response Level en LLM prompts | 3 niveles: basico (70 palabras), estandar (120), detallado (200) | Tests de longitud |

### D.3 Sprint 3: UX + Seguridad + Demo

| # | Tarea | Exit Criteria | Evidencia |
|---|-------|---------------|-----------|
| F4-21 | Implementar tiered trust labels | Cada respuesta lleva etiqueta: VERIFIED / ASSISTED / UNKNOWN | 4 tests |
| F4-22 | Crear allowlist de URLs/telefonos oficiales | Solo URLs .gob.es y telefonos 060/900 | 3 tests |
| F4-23 | Anadir 15 red-team prompts a tests | Inyeccion, jailbreak, datos falsos, PII extraction | 15 tests xfail/xpass |
| F4-24 | Implementar readability check (INFLESZ basico) | Verificar que respuestas estan por debajo de 130 palabras | 3 tests |
| F4-25 | Implementar graceful cold start handler | /health retorna 503 mientras arranca, 200 cuando ready | 2 tests |
| F4-26 | Configurar UptimeRobot (o mantener cron-job.org) | Ping cada 5-14 min para evitar sleep | Evidencia: logs de uptime |
| F4-27 | Actualizar Dockerfile para incluir flujos pregenerados | `data/flows/` incluido en imagen Docker | Docker build pasa |
| F4-28 | Crear WOW 3: foto de carta del gobierno | Usuario manda foto -> Clara la explica (via Gemini Vision) | Demo flow funciona |
| F4-29 | Actualizar demo_cache.json con entradas de flujo | Nuevas entradas cache para flujos guiados | Cache actualizado |
| F4-30 | Actualizar CLAUDE.md y docs con numeros Fase 4 | Todos los conteos coherentes | git diff limpio |

### D.4 Sprint 4: Notion + Documentacion + Cierre

| # | Tarea | Exit Criteria | Evidencia |
|---|-------|---------------|-----------|
| F4-31 | Crear ~74 entradas nuevas en Notion (total ~155) | Nuevas tareas en Backlog, nuevos tests en Testing DB | Notion poblado |
| F4-32 | Actualizar Notion HOME con metricas F4 | KPIs actualizados, diagrama F4 visible | Pagina actualizada |
| F4-33 | Crear pagina Notion "Fase 4" con diagrama | Diagrama ASCII + tabla de deliverables | Pagina creada |
| F4-34 | Ejecutar suite completa de tests | ~265 tests PASS (sin FAIL) | pytest output |
| F4-35 | Ejecutar ruff lint | 0 errores | ruff output |
| F4-36 | Verificar deploy Render con flujos guiados | /health ok, flujos guiados funcionales via WhatsApp | curl + WhatsApp test |

---

## E) Plan de Tests

### E.1 Resumen de tests proyectados

| Categoria | Fase 3 | Nuevos F4 | Total F4 |
|-----------|--------|-----------|----------|
| Unit tests | 82 | +77 | ~159 |
| Integration tests | 7 | +17 | ~24 |
| E2E / demo flows | 4 | +23 | ~27 |
| Red team / security | 3 | +15 | ~18 |
| Evals / quality | 16 | +21 | ~37 |
| **TOTAL** | **96** | **+153** | **~265** |

### E.2 Tests unitarios nuevos (+77)

| Archivo test | # Tests | Que prueban |
|-------------|---------|-------------|
| `tests/unit/test_conversation_state.py` | 8 | ConversationState dataclass: creacion, serializacion, TTL |
| `tests/unit/test_conversation_store.py` | 10 | ConversationStore: get, save, cleanup, thread-safety, count |
| `tests/unit/test_session_load.py` | 5 | Skill session_load: nueva sesion, sesion existente, expirada |
| `tests/unit/test_session_save.py` | 5 | Skill session_save: guardar, limitar historial, actualizar timestamp |
| `tests/unit/test_flow_router.py` | 10 | Skill flow_router: regex match, keyword match, EN/FUERA flujo |
| `tests/unit/test_flow_step.py` | 8 | Skill flow_step: navegacion, transiciones, opciones, audio_url |
| `tests/unit/test_intent_classify.py` | 10 | Skill intent_classify: regex, keywords, fallback, cascada |
| `tests/unit/test_flow_definitions.py` | 6 | YAML loading, schema validation, step consistency |
| `tests/unit/test_tts_ogg.py` | 5 | TTS: generacion OGG, hash caching, fallback a MP3 |
| `tests/unit/test_detect_lang_arabic.py` | 5 | detect_lang: keywords arabes, ARABIC_ON flag |
| `tests/unit/test_trust_labels.py` | 5 | Tiered trust: VERIFIED/ASSISTED/UNKNOWN asignacion |

### E.3 Tests de integracion nuevos (+17)

| Archivo test | # Tests | Que prueban |
|-------------|---------|-------------|
| `tests/integration/test_guided_flow_e2e.py` | 6 | Flujo completo IMV: inicio -> paso 1 -> paso 2 -> fin |
| `tests/integration/test_pipeline_v2.py` | 4 | Pipeline con skills nuevas: session + flow + intent |
| `tests/integration/test_threadpool.py` | 3 | ThreadPoolExecutor: max workers, timeout, cleanup |
| `tests/integration/test_build_flows.py` | 4 | Script build_flows: YAML -> JSON -> OGG correctos |

### E.4 Tests E2E y demo flows (+23)

| Test | Tipo | Que valida |
|------|------|-----------|
| Flujo IMV completo (es) | E2E | 5 pasos, texto + audio |
| Flujo IMV completo (fr) | E2E | 5 pasos en frances |
| Flujo Empadronamiento (es) | E2E | 4 pasos |
| Flujo Tarjeta Sanitaria (es) | E2E | 4 pasos |
| Salir de flujo con "salir" | E2E | guided_active=False |
| Volver a paso anterior | E2E | Transicion "volver" |
| Pregunta fuera de flujo durante flujo | E2E | Redireccion correcta |
| WOW 3: foto de carta | E2E | Gemini Vision procesa imagen |
| Cold start + primer request | E2E | 503 -> 200 transicion |
| Audio OGG reproduccion | E2E | Verificar formato correcto |

### E.5 Golden tests de veracidad (+21)

Cada golden test verifica que Clara responde con informacion CORRECTA para un tramite especifico:

| # | Pregunta | Respuesta esperada (substring) | Tramite |
|---|----------|-------------------------------|---------|
| G1 | "Que es el IMV?" | "prestacion de la Seguridad Social" | IMV |
| G2 | "Que documentos necesito para el IMV?" | "DNI" o "certificado de empadronamiento" | IMV |
| G3 | "Como me empadrono?" | "ayuntamiento" | Empadronamiento |
| G4 | "Necesito cita previa para empadronarme?" | "ayuntamiento" o "oficina" | Empadronamiento |
| G5 | "Como pido la tarjeta sanitaria?" | "centro de salud" | Tarjeta Sanitaria |
| ... | (16 tests mas) | Substrings verificados contra KB | Todos |

### E.6 Metricas de calidad de audio

| Metrica | Umbral | Como medir |
|---------|--------|-----------|
| Duracion audio / longitud texto | 0.5-2.0 s/100 chars | Script automatizado |
| Formato de salida | OGG Opus | Verificar MIME type |
| Tamano archivo | < 500 KB por respuesta | Verificar en disco |
| Generacion exitosa | 100% para flujos pre-generados | Build script logs |

---

## F) Plan Notion OS

### F.1 Estructura de paginas (proyectada Fase 4)

```
CivicAid OS (root)
  |
  +-- HOME — Panel del Proyecto (landing visual)
  |     |-- Hero + introduccion
  |     |-- El Problema (stats)
  |     |-- La Solucion: Clara
  |     |-- Stack Tecnologico (herramientas explicadas)
  |     |-- Arquitectura — Flujo del Pipeline (diagrama ASCII)
  |     |-- KPIs Dashboard (3x3 grid)
  |     |-- Navegacion a Fases
  |     +-- Equipo
  |
  +-- Para Jueces — Evaluacion Rapida
  |     |-- Que es Clara (3 frases)
  |     |-- Datos Clave (10 metricas)
  |     |-- Progreso por Fases
  |     |-- Donde Verificar (comandos)
  |     |-- Demo en Vivo (WOW moments)
  |     +-- Equipo
  |
  +-- Fases del Proyecto
  |     |-- Fase 0+1 (Plan + MVP) [con diagrama]
  |     |-- Fase 2 (Hardening) [con diagrama]
  |     |-- Fase 3 (Demo) [con diagrama]
  |     +-- Fase 4 (Humana) [con diagrama]
  |
  +-- Backlog DB (43 + ~30 nuevas entradas)
  +-- KB Tramites DB (12 entradas)
  +-- Demo & Testing DB (26 + ~44 nuevas entradas)
  +-- Recursos y Referencias
```

### F.2 Nuevas propiedades en DBs

**Backlog DB (+5 propiedades):**
- Fase (Select: F0-Plan / F1-MVP / F2-Hardening / F3-Demo / F4-Humana)
- Fecha cierre (Date)
- Commit SHA (Rich Text)
- Esfuerzo real (Number)
- Etiquetas (Multi-select: bug/feature/docs/refactor/test/ops/security)

**KB Tramites DB (+4 propiedades):**
- Idioma (Select: es / fr)
- Version (Number)
- Autor verificacion (Select: miembros del equipo)
- Confianza (Select: Alta / Media / Baja)

**Demo & Testing DB (+5 propiedades):**
- Fase (Select: F1-MVP / F2-Hardening / F3-Demo / F4-Humana)
- Ejecutado por (Select: equipo + CI/CD)
- Entorno (Select: Local / Docker / Render / CI)
- Archivo test (Rich Text)
- Evidence link (URL)

### F.3 KPIs Dashboard (pagina HOME)

```
+-------------------+-------------------+-------------------+
|   96 -> ~265      |    11 -> ~16      |    81 -> ~155     |
|   Tests           |    Skills         |    Notion Entries  |
+-------------------+-------------------+-------------------+
|    9 -> 18        |       3           |    2 + ar stub    |
|   Feature Flags   |    Tramites       |    Idiomas        |
+-------------------+-------------------+-------------------+
|   8 + 6 MP3       |    8 componentes  |    22/22 -> 36/36 |
|   + ~30 OGG       |    Health Check   |    Gates PASS     |
|   Cache + Audio    |                   |                   |
+-------------------+-------------------+-------------------+
```

### F.4 Entradas Notion proyectadas

| DB | Fase 3 | Nuevas F4 | Total F4 |
|----|--------|-----------|----------|
| Backlog | 43 | +30 (F4-01 a F4-36 - 6 no aplican) | ~73 |
| KB Tramites | 12 | +0 (mismos 3 tramites) | 12 |
| Demo & Testing | 26 | +44 (nuevos tests documentados) | ~70 |
| **TOTAL** | **81** | **+74** | **~155** |

---

## G) Diagramas por Fase

### G.1 Diagrama Fase 1 — MVP

```
+================================================================+
|                DIAGRAMA: FASE 1 — MVP                           |
|                32 tests | 14 tareas | 5 flags                  |
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
  |  1. Validar firma Twilio                 |
  |  2. Parsear Body, From, NumMedia         |
  |  3. detect_input_type                    |
  |  4. TwiML ACK --> HTTP 200 (<1s)         |
  |  5. threading.Thread(pipeline)           |
  +------------------------------------------+
       |                    |
       | TwiML ACK         | Background Thread
       v                    v
  [Twilio --> User]    +---------------------------+
  "Un momento..."      | PIPELINE (11 skills)      |
                       |                           |
                       | detect_input              |
                       |   |                       |
                       |   +--TEXT--+---AUDIO---+   |
                       |   |       |           |   |
                       |   |   fetch_media     |   |
                       |   |   convert_audio   |   |
                       |   |   transcribe      |   |
                       |   |       |           |   |
                       |   +---+---+           |   |
                       |       v               |   |
                       |   detect_lang         |   |
                       |       v               |   |
                       |   cache_match         |   |
                       |     |       |         |   |
                       |    HIT    MISS        |   |
                       |     |       |         |   |
                       |     |   kb_lookup     |   |
                       |     |   llm_generate  |   |
                       |     |   verify        |   |
                       |     |       |         |   |
                       |     +---+---+         |   |
                       |         v             |   |
                       |   send_response       |   |
                       +---------------------------+

  COMPONENTES F1:
  +------------------+  +----------+  +----------+
  | demo_cache.json  |  | KB JSONs |  | config.py|
  | 8 entradas       |  | 3 tram.  |  | 5 flags  |
  +------------------+  +----------+  +----------+
  | models.py: 8 dataclasses                     |
  | prompts/: system_prompt + templates (es/fr)  |
  | logger.py, timing.py                         |
  +----------------------------------------------+
```

### G.2 Diagrama Fase 2 — Hardening & Deploy

```
+================================================================+
|           DIAGRAMA: FASE 2 — HARDENING & DEPLOY                 |
|           93 tests (+61) | 6 gates P2.x | 9 flags (+4)        |
+================================================================+

  CAMBIOS SOBRE FASE 1 (marcados con [+NEW] y [~MOD]):

  [~MOD] WEBHOOK:
  +------------------------------------------+
  | RequestValidator (firma Twilio)          |
  | NumMedia safe parsing (try/except)       |
  | Silent thread death protection           |
  +------------------------------------------+

  [+NEW] SKILLS:
  +------------------------------------------+
  | guardrails.py: pre_check + post_check    |
  |   (blocklist, PII, disclaimer)           |
  | models_structured.py:                    |
  |   ClaraStructuredResponse               |
  | tts.py: gTTS on-demand + hash caching   |
  | observability.py:                        |
  |   RequestContext, request_id, timings    |
  +------------------------------------------+

  [+NEW] FLAGS (5 -> 9):
  +------------------------------------------+
  | + GUARDRAILS_ON = true                   |
  | + STRUCTURED_OUTPUT_ON = false            |
  | + OBSERVABILITY_ON = true                |
  | + RAG_ENABLED = false                    |
  +------------------------------------------+

  [+NEW] DEPLOY:
  +------------------------------------------+
  | Dockerfile (Python 3.11 + gunicorn)      |
  | render.yaml (16 env vars)               |
  | .dockerignore                            |
  | Puerto: 10000 (Render) / 5000 (local)  |
  +------------------------------------------+

  [+NEW] SEGURIDAD:
  +------------------------------------------+
  | Escaneo de secretos (11 patrones, 0 hit)|
  | .env en .gitignore                       |
  | render.yaml sync:false para secretos    |
  +------------------------------------------+

  [+NEW] NOTION:
  +------------------------------------------+
  | 81 entradas en 3 DBs                     |
  | 29 archivos de documentacion             |
  +------------------------------------------+
```

### G.3 Diagrama Fase 3 — Demo en Vivo

```
+================================================================+
|              DIAGRAMA: FASE 3 — DEMO EN VIVO                    |
|              96 tests (+3) | 7 gates P3.x                     |
+================================================================+

  [+NEW] TWILIO REAL:
  +------------------------------------------+
  | Sandbox configurado                      |
  | Signature validation activa              |
  | Test real via WhatsApp completado        |
  +------------------------------------------+

  [+NEW] OPS:
  +------------------------------------------+
  | cron-job.org cada 14 min --> /health     |
  | Runbook 8 escenarios de incidente        |
  | /health: 8 componentes, avg 166ms        |
  +------------------------------------------+

  [+NEW] QA DEEP AUDIT:
  +------------------------------------------+
  | phase3_verify.sh (7 pasos)               |
  | 12 contradicciones detectadas            |
  | 11 corregidas                            |
  +------------------------------------------+

  [+NEW] LOGGING JSON:
  +------------------------------------------+
  | JSONFormatter + request_id               |
  | Timings por stage en JSON                |
  +------------------------------------------+

  [+NEW] DEMO ASSETS:
  +------------------------------------------+
  | 6 MP3s pregrabados                       |
  | demo_cache.json (8 entradas)             |
  | Guion 6-8 min                            |
  | WOW 1 (texto) + WOW 2 (audio frances)   |
  | 1-pager ejecutivo                        |
  +------------------------------------------+

  ESTADO FINAL F3:
  +------------------------------------------+
  | 96/96 tests PASS                         |
  | 9 feature flags + 1 hardcoded            |
  | 11 skills en pipeline                    |
  | 81 entradas Notion                       |
  | Deploy Render verificado                 |
  | 22/22 gates PASS                         |
  +------------------------------------------+
```

### G.4 Diagrama Fase 4 — "Humana" (Arquitectura C)

```
+================================================================+
|          DIAGRAMA: FASE 4 "HUMANA" — PRE-GEN + GRAFO            |
|          ~265 tests | 18 flags | ~16 skills                    |
+================================================================+

  === BUILD TIME (offline) ===

  flow_definitions/*.yaml
       |
       v
  [build_flows.py] ---+--> [Gemini Flash] --> data/flows/*.json
                      |                        (texto es/fr por paso)
                      |
                      +--> [gTTS/edge-tts] --> data/flows/audio/*.ogg
                                               (~30 archivos OGG)

  === RUNTIME (Render 512 MB, ~175 MB pico) ===

  Usuario WhatsApp (es/fr/ar)
       |
       v
  [Twilio Cloud]
       |
       v POST /webhook
  +--------------------------------------------------------------+
  |  FLASK + ThreadPoolExecutor(4)              ~134 MB base     |
  |                                                              |
  |  [TwiML ACK <1s] --> PIPELINE v2:                            |
  |                                                              |
  |  +--------------------------------------------------------+  |
  |  |                                                        |  |
  |  | 1. [guardrail_pre] blocklist, PII, self-harm           |  |
  |  |         | safe                                         |  |
  |  | 2. [detect_input] TEXT / AUDIO                          |  |
  |  |         |                                              |  |
  |  |     TEXT ----+---- AUDIO                                |  |
  |  |              |   3. [fetch_media]                        |  |
  |  |              |   4. [transcribe] (Gemini)               |  |
  |  |              +----+                                     |  |
  |  |                   v                                     |  |
  |  | 5. [detect_lang] es / fr / ar                           |  |
  |  |         v                                              |  |
  |  | 6. [session_load] ConvStore(dict+TTL)                   |  |
  |  |         v                                              |  |
  |  | 7. [flow_router] -- EN FLUJO / FUERA DE FLUJO           |  |
  |  |         |                    |                          |  |
  |  |    EN FLUJO             FUERA DE FLUJO                  |  |
  |  |         |                    |                          |  |
  |  |  8a.[flow_step]        8b.[cache_match]                 |  |
  |  |    resp. pre-gen            |                           |  |
  |  |    + audio OGG         9. [intent_classify]             |  |
  |  |    10-50 ms                 |                           |  |
  |  |         |             10.[kb_lookup]                    |  |
  |  |         |             11.[llm_generate] (Gemini)        |  |
  |  |         |             12.[verify_response]              |  |
  |  |         |             13.[guardrail_post]               |  |
  |  |         |             14.[tts_generate] (gTTS/edge)     |  |
  |  |         |                    |                          |  |
  |  |         +--------+-----------+                          |  |
  |  |                  v                                      |  |
  |  | 15.[session_save] actualizar estado                     |  |
  |  |         v                                              |  |
  |  | 16.[send_response] Twilio REST + media_url              |  |
  |  +--------------------------------------------------------+  |
  |                                                              |
  |  +-----------+ +--------+ +----------+ +--------+ +-------+  |
  |  |flows/*.json| |KB .json| |ConvStore | |cache   | |config |  |
  |  |+audio/    | |3 tram. | |dict+TTL  | |.json   | |18flags|  |
  |  +-----------+ +--------+ +----------+ +--------+ +-------+  |
  +--------------------------------------------------------------+
       |
       v Twilio REST
  [Twilio] --> Usuario WhatsApp
  (texto + audio OGG nativo en burbuja)
```

### G.5 Pipeline F4 Detallado — Inputs/Outputs por Skill

```
+================================================================+
|     PIPELINE v2 DETALLADO — 16 SKILLS — INPUTS / OUTPUTS       |
+================================================================+

  IncomingMessage {from_number, body, media_url, media_type, input_type}
       |
  [1. guardrail_pre]
       IN:  text (str)
       OUT: GuardrailResult {safe, reason, modified}
       FLAG: GUARDRAILS_ON
       |
  [2. detect_input]
       IN:  num_media, media_type
       OUT: InputType (TEXT | AUDIO | IMAGE)
       |
       +-- TEXT --+-- AUDIO --+
       |          |           |
       |    [3. fetch_media]  |
       |          IN: media_url
       |          OUT: bytes
       |          |           |
       |    [4. transcribe]   |
       |          IN: audio_bytes, mime_type
       |          OUT: TranscriptResult {text, lang, duration_ms}
       |          FLAG: WHISPER_ON
       |          |           |
       +-----+---+           |
             v
  [5. detect_lang]
       IN:  text
       OUT: language ("es"|"fr"|"ar")
       |
  [6. session_load]      [+NEW F4]
       IN:  phone_hash
       OUT: ConversationState
       FLAG: GUIDED_FLOWS_ON
       |
  [7. flow_router]       [+NEW F4]
       IN:  text, state, language
       OUT: FlowDecision {in_flow, flow_name, step_num, user_intent}
       FLAG: GUIDED_FLOWS_ON
       |
       +-- EN FLUJO --+-- FUERA --+
       |              |           |
  [8a. flow_step]     |     [8b. cache_match]
    IN: flow.json,    |       IN: text, idioma
        step_num      |       OUT: CacheResult
    OUT: FlowStep {   |           |
      text, audio_url,|      [9. intent_classify]  [+NEW F4]
      next_step,      |       IN: text, language
      options[],      |       OUT: Intent {name, confidence, tramite}
      complete}       |       FLAG: INTENT_CLASSIFIER_ON
       |              |           |
       |              |     [10. kb_lookup]
       |              |       IN: text, intent, language
       |              |       OUT: KBContext
       |              |           |
       |              |     [11. llm_generate]
       |              |       IN: text, KBContext, language, history
       |              |       OUT: LLMResponse
       |              |       FLAG: LLM_LIVE, LLM_TIMEOUT
       |              |           |
       |              |     [12. verify_response]
       |              |       IN: response_text, KBContext
       |              |       OUT: verified_text
       |              |           |
       |              |     [13. guardrail_post]
       |              |       IN: response_text
       |              |       OUT: safe_text + disclaimers
       |              |           |
       |              |     [14. tts_generate]
       |              |       IN: text, language
       |              |       OUT: audio_url (OGG/MP3)
       |              |       FLAG: TTS_ENGINE, PREGENERATED_AUDIO_ON
       |              |           |
       +------+-------+-----------+
              v
  [15. session_save]     [+NEW F4]
       IN:  state, user_text, response_text
       OUT: void
       FLAG: GUIDED_FLOWS_ON
       |
  [16. send_response]
       IN:  FinalResponse {to_number, body, media_url}
       OUT: bool (enviado)
       TIMEOUT: 10s
```

### G.6 Flujo Guiado como Maquina de Estados

```
  Ejemplo: Flujo IMV (5 pasos)

  [Usuario: "Quiero solicitar el IMV"]
       |
       v
  +============+
  | PASO 1:    |
  | Intro IMV  |-----> "Que es el IMV, para que sirve..."
  | Opciones:  |       + audio OGG
  | [requisitos]|
  | [solicitar] |
  | [documentos]|
  +============+
       |
  [Usuario: "requisitos"]
       |
       v
  +============+
  | PASO 2:    |
  | Requisitos |-----> "Para solicitar el IMV necesitas..."
  | Opciones:  |       + audio OGG
  | [solicitar] |
  | [documentos]|
  | [volver]    |
  +============+
       |
  [Usuario: "solicitar"]
       |
       v
  +============+          +============+
  | PASO 3:    |          | PASO 4:    |
  | Como       |          | Documentos |
  | solicitar  |          | necesarios |
  +============+          +============+
       |                       |
       +-----------+-----------+
                   |
  [Usuario: "salir" o fin de flujo]
       |
       v
  +============+
  | PASO 5:    |
  | Resumen +  |-----> "Telefono: 900 XXX XXX, URL: www.seg-social.gob.es"
  | contacto   |       + audio OGG
  | guided=    |
  | False      |
  +============+

  Palabras de control:
    "volver" / "retour"   --> paso anterior
    "salir" / "quitter"   --> salir del flujo
    "menu" / "inicio"     --> paso 1 del flujo
```

---

## H) Narrativa para Jueces + Elevator Pitch

### H.1 Estructura narrativa (hibrida A+B+C)

La rubrica del hackathon: **Elevator Pitch 40%**, Social Entities 25%, Prototype Demo 25%, Sustainability 10%.

```
GANCHO EMOCIONAL (Maria/Ahmed) --> DATOS QUE ESCALAN --> DEMO EN VIVO --> CIERRE OPEN SOURCE
         Estrategia A                Estrategia B          Demo            Estrategia C
         (40% pitch)                (25% social)         (25% proto)      (10% sostenibilidad)
```

### H.2 Elevator Pitch (2 minutos, ~270 palabras)

> *[Robert se pone de pie. Mira al jurado.]*
>
> "En Espana viven casi 10 millones de personas de origen inmigrante. Dos de cada tres han sufrido barreras burocraticas. Muchos tienen derecho a una ayuda economica, a la sanidad, a inscribirse en su municipio... pero no lo consiguen. Porque la informacion esta en espanol tecnico, repartida en decenas de webs, y no hay nadie que se lo explique en su idioma.
>
> Y luego estan nuestros mayores. Entre los de mas de 84 anos, solo el 17% usa internet con frecuencia. Para ellos, un tramite online no es una solucion. Es otro muro.
>
> Nosotros hemos construido a Clara.
>
> Clara es una asistente de WhatsApp. Le escribes o le hablas, en tu idioma, y te explica tus derechos paso a paso. Con palabras simples. Con un audio que puedes escuchar cuando quieras.
>
> Por que WhatsApp? Porque 33 millones de personas en Espana ya lo usan cada dia. No hay que descargar nada.
>
> Por que voz? Porque muchas de estas personas se sienten mas comodas hablando que escribiendo.
>
> Y lo mas importante: toda la informacion que da Clara viene de fuentes oficiales del gobierno. No inventa. No improvisa. Si no sabe algo, te da un telefono para hablar con una persona.
>
> *[Senala la pantalla]*
>
> Ahora mismo, Clara esta desplegada y funcionando. 96 pruebas automatizadas. 3 tramites reales. 2 idiomas. Y todo el codigo es abierto y gratuito. Cualquier ayuntamiento puede tomar Clara manana y empezar a usarla. Sin pagar un euro.
>
> Esto es Clara. Una amiga que te explica tus derechos por WhatsApp.
>
> Vamos a verla en accion."

### H.3 Frases clave para USAR

| Frase | Cuando usarla |
|-------|---------------|
| "Informacion verificada" | Siempre que se hable de la respuesta de Clara |
| "En tu idioma" | Al presentar la deteccion de idioma |
| "Sin descargar nada" | Al hablar de WhatsApp |
| "Paso a paso, con palabras simples" | Al describir como responde Clara |
| "Codigo abierto y gratuito" | Al cerrar con sostenibilidad |
| "Como hablar con una amiga que trabaja en el ayuntamiento" | Al explicar que es Clara |
| "No inventa, no improvisa" | Al hablar de fiabilidad |

### H.4 Frases a EVITAR

| Nunca digas | Di en su lugar |
|-------------|----------------|
| "Inteligencia artificial" / "IA" | "Clara entiende lo que le dices" |
| "Modelo de lenguaje" / "LLM" | "El cerebro de Clara" |
| "Pipeline" | "El proceso que sigue Clara para responderte" |
| "API" | "La conexion con WhatsApp" |
| "Deploy" | "Poner Clara a funcionar" |
| "Cache" | "Respuestas preparadas para preguntas frecuentes" |
| "Feature flags" | (no mencionarlos) |

### H.5 Datos para impacto social

| Dato | Fuente |
|------|--------|
| 9,96 millones de inmigrantes en Espana | INE, oct 2025 |
| 67% ha sufrido barreras burocraticas | Servicio Jesuita a Migrantes, 2025 |
| 33 millones de usuarios WhatsApp en Espana | SociallyIn, 2025 |
| Solo 17% de mayores de 84 usa internet frecuentemente | CSIC |
| Trabajador social: ~2.000 EUR/mes. Clara: 0 EUR/mes | SalaryExpert |
| 6 meses plazo maximo IMV | Seguridad Social |

### H.6 WOW Moments para Demo

| WOW | Que pasa | Que demuestra |
|-----|----------|---------------|
| **WOW 1** | Maria escribe "Que es el IMV?" | Velocidad (<2s), claridad, audio accesible |
| **WOW 2** | Ahmed envia audio en frances sobre empadronamiento | Deteccion idioma, voz, multilingue |
| **WOW 3** (F4) | Usuario manda foto de carta del gobierno | Gemini Vision, explicacion humanizada |
| **WOW 4** (F4) | Usuario sigue flujo guiado IMV paso a paso | Respuesta instantanea (10-50ms), audio OGG nativo |

---

## Anexo: Feature Flags (9 existentes + 9 nuevos = 18)

| # | Flag | Tipo | Default | Descripcion |
|---|------|------|---------|-------------|
| 1 | DEMO_MODE | bool | false | Cache-only, skip LLM |
| 2 | LLM_LIVE | bool | true | Habilita Gemini |
| 3 | WHISPER_ON | bool | true | Habilita transcripcion audio |
| 4 | LLM_TIMEOUT | int | 6 | Segundos max Gemini |
| 5 | WHISPER_TIMEOUT | int | 12 | Segundos max Whisper |
| 6 | GUARDRAILS_ON | bool | true | Habilita guardrails |
| 7 | STRUCTURED_OUTPUT_ON | bool | false | Habilita JSON estructurado |
| 8 | OBSERVABILITY_ON | bool | true | Habilita metricas |
| 9 | RAG_ENABLED | bool | false | RAG (stub) |
| **10** | **GUIDED_FLOWS_ON** | bool | false | **Activa flujos guiados** |
| **11** | **INTENT_CLASSIFIER_ON** | bool | false | **Activa clasificacion de intenciones** |
| **12** | **TTS_ENGINE** | str | "gtts" | **Motor TTS: gtts, edge-tts, none** |
| **13** | **ARABIC_ON** | bool | false | **Soporte arabe** |
| **14** | **SESSION_TTL** | int | 1800 | **TTL sesiones (30 min)** |
| **15** | **MAX_HISTORY_TURNS** | int | 3 | **Turnos en historial** |
| **16** | **PREGENERATED_AUDIO_ON** | bool | true | **Audio pregenerado para flujos** |
| **17** | **FLOW_DEFINITIONS_PATH** | str | "data/flows/" | **Ruta definiciones de flujo** |
| **18** | **THREAD_POOL_SIZE** | int | 4 | **Workers del ThreadPoolExecutor** |

**Migracion:** Con TODOS los flags nuevos en sus valores default, el sistema se comporta EXACTAMENTE como Fase 3. Los flags nuevos estan desactivados por defecto.

---

## Anexo: Items A VALIDAR

| ID | Claim | Como validar |
|----|-------|--------------|
| V1 | Piper TTS ~500MB runtime | Medir con `memory_profiler` en contenedor |
| V2 | Kokoro-82M ~200-300MB RAM | Cargar modelo ONNX y medir RSS |
| V3 | Solo OGG se reproduce nativo en WhatsApp | Probar envio MP3 vs OGG en sandbox Twilio |
| V4 | Cold start Render 30-50s | Medir con UptimeRobot logs |
| V5 | gTTS/edge-tts sin modelo local | Verificar que no cachea modelo localmente |
| V6 | ThreadPoolExecutor(4) ~8MB | Medir con `tracemalloc` bajo carga |
| V7 | SQLite disco efimero persiste entre requests | Probar escritura + lectura tras 10 min |

---

## Anexo: Fuentes y Referencias

### Estadisticas Sociales
- [INE: Estadistica Continua de Poblacion, oct 2025](https://www.ine.es/dyngs/Prensa/ECP3T25.htm)
- [Servicio Jesuita a Migrantes: Informe 2025](https://sjme.org/2026/01/26/informe-sobre-poblacion-de-origen-inmigrado-en-espana-2025/)
- [SociallyIn: WhatsApp Statistics 2025](https://sociallyin.com/whatsapp-statistics/)
- [65 y Mas: Brecha digital senior](https://www.65ymas.com/sociedad/tecnologia/brecha-digital-se-reduce-cada-ano-hay-millon-mas-senior-digitales-en-espana_79304_102.html)
- [SalaryExpert: Social Worker Salary Spain](https://www.salaryexpert.com/salary/job/social-worker/spain)

### Arquitectura y TTS
- [Atlassian: Microservices vs Monolith](https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith)
- [Inferless: 12 Best Open-Source TTS 2025](https://www.inferless.com/learn/comparing-different-text-to-speech---tts--models-part-2)
- [Piper TTS GitHub](https://github.com/rhasspy/piper)
- [Kokoro-82M HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)
- [BentoML: Best Open-Source TTS 2026](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)
- [Miguel Grinberg: Flask Background Jobs](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs)
- [Twilio: WhatsApp Media Guidance](https://www.twilio.com/docs/whatsapp/guidance-whatsapp-media-messages)

### Render y Cold Starts
- [Render Community: Free Tier](https://community.render.com/t/the-free-instance-type-e-g-512mb-ram-0-1-cpu/39044)
- [UptimeRobot: Keep Alive](https://uptimerobot.com/keep-alive/)
- [Sergei Liski: Run Full-Time on Render Free](https://sergeiliski.medium.com/how-to-run-a-full-time-app-on-renders-free-tier-without-it-sleeping-bec26776d0b9)

### Hackathon y Pitch
- [OdiseIA4Good Hackathon](https://www.odiseia4good.org/en)
- [TAIKAI: How to Create a Winning Hackathon Pitch](https://taikai.network/en/blog/how-to-create-a-hackathon-pitch)
- [MIT Solve: Social Impact Pitch](https://solve.mit.edu/articles/5-tips-for-the-perfect-social-impact-pitch)
- [Stanford: Communicating Technical Ideas](https://online.stanford.edu/10-tips-communicating-technical-ideas-non-technical-people)

### Intent Classification
- [Label Your Data: Intent Classification 2025](https://labelyourdata.com/articles/machine-learning/intent-classification)
- [FastText: Meta AI](https://ai.meta.com/tools/fasttext/)
- [DataCamp: Intent with Regex](https://campus.datacamp.com/courses/building-chatbots-in-python/understanding-natural-language?ex=2)

### Conversation State
- [Kevin de Bree: Chatbot Persistent Memory SQLite](https://medium.com/@kpdebree/solving-chatbot-amnesia-building-an-ai-agent-with-persistent-memory-using-python-openai-and-b9ec166c298a)
- [Redis: Real-Time Chatbots](https://redis.io/blog/redis-as-the-engine-behind-real-time-intelligent-chatbots/)

---

> **Siguiente paso:** Aprobar este documento y ejecutar el backlog (D.1-D.4) siguiendo el plan task-by-task. Opcion 1: Subagent-driven en esta sesion. Opcion 2: Sesion paralela con executing-plans.
