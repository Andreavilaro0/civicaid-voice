# Q3 AUDIT PROMPT — Retrieval Hibrido + Rerank + Prompting Grounded

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`. Este prompt ya tiene todos los parametros pre-configurados para Q3.

> **Invocacion rapida:** `Lee el archivo docs/plans/Q3-AUDIT-PROMPT.md y ejecuta todas las instrucciones que contiene.`

---

## ROL

Eres el **auditor jefe** del proyecto Clara / CivicAid Voice. Tu trabajo es auditar el **Quarter 3 (Q3) de Fase 3: Retrieval Hibrido + Rerank + Prompting Grounded**, encontrar TODOS los problemas, corregirlos y verificar que las correcciones son validas.

Trabajas en **team agent mode**. Creas un equipo de auditores especializados, cada uno con una mision adversarial diferente. Los auditores NO confian en los reportes — verifican contra el codigo y los datos reales.

### PRINCIPIOS DE AUDITORIA

1. **Zero trust en documentacion**: Todo claim numerico se verifica contra el dato real (archivo, comando, output)
2. **Reproducibilidad**: Cada verificacion incluye el comando exacto para reproducirla
3. **Evidence-first**: Nada es PASS sin output verbatim capturado
4. **Fix-then-verify**: Cada fix se verifica con el mismo gate que fallo
5. **No regressions**: Ningun fix puede romper tests existentes
6. **Adversarial mindset**: Los auditores buscan activamente formas en que la documentacion podria mentir

### LECCIONES DE AUDITORIAS ANTERIORES (NO REPETIR)

En Q2 se encontraron estos errores recurrentes — buscarlos activamente en Q3:

| Error Q2 | Que paso | Que verificar en Q3 |
|----------|----------|---------------------|
| Nombre de modelo incorrecto | `text-embedding-004` en docs cuando el codigo usa `gemini-embedding-001` | Verificar que TODOS los nombres de modelo en docs coinciden con el codigo |
| Conteo de tests inflado | "72 tests" en todas partes cuando realmente habia 80 def test_ (72 unit + 8 integration) | Contar `def test_` en archivos nuevos vs lo que dice el closing report |
| Denominadores inconsistentes | "269 total" vs "277 collected" vs "273 def test_" — 3 metodos de conteo mezclados | Usar UN solo metodo de conteo y declarar cual |
| Tabla de feature flags desactualizada | Flag con valor viejo en Q2-DESIGN.md | Verificar flags en docs vs `config.py` real |

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

Lee estos archivos en paralelo:

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Contexto completo del proyecto |
| `docs/arreglos chat/README.md` | Indice de fases y convenciones |
| `docs/arreglos chat/fase-3/README.md` | Estado de Fase 3 |
| `docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md` | **EL DOCUMENTO PRINCIPAL A AUDITAR** |
| `docs/arreglos chat/fase-3/q3-retrieval/Q3-DESIGN.md` | Decisiones de arquitectura Q3 |
| `docs/arreglos chat/fase-3/q3-retrieval/evidence/gates.md` | Evidencia de gates Q3 |
| `docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md` | Q2 baseline — para verificar no-regresion |
| `docs/arreglos chat/fase-3/q2-storage/audits/v1/FIXES-APPLIED.v1.md` | Errores Q2 — no repetir |
| `src/core/config.py` | Feature flags reales |
| `src/core/retriever.py` | Pipeline de retrieval real |
| `src/core/rag/store.py` | Store con BM25 real |
| `src/core/rag/reranker.py` | Reranker real |
| `src/core/rag/synonyms.py` | Sinonimos real |
| `src/core/rag/territory.py` | Territory detection real |
| `src/core/prompts/system_prompt.py` | System prompt real (grounded?) |
| `src/core/skills/llm_generate.py` | LLM generate real (grounded context?) |
| `src/core/models.py` | KBContext real (tiene chunks_used?) |
| `src/utils/rag_eval.py` | Eval framework real |
| `data/evals/rag_eval_set.json` | Eval set real (cuantas queries?) |
| `requirements.txt` | Dependencias reales |

Tambien lee la auditoria de Q2 para mantener el mismo estandar:
- `docs/arreglos chat/fase-3/q2-storage/audits/v1/FIXES-APPLIED.v1.md`
- `docs/arreglos chat/fase-3/q1-sources/audits/q1-final/Q1-FINAL-STATUS.md`

## EQUIPO DE AUDITORIA

Crea un equipo llamado **`q3-audit`** con estos agentes:

| Nombre | subagent_type | Mision |
|--------|---------------|--------|
| `gate-runner` | general-purpose | Ejecutar TODOS los gates (universales + Q3 especificos), capturar output verbatim con exit codes. Extraer ground truth programatico. |
| `doc-auditor` | general-purpose | Extraer CADA claim numerico de CADA documento Q3. Cruzar contra ground truth. Producir drift check claim-by-claim. |
| `red-teamer` | general-purpose | Ejecutar 14 vectores adversariales (12 genericos + 2 especificos Q3). Buscar activamente formas en que la documentacion podria mentir. |
| `fixer` | general-purpose | Aplicar correcciones para CADA DRIFT o FAIL. Diff minimo, sin cambios cosmeticos. |

## PROTOCOLO DE AUDITORIA — 3 RONDAS

### RONDA 1: DESCUBRIMIENTO (gate-runner + doc-auditor + red-teamer en paralelo)

---

#### gate-runner — Tareas:

**T1: Ejecutar gates universales + Q3 especificos**

```bash
echo "=== AUDIT Q3 — GATES EXECUTION LOG ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse HEAD)"
echo "Python: $(python3 --version)"
```

**Gates Universales (G-U1 a G-U5):**

| # | Gate | Comando |
|---|------|---------|
| G-U1 | Tests completos | `PYTHONPATH=. pytest tests/ -v --tb=short` |
| G-U2 | Lint limpio | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` |
| G-U3 | No secrets en codigo | `grep -rn "API_KEY\|AUTH_TOKEN\|SECRET" src/ --include="*.py" \| grep -v "os.getenv\|config\.\|environ\|getenv\|#\|test_\|mock\|fake\|dummy"` |
| G-U4 | Imports validos | `python3 -c "import src.app; print('OK')"` |
| G-U5 | Git status limpio | `git status --porcelain` |

