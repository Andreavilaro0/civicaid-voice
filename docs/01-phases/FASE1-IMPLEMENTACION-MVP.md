# FASE 1 — Implementacion MVP "Clara" (WhatsApp-First)

> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good — UDIT
> **Fecha inicio:** 2026-02-12
> **Objetivo:** Entregar un MVP funcional: WhatsApp texto + WhatsApp audio + cache-first + logs estructurados + health endpoint + deploy en Render, con evidencia verificable de cada entregable.
>
> **Documentos relacionados:**
> [Plan Maestro (Fase 0)](./FASE0-PLAN-MAESTRO-FINAL.md) |
> [Arquitectura](../02-architecture/ARCHITECTURE.md) |
> [Runbook Demo](../03-runbooks/RUNBOOK-DEMO.md) |
> [Test Plan](../04-testing/TEST-PLAN.md) |
> [Phase Status](../07-evidence/PHASE-STATUS.md)

---

## 1. Objetivos

1. **MVP funcional end-to-end:** Un usuario envia un mensaje de texto o audio por WhatsApp y recibe una respuesta util sobre tramites (IMV, empadronamiento, tarjeta sanitaria) en menos de 20 segundos.
2. **Cache-first para fiabilidad de demo:** Con `DEMO_MODE=true`, las 8 preguntas frecuentes se responden desde cache en menos de 2 segundos, con audio pregrabado.
3. **Audio pipeline completo:** Whisper base transcribe notas de voz con timeout de 12s y fallback controlado.
4. **Deploy estable en Render:** Docker build exitoso, health endpoint funcional, cron keep-alive cada 14 minutos, cold start inferior a 15 segundos.
5. **Evidencia verificable:** Cada tarea y gate tiene evidencia medible: comando ejecutado, output obtenido, archivo generado, fecha y hora.

---

## 2. Alcance

### Dentro del Alcance (MVP listo)

| # | Condicion | Verificacion |
|---|-----------|-------------|
| 1 | WhatsApp texto funciona | `"Que es el IMV?"` → ACK + respuesta desde cache |
| 2 | WhatsApp audio funciona | Nota de voz → ACK + transcripcion + respuesta |
| 3 | Cache-first activo | `DEMO_MODE=true` → respuestas en <2s |
| 4 | Logs estructurados | `[ACK]`, `[CACHE]`, `[WHISPER]`, `[LLM]`, `[REST]` en logs |
| 5 | Health endpoint | `GET /health` → JSON con estado de componentes |
| 6 | Deploy estable | Render + cron cada 14 min + cold start <15s |

### Fuera del Alcance

| Excluido | Razon |
|----------|-------|
| Base de datos relacional | JSON suficiente para 3 tramites |
| Multi-user avanzado | Stateless por mensaje |
| Embeddings / RAG | Keyword matching suficiente para 8 entradas de cache |
| gTTS en vivo | Solo audios pre-generados en modo demo |
| Soporte de arabe | Frances ya demuestra multilingue |
| Web como canal principal | Solo backup (HuggingFace Space) |

---

## 3. Arquitectura de Referencia

### 3.1 Patron TwiML ACK + Respuesta Asincrona

```
POST /webhook → Parsear → TwiML ACK (HTTP 200, <1s) → Background Thread
                                                       → cache/whisper/gemini
                                                       → Twilio REST API → Usuario
```

El usuario recibe 2 mensajes: (1) ACK inmediato "Un momento...", (2) respuesta completa via REST API. Ver detalle completo en [`ARCHITECTURE.md` seccion 2](../02-architecture/ARCHITECTURE.md).

### 3.2 Pipeline de 10 Skills

```
detect_input → [audio?] fetch_media → convert_audio → transcribe
            → detect_lang → cache_match
                           → [HIT]  → send_response (cache)
                           → [MISS] → kb_lookup → llm_generate → verify → send_response (llm)
```

### 3.3 Feature Flags

