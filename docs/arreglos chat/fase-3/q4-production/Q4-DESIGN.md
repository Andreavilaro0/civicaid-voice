# Q4 Production Hardening — Architecture Decisions

**Date:** 2026-02-20
**Status:** CERRADO

## D1. Pipeline Integration (ADR-Q4-01)

**Context:** `pipeline.py:187` called `kb_lookup()` directly. The entire RAG pipeline (PGVector, FallbackRetriever, ResponseCache, rag_metrics) built in Q2-Q4 was dead code — WhatsApp messages only used the JSON keyword matcher.

**Decision:** Replace `kb_lookup(text, language)` with `get_retriever().retrieve(text, language)`.

**Rationale:**
- Minimal change (2 lines) — keeps pipeline.py stable
- `get_retriever()` returns the appropriate retriever based on config flags
- When `RAG_ENABLED=false`, `get_retriever()` returns `JSONKBRetriever` which internally calls `kb_lookup` — fully backward compatible
- When `RAG_ENABLED=true` + `RAG_FALLBACK_CHAIN=true`, returns `FallbackRetriever` with full chain
- `kb_lookup` import kept with `noqa: F401` for backward compatibility of external references

**Consequences:**
- All Q2-Q4 infrastructure is now reachable from production
- `RAG_ENABLED=false` (default) keeps behavior identical to pre-Q4
- Zero risk to existing functionality — feature flag controlled

## D2. Singleton get_retriever() (ADR-Q4-02)

**Context:** `get_retriever()` created a new `FallbackRetriever` per call. Each instantiation opened new DB connections (PGVectorStore), new Redis connections (ResponseCache), and fresh metric counters. Per-request instantiation caused resource leaks and lost observability data.

**Decision:** Implement module-level singleton with lazy initialization.

**Pattern:**
```python
_retriever_instance: Retriever | None = None

def get_retriever() -> Retriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = _build_retriever()
    return _retriever_instance

def reset_retriever() -> None:
    global _retriever_instance
    _retriever_instance = None
```

**Rationale:**
- Standard Python singleton via module-level variable — simple, well understood
- `_build_retriever()` encapsulates creation logic (config reading, chain assembly)
- `reset_retriever()` for test isolation — tests call it before/after factory tests
- Lazy init means no DB connection at import time — safe for test environments
- Thread safety: Python's GIL protects the simple reference assignment

**Consequences:**
- Single DB connection pool per process (via PGVectorStore)
- Single cache instance — hit/miss counters persist across requests
- Single metrics instance — rag_metrics records all retrievals
- Tests must call `reset_retriever()` to avoid cross-test contamination

## D3. FallbackRetriever Chain (ADR-Q4-03)

**Context:** Production must handle DB outages gracefully. A single retriever strategy is a single point of failure.

**Decision:** Three-tier fallback chain: PGVector -> JSON KB -> Directory.

**Chain construction (FallbackRetriever.__init__):**
1. If `RAG_ENABLED=true` and `RAG_DB_URL` set: try `PGVectorRetriever()` — if init fails (no DB), skip gracefully
2. Always: `JSONKBRetriever()` (keyword matching on `data/tramites/*.json`)
3. Always: `DirectoryRetriever()` (last resort, lists available procedures)

**Retrieval logic:**
1. Check cache (if `RAG_CACHE_ENABLED`)
2. Try each retriever in order — first non-None result wins
3. Store result in cache for future hits
4. Record metrics (source, latency, cache hit) if `RAG_METRICS_ENABLED`

**Rationale:**
- Graceful degradation: DB down -> keyword matching still works -> directory listing always works
- Cache reduces latency for repeated queries (common in WhatsApp conversations)
- Metrics track which tier is actually serving — critical for observability
- Each tier is independently togglable via config flags

**Consequences:**
- Resilience: Clara never returns "system error" for retrieval — always has a fallback
- Observability: `rag_metrics.record_retrieval(source, latency_ms, cache_hit)` tracks exactly what tier served each request
- Complexity: 4 code paths (cache, PGVector, JSON, Directory) — each tested independently

## D4. Response Cache (ADR-Q4-04)

**Context:** WhatsApp conversations often involve follow-up questions about the same tramite. Repeated queries to PGVector + Gemini reranker add latency.

**Decision:** LRU memory cache (default) with optional Redis backend.

**Implementation:** `ResponseCache` in `src/core/rag/response_cache.py`:
- Cache key: `hash(query + language)`
- TTL: `RAG_CACHE_TTL` (default 3600s)
- Backend: `RAG_CACHE_BACKEND` — "memory" (LRU, default) or "redis"
- Integrated into `FallbackRetriever.retrieve()` — cache check before chain, cache store after success

**Rationale:**
- Memory-first: Render free tier has 512MB RAM — LRU cache is zero-dependency
- Redis optional: for multi-worker deployments where shared cache matters
- TTL prevents stale answers after DB updates
- Cache key includes language — "ayuda IMV" (es) != "aide IMV" (fr)

**Consequences:**
- Second identical query in same session: ~0ms latency (cache hit)
- RAM bounded by LRU eviction policy
- Cache invalidation on ingestion: not automatic (TTL-based only)

