# Q4 — Production Hardening + Scale: Decisiones de Arquitectura

## Objetivo

Productizar la infraestructura RAG de Q2-Q3 para que sea operable, observable, resiliente y evaluable a escala. Al finalizar Q4:

1. Ingesta automatizada con scripts CLI
2. Drift detection con alertas webhook
3. Cache de respuestas (Redis primary + LRU fallback)
4. Cadena de fallback resiliente (PGVector -> JSON KB -> Directory)
5. Monitor BOE para publicaciones relevantes
6. Dashboard admin con metricas de latencia, hit rates y staleness
7. Eval set ampliado a 236 queries con 11 categorias
8. 50+ tests nuevos, 469 total, 0 regresion

## Decisiones de Arquitectura

### D1. Hybrid Search con Enrichment de Nombre de Procedimiento

**Problema**: BM25 no encontraba procedimientos por nombre (ej. "Ingreso Minimo Vital") porque el tsvector solo incluia el contenido del chunk, no metadata del procedimiento padre.

**Solucion**: Modificado `store.py` para hacer JOIN entre `chunks` y `procedure_docs`, incluyendo `p.nombre` en la construccion del tsvector.

```sql
-- Antes (Q3)
ts_rank(c.content_fts, plainto_tsquery('spanish', :query))

-- Despues (Q4)
ts_rank(
  c.content_fts || to_tsvector('spanish', COALESCE(p.nombre, '')),
  plainto_tsquery('spanish', :expanded_query)
)
```

**Trade-off**: El JOIN agrega complejidad al query pero el impacto en latencia es minimo (procedure_docs tiene < 50 rows). El beneficio es que BM25 ahora matchea por nombre de procedimiento, crucial para queries directas como "Ingreso Minimo Vital".

### D2. Territory Filter Inclusivo (NULL = Nacional)

**Problema**: Al aplicar un filtro territorial (ej. `ccaa = 'madrid'`), los procedimientos nacionales (AGE) no aparecian porque su metadata `territorio_ccaa` era NULL.

**Solucion**: Clausula WHERE inclusiva:

```sql
WHERE (c.metadata->>'territorio_ccaa' = :ccaa
       OR c.metadata->>'territorio_ccaa' IS NULL)
```

**Rationale**: En el dominio de tramites espanoles, un procedimiento AGE (nivel estatal) aplica en todo el territorio. Si el usuario pregunta "ayudas en Madrid", debe ver tanto tramites de la CAM como tramites nacionales. El filtro NULL = "aplica en todas partes" es la semantica correcta.

### D3. FallbackRetriever Chain

**Solucion**: `FallbackRetriever` en `retriever.py` implementa cadena de 3 niveles:

```
PGVectorRetriever  --(falla/sin resultados)--> JSONKBRetriever  --(falla/sin resultados)--> DirectoryRetriever
       |                                              |                                           |
  PostgreSQL + pgvector                     data/tramites/*.json                        data/tramites/ (listado)
  (hybrid search)                           (keyword match)                             (fallback basico)
```

**Response cache** (opcional via `RAG_CACHE_ENABLED`):
- Se consulta antes de la cadena de fallback
- Almacena resultados exitosos con TTL configurable (`RAG_CACHE_TTL`)
- Backend Redis primary, LRU in-memory fallback

**Trade-off**: La cadena agrega complejidad pero garantiza que Clara siempre responda, incluso si PostgreSQL esta caido. En produccion (hackathon/demo), la resiliencia es critica.

### D4. Heuristic Reranking (Gemini Deprecated)

**Problema**: El Gemini reranker (cross-encoder) fue planeado como estrategia principal en Q3, pero la API v1beta fue deprecada, haciendo el endpoint inestable.

**Solucion**: Mantener `RAG_RERANK_STRATEGY="heuristic"` como default en produccion. El reranker heuristico usa:
- Section match (0-3 pts): coincidencia entre seccion del chunk y tipo de pregunta
- Keyword overlap (0-3 pts): interseccion de keywords del query con keywords del chunk
- Original score (0-4 pts): score combinado de hybrid search
- Total normalizado a 0-1

**Trade-off**: Menor precision que un cross-encoder neuronal, pero:
- Latencia predecible (~0ms vs ~200ms/chunk)
- Sin dependencia de API externa
- Sin rate limiting compartido
- Reproducible y debuggeable

