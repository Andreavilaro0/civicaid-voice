# PROMPT — Auditar Feature de Vision (Gemini 1.5 Flash)

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el **audit lead** del proyecto **Clara / CivicAid Voice**. Vas a auditar la implementacion del **analisis de imagenes via Gemini 1.5 Flash Vision** que se implemento en 6 commits (bf63940..8a4d297).

Tu trabajo es **verificar, NO implementar**. Buscas bugs, gaps de cobertura, inconsistencias en docs, y edge cases no cubiertos. Solo modificas codigo si encuentras un BUG REAL o un gap critico de tests.

Trabaja en **team agent mode**. Crea un equipo de 4 agentes especializados. Los primeros 3 auditan dominios independientes EN PARALELO. El 4to recopila hallazgos y genera el reporte final.

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA (cada agente lee lo que necesita)

### Todos los agentes leen:

| # | Archivo | Para que |
|---|---------|----------|
| 1 | `CLAUDE.md` | Contexto completo del proyecto |
| 2 | `src/core/skills/analyze_image.py` | El skill de vision (90 lineas) |
| 3 | `src/core/pipeline.py` | Orquestador — IMAGE branch lineas 188-216 |

### audit-unit lee adicionalmente:

| # | Archivo | Para que |
|---|---------|----------|
| 4 | `tests/unit/test_analyze_image.py` | 6 tests unitarios del skill |
| 5 | `src/core/skills/transcribe.py` | Patron Gemini de referencia (audio) |

### audit-integration lee adicionalmente:

| # | Archivo | Para que |
|---|---------|----------|
| 6 | `tests/unit/test_pipeline_image.py` | 3 tests de integracion pipeline |
| 7 | `src/routes/webhook.py` | ACK de imagenes (elif IMAGE, linea 76) |
| 8 | `src/core/config.py` | Flags VISION_ENABLED, VISION_TIMEOUT (lineas 47-49) |
| 9 | `tests/unit/test_config.py` | Tests de config existentes |

### audit-docs lee adicionalmente:

| # | Archivo | Para que |
|---|---------|----------|
| 10 | `src/core/prompts/templates.py` | Templates ack_image, vision_fail |
| 11 | `presentacion/clara-pitch.html` | Pitch — verificar datos actualizados |
| 12 | `presentacion/demo-webapp.html` | Demo webapp — verificar boton Foto |
| 13 | `presentacion/demo-whatsapp.html` | Demo WhatsApp — verificar flujo imagen |

## CONTEXTO RAPIDO

**Clara** = chatbot WhatsApp-first para personas vulnerables en Espana. Stack: Python 3.11, Flask, Twilio, Gemini 1.5 Flash, Docker, Render.

**Que se implemento (6 commits):**

| Commit | Descripcion |
|--------|-------------|
| bf63940 | feat: add VISION_ENABLED and VISION_TIMEOUT config flags |
| ccb98bc | feat: add ack_image and vision_fail response templates |
| 926f4ab | feat: add analyze_image skill — Gemini 1.5 Flash vision for documents |
| be0c915 | feat: wire IMAGE branch into pipeline — Gemini vision after cache miss |
| 04c07d1 | feat: return image-specific ACK when user sends a photo |
| 8a4d297 | docs: update CLAUDE.md with vision feature flags and analyze_image skill |

**Estado reportado:** 508 passed, 19 skipped, 5 xpassed. 9/9 gates. Lint clean.

**Flujo implementado:**
```
Usuario envia foto -> Twilio -> webhook (ACK: "Analizando tu imagen... 📷")
                              -> Background thread:
                                1. cache_match -> image_demo HIT -> demo response (backward compat)
                                2. cache_match -> MISS -> fetch_media -> analyze_image (Gemini Vision)
                                   -> success -> send vision response (source="vision")
                                   -> failure -> send vision_fail fallback (source="fallback")
```

## EQUIPO (4 agentes)

