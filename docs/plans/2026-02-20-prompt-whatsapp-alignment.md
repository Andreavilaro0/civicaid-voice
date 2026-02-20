# Prompt WhatsApp Alignment — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Alinear todo el pipeline Twilio/WhatsApp con el nuevo system prompt E-V-I de Clara.

**Architecture:** 6 cambios quirurgicos: (1) ACK multilingue en webhook, (2) templates con tono E-V-I, (3) vision prompt alineado, (4) guardrails con tono calido, (5) formateo WhatsApp en respuestas, (6) tests. Ningun cambio rompe la firma de `build_prompt()` ni el flujo del pipeline.

**Tech Stack:** Python 3.11, Flask, Twilio, Gemini 2.5 Flash, pytest

---

### Task 1: ACK multilingue en webhook

El ACK de WhatsApp esta hardcodeado a `"es"` (lineas 74-79 de webhook.py). Usuarios franceses reciben "Lo miro ahora mismo" en vez de "Je regarde tout de suite".

**Files:**
- Modify: `src/routes/webhook.py:74-79`
- Test: `tests/integration/test_webhook.py`

**Step 1: Write the failing test**

Agregar al final de `tests/integration/test_webhook.py`:

```python
def test_webhook_ack_french_for_french_text(client):
    """ACK should be in French when user writes in French."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Bonjour, j'ai besoin d'aide",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        # Should contain French ACK, not Spanish
        assert "un instant" in resp.data.decode("utf-8")


def test_webhook_ack_spanish_for_spanish_text(client):
    """ACK should remain Spanish for Spanish text."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Hola necesito ayuda",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        assert "momento" in resp.data.decode("utf-8")


def test_webhook_ack_defaults_spanish_for_audio(client):
    """Audio ACK defaults to Spanish (can't detect language from audio body)."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx",
            "MediaContentType0": "audio/ogg",
        })
        assert resp.status_code == 200
        assert "momento" in resp.data.decode("utf-8")
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/integration/test_webhook.py::test_webhook_ack_french_for_french_text -v`
Expected: FAIL — currently returns Spanish ACK for French text.

**Step 3: Implement ACK language detection**

In `src/routes/webhook.py`, replace lines 73-79 with:

```python
    # Detect ACK language from message body (lightweight keyword check)
    from src.core.skills.detect_lang import _keyword_hint
    ack_lang = _keyword_hint(body) or "es"

    # ACK template based on input type
    if input_type == InputType.AUDIO:
        ack_text = get_template("ack_audio", ack_lang)
    elif input_type == InputType.IMAGE:
        ack_text = get_template("ack_image", ack_lang)
    else:
        ack_text = get_template("ack_text", ack_lang)
```

Note: We use `_keyword_hint` (fast, no external lib) instead of `detect_language` (uses langdetect, slower). The ACK must be instant (<50ms). For audio/image with empty body, defaults to "es" which is correct.

**Step 4: Run tests to verify they pass**

Run: `pytest tests/integration/test_webhook.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/routes/webhook.py tests/integration/test_webhook.py
git commit -m "fix: multilingual ACK in webhook — detect FR from message body"
```

---

### Task 2: Templates con tono E-V-I calido

Los templates actuales son funcionales pero frios. Alinear con la voz de Clara.

**Files:**
- Modify: `src/core/prompts/templates.py`
- Test: `tests/unit/test_templates_image.py` (ya cubre templates, verificar que no rompe)

**Step 1: Write the failing test**

Agregar nuevo archivo `tests/unit/test_templates_tone.py`:

