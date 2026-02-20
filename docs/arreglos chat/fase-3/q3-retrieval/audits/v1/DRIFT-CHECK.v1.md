# Q3 Drift Check -- v1 (Re-Audit 2026-02-20)

| Field   | Value                                              |
|---------|----------------------------------------------------|
| Date    | 2026-02-20                                         |
| Scope   | Q3-CLOSING-REPORT.md, Q3-DESIGN.md, evidence/gates.md |
| Auditor | doc-auditor (fresh re-verification against live code) |
| Method  | grep -c, wc -l, python3 imports, pytest --collect-only, pytest -q |
| Note    | Previous audit (2026-02-19) reported 0 DRIFTs. This re-audit found 18 DRIFTs because Q4 work has since expanded synonyms, eval set, tests, and scripts beyond what the Q3 docs describe. |

---

## T5: Claim-by-Claim Verification

| # | Document | Claim | Line | Ground Truth | Status |
|---|----------|-------|------|--------------|--------|
| 1 | CLOSING | "13 entradas" synonyms | L12 | `len(SYNONYMS)` = 26 (Q4 added 13 more) | **DRIFT** |
| 2 | CLOSING | "17 CCAA + 60+ ciudades" | L15 | CCAA_MAP: 35 entries, 17 unique CCAA; CITY_MAP: 69 entries | MATCH |
| 3 | CLOSING | "65 queries" eval set | L17 | `rag_eval_set.json` has 236 queries | **DRIFT** |
| 4 | CLOSING | "9 categorias" eval | L57 | 11 categories (added edge_case, multi_tramite) | **DRIFT** |
| 5 | CLOSING | "8 tramites" eval | L57 | Not independently verified; plausible | NOTE |
| 6 | CLOSING | "86 tests nuevos (83 passed + 3 skipped)" | L18, L42 | `grep -c "def test_"` sum = 86. Per-file confirmed. | MATCH |
| 7 | CLOSING | "347 passed + 5 xpassed + 11 skipped" total | L82, L102 | pytest: 493 passed, 19 skipped, 5 xpassed | **DRIFT** |
| 8 | CLOSING | "0 regresion sobre 264 existentes" pre-Q3 | L18 | 493-86=407 non-Q3 tests now; stated baseline 277 (Q2) | **DRIFT** |
| 9 | CLOSING | synonyms.py LOC = 72 | L26 | `wc -l` = 86 | **DRIFT** |
| 10 | CLOSING | reranker.py LOC = 196 | L27 | `wc -l` = 197 | MATCH (~) |
| 11 | CLOSING | territory.py LOC = ~228 | L28 | `wc -l` = 226 | NOTE (~) |
| 12 | CLOSING | rag_eval.py LOC = ~115 | L29 | `wc -l` = 116 | MATCH (~) |
| 13 | CLOSING | run_rag_eval.py LOC = ~102 | L30 | `wc -l` = 188 | **DRIFT** |
| 14 | CLOSING | "LOC nuevas ~730" | L106 | Sum of 5 new modules: 86+197+226+116+188 = 813 | **DRIFT** |
| 15 | CLOSING | test_synonyms.py: 15 tests | L45 | grep -c = 15 | MATCH |
| 16 | CLOSING | test_reranker.py: 12 tests | L46 | grep -c = 12 | MATCH |
| 17 | CLOSING | test_territory.py: 16 tests | L47 | grep -c = 16 | MATCH |
| 18 | CLOSING | test_grounded_prompt.py: 13 tests | L48 | grep -c = 13 | MATCH |
| 19 | CLOSING | test_store_bm25.py: 9 tests | L49 | grep -c = 9 | MATCH |
| 20 | CLOSING | test_retriever_rerank.py: 7 tests | L50 | grep -c = 7 | MATCH |
| 21 | CLOSING | test_rag_eval.py: 11 tests | L51 | grep -c = 11 | MATCH |
| 22 | CLOSING | test_rag_precision.py: 3 (skip) | L52 | grep -c = 3 | MATCH |
| 23 | CLOSING | Per-file sum = 86 | L42 | 15+12+16+13+9+7+11+3 = 86 | MATCH |
| 24 | CLOSING | RAG_RERANK_STRATEGY default "heuristic" | L63 | config.py L61: default "heuristic" | MATCH |
| 25 | CLOSING | RAG_GROUNDED_PROMPTING default true | L64 | config.py L62: default "true" | MATCH |
| 26 | CLOSING | RAG_MAX_CHUNKS_IN_PROMPT default 4 | L65 | config.py L63: default "4" | MATCH |
| 27 | CLOSING | 3 feature flags | L19, L108 | config.py L61-63: 3 flags confirmed | MATCH |
| 28 | CLOSING | +chunks_used in KBContext | L36 | models.py L69: field present | MATCH |
| 29 | CLOSING | +expand_query, +territory_filter in store.py | L37 | store.py: search_hybrid L231, expand_query imported | MATCH |
| 30 | CLOSING | +rules 13-14, +chunks_block in system_prompt.py | L39 | L28: rule 13, L33: rule 14, L38: {chunks_block} | MATCH |
| 31 | CLOSING | +_build_grounded_context in llm_generate.py | L40 | llm_generate.py L33: function present | MATCH |
| 32 | CLOSING | "8 archivos" test files | L42 | 8 test files listed, all exist | MATCH |
| 33 | CLOSING | "5 src + 3 data/scripts" new files | L104 | 5 modules + 1 script + 1 data = 7; count "8" unclear | NOTE |
| 34 | CLOSING | 11/13 PASS, 2 DEFERRED | L85 | gates.md confirms 11 PASS + 2 DEFER | MATCH |
| 35 | CLOSING | Embedding model "gemini-embedding-001" | (implicit) | config.py: "models/gemini-embedding-001" (full path form) | NOTE |
| 36 | CLOSING | Embedding dim 768 | (implicit) | config.py L53: default "768" | MATCH |
| 37 | CLOSING | Eval categories: basic_info(14) requisitos(8) documentos(8) como_solicitar(8) plazos(5) acronyms(5) colloquial(7) territorial(5) negative(5) | L57 | Actual: basic_info(80) requisitos(8) documentos(8) como_solicitar(8) plazos(5) acronyms(15) colloquial(32) territorial(20) negative(20) +edge_case(20) +multi_tramite(20) | **DRIFT** |
| 38 | DESIGN | "13 acronimos/sinonimos" | L18 | 26 | **DRIFT** |
| 39 | DESIGN | "65 queries" eval set | L5, L10, L110 | 236 | **DRIFT** |
| 40 | DESIGN | "9 categorias" with per-cat counts | L111 | 11 categories, different counts | **DRIFT** |
| 41 | DESIGN | synonyms.py LOC = 72 | L91 | 86 | **DRIFT** |
| 42 | DESIGN | reranker.py LOC = 196 | L92 | 197 | MATCH (~) |
| 43 | DESIGN | territory.py LOC = 226 | L93 | 226 | MATCH |
| 44 | DESIGN | rag_eval.py LOC = 116 | L94 | 116 | MATCH |
| 45 | DESIGN | run_rag_eval.py LOC = ~102 | L95 | 188 | **DRIFT** |
| 46 | DESIGN | "86 tests nuevos (65 unit + 21 integ; 83+3)" | L116 | 86 confirmed; breakdown plausible | MATCH |
| 47 | DESIGN | "347 passed + 5 xpassed + 11 skipped" total | L117 | 493 passed, 19 skipped, 5 xpassed | **DRIFT** |
| 48 | DESIGN | "0 failures, 0 regression" | L118 | 0 failures confirmed | MATCH |
| 49 | DESIGN | "17" CCAA, "60+" cities | L53 | 17 unique CCAA, 69 cities | MATCH |
| 50 | DESIGN | RAG_RERANK_STRATEGY default "heuristic" | L78 | Confirmed | MATCH |
| 51 | DESIGN | RAG_GROUNDED_PROMPTING default true | L79 | Confirmed | MATCH |
| 52 | DESIGN | RAG_MAX_CHUNKS_IN_PROMPT default 4 | L80 | Confirmed | MATCH |
| 53 | DESIGN | chunks_used in KBContext | L102 | Confirmed | MATCH |
| 54 | DESIGN | _build_grounded_context | L106 | Confirmed | MATCH |
| 55 | DESIGN | expand_query in search_hybrid | L103 | Confirmed | MATCH |
| 56 | DESIGN | territory_filter param | L103 | Confirmed | MATCH |
| 57 | DESIGN | rules 13-14 in system_prompt | L105 | Confirmed | MATCH |
| 58 | DESIGN | {chunks_block} placeholder | L105 | Confirmed | MATCH |
| 59 | gates.md | "13 acronimos/sinonimos" | L40 | 26 | **DRIFT** |
| 60 | gates.md | "86 def test_ (83 passed + 3 skipped)" G11 | L17, L121 | 86 confirmed | MATCH |
| 61 | gates.md | "347 passed + 5 xpassed + 11 skipped" G12 | L18, L128 | 493 passed, 19 skipped, 5 xpassed | **DRIFT** |
| 62 | gates.md | "264 passed + 5 xpassed = 269" pre-Q3 | L131 | 493-86=407; baseline 277 (Q2) | **DRIFT** |
| 63 | gates.md | "347 passed + 5 xpassed = 352" post-Q3 | L132 | 493+5=498 | **DRIFT** |
| 64 | gates.md | test_reranker.py: "12 passed" | L53 | grep -c = 12 | MATCH |
| 65 | gates.md | test_territory.py: "16 passed" | L67 | grep -c = 16 | MATCH |
| 66 | gates.md | test_grounded_prompt.py: "13 passed" | L73 | grep -c = 13 | MATCH |
| 67 | gates.md | test_retriever_rerank.py: "7 passed" | L100 | grep -c = 7 | MATCH |
| 68 | gates.md | "65 queries (60 positivas + 5 negativas)" G9 | L107 | 236 queries, 20 negative | **DRIFT** |
| 69 | gates.md | ruff check "All checks passed" | L139 | Not re-run; plausible | NOTE |