| Agente | Tipo | Tareas | Responsabilidad |
|--------|------|--------|-----------------|
| `audit-unit` | general-purpose | T1, T2, T3 | Tests unitarios, edge cases, cobertura de branches |
| `audit-integration` | general-purpose | T4, T5, T6, T7 | Pipeline flow, webhook, config, no-regresion |
| `audit-docs` | general-purpose | T8, T9, T10 | Docs, HTML, templates, consistencia datos |
| `audit-final` | general-purpose | T11, T12 | Recopila hallazgos, gates finales, genera reporte |

## DEPENDENCIAS

```
audit-unit (T1,T2,T3) ──────────┐
audit-integration (T4,T5,T6,T7) ├──> audit-final (T11,T12)
audit-docs (T8,T9,T10) ─────────┘
```

- T1-T3, T4-T7, T8-T10 corren **EN PARALELO** (3 agentes simultaneos)
- T11-T12 esperan a que los 3 agentes terminen

## FORMATO DE HALLAZGOS

Cada agente reporta hallazgos usando este formato exacto:

```
HALLAZGO [CRITICO|IMPORTANTE|MENOR]: <titulo corto>
  Archivo: <path:linea>
  Descripcion: <que esta mal>
  Impacto: <que pasa si no se arregla>
  Accion: <FIX_NEEDED | DOCUMENT | SKIP>
```

---

## AGENTE 1: audit-unit — Tests Unitarios + Edge Cases

### T1: Mapear branches vs tests en analyze_image.py

**Objetivo:** Verificar que CADA camino posible en `analyze_image()` tiene un test.

**Paso 1:** Leer `src/core/skills/analyze_image.py` y listar todos los branches:

```
Branch 1: VISION_ENABLED=False -> return failure "Vision disabled"
Branch 2: GEMINI_API_KEY="" -> return failure "No Gemini API key"
Branch 3: Happy path -> Gemini call -> response.text -> success
Branch 4: Gemini raises Exception -> return failure with error string
Branch 5: Gemini returns empty text "" -> ??? (verificar)
```

**Paso 2:** Leer `tests/unit/test_analyze_image.py` y mapear cada test a un branch:

```
test_analyze_image_returns_result_dataclass     -> Branch 1
test_analyze_image_disabled_returns_failure     -> Branch 1
test_analyze_image_no_api_key_returns_failure   -> Branch 2
test_analyze_image_calls_gemini_with_image_bytes -> Branch 3
test_analyze_image_handles_api_exception        -> Branch 4
test_analyze_image_result_has_duration          -> Branch 1 (duration check)
```

**Paso 3:** Identificar si Branch 5 (empty text) esta cubierto. Si no, reportar como hallazgo MENOR.

**Paso 4:** Verificar que el mock pattern es correcto:
- `patch.dict("sys.modules", {"google.genai": mock_genai, "google": ...})` — correcto?
- `mock_client.models.generate_content.assert_called_once()` — verifica la llamada?

**Resultado esperado:** Lista de branches con status CUBIERTO/GAP.

---

### T2: Verificar VISION_PROMPT vs requisitos

**Objetivo:** El prompt de vision debe cumplir criterios especificos de Clara.

**Paso 1:** Leer `src/core/skills/analyze_image.py:11-22` (VISION_PROMPT).

**Paso 2:** Verificar checklist:

| Criterio | Esperado | Verificar |
|----------|----------|-----------|
| Identidad | "Eres Clara" | Presente? |
| Publico | "personas vulnerables en Espana" | Presente? |
| 4 puntos analisis | tipo, organismo, accion, ayuda profesional | Los 4? |
| Fallback no-documento | "describe brevemente" + "pregunta" | Presente? |
| Idioma | "Responde en espanol" | Presente? |
| Simplicidad | "nivel de comprension: 12 anos" | Presente? |
| Limite | "Maximo 200 palabras" | Presente? |
| Consistencia | Alineado con system_prompt.py regla 10 | Verificar? |

**Paso 3:** Leer `src/core/prompts/system_prompt.py` y verificar que el VISION_PROMPT es consistente con el tono general de Clara.

**Resultado esperado:** Checklist completo con status OK/ISSUE.

---

### T3: Verificar ImageAnalysisResult dataclass

**Objetivo:** El dataclass no tiene campos faltantes ni tipos incorrectos.

