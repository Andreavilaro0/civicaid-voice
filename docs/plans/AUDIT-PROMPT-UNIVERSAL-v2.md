# AUDIT PROMPT UNIVERSAL v2 — Parametrico para cualquier Fase/Quarter

> **Version:** v2 (battle-tested con lecciones de Q1, Q2, Q3)
> **Uso:** Reemplaza los `{PLACEHOLDERS}` en la seccion CUSTOMIZE y ejecuta.

---

## CUSTOMIZE — Rellenar antes de ejecutar

```yaml
FASE_OBJETIVO: "Fase 3"
QUARTER: "Q3"
NOMBRE_CORTO: "Retrieval Hibrido + Rerank + Prompting Grounded"
VERSION_AUDIT: "v1"
CLOSING_REPORT: "docs/arreglos chat/fase-3/q3-retrieval/Q3-CLOSING-REPORT.md"
DESIGN_DOC: "docs/arreglos chat/fase-3/q3-retrieval/Q3-DESIGN.md"
GATES_DOC: "docs/arreglos chat/fase-3/q3-retrieval/evidence/gates.md"
AUDIT_DIR: "docs/arreglos chat/fase-3/q3-retrieval/audits"
EVIDENCE_DIR: "docs/arreglos chat/fase-3/q3-retrieval/evidence"
PREVIOUS_AUDIT: "docs/arreglos chat/fase-3/q2-storage/audits/v1/FIXES-APPLIED.v1.md"
PREVIOUS_BASELINE_TESTS: 277  # total tests antes de este quarter
TEST_FILES_NEW:  # archivos de test creados en este quarter
  - tests/unit/test_synonyms.py
  - tests/unit/test_reranker.py
  - tests/unit/test_territory.py
  - tests/unit/test_grounded_prompt.py
  - tests/unit/test_store_bm25.py
  - tests/integration/test_retriever_rerank.py
  - tests/integration/test_rag_eval.py
  - tests/evals/test_rag_precision.py
SRC_FILES_NEW:  # archivos de src creados en este quarter
  - src/core/rag/synonyms.py
  - src/core/rag/reranker.py
  - src/core/rag/territory.py
  - src/utils/rag_eval.py
  - scripts/run_rag_eval.py
  - data/evals/rag_eval_set.json
SRC_FILES_MODIFIED:  # archivos de src modificados
  - src/core/config.py
  - src/core/models.py
  - src/core/rag/store.py
  - src/core/retriever.py
  - src/core/prompts/system_prompt.py
  - src/core/skills/llm_generate.py
PHASE_SPECIFIC_GATES: |
  # Pega aqui los gates especificos de la fase (ver seccion GATES)
```

---

## ROL

Eres el **auditor jefe** del proyecto Clara / CivicAid Voice. Auditas **{QUARTER} de {FASE_OBJETIVO}: {NOMBRE_CORTO}**.

### PRINCIPIOS INMUTABLES

1. **Zero trust**: Todo claim se verifica contra codigo/datos reales
2. **Reproducible**: Cada verificacion incluye comando exacto copy-pasteable
3. **Evidence-first**: Nada es PASS sin output verbatim
4. **Fix-then-verify**: Cada fix se re-verifica con el gate que fallo
5. **No regressions**: 0 tests rotos post-fix
6. **Declare counting method**: Cada conteo numerico declara su metodo
7. **Cross-document consistency**: El mismo dato debe tener el mismo valor en todos los documentos

---

## EQUIPO

Crea equipo **`{QUARTER}-audit`** con 4 agentes:

| Nombre | subagent_type | Mision |
|--------|---------------|--------|
| `gate-runner` | general-purpose | Gates + ground truth programatico |
| `doc-auditor` | general-purpose | Drift check + cross-doc consistency |
| `red-teamer` | general-purpose | 14+ vectores adversariales |
| `fixer` | general-purpose | Correcciones + verificacion |

---

## RONDA 1: DESCUBRIMIENTO

### T1: Ground Truth Automatizado

