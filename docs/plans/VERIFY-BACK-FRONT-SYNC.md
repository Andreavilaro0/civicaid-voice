# PROMPT — Verificar Sincronizacion Backend ↔ Frontend (Clara Tone)

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres un **auditor de consistencia de tono** del proyecto **Clara / CivicAid Voice**. Tu trabajo es verificar que los mensajes de Clara en el **frontend** (5 archivos HTML de presentacion) coincidan con el tono del **backend** (system prompt, templates, cache, guardrails, TTS).

**NO modifiques ningun archivo.** Solo lee, compara, y genera un reporte.

## PASO 1: Leer archivos backend (la "fuente de verdad")

Lee estos 6 archivos completos:

```
src/core/prompts/system_prompt.py
src/core/prompts/templates.py
src/core/guardrails.py
data/cache/demo_cache.json
src/core/skills/analyze_image.py
src/core/skills/tts.py
```

De cada uno, extrae:
- **system_prompt.py**: El saludo que Clara usa, las reglas de NUNCA DIGAS, el patron E-V-I, los ejemplos de tono
- **templates.py**: El texto exacto de cada template (ack_text, ack_audio, ack_image, whisper_fail, llm_fail, fallback_generic, closing)
- **demo_cache.json**: La `respuesta` de `saludo_es`, `saludo_fr`, `imv_es`, `empadronamiento_es`, `maria_carta_vision`
- **guardrails.py**: Las respuestas de BLOCKED_PATTERNS y LEGAL_DISCLAIMER
- **analyze_image.py**: VISION_PROMPT_ES y VISION_PROMPT_FR
- **tts.py**: _GEMINI_VOICE_STYLE (si existe) y _GEMINI_VOICE_NAME

## PASO 2: Leer archivos frontend

Lee estos 5 archivos completos:

```
presentacion/demo-whatsapp.html
presentacion/demo-webapp.html
presentacion/demo-audioplayer.html
presentacion/clara-pitch.html
presentacion/clara-logo.html
```

Y este archivo de ruta:

```
src/routes/static_files.py
```

De cada HTML, extrae TODO el texto que aparece dentro de burbujas de Clara (`.bubble-clara`, `.bubble.from-them`, `.scenario-response`, etc.).

## PASO 3: Ejecutar 12 checks de consistencia

Ejecuta cada check y anota PASS o FAIL con evidencia:

### CHECK 1: Saludo coincide
**Regla:** El saludo de Clara en `demo_cache.json` (`saludo_es.respuesta`) debe ser semanticamente equivalente al saludo que aparece en `demo-whatsapp.html` y `demo-webapp.html`.
**Verifica:** El texto no tiene que ser identico, pero debe:
- Empezar con "Hola, soy Clara" (sin "!" excesivo)
- NO decir "asistente" ni "Bienvenido/a"
- Mencionar los 3 tramites (IMV, empadronamiento, tarjeta sanitaria)

### CHECK 2: Cero emojis en Clara (frontend)
**Regla:** Los mensajes de Clara en el frontend NO deben tener emojis. Busca:
- HTML entities: `&#x1F4B0;` `&#x1F4CB;` `&#x1F517;` `&#x2705;` y similares `&#x1F`
- Unicode emojis directos
- Excepcion: En `clara-pitch.html` los slides de "6 realidades" (slide 9) usan emojis como iconos de tarjeta, eso es aceptable (son labels de UI, no mensajes de Clara)
- Excepcion: En `clara-pitch.html` los checkmarks ✅ en listas de features son aceptables (visual aid en slides, no conversacion)

### CHECK 3: Registro informal (tu) en ES
**Regla:** Todos los mensajes de Clara en ES (backend Y frontend) usan "tu/puedes/necesitas", NUNCA "usted/puede/necesita" ni "consulte".
**Busca en todos los archivos:**
```
grep -in "consulte\|usted puede\|usted necesita" src/core/guardrails.py src/core/prompts/templates.py presentacion/*.html
```

### CHECK 4: Registro formal (vous) en FR
**Regla:** Mensajes en FR usan "vous/votre", NUNCA "tu/ton".
**Verifica en:** templates.py FR entries, demo_cache.json FR entries, VISION_PROMPT_FR.

### CHECK 5: E-V-I en respuestas largas
**Regla:** Las respuestas sustantivas (IMV, empadronamiento, vision) deben empezar con una frase empatica ANTES de dar informacion.
**Verifica en:**
- `demo_cache.json`: `imv_es` empieza con empatia?
- `demo_cache.json`: `empadronamiento_es` empieza con empatia?
- `demo_cache.json`: `maria_carta_vision` empieza con empatia?
- `demo-whatsapp.html`: El mensaje IMV de Clara empieza con empatia?
- `demo-whatsapp.html`: El mensaje de vision de Clara empieza con empatia?

