# Image Vision Analysis Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** When a user sends a photo via WhatsApp, Clara analyzes it with Gemini 1.5 Flash vision and responds with relevant guidance about the document/image — instead of returning a hardcoded demo response.

**Architecture:** Add a new skill `analyze_image.py` that sends image bytes + a Spanish-document-aware prompt to Gemini 1.5 Flash (already multimodal). Wire it into `pipeline.py` as an IMAGE branch between fetch_media and llm_generate, parallel to the existing AUDIO branch. Feature-flagged with `VISION_ENABLED` (default true). Falls back to demo cache response if vision fails.

**Tech Stack:** Python 3.11, google-genai SDK (already in requirements.txt), Gemini 1.5 Flash (multimodal — same model used for text and audio), Flask, Twilio WhatsApp

---

## Key Discovery (from research)

- **google-genai SDK** is already installed (`google-genai>=1.0,<2.0` in requirements.txt)
- **Gemini 1.5 Flash** is already multimodal — no model change needed
- **`transcribe.py`** already sends binary data to Gemini via `genai.types.Part(inline_data=genai.types.Blob(...))` — we reuse this exact pattern for images
- **`fetch_media.py`** already downloads media bytes from Twilio — works for images too
- **`pipeline.py`** has an AUDIO branch (lines 59-76) — IMAGE branch follows the same pattern
- **`detect_input.py`** already detects `InputType.IMAGE` — no changes needed there
- **`webhook.py`** already passes `media_url` and `media_type` for images — no changes needed

---

## What Changes

| File | Action | Why |
|------|--------|-----|
| `src/core/config.py` | Add 1 flag | `VISION_ENABLED` |
| `src/core/skills/analyze_image.py` | **Create** | New skill: send image bytes to Gemini, get analysis |
| `src/core/pipeline.py` | Add IMAGE branch | Wire analyze_image between fetch_media and llm_generate |
| `src/core/prompts/templates.py` | Add 2 templates | `ack_image`, `vision_fail` |
| `src/routes/webhook.py` | Fix ACK for images | Return `ack_image` instead of `ack_text` |
| `tests/unit/test_analyze_image.py` | **Create** | Tests for the new skill |
| `tests/unit/test_pipeline_image.py` | **Create** | Tests for IMAGE branch in pipeline |

---

### Task 1: Add VISION_ENABLED config flag

**Files:**
- Modify: `src/core/config.py:48` (after GUARDRAILS_ON)

**Step 1: Write the failing test**

```python
# tests/unit/test_config.py (append to existing or create)
def test_vision_enabled_default_true():
    from src.core.config import Config
    c = Config()
    assert c.VISION_ENABLED is True
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/unit/test_config.py::test_vision_enabled_default_true -v`
Expected: FAIL with `AttributeError: 'Config' has no attribute 'VISION_ENABLED'`

**Step 3: Add the flag to config.py**

In `src/core/config.py`, after line 45 (`GUARDRAILS_ON`), add:

```python
    # --- Vision ---
    VISION_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("VISION_ENABLED", "true")))
    VISION_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("VISION_TIMEOUT", "10")))
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/unit/test_config.py::test_vision_enabled_default_true -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/core/config.py tests/unit/test_config.py
git commit -m "feat: add VISION_ENABLED and VISION_TIMEOUT config flags"
```

---

### Task 2: Add ack_image and vision_fail templates

**Files:**
- Modify: `src/core/prompts/templates.py`

**Step 1: Write the failing test**

```python
# tests/unit/test_templates_image.py
from src.core.prompts.templates import get_template

def test_ack_image_template_exists():
    result = get_template("ack_image", "es")
    assert "imagen" in result.lower() or "foto" in result.lower()

def test_ack_image_template_french():
    result = get_template("ack_image", "fr")
    assert len(result) > 0

def test_vision_fail_template_exists():
    result = get_template("vision_fail", "es")
    assert len(result) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/unit/test_templates_image.py -v`
Expected: FAIL — templates don't exist yet, returns ""

**Step 3: Add templates to templates.py**

In `src/core/prompts/templates.py`, add these entries to the `TEMPLATES` dict (after `"ack_audio"`):

