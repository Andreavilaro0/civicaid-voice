# PROMPT DE AUDITORIA + CORRECCION — Clara / CivicAid Voice

> **Como usar:** Copia todo el contenido de este archivo y pegalo como primer mensaje en una nueva sesion de Claude Code dentro del directorio `civicaid-voice/`. Antes de pegar, reemplaza los valores de `[PARAMETROS]` en la seccion de configuracion.

---

## CONFIGURACION — REEMPLAZAR ANTES DE USAR

```
FASE_OBJETIVO = fase-3/q2-storage    # Carpeta dentro de docs/arreglos chat/ a auditar
NOMBRE_CORTO  = Q2                    # Para nombrar archivos (Q1, Q2, FASE1, FASE2, etc.)
VERSION_AUDIT = v1                    # Incrementar en cada ronda (v1, v2, v3... final)
SCOPE_CODIGO  = src/ tests/ scripts/  # Directorios de codigo a verificar
SCOPE_DATOS   = data/ schemas/        # Directorios de datos a verificar
SCOPE_DOCS    = docs/arreglos chat/fase-3/q2-storage/  # Docs de esta fase
REPORT_BASE   = docs/arreglos chat/fase-3/q2-storage/  # Donde guardar reportes de auditoria
```

---

## ROL

Eres el **auditor jefe** del proyecto Clara / CivicAid Voice. Tu trabajo es auditar la fase/quarter indicada arriba, encontrar TODOS los problemas, corregirlos y verificar que las correcciones son validas.

Trabajas en **team agent mode**. Creas un equipo de auditores especializados, cada uno con una mision adversarial diferente. Los auditores NO confian en los reportes — verifican contra el codigo y los datos reales.

### PRINCIPIOS DE AUDITORIA

1. **Zero trust en documentacion**: Todo claim numerico se verifica contra el dato real (archivo, comando, output)
2. **Reproducibilidad**: Cada verificacion incluye el comando exacto para reproducirla
3. **Evidence-first**: Nada es PASS sin output verbatim capturado
4. **Fix-then-verify**: Cada fix se verifica con el mismo gate que fallo
5. **No regressions**: Ningun fix puede romper tests existentes
6. **Adversarial mindset**: Los auditores buscan activamente formas en que la documentacion podria mentir

## ANTES DE EMPEZAR — LECTURA OBLIGATORIA

Lee estos archivos en paralelo:

| Archivo | Para que |
|---------|----------|
| `CLAUDE.md` | Contexto completo del proyecto |
| `docs/arreglos chat/README.md` | Indice de fases y convenciones |
| `docs/arreglos chat/fase-3/README.md` | Estado de Fase 3 (Q1 cerrado, Q2 en curso) |
| Todo dentro de `{SCOPE_DOCS}` | Los documentos a auditar |
| Todo dentro de `{SCOPE_DATOS}` | Los datos a verificar |
| `src/core/config.py` | Feature flags actuales |
| `requirements.txt` | Dependencias |

Tambien lee los reportes de auditorias anteriores para entender el estandar:
- `docs/arreglos chat/fase-3/q1-sources/audits/q1-final/Q1-FINAL-STATUS.md`
- `docs/arreglos chat/fase-3/q1-sources/audits/q1-final/GATES-RESULTS.final.md`
- `docs/arreglos chat/fase-3/q1-sources/audits/q1-final/RED-TEAM-REPORT.final.md`
- `docs/arreglos chat/fase-3/q1-sources/audits/q1-final/DRIFT-CHECK.md`

## EQUIPO DE AUDITORIA

Crea un equipo llamado **`{NOMBRE_CORTO}-audit`** con estos agentes:

| Nombre | subagent_type | Mision |
|--------|---------------|--------|
| `gate-runner` | general-purpose | Ejecutar TODOS los gates de calidad, capturar output verbatim con exit codes. Extraer ground truth programatico de archivos reales. |
| `doc-auditor` | general-purpose | Extraer CADA claim numerico de CADA documento de la fase. Cruzar contra ground truth. Producir drift check claim-by-claim. Auditar cobertura de URLs. |
| `red-teamer` | general-purpose | Ejecutar 12 vectores adversariales contra la fase. Buscar activamente formas de que la documentacion mienta. Validar integridad semantica. |
| `fixer` | general-purpose | Aplicar correcciones para CADA DRIFT o FAIL encontrado por los otros agentes. Cada fix = diff minimo, sin cambios cosmeticos. |

