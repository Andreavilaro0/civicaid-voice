# Fase 3 — RAG Universal de Tramites Espanoles

**Objetivo:** Construir un sistema RAG que permita a Clara responder sobre cualquier tramite gubernamental espanol, con fuentes oficiales verificadas.

## Estructura por Cuartos

| Quarter | Estado | Descripcion |
|---------|--------|-------------|
| **Q1** | CERRADO | Source-of-Truth: registros de fuentes, gobernanza de enlaces, diseno de pipeline de ingestion |
| **Q2** | **CERRADO** | PostgreSQL + pgvector storage layer, hybrid search, 8 tramites migrados |
| **Q3** | **CERRADO** | Retrieval hibrido + rerank + grounded prompting + territory detection + eval framework |
| **Q4** | **CERRADO** | Produccion: monitorizacion, frescura, fallback chain, eval expansion |

## Q1 — Source-of-Truth Layer

**Carpeta:** [`q1-sources/`](q1-sources/)

```
q1-sources/
  Q1-REPORT.md                          # Reporte consolidado
  source-registry/
    age.md                              # 25 fuentes AGE (ministerios, APIs)
    ccaa.md                             # 19/19 CCAA perfiladas
    local.md                            # Top 20 ciudades + estrategia 4 tiers
  link-governance/
    allowlist.md                        # Allowlist 3 tiers + blocklist
    canonicalization.md                 # 10 reglas de canonicalizacion
    link-checking-spec.md               # Health checker spec
  ingestion/
    ingestion-playbook.md               # Pipeline 6 etapas
    extraction-spec.md                  # Extraccion HTML/PDF/XML
    normalization-schema.md             # ProcedureDoc v1 schema
  backlog/
    Q1-backlog.md                       # Items Q1 completados + pendientes
    Q2Q3Q4-backlog.md                   # Roadmap Q2-Q4
  evidence/
    gates.md                            # 6/6 gates PASS, 4/4 abort cleared
    references.md                       # Fuentes consultadas
    assumptions-gaps.md                 # Supuestos + gaps + riesgos
```

**Metricas Q1:**
- 9 documentos de investigacion (4,448 lineas)
- 25 fuentes AGE catalogadas
- 19/19 CCAA perfiladas
- 20 sedes municipales verificadas
- 6/6 gates PASS
- 4/4 abort conditions cleared
- 0 lineas de codigo modificadas (research-only)

## Q1.1 — Biblioteca Oficial v0 (Machine-Readable Artifacts)

**Carpeta:** [`q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md`](q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md)

Convierte la investigacion Q1 en artefactos operativos:

| Artefacto | Path |
|-----------|------|
| Registry (44 sources) | `data/sources/registry.yaml` |
| Local seed (20 cities) | `data/sources/local_seed.yaml` |
| Allowlist | `data/policy/allowlist.yaml` |
| Blocklist | `data/policy/blocklist.yaml` |
| Canonical rules | `data/policy/canonical_rules.yaml` |
| SourceRegistry schema | `schemas/SourceRegistry.v1.schema.json` |
| ProcedureDoc schema | `schemas/ProcedureDoc.v1.schema.json` |
| Registry validator | `scripts/validate_source_registry.py` |
| Policy validator | `scripts/validate_policy.py` |
| ProcedureDoc validator | `scripts/validate_proceduredoc_schema.py` |
| Link checker | `scripts/link_check.py` |
| Unit tests | `tests/unit/test_validators.py` |

**Metricas Q1.1:**
- 64 fuentes totales (25 AGE + 19 CCAA + 20 local seed)
- 2 JSON Schemas (SourceRegistry + ProcedureDoc)
- 4 scripts de validacion
- 5 tests unitarios — 5/5 PASS
- 7/7 gates PASS, 4/4 abort conditions cleared

## Auditorias

| Audit | Fecha | Verdict | Ubicacion |
|-------|-------|---------|-----------|
| v4 | 2026-02-18 | CONDITIONAL | `q1-sources/audits/v4/` |
| v5 | 2026-02-18 | CONDITIONAL | `q1-sources/audits/v5/` |
| v6 | 2026-02-19 | FULL PASS | [`q1-sources/audits/v6/`](q1-sources/audits/v6/) |
| **q1-final** | **2026-02-19** | **FULL PASS** | [`q1-sources/audits/q1-final/`](q1-sources/audits/q1-final/) |

**Q1 = CERRADA (FULL PASS)** — ver [Q1-FINAL-STATUS.md](q1-sources/audits/q1-final/Q1-FINAL-STATUS.md)

### Auditorias Q2

| Audit | Fecha | Verdict | Ubicacion |
|-------|-------|---------|-----------|
| **q2-v1** | **2026-02-19** | **FULL PASS** | [`q2-storage/audits/v1/`](q2-storage/audits/v1/) |

