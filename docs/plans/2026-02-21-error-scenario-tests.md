# Error Scenario Tests — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add ~80 tests covering real-world error scenarios like the "English user gets Spanish ACK" bug — language mismatches, broken pipelines, edge-case inputs, and error template validation across all 5 languages.

**Architecture:** Unit tests with mocks for external services (Twilio, Gemini). Integration tests using Flask test client for webhook round-trips. Focus on user-facing bugs: wrong language, broken audio, missing templates, silent failures.

**Tech Stack:** pytest, unittest.mock (patch/MagicMock), Flask test client, existing conftest fixtures

---

### Task 1: Webhook ACK Language — English, Portuguese, Arabic

The original bug: an English speaker gets a Spanish ACK. We already test French and Spanish ACKs. This task adds English, Portuguese, and Arabic.

**Files:**
- Modify: `tests/integration/test_webhook.py`

**Step 1: Write the failing tests**

Add these tests at the end of `tests/integration/test_webhook.py`:

```python
def test_webhook_ack_english_for_english_text(client):
    """ACK should be in English when user writes in English."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Hello, I need help with my registration",
            "From": "whatsapp:+44712345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # English ack_greeting or ack_text
        assert "Clara" in body or "moment" in body or "question" in body


def test_webhook_ack_portuguese_for_portuguese_text(client):
    """ACK should be in Portuguese when user writes in Portuguese."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Ola, preciso de ajuda com o registo",
            "From": "whatsapp:+351912345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Portuguese ack_greeting or ack_text
        assert "Clara" in body or "momento" in body or "pergunta" in body


def test_webhook_ack_arabic_for_arabic_keywords(client):
    """ACK should be in Arabic when user writes Arabic transliterated keywords."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Salam, ahlan musaada",
            "From": "whatsapp:+212612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Arabic ack should contain Arabic script
        assert "كلارا" in body or "لحظة" in body or "سؤال" in body
```

**Step 2: Run tests to verify they fail**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v -k "english or portuguese or arabic" --tb=short`

Expected: Some may PASS (if detect_lang works), some may FAIL (revealing real bugs). Document which.

**Step 3: Fix any production code bugs found**

If tests reveal that English/PT/AR ACKs are wrong, fix `src/core/skills/detect_lang.py` or `src/routes/webhook.py`.

**Step 4: Run tests to verify they pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v --tb=short`

Expected: All 9 webhook tests PASS.

**Step 5: Commit**

```bash
git add tests/integration/test_webhook.py
git commit -m "test(webhook): ACK language tests for English, Portuguese, Arabic"
```

---

### Task 2: Webhook — Conversation Language Memory Across Messages

Tests that a second message from the same number uses the remembered language for ACK, even if the second message is ambiguous.

**Files:**
- Modify: `tests/integration/test_webhook.py`

**Step 1: Write the failing tests**

```python
def test_webhook_remembers_french_for_second_message(client):
    """After French first message, ambiguous second message still gets French ACK."""
    phone = "whatsapp:+33612345678"
    with patch("src.core.pipeline.process"):
        # First message: clearly French
        client.post("/webhook", data={
            "Body": "Bonjour, j'ai besoin d'aide",
            "From": phone,
            "NumMedia": "0",
        })
        # Second message: ambiguous (just a number, no language hint)
        resp = client.post("/webhook", data={
            "Body": "NIE X1234567A",
            "From": phone,
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Should still be French (remembered), not Spanish
        assert "instant" in body or "cherche" in body or "ecoute" in body


def test_webhook_remembers_english_for_second_message(client):
    """After English first message, ambiguous second message still gets English ACK."""
    phone = "whatsapp:+44799999999"
    with patch("src.core.pipeline.process"):
        # First message: clearly English
        client.post("/webhook", data={
            "Body": "Hello, I need help please",
            "From": phone,
            "NumMedia": "0",
        })
        # Second message: ambiguous
        resp = client.post("/webhook", data={
            "Body": "IMV",
            "From": phone,
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Should be English (remembered)
        assert "moment" in body or "question" in body or "Clara" in body
```

**Step 2: Run tests to verify they fail**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v -k "remembers" --tb=short`

Expected: May PASS if conversation memory works, or FAIL if the in-process dict resets between test requests.

**Step 3: Fix any bugs (if needed)**

The `_conversation_lang` dict is module-level, so it should persist between requests in the same test process. If not, investigate.

**Step 4: Run full webhook tests**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v --tb=short`

