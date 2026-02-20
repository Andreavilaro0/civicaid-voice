# Q3 — Retrieval Hibrido + Rerank + Prompting Grounded: Decisiones de Arquitectura

> **Snapshot:** Este documento refleja el estado del codigo al cierre de Q3 (2026-02-19). Cambios posteriores de Q4 pueden haber expandido sinonimos, queries de evaluacion, tests y scripts. Los numeros aqui son correctos para el momento del cierre Q3.

## Objetivo

Mejorar la calidad del retrieval y la generacion de Clara para que:
1. Encuentre chunks correctos con precision@3 >= 0.85
2. Re-rankee resultados con cross-encoder
3. Genere respuestas grounded con citas [C1], [C2]
4. Maneje consultas territoriales
5. Framework de evaluacion reproducible con 65 queries

## Decisiones de Arquitectura

### D1. Synonym Expansion para BM25

**Problema**: BM25 retornaba `score=0.0` para acronimos espanoles (IMV, NIE, SEPE) porque `plainto_tsquery('spanish', 'IMV')` no matchea `to_tsvector('spanish', 'ingreso minimo vital')`.

**Solucion**: `src/core/rag/synonyms.py` con diccionario de 13 acronimos/sinonimos. `expand_query()` se llama antes del SQL en `search_hybrid()`.

**Trade-off**: Diccionario manual vs. NLP automatico. Elegimos manual porque:
- Lista finita de tramites (< 50 en v1)
- Control total sobre expansiones
- Sin dependencia externa
- Mantenible por personas no-tecnicas

### D2. Dual Reranking Strategy

**Solucion**: `src/core/rag/reranker.py` con dos estrategias configurable via `RAG_RERANK_STRATEGY`:
- `"gemini"` (alta precision, mayor latencia): Gemini Flash puntua relevancia 0-10 por chunk
- `"heuristic"` (default en produccion): Section match + keyword overlap + original score
- `"none"`: Sin reranking (comportamiento Q2)

**Trade-off**: Gemini reranker es mas preciso pero:
- 1 API call por chunk (top_k = 5 -> 5 calls)
- Rate limit compartido con embedder (100 req/min)
- Latencia adicional (~200ms por call)
- Default en produccion: `"heuristic"` para latencia predecible

### D3. Grounded Prompting con Chunks Numerados

**Solucion**: System prompt incluye bloque `CHUNKS RECUPERADOS` con [C1], [C2], etc. Cada chunk tiene seccion, tramite, score, contenido y fuente URL.

**Reglas de citacion** (rules 13-14 en system_prompt.py):
- Basar respuesta exclusivamente en chunks
- Indicar fuente [C1] al final de cada parrafo
- Si ningun chunk responde, decir "No tengo esa informacion verificada"
- No mezclar informacion de distintos tramites

**Config**: `RAG_GROUNDED_PROMPTING=true` (activado), `RAG_MAX_CHUNKS_IN_PROMPT=4`

### D4. Territory Detection

**Solucion**: `src/core/rag/territory.py` con mapas de CCAA (17) y ciudades (60+).

**Algoritmo de 3 fases**:
1. Patron "en <territorio>" (alta confianza)
2. N-grams (2-4 palabras) contra CITY_MAP y CCAA_MAP
3. Palabra individual

**Pre-filtro SQL**: Chunks con `metadata->>'territorio_ccaa'` o `metadata->>'territorio_municipio'` matching.

**Nota**: Los 8 tramites actuales son AGE (nivel estatal), asi que el filtro no tiene efecto inmediato. La infraestructura esta lista para tramites CCAA/municipales en Q4.

### D5. Pipeline Integrado en Retriever

**Flujo completo** en `PGVectorRetriever.retrieve()`:
1. `detect_territory(query)` - detectar territorio
2. `embed_text(query)` - generar embedding
3. `store.search_hybrid(query, embedding, territory_filter)` - busqueda hibrida con sinonimos
4. `rerank(query, results, strategy)` - re-ranking
5. `_build_datos()` + `chunks_used` - construir contexto grounded
6. Retornar `KBContext` con chunks poblados

### D6. Feature Flags (Backward Compatible)

| Flag | Default | Efecto |
|------|---------|--------|
| `RAG_RERANK_STRATEGY` | `"heuristic"` | Estrategia de reranking |
| `RAG_GROUNDED_PROMPTING` | `true` | Chunks con citacion en prompt |
| `RAG_MAX_CHUNKS_IN_PROMPT` | `4` | Max chunks en prompt |

**Compatibilidad**:
- `RAG_ENABLED=false` → JSONKBRetriever (sin cambios)
- `RAG_RERANK_STRATEGY="none"` → Sin reranking (Q2)
- `RAG_GROUNDED_PROMPTING=false` → Prompt clasico

## Modulos Nuevos

| Modulo | LOC | Funcion |
|--------|-----|---------|
| `src/core/rag/synonyms.py` | 72 | Expansion de acronimos/sinonimos |
| `src/core/rag/reranker.py` | 196 | Gemini + heuristic reranking |
| `src/core/rag/territory.py` | 226 | Deteccion de territorio |
| `src/utils/rag_eval.py` | 116 | Framework de evaluacion |
| `scripts/run_rag_eval.py` | ~102 | CLI runner evaluacion |

## Modulos Modificados

| Modulo | Cambios |
|--------|---------|
| `src/core/config.py` | +3 flags (RAG_RERANK_STRATEGY, RAG_GROUNDED_PROMPTING, RAG_MAX_CHUNKS_IN_PROMPT) |
| `src/core/models.py` | +chunks_used field en KBContext |
| `src/core/rag/store.py` | +expand_query en search_hybrid, +territory_filter param |
| `src/core/retriever.py` | Pipeline completo: territory → search → rerank → grounded context |
| `src/core/prompts/system_prompt.py` | +reglas 13-14, +{chunks_block} placeholder |
| `src/core/skills/llm_generate.py` | +_build_grounded_context(), chunks_block en prompt |

## Eval Set

- 65 queries en `data/evals/rag_eval_set.json`
- Categorias: basic_info (14), requisitos (8), documentos (8), como_solicitar (8), plazos (5), acronyms (5), colloquial (7), territorial (5), negative (5)
- 8 tramites AGE cubiertos

## Tests

- 86 tests nuevos Q3 (65 unit + 21 integration/eval; 83 passed + 3 skipped/Docker)
- Total suite: 347 passed + 5 xpassed + 11 skipped
- 0 failures, 0 regression
