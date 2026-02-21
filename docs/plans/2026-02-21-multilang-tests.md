# Multi-Language Tests Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add tests that verify multi-language (ES/FR/EN/PT/AR) behavior across all Clara modules — system prompt, templates, guardrails, WhatsApp formatting, TTS, and pipeline flow.

**Architecture:** Each task targets a specific module's language-dependent behavior. Tests verify that all 5 supported languages (es, fr, en, pt, ar) work correctly through each layer.

**Tech Stack:** pytest, unittest.mock

---

### Task 1: System Prompt — Language-Specific Tone Rules

**Files:**
- Create: `tests/unit/test_system_prompt.py`

**Tests (~20):**
- `build_prompt` returns prompt with ES tone for `language="es"`
- `build_prompt` returns prompt with FR tone (vouvoiement) for `language="fr"`
- `build_prompt` returns prompt with EN tone for `language="en"`
- `build_prompt` returns prompt with PT tone (europeu) for `language="pt"`
- `build_prompt` returns prompt with AR tone (MSA) for `language="ar"`
- Unknown language falls back to ES tone
- `{language}` placeholder is replaced with correct code
- Memory blocks are injected when provided
- Memory blocks are empty string when not provided
- KB context is injected correctly
- Chunks block is injected correctly
- Prompt contains E-V-I pattern section
- Prompt contains security section
- Prompt contains citation section
- Each language tone is at least 50 chars
- All 5 languages present in _LANGUAGE_TONES
- FR tone includes "vouvoie" (formal)
- PT tone includes "europeu" (not Brazilian)
- AR tone includes "MSA" or "estandar"
- ES tone includes "tutea" (informal)

---

### Task 2: Template Completeness — All Keys x All Languages

**Files:**
- Modify: `tests/unit/test_error_templates.py`

**Tests (~30):**
- All ACK templates (ack_greeting, ack_text, ack_audio, ack_image) exist for all 5 languages
- All ACK templates are at least 15 chars
- Closing template exists for all 5 languages
- Memory templates exist for es/fr/en (only 3 supported for memory)
- FR templates use formal "vous" (not "tu")
- PT templates use European Portuguese hints ("podes", not "voce pode")
- AR templates contain Arabic script characters
- ES templates use informal "tu" form
- EN templates use "you" form
- ACK templates don't contain URLs (ACK should be simple)
- Error templates contain at least one help resource per language
- Each language's ack_greeting mentions "Clara"
- Closing templates offer continued help in all languages

---

### Task 3: Guardrails — Multi-Language Input Recognition

**Files:**
- Modify: `tests/unit/test_guardrails.py`

**Tests (~15):**
- pre_check blocks "je veux me suicider" (French self-harm variant) — note: guardrails are ES-only, so this tests the gap
- pre_check allows safe French input: "Bonjour, j'ai besoin d'aide"
- pre_check allows safe English input: "Hello, I need help with registration"
- pre_check allows safe Portuguese input: "Ola, preciso de ajuda"
- pre_check allows safe Arabic transliterated input: "Salam, ahlan musaada"
- pre_check allows "NIE" (looks like it could be flagged but shouldn't be)
- pre_check allows "cita previa" (appointment, not violence)
- post_check adds disclaimer for French legal mention "avocat"? (only if pattern matches)
- post_check redacts NIE format in French context response
- post_check preserves clean French response
- post_check preserves clean English response
- post_check preserves clean Arabic response
- BLOCKED_PATTERNS responses always contain a phone number (emergency or help)
- BLOCKED_PATTERNS responses don't contain emoji

---

### Task 4: WhatsApp Format — Multi-Language Content

**Files:**
- Modify: `tests/unit/test_whatsapp_format.py`

**Tests (~12):**
- French numbered steps get bolded: "1. Votre passeport"
- English numbered steps get bolded: "1. Your passport"
- Portuguese numbered steps get bolded: "1. O teu passaporte"
- Arabic text with numbers gets formatted correctly
- ATENCION keyword gets bolded (Spanish synonym of OJO)
- Already-formatted French text is not double-bolded
- Empty string returns empty string
- Whitespace-only returns whitespace
- Mixed language text (ES+FR) gets formatted
- Long numbered list (1-10) all get bolded
- Text with URLs and numbers doesn't mangle the URL
- Text with decimal numbers ("3.5 euros") doesn't get formatted as step

---

### Task 5: TTS Voice Selection Per Language

**Files:**
- Modify: `tests/unit/test_tts.py`

**Tests (~12):**
- Gemini voice for ES is "Aoede" (warm Clara voice)
- Gemini voice for FR exists and is different from ES
- Gemini voice for EN exists and is different from ES
- Gemini voice style for ES mentions "Clara"
- Gemini voice style for FR mentions "Clara"
- Gemini voice style for EN mentions "Clara"
- ElevenLabs voice ID for ES exists
- ElevenLabs voice ID for FR exists
- ElevenLabs voice ID for EN exists
- Prepare text function handles French parenthetical explanations
- Prepare text function handles Portuguese numbered steps
- Truncation works on French long text (word boundary in French)

---

### Task 6: Language Detection Edge Cases — Real-World Phrases

**Files:**
- Modify: `tests/unit/test_detect_lang.py`

**Tests (~20):**
- Detects ES from "necesito ayuda con el empadronamiento"
- Detects FR from "j'ai besoin d'aide pour l'inscription"
- Detects EN from "I need help with my registration"
- Detects PT from "preciso de ajuda com o registo"
- Detects AR from "salam musaada" (transliterated)
- Mixed ES+FR defaults to keyword winner
- Catalan "ca" mapped to "es"
- Galician "gl" mapped to "es"
- Empty text with phone returns conversation memory
- Empty text without phone returns "es"
- Very short FR ("merci") uses keyword hint
- Very short EN ("help") uses keyword hint
- Very short PT ("ola") uses keyword hint
- Code-mixed: "Hola, I need help" — tests the hybrid
- Conversation memory persists across calls
- Setting and getting conversation lang works
- Number-only input ("12345") returns default or memory
- URL-only input returns default or memory
- Emoji-only input returns default
- Punctuation-heavy input still detects language

---

### Task 7: Integration — Webhook ACK Language Flow

**Files:**
- Modify: `tests/integration/test_webhook.py`

**Tests (~8):**
- PT speaker gets PT greeting ACK on first message
- AR speaker gets AR greeting ACK on first message
- Language switches correctly: FR first, then ES message gets ES ACK
- Three messages same user: EN, EN, ambiguous — third still EN
- Greeting in each language gets ack_greeting (not ack_text)
- Non-greeting in each language gets ack_text
- Audio from FR-memory user gets FR ack_audio
- Image from EN-memory user gets EN ack_image

---

### Task 8: Commit

```bash
git add tests/unit/test_system_prompt.py tests/unit/test_error_templates.py \
  tests/unit/test_guardrails.py tests/unit/test_whatsapp_format.py \
  tests/unit/test_tts.py tests/unit/test_detect_lang.py \
  tests/integration/test_webhook.py docs/plans/2026-02-21-multilang-tests.md
git commit -m "test: add multi-language tests across all modules (ES/FR/EN/PT/AR)"
```