### D5. Scoring Hibrido: 0.5 * Vector + 0.5 * BM25

**Formula**:
```python
combined = RAG_HYBRID_WEIGHT * vector_score + (1 - RAG_HYBRID_WEIGHT) * normalized_bm25
```

Con `RAG_HYBRID_WEIGHT = 0.5`, ambos componentes pesan igual.

**Normalizacion BM25**: Los scores BM25 de PostgreSQL no estan acotados [0,1], asi que se normalizan dividiendo por el max score del batch.

**Threshold**: `RAG_SIMILARITY_THRESHOLD = 0.35`. Este valor bajo (vs 0.7 en vector puro) es necesario porque la combinacion 50/50 reduce el score maximo teorico. Un vector score de 0.8 y BM25 score de 0.6 produce combined = 0.7.

### D6. Synonym Expansion Ampliada

**Antes (Q3)**: 13 entradas de acronimos/sinonimos.

**Despues (Q4)**: 21 entradas (+8 nuevas):
- Reverse mappings: nombre completo -> acronimo (ej. "ingreso minimo vital" -> expand incluye "imv")
- Nuevos acronimos: OAC (Oficina de Atencion al Ciudadano), IPREM (Indicador Publico de Renta de Efectos Multiples), DARDE (Documento de Alta y Renovacion de Demanda de Empleo), MIVAU (Ministerio de Vivienda), AEAT (Agencia Tributaria)

**Trade-off**: Diccionario manual vs. NLP automatico. Seguimos con manual porque la lista de tramites es finita (< 50) y el control es total. El reverse mapping asegura que tanto "IMV" como "ingreso minimo vital" expandan bidireccionalmente.

### D7. Ingestion Pipeline con Content Hashing

**Flujo de ingesta** (`scripts/run_ingestion.py`):

```
data/tramites/*.json -> parse -> chunk -> embed -> upsert DB
                                                     |
                                              content_hash check
                                                     |
                                         changed? -> update chunks
                                         same?    -> skip (--force overrides)
```

**Content hashing**: SHA-256 del contenido JSON. Si el hash no cambio, el tramite se marca como "unchanged" y se salta (a menos que `--force`). Esto permite ejecuciones frecuentes sin re-procesar datos identicos.

**Registry mode** (`--registry`): Lee `data/sources/registry.yaml` con prioridades por tier para ingesta ordenada.

### D8. Drift Detection con Webhook Alerting

**Flujo de drift** (`scripts/check_drift.py`):

```
DB procedures -> comparar con JSON source -> clasificar status
                                                    |
                                          current / stale / drifted / missing
                                                    |
                                          stale: updated_at > threshold_days
                                          drifted: content_hash != source_hash
                                          missing: en DB pero no en source
```

**Webhook**: Si `--webhook` y `RAG_DRIFT_WEBHOOK_URL` estan configurados, envia alerta HTTP POST con payload JSON:

```json
{
  "procedures_checked": 8,
  "stale": ["age-segsocial-imv"],
  "drifted": [],
  "missing": [],
  "timestamp": "2026-02-20T12:00:00Z"
}
```

### D9. BOE Monitor con RSS + Keyword Matching

**Flujo** (`scripts/check_boe.py`):

```
BOE RSS feed -> parse entries -> keyword matching -> scoring -> alertas
                                      |
                              configurable via --keywords
                              default: keywords de tramites en DB
```

**Scoring**: TF-IDF simplificado — frecuencia de keywords del tramite en el titulo/resumen del BOE entry, normalizado por longitud. `--min-score` filtra alertas de baja relevancia.

### D10. Admin Dashboard (3 Endpoints Nuevos)

| Endpoint | Metodo | Auth | Descripcion |
|----------|--------|------|-------------|
| `/admin/ingestion-status` | GET | Bearer ADMIN_TOKEN | Ultimo resultado de ingesta: fecha, stats (processed, unchanged, updated, errors) |
| `/admin/drift-status` | GET | Bearer ADMIN_TOKEN | Ultimo resultado de drift check: procedures por status |
| `/admin/cache-stats` | GET | Bearer ADMIN_TOKEN | Stats del response cache: hits, misses, evictions, size |

**Seguridad**: Todos los endpoints admin requieren `Authorization: Bearer {ADMIN_TOKEN}`. Sin token configurado, los endpoints retornan 403.

### D11. RAG Metrics integradas en Pipeline