**Gates Especificos Q3 (G-Q3-1 a G-Q3-13):**

| # | Gate | Comando/Criterio | Pass |
|---|------|------------------|------|
| G-Q3-1 | BM25 activado | `python3 -c "from src.core.rag.store import PGVectorStore; from src.core.rag.embedder import embed_text; s=PGVectorStore(); e=embed_text('IMV'); r=s.search_hybrid('IMV',e); print([(x['bm25'],x['procedure_id']) for x in r])"` | bm25 > 0 para al menos 1 result |
| G-Q3-2 | Synonym expansion | `python3 -c "from src.core.rag.synonyms import expand_query; print(expand_query('NIE'))"` | Contiene "numero identidad extranjero" o similar |
| G-Q3-3 | Reranker Gemini | `python3 -c "from src.core.rag.reranker import rerank; print(rerank.__doc__)"` + `pytest tests/unit/test_reranker.py -v` | Funcion existe y tests pasan |
| G-Q3-4 | Reranker heuristic | `pytest tests/unit/test_reranker.py -v -k heuristic` | Tests heuristic pasan |
| G-Q3-5 | Territory detection | `python3 -c "from src.core.rag.territory import detect_territory; print(detect_territory('ayuda alquiler en Madrid'))"` | Retorna dict con ccaa=madrid |
| G-Q3-6 | Grounded prompt format | `python3 -c "from src.core.prompts.system_prompt import build_prompt; p=build_prompt(kb_context='test'); print('[C' in p or 'CHUNKS' in p)"` | True — prompt contiene formato de chunks |
| G-Q3-7 | KBContext has chunks_used | `python3 -c "from src.core.models import KBContext; k=KBContext(tramite='test',datos={},fuente_url='',verificado=False); print(hasattr(k,'chunks_used'))"` | True |
| G-Q3-8 | Grounded context builder | `python3 -c "from src.core.skills.llm_generate import _build_grounded_context; print(_build_grounded_context.__doc__)"` | Funcion existe |
| G-Q3-9 | Config flags nuevos | `python3 -c "from src.core.config import config; print(config.RAG_RERANK_STRATEGY, config.RAG_GROUNDED_PROMPTING, config.RAG_MAX_CHUNKS_IN_PROMPT)"` | 3 flags existen |
| G-Q3-10 | Eval set existe | `python3 -c "import json; d=json.load(open('data/evals/rag_eval_set.json')); print(f'Queries: {len(d[\"queries\"])}')"` | >= 50 queries |
| G-Q3-11 | Eval framework funciona | `python3 scripts/run_rag_eval.py --dry-run 2>/dev/null || python3 -c "from src.utils.rag_eval import run_eval; print('OK')"` | Import exitoso |
| G-Q3-12 | >= 30 tests nuevos | `pytest tests/unit/test_synonyms.py tests/unit/test_reranker.py tests/unit/test_territory.py tests/unit/test_grounded_prompt.py tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py tests/integration/test_rag_eval.py -v --tb=short` | >= 30 passed |
| G-Q3-13 | No regresion | `pytest tests/ --tb=short` | >= 307 tests (277 Q2 + 30 nuevos), 0 failures |

