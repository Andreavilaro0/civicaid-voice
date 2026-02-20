# Frontend Tone Sync — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update all 5 HTML presentation files + `static_files.py` to reflect the new Clara tone from Fase 5. Remove emojis from Clara messages, use E-V-I pattern, informal register (tu), and support WAV audio from Gemini TTS.

**Architecture:** Pure HTML text edits in `presentacion/*.html` + one Python file fix in `src/routes/static_files.py`. No build system, no dependencies, no logic changes. Each HTML file is self-contained with inline CSS/JS.

**Tech Stack:** Static HTML/CSS/JS, Flask route (static_files.py), Python

---

## Context

Fase 5 ("Voz de Clara") rewrites Clara's backend tone — system prompt, templates, cache, guardrails, TTS. But the **5 presentation HTML files** still use the old tone: exclamation marks, emojis in Clara messages, formal register, no empathy pattern.

### What "Clara tone" means (from FASE5-VOZ-CLARA.md):

- **E-V-I pattern**: Empatizar (1 sentence) -> Validar (1 sentence) -> Informar (max 4 steps)
- **No emojis** in Clara messages (max 1 per message, NEVER in greetings or errors)
- **Informal register**: "tu" in ES, "vous" in FR
- **Tramites = DERECHOS**: Present procedures as rights, not obligations
- **Clara takes blame**: "No he podido" not "No pudiste"
- **Legal jargon always explained**: parenthetical "(es decir, ...)"
- **2 options on failure**

### Files to modify:

| File | Lines | Main issues |
|------|-------|-------------|
| `presentacion/demo-whatsapp.html` | 671 | Emojis in Clara (💰📋🔗), "¡Hola!", robotic "He entendido/He analizado" |
| `presentacion/demo-webapp.html` | 653 | No empathy in greeting, loading text OK |
| `presentacion/demo-audioplayer.html` | 514 | No empathy in responses, synthetic beep audio |
| `presentacion/clara-pitch.html` | 608 | "Bienvenido/a" (formal), ✅ emojis, "asistente" (robotic) |
| `src/routes/static_files.py` | 17 | Hardcoded `mimetype="audio/mpeg"` — can't serve WAV |

---

### Task 1: Update demo-whatsapp.html — Clara messages

**Files:**
- Modify: `presentacion/demo-whatsapp.html`

This is the highest-impact file — it demonstrates a full WhatsApp conversation shown to judges.

**Step 1: Read the file and locate all Clara messages**

Read: `presentacion/demo-whatsapp.html`

Clara messages are at:
- Line 468: Greeting — "¡Hola! Soy Clara, tu asistente de ayudas sociales..."
- Lines 499-509: IMV response — has 💰📋🔗 emojis
- Lines 564-572: Empadronamiento response — "He entendido tu pregunta" + 🔗 emoji
- Lines 622-627: Document analysis — "He analizado tu documento"

**Step 2: Replace greeting (line 468)**

Replace the bubble-text content inside the first Clara message:

Old:
```
¡Hola! Soy Clara, tu asistente de ayudas sociales. Puedo informarte sobre trámites como el Ingreso Mínimo Vital, empadronamiento o tarjeta sanitaria.

Escribe, habla o envía una foto de tu documento.
```

New:
```
Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas del gobierno espanol.

Puedo ayudarte con:
1. Ingreso Minimo Vital (IMV) — ayuda economica
2. Empadronamiento — registro en tu municipio
3. Tarjeta Sanitaria — acceso a sanidad publica

Escribe, habla o envia una foto de tu documento.
```

**Step 3: Replace IMV response (lines 499-509)**

Old (with emojis):
```
El Ingreso Mínimo Vital (IMV) es una prestación mensual...

💰 Cantidad: entre 491€ y 1.033€/mes
📋 Requisitos principales:
• Tener entre 23 y 65 años
• Residir en España al menos 1 año
• Ingresos por debajo del límite

🔗 Fuente: seg-social.es/imv

¿Quieres saber cómo solicitarlo?
```

