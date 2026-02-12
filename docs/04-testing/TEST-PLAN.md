# TEST PLAN — CivicAid Voice "Clara"

> **Total de tests:** 10 (T1–T10)
> **Tolerancia a fallos:** CERO. Todos deben pasar.
> **Comando para ejecutar todos:** `pytest tests/ -v --tb=short`
> **Directorio de ejecución:** Raíz del proyecto (`civicaid-voice/`)

---

## Resumen de Cobertura

| Gate | Tests | Cobertura |
|---|---|---|
| **G1** (Cache + KB + Detect) | T1, T2, T3, T4, T5 | Caché de respuestas, base de conocimiento, detección de idioma |
| **G2** (Webhook + Pipeline + E2E) | T6, T7, T8, T9, T10 | Parsing de webhook, pipeline completo, integración WhatsApp |

| Tipo | Tests | Cantidad |
|---|---|---|
| Unit | T1, T2, T3, T4, T5, T6, T7 | 7 |
| Integration | T8 | 1 |
| E2E | T9, T10 | 2 |

---

## Criterio de Aprobación

- **TODOS** los tests T1–T10 deben pasar con resultado `PASS`.
- Cero tolerancia a fallos. Si un test falla, se bloquea el deploy.
- Los tests E2E (T9, T10) requieren el servidor corriendo localmente o stubs activos.
- Latencia no se mide en tests unitarios, pero sí se valida en tests E2E.

---

## Tests Detallados

### T1 — Cache Match: Keyword Exacto

| Campo | Valor |
|---|---|
| **Test ID** | T1 |
| **Archivo** | `tests/unit/test_cache.py::test_t1_cache_match_keyword_exact` |
| **Tipo** | Unit |
| **Gate** | G1 |
| **Input** | `message="Que es el IMV?"`, `lang="es"`, `input_type=TEXT` |
| **Output esperado** | `hit=True`, `id="imv_es"` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_cache.py::test_t1_cache_match_keyword_exact -v
```

**Descripción:** Verifica que cuando un usuario envía un mensaje de texto con la pregunta exacta "Que es el IMV?", el sistema de caché encuentra la respuesta pre-almacenada con el identificador `imv_es`. Este es el camino crítico para la demo WOW 1.

---

### T2 — Cache Match: Sin Match

| Campo | Valor |
|---|---|
| **Test ID** | T2 |
| **Archivo** | `tests/unit/test_cache.py::test_t2_cache_match_no_hit` |
| **Tipo** | Unit |
| **Gate** | G1 |
| **Input** | `message="Que tiempo hace?"`, `lang="es"`, `input_type=TEXT` |
| **Output esperado** | `hit=False` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_cache.py::test_t2_cache_match_no_hit -v
```

**Descripción:** Verifica que una pregunta que no está en la caché (ej. el tiempo meteorológico) devuelve `hit=False` correctamente, evitando falsos positivos.

---

### T3 — Cache Match: Imagen Demo

| Campo | Valor |
|---|---|
| **Test ID** | T3 |
| **Archivo** | `tests/unit/test_cache.py::test_t3_cache_match_image_demo` |
| **Tipo** | Unit |
| **Gate** | G1 |
| **Input** | `message=""`, `lang="es"`, `input_type=IMAGE` |
| **Output esperado** | `hit=True`, `id="maria_carta_vision"` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_cache.py::test_t3_cache_match_image_demo -v
```

**Descripción:** Verifica que cuando se recibe una imagen (sin texto) en español, el caché devuelve la respuesta de demo para el escenario de María enviando una foto de la carta del gobierno. El `id` devuelto debe ser `maria_carta_vision`.

---

### T4 — KB Lookup: Encuentra Trámite

| Campo | Valor |
|---|---|
| **Test ID** | T4 |
| **Archivo** | `tests/unit/test_kb.py::test_t4_kb_lookup_empadronamiento` |
| **Tipo** | Unit |
| **Gate** | G1 |
| **Input** | `query="necesito empadronarme"`, `lang="es"` |
| **Output esperado** | `tramite="empadronamiento"` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_kb.py::test_t4_kb_lookup_empadronamiento -v
```

**Descripción:** Verifica que la base de conocimiento (KB) identifica correctamente el trámite de "empadronamiento" cuando el usuario pregunta con lenguaje natural. La KB debe hacer matching semántico, no solo keyword exacto.

---

### T5 — Detect Language: Francés

| Campo | Valor |
|---|---|
| **Test ID** | T5 |
| **Archivo** | `tests/unit/test_lang.py::test_t5_detect_language_french` |
| **Tipo** | Unit |
| **Gate** | G1 |
| **Input** | `text="Bonjour, comment faire?"` |
| **Output esperado** | `lang="fr"` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_lang.py::test_t5_detect_language_french -v
```

**Descripción:** Verifica que el detector de idioma identifica correctamente el francés. Esto es crítico para la demo WOW 2 (Ahmed), donde la respuesta debe generarse en el idioma detectado.

---

### T6 — Webhook: Parsea POST Texto

| Campo | Valor |
|---|---|
| **Test ID** | T6 |
| **Archivo** | `tests/unit/test_webhook.py::test_t6_webhook_parse_text` |
| **Tipo** | Unit |
| **Gate** | G2 |
| **Input** | `POST Body="Hola"`, `NumMedia=0` |
| **Output esperado** | `input_type=TEXT`, `message="Hola"` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_webhook.py::test_t6_webhook_parse_text -v
```

**Descripción:** Verifica que el endpoint `/webhook` parsea correctamente un POST de Twilio con un mensaje de texto. Cuando `NumMedia=0`, el tipo de input debe ser `TEXT` y el contenido del mensaje se extrae del campo `Body`.

