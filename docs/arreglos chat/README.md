# Arreglos Chat — Registro de Auditorias e Implementaciones

> Carpeta organizada con todos los reportes, evidencia y backlog generados durante las sesiones de trabajo con Claude Code sobre el proyecto Clara / CivicAid Voice.

## Estado Actual

| Fase | Estado | Descripcion |
|------|--------|-------------|
| **Fase 1** | CERRADA | Estabilizacion + salida de demo + calidad percibida |
| **Fase 2** | CERRADA | Memoria + personalizacion por usuario + continuidad multi-turn |
| **Fase 3 Q1** | CERRADA | RAG Source-of-Truth: registros de fuentes AGE/CCAA/Local + gobernanza de enlaces + pipeline de ingestion (solo investigacion) |
| **Fase 3 Q1.1** | CERRADA | Biblioteca Oficial v0: artefactos machine-readable (YAML/JSON), schemas, validators, link checker |
| **Fase 3 Q2** | CERRADA | RAG: PostgreSQL + pgvector storage layer, hybrid search, 8 tramites migrados |
| **Fase 3 Q3** | CERRADA | RAG: Retrieval hibrido + rerank + grounded prompting + territory detection + eval framework |
| **Fase 3 Q4** | **CERRADA** | RAG: produccion, monitorizacion, fallback chain, eval expansion |

## Indice por Fases

### [Fase 1](fase-1/) — Estabilizacion + Salida de Demo

| Documento | Descripcion |
|-----------|-------------|
| [FASE1-CLOSING-REPORT.md](fase-1/FASE1-CLOSING-REPORT.md) | Reporte de cierre: resumen ejecutivo, gates before/after, tickets, cambios, flags, riesgos |
| [AUDIT-REPORT-FASE1-VALIDADO.md](fase-1/AUDIT-REPORT-FASE1-VALIDADO.md) | Auditoria tecnica completa validada contra codigo fuente |
| [backlog.md](fase-1/backlog.md) | Tickets pendientes post-Fase 1 con priorizacion |
| [evidence/gates.md](fase-1/evidence/gates.md) | Gates de calidad con comandos reproducibles |
| [evidence/prod-validation.md](fase-1/evidence/prod-validation.md) | Guia de verificacion en produccion (Render) |
| [evidence/commands-output/](fase-1/evidence/commands-output/) | Salidas capturadas de pytest y ruff |

### [Fase 2](fase-2/) — Memoria + Personalizacion

| Documento | Descripcion |
|-----------|-------------|
| [FASE2-CLOSING-REPORT.md](fase-2/FASE2-CLOSING-REPORT.md) | Reporte de cierre: resumen, gates, abort conditions, cambios |
| [FASE2-DESIGN.md](fase-2/FASE2-DESIGN.md) | Decisiones de arquitectura: backends, hashing, sanitizacion |
| [FASE2-IMPLEMENTATION.md](fase-2/FASE2-IMPLEMENTATION.md) | Log de implementacion por ticket (MEM-01 a MEM-15) |
| [backlog.md](fase-2/backlog.md) | Tickets pendientes post-Fase 2 |
| [evidence/gates.md](fase-2/evidence/gates.md) | Gates de calidad con abort conditions |
| [evidence/prod-validation.md](fase-2/evidence/prod-validation.md) | Guia de verificacion en produccion |
| [evidence/commands-output/](fase-2/evidence/commands-output/) | Salidas capturadas (pytest, ruff — baseline y final) |

### [Fase 3 Q1](fase-3/q1-sources/) — RAG Source-of-Truth Layer (Research)

| Documento | Descripcion |
|-----------|-------------|
| [Q1-REPORT.md](fase-3/q1-sources/Q1-REPORT.md) | Reporte consolidado: resumen ejecutivo, registros, gobernanza, pipeline, gates |
| [source-registry/age.md](fase-3/q1-sources/source-registry/age.md) | Registro de 25 fuentes AGE (ministerios, sedes electronicas, APIs) |
| [source-registry/ccaa.md](fase-3/q1-sources/source-registry/ccaa.md) | Registro de 19/19 CCAA con URLs, prioridades y procedimientos |
| [source-registry/local.md](fase-3/q1-sources/source-registry/local.md) | Estrategia municipal: top 20 ciudades + 4 tiers + desambiguacion |
| [link-governance/allowlist.md](fase-3/q1-sources/link-governance/allowlist.md) | Allowlist de dominios (3 tiers) + blocklist |
| [link-governance/canonicalization.md](fase-3/q1-sources/link-governance/canonicalization.md) | Politica de canonicalizacion de URLs (10 reglas) |
| [link-governance/link-checking-spec.md](fase-3/q1-sources/link-governance/link-checking-spec.md) | Especificacion del health checker de enlaces |
| [ingestion/ingestion-playbook.md](fase-3/q1-sources/ingestion/ingestion-playbook.md) | Pipeline de ingestion: 6 etapas (discovery a index) |
| [ingestion/extraction-spec.md](fase-3/q1-sources/ingestion/extraction-spec.md) | Especificacion de extraccion: HTML, PDF, BOE XML, formularios |
| [ingestion/normalization-schema.md](fase-3/q1-sources/ingestion/normalization-schema.md) | Schema ProcedureDoc v1 (29 campos) + migracion desde KB actual |
| [backlog/Q1-backlog.md](fase-3/q1-sources/backlog/Q1-backlog.md) | Items completados y pendientes Q1 |
| [backlog/Q2Q3Q4-backlog.md](fase-3/q1-sources/backlog/Q2Q3Q4-backlog.md) | Roadmap Q2-Q4: ingestion, vectores, cobertura, produccion |
| [evidence/gates.md](fase-3/q1-sources/evidence/gates.md) | 6 gates + 4 abort conditions — todos PASS |
| [evidence/references.md](fase-3/q1-sources/evidence/references.md) | Fuentes consultadas (leyes, portales, APIs) |
| [evidence/assumptions-gaps.md](fase-3/q1-sources/evidence/assumptions-gaps.md) | 10 supuestos + 13 gaps + registro de riesgos |

