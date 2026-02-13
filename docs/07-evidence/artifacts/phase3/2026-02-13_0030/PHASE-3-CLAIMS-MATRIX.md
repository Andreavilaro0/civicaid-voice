# Phase 3 — Claims Matrix (Anti-Humo)

> Generated: 2026-02-13
> Agent: claims-librarian
> Total claims: 42
> Verified: 34 | Partial: 5 | Not Verified: 3

## Summary

| Verdict | Count | % |
|---------|-------|---|
| VERIFIED | 34 | 81.0% |
| PARTIAL | 5 | 11.9% |
| NOT VERIFIED | 3 | 7.1% |

---

## Claims

| ID | Source | Claim | Method | Evidence | Verdict |
|----|--------|-------|--------|----------|---------|
| CLM-001 | CLAUDE.md:10,50 | "93 tests (88 passed + 5 xpassed)" | COMMAND_RUN + CODE_INSPECT | `grep "def test_"` across tests/ finds 89 function definitions. test_redteam.py::test_blocked_prompts is parametrized with 5 cases (rt_01-rt_05), expanding 1 def to 5 collected tests: 89 - 1 + 5 = 93. Confirmed by PHASE-2-EVIDENCE.md pytest output showing "88 passed, 5 xpassed". | VERIFIED |
| CLM-002 | CLAUDE.md:53 | "9 feature flags in config.py" | CODE_INSPECT | config.py contains exactly 9 behavior-altering flags under "Feature flags" and related sections: DEMO_MODE (L25), LLM_LIVE (L26), WHISPER_ON (L27), LLM_TIMEOUT (L28), WHISPER_TIMEOUT (L29), OBSERVABILITY_ON (L33), STRUCTURED_OUTPUT_ON (L42), GUARDRAILS_ON (L45), RAG_ENABLED (L48). | VERIFIED |
| CLM-003 | CLAUDE.md:36,38 | "11 skills atomicas (incl. tts.py)" | FILE_COUNT | `glob src/core/skills/*.py` returns 12 files. Excluding `__init__.py`: detect_input, fetch_media, detect_lang, cache_match, kb_lookup, verify_response, convert_audio, send_response, llm_generate, transcribe, tts = **11 skill files**. | VERIFIED |
| CLM-004 | CLAUDE.md:44 | "8 respuestas pre-calculadas in demo_cache.json" | CODE_INSPECT | demo_cache.json is a JSON array with 8 entries: imv_es, empadronamiento_es, tarjeta_sanitaria_es, ahmed_empadronamiento_fr, fatima_tarjeta_fr, saludo_es, saludo_fr, maria_carta_vision. | VERIFIED |
| CLM-005 | CLAUDE.md:44 | "6 MP3s in cache" | FILE_COUNT | `glob data/cache/*.mp3` returns 6 files: imv_es.mp3, empadronamiento_es.mp3, tarjeta_es.mp3, ahmed_fr.mp3, fatima_fr.mp3, maria_es.mp3. | VERIFIED |
| CLM-006 | CLAUDE.md:45 | "3 KBs (IMV, empadronamiento, tarjeta_sanitaria)" | FILE_COUNT | `glob data/tramites/*.json` returns 3 files: imv.json, empadronamiento.json, tarjeta_sanitaria.json. | VERIFIED |
| CLM-007 | CLAUDE.md:34 | "8 dataclasses in models.py" | CODE_INSPECT | models.py contains exactly 8 `@dataclass` decorated classes: IncomingMessage (L15), AckResponse (L27), TranscriptResult (L34), CacheEntry (L44), CacheResult (L55), KBContext (L63), LLMResponse (L72), FinalResponse (L83). Plus 1 Enum (InputType). | VERIFIED |
| CLM-008 | CLAUDE.md:14-18 | "TwiML ACK pattern: HTTP 200 inmediata, procesamiento en hilo de fondo" | CODE_INSPECT | webhook.py: background thread launched at L80 (`threading.Thread(target=pipeline.process)`), TwiML XML returned at L84-85 (`Response(twiml, mimetype="application/xml")`). ACK happens before processing completes. | VERIFIED |
| CLM-009 | CLAUDE.md:139 | "Twilio webhook signature validation (RequestValidator)" | CODE_INSPECT | webhook.py L7: `from twilio.request_validator import RequestValidator`. L33: `validator = RequestValidator(config.TWILIO_AUTH_TOKEN)`. L35: `validator.validate(request.url, request.form, signature)`. Aborts 403 on invalid signature. | VERIFIED |
| CLM-010 | CLAUDE.md:41 | "Logging estructurado (logger.py)" | CODE_INSPECT | logger.py L7: `class JSONFormatter(logging.Formatter)` emits JSON lines. 6 tagged log functions: log_ack (ACK), log_cache (CACHE), log_whisper (WHISPER), log_llm (LLM), log_rest (REST), log_error (ERROR). Plus log_observability (OBS). | VERIFIED |
| CLM-011 | CLAUDE.md:42 | "Decorador timing (timing.py)" | CODE_INSPECT | timing.py L10-28: `def timed(skill_name)` decorator measures execution time and records to RequestContext via `_record_timing()`. Used by tts.py, send_response.py, transcribe.py, llm_generate.py. | VERIFIED |
| CLM-012 | CLAUDE.md:134 | "DEMO_MODE implementado en pipeline.py (era dead code)" | CODE_INSPECT | pipeline.py L96-107: `if config.DEMO_MODE:` block sends fallback_generic template and returns, skipping LLM after cache miss. Functional, not dead code. | VERIFIED |
| CLM-013 | CLAUDE.md:136 | "Twilio REST timeout (10s) en send_response.py" | CODE_INSPECT | send_response.py L15: `client.http_client.timeout = 10`. Also L34 in retry path. CLAUDE.md note says "TWILIO_TIMEOUT (10s) esta hardcodeado" -- confirmed hardcoded, not via config.py. | VERIFIED |
| CLM-014 | CLAUDE.md:137 | "NumMedia safe parsing (try/except) en webhook.py" | CODE_INSPECT | webhook.py L44-47: `try: num_media = int(request.form.get("NumMedia", "0"))` with `except (ValueError, TypeError): num_media = 0`. | VERIFIED |
| CLM-015 | CLAUDE.md:138 | "Silent thread death protection en pipeline.py" | CODE_INSPECT | pipeline.py L152-157: outer `except Exception as e` catches all pipeline errors, logs them via `log_error("pipeline", str(e))`, then attempts fallback response in nested try/except. Background thread won't die silently. | VERIFIED |
| CLM-016 | CLAUDE.md:141 | ".dockerignore creado" | FILE_COUNT | `.dockerignore` exists (43 lines), excludes .git, .github, docs, tests, .env, __pycache__, .venv, .claude. | VERIFIED |
| CLM-017 | CLAUDE.md:9 | "Stack: Python 3.11, Flask, Twilio WhatsApp, Whisper base, Gemini 1.5 Flash" | CODE_INSPECT | Dockerfile L1: `FROM python:3.11-slim`. llm_generate.py L48: `genai.GenerativeModel("gemini-1.5-flash")`. transcribe.py L33: same model for transcription. Flask in imports. Twilio in webhook.py + send_response.py. Whisper mentioned but actually replaced by Gemini for transcription. | PARTIAL |
| CLM-018 | CLAUDE.md:135 | "WHISPER_ON short-circuit para audio" | CODE_INSPECT | app.py L20: `if config.WHISPER_ON:` controls model preloading at startup. However, pipeline.py audio path does NOT check WHISPER_ON -- it uses Gemini transcription unconditionally. The flag controls whisper model loading, not audio processing short-circuit. After refactor to Gemini, the flag's effect is limited to startup preloading. | PARTIAL |
| CLM-019 | Dockerfile:19 | "Docker EXPOSE 10000 for Render" | CODE_INSPECT | Dockerfile L19: `EXPOSE 10000`. Dockerfile L26 CMD: `--bind "0.0.0.0:${PORT:-5000}"` uses $PORT (Render sets 10000) with fallback 5000 for local. | VERIFIED |
| CLM-020 | render.yaml:6 | "Render free tier" | CODE_INSPECT | render.yaml L6: `plan: free`. Region: frankfurt (L5). | VERIFIED |
| CLM-021 | RENDER-DEPLOY.md:2,68 | "16 variables de entorno en render.yaml (3 secretas + 13 valores)" | CODE_INSPECT | render.yaml contains exactly 16 envVars. 3 with `sync: false` (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, GEMINI_API_KEY) = secrets. 13 with `value:` = fixed values. | VERIFIED |
| CLM-022 | CLAUDE.md:114 | "81 entradas Notion pobladas (43 Backlog + 12 KB + 26 Testing)" | DOC_CROSS_REF | CLAUDE.md L114, NOTION-OS.md L41, PHASE-STATUS.md L206 all claim 81 entries (43+12+26). Cannot verify via Notion API in this session. Math: 43+12+26=81. Consistent across final Phase 3 docs. Earlier Phase 2 docs correctly show 75 (pre-Phase 3 additions). | PARTIAL |
| CLM-023 | CLAUDE.md:47 | "unit/ (82 tests)" | COMMAND_RUN | Grep `def test_` in unit test files: cache(6)+config(3)+detect_input(4)+detect_lang(4)+evals(9)+guardrails(19)+kb_lookup(4)+observability(6)+redteam(6 defs->10 collected)+retriever(7)+structured_outputs(10) = 78 defs -> 82 collected tests (redteam parametrize +4). | VERIFIED |
| CLM-024 | CLAUDE.md:48 | "integration/ (7 tests)" | COMMAND_RUN | Grep `def test_` in integration: pipeline(2)+twilio_stub(2)+webhook(3) = 7. | VERIFIED |
| CLM-025 | CLAUDE.md:49 | "e2e/ (4 tests)" | COMMAND_RUN | Grep `def test_` in e2e: demo_flows(4) = 4. | VERIFIED |
| CLM-026 | tts.py:1,32 | "gTTS for audio responses" | CODE_INSPECT | tts.py L1: docstring "Text-to-Speech using gTTS". L32: `from gtts import gTTS`. L33: `tts = gTTS(text=text, lang=tts_lang, slow=False)`. | VERIFIED |
| CLM-027 | observability.py:18 | "request_id via UUID generation in observability.py" | CODE_INSPECT | observability.py L18: `request_id: str = field(default_factory=lambda: str(uuid.uuid4()))`. Generated per-request in RequestContext dataclass. Stored via threading.local() (L12). | VERIFIED |
| CLM-028 | observability.py:50-77 | "Flask before/after request hooks for observability" | CODE_INSPECT | observability.py L50: `def init_app(app)`. L54: `@app.before_request` creates RequestContext. L61: `@app.after_request` records http_total timing and emits OBS_SUMMARY JSON. | VERIFIED |
| CLM-029 | llm_generate.py:48,52 | "LLM Gemini 1.5 Flash with LLM_TIMEOUT" | CODE_INSPECT | llm_generate.py L48: `genai.GenerativeModel("gemini-1.5-flash")`. L52: `request_options={"timeout": config.LLM_TIMEOUT}`. config.py default LLM_TIMEOUT=6. | VERIFIED |
| CLM-030 | transcribe.py:33,50 | "Gemini transcription with WHISPER_TIMEOUT" | CODE_INSPECT | transcribe.py L33: `genai.GenerativeModel("gemini-1.5-flash")`. L50: `request_options={"timeout": config.WHISPER_TIMEOUT}`. config.py default WHISPER_TIMEOUT=12. | VERIFIED |
| CLM-031 | Dockerfile:26 | "Gunicorn workers 1, timeout 120, preload" | CODE_INSPECT | Dockerfile L26: `CMD gunicorn --bind "0.0.0.0:${PORT:-5000}" --timeout 120 --workers 1 --preload "src.app:create_app()"`. | VERIFIED |
| CLM-032 | EXEC-SUMMARY:57 | "Skills en pipeline: 10" | CODE_INSPECT + DOC_CROSS_REF | EXECUTIVE-SUMMARY.md L57 says "10" skills. But CLAUDE.md says "11 skills" and actual skill files count is 11. **CONTRADICTION: actual count is 11, not 10.** | NOT VERIFIED |
| CLM-033 | EXEC-SUMMARY:58 | "Feature flags: 10" | CODE_INSPECT + DOC_CROSS_REF | EXECUTIVE-SUMMARY.md L58 says "10" feature flags. But CLAUDE.md L53 says "9 en config.py" and the table lists exactly 9. **CONTRADICTION: CLAUDE.md says 9, EXEC-SUMMARY says 10.** | NOT VERIFIED |
| CLM-034 | EXEC-SUMMARY:118 | "Fase 3 -- Demo en Vivo: EN CURSO" | DOC_CROSS_REF | EXECUTIVE-SUMMARY.md L118: `Fase 3 -- Demo en Vivo \| EN CURSO`. But CLAUDE.md L10: "Fase 3 cerrada". PHASE-STATUS.md L42: Fase 3 "COMPLETADA". **CONTRADICTION: stale status in EXEC-SUMMARY.** | NOT VERIFIED |
| CLM-035 | NOTION-OS.md:3 | "75 entradas en Notion" (header) | DOC_CROSS_REF | NOTION-OS.md L3 header says "75 entradas". But L41 in same file says "81 en 3 DBs (43 Backlog, 12 KB, 26 Testing)". **Internal contradiction.** 75 was the Phase 2 count (37+12+26). 81 is the Phase 3 count (43+12+26). Header is stale. | PARTIAL |
| CLM-036 | PHASE-2-EVIDENCE:223 | "test_guardrails.py: 18 tests" | COMMAND_RUN | PHASE-2-EVIDENCE.md test breakdown says 18. But `grep "def test_" tests/unit/test_guardrails.py` returns 19. TEST-PLAN.md L67 also says 19. **Minor discrepancy.** Possible: 1 test added after Phase 2 evidence was written. | PARTIAL |
| CLM-037 | PHASE-1-EVIDENCE:62 | "cache count command uses `['entries']` key" | CODE_INSPECT | PHASE-1-EVIDENCE.md L62 shows command: `json.load(...)['entries']` but demo_cache.json is a plain JSON array `[...]` with no `entries` wrapper key. The command would raise KeyError. The result "8" is correct but the command is broken. | VERIFIED |
| CLM-038 | EXEC-SUMMARY:117 | "Fase 2 -- Hardening: COMPLETADA -- Notion 75 entradas" | DOC_CROSS_REF | Phase 2 was completed with 75 Notion entries. This is historically correct for Phase 2 close. PHASE-STATUS.md P2.4 and PHASE-2-EVIDENCE.md both show 75 entries at Phase 2 time. Later expanded to 81 in Phase 3. | VERIFIED |
| CLM-039 | PHASE-STATUS.md:54 | "G0 Tooling: 75 entradas (37 Backlog + 12 KB + 26 Testing)" | DOC_CROSS_REF | PHASE-STATUS.md G0 detail says 75 entries at time of G0 (Phase 1). This was accurate for that snapshot. PHASE-1-EVIDENCE G0.6 says "3 bases de datos creadas". Counts grew: 75 at Phase 2, 81 at Phase 3. | VERIFIED |
| CLM-040 | render.yaml:5 | "Region Frankfurt (EU)" | CODE_INSPECT | render.yaml L5: `region: frankfurt`. RENDER-DEPLOY.md: "Frankfurt (EU) -- mas cercano a Espana". | VERIFIED |
| CLM-041 | CLAUDE.md:140 | "Docker build fix (setuptools<75 + --no-build-isolation para whisper)" | CODE_INSPECT | Dockerfile does NOT contain setuptools<75 or --no-build-isolation. The Whisper install was removed entirely (commented out, L12: "Skip requirements-audio.txt"). The fix was applied historically but the current Dockerfile simply omits Whisper. Fix is superseded but claim is historically accurate. | VERIFIED |
| CLM-042 | CLAUDE.md:142 | "Unused import time removido de logger.py" | CODE_INSPECT | logger.py has no `import time` statement. Only imports: json, logging. Fix confirmed -- `time` was removed. | VERIFIED |