**Paso 1:** Leer definicion en `analyze_image.py:25-31`:

```python
@dataclass
class ImageAnalysisResult:
    text: str
    duration_ms: int
    success: bool
    error: Optional[str] = None
```

**Paso 2:** Comparar con `TranscriptResult` en `src/core/models.py`:

```python
@dataclass
class TranscriptResult:
    text: str
    language: str
    duration_ms: int
    success: bool
    error: Optional[str] = None
```

Verificar:
- [ ] Tiene los mismos campos base (text, duration_ms, success, error)
- [ ] Falta `language`? — Es intencional? (vision siempre responde en es)
- [ ] `error` default es `None` — consistente
- [ ] No hay campo `model` ni `tokens` — OK para MVP

**Paso 3:** Ejecutar `pytest tests/unit/test_analyze_image.py -v --tb=short`

**Resultado esperado:** 6 passed, 0 failed.

---

## AGENTE 2: audit-integration — Pipeline + Webhook + Config

### T4: Auditar posicion del IMAGE branch en pipeline.py

**Objetivo:** El branch IMAGE esta en la posicion correcta dentro del pipeline.

**Paso 1:** Leer `src/core/pipeline.py` completo y verificar el orden de ejecucion:

```
1. guardrails pre-check (line ~44) — ANTES de todo
2. audio pipeline (line ~60) — transcribe audio
3. detect_language (line ~80) — solo TEXT
4. memory block (line ~83) — opt-in, forget, etc.
5. cache_match (line ~152) — busca en demo_cache
6. DEMO_MODE (line ~175) — cache-only fallback
7. IMAGE pipeline (line ~188) — ** ESTE ES EL NUEVO **
8. KB lookup (line ~219) — retriever chain
9. LLM generate (line ~241) — Gemini text
10. verify + guardrails post (line ~249)
11. memory update (line ~264)
12. TTS (line ~274)
13. send final (line ~282)
```

**Paso 2:** Verificar que el IMAGE branch:
- [ ] Esta DESPUES de cache_match (linea 152) — permite backward compat con image_demo
- [ ] Esta DESPUES de DEMO_MODE (linea 175) — en demo, imagenes van a fallback generico
- [ ] Esta ANTES de KB lookup (linea 219) — imagenes NO usan RAG
- [ ] Tiene `return` en todas las ramas — no cae al KB lookup por accidente
- [ ] Usa `from src.core.skills.fetch_media import fetch_media` (lazy import)

**Paso 3:** Contar cuantos `return` tiene el bloque IMAGE:

```python
if msg.input_type == InputType.IMAGE and msg.media_url:
    # ...
    if media_bytes is None:
        _send_fallback(msg, "vision_fail", start)
        return  # <- return 1
    # ...
    if vision_result.success and vision_result.text:
        # ...
        send_final_message(response)
        return  # <- return 2
    else:
        _send_fallback(msg, "vision_fail", start)
        return  # <- return 3
```

Verificar que son 3 returns — TODOS los caminos salen.

**Resultado esperado:** Posicion correcta, 3 returns, no hay fall-through.

---

### T5: Auditar webhook IMAGE ACK

**Objetivo:** El webhook envia el ACK correcto para imagenes.

**Paso 1:** Leer `src/routes/webhook.py:73-79` y verificar:

```python
if input_type == InputType.AUDIO:
    ack_text = get_template("ack_audio", "es")
elif input_type == InputType.IMAGE:          # <- linea 76
    ack_text = get_template("ack_image", "es")  # <- linea 77
else:
    ack_text = get_template("ack_text", "es")
```

**Paso 2:** Verificar:
- [ ] Es `elif` (no `if` suelto que sobreescribiria)
- [ ] Usa `InputType.IMAGE` (no string "IMAGE")
- [ ] Usa template key `"ack_image"` (no typo)
- [ ] Idioma hardcoded `"es"` — consistente con audio y text

**Paso 3:** Buscar tests de webhook que cubran IMAGE:

```bash
grep -rn "IMAGE\|image\|NumMedia" tests/integration/test_webhook.py
```