### [Fase 3 Q1.1](fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md) — Biblioteca Oficial v0

| Documento | Descripcion |
|-----------|-------------|
| [Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md](fase-3/q1-sources/Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md) | Reporte: 64 fuentes, 2 schemas, 4 scripts, 6/6 gates |
| `data/sources/registry.yaml` | 44 fuentes AGE+CCAA machine-readable |
| `data/sources/local_seed.yaml` | 20 sedes municipales + tier strategy |
| `data/policy/allowlist.yaml` | Allowlist de dominios (3 tiers) |
| `data/policy/blocklist.yaml` | Dominios bloqueados |
| `data/policy/canonical_rules.yaml` | 12-step URL canonicalization |
| `schemas/SourceRegistry.v1.schema.json` | JSON Schema para registry |
| `schemas/ProcedureDoc.v1.schema.json` | JSON Schema para ProcedureDoc v1 |
| `scripts/validate_source_registry.py` | Validador de registros |
| `scripts/validate_policy.py` | Validador de politicas |
| `scripts/validate_proceduredoc_schema.py` | Validador de ProcedureDoc |
| `scripts/link_check.py` | Health checker de enlaces (skeleton) |
| `tests/unit/test_validators.py` | 5 tests unitarios — 5/5 PASS |

### Auditorias Q1

| Documento | Descripcion |
|-----------|-------------|
| [audits/q1-final/Q1-FINAL-STATUS.md](fase-3/q1-sources/audits/q1-final/Q1-FINAL-STATUS.md) | **FULL PASS** — Verdict final, 7/7 gates, 0 drift, 10/10 red team vectors |
| [audits/q1-final/GATES-RESULTS.final.md](fase-3/q1-sources/audits/q1-final/GATES-RESULTS.final.md) | Gates con output verbatim |
| [audits/q1-final/GROUND-TRUTH.final.txt](fase-3/q1-sources/audits/q1-final/GROUND-TRUTH.final.txt) | Ground truth programatico |
| [audits/q1-final/RED-TEAM-REPORT.final.md](fase-3/q1-sources/audits/q1-final/RED-TEAM-REPORT.final.md) | Red team: 9 PASS + 1 NOTE |
| [audits/v6/](fase-3/q1-sources/audits/v6/) | Audit v6 (pre-final) |

### [Fase 3 Q2](fase-3/q2-storage/) — Modelo de Datos + Storage (PG/Vec)

| Documento | Descripcion |
|-----------|-------------|
| [Q2-CLOSING-REPORT.md](fase-3/q2-storage/Q2-CLOSING-REPORT.md) | Reporte de cierre: FULL PASS 11/11 gates |
| [Q2-DESIGN.md](fase-3/q2-storage/Q2-DESIGN.md) | Decisiones de arquitectura: pgvector, chunking, hybrid search |
| [evidence/gates.md](fase-3/q2-storage/evidence/gates.md) | 11 gates con output verbatim |
| `docker-compose.yml` | pgvector/pgvector:pg16, port 5432 |
| `src/core/rag/models.py` | 4 tablas SQLAlchemy (procedure_docs, chunks, sources, ingestion_log) |
| `src/core/rag/chunker.py` | Section-based structured chunking |
| `src/core/rag/embedder.py` | Gemini gemini-embedding-001 (768 dims) |
| `src/core/rag/store.py` | PGVectorStore (hybrid BM25 + vector search) |
| `src/core/rag/migrator.py` | JSON -> PostgreSQL migration (8 tramites, 20 chunks) |
| `src/core/retriever.py` | PGVectorRetriever (RAG_ENABLED=true -> hybrid search) |

### [Fase 3 Q3](fase-3/q3-retrieval/) — Retrieval Hibrido + Rerank + Grounded Prompting

