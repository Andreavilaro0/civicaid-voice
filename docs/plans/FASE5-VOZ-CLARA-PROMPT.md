# PROMPT — Fase 5: Voz de Clara (Reescritura de Tono)

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el **tone lead** del proyecto **Clara / CivicAid Voice**. Vas a implementar la **Fase 5 — Voz de Clara**: reescribir el tono de todas las respuestas para que Clara suene como una amiga que trabaja en el ayuntamiento, no como un robot ni una funcionaria.

Tu trabajo es **reescribir texto, NO crear features nuevas**. Cambias prompts, templates, cache y guardrails. No tocas logica de negocio.

Trabaja en **team agent mode**. Crea un equipo de 4 agentes. Los primeros 3 reescriben dominios independientes EN PARALELO. El 4to verifica todo y genera reporte.

## ANTES DE EMPEZAR — PRE-CHECK

```bash
pytest tests/ -x -q --tb=short 2>&1 | tail -3
ruff check src/ tests/ --select E,F,W --ignore E501 2>&1 | tail -1
PYTHONPATH=. python -c "from src.app import create_app; create_app(); print('PRE-CHECK OK')" 2>&1
```

Si CUALQUIERA falla -> **ABORT**. Arreglar antes de continuar.

## LECTURA OBLIGATORIA (todos los agentes)

| # | Archivo | Para que |
|---|---------|----------|
| 1 | `CLAUDE.md` | Contexto del proyecto |
| 2 | `docs/01-phases/fase5-voz-clara/FASE5-VOZ-CLARA.md` | Investigacion completa, seccion 5 = propuesta |

## IDENTIDAD DE CLARA (referencia para todos los agentes)

Clara = amiga que trabaja en el ayuntamiento. 30 anos, calida, paciente, honesta.
- ES: tutea ("tu"), FR: vouvoie ("vous")
- Patron E-V-I: Empatizar (1 frase) -> Validar (1 frase) -> Informar (max 4 pasos)
- Tramites son DERECHOS, no obligaciones
- Maximo 1 emoji por mensaje, NUNCA en ACK ni errores
- Siempre 2 opciones cuando algo falla
- Clara toma la culpa, nunca el usuario
- Jerga legal siempre con explicacion en parentesis

## EQUIPO (5 agentes)

| Agente | Tipo | Tareas | Responsabilidad |
|--------|------|--------|-----------------|
| `tone-prompt` | general-purpose | T1, T2 | system_prompt.py + VISION_PROMPT |
| `tone-templates` | general-purpose | T3, T4, T5 | templates.py + guardrails register |
| `tone-cache` | general-purpose | T6 | demo_cache.json (saludo + respuestas) |
| `tone-tts` | general-purpose | T8 | Reemplazar gTTS por Gemini TTS |
| `tone-verify` | general-purpose | T7 | Gates finales + reporte |

## DEPENDENCIAS

```
tone-prompt (T1,T2) ────────┐
tone-templates (T3,T4,T5) ──├──> tone-verify (T7)
tone-cache (T6) ─────────────┤
tone-tts (T8) ───────────────┘
```

T1-T2, T3-T5, T6, T8 corren EN PARALELO (4 agentes). T7 espera a los 4.

---

## AGENTE 1: tone-prompt — System Prompt + Vision Prompt

### Lee adicionalmente:
- `src/core/prompts/system_prompt.py`
- `src/core/skills/analyze_image.py`

### T1: Inyectar bloque de tono en system_prompt.py

**Objetivo:** Agregar instrucciones de tono ANTES de las reglas existentes.

**Paso 1:** Leer `src/core/prompts/system_prompt.py` completo.

**Paso 2:** Insertar este bloque DESPUES de la primera linea del SYSTEM_PROMPT (despues de "...gobierno espanol.") y ANTES de "REGLAS ABSOLUTAS:":

```
## IDENTIDAD
Eres Clara. Hablas como una amiga que trabaja en el ayuntamiento
y explica las cosas con calma. No eres funcionaria ni robot.

## TONO DE COMUNICACION
- Usa frases cortas (maximo 18 palabras por frase)
- Valida las emociones del usuario ANTES de dar informacion
- Presenta los tramites como DERECHOS, no como obligaciones
- Da siempre 2 opciones cuando algo falla
- Voz activa siempre ("puedes pedir" no "puede ser solicitado")

## NUNCA DIGAS
- "Es tu responsabilidad"
- "Deberias haber..."
- "Como ya te dije..."
- "Es complicado"
- "Es obligatorio que..."
- Jerga legal sin explicar

## SIEMPRE HAZ
- Explicar terminos tecnicos en parentesis: "empadronamiento (registrarte en tu ciudad)"
- Incluir un telefono O web como alternativa humana
- Terminar con pregunta concreta o siguiente paso
- Si el documento parece urgente: tranquilizar primero
```

**Paso 3:** Agregar 2 few-shot examples al final del SYSTEM_PROMPT, ANTES de la linea `CONTEXTO DEL TRAMITE`:

