# AUDITOR INTEGRAL DEL PROYECTO — Clara / CivicAid Voice

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`.

---

Eres el **auditor integral** del proyecto **Clara / CivicAid Voice**. Tu mision es limpiar, consolidar y sanear TODO el proyecto: documentos basura, archivos duplicados, docs desactualizados, tests rotos, codigo muerto, paths fantasma, inconsistencias entre documentos, y cualquier cosa que no aporte valor.

Trabaja en **team agent mode**. Crea un equipo de auditores especializados. Usa los skills `/code-auditor`, `/code-reviewer`, `/test-master`, `/coverage-analysis`, `/link-checker`, `/codebase-documenter` y `/systematic-debugging` cuando necesites guia especializada.

## PRINCIPIOS

1. **No borrar sin verificar** — antes de eliminar cualquier archivo, confirma que no es importado/referenciado por otro
2. **Consolidar, no fragmentar** — si hay 3 copias del mismo doc, conserva UNA en la ubicacion canonica
3. **Actualizar, no inventar** — los numeros se actualizan con ground truth (pytest, wc -l, grep), no a mano
4. **Backward compatible** — ningun cambio debe romper tests, imports o funcionalidad
5. **Evidence-first** — cada decision de limpieza va documentada con evidencia

---

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Estado actual declarado (Fases 0-4, 469+ tests) |
| `docs/00-DOCS-INDEX.md` | Indice de documentacion — verificar que cada path existe |
| `docs/00-EXECUTIVE-SUMMARY.md` | Resumen ejecutivo — verificar numeros |
| `docs/02-architecture/ARCHITECTURE.md` | Arquitectura — verificar que refleja Q4 |
| `src/core/config.py` | Feature flags reales (ground truth) |
| `requirements.txt` | Dependencias reales |

---

## EQUIPO

Crea un equipo llamado **`project-audit`** con estos agentes:

| Nombre | subagent_type | Responsabilidad |
|--------|---------------|-----------------|
| `discovery-agent` | general-purpose | T1-T10: Encontrar TODO — archivos basura, duplicados, superseded, docs desactualizados, paths fantasma, codigo muerto, tests rotos, coverage gaps. Corre en paralelo todas las tareas de descubrimiento |
| `analyzer-agent` | general-purpose | T11-T12: Consolidar hallazgos, categorizar acciones, crear plan de limpieza priorizado |
| `fixer-agent` | general-purpose | T13-T17: Aplicar todas las correcciones: borrar, mover, actualizar, consolidar. Verificar post-fix |

> **Nota**: Equipo reducido de 4→3 agentes. En la v1 habia 3 auditores paralelos + 1 fixer, pero los auditores competian por los mismos archivos. Un solo `discovery-agent` es mas eficiente y evita hallazgos duplicados.

---

## FASE 1: DESCUBRIMIENTO (discovery-agent — T1-T10 en paralelo donde sea posible)

### discovery-agent — T1: Inventario de Basura

Buscar y clasificar:

```bash
echo "=== INVENTARIO DE LIMPIEZA ==="

echo "--- 1. Archivos __pycache__ ---"
find . -type d -name "__pycache__" | grep -v ".venv" | grep -v ".auditvenv" | grep -v ".venv-test"

echo "--- 2. Archivos .pyc fuera de venvs ---"
find . -name "*.pyc" | grep -v ".venv" | grep -v ".auditvenv" | grep -v ".venv-test"

echo "--- 3. .pytest_cache ---"
find . -type d -name ".pytest_cache" | grep -v ".venv"

echo "--- 4. Archivos temporales (.bak, .old, .tmp, .orig, .swp) ---"
find . \( -name "*.bak" -o -name "*.old" -o -name "*.tmp" -o -name "*.orig" -o -name "*.swp" \) | grep -v ".venv"

echo "--- 5. Archivos vacios (compatible macOS + Linux) ---"
find . \( -name "*.py" -o -name "*.md" -o -name "*.json" \) ! -size +0c 2>/dev/null | grep -v ".venv" | grep -v "__pycache__"