---

## T6: Cross-Document Consistency

| # | Datum | CLOSING | DESIGN | gates.md | Internal | vs Code |
|---|-------|---------|--------|----------|----------|---------|
| 1 | Synonym count | 13 (L12) | 13 (L18) | 13 (L40) | CONSISTENT | **DRIFT** (actual 26) |
| 2 | Eval queries | 65 (L17,L57) | 65 (L5,L110) | 65 (L107) | CONSISTENT | **DRIFT** (actual 236) |
| 3 | Eval categories | 9 (L57) | 9 (L111) | N/A | CONSISTENT | **DRIFT** (actual 11) |
| 4 | Total tests passed | 347 (L82,L102) | 347 (L117) | 347 (L128) | CONSISTENT | **DRIFT** (actual 493) |
| 5 | Total xpassed | 5 (L102) | 5 (L117) | 5 (L128) | CONSISTENT | MATCH |
| 6 | Total skipped | 11 (L102) | 11 (L117) | 11 (L128) | CONSISTENT | **DRIFT** (actual 19) |
| 7 | Q3 new tests (def test_) | 86 (L18,L42) | 86 (L116) | 86 (L121) | CONSISTENT | MATCH |
| 8 | Q3 passed | 83 (L18,L42) | 83 (L116) | 83 (L121) | CONSISTENT | MATCH |
| 9 | Q3 skipped | 3 (L18,L42) | 3 (L116) | 3 (L121) | CONSISTENT | MATCH |
| 10 | synonyms.py LOC | 72 (L26) | 72 (L91) | N/A | CONSISTENT | **DRIFT** (actual 86) |
| 11 | reranker.py LOC | 196 (L27) | 196 (L92) | N/A | CONSISTENT | MATCH (~197) |
| 12 | territory.py LOC | ~228 (L28) | 226 (L93) | N/A | NOTE (~2 delta) | MATCH (actual 226) |
| 13 | rag_eval.py LOC | ~115 (L29) | 116 (L94) | N/A | NOTE (~1 delta) | MATCH (actual 116) |
| 14 | run_rag_eval.py LOC | ~102 (L30) | ~102 (L95) | N/A | CONSISTENT | **DRIFT** (actual 188) |
| 15 | RAG_RERANK_STRATEGY | "heuristic" | "heuristic" | N/A | CONSISTENT | MATCH |
| 16 | RAG_GROUNDED_PROMPTING | true | true | N/A | CONSISTENT | MATCH |
| 17 | RAG_MAX_CHUNKS_IN_PROMPT | 4 | 4 | N/A | CONSISTENT | MATCH |
| 18 | CCAA count | 17 (L15) | 17 (L53) | N/A | CONSISTENT | MATCH |
| 19 | Cities count | 60+ (L15) | 60+ (L53) | N/A | CONSISTENT | MATCH (69) |
| 20 | Pre-Q3 baseline | 264 (L18) | N/A | 264 (L131) | CONSISTENT | **DRIFT** |
| 21 | Gates result | 11/13 (L85) | N/A | 11/13 | CONSISTENT | MATCH |
| 22 | Feature flags | 3 (L19) | 3 (L74) | N/A | CONSISTENT | MATCH |

