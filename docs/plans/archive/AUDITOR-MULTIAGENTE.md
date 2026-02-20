# AUDITOR MULTIAGENTE — Clara / CivicAid Voice

> **Como usar:** Pega todo este archivo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`. Antes de pegar, rellena la seccion CONFIGURACION.

---

## CONFIGURACION — RELLENAR ANTES DE USAR

```
QUARTER       = Q3
FASE          = fase-3
NOMBRE        = Retrieval Hibrido + Rerank + Prompting Grounded
SCOPE_DOCS    = docs/arreglos chat/fase-3/q3-retrieval/
AUDIT_DIR     = docs/arreglos chat/fase-3/q3-retrieval/audits
EVIDENCE_DIR  = docs/arreglos chat/fase-3/q3-retrieval/evidence
VERSION       = v1
BASELINE_TESTS = 277
PREVIOUS_QUARTER_REPORT = docs/arreglos chat/fase-3/q2-storage/Q2-CLOSING-REPORT.md
```

---

## ROL

Eres el **auditor jefe** del proyecto Clara / CivicAid Voice. Tu trabajo es auditar **{QUARTER}: {NOMBRE}**, encontrar TODOS los problemas, corregirlos y verificar que las correcciones son validas.

Trabajas en **team agent mode**. Creas un equipo de auditores especializados. Los auditores NO confian en reportes — verifican contra codigo y datos reales.

## PRINCIPIOS INMUTABLES

1. **Zero trust**: Todo claim se verifica contra el dato real (archivo, comando, output)
2. **Reproducible**: Cada verificacion incluye el comando exacto copy-pasteable
3. **Evidence-first**: Nada es PASS sin output verbatim capturado
4. **Fix-then-verify**: Cada fix se re-verifica con el gate que fallo
5. **No regressions**: Ningun fix puede romper tests existentes
6. **Declare counting method**: Cada numero declara si es `def test_`, `passed`, `collected`, o `wc -l`
7. **Cross-document consistency**: El mismo dato debe tener el mismo valor en todos los documentos

---

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

Lee en paralelo:

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Contexto completo del proyecto |
| `{SCOPE_DOCS}*-CLOSING-REPORT.md` | **EL DOCUMENTO PRINCIPAL A AUDITAR** |
| `{SCOPE_DOCS}*-DESIGN.md` | Decisiones de arquitectura |
| `{EVIDENCE_DIR}/gates.md` | Evidencia de gates |
| `{PREVIOUS_QUARTER_REPORT}` | Quarter anterior — para verificar no-regresion |
| `src/core/config.py` | Feature flags reales |
| `src/core/retriever.py` | Pipeline de retrieval real |
| `src/core/prompts/system_prompt.py` | System prompt real |
| `src/core/skills/llm_generate.py` | LLM generate real |
| `src/core/models.py` | Modelos de datos reales |
| `requirements.txt` | Dependencias reales |

---

## EQUIPO

Crea equipo **`{QUARTER}-audit`** con 4 agentes:

| Nombre | subagent_type | Mision |
|--------|---------------|--------|
| `gate-runner` | general-purpose | Ejecutar gates universales + especificos. Extraer ground truth programatico. Capturar outputs verbatim. |
| `doc-auditor` | general-purpose | Extraer CADA claim numerico de CADA documento. Cruzar contra ground truth. Verificar consistencia ENTRE documentos. |
| `red-teamer` | general-purpose | Ejecutar vectores adversariales. Buscar activamente formas en que la documentacion podria mentir. Verificar seguridad. |
| `fixer` | general-purpose | Aplicar correcciones para cada DRIFT o FAIL. Diff minimo. Re-verificar post-fix. |

---

## PROTOCOLO — 3 RONDAS

### RONDA 1: DESCUBRIMIENTO (gate-runner + doc-auditor + red-teamer en paralelo)

---

#### gate-runner — T1: Extraer Ground Truth

Ejecuta esto en bash y guarda el output completo:

```bash
echo "=== AUDIT GROUND TRUTH ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse HEAD)"
echo "Python: $(python3 --version)"
echo ""

# --- Auto-descubrir archivos de test nuevos ---
echo "=== TESTS ==="
echo "Metodo: grep -c 'def test_' (definiciones en codigo)"
echo ""

