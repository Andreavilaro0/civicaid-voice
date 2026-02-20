# Q2 Red Team Report v1

**Date:** 2026-02-19
**Auditor:** red-teamer (adversarial)
**Scope:** Q2 Storage Layer (PG/Vec) — all claims in Q2-CLOSING-REPORT.md, Q2-DESIGN.md, evidence/gates.md
**Verdict:** CONDITIONAL PASS (2 FAIL, 3 NOTE, 7 PASS)

---

## Summary

| Vector | Name | Verdict |
|--------|------|---------|
| V1 | Denominadores enganosos | **FAIL** |
| V2 | Scope ambiguity | PASS |
| V3 | Counting confusion | **FAIL** |
| V4 | Stale claims | NOTE |
| V5 | "No code touched" claims | PASS |
| V6 | URLs inventadas | PASS |
| V7 | Phantom files | PASS |
| V8 | Gates claims vs evidence | NOTE |
| V9 | Schema mismatches | PASS |
| V10 | Undeclared dependencies | PASS |
| V11 | Backward compatibility | NOTE |
| V12 | Security regression | PASS |

**Critical findings: 2 FAIL items require documentation correction before FULL PASS.**

---

## Vector 1: Denominadores enganosos
**Investigation:** Counted `def test_` in each RAG test file to verify "72 new tests" claim. Verified 11/11 gates against the defined gates.

**Finding:** The actual test count across all 7 RAG test files is **80**, not 72:

| File | Claimed | Actual `def test_` |
|------|---------|---------------------|
| test_chunker.py | 16 | **16** |
| test_embedder.py | 6 | **6** |
| test_store.py | (unlisted) | **11** |
| test_migrator.py | 20 | **30** |
| test_rag_models.py | (unlisted) | **9** |
| test_rag_pipeline.py | (integration) | **4** |
| test_rag_retriever.py | (integration) | **4** |
| **Total** | **72** | **80** |

The denominator "72 new tests" is **stale** — it was likely correct at an earlier point but the test files grew. `test_migrator.py` alone has 30 test functions, not 20. `test_store.py` has 11, `test_rag_models.py` has 9.

The 11/11 gates denomination is correct — there are exactly 11 gates defined (G1-G11) and all are documented.

**Verdict:** **FAIL**
**Fix:** Update Q2-CLOSING-REPORT.md, evidence/gates.md, and fase-3/README.md: "72 new tests" -> "80 new tests". Update "269 total" -> "277 total" (or re-run pytest to confirm actual totals, since 197 + 80 = 277, not 269).

**Evidence:**
```
test_chunker.py:     16 def test_
test_embedder.py:     6 def test_
test_store.py:       11 def test_
test_migrator.py:    30 def test_
test_rag_models.py:   9 def test_
test_rag_pipeline.py: 4 def test_
test_rag_retriever.py:4 def test_
TOTAL:               80
```

---

## Vector 2: Scope ambiguity
**Investigation:** Verified "8/8 tramites migrated" against actual JSON files. Checked integration test skip behavior.

**Finding:**
- `ls data/tramites/*.json | wc -l` = **8** files. The 8 files match exactly:
  - imv.json, empadronamiento.json, tarjeta_sanitaria.json, nie_tie.json, prestacion_desempleo.json, ayuda_alquiler.json, certificado_discapacidad.json, justicia_gratuita.json
- "8/8 tramites migrated" is an accurate fraction — the denominator is the complete set of tramites JSON files.
- Integration tests (test_rag_pipeline.py, test_rag_retriever.py) use `pytest.mark.skipif(not os.getenv("RAG_DB_URL"))` — they are properly excluded from the non-Docker test count.
- G10 says "264 passed + 5 xpassed = 269 total" and explicitly `--ignore`s the 2 integration RAG test files. This scope is properly declared.

**Verdict:** PASS
**Evidence:** 8 JSON files in `data/tramites/`. Integration tests properly skipif-decorated.

---

## Vector 3: Counting confusion
**Investigation:** Cross-referenced metrics across Q2-CLOSING-REPORT.md, evidence/gates.md, and fase-3/README.md.

**Finding:** Multiple inconsistencies found:

1. **"72 new tests"** — appears in Q2-CLOSING-REPORT.md (lines 12, 64, 92, 106), evidence/gates.md (lines 21, 118), and fase-3/README.md (line 119). Actual count is **80**. All three documents are wrong.

2. **"269 total tests"** — appears in Q2-CLOSING-REPORT.md (lines 12, 93, 107) and evidence/gates.md (lines 22, 117). If pre-existing was 197 and new is 80, total should be **277** (or re-run to confirm). The 264+5=269 arithmetic is internally consistent but based on stale "72 new" count.