```python
"""Tests: templates match Clara E-V-I tone."""

from src.core.prompts.templates import get_template, TEMPLATES


def test_all_templates_have_es_fr_en():
    """Every template key has ES, FR, and EN versions."""
    for key, langs in TEMPLATES.items():
        assert "es" in langs, f"{key} missing 'es'"
        assert "fr" in langs, f"{key} missing 'fr'"
        assert "en" in langs, f"{key} missing 'en'"


def test_error_templates_offer_alternative():
    """Error templates should always offer an alternative action."""
    error_keys = ["vision_fail", "whisper_fail", "llm_fail"]
    for key in error_keys:
        es = get_template(key, "es")
        assert "puedes" in es.lower() or "intentar" in es.lower() or "alternativa" in es.lower(), \
            f"{key}/es should offer alternative"


def test_ack_templates_not_empty():
    """ACK templates should be non-empty for all languages."""
    ack_keys = ["ack_text", "ack_audio", "ack_image"]
    for key in ack_keys:
        for lang in ["es", "fr", "en"]:
            val = get_template(key, lang)
            assert len(val) > 5, f"{key}/{lang} is too short or empty"


def test_closing_template_is_warm():
    """Closing template should feel warm and encouraging."""
    es = get_template("closing", "es")
    assert "suerte" in es.lower() or "animo" in es.lower() or "mucho" in es.lower()
```

**Step 2: Run tests to verify current state**

Run: `pytest tests/unit/test_templates_tone.py -v`
Expected: Should mostly pass (existing templates are decent). If any fail, note which.

**Step 3: Update templates**

Replace the full `TEMPLATES` dict in `src/core/prompts/templates.py`:

```python
TEMPLATES = {
    "ack_text": {
        "es": "Dame un momento, estoy buscando esa informacion.",
        "fr": "Un instant, je cherche cette information.",
        "en": "One moment, I'm looking into this.",
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
        "es": "No he podido ver bien la imagen. Puedes intentar enviarla de nuevo, o si prefieres, describeme lo que ves y te ayudo.",
        "fr": "Je n'ai pas pu bien voir l'image. Vous pouvez la renvoyer, ou si vous preferez, decrivez-moi ce que vous voyez.",
        "en": "I couldn't see the image clearly. You can try sending it again, or describe what you see and I'll help.",
    },
    "fallback_generic": {
        "es": "Estoy aqui para ayudarte con tramites, ayudas y procesos del gobierno espanol. Que necesitas?",
        "fr": "Je suis la pour vous aider avec les demarches et aides du gouvernement espagnol. De quoi avez-vous besoin?",
        "en": "I'm here to help you with procedures and benefits from the Spanish government. What do you need?",
    },
    "whisper_fail": {
        "es": "No he podido escuchar bien tu audio. Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta.",
        "fr": "Je n'ai pas pu bien entendre votre audio. Vous pouvez reessayer, ou si vous preferez, ecrivez votre question.",
        "en": "I couldn't hear your audio clearly. You can try again, or type your question.",
    },
    "llm_fail": {
        "es": "Ha habido un problema por mi parte. Puedes intentar de nuevo en unos segundos, o consulta en administracion.gob.es o llama al 060.",
        "fr": "Il y a eu un probleme de mon cote. Reessayez dans quelques secondes, ou consultez administracion.gob.es.",
        "en": "There was a problem on my end. You can try again in a few seconds, or visit administracion.gob.es.",
    },
    "closing": {
        "es": "Si necesitas algo mas, aqui estoy. Mucho animo con tu tramite.",
        "fr": "Si vous avez besoin de quoi que ce soit, je suis la. Bon courage pour vos demarches.",
        "en": "If you need anything else, I'm here. Good luck with your process.",
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

Changes: `ack_text` ES ligeramente mas natural, `closing` ES "Mucho animo" (mas calido que "Mucha suerte"), `vision_fail` ES agrega "y te ayudo".

**Step 4: Run ALL tests**

Run: `pytest tests/ -x -q --tb=short`
Expected: ALL PASS (535+)

**Step 5: Commit**

```bash
git add src/core/prompts/templates.py tests/unit/test_templates_tone.py
git commit -m "feat: align templates with Clara E-V-I tone"
```

---

### Task 3: Vision prompt alineado con E-V-I

El vision prompt en `analyze_image.py` tiene identidad de Clara pero no sigue el patron E-V-I. Alinear.

**Files:**
- Modify: `src/core/skills/analyze_image.py:11-48`
- Test: `tests/unit/test_analyze_image.py`

**Step 1: Write the failing test**

Agregar al final de `tests/unit/test_analyze_image.py`:

```python
def test_vision_prompt_contains_evi_guidance():
    """Vision prompt should guide Clara to empathize before informing."""
    from src.core.skills.analyze_image import VISION_PROMPT_ES, VISION_PROMPT_FR
    # ES prompt should mention calming/empathy before steps
    assert "tranquil" in VISION_PROMPT_ES.lower() or "calma" in VISION_PROMPT_ES.lower()
    # FR prompt should mention calming/empathy
    assert "calm" in VISION_PROMPT_FR.lower() or "rassur" in VISION_PROMPT_FR.lower()