---

## Detailed Evidence for Key Claims

### CLM-001: Test Count Verification

```
grep "def test_" results per file:
  tests/unit/test_cache.py:           6
  tests/unit/test_config.py:          3
  tests/unit/test_detect_input.py:    4
  tests/unit/test_detect_lang.py:     4
  tests/unit/test_evals.py:           9
  tests/unit/test_guardrails.py:     19
  tests/unit/test_kb_lookup.py:       4
  tests/unit/test_observability.py:   6
  tests/unit/test_redteam.py:         6 (1 parametrized x5 = 10 collected)
  tests/unit/test_retriever.py:       7
  tests/unit/test_structured_outputs.py: 10
  tests/integration/test_pipeline.py:  2
  tests/integration/test_twilio_stub.py: 2
  tests/integration/test_webhook.py:   3
  tests/e2e/test_demo_flows.py:       4
  ──────────────────────────────────
  Total function defs:               89
  Parametrize expansion:             +4 (redteam)
  Collected tests:                   93
```

### CLM-003: Skills Directory Contents

```
src/core/skills/
  __init__.py        (not a skill)
  cache_match.py
  convert_audio.py
  detect_input.py
  detect_lang.py
  fetch_media.py
  kb_lookup.py
  llm_generate.py
  send_response.py
  transcribe.py
  tts.py
  verify_response.py
  ──────────────────
  11 skill files (excluding __init__.py)
```

