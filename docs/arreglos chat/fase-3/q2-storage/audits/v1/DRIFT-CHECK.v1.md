# Q2 Drift Check — Claim-by-Claim Audit (v1)

**Date:** 2026-02-19
**Auditor:** doc-auditor (automated)
**Method:** Every numeric claim extracted from Q2 docs, cross-referenced against actual source files and grep counts.

---

## Legend

| Status | Meaning |
|--------|---------|
| MATCH | Claim matches ground truth exactly |
| DRIFT | Claim does NOT match ground truth (requires fix) |
| NOTE | Qualitative/external, not directly verifiable from code |
| STALE | Was correct at time of writing, no longer matches current code |

---

## Q2-CLOSING-REPORT.md

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 1 | "72 new tests" | Line 12, 64, 92, 106 | 80 `def test_` across 7 RAG test files (9+16+6+11+30+4+4) | **DRIFT** |
| 2 | "197 existing tests" | Line 12 | 193 `def test_` in non-RAG test files (counted all 28 non-RAG test files) | **DRIFT** |
| 3 | "269 total tests" | Line 12, 93, 107 | 273 total `def test_` (193 non-RAG + 80 RAG). Without 8 Docker-skip tests: 265 | **DRIFT** |
| 4 | "264 passed + 5 xpassed = 269" | Line 93 | Cannot reproduce without Docker; `def test_` count yields 265 non-Docker. Discrepancy of 4 | **DRIFT** |
| 5 | "8 tramites migrated" | Line 14, 50, 88, 115 | 8 JSON files in `data/tramites/` (imv, empadronamiento, tarjeta_sanitaria, nie_tie, prestacion_desempleo, ayuda_alquiler, certificado_discapacidad, justicia_gratuita) | **MATCH** |
| 6 | "20 chunks" | Line 14, 88, 116 | Claim from migration output (3+2+1+2+3+3+3+3=20). Consistent across all docs | **NOTE** (DB-dependent, code-consistent) |
| 7 | "3,879 words" | Line 14, 88, 117 | From migration output. Consistent across all Q2 docs | **NOTE** (DB-dependent, internally consistent) |
| 8 | "8 new Python files" | Line 104 | 7 files in `src/core/rag/` (__init__.py, chunker.py, database.py, embedder.py, migrator.py, models.py, store.py) + `scripts/init_db.py` = 8 Python files. Report says "6 src + 1 script + 1 docker-compose" — docker-compose.yml is YAML, not Python. Counting __init__.py as a file gives 8 Python files total | **MATCH** (if counting __init__.py; report's breakdown is misleading since docker-compose is YAML) |
| 9 | "7 new test files" | Line 64, 105 | 7 test files exist: test_rag_models.py, test_chunker.py, test_embedder.py, test_store.py, test_migrator.py, test_rag_pipeline.py, test_rag_retriever.py | **MATCH** |
| 10 | "test_chunker.py (16)" | Line 66 | 16 `def test_` in test_chunker.py | **MATCH** |
| 11 | "test_embedder.py (6)" | Line 67 | 6 `def test_` in test_embedder.py | **MATCH** |
| 12 | "test_migrator.py (20)" | Line 69 | **30** `def test_` in test_migrator.py | **DRIFT** |
| 13 | "8 new RAG flags" | Line 60, 110 | 8 RAG flags in config.py lines 51-58: RAG_DB_URL, RAG_EMBEDDING_MODEL, RAG_EMBEDDING_DIMS, RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP, RAG_SIMILARITY_THRESHOLD, RAG_TOP_K, RAG_HYBRID_WEIGHT | **MATCH** |
| 14 | "3 new deps (sqlalchemy, psycopg2-binary, pgvector)" | Line 61, 109 | requirements.txt lines 12-14: sqlalchemy, psycopg2-binary, pgvector | **MATCH** |
| 15 | "4 tables" | Line 26, 85, 113 | 4 SQLAlchemy models: ProcedureDoc, Chunk, Source, IngestionLog | **MATCH** |
| 16 | "25+ columns" | Line 27 | 29 columns in ProcedureDoc (counted from models.py) | **MATCH** (29 >= 25+) |
| 17 | "Vector(768)" | Line 28 | `embedding = Column(Vector(768))` in models.py line 97 | **MATCH** |
| 18 | "768 dims" | Line 38, 87, 118 | `_EMBEDDING_DIM = 768` in embedder.py line 13; `output_dimensionality=_EMBEDDING_DIM` | **MATCH** |
| 19 | "pgvector 0.8.1" | Line 84 | From Docker verbatim output in gates.md. Cannot verify without Docker running | **NOTE** (verbatim evidence provided) |
| 20 | "PG16" | Line 21, 84 | `docker-compose.yml` line 3: `image: pgvector/pgvector:pg16` | **MATCH** |
| 21 | "gemini-embedding-001" | Line 38, 118 | embedder.py line 12: `"models/gemini-embedding-001"`. config.py line 52: `"models/gemini-embedding-001"` | **MATCH** |
| 22 | "11/11 gates" | Line 6, 96 | 11 rows in gates table, all say PASS | **MATCH** (per doc structure) |
| 23 | "Embedding model 404 — text-embedding-004" | Line 179 | Code now uses gemini-embedding-001 everywhere. Bug description is historical context | **MATCH** |
| 24 | "0 ruff errors" | Line 94, 108 | Cannot verify without running ruff. Gates.md shows "All checks passed!" | **NOTE** |
| 25 | "pipeline.py NOT touched" | Line 57, 112 | pipeline.py last modified 2026-02-18 00:58, before Q2 date of 2026-02-19 | **MATCH** |
| 26 | "3 (PK btree, GIN tsvector, HNSW embedding)" DB indexes | Line 114 | init_db.py creates 2 explicit indexes (GIN + HNSW); PK btree is auto. Total: 3 | **MATCH** |
| 27 | "IMV -> 3 chunks" | Line 86, 126 | From migration output; consistent across docs | **NOTE** (DB-dependent) |
| 28 | "src/ files touched: 3 (config.py, retriever.py, embedder.py)" | Line 111 | config.py modified (RAG flags added). retriever.py exists with PGVectorRetriever. embedder.py in rag/. Listed as "Modified" section also | **MATCH** |

---

## Q2-DESIGN.md

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 29 | "RAG_EMBEDDING_MODEL default: models/text-embedding-004" | Line 85 (Feature Flags table) | config.py line 52: `"models/gemini-embedding-001"`. embedder.py line 12: `"models/gemini-embedding-001"` | **DRIFT** (CRITICAL) |
| 30 | "RAG_DB_URL default: empty string" | Line 84 | config.py line 51: `""` | **MATCH** |
| 31 | "RAG_EMBEDDING_DIMS default: 768" | Line 86 | config.py line 53: `"768"` | **MATCH** |
| 32 | "RAG_CHUNK_SIZE default: 400" | Line 87 | config.py line 54: `"400"` | **MATCH** |
| 33 | "RAG_CHUNK_OVERLAP default: 50" | Line 88 | config.py line 55: `"50"` | **MATCH** |
| 34 | "RAG_SIMILARITY_THRESHOLD default: 0.7" | Line 89 | config.py line 56: `"0.7"` | **MATCH** |
| 35 | "RAG_TOP_K default: 5" | Line 90 | config.py line 57: `"5"` | **MATCH** |
| 36 | "RAG_HYBRID_WEIGHT default: 0.5" | Line 91 | config.py line 58: `"0.5"` | **MATCH** |
| 37 | "Native 3072 dims, reduced to 768" | Line 19 | gemini-embedding-001 native dim is 3072. Correct per Gemini docs | **MATCH** |
| 38 | "100 requests/min" | Line 20 | embedder.py line 15: `_MAX_REQUESTS_PER_MINUTE = 100` | **MATCH** |
| 39 | "200-600 token target" | Line 30 | Qualitative design claim; not directly verifiable from chunker code without reading config | **NOTE** |
| 40 | "50-token overlap" | Line 32 | config.py line 55: `RAG_CHUNK_OVERLAP = 50` default | **MATCH** |
| 41 | "8 new flags" | Line 80 | 8 flags listed, 8 flags in config.py | **MATCH** |
| 42 | "text-embedding-004 was deprecated" | Line 22 | Historical note. Closing report confirms model was switched | **MATCH** |

---

## evidence/gates.md

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 43 | "G3: 16 tests" | Line 15, 56 | test_chunker.py has 16 `def test_` | **MATCH** |
| 44 | "G4: 6 tests" | Line 16, 61 | test_embedder.py has 6 `def test_` | **MATCH** |
| 45 | "G5: 8/8 migrated, 20 chunks, 3,879 words" | Line 17, 67-79 | 8 tramites JSON files exist. Chunk/word counts from output | **MATCH** (file count) / **NOTE** (chunks/words) |
| 46 | "G6: score=0.7666" | Line 18, 85 | From verbatim output | **NOTE** (DB-dependent) |
| 47 | "G9: 72 tests passed" | Line 21, 111 | 80 `def test_` in those files now | **DRIFT** |
| 48 | "G10: 264 passed, 5 xpassed = 269" | Line 22, 116-118 | Current non-Docker `def test_` = 265 (273 total - 8 Docker). Does not match 269 | **DRIFT** |
| 49 | "Pre-existing: 197 tests" | Line 118 | 193 non-RAG `def test_` counted | **DRIFT** |
| 50 | "11/11 gates PASS" | Line 25 | 11 rows in table, all PASS | **MATCH** (per doc structure) |

---

## README.md (Q2 section, lines 90+)

| # | Claim | Location | Ground Truth | Status |
|---|-------|----------|--------------|--------|
| 51 | "8/8 tramites migrados (20 chunks, 3,879 palabras)" | Line 118 | 8 JSON files. Chunks/words from migration output | **MATCH** (files) / **NOTE** (runtime) |
| 52 | "72 tests nuevos + 197 existentes = 269 total" | Line 119 | 80 new + 193 existing = 273 total `def test_` | **DRIFT** |
| 53 | "11/11 gates PASS" | Line 120 | Per gates.md structure | **MATCH** |
| 54 | "0 errores lint" | Line 121 | Cannot verify without running ruff | **NOTE** |
| 55 | "pipeline.py NO tocado" | Line 122 | pipeline.py dated 2026-02-18 00:58, before Q2 | **MATCH** |

---

## Summary

| Status | Count |
|--------|-------|
| MATCH | 35 |
| DRIFT | 10 |
| NOTE | 10 |
| STALE | 0 |

### DRIFT Items Requiring Fix

| Priority | Claim | Current Value | Correct Value | Files to Fix |
|----------|-------|---------------|---------------|--------------|
| **P0 (CRITICAL)** | RAG_EMBEDDING_MODEL default in Q2-DESIGN.md | `models/text-embedding-004` | `models/gemini-embedding-001` | Q2-DESIGN.md line 85 |
| **P1** | "72 new tests" (all 4 docs) | 72 | 80 | Q2-CLOSING-REPORT.md lines 12,64,92,106; gates.md line 21,111; README.md line 119 |
| **P1** | "test_migrator.py (20)" | 20 | 30 | Q2-CLOSING-REPORT.md line 69 |
| **P1** | "197 existing tests" (all docs) | 197 | 193 | Q2-CLOSING-REPORT.md line 12; gates.md line 118; README.md line 119 |
| **P1** | "269 total tests" (all docs) | 269 | 273 (or 265 without Docker tests) | Q2-CLOSING-REPORT.md lines 12,93,107; gates.md lines 22,116-118; README.md line 119 |
| **P1** | "264 passed + 5 xpassed" | 264+5=269 | Current count yields 265 non-Docker `def test_` | gates.md line 22,116 |

---

*Generated 2026-02-19 by doc-auditor v1*
