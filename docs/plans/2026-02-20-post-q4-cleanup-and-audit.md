# Post-Q4 Cleanup, Commit & Full Project Audit — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Commit all Q4 work properly, clean up the repo (dead files, duplicate plans, stale docs), run the full audit, and leave the project hackathon-ready.

**Architecture:** Three sequential phases — (1) Git hygiene: stage and commit 91 uncommitted files in logical groups, (2) Full Project Audit: run the automated audit from FULL-PROJECT-AUDIT-PROMPT.md to find dead code, broken links, doc inconsistencies, (3) Hackathon Polish: update CLAUDE.md, JUDGES-QUICK-EVAL.md, and verify the demo path works end-to-end.

**Tech Stack:** Python 3.11, Flask, pytest, ruff, git, bash

---

## Pre-Conditions

| Condition | Value |
|-----------|-------|
| Branch | `fix/fase3-full-pass` |
| Tests | 517 collected, 493+ passing |
| Lint | Clean |
| Q4 Gates | 26/26 PASS |
| Uncommitted files | 91 |
| Plan files | 21 (many superseded) |

---

## PHASE 1 — Git Hygiene (Commit Q4 Work)

The 91 uncommitted files need to be grouped into logical commits. Never use `git add -A`. Stage specific files by topic.

### Task 1: Commit core pipeline fixes (SHOWSTOPPER)

**Files:**
- Stage: `src/core/pipeline.py`, `src/core/retriever.py`
- Stage: `tests/unit/test_retriever.py`

**Step 1: Verify the files are modified**

Run: `git diff --stat src/core/pipeline.py src/core/retriever.py tests/unit/test_retriever.py`
Expected: 3 files with changes shown

**Step 2: Stage and commit**

```bash
git add src/core/pipeline.py src/core/retriever.py tests/unit/test_retriever.py
git commit -m "fix: integrate get_retriever() singleton into pipeline (SHOWSTOPPER)

- pipeline.py now calls get_retriever().retrieve() instead of kb_lookup()
- Added singleton pattern with reset_retriever() for test isolation
- All Q2-Q4 RAG infrastructure is now actually used in production

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Step 3: Verify commit**

Run: `git log --oneline -1`
Expected: Shows the new commit message

---

### Task 2: Commit config and models changes

**Files:**
- Stage: `src/core/config.py`, `src/core/models.py`

**Step 1: Stage and commit**

```bash
git add src/core/config.py src/core/models.py
git commit -m "feat: add Q4 config flags (RAG cache, ingestion, drift, memory)

- RAG_FALLBACK_CHAIN, RAG_CACHE_ENABLED, RAG_INGESTION_ENABLED
- RAG_DRIFT_CHECK_ENABLED, RAG_BOE_MONITOR_ENABLED, RAG_METRICS_ENABLED
- MEMORY_ENABLED, MEMORY_BACKEND, MEMORY_TTL_DAYS, MEMORY_OPTIN_DEFAULT

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: Commit RAG infrastructure (new modules)

**Files:**
- Stage: `src/core/rag/` (entire directory — new files)

**Step 1: List what's in src/core/rag/**

Run: `ls -la src/core/rag/`
Expected: Multiple .py files (store.py, chunker.py, embedder.py, models.py, database.py, etc.)

**Step 2: Stage and commit**

```bash
git add src/core/rag/
git commit -m "feat: add RAG infrastructure — pgvector store, chunker, embedder, cache

- PGVectorStore with hybrid BM25+vector search
- Chunker with heading-aware splitting
- Gemini embedder with 768-dim vectors
- ResponseCache (Redis primary + LRU memory fallback)
- FallbackRetriever chain: PGVector → JSON → Directory
- Reranker (heuristic + Gemini), grounded prompting
- Territory detection, synonym expansion
- Database models and migrations

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: Commit admin routes and utilities

**Files:**
- Stage: `src/routes/admin.py`, `src/utils/rag_eval.py`, `src/utils/rag_metrics.py`

**Step 1: Stage and commit**

```bash
git add src/routes/admin.py src/utils/rag_eval.py src/utils/rag_metrics.py
git commit -m "feat: add admin API routes and RAG evaluation utilities