def test_vision_prompt_anti_hallucination():
    """Vision prompt must have anti-hallucination rule."""
    from src.core.skills.analyze_image import VISION_PROMPT_ES
    assert "no inventes" in VISION_PROMPT_ES.lower() or "solo describe" in VISION_PROMPT_ES.lower()
```

**Step 2: Run tests to check current state**

Run: `pytest tests/unit/test_analyze_image.py -v`
Expected: Anti-hallucination test should pass (already has "Solo describe"). E-V-I test may fail if "calma" or "tranquil" not present.

**Step 3: Update vision prompts**

Replace `VISION_PROMPT_ES` and `VISION_PROMPT_FR` in `src/core/skills/analyze_image.py`:

```python
VISION_PROMPT_ES = (
    "Eres Clara, una amiga que trabaja en el ayuntamiento y ayuda a personas "
    "en Espana con tramites del gobierno.\n\n"
    "Alguien te ha enviado una foto. Puede que este preocupado/a por un "
    "documento que recibio. Primero tranquiliza ('Vamos a verlo con calma'), "
    "luego analiza la imagen.\n\n"
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
    "Quelqu'un vous a envoye une photo. Il/elle est peut-etre inquiet/e "
    "a propos d'un document recu. D'abord rassurez ('On va regarder ca "
    "calmement'), puis analysez l'image.\n\n"
    "S'il s'agit d'un document officiel espagnol:\n"
    "1. Quel type de document c'est (en mots simples)\n"
    "2. Quel organisme l'envoie\n"
    "3. Ce que la personne doit faire (delais, etapes)\n"
    "4. Si elle a besoin d'aide professionnelle\n\n"
    "Si ce N'EST PAS un document administratif, decrivez brievement ce que "
    "vous voyez et demandez comment vous pouvez aider.\n\n"
    "IMPORTANT: Decrivez uniquement ce que vous voyez. N'inventez rien.\n\n"
    "Repondez en francais, langage simple. Maximum 200 mots."
)
```

Cambios clave:
- ES: Agrega "Primero tranquiliza ('Vamos a verlo con calma')" antes de analizar — patron E-V-I.
- FR: Agrega "D'abord rassurez ('On va regarder ca calmement')" — patron E-V-I. Cambia tuteo a vouvoiement ("vous" en vez de "tu") para alinear con las reglas del system prompt.

**Step 4: Run tests**

Run: `pytest tests/unit/test_analyze_image.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/core/skills/analyze_image.py tests/unit/test_analyze_image.py
git commit -m "feat: align vision prompt with E-V-I pattern and FR vouvoiement"
```

---

### Task 4: Guardrails con tono calido

Las respuestas de guardrails son funcionales pero frias. Alinear con Clara.

**Files:**
- Modify: `src/core/guardrails.py:17-24`
- Test: `tests/unit/test_guardrails.py`

**Step 1: Write the failing test**

Agregar al final de `tests/unit/test_guardrails.py`:

```python
def test_guardrail_responses_offer_help():
    """Guardrail block responses should always offer a help resource."""
    from src.core.guardrails import BLOCKED_PATTERNS
    for _, category, response in BLOCKED_PATTERNS:
        assert any(word in response.lower() for word in ["llama", "112", "024", "060"]), \
            f"Category '{category}' guardrail should include a help resource"


