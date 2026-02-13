# FASE 2 — Hardening, Deploy & Integrations

> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good — UDIT
> **Fecha:** 2026-02-12
> **Objetivo:** "Demo + Ops + Integrations hardened" — Llevar el MVP de Fase 1 a un estado desplegado, verificado y documentado, con observabilidad, seguridad y Notion completamente operativos.
>
> **Documentos relacionados:**
> [Plan Maestro (Fase 0)](./FASE0-PLAN-MAESTRO-FINAL.md) |
> [Implementacion MVP (Fase 1)](./FASE1-IMPLEMENTACION-MVP.md) |
> [Arquitectura](../02-architecture/ARCHITECTURE.md) |
> [Phase Status](../07-evidence/PHASE-STATUS.md)

---

## 1. Objetivo de Fase

Fase 1 entrego un MVP funcional: 93 tests verdes (88 passed + 5 xpassed) (snapshot al cierre de Fase 2; estado actual: 96 tests, 11 skills), pipeline de 11 skills completo, cache-first operativo. Pero el deploy a Render, la configuracion de Twilio, la observabilidad y la sincronizacion de Notion quedaron pendientes.

Fase 2 cierra esas brechas:

- **Deploy reproducible** en Render con health check verificado.
- **Twilio end-to-end** verificado con guia de setup.
- **Cron warm-up** documentado y operativo.
- **Notion actualizado** con todas las paginas, DBs y enlaces de evidencia.
- **QA completa** con script de verificacion automatizado y evidencia capturada.
- **Seguridad** con scan de secretos y audit de .env/.gitignore.
- **Observabilidad** con logs estructurados y metricas basicas.
- **Documentacion** actualizada para reflejar el estado post-Fase-2.

---

## 2. Alcance

### Dentro del Alcance

| # | Area | Que se hace |
|---|------|-------------|
| 1 | **Twilio** | Verificar pipeline, documentar setup de webhook, validar signature |
| 2 | **Render** | Deploy reproducible, /health verificado, render.yaml completo |
| 3 | **Cron** | Documentar setup de cron-job.org, verificar keep-alive |
| 4 | **Notion** | Actualizar 3 DBs, crear paginas de evidencia, enlaces cruzados |
| 5 | **QA** | Script de verificacion automatizado, captura de evidencia |
| 6 | **Seguridad** | Scan de secretos, audit de .env y .gitignore, validacion de tokens |
| 7 | **Observabilidad** | Logs estructurados, feature flags de toolkit, metricas basicas |
| 8 | **Documentacion** | FASE2 plan, executive summary, diagramas de deploy/ops |

### Fuera del Alcance

| Excluido | Razon |
|----------|-------|
| Cambios al pipeline de skills | Pipeline completo y testeado en Fase 1 |
| Nuevos tramites o idiomas | Fuera del alcance del hackathon |
| Base de datos relacional | JSON suficiente para 3 tramites |
| RAG con embeddings | Keyword matching suficiente para demo |
| Web Gradio como canal principal | Solo backup; WhatsApp es el canal primario |
| CI/CD avanzado (staging, canary) | Deploy directo a Render es suficiente |

---

## 3. Que cambio desde Fase 1

| Aspecto | Fase 1 | Fase 2 |
|---------|--------|--------|
| **Codigo** | Pipeline completo, 93 tests verdes (snapshot Fase 2; actual: 96) | Sin cambios al core; se agrega observabilidad y guardrails como modulos opcionales |
| **Deploy** | Pendiente | Render desplegado y verificado |
| **Twilio** | Webhook implementado, no conectado | Guia de setup, signature validation verificada |
| **Notion** | DBs creadas y populadas (75 entradas: 37+12+26) (snapshot Fase 2; actual: 81 = 43+12+26) | Paginas actualizadas con evidencia de Fase 2 |
| **Observabilidad** | Logger basico con prefijos | Logger estructurado + metricas + feature flags de toolkit |
| **Seguridad** | .gitignore basico | Scan de secretos, audit completo |
| **Documentacion** | FASE1 plan, arquitectura, runbook | FASE2 plan, executive summary actualizado, diagrama deploy/ops |
| **Transcripcion** | Whisper base local | Gemini transcription como alternativa (menos RAM) |
| **Audio respuesta** | gTTS en vivo para cache miss | gTTS como default, audios pre-hosted para cache hits |

---

## 4. Gates

### P2.1 — Twilio Pipeline Verified