New (E-V-I pattern, no emojis):
```
Es buena pregunta — el IMV es una ayuda importante y tienes derecho a pedirla.

El Ingreso Minimo Vital (IMV) es una prestacion mensual de la Seguridad Social para personas con bajos ingresos.

Cantidad: entre 491&#x20AC; y 1.033&#x20AC;/mes.

Requisitos principales:
&#x2022; Tener entre 23 y 65 a&#xF1;os
&#x2022; Residir en Espa&#xF1;a al menos 1 a&#xF1;o
&#x2022; Ingresos por debajo del l&#xED;mite

Fuente: <span class="link">seg-social.es/imv</span>

&#xBF;Quieres saber c&#xF3;mo solicitarlo?
```

**Step 4: Replace empadronamiento response (lines 564-572)**

Old:
```
He entendido tu pregunta. Para empadronarte necesitas:
...
🔗 Fuente: administracion.gob.es
```

New:
```
El empadronamiento es uno de los primeros pasos cuando llegas a una ciudad — es mas sencillo de lo que parece.

Para empadronarte (registrarte oficialmente en tu municipio) necesitas:

1. Ir al Ayuntamiento de tu ciudad
2. Llevar tu pasaporte o NIE
3. Un contrato de alquiler o declaraci&#xF3;n del propietario

El tr&#xE1;mite es gratuito y suele tardar 1&#x2013;3 d&#xED;as.

Fuente: <span class="link">administracion.gob.es</span>
```

**Step 5: Replace document analysis response (lines 622-627)**

Old:
```
He analizado tu documento. Parece ser una carta del SEPE sobre tu prestación por desempleo.

El documento indica que tu prestación se renueva el 15 de marzo.

¿Necesitas ayuda para entender algún apartado específico?
```

New:
```
Veo que me has enviado una imagen. Entiendo que puede ser preocupante recibir documentos oficiales — vamos a mirarlo juntos.

Parece una carta del SEPE (Servicio de Empleo) sobre tu prestaci&#xF3;n por desempleo. El documento indica que se renueva el <strong>15 de marzo</strong>.

&#xBF;Necesitas que te explique alguna parte?
```

**Step 6: Open the file in browser to visually verify**

Run: `open presentacion/demo-whatsapp.html`

Verify:
- No emojis in any Clara bubble
- Greeting starts with "Hola, soy Clara." (no "!")
- IMV response has empathy first line
- Empadronamiento has parenthetical explanation
- Document analysis has empathy + "juntos"

**Step 7: Commit**

```bash
git add presentacion/demo-whatsapp.html
git commit -m "feat(fase5): update demo-whatsapp Clara messages — E-V-I pattern, no emojis"
```

---

### Task 2: Update demo-webapp.html — Clara greeting and IMV response

**Files:**
- Modify: `presentacion/demo-webapp.html`

**Step 1: Read the file and locate Clara messages**

Read: `presentacion/demo-webapp.html`

Clara messages are at:
- Line 517: Greeting — "Hola, soy Clara. ¿En qué puedo ayudarte?"
- Line 543: IMV response (factual, mostly OK but needs empathy)

**Step 2: Replace greeting (line 517)**

Old:
```html
Hola, soy Clara. &iquest;En qu&eacute; puedo ayudarte?
<br><br>
Puedo informarte sobre:
<ul>
  <li>Ingreso M&iacute;nimo Vital</li>
  <li>Empadronamiento</li>
  <li>Tarjeta sanitaria</li>
</ul>
```

New:
```html
Hola, soy Clara. Estoy aqu&iacute; para ayudarte con tr&aacute;mites y ayudas del gobierno espa&ntilde;ol.
<br><br>
Puedo ayudarte con:
<ul>
  <li>Ingreso M&iacute;nimo Vital (IMV) &mdash; ayuda econ&oacute;mica</li>
  <li>Empadronamiento &mdash; registro en tu municipio</li>
  <li>Tarjeta sanitaria &mdash; acceso a sanidad p&uacute;blica</li>
</ul>
```

