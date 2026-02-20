# Q3 AUDIT PROMPT v2 — Retrieval Hibrido + Rerank + Prompting Grounded

> **Version:** v2 (battle-tested — corrige errores de v1 encontrados en auditoria real)
> **Invocacion:** `Lee el archivo docs/plans/Q3-AUDIT-PROMPT-v2.md y ejecuta todas las instrucciones que contiene.`

---

## CAMBIOS vs v1

| Problema v1 | Fix v2 |
|-------------|--------|
| `RAGEvaluator` import inexistente | Cambiado a `compute_metrics, load_eval_set` |
| `CITIES_MAP` export inexistente | Cambiado a `CITY_MAP` |
| "83 tests" sin declarar metodo de conteo | Requiere declarar metodo: `def test_` vs `passed` vs `collected` |
| LOC contados a mano (off by 1-2) | Usa `wc -l < archivo` obligatorio |
| Sin check de consistencia entre docs | Nuevo task T3b: cross-document consistency |
| RT-14 generico | RT-14 con checks especificos de sanitizacion |
| D2 decia "gemini" default sin verificar | Gate cruzado: config.py vs docs |

---

## ROL

Eres el **auditor jefe** del proyecto Clara / CivicAid Voice. Tu trabajo es auditar el **Q3: Retrieval Hibrido + Rerank + Prompting Grounded**, encontrar TODOS los problemas, corregirlos y verificarlos.

### PRINCIPIOS

1. **Zero trust en documentacion**: Todo claim numerico se verifica contra codigo/datos
2. **Reproducibilidad**: Cada verificacion incluye el comando exacto
3. **Evidence-first**: Nada es PASS sin output verbatim capturado
4. **Fix-then-verify**: Cada fix se verifica con el mismo gate que fallo
5. **No regressions**: Ningun fix puede romper tests existentes
6. **Declare counting method**: Cada conteo declara si usa `def test_`, `passed`, o `collected`

---

## LECTURA OBLIGATORIA

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Contexto del proyecto |
| `docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md` | Documento principal a auditar |
| `docs/arreglos chat/fase-3/q3-retrieval/Q3-DESIGN.md` | Decisiones de arquitectura |
| `docs/arreglos chat/fase-3/q3-retrieval/evidence/gates.md` | Evidencia de gates |
| `src/core/config.py` | Feature flags reales |
| `src/core/retriever.py` | Pipeline real |
| `src/core/rag/store.py` | Store con hybrid search |
| `src/core/rag/reranker.py` | Reranker real |
| `src/core/rag/synonyms.py` | Sinonimos real |
| `src/core/rag/territory.py` | Territory detection real |
| `src/core/prompts/system_prompt.py` | System prompt (grounded?) |
| `src/core/skills/llm_generate.py` | LLM generate (grounded context?) |
| `src/core/models.py` | KBContext (chunks_used?) |
| `src/utils/rag_eval.py` | Eval framework |
| `data/evals/rag_eval_set.json` | Eval set |

---

## EQUIPO

Crea equipo **`q3-audit`** con 4 agentes:

| Nombre | subagent_type | Mision |
|--------|---------------|--------|
| `gate-runner` | general-purpose | Ejecutar gates, extraer ground truth |
| `doc-auditor` | general-purpose | Drift check claim-by-claim + cross-doc consistency |
| `red-teamer` | general-purpose | 14 vectores adversariales |
| `fixer` | general-purpose | Corregir, verificar, no romper |

---

## RONDA 1: DESCUBRIMIENTO

### gate-runner — T1: Ground Truth