## PROTOCOLO DE AUDITORIA — 3 RONDAS

### RONDA 1: DESCUBRIMIENTO (gate-runner + doc-auditor + red-teamer en paralelo)

Los 3 agentes de auditoria trabajan simultaneamente:

#### gate-runner — Tareas:

**T1: Ejecutar gates de calidad**
```bash
# Capturar TODO con timestamps y exit codes
echo "=== AUDIT {NOMBRE_CORTO} — GATES EXECUTION LOG ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse HEAD)"
echo "Python: $(python3 --version)"

# Gate basicos (SIEMPRE ejecutar)
pytest tests/ -v --tb=short              # Todos los tests
ruff check src/ tests/ scripts/ --select E,F,W --ignore E501  # Lint

# Gates especificos de la fase (ajustar segun FASE_OBJETIVO)
# Ejemplo para Q2:
# python scripts/init_db.py
# python -c "from src.core.rag.migrator import migrate_all; print(migrate_all())"
# etc.
```

Guardar output completo en: `{REPORT_BASE}/evidence/COMMANDS-AND-OUTPUTS.{VERSION_AUDIT}.log`

**T2: Extraer ground truth programatico**

Extraer numeros REALES de los archivos, NO de los reportes. Ejemplos:
```bash
# Contar tests
pytest tests/ --collect-only -q 2>/dev/null | tail -1

# Contar archivos de datos
ls data/tramites/*.json | wc -l

# Contar fuentes en registry
python3 -c "import yaml; d=yaml.safe_load(open('data/sources/registry.yaml')); print(f'Sources: {len(d.get(\"sources\",[]))}')"

# Contar lineas de archivos clave
wc -l schemas/*.json data/policy/*.yaml data/sources/*.yaml

# Feature flags
grep -c "field(default_factory" src/core/config.py

# Contar tests por directorio
find tests/ -name "test_*.py" -exec grep -c "def test_" {} + | awk -F: '{sum+=$2} END {print sum}'
```

Guardar en: `{REPORT_BASE}/evidence/GROUND-TRUTH.{VERSION_AUDIT}.txt`

#### doc-auditor — Tareas:

**T3: Drift Check (claim-by-claim)**

Para CADA documento .md dentro de `{SCOPE_DOCS}`:
1. Extraer CADA claim numerico (cantidades, conteos, porcentajes, versiones)
2. Cruzar contra ground truth de T2
3. Clasificar:
   - **MATCH** = claim coincide exactamente con ground truth
   - **DRIFT** = claim NO coincide (ERROR que requiere fix)
   - **NOTE** = claim es externo/historico, no verificable contra datos locales
   - **STALE** = claim era correcto pero ya no lo es (requiere update)

Formato de salida:
```markdown
| # | Documento | Claim | Ubicacion | Ground Truth | Status |
|---|-----------|-------|-----------|--------------|--------|
| 1 | Q2-CLOSING-REPORT.md | "20 tests nuevos" | line 15 | pytest: 22 tests nuevos | DRIFT |
```

Guardar en: `{REPORT_BASE}/evidence/DRIFT-CHECK.{VERSION_AUDIT}.md`

**T4: URL Coverage Audit**

Escanear todos los archivos en `{SCOPE_DOCS}` y `{SCOPE_DATOS}`:
1. Extraer TODAS las URLs unicas
2. Clasificar cada URL:
   - **COVERED** = dominio en allowlist.yaml
   - **GOV_NOT_COVERED** = dominio gubernamental NO en allowlist (ERROR)
   - **NON_GOV_REF** = dominio no gubernamental (informacional, OK)
3. Separar en 2 scopes:
   - **Scope A (Enforcement)**: solo archivos de datos (`data/`, `schemas/`)
   - **Scope B (Docs+Data)**: datos + documentacion

Guardar en: `{REPORT_BASE}/evidence/URL-COVERAGE.{VERSION_AUDIT}.md`

**T5: Path Verification**

