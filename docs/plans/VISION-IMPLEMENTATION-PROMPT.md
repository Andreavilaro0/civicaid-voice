# PROMPT — Implementar Analisis de Imagenes (Gemini Vision)

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el **implementation lead** del proyecto **Clara / CivicAid Voice**. Vas a implementar el **analisis real de imagenes** via Gemini 1.5 Flash Vision.

Trabaja en **team agent mode**. Crea un equipo de 3 agentes especializados, define tareas con dependencias, y coordina la implementacion completa. Ejecuta con TDD estricto: test primero, implementacion minima, commit frecuente.

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA (en paralelo)

| # | Archivo | Para que |
|---|---------|----------|
| 1 | `CLAUDE.md` | Contexto completo del proyecto |
| 2 | `docs/plans/2026-02-20-image-vision-analysis.md` | **EL PLAN** — 6 tareas con codigo exacto |
| 3 | `src/core/pipeline.py` | Orquestador — donde insertar el branch IMAGE |
| 4 | `src/core/skills/transcribe.py` | **Patron a copiar** — ya envia bytes a Gemini con `genai.types.Part(inline_data=Blob(...))` |
| 5 | `src/core/skills/detect_input.py` | Ya detecta `InputType.IMAGE` — no tocar |
| 6 | `src/core/skills/fetch_media.py` | Ya descarga bytes de Twilio — no tocar |
| 7 | `src/core/skills/cache_match.py` | Cache match con `image_demo` — entender backward compat |
| 8 | `src/core/config.py` | Feature flags — agregar VISION_ENABLED aqui |
| 9 | `src/core/prompts/templates.py` | Templates — agregar ack_image, vision_fail |
| 10 | `src/routes/webhook.py` | ACK — agregar elif IMAGE |
| 11 | `src/core/skills/llm_generate.py` | Referencia — patron de llamada a Gemini |
| 12 | `tests/unit/test_llm_generate.py` | Referencia — patron de mock de Gemini |
| 13 | `requirements.txt` | Verificar google-genai>=1.0 ya esta |

## CONTEXTO RAPIDO

**Clara** = chatbot WhatsApp-first para personas vulnerables en Espana. Stack: Python 3.11, Flask, Twilio, Gemini 1.5 Flash, Docker, Render.

**Estado actual de imagenes:** SOLO DEMO. Cuando un usuario envia una foto, `detect_input.py` la clasifica como `IMAGE`, `cache_match.py` devuelve la entrada hardcodeada `image_demo` de `demo_cache.json`, y el usuario siempre recibe la misma respuesta generica. **Ningun modelo de vision analiza la imagen real.**

**Que vamos a construir:** Cuando el cache miss ocurre (o no hay entrada `image_demo`), el pipeline descargara la imagen de Twilio, la enviara a Gemini 1.5 Flash (que ya es multimodal), y respondera con un analisis real del documento/imagen.

**Patron existente a reusar:** `transcribe.py` ya envia audio a Gemini con este patron exacto:
```python
from google import genai
client = genai.Client(api_key=config.GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=[
        genai.types.Content(parts=[
            genai.types.Part(inline_data=genai.types.Blob(mime_type=mime_type, data=b64_data)),
            genai.types.Part(text=PROMPT),
        ])
    ],
    config=genai.types.GenerateContentConfig(max_output_tokens=500, temperature=0.3),
)
```
Usamos exactamente este patron para imagenes. Solo cambia el mime_type (`image/jpeg` en vez de `audio/ogg`) y el prompt.

## EQUIPO (3 agentes)

| Agente | Tipo | Tareas | Responsabilidad |
|--------|------|--------|-----------------|
| `config-engineer` | general-purpose | T1, T2 | Config flag + templates. Rapido, sin dependencias |
| `vision-engineer` | general-purpose | T3 | Skill `analyze_image.py` + tests unitarios. Core de la feature |
| `pipeline-engineer` | general-purpose | T4, T5, T6 | Wiring en pipeline.py + webhook.py + docs + verificacion final |

