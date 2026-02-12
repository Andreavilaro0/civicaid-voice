# Checklist de Cierre — Fase 1 MVP

> **Proyecto:** CivicAid Voice / Clara
> **Fase:** 1 — MVP WhatsApp-First
> **Fecha cierre:** En progreso (2026-02-12)
> **Owner:** Equipo CivicAid
>
> **Related:** [Evidence Ledger](./PHASE-1-EVIDENCE.md) | [Phase Status](./PHASE-STATUS.md) | [FASE1 Plan](../01-phases/FASE1-IMPLEMENTACION-MVP.md)

---

## 1. Codigo

| Check | Comando | Resultado esperado | Estado |
|-------|---------|-------------------|--------|
| Todos los archivos del plan creados | `find src/ -name "*.py" \| wc -l` | 22 archivos Python | PASS |
| Todos los tests pasan | `pytest tests/ -v --tb=short` | 32/32 passed | PASS |
| Lint pasa | `ruff check src/ tests/` | 0 errors | PASS |
| Sin secretos en el codigo | `grep -r "TWILIO_AUTH\|ntn_\|sk-" src/` | 0 matches (secrets in .env only) | PASS |
| .env no commiteado | `git ls-files .env` | Not tracked | PASS |

```bash
# Ejecutar verificacion de codigo:
pytest tests/ -v --tb=short
ruff check src/ tests/
grep -r "TWILIO_AUTH\|ntn_\|sk-" src/ && echo "FAIL: secrets found" || echo "PASS: no secrets"
```

---

## 2. Deploy

| Check | Comando | Resultado esperado | Estado |
|-------|---------|-------------------|--------|
| Docker build exitoso | `docker build -t civicaid-voice .` | Successfully tagged | PASS |
| Deploy en Render exitoso | `curl -s https://civicaid-voice.onrender.com/health` | HTTP 200, JSON body | PENDING |
| /health retorna JSON OK | `curl -s [URL]/health \| python -m json.tool` | 8 component fields, status OK | PENDING |
| Twilio webhook configurado | Twilio Console > Sandbox > Webhook URL | POST https://[URL]/webhook | PENDING |
| cron-job.org activo (cada 8 min) | cron-job.org dashboard | GET [URL]/health every 8 min | PENDING |

```bash
# Ejecutar verificacion de deploy:
docker build -t civicaid-voice .
curl -s https://civicaid-voice.onrender.com/health | python -m json.tool
```

---

## 3. Documentacion

| Check | Archivo | Estado |
|-------|---------|--------|
| PHASE-STATUS.md actualizado | docs/07-evidence/PHASE-STATUS.md | PASS |
| PHASE-1-EVIDENCE.md con evidencia real | docs/07-evidence/PHASE-1-EVIDENCE.md | PASS |
| Architecture docs actualizados | docs/02-architecture/ARCHITECTURE.md | PASS |
| README.md refleja estado actual | README.md | PASS |
| Executive Summary creado | docs/00-EXECUTIVE-SUMMARY.md | PASS |

---

## 4. Notion

| Check | Accion | Estado |
|-------|--------|--------|
| Phase Releases DB actualizada | Crear entrada Phase 1 con commit SHA, URL, estado | PENDING |
| Backlog: tareas a "Hecho" | Mover D1.x, D2.x completadas a Hecho | PENDING |
| Demo & Testing: resultados | Actualizar con "Pasa"/"Falla" por test | PENDING |
| Metricas de latencia registradas | Cache <2s, TwiML ACK <1s, audio pipeline <15s | PENDING |

---

## 5. GitHub

| Check | Comando | Estado |
|-------|---------|--------|
| Commit con mensaje descriptivo | `git log -1 --oneline` | PENDING |
| Push a main | `git push origin main` | PENDING |
| Tag release | `git tag phase-1-v1.0 && git push --tags` | PENDING |
| Issues cerrados | `gh issue list --state open` | PENDING |

```bash
# Ejecutar cierre GitHub:
git add -A && git commit -m "feat: Phase 1 MVP complete — 32/32 tests, Docker, docs"
git push origin main
git tag phase-1-v1.0 && git push --tags
```

---

## 6. Demo / QA

| Check | Accion | Estado |
|-------|--------|--------|
| Demo rehearsal completado | Ejecutar guion completo de RUNBOOK-DEMO.md | PENDING |
| Video backup grabado | Screen recording del demo end-to-end | PENDING |
| Screenshots fallback listos | Capturas de /health, WA conversation, Notion | PENDING |

---

## 7. Comunicacion

| Check | Accion | Estado |
|-------|--------|--------|
| Equipo notificado del cierre | Mensaje en canal del equipo | PENDING |
| Siguiente fase planificada | Fase 2 scope definido en FASE2 doc | PENDING |

---

## Resumen

| Seccion | PASS | PENDING | Total |
|---------|------|---------|-------|
| 1. Codigo | 5 | 0 | 5 |
| 2. Deploy | 1 | 4 | 5 |
| 3. Documentacion | 5 | 0 | 5 |
| 4. Notion | 0 | 4 | 4 |
| 5. GitHub | 0 | 4 | 4 |
| 6. Demo/QA | 0 | 3 | 3 |
| 7. Comunicacion | 0 | 2 | 2 |
| **Total** | **11** | **17** | **28** |

---

> **Automated close:** Run `./scripts/phase_close.sh 1 [RENDER_URL]` to generate a full report.
> Script location: `scripts/phase_close.sh`
> Output: `docs/07-evidence/phase-1-close-report.md`
