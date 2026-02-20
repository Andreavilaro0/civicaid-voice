# Q4 PROMPT — Production Hardening + Scale

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el tech lead del proyecto **Clara / CivicAid Voice**. Vas a ejecutar el **Quarter 4 (Q4) de Fase 3: Production Hardening + Scale**.

Trabaja en **team agent mode**. Crea un equipo, define tareas con dependencias, spawna agentes especializados y coordina la implementacion completa. Usa los skills `/rag-architect`, `/postgres-pro`, `/docker-expert`, `/monitoring-expert`, `/sre-engineer`, `/database-optimizer`, `/test-driven-development` y `/systematic-debugging` cuando necesites guia especializada durante la ejecucion.

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

Lee estos archivos en paralelo antes de crear el equipo:

| # | Archivo | Para que |
|---|---------|----------|
| 1 | `CLAUDE.md` | Contexto completo del proyecto |
| 2 | `docs/plans/Q2-RAG-BEST-PRACTICES.md` | Principios RAG — fallbacks, cache, evaluacion |
| 3 | `docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md` | Que entrego Q2 — storage layer |
| 4 | `docs/arreglos chat/fase-3/q2-storage/Q2-DESIGN.md` | Decisiones arq Q2 |
| 5 | `docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md` | Que entrego Q3 — retrieval + rerank + grounding |
| 6 | `docs/arreglos chat/fase-3/q3-retrieval/Q3-DESIGN.md` | Decisiones arq Q3 |
| 7 | `docs/arreglos chat/fase-3/q3-retrieval/audits/v1/FIXES-APPLIED.v1.md` | Fixes de seguridad Q3 — no revertir |
| 8 | `src/core/config.py` | Feature flags — ya tiene 12 flags Q4 predefinidos |
| 9 | `src/core/retriever.py` | FallbackRetriever ya implementado |
| 10 | `src/core/rag/ingestion.py` | Pipeline de ingesta (269 LOC, implementado) |
| 11 | `src/core/rag/drift.py` | Deteccion de drift (216 LOC, implementado) |
| 12 | `src/core/rag/response_cache.py` | Cache RAG (216 LOC, implementado + testeado) |
| 13 | `src/core/rag/boe_monitor.py` | Monitor BOE (201 LOC, MVP implementado) |
| 14 | `src/core/rag/directory.py` | Fallback directory (98 LOC, implementado + testeado) |
| 15 | `src/core/rag/store.py` | PGVectorStore — YA tiene get_stale_procedures() (linea 417) |
| 16 | `src/core/rag/reranker.py` | Reranker — Gemini sin test real (solo mock) |
| 17 | `src/utils/rag_metrics.py` | Metricas RAG (185 LOC, implementado) |
| 18 | `src/routes/admin.py` | Endpoints admin (67 LOC, parcial) |
| 19 | `data/evals/rag_eval_set.json` | 65 queries eval — ampliar a 200+ |
| 20 | `data/tramites/*.json` | 8 tramites — verificar ingesta completa |
| 21 | `data/sources/registry.yaml` | 44 fuentes — para ingestion pipeline |
| 22 | `requirements.txt` | Dependencias actuales |
| 23 | `docker-compose.yml` | PG + pgvector dev |
| 24 | `tests/unit/test_response_cache.py` | Tests cache existentes (203 LOC) |
| 25 | `tests/unit/test_fallback_retriever.py` | Tests fallback existentes (205 LOC) |
| 26 | `tests/unit/test_directory.py` | Tests directory existentes (105 LOC) |
| 27 | `tests/integration/test_fallback_chain.py` | Tests cadena fallback (91 LOC) |
| 28 | `src/core/pipeline.py` | **CRITICO**: verificar linea ~187 — debe usar get_retriever(), NO kb_lookup() directo |

## CONTEXTO RAPIDO

**Clara** = chatbot WhatsApp que ayuda a personas vulnerables en Espana a navegar tramites del gobierno. Stack: Python 3.11, Flask, Twilio, Gemini 1.5 Flash, Docker, Render.

**Q1 (CERRADO — FULL PASS)**: 44 fuentes oficiales, ProcedureDoc v1 schema, validadores.

**Q2 (CERRADO — FULL PASS, 11/11 gates)**: PostgreSQL + pgvector, chunking por secciones, embeddings Gemini gemini-embedding-001 (768 dims), hybrid search BM25 + vector cosine, 8 tramites migrados (20 chunks), 80 tests RAG nuevos.

**Q3 (CERRADO — CONDITIONAL PASS, 11/13 gates, 2 DEFERRED Docker)**: Synonym expansion (13 entries), reranking dual (Gemini + heuristic), grounded prompting con [C1] citations, territory detection (17 CCAA, 69 ciudades), eval framework (65 queries), 86 tests nuevos. Security fixes: escape_xml_tags en chunks + [Cn] anti-spoofing. **Total post-Q3: 363 collected, 347 passed, 11 skipped, 5 xpassed.**

**Estado actual del codigo Q4**: Ya existen implementaciones de ingestion.py, drift.py, response_cache.py, boe_monitor.py, directory.py, rag_metrics.py y admin.py. **La mayoria estan ~95% completas pero les faltan tests unitarios, scripts de ejecucion programada, integracion con Docker real, y verificacion end-to-end.**