echo "--- 6. Eval reports sueltos en raiz ---"
ls -la eval_report_*.json 2>/dev/null

echo "--- 7. Virtual environments que NO deberian estar trackeados ---"
ls -d .venv .auditvenv .venv-test 2>/dev/null
grep -q ".venv" .gitignore && echo ".venv en .gitignore: SI" || echo ".venv en .gitignore: NO"
grep -q ".auditvenv" .gitignore && echo ".auditvenv en .gitignore: SI" || echo ".auditvenv en .gitignore: NO"

echo "--- 8. DS_Store y archivos macOS ---"
find . -name ".DS_Store" | grep -v ".venv"
```

### discovery-agent — T2: Detectar Duplicados

Verificar estos pares conocidos:

| Archivo A | Archivo B | Accion esperada |
|-----------|-----------|-----------------|
| `docs/plans/FASE4-IDEACION.md` | `docs/01-phases/FASE4-IDEACION.md` | Si identicos → borrar de `plans/` |
| `docs/plans/FASE4-PLAN.md` | `docs/01-phases/FASE4-PLAN.md` | Si identicos → borrar de `plans/` |
| `docs/plans/FASE4-PLAN-COMPLETO.md` | `docs/01-phases/FASE4-PLAN.md` | Determinar cual es canonico |
| `docs/FASE1-CLOSING-REPORT.md` | `docs/arreglos chat/fase-1/FASE1-CLOSING-REPORT.md` | Conservar uno, borrar duplicado |
| `docs/AUDIT-REPORT.md` | `docs/AUDIT-REPORT-FASE1-VALIDADO.md` | Verificar si son versiones o duplicados |

Para cada par:
```bash
diff "archivo_a" "archivo_b" | head -20
# Si diff vacio → IDENTICOS → marcar para borrar
# Si diff con cambios → DIVERGENTES → decidir cual es canonico
```

Buscar mas duplicados automaticamente:
```bash
# Buscar .md con nombres similares en ubicaciones distintas
find docs/ -name "*.md" | sort | while read f; do
  base=$(basename "$f")
  count=$(find docs/ -name "$base" | wc -l)
  [ "$count" -gt 1 ] && echo "DUPLICADO: $base ($count copias)"
done | sort -u
```

### discovery-agent — T3: Detectar Archivos Superseded

Estos archivos han sido reemplazados por versiones nuevas:

| Archivo viejo | Reemplazo | Evidencia |
|---------------|-----------|-----------|
| `docs/plans/AUDIT-FIX-PROMPT.md` | `docs/plans/AUDITOR-MULTIAGENTE.md` | prompt-engineer.md linea 103-108 |
| `docs/plans/Q3-AUDIT-PROMPT.md` | `docs/plans/Q3-AUDIT-PROMPT-v2.md` | v2 linea 3: "corrige errores de v1" |
| `docs/plans/AUDIT-PROMPT-UNIVERSAL-v2.md` | `docs/plans/AUDITOR-MULTIAGENTE.md` | multiagente es el definitivo |

Verificar que los archivos superseded NO son referenciados en ningun otro archivo:
```bash
for f in "AUDIT-FIX-PROMPT.md" "Q3-AUDIT-PROMPT.md" "AUDIT-PROMPT-UNIVERSAL-v2.md"; do
  echo "--- Referencias a $f ---"
  grep -rn "$f" docs/ --include="*.md" | grep -v "SUPERSEDED\|deprecated\|old\|reemplazado"
done
```

---

### discovery-agent — T4: Ground Truth del Proyecto

Ejecutar y guardar:

```bash
echo "=== PROJECT GROUND TRUTH ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Branch: $(git branch --show-current)"
echo ""

echo "--- TESTS (una sola ejecucion — collect + run) ---"
PYTHONPATH=. pytest tests/ -q --tb=no 2>/dev/null | tail -5
echo ""

echo "--- SOURCE FILES ---"
echo "Total .py en src/: $(find src/ -name '*.py' | wc -l)"
echo "Total .py en tests/: $(find tests/ -name '*.py' | wc -l)"
echo "Total .py en scripts/: $(find scripts/ -name '*.py' | wc -l)"
echo ""

