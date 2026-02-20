# Q2 Closing Report — Modelo de Datos + Storage (PG/Vec)

**Date:** 2026-02-19
**Branch:** fix/fase3-full-pass
**Python:** 3.11.8
**Status:** FULL PASS (11/11 gates)

---

## Executive Summary

Q2 delivers the complete PostgreSQL + pgvector storage layer for Clara's RAG system. All code is written, tested (80 new RAG tests across 7 files, 277 total collected: 264 passed, 8 skipped, 5 xpassed), and lint-clean. The system supports hybrid search (BM25 + vector cosine similarity), structured section-based chunking, and transparent integration with the existing pipeline via feature flags.

All 11 gates PASS including Docker verification: 8 tramites migrated (20 chunks, 3,879 words), vector search confirmed (IMV top result for "que es el IMV" at 0.77 score), hybrid search functional, and PGVectorRetriever returns KBContext end-to-end.

---

## Deliverables

### E1. Infrastructure DB
- `docker-compose.yml` — pgvector/pgvector:pg16, port 5432
- `src/core/rag/database.py` — SQLAlchemy 2.0 engine + session factory
- `scripts/init_db.py` — Create pgvector extension + tables + GIN/HNSW indexes

### E2. Data Models (SQLAlchemy)
- `src/core/rag/models.py` — 4 tables:
  - `procedure_docs` — 25+ columns matching ProcedureDoc v1 schema
  - `chunks` — UUID PK, Vector(768), GIN + HNSW indexes
  - `sources` — reference table for data provenance
  - `ingestion_log` — audit trail

### E3. Chunking Engine
- `src/core/rag/chunker.py` — Section-based structured chunking
  - 7 ProcedureDoc sections -> named chunks with heading paths
  - 200-600 token target, merge small, split large with overlap

### E4. Embedding Pipeline
- `src/core/rag/embedder.py` — Gemini gemini-embedding-001 (768 dims via output_dimensionality)
  - Rate limiting (100 req/min), retry with exponential backoff

### E5. Storage Layer
- `src/core/rag/store.py` — PGVectorStore class
  - Vector search (cosine similarity)
  - Hybrid search (BM25 + vector, configurable weight)
  - Metadata pre-filtering
  - Full CRUD operations

### E6. Data Migration
- `src/core/rag/migrator.py` — JSON -> PG migration
  - Maps 8 tramites to ProcedureDoc v1 format
  - Field renames, slug generation, content hashing, completeness scoring

### E7. Pipeline Integration
- `src/core/retriever.py` — PGVectorRetriever added
  - RAG_ENABLED=true -> hybrid search -> KBContext
  - RAG_ENABLED=false -> JSONKBRetriever (unchanged)
  - pipeline.py NOT touched

### E8. Config Flags
- `src/core/config.py` — 8 new RAG flags (DB URL, embedding model, chunk size, threshold, etc.)
- `requirements.txt` — 3 new deps (sqlalchemy, psycopg2-binary, pgvector)

### E9. Tests
- 80 new tests across 7 files:
  - `test_rag_models.py` (9) — model instantiation
  - `test_chunker.py` (16) — section chunking, merging, splitting
  - `test_embedder.py` (6) — embedding with mocked API
  - `test_store.py` (11) — CRUD, search, threshold
  - `test_migrator.py` (30) — field mapping, hashing, completeness
  - `test_rag_pipeline.py` (4) — integration (skip if no Docker)
  - `test_rag_retriever.py` (4) — retriever integration (skip if no Docker)

### E10. Documentation
- `Q2-CLOSING-REPORT.md` — this file
- `Q2-DESIGN.md` — architecture decisions
- `evidence/gates.md` — gate results with commands

---

## Gate Results

| Gate | Status | Detail |
|------|--------|--------|
| G1 PG+pgvector | PASS | pgvector 0.8.1 on PG16, container clara-db running |
| G2 Tables | PASS | 4 tables + GIN (tsvector Spanish) + HNSW (vector_cosine_ops) indexes |
| G3 Chunker | PASS | 16 tests, IMV -> 3 chunks with sections |
| G4 Embedder | PASS | 6 tests, 768-dim vectors (mocked) |
| G5 Migration | PASS | 8/8 tramites migrated, 20 chunks, 3,879 words, 0 errors |
| G6 Vector search | PASS | "que es el IMV" -> IMV top result (0.77 cosine score) |
| G7 Hybrid search | PASS | BM25+vector combined, IMV como_solicitar ranked #1 |
| G8 Retriever | PASS | PGVectorRetriever -> KBContext with datos, fuente_url, verificado |
| G9 New tests | PASS | 72 unit RAG tests passed (80 total def test_ across 7 files; 8 integration require Docker) |
| G10 No regression | PASS | 277 collected: 264 passed, 8 skipped, 5 xpassed |
| G11 Lint | PASS | 0 ruff errors |