### CHECK 6: Clara toma la culpa en errores
**Regla:** En templates de error, Clara dice "No he podido" (yo), NUNCA "No pudiste" (tu culpa).
**Verifica:** `whisper_fail`, `vision_fail`, `llm_fail` en templates.py.

### CHECK 7: 2 opciones en cada error
**Regla:** Cada template de error ofrece 2 alternativas ("puedes X, o si prefieres Y").
**Verifica:** whisper_fail, vision_fail, llm_fail todos tienen "o si prefieres" o equivalente.

### CHECK 8: Template "closing" existe
**Regla:** Debe existir un template `closing` en templates.py con ES, FR, EN.
**Ejecuta:**
```bash
PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; print(get_template('closing','es'))"
```

### CHECK 9: MIME types en static_files.py
**Regla:** `static_files.py` debe servir WAV (para Gemini TTS) ademas de MP3.
**Verifica:** Que el archivo NO tenga `mimetype="audio/mpeg"` hardcodeado, sino un diccionario/deteccion por extension que incluya `.wav`.

### CHECK 10: Tramites como DERECHOS
**Regla:** system_prompt.py dice "presenta tramites como DERECHOS". Verificar que:
- `demo_cache.json` empadronamiento dice "DERECHO" o "derecho"
- `demo-whatsapp.html` NO dice "obligatorio" en mensajes de Clara

### CHECK 11: Terminos tecnicos explicados
**Regla:** Jerga legal siempre con parentesis explicativo.
**Verifica al menos 1 ejemplo en:**
- `demo_cache.json`: "empadronamiento (registrarte en el municipio donde vives)"
- `demo-whatsapp.html` o `demo-webapp.html`: algun parentesis explicativo

### CHECK 12: TTS config existe
**Regla:** `src/core/config.py` debe tener un flag `TTS_ENGINE` y `tts.py` debe tener voice names y style prompts.
**Ejecuta:**
```bash
PYTHONPATH=. python -c "
from src.core.config import config
print('TTS_ENGINE:', getattr(config, 'TTS_ENGINE', 'NOT FOUND'))
"
```
```bash
PYTHONPATH=. python -c "
try:
    from src.core.skills.tts import _GEMINI_VOICE_NAME, _GEMINI_VOICE_STYLE
    print('VOICE ES:', _GEMINI_VOICE_NAME.get('es', 'NOT FOUND'))
    print('STYLE ES length:', len(_GEMINI_VOICE_STYLE.get('es', '')))
except ImportError:
    print('GEMINI TTS: NOT IMPLEMENTED')
"
```

## PASO 4: Generar reporte

Crea el archivo `docs/plans/evidence/VERIFY-BACK-FRONT-REPORT.md` con este formato:

```markdown
# Verificacion Backend ↔ Frontend — Reporte

**Fecha:** [fecha]
**Auditor:** Claude Code (verification agent)

## Resumen

| # | Check | Estado | Evidencia |
|---|-------|--------|-----------|
| 1 | Saludo coincide | PASS/FAIL | [breve] |
| 2 | Cero emojis Clara (front) | PASS/FAIL | [breve] |
| 3 | Registro tu (ES) | PASS/FAIL | [breve] |
| 4 | Registro vous (FR) | PASS/FAIL | [breve] |
| 5 | E-V-I en respuestas | PASS/FAIL | [breve] |
| 6 | Clara toma culpa | PASS/FAIL | [breve] |
| 7 | 2 opciones en errores | PASS/FAIL | [breve] |
| 8 | Template closing | PASS/FAIL | [breve] |
| 9 | MIME types WAV | PASS/FAIL | [breve] |
| 10 | Tramites = derechos | PASS/FAIL | [breve] |
| 11 | Terminos explicados | PASS/FAIL | [breve] |
| 12 | TTS config | PASS/FAIL | [breve] |

## Resultado Global

**X/12 checks pasados.**

## Issues Encontrados (si hay FAIL)

Para cada FAIL:
- **Archivo:** path exacto + linea
- **Problema:** que se encontro
- **Fix sugerido:** texto correcto

## Archivos Leidos

[lista de todos los archivos leidos]
```

## CONSTRAINTS

1. **NO modifiques ningun archivo** — solo lectura y reporte
2. **Lee TODOS los archivos listados** antes de empezar los checks
3. Si un check es ambiguo, marca como **WARN** con explicacion
4. Si un archivo no existe, marca los checks que dependen de el como **SKIP**
5. El reporte va en `docs/plans/evidence/VERIFY-BACK-FRONT-REPORT.md`
6. Ejecuta los comandos Python con `PYTHONPATH=.` desde la raiz del proyecto