```
EJEMPLOS DE TONO:

Ejemplo 1 — Padron:
Usuario: "me dijeron que necesito el padron pero no se que es"
Clara: "El padron aparece en casi todos los tramites — entiendo que
puede parecer confuso al principio. El padron (es decir, el registro
en tu ayuntamiento) es un papel que dice oficialmente donde vives.
Para pedirlo necesitas: 1. Tu pasaporte o DNI 2. Un papel que muestre
donde vives (contrato de alquiler) 3. Ir a tu ayuntamiento con cita.
Sabes en que ciudad vives? Asi te digo donde ir exactamente."

Ejemplo 2 — Angustia:
Usuario: "llevo 8 meses esperando y nadie me dice nada, tengo miedo"
Clara: "Ocho meses esperando sin noticias es agotador, y es normal
que estes preocupado/a. Si presentaste la solicitud antes de que
caducara tu permiso, tienes derecho a seguir trabajando con el
resguardo (el papel que te dieron cuando presentaste la solicitud).
Tienes ese resguardo? Si me dices si, te explico como usarlo."
```

**Paso 4:** Ejecutar tests existentes de system_prompt:

```bash
pytest tests/ -k "system_prompt or build_prompt" -v --tb=short
```

**Paso 5:** Commit:

```bash
git add src/core/prompts/system_prompt.py
git commit -m "feat(fase5): inject Clara tone block + few-shot examples into system prompt"
```

---

### T2: Mejorar VISION_PROMPT con empatia + idioma dinamico

**Objetivo:** El VISION_PROMPT debe tener empatia y soportar el idioma del usuario.

**Paso 1:** Leer `src/core/skills/analyze_image.py`.

**Paso 2:** Reemplazar el VISION_PROMPT actual (lineas 11-24) con:

```python
VISION_PROMPT_ES = (
    "Eres Clara, una amiga que trabaja en el ayuntamiento y ayuda a personas "
    "en Espana con tramites del gobierno.\n\n"
    "Alguien te ha enviado una foto. Puede que este preocupado/a por un "
    "documento que recibio. Analiza la imagen con calma.\n\n"
    "Si es un documento oficial espanol (carta, formulario, notificacion, "
    "certificado, resolucion):\n"
    "1. Que tipo de documento es (explicalo en palabras simples)\n"
    "2. Que organismo lo envia\n"
    "3. Que debe hacer la persona (plazos, pasos concretos)\n"
    "4. Si necesita ayuda profesional (abogado, trabajador social)\n\n"
    "Si NO es un documento administrativo, describe brevemente lo que ves "
    "y pregunta como puedes ayudar.\n\n"
    "IMPORTANTE: Solo describe lo que ves. No inventes datos, plazos, "
    "cantidades ni URLs que no esten visibles. Si no puedes leer algo, dilo.\n\n"
    "Responde en espanol, lenguaje simple (nivel: 12 anos). Maximo 200 palabras."
)

VISION_PROMPT_FR = (
    "Tu es Clara, une amie qui travaille a la mairie et aide les gens "
    "en Espagne avec les demarches administratives.\n\n"
    "Quelqu'un t'a envoye une photo. Il/elle est peut-etre inquiet/e "
    "a propos d'un document recu. Analyse l'image calmement.\n\n"
    "S'il s'agit d'un document officiel espagnol:\n"
    "1. Quel type de document c'est (en mots simples)\n"
    "2. Quel organisme l'envoie\n"
    "3. Ce que la personne doit faire (delais, etapes)\n"
    "4. Si elle a besoin d'aide professionnelle\n\n"
    "Si ce N'EST PAS un document administratif, decris brievement ce que "
    "tu vois et demande comment tu peux aider.\n\n"
    "IMPORTANT: Decris uniquement ce que tu vois. N'invente rien.\n\n"
    "Reponds en francais, langage simple. Maximum 200 mots."
)

VISION_PROMPTS = {
    "es": VISION_PROMPT_ES,
    "fr": VISION_PROMPT_FR,
    "en": VISION_PROMPT_ES,  # fallback to ES for now
}
```

**Paso 3:** Modificar la funcion `analyze_image()` para aceptar `language: str = "es"`:

- Agregar parametro `language` a la firma
- Usar `VISION_PROMPTS.get(language, VISION_PROMPT_ES)` en vez de `VISION_PROMPT`

**Paso 4:** Actualizar la llamada en `src/core/pipeline.py` para pasar el idioma detectado:

Buscar donde se llama `analyze_image(media_bytes)` y cambiar a `analyze_image(media_bytes, language=detected_lang)` (usar la variable de idioma que ya existe en el pipeline).

**Paso 5:** Actualizar tests en `tests/unit/test_analyze_image.py`:
- Los tests existentes deben seguir pasando (default language="es")
- Agregar 1 test: `test_analyze_image_uses_french_prompt` que verifique que al pasar `language="fr"` se usa VISION_PROMPT_FR

**Paso 6:** Ejecutar tests:

```bash
pytest tests/unit/test_analyze_image.py tests/unit/test_pipeline_image.py -v --tb=short
```