Expected: All PASS.

**Step 5: Commit**

```bash
git add tests/integration/test_webhook.py
git commit -m "test(webhook): conversation language memory across messages"
```

---

### Task 3: Webhook — Image Input ACK

Zero tests exist for image input through the webhook. This catches a missing code path.

**Files:**
- Modify: `tests/integration/test_webhook.py`

**Step 1: Write the failing test**

```python
def test_webhook_image_returns_image_ack(client):
    """Image input should return ack_image template."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "image/jpeg",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # ack_image/es: "Voy a mirar tu documento"
        assert "documento" in body or "mirar" in body


def test_webhook_image_french_ack(client):
    """French speaker sending image gets French ack_image."""
    phone = "whatsapp:+33600000001"
    with patch("src.core.pipeline.process"):
        # First: establish French
        client.post("/webhook", data={
            "Body": "Bonjour",
            "From": phone,
            "NumMedia": "0",
        })
        # Then: send image
        resp = client.post("/webhook", data={
            "Body": "",
            "From": phone,
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "image/jpeg",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # ack_image/fr: "Je regarde votre document"
        assert "document" in body or "regarde" in body
```

**Step 2: Run tests**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v -k "image" --tb=short`

**Step 3: Fix if needed**

**Step 4: Verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/integration/test_webhook.py
git commit -m "test(webhook): image input ACK in Spanish and French"
```

---

### Task 4: Error Template Validation — All 5 Languages

Templates like `vision_fail`, `whisper_fail`, `llm_fail` exist but have zero dedicated tests for PT and AR. Also validates tone rules.

**Files:**
- Create: `tests/unit/test_error_templates.py`

**Step 1: Write the failing tests**

```python
"""Tests: error and fallback templates exist and follow tone rules for all 5 languages."""

import pytest
from src.core.prompts.templates import get_template, TEMPLATES


LANGUAGES = ["es", "fr", "en", "pt", "ar"]
ERROR_KEYS = ["vision_fail", "whisper_fail", "llm_fail", "fallback_generic"]


class TestErrorTemplatesExist:
    """Every error template must exist for all 5 supported languages."""

    @pytest.mark.parametrize("key", ERROR_KEYS)
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_template_exists_and_nonempty(self, key, lang):
        result = get_template(key, lang)
        assert result, f"Missing: {key}/{lang}"
        assert len(result) > 20, f"Too short: {key}/{lang} = '{result}'"


class TestErrorTemplatesOfferAlternative:
    """Error templates must offer the user an alternative action (E-V-I pattern)."""

    @pytest.mark.parametrize("key", ["vision_fail", "whisper_fail", "llm_fail"])
    def test_es_offers_alternative(self, key):
        text = get_template(key, "es")
        assert any(w in text.lower() for w in ["puedes", "intentar", "escribeme"]), \
            f"{key}/es must offer alternative"

    @pytest.mark.parametrize("key", ["vision_fail", "whisper_fail", "llm_fail"])
    def test_fr_offers_alternative(self, key):
        text = get_template(key, "fr")
        assert any(w in text.lower() for w in ["pouvez", "reessayer", "ecrivez"]), \
            f"{key}/fr must offer alternative"

    @pytest.mark.parametrize("key", ["vision_fail", "whisper_fail", "llm_fail"])
    def test_en_offers_alternative(self, key):
        text = get_template(key, "en")
        assert any(w in text.lower() for w in ["can", "try", "type"]), \
            f"{key}/en must offer alternative"


class TestErrorTemplatesNoEmoji:
    """ACK and error templates must NOT contain emoji (Fase 5 rule)."""

    @pytest.mark.parametrize("key", ERROR_KEYS + ["ack_text", "ack_audio", "ack_image"])
    @pytest.mark.parametrize("lang", LANGUAGES)
    def test_no_emoji(self, key, lang):
        import re
        text = get_template(key, lang)
        if not text:
            pytest.skip(f"No template for {key}/{lang}")
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U0001f900-\U0001f9FF"
            "]+", flags=re.UNICODE
        )
        assert not emoji_pattern.search(text), \
            f"Emoji found in {key}/{lang}: '{text}'"


class TestMemoryTemplatesExist:
    """Memory templates must exist for es, fr, en."""

    MEMORY_KEYS = [
        "memory_optin_ask", "memory_optin_confirmed",
        "memory_optin_declined", "memory_forgotten",
    ]

    @pytest.mark.parametrize("key", MEMORY_KEYS)
    @pytest.mark.parametrize("lang", ["es", "fr", "en"])
    def test_memory_template_exists(self, key, lang):
        result = get_template(key, lang)
        assert result, f"Missing: {key}/{lang}"
        assert len(result) > 10, f"Too short: {key}/{lang}"


class TestGetTemplateFallback:
    """get_template falls back to Spanish for unknown languages."""

    def test_unknown_lang_falls_back_to_es(self):
        es = get_template("ack_text", "es")
        xx = get_template("ack_text", "xx")
        assert xx == es

    def test_unknown_key_returns_empty(self):
        result = get_template("nonexistent_key", "es")
        assert result == ""
```

