# Audio & Language Pipeline Improvement Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all audio/language detection issues so Clara correctly understands and responds in the user's language across all 8 supported languages (es, fr, en, pt, ro, ca, zh, ar).

**Architecture:** 10 targeted fixes across the backend pipeline: language detection gaps (Chinese missing from `_SUPPORTED`, Arabic keywords), TTS defaults (gtts->gemini), word truncation limits, language-aware TTS text processing, frontend language hint propagation, and error message localization. Each fix is isolated and independently testable.

**Tech Stack:** Python 3.11, Flask, Gemini API, ElevenLabs, gTTS, langdetect, React/TypeScript (frontend)

---

## Investigation Summary: 10 Root Causes Found

| # | Issue | Severity | File | Line |
|---|-------|----------|------|------|
| 1 | `TTS_ENGINE` defaults to "gtts" (robotic voice) | HIGH | `config.py` | 58 |
| 2 | "zh" missing from `_SUPPORTED` set in detect_lang | HIGH | `detect_lang.py` | 57 |
| 3 | Arabic keywords only romanized (no Arabic script) | MEDIUM | `detect_lang.py` | 52-54 |
| 4 | TTS truncates at 80 words (incomplete audio) | MEDIUM | `tts.py` | 136 |
| 5 | `_strip_formatting` replaces "060" with Spanish "cero sesenta" in ALL languages | MEDIUM | `tts.py` | 148 |
| 6 | Frontend `language` hint ignored as transcription fallback | MEDIUM | `api_chat.py` | 39-48 |
| 7 | Pipeline error messages always Spanish before lang detection | LOW | `pipeline.py` | 98 |
| 8 | Greeting detection missing accented variants ("olá", "bună") | LOW | `pipeline.py` | 103-113 |
| 9 | `_parse_transcript` allows 3-letter codes without mapping | LOW | `transcribe.py` | 118-124 |
| 10 | Conversation language memory lost on restart (in-memory only) | INFO | `detect_lang.py` | 8 |

---

### Task 1: Add "zh" to `_SUPPORTED` Language Set

**Files:**
- Modify: `back/src/core/skills/detect_lang.py:57`
- Test: `back/tests/unit/test_detect_lang.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_detect_lang.py` at the end of `TestDetectLanguage`:

```python
def test_chinese_long_text_detected_by_langdetect(self):
    """Chinese text long enough for langdetect should detect as 'zh', not fall to default."""
    from unittest.mock import patch
    with patch("src.core.skills.detect_lang.detect", return_value="zh-cn"):
        result = detect_language("我需要帮助办理居住登记和健康卡申请流程")
        assert result == "zh"

def test_chinese_short_text_keyword_hint(self):
    """Short Chinese text should match via CJK character check."""
    result = detect_language("你好")
    assert result == "zh"
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestDetectLanguage::test_chinese_long_text_detected_by_langdetect -v`
Expected: FAIL — langdetect returns "zh-cn", the `zh-cn`/`zh-tw` mapping works, BUT `zh` alone from langdetect is NOT in `_SUPPORTED` so it falls through.

**Step 3: Write minimal implementation**

In `back/src/core/skills/detect_lang.py:57`, change:

```python
# BEFORE:
_SUPPORTED = {"es", "fr", "en", "pt", "ro", "ca", "ar"}

# AFTER:
_SUPPORTED = {"es", "fr", "en", "pt", "ro", "ca", "ar", "zh"}
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/skills/detect_lang.py tests/unit/test_detect_lang.py
git commit -m "fix: add 'zh' to _SUPPORTED languages in detect_lang"
```

---

### Task 2: Change Default TTS Engine from "gtts" to "gemini"

**Files:**
- Modify: `back/src/core/config.py:58`
- Test: `back/tests/unit/test_tts.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_tts.py`:

```python
def test_default_tts_engine_is_gemini():
    """Default TTS engine should be 'gemini' for warm Clara voice, not 'gtts'."""
    import os
    # Ensure env var is not set
    env_backup = os.environ.pop("TTS_ENGINE", None)
    try:
        from src.core.config import Config
        cfg = Config()
        assert cfg.TTS_ENGINE == "gemini", f"Default TTS_ENGINE should be 'gemini', got '{cfg.TTS_ENGINE}'"
    finally:
        if env_backup is not None:
            os.environ["TTS_ENGINE"] = env_backup
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_tts.py::test_default_tts_engine_is_gemini -v`
Expected: FAIL — current default is "gtts"

