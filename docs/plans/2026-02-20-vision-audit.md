# Vision Feature — Multi-Agent Audit Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Auditar que la implementacion de vision (6 commits, 15 tests, 508 passed) funcione correctamente end-to-end, sin regresiones, con edge cases cubiertos y documentacion sincronizada.

**Architecture:** 3 agentes paralelos + 1 agente secuencial final. Cada agente audita un dominio independiente. El agente final ejecuta la validacion cruzada y genera el reporte.

**Tech Stack:** Python 3.11, pytest, ruff, Flask, Gemini 1.5 Flash vision, Twilio WhatsApp

---

## Estado Actual (pre-audit)

| Metrica | Valor |
|---------|-------|
| Commits vision | 6 (bf63940..8a4d297) |
| Tests nuevos | 15 (6 analyze_image + 3 pipeline_image + 4 template + 2 config) |
| Tests totales | 532 collected, 508 passed, 19 skipped, 5 xpassed |
| Lint | Clean (ruff E,F,W) |
| App boot | OK |
| Gates pasados | 9/9 (G1-G9) |

## Lectura Obligatoria (TODOS los agentes)

Antes de ejecutar CUALQUIER tarea, cada agente DEBE leer:

1. `CLAUDE.md` — Contexto completo del proyecto
2. `src/core/skills/analyze_image.py` — Skill de vision (90 lineas)
3. `src/core/pipeline.py:188-216` — IMAGE branch en pipeline
4. `tests/unit/test_analyze_image.py` — 6 tests unitarios
5. `tests/unit/test_pipeline_image.py` — 3 tests de integracion pipeline
6. `src/core/config.py:47-49` — Flags VISION_ENABLED, VISION_TIMEOUT
7. `src/core/prompts/templates.py:14-23` — Templates ack_image, vision_fail
8. `src/routes/webhook.py:76-77` — IMAGE ACK en webhook

---

## Equipo de Agentes

| Agente | Rol | Tipo | Skills |
|--------|-----|------|--------|
| **audit-unit** | Audita tests unitarios + edge cases | general-purpose | test-driven-development, code-reviewer |
| **audit-integration** | Audita pipeline + webhook + config | general-purpose | code-auditor, systematic-debugging |
| **audit-docs** | Audita docs + HTML + consistencia | general-purpose | review-implementing |
| **audit-final** | Validacion cruzada + reporte | general-purpose | code-reviewer |

## Dependencias

```
audit-unit ──────┐
audit-integration ├──> audit-final (reporte)
audit-docs ──────┘
```

Los 3 primeros agentes corren EN PARALELO. `audit-final` espera a que los 3 terminen.

---

## AGENTE 1: audit-unit (Tests Unitarios + Edge Cases)

### Task 1.1: Verificar cobertura de analyze_image.py

**Files:**
- Read: `src/core/skills/analyze_image.py`
- Read: `tests/unit/test_analyze_image.py`

**Step 1: Leer el skill y listar todos los branches**

Identificar TODOS los caminos posibles en `analyze_image()`:
1. `VISION_ENABLED=False` -> return failure "Vision disabled"
2. `GEMINI_API_KEY=""` -> return failure "No Gemini API key"
3. Happy path -> Gemini call -> success
4. Gemini raises Exception -> return failure with error
5. Gemini returns empty text -> (verificar si se maneja)

**Step 2: Verificar que cada branch tiene test**

Mapear tests existentes a branches:
- `test_analyze_image_returns_result_dataclass` -> branch 1 (VISION_ENABLED=False)
- `test_analyze_image_disabled_returns_failure` -> branch 1
- `test_analyze_image_no_api_key_returns_failure` -> branch 2
- `test_analyze_image_calls_gemini_with_image_bytes` -> branch 3
- `test_analyze_image_handles_api_exception` -> branch 4
- `test_analyze_image_result_has_duration` -> branch 1 (duration check)

**Step 3: Identificar gaps de cobertura**