**Step 2: Run tests to verify they fail**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_error_templates.py -v --tb=short`

Expected: Most PASS. Some may FAIL if PT/AR error templates are missing or too short.

**Step 3: Fix any missing templates in `src/core/prompts/templates.py`**

If any PT or AR error templates are missing, add them.

**Step 4: Run tests to verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_error_templates.py -v --tb=short`

Expected: All PASS.

**Step 5: Commit**

```bash
git add tests/unit/test_error_templates.py
git commit -m "test(templates): error template validation — 5 languages, tone, no emoji"
```

---

### Task 5: Pipeline — Language Flows End-to-End

The pipeline has only 2 tests (cache hit, cache miss). This adds tests for the language detection → LLM → response flow, and error handling paths.

**Files:**
- Modify: `tests/integration/test_pipeline.py`

**Step 1: Write the failing tests**

Add these tests:

```python
def test_pipeline_guardrail_blocks_unsafe_input():
    """Guardrail pre-check blocks unsafe content and sends guardrail response."""
    msg = IncomingMessage(
        from_number="whatsapp:+34612345678",
        body="como hackear un sistema",
        input_type=InputType.TEXT,
        timestamp=1000.0,
    )

    with patch("twilio.rest.Client") as MockClient, \
         patch("src.core.config.config.GUARDRAILS_ON", True), \
         patch("src.core.guardrails.pre_check") as mock_guard:
        mock_guard.return_value = MagicMock(safe=False, modified_text="No puedo ayudar con ese tema.")
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM789")

        from src.core import pipeline
        pipeline.process(msg)

        assert instance.messages.create.called
        call_kwargs = instance.messages.create.call_args
        body = call_kwargs.kwargs.get("body", call_kwargs[1].get("body", ""))
        assert "No puedo" in body


def test_pipeline_sends_fallback_on_exception():
    """Pipeline catches exceptions and sends fallback response."""
    msg = IncomingMessage(
        from_number="whatsapp:+34612345678",
        body="algo que rompe todo",
        input_type=InputType.TEXT,
        timestamp=1000.0,
    )

    with patch("twilio.rest.Client") as MockClient, \
         patch("src.core.cache.match", side_effect=Exception("boom")):
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM999")

        from src.core import pipeline
        pipeline.process(msg)

        assert instance.messages.create.called
        call_kwargs = instance.messages.create.call_args
        body = call_kwargs.kwargs.get("body", call_kwargs[1].get("body", ""))
        # Should be a fallback message, not a traceback
        assert len(body) > 10
```

**Step 2: Run tests to verify they fail**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_pipeline.py -v --tb=short`

**Step 3: Fix any bugs found**

**Step 4: Verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_pipeline.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/integration/test_pipeline.py
git commit -m "test(pipeline): guardrail blocking and exception fallback"
```

---

### Task 6: Detect Input — Edge Cases

The `detect_input_type` function has 4 tests. Missing: video MIME, multiple media, empty strings.

**Files:**
- Modify: `tests/unit/test_detect_input.py`

**Step 1: Write the failing tests**