Verificar que CADA path referenciado en los documentos existe en el filesystem:
```bash
# Extraer paths de los docs
grep -ohE '`[a-zA-Z][a-zA-Z0-9_/.-]+\.(py|yaml|json|md|txt|yml|sh)`' {SCOPE_DOCS}/*.md | sort -u
# Verificar existencia de cada uno
```

Guardar phantoms en: `{REPORT_BASE}/evidence/PHANTOM-PATHS.{VERSION_AUDIT}.txt`

#### red-teamer — Tareas:

**T6: Ejecutar 12 vectores adversariales**

| # | Vector | Que buscar |
|---|--------|------------|
| 1 | **Denominadores enganosos** | Buscar patrones N/N en docs. Verificar que N es el universo correcto, no cherry-picked |
| 2 | **Scope ambiguity** | Buscar claims que mezclan scopes diferentes sin declararlo |
| 3 | **Counting confusion** | Cruzar conteos de un mismo concepto entre documentos — buscar inconsistencias |
| 4 | **Stale claims** | Buscar numeros que eran correctos en una version anterior pero ya no |
| 5 | **"No code touched" claims** | Verificar con `git diff` que los archivos que dicen no haberse tocado, realmente no se tocaron |
| 6 | **URLs inventadas** | Spot-check 10 URLs aleatorias de los datos — verificar que los dominios son plausibles |
| 7 | **Phantom files** | Verificar que cada path referenciado en reportes existe en el filesystem |
| 8 | **Gates claims vs evidence** | Cruzar cada "PASS" en reportes contra el output real en COMMANDS-AND-OUTPUTS.log |
| 9 | **Schema mismatches** | Verificar que los schemas JSON usados son consistentes con los datos |
| 10 | **Undeclared dependencies** | Verificar que ningun test o script requiere internet/APIs sin declararlo |
| 11 | **Backward compatibility** | Verificar que con flags deshabilitados, todo sigue funcionando (ej: RAG_ENABLED=false) |
| 12 | **Security regression** | Buscar secrets hardcodeados, imports inseguros, PII en logs, SQL injection |

Formato de salida por vector:
```markdown
## Vector N: {Nombre}
**Investigation:** {que se hizo}
**Finding:** {que se encontro}
**Verdict:** PASS | NOTE | FAIL
```

Guardar en: `{REPORT_BASE}/evidence/RED-TEAM-REPORT.{VERSION_AUDIT}.md`

### RONDA 2: CORRECCION (fixer)

**T7: Recopilar hallazgos**

Leer los reportes de Ronda 1:
- DRIFT-CHECK → lista de DRIFTs y STALEs
- RED-TEAM-REPORT → lista de FAILs y NOTEs criticos
- URL-COVERAGE → lista de GOV_NOT_COVERED
- PHANTOM-PATHS → lista de paths fantasma
- COMMANDS-AND-OUTPUTS → lista de gates que fallaron

**T8: Aplicar correcciones**

Para cada hallazgo que requiere fix:
1. **Categorizar**:
   - `DOC-FIX` = el documento dice algo incorrecto → corregir el claim en el .md
   - `CODE-FIX` = el codigo tiene un bug → corregir en src/
   - `DATA-FIX` = los datos son inconsistentes → corregir en data/ o schemas/
   - `TEST-FIX` = un test falla o falta → agregar/corregir test
   - `CONFIG-FIX` = configuracion incorrecta → corregir config

2. **Principios de fix**:
   - Diff MINIMO — solo cambiar lo que esta mal, no mejorar "de paso"
   - NO cambios cosmeticos junto con fixes reales
   - Cada fix traceable al hallazgo que lo motiva
   - NO borrar evidencia de versiones anteriores

3. **Registrar cada fix**:
```markdown
| # | Hallazgo | Tipo | Archivo | Cambio | Status |
|---|----------|------|---------|--------|--------|
| 1 | DRIFT #3: "20 tests" deberia ser "22" | DOC-FIX | Q2-CLOSING-REPORT.md:15 | s/20 tests/22 tests/ | DONE |
```

Guardar en: `{REPORT_BASE}/evidence/FIXES-APPLIED.{VERSION_AUDIT}.md`

**T9: Re-ejecutar gates post-fix**

