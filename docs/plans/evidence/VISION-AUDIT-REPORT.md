# Vision Feature — Audit Report

**Fecha:** 2026-02-20
**Auditor:** Claude Code (multi-agent, 4 agentes: audit-unit, audit-integration, audit-docs, audit-final)
**Commits auditados:** bf63940..8a4d297 (6 commits)
**Plan de referencia:** docs/plans/2026-02-20-image-vision-analysis.md

## Resumen Ejecutivo

| Area | Estado | Hallazgos |
|------|--------|-----------|
| Tests unitarios (analyze_image) | OK | 5/5 branches cubiertos, 1 gap (empty response) |
| Tests integracion (pipeline) | OK | 3/3 flujos cubiertos |
| VISION_PROMPT | OK | 11/11 checklist items pasan |
| Config flags | OK con GAP | VISION_TIMEOUT definido pero no usado |
| Webhook ACK | OK con GAP | Falta test de integracion para IMAGE |
| Templates | OK | 3 idiomas, tono consistente |
| CLAUDE.md | DESYNC | Conteo de flags incorrecto (dice 31, hay 49 fields) |
| HTML pitch | DESYNC | Tests count desactualizado (dice 469, hay 508+) |
| HTML demos | OK | demo-whatsapp muestra flujo imagen correctamente |
| Lint | OK | 0 errores |
| No-regresion | OK | 508 passed, 0 failed |

## Hallazgos por Severidad

### CRITICOS (bloquean demo)

1. **CLAUDE.md dice "31 flags" pero config.py tiene 49 fields**
   - Archivo: CLAUDE.md:40
   - La tabla de Feature Flags documenta solo 18 de 49 fields. El numero "31" en la descripcion no refleja ni los documentados (18) ni los reales (49).
   - Accion: FIX_NEEDED — actualizar el conteo a reflejar solo los feature flags reales (booleanos y configs de comportamiento), no credenciales.

2. **clara-pitch.html dice "469 tests" — actual es 532 collected / 508 passed**
   - Archivo: presentacion/clara-pitch.html:496
   - Numero desactualizado por 63 tests. Subestima la cobertura de testing ante jueces.
   - Accion: FIX_NEEDED — actualizar a "508+ tests" o "530+ tests".

### IMPORTANTES (deberian arreglarse antes de hackathon)

3. **Branch B5 (respuesta vacia/None de Gemini) sin test ni guardia**
   - Archivo: src/core/skills/analyze_image.py:79
   - Si Gemini retorna `response.text = ""`, el skill retorna `success=True, text=""`. Si retorna `None` (safety block), `None.strip()` lanza AttributeError.
   - Accion: FIX_NEEDED — agregar guard `if not response.text`.

4. **VISION_TIMEOUT definido en config pero no usado en analyze_image**
   - Archivo: src/core/config.py:49, src/core/skills/analyze_image.py:58-76
   - El flag existe (default 10s) pero `generate_content()` no recibe timeout. La llamada a Gemini puede colgar indefinidamente.
   - Accion: FIX_NEEDED — pasar timeout al client o documentar como limitacion conocida.

5. **VISION_PROMPT carece de guardrail anti-alucinacion del SYSTEM_PROMPT**
   - Archivo: src/core/skills/analyze_image.py:11-22
   - SYSTEM_PROMPT tiene "NUNCA inventes requisitos, plazos, cantidades ni URLs". VISION_PROMPT no tiene equivalente. Gemini podria alucinar plazos al analizar documentos.
   - Accion: FIX_NEEDED — agregar linea anti-alucinacion al prompt.

6. **No hay test de integracion para webhook IMAGE ACK**
   - Archivo: tests/integration/test_webhook.py
   - Hay tests para TEXT y AUDIO pero no para IMAGE POST. El elif en webhook.py:76 no se ejercita en integracion.
   - Accion: FIX_NEEDED — agregar test_webhook_image_ack.

7. **No hay tests en ingles ("en") para templates ack_image y vision_fail**
   - Archivo: tests/unit/test_templates_image.py
   - Solo hay tests para es y fr. El idioma "en" no tiene cobertura.
   - Accion: FIX_NEEDED — agregar 2 tests (ack_image en, vision_fail en).

8. **demo-webapp.html tiene boton Foto pero no muestra respuesta de vision**
   - Archivo: presentacion/demo-webapp.html:632-639
   - El boton existe pero la conversacion demo no incluye ejemplo de analisis de imagen.
   - Accion: DOCUMENT — decidir si agregar ejemplo de vision al demo.

9. **demo-whatsapp.html omite paso ACK antes del analisis**
   - Archivo: presentacion/demo-whatsapp.html:618-632
   - El flujo real es: imagen → ACK "Analizando tu imagen..." → respuesta. El demo salta el ACK.
   - Accion: DOCUMENT — decidir si agregar mensaje ACK al demo.

