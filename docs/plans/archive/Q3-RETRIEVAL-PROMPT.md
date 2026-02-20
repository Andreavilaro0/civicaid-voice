# Q3 PROMPT — Retrieval Hibrido + Rerank + Prompting Grounded

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el tech lead del proyecto **Clara / CivicAid Voice**. Vas a ejecutar el **Quarter 3 (Q3) de Fase 3: Retrieval Hibrido + Rerank + Prompting Grounded**.

Trabaja en **team agent mode**. Crea un equipo, define tareas con dependencias, spawna agentes especializados y coordina la implementacion completa. Usa los skills `/rag-architect`, `/postgres-pro`, `/test-driven-development` y `/prompt-engineer` cuando necesites guia especializada durante la ejecucion.

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

Lee estos archivos en paralelo antes de crear el equipo:

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Contexto completo del proyecto |
| `docs/plans/Q2-RAG-BEST-PRACTICES.md` | Principios RAG — especialmente secciones de reranking, anti-alucinacion y evaluacion |
| `docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md` | Que entrego Q2 — tu punto de partida |
| `docs/arreglos chat/fase-3/q2-storage/Q2-DESIGN.md` | Decisiones de arquitectura Q2 — hybrid search, chunking, score threshold |
| `docs/arreglos chat/fase-3/q2-storage/evidence/gates.md` | Evidencia Q2 — lee G6 y G7 para ver los scores actuales |
| `docs/arreglos chat/fase-3/q2-storage/audits/v1/FIXES-APPLIED.v1.md` | Errores encontrados en Q2 — no repitas |
| `src/core/retriever.py` | PGVectorRetriever actual — aqui mejoras el retrieval |
| `src/core/rag/store.py` | PGVectorStore — hybrid search actual (BM25 + vector) |
| `src/core/rag/embedder.py` | Embedder Gemini — no cambiar modelo |
| `src/core/rag/chunker.py` | Chunker por secciones — puede necesitar ajustes |
| `src/core/rag/models.py` | SQLAlchemy models — puede necesitar columnas nuevas |
| `src/core/skills/llm_generate.py` | Como se construye el contexto KB y se llama a Gemini — aqui implementas grounded prompting |
| `src/core/prompts/system_prompt.py` | System prompt actual de Clara — aqui agregas instrucciones de citacion |
| `src/core/config.py` | Feature flags existentes — aqui agregas los nuevos |
| `data/tramites/*.json` | Los 8 tramites actuales — tus queries de evaluacion vienen de aqui |
| `docs/arreglos chat/fase-3/q1-sources/backlog/Q2Q3Q4-backlog.md` | Backlog original Q3 — referencia |
| `requirements.txt` | Dependencias actuales |

## CONTEXTO RAPIDO

**Clara** = chatbot WhatsApp que ayuda a personas vulnerables en Espana a navegar tramites del gobierno. Stack: Python 3.11, Flask, Twilio, Gemini 1.5 Flash, Docker, Render.

**Q1 (CERRADO — FULL PASS)** creo artefactos machine-readable: registry.yaml (44 fuentes), schemas JSON, validadores, tests.

**Q2 (CERRADO — FULL PASS, 11/11 gates)** implemento la capa de storage:
- PostgreSQL + pgvector (Docker, 4 tablas, GIN + HNSW indexes)
- Chunking estructurado por secciones (7 secciones del ProcedureDoc)
- Embeddings Gemini gemini-embedding-001 (768 dims)
- PGVectorStore con hybrid search (BM25 tsvector + vector cosine)
- PGVectorRetriever integrado en retriever.py
- 8 tramites migrados (20 chunks, 3,879 palabras)
- 80 nuevos tests RAG, 277 total (264 passed, 8 skipped, 5 xpassed)

**Problemas conocidos de Q2 (TU los resuelves):**
1. **BM25 retorna 0.0** para muchas queries — acronimos espanoles (IMV, NIE) no matchean en tsvector Spanish config
2. **Ranking quality pobre** — el retriever no tiene reranking, depende solo del score combinado crudo
3. **Prompting NO es grounded** — `llm_generate.py` pasa un JSON plano al LLM sin instrucciones de citacion ni trazabilidad
4. **Sin evaluacion sistematica** — no hay eval set ni metricas de precision/faithfulness
5. **Gemini SDK deprecation warning** — `google.generativeai` muestra FutureWarning (cosmetico pero a resolver si hay oportunidad)

## OBJETIVO Q3

