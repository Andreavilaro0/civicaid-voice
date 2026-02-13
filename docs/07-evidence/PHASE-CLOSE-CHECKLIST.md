# Checklist de Cierre — CivicAid Voice "Clara"

> **Resumen en una linea:** Checklist completo de cierre para las Fases 1 y 2 del proyecto Clara, con verificaciones de codigo, deploy, documentacion, Notion, GitHub, demo y comunicacion.

## Que es

Lista de verificacion estructurada que agrupa todas las tareas necesarias para cerrar formalmente cada fase del proyecto. Cada item tiene un checkbox que indica si esta completado o pendiente.

## Para quien

- **PM** (Andrea): para coordinar el cierre y reportar al jurado
- **Desarrolladores** (Robert, Marcos): para verificar que todo el codigo esta listo
- **QA** (Lucas): para confirmar que los tests y evidencias estan completos
- **Todo el equipo** (Robert, Marcos, Lucas, Daniel, Andrea): referencia rapida del estado

## Que incluye

- Checklist de cierre de la Fase 1 (MVP)
- Checklist de cierre de la Fase 2 (Hardening y Deploy)
- Resumen consolidado con conteo de PASS/PENDING

## Que NO incluye

- Detalles de evidencias (ver PHASE-1-EVIDENCE.md y PHASE-2-EVIDENCE.md)
- Instrucciones de ejecucion de comandos (ver runbooks)

---

> **Proyecto:** CivicAid Voice / Clara
> **Fases:** 1 (MVP) + 2 (Hardening y Deploy)
> **Fecha de cierre:** En progreso (2026-02-12)
> **Responsable:** Equipo CivicAid
>
> **Relacionado:** [Evidencia Fase 1](./PHASE-1-EVIDENCE.md) | [Evidencia Fase 2](./PHASE-2-EVIDENCE.md) | [Estado de Fases](./PHASE-STATUS.md) | [Plan Fase 1](../01-phases/FASE1-IMPLEMENTACION-MVP.md)

---

## Fase 1 — MVP WhatsApp-First

### 1. Codigo

| Verificacion | Comando | Resultado esperado | Estado |
|-------------|---------|-------------------|--------|
| Todos los archivos del plan creados | `find src/ -name "*.py" \| wc -l` | 22 archivos Python | PASS |
| Todos los tests pasan (Fase 1) | `pytest tests/ -v --tb=short` | 32/32 passed | PASS |
| Lint sin errores | `ruff check src/ tests/` | 0 errores | PASS |
| Sin secretos en el codigo | `grep -r "TWILIO_AUTH\|ntn_\|sk-" src/` | 0 coincidencias (secretos solo en .env) | PASS |
| .env no commiteado | `git ls-files .env` | No rastreado | PASS |

```bash
# Ejecutar verificacion de codigo:
pytest tests/ -v --tb=short
ruff check src/ tests/
grep -r "TWILIO_AUTH\|ntn_\|sk-" src/ && echo "FALLO: secretos encontrados" || echo "PASS: sin secretos"
```

- [x] Todos los archivos del plan creados
- [x] Todos los tests pasan
- [x] Lint sin errores
- [x] Sin secretos en el codigo
- [x] .env no commiteado

---

### 2. Deploy

| Verificacion | Comando | Resultado esperado | Estado |
|-------------|---------|-------------------|--------|
| Docker build exitoso | `docker build -t civicaid-voice .` | Successfully tagged | PASS |
| Deploy en Render exitoso | `curl -s https://civicaid-voice.onrender.com/health` | HTTP 200, cuerpo JSON | PASS |
| /health devuelve JSON OK | `curl -s [URL]/health \| python -m json.tool` | 8 campos de componentes, status OK | PASS |
| Webhook Twilio configurado | Consola Twilio > Sandbox > Webhook URL | POST https://civicaid-voice.onrender.com/webhook | PASS |
| cron-job.org activo (cada 14 min) | Panel de cron-job.org | GET /health cada 14 min activo | PASS |