```bash
echo "=== Q3 GROUND TRUTH ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse HEAD)"

echo "--- TESTS (def test_ per file) ---"
for f in tests/unit/test_synonyms.py tests/unit/test_reranker.py \
         tests/unit/test_territory.py tests/unit/test_grounded_prompt.py \
         tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py \
         tests/integration/test_rag_eval.py tests/evals/test_rag_precision.py; do
  if [ -f "$f" ]; then
    count=$(grep -c "def test_" "$f")
    echo "  $f: $count"
  else
    echo "  $f: MISSING"
  fi
done

echo "--- TOTAL def test_ in Q3 files ---"
total=0
for f in tests/unit/test_synonyms.py tests/unit/test_reranker.py \
         tests/unit/test_territory.py tests/unit/test_grounded_prompt.py \
         tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py \
         tests/integration/test_rag_eval.py tests/evals/test_rag_precision.py; do
  [ -f "$f" ] && total=$((total + $(grep -c "def test_" "$f")))
done
echo "  TOTAL: $total"

echo "--- PYTEST COLLECTED ---"
PYTHONPATH=. pytest tests/ --collect-only -q 2>/dev/null | tail -3

echo "--- FILE LOC (wc -l) ---"
for f in src/core/rag/synonyms.py src/core/rag/reranker.py \
         src/core/rag/territory.py src/utils/rag_eval.py \
         scripts/run_rag_eval.py; do
  [ -f "$f" ] && echo "  $f: $(wc -l < "$f")" || echo "  $f: MISSING"
done

echo "--- CONFIG FLAGS ---"
PYTHONPATH=. python3 -c "
from src.core.config import config
print(f'  RAG_RERANK_STRATEGY: {config.RAG_RERANK_STRATEGY}')
print(f'  RAG_GROUNDED_PROMPTING: {config.RAG_GROUNDED_PROMPTING}')
print(f'  RAG_MAX_CHUNKS_IN_PROMPT: {config.RAG_MAX_CHUNKS_IN_PROMPT}')
"

echo "--- EVAL SET ---"
python3 -c "
import json; d=json.load(open('data/evals/rag_eval_set.json'))
print(f'  Queries: {len(d[\"queries\"])}')
print(f'  Unique procs: {len(set(q.get(\"expected_procedure\",\"\") for q in d[\"queries\"]))}')
"

echo "--- SYNONYMS ---"
PYTHONPATH=. python3 -c "from src.core.rag.synonyms import SYNONYMS; print(f'  Entries: {len(SYNONYMS)}')"

echo "--- TERRITORY ---"
PYTHONPATH=. python3 -c "
from src.core.rag.territory import CCAA_MAP, CITY_MAP
print(f'  CCAA_MAP aliases: {len(CCAA_MAP)}')
print(f'  CCAA unique: {len(set(CCAA_MAP.values()))}')
print(f'  CITY_MAP aliases: {len(CITY_MAP)}')
"

echo "--- RAG EVAL EXPORTS ---"
PYTHONPATH=. python3 -c "
import src.utils.rag_eval as m
exports = [a for a in dir(m) if not a.startswith('_')]
print(f'  Exports: {exports}')
"

echo "--- GROUNDED PROMPTING ---"
PYTHONPATH=. python3 -c "
from src.core.prompts.system_prompt import build_prompt
p = build_prompt(kb_context='test')
print(f'  Has CHUNKS in prompt: {\"CHUNKS\" in p}')
print(f'  Has [C in prompt: {\"[C\" in p}')
"
PYTHONPATH=. python3 -c "
from src.core.skills.llm_generate import _build_grounded_context
print(f'  _build_grounded_context exists: True')
"
PYTHONPATH=. python3 -c "
from src.core.models import KBContext
print(f'  chunks_used in KBContext: {hasattr(KBContext(tramite=\"t\",datos={},fuente_url=\"\",verificado=False), \"chunks_used\")}')
"
```

### gate-runner — T2: Gates Universales

| # | Gate | Comando | Pass |
|---|------|---------|------|
| G-U1 | Tests completos | `PYTHONPATH=. pytest tests/ -v --tb=short` | 0 failures |
| G-U2 | Lint | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | All passed |
| G-U3 | No secrets | `grep -rn "API_KEY\|AUTH_TOKEN\|SECRET" src/ --include="*.py" \| grep -v "os.getenv\|config\.\|environ\|getenv\|#\|test_\|mock\|fake\|dummy"` | Vacio o solo comentarios |
| G-U4 | Imports | `PYTHONPATH=. python3 -c "import src.app; print('OK')"` | OK |
| G-U5 | Git status | `git status --porcelain` | Documentar estado |