```bash
echo "=== {QUARTER} GROUND TRUTH ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse HEAD)"
echo "Python: $(python3 --version)"

echo ""
echo "--- TESTS: def test_ per NEW file ---"
total_def=0
for f in {TEST_FILES_NEW}; do
  if [ -f "$f" ]; then
    count=$(grep -c "def test_" "$f")
    total_def=$((total_def + count))
    echo "  $f: $count"
  else
    echo "  $f: MISSING"
  fi
done
echo "  TOTAL def test_ (new): $total_def"

echo ""
echo "--- TESTS: pytest collected (whole project) ---"
PYTHONPATH=. pytest tests/ --collect-only -q 2>/dev/null | tail -3

echo ""
echo "--- TESTS: pytest run (whole project) ---"
PYTHONPATH=. pytest tests/ -q --tb=no 2>/dev/null | tail -3

echo ""
echo "--- FILE LOC (wc -l, mandatory method) ---"
for f in {SRC_FILES_NEW}; do
  [ -f "$f" ] && echo "  $f: $(wc -l < "$f") lines" || echo "  $f: MISSING"
done

echo ""
echo "--- CONFIG FLAGS (RAG_*) ---"
grep -n "RAG_" src/core/config.py 2>/dev/null

echo ""
echo "--- FILE EXISTENCE (new) ---"
for f in {SRC_FILES_NEW}; do
  [ -f "$f" ] && echo "  EXISTS: $f" || echo "  MISSING: $f"
done

echo ""
echo "--- FILE EXISTENCE (modified) ---"
for f in {SRC_FILES_MODIFIED}; do
  [ -f "$f" ] && echo "  EXISTS: $f" || echo "  MISSING: $f"
done
```

Guardar en: `{EVIDENCE_DIR}/GROUND-TRUTH.{VERSION_AUDIT}.txt`

### T2: Gates Universales (siempre presentes)

| # | Gate | Comando | Pass |
|---|------|---------|------|
| G-U1 | Tests completos | `PYTHONPATH=. pytest tests/ -v --tb=short` | 0 failures |
| G-U2 | Lint | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | All passed |
| G-U3 | No secrets | `grep -rn "API_KEY\|AUTH_TOKEN\|SECRET" src/ --include="*.py" \| grep -v "os.getenv\|config\.\|environ\|getenv\|#\|test_\|mock\|fake\|dummy"` | Vacio/comentarios |
| G-U4 | Imports | `PYTHONPATH=. python3 -c "import src.app; print('OK')"` | OK |
| G-U5 | Git status | `git status --porcelain` | Documentar |

### T3: Gates Especificos de Fase

> Pegar aqui los gates de {PHASE_SPECIFIC_GATES}

### T4: Drift Check (doc-auditor)

Para CADA documento .md en la carpeta del quarter:
1. Extraer CADA claim numerico (cantidades, conteos, %, versiones, scores, nombres)
2. Cruzar contra ground truth de T1
3. Clasificar: MATCH | DRIFT | NOTE | STALE

**REGLA OBLIGATORIA DE CONTEO:**
- `def test_` = definiciones en codigo (`grep -c "def test_"`)
- `passed` = tests que pasaron (pytest run output)
- `collected` = tests detectados (pytest --collect-only)
- `wc -l` = lineas de archivo (metodo LOC obligatorio)

**Claims universales a verificar:**

| Tipo | Que verificar | Contra que |
|------|---------------|------------|
| Test count new | "X new tests" en docs | `grep -c "def test_"` en {TEST_FILES_NEW} |
| Test total | "Y total" | `pytest --collect-only -q` |
| LOC per module | "N lines" | `wc -l < archivo` |
| Config flag names | Nombre y default | `grep RAG_ src/core/config.py` |
| File paths | Cada path mencionado | `ls path` |
| Function names | Cada funcion mencionada | `grep "def funcion"` |
| Model names | Cada nombre de modelo | Valor en config.py o codigo |
| Previous baseline | "277 tests Q2" | No debe haber cambiado |

### T4b: Cross-Document Consistency Check

Verificar que el MISMO dato tiene el MISMO valor en TODOS los documentos del quarter:

1. Leer {CLOSING_REPORT}, {DESIGN_DOC}, {GATES_DOC}
2. Para cada dato que aparece en mas de 1 doc:
   - Extraer valor de cada doc
   - Si difieren → DRIFT
   - Especial atencion a: test counts, LOC, config defaults, strategy defaults

### T5: Red Team (14+ vectores)

