# CivicAid Voice / Clara — Resumen Ejecutivo (1-Pager)

> **Resumen en una linea:** Clara es un asistente conversacional de WhatsApp que ayuda a personas vulnerables en Espana a navegar tramites de servicios sociales, respondiendo en su idioma con texto y audio.

**Hackathon:** OdiseIA4Good — UDIT | **Fecha:** Febrero 2026

---

## El Problema

En Espana, **3,2 millones de inmigrantes** y **9,5 millones de personas mayores** enfrentan barreras burocraticas para acceder a servicios sociales basicos. El **40% de los inmigrantes** no completa los tramites necesarios por barreras de idioma. Los procesos administrativos estan escritos en lenguaje tecnico, en un solo idioma, y repartidos en multiples webs oficiales dificiles de navegar.

## La Solucion

**Clara** reduce esa barrera a **cero**: responde en el idioma del usuario, por el canal que ya usa (WhatsApp, 95% de penetracion en Espana), con informacion verificada de fuentes oficiales del gobierno.

| Diferenciador | Descripcion |
|---------------|-------------|
| **WhatsApp nativo** | Cero descargas. Funciona donde los usuarios ya estan |
| **Voz primero** | Audio de entrada y salida. Critico para baja alfabetizacion digital |
| **Multilingue** | Deteccion automatica de idioma (espanol y frances) |
| **Informacion verificada** | Basada en datos oficiales del gobierno, no alucinaciones |

**3 tramites cubiertos:** Ingreso Minimo Vital (IMV), Empadronamiento, Tarjeta Sanitaria.

---

## Arquitectura

```
Usuario WhatsApp --> Twilio --> Flask /webhook --> TwiML ACK (<1s)
                                               --> Hilo de fondo:
                                                 cache_match --> HIT --> Twilio REST --> Usuario
                                                 cache_match --> MISS --> KB + Gemini --> Twilio REST --> Usuario
```

**Patron TwiML ACK:** Respuesta HTTP 200 inmediata (<1 segundo) al usuario ("Un momento..."), procesamiento real en hilo de fondo con pipeline de **11 skills** especializadas, respuesta final via Twilio REST API.

| Componente | Tecnologia |
|------------|-----------|
| Lenguaje | Python 3.11 |
| Framework | Flask |
| Canal | Twilio WhatsApp Sandbox |
| Transcripcion | Gemini (primario) / Whisper base (local) |
| LLM | Gemini 1.5 Flash |
| Text-to-Speech | gTTS |
| KB | JSON estatico (3 ficheros verificados) |
| Deploy | Render (free tier) + Docker |

---

## Validaciones

| Metrica | Valor | Comando de verificacion |
|---------|-------|------------------------|
| Tests automatizados | **93** (88 passed + 5 xpassed) | `pytest tests/ -v --tb=short` |
| Skills en pipeline | **11** | `ls src/core/skills/*.py` |
| Feature flags | **9** | `src/core/config.py` |
| Entradas de cache | **8** (6 con audio MP3) | `curl .../health` → `cache_entries: 8` |
| Tramites cubiertos | **3** (IMV, Empadronamiento, Tarjeta Sanitaria) | `ls data/tramites/` |
| Idiomas | **2** (ES, FR) | `src/core/skills/detect_lang.py` |
| Deploy verificado | Render + /health operativo | `curl https://civicaid-voice.onrender.com/health` |
| Lint limpio | 0 errores ruff | `ruff check src/ tests/ --select E,F,W --ignore E501` |
| Seguridad | 0 secretos en repo | Scan P2.6 PASS |
| Cron warm-up | Cada 14 min | cron-job.org configurado |

**Regla:** Cada claim = comando + output + archivo verificable.

---

## Impacto

- **40% de inmigrantes** en Espana no completan tramites por barrera idiomatica → Clara la elimina.
- **WhatsApp** tiene penetracion del **95%** en Espana → cero friccion, cero descargas.
- **Audio bidireccional** → accesible para personas con baja alfabetizacion digital.
- **Coste por consulta:** ~$0.002 (cache hit) a ~$0.01 (LLM + transcripcion).
- **Escalabilidad:** 3 tramites hoy, KB extensible a cientos. 2 idiomas hoy, ampliable.
- **Modelo B2G:** Ayuntamientos pagan por usuario atendido. Compatible con ONG/cooperacion.