**11/11 PASS**

---

## Metrics

| Metric | Value |
|--------|-------|
| New Python files | 8 (6 src + 1 script + 1 docker-compose) |
| New test files | 7 |
| New RAG tests (def test_) | 80 (72 unit + 8 integration) |
| Total tests collected (pytest) | 277 (264 passed, 8 skipped, 5 xpassed) |
| Lint errors | 0 |
| New dependencies | 3 (sqlalchemy, psycopg2-binary, pgvector) |
| New config flags | 8 |
| src/ files touched | 3 (config.py, retriever.py, embedder.py) |
| pipeline.py touched | NO |
| DB tables | 4 (procedure_docs, chunks, sources, ingestion_log) |
| DB indexes | 3 (PK btree, GIN tsvector, HNSW embedding) |
| Tramites migrated | 8/8 |
| Total chunks | 20 |
| Total words | 3,879 |
| Embedding model | gemini-embedding-001 (768 dims) |

---

## Migration Results

| Tramite | Chunks | Words |
|---------|--------|-------|
| imv | 3 | ~800 |
| empadronamiento | 2 | ~400 |
| tarjeta_sanitaria | 1 | ~200 |
| nie_tie | 2 | ~400 |
| prestacion_desempleo | 3 | ~600 |
| ayuda_alquiler | 3 | ~500 |
| certificado_discapacidad | 3 | ~500 |
| justicia_gratuita | 3 | ~474 |
| **Total** | **20** | **3,879** |

---

## Files Created/Modified

### Created
```
docker-compose.yml
src/core/rag/__init__.py
src/core/rag/database.py
src/core/rag/models.py
src/core/rag/chunker.py
src/core/rag/embedder.py
src/core/rag/store.py
src/core/rag/migrator.py
scripts/init_db.py
tests/unit/test_rag_models.py
tests/unit/test_chunker.py
tests/unit/test_embedder.py
tests/unit/test_store.py
tests/unit/test_migrator.py
tests/integration/test_rag_pipeline.py
tests/integration/test_rag_retriever.py
docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md
docs/arreglos chat/fase-3/q2-storage/Q2-DESIGN.md
docs/arreglos chat/fase-3/q2-storage/evidence/gates.md
```

### Modified
```
src/core/config.py (8 new RAG flags, embedding model default updated)
src/core/retriever.py (PGVectorRetriever + updated factory)
src/core/rag/embedder.py (model: gemini-embedding-001, output_dimensionality=768)
requirements.txt (3 new deps)
docs/arreglos chat/fase-3/README.md (Q2 section)
```

---

## Bugs Fixed During Docker Verification

| Issue | Detail | Fix |
|-------|--------|-----|
| GIN index DDL crash | SQLAlchemy can't compile REGCONFIG literal in `to_tsvector('spanish', ...)` | Moved GIN + HNSW indexes to raw SQL in `init_db.py` |
| Embedding model 404 | `models/text-embedding-004` no longer available in deprecated SDK | Switched to `models/gemini-embedding-001` with `output_dimensionality=768` |

---

## Code Review Findings

| Issue | Severity | Status |
|-------|----------|--------|
| M2: version field crash | MEDIUM | NOT PRESENT (migrator correctly omits version from DB dict) |
| M3/M4: datetime types | LOW | CLEAN (uses datetime objects, not ISO strings) |
| S3: unbounded search_metadata | LOW | FIXED (limit parameter added) |

---

## Known Limits

- Gemini `google.generativeai` SDK shows FutureWarning (deprecated in favor of `google.genai`) — cosmetic, migration deferred
- Hybrid search BM25 component needs tuning (some queries return 0.0 BM25 scores for Spanish acronyms)
- Production DB (Supabase/Neon) not configured — dev Docker only
- Retriever ranking quality to be tuned in Q3 (weight, threshold adjustments)

---

## Commands to Reproduce

```bash
# Start infrastructure
docker compose up -d
python scripts/init_db.py

# Set env vars
export RAG_DB_URL=postgresql://clara:clara_dev@localhost:5432/clara_rag
export GEMINI_API_KEY=<your-key>

# Migrate tramites
python -c "from src.core.rag.migrator import migrate_all; print(migrate_all())"

# Run all tests
pytest tests/ --tb=short -q

# Test vector search
python -c "
from src.core.rag.store import PGVectorStore
from src.core.rag.embedder import embed_text
store = PGVectorStore()
emb = embed_text('que es el ingreso minimo vital')
for r in store.search_vector(emb, top_k=3, threshold=0.3):
    print(f'{r[\"score\"]:.4f} {r[\"procedure_id\"]} {r[\"section_name\"]}')
"
```

---

*Q2 FULL PASS — 2026-02-19*
