# Q2 PROMPT — Modelo de Datos + Storage (PG/Vec)

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el tech lead del proyecto **Clara / CivicAid Voice**. Vas a ejecutar el **Quarter 2 (Q2) de Fase 3: Modelo de Datos + Storage con PostgreSQL + pgvector**.

Trabaja en **team agent mode**. Crea un equipo, define tareas con dependencias, spawna agentes especializados y coordina la implementacion completa. Usa los skills `/rag-architect`, `/postgres-pro`, `/docker-expert` y `/test-driven-development` cuando necesites guia especializada durante la ejecucion.

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

Lee estos archivos en paralelo antes de crear el equipo:

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Contexto completo del proyecto |
| `docs/plans/Q2-RAG-BEST-PRACTICES.md` | Principios RAG a seguir en Q2 |
| `schemas/ProcedureDoc.v1.schema.json` | Schema de datos (29 campos) — tu modelo de DB lo refleja |
| `src/core/retriever.py` | Stub del retriever — aqui conectas el VectorRetriever |
| `src/core/skills/kb_lookup.py` | Busqueda actual por keywords — el fallback |
| `src/core/skills/llm_generate.py` | Como se construye el contexto KB para el LLM (tiered priority) |
| `src/core/config.py` | Feature flags existentes — aqui agregas los de RAG |
| `src/core/models.py` | Dataclasses existentes (KBContext, etc.) |
| `data/tramites/imv.json` | Ejemplo de KB actual — lo que migras a PG |
| `data/sources/registry.yaml` | 44 fuentes oficiales catalogadas en Q1 |
| `data/policy/allowlist.yaml` | Allowlist de dominios — metadata para sources |
| `docs/arreglos chat/fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md` | Reporte Q1.1 — que se construyo |
| `docs/arreglos chat/fase-3/q1-sources/backlog/Q2Q3Q4-backlog.md` | Backlog original Q2 — referencia |
| `requirements.txt` | Dependencias actuales |

## CONTEXTO RAPIDO

**Clara** = chatbot WhatsApp que ayuda a personas vulnerables en Espana a navegar tramites del gobierno. Stack: Python 3.11, Flask, Twilio, Gemini 1.5 Flash, Docker, Render.

**Q1 (CERRADO — FULL PASS)** creo artefactos machine-readable: registry.yaml (44 fuentes), schemas JSON, validadores, tests. Todo en `data/sources/`, `data/policy/`, `schemas/`, `scripts/`.

**Codigo actual de busqueda**: `kb_lookup.py` carga JSONs de `data/tramites/`, matchea por keywords, devuelve `KBContext`. `retriever.py` tiene interfaz abstracta `Retriever` con `JSONKBRetriever` implementado y `VectorRetriever` como placeholder.

**8 tramites existentes**: imv, empadronamiento, tarjeta_sanitaria, nie_tie, prestacion_desempleo, ayuda_alquiler, certificado_discapacidad, justicia_gratuita.

## OBJETIVO Q2

Implementar la **capa de datos y storage** que permite a Clara almacenar, indexar y buscar procedimientos gubernamentales usando **PostgreSQL + pgvector**. Al finalizar, `RAG_ENABLED=true` activa busqueda vectorial hibrida en lugar de keyword matching.

## ENTREGABLES CONCRETOS

### E1. Infraestructura DB
- `docker-compose.yml` con `pgvector/pgvector:pg16` para desarrollo local
- `src/core/rag/database.py` — Engine SQLAlchemy 2.0, session factory, get_session()
- `scripts/init_db.py` — Crear extension pgvector + tablas

### E2. Modelos de Datos (SQLAlchemy)
- `src/core/rag/models.py` con estas tablas:

```
procedure_docs:
  id (PK, slug pattern del schema)
  nombre, descripcion, organismo, organismo_abrev
  source_url, source_type (age/ccaa/local/boe)
  territorio_nivel, territorio_ccaa, territorio_municipio
  canal, idioma
  requisitos (JSONB), documentos_necesarios (JSONB)
  plazos (JSONB), como_solicitar (JSONB), donde_solicitar (JSONB)
  tasas, base_legal (JSONB), keywords (JSONB), tags (JSONB)
  content_hash, word_count, completeness_score
  extracted_at, verified_at, verified_by
  created_at, updated_at

chunks:
  id (PK, UUID)
  procedure_id (FK -> procedure_docs.id)
  section_name (descripcion, requisitos, documentos, plazos, como_solicitar, etc.)
  heading_path (ej: "IMV > Requisitos")
  content (TEXT)
  token_count (INT)
  embedding (VECTOR(768))  -- pgvector
  chunk_index (INT, orden dentro del doc)
  metadata (JSONB: territorio, source_type, idioma, canal)
  created_at

sources:
  id (PK, slug)
  name, url, source_type, gov_tier
  priority, status
  last_checked_at, last_fetched_at
  metadata (JSONB)

ingestion_log:
  id (PK, serial)
  procedure_id, source_id
  action (insert/update/delete)
  chunks_created, chunks_updated
  duration_ms
  created_at
```

### E3. Motor de Chunking
- `src/core/rag/chunker.py`
- Chunking **estructurado por secciones** del ProcedureDoc:
  - Cada seccion (descripcion, requisitos, documentos, plazos, como_solicitar, donde_solicitar, base_legal) = 1 o mas chunks
  - Heading path preservado: `"{nombre} > {seccion}"`
  - Metadatos: procedure_id, section_name, territorio, source_type, idioma
- Tamano target: **200-600 tokens** (documentos gubernamentales son densos y cortos)
- Overlap configurable (default 50 tokens entre chunks si una seccion es muy larga)
- Si una seccion es <200 tokens, combinar con la siguiente (merge strategy)

### E4. Pipeline de Embeddings
- `src/core/rag/embedder.py`
- Modelo: **Gemini text-embedding-004** (768 dims) via `google-generativeai`
- Ya tienen `GEMINI_API_KEY` — NO necesita otra clave
- Funciones: `embed_text(text) -> list[float]`, `embed_batch(texts) -> list[list[float]]`
- Rate limiting: max 100 requests/min (Gemini free tier)
- Retry con backoff exponencial

### E5. Storage Layer
- `src/core/rag/store.py` — clase `PGVectorStore`
- Operaciones:
  - `insert_procedure(doc, chunks_with_embeddings)` — transaccional
  - `search_vector(query_embedding, top_k=5, threshold=0.7)` — cosine similarity
  - `search_hybrid(query_text, query_embedding, top_k=5)` — BM25 (tsvector) + vector, score combinado
  - `search_metadata(filters: dict)` — pre-filtrado por territorio, source_type, canal, idioma
  - `get_procedure(id)`, `delete_procedure(id)`, `count_procedures()`, `count_chunks()`
- Indice GIN en tsvector para full-text search en espanol (`spanish` config)
- Indice IVFFlat o HNSW en columna vector para busqueda aproximada
- **Score threshold**: configurable, default 0.7 — si ningun chunk supera, retornar None

### E6. Migracion de Datos
- `src/core/rag/migrator.py`
- Convierte los 8 `data/tramites/*.json` al formato ProcedureDoc v1
- Para cada tramite:
  1. Mapear campos existentes → ProcedureDoc fields
  2. Generar campos faltantes (id slug, content_hash, word_count, completeness_score, extracted_at)
  3. Validar contra ProcedureDoc.v1.schema.json
  4. Chunking por secciones
  5. Generar embeddings
  6. Insertar en PostgreSQL
- Salida: informe con stats (procedures migrados, chunks creados, errores)

### E7. Integracion con Pipeline
- Implementar `PGVectorRetriever(Retriever)` en `src/core/retriever.py`
  - `retrieve(query, language)` hace:
    1. Embed query con Gemini
    2. `search_hybrid()` con pre-filtrado por idioma
    3. Convertir top result a `KBContext` (compatible con pipeline existente)
    4. Si no hay resultado sobre threshold → retornar None (fallback a kb_lookup o "no tengo info")
- Actualizar `get_retriever()`:
  - `RAG_ENABLED=true` → `PGVectorRetriever`
  - `RAG_ENABLED=false` → `JSONKBRetriever` (sin cambios)
- **NO tocar `pipeline.py`** — la integracion es transparente via retriever.py

### E8. Config y Feature Flags
- Nuevos flags en `src/core/config.py`:

```python
# --- RAG Database ---
RAG_DB_URL: str           # postgresql://user:pass@host:5432/clara_rag
RAG_EMBEDDING_MODEL: str  # models/text-embedding-004
RAG_EMBEDDING_DIMS: int   # 768
RAG_CHUNK_SIZE: int       # 400 (tokens target)
RAG_CHUNK_OVERLAP: int    # 50 (tokens)
RAG_SIMILARITY_THRESHOLD: float  # 0.7
RAG_TOP_K: int            # 5
RAG_HYBRID_WEIGHT: float  # 0.5 (0=solo BM25, 1=solo vector)
```

### E9. Tests (minimo 20 nuevos)

```
tests/unit/
  test_rag_models.py       — Modelos SQLAlchemy (create, validate, serialize)
  test_chunker.py          — Chunking por secciones, merge, overlap, metadatos
  test_embedder.py         — Embeddings con mock de Gemini API
  test_store.py            — CRUD, vector search, hybrid search, metadata filter
  test_migrator.py         — Migracion JSON → ProcedureDoc, validacion

tests/integration/
  test_rag_pipeline.py     — Full: JSON → PG → embed → search → KBContext
  test_rag_retriever.py    — PGVectorRetriever con DB real (docker)
```

### E10. Documentacion
- `docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md`
- `docs/arreglos chat/fase-3/q2-storage/Q2-DESIGN.md` (decisiones de arquitectura)
- `docs/arreglos chat/fase-3/q2-storage/evidence/gates.md`
- README actualizado de `docs/arreglos chat/fase-3/README.md`

## EQUIPO

Crea un equipo llamado **`q2-storage`** con estos agentes:

| Nombre | subagent_type | Responsabilidad |
|--------|---------------|-----------------|
| `db-architect` | general-purpose | Docker compose, SQLAlchemy models, database.py, init_db.py |
| `rag-engineer` | general-purpose | chunker.py, embedder.py, store.py (motor RAG completo) |
| `integrator` | general-purpose | migrator.py, PGVectorRetriever, config flags, requirements.txt |
| `qa-tester` | general-purpose | Todos los tests, validacion de gates, no-regresion |

## TAREAS CON DEPENDENCIAS

```
FASE A — Infraestructura (db-architect)
  T1: docker-compose.yml + database.py + models.py + init_db.py
  T2: Verificar que PG+pgvector arranca y tablas se crean

FASE B — Motor RAG (rag-engineer) [T1 completado]
  T3: chunker.py (chunking estructurado por secciones)
  T4: embedder.py (Gemini text-embedding-004 con rate limiting)
  T5: store.py (CRUD + vector search + hybrid search + indices)

FASE C — Integracion (integrator) [T1 + T3 + T4 + T5 completados]
  T6: migrator.py (8 tramites JSON → PG con chunks + embeddings)
  T7: PGVectorRetriever en retriever.py
  T8: config.py flags + requirements.txt update

FASE D — Tests (qa-tester) [T3-T8 completados]
  T9:  tests unitarios (modelos, chunker, embedder, store, migrator)
  T10: tests integracion (pipeline completo, retriever con DB)
  T11: no-regresion: ejecutar TODOS los tests existentes (182+)

FASE E — Cierre (team lead)
  T12: Ejecutar gates de calidad
  T13: Q2-CLOSING-REPORT.md + Q2-DESIGN.md + evidence/gates.md
  T14: Actualizar README fase-3
```

## GATES DE CALIDAD

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G1 | PG + pgvector arranca | `docker compose up -d && docker exec clara-db psql -U clara -d clara_rag -c "CREATE EXTENSION IF NOT EXISTS vector; SELECT extversion FROM pg_extension WHERE extname='vector';"` | Extension activa |
| G2 | Tablas creadas | `python scripts/init_db.py` sin errores | 4 tablas |
| G3 | Chunker produce chunks correctos | `pytest tests/unit/test_chunker.py -v` | IMV.json → ≥5 chunks con section_name |
| G4 | Embedder genera vectores | `pytest tests/unit/test_embedder.py -v` | Shape (768,) |
| G5 | 8 tramites migrados | `python -c "from src.core.rag.migrator import migrate_all; print(migrate_all())"` | 8 docs + ≥40 chunks |
| G6 | Vector search funciona | Query "que es el IMV" → chunk IMV en top-3 | Score > 0.7 |
| G7 | Hybrid search funciona | BM25 + vector combinados retornan resultados | Score combinado |
| G8 | PGVectorRetriever integrado | `RAG_ENABLED=true RAG_DB_URL=... pytest tests/integration/test_rag_retriever.py -v` | KBContext valido |
| G9 | ≥20 tests nuevos PASS | `pytest tests/unit/test_rag*.py tests/unit/test_chunker.py tests/unit/test_embedder.py tests/unit/test_store.py tests/unit/test_migrator.py tests/integration/test_rag*.py -v` | 20+ passed |
| G10 | No regresion | `pytest tests/ -v --tb=short` | 182+ tests (todos los existentes + nuevos) |
| G11 | Lint limpio | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | 0 errores |

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | pgvector no funciona en Docker local | Fallback: usar numpy cosine similarity sobre SQLite (dev-only), documentar como limitacion |
| A2 | Gemini embedding API no disponible o rate-limited | Fallback: sentence-transformers `all-MiniLM-L6-v2` local (384 dims, ajustar schema) |
| A3 | SQLAlchemy + pgvector incompatibles | Fallback: psycopg2 directo con SQL raw, sin ORM |
| A4 | Tests existentes rompen | **STOP** — fix regresiones ANTES de continuar. No avanzar con tests rotos |
| A5 | Migracion corrompe datos existentes | **STOP** — la migracion es ADITIVA, no reemplaza los JSON files originales |