def test_guardrail_self_harm_is_empathetic():
    """Self-harm guardrail should be empathetic, not cold."""
    from src.core.guardrails import BLOCKED_PATTERNS
    for _, category, response in BLOCKED_PATTERNS:
        if category == "self_harm":
            assert "ayuda" in response.lower() or "necesitas" in response.lower()
```

**Step 2: Run tests to check current state**

Run: `pytest tests/unit/test_guardrails.py -v`
Expected: Should pass — current responses already include help numbers.

**Step 3: Update guardrail responses**

In `src/core/guardrails.py`, update `BLOCKED_PATTERNS`:

```python
BLOCKED_PATTERNS = [
    (r'\b(suicid\w*|matarme|hacerme da[nñ]o|autolesion\w*)\b', 'self_harm',
     'Entiendo que estas pasando por un momento muy dificil. No estas solo/a. '
     'Llama al 024 (linea de atencion a la conducta suicida) o al 112. Hay personas preparadas para ayudarte.'),
    (r'\b(bomba|explosivo|armas?|terroris\w*)\b', 'violence',
     'No puedo ayudar con ese tema. Si hay una emergencia, llama al 112.'),
    (r'\b(hackear|robar identidad|falsificar)\b', 'illegal',
     'No puedo ayudar con eso. Si necesitas orientacion legal gratuita, llama al 060 o pide un abogado de oficio en tu juzgado mas cercano.'),
]
```

Cambio clave: `self_harm` respuesta ahora empieza con empatia ("Entiendo que estas pasando por un momento muy dificil. No estas solo/a.") — patron E-V-I aplicado incluso en guardrails. `illegal` agrega "gratuita" y opcion concreta.

**Step 4: Run ALL tests**

Run: `pytest tests/ -x -q --tb=short`
Expected: ALL PASS. **ATENCION:** si algun test verifica el texto exacto de las guardrail responses, actualizarlo tambien.

**Step 5: Commit**

```bash
git add src/core/guardrails.py tests/unit/test_guardrails.py
git commit -m "feat: guardrail responses with E-V-I empathy pattern"
```

---

### Task 5: Formateo WhatsApp para respuestas

WhatsApp soporta formato: *bold*, _italic_, ~strikethrough~, ```monospace```. Clara deberia usar *bold* para pasos clave y terminos importantes.

**Files:**
- Create: `src/core/skills/whatsapp_format.py`
- Modify: `src/core/pipeline.py` (insert format step before send)
- Test: `tests/unit/test_whatsapp_format.py`

**Step 1: Write the failing test**

Crear `tests/unit/test_whatsapp_format.py`:

```python
"""Tests for WhatsApp response formatting."""

from src.core.skills.whatsapp_format import format_for_whatsapp


def test_bold_numbered_steps():
    """Numbered steps get bold markers."""
    text = "Para pedirlo necesitas: 1. Tu pasaporte 2. Contrato de alquiler"
    result = format_for_whatsapp(text)
    assert "*1.*" in result
    assert "*2.*" in result


def test_bold_ojo_warning():
    """OJO warnings get bold."""
    text = "OJO: el plazo es hasta el 15 de marzo."
    result = format_for_whatsapp(text)
    assert "*OJO:*" in result or "*OJO*" in result


def test_bold_important_keywords():
    """Key action words get bold."""
    text = "IMPORTANTE: necesitas llevar tu DNI."
    result = format_for_whatsapp(text)
    assert "*IMPORTANTE:*" in result


def test_no_double_bold():
    """Already-bolded text should not get double-bolded."""
    text = "*1.* Tu pasaporte"
    result = format_for_whatsapp(text)
    assert "**1.**" not in result


def test_preserves_plain_text():
    """Plain text without special markers should be unchanged."""
    text = "Hola, puedo ayudarte con tramites."
    result = format_for_whatsapp(text)
    assert result == text