echo "--- CONFIG FLAGS ---"
echo "Total flags: $(grep -c 'field(default_factory' src/core/config.py)"
echo "RAG flags: $(grep -c 'RAG_' src/core/config.py)"
echo "MEMORY flags: $(grep -c 'MEMORY_' src/core/config.py)"
echo ""

echo "--- DATA ---"
echo "Tramites: $(ls data/tramites/*.json 2>/dev/null | wc -l)"
echo "Eval queries: $(python3 -c "import json; d=json.load(open('data/evals/rag_eval_set.json')); print(len(d.get('queries', d if isinstance(d, list) else [])))" 2>/dev/null)"
echo ""

echo "--- DOCS ---"
echo "Total .md: $(find docs/ -name '*.md' | wc -l)"
echo "Plans .md: $(find docs/plans/ -name '*.md' 2>/dev/null | wc -l)"
echo ""

echo "--- REQUIREMENTS ---"
cat requirements.txt
```

### discovery-agent — T5: Numeros Desactualizados

Para CADA documento .md principal, verificar que los numeros coinciden con ground truth:

| Documento | Que verificar | Ground Truth |
|-----------|---------------|--------------|
| `CLAUDE.md` | Test count (linea 58), fase status, estructura | pytest output real |
| `docs/00-EXECUTIVE-SUMMARY.md` | "96 tests" → actualizar a valor real | pytest collected |
| `docs/02-architecture/ARCHITECTURE.md` | "96 tests", feature flags count, pipeline diagram | config.py, pytest |
| `docs/arreglos chat/README.md` | Estado de cada fase/quarter | Existencia de closing reports |
| `docs/arreglos chat/fase-3/README.md` | Q4 status | Existencia de Q4 closing report |

**Formato de salida:**
```markdown
| # | Archivo | Claim | Linea | Ground Truth | Status | Fix |
|---|---------|-------|-------|--------------|--------|-----|
```

### discovery-agent — T6: Paths Fantasma

Verificar que CADA path mencionado en los documentos principales existe:

```bash
echo "=== PATH VERIFICATION ==="

# Extraer paths de CLAUDE.md y verificar
grep -oE '(src|tests|scripts|docs|data|schemas)/[a-zA-Z0-9_./-]+' CLAUDE.md | sort -u | while read p; do
  [ -e "$p" ] && echo "OK: $p" || echo "PHANTOM: $p"
done

echo ""

# Extraer paths de 00-DOCS-INDEX.md
grep -oE '(docs|src)/[a-zA-Z0-9_./-]+\.md' docs/00-DOCS-INDEX.md | sort -u | while read p; do
  [ -e "$p" ] && echo "OK: $p" || echo "PHANTOM: $p"
done
```

### discovery-agent — T7: Cross-Document Consistency

Verificar que el MISMO dato tiene el MISMO valor en TODOS los documentos:

| Dato | Documentos donde buscar | Comando |
|------|------------------------|---------|
| Test count total | CLAUDE.md, EXECUTIVE-SUMMARY, ARCHITECTURE | `grep -n "test" archivo \| grep -i "total\|96\|277\|363\|469"` |
| Feature flags count | CLAUDE.md, ARCHITECTURE | `grep -n "flag" archivo \| grep -i "9\|23\|flag"` |
| Tramites count | CLAUDE.md, EXECUTIVE-SUMMARY, KB docs | `grep -n "tramite\|KB" archivo \| grep -i "3\|8"` |
| Stack description | CLAUDE.md, EXECUTIVE-SUMMARY, ARCHITECTURE | Verificar misma lista de tech |
| Flujo arquitectura | ARCHITECTURE.md diagrama de flujo | Verificar que refleja el flujo REAL del codigo (pipeline.py), no el aspiracional. Si ARCHITECTURE dice "Query → PGVector → Fallback" pero pipeline.py llama kb_lookup directo, eso es INCONSISTENCIA CRITICA |

---

### discovery-agent — T8: Codigo Muerto

```bash
echo "=== DEAD CODE CHECK ==="