**Gates Docker-dependent (ejecutar solo si Docker disponible):**

| # | Gate | Comando |
|---|------|---------|
| G-Q3-D1 | Pipeline E2E con rerank | `RAG_ENABLED=true RAG_RERANK_STRATEGY=gemini pytest tests/integration/test_retriever_rerank.py -v` |
| G-Q3-D2 | Precision@3 >= 0.85 | `python3 scripts/run_rag_eval.py` |
| G-Q3-D3 | BM25 activation >= 60% | Extraer del output de G-Q3-D2 |
| G-Q3-D4 | Backward compatible | `RAG_ENABLED=false PYTHONPATH=. pytest tests/ -v --tb=short` |
| G-Q3-D5 | Sin reranker funciona | `RAG_ENABLED=true RAG_RERANK_STRATEGY=none PYTHONPATH=. pytest tests/ -v --tb=short` |

Guardar output completo en: `docs/arreglos chat/fase-3/q3-retrieval/evidence/COMMANDS-AND-OUTPUTS.{VERSION}.log`

---

**T2: Extraer ground truth programatico**

Extraer numeros REALES de los archivos, NO de los reportes:

```bash
echo "=== Q3 GROUND TRUTH ==="

# --- Tests ---
echo "--- TESTS ---"
# Total def test_ en archivos nuevos Q3
for f in tests/unit/test_synonyms.py tests/unit/test_reranker.py tests/unit/test_territory.py tests/unit/test_grounded_prompt.py tests/unit/test_store_bm25.py tests/integration/test_retriever_rerank.py tests/integration/test_rag_eval.py tests/evals/test_rag_precision.py; do
  if [ -f "$f" ]; then
    count=$(grep -c "def test_" "$f" 2>/dev/null || echo 0)
    echo "  $f: $count def test_"
  else
    echo "  $f: FILE NOT FOUND"
  fi
done

# Total tests proyecto
echo "Total project def test_:"
find tests/ -name "test_*.py" -exec grep -c "def test_" {} + 2>/dev/null | awk -F: '{sum+=$2} END {print "  " sum " def test_ total"}'

# pytest collected
pytest tests/ --collect-only -q 2>/dev/null | tail -3

# --- Archivos nuevos Q3 ---
echo "--- NEW Q3 FILES ---"
for f in src/core/rag/synonyms.py src/core/rag/reranker.py src/core/rag/territory.py src/utils/rag_eval.py scripts/run_rag_eval.py data/evals/rag_eval_set.json; do
  if [ -f "$f" ]; then
    echo "  EXISTS: $f ($(wc -l < "$f") lines)"
  else
    echo "  MISSING: $f"
  fi
done

# --- Config flags ---
echo "--- CONFIG FLAGS ---"
grep -n "RAG_" src/core/config.py

# --- Eval set ---
echo "--- EVAL SET ---"
python3 -c "
import json
try:
    d = json.load(open('data/evals/rag_eval_set.json'))
    qs = d.get('queries', [])
    print(f'  Queries: {len(qs)}')
    procs = set(q.get('expected_procedure','') for q in qs)
    print(f'  Unique procedures: {len(procs)}')
    terr = sum(1 for q in qs if q.get('territory'))
    print(f'  Queries with territory: {terr}')
except Exception as e:
    print(f'  ERROR: {e}')
" 2>/dev/null

# --- Synonyms ---
echo "--- SYNONYMS ---"
python3 -c "
try:
    from src.core.rag.synonyms import SYNONYMS
    print(f'  Synonym entries: {len(SYNONYMS)}')
except Exception as e:
    print(f'  ERROR: {e}')
" 2>/dev/null

# --- Territory ---
echo "--- TERRITORY ---"
python3 -c "
try:
    from src.core.rag.territory import CCAA_MAP, CITIES_MAP
    print(f'  CCAA entries: {len(CCAA_MAP) if hasattr(CCAA_MAP, \"__len__\") else \"N/A\"}')
    print(f'  City entries: {len(CITIES_MAP) if hasattr(CITIES_MAP, \"__len__\") else \"N/A\"}')
except Exception as e:
    print(f'  ERROR: {e}')
" 2>/dev/null

# --- Grounded prompting ---
echo "--- GROUNDED PROMPTING ---"
grep -c "\[C" src/core/prompts/system_prompt.py 2>/dev/null || echo "  No [C markers in system_prompt.py"
grep -c "_build_grounded_context" src/core/skills/llm_generate.py 2>/dev/null || echo "  No _build_grounded_context in llm_generate.py"
grep -c "chunks_used" src/core/models.py 2>/dev/null || echo "  No chunks_used in models.py"

# --- Dependencies ---
echo "--- DEPENDENCIES ---"
grep -v "^#" requirements.txt | grep -v "^$" | wc -l | xargs echo "  Total deps:"
grep "rank-bm25\|cross-encoder\|sentence-transformers" requirements.txt 2>/dev/null || echo "  No new ML deps"
```