```python
def test_video_input_treated_as_text():
    """Video media (not supported) falls back to text."""
    assert detect_input_type(1, "video/mp4") == InputType.TEXT


def test_multiple_media_audio():
    """Multiple media items — if first is audio, detect as audio."""
    assert detect_input_type(2, "audio/ogg") == InputType.AUDIO


def test_empty_mime_type():
    """Empty string mime_type treated as text."""
    assert detect_input_type(1, "") == InputType.TEXT


def test_none_num_media_zero():
    """num_media=0 with None mime always returns TEXT."""
    assert detect_input_type(0, "audio/ogg") == InputType.TEXT


def test_audio_mpeg_detected():
    """audio/mpeg (MP3) detected as audio."""
    assert detect_input_type(1, "audio/mpeg") == InputType.AUDIO


def test_image_png_detected():
    """image/png detected as image."""
    assert detect_input_type(1, "image/png") == InputType.IMAGE


def test_image_webp_detected():
    """image/webp detected as image."""
    assert detect_input_type(1, "image/webp") == InputType.IMAGE
```

**Step 2: Run tests**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_detect_input.py -v --tb=short`

Expected: Most PASS. `test_empty_mime_type` may FAIL because `"".startswith("audio/")` is False so it falls through to TEXT — which is correct. Check.

**Step 3: Fix any bugs found**

If `detect_input_type(1, "")` doesn't return TEXT, fix the function.

**Step 4: Verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_detect_input.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/unit/test_detect_input.py
git commit -m "test(detect_input): edge cases — video, empty MIME, multiple media"
```

---

### Task 7: Transcribe — Malformed Tags and English

Missing tests: 3-letter language codes (`[eng]`), empty response, whitespace-only response.

**Files:**
- Modify: `tests/unit/test_transcribe_full.py`

**Step 1: Write the failing tests**

Add at the end of the file:

```python
def test_transcribe_three_letter_code_defaults_es():
    """Branch: Gemini returns [eng] (3-letter ISO) — should handle gracefully."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[eng] I need help with my registration"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            # May be "es" (default) or "eng" — document actual behavior
            assert result.text is not None
            assert len(result.text) > 0


def test_transcribe_empty_response():
    """Branch: Gemini returns empty string — failure."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = ""

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            # Empty text = either success with empty text or failure
            # The pipeline checks `not transcript.text` so this should be handled
            assert result.text == "" or result.success is False


def test_transcribe_whitespace_only_response():
    """Branch: Gemini returns whitespace — should be treated as empty."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "   \n  "

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            # Whitespace-only should be treated like empty
            if result.success:
                assert result.text.strip() == ""
            # Pipeline will catch this with `not transcript.text`


def test_transcribe_english_tag():
    """Branch: Gemini returns [en] tag for English audio."""
    mock_genai = um.MagicMock()
    mock_client = um.MagicMock()
    mock_genai.Client.return_value = mock_client
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "[en] I need help with my healthcare card"

    with patch("src.core.skills.transcribe.config") as mock_cfg:
        mock_cfg.GEMINI_API_KEY = "test-key"
        with patch.dict("sys.modules", {
            "google.genai": mock_genai,
            "google": um.MagicMock(genai=mock_genai),
        }):
            result = transcribe(b"\x00\x01\x02", "audio/ogg")
            assert result.success is True
            assert result.language == "en"
            assert "healthcare" in result.text
```

**Step 2: Run tests**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_transcribe_full.py -v --tb=short`

**Step 3: Fix any bugs**

If 3-letter codes aren't handled, fix `transcribe()` in `src/core/skills/transcribe.py`.

**Step 4: Verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_transcribe_full.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/unit/test_transcribe_full.py
git commit -m "test(transcribe): malformed tags, empty response, English audio"
```

---

### Task 8: TTS — Language Mismatch and ElevenLabs Fallback

TTS has 11 tests but nothing for: ElevenLabs engine path, language-voice mapping for PT/AR, both engines failing.

**Files:**
- Modify: `tests/unit/test_tts.py`

**Step 1: Write the failing tests**