Mejorar la **calidad del retrieval y la generacion** para que Clara:
1. Encuentre los chunks correctos con precision >= 0.85 (precision@3)
2. Re-rankee resultados con cross-encoder para poner el chunk mas relevante primero
3. Genere respuestas **grounded** — cada afirmacion trazable a un chunk + fuente oficial
4. Incluya citas con URLs reales al final de cada respuesta
5. Maneje consultas territoriales ("ayuda alquiler en Madrid" vs "ayuda alquiler en Barcelona")
6. Tenga un framework de evaluacion reproducible con 50+ queries

## ENTREGABLES CONCRETOS

### E1. BM25 Tuning + Synonym Expansion
- **Problema**: `search_hybrid()` retorna `bm25=0.0` para acronimos y terminos cortos
- **Fix en `src/core/rag/store.py`**:
  - Revisar la query tsvector — puede necesitar `plainto_tsquery` en lugar de `to_tsquery`
  - Agregar expansion de sinonimos/acronimos: `IMV` -> `ingreso minimo vital`, `NIE` -> `numero identidad extranjero`, `TIE` -> `tarjeta identidad extranjero`, etc.
  - Crear `src/core/rag/synonyms.py` — diccionario de acronimos/sinonimos para tramites espanoles
  - Normalizar queries antes de BM25 (minusculas, quitar acentos para matching)
- **Verificacion**: `search_hybrid("IMV")` debe retornar `bm25 > 0` para chunks de ingreso minimo vital

### E2. Cross-Encoder Reranking
- `src/core/rag/reranker.py` — modulo de reranking
- Implementar dos estrategias (configurable via flag):
  - **Gemini reranker** (default): usar Gemini Flash para re-puntuar (query, chunk) pairs
    - Prompt: "Rate relevance 0-10 of this passage to the query. Respond with just the number."
    - Batch los top_k results del hybrid search, re-ordenar por score del reranker
  - **Heuristic reranker** (fallback sin API): boost basado en:
    - Section match (si la query pregunta "requisitos", boost chunks de seccion "requisitos")
    - Keyword overlap entre query normalizada y chunk content
    - Recency (verified_at mas reciente = mas confiable)
- Funciones:
  - `rerank(query: str, results: list[dict], strategy: str = "gemini") -> list[dict]`
  - `_gemini_rerank(query, results) -> list[dict]`
  - `_heuristic_rerank(query, results) -> list[dict]`
- Rate limiting: reutilizar la misma API key de Gemini, max 100 req/min compartido con embedder
- **Config flag nuevo**: `RAG_RERANK_STRATEGY: str = "gemini"` (opciones: "gemini", "heuristic", "none")

### E3. Grounded Prompting + Citations
- **Modificar `src/core/prompts/system_prompt.py`**:
  - Agregar bloque `CHUNKS RECUPERADOS` despues de `CONTEXTO DEL TRAMITE`
  - Cada chunk incluye: `[C1] seccion: {section_name} | fuente: {source_url} | score: {score}`
  - Agregar reglas de citacion al system prompt:
    - "Basa tu respuesta EXCLUSIVAMENTE en los chunks [C1], [C2], etc."
    - "Al final de cada parrafo, indica la fuente: [C1]"
    - "Si ningun chunk responde la pregunta, di: 'No tengo esa informacion verificada...'"
    - "NUNCA mezcles informacion de chunks de distintos tramites sin advertirlo"

- **Modificar `src/core/skills/llm_generate.py`**:
  - Nueva funcion `_build_grounded_context(kb_context, chunks_with_scores)` que genera:
    ```
    CHUNKS RECUPERADOS:
    [C1] Seccion: requisitos | Tramite: Ingreso Minimo Vital | Score: 0.82
    Contenido: "Para solicitar el IMV necesitas..."
    Fuente: https://www.seg-social.es/...

    [C2] Seccion: como_solicitar | Tramite: Ingreso Minimo Vital | Score: 0.79
    Contenido: "Puedes solicitar el IMV por..."
    Fuente: https://www.seg-social.es/...
    ```
  - Mantener `_build_kb_context()` como fallback cuando `RAG_ENABLED=false`
  - Agregar `source_urls` al `LLMResponse` o crear nuevo campo para trazabilidad

- **Modificar `src/core/models.py`**:
  - Agregar `chunks_used: list[dict] = field(default_factory=list)` a `KBContext`
  - Cada dict: `{"chunk_id", "section_name", "procedure_id", "score", "source_url", "content_preview"}`

- **Config flags nuevos**:
  - `RAG_GROUNDED_PROMPTING: bool = True` — activa el formato de chunks con citacion
  - `RAG_MAX_CHUNKS_IN_PROMPT: int = 4` — maximo chunks a incluir en el prompt

