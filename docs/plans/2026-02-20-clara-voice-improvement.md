# Clara Voice & Response Improvement Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Aplicar la guia de tono CLARA-TONE-VOICE-GUIDE.md al codigo real — system prompt, templates, VISION_PROMPT, demo cache y guardrails — para que Clara suene como "una amiga que trabaja en el ayuntamiento" en vez de un sistema robotico.

**Architecture:** 4 agentes paralelos. Cada uno toca un dominio independiente. Sin conflictos de merge.

**Tech Stack:** Python 3.11, Gemini 1.5 Flash, gTTS, pytest

---

## Diagnostico: 10 Gaps Encontrados

| # | Gap | Severidad | Impacto Demo |
|---|-----|-----------|--------------|
| 1 | system_prompt.py no tiene instrucciones de tono/calidez | CRITICO | LLM genera respuestas frias |
| 2 | Templates usan emojis (viola guia) y culpan al usuario | CRITICO | Jueces ven respuestas roboticas |
| 3 | VISION_PROMPT hardcoded en espanol, sin tono | IMPORTANTE | Vision sin empatia |
| 4 | demo_cache.json saludo = ejemplo "MALO" de la guia | CRITICO | Primera impresion en demo |
| 5 | 5 templates propuestos en docs no existen en codigo | IMPORTANTE | Sin cierre calido |
| 6 | Guardrails usan "consulte" (formal) vs "tu" (informal) | MENOR | Cambio de registro brusco |
| 7 | whisper_fail culpa al usuario, solo 1 opcion | IMPORTANTE | UX pobre en audio |
| 8 | llm_fail solo da telefonos (excluye sordos) | IMPORTANTE | Accesibilidad |
| 9 | Arabe ausente de templates, TTS, cache | FUTURO | No bloquea demo |
| 10 | gTTS es robotico vs objetivo de voz calida | FUTURO | No bloquea demo |

## Prioridades para Hackathon

**HACER AHORA (bloquea demo):** Gaps 1, 2, 3, 4, 5, 6, 7, 8
**DOCUMENTAR (post-hackathon):** Gaps 9, 10

---

## Lectura Obligatoria (TODOS los agentes)

| # | Archivo | Para que |
|---|---------|----------|
| 1 | `CLAUDE.md` | Contexto proyecto |
| 2 | `docs/08-marketing/CLARA-TONE-VOICE-GUIDE.md` | **LA BIBLIA** — tono, principios, ejemplos buenos/malos |
| 3 | `src/core/prompts/system_prompt.py` | Prompt actual del LLM |
| 4 | `src/core/prompts/templates.py` | Templates actuales |
| 5 | `src/core/skills/analyze_image.py` | VISION_PROMPT |
| 6 | `data/cache/demo_cache.json` | Respuestas que ven los jueces |

---

## Equipo (4 agentes)

| Agente | Tareas | Archivos que toca |
|--------|--------|-------------------|
| `tone-engineer` | T1, T2 | system_prompt.py, analyze_image.py |
| `template-engineer` | T3, T4 | templates.py, tests |
| `cache-engineer` | T5, T6 | demo_cache.json, guardrails.py |
| `verify-engineer` | T7 | Tests, gates, reporte |

## Dependencias

```
tone-engineer (T1,T2) ────────┐
template-engineer (T3,T4) ────├──> verify-engineer (T7)
cache-engineer (T5,T6) ───────┘
```

T1-T6 en paralelo. T7 espera a todos.

---

## T1: Inyectar tono en system_prompt.py (tone-engineer)

**Archivos:** `src/core/prompts/system_prompt.py`

**Que hacer:** Agregar bloque de tono ANTES de las reglas existentes. No borrar nada. Solo agregar.

**Bloque a agregar (despues del primer parrafo de identidad, antes de reglas):**

```python
TONO DE COMUNICACION:
- Habla como una amiga que trabaja en el ayuntamiento y explica las cosas con calma.
- Usa frases cortas (maximo 20 palabras por frase).
- Valida las emociones del usuario antes de dar informacion ("Entiendo que puede ser estresante...").
- Presenta los tramites como DERECHOS del usuario, no como obligaciones.
- Da siempre dos opciones cuando algo falla ("puedes intentar de nuevo o escribirme").
- Nunca digas: "es tu responsabilidad", "deberias haber...", "como ya te dije", "es complicado".
- Nunca uses jerga sin explicarla: si dices "empadronamiento", explica que es.
- Incluye siempre un telefono O una web como alternativa humana.
- Maximo 2 emojis por mensaje. Nunca en mensajes de error.
```