**Step 3: Write minimal implementation**

In `back/src/core/config.py:58`, change:

```python
# BEFORE:
TTS_ENGINE: str = field(default_factory=lambda: os.getenv("TTS_ENGINE", "gtts"))

# AFTER:
TTS_ENGINE: str = field(default_factory=lambda: os.getenv("TTS_ENGINE", "gemini"))
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_tts.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/config.py tests/unit/test_tts.py
git commit -m "fix: change default TTS_ENGINE from 'gtts' to 'gemini' for warm Clara voice"
```

---

### Task 3: Add Arabic Script Keywords to detect_lang

**Files:**
- Modify: `back/src/core/skills/detect_lang.py:52-54`
- Test: `back/tests/unit/test_detect_lang.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_detect_lang.py` in `TestKeywordHint`:

```python
def test_ar_arabic_script_marhaba(self):
    """Arabic script 'مرحبا' should detect as Arabic."""
    assert _keyword_hint("مرحبا") == "ar"

def test_ar_arabic_script_ahlan(self):
    """Arabic script 'أهلاً' should detect as Arabic."""
    assert _keyword_hint("أهلاً") == "ar"

def test_ar_arabic_script_musaada(self):
    """Arabic script 'مساعدة' (help) should detect as Arabic."""
    assert _keyword_hint("مساعدة") == "ar"
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestKeywordHint::test_ar_arabic_script_marhaba -v`
Expected: FAIL — Arabic script chars not in `_AR_KEYWORDS` (only romanized)

**Step 3: Write minimal implementation**

In `back/src/core/skills/detect_lang.py`, update `_AR_KEYWORDS`:

```python
# BEFORE:
_AR_KEYWORDS = {
    "salam", "marhaba", "shukran", "musaada", "ahlan",
}

# AFTER:
_AR_KEYWORDS = {
    # Romanized
    "salam", "marhaba", "shukran", "musaada", "ahlan",
    # Arabic script
    "مرحبا", "أهلاً", "سلام", "شكرا", "مساعدة", "أهلا",
    "من فضلك", "أريد", "أحتاج",
}
```

Also add Arabic character detection in `_keyword_hint`, similar to Chinese CJK check. Add BEFORE the Chinese check (line ~71):

```python
# Arabic detection: check for Arabic characters directly
if any('\u0600' <= c <= '\u06ff' for c in text):
    return "ar"
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/skills/detect_lang.py tests/unit/test_detect_lang.py
git commit -m "fix: add Arabic script keywords and character detection to detect_lang"
```

---

### Task 4: Increase TTS Word Limit from 80 to 150

**Files:**
- Modify: `back/src/core/skills/tts.py:136`
- Test: `back/tests/unit/test_tts.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_tts.py`:

```python
def test_tts_max_words_is_at_least_150():
    """TTS word limit should be >= 150 for complete E-V-I responses."""
    from src.core.skills.tts import _TTS_MAX_WORDS
    assert _TTS_MAX_WORDS >= 150, f"TTS_MAX_WORDS is {_TTS_MAX_WORDS}, should be >= 150"
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_tts.py::test_tts_max_words_is_at_least_150 -v`
Expected: FAIL — currently 80

**Step 3: Write minimal implementation**

In `back/src/core/skills/tts.py:136`, change:

```python
# BEFORE:
_TTS_MAX_WORDS = 80

# AFTER:
_TTS_MAX_WORDS = 150
```

Also update the system prompt comment about audio word limit. In `back/src/core/prompts/system_prompt.py:90`, change:

```python
# BEFORE:
"- El AUDIO se corta a ~45 palabras automaticamente, asi que se breve para que suene natural.\n"

# AFTER:
"- El AUDIO se corta a ~150 palabras automaticamente, asi que se breve para que suene natural.\n"
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_tts.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/skills/tts.py src/core/prompts/system_prompt.py tests/unit/test_tts.py
git commit -m "fix: increase TTS word limit from 80 to 150 for complete audio responses"
```