Si NO hay test de webhook con IMAGE input, reportar como hallazgo IMPORTANTE.

**Resultado esperado:** ACK correcto, test presente o gap documentado.

---

### T6: Auditar config flags VISION_*

**Objetivo:** Los flags existen, tienen defaults correctos, y se usan donde deben.

**Paso 1:** Leer `src/core/config.py:47-49` y verificar:
- [ ] `VISION_ENABLED: bool` con default `"true"`
- [ ] `VISION_TIMEOUT: int` con default `"10"`
- [ ] Usan `_bool()` y `int()` correctamente
- [ ] Posicion: despues de GUARDRAILS_ON, antes de RAG_ENABLED

**Paso 2:** Verificar USO de los flags en el codigo:

```bash
grep -rn "VISION_ENABLED\|VISION_TIMEOUT" src/
```

Esperado:
- `config.py:48` — definicion
- `analyze_image.py:40` — `if not config.VISION_ENABLED`
- `pipeline.py` — posiblemente NO (usa analyze_image directamente)

**Paso 3:** VISION_TIMEOUT — Se usa?

Buscar `config.VISION_TIMEOUT` en `analyze_image.py`. Si NO se usa en la llamada a Gemini, reportar como hallazgo MENOR (el SDK tiene su propio timeout, pero el flag esta definido sin usar).

**Paso 4:** Buscar tests de config para VISION flags:

```bash
grep -rn "VISION" tests/unit/test_config.py
```

**Resultado esperado:** Flags correctos, VISION_TIMEOUT posible gap documentado.

---

### T7: No-regresion completa

**Objetivo:** CERO regresiones en la suite existente.

**Paso 1:** Ejecutar suite completa:

```bash
pytest tests/ -v --tb=short 2>&1 | tail -5
```

Esperado: `508 passed, 19 skipped, 5 xpassed` (o mas si se agregan tests).

**Paso 2:** Lint completo:

```bash
ruff check src/ tests/ --select E,F,W --ignore E501
```

Esperado: `All checks passed`

**Paso 3:** App boot:

```bash
PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('BOOT OK')"
```

Esperado: `BOOT OK`

**Paso 4:** Import chain:

```bash
PYTHONPATH=. python -c "from src.core.skills.analyze_image import analyze_image, ImageAnalysisResult, VISION_PROMPT; print('IMPORT OK')"
```

Esperado: `IMPORT OK`

**Resultado esperado:** 4/4 checks pasan.

---

## AGENTE 3: audit-docs — Documentacion + HTML + Consistencia

### T8: Auditar CLAUDE.md vs realidad

**Objetivo:** CLAUDE.md refleja el estado actual del proyecto con precision.

**Paso 1:** Contar flags reales en `config.py`:

```bash
grep -c "field(default_factory" src/core/config.py
```

CLAUDE.md dice "31 flags". Verificar match.

**Paso 2:** Contar skills reales:

```bash
ls src/core/skills/*.py | grep -v __pycache__ | wc -l
```

CLAUDE.md dice "12 skills atomicas". Verificar match.

**Paso 3:** Verificar conteo de tests:

```bash
pytest --co -q 2>&1 | tail -1
```

CLAUDE.md dice "532 collected (508 passed, 19 skipped, 5 xpassed)". Verificar match.

**Paso 4:** Verificar tabla de feature flags incluye VISION_*:

```bash
grep "VISION" CLAUDE.md
```

Debe tener `VISION_ENABLED` y `VISION_TIMEOUT`.

**Paso 5:** Verificar pipeline dice "12 skills":

```bash
grep "skills" CLAUDE.md | head -5
```

**Paso 6:** Verificar equipo humano:

CLAUDE.md muestra:
```
| Robert | Backend lead, pipeline, demo presenter |
| Marcos | Routes, Twilio, deploy, audio pipeline |
| Lucas  | KB research, testing, demo assets |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordination |
```

**ATENCION:** La desarrolladora dijo "solo lo he hecho yo (todo el proyecto)". Esta tabla puede ser incorrecta. Reportar como hallazgo IMPORTANTE — necesita decision de la usuaria.

**Resultado esperado:** Discrepancias documentadas.

