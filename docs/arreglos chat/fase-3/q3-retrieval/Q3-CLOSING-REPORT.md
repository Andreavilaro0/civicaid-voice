# Q3 — Retrieval Hibrido + Rerank + Prompting Grounded: Closing Report

> **Snapshot:** Este documento refleja el estado del codigo al cierre de Q3 (2026-02-19). Cambios posteriores de Q4 pueden haber expandido sinonimos, queries de evaluacion, tests y scripts. Los numeros aqui son correctos para el momento del cierre Q3.

**Estado**: CERRADO
**Fecha**: 2026-02-19
**Duracion**: 1 sesion
**Predecessor**: Q2 Storage Layer (CERRADO, FULL PASS 11/11 gates)

## Resumen Ejecutivo

Q3 implementa la capa de retrieval inteligente sobre la infraestructura de storage de Q2:

1. **BM25 arreglado** — Expansion de sinonimos/acronimos para tramites espanoles (13 entradas). `search_hybrid("IMV")` ahora busca "imv ingreso minimo vital"
2. **Reranking dual** — Gemini Flash (cross-encoder) + heuristic (section match + keywords). Configurable via `RAG_RERANK_STRATEGY`
3. **Grounded prompting** — Respuestas con citas [C1], [C2] y URLs oficiales. System prompt instruye exclusividad de chunks
4. **Territory detection** — 17 CCAA + 60+ ciudades. Pre-filtro SQL por territorio en metadata
5. **Pipeline integrado** — territory → embed → hybrid search → rerank → grounded context → KBContext
6. **Eval framework** — 65 queries, precision/MRR/BM25 metrics, CLI runner
7. **86 tests nuevos** (83 passed + 3 skipped/Docker) — 0 regresion sobre 264 existentes. Total: 347 passed
8. **Backward compatible** — 3 feature flags, todo detras de `RAG_ENABLED`

## Entregables

### Modulos Nuevos (5)
| Archivo | LOC | Funcion |
|---------|-----|---------|
| `src/core/rag/synonyms.py` | 72 | Expansion acronimos/sinonimos BM25 |
| `src/core/rag/reranker.py` | 196 | Gemini + heuristic reranking |
| `src/core/rag/territory.py` | ~228 | Deteccion CCAA/municipio en queries |
| `src/utils/rag_eval.py` | ~115 | Framework evaluacion RAG |
| `scripts/run_rag_eval.py` | ~102 | CLI runner evaluacion |

### Modulos Modificados (6)
| Archivo | Cambios |
|---------|---------|
| `src/core/config.py` | +3 flags Q3 |
| `src/core/models.py` | +chunks_used en KBContext |
| `src/core/rag/store.py` | +expand_query, +territory_filter |
| `src/core/retriever.py` | Pipeline completo Q3 |
| `src/core/prompts/system_prompt.py` | +rules 13-14, +chunks_block |
| `src/core/skills/llm_generate.py` | +_build_grounded_context |

### Tests Nuevos (8 archivos, 86 def test_ — 83 passed, 3 skipped)
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

### Datos
| Archivo | Contenido |
|---------|-----------|
| data/evals/rag_eval_set.json | 65 queries, 9 categorias, 8 tramites |

## Feature Flags

| Flag | Default | Opciones |
|------|---------|----------|
| `RAG_RERANK_STRATEGY` | `"heuristic"` | `"gemini"`, `"heuristic"`, `"none"` |
| `RAG_GROUNDED_PROMPTING` | `true` | `true`, `false` |
| `RAG_MAX_CHUNKS_IN_PROMPT` | `4` | 1-8 |

## Quality Gates

| # | Gate | Status |
|---|------|--------|
| G1 | BM25 activado para acronimos | PASS (offline) |
| G2 | Synonym expansion funciona | PASS |
| G3 | Reranker Gemini implementado | PASS |
| G4 | Reranker heuristic funciona | PASS |
| G5 | Territory detection funciona | PASS |
| G6 | Grounded prompt con [C1] | PASS |
| G7 | System prompt con reglas citacion | PASS |
| G8 | Pipeline end-to-end | PASS |
| G9 | Precision@3 >= 0.85 | DEFERRED (Docker) |
| G10 | BM25 activation >= 60% | DEFERRED (Docker) |
| G11 | >= 30 tests nuevos | PASS (86 def test_, 83 passed) |
| G12 | No regresion | PASS (347+5) |
| G13 | Lint limpio | PASS |

**Resultado**: 11/13 PASS, 2 DEFERRED (requieren Docker DB con datos migrados).
Los 2 deferred tienen tests implementados que se ejecutan automaticamente cuando Docker esta disponible.

## Abort Conditions

| ID | Condicion | Status |
|----|-----------|--------|
| A1 | Gemini reranker rate limit | No activada — default puesto en "heuristic" |
| A2 | BM25 no se arregla | No activada — synonym expansion resuelve |
| A3 | Grounded prompting reduce calidad | No activada — implementado con fallback |
| A4 | Tests existentes rompen | No activada — 0 regresion |
| A5 | Precision@3 < 0.85 | Pendiente verificacion con Docker |

## Metricas

| Metrica | Valor |
|---------|-------|
| Tests totales suite | 347 passed + 5 xpassed + 11 skipped |
| Tests nuevos Q3 (def test_) | 86 (83 passed + 3 skipped) |
| Archivos nuevos | 8 (5 src + 3 data/scripts) |
| Archivos modificados | 6 src |
| LOC nuevas | ~730 |
| Eval queries | 65 |
| Feature flags | 3 |
| Regresiones | 0 |

## Roadmap Q4

1. **Docker verification**: Ejecutar G9/G10 con DB poblada
2. **CCAA/Municipal tramites**: Agregar tramites no-AGE para activar territory filter
3. **Gemini SDK migration**: `google.generativeai` → `google.genai` (FutureWarning)
4. **Fine-tune reranker prompt**: Optimizar prompt de relevancia para dominio espanol
5. **A/B testing grounded vs classic**: Comparar calidad de respuestas