Verificar si faltan tests para:
- [ ] Gemini returns empty string `""` (branch 5)
- [ ] `mime_type` parameter se pasa correctamente a Blob
- [ ] `VISION_PROMPT` se incluye en la llamada
- [ ] `duration_ms` es > 0 en happy path
- [ ] `base64` encoding se aplica correctamente

**Step 4: Escribir tests faltantes si hay gaps**

```python
# Solo si se identifica un gap real
def test_analyze_image_empty_response():
    """When Gemini returns empty text, result still has success=True but empty text."""
    # ...mock setup...
    mock_response.text = ""
    result = analyze_image(b"\x89PNG\r\n", "image/png")
    # Verificar comportamiento actual — puede ser success=True con text=""
```

**Step 5: Ejecutar todos los tests de vision**

Run: `pytest tests/unit/test_analyze_image.py -v --tb=short`
Expected: ALL PASS

**Step 6: Documentar hallazgos**

Crear nota en formato:
```
## audit-unit Findings
- Branches cubiertos: X/Y
- Gaps encontrados: [lista]
- Tests agregados: [lista o "ninguno"]
- Edge cases: [OK/GAPS]
```

---

### Task 1.2: Verificar edge cases en ImageAnalysisResult

**Files:**
- Read: `src/core/skills/analyze_image.py:25-31`

**Step 1: Verificar dataclass fields y defaults**

```python
@dataclass
class ImageAnalysisResult:
    text: str          # required
    duration_ms: int   # required
    success: bool      # required
    error: Optional[str] = None  # optional
```

Verificar:
- [ ] `text` no tiene default -> fuerza valor explicito
- [ ] `duration_ms` es int, no float
- [ ] `error` es None por default (happy path no lo setea)
- [ ] No hay campos faltantes (e.g., `model`, `tokens_used`)

**Step 2: Ejecutar test de dataclass**

Run: `pytest tests/unit/test_analyze_image.py::test_analyze_image_returns_result_dataclass -v`
Expected: PASS

---

### Task 1.3: Verificar VISION_PROMPT

**Files:**
- Read: `src/core/skills/analyze_image.py:11-22`

**Step 1: Verificar contenido del prompt**

El prompt DEBE:
- [ ] Identificarse como "Clara"
- [ ] Mencionar "personas vulnerables en Espana"
- [ ] Pedir los 4 puntos de analisis (tipo, organismo, accion, ayuda profesional)
- [ ] Tener fallback para imagenes no-administrativas
- [ ] Pedir respuesta en espanol
- [ ] Limitar a 200 palabras
- [ ] Pedir lenguaje simple ("nivel de comprension: 12 anos")

**Step 2: Verificar que el prompt se pasa a Gemini**

En `test_analyze_image_calls_gemini_with_image_bytes`, verificar que `generate_content` recibe el prompt. Revisar si el test actual verifica el contenido del prompt o solo que se llama.

---

## AGENTE 2: audit-integration (Pipeline + Webhook + Config)

### Task 2.1: Auditar IMAGE branch en pipeline.py

**Files:**
- Read: `src/core/pipeline.py` (completo)
- Read: `tests/unit/test_pipeline_image.py`

**Step 1: Verificar posicion del IMAGE branch**

El branch IMAGE DEBE estar:
- DESPUES de guardrails pre-check (line 44)
- DESPUES de audio pipeline (line 60)
- DESPUES de detect_language (line 80)
- DESPUES de memory block (line 83)
- DESPUES de cache match (line 152)
- DESPUES de DEMO_MODE (line 175)
- ANTES de KB lookup (line 219)

Verificar: `pipeline.py:188-216` — `if msg.input_type == InputType.IMAGE and msg.media_url:`

**Step 2: Verificar flujo completo IMAGE**

```
cache_match(text, language, IMAGE)
  -> HIT: respuesta demo (backward compat) -> return
  -> MISS:
    -> DEMO_MODE: fallback -> return
    -> fetch_media(media_url) -> None: vision_fail fallback -> return
    -> analyze_image(bytes, mime) -> success: FinalResponse(source="vision") -> return
    -> analyze_image -> fail: vision_fail fallback -> return
```