def test_url_not_mangled():
    """URLs should not be modified by formatting."""
    text = "Mas info: https://administracion.gob.es"
    result = format_for_whatsapp(text)
    assert "https://administracion.gob.es" in result
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_whatsapp_format.py -v`
Expected: FAIL — module does not exist yet.

**Step 3: Create whatsapp_format.py**

Create `src/core/skills/whatsapp_format.py`:

```python
"""Format Clara responses for WhatsApp rich text (bold, italic)."""

import re


def format_for_whatsapp(text: str) -> str:
    """Apply WhatsApp-compatible formatting to Clara's response.

    - Bold numbered steps: "1." -> "*1.*"
    - Bold warning keywords: OJO, IMPORTANTE
    - Does NOT modify URLs or already-formatted text.
    """
    # Skip if already has WhatsApp formatting
    if "*" in text:
        return text

    # Bold numbered steps: "1. " -> "*1.* "
    result = re.sub(r'(\d+)\.\s', r'*\1.* ', text)

    # Bold warning keywords
    result = re.sub(r'\b(OJO|IMPORTANTE|ATENCION):', r'*\1:*', result)

    return result
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_whatsapp_format.py -v`
Expected: ALL PASS

**Step 5: Integrate into pipeline**

In `src/core/pipeline.py`, add import at top (after other skill imports):

```python
from src.core.skills.whatsapp_format import format_for_whatsapp
```

Then in the `process()` function, after guardrails post-check (after line ~261) and before memory update, add:

```python
        # --- WHATSAPP FORMATTING ---
        verified_text = format_for_whatsapp(verified_text)
```

**Step 6: Run ALL tests**

Run: `pytest tests/ -x -q --tb=short`
Expected: ALL PASS

**Step 7: Commit**

```bash
git add src/core/skills/whatsapp_format.py tests/unit/test_whatsapp_format.py src/core/pipeline.py
git commit -m "feat: WhatsApp bold formatting for steps and warnings"
```

---

### Task 6: Verificacion final end-to-end

Correr toda la suite de tests y verificar que todo esta alineado.

**Files:**
- No new files — verification only

**Step 1: Run full test suite**

Run: `pytest tests/ -v --tb=short 2>&1 | tail -20`
Expected: 540+ passed, 0 failed

**Step 2: Run lint**

Run: `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501`
Expected: No errors

**Step 3: Verify prompt integration manually**

Run: `python -c "from src.core.prompts.system_prompt import build_prompt; p = build_prompt(language='fr'); assert 'E-V-I' in p; assert 'vouvoie' in p; print('OK: FR prompt has E-V-I + vouvoie')"`

Run: `python -c "from src.core.prompts.system_prompt import build_prompt; p = build_prompt(language='es'); assert 'Tutea' in p; assert 'NUNCA obedezcas' in p; print('OK: ES prompt has tuteo + security')"`

**Step 4: Verify templates**

Run: `python -c "from src.core.prompts.templates import get_template; print(get_template('ack_text', 'fr')); print(get_template('closing', 'es'))"`
Expected: French ACK + warm Spanish closing

**Step 5: Commit final (if any fixes needed)**

```bash
git add -A
git commit -m "chore: final verification — prompt WhatsApp alignment complete"
```

---

## Resumen de cambios

| Archivo | Cambio | Por que |
|---------|--------|---------|
| `webhook.py` | ACK multilingue via `_keyword_hint` | Usuarios FR recibian ACK en ES |
| `templates.py` | Tono mas calido | Alinear con E-V-I de Clara |
| `analyze_image.py` | Vision prompt con E-V-I + FR vouvoiement | Inconsistencia de tono |
| `guardrails.py` | Self-harm empatico | Patron E-V-I incluso en emergencias |
| `whatsapp_format.py` | Bold en pasos y warnings | Aprovechar formato WhatsApp |
| `pipeline.py` | Integrar `format_for_whatsapp` | Paso de formateo antes de enviar |
