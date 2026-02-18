# Fase 2 — Implementation Log

## Tickets Implemented

### MEM-01: Memory Config Flags
- **Files:** `src/core/config.py`, `tests/unit/test_config.py`
- **Changes:** Added 6 flags: MEMORY_ENABLED, MEMORY_BACKEND, MEMORY_TTL_DAYS, MEMORY_SECRET_SALT, MEMORY_OPTIN_DEFAULT, FORGET_TOKEN
- **Tests:** +1 test

### MEM-02: MemoryState Schema + User Hash
- **Files:** `src/core/memory/__init__.py`, `src/core/memory/models.py`, `src/core/memory/user_hash.py`, `tests/unit/test_memory_models.py`
- **Changes:** MemoryState v1 dataclass with to_dict/from_dict, new_memory_state factory, derive_user_id SHA256 hash
- **Tests:** +7 tests

### MEM-03: MemoryStore Abstraction + Dev Backend
- **Files:** `src/core/memory/store.py`, `src/core/memory/backends/__init__.py`, `src/core/memory/backends/dev.py`, `tests/unit/test_memory_store.py`
- **Changes:** MemoryStore ABC (get/upsert/forget/health), InMemoryStore with TTL check, get_store factory
- **Tests:** +7 tests

### MEM-04: Redis Backend
- **Files:** `src/core/memory/backends/redis_store.py`, `requirements.txt`, `tests/unit/test_memory_redis.py`
- **Changes:** RedisStore with key prefix, setex TTL, ping health. Added redis>=5.0,<6.0 dependency
- **Tests:** +6 tests (all mocked, no real Redis needed)

### MEM-05: Tag Sanitization
- **Files:** `src/core/memory/sanitize.py`, `tests/unit/test_memory_sanitize.py`
- **Changes:** escape_xml_tags (prevent tag injection), sanitize_for_prompt (escape + PII redaction)
- **Tests:** +6 tests

### MEM-06: Memory-Aware System Prompt
- **Files:** `src/core/prompts/system_prompt.py`, `tests/unit/test_memory_prompt.py`
- **Changes:** Added Rule 11 (anti-injection for memory blocks), Rule 12 (personalization), memory_blocks placeholder, build_prompt accepts memory params
- **Tests:** +3 tests

### MEM-07: Opt-In/Forget Command Detection + Templates
- **Files:** `src/core/memory/commands.py`, `src/core/prompts/templates.py`, `tests/unit/test_memory_commands.py`
- **Changes:** MemoryCommand enum, detect_memory_command with accent normalization, 4 memory templates (optin_ask, confirmed, declined, forgotten) in es/fr/en
- **Tests:** +8 tests

### MEM-08: Pipeline Integration
- **Files:** `src/core/pipeline.py`, `src/core/skills/llm_generate.py`, `src/core/memory/update.py`, `tests/unit/test_memory_update.py`
- **Changes:** Full memory flow in pipeline (load → check commands → consent → inject → update), llm_generate accepts memory params, post-response update with PII redaction
- **Tests:** +5 tests

### MEM-09: /forget Admin Endpoint
- **Files:** `src/routes/forget.py`, `src/app.py`, `tests/unit/test_forget_endpoint.py`
- **Changes:** POST /forget with Bearer token auth, registers blueprint in app.py
- **Tests:** +3 tests

### MEM-10: Memory Observability
- **Files:** `src/utils/logger.py`
- **Changes:** log_memory() function with structured fields

### MEM-11: Health Endpoint Memory Status
- **Files:** `src/routes/health.py`
- **Changes:** Memory backend status in /health response

### MEM-12: Multi-Turn Eval Cases
- **Files:** `data/evals/multiturn_evals.json`, `tests/unit/test_memory_evals.py`
- **Changes:** 25 eval cases, 22 programmatic test validations
- **Tests:** +22 tests

### MEM-13: User Isolation Test
- **Files:** `tests/integration/test_memory_isolation.py`
- **Changes:** 3 integration tests proving user isolation
- **Tests:** +3 tests

### MEM-14: Config Deploy
- **Files:** `render.yaml`, `tests/conftest.py`
- **Changes:** 7 new env vars in render.yaml, test-safe defaults in conftest

## Summary
- **New files created:** 18
- **Files modified:** 12
- **New tests:** +72 (110 → 182)
- **All gates pass:** pytest PASS, ruff PASS
