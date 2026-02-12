# Toolkit Integration Evidence — CivicAid Voice / Clara

## Phase 0 — Baseline Audit (2026-02-12)

### Test Suite
- 32/32 tests pass (pytest tests/ -q in 0.79s)
- Unit: 21, Integration: 7, E2E: 4
- Lint: ruff clean (0 errors)

### Codebase Snapshot
- 10 skills in src/core/skills/
- 8 dataclass models in src/core/models.py
- 6 feature flags in src/core/config.py: DEMO_MODE, LLM_LIVE, WHISPER_ON, LLM_TIMEOUT, WHISPER_TIMEOUT, AUDIO_BASE_URL
- Pipeline pattern: detect_input -> [audio] -> detect_lang -> cache_match -> [miss] -> kb_lookup -> llm_generate -> verify_response -> send_response
- Logger: tagged prefixes [ACK] [CACHE] [WHISPER] [LLM] [REST] [ERROR]
- Timing: decorator exists in timing.py, used on llm_generate only

### Docker
- Build: PASS (3.7GB image with Whisper)
- Dockerfile: python:3.11-slim + ffmpeg + setuptools<75 fix
- render.yaml: web service, frankfurt, free plan, /health check

### Dependencies
- requirements.txt: flask, gunicorn, twilio, pydub, google-generativeai, langdetect, requests, python-dotenv, gTTS
- requirements-audio.txt: openai-whisper==20231117

### Git State
- Branch: main, 2 commits ahead of origin
- Latest: a13fd88 (chore: Notion populated)

### What's Missing (to be added by toolkit integration)
- No request_id per request
- No structured output parsing
- No guardrails/safety layer
- No eval framework
- No RAG interface
- No abuse/red-team tests
- Timing decorator only on 1 skill (llm_generate)
- No OpenTelemetry/tracing export

---

## Phase 2 — Observability (2026-02-12)

- Added `src/utils/observability.py` with `RequestContext` (request_id, stage timings)
- Middleware injects request_id into every request
- All pipeline skills instrumented with stage timing via decorators
- OTEL stub: structured export-ready spans (flag `OBSERVABILITY_ON`, default true)
- Verify: `bash scripts/verify_obs.sh`

## Phase 3 — Structured Outputs (2026-02-12)

- Added `src/core/models_structured.py` with Pydantic models (`ClaraStructuredResponse`)
- Parse/validate LLM output into structured schema
- Feature flag `STRUCTURED_OUTPUT_ON` (default false) — when off, pipeline behaves identically to Phase 1
- Verify: `bash scripts/verify_structured.sh`

## Phase 4 — Guardrails (2026-02-12)

- Added `src/core/guardrails.py` with `pre_check()` and `post_check()` functions
- Pre-check: blocklist filter, prompt injection detection
- Post-check: disclaimer injection, PII redaction
- Feature flag `GUARDRAILS_ON` (default true)
- Verify: `bash scripts/verify_guardrails.sh`

## Phase 5 — Evals (2026-02-12)

- Added `src/utils/eval_runner.py` with `load_eval_cases()` and eval harness
- Added `data/evals/` with 16 eval cases across cache-hit, LLM, and safety categories
- Added `scripts/run_evals.py` runner script
- Baseline: 56% pass rate (cache-only mode, expected — LLM cases fail without live API)
- Verify: `bash scripts/verify_evals.sh`

## Phase 6 — RAG Stub (2026-02-12)

- Added `src/core/retriever.py` with `Retriever` interface and `JSONKBRetriever` implementation
- `get_retriever()` factory returns JSON KB retriever (vector store swappable later)
- Feature flag `RAG_ENABLED` (default false)
- Verify: `python3 -c "from src.core.retriever import get_retriever; print('OK')"`

## Phase 7 — Red Team / Abuse Tests (2026-02-12)

- Added 10 abuse/adversarial prompt test cases
- Tests cover: prompt injection, jailbreak attempts, PII extraction, off-topic deflection, language confusion
- 5 tests xpassed (guardrails caught more than expected)
- Verify: `pytest tests/ -k "red_team or abuse" -v`

---

## Final State (2026-02-12)

### Test Suite
- 86/86 tests pass (pytest tests/ -q)
- Lint: ruff clean (0 errors)
- All new modules import successfully

### New Modules
| Module | Purpose |
|--------|---------|
| src/utils/observability.py | Request context, stage timings, OTEL stub |
| src/core/models_structured.py | Pydantic structured output models |
| src/core/guardrails.py | Pre/post safety checks |
| src/utils/eval_runner.py | Eval case loader and runner |
| src/core/retriever.py | RAG retriever interface + JSON KB impl |

### New Feature Flags
| Flag | Default | Purpose |
|------|---------|---------|
| OBSERVABILITY_ON | true | Enable request tracing and stage timings |
| STRUCTURED_OUTPUT_ON | false | Enable Pydantic output parsing |
| GUARDRAILS_ON | true | Enable pre/post safety checks |
| RAG_ENABLED | false | Enable RAG retriever in pipeline |

### Verification
```bash
bash scripts/verify_toolkit.sh   # Full toolkit check
bash scripts/verify_evals.sh     # Eval-specific check
```