### gate-runner — T3: Gates Q3

| # | Gate | Comando | Pass |
|---|------|---------|------|
| G-Q3-1 | BM25 activado | Requiere Docker DB | DEFER si no hay Docker |
| G-Q3-2 | Synonym expansion | `PYTHONPATH=. python3 -c "from src.core.rag.synonyms import expand_query; print(expand_query('IMV')); print(expand_query('NIE'))"` | Contiene expansion |
| G-Q3-3 | Reranker existe | `PYTHONPATH=. python3 -c "from src.core.rag.reranker import rerank; print(rerank.__doc__)"` | Funcion existe |
| G-Q3-4 | Heuristic tests | `PYTHONPATH=. pytest tests/unit/test_reranker.py -v -k heuristic --tb=short` | Tests pasan |
| G-Q3-5 | Territory | `PYTHONPATH=. python3 -c "from src.core.rag.territory import detect_territory; print(detect_territory('ayuda alquiler en Madrid'))"` | Dict con ccaa |
| G-Q3-6 | Grounded prompt | `PYTHONPATH=. python3 -c "from src.core.prompts.system_prompt import build_prompt; p=build_prompt(kb_context='test'); print('CHUNKS' in p)"` | True |
| G-Q3-7 | KBContext chunks | `PYTHONPATH=. python3 -c "from src.core.models import KBContext; k=KBContext(tramite='t',datos={},fuente_url='',verificado=False); print(hasattr(k,'chunks_used'))"` | True |
| G-Q3-8 | Grounded builder | `PYTHONPATH=. python3 -c "from src.core.skills.llm_generate import _build_grounded_context; print('OK')"` | OK |
| G-Q3-9 | Config flags | `PYTHONPATH=. python3 -c "from src.core.config import config; print(config.RAG_RERANK_STRATEGY, config.RAG_GROUNDED_PROMPTING, config.RAG_MAX_CHUNKS_IN_PROMPT)"` | 3 valores |
| G-Q3-10 | Eval set | `python3 -c "import json; d=json.load(open('data/evals/rag_eval_set.json')); print(len(d['queries']))"` | >= 50 |
| G-Q3-11 | Eval framework | `PYTHONPATH=. python3 -c "from src.utils.rag_eval import compute_metrics, load_eval_set; print('OK')"` | OK |
| G-Q3-12 | Tests nuevos | `PYTHONPATH=. pytest tests/unit/test_synonyms.py tests/unit/test_reranker.py tests/unit/test_territory.py tests/unit/test_grounded_prompt.py tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py tests/integration/test_rag_eval.py -v --tb=short` | >= 30 passed |
| G-Q3-13 | No regresion | `PYTHONPATH=. pytest tests/ --tb=short` | 0 failures |

### gate-runner — T3b: Security Gate (NUEVO en v2)

| # | Gate | Comando | Pass |
|---|------|---------|------|
| G-Q3-S1 | Chunks en rule 11 | `grep -c "CHUNKS\|chunks" src/core/prompts/system_prompt.py` | Rule 11 menciona chunks como datos |
| G-Q3-S2 | Chunk sanitization | `grep -c "replace\|sanitize\|escape" src/core/skills/llm_generate.py` | > 0 (chunks sanitizados) |
| G-Q3-S3 | No [Cn] spoofing | Verificar que content_preview tiene escape de `[C` | Algun mecanismo de escape |

---

### doc-auditor — T4: Drift Check

Para CADA documento en `docs/arreglos chat/fase-3/q3-retrieval/`:
1. Extraer CADA claim numerico
2. Cruzar contra ground truth de T1
3. Clasificar: MATCH | DRIFT | NOTE

**REGLA DE CONTEO (OBLIGATORIA):** Declarar si el numero es:
- `def test_` = definiciones en codigo (grep -c "def test_")
- `passed` = tests que pasaron (pytest output)
- `collected` = tests recolectados (pytest --collect-only)

**Claims criticos Q3:**