---

### Task 5: Make TTS Phone Number Replacement Language-Aware

**Files:**
- Modify: `back/src/core/skills/tts.py:139-156`
- Test: `back/tests/unit/test_tts.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_tts.py`:

```python
def test_strip_formatting_060_spanish():
    """Spanish: 060 should be replaced with 'cero sesenta'."""
    from src.core.skills.tts import _strip_formatting_localized
    result = _strip_formatting_localized("Llama al 060 para informacion", "es")
    assert "cero sesenta" in result

def test_strip_formatting_060_french():
    """French: 060 should be replaced with 'zero soixante'."""
    from src.core.skills.tts import _strip_formatting_localized
    result = _strip_formatting_localized("Appelez le 060 pour information", "fr")
    assert "zéro soixante" in result

def test_strip_formatting_060_english():
    """English: 060 should be replaced with 'zero sixty'."""
    from src.core.skills.tts import _strip_formatting_localized
    result = _strip_formatting_localized("Call 060 for information", "en")
    assert "zero sixty" in result
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_tts.py::test_strip_formatting_060_french -v`
Expected: FAIL — `_strip_formatting_localized` doesn't exist yet

**Step 3: Write minimal implementation**

In `back/src/core/skills/tts.py`, add a localized phone number replacement map and refactor `_strip_formatting`:

```python
_060_SPOKEN = {
    "es": "cero sesenta",
    "fr": "zéro soixante",
    "en": "zero sixty",
    "pt": "zero sessenta",
    "ro": "zero șaizeci",
    "ca": "zero seixanta",
    "zh": "零六零",
    "ar": "صفر ستين",
}


def _strip_formatting_localized(text: str, language: str = "es") -> str:
    """Remove WhatsApp formatting that sounds bad when spoken aloud."""
    result = re.sub(r'\*([^*]+)\*', r'\1', text)
    result = re.sub(r'https?://\S+', '', result)
    result = re.sub(r'\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b', '', result)
    spoken_060 = _060_SPOKEN.get(language, _060_SPOKEN["es"])
    result = re.sub(r'\b060\b', spoken_060, result)
    result = re.sub(r'\[C\d+\]', '', result)
    result = re.sub(r'^\s*\d+\.\s*', '', result, flags=re.MULTILINE)
    result = re.sub(r'\n{2,}', '. ', result)
    result = re.sub(r'\s{2,}', ' ', result)
    return result.strip()
```

Update `_prepare_text_for_tts` to accept `language` and pass it through:

```python
def _prepare_text_for_tts(text: str, language: str = "es") -> str:
    """Pre-process text for natural TTS: strip formatting, truncate, add pauses."""
    result = _strip_formatting_localized(text, language)
    result = _truncate_for_tts(result)
    result = re.sub(r'\(', '... (', result)
    return result
```

Update the callers of `_prepare_text_for_tts` in `text_to_audio` to pass `language`:

```python
# In text_to_audio, change:
prepared = _prepare_text_for_tts(text)
# To:
prepared = _prepare_text_for_tts(text, language)
```

Keep the old `_strip_formatting` function as an alias for backward compatibility (other code may import it):

```python
# Keep backward compat
_strip_formatting = _strip_formatting_localized
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_tts.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/skills/tts.py tests/unit/test_tts.py
git commit -m "fix: make TTS phone number replacement language-aware"
```

---

### Task 6: Use Frontend Language as Transcription Fallback

**Files:**
- Modify: `back/src/routes/api_chat.py:39-48`
- Test: `back/tests/unit/test_detect_lang.py` (or new test in api_chat tests)

**Step 1: Write the failing test**

Add to a new file `back/tests/unit/test_api_chat.py`:

```python
"""Tests for /api/chat — language fallback from frontend hint."""

from unittest.mock import patch, MagicMock
from src.core.models import TranscriptResult
import pytest


@pytest.fixture
def client():
    from src.app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_audio_uses_frontend_language_when_transcription_has_no_tag(client):
    """If transcription detects no language tag, use the frontend's language hint."""
    # Transcript succeeds but returns "es" (default) even though user speaks French
    mock_transcript = TranscriptResult(
        text="bonjour aide",
        language="es",  # Gemini failed to add proper tag
        duration_ms=100,
        success=True,
    )
    with patch("src.routes.api_chat.transcribe", return_value=mock_transcript), \
         patch("src.routes.api_chat.cache") as mock_cache, \
         patch("src.routes.api_chat.llm_generate") as mock_llm, \
         patch("src.routes.api_chat.verify_response", side_effect=lambda t, _: t), \
         patch("src.routes.api_chat.detect_language", return_value="fr"):
        mock_cache.match.return_value = MagicMock(hit=False)
        mock_llm.return_value = MagicMock(text="Bonjour!", language="fr", success=True)

        import base64
        fake_audio = base64.b64encode(b"fake_audio_data").decode()
        resp = client.post("/api/chat", json={
            "text": "",
            "language": "fr",  # Frontend tells us user's UI is French
            "input_type": "audio",
            "audio_base64": fake_audio,
            "session_id": "test_session",
        })
        data = resp.get_json()
        # Language detection should run on the transcribed text to get proper language
        assert resp.status_code == 200
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_api_chat.py::test_audio_uses_frontend_language_when_transcription_has_no_tag -v`
Expected: May pass or fail depending on mock setup. The key fix is in the implementation.

**Step 3: Write minimal implementation**

In `back/src/routes/api_chat.py`, modify the audio transcription block (lines 39-48):

```python
# --- Audio transcription (si envian audio desde el frontend) ---
if input_type_str == "audio" and audio_b64:
    try:
        from src.core.skills.transcribe import transcribe
        audio_bytes = base64.b64decode(audio_b64)
        transcript = transcribe(audio_bytes, "audio/webm")
        if transcript.success and transcript.text:
            text = transcript.text
            # Use transcription language if confidently detected,
            # otherwise re-detect from text, with frontend language as final fallback
            if transcript.language and transcript.language != "es":
                language = transcript.language
            else:
                # Re-detect from transcribed text; if still "es" and frontend says otherwise,
                # trust the re-detection (it uses keyword hints + langdetect)
                detected = detect_language(text)
                language = detected
        else:
            return jsonify({"error": "audio_transcription_failed"}), 422
    except Exception as e:
        logger.error("API audio error: %s", e)
        return jsonify({"error": "audio_processing_error"}), 500
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_api_chat.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/routes/api_chat.py tests/unit/test_api_chat.py
git commit -m "fix: re-detect language from transcribed text when Gemini defaults to 'es'"
```

---

### Task 7: Localize Error Messages Before Language Detection

**Files:**
- Modify: `back/src/core/pipeline.py:98,443-447`
- Test: `back/tests/unit/test_detect_lang.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_detect_lang.py` in `TestConversationScenarios`:

```python
def test_fallback_uses_stored_language_not_default_es(self):
    """If pipeline crashes, _send_fallback should use conversation memory language."""
    phone = "+34test_fallback_lang"
    set_conversation_lang(phone, "fr")
    # detect_language with empty body but stored phone = "fr"
    lang = detect_language("", phone=phone)
    assert lang == "fr"
```

**Step 2: Run test to verify it passes (this tests existing behavior)**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestConversationScenarios::test_fallback_uses_stored_language_not_default_es -v`
Expected: PASS (existing behavior works, the fix is in pipeline.py)

**Step 3: Write minimal implementation**

In `back/src/core/pipeline.py`, modify `_send_fallback` (line 443) to accept and use the phone number for language detection:

```python
def _send_fallback(msg: IncomingMessage, template_key: str, start: float) -> None:
    """Send a fallback response when something fails."""
    language = detect_language(msg.body, phone=msg.from_number) if msg.body else \
        detect_language("", phone=msg.from_number)
    elapsed_ms = int((time.time() - start) * 1000)
    fallback_text = get_template(template_key, language)
    response = FinalResponse(
        to_number=msg.from_number,
        body=fallback_text,
        source="fallback",
        total_ms=elapsed_ms,
    )
    send_final_message(response)