**Q2 Audit:** 55 claims checked, 10 DRIFTs found + fixed, 12 red-team vectors (7 PASS, 3 NOTE, 2 FAIL→fixed). Ver [Q2-FINAL-STATUS.v1.md](q2-storage/audits/v1/Q2-FINAL-STATUS.v1.md)

### Auditorias Q3

| Audit | Fecha | Verdict | Ubicacion |
|-------|-------|---------|-----------|
| q3-v0 | 2026-02-19 | CONDITIONAL PASS | `q3-retrieval/audits/v1/` (initial) |
| **q3-v1 (re-audit)** | **2026-02-20** | **FULL PASS** | [`q3-retrieval/audits/v1/`](q3-retrieval/audits/v1/) |

**Q3 Re-Audit (v1):** 69 claims checked, 18 DRIFTs (all Q4-stale, addressed via Snapshot headers), 15 red-team vectors (10 PASS, 5 NOTE, 0 FAIL). 7 lint errors fixed, 1 defense-in-depth added. Ver [FINAL-STATUS.md](q3-retrieval/audits/v1/FINAL-STATUS.md)

## Q2 — Modelo de Datos + Storage (PG/Vec)

**Carpeta:** [`q2-storage/`](q2-storage/)

```
q2-storage/
  Q2-CLOSING-REPORT.md                  # Reporte final (FULL PASS 11/11)
  Q2-DESIGN.md                          # Decisiones de arquitectura
  evidence/
    gates.md                            # 11 gates con evidencia
    GROUND-TRUTH.v1.txt                 # Ground truth programatico
    COMMANDS-AND-OUTPUTS.v1.log         # Gate execution log
  audits/v1/
    Q2-FINAL-STATUS.v1.md              # Verdict final: FULL PASS
    DRIFT-CHECK.v1.md                  # 55 claims verificadas
    RED-TEAM-REPORT.v1.md              # 12 vectores adversariales
    FIXES-APPLIED.v1.md                # 7 correcciones aplicadas
```

**Implementacion:**

| Componente | Path |
|------------|------|
| Docker compose (PG16 + pgvector) | `docker-compose.yml` |
| SQLAlchemy models (4 tablas) | `src/core/rag/models.py` |
| Database engine + session | `src/core/rag/database.py` |
| Section-based chunker | `src/core/rag/chunker.py` |
| Gemini embedding wrapper | `src/core/rag/embedder.py` |
| PGVectorStore (hybrid search) | `src/core/rag/store.py` |
| JSON -> PG migrator | `src/core/rag/migrator.py` |
| PGVectorRetriever | `src/core/retriever.py` |
| DB init script | `scripts/init_db.py` |
| 8 RAG config flags | `src/core/config.py` |

**Metricas Q2:**
- 8/8 tramites migrados (20 chunks, 3,879 palabras)
- 80 tests RAG nuevos (72 unit + 8 integration) — 277 collected total (264 passed, 8 skipped, 5 xpassed)
- 11/11 gates PASS
- 0 errores lint
- pipeline.py NO tocado (integracion transparente via retriever.py)

**Q2 = CERRADA (FULL PASS)** — ver [Q2-CLOSING-REPORT.md](q2-storage/Q2-CLOSING-REPORT.md)

## Q3 — Retrieval Hibrido + Rerank + Prompting Grounded

**Carpeta:** [`q3-retrieval/`](q3-retrieval/)

```
q3-retrieval/
  Q3-CLOSING-REPORT.md                  # Reporte final (11/13 PASS, 2 DEFERRED)
  Q3-DESIGN.md                          # Decisiones de arquitectura (D1-D6)
  evidence/
    gates.md                            # 13 gates con evidencia
    GROUND-TRUTH.v1.txt                 # Ground truth programatico
    COMMANDS-AND-OUTPUTS.v1.log         # Gate execution log
    GATES-POSTFIX.v1.log                # Post-fix gate verification
  audits/v1/
    FINAL-STATUS.md                     # Verdict final: FULL PASS
    DRIFT-CHECK.v1.md                   # 66 claims verificadas
    RED-TEAM-REPORT.v1.md               # 15 vectores adversariales
    FIXES-APPLIED.v1.md                 # 3 P0 security fixes
```

**Implementacion:**

| Componente | Path |
|------------|------|
| Synonym expansion (13 acronimos) | `src/core/rag/synonyms.py` |
| Gemini + heuristic reranker | `src/core/rag/reranker.py` |
| Territory detection (17 CCAA + 60 cities) | `src/core/rag/territory.py` |
| RAG eval framework | `src/utils/rag_eval.py` |
| Eval CLI runner | `scripts/run_rag_eval.py` |
| Eval set (65 queries) | `data/evals/rag_eval_set.json` |
| +3 config flags | `src/core/config.py` |
| Pipeline completo | `src/core/retriever.py` |
| Grounded prompting | `src/core/skills/llm_generate.py` + `src/core/prompts/system_prompt.py` |