## CONSTRAINTS TECNICAS

- **Python 3.11** — no cambiar
- **Flask** — no migrar a FastAPI
- **Sin Alembic** — usar scripts simples de init_db (hackathon, no enterprise)
- **Embedding**: `models/text-embedding-004` de Google (768 dims)
- **Similarity**: cosine (default pgvector, operator `<=>`)
- **NO tocar `src/core/pipeline.py`** — integracion transparente via retriever.py
- **Backward compatible**: `RAG_ENABLED=false` = todo sigue igual (JSONKBRetriever)
- **Feature flags**: todo nuevo detras de flags en config.py
- **No secrets en codigo**: DB URL via env var `RAG_DB_URL`
- **Docker compose = dev only**: produccion usara Supabase o Neon (no configurar ahora)
- **No borrar `data/tramites/*.json`**: la migracion es aditiva, los JSON quedan como backup
- **requirements.txt**: agregar `sqlalchemy>=2.0,<3.0`, `psycopg2-binary>=2.9,<3.0`, `pgvector>=0.3,<1.0`

## ESTRUCTURA FINAL ESPERADA

```
civicaid-voice/
  docker-compose.yml                    # NUEVO: PG+pgvector dev
  src/core/rag/
    __init__.py                         # NUEVO
    database.py                         # NUEVO: engine, sessions
    models.py                           # NUEVO: SQLAlchemy models
    chunker.py                          # NUEVO: structured chunking
    embedder.py                         # NUEVO: Gemini embeddings
    store.py                            # NUEVO: PGVectorStore
    migrator.py                         # NUEVO: JSON → PG migration
  src/core/retriever.py                 # MODIFICADO: + PGVectorRetriever
  src/core/config.py                    # MODIFICADO: + 8 RAG flags
  scripts/init_db.py                    # NUEVO: create tables
  requirements.txt                      # MODIFICADO: + 3 deps
  tests/unit/
    test_rag_models.py                  # NUEVO
    test_chunker.py                     # NUEVO
    test_embedder.py                    # NUEVO
    test_store.py                       # NUEVO
    test_migrator.py                    # NUEVO
  tests/integration/
    test_rag_pipeline.py                # NUEVO
    test_rag_retriever.py               # NUEVO
  docs/arreglos chat/fase-3/
    README.md                           # MODIFICADO: + Q2
    q2-storage/
      Q2-CLOSING-REPORT.md             # NUEVO
      Q2-DESIGN.md                     # NUEVO
      evidence/gates.md                 # NUEVO
```

## CRITERIOS DE EXITO Q2

Al finalizar, un juez deberia poder:

1. `docker compose up -d` → PostgreSQL con pgvector corriendo
2. `python scripts/init_db.py` → tablas creadas
3. `python -c "from src.core.rag.migrator import migrate_all; migrate_all()"` → 8 tramites migrados con chunks + embeddings
4. Hacer una query: "que es el IMV" → obtener chunks relevantes con score > 0.7
5. `RAG_ENABLED=true pytest tests/` → todos los tests pasan
6. `RAG_ENABLED=false pytest tests/` → todo sigue funcionando como antes

**EMPIEZA AHORA. Crea el equipo, define las tareas y spawna los agentes.**
