# Q3 — Evidence: Quality Gates

> **Snapshot:** Este documento refleja el estado del codigo al cierre de Q3 (2026-02-19). Cambios posteriores de Q4 pueden haber expandido sinonimos, queries de evaluacion, tests y scripts. Los numeros aqui son correctos para el momento del cierre Q3.

## Resumen

| Gate | Status | Evidencia |
|------|--------|-----------|
| G1 | PASS (offline) | expand_query("IMV") incluye "ingreso minimo vital" — BM25 encontrara match |
| G2 | PASS (offline) | expand_query("NIE") incluye "numero de identidad de extranjero" |
| G3 | PASS | reranker.py implementa _gemini_rerank con score 0-10 |
| G4 | PASS | _heuristic_rerank testado: section match + keyword overlap + original score |
| G5 | PASS | detect_territory("ayuda alquiler en Madrid") retorna {"ccaa": "madrid"} |
| G6 | PASS | _build_grounded_context produce [C1], [C2] con URLs |
| G7 | PASS (design) | System prompt rules 13-14 instruyen citacion [C1] |
| G8 | PASS (offline) | Pipeline completo implementado en retriever.py |
| G9 | DEFER | Precision@3 requiere Docker DB — test en tests/evals/test_rag_precision.py |
| G10 | DEFER | BM25 activation requiere Docker DB — test en tests/evals/test_rag_precision.py |
| G11 | PASS | 86 def test_ nuevos Q3 (83 passed + 3 skipped/Docker) |
| G12 | PASS | 347 passed + 5 xpassed + 11 skipped = 0 regression |
| G13 | PASS | ruff check 0 errores |

## G1: BM25 Activado

```
$ python -c "from src.core.rag.synonyms import expand_query; print(expand_query('IMV'))"
imv ingreso minimo vital
```

Antes de Q3: `search_hybrid("IMV")` retornaba bm25=0.0
Despues de Q3: query expandida a "imv ingreso minimo vital" → BM25 matcheara via tsvector Spanish config.

Verificacion DB-level requiere Docker (test en tests/evals/test_rag_precision.py).

## G2: Synonym Expansion

```
$ python -c "from src.core.rag.synonyms import expand_query; print(expand_query('NIE'))"
nie numero de identidad de extranjero
```

13 acronimos/sinonimos configurados en SYNONYMS dict.

## G3: Reranker Gemini

Implementado en `src/core/rag/reranker.py:_gemini_rerank()`:
- Usa Gemini Flash para puntuar relevancia 0-10
- Rate limiting (100 req/min compartido)
- Fallback a heuristic en caso de error

## G4: Reranker Heuristic

```
$ python -m pytest tests/unit/test_reranker.py -v --tb=short
12 passed
```

Scoring: section match (0-3) + keyword overlap (0-3) + original score (0-4) = max 10, normalizado a 0-1.

## G5: Territory Detection

```
$ python -c "from src.core.rag.territory import detect_territory; print(detect_territory('ayuda alquiler en Madrid'))"
{'nivel': 'municipal', 'ccaa': 'madrid', 'municipio': 'madrid'}
```

```
$ python -m pytest tests/unit/test_territory.py -v --tb=short
16 passed
```

## G6: Grounded Prompt

```
$ python -m pytest tests/unit/test_grounded_prompt.py -v --tb=short
13 passed
```

_build_grounded_context produce:
```
CHUNKS RECUPERADOS:
[C1] Seccion: requisitos | Tramite: age-imv | Score: 0.92
Contenido: Para solicitar el IMV necesitas...
Fuente: https://seg-social.es/imv
```

## G7: LLM con Citas

System prompt rules 13-14:
- "Basa tu respuesta EXCLUSIVAMENTE en el contenido de esos chunks."
- "Al final de cada parrafo relevante, indica la fuente entre corchetes: [C1]."

Verificacion end-to-end requiere LLM call (Gemini API).

## G8: Pipeline End-to-End

Pipeline completo en `PGVectorRetriever.retrieve()`:
1. detect_territory → 2. embed_text → 3. search_hybrid (con expand_query + territory filter) → 4. rerank → 5. build chunks_used → KBContext

```
$ python -m pytest tests/integration/test_retriever_rerank.py -v --tb=short
7 passed
```

## G9: Precision@3 >= 0.85

DEFERRED — requiere Docker PostgreSQL con datos migrados.
Test implementado: `tests/evals/test_rag_precision.py::test_precision_at_3_above_threshold`
Eval set: 65 queries (60 positivas + 5 negativas).

## G10: BM25 Activation >= 60%

DEFERRED — requiere Docker PostgreSQL.
Test implementado: `tests/evals/test_rag_precision.py::test_bm25_activation_rate`

## G11: >= 30 Tests Nuevos PASS

```
$ python -m pytest tests/unit/test_synonyms.py tests/unit/test_reranker.py tests/unit/test_territory.py tests/unit/test_grounded_prompt.py tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py tests/integration/test_rag_eval.py -v --tb=short
83 passed
```

Desglose: test_synonyms (15) + test_reranker (12) + test_territory (16) + test_grounded_prompt (13) + test_store_bm25 (9) + test_retriever_rerank (7) + test_rag_eval (11) + test_rag_precision (3 skipped) = 86 def test_ (83 passed, 3 skipped)
Metodo de conteo: `grep -c "def test_"` por archivo. Pytest result: 83 passed de esos archivos.

## G12: No Regresion

```
$ python -m pytest tests/ --tb=short -q
347 passed, 11 skipped, 5 xpassed, 1 warning in 4.20s
```

Antes de Q3: 264 passed + 5 xpassed = 269 definitions ejecutadas
Despues de Q3: 347 passed + 5 xpassed = 352 definitions ejecutadas
Delta: +83 tests nuevos, 0 rotos.

## G13: Lint Limpio

```
$ ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
All checks passed!
```