**11 Problemas conocidos (Q3 → Q4):**
1. **CRITICO — SHOWSTOPPER**: `pipeline.py:187` llama a `kb_lookup()` directamente — NUNCA usa `get_retriever()`. Todo el RAG pipeline (PGVector, FallbackRetriever, cache, metricas) es **dead code en produccion**
2. **CRITICO**: `get_retriever()` crea instancia nueva por llamada — sin singleton. Cada request abre conexiones DB+Redis nuevas, contadores de metricas se pierden
3. Docker-dependent gates sin verificar: Precision@3 >= 0.85 y BM25 activation >= 60%
4. Gemini reranker sin test real — solo mock/fallback testeado
5. Gemini SDK deprecation — `google.generativeai` → `google.genai` (ya migrado, verificar)
6. Territory filter sin efecto — 8 tramites son AGE (nivel estatal)
7. Sin script de ingestion programada — ingestion.py existe pero no hay runner
8. Sin script de drift check programada — drift.py existe pero no hay runner
9. Sin monitoring dashboard completo — rag_metrics.py existe, admin.py parcial
10. store.get_stale_procedures() YA EXISTE en store.py (lineas 417-442) — verificar con DB real
11. Eval set solo tiene 65 queries — necesita 200+

## OBJETIVO Q4

**"Productizar"** la infraestructura RAG: que todo lo que se construyo en Q2-Q3 sea operable, observable, resiliente y evaluable a escala. Al finalizar Q4:

1. **Ingesta automatizada** — script ejecutable que procesa tramites JSON, detecta cambios y actualiza DB
2. **Drift detection** — script que detecta contenido stale/cambiado y alerta via webhook
3. **Cache de respuestas** — LRU memory (default) + Redis opcional, reduce latencia en queries repetidas
4. **Cadena de fallback** — PGVector → JSON KB → Directory, resiliente cuando DB cae
5. **Monitor BOE** — detecta publicaciones relevantes en el BOE RSS
6. **Metricas + observabilidad** — dashboard admin con latencias, hit rates, staleness, satisfaccion
7. **Eval a escala** — 200+ queries, precision@3 >= 0.90, cobertura de 8 tramites x 5 categorias
8. **Tests completos** — 50+ tests nuevos, 519+ total, 0 regresion
9. **Docker gates Q3 cerrados** — Precision@3 y BM25 activation verificados con DB real

---

## FASE -1 — PREFLIGHT CHECK (5 min, OBLIGATORIO)

> Verifica que la infraestructura basica funciona antes de intentar cualquier otra cosa.

```bash
echo "=== PREFLIGHT CHECK ==="
echo "1. Docker:    $(docker --version 2>/dev/null || echo 'NOT FOUND')"
echo "2. Compose:   $(docker compose version 2>/dev/null || echo 'NOT FOUND')"
echo "3. Python:    $(python3 --version 2>/dev/null || echo 'NOT FOUND')"
echo "4. Deps:      $(pip list 2>/dev/null | grep -cE 'psycopg2|sqlalchemy|flask') de 3 encontradas"
echo "5. Puerto 5432: $(lsof -i :5432 2>/dev/null | head -1 || echo 'LIBRE')"
echo "6. .env:      $(test -f .env && echo 'OK' || echo 'MISSING')"
echo "7. GEMINI_API_KEY: $(grep -q 'GEMINI_API_KEY' .env 2>/dev/null && echo 'SET' || echo 'MISSING')"
```

**Si cualquier check critico falla** (Docker, Python, .env): arreglar ANTES de continuar. No hay valor en intentar Fase 0 con infra rota.

---

## FASE 0 — INTEGRACION CRITICA + CLEANUP Q3 (OBLIGATORIO ANTES DE Q4)

> Esta fase resuelve los 2 SHOWSTOPPERS arquitectonicos, los 2 gates DEFERRED de Q3, y los problemas conocidos mas criticos. **NO avanzar a Q4 sin completar Fase 0.**

### F0.0: CRITICO — Integrar Retriever en Pipeline (SHOWSTOPPER)

**Hallazgo de auditoria arquitectonica**: `pipeline.py:187` llama directamente a `kb_lookup(text, language)` — NUNCA usa `get_retriever()`. Esto significa que TODO el pipeline RAG construido en Q2-Q4 (PGVector, FallbackRetriever, ResponseCache, rag_metrics) es **dead code en produccion**. Los mensajes WhatsApp reales solo usan el JSON keyword matcher.

**Fix** (2 lineas en pipeline.py):
1. Agregar import: `from src.core.retriever import get_retriever`
2. Linea ~187: cambiar `kb_context: KBContext | None = kb_lookup(text, language)` por:
   ```python
   kb_context: KBContext | None = get_retriever().retrieve(text, language)
   ```

**Verificacion**:
- `grep "get_retriever" src/core/pipeline.py` → debe dar 1+ resultados
- `RAG_ENABLED=false pytest tests/ --tb=short` → 0 failures (backward compatible: sin RAG, get_retriever() devuelve JSONKBRetriever que internamente llama a kb_lookup)
- `RAG_ENABLED=true pytest tests/integration/test_pipeline.py -v` → usa PGVector

**Gate F0-0**: `grep -c "get_retriever" src/core/pipeline.py` >= 1

### F0.0b: Singleton get_retriever()

**Hallazgo**: `get_retriever()` crea una nueva instancia de `FallbackRetriever` en cada llamada. Cada instanciacion abre nuevas conexiones DB + Redis + ping. Los contadores de `rag_metrics` (hits, misses) se pierden con la instancia.