## D5. Automated Scripts (ADR-Q4-05)

**Context:** Ingestion, drift detection, and BOE monitoring were library code without CLI entry points. Operators need runnable scripts for scheduled execution.

**Decision:** Three CLI scripts using `argparse` pattern:

| Script | Module | Key Flags |
|--------|--------|-----------|
| `scripts/run_ingestion.py` | `src/core/rag/ingestion.py` | `--all`, `--dry-run`, `--force` |
| `scripts/check_drift.py` | `src/core/rag/drift.py` | `--all`, `--stale`, `--json` |
| `scripts/check_boe.py` | `src/core/rag/boe_monitor.py` | `--check`, `--json` |

**Rationale:**
- `argparse` — standard library, no dependency
- `if __name__ == "__main__":` — importable as module, runnable as script
- `--dry-run` — safe exploration without DB writes
- `--json` — machine-readable output for automation/webhooks
- Scripts are thin wrappers — business logic stays in `src/core/rag/`

**Consequences:**
- Operators can schedule via cron or manual execution
- Scripts are testable via subprocess or direct import
- JSON output enables integration with monitoring dashboards

## D6. Eval Set Expansion (ADR-Q4-06)

**Context:** Q3 had 65 eval queries. For production confidence, need broader coverage of query patterns, edge cases, and negative examples.

**Decision:** Expand to 236 queries with structured categories.

**Distribution:**
- Basic info, requisitos, documentos, plazos per tramite
- Acronym queries (IMV, NIE, TIE, SEPE, etc.)
- Colloquial/informal queries
- Territorial queries (cities, CCAA)
- Negative queries (out-of-scope topics)
- Multi-tramite queries
- Edge cases (very short, very long, mixed languages)

**Schema per query:**
```json
{
  "id": "imv_basic_001",
  "query": "como pido el ingreso minimo vital",
  "expected_procedure": "ingreso_minimo_vital",
  "expected_section": "como_solicitar",
  "category": "basic_info",
  "difficulty": "easy"
}
```

**Rationale:**
- Each tramite >= 15 queries ensures no tramite is under-tested
- Negative queries validate that the system correctly returns None for out-of-scope
- Territorial queries test territory detection integration
- Edge cases catch parser/tokenizer issues

**Consequences:**
- Eval runtime increases (~2-3 minutes with Docker DB)
- More granular precision metrics per category
- Can identify weak spots (e.g., "coloquial P@3 = 0.70 while basic = 0.95")

## D7. Observability & Metrics (ADR-Q4-07)

**Context:** No visibility into which retriever tier serves requests, cache effectiveness, or query latency distribution.

**Decision:** `rag_metrics` singleton integrated into FallbackRetriever, exposed via admin endpoints.

**Metrics recorded per retrieval:**
- `source`: pgvector / json_fallback / directory_fallback / error
- `latency_ms`: end-to-end retrieval time
- `cache_hit`: boolean

**Admin endpoints:**
- `/admin/rag-metrics` — counters, latencies, hit rates
- `/admin/staleness` — procedure freshness report
- `/admin/satisfaction` — user satisfaction metrics (from feedback)

**Rationale:**
- Metrics inside the retriever (not outside) — captures actual behavior including cache
- Admin endpoints protected by Bearer token — prevents public exposure
- In-memory counters (not external system) — zero dependency for 512MB Render instance

**Consequences:**
- Dashboard possible: Grafana can poll `/admin/rag-metrics`
- Metrics reset on process restart (in-memory) — acceptable for hackathon
- Thread-safe counters via simple Python locking

## Architecture Diagram

```
WhatsApp User
    |
    v
Twilio -> Flask /webhook -> pipeline.py
                               |
                          get_retriever()  <-- singleton
                               |
                          FallbackRetriever
                               |
                    +----------+-----------+
                    |          |           |
                ResponseCache  |           |
                (if enabled)   |           |
                    |          |           |
              PGVectorRetriever  JSONKBRetriever  DirectoryRetriever
              (if RAG_ENABLED)   (keyword match)   (list procedures)
                    |
              +-----+-----+
              |     |     |
           embed  hybrid  rerank
           (Gemini) search (heuristic/Gemini)
                    |
              PostgreSQL + pgvector
              (8 procedures, 20 chunks)
```

## Feature Flag Matrix

| Flag | Default | Effect when false |
|------|---------|-------------------|
| RAG_ENABLED | false | Skip PGVector in chain, use JSON KB |
| RAG_FALLBACK_CHAIN | true | Use single retriever (PGVector or JSON), no chain |
| RAG_CACHE_ENABLED | false | No caching, every query hits retrievers |
| RAG_METRICS_ENABLED | true | No metrics recording |
| RAG_INGESTION_ENABLED | false | Ingestion scripts still work manually |
| RAG_DRIFT_CHECK_ENABLED | false | Drift scripts still work manually |
| RAG_BOE_MONITOR_ENABLED | false | BOE scripts still work manually |
| RAG_GROUNDED_PROMPTING | true | No [C1] citations in LLM responses |