Verificar que CADA rama tiene test en `test_pipeline_image.py`.

**Step 3: Verificar test de cache hit skips vision**

```python
# test_pipeline_image.py::test_pipeline_image_cache_hit_skips_vision
# Debe verificar que mock_analyze.assert_not_called()
```

**Step 4: Verificar test de vision failure fallback**

```python
# test_pipeline_image.py::test_pipeline_image_falls_back_on_vision_failure
# Debe verificar que sent.source == "fallback"
```

**Step 5: Identificar ramas no testeadas**

Revisar si falta test para:
- [ ] `fetch_media` returns None (media download fails)
- [ ] `DEMO_MODE=True` con IMAGE input (goes to fallback_generic, NOT vision)
- [ ] `GUARDRAILS_ON=True` con IMAGE input (guardrails pre-check before image)

**Step 6: Escribir tests faltantes si hay gaps**

Solo si se identifica un gap real en un camino critico.

**Step 7: Ejecutar tests de pipeline image**

Run: `pytest tests/unit/test_pipeline_image.py -v --tb=short`
Expected: ALL PASS

---

### Task 2.2: Auditar webhook IMAGE ACK

**Files:**
- Read: `src/routes/webhook.py`
- Read: `tests/integration/test_webhook.py` (si existe)

**Step 1: Verificar el elif IMAGE en webhook**

```python
# webhook.py:76-77
elif input_type == InputType.IMAGE:
    ack_text = get_template("ack_image", "es")
```

Verificar:
- [ ] Se usa `elif` (no `if` suelto)
- [ ] Se usa `InputType.IMAGE` (no string literal)
- [ ] Se usa `get_template("ack_image", "es")`
- [ ] Esta DESPUES del `if AUDIO` (line 74) y ANTES del `else` text (line 78)

**Step 2: Verificar que existe test de webhook con IMAGE**

Buscar en `tests/integration/test_webhook.py` un test que envie `NumMedia=1, MediaContentType0=image/jpeg` y verifique que el ACK contiene "analizando tu imagen".

Si NO existe, marcar como gap.

**Step 3: Documentar hallazgos**

---

### Task 2.3: Auditar config flags VISION_*

**Files:**
- Read: `src/core/config.py:47-49`
- Read: `tests/unit/test_config.py`

**Step 1: Verificar definicion de flags**

```python
VISION_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("VISION_ENABLED", "true")))
VISION_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("VISION_TIMEOUT", "10")))
```

Verificar:
- [ ] Default VISION_ENABLED es `"true"` (activo por default)
- [ ] Default VISION_TIMEOUT es `"10"` (segundos)
- [ ] Tipo es `bool` y `int` respectivamente
- [ ] Usan `_bool()` y `int()` para parsing

**Step 2: Verificar tests de config**

Buscar en `tests/unit/test_config.py` tests para `VISION_ENABLED` y `VISION_TIMEOUT`.

**Step 3: Verificar que VISION_TIMEOUT se usa en el skill**

Buscar en `analyze_image.py` si `config.VISION_TIMEOUT` se usa (actualmente NO se usa en la llamada a Gemini — posible gap).

Nota: El timeout NO se pasa a `client.models.generate_content()`. Esto es un gap conocido — Gemini SDK maneja timeouts internamente, pero deberiamos documentarlo.

---

### Task 2.4: Verificar no-regresion completa

**Step 1: Ejecutar suite completa**

Run: `pytest tests/ -v --tb=short`
Expected: 508 passed, 19 skipped, 5 xpassed (0 failures)

**Step 2: Ejecutar lint**

Run: `ruff check src/ tests/ --select E,F,W --ignore E501`
Expected: All checks passed

**Step 3: Verificar app boot**

Run: `PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('OK')"`
Expected: OK

**Step 4: Verificar import chain**

Run: `PYTHONPATH=. python -c "from src.core.skills.analyze_image import analyze_image, ImageAnalysisResult; print('OK')"`
Expected: OK

---

## AGENTE 3: audit-docs (Documentacion + HTML + Consistencia)