3. **"20 chunks"** — consistent across Q2-CLOSING-REPORT.md (lines 14, 88, 116, 134), evidence/gates.md (lines 17, 69). The migration table sums to 3+2+1+2+3+3+3+3 = 20. CORRECT.

4. **"3,879 words"** — consistent across all docs. Migration table totals not precisely verifiable without running migration, but the claim is internally consistent.

5. **"New Python files: 8 (6 src + 1 script + 1 docker-compose)"** — `docker-compose.yml` is YAML, not Python. The correct count is **7 new Python files** (6 src/core/rag/*.py + 1 scripts/init_db.py) plus 1 YAML file. The `__init__.py` in rag/ is also new, making it 8 Python files if counted. Either way, calling docker-compose.yml a "Python file" is misleading.

6. **"test_migrator.py (20)"** in Q2-CLOSING-REPORT.md line 69 — actual count is **30**.

**Verdict:** **FAIL**
**Fix required:**
- "72 new tests" -> "80 new tests" (all 3 documents)
- "269 total" -> re-run `pytest tests/ --ignore=... -q` to get actual total
- "test_migrator.py (20)" -> "test_migrator.py (30)"
- "New Python files: 8 (6 src + 1 script + 1 docker-compose)" -> "New Python files: 8 (7 src incl __init__.py + 1 script) + 1 docker-compose.yml (YAML)"

---

## Vector 4: Stale claims
**Investigation:** Searched for "text-embedding-004" across the entire repo. Checked Q2-DESIGN.md Feature Flags table.

**Finding:** Q2-DESIGN.md line 85 Feature Flags table says:
```
| RAG_EMBEDDING_MODEL | models/text-embedding-004 | Gemini embedding model |
```

But the actual code defaults are:
- `src/core/config.py:52` -> `"models/gemini-embedding-001"`
- `src/core/rag/embedder.py:12` -> `"models/gemini-embedding-001"`

The Q2-CLOSING-REPORT.md correctly says "gemini-embedding-001" everywhere (lines 38, 118, 167, 179), and Q2-DESIGN.md line 22 even notes "text-embedding-004 was deprecated; gemini-embedding-001 is the current model". But the Feature Flags TABLE on line 85 of Q2-DESIGN.md still shows the old model name.

Additionally, several plan documents still reference the old model:
- `docs/plans/Q2-RAG-BEST-PRACTICES.md:71`
- `docs/plans/Q2-STORAGE-PROMPT.md:110, 158, 208, 258`

These are pre-implementation plan docs, so arguably acceptable as historical, but the Q2-DESIGN.md table is the active reference doc.

**Verdict:** NOTE
**Fix recommended:** Update Q2-DESIGN.md line 85: `models/text-embedding-004` -> `models/gemini-embedding-001`. Plan documents can be left as-is (historical).

**Evidence:**
```
Q2-DESIGN.md:85: | RAG_EMBEDDING_MODEL | models/text-embedding-004 | ...
config.py:52:    default="models/gemini-embedding-001"
embedder.py:12:  _MODEL = os.getenv("RAG_EMBEDDING_MODEL", "models/gemini-embedding-001")
```

---

## Vector 5: "No code touched" claims
**Investigation:** Searched pipeline.py for any RAG/pgvector references. Verified "src/ files touched: 3" claim.

**Finding:**
- `grep -n "rag\|RAG\|PGVector\|pgvector\|vector" src/core/pipeline.py` returns **zero matches**. The claim "pipeline.py NOT touched" is **correct**. Pipeline still uses `kb_lookup` directly; the RAG path would go through `retriever.py` if wired up.
- "src/ files touched: 3 (config.py, retriever.py, embedder.py)" — Q2-CLOSING-REPORT.md line 111 lists these as "touched" (modified). However, line 167 lists `embedder.py` as **both Created and Modified**, which is contradictory. `embedder.py` is in `src/core/rag/embedder.py` and was created new. The `retriever.py` at `src/core/retriever.py` was modified (existed before as RAG stub). `config.py` was modified (8 new flags added). So the "3 src files touched" means 2 existing files modified (config.py, retriever.py) + 1 file listed in both sections (embedder.py). This is a bookkeeping error but not materially misleading.

**Verdict:** PASS
**Evidence:** Zero RAG references in pipeline.py. The "3 files touched" claim is essentially correct (2 modified pre-existing + embedder in both lists).

---

## Vector 6: URLs inventadas
**Investigation:** Extracted all `fuente_url` values from 8 tramites JSON files and verified domain plausibility.

**Finding:** All 8 URLs point to legitimate Spanish government domains:

| Tramite | Domain | Plausible |
|---------|--------|-----------|
| imv | seg-social.es | YES (Seguridad Social) |
| empadronamiento | madrid.es | YES (Ayto Madrid) |
| tarjeta_sanitaria | comunidad.madrid | YES (CAM) |
| nie_tie | inclusion.gob.es | YES (Ministerio) |
| prestacion_desempleo | sepe.es | YES (SEPE) |
| ayuda_alquiler | mivau.gob.es | YES (Ministerio Vivienda) |
| certificado_discapacidad | comunidad.madrid | YES (CAM) |
| justicia_gratuita | mjusticia.gob.es | YES (Ministerio Justicia) |

All domains are `.es`, `.gob.es`, or `.madrid` — consistent with Spanish government sites. No invented domains.

**Verdict:** PASS
**Evidence:** URLs extracted from `data/tramites/*.json` via `fuente_url` field. All domains verified as legitimate gov entities.

---

## Vector 7: Phantom files
**Investigation:** Checked existence of every file listed in Q2-CLOSING-REPORT.md "Files Created" section.

**Finding:** All 16 claimed files exist on disk:
```
EXISTS: docker-compose.yml
EXISTS: src/core/rag/__init__.py
EXISTS: src/core/rag/database.py
EXISTS: src/core/rag/models.py
EXISTS: src/core/rag/chunker.py
EXISTS: src/core/rag/embedder.py
EXISTS: src/core/rag/store.py
EXISTS: src/core/rag/migrator.py
EXISTS: scripts/init_db.py
EXISTS: tests/unit/test_rag_models.py
EXISTS: tests/unit/test_chunker.py
EXISTS: tests/unit/test_embedder.py
EXISTS: tests/unit/test_store.py
EXISTS: tests/unit/test_migrator.py
EXISTS: tests/integration/test_rag_pipeline.py
EXISTS: tests/integration/test_rag_retriever.py
```

Zero phantom files.

**Verdict:** PASS

---

## Vector 8: Gates claims vs evidence
**Investigation:** Verified G10 arithmetic and G9 test count against actual files.

**Finding:**
1. **G10 "264 passed + 5 xpassed = 269 total"** — the arithmetic 264 + 5 = 269 is correct. However, this was likely from a snapshot before test_migrator and test_store grew. If the current codebase has 80 RAG tests (not 72), the G10 total may not match a fresh run. Cannot verify without actually running pytest.

2. **G9 "72 tests passed"** — as established in V1, the actual `def test_` count is 80. The G9 verbatim output says "72 passed, 1 warning in 1.00s" — this was a real pytest run, but at a point when there were fewer tests. The tests have since grown.

3. Gate evidence format is clear and includes verbatim output. G1-G8 claims are well-supported by their output. G6 "score=0.7666" and G7 "combined=0.3998" are specific enough to be credible.

**Verdict:** NOTE (G9/G10 counts are stale snapshots, not fabricated — they reflect a prior state)
**Fix recommended:** Re-run G9 and G10 gates with current codebase and update evidence.

---

## Vector 9: Schema mismatches
**Investigation:** Counted Column() definitions in ProcedureDoc model. Cannot verify DB directly without Docker running.

**Finding:**
- ProcedureDoc model has **28 columns**: id, nombre, descripcion, organismo, organismo_abrev, source_url, source_type, territorio_nivel, territorio_ccaa, territorio_municipio, canal, idioma, requisitos, documentos_necesarios, plazos, como_solicitar, donde_solicitar, tasas, base_legal, keywords, tags, content_hash, word_count, completeness_score, extracted_at, verified_at, verified_by, created_at, updated_at.
- Q2-CLOSING-REPORT.md says "25+ columns" — 28 satisfies "25+". CORRECT.
- 4 tables claimed: procedure_docs, chunks, sources, ingestion_log. All 4 exist in models.py. CORRECT.
- Chunks model has Vector(768) as claimed. CORRECT.

**Verdict:** PASS (model code is consistent with claims; DB schema verification requires Docker)

---

## Vector 10: Undeclared dependencies
**Investigation:** Searched for unguarded API calls in tests and external network calls in source.

**Finding:**
1. All `genai.embed_content` references in test files are wrapped in `mock`, `Mock`, `patch`, or `MagicMock`:
   - test_embedder.py: all 9 occurrences are inside `mock_genai.embed_content` blocks
   - test_rag_pipeline.py: uses `patch("src.core.rag.embedder.genai")`
   - test_rag_retriever.py: uses `patch("src.core.rag.embedder.genai")`

2. No `requests.get`, `urllib`, or `httpx` calls in `src/core/rag/*.py` — the RAG code has no external HTTP dependencies beyond the Gemini SDK.

3. Integration tests properly use `pytest.mark.skipif(not os.getenv("RAG_DB_URL"))` — they declare the Docker dependency.

4. `requirements.txt` includes all 3 new deps: sqlalchemy, psycopg2-binary, pgvector.

**Verdict:** PASS
**Evidence:** All Gemini API calls in tests are mocked. Integration tests properly skip when DB unavailable.

---

## Vector 11: Backward compatibility
**Investigation:** Verified RAG_ENABLED flag defaults, pipeline.py isolation, and retriever factory.

**Finding:**
- `config.py:48`: `RAG_ENABLED` defaults to `false`. CORRECT.
- `pipeline.py` has zero RAG references — it still calls `kb_lookup()` directly. It does NOT call `get_retriever()`. This means even with `RAG_ENABLED=true`, the pipeline would NOT use the RAG path via `pipeline.py`. The PGVectorRetriever is available via `retriever.py` but is NOT wired into the main pipeline.
- This is actually a **design gap** rather than a backward-compat issue: the RAG path is complete but not integrated into the pipeline. Backward compatibility is preserved by default.
- Cannot run tests without environment setup, but the code structure confirms isolation.

**Verdict:** NOTE (RAG is not actually wired into pipeline.py — backward compat preserved, but the "integration" is incomplete in that the main pipeline never calls the retriever factory)

---

## Vector 12: Security regression
**Investigation:** Checked for SQL injection, hardcoded secrets, and PII in logs.

**Finding:**

1. **SQL injection in store.py `search_metadata()`:**
   - Line 350 uses `f"""...WHERE {where_clause}..."""` with `text()`.
   - HOWEVER, `where_clause` is constructed from a whitelist of `supported_filters` (line 333-341) that maps only known keys to hardcoded SQL fragments with named bind parameters (`:source_type`, `:idioma`, etc.).
   - User-supplied filter VALUES go through `params[key] = value` and are passed as bind parameters to `session.execute(sql, params)`.
   - User-supplied filter KEYS are checked against `supported_filters` dict — unknown keys are silently ignored.
   - **Verdict: NOT a SQL injection risk.** The f-string only interpolates strings from a hardcoded whitelist, not user input. Values are parameterized.

2. **Hardcoded credentials in database.py:**
   - Line 11: `"postgresql://clara:clara_dev@localhost:5432/clara_rag"` is the fallback default when `RAG_DB_URL` env var is not set.
   - This exposes the dev password `clara_dev` in source code. In production, `RAG_DB_URL` would be set via env var.
   - docker-compose.yml also contains `POSTGRES_PASSWORD: clara_dev`.
   - For a hackathon dev environment, this is acceptable but should be noted.

3. **Hardcoded credentials in docker-compose.yml:**
   - `POSTGRES_USER: clara`, `POSTGRES_PASSWORD: clara_dev` — these are dev-only credentials.

4. **Logger usage in RAG files:** All logger calls use standard levels (info, warning, error). No custom levels or PII-leaking patterns detected. Procedure IDs and counts are logged, not user queries or personal data.

**Verdict:** PASS (no SQL injection; dev credentials in source are acceptable for hackathon context; logging is clean)
**Evidence:**
```
store.py:350 — f-string only interpolates from hardcoded supported_filters whitelist
database.py:11 — fallback default "clara_dev" password (dev-only, env var overrides)
docker-compose.yml:7 — POSTGRES_PASSWORD: clara_dev (dev-only)
```

---

## Required Fixes (FAIL items)

### Fix 1: Test count correction
**Files to update:**
- `docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md`:
  - Line 12: "72 new" -> "80 new"
  - Line 64: "72 new tests across 7 files" -> "80 new tests across 7 files"
  - Line 69: "test_migrator.py (20)" -> "test_migrator.py (30)"
  - Line 92: "72 tests passed" -> "80 tests passed"
  - Line 106: "72" -> "80"
  - Line 107: "269" -> re-run to confirm
  - Line 93: "264+5 xpassed" -> re-run to confirm
- `docs/arreglos chat/fase-3/q2-storage/evidence/gates.md`:
  - Lines 21, 109-112, 117-118: update G9 and G10 output
- `docs/arreglos chat/fase-3/README.md`:
  - Line 119: "72 tests nuevos" -> "80 tests nuevos"

### Fix 2: Q2-DESIGN.md stale model name (NOTE -> should fix)
- `docs/arreglos chat/fase-3/q2-storage/Q2-DESIGN.md` line 85:
  - `models/text-embedding-004` -> `models/gemini-embedding-001`

---

*Generated 2026-02-19 by red-teamer (adversarial audit)*