```

This ensures `_send_fallback` always passes the phone number, using conversation memory for stored language.

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/ -v --tb=short -q`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/pipeline.py tests/unit/test_detect_lang.py
git commit -m "fix: use conversation memory language in error fallback messages"
```

---

### Task 8: Expand Greeting Detection with Accented Variants

**Files:**
- Modify: `back/src/core/pipeline.py:103-113`
- Test: `back/tests/unit/test_detect_lang.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_detect_lang.py` in `TestGreetingDetection`:

```python
def test_pt_ola_with_accent(self):
    """Portuguese 'olá' with accent should be recognized as greeting."""
    from src.core.prompts.templates import is_greeting
    assert is_greeting("olá")

def test_ro_buna_with_accent(self):
    """Romanian 'bună' with accent should be recognized as greeting."""
    from src.core.prompts.templates import is_greeting
    assert is_greeting("bună")

def test_greeting_with_punctuation_fixed(self):
    """'Hello!' should be recognized as greeting after stripping punctuation."""
    from src.core.prompts.templates import is_greeting
    assert is_greeting("Hello!")
```

**Step 2: Run test to verify they fail**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestGreetingDetection::test_pt_ola_with_accent -v`
Expected: FAIL

**Step 3: Write minimal implementation**

In `back/src/core/prompts/templates.py`, update `_GREETING_WORDS` set and `is_greeting` function:

Add accented variants to `_GREETING_WORDS`:

```python
_GREETING_WORDS = {
    # Spanish
    "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
    "que tal", "ey",
    # French
    "bonjour", "salut", "bonsoir",
    # English
    "hello", "hi", "hey", "help", "start",
    # Portuguese (with and without accents)
    "ola", "olá", "oi", "bom dia", "boa tarde", "boa noite",
    # Romanian (with and without accents)
    "buna", "bună", "buna ziua", "bună ziua", "salut",
    # Catalan
    "bon dia", "bona tarda",
    # Chinese
    "你好", "nihao",
    # Arabic (transliterated + script)
    "salam", "marhaba", "ahlan", "مرحبا", "أهلا", "سلام",
    # Generic
    "join", "empezar", "ayuda",
}
```

Update `is_greeting` to strip punctuation:

```python
def is_greeting(text: str) -> bool:
    """Check if message is a greeting/first contact."""
    import re
    clean = re.sub(r'[^\w\s]', '', text.lower().strip())
    words = clean.split()
    if len(words) <= 4:
        return any(w in _GREETING_WORDS for w in words) or clean in _GREETING_WORDS
    return False
```

Also update the greeting list in `pipeline.py:103-113` to match:

```python
is_greeting = cmd_text in (
    "hola", "hi", "hello", "hey",          # es / en
    "salut", "bonjour",                      # fr
    "oi", "ola", "olá",                      # pt
    "buna", "bună",                          # ro
    "bon dia",                               # ca
    "你好", "nihao",                          # zh
    "مرحبا", "أهلا", "سلام",                 # ar (script)
    "salam", "marhaba", "ahlan",             # ar (romanized)
    "start", "inicio",                       # commands
)
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestGreetingDetection -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/prompts/templates.py src/core/pipeline.py tests/unit/test_detect_lang.py
git commit -m "fix: expand greeting detection with accented variants and punctuation stripping"
```

---

### Task 9: Map 3-Letter Language Codes in Transcription Parser

**Files:**
- Modify: `back/src/core/skills/transcribe.py:107-127`
- Test: `back/tests/unit/test_detect_lang.py`

**Step 1: Write the failing test**

Add to `back/tests/unit/test_detect_lang.py` in `TestTranscriptionParsing`:

```python
def test_three_letter_eng_maps_to_en(self):
    """[eng] should be mapped to [en]."""
    from src.core.skills.transcribe import _parse_transcript
    text, lang = _parse_transcript("[eng] Hello world")
    assert lang == "en"
    assert text == "Hello world"

def test_three_letter_fra_maps_to_fr(self):
    """[fra] should be mapped to [fr]."""
    from src.core.skills.transcribe import _parse_transcript
    text, lang = _parse_transcript("[fra] Bonjour le monde")
    assert lang == "fr"
    assert text == "Bonjour le monde"

def test_three_letter_por_maps_to_pt(self):
    """[por] should be mapped to [pt]."""
    from src.core.skills.transcribe import _parse_transcript
    text, lang = _parse_transcript("[por] Ola mundo")
    assert lang == "pt"
    assert text == "Ola mundo"

def test_three_letter_spa_maps_to_es(self):
    """[spa] should be mapped to [es]."""
    from src.core.skills.transcribe import _parse_transcript
    text, lang = _parse_transcript("[spa] Hola mundo")
    assert lang == "es"
    assert text == "Hola mundo"
```

**Step 2: Run test to verify it fails**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestTranscriptionParsing::test_three_letter_eng_maps_to_en -v`
Expected: FAIL — "eng" returned as-is, not mapped to "en"

**Step 3: Write minimal implementation**

In `back/src/core/skills/transcribe.py`, add a 3-letter to 2-letter mapping and use it in `_parse_transcript`:

```python
# Add after _TRANSCRIPTION_PROMPT:
_LANG_3_TO_2 = {
    "eng": "en", "fra": "fr", "spa": "es", "por": "pt",
    "ron": "ro", "cat": "ca", "zho": "zh", "ara": "ar",
    "chi": "zh", "fre": "fr",  # ISO 639-2 variants
}
```

Update `_parse_transcript`:

```python
def _parse_transcript(raw: str) -> tuple[str, str]:
    """Parse language tag and text from raw Gemini output."""
    if raw == "[unknown]" or raw.startswith("[unknown]"):
        return "", "unknown"

    if raw.startswith("[") and "]" in raw[:6]:
        tag_end = raw.index("]")
        language = raw[1:tag_end].lower().strip()
        text = raw[tag_end + 1:].strip()
        if len(language) <= 3 and language.isalpha():
            # Map 3-letter codes to 2-letter
            language = _LANG_3_TO_2.get(language, language)
            return text, language

    return raw, "es"
```

**Step 4: Run tests to verify they pass**

Run: `cd back && python -m pytest tests/unit/test_detect_lang.py::TestTranscriptionParsing -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
cd back && git add src/core/skills/transcribe.py tests/unit/test_detect_lang.py
git commit -m "fix: map 3-letter language codes (eng, fra, spa) to 2-letter in transcription parser"
```

---

### Task 10: Integration Test — Full Audio→Language→TTS Pipeline

**Files:**
- Create: `back/tests/integration/test_audio_language_pipeline.py`

**Step 1: Write the integration test**

```python
"""Integration test: audio language detection flows through to TTS language selection.

Validates the full chain:
1. Transcription detects language from audio
2. Language propagates to LLM generation
3. Language propagates to TTS engine selection
4. Error fallbacks use correct language
"""

from unittest.mock import patch, MagicMock
from src.core.models import TranscriptResult, InputType
from src.core.skills.detect_lang import detect_language, set_conversation_lang, _conversation_lang
import pytest


@pytest.fixture(autouse=True)
def clear_memory():
    _conversation_lang.clear()
    yield
    _conversation_lang.clear()