- Admin routes for procedure management, cache control, metrics
- RAG evaluation runner with P@K, BM25 metrics
- RAG observability metrics collection

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: Commit other modified source files

**Files:**
- Stage: `src/core/prompts/system_prompt.py`, `src/core/skills/llm_generate.py`, `src/core/skills/transcribe.py`
- Stage: `src/utils/logger.py`, `src/utils/observability.py`

**Step 1: Stage and commit**

```bash
git add src/core/prompts/system_prompt.py src/core/skills/llm_generate.py src/core/skills/transcribe.py src/utils/logger.py src/utils/observability.py
git commit -m "refactor: update prompts, LLM generate, transcribe, and observability for Q4

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: Commit all new unit tests

**Files:**
- Stage: all `tests/unit/test_*.py` untracked files

**Step 1: List new unit test files**

Run: `git status --short tests/unit/ | grep "^??"`
Expected: ~20 new test files

**Step 2: Stage and commit**

```bash
git add tests/unit/
git commit -m "test: add Q2-Q4 unit tests — RAG store, chunker, embedder, reranker, cache, admin

- 20+ new test files covering all RAG modules
- Territory detection, synonym expansion, BM25, validators
- Drift detection, BOE monitor, ingestion pipeline
- Total: 517 tests collected

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7: Commit all new integration and eval tests

**Files:**
- Stage: `tests/integration/` (new files), `tests/evals/`

**Step 1: Stage and commit**