**Tests Q3:**

| Archivo | Tests |
|---------|-------|
| tests/unit/test_synonyms.py | 15 |
| tests/unit/test_reranker.py | 12 |
| tests/unit/test_territory.py | 16 |
| tests/unit/test_grounded_prompt.py | 13 |
| tests/unit/test_store_bm25.py | 9 |
| tests/integration/test_retriever_rerank.py | 7 |
| tests/integration/test_rag_eval.py | 11 |
| tests/evals/test_rag_precision.py | 3 (skip sin Docker) |
| **Total** | **83 + 3** |

**Metricas Q3:**
- 83 tests nuevos Q3 — todos PASS (+ 3 evals skip sin Docker)
- Total suite: 347 passed + 5 xpassed + 11 skipped = 0 regresion
- 65 queries en eval set (9 categorias, 8 tramites AGE)
- 3 feature flags nuevos (RAG_RERANK_STRATEGY, RAG_GROUNDED_PROMPTING, RAG_MAX_CHUNKS_IN_PROMPT)
- 11/13 gates PASS (2 DEFERRED: G9 Precision@3, G10 BM25 activation — requieren Docker)
- 0 errores lint

**Q3 = CERRADO (FULL PASS)** — ver [Q3-CLOSING-REPORT.md](q3-retrieval/Q3-CLOSING-REPORT.md) | Audit: [FINAL-STATUS.md](q3-retrieval/audits/v1/FINAL-STATUS.md)

## Q4 — Production Hardening + Scale

**Carpeta:** [`q4-production/`](q4-production/)

```
q4-production/
  Q4-CLOSING-REPORT.md                  # Reporte final (24 PASS, 2 CONDITIONAL)
  Q4-DESIGN.md                          # Decisiones de arquitectura (D1-D7)
  evidence/
    gates.md                            # 26 gates con evidencia
    COMMANDS-AND-OUTPUTS.v1.log         # Gate execution log
```

**Implementacion:**

| Componente | Path |
|------------|------|
| Pipeline integration (get_retriever) | `src/core/pipeline.py` (2 lineas) |
| Singleton get_retriever() | `src/core/retriever.py` |
| FallbackRetriever (PGVector->JSON->Directory) | `src/core/retriever.py` |
| Ingestion pipeline | `src/core/rag/ingestion.py` (269 LOC) |
| Drift detection | `src/core/rag/drift.py` (216 LOC) |
| Response cache (memory/Redis) | `src/core/rag/response_cache.py` (216 LOC) |
| BOE monitor | `src/core/rag/boe_monitor.py` (201 LOC) |
| Directory fallback retriever | `src/core/rag/directory.py` (98 LOC) |
| RAG metrics | `src/utils/rag_metrics.py` (185 LOC) |
| Admin endpoints | `src/routes/admin.py` (67 LOC) |
| Ingestion CLI runner | `scripts/run_ingestion.py` |
| Drift check CLI runner | `scripts/check_drift.py` |
| BOE monitor CLI runner | `scripts/check_boe.py` |
| Eval set expanded (236 queries) | `data/evals/rag_eval_set.json` |
| 12 Q4 config flags | `src/core/config.py` |

**Tests Q4:**

| Archivo | Tests |
|---------|-------|
| tests/unit/test_ingestion.py | ~15 |
| tests/unit/test_drift.py | ~12 |
| tests/unit/test_boe_monitor.py | ~10 |
| tests/unit/test_admin.py | ~15 |
| tests/unit/test_rag_metrics.py | ~10 |
| tests/unit/test_response_cache.py | ~15 |
| tests/unit/test_directory.py | ~10 |
| tests/unit/test_fallback_retriever.py | ~15 |
| tests/integration/test_fallback_chain.py | ~10 |
| tests/integration/test_admin_integration.py | ~8 |
| tests/integration/test_ingestion_pipeline.py | ~8 |
| tests/integration/test_drift_pipeline.py | ~8 |
| tests/evals/test_rag_precision_q4.py | ~5 |
| **Total** | **150+** |

**Metricas Q4:**
- 150+ tests nuevos Q4 — todos PASS
- Total suite: 493 passed + 5 xpassed + 19 skipped = 0 regresion
- 236 queries en eval set (up from 65 in Q3)
- P@3 = 86.02%, P@1 = 74.15%, MRR = 79.52%, BM25 = 100%
- 12 feature flags nuevos
- 24/26 gates PASS (2 CONDITIONAL: P@3 vs aspirational 0.90, P@1/MRR close to targets)
- 0 errores lint
- 2 SHOWSTOPPERS arreglados (pipeline integration + singleton)

**Q4 = CERRADO** — ver [Q4-CLOSING-REPORT.md](q4-production/Q4-CLOSING-REPORT.md) | Design: [Q4-DESIGN.md](q4-production/Q4-DESIGN.md)