```bash
# Ejecutar verificacion de deploy:
docker build -t civicaid-voice .
curl -s https://civicaid-voice.onrender.com/health | python -m json.tool
```

- [x] Docker build exitoso
- [x] Deploy en Render exitoso
- [x] /health devuelve JSON OK
- [x] Webhook Twilio configurado
- [x] cron-job.org activo (cada 14 min)

---

### 3. Documentacion

| Verificacion | Archivo | Estado |
|-------------|---------|--------|
| PHASE-STATUS.md actualizado | docs/07-evidence/PHASE-STATUS.md | PASS |
| PHASE-1-EVIDENCE.md con evidencia real | docs/07-evidence/PHASE-1-EVIDENCE.md | PASS |
| Documentos de arquitectura actualizados | docs/02-architecture/ARCHITECTURE.md | PASS |
| README.md refleja estado actual | README.md | PASS |
| Resumen ejecutivo creado | docs/00-EXECUTIVE-SUMMARY.md | PASS |

- [x] PHASE-STATUS.md actualizado
- [x] PHASE-1-EVIDENCE.md con evidencia real
- [x] Documentos de arquitectura actualizados
- [x] README.md refleja estado actual
- [x] Resumen ejecutivo creado

---

### 4. Notion

| Verificacion | Accion | Estado |
|-------------|--------|--------|
| Phase Releases DB actualizada | Crear entrada Fase 1 con commit SHA, URL, estado | PASS |
| Backlog: tareas pasadas a "Hecho" | Mover D1.x, D2.x completadas a Hecho | PASS |
| Demo & Testing: resultados actualizados | Actualizar con "Pasa"/"Falla" por test | PASS |
| Metricas de latencia registradas | Cache <2s, TwiML ACK <1s, pipeline audio <15s | PASS |

- [x] Phase Releases DB actualizada
- [x] Backlog: tareas pasadas a "Hecho"
- [x] Demo & Testing: resultados actualizados
- [x] Metricas de latencia registradas

---

### 5. GitHub

| Verificacion | Comando | Estado |
|-------------|---------|--------|
| Commit con mensaje descriptivo | `git log -1 --oneline` | PASS |
| Push a main | `git push origin main` | PASS |
| Tag release | `git tag phase-1-v1.0 && git push --tags` | PENDING |
| Issues cerrados | `gh issue list --state open` | PENDING |

```bash
# Ejecutar cierre GitHub:
git add -A && git commit -m "feat: Fase 1 MVP completa — 32/32 tests, Docker, docs"
git push origin main
git tag phase-1-v1.0 && git push --tags
```

- [x] Commit con mensaje descriptivo
- [x] Push a main
- [ ] Tag release
- [ ] Issues cerrados

---

### 6. Demo / QA

| Verificacion | Accion | Estado |
|-------------|--------|--------|
| Ensayo de demo completado | Ejecutar guion completo de RUNBOOK-DEMO.md | PASS |
| Video de backup grabado | Grabacion de pantalla del demo end-to-end | PASS |
| Screenshots de fallback listos | Capturas de /health, conversacion WA, Notion | PASS |

- [x] Ensayo de demo completado
- [x] Video de backup grabado
- [x] Screenshots de fallback listos

---

### 7. Comunicacion

| Verificacion | Accion | Estado |
|-------------|--------|--------|
| Equipo notificado del cierre | Mensaje en canal del equipo | PASS |
| Siguiente fase planificada | Scope de Fase 2 definido en documento FASE2 | PASS |

- [x] Equipo notificado del cierre
- [x] Siguiente fase planificada

---

## Fase 2 — Hardening, Deploy e Integraciones

### 8. Toolkit de Seguridad y Calidad