echo "--- 1. Imports no usados ---"
ruff check src/ --select F401 2>/dev/null

echo ""
echo "--- 2. Variables no usadas ---"
ruff check src/ --select F841 2>/dev/null

echo ""
echo "--- 3. Funciones standalone definidas pero nunca llamadas ---"
echo "(Nota: excluye metodos de clase — self.method() no es detectable por grep simple)"
# Solo buscar funciones TOP-LEVEL (no indentadas) en src/core/rag/
for f in src/core/rag/*.py; do
  grep -n "^def " "$f" | while read line; do
    func=$(echo "$line" | sed 's/.*def \([a-zA-Z_]*\).*/\1/')
    if [ "$func" != "__init__" ] && [ "$func" != "__repr__" ] && [ "$func" != "__str__" ]; then
      count=$(grep -rn "$func" src/ tests/ scripts/ --include="*.py" | grep -v "^.*def $func" | wc -l)
      [ "$count" -eq 0 ] && echo "DEAD: $f → $func() (0 references)"
    fi
  done
done

echo ""
echo "--- 3b. CRITICO — Verificar que pipeline.py usa get_retriever() ---"
echo "Si pipeline.py no importa get_retriever, todo el RAG pipeline es dead code funcional"
grep -n "get_retriever\|from src.core.retriever" src/core/pipeline.py || echo "CRITICO: pipeline.py NO usa get_retriever() — todo RAG es dead code"

echo ""
echo "--- 4. TODO/FIXME/HACK ---"
grep -rn "TODO\|FIXME\|HACK\|XXX\|DEPRECATED" src/ tests/ --include="*.py"

echo ""
echo "--- 5. Archivos __init__.py vacios o triviales ---"
for f in $(find src/ tests/ -name "__init__.py"); do
  lines=$(wc -l < "$f")
  [ "$lines" -le 1 ] && echo "TRIVIAL: $f ($lines lines)"
done
```

### discovery-agent — T9: Tests Rotos o Inservibles

```bash
echo "=== TEST HEALTH CHECK ==="

echo "--- 1. Tests que fallan ---"
PYTHONPATH=. pytest tests/ -v --tb=short 2>&1 | grep "FAILED\|ERROR" | head -20

echo ""
echo "--- 2. Tests permanentemente skipped ---"
PYTHONPATH=. pytest tests/ -v 2>&1 | grep "SKIPPED" | head -20

echo ""
echo "--- 3. Tests que solo tienen pass o assert True ---"
grep -rn "def test_" tests/ --include="*.py" -A 3 | grep -B 1 "pass$\|assert True$" | head -20

echo ""
echo "--- 4. Tests duplicados (mismo nombre en distintos archivos) ---"
grep -rn "def test_" tests/ --include="*.py" | awk -F: '{print $NF}' | sort | uniq -c | sort -rn | head -10

echo ""
echo "--- 5. Archivos de test sin tests ---"
for f in $(find tests/ -name "test_*.py"); do
  count=$(grep -c "def test_" "$f")
  [ "$count" -eq 0 ] && echo "EMPTY: $f (0 test functions)"
done

echo ""
echo "--- 6. Lint en tests ---"
ruff check tests/ --select E,F,W --ignore E501 2>/dev/null | head -20
```

### discovery-agent — T10: Coverage Gaps

```bash
echo "=== COVERAGE ANALYSIS ==="

echo "--- Archivos src/ sin test correspondiente ---"
for f in $(find src/core/ -name "*.py" | grep -v "__init__\|__pycache__"); do
  module=$(basename "$f" .py)
  test_exists=$(find tests/ -name "test_$module.py" 2>/dev/null | head -1)
  [ -z "$test_exists" ] && echo "NO TEST: $f"
done

echo ""
echo "--- Archivos scripts/ sin test ---"
for f in $(find scripts/ -name "*.py"); do
  echo "NO TEST: $f (scripts typically not unit-tested)"