**Step 3: Add empathy to IMV response (line 543)**

Old:
```html
El Ingreso M&iacute;nimo Vital es una prestaci&oacute;n mensual de la Seguridad Social para personas con bajos ingresos. Puedes recibir entre <strong>491&euro;</strong> y <strong>1.033&euro;</strong> al mes.
```

New:
```html
Es buena pregunta &mdash; el IMV es una ayuda importante y tienes derecho a pedirla.
<br><br>
El Ingreso M&iacute;nimo Vital (IMV) es una prestaci&oacute;n mensual de la Seguridad Social para personas con bajos ingresos. Puedes recibir entre <strong>491&euro;</strong> y <strong>1.033&euro;</strong> al mes.
```

**Step 4: Open in browser to verify**

Run: `open presentacion/demo-webapp.html`

Verify:
- Greeting says "Estoy aqui para ayudarte" not "¿En qué puedo ayudarte?"
- Each list item has parenthetical explanation
- IMV response starts with empathy line

**Step 5: Commit**

```bash
git add presentacion/demo-webapp.html
git commit -m "feat(fase5): update demo-webapp greeting + IMV response with Clara tone"
```

---

### Task 3: Update demo-audioplayer.html — response texts with empathy

**Files:**
- Modify: `presentacion/demo-audioplayer.html`

**Step 1: Read and locate text content**

Read: `presentacion/demo-audioplayer.html`

Content is at:
- Line 249: ES scenario question "Que es el Ingreso Minimo Vital?"
- Line 250: ES response "El Ingreso Minimo Vital es una ayuda mensual..."
- Line 274: FR scenario question "Comment obtenir la carte sanitaire?"
- Line 275: FR response "La carte sanitaire (tarjeta sanitaria) est delivree..."

**Step 2: Update ES response text (line 250)**

Old:
```html
<div class="scenario-response">El Ingreso Minimo Vital es una ayuda mensual de la Seguridad Social para personas en situacion de vulnerabilidad...</div>
```

New:
```html
<div class="scenario-response">Es buena pregunta — el IMV es una ayuda importante y tienes derecho a pedirla. El Ingreso Minimo Vital es una prestacion mensual de la Seguridad Social para personas con bajos ingresos...</div>
```

**Step 3: Update FR response text (line 275)**

Old:
```html
<div class="scenario-response">La carte sanitaire (tarjeta sanitaria) est delivree par le centre de sante de votre communaute autonome...</div>
```

New:
```html
<div class="scenario-response">C'est une bonne question. La carte sanitaire (tarjeta sanitaria) est un droit — elle est delivree par le centre de sante de votre communaute autonome...</div>
```

**Step 4: Open in browser to verify**

Run: `open presentacion/demo-audioplayer.html`

Verify:
- ES response starts with empathy + "derecho"
- FR response starts with validation + "droit"
- Audio player still works (synthetic beeps are fine for demo — they demonstrate the UI)

**Step 5: Commit**

```bash
git add presentacion/demo-audioplayer.html
git commit -m "feat(fase5): add empathy + rights framing to audioplayer demo texts"
```

---

### Task 4: Update clara-pitch.html — slide text with Clara tone

**Files:**
- Modify: `presentacion/clara-pitch.html`

This is the pitch deck shown to judges. Multiple slides have Clara message previews.

**Step 1: Read and locate Clara messages in slides**

Read: `presentacion/clara-pitch.html`

Clara messages in slides:
- Line 366 (Slide 5): "Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas." — close but generic
- Line 369: IMV response "El Ingreso Minimo Vital (IMV) es una ayuda economica para personas con pocos recursos." — no empathy
- Line 380: Steps response "Para solicitarlo necesitas: 1. DNI/NIE 2. Empadronamiento 3. Declaracion renta" — OK
- Line 402 (Slide 6): "Bienvenido/a. Soy Clara, tu asistente para tramites y ayudas sociales." — BAD: formal, "asistente"
- Line 404-407: Uses ✅ emojis — ideally keep these for slide visual (different context than WhatsApp)