| Tipo | Que verificar | Contra que |
|------|---------------|------------|
| Test count new | "X new tests" | `grep -c "def test_"` en 8 archivos Q3 |
| Test count total | "Y total" | `pytest --collect-only -q` |
| LOC | "N lines" por modulo | `wc -l < archivo` |
| Eval queries | "50+" | `len(json['queries'])` |
| Synonyms | "13 entradas" | `len(SYNONYMS)` |
| Territory CCAA | "17 CCAA" | `len(set(CCAA_MAP.values()))` |
| Territory cities | "60+ ciudades" | `len(CITY_MAP)` (export es CITY_MAP) |
| Config defaults | nombre y valor | `grep RAG_ src/core/config.py` |
| Model names | "gemini-embedding-001" | config.py real |

### doc-auditor — T4b: Cross-Document Consistency (NUEVO en v2)

Verificar que el MISMO dato tiene el MISMO valor en TODOS los documentos:

| Dato | Docs donde aparece | Verificar |
|------|-------------------|-----------|
| Test count | closing, design, gates | Mismo numero, mismo metodo |
| LOC per module | closing, design | Mismos valores |
| Config defaults | closing, design | Mismos defaults |
| Reranker default | design D2 vs design table vs closing | Consistente ("heuristic") |

---

### red-teamer — T5: 14 Vectores

**Vectores genericos (RT-01 a RT-12):** [mismos que v1]

**Vectores Q3 mejorados (v2):**

**RT-13: Reranker hallucination**
- Leer `src/core/rag/reranker.py` completo
- Verificar que el prompt del Gemini reranker NO filtra datos del sistema
- Verificar que heuristic produce scores diferenciados (no todos iguales)
- Verificar que existe fallback de Gemini a heuristic

**RT-14: Grounded prompt injection (MEJORADO v2)**
Ejecutar estos 3 sub-checks especificos:

```bash
# RT-14a: chunks_block en rule 11?
grep -n "SEGURIDAD" src/core/prompts/system_prompt.py
# Verificar que rule 11 menciona "CHUNKS" o "chunks" como datos, no solo user_query/memory

# RT-14b: [Cn] tag escaping?
grep -n "replace\|escape\|sanitize" src/core/skills/llm_generate.py
# Verificar que content_preview tiene algun escape de [C para evitar spoofing

# RT-14c: Asimetria de sanitizacion?
grep -rn "sanitize_for_prompt" src/
# Verificar que SI se usa para memory blocks
# Verificar SI se usa (o equivalente) para chunk content
# Si memory sanitiza pero chunks no = FAIL
```

---

## RONDA 2: CORRECCION (fixer)

Para cada hallazgo: priorizar (P0/P1/P2), categorizar (DOC-FIX/CODE-FIX), aplicar diff minimo, re-ejecutar gate.

## RONDA 3: VERIFICACION

Si 0 DRIFT + 0 FAIL + 0 gates rotos → **FULL PASS**
Si quedan hallazgos → incrementar VERSION, repetir (max 3 rondas)

Escribir reporte final en: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/Q3-FINAL-STATUS.md`

---

## LECCIONES INCORPORADAS DE AUDITORIAS ANTERIORES

| Leccion | Origen | Aplicada en v2 |
|---------|--------|-----------------|
| Nombre de modelo incorrecto en docs | Q2 | Cross-doc consistency check (T4b) |
| Conteo de tests inflado | Q2 | Metodo de conteo obligatorio |
| Denominadores inconsistentes | Q2 | Declarar `def test_` vs `passed` vs `collected` |
| Feature flags desactualizados en docs | Q2 | Gate cruzado config.py vs docs |
| "83 tests" era passed, no def test_ | Q3-v1 | Ground truth script cuenta ambos |
| LOC off by 1-2 | Q3-v1 | `wc -l` obligatorio |
| CITIES_MAP no existe | Q3-v1 | Corregido a CITY_MAP |
| RAGEvaluator no existe | Q3-v1 | Corregido a compute_metrics, load_eval_set |
| Design D2 decia "gemini" default | Q3-v1 | Cross-doc check incluye D2 vs config |
| Chunks no sanitizados | Q3-v1 RT-14 | Nuevo gate G-Q3-S1/S2/S3 |