| Documento | Descripcion |
|-----------|-------------|
| [Q3-CLOSING-REPORT.md](fase-3/q3-retrieval/Q3-CLOSING-REPORT.md) | Reporte de cierre: 11/13 PASS (2 DEFERRED Docker) |
| [Q3-DESIGN.md](fase-3/q3-retrieval/Q3-DESIGN.md) | Decisiones de arquitectura: D1-D6 |
| [evidence/gates.md](fase-3/q3-retrieval/evidence/gates.md) | 13 gates con evidencia |
| `src/core/rag/synonyms.py` | Expansion de 13 acronimos/sinonimos espanoles |
| `src/core/rag/reranker.py` | Gemini Flash + heuristic reranking |
| `src/core/rag/territory.py` | Deteccion de 17 CCAA + 60+ ciudades |
| `src/utils/rag_eval.py` | Framework de evaluacion (precision, MRR, BM25) |
| `scripts/run_rag_eval.py` | CLI runner para evaluacion |
| `data/evals/rag_eval_set.json` | 65 queries (9 categorias, 8 tramites) |

### Auditorias Q3

| Documento | Descripcion |
|-----------|-------------|
| [FINAL-STATUS.md](fase-3/q3-retrieval/audits/v1/FINAL-STATUS.md) | **FULL PASS** (re-audit 2026-02-20) — 69 claims, 18 DRIFTs (Q4-stale, addressed), 0 FAIL |
| [DRIFT-CHECK.v1.md](fase-3/q3-retrieval/audits/v1/DRIFT-CHECK.v1.md) | 69 claims verificadas claim-by-claim |
| [RED-TEAM-REPORT.v1.md](fase-3/q3-retrieval/audits/v1/RED-TEAM-REPORT.v1.md) | 15 vectores adversariales: 10 PASS, 5 NOTE, 0 FAIL |
| [FIXES-APPLIED.v1.md](fase-3/q3-retrieval/audits/v1/FIXES-APPLIED.v1.md) | 7 lint fixes + 3 snapshot headers + 1 defense-in-depth |
| [GATES-POSTFIX.v1.log](fase-3/q3-retrieval/evidence/GATES-POSTFIX.v1.log) | Post-fix gate verification |

### [Fase 3 Q4](fase-3/q4-production/) — Production Hardening + Scale

| Documento | Descripcion |
|-----------|-------------|
| [Q4-CLOSING-REPORT.md](fase-3/q4-production/Q4-CLOSING-REPORT.md) | Reporte de cierre: 24 PASS, 2 CONDITIONAL, 0 FAIL |
| [Q4-DESIGN.md](fase-3/q4-production/Q4-DESIGN.md) | Decisiones de arquitectura: D1-D7 (pipeline, singleton, fallback, cache, scripts, eval, metrics) |
| [evidence/gates.md](fase-3/q4-production/evidence/gates.md) | 26 gates con evidencia |
| `scripts/run_ingestion.py` | CLI ingestion runner (--all, --dry-run, --force) |
| `scripts/check_drift.py` | CLI drift detection runner (--all, --stale, --json) |
| `scripts/check_boe.py` | CLI BOE monitor runner (--check, --json) |
| `src/core/rag/ingestion.py` | Ingestion pipeline (269 LOC) |
| `src/core/rag/drift.py` | Drift detection (216 LOC) |
| `src/core/rag/response_cache.py` | Response cache memory/Redis (216 LOC) |
| `src/core/rag/boe_monitor.py` | BOE RSS monitor (201 LOC) |
| `src/core/rag/directory.py` | Directory fallback retriever (98 LOC) |
| `src/utils/rag_metrics.py` | RAG metrics recording (185 LOC) |
| `src/routes/admin.py` | Admin endpoints: rag-metrics, staleness, satisfaction |
| `data/evals/rag_eval_set.json` | 236 eval queries (up from 65 in Q3) |

**Key changes:** Pipeline integration (`get_retriever()` in pipeline.py), singleton pattern, FallbackRetriever chain, 12 Q4 config flags, 150+ new tests, P@3=86.02% on 236 queries

## Convenciones

### Estructura por fase
```
fase-N/
  FASE{N}-CLOSING-REPORT.md    # Reporte de cierre (obligatorio)
  AUDIT-REPORT-*.md             # Auditoria si aplica
  backlog.md                    # Tickets pendientes al cerrar
  evidence/
    gates.md                    # Gates de calidad verificados
    prod-validation.md          # Verificacion en produccion
    commands-output/            # Salidas capturadas (pytest, ruff, etc.)
```

### Nombrado
- Reportes: `FASE{N}-CLOSING-REPORT.md` (siempre en mayusculas)
- Evidencia: minusculas con guiones (`gates.md`, `prod-validation.md`)
- Salidas de comandos: nombre del comando + sufijo (`pytest-full.txt`, `ruff-check.txt`)

### Como agregar una nueva fase
1. Crear carpeta `fase-N/` con la estructura de arriba
2. Agregar entrada en la tabla "Estado Actual" de este README
3. Agregar seccion en "Indice por Fases"
4. Al cerrar la fase, asegurarse de que tenga: closing report + gates + backlog

## Contexto del Proyecto

- **Proyecto:** Clara — asistente WhatsApp-first para personas vulnerables en Espana
- **Hackathon:** OdiseIA4Good — UDIT (Feb 2026)
- **Stack:** Python 3.11, Flask, Twilio WhatsApp, Gemini 1.5 Flash, Docker, Render
- **Repo:** civicaid-voice
