# Fase 5 — Voz de Clara: Tone Rewrite Report

**Fecha:** 2026-02-20
**Implementador:** Claude Code (multi-agent, 5 agentes)
**Plan de referencia:** docs/01-phases/fase5-voz-clara/FASE5-VOZ-CLARA.md

## Resumen

| Area | Estado | Cambio |
|------|--------|--------|
| system_prompt.py | OK | Tone block IDENTIDAD/TONO/NUNCA DIGAS + few-shot examples |
| VISION_PROMPT | OK | Empathy + FR support via VISION_PROMPTS dict |
| templates.py | OK | No emoji, 2 options on fail, closing template added |
| guardrails.py | OK | Tu vs usted — no formal "consulte"/"usted" in blocklist |
| demo_cache.json | OK | E-V-I pattern, warm tone, no exclamation spam |
| tts.py | OK | Gemini TTS (Sulafat voice) + gTTS fallback |

## Gates

| Gate | Resultado |
|------|-----------|
| G1 (tests) | PASS — 535 passed, 19 skipped, 5 xpassed |
| G2 (lint) | PASS — All checks passed (after fixing unused imports) |
| G3 (boot) | PASS — BOOT OK |
| G4 (ACK no emoji) | PASS — "Lo miro ahora mismo, dame un momento." |
| G5 (closing) | PASS — "Si necesitas algo mas, aqui estoy. Mucha suerte con tu tramite." |
| G6 (2 options) | PASS — "Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta." |
| G7 (no formal) | PASS — No "consulte" in BLOCKED_PATTERNS |
| G8 (saludo OK) | PASS — No exclamation spam, no emoji |
| G9 (tone block) | PASS — IDENTIDAD + NUNCA DIGAS blocks present |
| G10 (TTS_ENGINE) | PASS — TTS_ENGINE: gtts (default, Gemini available) |
| G11 (Gemini TTS) | PASS — Sulafat voice for es confirmed |

## Manual Tone Verification

- **ACK templates (ack_text, ack_audio, ack_image):** No emoji, warm and concise.
- **guardrails.py:** No "consulte", no "usted" anywhere in file. Uses tu register.
- **demo_cache.json saludo_es:** "Hola, soy Clara." — no exclamation after Hola, no emoji.
- **whisper_fail:** "No he podido escuchar bien tu audio" — blame on system, not user. Two recovery options provided.
- **vision_fail:** "No he podido ver bien la imagen" — blame on system, two recovery options.
- **All fail templates:** Self-blame pattern ("no he podido") + 2 alternatives offered.

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
- tests/unit/test_analyze_image.py
- tests/unit/test_guardrails.py
- tests/unit/test_templates_image.py
- tests/unit/test_config.py
- CLAUDE.md

## Commits

```
e5562c2 feat(fase5): integrate Gemini TTS with Clara warm voice — fallback to gTTS
5edc67c feat(fase5): add empathy + multilingual support to VISION_PROMPT
60ce2ee feat(fase5): fix formal register in guardrails — use tu instead of usted
c740f04 feat(fase5): inject Clara tone block + few-shot examples into system prompt
```