| # | Vector | Que buscar |
|---|--------|------------|
| RT-01 | Denominadores enganosos | Verificar N/N ratios, ej: "precision@3 = 0.90" |
| RT-02 | Scope ambiguity | "X new tests" — unit? integration? total? |
| RT-03 | Counting confusion | Mismo concepto con distinto numero entre docs |
| RT-04 | Stale claims | Numeros de quarter anterior no actualizados |
| RT-05 | No code touched | `git diff` verifica que lo declarado no-tocado realmente no cambio |
| RT-06 | URLs inventadas | Spot-check 10 URLs de datos |
| RT-07 | Phantom files | Cada path en reportes existe en filesystem |
| RT-08 | Gates claims vs evidence | Cada "PASS" verificado contra output real |
| RT-09 | Schema mismatches | Estructuras declaradas vs codigo real |
| RT-10 | Undeclared dependencies | Tests/scripts que requieren internet/APIs sin declararlo |
| RT-11 | Backward compatibility | Feature flags en modo off/none/false funcionan |
| RT-12 | Security regression | Secrets, PII, SQL injection, prompt injection |
| RT-13 | [Fase-especifico 1] | Definir segun la fase |
| RT-14 | [Fase-especifico 2] | Definir segun la fase |

**Para RT-12 SIEMPRE verificar:**
```bash
# Asimetria de sanitizacion — dato critico de Q3
grep -rn "sanitize_for_prompt\|sanitize\|escape" src/
# Si un tipo de input se sanitiza y otro no = FAIL
```

---

## RONDA 2: CORRECCION

**Prioridades:**
- **P0** (bloqueante): Gate falla, codigo incorrecto, seguridad
- **P1** (critico): DRIFT numerico, FAIL en red team
- **P2** (menor): NOTE confuso, cosmetico significativo

**Tipos:**
- `DOC-FIX` | `CODE-FIX` | `DATA-FIX` | `TEST-FIX` | `CONFIG-FIX` | `PROMPT-FIX`

**Principios:**
- Diff MINIMO
- NO cambios cosmeticos junto con fixes
- Cada fix traceable al hallazgo
- NO borrar evidencia de versiones anteriores
- Re-ejecutar tests post-fix

Guardar en: `{AUDIT_DIR}/{VERSION_AUDIT}/FIXES-APPLIED.{VERSION_AUDIT}.md`

---

## RONDA 3: VERIFICACION

Si 0 DRIFT + 0 FAIL + 0 gates rotos → **FULL PASS**
Si quedan hallazgos → VERSION++ y repetir (max 3 rondas)

Escribir reporte final: `{AUDIT_DIR}/{VERSION_AUDIT}/FINAL-STATUS.md`

Estructura obligatoria del reporte final:
```markdown
# {QUARTER} Final Close-Out Status — {NOMBRE_CORTO}

**Date:** {fecha}  **Branch:** {branch}  **Commit:** {hash}

## Verdict: {FULL PASS | CONDITIONAL PASS | FAIL}

## Gates Summary (tabla)
## Ground Truth Numbers (tabla)
## Anti-Hallucination Checklist (tabla)
## {QUARTER} vs {QUARTER-1} Comparison (tabla)
## Audit Trail (tabla de rondas)
## Known Limits
## Deliverables
```

---

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Tests fallan ANTES de auditar | STOP — baseline roto |
| A2 | No existe closing report | STOP — quarter no ejecutado |
| A3 | > 20 DRIFTs en Ronda 1 | Considerar re-implementacion |
| A4 | Fixer introduce regresiones | REVERT todo, re-asignar |
| A5 | 3 rondas sin FULL PASS | CONDITIONAL PASS con Known Issues |

---

## LECCIONES ACUMULADAS (Q1 + Q2 + Q3)

| # | Leccion | Origen | Prevencion |
|---|---------|--------|------------|
| L1 | Nombre de modelo incorrecto en docs | Q2 | Cross-doc consistency (T4b) |
| L2 | Conteo de tests inflado | Q2 | Metodo de conteo obligatorio |
| L3 | Denominadores inconsistentes | Q2 | `def test_` vs `passed` vs `collected` |
| L4 | Feature flags desactualizados en docs | Q2 | Gate cruzado config.py vs docs |
| L5 | "83 tests" era passed, no def test_ | Q3 | Ground truth cuenta ambos |
| L6 | LOC off by 1-2 | Q3 | `wc -l` obligatorio |
| L7 | Export name incorrecto (CITIES_MAP) | Q3 | Verificar imports reales antes de gates |
| L8 | Clase inexistente (RAGEvaluator) | Q3 | `dir(module)` para verificar exports |
| L9 | Design doc contradice config.py | Q3 | Cross-doc check incluye design vs code |
| L10 | Chunk content no sanitizado | Q3 | RT-12 incluye check de asimetria sanitizacion |
| L11 | [Cn] tags spoofeable | Q3 | RT-14 check especifico de escape |
