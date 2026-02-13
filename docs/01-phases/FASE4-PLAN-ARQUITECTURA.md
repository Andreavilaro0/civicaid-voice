# FASE 4 — Plan de Arquitectura e Implementacion

**Proyecto:** CivicAid Voice / Clara
**Autor:** Agent F (PM-Architect Lead)
**Fecha:** 2026-02-13
**Estado:** PROPUESTA — Pendiente aprobacion del equipo

---

## Indice

1. [Estado Actual (Baseline)](#1-estado-actual-baseline)
2. [Objetivos Fase 4](#2-objetivos-fase-4)
3. [Arquitectura A: Incremental (Evolucion in-place)](#3-arquitectura-a-incremental)
4. [Arquitectura B: Pipeline v2 (Rewrite parcial)](#4-arquitectura-b-pipeline-v2)
5. [Arquitectura C: Event-Driven (Desacoplado)](#5-arquitectura-c-event-driven)
6. [Comparativa y Recomendacion](#6-comparativa-y-recomendacion)
7. [Plan de Implementacion F4.1-F4.6](#7-plan-de-implementacion)
8. [Top 10 Riesgos](#8-top-10-riesgos)
9. [Gate Criteria Fase 4](#9-gate-criteria)

---

## 1. Estado Actual (Baseline)

### Pipeline Actual (Fase 3)

```
  +--------------------+
  | Usuario WhatsApp   |
  +--------+-----------+
           |
           v
  +--------+-----------+
  | Twilio POST        |
  +--------+-----------+
           |
           v
  +--------+-----------+     +------------------+
  | Flask /webhook     +---->| TwiML ACK (<1s)  |---> HTTP 200 al usuario
  +--------+-----------+     +------------------+
           |
           | threading.Thread(daemon=True)
           v
  +--------+-------------------------------------------+
  |              pipeline.process(msg)                  |
  |                                                     |
  |  [1] guardrail_pre -----> BLOCKED? --> send + EXIT  |
  |         |                                           |
  |  [2] input_type == AUDIO?                           |
  |         |--YES--> fetch_media --> transcribe         |
  |         |                  (Gemini Flash)            |
  |         |--NO---> detect_lang (langdetect)          |
  |         |                                           |
  |  [3] cache_match -----> HIT? --> send + EXIT        |
  |         |                                           |
  |  [4] DEMO_MODE? -----> YES --> fallback + EXIT      |
  |         |                                           |
  |  [5] kb_lookup (JSON)                               |
  |         |                                           |
  |  [6] llm_generate (Gemini Flash)                    |
  |         |                                           |
  |  [7] verify_response (rules-based)                  |
  |         |                                           |
  |  [8] structured_output? (optional parse)            |
  |         |                                           |
  |  [9] guardrail_post (PII + disclaimer)              |
  |         |                                           |
  | [10] tts (gTTS -> MP3) --- puede fallar silencioso  |
  |         |                                           |
  | [11] send_response (Twilio REST + retry)            |
  +-----------------------------------------------------+
```

### Metricas Baseline

| Metrica | Valor |
|---------|-------|
| Skills | 11 (detect_input, fetch_media, convert_audio, transcribe, detect_lang, cache_match, kb_lookup, llm_generate, verify_response, tts, send_response) |
| Feature Flags | 9 (DEMO_MODE, LLM_LIVE, WHISPER_ON, LLM_TIMEOUT, WHISPER_TIMEOUT, GUARDRAILS_ON, STRUCTURED_OUTPUT_ON, OBSERVABILITY_ON, RAG_ENABLED) |
| Dataclasses | 8 (IncomingMessage, AckResponse, TranscriptResult, CacheEntry, CacheResult, KBContext, LLMResponse, FinalResponse) |
| Tests | 96 |
| Tramites KB | 3 (IMV, empadronamiento, tarjeta_sanitaria) |
| Idiomas | 2 (es, fr) |
| Cache entries | 8 |
| Audio format | MP3 (gTTS) |
| RAM Render | ~200MB (sin Whisper local) |

### Problemas Identificados

1. **Audio no garantizado**: TTS puede fallar silenciosamente, cache entries sin audio (saludos)
2. **Verificacion debil**: `verify_response` solo anade URL y limita palabras, no valida claims
3. **Sin arabe**: detect_lang no lo contempla, templates no lo tienen
4. **Errores genericos**: fallback_generic y llm_fail son los unicos mensajes de error
5. **Sin metricas por skill**: observability existe pero no emite latencias individuales de forma analizable
6. **Formato MP3**: WhatsApp prefiere OGG para notas de voz nativas
7. **Sin trust labels**: usuario no sabe si la info viene de KB verificada o de LLM

---

## 2. Objetivos Fase 4

| # | Objetivo | Criterio de Exito |
|---|----------|-------------------|
| O1 | Respuesta dual (texto + audio SIEMPRE) | 100% de respuestas incluyen media_url no-null |
| O2 | Truth Mode | Cada claim lleva etiqueta [VERIFICADO]/[ORIENTATIVO] + fuente |
| O3 | Arabic stub | detect_lang reconoce arabe, responde con template + telefono |
| O4 | UX accesible | Respuestas <150 palabras, sin jerga, con pregunta de seguimiento |
| O5 | Audio OGG | Formato nativo WhatsApp, fallback a MP3 |
| O6 | Error recovery mejorado | Mensajes de error especificos por tipo de fallo |
| O7 | Observabilidad avanzada | Latencia por skill en JSON, fallback_reason, source tracking |
| O8 | LOCAL first | Todo funciona con `python src/app.py`, sin dependencias externas obligatorias |

---

## 3. Arquitectura A: Incremental

**Filosofia:** Modificar los archivos existentes, anadir skills nuevos, no tocar la estructura del pipeline.

### Diagrama

```
  +--------------------+
  | Usuario WhatsApp   |
  +--------+-----------+
           |
           v
  +--------+-----------+
  | Twilio POST        |
  +--------+-----------+
           |
           v
  +--------+-----------+     +------------------+
  | Flask /webhook     +---->| TwiML ACK (<1s)  |---> HTTP 200
  +--------+-----------+     +------------------+
           |
           | threading.Thread(daemon=True)
           v
  +--------+-------------------------------------------+
  |              pipeline.process(msg)                  |
  |                                                     |
  |  [1] guardrail_pre -----> BLOCKED? --> send + EXIT  |
  |         |                                           |
  |  [2] input_type == AUDIO?                           |
  |         |--YES--> fetch_media --> transcribe         |
  |         |--NO---> detect_lang  <-- MODIFICADO:      |
  |         |             ahora detecta ar/es/fr        |
  |         |                                           |
  |  [3] lang == "ar"? --> arabic_stub --> send + EXIT   |
  |         |                   NUEVO SKILL             |
  |  [4] cache_match -----> HIT? --> tts_ensure -->     |
  |         |                        send + EXIT        |
  |         |                                           |
  |  [5] DEMO_MODE? --> fallback + EXIT                 |
  |         |                                           |
  |  [6] kb_lookup (JSON)                               |
  |         |                                           |
  |  [7] llm_generate (Gemini)                          |
  |         |                                           |
  |  [8] verify_response_v2  <-- MODIFICADO:            |
  |         |   trust_labels, claim grounding,          |
  |         |   fuente obligatoria                      |
  |         |                                           |
  |  [9] structured_output? (opcional)                  |
  |         |                                           |
  | [10] guardrail_post                                 |
  |         |                                           |
  | [11] simplify_response  <-- NUEVO SKILL             |
  |         |   (jargon dict, word limit, follow-up Q)  |
  |         |                                           |
  | [12] tts_ogg  <-- MODIFICADO: OGG primary,          |
  |         |         MP3 fallback, NUNCA None           |
  |         |                                           |
  | [13] send_response (sin cambios)                    |
  +-----------------------------------------------------+
```

### Especificaciones

| Aspecto | Detalle |
|---------|---------|
| Skills totales | 14 (11 existentes + arabic_stub, simplify_response, tts_ensure) |
| Flags nuevos | 3 (TRUTH_MODE, ARABIC_STUB_ON, OGG_AUDIO) |
| Flags totales | 12 |
| Dataclasses nuevos | 3 (TrustLabel, VerifiedResponse, SkillMetrics) |
| Dataclasses totales | 11 |
| RAM estimado | ~220MB (+20MB por pyttsx3/OGG libs) |
| Archivos a CREAR | 5 |
| Archivos a MODIFICAR | 9 |

### Archivos

**Crear:**
- `src/core/skills/arabic_stub.py` — Template response para arabe
- `src/core/skills/simplify_response.py` — Jargon dict + readability
- `src/core/skills/tts_ensure.py` — Garantiza audio para cache hits sin MP3
- `src/core/models_v2.py` — TrustLabel, VerifiedResponse, SkillMetrics
- `data/dictionaries/jargon_es.json` — Diccionario jerga -> lenguaje simple

**Modificar:**
- `src/core/config.py` — +3 flags
- `src/core/models.py` — Ampliar FinalResponse con trust_label, source_ref
- `src/core/pipeline.py` — Insertar arabic_stub, simplify, tts_ensure
- `src/core/skills/detect_lang.py` — Anadir deteccion arabe
- `src/core/skills/verify_response.py` — Truth mode, trust labels
- `src/core/skills/tts.py` — OGG primary, MP3 fallback, never-null
- `src/core/prompts/templates.py` — +templates ar, +fallback especificos
- `src/core/prompts/system_prompt.py` — Instrucciones trust labels
- `src/utils/observability.py` — SkillMetrics collection

### Ventajas / Desventajas

| Ventajas | Desventajas |
|----------|-------------|
| Minimo riesgo de regresion | pipeline.py crece a >250 lineas |
| Sin cambios estructurales | Dificil testear skills aislados |
| Familiar para el equipo | Logica condicional anidada compleja |
| Deploy identico | Dificil anadir mas idiomas en futuro |
| Reutiliza toda la infra | verify_response_v2 mezclado con v1 |

**Nivel de riesgo: BAJO**

---

## 4. Arquitectura B: Pipeline v2 (Rewrite parcial)

**Filosofia:** Extraer la logica de pipeline.py a un orquestador basado en steps, donde cada step es un callable registrado. Mantener skills existentes pero envolverlos en una interfaz uniforme.

### Diagrama

```
  +--------------------+
  | Usuario WhatsApp   |
  +--------+-----------+
           |
           v
  +--------+-----------+
  | Twilio POST        |
  +--------+-----------+
           |
           v
  +--------+-----------+     +------------------+
  | Flask /webhook     +---->| TwiML ACK (<1s)  |---> HTTP 200
  +--------+-----------+     +------------------+
           |
           | threading.Thread(daemon=True)
           v
  +--------+-------------------------------------------+
  |         PipelineV2.run(msg)                         |
  |                                                     |
  |  +-----------------------------------------------+  |
  |  | PipelineContext                                |  |
  |  |   .msg: IncomingMessage                       |  |
  |  |   .text: str                                  |  |
  |  |   .language: str                              |  |
  |  |   .kb: KBContext | None                       |  |
  |  |   .trust: TrustLabel                          |  |
  |  |   .response_text: str                         |  |
  |  |   .audio_url: str | None                      |  |
  |  |   .metrics: SkillMetrics                      |  |
  |  |   .should_stop: bool                          |  |
  |  |   .stop_reason: str                           |  |
  |  +-----------------------------------------------+  |
  |                                                     |
  |  STEPS (lista ordenada, cada uno recibe Context):   |
  |                                                     |
  |  [S1] GuardrailPreStep                              |
  |    |-- si unsafe: ctx.should_stop = True            |
  |    v                                                |
  |  [S2] AudioPipelineStep                             |
  |    |-- si AUDIO: fetch + transcribe                 |
  |    v                                                |
  |  [S3] DetectLangStep                                |
  |    |-- detecta es/fr/ar/en                          |
  |    v                                                |
  |  [S4] ArabicStubStep                                |
  |    |-- si ar: template + ctx.should_stop            |
  |    v                                                |
  |  [S5] CacheMatchStep                                |
  |    |-- si HIT: ctx.response_text = cached           |
  |    |-- ctx.should_stop = True                       |
  |    v                                                |
  |  [S6] DemoModeStep                                  |
  |    |-- si DEMO_MODE: fallback + stop                |
  |    v                                                |
  |  [S7] KBLookupStep                                  |
  |    |-- ctx.kb = resultado                           |
  |    v                                                |
  |  [S8] LLMGenerateStep                               |
  |    |-- ctx.response_text = llm_output               |
  |    v                                                |
  |  [S9] TruthVerifyStep                               |
  |    |-- grounding check, trust labels, sources       |
  |    v                                                |
  |  [S10] GuardrailPostStep                            |
  |    |-- PII redaction, disclaimer                    |
  |    v                                                |
  |  [S11] SimplifyStep                                 |
  |    |-- jargon replace, word limit, follow-up Q      |
  |    v                                                |
  |  [S12] TTSStep                                      |
  |    |-- OGG primary, MP3 fallback, never None        |
  |    v                                                |
  |  [S13] SendResponseStep                             |
  |    |-- Twilio REST + retry                          |
  +-----------------------------------------------------+
```

### Interfaz Step

```python
class PipelineStep:
    name: str
    def execute(self, ctx: PipelineContext) -> PipelineContext:
        """Modifica ctx y retorna. Si ctx.should_stop, pipeline salta a SendStep."""
        ...
```

### Especificaciones

| Aspecto | Detalle |
|---------|---------|
| Skills totales | 13 steps (cada step envuelve 1+ skills) |
| Flags nuevos | 4 (TRUTH_MODE, ARABIC_STUB_ON, OGG_AUDIO, PIPELINE_V2) |
| Flags totales | 13 |
| Dataclasses nuevos | 4 (PipelineContext, PipelineStep, TrustLabel, VerifiedResponse) |
| Dataclasses totales | 12 |
| RAM estimado | ~225MB (+25MB) |
| Archivos a CREAR | 8 |
| Archivos a MODIFICAR | 8 |

### Archivos

**Crear:**
- `src/core/pipeline_v2.py` — Orquestador basado en steps
- `src/core/steps/` — Directorio con 13 step classes
- `src/core/steps/__init__.py`
- `src/core/steps/guardrail_pre.py`
- `src/core/steps/audio_pipeline.py`
- `src/core/steps/detect_lang.py`
- `src/core/steps/arabic_stub.py`
- `src/core/steps/cache_match.py`
- `src/core/steps/demo_mode.py`
- `src/core/steps/kb_lookup.py`
- `src/core/steps/llm_generate.py`
- `src/core/steps/truth_verify.py`
- `src/core/steps/guardrail_post.py`
- `src/core/steps/simplify.py`
- `src/core/steps/tts.py`
- `src/core/steps/send_response.py`
- `src/core/models_v2.py` — PipelineContext, TrustLabel, etc.
- `data/dictionaries/jargon_es.json`

**Modificar:**
- `src/core/config.py` — +4 flags
- `src/core/pipeline.py` — Redirigir a pipeline_v2 si PIPELINE_V2=true
- `src/core/skills/detect_lang.py` — +arabe
- `src/core/skills/tts.py` — OGG + never-null
- `src/core/skills/verify_response.py` — Trust mode
- `src/core/prompts/templates.py` — +ar, +fallback especificos
- `src/core/prompts/system_prompt.py` — Trust labels
- `src/utils/observability.py` — Step-level metrics

### Ventajas / Desventajas

| Ventajas | Desventajas |
|----------|-------------|
| Cada step testeable aislado | Mas archivos nuevos (~16) |
| PipelineContext unificado | Requiere migrar tests de pipeline |
| Facil anadir/quitar steps | Feature flag PIPELINE_V2 para rollback |
| Metrics automaticas por step | Curva de aprendizaje para equipo |
| Patrones claros para futuro | Doble codigo durante transicion |
| should_stop elimina returns anidados | Mas abstracciones |

**Nivel de riesgo: MEDIO**

---

## 5. Arquitectura C: Event-Driven (Desacoplado)

**Filosofia:** Cada skill es un handler que se suscribe a eventos. Un event bus envia mensajes entre skills. Pipeline = cadena de eventos.

### Diagrama

```
  +--------------------+
  | Usuario WhatsApp   |
  +--------+-----------+
           |
           v
  +--------+-----------+
  | Twilio POST        |
  +--------+-----------+
           |
           v
  +--------+-----------+     +------------------+
  | Flask /webhook     +---->| TwiML ACK (<1s)  |---> HTTP 200
  +--------+-----------+     +------------------+
           |
           | threading.Thread(daemon=True)
           v
  +--------+-------------------------------------------+
  |              EventBus.dispatch(MessageReceived)      |
  |                                                     |
  |  EventBus (in-memory, sync, ordered)                |
  |                                                     |
  |  MessageReceived                                    |
  |    --> GuardrailPreHandler                          |
  |        emit(InputValidated) o emit(Blocked)         |
  |                                                     |
  |  InputValidated                                     |
  |    --> AudioHandler (si audio)                      |
  |        emit(TextReady)                              |
  |    --> TextPassthrough (si texto)                   |
  |        emit(TextReady)                              |
  |                                                     |
  |  TextReady                                          |
  |    --> LangDetector                                 |
  |        emit(LangDetected{lang})                     |
  |                                                     |
  |  LangDetected{lang="ar"}                            |
  |    --> ArabicStubHandler                            |
  |        emit(ResponseReady)                          |
  |                                                     |
  |  LangDetected{lang="es"|"fr"}                       |
  |    --> CacheHandler                                 |
  |        HIT:  emit(ResponseReady)                    |
  |        MISS: emit(CacheMiss)                        |
  |                                                     |
  |  CacheMiss                                          |
  |    --> KBHandler --> LLMHandler --> VerifyHandler    |
  |        emit(ResponseDraft)                          |
  |                                                     |
  |  ResponseDraft                                      |
  |    --> GuardrailPostHandler --> SimplifyHandler      |
  |        emit(ResponseReady)                          |
  |                                                     |
  |  ResponseReady                                      |
  |    --> TTSHandler                                   |
  |        emit(AudioReady)                             |
  |                                                     |
  |  AudioReady                                         |
  |    --> SendHandler (Twilio REST)                    |
  |        emit(MessageSent)                            |
  |                                                     |
  |  Blocked                                            |
  |    --> BlockedSendHandler                           |
  |        emit(MessageSent)                            |
  +-----------------------------------------------------+
```

### Especificaciones

| Aspecto | Detalle |
|---------|---------|
| Handlers | 12 event handlers |
| Event types | 9 (MessageReceived, InputValidated, Blocked, TextReady, LangDetected, CacheMiss, ResponseDraft, ResponseReady, AudioReady, MessageSent) |
| Flags nuevos | 5 (TRUTH_MODE, ARABIC_STUB_ON, OGG_AUDIO, EVENT_BUS, EVENT_LOG) |
| Flags totales | 14 |
| Dataclasses nuevos | 12+ (todos los Event types + context) |
| RAM estimado | ~240MB (+40MB por overhead de eventos) |
| Archivos a CREAR | 15+ |
| Archivos a MODIFICAR | 8 |

### Archivos

**Crear:**
- `src/core/events/bus.py` — EventBus in-memory
- `src/core/events/types.py` — 9+ event dataclasses
- `src/core/events/__init__.py`
- `src/core/handlers/` — 12 handler files
- `src/core/pipeline_events.py` — Registrar handlers

**Modificar:** (los mismos que B, mas bus integration)

### Ventajas / Desventajas

| Ventajas | Desventajas |
|----------|-------------|
| Maximo desacoplamiento | Sobreingenieria para un chatbot |
| Cada handler 100% aislado | Debug complejo (flujo no lineal) |
| Facil anadir comportamiento | 15+ archivos nuevos |
| Event log gratis | RAM overhead innecesario |
| Patron profesional | Equipo no tiene experiencia en event-driven |
| Replay posible | Latencia adicional por dispatch |

**Nivel de riesgo: ALTO**

---

## 6. Comparativa y Recomendacion

### Tabla Comparativa

| Criterio | A (Incremental) | B (Pipeline v2) | C (Event-Driven) |
|----------|:---:|:---:|:---:|
| Archivos nuevos | 5 | ~16 | ~20 |
| Archivos modificados | 9 | 8 | 8 |
| Skills/Steps | 14 | 13 | 12 handlers |
| Flags nuevos | 3 | 4 | 5 |
| Dataclasses nuevos | 3 | 4 | 12+ |
| RAM extra | +20MB | +25MB | +40MB |
| Riesgo de regresion | Bajo | Medio | Alto |
| Testabilidad | Media | Alta | Muy alta |
| Complejidad para equipo | Baja | Media | Alta |
| Tiempo estimado | 2 dias | 3 dias | 5+ dias |
| Escalabilidad futura | Media | Alta | Muy alta |
| Apropiado para hackathon | Si | Si | No |

### RECOMENDACION: Arquitectura A (Incremental)

**Justificacion:**

1. **Contexto hackathon**: Estamos en OdiseIA4Good con 5 personas y dias limitados. No es momento de refactors arquitectonicos. El objetivo es DEMOSTRAR funcionalidad, no elegancia de codigo.

2. **Riesgo minimo**: La Fase 3 esta cerrada con 96 tests passing. Arquitectura A modifica files existentes sin cambiar la estructura fundamental. Cada cambio es aditivo.

3. **Deploy identico**: No hay cambios en el Dockerfile ni en render.yaml para el core. Solo se anaden dependencias (ffmpeg o pydub para OGG).

4. **Familiar**: El equipo ya conoce pipeline.py y la estructura de skills/. No necesitan aprender Steps ni EventBus.

5. **Rollback facil**: Los 3 flags nuevos (TRUTH_MODE, ARABIC_STUB_ON, OGG_AUDIO) permiten desactivar cualquier feature nueva sin tocar codigo.

6. **RAM safe**: +20MB esta muy dentro del margen de 512MB de Render free tier (baseline ~200MB).

7. **B es mejor ingenieria pero peor timing**: Pipeline v2 seria la eleccion correcta si tuvieramos 2 semanas. Para el hackathon, A es suficiente y mas segura.

> **Decision: Arquitectura A es la recomendada para Fase 4.**

---

## 7. Plan de Implementacion F4.1-F4.6

### F4.1 — Foundation (Modelos, Config, Feature Flags)

**Objetivo:** Establecer los nuevos dataclasses, feature flags y diccionarios que todas las subfases siguientes consumiran.

**Dependencias:** Ninguna (es el punto de partida).

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/models_v2.py` | TrustLabel (enum), VerifiedResponse (dataclass), SkillMetrics (dataclass), ErrorContext (dataclass) |
| `data/dictionaries/jargon_es.json` | Diccionario jerga administrativa -> lenguaje simple (~50 entradas) |
| `data/dictionaries/arabic_templates.json` | Templates de respuesta en arabe (saludo, derivacion, error) |
| `tests/unit/test_models_v2.py` | Tests para nuevos dataclasses |
| `tests/unit/test_jargon_dict.py` | Tests de carga y validacion del diccionario |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/config.py` | +3 flags: TRUTH_MODE (bool, default false), ARABIC_STUB_ON (bool, default true), OGG_AUDIO (bool, default true) |
| `src/core/models.py` | Ampliar FinalResponse: +trust_label (str, default ""), +source_ref (str, default ""), +fallback_reason (str, default "") |
| `src/core/prompts/templates.py` | +4 templates: ack_audio_ar, fallback_generic_ar, arabic_redirect, fallback_tts_fail; +ar entries en templates existentes |
| `tests/unit/test_config.py` | +3 tests para nuevos flags |

**Tests a anadir:**

| Test File | Funciones |
|-----------|-----------|
| `tests/unit/test_models_v2.py` | `test_trust_label_values`, `test_verified_response_defaults`, `test_verified_response_with_sources`, `test_skill_metrics_creation`, `test_error_context_creation` |
| `tests/unit/test_jargon_dict.py` | `test_jargon_dict_loads`, `test_jargon_dict_has_entries`, `test_jargon_dict_no_duplicates`, `test_jargon_dict_values_simpler` |
| `tests/unit/test_config.py` | `test_truth_mode_default_false`, `test_arabic_stub_default_true`, `test_ogg_audio_default_true` |

**Evidencia:**
- `docs/07-evidence/artifacts/phase4/f41-models-screenshot.txt`
- `docs/07-evidence/artifacts/phase4/f41-config-diff.txt`

**Exit Criteria:**
- Los 3 nuevos flags existen en config.py con defaults correctos
- TrustLabel tiene valores: VERIFIED, ORIENTATIVE, UNVERIFIED
- FinalResponse tiene campos trust_label, source_ref, fallback_reason
- jargon_es.json carga sin errores y tiene >= 30 entradas
- arabic_templates.json carga sin errores y tiene >= 3 templates
- Todos los tests nuevos PASS
- `ruff check src/ tests/ --select E,F,W --ignore E501` limpio
- Tests baseline (96 existentes) siguen PASS

**Tests nuevos estimados:** 12

---

### F4.2 — Truth Mode (Verificacion, Trust Labels, KB Grounding)

**Objetivo:** Que cada respuesta LLM lleve etiquetas de confianza y fuentes verificables, eliminando respuestas sin fundamentar.

**Dependencias:** F4.1 (necesita TrustLabel, VerifiedResponse, TRUTH_MODE flag)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/skills/truth_verify.py` | Skill de verificacion avanzada: claim extraction, KB grounding, trust label assignment |
| `tests/unit/test_truth_verify.py` | Tests unitarios de truth verification |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/skills/verify_response.py` | Delegar a truth_verify cuando TRUTH_MODE=true, mantener logica actual como fallback |
| `src/core/skills/kb_lookup.py` | Retornar KBContext con campo `claims_available: list[str]` (lista de facts del JSON) |
| `src/core/models.py` | Ampliar KBContext: +claims_available (list[str], default []) |
| `src/core/prompts/system_prompt.py` | Anadir instrucciones de trust labels al system prompt cuando TRUTH_MODE=true |
| `src/core/pipeline.py` | Usar truth_verify en lugar de verify_response cuando TRUTH_MODE=true |

**Logica de `truth_verify.py`:**

```
1. Extraer claims del response_text (frases con datos concretos: cantidades, plazos, URLs)
2. Para cada claim, buscar match en kb_context.datos
3. Asignar trust_label:
   - VERIFIED: claim matchea con KB.datos y KB.verificado == true
   - ORIENTATIVE: claim matchea con KB.datos pero KB.verificado == false
   - UNVERIFIED: claim no matchea con nada en KB
4. Formatear: [VERIFICADO] o [ORIENTATIVO] antes de cada claim
5. Anadir fuente al final: "Fuente: {kb_context.fuente_url}"
6. Si >50% claims son UNVERIFIED, anadir disclaimer reforzado
```

**Tests a anadir:**

| Test File | Funciones |
|-----------|-----------|
| `tests/unit/test_truth_verify.py` | `test_all_claims_verified`, `test_mixed_claims`, `test_no_kb_context_all_unverified`, `test_trust_label_formatting`, `test_source_appended`, `test_disclaimer_on_high_unverified`, `test_empty_response`, `test_truth_mode_off_passthrough`, `test_claims_extraction_numbers`, `test_claims_extraction_urls` |

**Evidencia:**
- `docs/07-evidence/artifacts/phase4/f42-truth-mode-example.txt` — Ejemplo de respuesta con trust labels
- `docs/07-evidence/artifacts/phase4/f42-test-results.txt`

**Exit Criteria:**
- truth_verify.py funciona standalone con tests unitarios
- Con TRUTH_MODE=true, respuestas LLM llevan etiquetas [VERIFICADO]/[ORIENTATIVO]
- Con TRUTH_MODE=false, comportamiento identico a Fase 3
- Fuente oficial siempre presente cuando hay KBContext
- Tests nuevos PASS + 96 existentes PASS

**Tests nuevos estimados:** 10

---

### F4.3 — Voice (TTS Upgrade, OGG, Dual Response Garantizado)

**Objetivo:** Que TODAS las respuestas (cache, LLM, fallback) incluyan audio, en formato OGG nativo de WhatsApp.

**Dependencias:** F4.1 (necesita OGG_AUDIO flag, FinalResponse ampliado)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/skills/tts_ogg.py` | Conversion texto->OGG usando gTTS+pydub, con cache de archivos |
| `tests/unit/test_tts_ogg.py` | Tests unitarios de generacion OGG |
| `tests/unit/test_dual_response.py` | Tests que verifican que toda respuesta tiene audio |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/skills/tts.py` | Refactor: si OGG_AUDIO=true, delegar a tts_ogg; si false, mantener MP3; NUNCA retornar None (usar fallback silencioso) |
| `src/core/pipeline.py` | Garantizar audio en TODOS los paths (cache hit, LLM, fallback, guardrail block); si TTS falla, enviar texto-only con log_error, no silenciar |
| `src/core/prompts/templates.py` | +template fallback_tts_fail con mensaje "No pude generar audio para esta respuesta" |
| `requirements.txt` | +pydub (para conversion MP3->OGG) |

**Logica de `tts_ogg.py`:**

```
1. Recibir texto + idioma
2. Generar MP3 con gTTS (ya funciona)
3. Convertir MP3 -> OGG Opus con pydub
4. Cache con hash determinista (tts_{hash}.ogg)
5. Si conversion falla, retornar MP3 como fallback
6. Si todo falla, retornar None (pipeline maneja)
```

**Cambio en pipeline.py (garantia dual):**

```python
# ANTES (actual): audio_url puede ser None, se envia sin audio
# DESPUES: si audio_url es None, se intenta de nuevo; si falla, se loguea pero se envia text-only
```

**Tests a anadir:**

| Test File | Funciones |
|-----------|-----------|
| `tests/unit/test_tts_ogg.py` | `test_ogg_generation_basic`, `test_ogg_cache_hit`, `test_ogg_fallback_to_mp3`, `test_ogg_language_mapping`, `test_ogg_empty_text`, `test_ogg_long_text_truncation` |
| `tests/unit/test_dual_response.py` | `test_cache_hit_has_audio`, `test_llm_response_has_audio`, `test_fallback_has_audio_attempt`, `test_guardrail_block_has_audio_attempt`, `test_arabic_stub_has_audio` |

**Evidencia:**
- `docs/07-evidence/artifacts/phase4/f43-ogg-sample.ogg` — Muestra de audio OGG generado
- `docs/07-evidence/artifacts/phase4/f43-dual-response-proof.txt`

**Exit Criteria:**
- Con OGG_AUDIO=true, archivos generados son .ogg validos
- Con OGG_AUDIO=false, archivos son .mp3 (comportamiento Fase 3)
- En pipeline, NUNCA se envia respuesta sin intentar generar audio
- Cache hits sin audio_file pre-existente generan audio on-the-fly
- Fallback a MP3 funciona si OGG conversion falla
- Tests nuevos PASS + todos los existentes PASS

**Tests nuevos estimados:** 11

---

### F4.4 — Accessibility (Templates, Arabic Stub, Jargon Dict, Adaptive)

**Objetivo:** Respuestas mas cortas, sin jerga, con pregunta de seguimiento; stub funcional para arabe.

**Dependencias:** F4.1 (jargon dict, arabic templates), F4.3 (audio para arabic stub)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/core/skills/arabic_stub.py` | Detecta arabe, responde con template + numero de telefono |
| `src/core/skills/simplify_response.py` | Reemplaza jerga, limita palabras, anade pregunta de seguimiento |
| `tests/unit/test_arabic_stub.py` | Tests del stub arabe |
| `tests/unit/test_simplify_response.py` | Tests de simplificacion |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/core/skills/detect_lang.py` | +_AR_KEYWORDS, deteccion de arabe (keywords + langdetect) |
| `src/core/pipeline.py` | Insertar arabic_stub check despues de detect_lang; insertar simplify_response antes de TTS |
| `src/core/prompts/templates.py` | Templates en arabe para: ack, fallback, redirect a telefono |
| `src/core/prompts/system_prompt.py` | Instruccion de respuesta adaptativa (follow-up question) |
| `tests/unit/test_detect_lang.py` | +tests para deteccion de arabe |

**Logica de `arabic_stub.py`:**

```python
def arabic_stub(language: str, tramite_hint: str | None) -> str | None:
    """Si idioma es arabe, retorna template con numero de telefono.
    Retorna None si idioma no es arabe."""
    if language != "ar":
        return None
    # Template: saludo en arabe + "Podemos ayudarte por telefono"
    # + numero 012 (informacion general) o especifico del tramite
    return load_arabic_template(tramite_hint or "generic")
```

**Logica de `simplify_response.py`:**

```python
def simplify_response(text: str, language: str, jargon_dict: dict) -> str:
    """Simplifica respuesta: reemplaza jerga, limita a 150 palabras,
    anade pregunta de seguimiento."""
    # 1. Reemplazar jerga (ej: "empadronamiento" -> "registro en tu ayuntamiento")
    for jargon, simple in jargon_dict.items():
        text = text.replace(jargon, simple)
    # 2. Limitar a 150 palabras
    words = text.split()
    if len(words) > 150:
        text = " ".join(words[:150]) + "..."
    # 3. Anadir pregunta de seguimiento si no la tiene
    if "?" not in text[-50:]:
        followups = {
            "es": "Tienes alguna otra duda sobre este tramite?",
            "fr": "Avez-vous d'autres questions sur cette demarche?",
        }
        text += f"\n\n{followups.get(language, followups['es'])}"
    return text
```

**Tests a anadir:**

| Test File | Funciones |
|-----------|-----------|
| `tests/unit/test_arabic_stub.py` | `test_arabic_returns_template`, `test_non_arabic_returns_none`, `test_arabic_has_phone_number`, `test_arabic_generic_template`, `test_arabic_imv_template`, `test_arabic_template_encoding` |
| `tests/unit/test_simplify_response.py` | `test_jargon_replacement`, `test_word_limit_150`, `test_followup_added`, `test_followup_not_duplicated`, `test_french_followup`, `test_empty_text`, `test_short_text_unchanged` |
| `tests/unit/test_detect_lang.py` | `test_arabic_detected_by_keywords`, `test_arabic_detected_by_langdetect`, `test_arabic_short_text` |

**Evidencia:**
- `docs/07-evidence/artifacts/phase4/f44-arabic-example.txt` — Ejemplo de respuesta en arabe
- `docs/07-evidence/artifacts/phase4/f44-simplify-before-after.txt` — Comparativa antes/despues

**Exit Criteria:**
- detect_lang reconoce "ar" para texto en arabe
- arabic_stub retorna template valido con numero de telefono
- simplify_response reemplaza >= 10 terminos de jerga
- Respuestas <= 150 palabras
- Pregunta de seguimiento presente si no habia pregunta
- Con ARABIC_STUB_ON=false, arabe pasa al flujo normal (LLM intenta responder)
- Tests nuevos PASS + todos los existentes PASS

**Tests nuevos estimados:** 16

---

### F4.5 — Observability (Latencia por Skill, Analytics de Fallback, Evidence)

**Objetivo:** Que cada request genere un registro JSON con latencia por skill, razon de fallback, source tracking, exportable para evidencia.

**Dependencias:** F4.1 (SkillMetrics), F4.2 (trust labels en logs)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `src/utils/metrics_collector.py` | Collector de metricas por request: latencias, fallback reasons, sources |
| `tests/unit/test_metrics_collector.py` | Tests del collector |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `src/utils/observability.py` | Ampliar RequestContext con fields: fallback_reason, source_chain (list), trust_label, language_detected |
| `src/utils/timing.py` | Decorator ahora tambien registra nombre de skill + success/fail en RequestContext |
| `src/utils/logger.py` | +log_skill_metrics(ctx) — emite JSON con todas las latencias |
| `src/core/pipeline.py` | Al final de process(), llamar log_skill_metrics; en cada fallback, registrar fallback_reason |
| `src/routes/health.py` | +endpoint GET /metrics — ultimas N requests con latencias (protegido con ADMIN_TOKEN) |
| `tests/unit/test_observability.py` | +tests para nuevos campos |

**Formato de log JSON esperado:**

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
    "guardrail_post": 3,
    "simplify": 2,
    "tts": 450,
    "send_response": 320,
    "total": 2005
  },
  "source_chain": ["cache_miss", "kb_hit:imv", "llm:gemini", "truth:verified"]
}
```

**Tests a anadir:**

| Test File | Funciones |
|-----------|-----------|
| `tests/unit/test_metrics_collector.py` | `test_collector_records_timing`, `test_collector_records_fallback`, `test_collector_source_chain`, `test_collector_to_json`, `test_collector_reset` |
| `tests/unit/test_observability.py` | `test_context_has_fallback_reason`, `test_context_has_source_chain`, `test_context_has_trust_label`, `test_full_context_serialization` |

**Evidencia:**
- `docs/07-evidence/artifacts/phase4/f45-metrics-sample.json` — Ejemplo de salida de metricas
- `docs/07-evidence/artifacts/phase4/f45-latency-targets.txt`

**Exit Criteria:**
- Cada request genera log JSON con latencias por skill
- fallback_reason registrado en TODOS los paths de fallback
- source_chain traza la ruta completa del pipeline
- GET /metrics (con ADMIN_TOKEN) retorna ultimas requests
- Latencia targets: total < 8s, TTS < 2s, LLM < 4s
- Tests nuevos PASS + todos los existentes PASS

**Tests nuevos estimados:** 9

---

### F4.6 — Integration + QA (Full Pipeline, 6 Demos, Evidence Pack)

**Objetivo:** Integrar todas las subfases, ejecutar 6 conversaciones demo end-to-end, generar paquete de evidencia completo.

**Dependencias:** F4.1, F4.2, F4.3, F4.4, F4.5 (TODAS)

**Archivos a CREAR:**

| Archivo | Descripcion |
|---------|-------------|
| `tests/e2e/test_phase4_flows.py` | 6 conversaciones demo E2E |
| `tests/integration/test_pipeline_v2.py` | Test de integracion del pipeline completo con todas las features F4 |
| `docs/07-evidence/PHASE-4-EVIDENCE.md` | Documento de evidencia |
| `docs/07-evidence/artifacts/phase4/f46-demo-conversations.txt` | Transcripciones de 6 demos |
| `scripts/phase4_verify.sh` | Script de verificacion automatizada Fase 4 |

**Archivos a MODIFICAR:**

| Archivo | Cambio |
|---------|--------|
| `data/cache/demo_cache.json` | +2 entradas: saludo_ar, imv_ar (con audio_file OGG) |
| `src/core/pipeline.py` | Ajustes finales de integracion, order of operations |
| `docs/07-evidence/PHASE-STATUS.md` | Actualizar estado Fase 4 |
| `docs/07-evidence/PHASE-CLOSE-CHECKLIST.md` | Anadir seccion Fase 4 |

**6 Conversaciones Demo:**

| # | Nombre | Idioma | Input | Flujo esperado |
|---|--------|--------|-------|----------------|
| D1 | Maria IMV | es | texto | cache hit -> texto + audio OGG |
| D2 | Ahmed empadronamiento | fr | texto | cache hit -> texto fr + audio OGG |
| D3 | Fatima tarjeta sanitaria | es | texto | cache miss -> LLM -> truth verify -> texto [VERIFICADO] + audio OGG |
| D4 | Omar saludo | ar | texto | arabic stub -> template ar + telefono + audio OGG |
| D5 | Robert audio IMV | es | audio | transcribe -> cache hit -> texto + audio OGG |
| D6 | Error recovery | es | texto (off-topic) | guardrail/fallback -> mensaje especifico + audio OGG |

**Tests a anadir:**

| Test File | Funciones |
|-----------|-----------|
| `tests/e2e/test_phase4_flows.py` | `test_demo_d1_maria_imv_cache`, `test_demo_d2_ahmed_fr_cache`, `test_demo_d3_fatima_llm_truth`, `test_demo_d4_omar_arabic_stub`, `test_demo_d5_audio_pipeline`, `test_demo_d6_error_recovery` |
| `tests/integration/test_pipeline_v2.py` | `test_full_pipeline_text_es`, `test_full_pipeline_text_fr`, `test_full_pipeline_arabic`, `test_full_pipeline_truth_mode`, `test_full_pipeline_ogg_audio`, `test_full_pipeline_fallback_reason_logged` |

**Evidencia:**
- `docs/07-evidence/PHASE-4-EVIDENCE.md` — Documento completo
- `docs/07-evidence/artifacts/phase4/f46-demo-conversations.txt`
- `docs/07-evidence/artifacts/phase4/f46-test-results.txt`
- `docs/07-evidence/artifacts/phase4/f46-metrics-full.json`
- `docs/07-evidence/artifacts/phase4/f46-lint-clean.txt`

**Exit Criteria:**
- TODOS los tests PASS (96 existentes + ~58 nuevos = ~154 total)
- `ruff check` limpio
- 6 conversaciones demo documentadas con input/output
- Cada demo incluye texto + audio
- PHASE-4-EVIDENCE.md completo con screenshots/logs
- PHASE-STATUS.md actualizado con semaforo verde para Fase 4
- Latencia promedio < 8s en las 6 demos

**Tests nuevos estimados:** 12

---

### Resumen de Tests por Subfase

| Subfase | Tests nuevos | Total acumulado |
|---------|:---:|:---:|
| Baseline (Fase 3) | - | 96 |
| F4.1 Foundation | 12 | 108 |
| F4.2 Truth Mode | 10 | 118 |
| F4.3 Voice | 11 | 129 |
| F4.4 Accessibility | 16 | 145 |
| F4.5 Observability | 9 | 154 |
| F4.6 Integration | 12 | 166 |
| **TOTAL FASE 4** | **70** | **166** |

### Resumen de Archivos por Subfase

| Subfase | Crear | Modificar |
|---------|:---:|:---:|
| F4.1 | 5 | 4 |
| F4.2 | 2 | 5 |
| F4.3 | 3 | 4 |
| F4.4 | 4 | 5 |
| F4.5 | 2 | 6 |
| F4.6 | 5 | 4 |
| **TOTAL** | **21** | **28** |

(Nota: algunos archivos se modifican en multiples subfases; el numero real de archivos unicos modificados es ~12.)

### Diagrama de Dependencias

```
  F4.1 Foundation
    |
    +------+------+------+
    |      |      |      |
    v      v      v      |
  F4.2   F4.3   F4.4    |
  Truth  Voice  Access   |
    |      |      |      |
    +------+------+      |
    |                    |
    v                    v
  F4.5 Observability
    |
    v
  F4.6 Integration + QA
```

Orden recomendado de ejecucion:
1. F4.1 (bloquea todo)
2. F4.2 + F4.3 + F4.4 (pueden ser paralelas entre 3 developers)
3. F4.5 (necesita F4.1 y F4.2)
4. F4.6 (necesita todo)

---

## 8. Top 10 Riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigacion |
|---|--------|:---:|:---:|------------|
| R1 | **gTTS no soporta OGG nativo** — gTTS genera solo MP3 | Alta | Alto | Usar gTTS->MP3 + pydub->OGG como pipeline. Si pydub falla, fallback a MP3 que WhatsApp tambien acepta. Flag OGG_AUDIO para rollback. |
| R2 | **pydub requiere ffmpeg** que no esta en Docker image | Alta | Alto | Anadir `apt-get install -y ffmpeg` al Dockerfile. Solo ~30MB extra. Si excede RAM de Render, usar MP3 directamente (WhatsApp lo soporta como media adjunto). |
| R3 | **RAM de Render excede 512MB** con ffmpeg + pydub | Media | Alto | Monitorear con `docker stats`. Si excede, desactivar OGG_AUDIO=false y enviar MP3. Whisper local ya esta desactivado, asi que hay margen. |
| R4 | **Trust labels confunden al usuario** — [VERIFICADO] no se entiende | Media | Medio | Usar iconos simples: "Dato oficial" vs "Informacion orientativa". User testing con 2 personas antes de demo final. |
| R5 | **Deteccion de arabe falla** con texto corto o mixto | Media | Medio | Keyword list agresiva (_AR_KEYWORDS con 15+ palabras comunes). Fallback: si langdetect dice "ar", confiar. Si ambiguo, preguntar idioma. |
| R6 | **Jargon dict incompleto** — no cubre todos los terminos | Baja | Bajo | Empezar con 30-50 terminos mas comunes. Es un JSON, facil de ampliar post-demo. No bloquea si falta un termino. |
| R7 | **Regresion en tests existentes** al modificar pipeline.py | Media | Alto | Correr `pytest tests/ -v` despues de CADA cambio en pipeline.py. No mergear subfase sin 100% tests green. Flag-guard cada feature nueva. |
| R8 | **Latencia > 8s** con TTS OGG anadido al pipeline | Media | Medio | TTS corre en paralelo? No, es secuencial. Pero gTTS + pydub conversion deberia ser <2s para textos <200 palabras. Cache de OGG evita regeneracion. Monitor con observabilidad. |
| R9 | **Templates en arabe incorrectos** — el equipo no habla arabe | Alta | Medio | Usar traducciones verificadas de fuentes oficiales (ACNUR, Cruz Roja). Incluir solo 3-4 templates basicos. Marcar como "stub" en documentacion. Validar con native speaker si posible. |
| R10 | **Conflictos de merge** entre 3 developers trabajando en paralelo | Media | Medio | Cada subfase tiene archivos distintos (excepto pipeline.py y config.py). Pipeline.py se modifica secuencialmente por subfase. Config.py tiene un PR unico de F4.1 que todos basan. |

---

## 9. Gate Criteria Fase 4

### G4.0 — Foundation Gate (post-F4.1)

| Criterio | Target |
|----------|--------|
| Tests totales PASS | >= 108 |
| Flags en config.py | 12 (9 existentes + 3 nuevos) |
| jargon_es.json entries | >= 30 |
| arabic_templates.json entries | >= 3 |
| ruff clean | 0 errores |

### G4.1 — Truth Gate (post-F4.2)

| Criterio | Target |
|----------|--------|
| Tests totales PASS | >= 118 |
| Respuesta LLM con TRUTH_MODE=true lleva trust label | 100% |
| Fuente oficial presente cuando KBContext existe | 100% |
| TRUTH_MODE=false no cambia comportamiento | Verified by diff test |

### G4.2 — Voice Gate (post-F4.3)

| Criterio | Target |
|----------|--------|
| Tests totales PASS | >= 129 |
| Respuestas con audio_url no-null | >= 95% (5% tolerancia por TTS failures) |
| Archivos OGG generados validos | Verified by header check |
| Fallback MP3 funciona si OGG falla | Test PASS |

### G4.3 — Access Gate (post-F4.4)

| Criterio | Target |
|----------|--------|
| Tests totales PASS | >= 145 |
| detect_lang reconoce "ar" | Test PASS |
| arabic_stub retorna template valido | Test PASS |
| Respuesta promedio <= 150 palabras | Verified by test |
| Pregunta de seguimiento presente | >= 90% responses |

### G4.4 — Observability Gate (post-F4.5)

| Criterio | Target |
|----------|--------|
| Tests totales PASS | >= 154 |
| Log JSON con latencias por skill | Every request |
| fallback_reason registrado | Every fallback path |
| /metrics endpoint funcional | Test PASS |
| Latencia total < 8s | 90th percentile |

### G4.5 — Final Gate (post-F4.6)

| Criterio | Target |
|----------|--------|
| Tests totales PASS | >= 166 |
| ruff clean | 0 errores |
| 6 demos documentadas | PHASE-4-EVIDENCE.md |
| Cada demo tiene texto + audio | Verified |
| PHASE-STATUS.md actualizado | Fase 4 = verde |
| Docker build exitoso | `docker build -t civicaid-voice:f4 .` |
| Latencia promedio demos | < 8s |

### Notion Entries a Crear

| DB | Entries nuevas | Total |
|----|:---:|:---:|
| Backlog | +8 (1 por subfase + 2 bugs) | 51 |
| KB Tramites | +1 (arabic_templates reference) | 13 |
| Testing | +12 (test plans F4.1-F4.6) | 38 |
| **Total nuevas** | **21** | **102** |

### Latency Targets

| Skill | P50 Target | P90 Target |
|-------|:---:|:---:|
| guardrail_pre | < 5ms | < 10ms |
| detect_lang | < 10ms | < 20ms |
| cache_match | < 5ms | < 10ms |
| kb_lookup | < 15ms | < 30ms |
| llm_generate | < 2000ms | < 4000ms |
| truth_verify | < 10ms | < 20ms |
| simplify | < 5ms | < 10ms |
| tts (OGG) | < 1000ms | < 2000ms |
| send_response | < 500ms | < 1000ms |
| **total** | **< 4000ms** | **< 8000ms** |

### Evidence Files Required

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

## Apendice: Pipeline Completo Post-Fase 4

```
  +--------------------+
  | Usuario WhatsApp   |
  +--------+-----------+
           |
           v
  +--------+-----------+
  | Twilio POST        |
  +--------+-----------+
           |
           v
  +--------+-----------+     +------------------+
  | Flask /webhook     +---->| TwiML ACK (<1s)  |---> HTTP 200
  +--------+-----------+     +------------------+
           |
           | threading.Thread(daemon=True)
           v
  +--------+----------------------------------------------------+
  |              pipeline.process(msg)                           |
  |                                                              |
  |  [1] guardrail_pre ------> BLOCKED?                         |
  |         |                    |--YES--> tts_safe --> send     |
  |         |                                                    |
  |  [2] detect_input + AUDIO?                                  |
  |         |--YES--> fetch_media --> transcribe (Gemini)        |
  |         |--NO---> detect_lang (es/fr/ar/en)                 |
  |         |                                                    |
  |  [3] lang == "ar" && ARABIC_STUB_ON?                        |
  |         |--YES--> arabic_stub --> tts --> send + EXIT        |
  |         |                                                    |
  |  [4] cache_match ------> HIT?                               |
  |         |                 |--YES--> tts_ensure --> send      |
  |         |                                                    |
  |  [5] DEMO_MODE? -------> YES --> fallback --> tts --> send   |
  |         |                                                    |
  |  [6] kb_lookup (JSON, con claims_available)                  |
  |         |                                                    |
  |  [7] llm_generate (Gemini Flash)                             |
  |         |                                                    |
  |  [8] TRUTH_MODE? --> truth_verify (labels + grounding)       |
  |         |       \--> verify_response (legacy: URL + limit)   |
  |         |                                                    |
  |  [9] structured_output? (opcional)                           |
  |         |                                                    |
  | [10] guardrail_post (PII + disclaimer)                       |
  |         |                                                    |
  | [11] simplify_response (jargon + 150 words + follow-up Q)   |
  |         |                                                    |
  | [12] tts (OGG primary, MP3 fallback, NEVER None)             |
  |         |                                                    |
  | [13] send_response (Twilio REST + retry sin media)           |
  |         |                                                    |
  | [14] log_skill_metrics (JSON con latencias + source_chain)   |
  +--------------------------------------------------------------+
```

### Tabla de Skills Post-Fase 4

| # | Skill | Archivo | Nuevo/Modificado |
|---|-------|---------|:---:|
| 1 | guardrail_pre | src/core/guardrails.py | Sin cambios |
| 2 | detect_input | src/core/skills/detect_input.py | Sin cambios |
| 3 | fetch_media | src/core/skills/fetch_media.py | Sin cambios |
| 4 | transcribe | src/core/skills/transcribe.py | Sin cambios |
| 5 | detect_lang | src/core/skills/detect_lang.py | MODIFICADO (+ar) |
| 6 | arabic_stub | src/core/skills/arabic_stub.py | NUEVO |
| 7 | cache_match | src/core/skills/cache_match.py | Sin cambios |
| 8 | kb_lookup | src/core/skills/kb_lookup.py | MODIFICADO (+claims) |
| 9 | llm_generate | src/core/skills/llm_generate.py | Sin cambios |
| 10 | truth_verify | src/core/skills/truth_verify.py | NUEVO |
| 11 | verify_response | src/core/skills/verify_response.py | MODIFICADO (delegate) |
| 12 | guardrail_post | src/core/guardrails.py | Sin cambios |
| 13 | simplify_response | src/core/skills/simplify_response.py | NUEVO |
| 14 | tts_ensure | src/core/skills/tts_ensure.py | NUEVO (wrapper) |
| 15 | tts | src/core/skills/tts.py | MODIFICADO (OGG) |
| 16 | tts_ogg | src/core/skills/tts_ogg.py | NUEVO |
| 17 | send_response | src/core/skills/send_response.py | Sin cambios |

**Total: 17 skills (11 existentes + 3 nuevos + 3 nuevos auxiliares)**

### Feature Flags Post-Fase 4

| Flag | Default | Subfase |
|------|---------|---------|
| DEMO_MODE | false | Fase 1 |
| LLM_LIVE | true | Fase 1 |
| WHISPER_ON | true | Fase 1 |
| LLM_TIMEOUT | 6 | Fase 1 |
| WHISPER_TIMEOUT | 12 | Fase 1 |
| GUARDRAILS_ON | true | Fase 2 |
| STRUCTURED_OUTPUT_ON | false | Fase 2 |
| OBSERVABILITY_ON | true | Fase 2 |
| RAG_ENABLED | false | Fase 2 |
| **TRUTH_MODE** | **false** | **F4.1** |
| **ARABIC_STUB_ON** | **true** | **F4.1** |
| **OGG_AUDIO** | **true** | **F4.1** |

**Total: 12 flags (9 existentes + 3 nuevos)**

---

*Documento generado por Agent F (PM-Architect Lead) — 2026-02-13*
*Para aprobar, revisar con el equipo completo y confirmar asignacion de subfases a agentes.*