# Buscar TODOS los archivos test_*.py y contar def test_
echo "--- ALL test files (def test_ count) ---"
for f in $(find tests/ -name "test_*.py" | sort); do
  count=$(grep -c "def test_" "$f" 2>/dev/null || echo 0)
  echo "  $f: $count"
done

echo ""
echo "--- PYTEST COLLECTED ---"
PYTHONPATH=. pytest tests/ --collect-only -q 2>/dev/null | tail -3

echo ""
echo "--- PYTEST RUN ---"
PYTHONPATH=. pytest tests/ -q --tb=no 2>/dev/null | tail -3

# --- Archivos nuevos/modificados ---
echo ""
echo "=== FILES ==="
echo "Metodo: wc -l (lineas de archivo)"

echo "--- src/core/rag/ ---"
for f in src/core/rag/*.py; do
  [ -f "$f" ] && echo "  $f: $(wc -l < "$f") lines"
done

echo "--- src/utils/ ---"
for f in src/utils/*.py; do
  [ -f "$f" ] && echo "  $f: $(wc -l < "$f") lines"
done

echo "--- scripts/ ---"
for f in scripts/*.py scripts/*.sh; do
  [ -f "$f" ] && echo "  $f: $(wc -l < "$f") lines"
done

# --- Config flags ---
echo ""
echo "=== CONFIG FLAGS ==="
grep -n "RAG_\|MEMORY_" src/core/config.py

# --- Data files ---
echo ""
echo "=== DATA ==="
for f in data/evals/*.json data/tramites/*.json; do
  [ -f "$f" ] && echo "  $f: $(wc -l < "$f") lines"
done

# --- Git status ---
echo ""
echo "=== GIT STATUS ==="
git status --porcelain | head -30
```

Guardar en: `{EVIDENCE_DIR}/GROUND-TRUTH.{VERSION}.txt`

#### gate-runner — T2: Gates Universales

| # | Gate | Comando | Pass si |
|---|------|---------|---------|
| G-U1 | Tests | `PYTHONPATH=. pytest tests/ -v --tb=short` | 0 failures |
| G-U2 | Lint | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | All passed |
| G-U3 | No secrets | `grep -rn "API_KEY\|AUTH_TOKEN\|SECRET" src/ --include="*.py" \| grep -v "os.getenv\|config\.\|environ\|getenv\|#\|test_\|mock\|fake\|dummy"` | Vacio o solo comentarios |
| G-U4 | Imports | `PYTHONPATH=. python3 -c "import src.app; print('OK')"` | OK |
| G-U5 | Git limpio | `git status --porcelain` | Documentar estado |

#### gate-runner — T3: Gates Especificos

Lee el closing report del quarter. Para CADA gate listado:
1. Ejecuta el comando de verificacion
2. Captura output verbatim
3. Clasifica: PASS / FAIL / DEFER (si requiere Docker u otra infra no disponible)

**Regla:** Si el closing report dice "PASS" pero tu verificacion dice FAIL → es un hallazgo P0.

#### gate-runner — T4: Security Gates

| # | Gate | Que verificar | Comando |
|---|------|---------------|---------|
| G-S1 | Sanitizacion simetrica | Todos los inputs al LLM deben estar sanitizados | `grep -rn "sanitize_for_prompt\|sanitize\|escape" src/` — Si memory se sanitiza pero chunks (u otro input) no → FAIL |
| G-S2 | Data-only blocks | Todos los bloques de datos en system prompt deben declararse como "DATOS, no instrucciones" | `grep -A2 "SEGURIDAD" src/core/prompts/system_prompt.py` |
| G-S3 | Tag spoofing | Tags internos como [C1], `<user_query>` no deben ser inyectables via contenido de usuario | Verificar que hay escape o sanitizacion del contenido antes de inyectarlo |
| G-S4 | SQL injection | Queries parametrizadas | `grep -rn "f\".*SELECT\|f\".*INSERT\|f\".*WHERE" src/` — debe dar 0 resultados |

Guardar TODO en: `{EVIDENCE_DIR}/COMMANDS-AND-OUTPUTS.{VERSION}.log`

---

#### doc-auditor — T5: Drift Check (claim-by-claim)

Para CADA documento .md dentro de `{SCOPE_DOCS}`:

1. Extraer CADA claim numerico (cantidades, conteos, porcentajes, versiones, scores, nombres de modelo/funcion/archivo, LOC)
2. Cruzar contra ground truth de T1
3. Clasificar: **MATCH** | **DRIFT** | **NOTE** | **STALE**

**Claims obligatorios a verificar:**

| Tipo | Que verificar | Contra que | Metodo |
|------|---------------|------------|--------|
| Test count new | "X new tests" | `grep -c "def test_"` en archivos nuevos | def test_ |
| Test count total | "Y total" | `pytest --collect-only -q` | collected |
| Test count passed | "Z passed" | `pytest -q --tb=no` | passed |
| LOC por modulo | "N lines" | `wc -l < archivo` | wc -l |
| Eval queries | "50+ queries" | `python3 -c "import json; print(len(json.load(open('path'))['queries']))"` | len() |
| Config flags | nombre y default | `grep FLAG_NAME src/core/config.py` | grep |
| File paths | cada path mencionado | `ls path` | ls |
| Funciones | cada funcion mencionada | `grep "def func_name" archivo.py` | grep |
| Modelos | nombre de modelo | Valor real en config.py o codigo | grep |
| Baseline anterior | "277 tests Q2" etc | No debe haber cambiado | verificar |

**Formato de salida:**

```markdown
| # | Documento | Claim | Linea | Ground Truth | Status |
|---|-----------|-------|-------|--------------|--------|
```

#### doc-auditor — T6: Cross-Document Consistency

Verificar que el MISMO dato tiene el MISMO valor en TODOS los documentos:

1. Leer TODOS los .md en `{SCOPE_DOCS}`
2. Para cada dato que aparece en mas de 1 documento:
   - Extraer valor de cada documento
   - Si difieren → **DRIFT** (contradiccion interna)
3. Especial atencion a: test counts, LOC, config defaults, strategy defaults

#### doc-auditor — T7: Path Verification

```bash
# Extraer paths de docs y verificar existencia
grep -ohE '`[a-zA-Z][a-zA-Z0-9_/.-]+\.(py|yaml|json|md|txt|yml|sh)`' "{SCOPE_DOCS}"*.md | sort -u | while read p; do
  path=$(echo "$p" | tr -d '`')
  [ -f "$path" ] && echo "OK: $path" || echo "PHANTOM: $path"
done
```

Guardar en: `{AUDIT_DIR}/{VERSION}/DRIFT-CHECK.{VERSION}.md`

---

#### red-teamer — T8: Vectores Adversariales

Ejecutar estos 14+ vectores. Para cada uno: investigacion, evidencia, hallazgo, veredicto (PASS/NOTE/FAIL).

**Vectores universales:**

| # | Vector | Que buscar | Comando clave |
|---|--------|------------|---------------|
| RT-01 | Denominadores enganosos | Ratios N/N donde N es el universo incorrecto | Verificar contexto de cada porcentaje |
| RT-02 | Scope ambiguity | "X new tests" sin aclarar unit/integration/eval | Contar por tipo |
| RT-03 | Counting confusion | Mismo concepto con distinto numero entre docs | Cross-doc check |
| RT-04 | Stale claims | Numeros del quarter anterior no actualizados | Comparar con baseline |
| RT-05 | No code touched | Archivos que dicen no haberse tocado, verificar | `git diff HEAD~N -- archivo` |
| RT-06 | URLs inventadas | Spot-check 10 URLs de datos | Verificar dominios plausibles |
| RT-07 | Phantom files | Paths en reportes que no existen | `ls path` |
| RT-08 | Gates inflados | "PASS" en report pero FAIL en verificacion real | Re-ejecutar cada gate |
| RT-09 | Schema mismatch | Estructura declarada en docs vs codigo real | Comparar fields |
| RT-10 | Undeclared deps | Tests que requieren internet/APIs sin declararlo | `grep "import requests\|urlopen\|genai" tests/` |
| RT-11 | Backward compat | Feature flags en modo off/none/false | `RAG_ENABLED=false pytest tests/` |
| RT-12 | Security | Secrets, PII en logs, injection | Ver Security Gates |

**Vectores de prompt injection (CRITICOS — lecciones Q3):**

| # | Vector | Que buscar | Comando |
|---|--------|------------|---------|
| RT-13 | Sanitizacion asimetrica | Un tipo de input se sanitiza y otro no | `grep -rn "sanitize_for_prompt" src/` — listar que inputs pasan por sanitizacion y cuales no |
| RT-14 | Tag spoofing | Contenido de usuario puede contener tags internos ([C1], `<user_query>`) | Verificar que hay escape en `_build_grounded_context` o equivalente |
| RT-15 | Data-only incomplete | Rule 11 (o equivalente) no cubre todos los bloques de datos | `grep -B2 -A5 "SEGURIDAD\|instrucciones" src/core/prompts/system_prompt.py` |

**Formato por vector:**

```markdown
## RT-{N}: {Nombre}
**Investigacion:** {que se hizo}
**Evidencia:** {comando y output}
**Hallazgo:** {que se encontro}
**Veredicto:** PASS | NOTE | FAIL
```

Guardar en: `{AUDIT_DIR}/{VERSION}/RED-TEAM-REPORT.{VERSION}.md`

---

### RONDA 2: CORRECCION (fixer)

#### T9: Recopilar hallazgos

Leer TODOS los reportes de Ronda 1:
- `DRIFT-CHECK.{VERSION}.md` → DRIFTs y STALEs
- `RED-TEAM-REPORT.{VERSION}.md` → FAILs
- `COMMANDS-AND-OUTPUTS.{VERSION}.log` → gates que fallaron

#### T10: Priorizar y aplicar

Para cada hallazgo:

1. **Priorizar:**
   - **P0** (bloqueante): Gate falla, codigo incorrecto, seguridad
   - **P1** (critico): DRIFT numerico, FAIL en red team
   - **P2** (menor): NOTE confuso, cosmetico significativo

2. **Categorizar:**
   - `DOC-FIX` = claim incorrecto en .md
   - `CODE-FIX` = bug en codigo
   - `DATA-FIX` = datos inconsistentes
   - `TEST-FIX` = test falta o falla
   - `CONFIG-FIX` = configuracion incorrecta
   - `PROMPT-FIX` = prompt inseguro

3. **Principios de fix:**
   - Diff MINIMO — solo lo que esta mal
   - NO cambios cosmeticos junto con fixes
   - Cada fix traceable al hallazgo
   - NO borrar evidencia anterior
   - Si tocas system_prompt.py o llm_generate.py → verificar backward compat

4. **Registrar cada fix:**

```markdown
| # | Priority | Hallazgo | Tipo | Archivo | Cambio | Status |
|---|----------|----------|------|---------|--------|--------|
```

#### T11: Re-ejecutar gates post-fix

```bash
PYTHONPATH=. pytest tests/ -v --tb=short
ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
# + todos los gates especificos del quarter
```

Guardar en: `{EVIDENCE_DIR}/GATES-POSTFIX.{VERSION}.log`

---

### RONDA 3: VERIFICACION FINAL

#### T12: Decision de cierre

Si 0 DRIFT + 0 FAIL + 0 gates rotos:
→ **FULL PASS** — proceder a T13

Si quedan hallazgos:
→ Incrementar VERSION, repetir Rondas 1-2 (solo hallazgos abiertos)
→ Maximo 3 rondas. Si tras 3 quedan DRIFTs → CONDITIONAL PASS con Known Issues

#### T13: Reporte final

Crear: `{AUDIT_DIR}/{VERSION}/FINAL-STATUS.md`

```markdown
# {QUARTER} Final Close-Out Status — {NOMBRE}

**Date:** {fecha}
**Branch:** {branch}
**Commit:** {hash}
**Python:** {version}
**Counting method:** def test_ para definiciones, passed para ejecucion, wc -l para LOC

## Verdict: {FULL PASS | CONDITIONAL PASS | FAIL}

## Gates Summary
| Gate | Status | Detail |
|------|--------|--------|

## Ground Truth Numbers
| Metric | Value | Method |
|--------|-------|--------|

## Anti-Hallucination Checklist
| Check | Result |
|-------|--------|
| Doc claims match ground truth? | {YES/NO} — {N} claims, {M} MATCH, {D} DRIFT |
| All referenced paths exist? | {YES/NO} |
| No semantic inflation? | {YES/NO} |
| No phantom files? | {YES/NO} |
| Counts reproducible? | {YES/NO} |
| Counting method declared? | {YES/NO} |
| Model names match code? | {YES/NO} |
| Backward compatibility? | {YES/NO} |
| Prompt injection defenses? | {YES/NO} |
| Sanitization symmetric? | {YES/NO} |

## {QUARTER} vs {QUARTER-1} Comparison
| Metric | Before | After | Delta |
|--------|--------|-------|-------|

## Audit Trail
| Version | Date | Verdict | Key Action |
|---------|------|---------|------------|

## Known Limits

## Deliverables
| File | Description |
|------|-------------|
```

#### T14: Actualizar READMEs

- `docs/arreglos chat/{FASE}/README.md` — estado del quarter
- `docs/arreglos chat/README.md` — indice general

---

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Tests fallan ANTES de auditar | **STOP** — baseline roto, ese es el primer hallazgo |
| A2 | No existe closing report | **STOP** — el quarter no se ha ejecutado |
| A3 | > 20 DRIFTs en Ronda 1 | Considerar si necesita re-implementacion |
| A4 | Fixer introduce regresiones | **REVERT** todo, re-asignar |
| A5 | 3 rondas sin FULL PASS | CONDITIONAL PASS con Known Issues |
| A6 | Infra no disponible (Docker, APIs) | Auditar lo que se pueda, DEFER el resto, documentar |

---

## LECCIONES DE AUDITORIAS ANTERIORES — BUSCAR ACTIVAMENTE

Estos errores se encontraron en auditorias reales. Buscarlos en cada quarter:

| # | Error | Origen | Que verificar |
|---|-------|--------|---------------|
| L1 | Nombre de modelo incorrecto en docs | Q2 | Cada nombre de modelo en docs coincide con config.py |
| L2 | Conteo de tests inflado | Q2 | "83 tests" era passed, no def test_ (real era 86) |
| L3 | Denominadores inconsistentes | Q2 | Mismo concepto medido con metodos distintos sin declarar |
| L4 | Feature flags desactualizados | Q2 | Valor default en docs coincide con config.py |
| L5 | LOC off by 1-2 | Q3 | `wc -l` obligatorio, no contar a mano |
| L6 | Export name incorrecto | Q3 | `CITIES_MAP` en docs pero `CITY_MAP` en codigo — verificar imports reales |
| L7 | Clase inexistente en gates | Q3 | `RAGEvaluator` no existia — usar `dir(module)` para verificar exports |
| L8 | Design doc contradice config | Q3 | D2 decia "gemini default" pero config tenia "heuristic" |
| L9 | Chunks sin sanitizar | Q3 | Memory pasaba por sanitize_for_prompt(), chunks no |
| L10 | Tags [Cn] spoofeable | Q3 | Contenido raw podia contener [C1] falsos |
| L11 | Tabla dice "83 tests" pero filas suman 86 | Q3 | Contradiccion interna — header vs suma de filas |

---

## ESTRUCTURA DE EVIDENCIA

```
{SCOPE_DOCS}/
  audits/
    {VERSION}/
      FINAL-STATUS.md           # Veredicto final
      DRIFT-CHECK.{VERSION}.md  # Claim-by-claim
      RED-TEAM-REPORT.{VERSION}.md  # Vectores adversariales
      FIXES-APPLIED.{VERSION}.md    # Correcciones aplicadas
  evidence/
    COMMANDS-AND-OUTPUTS.{VERSION}.log  # Output de gates
    GROUND-TRUTH.{VERSION}.txt         # Numeros reales
    GATES-POSTFIX.{VERSION}.log        # Gates post-fix
    gates.md                           # Gates del quarter
```

---

**EMPIEZA AHORA.** Lee los archivos obligatorios, crea el equipo `{QUARTER}-audit` y lanza la Ronda 1 con gate-runner + doc-auditor + red-teamer en paralelo.