## DEPENDENCIAS

```
T1 (config flag) ──┐
                    ├──> T3 (analyze_image skill) ──> T4 (pipeline wiring) ──> T6 (docs + verify)
T2 (templates) ────┘                                  T5 (webhook ACK) ──────┘
```

- T1 y T2 son independientes — ejecutar en paralelo
- T3 depende de T1 (necesita `config.VISION_ENABLED`)
- T4 depende de T3 (necesita `analyze_image` importable)
- T5 depende de T2 (necesita template `ack_image`)
- T6 depende de T4 y T5

## TAREAS

### T1: Config flag VISION_ENABLED (config-engineer)

**Archivos:**
- Modificar: `src/core/config.py` — agregar despues de linea 45 (GUARDRAILS_ON)
- Crear/Modificar: `tests/unit/test_config.py`

**Codigo exacto a agregar en config.py:**
```python
    # --- Vision ---
    VISION_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("VISION_ENABLED", "true")))
    VISION_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("VISION_TIMEOUT", "10")))
```

**Test:**
```python
def test_vision_enabled_default_true():
    from src.core.config import Config
    c = Config()
    assert c.VISION_ENABLED is True
```

**Verificacion:** `python -m pytest tests/unit/test_config.py::test_vision_enabled_default_true -v`

**Commit:** `git commit -m "feat: add VISION_ENABLED and VISION_TIMEOUT config flags"`

---

### T2: Templates ack_image y vision_fail (config-engineer)

**Archivos:**
- Modificar: `src/core/prompts/templates.py` — agregar despues de `ack_audio`
- Crear: `tests/unit/test_templates_image.py`

**Codigo exacto a agregar en templates.py (dentro de TEMPLATES dict):**
```python
    "ack_image": {
        "es": "Estoy analizando tu imagen... \U0001f4f7",
        "fr": "J'analyse votre image... \U0001f4f7",
        "en": "Analyzing your image... \U0001f4f7",
    },
    "vision_fail": {
        "es": "No pude analizar la imagen. \u00bfPodr\u00edas describir lo que ves o escribir tu pregunta?",
        "fr": "Je n'ai pas pu analyser l'image. Pourriez-vous d\u00e9crire ce que vous voyez ?",
        "en": "I couldn't analyze the image. Could you describe what you see or type your question?",
    },
```

**Tests:**
```python
from src.core.prompts.templates import get_template

def test_ack_image_template_exists():
    result = get_template("ack_image", "es")
    assert "imagen" in result.lower()

def test_ack_image_template_french():
    result = get_template("ack_image", "fr")
    assert len(result) > 0

def test_vision_fail_template_exists():
    result = get_template("vision_fail", "es")
    assert len(result) > 0

def test_vision_fail_template_french():
    result = get_template("vision_fail", "fr")
    assert len(result) > 0
```

**Verificacion:** `python -m pytest tests/unit/test_templates_image.py -v`

**Commit:** `git commit -m "feat: add ack_image and vision_fail response templates"`

---

### T3: Skill analyze_image.py (vision-engineer) [depends_on: T1]

**Archivos:**
- Crear: `src/core/skills/analyze_image.py`
- Crear: `tests/unit/test_analyze_image.py`

**IMPORTANTE — El prompt de vision para Clara:**
```
Eres Clara, asistente que ayuda a personas vulnerables en Espana con tramites del gobierno.
Analiza esta imagen. Si es un documento oficial espanol (carta, formulario, notificacion, certificado, resolucion), identifica:
1. Que tipo de documento es
2. Que organismo lo envia
3. Que accion debe tomar la persona (plazos, pasos)
4. Si necesita ayuda profesional

Si NO es un documento administrativo, describe brevemente lo que ves y pregunta como puedes ayudar con tramites del gobierno espanol.

Responde en espanol, lenguaje simple (nivel de comprension: 12 anos). Maximo 200 palabras.
```