| # | Criterio | DoD | Evidencia |
|---|----------|-----|-----------|
| P2.1.1 | Twilio credentials documentadas | Guia de setup en docs/ | Archivo existente con instrucciones |
| P2.1.2 | Signature validation funcional | Test pasa con firma valida e invalida | pytest output |
| P2.1.3 | Webhook flow documentado | Diagrama de secuencia actualizado | Mermaid diagram |
| P2.1.4 | REST API send verificado | Twilio client wrapper testeado | pytest output |

### P2.2 — Render Deploy Reproducible

| # | Criterio | DoD | Evidencia |
|---|----------|-----|-----------|
| P2.2.1 | render.yaml completo | Todas las env vars declaradas | Archivo render.yaml |
| P2.2.2 | Dockerfile funcional | `docker build` exitoso | Build log |
| P2.2.3 | /health accesible | curl retorna JSON con todos los componentes | curl output |
| P2.2.4 | Deploy reproducible | Instrucciones paso a paso documentadas | Guia en docs/ |

### P2.3 — Cron Warm-Up Operational

| # | Criterio | DoD | Evidencia |
|---|----------|-----|-----------|
| P2.3.1 | Cron setup documentado | Instrucciones para cron-job.org | Guia en docs/ |
| P2.3.2 | Frecuencia correcta | Cada 14 minutos al /health | Configuracion documentada |
| P2.3.3 | Cold start mitigado | Render no duerme con cron activo | Explicacion tecnica |

### P2.4 — Notion Fully Updated

| # | Criterio | DoD | Evidencia |
|---|----------|-----|-----------|
| P2.4.1 | 3 DBs actualizadas | Backlog, KB Tramites, Demo & Testing con datos actuales | Notion page IDs |
| P2.4.2 | Paginas de evidencia | Enlaces a logs, outputs, reportes | Links en Notion |
| P2.4.3 | Estado de fases actualizado | Fase 1 y Fase 2 con estado correcto | Notion entries |

### P2.5 — Evidencia QA Completa

| # | Criterio | DoD | Evidencia |
|---|----------|-----|-----------|
| P2.5.1 | Script de verificacion | Script automatizado que valida gates | Archivo en scripts/ |
| P2.5.2 | Tests pasan | 93+ tests verdes | pytest output |
| P2.5.3 | Lint limpio | ruff sin errores criticos | ruff output |
| P2.5.4 | Evidencia capturada | Salidas guardadas en docs/07-evidence/ | Archivos de evidencia |

### P2.6 — Escaneo de Seguridad

| # | Criterio | DoD | Evidencia |
|---|----------|-----|-----------|
| P2.6.1 | Scan de secretos | No hay secretos en el repositorio | Scan output |
| P2.6.2 | .gitignore completo | .env, __pycache__, .pyc, etc. excluidos | .gitignore content |
| P2.6.3 | Tokens seguros | Tokens en env vars, no hardcodeados | grep output |
| P2.6.4 | Dependencias auditadas | No hay vulnerabilidades criticas conocidas | pip audit o similar |

---

## 5. Dependencias entre Gates

```
P2.1 (Twilio) ────────────────────────────────┐
P2.2 (Render) ──→ P2.3 (Cron)                 │
P2.4 (Notion) ─────────────────────────────────┤
P2.5 (QA) ─────────────────────────────────────┤──→ P2.SYNC (Final)
P2.6 (Seguridad) ── bloqueado por P2.1 + P2.2 ─┤
P2.OBS (Observability) ────────────────────────┤
P2.VIS (Docs + Diagrams) ─────────────────────┘
```

P2.SYNC (Final Sync) es el gate de cierre que consolida toda la evidencia y actualiza PHASE-STATUS.md. Solo se ejecuta cuando todos los demas gates estan completos o documentados.

---

## 6. Asignacion de Equipos

| # | Agente | Gate | Alcance de archivos | Salidas |
|---|--------|------|-------------------|---------|
| 1 | **Integrations** | P2.1 | src/routes/webhook.py (read-only), docs/ | Guia de Twilio setup, verificacion de pipeline |
| 2 | **DevOps** | P2.2, P2.3 | Dockerfile, render.yaml, scripts/ | Deploy verificado, cron documentado |
| 3 | **QA** | P2.5 | tests/, scripts/, docs/07-evidence/ | Script de verificacion, evidencia capturada |
| 4 | **Notion/PMO** | P2.4 | docs/06-integrations/, Notion MCP | DBs actualizadas, paginas de evidencia |
| 5 | **Comms/Visuals** | P2.VIS, P2.PLAN | docs/00-*, docs/01-phases/, docs/02-architecture/ | Este documento, executive summary, diagramas |
| 6 | **Observability** | P2.OBS | src/utils/observability.py, src/core/guardrails.py | Logs estructurados, metricas, guardrails |
| 7 | **Security** | P2.6 | .gitignore, .env (audit), src/ (scan) | Scan de secretos, audit de seguridad |