| Flag | Tipo | Default | Efecto |
|------|------|---------|--------|
| `DEMO_MODE` | bool | false | Prioriza cache, audios pre-hosted |
| `LLM_LIVE` | bool | true | Habilita llamadas a Gemini |
| `WHISPER_ON` | bool | true | Habilita transcripcion audio |
| `LLM_TIMEOUT` | int | 6 | Segundos max para Gemini |
| `WHISPER_TIMEOUT` | int | 12 | Segundos max para Whisper |
| `AUDIO_BASE_URL` | str | "" | Base URL para MP3 publicos |

### 3.4 Timeouts y Fallbacks

| Skill | Timeout | Fallback |
|-------|---------|----------|
| fetch_media | 5s | "Escribe tu pregunta" |
| convert_ogg_to_wav | 3s | "Escribe tu pregunta" |
| transcribe_whisper | 12s (ThreadPoolExecutor) | "No pude entender tu audio" |
| detect_language | — | Default "es" |
| cache_match | — | CacheResult(hit=False) |
| llm_generate | 6s (request_options) | Respuesta generica con URLs oficiales |
| send_final_message | 5s | Retry x1, luego silencio |

Ver diagramas Mermaid en [`docs/02-architecture/`](../02-architecture/).

---

## 4. Gates

Cada gate es un checkpoint de calidad. **No se avanza al siguiente gate sin evidencia de que todos los criterios se cumplen.**

### Gate 0 — Tooling Ready (pre-requisito)

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| G0.1 | 15 skills instaladas | Lista de skills visible en Claude Code | `cat docs/00-tooling/installed.md` → 15+ skills listadas |
| G0.2 | 5 agents globales + 3 proyecto | Archivos `.md` existen en `.claude/agents/` | `ls .claude/agents/` → 3 archivos; agentes globales configurados |
| G0.3 | `NOTION_TOKEN` configurado | MCP Notion responde | Consulta exitosa a Notion API |
| G0.4 | `GITHUB_TOKEN` configurado | `gh auth status` exitoso | Output de `gh auth status` |
| G0.5 | `.env` con valores reales | Todas las variables criticas tienen valor | `.env` existe (no se commitea), `python -c "from src.core.config import Config; c = Config(); print(c)"` sin errores |
| G0.6 | Notion OS (3 DBs) creadas | 3 databases visibles en Notion | IDs en `project-settings.json` o captura de pantalla de Notion |

### Gate 1 — Texto OK

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| G1.1 | POST /webhook retorna TwiML ACK <1s | Test de integracion pasa | `pytest tests/integration/test_webhook.py -v` → PASSED |
| G1.2 | WA texto cache hit funciona | Cache match retorna respuesta correcta | `pytest tests/unit/test_cache.py -v` → PASSED |
| G1.3 | Respuesta incluye audio MP3 | `media_url` presente en FinalResponse | `pytest tests/integration/test_pipeline.py -v` → PASSED |
| G1.4 | /health retorna JSON | Endpoint responde con componentes | `curl http://localhost:5000/health \| python -m json.tool` → JSON valido |
| G1.5 | Tests T1-T8 pasan | Suite completa verde | `pytest tests/ -v --tb=short` → 93 passed (88 passed + 5 xpassed) |
| G1.6 | CI workflow funcional | GitHub Actions verde | Link a workflow run en GitHub |
| G1.7 | Deploy Render exitoso | App accesible en URL publica | `curl https://[render-url]/health` → JSON OK |

### Gate 2 — Audio OK

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| G2.1 | Audio pipeline implementado | Skills 2-4 existen y pasan tests | `pytest tests/ -k "audio or whisper or fetch_media or convert" -v` → PASSED |
| G2.2 | Whisper timeout enforced (12s) | ThreadPoolExecutor con timeout | `grep -n "ThreadPoolExecutor\|timeout" src/core/skills/transcribe.py` → lineas relevantes |
| G2.3 | LLM timeout (6s) | request_options con timeout | `grep -n "timeout\|request_options" src/core/skills/llm_generate.py` → lineas relevantes |
| G2.4 | Tests completos pasan | 93+ tests verdes | `pytest tests/ -v --tb=short` → todos pasan |
| G2.5 | Test real con audio en Render | Nota de voz → respuesta | Captura de pantalla o log de Render con `[WHISPER] Done` |