**Step 2: Update Slide 5 greeting (line 366)**

Old:
```html
<div class="bubble bubble-clara">Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas. Puedes escribirme o enviar una nota de voz.</div>
```

New:
```html
<div class="bubble bubble-clara">Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas del gobierno espanol. Puedes escribirme, enviar una nota de voz o una foto.</div>
```

**Step 3: Add empathy to IMV response in Slide 5 (line 368-369)**

Old:
```html
<div class="bubble bubble-clara">
  El Ingreso Minimo Vital (IMV) es una ayuda economica para personas con pocos recursos. Puede ser entre 604-1.200€/mes.
```

New:
```html
<div class="bubble bubble-clara">
  Es buena pregunta — el IMV es una ayuda importante y tienes derecho a pedirla. Es una prestacion de entre 604-1.200€/mes para personas con pocos recursos.
```

**Step 4: Update Slide 6 greeting (line 402)**

Old:
```html
<div class="bubble bubble-clara">Bienvenido/a. Soy Clara, tu asistente para tramites y ayudas sociales.</div>
```

New:
```html
<div class="bubble bubble-clara">Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas del gobierno espanol.</div>
```

**Step 5: Keep ✅ in Slide 6 tarjeta sanitaria response (lines 404-407)**

The ✅ emojis in the pitch slide serve as visual bullet markers for readability in a presentation context. This is different from WhatsApp/chat where Clara shouldn't use emojis. **Keep as-is** — pitch deck is a visual aid, not a Clara conversation.

**Step 6: Open in browser to verify**

Run: `open presentacion/clara-pitch.html`

Navigate through slides 5 and 6. Verify:
- Slide 5: "Hola, soy Clara." (not "¡Hola!"), IMV has empathy
- Slide 6: No "Bienvenido/a", no "asistente"
- All slide navigation still works (keyboard arrows, dots, swipe)

**Step 7: Commit**

```bash
git add presentacion/clara-pitch.html
git commit -m "feat(fase5): update pitch deck Clara messages — warm tone, remove formal register"
```

---

### Task 5: Update static_files.py — serve WAV files for Gemini TTS

**Files:**
- Modify: `src/routes/static_files.py`
- Test: `tests/unit/test_static_files.py` (create if needed)

This is needed for T8 (Gemini TTS outputs WAV, not MP3).

**Step 1: Read current file**

Read: `src/routes/static_files.py`

Current code (line 16): `mimetype="audio/mpeg"` — hardcoded MP3.

**Step 2: Replace with MIME type detection based on file extension**

Old:
```python
"""GET /static/cache/<file> — serve pre-generated MP3 audio files."""

import os
from flask import Blueprint, send_from_directory

static_bp = Blueprint("static_files", __name__)

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")


@static_bp.route("/static/cache/<path:filename>", methods=["GET"])
def serve_cache_file(filename: str):
    return send_from_directory(
        os.path.abspath(_CACHE_DIR),
        filename,
        mimetype="audio/mpeg",
    )
```

New:
```python
"""GET /static/cache/<file> — serve pre-generated audio files (MP3, WAV)."""

import os
from flask import Blueprint, send_from_directory

static_bp = Blueprint("static_files", __name__)

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")

_MIME_TYPES = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
}


@static_bp.route("/static/cache/<path:filename>", methods=["GET"])
def serve_cache_file(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    mime = _MIME_TYPES.get(ext, "application/octet-stream")
    return send_from_directory(
        os.path.abspath(_CACHE_DIR),
        filename,
        mimetype=mime,
    )
```

**Step 3: Write test for new MIME type logic**

Check if `tests/unit/test_static_files.py` exists:

```bash
ls tests/unit/test_static_files.py 2>/dev/null || echo "NOT FOUND"
```

If not found, create `tests/unit/test_static_files.py`:

```python
"""Tests for static file serving with correct MIME types."""


def test_mime_types_map_has_mp3_wav():
    from src.routes.static_files import _MIME_TYPES
    assert _MIME_TYPES[".mp3"] == "audio/mpeg"
    assert _MIME_TYPES[".wav"] == "audio/wav"
    assert _MIME_TYPES[".ogg"] == "audio/ogg"
```

**Step 4: Run test**

Run: `pytest tests/unit/test_static_files.py -v --tb=short`
Expected: PASS

**Step 5: Run full test suite to verify no regression**

Run: `pytest tests/ -x -q --tb=short`
Expected: 508+ passed, 0 failed

**Step 6: Commit**

```bash
git add src/routes/static_files.py tests/unit/test_static_files.py
git commit -m "feat(fase5): support WAV + OGG MIME types in static file serving"
```

---

### Task 6: Verification — all HTML files and static_files.py

**Step 1: Run the full test suite**

```bash
pytest tests/ -x -q --tb=short
```

Expected: 508+ passed, 0 failed

**Step 2: Verify no emojis in Clara messages across all HTML files**

```bash
# Search for common emoji patterns in Clara bubbles
grep -n "&#x1F" presentacion/demo-whatsapp.html || echo "NO EMOJIS IN WHATSAPP"
grep -n "Hola!" presentacion/demo-whatsapp.html || echo "NO EXCLAMATION IN WHATSAPP"
grep -n "Bienvenido" presentacion/clara-pitch.html || echo "NO FORMAL IN PITCH"
grep -n "asistente" presentacion/clara-pitch.html presentacion/demo-whatsapp.html || echo "NO ROBOTIC WORD"
```

Expected: All return "NO ..." messages (no matches).

**Step 3: Verify static_files.py serves WAV**

```bash
PYTHONPATH=. python -c "
from src.routes.static_files import _MIME_TYPES
assert _MIME_TYPES['.wav'] == 'audio/wav'
assert _MIME_TYPES['.mp3'] == 'audio/mpeg'
print('MIME TYPES OK')
"
```

Expected: `MIME TYPES OK`

**Step 4: Open all HTML files to visually verify**

```bash
open presentacion/demo-whatsapp.html
open presentacion/demo-webapp.html
open presentacion/demo-audioplayer.html
open presentacion/clara-pitch.html
```

Visual checklist:
- [ ] demo-whatsapp: Clara greeting = "Hola, soy Clara." (no "!")
- [ ] demo-whatsapp: IMV response starts with empathy, no emojis
- [ ] demo-whatsapp: Empadronamiento has "(registrarte oficialmente...)"
- [ ] demo-whatsapp: Document analysis has empathy + "juntos"
- [ ] demo-webapp: Greeting = "Estoy aqui para ayudarte"
- [ ] demo-webapp: List items have parenthetical explanations
- [ ] demo-audioplayer: ES response has empathy + "derecho"
- [ ] demo-audioplayer: FR response has "droit"
- [ ] clara-pitch: Slide 5 = "Hola, soy Clara." (no "Bienvenido/a")
- [ ] clara-pitch: Slide 5 IMV has empathy
- [ ] clara-pitch: Slide 6 = no "asistente"

---

## Summary of Changes

| File | What changes | Lines affected |
|------|-------------|----------------|
| `presentacion/demo-whatsapp.html` | 4 Clara messages rewritten (greeting, IMV, empadronamiento, vision) | ~468, 499-509, 564-572, 622-627 |
| `presentacion/demo-webapp.html` | Greeting + IMV response | ~517, 543 |
| `presentacion/demo-audioplayer.html` | ES + FR response texts | ~250, 275 |
| `presentacion/clara-pitch.html` | 3 slide messages (greeting, IMV, web greeting) | ~366, 369, 402 |
| `src/routes/static_files.py` | MIME type detection for WAV/OGG | All 17 lines |
| `tests/unit/test_static_files.py` | New: MIME type test | New file |

**Total: 5 files modified, 1 file created, ~20 text edits, 0 logic changes.**