---

### T9: Auditar presentacion HTML

**Objetivo:** Las presentaciones HTML reflejan el estado actual del proyecto.

**Paso 1:** Leer `presentacion/clara-pitch.html` y verificar:

| Dato | Valor actual en HTML | Valor real | Match? |
|------|---------------------|------------|--------|
| Tests | "469 tests" (slide 7) | 508+ passed | NO |
| Skills | ? | 12 skills | ? |
| Vision | mencionada? | Si, implementada | ? |
| Equipo | 5 personas (slide 10) | 1 persona (Andrea) | NO |

**Paso 2:** Leer `presentacion/demo-webapp.html` y verificar:
- [ ] Tiene boton/modo "Foto" (ademas de Escribir y Voz)
- [ ] Muestra respuesta de vision cuando se selecciona foto

**Paso 3:** Leer `presentacion/demo-whatsapp.html` y verificar:
- [ ] Muestra mensaje con imagen enviada por usuario
- [ ] Muestra respuesta de Clara analizando documento
- [ ] El flujo es realista (ACK -> analisis -> respuesta)

**Paso 4:** Documentar TODOS los datos desactualizados.

**NOTA:** NO modificar los HTML automaticamente. Reportar hallazgos para que la usuaria decida.

**Resultado esperado:** Lista de datos desactualizados en cada HTML.

---

### T10: Auditar templates de vision

**Objetivo:** Templates existen en 3 idiomas, son empaticos y accesibles.

**Paso 1:** Leer `src/core/prompts/templates.py:14-23` y verificar:

**ack_image:**
- [ ] Existe en es, fr, en
- [ ] Tiene emoji 📷 en los 3 idiomas
- [ ] Tono consistente con ack_text ("Un momento...") y ack_audio ("Estoy escuchando...")
- [ ] Lenguaje simple (accesible para personas vulnerables)

**vision_fail:**
- [ ] Existe en es, fr, en
- [ ] Ofrece alternativa ("describir lo que ves" o "escribir tu pregunta")
- [ ] Tono empatico (no culpa al usuario)
- [ ] Consistente con whisper_fail y llm_fail

**Paso 2:** Buscar tests de templates para vision:

```bash
grep -rn "ack_image\|vision_fail" tests/
```

Verificar que hay al menos 1 test por template por idioma.

**Paso 3:** Verificar que webhook usa el template correcto:

```bash
grep "ack_image" src/routes/webhook.py
```

**Resultado esperado:** Templates correctos, tests presentes.

---

## AGENTE 4: audit-final — Recopilacion + Reporte

> **EJECUTAR SOLO DESPUES DE QUE LOS 3 AGENTES ANTERIORES TERMINEN.**

### T11: Ejecutar gates finales

**Los 9 gates de verificacion:**

| Gate | Comando | Esperado |
|------|---------|----------|
| G1 | `pytest tests/unit/test_analyze_image.py -v` | 6+ passed |
| G2 | `pytest tests/unit/test_pipeline_image.py -v` | 3+ passed |
| G3 | `pytest tests/ --tb=short` | 508+ passed, 0 failed |
| G4 | `ruff check src/ tests/ --select E,F,W --ignore E501` | All checks passed |
| G5 | `PYTHONPATH=. python -c "from src.core.skills.analyze_image import analyze_image; print('OK')"` | OK |
| G6 | `PYTHONPATH=. python -c "from src.core.config import config; print(config.VISION_ENABLED, config.VISION_TIMEOUT)"` | True 10 |
| G7 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; print(get_template('ack_image', 'es'))"` | "Estoy analizando..." |
| G8 | `PYTHONPATH=. python -c "from src.app import create_app; create_app(); print('BOOT')"` | BOOT |
| G9 | `grep -c "analyze_image" src/core/pipeline.py` | >= 2 (import + uso) |

Ejecutar TODOS en paralelo. Reportar tabla de resultados.

---

### T12: Generar reporte de auditoria

**Paso 1:** Recopilar hallazgos de audit-unit, audit-integration, audit-docs.

**Paso 2:** Crear `docs/plans/evidence/VISION-AUDIT-REPORT.md`:

```markdown
# Vision Feature — Audit Report

**Fecha:** 2026-02-20
**Auditor:** Claude Code (multi-agent, 4 agentes)
**Commits auditados:** bf63940..8a4d297 (6 commits)
**Plan de referencia:** docs/plans/2026-02-20-vision-audit.md

## Resumen Ejecutivo

| Area | Estado | Hallazgos |
|------|--------|-----------|
| Tests unitarios (analyze_image) | [OK/GAPS] | X/Y branches cubiertos |
| Tests integracion (pipeline) | [OK/GAPS] | X/Y flujos cubiertos |
| VISION_PROMPT | [OK/ISSUE] | Checklist X/Y |
| Config flags | [OK/GAP] | VISION_TIMEOUT usage |
| Webhook ACK | [OK/GAP] | Test presente? |
| Templates | [OK/ISSUE] | 3 idiomas, tono |
| CLAUDE.md | [OK/DESYNC] | Conteos match? |
| HTML pitch | [DESYNC] | Tests count, equipo |
| HTML demos | [OK/NEEDS_WORK] | Vision flow |
| Lint | [OK] | 0 errores |
| No-regresion | [OK] | 508+ passed, 0 failed |

## Hallazgos por Severidad

### CRITICOS (bloquean demo)
- [lista o "Ninguno"]

### IMPORTANTES (deberian arreglarse antes de hackathon)
- [lista]

### MENORES (nice-to-have)
- [lista]

## Gates Finales

| Gate | Resultado |
|------|-----------|
| G1 | PASS/FAIL |
| G2 | PASS/FAIL |
| ... | ... |
| G9 | PASS/FAIL |

## Metricas

| Metrica | Valor |
|---------|-------|
| Tests passed | X |
| Tests skipped | X |
| Tests xpassed | X |
| Lint errors | 0 |
| Branches cubiertos | X/Y |
| Templates verificados | X/Y |

## Acciones Recomendadas

1. [Accion 1 — si hay hallazgos criticos]
2. [Accion 2 — si hay hallazgos importantes]
3. [Accion 3 — nice-to-haves]

## Conclusion

[1-2 parrafos resumiendo: la feature esta lista para demo? que falta?]
```

**Paso 3:** Commit del reporte:

```bash
git add docs/plans/evidence/VISION-AUDIT-REPORT.md
git commit -m "docs: add vision feature audit report — multi-agent verification"
```

---

## CONSTRAINTS

1. **NO modificar codigo de produccion** a menos que encuentres un BUG REAL que rompe funcionalidad
2. **NO modificar HTML** — solo reportar hallazgos para que la desarrolladora decida
3. **SI puedes agregar tests** para cubrir gaps criticos, pero documentar que son nuevos
4. **NO cambiar el VISION_PROMPT** — solo verificar que cumple los criterios
5. **Cada agente reporta hallazgos al audit-final** — no arreglan solos sin coordinar
6. **Formato de hallazgos ESTRICTO** — usar el template HALLAZGO [CRITICO|IMPORTANTE|MENOR]
7. **Si un gate falla, PARAR** y diagnosticar antes de continuar

## CONDICION DE ABORT

Antes de lanzar los 3 agentes paralelos, ejecutar este pre-check:

```bash
pytest tests/ -x -q --tb=short 2>&1 | tail -3
ruff check src/ tests/ --select E,F,W --ignore E501 2>&1 | tail -1
PYTHONPATH=. python -c "from src.app import create_app; create_app(); print('PRE-CHECK OK')" 2>&1
```

Si CUALQUIERA falla -> **ABORT**. La codebase esta rota y hay que arreglarla antes de auditar.

## CHECKLIST FINAL (audit-final verifica)

- [ ] 9/9 gates pasan
- [ ] 0 hallazgos CRITICOS (o todos resueltos)
- [ ] Hallazgos IMPORTANTES documentados con accion recomendada
- [ ] Reporte guardado en `docs/plans/evidence/VISION-AUDIT-REPORT.md`
- [ ] Commit limpio del reporte
- [ ] Resumen ejecutivo entregado a la desarrolladora