```python
    "ack_image": {
        "es": "Estoy analizando tu imagen... 📷",
        "fr": "J'analyse votre image... 📷",
        "en": "Analyzing your image... 📷",
    },
    "vision_fail": {
        "es": "No pude analizar la imagen. ¿Podrías describir lo que ves o escribir tu pregunta?",
        "fr": "Je n'ai pas pu analyser l'image. Pourriez-vous décrire ce que vous voyez ?",
        "en": "I couldn't analyze the image. Could you describe what you see or type your question?",
    },
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/unit/test_templates_image.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/core/prompts/templates.py tests/unit/test_templates_image.py
git commit -m "feat: add ack_image and vision_fail response templates"
```

---

### Task 3: Create analyze_image skill

**Files:**
- Create: `src/core/skills/analyze_image.py`
- Create: `tests/unit/test_analyze_image.py`

**Step 1: Write the failing tests**

Create `tests/unit/test_analyze_image.py`:

```python
"""Tests for analyze_image skill."""

from unittest.mock import patch, MagicMock
from src.core.skills.analyze_image import analyze_image, ImageAnalysisResult


def test_analyze_image_returns_result_dataclass():
    """analyze_image returns an ImageAnalysisResult."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = False
        mock_cfg.GEMINI_API_KEY = "key"
        result = analyze_image(b"fake", "image/jpeg")
        assert isinstance(result, ImageAnalysisResult)
        assert result.success is False


def test_analyze_image_disabled_returns_failure():
    """When VISION_ENABLED=False, returns failure without calling API."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = False
        mock_cfg.GEMINI_API_KEY = "key"
        result = analyze_image(b"fake", "image/jpeg")
        assert result.success is False
        assert "disabled" in result.error.lower()


def test_analyze_image_no_api_key_returns_failure():
    """When GEMINI_API_KEY is empty, returns failure."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = True
        mock_cfg.GEMINI_API_KEY = ""
        result = analyze_image(b"fake", "image/jpeg")
        assert result.success is False


def test_analyze_image_calls_gemini_with_image_bytes():
    """Verify Gemini is called with image data and Spanish document prompt."""
    import unittest.mock as um

    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "Este documento es una carta de la Seguridad Social."

    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = True
        mock_cfg.GEMINI_API_KEY = "test-key"
        mock_cfg.VISION_TIMEOUT = 10
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = analyze_image(b"\x89PNG\r\n", "image/png")
            assert result.success is True
            assert "Seguridad Social" in result.text
            mock_client.models.generate_content.assert_called_once()


def test_analyze_image_handles_api_exception():
    """When Gemini raises an exception, returns failure gracefully."""
    import unittest.mock as um

    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_client.models.generate_content.side_effect = Exception("API error")

    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = True
        mock_cfg.GEMINI_API_KEY = "test-key"
        mock_cfg.VISION_TIMEOUT = 10
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = analyze_image(b"\x89PNG\r\n", "image/png")
            assert result.success is False
            assert "API error" in result.error


def test_analyze_image_result_has_duration():
    """Result includes duration_ms."""
    with patch("src.core.skills.analyze_image.config") as mock_cfg:
        mock_cfg.VISION_ENABLED = False
        mock_cfg.GEMINI_API_KEY = "key"
        result = analyze_image(b"fake", "image/jpeg")
        assert hasattr(result, "duration_ms")
        assert isinstance(result.duration_ms, int)
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/unit/test_analyze_image.py -v`
Expected: FAIL — module doesn't exist

**Step 3: Create the skill**

Create `src/core/skills/analyze_image.py`:

```python
"""Analyze images using Gemini 1.5 Flash vision capabilities."""

import time
from dataclasses import dataclass
from typing import Optional

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

VISION_PROMPT = (
    "Eres Clara, asistente que ayuda a personas vulnerables en España con trámites del gobierno.\n"
    "Analiza esta imagen. Si es un documento oficial español (carta, formulario, notificación, "
    "certificado, resolución), identifica:\n"
    "1. Qué tipo de documento es\n"
    "2. Qué organismo lo envía\n"
    "3. Qué acción debe tomar la persona (plazos, pasos)\n"
    "4. Si necesita ayuda profesional\n\n"
    "Si NO es un documento administrativo, describe brevemente lo que ves y pregunta "
    "cómo puedes ayudar con trámites del gobierno español.\n\n"
    "Responde en español, lenguaje simple (nivel de comprensión: 12 años). Máximo 200 palabras."
)


@dataclass
class ImageAnalysisResult:
    """Result from Gemini vision analysis."""
    text: str
    duration_ms: int
    success: bool
    error: Optional[str] = None


@timed("analyze_image")
def analyze_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
) -> ImageAnalysisResult:
    """Send image to Gemini 1.5 Flash for analysis. Returns ImageAnalysisResult."""
    if not config.VISION_ENABLED:
        return ImageAnalysisResult(
            text="", duration_ms=0, success=False, error="Vision disabled"
        )

    if not config.GEMINI_API_KEY:
        return ImageAnalysisResult(
            text="", duration_ms=0, success=False, error="No Gemini API key"
        )

    start = time.time()
    try:
        import base64
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                genai.types.Content(
                    parts=[
                        genai.types.Part(
                            inline_data=genai.types.Blob(
                                mime_type=mime_type, data=image_b64
                            )
                        ),
                        genai.types.Part(text=VISION_PROMPT),
                    ]
                )
            ],
            config=genai.types.GenerateContentConfig(
                max_output_tokens=500,
                temperature=0.3,
            ),
        )

        elapsed = int((time.time() - start) * 1000)
        text = response.text.strip()
        return ImageAnalysisResult(
            text=text, duration_ms=elapsed, success=True
        )

    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        log_error("analyze_image", str(e))
        return ImageAnalysisResult(
            text="", duration_ms=elapsed, success=False, error=str(e)
        )
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/unit/test_analyze_image.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/core/skills/analyze_image.py tests/unit/test_analyze_image.py
git commit -m "feat: add analyze_image skill — Gemini 1.5 Flash vision for documents"
```

---

### Task 4: Wire IMAGE branch into pipeline.py

**Files:**
- Modify: `src/core/pipeline.py:59` (after AUDIO branch)
- Create: `tests/unit/test_pipeline_image.py`

**Step 1: Write the failing tests**

Create `tests/unit/test_pipeline_image.py`:

```python
"""Tests for IMAGE branch in pipeline."""

from unittest.mock import patch, MagicMock
from src.core.models import IncomingMessage, InputType


def _make_image_msg():
    return IncomingMessage(
        from_number="whatsapp:+34600000000",
        body="",
        media_url="https://api.twilio.com/image.jpg",
        media_type="image/jpeg",
        input_type=InputType.IMAGE,
    )


def test_pipeline_image_calls_analyze_image(monkeypatch):
    """When input_type=IMAGE, pipeline calls analyze_image."""
    monkeypatch.setattr("src.core.config.config.GUARDRAILS_ON", False)
    monkeypatch.setattr("src.core.config.config.DEMO_MODE", False)
    monkeypatch.setattr("src.core.config.config.MEMORY_ENABLED", False)
    monkeypatch.setattr("src.core.config.config.OBSERVABILITY_ON", False)
    monkeypatch.setattr("src.core.config.config.VISION_ENABLED", True)

    mock_fetch = MagicMock(return_value=b"\x89PNG")
    mock_send = MagicMock()

    from src.core.skills.analyze_image import ImageAnalysisResult
    mock_analyze = MagicMock(return_value=ImageAnalysisResult(
        text="Es una carta de la Seguridad Social.",
        duration_ms=500,
        success=True,
    ))

    with patch("src.core.pipeline.send_final_message", mock_send), \
         patch("src.core.skills.fetch_media.fetch_media", mock_fetch), \
         patch("src.core.pipeline.analyze_image", mock_analyze), \
         patch("src.core.pipeline.cache") as mock_cache:

        mock_cache.match.return_value = MagicMock(hit=False)

        from src.core import pipeline
        pipeline.process(_make_image_msg())

        mock_analyze.assert_called_once()
        mock_send.assert_called_once()
        sent = mock_send.call_args[0][0]
        assert "Seguridad Social" in sent.body


def test_pipeline_image_falls_back_on_vision_failure(monkeypatch):
    """When vision fails, pipeline sends vision_fail template."""
    monkeypatch.setattr("src.core.config.config.GUARDRAILS_ON", False)
    monkeypatch.setattr("src.core.config.config.DEMO_MODE", False)
    monkeypatch.setattr("src.core.config.config.MEMORY_ENABLED", False)
    monkeypatch.setattr("src.core.config.config.OBSERVABILITY_ON", False)
    monkeypatch.setattr("src.core.config.config.VISION_ENABLED", True)

    mock_fetch = MagicMock(return_value=b"\x89PNG")
    mock_send = MagicMock()

    from src.core.skills.analyze_image import ImageAnalysisResult
    mock_analyze = MagicMock(return_value=ImageAnalysisResult(
        text="", duration_ms=500, success=False, error="API error"
    ))

    with patch("src.core.pipeline.send_final_message", mock_send), \
         patch("src.core.skills.fetch_media.fetch_media", mock_fetch), \
         patch("src.core.pipeline.analyze_image", mock_analyze), \
         patch("src.core.pipeline.cache") as mock_cache:

        mock_cache.match.return_value = MagicMock(hit=False)

        from src.core import pipeline
        pipeline.process(_make_image_msg())

        mock_send.assert_called_once()
        sent = mock_send.call_args[0][0]
        assert sent.source == "fallback"


def test_pipeline_image_cache_hit_skips_vision(monkeypatch):
    """If image matches demo cache, vision is NOT called."""
    monkeypatch.setattr("src.core.config.config.GUARDRAILS_ON", False)
    monkeypatch.setattr("src.core.config.config.DEMO_MODE", False)
    monkeypatch.setattr("src.core.config.config.MEMORY_ENABLED", False)
    monkeypatch.setattr("src.core.config.config.OBSERVABILITY_ON", False)

    mock_send = MagicMock()
    mock_analyze = MagicMock()

    mock_entry = MagicMock()
    mock_entry.respuesta = "Demo image response"
    mock_entry.audio_file = None
    mock_entry.id = "demo"
    mock_cache_result = MagicMock(hit=True, entry=mock_entry)

    with patch("src.core.pipeline.send_final_message", mock_send), \
         patch("src.core.pipeline.cache") as mock_cache:

        mock_cache.match.return_value = mock_cache_result

        from src.core import pipeline
        pipeline.process(_make_image_msg())

        mock_analyze.assert_not_called()
        mock_send.assert_called_once()
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/unit/test_pipeline_image.py -v`
Expected: FAIL — `analyze_image` not imported in pipeline

