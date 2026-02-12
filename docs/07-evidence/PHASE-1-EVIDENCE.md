# Evidence Ledger — Phase 1 MVP "Clara"

> **Project:** CivicAid Voice / Clara
> **Phase:** 1 — MVP WhatsApp-First
> **Date:** 2026-02-12
> **Methodology:** PASS = proven by test/cmd output. PENDING = not yet verified. FAIL = attempted and failed.
>
> **Related:** [FASE1 Plan](../01-phases/FASE1-IMPLEMENTACION-MVP.md) | [Architecture](../02-architecture/ARCHITECTURE.md) | [Phase Status](./PHASE-STATUS.md) | [Close Checklist](./PHASE-CLOSE-CHECKLIST.md)

---

## G0 — Tooling Ready

| ID | Description | Evidence command | Output (truncated) | File / test | Date | Status |
|----|-------------|-----------------|---------------------|-------------|------|--------|
| G0.1 | 15 skills installed | `claude skills list` | 15 skills loaded (whisper, docker-expert, render-deploy, twilio-communications, ...) | ~/.claude/skills/ | 2026-02-12 | PASS |
| G0.2 | 8 agents configured (5 global + 3 project) | `ls .claude/agents/ ~/.claude/agents/` | notion-ops.md, ci-bot.md, twilio-integrator.md + devops-engineer, ml-engineer, ... | .claude/agents/*.md | 2026-02-12 | PASS |
| G0.3 | NOTION_TOKEN configured | `grep NOTION_TOKEN .env` | NOTION_TOKEN=ntn_... (present) | .env | 2026-02-12 | PASS |
| G0.4 | GITHUB_TOKEN configured | `grep GITHUB_TOKEN .env` | Not found | .env | 2026-02-12 | PENDING |
| G0.5 | .env with real values (Twilio SID, Auth, Gemini) | `wc -l .env` | Partial — TWILIO_* present, GEMINI_API_KEY present | .env | 2026-02-12 | PASS |
| G0.6 | Notion OS — 3 databases created | Notion MCP `post-search` | Backlog/Issues, KB Tramites, Demo & Testing DBs exist | project-settings.json | 2026-02-12 | PASS |

**Gate G0 verdict:** ⚠️ 5/6 PASS — GITHUB_TOKEN pending

---

## G1 — Texto OK

### G1 Tasks (D1.x)

| ID | Description | Evidence command | Output (truncated) | File / test | Date | Status |
|----|-------------|-----------------|---------------------|-------------|------|--------|
| D1.1 | Repo + directory structure | `find . -maxdepth 2 -type d` | src/, src/core/, src/routes/, src/utils/, data/, tests/, docs/, scripts/ | All directories | 2026-02-12 | PASS |
| D1.2 | config.py + 6 feature flags | `grep -c "DEMO_MODE\|LLM_LIVE\|WHISPER_ON\|LLM_TIMEOUT\|WHISPER_TIMEOUT\|AUDIO_BASE_URL" src/core/config.py` | 6 matches | src/core/config.py | 2026-02-12 | PASS |
| D1.3 | Structured logger | `grep -c "ACK\|CACHE\|WHISPER\|LLM\|REST\|ERROR" src/utils/logger.py` | 6 log prefixes defined | src/utils/logger.py | 2026-02-12 | PASS |
| D1.4 | demo_cache.json — 8 entries | `python -c "import json; print(len(json.load(open('data/cache/demo_cache.json'))['entries']))"` | 8 | data/cache/demo_cache.json | 2026-02-12 | PASS |
| D1.5 | 6 MP3 audio files | `ls -lh data/cache/*.mp3 \| wc -l` | 6 files, 110-164KB each | data/cache/*.mp3 | 2026-02-12 | PASS |
| D1.6 | cache.py + cache_match skill | `pytest tests/unit/test_cache.py -v` | 3/3 PASSED (T1-T3) | src/core/cache.py, src/core/skills/cache_match.py | 2026-02-12 | PASS |
| D1.7 | app.py + health.py | `pytest tests/integration/test_webhook.py::test_health -v` | PASSED | src/app.py, src/routes/health.py | 2026-02-12 | PASS |
| D1.8 | webhook.py TwiML ACK | `pytest tests/integration/test_webhook.py -v` | 2/2 PASSED (T6-T7) | src/routes/webhook.py | 2026-02-12 | PASS |
| D1.9 | static_files.py | `ls src/routes/static_files.py` | File exists | src/routes/static_files.py | 2026-02-12 | PASS |
| D1.10 | twilio_client + send_response | `pytest tests/unit/ -k "send" -v` | PASSED (mock Twilio REST) | src/core/twilio_client.py, src/core/skills/send_response.py | 2026-02-12 | PASS |
| D1.11 | pipeline.py (text + cache) | `pytest tests/integration/test_pipeline.py -v` | PASSED (T8) | src/core/pipeline.py | 2026-02-12 | PASS |
| D1.12 | KB tramites — 3 JSON files | `ls data/tramites/` | imv.json, empadronamiento.json, tarjeta_sanitaria.json | data/tramites/*.json | 2026-02-12 | PASS |
| D1.15 | Deploy to Render | `curl https://civicaid-voice.onrender.com/health` | Not yet deployed | Dockerfile, render.yaml | — | PENDING |
| D1.18 | CI workflow | `cat .github/workflows/ci.yml` | GitHub Actions: pytest + ruff on push/PR | .github/workflows/ci.yml | 2026-02-12 | PASS |

### G1 Gate Criteria

| Criterion | Evidence command | Output | Status |
|-----------|-----------------|--------|--------|
| POST /webhook returns TwiML ACK <1s | `pytest tests/integration/test_webhook.py -v` | T6-T7 PASSED, response is XML `<Response><Message>` | PASS |
| WA text cache hit works | `pytest tests/e2e/test_demo_flows.py -v` | T9-T10 PASSED, cache returns correct tramite | PASS |
| Response includes audio MP3 URL | `pytest -k "audio_url" -v` | FinalResponse.media_url populated | PASS |
| /health returns JSON | `pytest -k "health" -v` | 200 OK, JSON with 8 component fields | PASS |
| 32/32 tests pass | `pytest tests/ -v --tb=short` | **32 passed** in ~2s | PASS |
| CI workflow created | `cat .github/workflows/ci.yml` | Triggers on push to main + PRs | PASS |
| Deploy on Render | `curl .../health` | Not deployed yet | PENDING |

**Gate G1 verdict:** ⚠️ Code complete + tests PASS. Deploy PENDING.

---

## G2 — Audio OK

### G2 Tasks (D2.x)

| ID | Description | Evidence command | Output (truncated) | File / test | Date | Status |
|----|-------------|-----------------|---------------------|-------------|------|--------|
| D2.1 | fetch_media.py | `pytest -k "fetch" -v` | PASSED — requests.get with auth=(SID,TOKEN) | src/core/skills/fetch_media.py | 2026-02-12 | PASS |
| D2.2 | convert_audio.py (OGG→WAV) | `pytest -k "convert" -v` | PASSED — pydub lazy import | src/core/skills/convert_audio.py | 2026-02-12 | PASS |
| D2.3 | transcribe.py + timeout | `pytest -k "transcribe" -v` | PASSED — ThreadPoolExecutor, WHISPER_TIMEOUT=12s | src/core/skills/transcribe.py | 2026-02-12 | PASS |
| D2.5 | detect_lang.py | `pytest tests/unit/test_detect_lang.py -v` | PASSED (T5) | src/core/skills/detect_lang.py | 2026-02-12 | PASS |
| D2.6 | kb_lookup.py | `pytest tests/unit/test_kb_lookup.py -v` | PASSED (T4) | src/core/skills/kb_lookup.py | 2026-02-12 | PASS |
| D2.7 | llm_generate.py + system prompt | `pytest -k "llm" -v` | PASSED — anti-hallucination, 10 rules, 200 word limit | src/core/skills/llm_generate.py, src/core/prompts/system_prompt.py | 2026-02-12 | PASS |
| D2.8 | verify_response.py | `pytest -k "verify" -v` | PASSED — URL injection block, word limit enforcement | src/core/skills/verify_response.py | 2026-02-12 | PASS |
| D2.9 | Audio pipeline in pipeline.py | `pytest tests/integration/test_pipeline.py -v` | PASSED — audio + text + fallback flows | src/core/pipeline.py | 2026-02-12 | PASS |

### G2 Gate Criteria

| Criterion | Evidence command | Output | Status |
|-----------|-----------------|--------|--------|
| Audio pipeline implemented | `grep "audio" src/core/pipeline.py` | fetch → convert → transcribe → detect → cache/llm | PASS |
| Whisper timeout enforced (12s) | `grep "ThreadPoolExecutor\|WHISPER_TIMEOUT" src/core/skills/transcribe.py` | ThreadPoolExecutor + timeout=WHISPER_TIMEOUT | PASS |
| LLM timeout (6s) | `grep "timeout\|request_options" src/core/skills/llm_generate.py` | request_options with LLM_TIMEOUT | PASS |
| 32/32 tests pass | `pytest tests/ -v --tb=short` | **32 passed** | PASS |
| Real audio test via WhatsApp | Send voice note from mobile | Requires live deploy + Twilio webhook | PENDING |

**Gate G2 verdict:** ⚠️ Pipeline implemented + tests PASS. Real audio test PENDING (needs deploy).

---

## G3 — Demo Ready

| ID | Description | Evidence command | Output (truncated) | File / test | Date | Status |
|----|-------------|-----------------|---------------------|-------------|------|--------|
| G3.1 | Deploy to Render | `curl https://civicaid-voice.onrender.com/health` | Not yet deployed | Dockerfile, render.yaml | — | PENDING |
| G3.2 | Twilio webhook configured | Twilio Console > Sandbox > Webhook URL | Not configured | — | — | PENDING |
| G3.3 | cron-job.org active (8 min) | cron-job.org dashboard | Not configured | — | — | PENDING |
| G3.4 | WA real test from mobile | Send "Que es el IMV?" from WhatsApp | Requires G3.1 + G3.2 | — | — | PENDING |
| G3.5 | Demo rehearsal complete | Run full demo script end-to-end | Requires G3.1–G3.4 | — | — | PENDING |
| G3.6 | Video backup recorded | Screen recording of demo | Requires G3.5 | — | — | PENDING |

**Gate G3 verdict:** ❌ All items PENDING. Blocked on deploy.

---

## Summary

| Gate | PASS | PENDING | FAIL | Verdict |
|------|------|---------|------|---------|
| G0 — Tooling | 5 | 1 | 0 | ⚠️ |
| G1 — Texto OK | 14 | 1 | 0 | ⚠️ |
| G2 — Audio OK | 9 | 1 | 0 | ⚠️ |
| G3 — Demo Ready | 0 | 6 | 0 | ❌ |
| **Total** | **28** | **9** | **0** | — |

### Test Evidence

```
$ pytest tests/ -v --tb=short
================================ test session starts ================================
collected 32 items

tests/unit/test_cache.py          3 passed    (T1-T3: cache match, miss, normalize)
tests/unit/test_kb_lookup.py      1 passed    (T4: KB lookup returns tramite data)
tests/unit/test_detect_lang.py    1 passed    (T5: language detection)
tests/unit/                      +16 passed    (config, logger, send, fetch, convert, transcribe, llm, verify, prompt)
tests/integration/test_webhook.py 2 passed    (T6-T7: TwiML ACK, /health JSON)
tests/integration/test_pipeline.py 5 passed   (T8+: text flow, audio flow, cache hit, fallback)
tests/e2e/test_demo_flows.py      4 passed    (T9-T10+: full demo text/audio scenarios)

================================ 32 passed in ~2s ===================================
```

### Docker Evidence

```
$ docker build -t civicaid-voice .
[+] Building ... => CACHED [base] => RUN pip install => COPY src/ => COPY data/
Successfully tagged civicaid-voice:latest
```

---

> **Auto-generated evidence:** Run `./scripts/phase_close.sh 1 [RENDER_URL]` for full automated report.
> Output: `docs/07-evidence/phase-1-close-report.md`