Despues de TODAS las correcciones:
```bash
# Re-run gates
pytest tests/ -v --tb=short
ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
# + gates especificos de la fase
```

Verificar que:
- Todos los gates pasan
- No hay regresiones (mismos tests que antes siguen pasando)
- Los DRIFTs corregidos ya no aparecen

Guardar en: `{REPORT_BASE}/evidence/GATES-POSTFIX.{VERSION_AUDIT}.log`

### RONDA 3: VERIFICACION FINAL (team lead)

**T10: Decision de cierre**

Si Ronda 2 deja 0 DRIFT + 0 FAIL + 0 gates rotos:
→ **FULL PASS** — proceder a T11

Si quedan hallazgos abiertos:
→ Incrementar VERSION_AUDIT y repetir Ronda 1-2 (solo para hallazgos abiertos)
→ Maximo 3 rondas. Si tras 3 rondas quedan DRIFTs, documentar como "Known Issues"

**T11: Escribir reporte final**

Crear: `{REPORT_BASE}/audits/{VERSION_AUDIT}/{NOMBRE_CORTO}-FINAL-STATUS.md`

Estructura obligatoria:
```markdown
# {NOMBRE_CORTO} Final Close-Out Status

**Date:** {fecha}
**Branch:** {branch}
**Commit:** {commit hash}
**Python:** {version}

## Verdict: {FULL PASS | CONDITIONAL PASS | FAIL}

## Gates Summary
| Gate | Status | Detail |
|------|--------|--------|

## Ground Truth Numbers
| Metric | Value |
|--------|-------|

## Anti-Hallucination Checklist
| Check | Result |
|-------|--------|
| Doc claims match ground truth? | {YES/NO} — {count} claims, {match} MATCH |
| All referenced paths exist? | {YES/NO} — {count}/{total} exist |
| No semantic inflation? | {YES/NO} — RED-TEAM: {pass}/{total} PASS |
| No phantom files? | {YES/NO} |
| Counts reproducible from data? | {YES/NO} |
| URL scopes declared? | {YES/NO} |

## Audit Trail
| Version | Date | Verdict | Key Action |

## Known Limits
{lista de limitaciones conocidas que se difieren}

## Deliverables in This Directory
| File | Description |
```

**T12: Actualizar README de fase**

Actualizar `docs/arreglos chat/fase-3/README.md` con:
- Estado de {NOMBRE_CORTO}: CERRADO
- Link al reporte final
- Resumen de metricas

**T13: Actualizar README principal**

Actualizar `docs/arreglos chat/README.md` con:
- Estado actualizado en tabla "Estado Actual"
- Nueva seccion en "Indice por Fases" si no existe

## GATES UNIVERSALES (ejecutar SIEMPRE)

Estos gates se ejecutan en TODA auditoria, independientemente de la fase:

| # | Gate | Comando | Criterio de PASS |
|---|------|---------|-----------------|
| G-U1 | Tests completos | `PYTHONPATH=. pytest tests/ -v --tb=short` | 0 failures, 0 errors |
| G-U2 | Lint limpio | `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` | 0 errors |
| G-U3 | No secrets en codigo | `grep -rn "API_KEY\|AUTH_TOKEN\|SECRET" src/ --include="*.py" \| grep -v "os.getenv\|config\.\|environ\|getenv\|#\|test_\|mock\|fake\|dummy"` | 0 matches |
| G-U4 | Imports validos | `python3 -c "import src.app; print('OK')"` | OK |
| G-U5 | Git status limpio | `git status --porcelain` | Solo archivos de la fase actual |

## GATES ESPECIFICOS POR FASE

Agregar al bloque de gate-runner segun la fase auditada:

### Si auditando Q2 (Storage):
| # | Gate | Comando |
|---|------|---------|
| G-Q2-1 | Docker PG arranca | `docker compose up -d && docker exec clara-db psql -U clara -d clara_rag -c "SELECT extversion FROM pg_extension WHERE extname='vector';"` |
| G-Q2-2 | Tablas creadas | `python scripts/init_db.py` |
| G-Q2-3 | Migracion exitosa | `python -c "from src.core.rag.migrator import migrate_all; print(migrate_all())"` |
| G-Q2-4 | Vector search funciona | `python -c "from src.core.rag.store import PGVectorStore; s=PGVectorStore(); print(s.search_vector(s.embed('que es el IMV'), top_k=3))"` |
| G-Q2-5 | Backward compatible | `RAG_ENABLED=false PYTHONPATH=. pytest tests/ -v --tb=short` |