### Gate 3 — Demo Ready

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| G3.1 | Fallbacks completos | Cada skill tiene fallback implementado | `grep -rn "except\|fallback\|timeout" src/core/skills/` → cobertura completa |
| G3.2 | Feature flags probados | Cada flag cambia comportamiento | Test manual o automatizado por flag |
| G3.3 | Demo rehearsal completado | Equipo ejecuto runbook completo | Notas del rehearsal con tiempos medidos |
| G3.4 | Video backup grabado | Video de 90s disponible | Archivo de video en equipo o link |
| G3.5 | `phase_close.sh` ejecutado | Reporte de cierre generado | `./scripts/phase_close.sh 1 [URL]` → `docs/07-evidence/phase-1-close-report.md` |

---

## 5. Tareas por Dia

### Dia 1 — Infraestructura + WA Texto

| ID | Descripcion | Responsable | Depende de | DoD | Evidencia (comando + output esperado) | Estado |
|----|-------------|-------------|------------|-----|---------------------------------------|--------|
| D1.1 | Crear repo + estructura de carpetas | Robert | — | `git clone` + `pip install` funciona | `ls src/ tests/ data/ docs/` → carpetas existen | Hecho |
| D1.2 | `config.py` con 6 feature flags | Robert | — | Dataclass Config carga 6 flags de env | `python -c "from src.core.config import Config; print(Config())"` → sin error | Hecho |
| D1.3 | `logger.py` estructurado | Robert | — | Logs con prefijos `[ACK]`, `[CACHE]`, etc. | `grep -rn "ACK\|CACHE\|WHISPER" src/utils/logger.py` → patrones presentes | Hecho |
| D1.4 | `demo_cache.json` con 8 entradas | Robert | — | 8 entradas validas con patterns e idioma | `python -c "import json; d=json.load(open('data/cache/demo_cache.json')); print(len(d['entries']))"` → 8 | Hecho |
| D1.5 | 6 audios MP3 pre-generados | Robert | — | 6 archivos .mp3 en `data/cache/` | `ls data/cache/*.mp3 \| wc -l` → 6 | Hecho |
| D1.6 | `cache.py` + `cache_match.py` | Robert | D1.4 | Cache match retorna hit para keywords conocidos | `pytest tests/unit/test_cache.py -v` → PASSED | Hecho |
| D1.7 | `app.py` + `health.py` | Marcos | — | Flask app inicia, /health responde | `curl localhost:5000/health` → JSON | Hecho |
| D1.8 | `webhook.py` con TwiML ACK | Marcos | — | POST /webhook retorna TwiML en <1s | `pytest tests/integration/test_webhook.py -v` → PASSED | Hecho |
| D1.9 | `static_files.py` para servir MP3 | Marcos | D1.5 | GET /static/cache/*.mp3 retorna audio | `curl -I localhost:5000/static/cache/imv_es.mp3` → 200 | Hecho |
| D1.10 | `twilio_client.py` + `send_response.py` | Marcos | — | Twilio REST wrapper funcional | `pytest tests/unit/ -k "twilio or send" -v` → PASSED | Hecho |
| D1.11 | `pipeline.py` (texto + cache) | Marcos | D1.6, D1.8 | Pipeline texto completo funciona | `pytest tests/integration/test_pipeline.py -v` → PASSED | Hecho |
| D1.12 | JSONs tramites (IMV, empadronamiento, tarjeta) | Lucas | — | 3 JSONs validos en `data/tramites/` | `ls data/tramites/*.json \| wc -l` → 3 | Hecho |
| D1.13 | CI workflow (GitHub Actions) | Robert | — | Lint + tests en CI | `cat .github/workflows/ci.yml` → existe; link a run verde | Hecho |
| D1.14 | Deploy Render | Marcos | D1.7, D1.11 | App accesible en URL publica | `curl https://[render-url]/health` → JSON OK | Pendiente |

### Dia 2 — Audio Pipeline + Whisper + LLM

| ID | Descripcion | Responsable | Depende de | DoD | Evidencia (comando + output esperado) | Estado |
|----|-------------|-------|------------|-----|---------------------------------------|--------|
| D2.1 | `fetch_media.py` | Marcos | D1.8 | Descarga .ogg de Twilio con auth | `pytest tests/ -k "fetch_media" -v` → PASSED | Hecho |
| D2.2 | `convert_audio.py` | Marcos | — | Convierte .ogg a .wav via ffmpeg | `pytest tests/ -k "convert" -v` → PASSED | Hecho |
| D2.3 | `transcribe.py` con timeout 12s | Marcos | D2.2 | Whisper base transcribe con ThreadPoolExecutor | `pytest tests/ -k "transcribe" -v` → PASSED | Hecho |
| D2.4 | `detect_lang.py` | Robert | — | Detecta idioma con langdetect, fallback "es" | `pytest tests/unit/test_detect_lang.py -v` → PASSED | Hecho |
| D2.5 | `kb_lookup.py` | Robert | D1.12 | Extrae secciones relevantes de JSONs de tramites | `pytest tests/unit/test_kb_lookup.py -v` → PASSED | Hecho |
| D2.6 | `llm_generate.py` con timeout 6s | Robert | D2.5 | Gemini genera respuesta con timeout enforced | `pytest tests/ -k "llm" -v` → PASSED | Hecho |
| D2.7 | `verify_response.py` | Robert | D2.6 | Valida longitud, idioma, no-alucinaciones | `pytest tests/ -k "verify" -v` → PASSED | Hecho |
| D2.8 | Audio pipeline en `pipeline.py` | Marcos | D2.1-D2.3 | Pipeline audio completo funciona e2e | `pytest tests/e2e/test_demo_flows.py -v` → PASSED | Hecho |

### Dia 3 — Endurecimiento + Demo

| ID | Descripcion | Responsable | Depende de | DoD | Evidencia (comando + output esperado) | Estado |
|----|-------------|-------|------------|-----|---------------------------------------|--------|
| D3.1 | Fallbacks completos en todos los skills | Marcos | D2.8 | Cada skill tiene except/fallback | `grep -c "except\|fallback" src/core/skills/*.py` → cobertura | Hecho |
| D3.2 | Feature flags probados en deploy | Robert | D1.14 | Cambiar flag → comportamiento cambia | Test manual documentado en evidence | Pendiente |
| D3.3 | Demo rehearsal | Robert | D3.1, D3.2 | Runbook ejecutado completo, tiempos medidos | Notas del rehearsal en `docs/07-evidence/` | Pendiente |
| D3.4 | Video backup (90s) | Daniel | D3.3 | Video grabado y disponible | Archivo de video o link | Pendiente |
| D3.5 | Phase close script ejecutado | Release/PM | D3.1-D3.4 | Reporte de cierre generado | `./scripts/phase_close.sh 1 [URL]` → report en `docs/07-evidence/` | Pendiente |

---

## 6. Riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigacion |
|---|--------|-------------|---------|------------|
| R1 | Render cold start >15s durante demo | Media | Alto | Cron keep-alive cada 14 min via cron-job.org. Warm-up manual T-15 min antes de demo |
| R2 | Whisper excede 512MB RAM en Render free | Media | Alto | Usar modelo `base` (290MB). Si falla: `WHISPER_ON=false` y solo texto |
| R3 | Gemini API timeout o caida | Baja | Alto | Timeout 6s enforced. Fallback: respuesta generica con URLs oficiales. Kill switch: `LLM_LIVE=false` |
| R4 | Twilio sandbox expira o rate limit | Baja | Critico | Re-enviar `join [code]` desde cada telefono. Tener screenshots backup de respuestas |
| R5 | ffmpeg no disponible en container | Baja | Alto | Dockerfile incluye `apt-get install ffmpeg`. Verificar en build |
| R6 | Audio demo de Ahmed no se transcribe bien | Media | Medio | Audio pre-grabado y testeado. Cache hit lo cubre en DEMO_MODE |
| R7 | Internet caido durante demo | Muy baja | Critico | Video backup de 90s. Robert narra encima del video |
| R8 | Tests pasan local pero fallan en CI | Baja | Medio | CI usa misma version Python 3.11 + Docker. Ejecutar CI antes del cierre |

---

## 7. Equipos de Agentes (6 Paneles)

El proyecto se ejecuta con 6 equipos de agentes especializados, coordinados por un lead que **no implementa**.

### Panel 1 — DevOps / Infra

| Campo | Valor |
|-------|-------|
| **Responsabilidad** | Docker build, Render deploy, health endpoint, cron keep-alive, CI/CD pipeline |
| **Skills / MCP** | `docker-expert`, `github-actions-creator`, `devops-engineer`, `render-deploy` |
| **Salidas** | `Dockerfile`, `render.yaml`, `.github/workflows/ci.yml`, health endpoint funcional |
| **Reporte** | URL de deploy + salida JSON de `/health` + enlace a ejecucion de CI |

### Panel 2 — Backend / Pipeline

| Campo | Valor |
|-------|-------|
| **Responsabilidad** | Flask app, webhook handler, TwiML ACK, pipeline de 11 skills, timeouts, Twilio REST integration |
| **Skills / MCP** | `twilio-communications`, `python-patterns`, `senior-fullstack` |
| **Salidas** | `src/app.py`, `src/routes/*.py`, `src/core/pipeline.py`, `src/core/skills/*.py` |
| **Reporte** | Resultados de tests (`pytest -v`) + log de pipeline con tiempos por skill |

### Panel 3 — QA / Testing

| Campo | Valor |
|-------|-------|
| **Responsabilidad** | Tests unitarios, de integracion y e2e. Cobertura. Criterios de aceptacion por gate. Validacion de evidencia |
| **Skills / MCP** | `pytest`, `webapp-testing`, `python-patterns` |
| **Salidas** | `tests/unit/*.py`, `tests/integration/*.py`, `tests/e2e/*.py`, reporte de cobertura |
| **Reporte** | Salida completa de `pytest tests/ -v --tb=short` + conteo de pasados/fallidos |

### Panel 4 — Notion Ops

| Campo | Valor |
|-------|-------|
| **Responsabilidad** | Crear y mantener workspace Notion: 3 databases (Backlog, KB Tramites, Demo & Testing), vistas Kanban, actualizaciones de estado |
| **Skills / MCP** | `notion-knowledge-capture`, `notion-template-business`, MCP `notionApi` |
| **Salidas** | 3 databases populadas, vistas creadas, tareas actualizadas |
| **Reporte** | IDs de databases + enlace al workspace + captura de pantalla de vistas |

### Panel 5 — Docs / Arquitectura

| Campo | Valor |
|-------|-------|
| **Responsabilidad** | `ARCHITECTURE.md`, diagramas Mermaid (secuencia, dataflow, componentes), README, runbooks |
| **Skills / MCP** | Markdown, Mermaid, `obsidian-markdown` |
| **Salidas** | `docs/02-architecture/ARCHITECTURE.md`, `*.mmd` diagramas, `docs/03-runbooks/RUNBOOK-DEMO.md` |
| **Reporte** | Lista de archivos actualizados + diff de cambios |

### Panel 6 — Release / PM

| Campo | Valor |
|-------|-------|
| **Responsabilidad** | Estructura del plan, tracking de gates, riesgos, milestones, cierre de fase, evidencia consolidada |
| **Skills / MCP** | `writing-plans`, `executing-plans` |
| **Salidas** | Este documento (`FASE1-IMPLEMENTACION-MVP.md`), `PHASE-STATUS.md`, reportes de evidencia |
| **Reporte** | Estado de gates + registro de riesgos + reporte de cierre de fase |

---

## 8. Regla del Lead Delegador

> **El lead solo coordina y sintetiza. Toda la implementacion la realizan los teammates.**

El lead:
- Asigna tareas a los paneles correspondientes.
- Revisa evidencia y aprueba gates.
- Sintetiza reportes y actualiza este documento.
- Resuelve bloqueos entre equipos.

El lead **no** escribe codigo, no ejecuta deploys, no crea tests. Si una tarea necesita hacerse, se asigna a un teammate.

---

## 9. Reglas de Evidencia (ESTRICTAS)

> **Nada esta "Hecho" sin evidencia verificable.**

### Minimo requerido por tarea

Cada tarea marcada como "Hecho" debe tener **todos** estos elementos:

| Elemento | Descripcion | Ejemplo |
|----------|-------------|---------|
| **Comando** | El comando exacto ejecutado | `pytest tests/unit/test_cache.py -v` |
| **Output** | La salida real del comando (no inventada) | `3 passed in 0.42s` |
| **Archivo/test** | El archivo creado o test que lo valida | `src/core/cache.py`, `tests/unit/test_cache.py` |
| **Fecha/hora** | Marca temporal de cuando se obtuvo la evidencia | `2026-02-12 14:30 UTC` |

### Reglas adicionales

1. **Las capturas de pantalla no reemplazan logs.** Una captura de pantalla es complemento, no evidencia primaria.
2. **"Tests pasan" requiere output de pytest.** No basta con decir "funciona".
3. **Deploy requiere curl al endpoint publico.** No basta con "Render dice deployed".
4. **Evidencia se guarda en `docs/07-evidence/`.** Logs, outputs, reportes.
5. **Si no hay evidencia, la tarea vuelve a Pendiente.** Sin excepciones.

---

## 10. Politica de Cierre de Fase

Al cerrar la Fase 1, se ejecutan estos pasos **en orden**:

1. **Verificar gates:** Confirmar que G0, G1, G2, G3 tienen todos sus criterios con evidencia.
2. **Ejecutar test suite completa:**
   ```bash
   pytest tests/ -v --tb=short
   ```
   Todos los tests deben pasar. Guardar output en `docs/07-evidence/logs/`.
3. **Ejecutar script de cierre:**
   ```bash
   ./scripts/phase_close.sh 1 https://[render-url]
   ```
   Esto genera automaticamente: test results, arbol del proyecto, checksums de docs, health check, git status. Output en `docs/07-evidence/phase-1-close-report.md`.
4. **Actualizar Notion:**
   - Phase Releases DB: estado = "Cerrada", commit SHA, deploy URL.
   - Backlog: todas las tareas de Fase 1 movidas a "Hecho".
   - Demo & Testing: resultados actualizados con "Pasa"/"Falla" y latencias.
5. **Actualizar documentacion:**
   - `docs/07-evidence/PHASE-STATUS.md` → Fase 1 = Cerrada con fecha.
   - `docs/07-evidence/PHASE-1-EVIDENCE.md` → Evidencia consolidada con logs reales.
   - Diagramas Mermaid actualizados si hubo cambios de arquitectura.
6. **Git:**
   - Commit con mensaje descriptivo.
   - Push a `main`.
   - Tag: `phase-1-vX.Y`.
   - Cerrar issues asociados.
7. **Demo/QA:**
   - Demo rehearsal completado y documentado.
   - Video backup grabado.
   - Screenshots fallback listos.
8. **Comunicar cierre:** Notificar al equipo. Registrar en Notion.

---

## 11. Verificacion Rapida

### Correr tests

```bash
# Suite completa:
pytest tests/ -v --tb=short

# Por categoria:
pytest tests/unit/test_cache.py -v          # Cache matching
pytest tests/unit/test_kb_lookup.py -v      # KB lookup
pytest tests/unit/test_detect_lang.py -v    # Deteccion de idioma
pytest tests/integration/test_webhook.py -v # Webhook + TwiML
pytest tests/integration/test_pipeline.py -v # Pipeline completo
pytest tests/e2e/test_demo_flows.py -v      # Flujos demo e2e
```

### Health check local

```bash
python -m src.app &
curl http://localhost:5000/health | python -m json.tool
```

### Cierre de fase

```bash
./scripts/phase_close.sh 1 https://civicaid-voice.onrender.com
# Genera: docs/07-evidence/phase-1-close-report.md
```

---

## 12. Referencia: Checklist de Cierre

Ver checklist completo en [`docs/07-evidence/PHASE-CLOSE-CHECKLIST.md`](../07-evidence/PHASE-CLOSE-CHECKLIST.md).

La checklist cubre: codigo, deploy, documentacion, Notion, GitHub, demo/QA, y comunicacion. Copiar como `PHASE-1-CLOSE.md` al cerrar esta fase.