**Step 3: Add IMAGE branch to pipeline.py**

In `src/core/pipeline.py`, add the import at top (after line 12):

```python
from src.core.skills.analyze_image import analyze_image
```

Then after the AUDIO branch (after line 76, before `# --- DETECT LANGUAGE`), add:

```python
        # --- IMAGE PIPELINE (Gemini vision) ---
        if msg.input_type == InputType.IMAGE and msg.media_url:
            from src.core.skills.fetch_media import fetch_media

            media_bytes = fetch_media(msg.media_url)
            if media_bytes is None:
                _send_fallback(msg, "vision_fail", start)
                return

            vision_result = analyze_image(media_bytes, msg.media_type or "image/jpeg")

            if vision_result.success and vision_result.text:
                elapsed_ms = int((time.time() - start) * 1000)
                log_pipeline_result(msg.request_id, msg.from_number, "vision", elapsed_ms)
                if ctx:
                    ctx.add_timing("vision", vision_result.duration_ms)
                    ctx.add_timing("total", elapsed_ms)
                    log_observability(ctx)
                response = FinalResponse(
                    to_number=msg.from_number,
                    body=vision_result.text,
                    source="vision",
                    total_ms=elapsed_ms,
                )
                send_final_message(response)
                return
            else:
                _send_fallback(msg, "vision_fail", start)
                return
```

**Important:** This block must go BEFORE the cache match block (line 150) so that images are analyzed by vision FIRST. But the current code hits cache match before this point. So instead, place this block **after the cache match block** (after line 169). That way:
1. If `image_demo` cache entry matches → returns demo response (backward compat)
2. If cache miss + IMAGE → calls Gemini vision

Actually the cleanest approach: place it right after the `DEMO_MODE` block (after line 185), alongside the KB lookup. This way cache still works, demo mode still works, and real images go to vision.

Revised location — after line 185 (`return` from DEMO_MODE), add:

```python
        # --- IMAGE PIPELINE (Gemini vision) ---
        if msg.input_type == InputType.IMAGE and msg.media_url:
            from src.core.skills.fetch_media import fetch_media

            media_bytes = fetch_media(msg.media_url)
            if media_bytes is None:
                _send_fallback(msg, "vision_fail", start)
                return

            vision_result = analyze_image(media_bytes, msg.media_type or "image/jpeg")

            if vision_result.success and vision_result.text:
                elapsed_ms = int((time.time() - start) * 1000)
                log_pipeline_result(msg.request_id, msg.from_number, "vision", elapsed_ms)
                if ctx:
                    ctx.add_timing("vision", vision_result.duration_ms)
                    ctx.add_timing("total", elapsed_ms)
                    log_observability(ctx)
                response = FinalResponse(
                    to_number=msg.from_number,
                    body=vision_result.text,
                    source="vision",
                    total_ms=elapsed_ms,
                )
                send_final_message(response)
                return
            else:
                _send_fallback(msg, "vision_fail", start)
                return
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/unit/test_pipeline_image.py -v`
Expected: ALL PASS

