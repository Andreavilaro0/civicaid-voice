# Q2 Design Decisions — PostgreSQL + pgvector Storage Layer

**Date:** 2026-02-19

---

## Why PostgreSQL + pgvector

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **pgvector (chosen)** | Single DB for structured + vector, SQL familiarity, hybrid BM25+vector, no extra infra | Slightly slower than dedicated vector DBs at scale | **CHOSEN** — hackathon simplicity, hybrid search built-in |
| ChromaDB | Easy Python API, in-memory dev mode | No SQL, limited hybrid search, another dependency | Rejected |
| FAISS | Fast, Meta-backed | No persistence by default, no BM25, complex | Rejected |
| Pinecone/Weaviate | Managed, scalable | External service, cost, overkill for 8 tramites | Rejected |

## Why Gemini gemini-embedding-001

- Already have `GEMINI_API_KEY` for the LLM (Gemini Flash) — zero extra cost
- Native 3072 dims, reduced to 768 via `output_dimensionality=768` — good balance of quality and storage
- Free tier: 100 requests/min — sufficient for migration and dev queries
- Same vendor for embed + generate = simpler ops
- Note: `text-embedding-004` was deprecated; `gemini-embedding-001` is the current model

## Chunking Strategy

**Section-based** (not fixed-size):
- Each ProcedureDoc section (descripcion, requisitos, documentos, plazos, como_solicitar, etc.) = 1+ chunks
- Preserves semantic boundaries — a "requisitos" chunk is always about requirements
- Heading path: "Ingreso Minimo Vital > Requisitos" — provides context to LLM
- Target: 200-600 tokens (gov docs are dense and short)
- Merge small sections (< 200 tokens) to avoid single-sentence chunks
- Split large sections (> 600 tokens) with 50-token overlap

**Why not fixed-size chunking:**
- Gov procedure documents have clear section structure
- Section-level retrieval gives the LLM focused, actionable context
- Fixed-size would cut across sections, mixing unrelated info

## Hybrid Search Design

```
Query: "que necesito para pedir el IMV"
  ├── BM25 (tsvector, Spanish config)
  │   └── Exact term matching: "IMV", "necesito", "pedir"
  ├── Vector (cosine similarity, pgvector)
  │   └── Semantic matching: "requisitos", "solicitar", "prestacion"
  └── Combined score = weight * vector + (1-weight) * bm25_normalized
      └── Default weight: 0.5 (tunable via RAG_HYBRID_WEIGHT)
```

BM25 catches exact terms (acronyms, procedure names). Vector catches semantic meaning. Combined is more robust than either alone.

## Score Threshold

- Default: 0.7 (configurable via `RAG_SIMILARITY_THRESHOLD`)
- If no chunk exceeds threshold → return None → fallback to kb_lookup (keyword) or "no tengo info"
- Prevents hallucination: better to say "no se" than to use a low-confidence chunk

## Backward Compatibility

- `RAG_ENABLED=false` (default) → `JSONKBRetriever` → existing keyword matching → zero behavior change
- `RAG_ENABLED=true` + `RAG_DB_URL` set → `PGVectorRetriever` → hybrid search
- Pipeline (`pipeline.py`) NOT touched — integration is transparent via `retriever.py`
- Original `data/tramites/*.json` NOT deleted — migration is additive

## Data Model

```
procedure_docs (1) ──< chunks (many)
     │                    │
     │                    └── embedding VECTOR(768)
     │                    └── tsvector GIN index (Spanish)
     │                    └── HNSW index on embedding
     │
sources (reference table)
     │
ingestion_log (audit trail)
```

## Feature Flags (8 new)

| Flag | Default | Purpose |
|------|---------|---------|
| RAG_DB_URL | "" | PostgreSQL connection string |
| RAG_EMBEDDING_MODEL | models/gemini-embedding-001 | Gemini embedding model |
| RAG_EMBEDDING_DIMS | 768 | Embedding dimensions |
| RAG_CHUNK_SIZE | 400 | Target chunk size (tokens) |
| RAG_CHUNK_OVERLAP | 50 | Overlap between split chunks |
| RAG_SIMILARITY_THRESHOLD | 0.7 | Minimum score to return results |
| RAG_TOP_K | 5 | Number of results to retrieve |
| RAG_HYBRID_WEIGHT | 0.5 | Vector vs BM25 weight (0=BM25, 1=vector) |

All configurable via environment variables. Existing `RAG_ENABLED` flag controls the switch.