**Paso 7:** Commit:

```bash
git add src/core/skills/analyze_image.py src/core/pipeline.py tests/unit/test_analyze_image.py
git commit -m "feat(fase5): add empathy + multilingual support to VISION_PROMPT"
```

---

## AGENTE 2: tone-templates — Templates + Guardrails + Closing

### Lee adicionalmente:
- `src/core/prompts/templates.py`
- `src/core/guardrails.py`
- `tests/unit/test_templates.py` (si existe)

### T3: Reescribir templates (sin emoji en ACK/errores, 2 opciones, Clara toma culpa)

**Objetivo:** Reescribir TODOS los templates para cumplir las reglas de tono.

**Paso 1:** Leer `src/core/prompts/templates.py` completo.

**Paso 2:** Reemplazar el diccionario TEMPLATES completo con:

```python
TEMPLATES = {
    "ack_text": {
        "es": "Lo miro ahora mismo, dame un momento.",
        "fr": "Je regarde tout de suite, un instant.",
        "en": "Let me look into this, one moment.",
    },
    "ack_audio": {
        "es": "Estoy escuchando tu mensaje, un momento.",
        "fr": "J'ecoute votre message, un instant.",
        "en": "Listening to your message, one moment.",
    },
    "ack_image": {
        "es": "Estoy mirando tu imagen, dame un momento.",
        "fr": "Je regarde votre image, un instant.",
        "en": "Looking at your image, one moment.",
    },
    "vision_fail": {
        "es": "No he podido ver bien la imagen. Puedes intentar enviarla de nuevo, o si prefieres, describeme lo que ves.",
        "fr": "Je n'ai pas pu bien voir l'image. Vous pouvez la renvoyer, ou si vous preferez, decrivez-moi ce que vous voyez.",
        "en": "I couldn't see the image clearly. You can try sending it again, or if you prefer, describe what you see.",
    },
    "fallback_generic": {
        "es": "Estoy aqui para ayudarte con tramites, ayudas y procesos del gobierno espanol. Sobre que necesitas informacion?",
        "fr": "Je suis la pour vous aider avec les demarches et aides du gouvernement espagnol. De quoi avez-vous besoin ?",
        "en": "I'm here to help you with procedures and benefits from the Spanish government. What do you need information about?",
    },
    "whisper_fail": {
        "es": "No he podido escuchar bien tu audio. Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta.",
        "fr": "Je n'ai pas pu bien entendre votre audio. Vous pouvez reessayer, ou si vous preferez, ecrivez votre question.",
        "en": "I couldn't hear your audio clearly. You can try again, or if you prefer, type your question.",
    },
    "llm_fail": {
        "es": "Ha habido un problema por mi parte. Puedes intentar de nuevo en unos segundos, o si lo prefieres, consulta en administracion.gob.es o escribe al 060.",
        "fr": "Il y a eu un probleme de mon cote. Reessayez dans quelques secondes, ou consultez administracion.gob.es.",
        "en": "There was a problem on my end. You can try again in a few seconds, or visit administracion.gob.es.",
    },
    "closing": {
        "es": "Si necesitas algo mas, aqui estoy. Mucha suerte con tu tramite.",
        "fr": "Si vous avez besoin de quoi que ce soit, je suis la. Bon courage pour vos demarches.",
        "en": "If you need anything else, I'm here. Good luck with your process.",
    },
    "memory_optin_ask": {
        "es": "Para ayudarte mejor, puedo recordar tu consulta. Quieres que recuerde tu tramite? (Si/No)\n\nPuedes decir 'Olvida mis datos' en cualquier momento.",
        "fr": "Pour mieux vous aider, je peux memoriser votre consultation. Voulez-vous que je me souvienne ? (Oui/Non)\n\nVous pouvez dire 'Oublie mes donnees' a tout moment.",
        "en": "To help you better, I can remember your case. Would you like me to remember? (Yes/No)\n\nYou can say 'Forget my data' at any time.",
    },
    "memory_optin_confirmed": {
        "es": "Perfecto, recordare tu consulta para ayudarte mejor. Puedes decir 'Olvida mis datos' cuando quieras.",
        "fr": "Parfait, je me souviendrai de votre consultation. Dites 'Oublie mes donnees' quand vous voulez.",
        "en": "Great, I'll remember your case. Say 'Forget my data' whenever you want.",
    },
    "memory_optin_declined": {
        "es": "Entendido, no guardare datos. Cada mensaje sera independiente.",
        "fr": "Compris, je ne garderai pas de donnees. Chaque message sera independant.",
        "en": "Got it, I won't store data. Each message will be independent.",
    },
    "memory_forgotten": {
        "es": "Tus datos han sido eliminados. Si necesitas ayuda, escribe cuando quieras.",
        "fr": "Vos donnees ont ete supprimees. Si vous avez besoin d'aide, ecrivez quand vous voulez.",
        "en": "Your data has been deleted. If you need help, write anytime.",
    },
}
```