### E4. Territorial Disambiguation
- **Modificar `src/core/rag/store.py`** — agregar `search_hybrid()` parameter `territory_filter: Optional[str]`
  - Si el usuario menciona una CCAA o ciudad, pre-filtrar chunks por `metadata->>'territorio_ccaa'` o `metadata->>'territorio_municipio'`
- **Crear `src/core/rag/territory.py`**:
  - `detect_territory(query: str) -> Optional[dict]` — detecta mencion de territorio en la query
  - Diccionario de CCAA (17) + ciudades principales (50+) con variantes ("Madrid", "madrileno", "CAM")
  - Retorna `{"nivel": "ccaa|municipal", "ccaa": "madrid", "municipio": "madrid"}` o None
- **Modificar `src/core/retriever.py`**:
  - `PGVectorRetriever.retrieve()` llama `detect_territory(query)` antes del search
  - Si detecta territorio, pasa `territory_filter` al hybrid search
  - Si no detecta, busqueda normal (sin filtro)
- **Nota importante**: los 8 tramites actuales son todos AGE (nivel estatal). El filtro territorial no tendra efecto inmediato pero la infraestructura debe estar lista para cuando se ingresen tramites CCAA/municipales en Q4.

### E5. Retriever Pipeline Mejorado
- **Modificar `src/core/retriever.py`** — PGVectorRetriever.retrieve() ahora hace:
  1. `detect_territory(query)` — detectar territorio (E4)
  2. `embed_text(query)` — generar embedding
  3. `store.search_hybrid(query, embedding, territory_filter)` — busqueda hibrida mejorada (E1)
  4. `rerank(query, results)` — re-ranking (E2)
  5. `_build_kb_context_grounded(results)` — construir contexto con chunks (E3)
  6. Retornar `KBContext` con `chunks_used` poblado
- El pipeline es configurable: si `RAG_RERANK_STRATEGY="none"`, skip paso 4

### E6. Evaluation Framework
- `src/utils/rag_eval.py` — framework de evaluacion
- `data/evals/rag_eval_set.json` — 50+ queries con respuesta esperada:
  ```json
  {
    "queries": [
      {
        "id": "q001",
        "query": "que es el ingreso minimo vital",
        "expected_procedure": "age-segsocial-ingreso-minimo-vital",
        "expected_section": "descripcion",
        "expected_keywords": ["prestacion", "SEPE", "renta"],
        "territory": null
      },
      {
        "id": "q002",
        "query": "requisitos para pedir el IMV",
        "expected_procedure": "age-segsocial-ingreso-minimo-vital",
        "expected_section": "requisitos",
        "expected_keywords": ["renta", "edad", "residencia"],
        "territory": null
      }
    ]
  }
  ```
- Metricas a calcular:
  - **Precision@3**: el tramite correcto esta en top-3 resultados
  - **Precision@1**: el tramite correcto es el primer resultado
  - **Section accuracy**: la seccion correcta esta en el top result
  - **MRR (Mean Reciprocal Rank)**: posicion promedio del resultado correcto
  - **BM25 activation rate**: % de queries donde BM25 > 0
  - **Rerank improvement**: delta de precision@1 con/sin reranker
- Script: `scripts/run_rag_eval.py` que ejecuta todo y genera reporte
- **Criterio**: precision@3 >= 0.85, precision@1 >= 0.70, BM25 activation >= 0.60

### E7. Tests (minimo 30 nuevos)

```
tests/unit/
  test_synonyms.py         — Expansion de acronimos, normalizacion
  test_reranker.py         — Gemini reranker (mocked), heuristic reranker
  test_territory.py        — Deteccion de territorio en queries
  test_grounded_prompt.py  — Generacion de contexto grounded con chunks
  test_store_bm25.py       — BM25 tuning, queries que antes fallaban

tests/integration/
  test_retriever_rerank.py — Pipeline completo: search -> rerank -> grounded context
  test_rag_eval.py         — Eval framework produce metricas correctas

tests/evals/
  test_rag_precision.py    — Eval de precision@3 sobre el eval set (require Docker)
```

### E8. Documentacion
- `docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md`
- `docs/arreglos chat/fase-3/q3-retrieval/Q3-DESIGN.md` (decisiones de arquitectura)
- `docs/arreglos chat/fase-3/q3-retrieval/evidence/gates.md`
- README actualizado de `docs/arreglos chat/fase-3/README.md`

## EQUIPO

Crea un equipo llamado **`q3-retrieval`** con estos agentes:

| Nombre | subagent_type | Responsabilidad |
|--------|---------------|-----------------|
| `search-engineer` | general-purpose | BM25 tuning, synonyms.py, territory.py, mejoras a store.py |
| `rerank-engineer` | general-purpose | reranker.py (Gemini + heuristic), integracion en retriever pipeline |
| `prompt-grounding` | general-purpose | Grounded prompting: system_prompt.py, llm_generate.py, models.py, contexto con chunks |
| `eval-tester` | general-purpose | Eval framework, eval set, todos los tests, validacion de gates, no-regresion |

## TAREAS CON DEPENDENCIAS

```
FASE A — Search Quality (search-engineer)
  T1: synonyms.py + BM25 tuning en store.py (fix bm25=0.0)
  T2: territory.py (deteccion de territorio en queries)
  T3: Verificar que search_hybrid retorna bm25 > 0 para acronimos

FASE B — Reranking (rerank-engineer) [T1 completado]
  T4: reranker.py (Gemini reranker + heuristic fallback)
  T5: Integrar reranker en PGVectorRetriever pipeline
  T6: Config flags nuevos (RAG_RERANK_STRATEGY)

FASE C — Grounded Prompting (prompt-grounding) [T1 + T4 completados]
  T7: Modificar KBContext en models.py (agregar chunks_used)
  T8: Modificar system_prompt.py (reglas de citacion + bloque CHUNKS)
  T9: Modificar llm_generate.py (_build_grounded_context)
  T10: Config flags nuevos (RAG_GROUNDED_PROMPTING, RAG_MAX_CHUNKS_IN_PROMPT)

FASE D — Integration (search-engineer + rerank-engineer) [T2 + T5 + T9 completados]
  T11: Integrar territory detection en PGVectorRetriever
  T12: Pipeline completo: territory -> search -> rerank -> grounded context -> LLM

FASE E — Evaluation + Tests (eval-tester) [T12 completado]
  T13: Crear rag_eval_set.json (50+ queries)
  T14: rag_eval.py + run_rag_eval.py (framework de evaluacion)
  T15: Tests unitarios (synonyms, reranker, territory, grounded prompt, bm25)
  T16: Tests integracion (retriever pipeline, eval framework)
  T17: No-regresion: ejecutar TODOS los tests existentes (277+)

FASE F — Cierre (team lead)
  T18: Ejecutar gates de calidad
  T19: Q3-CLOSING-REPORT.md + Q3-DESIGN.md + evidence/gates.md
  T20: Actualizar README fase-3
```

## GATES DE CALIDAD

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G1 | BM25 activado | `search_hybrid("IMV")` retorna `bm25 > 0` | BM25 score > 0 para acronimos |
| G2 | Synonym expansion | `search_hybrid("NIE")` encuentra chunks de NIE/TIE | Top result = nie_tie |
| G3 | Reranker Gemini | `rerank(query, results, strategy="gemini")` re-ordena correctamente | Top result mas relevante |
| G4 | Reranker heuristic | `rerank(query, results, strategy="heuristic")` funciona sin API | Resultados re-ordenados |
| G5 | Territory detection | `detect_territory("ayuda alquiler en Madrid")` retorna `{"ccaa": "madrid"}` | Territorio detectado |
| G6 | Grounded prompt | System prompt incluye `[C1]`, `[C2]` con fuentes | Chunks numerados con URLs |
| G7 | LLM responde con citas | Clara genera respuesta mencionando fuentes `[C1]` | Citas presentes en output |
| G8 | Pipeline end-to-end | Query "requisitos IMV" -> reranked chunks -> grounded response con citas | Pipeline completo funciona |
| G9 | Precision@3 >= 0.85 | `python scripts/run_rag_eval.py` | >= 0.85 |
| G10 | BM25 activation >= 60% | Eval report muestra % queries con bm25 > 0 | >= 60% |
| G11 | >= 30 tests nuevos PASS | `pytest tests/unit/test_synonyms.py tests/unit/test_reranker.py tests/unit/test_territory.py tests/unit/test_grounded_prompt.py tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py tests/integration/test_rag_eval.py -v` | 30+ passed |
| G12 | No regresion | `pytest tests/ --tb=short` | 307+ tests (277 existentes + 30+ nuevos) |
| G13 | Lint limpio | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | 0 errores |

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Gemini reranker excede rate limit constantemente | Fallback a `RAG_RERANK_STRATEGY="heuristic"` como default. Documentar la limitacion |
| A2 | BM25 no se puede arreglar con tsvector Spanish | Alternativa: implementar BM25 puro en Python con rank_bm25 library (pip install rank-bm25) |
| A3 | Grounded prompting reduce calidad de respuestas | Hacer A/B: comparar respuestas con y sin grounding en 10 queries manuales. Si grounded es peor, iterar prompt antes de desactivar |
| A4 | Tests existentes rompen | **STOP** — fix regresiones ANTES de continuar. No avanzar con tests rotos |
| A5 | Precision@3 no alcanza 0.85 | Revisar: (1) calidad de chunks, (2) BM25 weights, (3) reranker prompt. Si aun no alcanza, documentar valor alcanzado y roadmap de mejora |