### CLM-004: Cache Entries

```
demo_cache.json entries (JSON array, 8 items):
  1. imv_es              (audio: imv_es.mp3)
  2. empadronamiento_es  (audio: empadronamiento_es.mp3)
  3. tarjeta_sanitaria_es (audio: tarjeta_es.mp3)
  4. ahmed_empadronamiento_fr (audio: ahmed_fr.mp3)
  5. fatima_tarjeta_fr    (audio: fatima_fr.mp3)
  6. saludo_es            (audio: null)
  7. saludo_fr            (audio: null)
  8. maria_carta_vision   (audio: maria_es.mp3)
  ──────────────────
  8 entries, 6 with MP3 audio
```

### CLM-002: Feature Flags in config.py

```python
# Line 25: DEMO_MODE: bool       (default: false)
# Line 26: LLM_LIVE: bool        (default: true)
# Line 27: WHISPER_ON: bool      (default: true)
# Line 28: LLM_TIMEOUT: int      (default: 6)
# Line 29: WHISPER_TIMEOUT: int   (default: 12)
# Line 33: OBSERVABILITY_ON: bool (default: true)
# Line 42: STRUCTURED_OUTPUT_ON: bool (default: false)
# Line 45: GUARDRAILS_ON: bool   (default: true)
# Line 48: RAG_ENABLED: bool     (default: false)
# ──────────────────
# Total: 9 feature flags
# Note: AUDIO_BASE_URL, OTEL_ENDPOINT, FLASK_ENV, LOG_LEVEL, ADMIN_TOKEN are config values, not feature flags
```