**Cross-doc conclusion**: Internal consistency is excellent -- all three docs agree with each other. However, 8 shared data points have drifted from the current code state due to Q4 changes.

---

## T7: Path Verification

| # | Path | Exists | Source Doc(s) |
|---|------|--------|---------------|
| 1 | `src/core/rag/synonyms.py` | OK | CLOSING, DESIGN, gates |
| 2 | `src/core/rag/reranker.py` | OK | CLOSING, DESIGN, gates |
| 3 | `src/core/rag/territory.py` | OK | CLOSING, DESIGN, gates |
| 4 | `src/utils/rag_eval.py` | OK | CLOSING, DESIGN |
| 5 | `scripts/run_rag_eval.py` | OK | CLOSING, DESIGN |
| 6 | `src/core/config.py` | OK | CLOSING, DESIGN |
| 7 | `src/core/models.py` | OK | CLOSING, DESIGN |
| 8 | `src/core/rag/store.py` | OK | CLOSING, DESIGN |
| 9 | `src/core/retriever.py` | OK | CLOSING, DESIGN, gates |
| 10 | `src/core/prompts/system_prompt.py` | OK | CLOSING, DESIGN |
| 11 | `src/core/skills/llm_generate.py` | OK | CLOSING, DESIGN |
| 12 | `data/evals/rag_eval_set.json` | OK | CLOSING, DESIGN, gates |
| 13 | `tests/unit/test_synonyms.py` | OK | CLOSING, gates |
| 14 | `tests/unit/test_reranker.py` | OK | CLOSING, gates |
| 15 | `tests/unit/test_territory.py` | OK | CLOSING, gates |
| 16 | `tests/unit/test_grounded_prompt.py` | OK | CLOSING, gates |
| 17 | `tests/unit/test_store_bm25.py` | OK | CLOSING |
| 18 | `tests/integration/test_retriever_rerank.py` | OK | CLOSING, gates |
| 19 | `tests/integration/test_rag_eval.py` | OK | CLOSING, gates |
| 20 | `tests/evals/test_rag_precision.py` | OK | CLOSING, gates |