## CONSTRAINTS TECNICAS

- **Python 3.11** — no cambiar
- **Flask** — no migrar a FastAPI
- **Gemini gemini-embedding-001** — NO cambiar modelo de embedding (coherencia con Q2)
- **Gemini 1.5 Flash** — modelo LLM (no cambiar)
- **PostgreSQL + pgvector** — infraestructura existente de Q2 (no cambiar)
- **NO tocar `src/core/pipeline.py`** — integracion transparente via retriever.py y llm_generate.py
- **Backward compatible**:
  - `RAG_ENABLED=false` = todo sigue igual (JSONKBRetriever, prompt sin chunks)
  - `RAG_GROUNDED_PROMPTING=false` = prompt clasico (sin [C1], [C2])
  - `RAG_RERANK_STRATEGY="none"` = sin reranking (comportamiento Q2)
- **Feature flags**: todo nuevo detras de flags en config.py
- **No secrets en codigo**: API keys via env vars
- **No borrar archivos de Q2**: todos los modulos Q2 siguen funcionando. Q3 es ADITIVO
- **requirements.txt**: agregar solo si necesario. Candidato: `rank-bm25>=0.2` (solo si A2 se activa)
- **Score threshold 0.7** — mantener default de Q2, pero evaluar si necesita ajuste con el reranker
- **Max 4 chunks en prompt** — evitar diluir contexto (best practice: top_k 4-8)
- **Respuestas max 200 palabras** — regla existente de Clara, no cambiar

## ESTRUCTURA FINAL ESPERADA

```
civicaid-voice/
  src/core/rag/
    synonyms.py                          # NUEVO: acronimos/sinonimos para BM25
    reranker.py                          # NUEVO: Gemini + heuristic reranking
    territory.py                         # NUEVO: deteccion de territorio
    store.py                             # MODIFICADO: BM25 tuning, territory filter
  src/core/
    retriever.py                         # MODIFICADO: pipeline mejorado (territory + rerank)
    models.py                            # MODIFICADO: chunks_used en KBContext
    config.py                            # MODIFICADO: + 3 flags nuevos
    prompts/
      system_prompt.py                   # MODIFICADO: reglas de citacion + bloque CHUNKS
    skills/
      llm_generate.py                    # MODIFICADO: _build_grounded_context
  src/utils/
    rag_eval.py                          # NUEVO: framework de evaluacion
  scripts/
    run_rag_eval.py                      # NUEVO: ejecutar evaluacion
  data/evals/
    rag_eval_set.json                    # NUEVO: 50+ queries con respuestas esperadas
  tests/unit/
    test_synonyms.py                     # NUEVO
    test_reranker.py                     # NUEVO
    test_territory.py                    # NUEVO
    test_grounded_prompt.py              # NUEVO
    test_store_bm25.py                   # NUEVO
  tests/integration/
    test_retriever_rerank.py             # NUEVO
    test_rag_eval.py                     # NUEVO
  tests/evals/
    test_rag_precision.py                # NUEVO (require Docker)
  docs/arreglos chat/fase-3/
    README.md                            # MODIFICADO: + Q3
    q3-retrieval/
      Q3-CLOSING-REPORT.md              # NUEVO
      Q3-DESIGN.md                       # NUEVO
      evidence/gates.md                  # NUEVO
```

## CRITERIOS DE EXITO Q3

Al finalizar, un juez deberia poder:

1. `search_hybrid("IMV")` -> retorna resultados con `bm25 > 0` (BM25 arreglado)
2. `rerank("requisitos IMV", results)` -> chunk de requisitos sube al top (reranking funciona)
3. Enviar "que necesito para el IMV" a Clara -> respuesta con citas `[C1]` y URL oficial al final
4. Enviar "ayuda alquiler en Madrid" -> Clara detecta territorio y responde con fuentes
5. `python scripts/run_rag_eval.py` -> precision@3 >= 0.85 sobre 50+ queries
6. `RAG_ENABLED=false pytest tests/` -> todo sigue funcionando como antes
7. `RAG_ENABLED=true RAG_RERANK_STRATEGY=none pytest tests/` -> funciona sin reranker
8. `pytest tests/ --tb=short` -> 307+ tests (sin regresion)

**EMPIEZA AHORA. Crea el equipo, define las tareas y spawna los agentes.**