**Fix** en `src/core/retriever.py`:
```python
_retriever_instance: Retriever | None = None

def get_retriever() -> Retriever:
    """Factory — returns singleton retriever based on config."""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = _build_retriever()
    return _retriever_instance

def _build_retriever() -> Retriever:
    """Build the active retriever. Called once."""
    from src.core.config import config
    if config.RAG_FALLBACK_CHAIN:
        logger.info("Using FallbackRetriever (RAG_FALLBACK_CHAIN=true)")
        return FallbackRetriever()
    if config.RAG_ENABLED and config.RAG_DB_URL:
        logger.info("Using PGVectorRetriever")
        return PGVectorRetriever()
    return JSONKBRetriever()

def reset_retriever() -> None:
    """Reset singleton (for testing only)."""
    global _retriever_instance
    _retriever_instance = None
```

**Verificacion**: `python -c "from src.core.retriever import get_retriever; a=get_retriever(); b=get_retriever(); print(id(a)==id(b))"` → True

### F0.1: Docker + DB verificacion
1. `docker compose up -d` — levantar PostgreSQL + pgvector
2. `python scripts/init_db.py` — crear tablas
3. Ejecutar migracion: `python -c "from src.core.rag.migrator import migrate_all; print(migrate_all())"` → 8 docs migrados
4. Verificar: `python -c "from src.core.rag.store import PGVectorStore; s=PGVectorStore(); print(s.count_procedures(), s.count_chunks())"` → 8 procedures, >= 20 chunks

### F0.2: Gate Q3-G9 — Precision@3
1. Con DB poblada: `RAG_ENABLED=true RAG_DB_URL=postgresql://clara:clara_dev@localhost:5432/clara_rag python scripts/run_rag_eval.py`
2. **Criterio**: precision@3 >= 0.85
3. Si FAIL: revisar calidad de chunks, BM25 weights, reranker. Iterar hasta pasar

### F0.3: Gate Q3-G10 — BM25 activation
1. Verificar del eval report: BM25 activation rate >= 60%
2. Si FAIL: revisar synonym expansion, puede necesitar mas entradas en synonyms.py

### F0.4: Gemini reranker test real
1. Con DB + API key: ejecutar `rerank(query, results, strategy="gemini")` con datos reales
2. Verificar que el Gemini reranker produce scores diferenciados
3. Si rate limit: confirmar que fallback a heuristic funciona correctamente

### F0.5: Gemini SDK verification
1. Verificar que `google-genai` es el import usado (no `google.generativeai`)
2. `grep -rn "google.generativeai" src/` → debe dar 0 resultados
3. Si hay imports legacy: migrar a `google.genai`

**Gate Fase 0**: Los 7 sub-gates (F0-0, F0-0b, F0.1 a F0.5) deben PASS antes de continuar a Fase A.

---

## ENTREGABLES Q4

### E1. Script de Ingestion Programada
- **`scripts/run_ingestion.py`** — CLI runner para ingestion pipeline
- Funciones:
  - `--all` — re-ingestar todos los tramites desde `data/tramites/`
  - `--source <id>` — ingestar un tramite especifico
  - `--registry` — ingestar desde `data/sources/registry.yaml` (tier-based priority)
  - `--dry-run` — simular sin escribir a DB
  - `--force` — ignorar content hash (re-procesar aunque no haya cambios)
- Output: reporte JSON con stats (processed, unchanged, updated, errors, duration)
- Usa `src/core/rag/ingestion.py` (ya implementado, 269 LOC)
- **Pattern obligatorio**: usar `argparse` con `if __name__ == "__main__":`:
  ```python
  if __name__ == "__main__":
      import argparse
      parser = argparse.ArgumentParser(description="Ingestion runner for Clara RAG")
      parser.add_argument("--all", action="store_true", help="Ingest all tramites")
      parser.add_argument("--dry-run", action="store_true", help="Simulate without DB writes")
      args = parser.parse_args()
      main(args)
  ```
- Verificacion: `python scripts/run_ingestion.py --all --dry-run` → lista 8 tramites sin error

### E2. Script de Drift Detection
- **`scripts/check_drift.py`** — CLI runner para drift detection
- Funciones:
  - `--all` — verificar todos los procedures en DB vs JSON source
  - `--stale` — listar solo procedures con staleness > RAG_STALENESS_THRESHOLD_DAYS
  - `--webhook` — enviar alerta a RAG_DRIFT_WEBHOOK_URL si hay drift
  - `--json` — output en formato JSON para integracion
- Output: tabla con procedure_id, status (current/stale/drifted/missing), staleness_days, detail
- Usa `src/core/rag/drift.py` (ya implementado, 216 LOC)
- **Pattern obligatorio**: usar `argparse` con `if __name__ == "__main__":` (mismo patron que E1)
- Verificacion: `python scripts/check_drift.py --all` → 8 procedures "current" (si recien migrados)

### E3. Script de BOE Monitor
> **PRIORITY: LOW** — Ejecutar solo despues de que G16-G22 pasen. El BOE monitor no aporta al scoring del hackathon directamente. Si falta tiempo, SKIP este entregable.