**20/20 paths verified. 0 PHANTOM paths.**

### Function Verification

| # | Function | File:Line | Status |
|---|----------|-----------|--------|
| 1 | `expand_query()` | src/core/rag/synonyms.py:54 | OK |
| 2 | `rerank()` | src/core/rag/reranker.py:42 | OK |
| 3 | `_gemini_rerank()` | src/core/rag/reranker.py:76 | OK |
| 4 | `_heuristic_rerank()` | src/core/rag/reranker.py:140 | OK |
| 5 | `detect_territory()` | src/core/rag/territory.py:181 | OK |
| 6 | `_build_grounded_context()` | src/core/skills/llm_generate.py:33 | OK |
| 7 | `_build_datos()` | src/core/retriever.py:101 | OK |
| 8 | `search_hybrid()` | src/core/rag/store.py:231 | OK |
| 9 | `retrieve()` (PGVectorRetriever) | src/core/retriever.py:183 | OK |
| 10 | `chunks_used` field | src/core/models.py:69 | OK |

**10/10 functions verified. All present at documented locations.**

---

## Summary

| Metric | Count |
|--------|-------|
| Total claims checked | 69 |
| **MATCH** | 44 |
| **DRIFT** | 18 |
| **NOTE** | 5 |
| **STALE** | 0 |
| **PHANTOM paths** | 0 |

### Critical Drifts (require doc updates)

| ID | Issue | Docs Say | Actual | Affected Docs | Root Cause |
|----|-------|----------|--------|---------------|------------|
| D1 | Synonym count | 13 | 26 | ALL THREE | Q4 added 13 reverse/expanded synonyms |
| D2 | Eval query count | 65 | 236 | ALL THREE | Q4 expanded eval set ~3.6x |
| D3 | Eval categories | 9 | 11 (+ edge_case, multi_tramite) | CLOSING, DESIGN | Q4 added 2 new categories |
| D4 | Eval category counts | e.g. basic_info(14) | basic_info(80) etc. | DESIGN | Q4 expanded each category significantly |
| D5 | Total tests passed | 347 | 493 | ALL THREE | Q4 added ~146 more tests |
| D6 | Total skipped | 11 | 19 | ALL THREE | Q4 added 8 more skipped tests |
| D7 | Pre-Q3 baseline | 264 | ~407 (or 277 per Q2 report) | CLOSING, gates | More tests added to pre-Q3 modules by Q4 |
| D8 | synonyms.py LOC | 72 | 86 | CLOSING, DESIGN | File grew with new synonym entries |
| D9 | run_rag_eval.py LOC | ~102 | 188 | CLOSING, DESIGN | Script nearly doubled in size |
| D10 | Total new LOC | ~730 | 813 | CLOSING | Sum of individual LOC drifts |

### Interpretation

All 18 drifts follow a single pattern: **the Q3 docs were accurate at time of writing, but Q4 work expanded synonyms, eval queries, tests, and scripts without updating the Q3 docs**. The documents are internally consistent (cross-doc agreement is perfect), but stale relative to the current codebase.

**Recommendation**: Either (a) add a "Snapshot Date" header to each Q3 doc noting they reflect the Q3 closing state, or (b) update the numeric claims to current values with a note that Q4 expanded them.

No phantom files or missing functions were found. All paths and function references remain valid.