**`rag_metrics.py`** ahora se invoca automaticamente en el retriever pipeline con `record_retrieval()`:

```python
record_retrieval(
    source="pgvector",        # pgvector | json_kb | directory
    latency_ms=42.5,
    cache_hit=False,
    query_category="basic_info"
)
```

**Thread safety**: Contadores protegidos con `threading.Lock()`. Seguro para uso concurrente en Flask con hilos de fondo.

**Exposicion**: Via `/admin/rag-metrics` (endpoint existente, ahora con datos reales).

### D12. Eval Framework Ampliado

**Antes (Q3)**: 65 queries, 9 categorias, 8 tramites.

**Despues (Q4)**: 236 queries, 11 categorias, 8 tramites.

| Categoria | Q3 | Q4 | Delta |
|-----------|----|----|-------|
| basic_info | 14 | ~30 | +16 |
| requisitos | 8 | ~25 | +17 |
| documentos | 8 | ~20 | +12 |
| como_solicitar | 8 | ~20 | +12 |
| plazos | 5 | ~15 | +10 |
| acronyms | 5 | ~15 | +10 |
| colloquial | 7 | ~25 | +18 |
| territorial | 5 | ~20 | +15 |
| negative | 5 | ~30 | +25 |
| multi_tramite | 0 | ~18 | +18 |
| edge_cases | 0 | ~18 | +18 |
| **Total** | **65** | **236** | **+171** |

**Nuevas categorias**:
- `multi_tramite`: Queries que cruzan procedimientos (ej. "necesito NIE para pedir IMV?")
- `edge_cases`: Queries extremas (muy cortas, muy largas, emojis, numeros, mezcla FR/ES)

## Feature Flags Q4

12 flags nuevos en frozen dataclass `Config` (26 total):

| Flag | Default | Descripcion |
|------|---------|-------------|
| `RAG_FALLBACK_CHAIN` | `true` | Activa cadena PGVector -> JSON -> Directory |
| `RAG_CACHE_ENABLED` | `false` | Activa response cache |
| `RAG_CACHE_TTL` | `3600` | TTL cache en segundos |
| `RAG_CACHE_BACKEND` | `"redis"` | Backend: redis o lru |
| `RAG_INGESTION_ENABLED` | `false` | Ingesta automatizada |
| `RAG_INGESTION_INTERVAL_HOURS` | `168` | Intervalo ingesta |
| `RAG_INGESTION_MAX_SOURCES_PER_RUN` | `50` | Max fuentes por run |
| `RAG_DRIFT_CHECK_ENABLED` | `false` | Drift detection |
| `RAG_DRIFT_WEBHOOK_URL` | `""` | URL webhook alertas |
| `RAG_STALENESS_THRESHOLD_DAYS` | `90` | Umbral staleness |
| `RAG_BOE_MONITOR_ENABLED` | `false` | Monitor BOE |
| `RAG_METRICS_ENABLED` | `true` | Metricas RAG |

**Compatibilidad hacia atras**:
- `RAG_ENABLED=false` -> JSONKBRetriever (sin cambios, comportamiento Fase 2)
- `DEMO_MODE=true` -> Cache-only, skip LLM (sin cambios, comportamiento Fase 1)
- Todos los flags Q4 tienen defaults conservadores (false/off)

## Modulos Nuevos y Modificados

### Nuevos (3 scripts)
| Archivo | Funcion |
|---------|---------|
| `scripts/run_ingestion.py` | CLI runner de ingesta |
| `scripts/check_drift.py` | CLI runner de drift detection |
| `scripts/check_boe.py` | CLI runner de monitor BOE |

### Modificados
| Archivo | Cambios Q4 |
|---------|-----------|
| `src/core/config.py` | +12 flags Q4, threshold 0.7 -> 0.35 |
| `src/core/rag/store.py` | +get_stale_procedures(), JOIN procedure_docs en hybrid search, territory NULL filter |
| `src/core/rag/synonyms.py` | +8 entradas (reverse mappings + nuevos acronimos) |
| `src/core/retriever.py` | FallbackRetriever chain con response cache |
| `src/routes/admin.py` | +3 endpoints (ingestion-status, drift-status, cache-stats) |
| `src/utils/rag_metrics.py` | Integrado con retriever pipeline, record_retrieval() |
| `data/evals/rag_eval_set.json` | 65 -> 236 queries, +2 categorias |