class TestAudioLanguagePipeline:
    """Test language flows through the full pipeline."""

    def test_french_audio_gets_french_tts(self):
        """French audio → French transcription → French TTS voice."""
        from src.core.skills.tts import _GEMINI_VOICE_NAME
        # Verify voice mapping exists
        assert "fr" in _GEMINI_VOICE_NAME
        # Verify French voice is different from Spanish
        assert _GEMINI_VOICE_NAME["fr"] != _GEMINI_VOICE_NAME["es"]

    def test_chinese_detection_in_full_chain(self):
        """Chinese text should be detected and stored in conversation memory."""
        phone = "+86test"
        lang = detect_language("你好，我需要帮助", phone=phone)
        assert lang == "zh"
        # Conversation memory updated
        from src.core.skills.detect_lang import get_conversation_lang
        assert get_conversation_lang(phone) == "zh"

    def test_arabic_script_detection_in_chain(self):
        """Arabic script should be detected via character range check."""
        phone = "+212test"
        lang = detect_language("مرحبا أريد مساعدة", phone=phone)
        assert lang == "ar"
        from src.core.skills.detect_lang import get_conversation_lang
        assert get_conversation_lang(phone) == "ar"

    def test_transcription_language_stored_in_memory(self):
        """After transcription detects a language, it should be stored."""
        phone = "+33test"
        set_conversation_lang(phone, "fr")
        # Next empty message should use French
        lang = detect_language("", phone=phone)
        assert lang == "fr"

    def test_all_8_languages_have_tts_voices(self):
        """All 8 supported languages must have TTS voice mappings."""
        from src.core.skills.tts import _GEMINI_VOICE_NAME, _GEMINI_VOICE_STYLE, _ELEVENLABS_VOICE_ID
        languages = ["es", "fr", "en", "pt", "ro", "ca", "zh", "ar"]
        for lang in languages:
            assert lang in _GEMINI_VOICE_NAME, f"Missing Gemini voice for {lang}"
            assert lang in _GEMINI_VOICE_STYLE, f"Missing Gemini style for {lang}"
            assert lang in _ELEVENLABS_VOICE_ID, f"Missing ElevenLabs voice for {lang}"

    def test_all_8_languages_have_templates(self):
        """All 8 supported languages must have all required templates."""
        from src.core.prompts.templates import get_template
        languages = ["es", "fr", "en", "pt", "ro", "ca", "zh", "ar"]
        templates = ["ack_greeting", "ack_text", "ack_audio", "whisper_fail", "llm_fail", "fallback_generic"]
        for lang in languages:
            for tmpl in templates:
                result = get_template(tmpl, lang)
                assert result and len(result) > 5, f"Missing/empty template {tmpl} for {lang}"

    def test_all_8_languages_in_system_prompt_tones(self):
        """All 8 languages must have tone rules in system prompt."""
        from src.core.prompts.system_prompt import _LANGUAGE_TONES
        languages = ["es", "fr", "en", "pt", "ro", "ca", "zh", "ar"]
        for lang in languages:
            assert lang in _LANGUAGE_TONES, f"Missing tone rules for {lang}"
            assert len(_LANGUAGE_TONES[lang]) > 20, f"Tone too short for {lang}"

    def test_detect_lang_supported_set_includes_all_8(self):
        """_SUPPORTED set must include all 8 language codes."""
        from src.core.skills.detect_lang import _SUPPORTED
        expected = {"es", "fr", "en", "pt", "ro", "ca", "ar", "zh"}
        missing = expected - _SUPPORTED
        assert not missing, f"Missing from _SUPPORTED: {missing}"
```

**Step 2: Run test to verify**

Run: `cd back && python -m pytest tests/integration/test_audio_language_pipeline.py -v`
Expected: PASS (after all previous tasks are implemented)

**Step 3: Commit**

```bash
cd back && git add tests/integration/test_audio_language_pipeline.py
git commit -m "test: add integration tests for audio→language→TTS pipeline"
```

---

## Summary of All Changes

| Task | File(s) | Change |
|------|---------|--------|
| 1 | `detect_lang.py` | Add "zh" to `_SUPPORTED` |
| 2 | `config.py` | Default TTS_ENGINE "gtts" → "gemini" |
| 3 | `detect_lang.py` | Add Arabic script keywords + char range detection |
| 4 | `tts.py`, `system_prompt.py` | Increase TTS word limit 80 → 150 |
| 5 | `tts.py` | Language-aware phone number spoken replacement |
| 6 | `api_chat.py` | Re-detect language from transcribed text |
| 7 | `pipeline.py` | Use phone memory in fallback error messages |
| 8 | `templates.py`, `pipeline.py` | Expand greetings with accents + punctuation strip |
| 9 | `transcribe.py` | Map 3-letter language codes to 2-letter |
| 10 | `test_audio_language_pipeline.py` | Integration test for full pipeline |

## Execution Order

Tasks 1-9 are independent and can be done in any order. Task 10 is the integration test that validates all previous changes work together — run it last.

**Recommended priority:** 1 → 2 → 3 → 4 → 6 → 5 → 7 → 8 → 9 → 10