### Task 3.1: Auditar CLAUDE.md con realidad del codigo

**Files:**
- Read: `CLAUDE.md`
- Read: `src/core/config.py` (contar flags reales)
- Read: `src/core/skills/` (contar skills reales)

**Step 1: Verificar conteo de flags**

CLAUDE.md dice "31 flags". Contar flags reales en `config.py` y verificar match.

**Step 2: Verificar conteo de skills**

CLAUDE.md dice "12 skills atomicas". Listar archivos en `src/core/skills/` y verificar match.

**Step 3: Verificar conteo de tests**

CLAUDE.md dice "532 collected (508 passed, 19 skipped, 5 xpassed)". Ejecutar `pytest --co -q` y verificar match.

**Step 4: Verificar tabla de feature flags**

La tabla en CLAUDE.md debe incluir:
- [ ] `VISION_ENABLED | true | Habilita analisis de imagenes via Gemini Vision`
- [ ] `VISION_TIMEOUT | 10 | Segundos max Gemini Vision`

**Step 5: Verificar que pipeline dice "12 skills"**

CLAUDE.md: `pipeline.py  # Orquestador de 12 skills`

**Step 6: Documentar discrepancias**

---

### Task 3.2: Auditar presentacion HTML — Datos y Consistencia

**Files:**
- Read: `presentacion/clara-pitch.html`
- Read: `presentacion/demo-webapp.html`
- Read: `presentacion/demo-whatsapp.html`

**Step 1: Verificar estadisticas en clara-pitch.html**

El pitch muestra (slide 7, arquitectura):
- "469 tests" — INCORRECTO, debe ser 508+ (o 532 collected)
- Verificar si menciona vision/imagenes

**Step 2: Verificar equipo en clara-pitch.html**

El pitch muestra (slide 10):
- Team de 5: Robert, Marcos, Lucas, Daniel, Andrea
- PERO la usuaria dijo "solo lo he hecho yo (todo el proyecto)"
- MARCAR como discrepancia critica — necesita decision de la usuaria

**Step 3: Verificar que demo-webapp.html tiene boton Foto**

El demo de webapp debe tener un modo "Foto" (ademas de Escribir y Voz).

**Step 4: Verificar que demo-whatsapp.html muestra flujo de imagen**

El demo WhatsApp debe mostrar un mensaje con imagen y respuesta de vision.

**Step 5: Documentar todos los hallazgos HTML**

```
## HTML Findings
- clara-pitch.html: tests count WRONG (469 -> 508+)
- clara-pitch.html: team section NEEDS REVIEW (5 personas vs 1)
- demo-webapp.html: [OK/NEEDS WORK]
- demo-whatsapp.html: [OK/NEEDS WORK]
```

---

### Task 3.3: Auditar templates vision

**Files:**
- Read: `src/core/prompts/templates.py:14-23`

**Step 1: Verificar ack_image en 3 idiomas**

```python
"ack_image": {
    "es": "Estoy analizando tu imagen... 📷",
    "fr": "J'analyse votre image... 📷",
    "en": "Analyzing your image... 📷",
}
```

Verificar:
- [ ] Existe en es, fr, en
- [ ] Emoji presente en los 3
- [ ] Tono consistente con ack_text y ack_audio

**Step 2: Verificar vision_fail en 3 idiomas**

```python
"vision_fail": {
    "es": "No pude analizar la imagen. ¿Podrias describir lo que ves o escribir tu pregunta?",
    "fr": "...",
    "en": "...",
}
```

Verificar:
- [ ] Existe en es, fr, en
- [ ] Ofrece alternativa (describir/escribir)
- [ ] Tono empatico y accesible

**Step 3: Verificar que tests de templates cubren vision**

Buscar en `tests/unit/test_templates.py` tests para `ack_image` y `vision_fail`.

---

## AGENTE 4: audit-final (Validacion Cruzada + Reporte)

> **Ejecutar DESPUES de que los 3 agentes anteriores terminen.**

### Task 4.1: Recopilar hallazgos de los 3 agentes

**Step 1: Leer outputs de audit-unit, audit-integration, audit-docs**