**Test:**
```python
def test_system_prompt_contains_tone_block():
    from src.core.prompts.system_prompt import SYSTEM_PROMPT
    assert "amiga" in SYSTEM_PROMPT.lower() or "ayuntamiento" in SYSTEM_PROMPT.lower()
    assert "DERECHOS" in SYSTEM_PROMPT

def test_system_prompt_has_never_say_rules():
    from src.core.prompts.system_prompt import SYSTEM_PROMPT
    assert "nunca" in SYSTEM_PROMPT.lower()
```

**Run:** `pytest tests/unit/test_system_prompt_tone.py -v`

**Commit:** `feat: add tone and warmth instructions to system prompt`

---

## T2: Mejorar VISION_PROMPT con tono y variable de idioma (tone-engineer)

**Archivos:** `src/core/skills/analyze_image.py`

**Problema actual:** VISION_PROMPT hardcoded en espanol, sin instrucciones de empatia. Un usuario asustado por una carta oficial recibe analisis clinico sin calidez.

**Nuevo VISION_PROMPT:**

```python
VISION_PROMPT = (
    "Eres Clara, una amiga que trabaja en el ayuntamiento y ayuda a personas "
    "en Espana con tramites del gobierno.\n\n"
    "Analiza esta imagen. Si es un documento oficial espanol "
    "(carta, formulario, notificacion, certificado, resolucion):\n"
    "1. Explica que tipo de documento es, en palabras sencillas\n"
    "2. Di que organismo lo envia\n"
    "3. Explica que debe hacer la persona (plazos, pasos), paso a paso\n"
    "4. Si necesita ayuda profesional, dilo con tranquilidad\n\n"
    "IMPORTANTE: Si el documento parece urgente o preocupante, "
    "empieza tranquilizando al usuario. Ejemplo: "
    "'Tranquilo/a, vamos a ver esto juntos.'\n\n"
    "Si NO es un documento administrativo, describe brevemente lo que ves "
    "y pregunta como puedes ayudar.\n\n"
    "Responde en {language}. Lenguaje simple (nivel de comprension: 12 anos). "
    "Maximo 200 palabras."
)
```

**Cambio en analyze_image():** Pasar `language` como parametro y hacer `.format(language=language)`.

```python
def analyze_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    language: str = "es",
) -> ImageAnalysisResult:
```

Y en la llamada a Gemini:
```python
genai.types.Part(text=VISION_PROMPT.format(language=language_name)),
```

Donde `language_name` mapea: `{"es": "espanol", "fr": "francais", "en": "English"}`.

**Cambio en pipeline.py:** Pasar `language` a `analyze_image()`:
```python
vision_result = analyze_image(media_bytes, msg.media_type or "image/jpeg", language)
```

**Tests:** Actualizar `test_analyze_image_calls_gemini_with_image_bytes` para verificar que el prompt contiene "amiga" y acepta language parameter.

**Run:** `pytest tests/unit/test_analyze_image.py -v`

**Commit:** `feat: add warmth and language support to VISION_PROMPT`

---

## T3: Reescribir templates existentes (template-engineer)

**Archivos:** `src/core/prompts/templates.py`, `tests/unit/test_templates.py`

**Principio:** Aplicar las reescrituras de CLARA-TONE-VOICE-GUIDE.md Section 5. Quitar emojis de ACKs y errores. Dar 2 opciones en fallos. Tono calido.

**Templates reescritos:**