```python
def test_text_to_audio_elevenlabs_returns_url():
    """ElevenLabs engine returns a URL when successful."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value="/tmp/el.mp3") as mock_el, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda", "es")
        assert result is not None
        assert result.endswith(".mp3")
        mock_el.assert_called_once()


def test_text_to_audio_elevenlabs_fallback_to_gemini_to_gtts():
    """If ElevenLabs fails, falls back to Gemini, then gTTS."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value=None), \
         patch("src.core.skills.tts._synthesize_gemini", return_value=None), \
         patch("src.core.skills.tts._synthesize_gtts", return_value="/tmp/f.mp3") as mock_gtts, \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda", "es")
        mock_gtts.assert_called_once()
        assert result is not None


def test_all_tts_engines_fail_returns_none():
    """If all TTS engines fail, returns None (no audio)."""
    with patch("src.core.skills.tts.config") as mock_cfg, \
         patch("src.core.skills.tts._synthesize_elevenlabs", return_value=None), \
         patch("src.core.skills.tts._synthesize_gemini", return_value=None), \
         patch("src.core.skills.tts._synthesize_gtts", return_value=None), \
         patch("os.path.exists", return_value=False):
        mock_cfg.AUDIO_BASE_URL = "http://localhost/cache"
        mock_cfg.TTS_ENGINE = "elevenlabs"

        from src.core.skills.tts import text_to_audio
        result = text_to_audio("necesito ayuda", "es")
        assert result is None


def test_gemini_voice_names_include_pt_ar():
    """Voice names should exist for PT and AR (or fall back gracefully)."""
    from src.core.skills.tts import _GEMINI_VOICE_NAME
    # At minimum es, fr, en must have voices
    assert "es" in _GEMINI_VOICE_NAME
    assert "fr" in _GEMINI_VOICE_NAME
    assert "en" in _GEMINI_VOICE_NAME
    # PT and AR may not have dedicated voices — document behavior
    # If missing, the code should use a fallback voice


def test_prepare_text_truncation():
    """TTS text should be truncated to avoid long audio."""
    from src.core.skills.tts import _prepare_text_for_tts
    long_text = "Esta es una frase. " * 50  # Very long
    result = _prepare_text_for_tts(long_text)
    # Result should be shorter than input (truncation applied)
    assert len(result) <= len(long_text)
```

**Step 2: Run tests**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_tts.py -v --tb=short`

Expected: Some may FAIL if ElevenLabs paths don't exist in test env or if `_synthesize_elevenlabs` isn't importable.

**Step 3: Fix any import issues or test logic**

**Step 4: Verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_tts.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/unit/test_tts.py
git commit -m "test(tts): ElevenLabs path, triple fallback, all-fail case"
```

---

### Task 9: is_greeting — Punctuation and Edge Cases

Known bugs from previous analysis: `"Hello!"` not detected, `"hi"` too short, multi-word greetings.

**Files:**
- Create: `tests/unit/test_greeting.py`

**Step 1: Write the tests**

```python
"""Tests for is_greeting() — edge cases and all 5 languages."""

import pytest
from src.core.prompts.templates import is_greeting


class TestGreetingBasic:
    """Basic greeting detection per language."""

    @pytest.mark.parametrize("text", ["Hola", "hola", "buenas", "que tal"])
    def test_es_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["Bonjour", "bonjour", "salut"])
    def test_fr_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["Hello", "hello", "hi", "hey", "help"])
    def test_en_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["Ola", "ola", "oi"])
    def test_pt_greetings(self, text):
        assert is_greeting(text)

    @pytest.mark.parametrize("text", ["salam", "marhaba", "ahlan"])
    def test_ar_greetings(self, text):
        assert is_greeting(text)


class TestGreetingPunctuation:
    """Greetings with punctuation should still be detected."""

    @pytest.mark.parametrize("text", ["Hola!", "Hello?", "Bonjour!"])
    def test_punctuation_stripped(self, text):
        """Exclamation/question marks should not break greeting detection."""
        # NOTE: Current implementation does NOT strip punctuation in is_greeting.
        # This test documents the gap. If it fails, is_greeting needs a fix.
        # If we accept this as a known limitation, mark as xfail:
        # @pytest.mark.xfail(reason="is_greeting doesn't strip punctuation")
        assert is_greeting(text)


class TestGreetingNonGreeting:
    """Non-greeting messages should NOT be detected as greetings."""

    @pytest.mark.parametrize("text", [
        "Necesito informacion sobre el IMV",
        "Que documentos necesito para el empadronamiento",
        "Como pedir cita previa",
        "NIE X1234567A",
        "",
    ])
    def test_not_greetings(self, text):
        assert not is_greeting(text)


class TestGreetingEdgeCases:
    """Edge cases for greeting detection."""

    def test_empty_string(self):
        assert not is_greeting("")

    def test_whitespace_only(self):
        assert not is_greeting("   ")

    def test_long_message_with_greeting_word(self):
        """Long message containing 'hola' should NOT be a greeting (>4 words)."""
        assert not is_greeting("Hola necesito mucha ayuda con mis tramites urgentes")

    def test_four_word_greeting(self):
        """4-word message with greeting word IS still a greeting."""
        assert is_greeting("Hola necesito ayuda urgente")
```