- **`scripts/check_boe.py`** — CLI runner para BOE monitoring
- Funciones:
  - `--check` — fetch RSS + match keywords + report alerts
  - `--keywords "imv,nie,desempleo"` — override keywords default
  - `--min-score 0.5` — threshold minimo de relevancia
  - `--json` — output JSON
- **Pattern obligatorio**: usar `argparse` con `if __name__ == "__main__":` (mismo patron que E1)
- Usa `src/core/rag/boe_monitor.py` (ya implementado, 201 LOC)
- Verificacion: `python scripts/check_boe.py --check` → lista de alertas (puede ser vacia si no hay publicaciones recientes)

### E4. Verificar PGVectorStore.get_stale_procedures()
- **YA EXISTE** en `src/core/rag/store.py` (lineas 417-442). Consulta procedures con `updated_at < NOW() - threshold_days`, retorna lista de dicts con id, nombre, updated_at, staleness_days.
- **Verificar con DB real**: `python -c "from src.core.rag.store import PGVectorStore; s=PGVectorStore(); print(s.get_stale_procedures(90))"` → lista (puede ser vacia si recien migrados)
- Esto desbloquea el endpoint `/admin/staleness` en admin.py

### E5. Completar Admin Endpoints + Health Check Profundo
- **Verificar y mejorar `src/routes/admin.py`**:
  - `/admin/rag-metrics` — ya funciona, verificar output completo
  - `/admin/staleness` — depende de E4, verificar que no falla
  - `/admin/satisfaction` — verificar que funciona
  - **Nuevo**: `/admin/ingestion-status` — ultimo resultado de ingestion (fecha, stats)
  - **Nuevo**: `/admin/drift-status` — ultimo resultado de drift check
  - **Nuevo**: `/admin/cache-stats` — stats del response cache (hits, misses, evictions)
- **Constraints admin**:
  - Paginacion: max 100 items por response (`?limit=100&offset=0`)
  - Timeout: queries DB admin con timeout 5s (para evitar colgar workers)
  - Proteccion: todos los endpoints requieren `Authorization: Bearer {ADMIN_TOKEN}`
- **Mejorar `/health`** — health check profundo:
  - DB connectivity (si RAG_ENABLED): `SELECT 1` via store session
  - Cache connectivity (si RAG_CACHE_ENABLED): ping Redis o verificar LRU
  - Response: `{"status": "healthy|degraded|unhealthy", "checks": {"db": "ok", "cache": "ok", "gemini": "unchecked"}}`

### E6. Eval Set Ampliado (200+ queries)
- **Ampliar `data/evals/rag_eval_set.json`** de 65 → 200+ queries
- Distribucion:
  - 8 tramites x 5 categorias basicas (basic_info, requisitos, documentos, como_solicitar, plazos) = 40 queries existentes → ampliar a 80
  - Acronimos: 5 → 15 (IMV, NIE, TIE, SEPE, TSI, DARDE, OAC, CAEM, MIVAU, AEAT, DGT, IPREM, BOE, AGE, CCAA)
  - Coloquiales: 5 → 25 (preguntas informales, con errores ortograficos, mezcla idiomas)
  - Territoriales: 5 → 20 (ciudades, CCAA, "en mi zona", "aqui en Valencia")
  - Negativos: 5 → 20 (becas, pasaporte, maternidad, nacionalidad, hipoteca, herencias, divorcios...)
  - Multi-tramite: 0 → 20 (preguntas que cruzan tramites: "necesito NIE para pedir IMV?")
  - Edge cases: 0 → 20 (queries muy cortas, queries muy largas, solo emojis, solo numeros, mezcla FR/ES)
- Total target: **200 queries minimo**
- Cada query debe seguir este schema exacto:
  ```json
  {
    "id": "imv_basic_001",
    "query": "como pido el ingreso minimo vital",
    "expected_procedure": "ingreso_minimo_vital",
    "expected_section": "como_solicitar",
    "expected_keywords": ["imv", "solicitar", "ingreso minimo"],
    "territory": null,
    "category": "basic_info",
    "difficulty": "easy"
  }
  ```
- **Validacion de calidad**: muestreo aleatorio de 20 queries nuevas → verificar que expected_procedure es correcto. Distribucion uniforme: cada tramite >= 15 queries