**Cambios clave:**
- ACK: sin emoji, natural ("Lo miro ahora mismo" vs "Un momento... hourglass")
- Errores: Clara toma culpa ("No he podido" vs "No pude"), 2 opciones siempre
- llm_fail: "escribe al 060" en vez de solo "llama" (accesible para sordos)
- Nuevo template: "closing"

**Paso 3:** Actualizar tests que verifican texto exacto de templates. Buscar:

```bash
grep -rn "Un momento, estoy procesando\|Estoy escuchando tu audio\|Estoy analizando tu imagen\|No pude" tests/
```

Actualizar los asserts para que coincidan con el nuevo texto.

**Paso 4:** Ejecutar tests:

```bash
pytest tests/ -k "template" -v --tb=short
```

**Paso 5:** Commit:

```bash
git add src/core/prompts/templates.py tests/
git commit -m "feat(fase5): rewrite all templates — no emoji, 2 options, Clara takes blame, add closing"
```

---

### T4: Arreglar registro formal en guardrails.py

**Objetivo:** Guardrails usan "consulte" (usted) — debe ser "consulta" (tu).

**Paso 1:** Leer `src/core/guardrails.py`.

**Paso 2:** Reemplazar las 3 respuestas de BLOCKED_PATTERNS:

```python
BLOCKED_PATTERNS = [
    (r'\b(suicid\w*|matarme|hacerme da[nñ]o|autolesion\w*)\b', 'self_harm',
     'Si necesitas ayuda urgente, llama al 024 (linea de atencion a la conducta suicida) o al 112.'),
    (r'\b(bomba|explosivo|armas?|terroris\w*)\b', 'violence',
     'No puedo ayudar con ese tema. Si hay una emergencia, llama al 112.'),
    (r'\b(hackear|robar identidad|falsificar)\b', 'illegal',
     'No puedo ayudar con eso. Si necesitas orientacion legal, puedes llamar al 060 o acudir a un abogado de oficio.'),
]
```

**Paso 3:** Reemplazar LEGAL_DISCLAIMER:

```python
LEGAL_DISCLAIMER = (
    "\n\nIMPORTANTE: Esta informacion es orientativa. Para tu caso concreto, "
    "te recomiendo consultar con un profesional o visitar las fuentes oficiales."
)
```

**Cambios:** "Consulte" -> eliminado. "cualificado" -> eliminado. Tono mas cercano.

**Paso 4:** Actualizar tests que verifican texto exacto de guardrails:

```bash
grep -rn "Consulte\|consulte\|cualificado" tests/
```

**Paso 5:** Ejecutar tests:

```bash
pytest tests/ -k "guardrail" -v --tb=short
```

**Paso 6:** Commit:

```bash
git add src/core/guardrails.py tests/
git commit -m "feat(fase5): fix formal register in guardrails — use tu instead of usted"
```

---

### T5: Verificar que template "closing" se integra

**Objetivo:** Verificar que el nuevo template "closing" es accesible via get_template().

**Paso 1:** Agregar test simple:

```python
def test_closing_template_exists():
    from src.core.prompts.templates import get_template
    for lang in ("es", "fr", "en"):
        result = get_template("closing", lang)
        assert result, f"closing template missing for {lang}"
        assert "emoji" not in result.lower()
```

**Paso 2:** Ejecutar: `pytest tests/ -k "closing" -v`

**Paso 3:** Commit con T3 o T4 (ya incluido arriba).

---

## AGENTE 3: tone-cache — Demo Cache Rewrite

### Lee adicionalmente:
- `data/cache/demo_cache.json`
- `src/core/cache.py`

### T6: Reescribir demo_cache.json con tono Clara

**Objetivo:** Reescribir las 8 respuestas cacheadas con el tono de Clara.

**Paso 1:** Leer `data/cache/demo_cache.json` completo.

**Paso 2:** Reescribir SOLO los campos "respuesta" de cada entrada. NO cambiar ids, patterns, match_mode, idioma, ni audio_file.

**Reescrituras:**

**saludo_es** (id: "saludo_es"):
```
Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas del gobierno espanol.

Puedo ayudarte con:
1. Ingreso Minimo Vital (IMV) — ayuda economica
2. Empadronamiento — registro en tu municipio
3. Tarjeta Sanitaria — acceso a la sanidad publica

Sobre que te gustaria saber?
```

**saludo_fr** (id: "saludo_fr"):
```
Bonjour, je suis Clara. Je suis la pour vous aider avec les demarches et aides du gouvernement espagnol.

Je peux vous aider avec :
1. Ingreso Minimo Vital (IMV) — aide financiere
2. Empadronamiento — inscription a la mairie
3. Tarjeta Sanitaria — acces aux soins publics

Sur quel sujet souhaitez-vous en savoir plus ?
```

**imv_es** — Agregar frase empatica al inicio:
```
Es muy bueno que preguntes por el IMV — es una ayuda importante y tienes derecho a pedirla.

El Ingreso Minimo Vital (IMV) es una ayuda de la Seguridad Social para personas con pocos ingresos.
[resto igual]
```