```python
TEMPLATES = {
    "ack_text": {
        "es": "Lo miro ahora mismo, dame un momento.",
        "fr": "Je regarde tout de suite, un instant.",
        "en": "Looking into it right now, one moment.",
    },
    "ack_audio": {
        "es": "Estoy escuchando tu mensaje, un momento.",
        "fr": "J'ecoute votre message, un instant.",
        "en": "Listening to your message, one moment.",
    },
    "ack_image": {
        "es": "Voy a mirar tu imagen, dame un momento.",
        "fr": "Je regarde votre image, un instant.",
        "en": "Looking at your image, one moment.",
    },
    "vision_fail": {
        "es": "No he podido analizar la imagen. Puedes intentar enviarla de nuevo, o si prefieres, describeme lo que ves y te ayudo.",
        "fr": "Je n'ai pas pu analyser l'image. Vous pouvez reessayer, ou si vous preferez, decrivez-moi ce que vous voyez.",
        "en": "I couldn't analyze the image. You can try sending it again, or describe what you see and I'll help.",
    },
    "whisper_fail": {
        "es": "No he podido escuchar bien tu audio. Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta.",
        "fr": "Je n'ai pas pu bien entendre votre audio. Vous pouvez reessayer, ou ecrire votre question.",
        "en": "I couldn't hear your audio clearly. You can try again, or type your question if you prefer.",
    },
    "llm_fail": {
        "es": "Ha habido un problema con tu consulta. Prueba de nuevo en unos segundos. Tambien puedes consultar en administracion.gob.es o llamar al 060.",
        "fr": "Un probleme est survenu. Reessayez dans quelques secondes. Vous pouvez aussi consulter administracion.gob.es ou appeler le 060.",
        "en": "There was a problem with your query. Try again in a few seconds. You can also visit administracion.gob.es or call 060.",
    },
    "fallback_generic": {
        "es": "Puedo ayudarte con tramites y ayudas del gobierno espanol. Por ejemplo:\n1. Empadronamiento\n2. Tarjeta sanitaria\n3. Ayudas economicas (IMV)\n\nEscribeme sobre que necesitas informacion.",
        "fr": "Je peux vous aider avec les demarches du gouvernement espagnol. Par exemple:\n1. Empadronamiento\n2. Carte sanitaire\n3. Aides economiques (IMV)\n\nDites-moi ce dont vous avez besoin.",
        "en": "I can help with Spanish government procedures. For example:\n1. Registration (empadronamiento)\n2. Health card\n3. Financial aid (IMV)\n\nTell me what you need help with.",
    },
    "memory_optin_ask": {
        "es": "Para ayudarte mejor, puedo recordar tu consulta. Quieres que recuerde tu tramite? (Si/No)\n\nPuedes decir 'Olvida mis datos' en cualquier momento.",
        "fr": "Pour mieux vous aider, je peux memoriser votre consultation. Voulez-vous que je me souvienne? (Oui/Non)\n\nVous pouvez dire 'Oublie mes donnees' a tout moment.",
        "en": "To help you better, I can remember your case. Would you like me to remember? (Yes/No)\n\nYou can say 'Forget my data' at any time.",
    },
    "memory_optin_confirmed": {
        "es": "Perfecto, recordare tu consulta para ayudarte mejor. Puedes decir 'Olvida mis datos' cuando quieras.",
        "fr": "Parfait, je me souviendrai de votre consultation. Dites 'Oublie mes donnees' quand vous voulez.",
        "en": "Great, I'll remember your case. Say 'Forget my data' whenever you want.",
    },
    "memory_optin_declined": {
        "es": "Entendido, no guardare nada. Cada mensaje sera independiente. Estoy aqui para lo que necesites.",
        "fr": "Compris, je ne garderai rien. Chaque message sera independant. Je suis la pour vous.",
        "en": "Got it, I won't store anything. Each message will be independent. I'm here whenever you need.",
    },
    "memory_forgotten": {
        "es": "Tus datos han sido eliminados. Si necesitas ayuda con algun tramite, escribeme cuando quieras.",
        "fr": "Vos donnees ont ete supprimees. Si vous avez besoin d'aide, ecrivez-moi quand vous voulez.",
        "en": "Your data has been deleted. If you need help, write me anytime.",
    },
    "closing": {
        "es": "Me alegro de haberte ayudado. Si te surge otra duda, escribeme cuando quieras. Mucho animo con el tramite.",
        "fr": "Je suis contente de vous avoir aide. Si vous avez d'autres questions, ecrivez-moi. Bon courage!",
        "en": "Glad I could help. If you have more questions, write me anytime. Good luck!",
    },
}
```

**Cambios clave vs actual:**
- ACKs: Sin emojis. "Lo miro ahora mismo" vs "Procesando tu mensaje... hourglass"
- Fallos: 2 opciones siempre. Clara toma la culpa ("No he podido")
- llm_fail: Web + telefono (accesible para sordos)
- fallback_generic: Lista numerada de temas (no parrafo generico)
- memory_forgotten: Cierre calido vs "empieza de nuevo"
- NUEVO: template `closing` para cierre de conversacion

**Tests:** Actualizar tests existentes de templates (los asserts de emoji ya no aplican).

**Run:** `pytest tests/ -v --tb=short -k template`

**Commit:** `feat: rewrite all templates with warm, accessible tone per voice guide`

---

## T4: Agregar template closing al pipeline (template-engineer)

**Archivos:** `src/core/pipeline.py` (solo si aplica)

**Nota:** El template `closing` no necesita wiring automatico en el pipeline ahora — se puede usar manualmente o en futuras iteraciones cuando Clara detecte fin de conversacion. Solo verificar que `get_template("closing", "es")` funciona.

**Test:**
```python
def test_closing_template_exists():
    from src.core.prompts.templates import get_template
    result = get_template("closing", "es")
    assert "animo" in result.lower() or "alegro" in result.lower()
```

**Run:** `pytest tests/unit/test_templates.py -v`

**Commit:** (incluido en commit de T3)

---

## T5: Reescribir demo_cache.json (cache-engineer)

**Archivos:** `data/cache/demo_cache.json`

**Problema:** Las respuestas cacheadas son lo que los jueces ven. El saludo actual es el ejemplo "MALO" de la guia de voz.