**Regla:** El lead solo coordina y sintetiza. Todo trabajo lo hacen los teammates. Ningun teammate edita fuera de su scope.

---

## 7. Entregables

| # | Entregable | Responsable | Estado |
|---|-------------|-------|--------|
| 1 | render.yaml completo + Dockerfile verificado | DevOps | En progreso |
| 2 | Guia de configuracion del webhook de Twilio | Integrations | En progreso |
| 3 | Guia de configuracion de cron-job.org | DevOps | Pendiente |
| 4 | Script de verificacion (verify.sh o similar) | QA | En progreso |
| 5 | Notion 3 DBs actualizadas con evidencia Fase 2 | Notion/PMO | En progreso |
| 6 | FASE2-HARDENING-DEPLOY-INTEGRATIONS.md (este doc) | Comms/Visuals | En progreso |
| 7 | Resumen Ejecutivo actualizado | Comms/Visuals | En progreso |
| 8 | Diagrama deploy-ops-flow.mmd | Comms/Visuals | En progreso |
| 9 | observability.py + guardrails.py | Observability | En progreso |
| 10 | Reporte de escaneo de seguridad | Security | Pendiente |
| 11 | PHASE-STATUS.md actualizado | Sync | Pendiente |
| 12 | PHASE-CLOSE-CHECKLIST.md para Fase 2 | Sync | Pendiente |

---

## 8. Cronograma

Fase 2 se ejecuta en una **sesion unica** el 12 de Febrero de 2026, inmediatamente despues de cerrar el codigo de Fase 1.

```
Fase 1 (codigo) ──DONE──> Fase 2 (hardening) ──> Demo rehearsal ──> Presentacion
                           ↑ Estamos aqui
```

Todos los gates de Fase 2 se ejecutan en paralelo donde sea posible, con P2.SYNC como paso final de consolidacion.

---

## 9. Observabilidad (Toolkit Phase 2)

Fase 2 introdujo modulos opcionales de toolkit controlados por feature flags:

| Flag | Default | Modulo | Descripcion |
|------|---------|--------|-------------|
| `OBSERVABILITY_ON` | true | `src/utils/observability.py` | Logs estructurados con contexto de request |
| `STRUCTURED_OUTPUT_ON` | false | Pipeline output | Outputs JSON estructurados del LLM |
| `GUARDRAILS_ON` | true | `src/core/guardrails.py` | Validacion de inputs y outputs |
| `RAG_ENABLED` | false | Stub | RAG placeholder para futuras fases |

Estos modulos son **aditivos** y no modifican el pipeline existente de 11 skills. Se activan via variables de entorno en render.yaml.

---

## 10. Riesgos Fase 2

| # | Riesgo | Probabilidad | Impacto | Mitigacion |
|---|--------|-------------|---------|------------|
| R1 | Deploy a Render falla por RAM | Media | Alto | WHISPER_ON=false en render.yaml; usar Gemini transcription |
| R2 | Twilio sandbox expirado | Baja | Critico | Re-enviar join code; tener screenshots backup |
| R3 | Notion MCP no responde | Media | Medio | Script populate_notion.sh como fallback |
| R4 | cron-job.org no esta configurado a tiempo | Baja | Medio | Warm-up manual T-15 antes de demo |
| R5 | Secretos expuestos en repo | Baja | Critico | Scan pre-commit; .gitignore robusto |

---

## 11. Criterio de Cierre

Fase 2 se considera cerrada cuando:

1. Todos los gates P2.1 a P2.6 tienen evidencia documentada (PASS o DOCUMENTED-BLOCKED).
2. PHASE-STATUS.md refleja el estado actual de todos los gates.
3. Executive Summary actualizado con seccion de Fase 2.
4. Notion 3 DBs actualizadas.
5. Ningun secreto expuesto en el repositorio.
6. Script de verificacion ejecutado y evidencia capturada.

---

> **FIN DEL PLAN FASE 2.**
> **Proxima accion:** Cada agente ejecuta su gate asignado. P2.SYNC consolida al final.