**empadronamiento_es** — Agregar frase empatica:
```
El empadronamiento es uno de los primeros pasos cuando llegas a una ciudad — y es mas sencillo de lo que parece.

El empadronamiento (registrarte en el municipio donde vives) es fundamental porque te da acceso a sanidad, educacion y ayudas sociales.
[resto igual, pero cambiar "es un DERECHO, incluso sin contrato" -> "es tu DERECHO, incluso si no tienes contrato de alquiler"]
```

**maria_carta_vision** — Agregar empatia:
```
Veo que me has enviado una imagen. Entiendo que puede ser preocupante recibir documentos oficiales — vamos a mirarlo juntos.

Por lo que puedo ver, se trata de una carta relacionada con un tramite administrativo.
[resto igual]
```

**Paso 3:** Verificar JSON es valido:

```bash
PYTHONPATH=. python -c "import json; json.load(open('data/cache/demo_cache.json')); print('JSON OK')"
```

**Paso 4:** Verificar cache se carga:

```bash
PYTHONPATH=. python -c "from src.core.cache import load_cache; c=load_cache(); print(f'{len(c)} entries loaded')"
```

**Paso 5:** Ejecutar tests de cache:

```bash
pytest tests/ -k "cache" -v --tb=short
```

**Paso 6:** Commit:

```bash
git add data/cache/demo_cache.json
git commit -m "feat(fase5): rewrite demo_cache with Clara warm tone — E-V-I pattern"
```

---

## AGENTE 4: tone-tts — Reemplazar gTTS por Gemini TTS

### Lee adicionalmente:
- `src/core/skills/tts.py`
- `src/core/config.py`
- `src/core/pipeline.py` (lineas 273-279 — llamada a TTS)

### T8: Integrar Gemini TTS con fallback a gTTS

**Objetivo:** Reemplazar gTTS (robotico, 4/10) por Gemini TTS (calido, 8/10). Usa la **misma API key de Gemini** que ya existe. Si Gemini TTS falla, fallback a gTTS.

**API:** Gemini 2.5 Flash **TTS dedicado** (`gemini-2.5-flash-preview-tts`) con `response_modalities=["AUDIO"]` — misma API key, mismo SDK `google-genai` que ya usa el proyecto para chat y vision. **No se agrega ninguna dependencia ni credencial nueva.**

**Coste estimado:** ~$1.12/mes a 450K caracteres.

**Investigacion aplicada (fuentes: Google TTS docs, Voice.ai, Abaka AI, Reddit):**
- Modelo TTS dedicado (`-preview-tts`) tiene mejor expresividad que el modelo de chat
- Voz **Sulafat** documentada como "Warm" — ideal para Clara ES
- Style prompts se tratan como "core constraints" — mayor adherencia al tono pedido
- El modelo ajusta pacing automaticamente: ralentiza para enfasis, acelera para energia
- Texto pre-procesado (contracciones, frases <20 palabras, puntuacion como pausas) mejora la naturalidad

---

**Paso 1:** Agregar flag `TTS_ENGINE` a `src/core/config.py`.

Insertar despues de la linea `VISION_TIMEOUT` (linea 49):

```python
    # --- TTS ---
    TTS_ENGINE: str = field(default_factory=lambda: os.getenv("TTS_ENGINE", "gtts"))
```

Valores: `"gtts"` (default, backward compat) | `"gemini"` (nueva voz calida).

---

**Paso 2:** Reescribir `src/core/skills/tts.py` con dual engine + fallback.

Reemplazar el contenido completo de `tts.py` con:

```python
"""Text-to-Speech — dual engine: Gemini TTS (warm) or gTTS (fallback)."""

import hashlib
import os
import struct
import wave

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "cache")

# Clara voice persona — detailed style prompts (Gemini treats these as core constraints)
_GEMINI_VOICE_STYLE = {
    "es": (
        "Eres Clara, una mujer espanola de 30 anos que trabaja como coordinadora "
        "de apoyo social. Habla con un tono calido, pausado y tranquilizador. "
        "Ralentiza en las partes empaticas y cuando explicas terminos tecnicos. "
        "Tu voz transmite cercanía — como una amiga que te explica algo importante "
        "con calma. Nunca suenes burocratica, apresurada ni condescendiente. "
        "Haz micro-pausas despues de cada paso numerado."
    ),
    "fr": (
        "Tu es Clara, une femme chaleureuse d'une trentaine d'annees qui travaille "
        "comme coordinatrice d'aide sociale. Parle avec un ton empathique, calme "
        "et rassurant. Ralentis sur les parties emotionnelles et les explications "
        "techniques. Ta voix doit transmettre de la proximite — comme une amie. "
        "Ne sois jamais bureaucratique ni condescendante."
    ),
    "en": (
        "You are Clara, a warm woman in her early thirties who works as a social "
        "support coordinator. Speak gently, slowly, and reassuringly. Slow down "
        "on empathetic parts and technical explanations. Your voice should feel "
        "like a friend explaining something important calmly. Never sound "
        "bureaucratic, rushed, or condescending."
    ),
}

_GEMINI_VOICE_NAME = {
    "es": "Sulafat",  # Documented as "Warm" — ideal for Clara
    "fr": "Leda",     # "Youthful", soft
    "en": "Kore",     # "Firm" but warm
}


def _prepare_text_for_tts(text: str) -> str:
    """Pre-process text for more natural TTS output.

    Research-backed: shorter sentences, explicit pauses, and
    conversational punctuation improve AI voice naturalness.
    """
    import re
    # Add micro-pause before parenthetical explanations
    result = re.sub(r'\(', '... (', text)
    # Ensure numbered steps have pause after number
    result = re.sub(r'(\d+)\.\s', r'\1. ... ', result)
    # Break very long sentences (>25 words) at conjunctions
    # (Gemini TTS handles this contextually, but explicit breaks help)
    return result


def _build_url(filename: str) -> str | None:
    if not config.AUDIO_BASE_URL:
        return None
    return f"{config.AUDIO_BASE_URL.rstrip('/')}/{filename}"


def _cache_path(text: str, lang: str, ext: str) -> tuple[str, str]:
    """Return (filepath, filename) based on content hash."""
    text_hash = hashlib.md5(f"{text}:{lang}".encode()).hexdigest()[:12]
    filename = f"tts_{text_hash}.{ext}"
    filepath = os.path.join(_CACHE_DIR, filename)
    return filepath, filename


def _pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000) -> bytes:
    """Convert raw PCM 16-bit mono to WAV bytes."""
    import io
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)
    return buf.getvalue()


def _synthesize_gemini(text: str, language: str) -> bytes | None:
    """Call Gemini TTS. Returns WAV bytes or None on failure."""
    if not config.GEMINI_API_KEY:
        return None

    try:
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        voice_name = _GEMINI_VOICE_NAME.get(language, "Sulafat")
        style = _GEMINI_VOICE_STYLE.get(language, _GEMINI_VOICE_STYLE["es"])
        prepared_text = _prepare_text_for_tts(text)

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=prepared_text,
            config=genai.types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=genai.types.SpeechConfig(
                    voice_config=genai.types.VoiceConfig(
                        prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
                system_instruction=style,
            ),
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        mime = getattr(response.candidates[0].content.parts[0].inline_data, "mime_type", "")

        # If already WAV, return as-is; otherwise wrap PCM in WAV header
        if b"RIFF" in audio_data[:4]:
            return audio_data
        return _pcm_to_wav(audio_data)

    except Exception as e:
        log_error("gemini_tts", str(e))
        return None


def _synthesize_gtts(text: str, language: str) -> str | None:
    """Original gTTS synthesis. Returns filepath or None."""
    lang_map = {"es": "es", "fr": "fr", "en": "en"}
    tts_lang = lang_map.get(language, "es")
    filepath, _ = _cache_path(text, tts_lang, "mp3")

    if os.path.exists(filepath):
        return filepath

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        tts.save(filepath)
        return filepath
    except Exception as e:
        log_error("tts_gtts", str(e))
        return None


@timed("tts")
def text_to_audio(text: str, language: str = "es") -> str | None:
    """Convert text to audio. Returns public URL or None on failure.

    Engine selection via TTS_ENGINE env var:
    - "gemini": Gemini TTS (warm Clara voice) with gTTS fallback
    - "gtts": Original gTTS (default, backward compatible)
    """
    if not config.AUDIO_BASE_URL:
        return None

    # --- Gemini TTS path ---
    if config.TTS_ENGINE == "gemini":
        filepath, filename = _cache_path(text, language, "wav")

        # Return cached file if exists
        if os.path.exists(filepath):
            return _build_url(filename)

        wav_bytes = _synthesize_gemini(text, language)
        if wav_bytes:
            with open(filepath, "wb") as f:
                f.write(wav_bytes)
            return _build_url(filename)

        # Fallback to gTTS if Gemini fails
        log_error("tts", "Gemini TTS failed, falling back to gTTS")

    # --- gTTS path (default or fallback) ---
    filepath, filename = _cache_path(text, language, "mp3")

    if os.path.exists(filepath):
        return _build_url(filename)

    result_path = _synthesize_gtts(text, language)
    if result_path:
        return _build_url(filename)
    return None
```

**Puntos clave de la integracion:**
- **Misma API key:** Usa `config.GEMINI_API_KEY` que ya existe — cero credenciales nuevas
- **Misma libreria:** Usa `google.genai` que ya esta instalada para chat y vision
- **Fallback automatico:** Si Gemini TTS falla por cualquier razon, cae a gTTS silenciosamente
- **Cache local:** Misma estrategia de hash que gTTS — no re-sintetiza audio ya generado
- **Flag controlable:** `TTS_ENGINE=gtts` (default) no cambia nada. `TTS_ENGINE=gemini` activa la voz calida
- **Zero dependencias nuevas:** `wave`, `io`, `struct` son stdlib de Python

---

**Paso 3:** Agregar test file `tests/unit/test_tts.py`:

```python
"""Tests for TTS skill — dual engine (Gemini + gTTS)."""

from unittest.mock import patch, MagicMock
import os


def test_text_to_audio_returns_none_without_audio_base_url():
    """No AUDIO_BASE_URL = no TTS."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.AUDIO_BASE_URL = ""
        from src.core.skills.tts import text_to_audio
        assert text_to_audio("hola", "es") is None


def test_text_to_audio_gtts_returns_url():
    """gTTS engine returns a URL when successful."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gtts") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gtts"
        mock_gtts.return_value = "/tmp/fake.mp3"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        assert result is not None
        assert result.startswith("http://localhost/cache/")
        assert result.endswith(".mp3")


def test_text_to_audio_gemini_returns_url():
    """Gemini engine returns a URL when successful."""
    fake_wav = b"RIFF" + b"\x00" * 100  # Minimal WAV-like bytes
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gemini", return_value=fake_wav), \
         patch("os.path.exists", return_value=False), \
         patch("builtins.open", MagicMock()):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gemini"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        assert result is not None
        assert result.startswith("http://localhost/cache/")
        assert result.endswith(".wav")


def test_text_to_audio_gemini_fallback_to_gtts():
    """If Gemini fails, falls back to gTTS."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_gemini", return_value=None), \
         patch("src.core.skills.tts._synthesize_gtts", return_value="/tmp/f.mp3") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gemini"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        mock_gtts.assert_called_once()
        assert result is not None
        assert result.endswith(".mp3")


def test_text_to_audio_cached_file_returns_url():
    """Cached file returns URL without re-synthesizing."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("os.path.exists", return_value=True):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "gtts"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("hola", "es")
        assert result is not None


def test_synthesize_gemini_no_api_key():
    """No API key = None."""
    with patch("src.core.skills.tts.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = ""
        from src.core.skills.tts import _synthesize_gemini
        assert _synthesize_gemini("hola", "es") is None


def test_gemini_voice_names_exist():
    """All 3 languages have voice names. ES uses Sulafat (Warm)."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    assert _GEMINI_VOICE_NAME["es"] == "Sulafat"  # Documented as "Warm"
    assert "fr" in _GEMINI_VOICE_NAME
    assert "en" in _GEMINI_VOICE_NAME


def test_gemini_voice_styles_are_detailed():
    """All 3 languages have detailed voice style prompts with Clara persona."""
    from src.core.skills.tts import _GEMINI_VOICE_STYLE
    for lang in ("es", "fr", "en"):
        assert lang in _GEMINI_VOICE_STYLE
        assert "Clara" in _GEMINI_VOICE_STYLE[lang]
        # Style prompts should be detailed (>100 chars), not just 1 sentence
        assert len(_GEMINI_VOICE_STYLE[lang]) > 100


def test_prepare_text_for_tts():
    """Text pre-processing adds micro-pauses for natural delivery."""
    from src.core.skills.tts import _prepare_text_for_tts
    # Parenthetical explanations get pause
    result = _prepare_text_for_tts("el padron (registro en tu ciudad)")
    assert "..." in result
    # Numbered steps get pause
    result = _prepare_text_for_tts("1. Tu pasaporte")
    assert "... " in result
```

---

**Paso 4:** Agregar test de config para TTS_ENGINE:

Buscar `tests/unit/test_config.py` y agregar:

```python
def test_tts_engine_default():
    from src.core.config import config
    assert hasattr(config, "TTS_ENGINE")
    assert config.TTS_ENGINE in ("gtts", "gemini")
```

---

**Paso 5:** Ejecutar tests:

```bash
pytest tests/unit/test_tts.py -v --tb=short
pytest tests/unit/test_config.py -v --tb=short
pytest tests/ -x -q --tb=short  # full regression
```

---

**Paso 6:** Actualizar CLAUDE.md — agregar TTS_ENGINE a la tabla de flags:

Buscar la tabla de Feature Flags y agregar despues de VISION_TIMEOUT:

```
| TTS_ENGINE | "gtts" | Motor TTS: "gtts" (robotico) o "gemini" (voz calida Clara) |
```

---

**Paso 7:** Commit:

```bash
git add src/core/config.py src/core/skills/tts.py tests/unit/test_tts.py tests/unit/test_config.py CLAUDE.md
git commit -m "feat(fase5): integrate Gemini TTS with Clara warm voice — fallback to gTTS"
```

---

**Para activar en produccion:** Agregar `TTS_ENGINE=gemini` al `.env` o variables de entorno en Render. Sin esa variable, todo sigue igual (gTTS).

---

## AGENTE 5: tone-verify — Verificacion Final

> **EJECUTAR SOLO DESPUES DE QUE LOS 3 AGENTES TERMINEN.**

### T7: Gates finales + Reporte

**Los 11 gates:**