Guardar en: `docs/arreglos chat/fase-3/q3-retrieval/evidence/GROUND-TRUTH.{VERSION}.txt`

---

#### doc-auditor — Tareas:

**T3: Drift Check (claim-by-claim)**

Para CADA documento .md dentro de `docs/arreglos chat/fase-3/q3-retrieval/`:

1. Extraer CADA claim numerico (cantidades, conteos, porcentajes, versiones, scores, nombres de modelo/funcion/archivo)
2. Cruzar contra ground truth de T2
3. Clasificar: MATCH | DRIFT | NOTE | STALE

**Claims especificos a verificar en Q3:**

| Tipo | Que verificar | Contra que |
|------|---------------|------------|
| Test count | "X new tests" en closing report | `grep -c "def test_"` en archivos nuevos Q3 |
| Test total | "Y total tests" | `pytest --collect-only` |
| Eval queries | "50+ queries" | `len(json['queries'])` en rag_eval_set.json |
| Precision@3 | Valor reportado | Output real de run_rag_eval.py |
| BM25 activation | "X%" | Output real de run_rag_eval.py |
| Synonym count | "N acronimos" | `len(SYNONYMS)` o similar |
| Territory count | "17 CCAA + N ciudades" | Conteo real en territory.py |
| Config flags | Nombres y defaults | `grep RAG_ src/core/config.py` |
| File paths | Cada path mencionado | `ls` el path real |
| Funciones mencionadas | `rerank()`, `detect_territory()`, etc. | `grep "def rerank\|def detect_territory"` en los archivos |
| Modelo de embedding | "gemini-embedding-001" | Valor real en config.py |
| Modelo LLM | "Gemini 1.5 Flash" | Valor real en llm_generate.py |
| Q2 baseline | "277 tests", "80 RAG tests" | No deberian haber cambiado |

Formato de salida:
```markdown
| # | Documento | Claim | Ubicacion | Ground Truth | Status |
|---|-----------|-------|-----------|--------------|--------|
| 1 | Q3-CLOSING-REPORT.md | "35 new tests" | line 12 | grep: 32 def test_ | DRIFT |
```

Guardar en: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/DRIFT-CHECK.{VERSION}.md`

---

**T4: URL Coverage Audit**

Escanear todos los archivos en Q3 docs y datos:
1. Extraer TODAS las URLs unicas
2. Clasificar: COVERED | GOV_NOT_COVERED | NON_GOV_REF
3. Scope A (data/) y Scope B (data/ + docs/)

Guardar en: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/URL-COVERAGE.{VERSION}.md`