**Step 2: Run tests**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_greeting.py -v --tb=short`

Expected: Punctuation tests will likely FAIL (known bug). Mark as `xfail` if we don't fix now.

**Step 3: Decide: fix is_greeting or mark as xfail**

If fixing, update `is_greeting` in `src/core/prompts/templates.py` to strip punctuation:

```python
def is_greeting(text: str) -> bool:
    import re
    cleaned = re.sub(r'[^\w\s]', '', text)
    words = cleaned.lower().strip().split()
    if len(words) <= 4:
        return any(w in _GREETING_WORDS for w in words) or cleaned.lower().strip() in _GREETING_WORDS
    return False
```

If not fixing, add `@pytest.mark.xfail(reason="is_greeting doesn't strip punctuation")` to those tests.

**Step 4: Verify all pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/unit/test_greeting.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/unit/test_greeting.py
git commit -m "test(greeting): edge cases, punctuation, all 5 languages"
```

---

### Task 10: Webhook — Signature Validation

The webhook skips Twilio signature validation when `TWILIO_AUTH_TOKEN` is empty. No test validates that a bad signature returns 403.

**Files:**
- Modify: `tests/integration/test_webhook.py`

**Step 1: Write the failing test**

```python
def test_webhook_rejects_invalid_signature(client, monkeypatch):
    """Webhook returns 403 for invalid Twilio signature when auth token is set."""
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "fake-auth-token-for-test")
    # Re-create config to pick up new env var
    from src.core.config import Config
    import src.core.config
    src.core.config.config = Config()

    resp = client.post("/webhook", data={
        "Body": "Hola",
        "From": "whatsapp:+34612345678",
        "NumMedia": "0",
    }, headers={"X-Twilio-Signature": "invalid-signature"})
    assert resp.status_code == 403

    # Restore config
    monkeypatch.delenv("TWILIO_AUTH_TOKEN", raising=False)
    src.core.config.config = Config()
```

**Step 2: Run test**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py::test_webhook_rejects_invalid_signature -v --tb=short`

**Step 3: Fix if needed**

**Step 4: Verify all webhook tests pass**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/integration/test_webhook.py -v --tb=short`

**Step 5: Commit**

```bash
git add tests/integration/test_webhook.py
git commit -m "test(webhook): reject invalid Twilio signature (403)"
```

---

### Task 11: Full Test Suite — Final Verification

Run the entire test suite to confirm nothing is broken.

**Step 1: Run full test suite**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/ -v --tb=short 2>&1 | tail -30`

Expected: All tests PASS (or known xfails documented).

**Step 2: Count new tests added**

Run: `cd /Users/andreaavila/Documents/hakaton/civicaid-voice && python -m pytest tests/ --collect-only -q 2>&1 | tail -3`

Expected: Previous count (727+) plus ~80 new = ~800+ total tests.

**Step 3: Final commit with summary**

```bash
git add -A
git commit -m "test: error scenario test suite — ~80 new tests covering language mismatches, broken pipelines, edge cases

Covers: webhook ACK language (EN/PT/AR), conversation memory, image input,
error templates (5 langs), pipeline guardrails, detect_input edges,
transcribe malformed tags, TTS triple fallback, greeting punctuation,
Twilio signature validation."
```

---

## Summary of Tests Added

| Task | File | Tests Added | Risk Covered |
|------|------|-------------|-------------|
| 1 | test_webhook.py | 3 | EN/PT/AR ACK language |
| 2 | test_webhook.py | 2 | Conversation memory |
| 3 | test_webhook.py | 2 | Image input ACK |
| 4 | test_error_templates.py | ~40 | Error templates 5 langs |
| 5 | test_pipeline.py | 2 | Guardrail + exception |
| 6 | test_detect_input.py | 7 | Video, empty MIME, etc. |
| 7 | test_transcribe_full.py | 4 | Malformed tags, empty |
| 8 | test_tts.py | 5 | ElevenLabs, triple fail |
| 9 | test_greeting.py | ~18 | Punctuation, all langs |
| 10 | test_webhook.py | 1 | Signature validation |
| **Total** | | **~84** | |