### E7. Production Evaluation
- **Ejecutar eval completo** con Docker DB poblada sobre el eval set ampliado
- Metricas target:
  - precision@3 >= **0.90** (upgrade from Q3's 0.85)
  - precision@1 >= **0.75**
  - MRR >= **0.80**
  - BM25 activation >= **65%**
  - Section accuracy >= **0.70**
- Si no alcanza targets: iterar sobre synonym expansion, reranker weights, hybrid_weight
- Generar reporte: `scripts/run_rag_eval.py --output eval_report_q4.json`

### E8. Tests Nuevos (50+ minimo)

```
tests/unit/
  test_ingestion.py          — IngestionPipeline: ingest_source, content hash, dry-run, force
  test_drift.py              — DriftDetector: check_procedure, check_all, staleness scoring
  test_boe_monitor.py        — BOEMonitor: RSS parsing, keyword matching, scoring, error handling
  test_admin.py              — Admin endpoints: auth, rag-metrics, staleness, satisfaction, new endpoints
  test_rag_metrics.py        — RAGMetrics: thread safety, counters, to_dict, reset

tests/integration/
  test_ingestion_pipeline.py — Full: JSON → chunk → embed → DB (Docker required)
  test_drift_pipeline.py     — Full: modify JSON → detect drift → alert
  test_admin_integration.py  — Flask test client → admin endpoints → real metrics
  test_eval_200.py           — Eval 200+ queries (Docker required, puede ser slow)

tests/evals/
  test_rag_precision_q4.py   — Precision metrics sobre eval set ampliado (Docker)
```

**Criterio**: 50+ tests nuevos def test_, total suite 519+ collected, 0 regresion.

### E9. Documentacion
- `docs/arreglos chat/fase-3/q4-production/Q4-CLOSING-REPORT.md`
- `docs/arreglos chat/fase-3/q4-production/Q4-DESIGN.md` (decisiones de arquitectura, incluyendo ADR del fix pipeline.py y singleton)
- `docs/arreglos chat/fase-3/q4-production/evidence/gates.md`
- README actualizado de `docs/arreglos chat/fase-3/README.md`
- **Actualizar `docs/06-integrations/JUDGES-QUICK-EVAL.md`** con los nuevos scripts Q4 (ingestion, drift, admin, cache stats)

---

## EQUIPO

Crea un equipo llamado **`q4-production`** con estos agentes:

| Nombre | subagent_type | Skills recomendados | Responsabilidad |
|--------|---------------|---------------------|-----------------|
| `ingestion-engineer` | general-purpose | `/rag-architect`, `/database-optimizer` | Fase 0 (Docker + DB), scripts de ingestion/drift/BOE, verificar store.get_stale_procedures() con DB real, ingestion pipeline E2E |
| `resilience-engineer` | general-purpose | `/sre-engineer`, `/postgres-pro`, `/systematic-debugging` | Cadena de fallback verificacion, response cache integracion, admin endpoints completos, Gemini reranker test real |
| `observability-engineer` | general-purpose | `/monitoring-expert`, `/sre-engineer` | rag_metrics verificacion, admin dashboard, staleness/drift/satisfaction endpoints, alerting via webhook |
| `eval-qa` | general-purpose | `/test-driven-development`, `/rag-architect` | Eval set 200+, production eval, TODOS los tests nuevos (50+), no-regresion, gates |

## TAREAS CON DEPENDENCIAS

> **Formato**: `Tx: descripcion (owner) [depends_on: Ty, Tz]`

```
FASE 0 — INTEGRACION CRITICA + Cleanup Q3 (ingestion-engineer + resilience-engineer)
  T0a: SHOWSTOPPER — Integrar get_retriever() en pipeline.py (resilience-engineer) []
  T0b: Singleton get_retriever() con lazy init (resilience-engineer) [depends_on: T0a]
  T1:  Docker compose up + init_db + migrate_all (ingestion-engineer) []
  T2:  Gate Q3-G9 Precision@3 >= 0.85 con DB real (eval-qa) [depends_on: T0a, T0b, T1]
  T3:  Gate Q3-G10 BM25 activation >= 60% (eval-qa) [depends_on: T2]
  T4:  Gemini reranker test real con DB + API key (resilience-engineer) [depends_on: T1]
  T5:  Gemini SDK verification — 0 imports legacy (ingestion-engineer) []

  >>> CHECKPOINT: Los 7 sub-gates de Fase 0 deben PASS <<<
  >>> Si T2 o T3 FAIL: iterar synonyms.py/reranker/hybrid_weight antes de continuar <<<

FASE A — Ingestion & Drift Scripts (ingestion-engineer) [depends_on: T1, T5]
  T6:  scripts/run_ingestion.py — argparse CLI (ingestion-engineer) [depends_on: T1]
  T7:  scripts/check_drift.py — argparse CLI (ingestion-engineer) [depends_on: T1]
  T8:  scripts/check_boe.py — argparse CLI (ingestion-engineer) [depends_on: T5]  PRIORITY:LOW
  T9:  Verificar store.get_stale_procedures() con DB real (ingestion-engineer) [depends_on: T1]
  T10: Verificar ingestion E2E: run_ingestion.py --all → 8 tramites (ingestion-engineer) [depends_on: T6]

FASE B — Resilience & Cache (resilience-engineer) [depends_on: T0a, T0b, T1]
  T11: Verificar FallbackRetriever E2E: PGVector → JSON → Directory (resilience-engineer) [depends_on: T0b, T1]
  T12: Verificar response_cache integracion con singleton retriever (resilience-engineer) [depends_on: T0b]
  T13: Test de resilience: apagar Docker DB → degradar a JSON → Directory (resilience-engineer) [depends_on: T11]
  T14: Verificar que RAG_CACHE_ENABLED=true activa cache correctamente (resilience-engineer) [depends_on: T12]

FASE C — Observability & Admin (observability-engineer) [depends_on: T9, T11]
  T15: Completar admin.py: +ingestion-status, +drift-status, +cache-stats (observability-engineer) [depends_on: T9]
  T16: Mejorar /health — health check profundo (DB, cache, status) (observability-engineer) [depends_on: T14]
  T17: Integrar rag_metrics con singleton retriever (record_retrieval) (observability-engineer) [depends_on: T0b]
  T18: Verificar webhook alerting en drift.py (observability-engineer) [depends_on: T7]

FASE D — Eval Ampliado (eval-qa) [depends_on: T0a, T0b, T1]
  T19: Ampliar rag_eval_set.json 65 → 200+ queries con template JSON (eval-qa) [depends_on: T1]
  T20: Validar calidad: muestreo 20 queries, distribucion >= 15/tramite (eval-qa) [depends_on: T19]
  T21: Ejecutar production eval + iterar si precision@3 < 0.90 (eval-qa) [depends_on: T20]
  T22: Generar eval_report_q4.json con todas las metricas (eval-qa) [depends_on: T21]

FASE E — Tests Completos (eval-qa) [depends_on: T6-T18]
  T23: Tests unitarios: test_ingestion.py, test_drift.py, test_boe_monitor.py (eval-qa) [depends_on: T6, T7, T8]
  T24: Tests unitarios: test_admin.py, test_rag_metrics.py (eval-qa) [depends_on: T15, T16]
  T25: Tests integracion: test_ingestion_pipeline.py, test_drift_pipeline.py (eval-qa) [depends_on: T10]
  T26: Tests integracion: test_admin_integration.py (eval-qa) [depends_on: T15]
  T27: Tests evals: test_rag_precision_q4.py 200+ queries Docker (eval-qa) [depends_on: T22]
  T28: No-regresion: TODOS los tests existentes (469+) (eval-qa) [depends_on: T23-T27]

FASE F — Cierre (team lead) [depends_on: T28]
  T29: Ejecutar TODOS los gates de calidad (team lead) [depends_on: T28]
  T30: Q4-CLOSING-REPORT.md + Q4-DESIGN.md + evidence/gates.md (team lead) [depends_on: T29]
  T31: Actualizar README fase-3 + JUDGES-QUICK-EVAL.md (team lead) [depends_on: T30]
  T32: Verificacion final backward compatibility RAG_ENABLED=false (team lead) [depends_on: T28]
```

## GATES DE CALIDAD

### Gates Fase 0 (Integracion Critica + Q3 Deferred)

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G0-0 | **Pipeline usa retriever** | `grep -c "get_retriever" src/core/pipeline.py` | >= 1 |
| G0-0b | **Singleton funciona** | `python -c "from src.core.retriever import get_retriever; a=get_retriever(); b=get_retriever(); print(id(a)==id(b))"` | True |
| G0-1 | Docker DB arranca | `docker compose up -d && python scripts/init_db.py` sin errores | Tablas creadas |
| G0-2 | 8 tramites migrados | `python -c "from src.core.rag.migrator import migrate_all; print(migrate_all())"` | 8 docs, >= 20 chunks |
| G0-3 | Precision@3 >= 0.85 | `RAG_ENABLED=true RAG_DB_URL=... python scripts/run_rag_eval.py` | >= 0.85 |
| G0-4 | BM25 activation >= 60% | Del eval report | >= 60% |
| G0-5 | Gemini SDK limpio | `grep -rn "google.generativeai" src/` | 0 resultados |

### Gates Q4 — Ingestion & Scripts

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G1 | Ingestion script | `python scripts/run_ingestion.py --all --dry-run` | 8 tramites listados sin error |
| G2 | Ingestion real | `python scripts/run_ingestion.py --all` con DB | 8 ingested, stats JSON |
| G3 | Drift script | `python scripts/check_drift.py --all` con DB | 8 procedures "current" |
| G4 | BOE script | `python scripts/check_boe.py --check --json` | JSON output (puede ser []) |
| G5 | Stale procedures | `python -c "from src.core.rag.store import PGVectorStore; s=PGVectorStore(); print(s.get_stale_procedures(90))"` | Lista (puede ser vacia) |

### Gates Q4 — Resilience

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G6 | Fallback chain E2E | Query con DB arriba → PGVector result | KBContext valido |
| G7 | Fallback degradation | Query con DB apagada → JSON KB result | KBContext con source="json" |
| G8 | Directory fallback | Query con DB apagada + RAG_ENABLED=false → Directory result | KBContext con source="directory_fallback" |
| G9 | Cache funciona | Misma query 2 veces → segunda es cache hit | Latencia 2da < 5ms |
| G10 | Cache invalidation | Invalidar + re-query → cache miss | Hit count no incrementa |

### Gates Q4 — Observability

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G11 | Admin metrics | `curl -H "Authorization: Bearer $ADMIN_TOKEN" localhost:5000/admin/rag-metrics` | JSON con counters |
| G12 | Admin staleness | `curl -H "Authorization: Bearer $ADMIN_TOKEN" localhost:5000/admin/staleness` | JSON lista |
| G13 | Admin cache stats | `curl -H "Authorization: Bearer $ADMIN_TOKEN" localhost:5000/admin/cache-stats` | JSON con hits/misses |
| G14 | Metrics recording | Hacer 5 queries → rag_metrics.retrieval_total == 5 | Counter correcto |

### Gates Q4 — Eval & Quality

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G15 | Eval set 200+ | `python -c "import json; d=json.load(open('data/evals/rag_eval_set.json')); print(len(d['queries']))"` | >= 200 |
| G15.1 | Eval calidad | Muestreo aleatorio 20 queries nuevas → expected_procedure correcto | 20/20 correctos |
| G15.2 | Eval distribucion | Cada tramite tiene >= 15 queries en eval set | 8 tramites con >= 15 |
| G16 | Precision@3 >= 0.90 | `python scripts/run_rag_eval.py` con DB | >= 0.90 |
| G17 | Precision@1 >= 0.75 | Del eval report | >= 0.75 |
| G18 | MRR >= 0.80 | Del eval report | >= 0.80 |
| G19 | BM25 activation >= 65% | Del eval report | >= 65% |

### Gates Q4 — Tests

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G20 | >= 50 tests nuevos | `grep -c "def test_"` en archivos nuevos Q4 | >= 50 def test_ |
| G21 | Tests Q4 pasan | `pytest tests/unit/test_ingestion.py tests/unit/test_drift.py tests/unit/test_boe_monitor.py tests/unit/test_admin.py tests/unit/test_rag_metrics.py -v` | 0 failures |
| G22 | No regresion | `pytest tests/ --tb=short` | 519+ collected, 0 failures |
| G23 | Lint limpio | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | 0 errores |

### Gates Q4 — Backward Compatibility

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G24 | RAG off | `RAG_ENABLED=false pytest tests/ --tb=short` | 0 failures |
| G25 | Cache off | `RAG_CACHE_ENABLED=false pytest tests/ --tb=short` | 0 failures |
| G26 | Fallback off | `RAG_FALLBACK_CHAIN=false RAG_ENABLED=true pytest tests/ --tb=short` | 0 failures |
| G27 | Metrics off | `RAG_METRICS_ENABLED=false pytest tests/ --tb=short` | 0 failures |

### Gates Q4 — Security

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G28 | No secrets | `grep -rn "API_KEY\|AUTH_TOKEN\|SECRET" src/ --include="*.py" \| grep -v "os.getenv\|config\.\|environ\|getenv\|#\|test_\|mock\|fake\|dummy\|field(default"` | 0 resultados |
| G29 | Admin auth | `curl localhost:5000/admin/rag-metrics` (sin token) | 401 Unauthorized |
| G30 | SQL injection | `grep -rn "f\".*SELECT\|f\".*INSERT\|f\".*WHERE" src/` | 0 resultados (queries parametrizadas) |
| G31 | Sanitizacion | `grep -rn "escape_xml_tags" src/core/skills/llm_generate.py` | >= 3 llamadas (user_text, chunks, source_url) |

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Docker no arranca o pgvector falla | **STOP** — sin DB no se puede hacer Fase 0 ni Q4. Documentar y escalar |
| A2 | Precision@3 Q3 < 0.70 con DB real | **STOP** — problema fundamental en Q2/Q3, no es tema de Q4. Revisar chunks, embeddings |
| A3 | Gemini API no disponible o rate-limited | Usar `RAG_RERANK_STRATEGY="heuristic"` y mock embeddings para tests. Documentar |
| A4 | Tests existentes rompen ANTES de cambios Q4 | **STOP** — fix regresiones primero. Baseline roto es hallazgo P0 |
| A5 | store.get_stale_procedures() falla con DB real | Verificar query SQL en store.py:421-431. Puede necesitar ajuste de tipos en EXTRACT/MAKE_INTERVAL |
| A6 | Eval precision@3 no alcanza 0.90 tras 3 iteraciones | Documentar valor alcanzado y delta vs 0.90. CONDITIONAL PASS si >= 0.85 |

## CONSTRAINTS TECNICAS

- **Python 3.11** — no cambiar
- **Flask** — no migrar a FastAPI
- **Gemini gemini-embedding-001** — NO cambiar modelo de embedding (coherencia con Q2/Q3)
- **Gemini 1.5 Flash** — modelo LLM (no cambiar)
- **PostgreSQL + pgvector** — infraestructura existente de Q2 (no cambiar)
- **Cambio minimo en `src/core/pipeline.py`**: SOLO sustituir `kb_lookup()` por `get_retriever().retrieve()` (2 lineas, Fase 0). No tocar el resto del pipeline
- **NO tocar security fixes de Q3** — escape_xml_tags en llm_generate.py, [Cn] anti-spoofing, rule 11 chunks_block
- **Backward compatible**:
  - `RAG_ENABLED=false` = todo sigue igual (JSONKBRetriever)
  - `RAG_CACHE_ENABLED=false` = sin cache
  - `RAG_FALLBACK_CHAIN=false` = solo PGVectorRetriever (sin fallback)
  - `RAG_INGESTION_ENABLED=false` = sin ingestion automatica
  - `RAG_DRIFT_CHECK_ENABLED=false` = sin drift detection
  - `RAG_BOE_MONITOR_ENABLED=false` = sin monitor BOE
  - `RAG_METRICS_ENABLED=false` = sin metricas
- **Feature flags**: todo nuevo detras de flags en config.py (12 flags Q4 ya definidos)
- **No secrets en codigo**: API keys, DB URLs, tokens via env vars
- **No borrar archivos de Q2/Q3**: Q4 es ADITIVO
- **No borrar `data/tramites/*.json`**: la ingestion es aditiva, los JSON quedan como source of truth
- **requirements.txt**: NO agregar dependencias nuevas salvo que sea estrictamente necesario
- **Score threshold 0.7** — mantener default de Q2
- **Max 4 chunks en prompt** — mantener default de Q3
- **Respuestas max 200 palabras** — regla existente de Clara, no cambiar
- **Docker compose = dev only**: produccion usa managed PostgreSQL (Neon/Supabase)
- **Render free tier** (512MB RAM): scripts de ingestion/drift/BOE se ejecutan manualmente o via cron externo, no como procesos residentes
- **Cache default = memory**: `RAG_CACHE_BACKEND="memory"` por defecto (LRU, ideal para 512MB). Solo cambiar a `"redis"` si hay Redis disponible

## ROLLBACK STRATEGY

1. **Git tags antes de cada fase**: `git tag pre-q4-fase-X` antes de empezar cada fase
2. **Feature flags como kill switch**: Si algo rompe produccion, revertir el flag a `false` en .env — cada feature Q4 tiene su flag independiente
3. **Health check post-cambio**: Despues de cada entregable, verificar:
   - `curl localhost:5000/health` → 200 OK
   - `PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('App boots OK')"` → sin errores
4. **Revert atomico**: Si un entregable rompe tests, `git checkout -- archivo` para ese entregable especifico

## CI/CD (OPCIONAL)

Si se configura GitHub Actions, minimo:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    env:
      POSTGRES_PASSWORD: clara_dev
    ports:
      - 5432:5432
```

Marcar tests Docker-dependent con `@pytest.mark.docker` para poder correr pipeline sin Docker:
```bash
pytest tests/ -v --tb=short -m "not docker"  # CI sin Docker
pytest tests/ -v --tb=short                   # CI con Docker service
```

## ESTRUCTURA FINAL ESPERADA

```
civicaid-voice/
  scripts/
    run_ingestion.py                       # NUEVO: CLI ingestion runner
    check_drift.py                         # NUEVO: CLI drift detection runner
    check_boe.py                           # NUEVO: CLI BOE monitor runner
  src/core/
    pipeline.py                            # MODIFICADO: kb_lookup() → get_retriever().retrieve() (2 lineas)
    retriever.py                           # MODIFICADO: singleton get_retriever() + reset_retriever()
  src/core/rag/
    ingestion.py                           # YA EXISTE (269 LOC) — verificar completeness
    drift.py                               # YA EXISTE (216 LOC) — verificar completeness
    response_cache.py                      # YA EXISTE (216 LOC) — verificar integracion
    boe_monitor.py                         # YA EXISTE (201 LOC) — verificar completeness
    directory.py                           # YA EXISTE (98 LOC) — verificar completeness
    store.py                               # YA TIENE get_stale_procedures() — verificar con DB
  src/utils/
    rag_metrics.py                         # YA EXISTE (185 LOC) — verificar integracion
  src/routes/
    admin.py                               # MODIFICADO: + 3 endpoints nuevos
  data/evals/
    rag_eval_set.json                      # MODIFICADO: 65 → 200+ queries
  tests/unit/
    test_ingestion.py                      # NUEVO
    test_drift.py                          # NUEVO
    test_boe_monitor.py                    # NUEVO
    test_admin.py                          # NUEVO
    test_rag_metrics.py                    # NUEVO
  tests/integration/
    test_ingestion_pipeline.py             # NUEVO (Docker)
    test_drift_pipeline.py                 # NUEVO (Docker)
    test_admin_integration.py              # NUEVO
  tests/evals/
    test_rag_precision_q4.py              # NUEVO (Docker, 200+ queries)
  docs/arreglos chat/fase-3/
    README.md                              # MODIFICADO: + Q4
    q4-production/
      Q4-CLOSING-REPORT.md               # NUEVO
      Q4-DESIGN.md                        # NUEVO
      evidence/
        gates.md                           # NUEVO
```

## CRITERIOS DE EXITO Q4

Al finalizar, un juez deberia poder:

1. `docker compose up -d && python scripts/init_db.py` → PostgreSQL con pgvector corriendo, tablas creadas
2. `python scripts/run_ingestion.py --all` → 8 tramites ingestados con stats JSON
3. `python scripts/check_drift.py --all` → 8 procedures "current", reporte legible
4. `python scripts/check_boe.py --check --json` → lista de alertas BOE (puede ser vacia)
5. Hacer 5 queries iguales → 2da-5ta responden desde cache (latencia < 5ms)
6. Apagar Docker DB → queries siguen funcionando via JSON KB → Directory fallback
7. `curl -H "Authorization: Bearer $TOKEN" localhost:5000/admin/rag-metrics` → JSON con metricas
8. `python scripts/run_rag_eval.py` → precision@3 >= 0.90 sobre 200+ queries
9. `RAG_ENABLED=false pytest tests/` → todo sigue funcionando como antes
10. `RAG_ENABLED=true pytest tests/ --tb=short` → 519+ tests, 0 failures
11. Los 35 gates de calidad pasan (o DEFER documentado para los que requieren infra especifica)

---

## POST-Q4: AUDITORIA

Despues de ejecutar Q4, abrir una nueva sesion y ejecutar el auditor:

```
Lee el archivo docs/plans/AUDITOR-MULTIAGENTE.md y ejecuta todas las instrucciones que contiene.
```

Con esta CONFIGURACION:

```
QUARTER       = Q4
FASE          = fase-3
NOMBRE        = Production Hardening + Scale
SCOPE_DOCS    = docs/arreglos chat/fase-3/q4-production/
AUDIT_DIR     = docs/arreglos chat/fase-3/q4-production/audits
EVIDENCE_DIR  = docs/arreglos chat/fase-3/q4-production/evidence
VERSION       = v1
BASELINE_TESTS = 469
PREVIOUS_QUARTER_REPORT = docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md
```

---

**EMPIEZA AHORA. Crea el equipo `q4-production`, define las tareas empezando por Fase 0, y spawna los agentes. NO avanzar a Fase A sin completar Fase 0.**