---

### T7 — Webhook: Parsea POST Audio

| Campo | Valor |
|---|---|
| **Test ID** | T7 |
| **Archivo** | `tests/unit/test_webhook.py::test_t7_webhook_parse_audio` |
| **Tipo** | Unit |
| **Gate** | G2 |
| **Input** | `POST NumMedia=1`, `MediaContentType0=audio/ogg` |
| **Output esperado** | `input_type=AUDIO`, `media_type="audio/ogg"` |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/unit/test_webhook.py::test_t7_webhook_parse_audio -v
```

**Descripción:** Verifica que el endpoint `/webhook` detecta correctamente cuando Twilio envía un mensaje con audio. Cuando `NumMedia=1` y el content type es `audio/ogg`, el tipo de input debe ser `AUDIO`.

---

### T8 — Pipeline: Texto con Stub

| Campo | Valor |
|---|---|
| **Test ID** | T8 |
| **Archivo** | `tests/integration/test_pipeline.py::test_t8_pipeline_text_stub` |
| **Tipo** | Integration |
| **Gate** | G2 |
| **Input** | `IncomingMessage("Que es el IMV?", type=TEXT)` |
| **Output esperado** | Twilio `send()` llamado con mensaje que contiene "Ingreso Mínimo Vital" |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/integration/test_pipeline.py::test_t8_pipeline_text_stub -v
```

**Descripción:** Test de integración que verifica el pipeline completo para un mensaje de texto. Se usa un stub para Twilio (no se envía realmente el mensaje). Verifica que la respuesta generada contiene información sobre el IMV y que se llama correctamente a la función de envío de Twilio.

---

### T9 — WhatsApp Texto: Demo Completo

| Campo | Valor |
|---|---|
| **Test ID** | T9 |
| **Archivo** | `tests/e2e/test_wa.py::test_t9_wa_text_demo` |
| **Tipo** | E2E |
| **Gate** | G2 |
| **Input** | `POST /webhook` con `Body="Que es el IMV?"`, `NumMedia=0` |
| **Output esperado** | HTTP 200, respuesta contiene información del IMV (cache hit) |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/e2e/test_wa.py::test_t9_wa_text_demo -v
```

**Descripción:** Test end-to-end que simula un POST completo al webhook como lo haría Twilio. Verifica que toda la cadena funciona: parsing → cache lookup → respuesta con información del IMV. Es la validación directa del escenario WOW 1 de la demo.

---

### T10 — WhatsApp Audio: Demo Stub

| Campo | Valor |
|---|---|
| **Test ID** | T10 |
| **Archivo** | `tests/e2e/test_wa.py::test_t10_wa_audio_demo_stub` |
| **Tipo** | E2E |
| **Gate** | G2 |
| **Input** | `POST /webhook` con `NumMedia=1`, `MediaContentType0=audio/ogg`, `MediaUrl0=<stub_url>` |
| **Output esperado** | Pipeline llamado con `input_type=AUDIO`, procesamiento iniciado |
| **Output real** | _(rellenar al ejecutar)_ |
| **Resultado** | ☐ PASS / ☐ FAIL |

**Comando:**
```bash
pytest tests/e2e/test_wa.py::test_t10_wa_audio_demo_stub -v
```

**Descripción:** Test end-to-end que simula el envío de una nota de voz al webhook. Usa stubs para Whisper y Twilio media para no depender de servicios externos. Verifica que el pipeline identifica correctamente el tipo de input como `AUDIO` y ejecuta la ruta de procesamiento de audio.

---

## Resumen de Ejecución

### Ejecutar todos los tests

```bash
pytest tests/ -v --tb=short
```

### Ejecutar solo tests de Gate G1

```bash
pytest tests/unit/test_cache.py tests/unit/test_kb.py tests/unit/test_lang.py -v --tb=short
```

### Ejecutar solo tests de Gate G2

```bash
pytest tests/unit/test_webhook.py tests/integration/ tests/e2e/ -v --tb=short
```

### Ejecutar solo tests unitarios

```bash
pytest tests/unit/ -v --tb=short
```

### Ejecutar solo tests de integración

```bash
pytest tests/integration/ -v --tb=short
```

### Ejecutar solo tests E2E

```bash
pytest tests/e2e/ -v --tb=short
```

---

## Tabla Resumen

| Test | Tipo | Gate | Input | Output Esperado | Resultado |
|---|---|---|---|---|---|
| T1 | Unit | G1 | "Que es el IMV?", es, TEXT | hit=True, id=imv_es | ☐ |
| T2 | Unit | G1 | "Que tiempo hace?", es, TEXT | hit=False | ☐ |
| T3 | Unit | G1 | "", es, IMAGE | hit=True, id=maria_carta_vision | ☐ |
| T4 | Unit | G1 | "necesito empadronarme", es | tramite=empadronamiento | ☐ |
| T5 | Unit | G1 | "Bonjour, comment faire?" | lang="fr" | ☐ |
| T6 | Unit | G2 | POST Body="Hola", NumMedia=0 | input_type=TEXT | ☐ |
| T7 | Unit | G2 | POST NumMedia=1, audio/ogg | input_type=AUDIO | ☐ |
| T8 | Integration | G2 | IncomingMessage "Que es el IMV?" TEXT | Twilio send con "Ingreso Mínimo Vital" | ☐ |
| T9 | E2E | G2 | POST /webhook "Que es el IMV?" | Cache response con info IMV | ☐ |
| T10 | E2E | G2 | POST /webhook audio/ogg | Pipeline con AUDIO type | ☐ |

---

> **Regla:** Si algún test falla, NO se despliega. Corregir primero, re-ejecutar todos, y solo con 10/10 PASS se procede al deploy.