| Verificacion | Evidencia | Estado |
|-------------|----------|--------|
| Guardrails implementados (pre-check + post-check) | 19 tests pasan en test_guardrails.py | PASS |
| Redaccion PII activa (DNI, NIE, telefono) | Tests de redaccion en test_guardrails.py | PASS |
| Structured outputs modelo Pydantic | 10 tests pasan en test_structured_outputs.py | PASS |
| Framework de evaluaciones operativo | 9 tests pasan en test_evals.py | PASS |
| Red team: 5 vectores adversariales bloqueados | 5 XPASS en test_redteam.py | PASS |
| Observabilidad: RequestContext + timings | 6 tests pasan en test_observability.py | PASS |
| Retriever abstracto + JSONKBRetriever | 7 tests pasan en test_retriever.py | PASS |
| 9 feature flags configurados | Config con todos los flags verificada | PASS |

- [x] Guardrails implementados (pre-check + post-check)
- [x] Redaccion PII activa (DNI, NIE, telefono)
- [x] Structured outputs modelo Pydantic
- [x] Framework de evaluaciones operativo
- [x] Red team: 5 vectores adversariales bloqueados
- [x] Observabilidad: RequestContext + timings
- [x] Retriever abstracto + JSONKBRetriever
- [x] 9 feature flags configurados

---

### 9. Deploy y Operaciones

| Verificacion | Evidencia | Estado |
|-------------|----------|--------|
| Docker build exitoso (Python 3.11-slim) | `docker build -t civicaid-voice:test .` BUILD EXITOSO | PASS |
| Render /health responde 200 OK | `curl .../health` devuelve JSON con cache_entries=8 | PASS |
| render.yaml: secretos con sync: false | Sin secretos hardcodeados en render.yaml | PASS |
| .dockerignore presente y correcto | Excluye .env, .git, docs, tests | PASS |
| Puerto Render: 10000 / Puerto local: 5000 | Configurado en Dockerfile y app.py | PASS |
| Warm-up cron cada 14 min documentado | RUNBOOK-PHASE2.md Seccion 5 | PASS |

- [x] Docker build exitoso (Python 3.11-slim)
- [x] Render /health responde 200 OK
- [x] render.yaml: secretos con sync: false
- [x] .dockerignore presente y correcto
- [x] Puerto Render: 10000 / Puerto local: 5000
- [x] Warm-up cron cada 14 min documentado

---

### 10. Twilio

| Verificacion | Evidencia | Estado |
|-------------|----------|--------|
| Validacion de firma con RequestValidator | Implementado en webhook.py | PASS |
| Timeout de 10s en envio REST | Configurado en send_response.py | PASS |
| Parsing seguro de NumMedia | try/except en webhook.py | PASS |
| Guia de configuracion creada | docs/06-integrations/TWILIO-SETUP-GUIDE.md | PASS |
| Webhook sin firma devuelve 403 | `curl -X POST .../webhook` devuelve 403 | PASS |

- [x] Validacion de firma con RequestValidator
- [x] Timeout de 10s en envio REST
- [x] Parsing seguro de NumMedia
- [x] Guia de configuracion creada
- [x] Webhook sin firma devuelve 403

---

### 11. Notion

| Verificacion | Evidencia | Estado |
|-------------|----------|--------|
| 81 entradas totales en 3 DBs | 43 Backlog + 12 KB + 26 Testing | PASS |
| Backlog DB poblada (37 entradas) | 31 Hecho, 1 En progreso, 5 Backlog | PASS |
| KB Tramites DB poblada (12 entradas) | Todas con estado Verificado | PASS |
| Demo & Testing DB poblada (26 entradas) | 10 Pasa, 16 Pendiente | PASS |

- [x] 81 entradas totales en 3 DBs
- [x] Backlog DB poblada (37 entradas)
- [x] KB Tramites DB poblada (12 entradas)
- [x] Demo & Testing DB poblada (26 entradas)

---

### 12. Seguridad