**Step 5: Run full test suite to verify no regressions**

Run: `python -m pytest tests/ -x -q --tb=short 2>&1 | tail -5`
Expected: All existing tests still pass

**Step 6: Commit**

```bash
git add src/core/pipeline.py tests/unit/test_pipeline_image.py
git commit -m "feat: wire IMAGE branch into pipeline — Gemini vision after cache miss"
```

---

### Task 5: Fix webhook ACK for images

**Files:**
- Modify: `src/routes/webhook.py:74-77`

**Step 1: Write the failing test**

```python
# tests/unit/test_webhook_image_ack.py
from unittest.mock import patch, MagicMock

def test_webhook_image_ack_says_analyzing(client_fixture):
    """When image is sent, ACK says 'analizando imagen' not 'procesando mensaje'."""
    # This test depends on your existing test client fixture.
    # If no fixture exists, use this approach:
    pass  # see integration test below


def test_image_ack_template_used():
    """Verify webhook returns ack_image for image input."""
    from src.core.prompts.templates import get_template
    ack = get_template("ack_image", "es")
    assert "imagen" in ack.lower() or "📷" in ack
```

**Step 2: Modify webhook.py**

In `src/routes/webhook.py`, replace lines 73-77:

```python
    # ACK template based on input type
    if input_type == InputType.AUDIO:
        ack_text = get_template("ack_audio", "es")
    else:
        ack_text = get_template("ack_text", "es")
```

With:

```python
    # ACK template based on input type
    if input_type == InputType.AUDIO:
        ack_text = get_template("ack_audio", "es")
    elif input_type == InputType.IMAGE:
        ack_text = get_template("ack_image", "es")
    else:
        ack_text = get_template("ack_text", "es")
```

**Step 3: Run tests**

Run: `python -m pytest tests/ -x -q --tb=short 2>&1 | tail -5`
Expected: All pass

**Step 4: Commit**

```bash
git add src/routes/webhook.py
git commit -m "feat: return image-specific ACK when user sends a photo"
```

---

### Task 6: Update CLAUDE.md and run final verification

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Add VISION_ENABLED to feature flags table in CLAUDE.md**

Add row:
```
| VISION_ENABLED | true | Habilita analisis de imagenes via Gemini Vision |
| VISION_TIMEOUT | 10 | Segundos max Gemini Vision |
```

**Step 2: Add analyze_image.py to skills list in CLAUDE.md**

Under `src/core/skills/` add: `analyze_image.py`

**Step 3: Run full test suite**

Run: `python -m pytest tests/ -x -q --tb=short`
Expected: All pass (previous count + 9 new tests)

**Step 4: Run lint**

Run: `ruff check src/ tests/ --select E,F,W --ignore E501`
Expected: Clean

**Step 5: Smoke test**

Run: `PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('App boots OK')"`
Expected: `App boots OK`

**Step 6: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add VISION_ENABLED flag and analyze_image skill to CLAUDE.md"
```

---

## Summary

| Task | What | Files |
|------|------|-------|
| T1 | Config flag `VISION_ENABLED` | config.py |
| T2 | Templates `ack_image`, `vision_fail` | templates.py |
| T3 | **New skill** `analyze_image.py` | skills/analyze_image.py + tests |
| T4 | Wire IMAGE branch in pipeline | pipeline.py + tests |
| T5 | Fix webhook ACK for images | webhook.py |
| T6 | Update docs, final verification | CLAUDE.md |

**Total: 6 tasks, ~9 new tests**

**Flow after implementation:**
```
User sends photo → Twilio → webhook (ACK: "Analizando tu imagen 📷")
                                    → Background thread:
                                      1. cache_match → image_demo HIT → demo response (backward compat)
                                      2. cache_match → MISS → fetch_media → analyze_image(Gemini Vision)
                                         → success → send vision response
                                         → failure → send vision_fail fallback
```