**Patron de codigo — copiar de transcribe.py (lineas 33-63), cambiando:**
- mime_type: usa el que viene del parametro (image/jpeg, image/png, etc.)
- prompt: usa VISION_PROMPT en vez del prompt de transcripcion
- return type: `ImageAnalysisResult` (nuevo dataclass) en vez de `TranscriptResult`

**El codigo completo de analyze_image.py esta en el plan:** `docs/plans/2026-02-20-image-vision-analysis.md` Task 3, Step 3.

**Tests (6 tests):**
1. `test_analyze_image_returns_result_dataclass` — returns ImageAnalysisResult
2. `test_analyze_image_disabled_returns_failure` — VISION_ENABLED=False
3. `test_analyze_image_no_api_key_returns_failure` — empty API key
4. `test_analyze_image_calls_gemini_with_image_bytes` — mock Gemini, verify call
5. `test_analyze_image_handles_api_exception` — graceful error handling
6. `test_analyze_image_result_has_duration` — duration_ms present

**El codigo completo de los tests esta en el plan:** Task 3, Step 1.

**Patron de mock de Gemini (copiar de test_llm_generate.py):**
```python
import unittest.mock as um
mock_genai = um.MagicMock()
mock_client = um.MagicMock()
mock_genai.Client.return_value = mock_client
mock_response = mock_client.models.generate_content.return_value
mock_response.text = "Respuesta mock"
with patch.dict("sys.modules", {
    "google.genai": mock_genai,
    "google": um.MagicMock(genai=mock_genai),
}):
    # call analyze_image here
```

**Verificacion:** `python -m pytest tests/unit/test_analyze_image.py -v`

**Commit:** `git commit -m "feat: add analyze_image skill — Gemini 1.5 Flash vision for documents"`

---

### T4: Wiring IMAGE branch en pipeline.py (pipeline-engineer) [depends_on: T3]

**Archivos:**
- Modificar: `src/core/pipeline.py`
- Crear: `tests/unit/test_pipeline_image.py`

**Que hacer:**

1. Agregar import en la parte superior de pipeline.py:
   ```python
   from src.core.skills.analyze_image import analyze_image
   ```

2. Agregar el bloque IMAGE **despues de la seccion DEMO_MODE** (despues de `return` en linea ~185), y **antes de KB LOOKUP**. La logica:
   - Si `msg.input_type == InputType.IMAGE and msg.media_url`:
     - `fetch_media()` para descargar bytes
     - `analyze_image(bytes, mime_type)` para analizar
     - Si success: enviar respuesta con `source="vision"`
     - Si fail: enviar fallback `vision_fail`

**UBICACION CRITICA:** El bloque IMAGE va DESPUES del cache match y DESPUES de DEMO_MODE. Asi:
- Cache hit con `image_demo` → respuesta demo (backward compat) ✓
- Cache miss en DEMO_MODE → fallback generico ✓
- Cache miss + IMAGE → **vision analysis** (NUEVO) ✓
- Cache miss + TEXT → KB lookup + LLM (sin cambios) ✓

**Codigo exacto en el plan:** Task 4, Step 3 (seccion "Revised location").

**Tests (3 tests):**
1. `test_pipeline_image_calls_analyze_image` — happy path, vision succeeds
2. `test_pipeline_image_falls_back_on_vision_failure` — vision fails, fallback sent
3. `test_pipeline_image_cache_hit_skips_vision` — demo cache hit, vision NOT called

**Codigo exacto de los tests en el plan:** Task 4, Step 1.

**Verificacion:**
```bash
python -m pytest tests/unit/test_pipeline_image.py -v
python -m pytest tests/ -x -q --tb=short  # regresion completa
```

**Commit:** `git commit -m "feat: wire IMAGE branch into pipeline — Gemini vision after cache miss"`

---

### T5: Fix webhook ACK para imagenes (pipeline-engineer) [depends_on: T2]

**Archivos:**
- Modificar: `src/routes/webhook.py:73-77`