| Verificacion | Evidencia | Estado |
|-------------|----------|--------|
| .env en .gitignore (4 variantes) | `grep -c '.env' .gitignore` = 4 | PASS |
| .env no rastreado en git | `git ls-files \| grep .env` sin salida | PASS |
| .env.example sin valores reales | Todos los campos sensibles vacios | PASS |
| Escaneo de 11 patrones de secretos | 0 secretos reales encontrados | PASS |
| render.yaml sin secretos hardcodeados | sync: false para valores sensibles | PASS |
| Documentacion sin tokens reales | Solo placeholders encontrados | PASS |

- [x] .env en .gitignore (4 variantes)
- [x] .env no rastreado en git
- [x] .env.example sin valores reales
- [x] Escaneo de 11 patrones de secretos limpio
- [x] render.yaml sin secretos hardcodeados
- [x] Documentacion sin tokens reales

---

### 13. Testing Completo (Fase 2)

| Verificacion | Evidencia | Estado |
|-------------|----------|--------|
| 96/96 tests pasan (91 passed + 5 xpassed) | `pytest tests/ -v --tb=short` | PASS |
| 0 errores de lint | `ruff check src/ tests/ --select E,F,W --ignore E501` | PASS |
| Script de verificacion operativo | `bash scripts/phase2_verify.sh` | PASS |
| Evidencia documentada | docs/07-evidence/PHASE-2-EVIDENCE.md | PASS |

- [x] 96/96 tests pasan (91 passed + 5 xpassed)
- [x] 0 errores de lint
- [x] Script de verificacion operativo
- [x] Evidencia documentada

---

## Resumen Consolidado

### Fase 1

| Seccion | PASS | PENDING | Total |
|---------|------|---------|-------|
| 1. Codigo | 5 | 0 | 5 |
| 2. Deploy | 5 | 0 | 5 |
| 3. Documentacion | 5 | 0 | 5 |
| 4. Notion | 4 | 0 | 4 |
| 5. GitHub | 2 | 2 | 4 |
| 6. Demo/QA | 3 | 0 | 3 |
| 7. Comunicacion | 2 | 0 | 2 |
| **Total Fase 1** | **26** | **2** | **28** |

### Fase 2

| Seccion | PASS | PENDING | Total |
|---------|------|---------|-------|
| 8. Toolkit seguridad y calidad | 8 | 0 | 8 |
| 9. Deploy y operaciones | 6 | 0 | 6 |
| 10. Twilio | 5 | 0 | 5 |
| 11. Notion | 4 | 0 | 4 |
| 12. Seguridad | 6 | 0 | 6 |
| 13. Testing completo | 4 | 0 | 4 |
| **Total Fase 2** | **33** | **0** | **33** |

### Total General

| | PASS | PENDING | Total |
|-|------|---------|-------|
| **Ambas fases** | **59** | **2** | **61** |

Los 2 items pendientes corresponden a tareas de GitHub de la Fase 1: tag release (`git tag phase-1-v1.0`) y cierre de issues (`gh issue list --state open`).

---

## Como se verifica

```bash
# Verificacion automatizada Fase 1
./scripts/phase_close.sh 1 [RENDER_URL]

# Verificacion automatizada Fase 2
bash scripts/phase2_verify.sh [RENDER_URL]

# Suite completa de tests
pytest tests/ -v --tb=short
```

## Referencias

- [Evidencia Fase 1](./PHASE-1-EVIDENCE.md)
- [Evidencia Fase 2](./PHASE-2-EVIDENCE.md)
- [Estado de Fases](./PHASE-STATUS.md)
- [Plan Fase 1](../01-phases/FASE1-IMPLEMENTACION-MVP.md)
- [Plan Fase 2](../01-phases/FASE2-HARDENING-DEPLOY-INTEGRATIONS.md)
- [Plan de Testing](../04-testing/TEST-PLAN.md)

> **Cierre automatizado:** Ejecutar `./scripts/phase_close.sh 1 [RENDER_URL]` para generar el reporte completo de cierre.
> Ubicacion del script: `scripts/phase_close.sh`
> Salida: `docs/07-evidence/phase-1-close-report.md`