---

## Demo en Vivo (6-8 min)

| Tiempo | Que ocurre | Ruta tecnica |
|--------|-----------|--------------|
| 0:00 | **Apertura** — el problema de la exclusion burocratica | Slide con datos |
| 1:00 | Presentacion de Clara | Transicion a movil |
| 1:30 | **WOW 1:** Maria pregunta "Que es el IMV?" por texto → respuesta instantanea con texto + audio | Cache hit, <2s |
| 3:30 | Transicion — presentando a Ahmed, inmigrante francofono | Narrativa |
| 4:00 | **WOW 2:** Ahmed envia nota de voz en frances sobre empadronamiento → respuesta en frances con audio | Transcripcion → detect lang → KB → ~10s |
| 6:00 | **Evidencia tecnica** — 93 tests, 11 skills, deploy verificado | Datos en pantalla |
| 7:00 | **Cierre** — escalabilidad, impacto, vision | Slide final |

Guion completo con procedimientos de fallback: [RUNBOOK-DEMO.md](03-runbooks/RUNBOOK-DEMO.md)
Analisis de conceptos y riesgos: [FASE3-DEMO-OPS-REAL.md](01-phases/FASE3-DEMO-OPS-REAL.md)

---

## Equipo

| Persona | Rol |
|---------|-----|
| Robert | Backend lead, pipeline, presentador de demo |
| Marcos | Routes, Twilio, deploy, pipeline de audio |
| Lucas | Investigacion KB, testing, assets de demo |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordinacion |

---

## Estado del Proyecto

| Fase | Estado |
|------|--------|
| Fase 0 — Plan Maestro | COMPLETADA |
| Fase 1 — MVP | COMPLETADA — 93 tests, pipeline 11 skills, cache-first |
| Fase 2 — Hardening | COMPLETADA — deploy Render, Twilio, Notion 81 entradas, observabilidad |
| Fase 3 — Demo en Vivo | COMPLETADA — Twilio, ops, observabilidad, Notion, QA Deep PASS |

---

## Mapa de Documentacion

| Documento | Ruta |
|-----------|------|
| Indice de Documentacion | [docs/00-DOCS-INDEX.md](00-DOCS-INDEX.md) |
| Plan Maestro (Fase 0) | [docs/01-phases/FASE0-PLAN-MAESTRO-FINAL.md](01-phases/FASE0-PLAN-MAESTRO-FINAL.md) |
| Implementacion MVP (Fase 1) | [docs/01-phases/FASE1-IMPLEMENTACION-MVP.md](01-phases/FASE1-IMPLEMENTACION-MVP.md) |
| Hardening y Deploy (Fase 2) | [docs/01-phases/FASE2-HARDENING-DEPLOY-INTEGRATIONS.md](01-phases/FASE2-HARDENING-DEPLOY-INTEGRATIONS.md) |
| Demo en Vivo (Fase 3) | [docs/01-phases/FASE3-DEMO-OPS-REAL.md](01-phases/FASE3-DEMO-OPS-REAL.md) |
| Arquitectura Tecnica | [docs/02-architecture/ARCHITECTURE.md](02-architecture/ARCHITECTURE.md) |
| Runbook Demo | [docs/03-runbooks/RUNBOOK-DEMO.md](03-runbooks/RUNBOOK-DEMO.md) |
| Plan de Tests | [docs/04-testing/TEST-PLAN.md](04-testing/TEST-PLAN.md) |
| Deploy en Render | [docs/05-ops/RENDER-DEPLOY.md](05-ops/RENDER-DEPLOY.md) |
| Notion OS | [docs/06-integrations/NOTION-OS.md](06-integrations/NOTION-OS.md) |
| Estado de Fases | [docs/07-evidence/PHASE-STATUS.md](07-evidence/PHASE-STATUS.md) |

---

## Como se verifica

```bash
# Ejecutar todos los tests
pytest tests/ -q

# Verificar health endpoint en Render
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool

# Verificar audios MP3
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3

# Lint del codigo
ruff check src/ tests/ --select E,F,W --ignore E501
```