### Si auditando Q1 (Sources):
| # | Gate | Comando |
|---|------|---------|
| G-Q1-1 | Registry valida | `python3 scripts/validate_source_registry.py` |
| G-Q1-2 | Policy valida | `python3 scripts/validate_policy.py` |
| G-Q1-3 | ProcedureDoc valida | `python3 scripts/validate_proceduredoc_schema.py "docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"` |
| G-Q1-4 | Link checker | `python3 scripts/link_check.py --dry-run --limit 10` |

### Si auditando Fase 1 o 2 (Codigo):
| # | Gate | Comando |
|---|------|---------|
| G-F1-1 | Tests unitarios | `PYTHONPATH=. pytest tests/unit/ -v --tb=short` |
| G-F1-2 | Tests integracion | `PYTHONPATH=. pytest tests/integration/ -v --tb=short` |
| G-F1-3 | Tests e2e | `PYTHONPATH=. pytest tests/e2e/ -v --tb=short` |
| G-F1-4 | Health endpoint | `python3 -c "from src.app import create_app; app=create_app(); c=app.test_client(); r=c.get('/health'); print(r.status_code, r.json)"` |

## ESTRUCTURA DE EVIDENCIA GENERADA

```
{REPORT_BASE}/
  audits/
    {VERSION_AUDIT}/
      {NOMBRE_CORTO}-FINAL-STATUS.md        # Verdict final
      GATES-RESULTS.{VERSION_AUDIT}.md       # Gates con output verbatim
      DRIFT-CHECK.{VERSION_AUDIT}.md         # Claim-by-claim
      RED-TEAM-REPORT.{VERSION_AUDIT}.md     # 12 vectores adversariales
      URL-COVERAGE.{VERSION_AUDIT}.md        # Cobertura de URLs
      FIXES-APPLIED.{VERSION_AUDIT}.md       # Registro de correcciones
  evidence/
    COMMANDS-AND-OUTPUTS.{VERSION_AUDIT}.log # Output completo de gates
    GROUND-TRUTH.{VERSION_AUDIT}.txt         # Numeros extraidos programaticamente
    PHANTOM-PATHS.{VERSION_AUDIT}.txt        # Paths fantasma encontrados
    GATES-POSTFIX.{VERSION_AUDIT}.log        # Gates post-correccion
```

## ABORT CONDITIONS

| ID | Condicion | Accion |
|----|-----------|--------|
| A1 | Tests existentes fallan ANTES de la auditoria | **STOP** — los tests deben pasar como baseline antes de auditar |
| A2 | No existe el directorio SCOPE_DOCS | **STOP** — no hay nada que auditar, la fase no se ha ejecutado |
| A3 | Mas de 20 DRIFTs en Ronda 1 | Considerar si la fase necesita re-implementacion, no solo fixes |
| A4 | Fixer introduce regresiones | **REVERT** todos los fixes del fixer, re-asignar a otro enfoque |
| A5 | 3 rondas sin llegar a FULL PASS | Cerrar como CONDITIONAL PASS con Known Issues documentados |

## CRITERIOS DE CIERRE

La auditoria se cierra como **FULL PASS** cuando:

- [ ] Todos los gates universales (G-U1 a G-U5) pasan
- [ ] Todos los gates especificos de la fase pasan
- [ ] Drift check: 0 DRIFT (MATCHs y NOTEs son aceptables)
- [ ] Red team: 0 FAIL (PASS y NOTE son aceptables)
- [ ] URL coverage: 0 GOV_NOT_COVERED
- [ ] Phantom paths: 0 paths fantasma
- [ ] No regresiones: mismos tests que antes de la auditoria siguen pasando
- [ ] Reporte final escrito con estructura completa
- [ ] READMEs actualizados

**EMPIEZA AHORA. Lee los archivos obligatorios, crea el equipo y lanza la Ronda 1.**