done
```

---

## FASE 2: PLAN DE LIMPIEZA (analyzer-agent)

### T11: Recopilar Hallazgos

Leer TODOS los reportes de Fase 1 y crear tabla maestra:

```markdown
| # | Tipo | Severidad | Archivo | Problema | Accion |
|---|------|-----------|---------|----------|--------|
```

Tipos: `DUPLICATE`, `SUPERSEDED`, `OUTDATED`, `PHANTOM`, `DEAD_CODE`, `BROKEN_TEST`, `GARBAGE`, `INCONSISTENT`

Severidad: `P0` (bloquea), `P1` (importante), `P2` (menor), `P3` (cosmetico)

### T12: Categorizar acciones

Para cada hallazgo, decidir:

| Accion | Descripcion | Ejemplo |
|--------|-------------|---------|
| `DELETE` | Borrar archivo completamente | Archivo duplicado, basura |
| `ARCHIVE` | Mover a carpeta `docs/archive/` | Doc superseded pero con valor historico |
| `UPDATE` | Actualizar contenido con ground truth | Numeros desactualizados |
| `CONSOLIDATE` | Fusionar multiples archivos en uno | FASE4-PLAN + FASE4-PLAN-COMPLETO |
| `FIX_PATH` | Corregir referencia rota | Path fantasma en indice |
| `FIX_CODE` | Corregir codigo | Import muerto, funcion sin usar |
| `SKIP` | No hacer nada (evidencia historica valida) | Audit trail de Q1-Q3 con numeros de su epoca |

---

## FASE 3: EJECUCION (fixer-agent)

### T13: Limpieza de Archivos

**Orden de ejecucion (de menor a mayor riesgo):**

1. **Borrar basura** (riesgo cero):
   - `__pycache__/` fuera de venvs
   - `.pytest_cache/`
   - `.DS_Store`
   - Eval reports sueltos en raiz (mover a `data/evals/archive/`)

2. **Borrar duplicados** (riesgo bajo — verificar diff primero):
   - Archivos identicos en `docs/plans/` que ya estan en `docs/01-phases/`
   - Closing reports duplicados

3. **Archivar superseded** (riesgo bajo):
   - Crear `docs/plans/archive/` si no existe
   - Mover: AUDIT-FIX-PROMPT.md, Q3-AUDIT-PROMPT.md (v1)
   - Agregar nota al inicio: `> ARCHIVED: Superseded by [archivo nuevo]. Conservado como referencia historica.`

4. **Actualizar docs** (riesgo medio — verificar cada numero):
   - EXECUTIVE-SUMMARY.md: test count, features, stack
   - ARCHITECTURE.md: feature flags, test count, Q4 features
   - arreglos chat/README.md: estados de fases
   - Cualquier doc con numeros viejos (96, 277, 363 cuando el real es 469+)

5. **Limpiar codigo** (riesgo medio — run tests after):
   - Borrar imports no usados (F401)
   - Borrar variables no usadas (F841)
   - NO borrar funciones sin verificar que realmente son dead code

### T14: Verificar .gitignore

Asegurar que `.gitignore` incluye:
```
__pycache__/
*.pyc
.pytest_cache/
.venv/
.auditvenv/
.venv-test/
*.egg-info/
.DS_Store
eval_report_*.json
*.mp3
```

### T15: Re-run Tests Post-Fix

```bash
# Verificar que nada se rompio
PYTHONPATH=. pytest tests/ -v --tb=short
ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
```

**ABORT si algun test falla post-fix** → revertir ultimo cambio.

### T15.5: Smoke Test — App Boots OK

```bash
# Verificar que la app sigue arrancando despues de la limpieza
PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('App boots OK')"
```

**Si FALLA**: algun import roto o archivo borrado que era necesario. REVERT inmediato del ultimo cambio.

---

## FASE 4: VERIFICACION FINAL

### T16: Reporte Final

Crear: `docs/plans/FULL-PROJECT-AUDIT-REPORT.md`

```markdown
# Auditoria Integral del Proyecto — Clara / CivicAid Voice

**Fecha:** {fecha}
**Branch:** {branch}
**Ejecutado por:** project-audit team

## Resumen