**Reescrituras (solo texto, no tocar audio_file ni keywords):**

**saludo_es:**
```
Actual: "¡Hola! Soy Clara, tu asistente para trámites de servicios sociales en España. 😊 ..."
Nuevo:  "Hola, soy Clara. Estoy aquí para ayudarte con trámites y ayudas del gobierno español. Puedo ayudarte con empadronamiento, tarjeta sanitaria, ayudas económicas como el IMV, y mucho más. Escríbeme lo que necesitas, sin prisa."
```

**imv_es:**
```
Actual: "El Ingreso Mínimo Vital (IMV) es una prestación de la Seguridad Social que garantiza un nivel mínimo de ingresos a quienes se encuentran en situación de vulnerabilidad económica."
Nuevo:  "El IMV es una ayuda de dinero que te da el gobierno cada mes si tienes pocos ingresos. No es un préstamo — no tienes que devolverlo. Es tu derecho.\n\nPara pedirlo necesitas:\n1. Estar empadronado/a en España\n2. Tener ingresos bajos (depende del tamaño de tu familia)\n3. Ser mayor de 23 años (o tener hijos a cargo)\n\nPuedes solicitarlo en sede.seg-social.gob.es o llamando al 900 20 22 22."
```

**empadronamiento_es:** Reemplazar "El empadronamiento es el registro obligatorio" con "El empadronamiento es inscribirte en el pueblo o ciudad donde vives. Es tu derecho y es gratuito."

**IMPORTANTE:** No cambiar campos `id`, `keywords`, `audio_file`, `input_type`. Solo `respuesta`.

**Test:** Los tests de cache que verifican contenido pueden romper — actualizar asserts.

**Run:** `pytest tests/ -v --tb=short -k cache`

**Commit:** `feat: rewrite demo cache responses with warm, accessible tone`

---

## T6: Arreglar registro formal en guardrails (cache-engineer)

**Archivos:** `src/core/guardrails.py`

**Problema:** Usa "consulte" (formal) cuando la guia dice "tu" (informal).

**Cambios:**
```python
# Antes:
"Consulte con un profesional legal."
# Despues:
"Te recomiendo consultar con un profesional legal."

# Antes (post_check disclaimer):
"Consulte con un profesional cualificado o visite las fuentes oficiales"
# Despues:
"Te recomiendo consultar con un profesional o visitar las fuentes oficiales"
```

**Test:** Buscar tests de guardrails que verifiquen texto exacto — actualizar.

**Run:** `pytest tests/ -v --tb=short -k guardrail`

**Commit:** `fix: use informal register in guardrails per voice guide`

---

## T7: Verificacion final (verify-engineer)

**Ejecutar DESPUES de T1-T6.**

### Gates

| Gate | Comando | Esperado |
|------|---------|----------|
| G1 | `pytest tests/ --tb=short` | 508+ passed, 0 failed |
| G2 | `ruff check src/ tests/ --select E,F,W --ignore E501` | Clean |
| G3 | `PYTHONPATH=. python -c "from src.app import create_app; create_app(); print('OK')"` | OK |
| G4 | `grep -c "amiga\|ayuntamiento\|DERECHOS" src/core/prompts/system_prompt.py` | >= 1 |
| G5 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; t=get_template('ack_text','es'); assert 'hourglass' not in t and 'reloj' not in t; print(t)"` | Sin emoji |
| G6 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; print(get_template('closing','es'))"` | Existe |
| G7 | `python -c "import json; d=json.load(open('data/cache/demo_cache.json')); print([e['id'] for e in d])"` | IDs intactos |

**Commit:** `docs: update CLAUDE.md with voice improvement changes`

---

## Gaps Documentados (Post-Hackathon)

Estos NO se implementan ahora pero se documentan:

| Gap | Descripcion | Esfuerzo |
|-----|-------------|----------|
| Arabe | Agregar ar a templates, TTS lang_map, detect_lang, cache | 2-3h |
| TTS upgrade | Migrar de gTTS a ElevenLabs o Qwen3-TTS | 4-6h |
| Closing auto | Detectar fin de conversacion y enviar template closing | 1-2h |
| Empathy detect | Detectar frustracion y responder con empathy_acknowledge | 2-3h |

---

## Constraints

1. **NO romper tests existentes** — si un assert verifica texto exacto de template, actualizarlo
2. **NO cambiar IDs, keywords, ni audio_file en demo_cache.json** — solo campo `respuesta`
3. **NO agregar arabe ahora** — es post-hackathon
4. **NO cambiar engine TTS** — es post-hackathon
5. **Mantener max 200 palabras** en system prompt y VISION_PROMPT
6. **TDD:** test primero cuando sea posible, commit frecuente