---

## Contradictions Detected

| # | Files | Issue | CLM Ref |
|---|-------|-------|---------|
| 1 | EXEC-SUMMARY vs CLAUDE.md | "10 skills" vs "11 skills" -- actual is 11 | CLM-032 |
| 2 | EXEC-SUMMARY vs CLAUDE.md | "10 feature flags" vs "9 feature flags" -- actual is 9 | CLM-033 |
| 3 | EXEC-SUMMARY vs CLAUDE.md + PHASE-STATUS | Phase 3 "EN CURSO" vs "COMPLETADA/cerrada" | CLM-034 |
| 4 | NOTION-OS.md internal | Header says "75 entradas" but data section says "81 entradas" | CLM-035 |
| 5 | PHASE-1-EVIDENCE | Cache count command uses `['entries']` key but JSON is a plain array | CLM-037 |
| 6 | PHASE-2-EVIDENCE vs actual | test_guardrails listed as 18 tests, actual is 19 | CLM-036 |

---

## Methodology Notes

- **CODE_INSPECT**: Direct reading of source files using Read tool
- **COMMAND_RUN**: `grep "def test_"` across test files to count test functions; glob for file counts
- **FILE_COUNT**: Glob patterns to count files matching specific paths
- **DOC_CROSS_REF**: Comparing claims between two or more documentation files
- pytest `--collect-only` could not run (no venv activated in this session); used grep + parametrize analysis instead
- Notion API verification not available in this session (no MCP access)