**Cambio exacto — reemplazar:**
```python
    if input_type == InputType.AUDIO:
        ack_text = get_template("ack_audio", "es")
    else:
        ack_text = get_template("ack_text", "es")
```

**Con:**
```python
    if input_type == InputType.AUDIO:
        ack_text = get_template("ack_audio", "es")
    elif input_type == InputType.IMAGE:
        ack_text = get_template("ack_image", "es")
    else:
        ack_text = get_template("ack_text", "es")
```

**Verificacion:** `python -m pytest tests/ -x -q --tb=short`

**Commit:** `git commit -m "feat: return image-specific ACK when user sends a photo"`

---

### T6: Documentacion + verificacion final (pipeline-engineer) [depends_on: T4, T5]

**Archivos:**
- Modificar: `CLAUDE.md`

**Que hacer:**
1. Agregar a tabla Feature Flags:
   ```
   | VISION_ENABLED | true | Habilita analisis de imagenes via Gemini Vision |
   | VISION_TIMEOUT | 10 | Segundos max Gemini Vision |
   ```
2. Agregar `analyze_image.py` a la lista de skills en estructura de codigo
3. Actualizar conteo de tests

**Gates de verificacion final:**

| # | Gate | Comando | Esperado |
|---|------|---------|----------|
| G1 | Tests pasan | `python -m pytest tests/ -x -q --tb=short` | 0 failures |
| G2 | Lint clean | `ruff check src/ tests/ --select E,F,W --ignore E501` | 0 errores |
| G3 | App boots | `PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('OK')"` | `OK` |
| G4 | Import works | `PYTHONPATH=. python -c "from src.core.skills.analyze_image import analyze_image; print('OK')"` | `OK` |
| G5 | Config flag exists | `PYTHONPATH=. python -c "from src.core.config import config; print(config.VISION_ENABLED)"` | `True` |
| G6 | Template exists | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; print(get_template('ack_image', 'es'))"` | Contiene "imagen" |
| G7 | Pipeline imports vision | `grep -n "analyze_image" src/core/pipeline.py` | Muestra import y uso |
| G8 | Webhook has IMAGE ACK | `grep -n "IMAGE" src/routes/webhook.py` | Muestra elif IMAGE |
| G9 | No secrets in code | `grep -rn "API_KEY\|SECRET\|TOKEN" src/core/skills/analyze_image.py` | Solo referencia a config |

**Commit:** `git commit -m "docs: update CLAUDE.md with vision feature"`

## CONSTRAINTS

1. **NO modificar** `detect_input.py`, `fetch_media.py`, `demo_cache.json` — ya funcionan
2. **NO agregar dependencias** — google-genai ya esta en requirements.txt
3. **Backward compat**: si `image_demo` existe en cache, esa respuesta tiene prioridad (cache hit antes de vision)
4. **Feature flag**: todo detras de `VISION_ENABLED` — si es False, imagenes van al cache y si no hay match, fallback generico
5. **TDD estricto**: test primero, implementacion despues, verificar que pasa, commit
6. **Patron Gemini**: copiar EXACTAMENTE el patron de `transcribe.py` para enviar bytes — no inventar otro
7. **Max 200 palabras** en respuesta de vision (consistente con system_prompt.py regla 10)
8. **Frozen dataclass**: config.py usa `@dataclass(frozen=True)` — los flags se definen con `field(default_factory=lambda: ...)`

## CONDICION DE ABORT

Si alguno de estos tests falla despues de implementar, PARA y diagnostica antes de continuar:
- Tests existentes que pasaban antes ahora fallan (regresion)
- `from src.app import create_app` falla (import roto)
- `ruff check` muestra errores en archivos nuevos

## CHECKLIST FINAL

Al terminar toda la implementacion, verifica:
- [ ] 6 commits limpios (uno por tarea)
- [ ] 9+ tests nuevos pasando
- [ ] 0 regresiones
- [ ] Lint clean
- [ ] App boots OK
- [ ] CLAUDE.md actualizado
- [ ] Todos los gates G1-G9 pasan