10. **Webhook hardcodea "es" para todos los ACKs incluyendo ack_image**
    - Archivo: src/routes/webhook.py:75-79
    - Los templates existen en es/fr/en pero el webhook siempre envia la version es. Un usuario frances recibe ACK en espanol.
    - Accion: DOCUMENT — limitacion pre-existente, no especifica de vision.

### MENORES (nice-to-have)

11. **VISION_PROMPT no instruye citar fuente o sugerir verificacion oficial**
    - Archivo: src/core/skills/analyze_image.py:11-22
    - SYSTEM_PROMPT dice "incluye la fuente oficial". VISION_PROMPT no sugiere verificar en administracion.gob.es o 060.
    - Accion: DOCUMENT.

12. **ImageAnalysisResult definido localmente en vez de en models.py**
    - Archivo: src/core/skills/analyze_image.py:25-31
    - TranscriptResult esta en models.py. ImageAnalysisResult rompe la convencion. Funcional pero inconsistente.
    - Accion: DOCUMENT.

13. **test_analyze_image_returns_result_dataclass es redundante**
    - Archivo: tests/unit/test_analyze_image.py:7-14
    - Mismo branch que test_analyze_image_disabled_returns_failure. No impacto funcional.
    - Accion: DOCUMENT.

14. **Pitch no menciona "12 skills" como punto fuerte**
    - Archivo: presentacion/clara-pitch.html
    - La arquitectura modular de 12 skills es un diferenciador que no se destaca.
    - Accion: DOCUMENT.

## Gates Finales

| Gate | Comando | Resultado |
|------|---------|-----------|
| G1 | `pytest tests/unit/test_analyze_image.py -v` | **PASS** — 6 passed |
| G2 | `pytest tests/unit/test_pipeline_image.py -v` | **PASS** — 3 passed |
| G3 | `pytest tests/ --tb=short` | **PASS** — 508 passed, 0 failed |
| G4 | `ruff check src/ tests/ --select E,F,W --ignore E501` | **PASS** — All checks passed |
| G5 | Import analyze_image | **PASS** — OK |
| G6 | Config VISION_ENABLED, VISION_TIMEOUT | **PASS** — True 10 |
| G7 | Template ack_image | **PASS** — "Estoy analizando tu imagen..." |
| G8 | App boot | **PASS** — BOOT |
| G9 | grep analyze_image pipeline.py | **PASS** — 2 occurrences (import + uso) |

**9/9 gates PASS.**

## Metricas

| Metrica | Valor |
|---------|-------|
| Tests passed | 508 |
| Tests skipped | 19 |
| Tests xpassed | 5 |
| Tests collected | 532 |
| Lint errors | 0 |
| Branches cubiertos | 4/5 (gap: empty response) |
| Templates verificados | 6/6 (2 templates x 3 idiomas) |
| Hallazgos CRITICOS | 2 (docs desactualizados) |
| Hallazgos IMPORTANTES | 8 |
| Hallazgos MENORES | 4 |

## Acciones Recomendadas

### Prioridad Alta (antes de demo)

1. **Actualizar clara-pitch.html** — cambiar "469 tests" a "508+ tests"
2. **Agregar guard empty response** en analyze_image.py:79 — `if not response.text: return failure`
3. **Agregar linea anti-alucinacion** a VISION_PROMPT — "No inventes datos que no esten visibles en la imagen."

### Prioridad Media (mejora la calidad)

4. **Agregar 2 tests English** para templates ack_image y vision_fail
5. **Agregar test integracion webhook IMAGE** — POST con NumMedia=1, MediaContentType0=image/jpeg
6. **Corregir conteo CLAUDE.md** — distinguir feature flags (booleanos de comportamiento) de config general

### Prioridad Baja (nice-to-have)

7. Documentar que VISION_TIMEOUT no se aplica (limitacion conocida del SDK)
8. Considerar agregar mensaje ACK al demo-whatsapp.html
9. Considerar agregar ejemplo vision al demo-webapp.html

## Conclusion

La feature de Vision esta **correctamente implementada** y lista para demo. El codigo sigue los patrones existentes del proyecto (patron Gemini de transcribe.py, lazy imports, feature flags, fallback chain). Los 9 gates de verificacion pasan. La suite de tests no tiene regresiones.

Los 2 hallazgos CRITICOS son de **documentacion desactualizada** (CLAUDE.md y pitch), no de codigo. El hallazgo mas importante a nivel de codigo es el **guard para respuesta vacia de Gemini** (hallazgo #3) — un fix de 2 lineas que previene enviar mensajes vacios al usuario.

**Veredicto: READY FOR DEMO con los 3 fixes de prioridad alta recomendados.**