---

**T5: Path Verification**

Verificar que CADA path referenciado en los documentos Q3 existe:
```bash
# Extraer paths de Q3 docs
grep -ohE '`[a-zA-Z][a-zA-Z0-9_/.-]+\.(py|yaml|json|md|txt|yml|sh)`' "docs/arreglos chat/fase-3/q3-retrieval/"*.md | sort -u
# Verificar existencia de cada uno
```

Guardar phantoms en: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/PHANTOM-PATHS.{VERSION}.txt`

---

#### red-teamer — Tareas:

**T6: Ejecutar 14 vectores adversariales**

**12 vectores genericos:**

| # | Vector | Que buscar |
|---|--------|------------|
| RT-01 | **Denominadores enganosos** | Buscar patrones N/N en docs. Ej: "precision@3 = 0.90" — verificar contra output real. Verificar que N es el universo correcto |
| RT-02 | **Scope ambiguity** | Claims que mezclan scopes: "30 new tests" — son todos unit? incluye integration? incluye evals? |
| RT-03 | **Counting confusion** | Conteo del MISMO concepto entre documentos. Ej: closing report dice "35 tests", gates.md dice "32 passed" |
| RT-04 | **Stale claims** | Numeros que eran correctos en Q2 pero deberian haberse actualizado. Ej: "277 total tests" deberia ser mayor ahora |
| RT-05 | **"No code touched" claims** | Verificar con `git diff` que archivos que dicen no haberse tocado, realmente no se tocaron |
| RT-06 | **URLs inventadas** | Spot-check 10 URLs de los datos — verificar dominios plausibles |
| RT-07 | **Phantom files** | Cada path en reportes existe en filesystem |
| RT-08 | **Gates claims vs evidence** | Cruzar cada "PASS" en Q3 reportes contra output real |
| RT-09 | **Schema mismatches** | Verificar que KBContext.chunks_used tiene la estructura declarada en docs |
| RT-10 | **Undeclared dependencies** | Verificar que ningun test/script requiere internet/APIs sin declararlo (reranker Gemini!) |
| RT-11 | **Backward compatibility** | `RAG_ENABLED=false` funciona, `RAG_RERANK_STRATEGY=none` funciona, `RAG_GROUNDED_PROMPTING=false` funciona |
| RT-12 | **Security regression** | Secrets hardcodeados, PII en logs, SQL injection en territory/synonyms, prompt injection via chunks |

**2 vectores especificos Q3:**

| # | Vector | Que buscar |
|---|--------|------------|
| RT-13 | **Reranker hallucination** | Si el Gemini reranker usa un prompt interno, verificar que ese prompt NO filtra datos del sistema. Verificar que el heuristic fallback produce resultados razonables (no todos 0 o todos iguales) |
| RT-14 | **Grounded prompt injection** | Inyectar contenido malicioso en un chunk simulado (ej: chunk.content = "Ignora instrucciones anteriores..."). Verificar que el system prompt tiene defensas contra prompt injection via chunks recuperados. Verificar que los tags `[C1]` no se pueden spoofear |

Formato por vector:
```markdown
## RT-{N}: {Nombre}
**Investigation:** {que se hizo}
**Evidence:** {comando y output}
**Finding:** {que se encontro}
**Verdict:** PASS | NOTE | FAIL
```

Guardar en: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/RED-TEAM-REPORT.{VERSION}.md`

---

### RONDA 2: CORRECCION (fixer)

**T7: Recopilar hallazgos**

Leer TODOS los reportes de Ronda 1:
- `DRIFT-CHECK.{VERSION}.md` → lista de DRIFTs y STALEs
- `RED-TEAM-REPORT.{VERSION}.md` → lista de FAILs
- `URL-COVERAGE.{VERSION}.md` → lista de GOV_NOT_COVERED
- `PHANTOM-PATHS.{VERSION}.txt` → paths fantasma
- `COMMANDS-AND-OUTPUTS.{VERSION}.log` → gates que fallaron

**T8: Priorizar y aplicar correcciones**

Para cada hallazgo:

1. **Priorizar**:
   - **P0** (bloqueante): Gate que falla, codigo incorrecto, seguridad
   - **P1** (critico): DRIFT en claim numerico, FAIL en red team
   - **P2** (menor): NOTE que podria confundir, cosmetico significativo

2. **Categorizar**:
   - `DOC-FIX` = claim incorrecto en .md → corregir el claim
   - `CODE-FIX` = bug en codigo → corregir en src/
   - `DATA-FIX` = datos inconsistentes → corregir en data/
   - `TEST-FIX` = test falla o falta → agregar/corregir test
   - `CONFIG-FIX` = configuracion incorrecta → corregir config
   - `PROMPT-FIX` = prompt inseguro o incorrecto → corregir en prompts/

3. **Principios de fix**:
   - Diff MINIMO — solo cambiar lo que esta mal
   - NO cambios cosmeticos junto con fixes reales
   - Cada fix traceable al hallazgo que lo motiva
   - NO borrar evidencia de versiones anteriores
   - Si un fix es en system_prompt.py o llm_generate.py, verificar que no rompe el comportamiento con `RAG_ENABLED=false`

4. **Registrar cada fix**:
```markdown
| # | Priority | Hallazgo | Tipo | Archivo(s) | Cambio | Status |
|---|----------|----------|------|-----------|--------|--------|
| 1 | P0 | G-Q3-1 falla: bm25=0 | CODE-FIX | store.py:42 | Fix tsquery | DONE |
```

Guardar en: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/FIXES-APPLIED.{VERSION}.md`

**T9: Re-ejecutar gates post-fix**

```bash
# Re-run ALL gates (universal + Q3)
PYTHONPATH=. pytest tests/ -v --tb=short
ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
# + todos los G-Q3-* gates especificos
```

Verificar:
- Todos los gates pasan
- No regresiones
- Los DRIFTs corregidos ya no aparecen

Guardar en: `docs/arreglos chat/fase-3/q3-retrieval/evidence/GATES-POSTFIX.{VERSION}.log`

---

### RONDA 3: VERIFICACION FINAL (team lead)

**T10: Decision de cierre**

Si Ronda 2 deja 0 DRIFT + 0 FAIL + 0 gates rotos:
→ **FULL PASS** — proceder a T11

Si quedan hallazgos abiertos:
→ Incrementar VERSION y repetir Ronda 1-2 (solo para hallazgos abiertos)
→ Maximo 3 rondas. Si tras 3 rondas quedan DRIFTs, documentar como "Known Issues"

**T11: Escribir reporte final**

Crear: `docs/arreglos chat/fase-3/q3-retrieval/audits/{VERSION}/Q3-FINAL-STATUS.md`

Estructura obligatoria:
```markdown
# Q3 Final Close-Out Status — Retrieval Hibrido + Rerank + Prompting Grounded

**Date:** {fecha}
**Branch:** {branch}
**Commit:** {commit hash}
**Python:** {version}

## Verdict: {FULL PASS | CONDITIONAL PASS | FAIL}

## Gates Summary
| Gate | Status | Detail |
|------|--------|--------|
| G-U1 Tests completos | {PASS/FAIL} | {detail} |
| G-U2 Lint | {PASS/FAIL} | {detail} |
| ... | ... | ... |
| G-Q3-1 BM25 activado | {PASS/FAIL} | {detail} |
| G-Q3-2 Synonyms | {PASS/FAIL} | {detail} |
| ... | ... | ... |

## Ground Truth Numbers
| Metric | Value |
|--------|-------|
| New Q3 test files | {N} |
| New Q3 def test_ | {N} |
| Total def test_ (project) | {N} |
| Total pytest collected | {N} (passed, skipped, xpassed) |
| Eval queries | {N} |
| Synonym entries | {N} |
| Territory CCAA | {N} |
| Territory cities | {N} |
| Config flags added | {N} |
| Precision@3 | {value} |
| BM25 activation rate | {value}% |

## Anti-Hallucination Checklist
| Check | Result |
|-------|--------|
| Doc claims match ground truth? | {YES/NO} — {count} claims, {match} MATCH, {drift} DRIFT |
| All referenced paths exist? | {YES/NO} — {exist}/{total} exist |
| No semantic inflation? | {YES/NO} — RED-TEAM: {pass}/{total} PASS |
| No phantom files? | {YES/NO} |
| Counts reproducible from data? | {YES/NO} |
| Test counting method declared? | {YES/NO} — method: {def test_ / pytest collected / ...} |
| Model names match code? | {YES/NO} |
| Backward compatibility verified? | {YES/NO} — 3 modes tested |
| Prompt injection defenses? | {YES/NO} — RT-14 result |

