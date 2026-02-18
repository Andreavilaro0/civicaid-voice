# Fase 2 — Gates Evidence

## Gate 1: pytest
- **Before (baseline):** 110 passed, 1 skipped, 1 deselected (0.73s)
- **After (Fase 2):** 182 passed, 1 skipped (0.94s)
- **Delta:** +72 new tests (all memory-related)
- **Command:** `PYTHONPATH=. pytest tests/ -v --tb=short`
- **Evidence:** `commands-output/pytest-full.txt`
- **Status:** PASS

## Gate 2: ruff
- **Before:** All checks passed
- **After:** All checks passed
- **Command:** `ruff check src/ tests/ --select E,F,W --ignore E501`
- **Evidence:** `commands-output/ruff-check.txt`
- **Status:** PASS

## Gate 3: Multi-turn Evals
- **Eval file:** `data/evals/multiturn_evals.json` (25 cases)
- **Test file:** `tests/unit/test_memory_evals.py` (22 programmatic validations)
- **Coverage:** Follow-ups, forget, opt-in, language switch, tramite switch, PII redaction, isolation, TTL, injection, sanitization
- **Status:** PASS (all 22 eval tests pass)

## Gate 4: User Isolation
- **Test file:** `tests/integration/test_memory_isolation.py` (3 tests)
- **Tests:** Two-user isolation, parallel upserts (10 users), hash uniqueness
- **Status:** PASS

## Gate 5: verify_toolkit / verify_obs / verify_guardrails / verify_structured
- **Status:** Scripts not present in repo — checklist equivalent below
- **verify_toolkit:** Memory store API (get/upsert/forget/health) tested in test_memory_store.py — PASS
- **verify_obs:** Memory logging (log_memory) added to logger.py, called in pipeline — PASS
- **verify_guardrails:** Sanitization (escape_xml_tags, sanitize_for_prompt) + PII redaction tested — PASS
- **verify_structured:** MemoryState.to_dict/from_dict round-trip tested in test_memory_models.py — PASS

## Abort Condition Checklist

| ID | Condition | Status | Evidence |
|----|-----------|--------|----------|
| A1 | No persistent prod backend | CLEAR | RedisStore in `src/core/memory/backends/redis_store.py`, selectable via `MEMORY_BACKEND=redis` |
| A2 | User state cross-contamination | CLEAR | `test_memory_isolation.py` (3 tests), `test_mt08_user_isolation` |
| A3 | No opt-in/consent + forget | CLEAR | Pipeline opt-in flow, `detect_memory_command()`, `/forget` endpoint |
| A4 | Gates don't pass | CLEAR | 182 passed, ruff clean |
| A5 | Memory injection without sanitization | CLEAR | `escape_xml_tags()` + `sanitize_for_prompt()` + Rule 11 in system prompt |
| A6 | Filesystem-only backend | CLEAR | InMemoryStore is dev-only fallback; Redis is prod backend |