Recopilar:
- Gaps de cobertura
- Tests agregados
- Discrepancias de docs
- Edge cases no cubiertos

### Task 4.2: Ejecutar suite final completa

**Step 1: Full test run**

Run: `pytest tests/ -v --tb=short 2>&1 | tail -5`
Expected: X passed, 19 skipped, 5 xpassed (0 failures)

**Step 2: Lint final**

Run: `ruff check src/ tests/ --select E,F,W --ignore E501`
Expected: All checks passed

**Step 3: Verificar imports no rotos**

Run: `PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('BOOT OK')"`
Expected: BOOT OK

### Task 4.3: Generar reporte de auditoria

**Step 1: Crear reporte**

Crear `docs/plans/evidence/VISION-AUDIT-REPORT.md` con formato:

```markdown
# Vision Feature — Audit Report

**Fecha:** 2026-02-20
**Auditor:** Claude Code (multi-agent)
**Commits auditados:** bf63940..8a4d297 (6 commits)

## Resumen Ejecutivo

| Area | Estado | Hallazgos |
|------|--------|-----------|
| Tests unitarios | OK/GAPS | ... |
| Tests integracion | OK/GAPS | ... |
| Pipeline flow | OK/GAPS | ... |
| Config flags | OK/GAPS | ... |
| Webhook ACK | OK/GAPS | ... |
| Templates | OK/GAPS | ... |
| Documentacion | OK/GAPS | ... |
| HTML/Pitch | OK/GAPS | ... |
| Lint | OK | ... |
| No-regresion | OK | ... |

## Hallazgos Detallados

### Criticos (bloquean demo)
- [lista o "ninguno"]

### Importantes (deberian arreglarse)
- [lista]

### Menores (nice-to-have)
- [lista]

## Metricas Finales

| Metrica | Pre-audit | Post-audit |
|---------|-----------|------------|
| Tests passed | 508 | X |
| Tests skipped | 19 | X |
| Lint errors | 0 | 0 |
| Coverage gaps | ? | X |

## Conclusion

[1-2 parrafos resumiendo el estado de la feature]
```

**Step 2: Commit reporte**

```bash
git add docs/plans/evidence/VISION-AUDIT-REPORT.md
git commit -m "docs: add vision feature audit report"
```

---

## Gates de Verificacion (9 gates)

| Gate | Comando | Expected |
|------|---------|----------|
| G1 | `pytest tests/unit/test_analyze_image.py -v` | 6+ passed |
| G2 | `pytest tests/unit/test_pipeline_image.py -v` | 3+ passed |
| G3 | `pytest tests/ --tb=short` | 508+ passed, 0 failed |
| G4 | `ruff check src/ tests/ --select E,F,W --ignore E501` | All checks passed |
| G5 | `PYTHONPATH=. python -c "from src.core.skills.analyze_image import analyze_image; print('OK')"` | OK |
| G6 | `PYTHONPATH=. python -c "from src.core.config import config; print(config.VISION_ENABLED, config.VISION_TIMEOUT)"` | True 10 |
| G7 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; print(get_template('ack_image', 'es'))"` | "Estoy analizando..." |
| G8 | `PYTHONPATH=. python -c "from src.app import create_app; create_app(); print('BOOT')"` | BOOT |
| G9 | Verificar que `docs/plans/evidence/VISION-AUDIT-REPORT.md` existe | File exists |

## Constraints

- **NO modificar codigo de produccion** a menos que se encuentre un BUG real
- **NO agregar tests innecesarios** — solo cubrir gaps reales
- **NO cambiar HTML** sin confirmacion de la usuaria (marcar como hallazgo)
- **SI un gate falla, PARAR** y reportar antes de continuar
- Cada agente reporta hallazgos, NO arregla automaticamente

## Abort Conditions

- Si `pytest tests/` tiene >0 failures antes de empezar -> ABORT (codebase rota)
- Si `ruff check` tiene errores antes de empezar -> ABORT (lint roto)
- Si app no boota -> ABORT (imports rotos)