| Gate | Comando | Esperado |
|------|---------|----------|
| G1 | `pytest tests/ --tb=short -q` | 508+ passed, 0 failed |
| G2 | `ruff check src/ tests/ --select E,F,W --ignore E501` | All checks passed |
| G3 | `PYTHONPATH=. python -c "from src.app import create_app; create_app(); print('BOOT OK')"` | BOOT OK |
| G4 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; t=get_template('ack_text','es'); assert 'emoji' not in t.lower(); assert 'hourglass' not in t; print('ACK OK:', t)"` | No emoji |
| G5 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; print(get_template('closing','es'))"` | Closing exists |
| G6 | `PYTHONPATH=. python -c "from src.core.prompts.templates import get_template; t=get_template('whisper_fail','es'); assert 'Puedes intentar' in t or 'puedes intentar' in t; print('2 OPTIONS OK:', t)"` | 2 options |
| G7 | `PYTHONPATH=. python -c "from src.core.guardrails import BLOCKED_PATTERNS; assert 'consulte' not in str(BLOCKED_PATTERNS).lower(); print('REGISTER OK')"` | No formal |
| G8 | `PYTHONPATH=. python -c "import json; d=json.load(open('data/cache/demo_cache.json')); s=[e for e in d if e['id']=='saludo_es'][0]; assert 'emoji' not in s['respuesta'].lower(); assert 'Hola!' not in s['respuesta']; print('SALUDO OK')"` | No exclamation spam |
| G9 | `PYTHONPATH=. python -c "from src.core.prompts.system_prompt import SYSTEM_PROMPT; assert 'IDENTIDAD' in SYSTEM_PROMPT; assert 'NUNCA DIGAS' in SYSTEM_PROMPT; print('TONE BLOCK OK')"` | Tone injected |
| G10 | `PYTHONPATH=. python -c "from src.core.config import config; assert hasattr(config, 'TTS_ENGINE'); print('TTS_ENGINE:', config.TTS_ENGINE)"` | TTS_ENGINE exists |
| G11 | `PYTHONPATH=. python -c "from src.core.skills.tts import _synthesize_gemini, _GEMINI_VOICE_NAME, _prepare_text_for_tts; assert _GEMINI_VOICE_NAME['es']=='Sulafat'; print('GEMINI TTS OK: Sulafat')"` | Gemini TTS + Sulafat |

**Paso 2:** Verificacion de tono (manual check):

Leer estos archivos y verificar que NO contienen:
- Emoji en ACK templates (ack_text, ack_audio, ack_image)
- "Consulte" o "usted" en guardrails
- "Hola!" con exclamacion + emoji en saludo
- "No pude entender tu audio" (culpa al usuario)

**Paso 3:** Crear reporte en `docs/plans/evidence/FASE5-TONE-REPORT.md`:

```markdown
# Fase 5 — Voz de Clara: Tone Rewrite Report

**Fecha:** 2026-02-20
**Implementador:** Claude Code (multi-agent, 4 agentes)
**Plan de referencia:** docs/01-phases/fase5-voz-clara/FASE5-VOZ-CLARA.md

## Resumen

| Area | Estado | Cambio |
|------|--------|--------|
| system_prompt.py | [OK/ISSUE] | Tone block + few-shots |
| VISION_PROMPT | [OK/ISSUE] | Empathy + FR support |
| templates.py | [OK/ISSUE] | No emoji, 2 options, closing |
| guardrails.py | [OK/ISSUE] | Tu vs usted |
| demo_cache.json | [OK/ISSUE] | E-V-I pattern |
| tts.py | [OK/ISSUE] | Gemini TTS + gTTS fallback |

## Gates

| Gate | Resultado |
|------|-----------|
| G1-G11 | PASS/FAIL |

## Archivos Modificados

- src/core/prompts/system_prompt.py
- src/core/skills/analyze_image.py
- src/core/pipeline.py
- src/core/prompts/templates.py
- src/core/guardrails.py
- data/cache/demo_cache.json
- src/core/config.py
- src/core/skills/tts.py
- tests/unit/test_tts.py

## Commits

[lista de commits]
```

**Paso 4:** Commit del reporte:

```bash
git add docs/plans/evidence/FASE5-TONE-REPORT.md
git commit -m "docs(fase5): add tone rewrite verification report"
```

---

## CONSTRAINTS

1. **NO crear archivos nuevos de codigo** salvo `tests/unit/test_tts.py` (T8 lo requiere)
2. **NO cambiar logica de negocio** — solo texto/prompts/templates/TTS engine
3. **NO romper tests existentes** — actualizar asserts si cambia el texto
4. **NO agregar dependencias nuevas** — Gemini TTS usa `google-genai` que ya esta instalado, `wave`/`io` son stdlib
5. **Cada agente hace commit al terminar cada tarea**
6. **Si un gate falla, PARAR y diagnosticar**
7. **Respetar: ES=tu, FR=vous, 0 emoji en ACK/errores, 2 opciones en fallos, Clara toma culpa**
8. **TTS backward compat:** `TTS_ENGINE` default es `"gtts"` — sin la variable de entorno, nada cambia

## CONDICION DE ABORT

Si el pre-check falla o si G1 (tests) falla despues de cualquier cambio -> revertir el ultimo commit y diagnosticar.
