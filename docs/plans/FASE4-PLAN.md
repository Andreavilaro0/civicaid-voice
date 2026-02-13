# FASE 4 — Plan de Implementacion Consolidado

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Evolucionar Clara de MVP funcional a asistente accesible, verificable y con audio nativo — priorizando personas vulnerables (inmigrantes, mayores, baja alfabetizacion, discapacidad visual).

**Architecture:** Incremental (Architecture A) — modificar archivos existentes, anadir 6 skills nuevos, 3 feature flags. Sin refactor estructural. Cada feature protegida por flag para rollback inmediato.

**Tech Stack:** Python 3.11, Flask, gTTS + pydub (OGG Opus), Gemini 1.5 Flash, Twilio WhatsApp, Docker, Render

---

## Indice

1. [Vision y Contexto](#1-vision-y-contexto)
2. [Decision de Arquitectura](#2-decision-de-arquitectura)
3. [Pipeline Post-Fase 4 (Diagrama)](#3-pipeline-post-fase-4)
4. [Como Funciona Clara (Explicado para Humanos)](#4-como-funciona-clara)
5. [Stack Tecnologico (Que Hace Cada Herramienta)](#5-stack-tecnologico)
6. [Plan F4.1-F4.6 (Tareas + Gates + Evidencia)](#6-plan-de-implementacion)
7. [Top 10 Riesgos y Mitigaciones](#7-top-10-riesgos)
8. [6 Conversaciones de Ejemplo](#8-conversaciones-de-ejemplo)
9. [Como Verificar (Comandos)](#9-como-verificar)
10. [Notion Dashboard Schema](#10-notion-dashboard)

---

## 1. Vision y Contexto

### El Problema

```
  +------------------------------------------------------------------+
  |                    BARRERA BUROCRATICA                            |
  |                                                                  |
  |  3,2M inmigrantes  +  9,5M personas mayores  +  8% analfabetos  |
  |       en Espana          con baja           funcionales          |
  |                       alfabetizacion                             |
  |                         digital                                  |
  |                                                                  |
  |  Necesitan:                                                      |
  |  - IMV (Ingreso Minimo Vital)      -> 900 20 22 22              |
  |  - Empadronamiento                 -> 010                       |
  |  - Tarjeta Sanitaria               -> 900 102 112               |
  |                                                                  |
  |  Pero enfrentan:                                                 |
  |  - Formularios solo en espanol, lenguaje juridico                |
  |  - Webs inaccesibles (WCAG incumplido)                          |
  |  - Citas previas con procesos digitales exclusivamente           |
  |  - Informacion contradictoria entre fuentes                      |
  +------------------------------------------------------------------+
```

### La Solucion: Clara

Clara es un asistente WhatsApp que responde por TEXTO + AUDIO SIEMPRE, en espanol, frances y arabe (stub), usando SOLO informacion verificada de fuentes oficiales.

### Estado Actual (Baseline Fase 3)

| Metrica | Valor |
|---------|-------|
| Skills | 11 |
| Feature Flags | 9 |
| Tests | 96 (91 passed + 5 xpassed) |
| Tramites KB | 3 (IMV, empadronamiento, tarjeta sanitaria) |
| Idiomas | 2 (es, fr) |
| Cache entries | 8 + 6 MP3 |
| Audio formato | MP3 (gTTS) — NO nativo WhatsApp |
| RAM Render | ~200MB |

### Problemas a Resolver en Fase 4

```
  PROBLEMA                              SOLUCION FASE 4
  +----------------------------------+  +----------------------------------+
  | Audio NO garantizado             |  | Dual response SIEMPRE            |
  | (TTS puede fallar, cache sin     |  | (texto + audio OGG en cada       |
  |  audio para saludos)             |  |  respuesta, 0 excepciones)       |
  +----------------------------------+  +----------------------------------+
  | Verificacion DEBIL               |  | Truth Mode: trust labels         |
  | (verify_response solo anade      |  | [VERIFICADO] / [ORIENTATIVO]     |
  |  URL y limita palabras)          |  | con grounding contra KB          |
  +----------------------------------+  +----------------------------------+
  | SIN arabe                        |  | Arabic stub: detecta ar,         |
  | (detect_lang no lo contempla,    |  | responde template + telefono     |
  |  templates sin soporte)          |  | de atencion oficial              |
  +----------------------------------+  +----------------------------------+
  | Respuestas con JERGA             |  | simplify_response: diccionario   |
  | (lenguaje administrativo que     |  | jerga->simple, limite 150        |
  |  el usuario no entiende)         |  | palabras, pregunta seguimiento   |
  +----------------------------------+  +----------------------------------+
  | Audio MP3                        |  | OGG Opus: formato nativo         |
  | (no se reproduce inline          |  | WhatsApp, se reproduce como      |
  |  en WhatsApp)                    |  | nota de voz                      |
  +----------------------------------+  +----------------------------------+
  | SIN metricas por skill           |  | JSON logs: latencia por skill,   |
  | (observability global pero       |  | fallback_reason, source_chain    |
  |  no granular)                    |  | exportable para evidencia        |
  +----------------------------------+  +----------------------------------+
```

---

## 2. Decision de Arquitectura

### 3 Opciones Evaluadas

```
  +---------------------+  +---------------------+  +---------------------+
  | A: INCREMENTAL      |  | B: PIPELINE v2      |  | C: EVENT-DRIVEN     |
  | (Evolucion in-place)|  | (Rewrite parcial)   |  | (Desacoplado)       |
  +---------------------+  +---------------------+  +---------------------+
  | Archivos nuevos: 5  |  | Archivos nuevos: 16 |  | Archivos nuevos: 20+|
  | Archivos modif.: 9  |  | Archivos modif.: 8  |  | Archivos modif.: 8  |
  | Flags nuevos: 3     |  | Flags nuevos: 4     |  | Flags nuevos: 5     |
  | RAM extra: +20MB    |  | RAM extra: +25MB    |  | RAM extra: +40MB    |
  | Riesgo: BAJO        |  | Riesgo: MEDIO       |  | Riesgo: ALTO        |
  | Tiempo: 2 dias      |  | Tiempo: 3 dias      |  | Tiempo: 5+ dias     |
  +---------------------+  +---------------------+  +---------------------+
         ^^^
     SELECCIONADA
```

### Justificacion: Arquitectura A (Incremental)

1. **Hackathon = velocidad**: 5 personas, dias limitados. No es momento de refactors.
2. **Riesgo minimo**: 96 tests passing. Cambios aditivos, no destructivos.
3. **Deploy identico**: Sin cambios en Dockerfile base (solo +ffmpeg para OGG).
4. **Familiar**: El equipo ya conoce pipeline.py y skills/. Zero curva de aprendizaje.
5. **Rollback por flag**: TRUTH_MODE, ARABIC_STUB_ON, OGG_AUDIO — desactivar sin tocar codigo.
6. **RAM safe**: +20MB dentro del margen de 512MB de Render free tier.

---

## 3. Pipeline Post-Fase 4

### Diagrama Completo

```
  USUARIO (WhatsApp)
    |
    | Envia texto, audio o imagen
    v
  +------------------------------------------------------------------+
  |                        TWILIO                                     |
  |  Recibe mensaje, envia POST a /webhook con Body, From,           |
  |  MediaUrl0, MediaContentType0, NumMedia                          |
  +------------------------------------------------------------------+
    |
    v
  +------------------------------------------------------------------+
  |                    FLASK /webhook                                 |
  |  1. Valida firma Twilio (RequestValidator)                       |
  |  2. Parsea IncomingMessage (from, body, media_url, input_type)   |
  |  3. Devuelve TwiML ACK al instante (<1 segundo)                 |
  |  4. Lanza hilo de fondo: threading.Thread(target=process)        |
  +------------------------------------------------------------------+
    |                    |
    | HTTP 200 (ACK)     | Background Thread
    v                    v
  USUARIO ve:       +----------------------------------------------------+
  "Procesando..."   |          pipeline.process(msg)                      |
                    |                                                      |
                    |  [1] GUARDRAIL PRE                                   |
                    |      Detecta contenido inseguro (inyeccion,          |
                    |      off-topic, PII). Si BLOCKED -> tts -> send     |
                    |                                                      |
                    |  [2] AUDIO?                                          |
                    |      SI -> fetch_media (descarga audio de Twilio)    |
                    |        -> transcribe (Gemini Flash: audio -> texto)  |
                    |      NO -> detect_lang (langdetect + keywords)       |
                    |            Detecta: es, fr, ar, en                   |
                    |                                                      |
                    |  [3] ARABE? (ARABIC_STUB_ON=true)                    |
                    |      SI -> arabic_stub: template en arabe +          |
                    |            telefono de atencion -> tts -> send       |
                    |                                                      |
                    |  [4] CACHE MATCH                                     |
                    |      Busca en demo_cache.json (8 respuestas pre-     |
                    |      calculadas). HIT -> tts_ensure (genera audio    |
                    |      si falta) -> send                               |
                    |                                                      |
                    |  [5] DEMO_MODE?                                      |
                    |      SI -> fallback generico -> tts -> send          |
                    |                                                      |
                    |  [6] KB LOOKUP                                       |
                    |      Busca en data/tramites/*.json (3 KBs:           |
                    |      IMV, empadronamiento, tarjeta_sanitaria)        |
                    |      Retorna: tramite, datos, fuente_url,            |
                    |      verificado, claims_available                    |
                    |                                                      |
                    |  [7] LLM GENERATE                                    |
                    |      Gemini 1.5 Flash con system prompt anti-        |
                    |      alucinacion + KB como contexto. temp=0.3,       |
                    |      max_tokens=500, timeout=6s                      |
                    |                                                      |
                    |  [8] TRUTH VERIFY (TRUTH_MODE=true)                  |
                    |      Extrae claims -> compara con KB ->              |
                    |      asigna etiquetas:                               |
                    |        [VERIFICADO] = dato en KB verificada          |
                    |        [ORIENTATIVO] = dato en KB no verificada      |
                    |        [NO VERIFICADO] = dato sin fuente             |
                    |      Anade fuente oficial al final                   |
                    |      Si >50% no verificado -> disclaimer reforzado   |
                    |                                                      |
                    |  [9] STRUCTURED OUTPUT (opcional)                    |
                    |                                                      |
                    | [10] GUARDRAIL POST                                  |
                    |      Redaccion PII, disclaimer final                 |
                    |                                                      |
                    | [11] SIMPLIFY RESPONSE                               |
                    |      Reemplaza jerga administrativa por              |
                    |      lenguaje simple (diccionario 50+ terminos)      |
                    |      Limita a 150 palabras                           |
                    |      Anade pregunta de seguimiento                   |
                    |                                                      |
                    | [12] TTS (OGG primary, MP3 fallback)                 |
                    |      gTTS genera MP3 -> pydub convierte a OGG Opus  |
                    |      Cache por hash. NUNCA retorna None              |
                    |      Si OGG falla -> MP3. Si todo falla -> log       |
                    |                                                      |
                    | [13] SEND RESPONSE (Twilio REST API)                 |
                    |      Envia: texto + media_url (audio OGG/MP3)       |
                    |      Retry sin media si falla con media              |
                    |                                                      |
                    | [14] LOG METRICS (JSON)                              |
                    |      Latencia por skill, source_chain,               |
                    |      fallback_reason, trust_label                    |
                    +----------------------------------------------------+
                                        |
                                        v
                                   USUARIO recibe:
                                   Texto + Nota de Voz (OGG)
```

### Resumen de Skills (17 total)

```
  SKILLS EXISTENTES (11)             SKILLS NUEVOS (6)
  +---------------------------+      +---------------------------+
  | 1. guardrail_pre          |      | 6. arabic_stub       NUEVO|
  | 2. detect_input           |      |10. truth_verify      NUEVO|
  | 3. fetch_media            |      |13. simplify_response NUEVO|
  | 4. transcribe             |      |14. tts_ensure        NUEVO|
  | 5. detect_lang  MODIFICADO|      |16. tts_ogg           NUEVO|
  | 7. cache_match            |      |18. metrics_collector NUEVO|
  | 8. kb_lookup    MODIFICADO|      +---------------------------+
  | 9. llm_generate           |
  |11. verify_resp  MODIFICADO|      FEATURE FLAGS NUEVOS (3)
  |12. guardrail_post         |      +---------------------------+
  |15. tts          MODIFICADO|      | TRUTH_MODE    = false     |
  |17. send_response          |      | ARABIC_STUB_ON= true      |
  +---------------------------+      | OGG_AUDIO     = true      |
                                     +---------------------------+
```

---

## 4. Como Funciona Clara

### Para Humanos (sin jerga tecnica)

```
  +-------------------------------------------------------------------+
  |  COMO FUNCIONA CLARA — Explicado Simple                           |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  1. ESCRIBES O HABLAS por WhatsApp                                |
  |     -> "Hola, necesito ayuda con el empadronamiento"              |
  |     -> O envias un audio preguntando lo mismo                     |
  |                                                                   |
  |  2. CLARA ENTIENDE tu mensaje                                     |
  |     -> Si escribiste: detecta tu idioma (espanol, frances)        |
  |     -> Si hablaste: convierte tu voz a texto y luego lo entiende  |
  |     -> Si es arabe: te da un telefono de atencion directa         |
  |                                                                   |
  |  3. CLARA BUSCA la informacion OFICIAL                            |
  |     -> Primero: mira si ya tiene esa respuesta preparada (cache)  |
  |     -> Si no: busca en su base de datos de tramites verificados   |
  |     -> Usa IA para redactar la respuesta en lenguaje simple       |
  |     -> VERIFICA que todo lo que dice esta en fuentes oficiales    |
  |                                                                   |
  |  4. CLARA TE RESPONDE con TEXTO + AUDIO                          |
  |     -> Texto: respuesta corta (max 150 palabras), sin jerga       |
  |     -> Audio: nota de voz para que puedas escuchar sin leer       |
  |     -> Fuente: siempre incluye web o telefono oficial             |
  |     -> Pregunta: "Tienes alguna otra duda sobre este tramite?"    |
  |                                                                   |
  +-------------------------------------------------------------------+
```

### Para Tecnicos (diagrama de decision)

```
  Mensaje llega
    |
    +-- Es seguro? --(NO)--> "No puedo ayudar con ese tema"
    |
    +-- Es audio? --(SI)--> Descargar -> Transcribir (Gemini)
    |               (NO)--> Detectar idioma
    |
    +-- Es arabe? --(SI)--> Template arabe + telefono
    |
    +-- Esta en cache? --(SI)--> Respuesta pre-calculada + audio
    |
    +-- DEMO_MODE? --(SI)--> Fallback generico
    |
    +-- Buscar KB --> Encontro tramite? --(NO)--> "No tengo esa info"
    |                                   --(SI)--> Datos del tramite
    |
    +-- Gemini genera respuesta (con system prompt anti-alucinacion)
    |
    +-- Verificar contra KB --> [VERIFICADO] / [ORIENTATIVO]
    |
    +-- Simplificar (quitar jerga, max 150 palabras)
    |
    +-- Generar audio OGG Opus
    |
    +-- Enviar: texto + audio por WhatsApp
```

---

## 5. Stack Tecnologico

### Que Hace Cada Herramienta

```
  +---------------------------------------------------------------------+
  |                   STACK TECNOLOGICO DE CLARA                        |
  +---------------------------------------------------------------------+
  |                                                                     |
  |  LENGUAJE Y FRAMEWORK                                              |
  |  +-------------------+  +-------------------+                      |
  |  | Python 3.11       |  | Flask             |                      |
  |  | Lenguaje principal|  | Framework web     |                      |
  |  | Facil de leer,    |  | ligero. Recibe    |                      |
  |  | gran ecosistema   |  | webhooks de       |                      |
  |  | de IA/ML          |  | Twilio, sirve     |                      |
  |  |                   |  | /health, /static  |                      |
  |  +-------------------+  +-------------------+                      |
  |                                                                     |
  |  COMUNICACION                                                      |
  |  +-------------------+  +-------------------+                      |
  |  | Twilio            |  | WhatsApp          |                      |
  |  | API que conecta   |  | Canal donde vive  |                      |
  |  | nuestra app con   |  | el usuario. Envia |                      |
  |  | WhatsApp. Recibe  |  | texto, audio,     |                      |
  |  | mensajes (POST    |  | imagenes. Recibe  |                      |
  |  | webhook) y envia  |  | texto + notas de  |                      |
  |  | respuestas (REST) |  | voz (OGG Opus)    |                      |
  |  +-------------------+  +-------------------+                      |
  |                                                                     |
  |  INTELIGENCIA ARTIFICIAL                                           |
  |  +-------------------+  +-------------------+                      |
  |  | Gemini 1.5 Flash  |  | langdetect        |                      |
  |  | Modelo de Google.  |  | Libreria que      |                      |
  |  | Genera respuestas |  | detecta el idioma  |                      |
  |  | sobre tramites    |  | del texto (es, fr, |                      |
  |  | usando KB como    |  | ar, en). Usa       |                      |
  |  | contexto. Tambien |  | keywords + stats   |                      |
  |  | transcribe audio. |  |                    |                      |
  |  +-------------------+  +-------------------+                      |
  |                                                                     |
  |  AUDIO                                                             |
  |  +-------------------+  +-------------------+                      |
  |  | gTTS              |  | pydub + ffmpeg    |                      |
  |  | Google Text-to-   |  | Convierte MP3 a   |                      |
  |  | Speech. Convierte |  | OGG Opus (formato  |                      |
  |  | texto a MP3.      |  | nativo de notas de |                      |
  |  | Gratis, soporta   |  | voz de WhatsApp).  |                      |
  |  | es/fr/en/ar.      |  | ffmpeg: ~30MB.     |                      |
  |  +-------------------+  +-------------------+                      |
  |                                                                     |
  |  INFRAESTRUCTURA                                                   |
  |  +-------------------+  +-------------------+  +-----------------+ |
  |  | Docker            |  | Render            |  | Notion MCP      | |
  |  | Empaqueta toda la |  | Hosting cloud     |  | Base de datos   | |
  |  | app en un         |  | gratis. Ejecuta   |  | del proyecto:   | |
  |  | contenedor que    |  | nuestro Docker.   |  | backlog (43),   | |
  |  | funciona igual en |  | Free tier: 512MB  |  | KB (12),        | |
  |  | cualquier maquina |  | RAM, auto-sleep   |  | testing (26).   | |
  |  +-------------------+  +-------------------+  +-----------------+ |
  +---------------------------------------------------------------------+
```

### Flujo de Datos (estilo n8n)

```
  +----------+     +----------+     +----------+     +----------+
  | WhatsApp |---->| Twilio   |---->| Flask    |---->| Pipeline |
  | (usuario)|     | (puente) |     | (webhook)|     | (11-14   |
  |          |     |          |     |          |     |  skills) |
  +----------+     +----------+     +----+-----+     +----+-----+
                                         |                 |
                                    TwiML ACK         Background
                                    (<1 seg)          Thread
                                         |                 |
                                         v                 v
                                    Usuario ve:      +-----+------+
                                    "Procesando..."  | Resultado  |
                                                     | texto+audio|
                                                     +-----+------+
                                                           |
                                    +----------+     +-----+------+
                                    | WhatsApp |<----| Twilio REST|
                                    | (usuario)|     | (envio)    |
                                    | recibe   |     |            |
                                    | respuesta|     +------------+
                                    +----------+

  DETALLE DEL PIPELINE (14 pasos):

  [1] guardrail  [2] audio?   [3] arabe?  [4] cache?  [5] demo?
   pre              |            |            |            |
   |            fetch+transcr  stub+tel    tts_ensure   fallback
   |                |            |            |            |
   v                v            v            v            v
  [6] kb_lookup  [7] llm      [8] truth   [9] struct  [10] guard
      (JSON)        generate      verify      output       post
                    (Gemini)      (labels)    (opt)        (PII)
   |                |            |            |            |
   v                v            v            v            v
  [11] simplify  [12] tts     [13] send   [14] log
       (jerga)       (OGG)        (Twilio)     (metrics)
```

---

## 6. Plan de Implementacion

### F4.1 — Foundation (Modelos, Config, Diccionarios)

**Objetivo:** Nuevos dataclasses, feature flags y diccionarios que TODAS las subfases necesitan.

**Dependencias:** Ninguna (punto de partida).

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/models_v2.py` | TrustLabel (enum: VERIFIED, ORIENTATIVE, UNVERIFIED), VerifiedResponse, SkillMetrics, ErrorContext |
| `data/dictionaries/jargon_es.json` | 50+ entradas: jerga admin -> lenguaje simple ("empadronamiento" -> "registro en tu ayuntamiento") |
| `data/dictionaries/arabic_templates.json` | 3 templates: saludo, derivacion a telefono, error |
| `tests/unit/test_models_v2.py` | 5 tests para nuevos dataclasses |
| `tests/unit/test_jargon_dict.py` | 4 tests de carga y validacion |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/config.py` | +3 flags: TRUTH_MODE(false), ARABIC_STUB_ON(true), OGG_AUDIO(true) |
| `src/core/models.py` | +3 campos en FinalResponse: trust_label, source_ref, fallback_reason |
| `src/core/prompts/templates.py` | +4 templates: ack_audio_ar, fallback_generic_ar, arabic_redirect, fallback_tts_fail |
| `tests/unit/test_config.py` | +3 tests para nuevos flags |

**Tests nuevos: 12** | Total acumulado: 108

**Exit Criteria:**
- 3 flags existen en config.py con defaults correctos
- TrustLabel enum con VERIFIED/ORIENTATIVE/UNVERIFIED
- FinalResponse tiene trust_label, source_ref, fallback_reason
- jargon_es.json >= 30 entradas, carga sin errores
- arabic_templates.json >= 3 templates
- `pytest tests/ -v` = 108 PASS
- `ruff check src/ tests/ --select E,F,W --ignore E501` = 0 errores

---

### F4.2 — Truth Mode (Verificacion, Trust Labels, KB Grounding)

**Objetivo:** Cada respuesta LLM lleva etiqueta de confianza y fuente verificable.

**Dependencias:** F4.1 (TrustLabel, TRUTH_MODE flag)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/skills/truth_verify.py` | Claim extraction, KB grounding, trust label assignment |
| `tests/unit/test_truth_verify.py` | 10 tests de verificacion |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/skills/verify_response.py` | Delegar a truth_verify cuando TRUTH_MODE=true |
| `src/core/skills/kb_lookup.py` | Retornar claims_available (lista de facts del JSON) |
| `src/core/models.py` | KBContext +claims_available (list[str]) |
| `src/core/prompts/system_prompt.py` | Instrucciones trust labels cuando TRUTH_MODE=true |
| `src/core/pipeline.py` | Usar truth_verify si TRUTH_MODE=true |

**Logica de truth_verify.py:**

```
  Input: response_text + kb_context
    |
    v
  1. Extraer claims (frases con datos: cantidades, plazos, URLs)
    |
    v
  2. Para cada claim, buscar en kb_context.datos
    |
    +-- Match en KB.verificado=true --> [VERIFICADO]
    +-- Match en KB.verificado=false --> [ORIENTATIVO]
    +-- Sin match --> [NO VERIFICADO]
    |
    v
  3. Formatear: etiqueta antes de cada claim
    |
    v
  4. Anadir "Fuente: {fuente_url}" al final
    |
    v
  5. Si >50% claims NO VERIFICADOS --> disclaimer reforzado:
     "Esta informacion es orientativa. Confirma en {url} o llama al {tel}"
```

**Tests nuevos: 10** | Total acumulado: 118

**Exit Criteria:**
- TRUTH_MODE=true: respuestas LLM llevan [VERIFICADO]/[ORIENTATIVO]
- TRUTH_MODE=false: comportamiento identico a Fase 3
- Fuente oficial SIEMPRE presente cuando hay KBContext
- `pytest tests/ -v` = 118 PASS

---

### F4.3 — Voice (TTS OGG, Dual Response Garantizado)

**Objetivo:** TODAS las respuestas incluyen audio en formato OGG nativo de WhatsApp.

**Dependencias:** F4.1 (OGG_AUDIO flag)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/skills/tts_ogg.py` | gTTS -> MP3 -> pydub -> OGG Opus, cache por hash |
| `src/core/skills/tts_ensure.py` | Garantiza audio para cache hits sin MP3 pre-existente |
| `tests/unit/test_tts_ogg.py` | 6 tests de generacion OGG |
| `tests/unit/test_dual_response.py` | 5 tests de dual response |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/skills/tts.py` | Si OGG_AUDIO=true -> delegar a tts_ogg; NUNCA retornar None |
| `src/core/pipeline.py` | Garantizar audio en TODOS los paths (cache, LLM, fallback, block) |
| `src/core/prompts/templates.py` | +fallback_tts_fail |
| `requirements.txt` | +pydub |

**Flujo de audio:**

```
  texto + idioma
    |
    v
  gTTS genera MP3
    |
    v
  OGG_AUDIO=true?
    |
    +--SI--> pydub convierte MP3 -> OGG Opus (32kbps, 48kHz, mono)
    |         |
    |         +-- OK? --> cache tts_{hash}.ogg --> URL publica
    |         +-- FALLO? --> fallback a MP3
    |
    +--NO--> cache tts_{hash}.mp3 --> URL publica

  IMPORTANTE: WhatsApp reproduce OGG Opus como nota de voz inline.
  MP3 se reproduce como archivo adjunto (peor UX).
```

**Tests nuevos: 11** | Total acumulado: 129

**Exit Criteria:**
- OGG_AUDIO=true: archivos generados son .ogg validos
- OGG_AUDIO=false: archivos son .mp3 (Fase 3 behavior)
- NUNCA se envia respuesta sin intentar generar audio
- Fallback MP3 funciona si OGG falla
- `pytest tests/ -v` = 129 PASS

---

### F4.4 — Accessibility (Arabe, Jerga, Simplificacion, Adaptive)

**Objetivo:** Respuestas cortas, sin jerga, con pregunta de seguimiento. Stub arabe funcional.

**Dependencias:** F4.1 (jargon dict, arabic templates), F4.3 (audio para arabic stub)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/skills/arabic_stub.py` | Detecta arabe -> template + telefono |
| `src/core/skills/simplify_response.py` | Reemplaza jerga, max 150 palabras, pregunta seguimiento |
| `tests/unit/test_arabic_stub.py` | 6 tests |
| `tests/unit/test_simplify_response.py` | 7 tests |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/skills/detect_lang.py` | +_AR_KEYWORDS (15+ palabras), deteccion arabe |
| `src/core/pipeline.py` | arabic_stub despues de detect_lang; simplify antes de TTS |
| `src/core/prompts/templates.py` | Templates arabe: ack, fallback, redirect |
| `src/core/prompts/system_prompt.py` | Instruccion adaptativa (follow-up) |
| `tests/unit/test_detect_lang.py` | +3 tests deteccion arabe |

**UX Adaptativa (basada en investigacion Agent A: MomConnect, UNE 153101):**

```
  Senales del usuario          Nivel de complejidad
  +------------------------+   +----------------------------+
  | Texto < 5 palabras     |   | BASICO (60 palabras max)   |
  | Sin acentos            |   | - Frases cortas            |
  | Pregunta simple        |   | - 0 jerga                  |
  | Audio (no texto)       |   | - Pasos numerados          |
  +------------------------+   +----------------------------+

  +------------------------+   +----------------------------+
  | Texto 5-15 palabras    |   | MEDIO (120 palabras max)   |
  | Algunos detalles       |   | - Jerga con explicacion    |
  | Pregunta especifica    |   | - Mas detalle              |
  +------------------------+   +----------------------------+

  +------------------------+   +----------------------------+
  | Texto > 15 palabras    |   | DETALLADO (200 palabras)   |
  | Terminos tecnicos      |   | - Respuesta completa       |
  | Referencia a articulos |   | - Links oficiales          |
  +------------------------+   +----------------------------+

  Nota: Para Fase 4, implementamos BASICO como default con
  simplify_response. Niveles MEDIO/DETALLADO son post-F4.
```

**Tests nuevos: 16** | Total acumulado: 145

**Exit Criteria:**
- detect_lang reconoce "ar" para texto arabe
- arabic_stub retorna template + telefono
- simplify_response reemplaza >= 10 terminos de jerga
- Respuestas <= 150 palabras
- Pregunta de seguimiento presente si no habia pregunta
- ARABIC_STUB_ON=false: arabe pasa al flujo LLM normal
- `pytest tests/ -v` = 145 PASS

---

### F4.5 — Observability (Latencia por Skill, Analytics, Evidence)

**Objetivo:** Cada request genera JSON con latencia por skill, razon de fallback, source chain.

**Dependencias:** F4.1 (SkillMetrics), F4.2 (trust labels en logs)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/utils/metrics_collector.py` | Collector: latencias, fallback reasons, source chain |
| `tests/unit/test_metrics_collector.py` | 5 tests |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/utils/observability.py` | +fallback_reason, +source_chain, +trust_label, +language_detected |
| `src/utils/timing.py` | Decorator registra skill name + success/fail |
| `src/utils/logger.py` | +log_skill_metrics(ctx) — emite JSON completo |
| `src/core/pipeline.py` | log_skill_metrics al final; fallback_reason en cada path |
| `src/routes/health.py` | +GET /metrics (protegido con ADMIN_TOKEN) |
| `tests/unit/test_observability.py` | +4 tests nuevos campos |

**Formato de log esperado:**

```json
{
  "tag": "OBS_FULL",
  "request_id": "abc-123",
  "language": "es",
  "input_type": "text",
  "source": "llm",
  "trust_label": "VERIFIED",
  "fallback_reason": null,
  "timings": {
    "guardrail_pre": 2,
    "detect_lang": 5,
    "cache_match": 3,
    "kb_lookup": 12,
    "llm_generate": 1200,
    "truth_verify": 8,
    "simplify": 2,
    "tts": 450,
    "send_response": 320,
    "total": 2005
  },
  "source_chain": ["cache_miss", "kb_hit:imv", "llm:gemini", "truth:verified"]
}
```

**Latency Targets:**

```
  Skill            P50        P90
  +----------------+----------+-----------+
  | guardrail_pre  | < 5ms    | < 10ms    |
  | detect_lang    | < 10ms   | < 20ms    |
  | cache_match    | < 5ms    | < 10ms    |
  | kb_lookup      | < 15ms   | < 30ms    |
  | llm_generate   | < 2000ms | < 4000ms  |
  | truth_verify   | < 10ms   | < 20ms    |
  | simplify       | < 5ms    | < 10ms    |
  | tts (OGG)      | < 1000ms | < 2000ms  |
  | send_response  | < 500ms  | < 1000ms  |
  | TOTAL          | < 4000ms | < 8000ms  |
  +----------------+----------+-----------+
```

**Tests nuevos: 9** | Total acumulado: 154

**Exit Criteria:**
- Cada request genera log JSON con latencias por skill
- fallback_reason en TODOS los paths de fallback
- source_chain traza ruta completa del pipeline
- GET /metrics funcional con ADMIN_TOKEN
- `pytest tests/ -v` = 154 PASS

---

### F4.6 — Integration + QA (Full Pipeline, 6 Demos, Evidence Pack)

**Objetivo:** Integrar todo, ejecutar 6 demos E2E, generar paquete de evidencia completo.

**Dependencias:** F4.1, F4.2, F4.3, F4.4, F4.5 (TODAS)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `tests/e2e/test_phase4_flows.py` | 6 conversaciones demo E2E |
| `tests/integration/test_pipeline_v2.py` | 6 tests integracion pipeline completo |
| `docs/07-evidence/PHASE-4-EVIDENCE.md` | Documento de evidencia |
| `docs/07-evidence/artifacts/phase4/f46-demo-conversations.txt` | Transcripciones |
| `scripts/phase4_verify.sh` | Script de verificacion automatizada |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `data/cache/demo_cache.json` | +2 entradas: saludo_ar, imv_ar |
| `src/core/pipeline.py` | Ajustes finales de integracion |
| `docs/07-evidence/PHASE-STATUS.md` | Fase 4 = verde |
| `docs/07-evidence/PHASE-CLOSE-CHECKLIST.md` | +seccion Fase 4 |

**6 Demos:**

| # | Nombre | Idioma | Input | Flujo |
|---|--------|--------|-------|-------|
| D1 | Maria IMV | es | texto | cache HIT -> texto + audio OGG |
| D2 | Ahmed empadronamiento | fr | texto | cache HIT -> texto fr + audio OGG |
| D3 | Fatima tarjeta sanitaria | es | texto | cache MISS -> LLM -> truth verify -> [VERIFICADO] + audio OGG |
| D4 | Omar saludo | ar | texto | arabic stub -> template ar + telefono + audio OGG |
| D5 | Robert audio IMV | es | audio | transcribe -> cache HIT -> texto + audio OGG |
| D6 | Error recovery | es | off-topic | guardrail/fallback -> mensaje especifico + audio OGG |

**Tests nuevos: 12** | Total acumulado: 166

**Exit Criteria:**
- 166 tests PASS
- ruff clean
- 6 demos documentadas con input/output
- Cada demo: texto + audio
- PHASE-4-EVIDENCE.md completo
- PHASE-STATUS.md con Fase 4 = verde
- Docker build exitoso
- Latencia promedio demos < 8s

---

### Resumen de Esfuerzo

```
  SUBFASE          TESTS    CREAR    MODIFICAR    DEPENDENCIAS
  +----------------+--------+--------+-----------+------------------+
  | F4.1 Foundation|    12  |    5   |     4     | (ninguna)        |
  | F4.2 Truth     |    10  |    2   |     5     | F4.1             |
  | F4.3 Voice     |    11  |    4   |     4     | F4.1             |
  | F4.4 Access    |    16  |    4   |     5     | F4.1, F4.3       |
  | F4.5 Observ    |     9  |    2   |     6     | F4.1, F4.2       |
  | F4.6 Integr    |    12  |    5   |     4     | TODAS            |
  +----------------+--------+--------+-----------+------------------+
  | TOTAL          |    70  |   22   |    28     |                  |
  +----------------+--------+--------+-----------+------------------+

  Tests: 96 (Fase 3) + 70 (Fase 4) = 166 total
```

### Diagrama de Dependencias

```
                    F4.1 Foundation
                         |
              +----------+----------+
              |          |          |
              v          v          v
           F4.2       F4.3       F4.4
           Truth      Voice      Access
              |          |          |
              +----------+          |
              |                     |
              v                     |
           F4.5 Observability <-----+
              |
              v
           F4.6 Integration + QA

  Orden recomendado:
  1. F4.1 (bloquea todo)
  2. F4.2 + F4.3 + F4.4 (PARALELAS entre 3 developers)
  3. F4.5 (necesita F4.1 + F4.2)
  4. F4.6 (necesita todo)
```

### Gate Criteria

| Gate | Post | Tests | Criterio clave |
|------|------|:-----:|----------------|
| G4.0 | F4.1 | >= 108 | 12 flags, jargon >= 30, arabic >= 3 |
| G4.1 | F4.2 | >= 118 | Trust labels en 100% respuestas LLM |
| G4.2 | F4.3 | >= 129 | Audio en >= 95% respuestas, OGG validos |
| G4.3 | F4.4 | >= 145 | detect_lang("ar"), <= 150 palabras |
| G4.4 | F4.5 | >= 154 | JSON metrics, fallback_reason, /metrics |
| G4.5 | F4.6 | >= 166 | 6 demos, evidence pack, Docker OK |

---

## 7. Top 10 Riesgos

| # | Riesgo | Prob. | Impacto | Mitigacion |
|---|--------|:-----:|:-------:|------------|
| R1 | **gTTS no genera OGG** — solo MP3 | Alta | Alto | gTTS->MP3 + pydub->OGG como pipeline. Si pydub falla: fallback MP3. Flag OGG_AUDIO para rollback. |
| R2 | **pydub requiere ffmpeg** en Docker | Alta | Alto | `apt-get install -y ffmpeg` en Dockerfile (~30MB). Si RAM excede: OGG_AUDIO=false. |
| R3 | **RAM > 512MB** en Render free tier | Media | Alto | Monitorear `docker stats`. Sin Whisper local, baseline ~200MB + ffmpeg ~30MB + pydub ~10MB = ~240MB. Margen: 270MB. |
| R4 | **Trust labels confunden** al usuario | Media | Medio | Usar lenguaje simple: "Dato oficial" vs "Info orientativa". Probar con 2 personas antes de demo. |
| R5 | **Deteccion arabe falla** con texto corto/mixto | Media | Medio | 15+ keywords arabes. langdetect como backup. Si ambiguo: preguntar idioma. |
| R6 | **Jargon dict incompleto** | Baja | Bajo | 30-50 terminos iniciales. JSON ampliable. No bloquea si falta termino. |
| R7 | **Regresion en 96 tests** al modificar pipeline.py | Media | Alto | `pytest tests/ -v` despues de CADA cambio. No mergear sin 100% green. Flag-guard todo. |
| R8 | **Latencia > 8s** con TTS OGG | Media | Medio | gTTS + pydub < 2s para textos < 200 palabras. Cache OGG evita regeneracion. |
| R9 | **Templates arabe incorrectos** | Alta | Medio | Traducciones de ACNUR/Cruz Roja. Solo 3-4 templates basicos. Marcar como "stub". |
| R10 | **Conflictos de merge** en paralelo | Media | Medio | Archivos distintos por subfase (excepto pipeline.py y config.py). Pipeline se modifica secuencialmente. |

---

## 8. Conversaciones de Ejemplo

### D1: Maria — IMV en espanol (persona mayor, texto corto)

```
  MARIA (es, mayor, baja alfabetizacion):
  > "hola necesito ayuda con el imv"

  CLARA responde (cache HIT, ~2s):
  +------------------------------------------------------------------+
  | Hola Maria! El Ingreso Minimo Vital (IMV) es una ayuda           |
  | economica del gobierno para personas con pocos ingresos.          |
  |                                                                   |
  | Para pedirlo necesitas:                                           |
  | 1. Tu DNI o NIE                                                  |
  | 2. Estar registrada en tu ayuntamiento (empadronamiento)         |
  | 3. Tener ingresos por debajo del limite                          |
  |                                                                   |
  | [VERIFICADO] Puedes solicitarlo en la Seguridad Social           |
  | o llamando al 900 20 22 22 (gratuito).                           |
  |                                                                   |
  | Fuente: https://www.seg-social.es/imv                            |
  |                                                                   |
  | Tienes alguna otra duda sobre este tramite?                      |
  +------------------------------------------------------------------+
  + AUDIO: nota de voz OGG (se reproduce inline en WhatsApp)
```

### D2: Ahmed — Empadronamiento en frances (inmigrante)

```
  AHMED (fr, inmigrante reciente):
  > "bonjour comment faire l'empadronamiento"

  CLARA responde (cache HIT, ~2s):
  +------------------------------------------------------------------+
  | Bonjour Ahmed! L'empadronamiento c'est l'inscription au          |
  | registre de votre ville. C'est obligatoire pour vivre en         |
  | Espagne.                                                         |
  |                                                                   |
  | Pour le faire:                                                   |
  | 1. Allez a votre mairie (ayuntamiento)                           |
  | 2. Apportez votre passeport et contrat de logement               |
  | 3. Remplissez le formulaire sur place                            |
  |                                                                   |
  | [VERIFICADO] Appelez le 010 pour prendre rendez-vous.            |
  |                                                                   |
  | Source: https://sede.madrid.es/padron                            |
  |                                                                   |
  | Avez-vous d'autres questions sur cette demarche?                 |
  +------------------------------------------------------------------+
  + AUDIO: nota de voz OGG en frances
```

### D3: Fatima — Tarjeta sanitaria (cache MISS -> LLM -> Truth)

```
  FATIMA (es, inmigrante):
  > "como saco la tarjeta sanitaria para mi hijo que nacio aqui"

  CLARA responde (LLM + truth verify, ~6s):
  +------------------------------------------------------------------+
  | Hola! Para sacar la tarjeta sanitaria de tu hijo nacido          |
  | en Espana:                                                       |
  |                                                                   |
  | [VERIFICADO] 1. Ve a tu centro de salud mas cercano              |
  | [VERIFICADO] 2. Lleva el certificado de nacimiento y tu          |
  |    tarjeta sanitaria                                             |
  | [VERIFICADO] 3. Rellena el formulario de alta                    |
  | [ORIENTATIVO] El proceso tarda entre 1-2 semanas                 |
  |                                                                   |
  | Fuente: https://www.comunidad.madrid/salud                       |
  | Telefono: 900 102 112 (gratuito)                                 |
  |                                                                   |
  | Tienes alguna otra duda sobre este tramite?                      |
  +------------------------------------------------------------------+
  + AUDIO: nota de voz OGG
```

### D4: Omar — Saludo en arabe (arabic stub)

```
  OMAR (ar, inmigrante):
  > "مرحبا أحتاج مساعدة"

  CLARA responde (arabic stub, ~2s):
  +------------------------------------------------------------------+
  | مرحبًا! شكرًا لتواصلك مع كلارا.                                  |
  |                                                                   |
  | حاليًا، خدمتنا متاحة بالإسبانية والفرنسية.                        |
  | للمساعدة بالعربية، يمكنك الاتصال بـ:                              |
  |                                                                   |
  | - معلومات عامة: 012                                               |
  | - مساعدة اجتماعية: 900 918 784                                    |
  | - الصليب الأحمر: 900 22 22 92                                     |
  |                                                                   |
  | Hola! Gracias por contactar con Clara.                            |
  | Nuestro servicio esta disponible en espanol y frances.            |
  | Para ayuda en arabe, puedes llamar a los telefonos de arriba.    |
  +------------------------------------------------------------------+
  + AUDIO: nota de voz OGG (bilingue ar+es)
```

### D5: Robert — Audio IMV (pipeline audio completo)

```
  ROBERT (es, envia audio):
  > [Audio: "oye quiero saber que papeles necesito para el imv"]

  CLARA procesa:
  1. fetch_media: descarga audio de Twilio
  2. transcribe: Gemini Flash -> "quiero saber que papeles necesito para el imv"
  3. detect_lang: "es"
  4. cache_match: HIT (imv_es)
  5. tts_ensure: genera OGG si no existe

  CLARA responde (~3s):
  +------------------------------------------------------------------+
  | Para el Ingreso Minimo Vital necesitas estos papeles:            |
  |                                                                   |
  | [VERIFICADO] 1. DNI o NIE en vigor                               |
  | [VERIFICADO] 2. Certificado de empadronamiento                   |
  | [VERIFICADO] 3. Libro de familia o certificado de convivencia    |
  | [VERIFICADO] 4. Declaracion de la renta (o certificado AEAT)     |
  |                                                                   |
  | Puedes presentarlo online en sede.seg-social.es o en             |
  | oficina con cita previa: 900 20 22 22                            |
  |                                                                   |
  | Fuente: https://www.seg-social.es/imv                            |
  |                                                                   |
  | Tienes alguna otra duda sobre este tramite?                      |
  +------------------------------------------------------------------+
  + AUDIO: nota de voz OGG
```

### D6: Error Recovery (off-topic -> guardrail)

```
  USUARIO (es):
  > "que tiempo va a hacer manana en madrid"

  CLARA responde (guardrail, ~1s):
  +------------------------------------------------------------------+
  | Ahora mismo puedo ayudarte con:                                  |
  |                                                                   |
  | - Ingreso Minimo Vital (IMV)                                     |
  | - Empadronamiento (registro en tu ayuntamiento)                  |
  | - Tarjeta Sanitaria                                              |
  |                                                                   |
  | Sobre que te gustaria saber?                                     |
  +------------------------------------------------------------------+
  + AUDIO: nota de voz OGG
```

---

## 9. Como Verificar

### Comandos de Verificacion

```bash
# --- TESTS ---
# Correr todos los tests (esperar 166 PASS en Fase 4 completa)
pytest tests/ -v --tb=short

# Solo tests de Fase 4
pytest tests/unit/test_models_v2.py tests/unit/test_truth_verify.py \
       tests/unit/test_tts_ogg.py tests/unit/test_arabic_stub.py \
       tests/unit/test_simplify_response.py tests/unit/test_metrics_collector.py \
       tests/e2e/test_phase4_flows.py -v

# --- LINT ---
ruff check src/ tests/ --select E,F,W --ignore E501

# --- LOCAL ---
# Arrancar app local
python src/app.py
# o
bash scripts/run-local.sh

# --- HEALTH ---
curl http://localhost:5000/health | python3 -m json.tool

# --- METRICS (Fase 4) ---
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:5000/metrics

# --- DOCKER ---
docker build -t civicaid-voice:f4 .
docker run -p 5000:5000 --env-file .env civicaid-voice:f4

# --- VERIFICACION AUTOMATIZADA (Fase 4) ---
bash scripts/phase4_verify.sh
```

### Checklist Manual

```
  [ ] pytest tests/ -v = 166 PASS (0 FAIL)
  [ ] ruff check = 0 errores
  [ ] python src/app.py arranca sin errores
  [ ] curl /health retorna status: healthy
  [ ] docker build exitoso
  [ ] docker run + curl /health = healthy
  [ ] Enviar "hola imv" por WhatsApp -> recibe texto + audio
  [ ] Enviar audio por WhatsApp -> recibe transcripcion + respuesta + audio
  [ ] Enviar texto en arabe -> recibe template + telefonos
  [ ] Respuesta contiene [VERIFICADO] o [ORIENTATIVO]
  [ ] Audio es OGG Opus (nota de voz inline)
  [ ] Respuesta <= 150 palabras
  [ ] Respuesta incluye pregunta de seguimiento
  [ ] Logs contienen JSON con latencias por skill
```

---

## 10. Notion Dashboard

### Entries Nuevas

| DB | Nuevas | Total |
|----|:------:|:-----:|
| Backlog | +8 | 51 |
| KB Tramites | +1 | 13 |
| Testing | +12 | 38 |
| **Total** | **+21** | **102** |

### Propiedades Nuevas (para agregar manualmente)

**Backlog DB** (+5 propiedades):
- Fase (Select: F0-Plan / F1-MVP / F2-Hardening / F3-Demo / F4-Polish)
- Fecha cierre (Date)
- Commit SHA (Rich Text)
- Esfuerzo real (Number)
- Etiquetas (Multi-select: bug/feature/docs/refactor/test/ops)

**KB Tramites DB** (+4 propiedades):
- Idioma (Select: es/fr/ar)
- Version (Number)
- Autor verificacion (Select: equipo)
- Confianza (Select: Alta/Media/Baja)

**Demo & Testing DB** (+5 propiedades):
- Fase (Select: F1/F2/F3/F4)
- Ejecutado por (Select: equipo + CI/CD)
- Entorno (Select: Local/Docker/Render/CI)
- Archivo test (Rich Text)
- Evidence link (URL)

### Vistas Recomendadas (manuales en Notion UI)

- **Board por Fase**: Kanban agrupado por F0/F1/F2/F3/F4
- **Timeline**: Vista calendario por fecha de cierre
- **Tareas bloqueadas**: Filtro donde blockedBy no esta vacio
- **Tests por entorno**: Agrupado por Local/Docker/Render

> **Nota:** Las vistas de Notion NO se pueden crear por API. Se configuran manualmente en la interfaz.

---

## Apendice: Evidence Files Required

```
docs/07-evidence/
  PHASE-4-EVIDENCE.md
  artifacts/phase4/
    f41-models-screenshot.txt
    f41-config-diff.txt
    f42-truth-mode-example.txt
    f42-test-results.txt
    f43-ogg-sample.ogg
    f43-dual-response-proof.txt
    f44-arabic-example.txt
    f44-simplify-before-after.txt
    f45-metrics-sample.json
    f45-latency-targets.txt
    f46-demo-conversations.txt
    f46-test-results.txt
    f46-metrics-full.json
    f46-lint-clean.txt
```

---

## Apendice: Decisiones de los 6 Agentes

| Agente | Rol | Propuestas | Seleccion | Razon |
|--------|-----|------------|-----------|-------|
| A | Product-UX | Lectura Facil Total / **Clara Adaptativa** / Clara Menu-First | B: Clara Adaptativa | 3 niveles complejidad (60/120/200 palabras) auto-detectados. Basado en MomConnect + UNE 153101 |
| B | Voice-TTS | **Piper TTS Local** / Pre-gen + on-demand / Hybrid | Ajustado: gTTS + pydub -> OGG | Piper necesita ~500MB RAM (excede Render). gTTS+pydub = ~10MB extra, misma calidad |
| C | Truth-KB | Rules-Only / **LLM-as-Judge + Allowlist** / KB-Template-Only | B: LLM-as-Judge | Claim grounding + trust labels + URL/phone allowlists. Basado en RAGAS + GOV.UK Chat |
| D | QA Engineer | Coverage-First (90) / **Risk-First (65)** / Eval-Driven (55+40) | B: Risk-First 65 tests | Targets: golden truthfulness (10), red-team (15), audio format (5), latency (5), arabic (5) |
| E | Obs-Perf | **Zero-Dep Metrics** / Structlog + File / OTel-Lite | A: Zero-Dep | collections.deque + statistics.quantiles(). ~50KB RAM, zero dependencias nuevas |
| F | PM-Arch | **Incremental** / Pipeline v2 / Event-Driven | A: Incremental | Minimo riesgo, 5 archivos nuevos, 3 flags, familiar para equipo, apropiado para hackathon |

### Nota sobre TTS

Agent B recomendo Piper TTS Local (~270MB peak, MIT, ES/FR/AR nativo). Sin embargo, analisis previo identifico que Piper necesita ~500MB runtime, lo cual excede el margen de Render free tier (512MB total). **Decision: usar gTTS + pydub -> OGG Opus** como estrategia principal:

- gTTS: genera MP3 (gratis, soporta es/fr/en/ar, ~0 RAM extra)
- pydub + ffmpeg: convierte MP3 -> OGG Opus 32kbps mono (~30MB por ffmpeg)
- Total RAM extra: ~40MB (vs ~500MB de Piper)
- Piper queda como upgrade futuro post-hackathon cuando se migre a tier pago

---

*Documento generado: 2026-02-13 | Hackathon OdiseIA4Good — UDIT*
*Basado en investigacion de 6 agentes especializados (Product-UX, Voice-TTS, Truth-KB, QA Engineer, Obs-Perf, PM-Arch)*
*Arquitectura A (Incremental) aprobada. 70 tests nuevos. 166 total. 6 subfases. 6 gates.*