| Categoria | Hallazgos | Resueltos | Pendientes |
|-----------|-----------|-----------|------------|
| Archivos duplicados | | | |
| Docs desactualizados | | | |
| Archivos superseded | | | |
| Paths fantasma | | | |
| Codigo muerto | | | |
| Tests rotos/vacios | | | |
| Basura (cache, temp) | | | |
| Inconsistencias cross-doc | | | |
| Flujo arq vs codigo real | | | |

## Ground Truth Post-Limpieza

| Metrica | Valor | Metodo |
|---------|-------|--------|
| Tests collected | | pytest --collect-only |
| Tests passed | | pytest -q |
| Tests skipped | | pytest -q |
| .py files (src) | | find src/ -name '*.py' |
| .py files (tests) | | find tests/ -name '*.py' |
| .md files (docs) | | find docs/ -name '*.md' |
| Feature flags | | grep -c field config.py |
| Tramites | | ls data/tramites/*.json |
| Eval queries | | len(json) |

## Acciones Ejecutadas

| # | Tipo | Archivo | Accion | Resultado |
|---|------|---------|--------|-----------|

## Archivos Eliminados

| Archivo | Razon | Verificado que no rompe nada |
|---------|-------|------------------------------|

## Archivos Movidos a Archive

| Origen | Destino | Razon |
|--------|---------|-------|

## Documentos Actualizados

| Archivo | Cambio | Antes | Despues |
|---------|--------|-------|---------|

## Tests Post-Limpieza

| Check | Resultado |
|-------|-----------|
| pytest tests/ | |
| ruff check | |
| Imports OK | |
| App boots OK | |
| No regresion | |

## Notas y Recomendaciones
```

### T17: Actualizar CLAUDE.md con estado post-limpieza

Actualizar `CLAUDE.md` en la raiz del proyecto con:
- Nuevo conteo de tests (ground truth de T4)
- Nuevo conteo de archivos .py, .md
- Nuevo conteo de feature flags (si cambio)
- Estado de cada fase/quarter
- Nota de que se ejecuto auditoria integral

> **Nota**: NO tocar `/Users/andreaavila/Desktop/prompt-engineer.md` — ese archivo es externo al proyecto y no debe ser modificado por un audit automatizado.

---

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Tests fallan ANTES de hacer cambios | Documentar como hallazgo, NO limpiar hasta que se arreglen |
| A2 | Un archivo "duplicado" tiene diferencias sustanciales | NO borrar — marcar como "DIVERGENT, needs manual review" |
| A3 | Un archivo "muerto" es importado dinamicamente | NO borrar — verificar con `grep -rn "import\|from.*import\|importlib" src/` |
| A4 | Borrar un .md rompe un link en otro .md | Actualizar el link antes de borrar |
| A5 | Fixer introduce regresiones (tests fallan post-fix) | **REVERT** inmediato, re-evaluar |

## CONSTRAINTS

- **NO tocar `src/core/pipeline.py`** — solo el Q4 prompt puede modificar este archivo (2 lineas: integrar get_retriever)
- **NO tocar security fixes** — escape_xml_tags, anti-spoofing, rule 11
- **NO borrar archivos de `data/tramites/`** — son source of truth
- **NO borrar `data/evals/rag_eval_set.json`** — es el eval set activo
- **NO borrar tests que pasan** — solo limpiar tests que NUNCA pasan o son triviales (assert True)
- **NO borrar audit evidence** (`docs/arreglos chat/*/audits/`) — conservar como trail historico
- **NO modificar `docs/plans/AUDITOR-MULTIAGENTE.md`** — es el auditor battle-tested
- **NO modificar `docs/plans/Q4-PRODUCTION-HARDENING-PROMPT.md`** — es el prompt de Q4 activo
- **Conservar `docs/plans/Q2-RAG-BEST-PRACTICES.md`** — referencia de principios RAG
- **Los virtual environments (.venv, etc.) NO se borran** — solo se verifican en .gitignore

---

**EMPIEZA AHORA. Crea el equipo `project-audit`, lanza Fase 1 con `discovery-agent` (T1-T10). NO aplicar fixes hasta que Fase 1 complete y `analyzer-agent` cree el plan (T11-T12).**
