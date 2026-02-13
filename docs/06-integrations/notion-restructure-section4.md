# SECCION 4 — PAGINAS POR FASE (F1, F2, F3)

> **Documento:** Reestructuracion Notion OS — Seccion 4
> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good — UDIT
> **Fecha:** 2026-02-13
> **Autor:** Agent C (Technical Writer)
>
> **Paginas Notion existentes:**
> - F0+F1: `305c5a0f-372a-81c8-b609-cc5fe793bfe4`
> - F2: `305c5a0f-372a-813b-8915-f7e6c21fd055`
> - F3: `305c5a0f-372a-818d-91a7-f59c22551350`

---

## Indice de esta seccion

1. [Pagina Fase 1 — MVP WhatsApp-First](#pagina-fase-1--mvp-whatsapp-first)
2. [Pagina Fase 2 — Hardening, Deploy e Integraciones](#pagina-fase-2--hardening-deploy-e-integraciones)
3. [Pagina Fase 3 — Demo en Vivo, Ops Reales y Presentacion](#pagina-fase-3--demo-en-vivo-ops-reales-y-presentacion)
4. [Vista Timeline: Todas las fases](#vista-timeline-todas-las-fases)
5. [Tabla comparativa cross-fase](#tabla-comparativa-cross-fase)

---

---

# PAGINA FASE 1 — MVP WhatsApp-First

---

## Header

| Campo | Valor |
|-------|-------|
| **Fase** | F1 — Implementacion MVP "Clara" |
| **Fechas** | 2026-02-12 (inicio y cierre en una sola sesion) |
| **Estado** | COMPLETADA |
| **Commit SHA** | `c6a896e` |
| **Notion Page ID** | `305c5a0f-372a-81c8-b609-cc5fe793bfe4` (compartida con F0) |
| **Responsables** | Robert (Backend lead), Marcos (Routes/Twilio/Deploy), Lucas (KB/Testing) |
| **Documento fuente** | `docs/01-phases/FASE1-IMPLEMENTACION-MVP.md` |

---

## Objetivo

Entregar un MVP funcional end-to-end: un usuario envia un mensaje de texto o audio por WhatsApp y recibe una respuesta util sobre tramites (IMV, empadronamiento, tarjeta sanitaria) en menos de 20 segundos, con cache-first para fiabilidad de demo, pipeline de 11 skills, logs estructurados, health endpoint y deploy estable en Render.

---

## Entregables

| # | Entregable | Descripcion | Responsable | Estado |
|---|------------|-------------|-------------|--------|
| E1.1 | Repositorio + estructura | `src/`, `tests/`, `data/`, `docs/`, `scripts/` creados | Robert | Hecho |
| E1.2 | `config.py` con 6 feature flags | Dataclass Config con DEMO_MODE, LLM_LIVE, WHISPER_ON, LLM_TIMEOUT, WHISPER_TIMEOUT, AUDIO_BASE_URL | Robert | Hecho |
| E1.3 | Logger estructurado | Prefijos `[ACK]`, `[CACHE]`, `[WHISPER]`, `[LLM]`, `[REST]`, `[ERROR]` | Robert | Hecho |
| E1.4 | `demo_cache.json` (8 entradas) | 8 respuestas pre-calculadas con patterns e idioma (ES, FR) | Robert | Hecho |
| E1.5 | 6 audios MP3 pre-generados | `imv_es.mp3`, `empadronamiento_es.mp3`, `tarjeta_es.mp3`, `ahmed_fr.mp3`, `fatima_fr.mp3`, `maria_es.mp3` | Robert | Hecho |
| E1.6 | Cache engine + skill cache_match | Cache match por keyword con soporte multilingue | Robert | Hecho |
| E1.7 | Flask app + health endpoint | `/health` retorna JSON con 8 componentes de estado | Marcos | Hecho |
| E1.8 | Webhook TwiML ACK | `POST /webhook` retorna TwiML XML en <1s, procesamiento en hilo de fondo | Marcos | Hecho |
| E1.9 | Servicio de archivos estaticos | `GET /static/cache/*.mp3` sirve audios pre-generados | Marcos | Hecho |
| E1.10 | Twilio client + send_response | Wrapper REST con timeout 10s y retry sin media en caso de fallo | Marcos | Hecho |
| E1.11 | Pipeline completo (texto + cache) | Pipeline orquesta 11 skills secuencialmente | Marcos | Hecho |
| E1.12 | KB tramites (3 JSONs) | `imv.json`, `empadronamiento.json`, `tarjeta_sanitaria.json` con fuentes oficiales | Lucas | Hecho |
| E1.13 | CI workflow (GitHub Actions) | `pytest` + `ruff` en push a main y PRs | Robert | Hecho |
| E1.14 | Pipeline audio completo | fetch_media + convert_audio + transcribe + detect_lang | Marcos | Hecho |
| E1.15 | Skills de generacion | kb_lookup + llm_generate + verify_response con anti-alucinacion | Robert | Hecho |
| E1.16 | Suite de tests (32) | Unit (21) + Integration (7) + E2E (4) = 32 tests | Lucas | Hecho |

---

## Gates

### Gate G0 — Tooling Listo

| # | Criterio | DoD | Evidencia | Estado |
|---|----------|-----|-----------|--------|
| G0.1 | 15 skills instaladas | Lista visible en Claude Code | `claude skills list` -> 15 skills cargadas | PASS |
| G0.2 | 8 agentes configurados | 5 globales + 3 de proyecto | `ls .claude/agents/` -> notion-ops.md, ci-bot.md, twilio-integrator.md | PASS |
| G0.3 | NOTION_TOKEN configurado | MCP Notion responde | `grep NOTION_TOKEN .env` -> ntn_... presente | PASS |
| G0.4 | GITHUB_TOKEN configurado | `gh auth status` exitoso | No encontrado en .env | PENDING |
| G0.5 | .env con valores reales | Variables criticas con valor | TWILIO_*, GEMINI_API_KEY presentes | PASS |
| G0.6 | Notion OS (3 DBs) creadas | 3 databases visibles en Notion | Backlog/Issues, KB Tramites, Demo & Testing existen | PASS |

**Veredicto G0:** 5/6 PASS (GITHUB_TOKEN pendiente, no bloqueante)

### Gate G1 — Texto OK

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| G1.1 | POST /webhook retorna TwiML ACK <1s | `pytest tests/integration/test_webhook.py -v` -> T6-T7 PASSED | PASS |
| G1.2 | WA texto cache hit funciona | `pytest tests/e2e/test_demo_flows.py -v` -> T9-T10 PASSED | PASS |
| G1.3 | Respuesta incluye audio MP3 | FinalResponse.media_url rellenado | PASS |
| G1.4 | /health retorna JSON | 200 OK, JSON con 8 campos de componentes | PASS |
| G1.5 | 32/32 tests pasan | `pytest tests/ -v --tb=short` -> 32 passed en ~2s | PASS |
| G1.6 | CI workflow funcional | `.github/workflows/ci.yml` se dispara en push + PRs | PASS |
| G1.7 | Deploy Render exitoso | `curl .../health` -> 200 OK, cache_entries=8 | PASS |

**Veredicto G1:** 7/7 PASS

### Gate G2 — Audio OK

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| G2.1 | Audio pipeline implementado | fetch_media -> convert_audio -> transcribe -> detect_lang -> cache/llm | PASS |
| G2.2 | Whisper timeout enforced (12s) | ThreadPoolExecutor + WHISPER_TIMEOUT en transcribe.py | PASS |
| G2.3 | LLM timeout (6s) | request_options con LLM_TIMEOUT en llm_generate.py | PASS |
| G2.4 | 32/32 tests pasan | `pytest tests/ -v --tb=short` -> 32 passed | PASS |
| G2.5 | Test real con audio en Render | Flujos WOW 1 + WOW 2 verificados via WhatsApp real | PASS |

**Veredicto G2:** 5/5 PASS

### Gate G3 — Demo Listo

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| G3.1 | Deploy en Render | `curl .../health` -> 200 OK, cache_entries=8 | PASS |
| G3.2 | Webhook Twilio configurado | POST https://civicaid-voice.onrender.com/webhook | PASS |
| G3.3 | cron-job.org activo (14 min) | GET /health cada 14 min | PASS |
| G3.4 | Test real WA desde movil | Flujos WOW 1 + WOW 2 verificados | PASS |
| G3.5 | Ensayo de demo completado | Guion ejecutado, flujos verificados | PASS |
| G3.6 | Video de backup grabado | Video de backup disponible | PASS |

**Veredicto G3:** 6/6 PASS

---

## Metricas

| Metrica | Valor |
|---------|-------|
| Tests totales | 32 |
| Tests passed | 32/32 (100%) |
| Tests unitarios | 21 |
| Tests integracion | 7 |
| Tests E2E | 4 |
| Skills en pipeline | 11 (detect_input, fetch_media, convert_audio, transcribe, detect_lang, cache_match, kb_lookup, llm_generate, verify_response, send_response, tts) |
| Feature flags | 6 (DEMO_MODE, LLM_LIVE, WHISPER_ON, LLM_TIMEOUT, WHISPER_TIMEOUT, AUDIO_BASE_URL) |
| Cache entries | 8 respuestas pre-calculadas |
| Audios MP3 | 6 archivos |
| KB tramites | 3 JSONs (IMV, empadronamiento, tarjeta sanitaria) |
| Deploy | Render free tier, region Frankfurt (EU) |
| Latencia cache | <2s |
| Latencia TwiML ACK | <1s |
| Tareas completadas (D1.x) | 14/14 Hecho |

---

## Vistas embebidas (Linked Views)

### Vista Backlog filtrada por Gate F1

> **Instrucciones Notion:** Crear un Linked View de la base de datos **Backlog/Issues** con filtro `Gate = G0 OR G1 OR G2 OR G3` y vista tipo Tabla agrupada por Gate.

| Filtro | Valor |
|--------|-------|
| Base de datos | Backlog/Issues |
| Filtro Gate | `G0`, `G1`, `G2`, `G3` |
| Agrupacion | Por Gate |
| Ordenacion | Por ID de tarea (D1.1 ... D3.5) |
| Vista | Tabla |

### Vista Testing filtrada por Fase 1

> **Instrucciones Notion:** Crear un Linked View de la base de datos **Demo & Testing** con filtro `Phase = F1` y vista tipo Tabla.

| Filtro | Valor |
|--------|-------|
| Base de datos | Demo & Testing |
| Filtro Phase | `F1` |
| Columnas visibles | ID, Test, Resultado (Pasa/Falla), Latencia, Fecha |
| Vista | Tabla |

---

## Lecciones aprendidas

1. **Cache-first fue la decision mas acertada de F1.** Garantizar respuestas deterministas en modo demo elimino el riesgo de fallos de LLM o red durante la presentacion. Las 8 entradas de cache cubrieron los flujos criticos (WOW 1 y WOW 2) con latencia <2s.

2. **El patron TwiML ACK + hilo de fondo resolvio el problema de timeout de Twilio.** Twilio espera respuesta en <15s, pero el pipeline completo (transcripcion + LLM + TTS) puede tardar 10-20s. Responder con ACK inmediato y procesar en background fue la clave arquitectonica.

3. **Tener 32 tests desde el dia 1 evito regresiones en fases posteriores.** La suite de tests de F1 sirvio como red de seguridad cuando se anadieron guardrails, observabilidad y structured outputs en F2, detectando inmediatamente cualquier rotura del pipeline core.

---

## Enlace a evidencia

- **Documento completo:** `docs/07-evidence/PHASE-1-EVIDENCE.md`
- **Reporte automatizado de cierre:** `docs/07-evidence/phase-1-close-report.md`
- **Script de cierre:** `scripts/phase_close.sh 1 [RENDER_URL]`

---

---

# PAGINA FASE 2 — Hardening, Deploy e Integraciones

---

## Header

| Campo | Valor |
|-------|-------|
| **Fase** | F2 — Hardening, Deploy & Integrations |
| **Fechas** | 2026-02-12 (sesion unica, inmediatamente despues de F1) |
| **Estado** | COMPLETADA |
| **Commit SHA** | `ec05382` |
| **Notion Page ID** | `305c5a0f-372a-813b-8915-f7e6c21fd055` |
| **Responsables** | Robert (Backend lead), Marcos (DevOps/Deploy), Lucas (QA/Testing), Andrea (Notion/PMO) |
| **Documento fuente** | `docs/01-phases/FASE2-HARDENING-DEPLOY-INTEGRATIONS.md` |

---

## Objetivo

Llevar el MVP funcional de Fase 1 a un estado desplegado, verificado y documentado. Cerrar las brechas de deploy en Render, configuracion de Twilio, observabilidad, seguridad y sincronizacion de Notion. Consolidar la suite de tests de 32 a 93 con guardrails, red team, structured outputs y observabilidad.

---

## Entregables

| # | Entregable | Descripcion | Responsable | Estado |
|---|------------|-------------|-------------|--------|
| E2.1 | render.yaml completo + Dockerfile verificado | 16 env vars (3 secretas + 13 valores), Docker build exitoso | Marcos (DevOps) | Hecho |
| E2.2 | Guia de configuracion Twilio | `docs/06-integrations/TWILIO-SETUP-GUIDE.md` con 15 pasos | Integrations | Hecho |
| E2.3 | Guia de configuracion cron-job.org | Documentado en RUNBOOK-PHASE2.md Seccion 5 (cada 14 min) | Marcos (DevOps) | Hecho |
| E2.4 | Script de verificacion | `scripts/phase2_verify.sh` — pytest + ruff + docker + health | Lucas (QA) | Hecho |
| E2.5 | Notion 3 DBs actualizadas | 75 entradas: 37 Backlog + 12 KB Tramites + 26 Demo & Testing | Andrea (Notion/PMO) | Hecho |
| E2.6 | Plan Fase 2 documentado | `FASE2-HARDENING-DEPLOY-INTEGRATIONS.md` con 6 gates | Comms/Visuals | Hecho |
| E2.7 | Resumen Ejecutivo actualizado | `docs/00-EXECUTIVE-SUMMARY.md` con seccion de Fase 2 | Comms/Visuals | Hecho |
| E2.8 | Diagrama deploy-ops-flow.mmd | Flujo de deploy y operaciones en Mermaid | Comms/Visuals | Hecho |
| E2.9 | Modulos de observabilidad | `observability.py` (RequestContext + timings) + `guardrails.py` (pre/post check) | Observability | Hecho |
| E2.10 | Reporte de escaneo de seguridad | 11 patrones escaneados, 0 secretos reales encontrados | Security | Hecho |
| E2.11 | PHASE-STATUS.md actualizado | Estado de todas las fases y gates | Sync | Hecho |
| E2.12 | PHASE-CLOSE-CHECKLIST.md | Checklist de cierre Fases 1 y 2 | Sync | Hecho |

---

## Gates

### P2.1 — Twilio Pipeline Verificado

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P2.1.1 | Validacion de firma de webhook | `RequestValidator` en webhook.py L7, L33, L35 | PASS |
| P2.1.2 | Envio REST con timeout 10s | `timeout=10` en send_response.py L15 | PASS |
| P2.1.3 | Parsing seguro de NumMedia | try/except en webhook.py L44-47 | PASS |
| P2.1.4 | Guia de configuracion Twilio | `docs/06-integrations/TWILIO-SETUP-GUIDE.md` creada | PASS |

**Veredicto P2.1:** 4/4 PASS

### P2.2 — Render Deploy Reproducible

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P2.2.1 | Dockerfile compila | `docker build -t civicaid-voice:test .` exitoso | PASS |
| P2.2.2 | render.yaml usa sync: false para secretos | TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, GEMINI_API_KEY | PASS |
| P2.2.3 | /health devuelve JSON | `curl .../health` -> 200 OK, `{"status":"ok","cache_entries":8}` | PASS |
| P2.2.4 | .dockerignore presente | Excluye .env, .git, docs, tests | PASS |

**Veredicto P2.2:** 4/4 PASS

### P2.3 — Cron Warm-Up Documentado

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P2.3.1 | Configuracion documentada | Seccion 5 de RUNBOOK-PHASE2.md | PASS |
| P2.3.2 | Intervalo correcto (14 min) | Previene cold start de Render free tier (15 min sleep) | PASS |

**Veredicto P2.3:** 2/2 PASS

### P2.4 — Notion Completamente Actualizado

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P2.4.1 | 3 DBs pobladas | 75 entradas totales | PASS |
| P2.4.2 | Backlog DB: 37 entradas | 31 Hecho, 1 En progreso, 5 Backlog | PASS |
| P2.4.3 | KB Tramites DB: 12 entradas | Todas con estado Verificado | PASS |
| P2.4.4 | Demo & Testing DB: 26 entradas | 10 Pasa, 16 Pendiente | PASS |

**Veredicto P2.4:** 4/4 PASS

### P2.5 — Script de Verificacion + Evidencia QA

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P2.5.1 | Script de verificacion | `scripts/phase2_verify.sh` operativo | PASS |
| P2.5.2 | 93/93 tests pasan | 88 passed + 5 xpassed en 1.27s | PASS |
| P2.5.3 | Lint limpio | `ruff check` -> 0 errores | PASS |

**Veredicto P2.5:** 3/3 PASS

### P2.6 — Escaneo de Seguridad

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P2.6.1 | Scan de 11 patrones de secretos | 0 secretos reales encontrados | PASS |
| P2.6.2 | .gitignore completo (4 variantes .env) | `.env`, `.env.local`, `.env.production`, `.env.*.local` | PASS |
| P2.6.3 | .env no rastreado en git | `git ls-files | grep .env` -> sin salida | PASS |
| P2.6.4 | .env.example sin valores reales | Todos los campos sensibles vacios o placeholder | PASS |
| P2.6.5 | render.yaml sin secretos | `sync: false` para valores sensibles | PASS |
| P2.6.6 | Documentacion sin tokens reales | Solo placeholders (ntn_xxx, etc.) | PASS |
| P2.6.7 | .dockerignore existe y excluye .env | Presente y correcto | PASS |

**Veredicto P2.6:** 7/7 PASS

---

## Metricas

| Metrica | Valor F1 | Valor F2 | Delta |
|---------|----------|----------|-------|
| Tests totales | 32 | 93 | +61 (+190%) |
| Tests unitarios | 21 | 75 | +54 |
| Tests integracion | 7 | 8 | +1 |
| Tests E2E | 4 | 4 | 0 |
| Tests red team (xpassed) | 0 | 5 | +5 |
| Skills en pipeline | 11 | 11 | 0 |
| Feature flags | 6 | 9 | +3 (OBSERVABILITY_ON, STRUCTURED_OUTPUT_ON, GUARDRAILS_ON) |
| Entradas Notion | — | 75 (37+12+26) | +75 |
| Deploy | Pendiente | Render verificado | Completado |
| Seguridad | .gitignore basico | 11 patrones escaneados, 0 secretos | Completado |
| Observabilidad | Logger con prefijos | RequestContext + timings + feature flags | Completado |

### Archivos de test nuevos en Fase 2

| Archivo | Tests | Cobertura |
|---------|-------|-----------|
| `tests/unit/test_evals.py` | 9 | Eval runner, casos de evaluacion, reportes |
| `tests/unit/test_guardrails.py` | 19 | Pre-check bloqueadores, post-check disclaimers, redaccion PII |
| `tests/unit/test_observability.py` | 6 | RequestContext, timings, thread-local, feature flag |
| `tests/unit/test_redteam.py` | 9 (5 xpassed) | Archivo red team, prompts adversariales contra guardrails |
| `tests/unit/test_retriever.py` | 7 | Interfaz Retriever abstracta, JSON KB retriever, factory |
| `tests/unit/test_structured_outputs.py` | 11 | Modelo Pydantic, parsing JSON, fallbacks, display |

---

## Vistas embebidas (Linked Views)

### Vista Backlog filtrada por Gates F2

> **Instrucciones Notion:** Crear un Linked View de la base de datos **Backlog/Issues** con filtro `Gate = P2.1 OR P2.2 OR P2.3 OR P2.4 OR P2.5 OR P2.6` y vista tipo Tabla agrupada por Gate.

| Filtro | Valor |
|--------|-------|
| Base de datos | Backlog/Issues |
| Filtro Gate | `P2.1`, `P2.2`, `P2.3`, `P2.4`, `P2.5`, `P2.6` |
| Agrupacion | Por Gate |
| Ordenacion | Por ID de entregable |
| Vista | Tabla |

### Vista Testing filtrada por Fase 2

> **Instrucciones Notion:** Crear un Linked View de la base de datos **Demo & Testing** con filtro `Phase = F2` y vista tipo Tabla.

| Filtro | Valor |
|--------|-------|
| Base de datos | Demo & Testing |
| Filtro Phase | `F2` |
| Columnas visibles | ID, Test, Resultado, Suite (unit/integration/e2e/redteam), Delta vs F1 |
| Vista | Tabla |

---

## Lecciones aprendidas

1. **Los guardrails son imprescindibles desde el primer momento.** Se implementaron 19 tests de guardrails (pre-check para contenido danino + post-check para disclaimers legales/medicos + redaccion PII) que bloquearon 5 vectores adversariales de red team. En un proyecto de impacto social con poblaciones vulnerables, esta capa de seguridad no es opcional.

2. **El escaneo de seguridad debe ser automatizado y repetible.** Escanear 11 patrones de secretos en todos los archivos rastreados de forma sistematica es mucho mas fiable que revisiones manuales. El resultado fue 0 secretos filtrados, pero el proceso importa tanto como el resultado.

3. **Llevar los tests de 32 a 93 en una sola sesion fue posible gracias a la arquitectura modular.** Cada modulo nuevo (guardrails, observability, structured outputs, retriever, evals) tenia una interfaz clara y tests independientes. La arquitectura de skills aisladas facilito testear cada componente sin afectar el pipeline core.

---

## Enlace a evidencia

- **Documento completo:** `docs/07-evidence/PHASE-2-EVIDENCE.md`
- **Script de verificacion:** `scripts/phase2_verify.sh`
- **Checklist de cierre:** `docs/07-evidence/PHASE-CLOSE-CHECKLIST.md`

---

---

# PAGINA FASE 3 — Demo en Vivo, Ops Reales y Presentacion

---

## Header

| Campo | Valor |
|-------|-------|
| **Fase** | F3 — Demo en Vivo, Operaciones Reales y Presentacion |
| **Fechas** | 2026-02-12 (inicio) — 2026-02-13 (cierre) |
| **Estado** | COMPLETADA |
| **Commit SHA** | `77d5f88` |
| **Notion Page ID** | `305c5a0f-372a-818d-91a7-f59c22551350` |
| **Responsables** | Robert (Backend/Demo lead), Marcos (DevOps/Twilio), Lucas (QA), Daniel (Video), Andrea (Notion/Slides) |
| **Documento fuente** | `docs/01-phases/FASE3-DEMO-OPS-REAL.md` |

---

## Objetivo

Convertir el MVP desplegado y verificado de las Fases 1-2 en una presentacion convincente de 6-8 minutos ante el jurado del hackathon OdiseIA4Good. Ejecutar 2 momentos WOW en vivo (texto espanol + audio frances), verificar Twilio WhatsApp real end-to-end, crear runbook de 8 incidentes, implementar logging JSON con request_id, y completar QA Deep Audit con 96 tests.

---

## Entregables

| # | Entregable | Descripcion | Responsable | Estado |
|---|------------|-------------|-------------|--------|
| E3.1 | Twilio WhatsApp real E2E | Sandbox configurado, signature validation activa (403), checklist 15 pasos | Marcos | Hecho |
| E3.2 | Deploy ops demo-grade | Health <2s, cron 14 min, feature flags configurados, logs operativos | Marcos | Hecho |
| E3.3 | Runbook de incidentes | `docs/03-runbooks/RUNBOOK-PHASE3.md` con 8 escenarios (INC-01 a INC-08) | Marcos | Hecho |
| E3.4 | Script phase3_verify.sh | 7 pasos: pytest + ruff + docker build + docker /health + Render + webhook + Twilio smoke | Lucas | Hecho |
| E3.5 | Logging JSON | JSONFormatter con request_id + timings por stage en logger.py | Robert | Hecho |
| E3.6 | Observabilidad demo-grade | Hook before/after_request, OBS_SUMMARY con request_id y timings | Robert | Hecho |
| E3.7 | Notion PMO actualizado | 81 entradas (43 Backlog + 12 KB + 26 Testing), owners asignados (97.7%) | Andrea | Hecho |
| E3.8 | Guion demo 6-8 min | Timeline con cues MUESTRO/DIGO/EVIDENCIA, concepto Ciudadano-first | Robert | Hecho |
| E3.9 | WOW 1 + WOW 2 definidos | WOW 1: Maria texto IMV (<2s) / WOW 2: Ahmed audio frances (~10s) | Robert | Hecho |
| E3.10 | 1-pager para jurado | `docs/00-EXECUTIVE-SUMMARY.md` actualizado | Robert | Hecho |
| E3.11 | QA Deep Audit (P3.Q1-Q7) | Claims matrix (42 claims, 34 verified), 12 contradicciones detectadas, 11 corregidas | Lucas | Hecho |
| E3.12 | Suite de tests (96) | 91 passed + 5 xpassed, incluyendo 3 tests nuevos de transcribe | Lucas | Hecho |

---

## Gates

### P3.1 — Twilio WhatsApp Real End-to-End

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.1.1 | Texto en espanol funciona en vivo | "Que es el IMV?" -> cache HIT imv_es -> respuesta correcta | PASS |
| P3.1.2 | Audio en frances funciona en vivo | Nota de voz -> transcripcion Gemini -> respuesta en frances | PASS |
| P3.1.3 | Audio MP3 se reproduce en WhatsApp | `curl -I .../static/cache/imv_es.mp3` -> HTTP 200, audio/mpeg, 163584 bytes | PASS |
| P3.1.4 | Latencia cache <2s | Logs con timing: cache match en 479ms | PASS |
| P3.1.5 | Validacion firma activa | curl sin firma -> 403 Forbidden | PASS |
| P3.1.6 | Pipeline codigo verificado | webhook -> pipeline -> REST, todos los skills encadenados | PASS |

**Veredicto P3.1:** 6/6 PASS

### P3.2 — Deploy y Ops Demo-Grade

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.2.1 | Render activo sin cold start | /health avg 101ms (3 requests: 93ms, 120ms, 88ms) | PASS |
| P3.2.2 | Cron warm-up operativo | cron-job.org cada 14 min, GET /health | PASS |
| P3.2.3 | Feature flags configurados | DEMO_MODE=true, LLM_LIVE=true en Render | PASS |
| P3.2.4 | Logs operativos para debug | Tags: ACK, CACHE, LLM, OBS, ERROR en JSON | PASS |
| P3.2.5 | 3 estrategias cold-start documentadas | cron-job.org (elegida) + Render paid + keep-warm | PASS |
| P3.2.6 | Runbook 8 incidentes | INC-01 a INC-08 con diagnostico + remediacion | PASS |
| P3.2.7 | Cron configurado y documentado | cron-job.org, */14 * * * *, GET, timeout 30s | PASS |
| P3.2.8 | Smoke test post-deploy (5 checks) | Health 200 + MP3 200 + Webhook 403 + <1s + Live | PASS |

**Veredicto P3.2:** 8/8 PASS

### P3.3 — QA y Evidencia

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.3.1 | 96 tests pasan | 91 passed + 5 xpassed en 0.87s (phase3-verify-FINAL.txt) | PASS |
| P3.3.2 | Lint limpio | `ruff check` -> All checks passed | PASS |
| P3.3.3 | Docker build OK | `civicaid-voice:phase3` construida exitosamente | PASS |
| P3.3.4 | Docker /health OK | status=ok, cache_entries=8 | PASS |
| P3.3.5 | Script phase3_verify.sh | 4/4 pasos PASS (pytest + ruff + docker build + docker health) | PASS |
| P3.3.6 | Evidencia capturada | `docs/07-evidence/phase3-verify-output.txt` | PASS |

**Veredicto P3.3:** 6/6 PASS

### P3.4 — Observabilidad Demo-Grade

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.4.1 | JSON logging activo | JSONFormatter emite JSON valido por linea | PASS |
| P3.4.2 | request_id en cada peticion | UUID generado via RequestContext (observability.py L18) | PASS |
| P3.4.3 | Timings por skill | @timed decorator alimenta RequestContext.timings | PASS |
| P3.4.4 | OBS_SUMMARY emitido | after_request hook emite JSON con request_id + http_total_ms + timings | PASS |
| P3.4.5 | 93/93 tests retrocompatibles | Refactor de logging no rompio ningun test existente | PASS |
| P3.4.6 | Guia "como leer logs" | Tags ACK, CACHE, LLM, OBS, ERROR documentados | PASS |

**Veredicto P3.4:** 6/6 PASS

### P3.5 — Notion PMO Actualizado

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.5.1 | 3 DBs consistentes con datos actuales | 81 entradas (43 Backlog + 12 KB + 26 Testing) | PASS |
| P3.5.2 | Estado Fase 3 reflejado | Entradas P3.x creadas en Backlog | PASS |
| P3.5.3 | Owners asignados | 97.7% de entradas con owner | PASS |
| P3.5.4 | Pagina Phase 3 Demo Ready creada | ID: 305c5a0f-372a-818d-91a7-f59c22551350 | PASS |

**Veredicto P3.5:** 4/4 PASS (verificado via API Notion para conteo)

### P3.6 — Demo Ready

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.6.1 | 3 conceptos analizados | Ciudadano-first (elegido), Institucional, Tecnico — con pros/cons | PASS |
| P3.6.2 | Guion 6-8 min escrito | Timeline con MUESTRO/DIGO/EVIDENCIA en FASE3 doc + RUNBOOK-DEMO.md | PASS |
| P3.6.3 | WOW 1 y WOW 2 definidos | Rutas tecnicas + evidence checkpoints | PASS |

**Veredicto P3.6:** 3/3 PASS

### P3.Q1-Q7 — QA Deep Audit

| # | Criterio | Evidencia | Estado |
|---|----------|-----------|--------|
| P3.Q1 | Repo Forensics | 0 secretos, 7 contradicciones corregidas | PASS |
| P3.Q2 | Testing Repro | venv reproducible, xpassed documentado | PASS |
| P3.Q3 | Docker/CI | Build OK, .venv bloat corregido | PASS |
| P3.Q4-Q5 | Deploy Smoke | Health 200, webhook 403, 6 MP3s OK | PASS |
| P3.Q6 | Notion Truth | 81 entradas verificadas por API | PASS |
| P3.Q7 | Observability | JSON valido con request_id | PASS |

**Veredicto QA Deep Audit:** 7/7 PASS

**Claims Matrix:** 42 claims analizados — 34 VERIFIED (81.0%), 5 PARTIAL (11.9%), 3 NOT VERIFIED (7.1%). Los 3 NOT VERIFIED fueron contradicciones entre documentos (skills 10 vs 11, flags 10 vs 9, estado F3 stale) que fueron corregidas.

---

## Metricas

| Metrica | Valor F2 | Valor F3 | Delta |
|---------|----------|----------|-------|
| Tests totales | 93 | 96 | +3 |
| Tests passed | 88 + 5 xpassed | 91 + 5 xpassed | +3 nuevos tests transcribe |
| Skills en pipeline | 11 | 11 | 0 |
| Feature flags | 9 | 9 | 0 |
| Entradas Notion | 75 | 81 | +6 (entradas F3 en Backlog) |
| Owners asignados | — | 97.7% | Completado |
| Deploy | Verificado | Demo-grade (avg 101ms) | Optimizado |
| Incidentes documentados | 0 | 8 (INC-01 a INC-08) | +8 |
| Claims verificados | — | 34/42 (81%) | Audit completo |
| Contradicciones corregidas | — | 11/12 | Casi todas resueltas |
| Health response time (avg) | — | 101ms | Sub-200ms |

### Tests nuevos en Fase 3

| Archivo | Tests nuevos | Cobertura |
|---------|-------------|-----------|
| `tests/unit/test_transcribe.py` | 3 | whisper_model_none_when_disabled, whisper_model_truthy_when_enabled, whisper_model_none_when_no_key |

---

## Vistas embebidas (Linked Views)

### Vista Backlog filtrada por Gates F3

> **Instrucciones Notion:** Crear un Linked View de la base de datos **Backlog/Issues** con filtro `Gate = P3.1 OR P3.2 OR P3.3 OR P3.4 OR P3.5 OR P3.6` y vista tipo Tabla agrupada por Gate.

| Filtro | Valor |
|--------|-------|
| Base de datos | Backlog/Issues |
| Filtro Gate | `P3.1`, `P3.2`, `P3.3`, `P3.4`, `P3.5`, `P3.6` |
| Agrupacion | Por Gate |
| Ordenacion | Por ID de entregable |
| Vista | Tabla |

### Vista Testing filtrada por Fase 3

> **Instrucciones Notion:** Crear un Linked View de la base de datos **Demo & Testing** con filtro `Phase = F3` y vista tipo Tabla.

| Filtro | Valor |
|--------|-------|
| Base de datos | Demo & Testing |
| Filtro Phase | `F3` |
| Columnas visibles | ID, Test, Resultado, Gate (Q1-Q7), Evidencia |
| Vista | Tabla |

### Vista QA Deep Audit (Claims Matrix)

> **Instrucciones Notion:** Crear un Linked View o tabla embebida mostrando los 42 claims del QA Deep Audit con veredicto VERIFIED/PARTIAL/NOT VERIFIED.

| Filtro | Valor |
|--------|-------|
| Tipo | Tabla manual o base de datos temporal |
| Columnas | ID, Claim, Metodo, Veredicto |
| Fuente | `docs/07-evidence/artifacts/phase3/2026-02-13_0030/PHASE-3-CLAIMS-MATRIX.md` |

---

## Lecciones aprendidas

1. **El QA Deep Audit (Claims Matrix) revelo contradicciones reales entre documentos.** De 42 claims verificados, se encontraron 12 contradicciones entre CLAUDE.md, EXECUTIVE-SUMMARY.md, PHASE-STATUS.md y NOTION-OS.md. Ejemplo: unos documentos decian "10 skills" y otros "11 skills" (el real es 11). El audit sistematico con 4 metodos (CODE_INSPECT, COMMAND_RUN, FILE_COUNT, DOC_CROSS_REF) fue critico para garantizar consistencia antes de la presentacion.

2. **Preparar 3 conceptos de demo antes de elegir uno salvo tiempo y discusiones.** Documentar pros/cons de Ciudadano-first, Institucional y Tecnico permitio tomar una decision informada (Concepto A) con refuerzo tecnico, en vez de debatir sin estructura. El jurado de un hackathon de impacto social necesita emocion primero, evidencia despues.

3. **El runbook de 8 incidentes fue la mejor inversion de tiempo pre-demo.** Cubrir escenarios desde cold start hasta internet caido con diagnostico + remediacion especifica significo que cualquier fallo durante la demo tenia un plan B inmediato. La tranquilidad del equipo durante la presentacion fue directamente proporcional a la preparacion de contingencias.

---

## Enlace a evidencia

- **Documento completo:** `docs/07-evidence/PHASE-3-EVIDENCE.md`
- **Claims Matrix:** `docs/07-evidence/artifacts/phase3/2026-02-13_0030/PHASE-3-CLAIMS-MATRIX.md`
- **Verificacion final:** `docs/07-evidence/artifacts/phase3/2026-02-13_0135/phase3-verify-FINAL.txt`
- **Contradicciones corregidas:** `docs/07-evidence/artifacts/phase3/2026-02-13_0030/contradictions_fixed.md`
- **Script de verificacion:** `scripts/phase3_verify.sh`

---

---

# VISTA TIMELINE — TODAS LAS FASES

---

## Timeline del proyecto

> **Instrucciones Notion:** Crear una vista Timeline de la base de datos **Phase Releases** (o una nueva base de datos **Fases**) con propiedades Start Date y End Date. Cada fase es una entrada.

```
2026-02-10     2026-02-11     2026-02-12                    2026-02-13
    |              |              |                              |
    |--- F0 -------|              |                              |
    | Plan Maestro |              |                              |
    |              |              |                              |
                                  |--- F1 ---|--- F2 ---|       |
                                  |   MVP    | Hardening|       |
                                  |  32 tests|  93 tests|       |
                                  |  c6a896e | ec05382  |       |
                                  |          |          |       |
                                  |--- F3 ----------------------|
                                  |   Demo en Vivo + Ops Reales |
                                  |   96 tests  |  77d5f88      |
                                  |             |               |
```

### Datos para la vista Timeline en Notion

| Fase | Nombre | Start Date | End Date | Commit SHA | Tests | Estado |
|------|--------|------------|----------|------------|-------|--------|
| F0 | Plan Maestro | 2026-02-10 | 2026-02-11 | — | — | COMPLETADA |
| F1 | MVP WhatsApp-First | 2026-02-12 | 2026-02-12 | `c6a896e` | 32 | COMPLETADA |
| F2 | Hardening, Deploy & Integrations | 2026-02-12 | 2026-02-12 | `ec05382` | 93 | COMPLETADA |
| F3 | Demo en Vivo, Ops Reales | 2026-02-12 | 2026-02-13 | `77d5f88` | 96 | COMPLETADA |

### Propiedades de la base de datos Timeline

| Propiedad | Tipo | Descripcion |
|-----------|------|-------------|
| Fase | Title | Nombre de la fase (F0, F1, F2, F3) |
| Nombre | Text | Descripcion corta |
| Start Date | Date | Fecha de inicio |
| End Date | Date | Fecha de cierre |
| Commit SHA | Text | Hash del commit de cierre |
| Tests | Number | Cantidad de tests al cerrar la fase |
| Estado | Select | COMPLETADA / EN PROGRESO / PENDIENTE |
| Deploy URL | URL | URL de Render (si aplica) |
| Notion Page | Relation | Relacion a la pagina de fase correspondiente |

---

---

# TABLA COMPARATIVA CROSS-FASE

---

## Comparacion general entre fases

| Dimension | F1 — MVP | F2 — Hardening | F3 — Demo Ready |
|-----------|----------|----------------|-----------------|
| **Fechas** | 2026-02-12 | 2026-02-12 | 2026-02-12 a 2026-02-13 |
| **Commit SHA** | `c6a896e` | `ec05382` | `77d5f88` |
| **Objetivo principal** | Pipeline funcional E2E | Deploy verificado + seguridad | Demo en vivo + ops reales |

### Tests

| Metrica | F1 | F2 | F3 |
|---------|----|----|-----|
| Tests totales | 32 | 93 | 96 |
| Tests unitarios | 21 | 75 | 78 |
| Tests integracion | 7 | 8 | 8 |
| Tests E2E | 4 | 4 | 4 |
| Tests red team (xpassed) | 0 | 5 | 5 |
| Tests transcribe | 0 | 0 | 3 |
| Crecimiento vs fase anterior | — | +61 (+190%) | +3 (+3.2%) |
| Tiempo ejecucion | ~0.76s | ~1.27s | ~0.87s |

### Skills y Arquitectura

| Metrica | F1 | F2 | F3 |
|---------|----|----|-----|
| Skills en pipeline | 11 | 11 | 11 |
| Feature flags | 6 | 9 | 9 |
| Dataclasses (models.py) | 8 | 8 | 8 |
| Cache entries | 8 | 8 | 8 |
| Audios MP3 | 6 | 6 | 6 |
| KB tramites | 3 | 3 | 3 |
| Idiomas soportados | 2 (ES, FR) | 2 (ES, FR) | 2 (ES, FR) |

### Deploy y Operaciones

| Metrica | F1 | F2 | F3 |
|---------|----|----|-----|
| Deploy status | Verificado | Verificado | Demo-grade (avg 101ms) |
| Plataforma | Render free, Frankfurt | Render free, Frankfurt | Render free, Frankfurt |
| Health endpoint | JSON 8 componentes | JSON 8 componentes | JSON 8 componentes |
| Cron warm-up | Cada 14 min | Cada 14 min, documentado | Cada 14 min, verificado |
| Runbook | RUNBOOK-DEMO.md | RUNBOOK-PHASE2.md | RUNBOOK-PHASE3.md (8 incidentes) |
| Docker build | Exitoso | Exitoso | Exitoso |
| Signature validation | Implementada | Verificada | Produccion (403 confirmado) |

### Notion y Documentacion

| Metrica | F1 | F2 | F3 |
|---------|----|----|-----|
| Entradas Notion totales | — | 75 | 81 |
| Backlog DB | — | 37 | 43 |
| KB Tramites DB | — | 12 | 12 |
| Demo & Testing DB | — | 26 | 26 |
| Owners asignados | — | — | 97.7% |
| Paginas de fase en Notion | 1 (F0+F1) | 2 (+F2) | 3 (+F3) |

### Seguridad y Calidad

| Metrica | F1 | F2 | F3 |
|---------|----|----|-----|
| Escaneo de secretos | No realizado | 11 patrones, 0 secretos | Mantenido |
| Guardrails | No implementados | 19 tests pre/post check | Mantenidos |
| Red team | No realizado | 5 vectores bloqueados | Mantenidos |
| PII redaction | No implementado | DNI, NIE, telefono | Mantenido |
| Claims audit | No realizado | No realizado | 42 claims, 34 verified (81%) |
| Contradicciones | — | — | 12 detectadas, 11 corregidas |

### Gates por Fase

| Gate | F1 | F2 | F3 |
|------|----|----|-----|
| G0 Tooling | 5/6 PASS | — | — |
| G1 Texto OK | 7/7 PASS | — | — |
| G2 Audio OK | 5/5 PASS | — | — |
| G3 Demo Listo | 6/6 PASS | — | — |
| P2.1 Twilio | — | 4/4 PASS | — |
| P2.2 Render | — | 4/4 PASS | — |
| P2.3 Cron | — | 2/2 PASS | — |
| P2.4 Notion | — | 4/4 PASS | — |
| P2.5 QA | — | 3/3 PASS | — |
| P2.6 Seguridad | — | 7/7 PASS | — |
| P3.1 Twilio Real | — | — | 6/6 PASS |
| P3.2 Deploy Ops | — | — | 8/8 PASS |
| P3.3 QA Evidence | — | — | 6/6 PASS |
| P3.4 Observability | — | — | 6/6 PASS |
| P3.5 Notion PMO | — | — | 4/4 PASS (API verified) |
| P3.6 Demo Ready | — | — | 3/3 PASS |
| P3.Q1-Q7 QA Deep | — | — | 7/7 PASS |
| **Total items** | **23/24** | **24/24** | **40/40** |

---

## Equipo por fase

| Miembro | Rol | F1 | F2 | F3 |
|---------|-----|----|----|-----|
| Robert | Backend lead | Pipeline 11 skills, config, cache, KB, llm, verify | Observabilidad, guardrails | Demo guion, logging JSON, WOW design |
| Marcos | Routes/Twilio/Deploy | Webhook, Twilio client, pipeline orchestration, deploy | Render deploy, Dockerfile, cron | Twilio real E2E, runbook, ops |
| Lucas | KB/Testing | KB JSONs (3 tramites), tests suite | Tests (32->93), QA script | QA Deep Audit, Claims Matrix, tests (93->96) |
| Daniel | Web/Video | — | — | Video backup |
| Andrea | Notion/Slides | — | Notion 3 DBs (75 entradas), PMO | Notion (81 entradas), slides presentacion |

---

## Instrucciones de implementacion en Notion

### Para crear las 3 paginas de fase

1. **Navegar a cada pagina existente** usando los Notion Page IDs indicados en cada header.
2. **Reemplazar el contenido** con las secciones descritas en este documento.
3. **Crear Linked Views** siguiendo las instrucciones de filtro para cada vista embebida.
4. **Verificar los enlaces** a las paginas de evidencia (`docs/07-evidence/`).

### Para crear la vista Timeline

1. Crear una nueva base de datos **Phase Releases** (si no existe) con las propiedades listadas.
2. Insertar las 4 entradas (F0, F1, F2, F3) con sus fechas y metadatos.
3. Cambiar la vista a **Timeline** agrupada por rango de fechas.

### Para crear la tabla comparativa

1. Crear un bloque **Table** en la pagina principal del proyecto.
2. Copiar los datos de la tabla comparativa cross-fase.
3. Alternativamente, crear una base de datos **Metricas por Fase** con una entrada por fase y propiedades numericas para cada metrica.

---

## Referencias

- [Plan Fase 0](../../docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md)
- [Plan Fase 1](../../docs/01-phases/FASE1-IMPLEMENTACION-MVP.md)
- [Plan Fase 2](../../docs/01-phases/FASE2-HARDENING-DEPLOY-INTEGRATIONS.md)
- [Plan Fase 3](../../docs/01-phases/FASE3-DEMO-OPS-REAL.md)
- [Evidencia Fase 1](../../docs/07-evidence/PHASE-1-EVIDENCE.md)
- [Evidencia Fase 2](../../docs/07-evidence/PHASE-2-EVIDENCE.md)
- [Evidencia Fase 3](../../docs/07-evidence/PHASE-3-EVIDENCE.md)
- [Estado de Fases](../../docs/07-evidence/PHASE-STATUS.md)
- [Claims Matrix](../../docs/07-evidence/artifacts/phase3/2026-02-13_0030/PHASE-3-CLAIMS-MATRIX.md)
- [Checklist de Cierre](../../docs/07-evidence/PHASE-CLOSE-CHECKLIST.md)

---

> **FIN DE SECCION 4 — PAGINAS POR FASE**