```bash
git add tests/integration/ tests/evals/
git commit -m "test: add integration and eval tests — RAG pipeline, fallback chain, admin, drift

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 8: Commit scripts

**Files:**
- Stage: all new `scripts/*.py` files

**Step 1: List new scripts**

Run: `git status --short scripts/`
Expected: ~8 new scripts

**Step 2: Stage and commit**

```bash
git add scripts/
git commit -m "feat: add Q4 operational scripts — ingestion, drift check, BOE monitor, DB init

- run_ingestion.py, check_drift.py, check_boe.py, init_db.py
- run_rag_eval.py, validate_policy.py, validate_proceduredoc_schema.py
- validate_source_registry.py, link_check.py

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 9: Commit data files (evals, policy, sources)

**Files:**
- Stage: `data/evals/eval_report_q3_gates.json`, `data/evals/rag_eval_set.json`
- Stage: `data/policy/`, `data/sources/`
- Stage: `schemas/`
- Stage: `docker-compose.yml`

**Step 1: Check for sensitive data**

Run: `grep -r "password\|secret\|token\|api_key" data/policy/ data/sources/ schemas/ --include="*.json" --include="*.yaml" -l 2>/dev/null || echo "No secrets found"`
Expected: No secrets found (or review any matches)

**Step 2: Stage and commit**

```bash
git add data/evals/eval_report_q3_gates.json data/evals/rag_eval_set.json data/policy/ data/sources/ schemas/ docker-compose.yml
git commit -m "feat: add eval datasets, policy configs, source registry, and docker-compose

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 10: Commit documentation and plans

**Files:**
- Stage: `docs/` (all new and modified)
- Stage: `design/`
- Stage: `CLAUDE.md`, `README.md`

**Step 1: Stage and commit docs**

```bash
git add docs/ design/ CLAUDE.md README.md
git commit -m "docs: add Q1-Q4 documentation, plans, closing reports, and design docs

- Q4-CLOSING-REPORT.md, Q4-DESIGN.md (7 ADRs)
- Phase documentation for Q1-Q4 (sources, storage, retrieval, production)
- Updated CLAUDE.md with current project state
- 21 plan files (prompts, audits, implementation plans)
- Design directory with architecture diagrams

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 11: Commit remaining loose files and verify clean state

**Files:**
- Stage: any remaining untracked files (eval reports at root level, etc.)

**Step 1: Check what's left**

Run: `git status --short`
Expected: Remaining loose files like `eval_report_q4*.json` at root

**Step 2: Stage eval reports**

```bash
git add eval_report_q3_gates.json eval_report_q4.json eval_report_q4_fix1.json eval_report_q4_fix2.json eval_report_q4_fix3.json
git commit -m "data: add Q3/Q4 evaluation report snapshots

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Step 3: Verify clean working tree**

Run: `git status`
Expected: `nothing to commit, working tree clean`

**Step 4: Verify all tests still pass**

Run: `python -m pytest tests/ -x -q --tb=short 2>&1 | tail -5`
Expected: `493+ passed` (or 517 collected with some xpass/skip)

---

## PHASE 2 — Full Project Audit

Run the audit defined in `FULL-PROJECT-AUDIT-PROMPT.md` to clean up the repo.

### Task 12: Run T1-T5 — File system audit (discovery)

**Files:**
- Read: `docs/plans/FULL-PROJECT-AUDIT-PROMPT.md` (for exact commands)

**Step 1: Run the discovery commands from the audit prompt**

Execute the bash commands from T1 through T5 of `FULL-PROJECT-AUDIT-PROMPT.md`:
- T1: Empty files check
- T2: Duplicate file names
- T3: Large files (>100KB)
- T4: Collect test count
- T5: Find TODO/FIXME/HACK comments

**Step 2: Record results**

Save output to `docs/plans/evidence/audit-results-2026-02-20.md`

---

### Task 13: Run T6-T8 — Code quality audit

**Step 1: Execute code quality checks**

- T6: Unused imports (ruff)
- T7: Architecture consistency (imports follow layering)
- T8: Dead code detection (unused functions)
  - Include T8 3b: verify pipeline.py uses get_retriever() (CRITICAL)

**Step 2: Fix any issues found**

For each issue:
1. Note the file and line
2. Apply fix via Edit tool
3. Run `ruff check src/ --select E,F,W --ignore E501` to verify

**Step 3: Commit fixes if any**

```bash
git add -p  # stage only changed files
git commit -m "fix: address audit findings — unused imports, dead code cleanup

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 14: Run T9-T12 — Documentation audit

**Step 1: Execute documentation checks**

- T9: Check all paths in CLAUDE.md exist
- T10: Cross-reference docs index vs actual files
- T11: Check for outdated references (old class names, removed functions)
- T12: Verify README instructions work

**Step 2: Fix documentation inconsistencies**

For each mismatch:
1. Determine which is correct (code or doc)
2. Update the stale reference
3. Verify the fix

**Step 3: Commit fixes**

```bash
git add docs/ CLAUDE.md README.md
git commit -m "docs: fix audit findings — stale paths, outdated references

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 15: Run T13-T15 — Integration checks

**Step 1: Execute integration checks**

- T13: Verify all feature flag combos don't crash
- T14: Check .env.example has all config vars from config.py
- T15: Smoke test — app boots OK
  ```bash
  PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('App boots OK')"
  ```

**Step 2: Fix any issues**

**Step 3: Commit**

```bash
git commit -am "fix: address integration audit findings

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 16: Clean up plan files

21 plan files exist. Many are superseded. Consolidate.

**Step 1: Identify superseded plans**

Read each plan file header. Plans that are fully superseded:
- `Q3-AUDIT-PROMPT.md` (superseded by `Q3-AUDIT-PROMPT-v2.md`)
- `AUDIT-FIX-PROMPT.md` (superseded by `FULL-PROJECT-AUDIT-PROMPT.md`)
- `AUDIT-PROMPT-UNIVERSAL-v2.md` (superseded by `FULL-PROJECT-AUDIT-PROMPT.md`)
- `AUDITOR-MULTIAGENTE.md` (superseded by `FULL-PROJECT-AUDIT-PROMPT.md`)
- `Q2-STORAGE-PROMPT.md` (Q2 completed)
- `Q3-RETRIEVAL-PROMPT.md` (Q3 completed)
- `Q2-RAG-BEST-PRACTICES.md` (Q2 completed, info captured in design docs)

**Step 2: Create archive directory and move old plans**

```bash
mkdir -p docs/plans/archive
git mv docs/plans/Q3-AUDIT-PROMPT.md docs/plans/archive/
git mv docs/plans/AUDIT-FIX-PROMPT.md docs/plans/archive/
git mv docs/plans/AUDIT-PROMPT-UNIVERSAL-v2.md docs/plans/archive/
git mv docs/plans/AUDITOR-MULTIAGENTE.md docs/plans/archive/
git mv docs/plans/Q2-STORAGE-PROMPT.md docs/plans/archive/
git mv docs/plans/Q3-RETRIEVAL-PROMPT.md docs/plans/archive/
git mv docs/plans/Q2-RAG-BEST-PRACTICES.md docs/plans/archive/
```

**Step 3: Verify the moves were clean**

Run: `ls docs/plans/archive/`
Expected: 7 archived files

**Step 4: Commit**

```bash
git add docs/plans/
git commit -m "chore: archive 7 superseded plan files to docs/plans/archive/

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 17: Move root-level eval reports into data/evals/

**Step 1: Move eval report files**

```bash
git mv eval_report_q3_gates.json data/evals/
git mv eval_report_q4.json data/evals/
git mv eval_report_q4_fix1.json data/evals/
git mv eval_report_q4_fix2.json data/evals/
git mv eval_report_q4_fix3.json data/evals/
```

**Step 2: Commit**

```bash
git add .
git commit -m "chore: move eval report snapshots from root to data/evals/

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## PHASE 3 — Hackathon Polish

### Task 18: Update CLAUDE.md with final project state

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Read current CLAUDE.md**

Read the file to check what needs updating.

**Step 2: Update key metrics**

Update the following sections:
- Test count: `517 tests collected` (update from 469)
- Add Q4 documentation files to the docs table
- Add new scripts to scripts table
- Update feature flags table with Q4 additions
- Add RAG modules to code structure

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with final post-Q4 project state

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 19: Update JUDGES-QUICK-EVAL.md

**Files:**
- Modify: `docs/06-integrations/JUDGES-QUICK-EVAL.md`

**Step 1: Read current file**

**Step 2: Update with Q4 achievements**

Add/update:
- RAG pipeline (hybrid BM25 + vector search) with P@3 = 86%
- Fallback chain: PGVector → JSON → Directory
- 517 tests, 26/26 quality gates
- Admin API for content management
- Response caching, drift detection, ingestion pipeline
- Memory/personalization system (behind feature flag)

**Step 3: Commit**

```bash
git add docs/06-integrations/JUDGES-QUICK-EVAL.md
git commit -m "docs: update judges guide with Q4 RAG achievements and metrics

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 20: Final smoke test and lint

**Step 1: Run full test suite**

Run: `python -m pytest tests/ -x -q --tb=short 2>&1 | tail -10`
Expected: All tests pass

**Step 2: Run lint**

Run: `ruff check src/ tests/ --select E,F,W --ignore E501`
Expected: Clean

**Step 3: Verify app boots**

```bash
PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('App boots OK')"
```
Expected: `App boots OK`

**Step 4: Verify git status is clean**

Run: `git status`
Expected: `nothing to commit, working tree clean`

**Step 5: Count final commits**

Run: `git log --oneline | head -20`
Expected: See all new commits from this session

---

## Summary

| Phase | Tasks | Purpose |
|-------|-------|---------|
| 1 — Git Hygiene | T1-T11 | Commit 91 files in 11 logical groups |
| 2 — Full Audit | T12-T17 | Run audit, fix issues, archive old plans |
| 3 — Hackathon Polish | T18-T20 | Update docs, final verification |

**Total: 20 tasks**

**Success Criteria:**
- [ ] Working tree clean (0 uncommitted files)
- [ ] All tests pass (517+)
- [ ] Lint clean
- [ ] App boots OK
- [ ] CLAUDE.md reflects current state
- [ ] Judges guide updated with Q4 achievements
- [ ] Superseded plans archived
- [ ] Root-level eval reports moved to data/evals/