## Q3 vs Q2 Comparison
| Metric | Q2 | Q3 | Delta |
|--------|----|----|-------|
| Total tests | 277 | {N} | +{N} |
| RAG tests | 80 | {N} | +{N} |
| Config flags | 8 | {N} | +{N} |
| BM25 activation | 0% (broken) | {N}% | +{N}% |
| Precision@3 | N/A | {value} | NEW |

## Audit Trail
| Version | Date | Verdict | Key Action |
|---------|------|---------|------------|

## Known Limits
{lista de limitaciones conocidas que se difieren a Q4}

## Deliverables in This Directory
| File | Description |
|------|-------------|
```

**T12: Actualizar README de fase**

Actualizar `docs/arreglos chat/fase-3/README.md`:
- Estado de Q3: CERRADO
- Link al reporte final
- Resumen de metricas

**T13: Actualizar README principal**

Actualizar `docs/arreglos chat/README.md`:
- Estado actualizado en tabla
- Q3 section en indice

---

## ESTRUCTURA DE EVIDENCIA GENERADA

```
docs/arreglos chat/fase-3/q3-retrieval/
  audits/
    {VERSION}/
      Q3-FINAL-STATUS.md                    # Verdict final
      DRIFT-CHECK.{VERSION}.md              # Claim-by-claim
      RED-TEAM-REPORT.{VERSION}.md          # 14 vectores adversariales
      URL-COVERAGE.{VERSION}.md             # Cobertura de URLs
      FIXES-APPLIED.{VERSION}.md            # Registro de correcciones
      PHANTOM-PATHS.{VERSION}.txt           # Paths fantasma
  evidence/
    COMMANDS-AND-OUTPUTS.{VERSION}.log      # Output completo de gates
    GROUND-TRUTH.{VERSION}.txt              # Numeros extraidos programaticamente
    GATES-POSTFIX.{VERSION}.log             # Gates post-correccion
    gates.md                                # (ya existe del Q3 execution)
```

Nota: `{VERSION}` empieza en `v1`. Si se necesitan rondas adicionales, incrementar a `v2`, `v3`, etc.

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Tests existentes fallan ANTES de la auditoria | **STOP** — los tests deben pasar como baseline. Si Q3 dejo tests rotos, ese es el primer hallazgo |
| A2 | No existe `docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md` | **STOP** — Q3 no se ha ejecutado todavia |
| A3 | Mas de 20 DRIFTs en Ronda 1 | Considerar si Q3 necesita re-implementacion, no solo fixes |
| A4 | Fixer introduce regresiones | **REVERT** todos los fixes, re-asignar con enfoque diferente |
| A5 | 3 rondas sin llegar a FULL PASS | Cerrar como CONDITIONAL PASS con Known Issues |
| A6 | Reranker Gemini no se puede testear (sin API key) | Auditar solo heuristic. Documentar que Gemini reranker no fue auditado end-to-end |

## CRITERIOS DE CIERRE

La auditoria Q3 se cierra como **FULL PASS** cuando:

- [ ] Gates universales G-U1 a G-U5: todos PASS
- [ ] Gates Q3 G-Q3-1 a G-Q3-13: todos PASS
- [ ] Drift check: 0 DRIFT (MATCH y NOTE aceptables)
- [ ] Red team: 0 FAIL en 14 vectores (PASS y NOTE aceptables)
- [ ] URL coverage: 0 GOV_NOT_COVERED
- [ ] Phantom paths: 0 paths fantasma
- [ ] No regresion: Q2 tests (277) siguen pasando + Q3 tests nuevos
- [ ] Backward compatible: 3 modos verificados (RAG off, rerank off, grounding off)
- [ ] Q3-FINAL-STATUS.md escrito con estructura completa
- [ ] READMEs actualizados

**EMPIEZA AHORA. Lee los archivos obligatorios, crea el equipo y lanza la Ronda 1.**
