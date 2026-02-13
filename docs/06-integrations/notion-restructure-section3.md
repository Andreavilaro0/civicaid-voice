# SECCION 3: DASHBOARD HOME — CivicAid OS

> **Documento:** Reestructuracion Notion OS — Seccion 3 de N
> **Proyecto:** CivicAid Voice / Clara
> **Autor:** Agente B — Dashboard / BI Designer
> **Fecha:** 2026-02-13
> **Pagina raiz:** CivicAid OS = `304c5a0f-372a-801f-995f-ce24036350ad`

---

## Indice

1. [Especificacion de Layout (Wireframe ASCII)](#1-especificacion-de-layout-wireframe-ascii)
2. [Tarjetas KPI — Detalle de Metricas](#2-tarjetas-kpi--detalle-de-metricas)
3. [Vistas Embebidas de Bases de Datos](#3-vistas-embebidas-de-bases-de-datos)
4. [Bloques Callout — Mensajes de Estado](#4-bloques-callout--mensajes-de-estado)
5. [Bloques de Navegacion — Enlaces Rapidos por Persona](#5-bloques-de-navegacion--enlaces-rapidos-por-persona)
6. [Especificacion de Bloques para la API de Notion](#6-especificacion-de-bloques-para-la-api-de-notion)

---

## 1. Especificacion de Layout (Wireframe ASCII)

El Dashboard Home es la pagina de aterrizaje del workspace CivicAid OS. Se crea como pagina hija de la raiz (`304c5a0f-372a-801f-995f-ce24036350ad`). La composicion visual sigue el orden vertical de bloques de Notion, usando columnas de 2 y 3 donde la API lo permite.

```
+===========================================================================+
|                          CIVICAID OS — DASHBOARD HOME                      |
+===========================================================================+
|                                                                           |
|  [ICONO: telefono] CivicAid Voice / Clara                                |
|  Asistente conversacional de WhatsApp para personas vulnerables en Espana |
|  Hackathon OdiseIA4Good — UDIT — Febrero 2026                            |
|                                                                           |
|  [Enlace GitHub]  [Enlace Render]  [Enlace Notion OS raiz]               |
|                                                                           |
+---------------------------------------------------------------------------+
|                                                                           |
|  ==========================  CALLOUT: ESTADO GLOBAL  ===================  |
|  | Todos los 96 tests pasando (91 passed + 5 xpassed) | F0-F3 COMPLETAS| |
|  | Deploy: Render Frankfurt OK  |  0 secretos  |  0 errores lint       | |
|  ====================================================================== | |
|                                                                           |
+---------------------------------------------------------------------------+
|                        FILA DE TARJETAS KPI (3 columnas)                  |
|                                                                           |
|  +-------------------+  +-------------------+  +-------------------+      |
|  | Tests             |  | Skills            |  | Entradas Notion   |      |
|  | 96                |  | 11                |  | 81                |      |
|  | 91 passed         |  | Pipeline completo |  | 43+12+26          |      |
|  | 5 xpassed         |  |                   |  |                   |      |
|  +-------------------+  +-------------------+  +-------------------+      |
|                                                                           |
|  +-------------------+  +-------------------+  +-------------------+      |
|  | Feature Flags     |  | Tramites          |  | Idiomas           |      |
|  | 9                 |  | 3                 |  | 2                 |      |
|  | DEMO_MODE, etc.   |  | IMV, Empadr, TS   |  | ES, FR            |      |
|  +-------------------+  +-------------------+  +-------------------+      |
|                                                                           |
|  +-------------------+  +-------------------+  +-------------------+      |
|  | Cache Entries     |  | Health Components |  | Gates Completados |      |
|  | 8                 |  | 8                 |  | 22/22             |      |
|  | 6 con audio MP3   |  | /health endpoint  |  | G0-G3 + P2-P3     |      |
|  +-------------------+  +-------------------+  +-------------------+      |
|                                                                           |
+---------------------------------------------------------------------------+
|                    PROGRESO DE FASES  (F0 --> F3)                         |
|                                                                           |
|  [F0 Plan]-----[F1 MVP]-----[F2 Hardening]-----[F3 Demo Ready]          |
|  COMPLETA       COMPLETA      COMPLETA           COMPLETA                |
|  2026-02-10     2026-02-12    2026-02-12         2026-02-13              |
|  ---            32 tests      93 tests           96 tests                |
|  ---            c6a896e       ec05382            77d5f88                  |
|                                                                           |
+---------------------------------------------------------------------------+
|                                                                           |
|  ==================  VISTAS EMBEBIDAS DE BASES DE DATOS  ==============  |
|                                                                           |
|  --- BACKLOG / ISSUES (Tareas activas, no Hecho) ---                     |
|  +---------------------------------------------------------------+       |
|  | [Vista embebida: Kanban agrupado por Gate]                     |       |
|  | Filtro: Estado != "Hecho"                                      |       |
|  | Columnas: Titulo, Estado, Gate, Owner, Prioridad               |       |
|  | DB ID: 304c5a0f-372a-81de-92a8-f54c03b391c0                   |       |
|  +---------------------------------------------------------------+       |
|                                                                           |
|  --- KB TRAMITES (Estado de todos los tramites) ---                      |
|  +---------------------------------------------------------------+       |
|  | [Vista embebida: Tabla todos los tramites]                     |       |
|  | Sin filtro (mostrar todas las 12 entradas)                     |       |
|  | Columnas: Tramite, Campo, Estado, Organismo, Fecha verif.      |       |
|  | DB ID: 304c5a0f-372a-81ff-9d45-c785e69f7335                   |       |
|  +---------------------------------------------------------------+       |
|                                                                           |
|  --- DEMO & TESTING (Resultados recientes, fallos resaltados) ---        |
|  +---------------------------------------------------------------+       |
|  | [Vista embebida: Board por Gate]                               |       |
|  | Ordenar: Fecha desc                                            |       |
|  | Color condicional: Resultado="Falla" -> rojo                   |       |
|  | Columnas: Test, Tipo, Resultado, Gate, Fecha, Latencia         |       |
|  | DB ID: 304c5a0f-372a-810d-8767-d77efbd46bb2                   |       |
|  +---------------------------------------------------------------+       |
|                                                                           |
+---------------------------------------------------------------------------+
|                        ENLACES RAPIDOS POR PERSONA                        |
|                                                                           |
|  +---------------------+  +---------------------+  +------------------+  |
|  | JUEZ / REVISOR      |  | DESARROLLADOR       |  | PM / COORDINADOR |  |
|  | > Resumen Ejecutivo  |  | > Arquitectura      |  | > Backlog Kanban |  |
|  | > Demo (Runbook)     |  | > Plan de Tests     |  | > Phase Status   |  |
|  | > Phase Status       |  | > Render Deploy     |  | > Notion OS      |  |
|  | > KB Tramites        |  | > Observability     |  | > Team Activity  |  |
|  | > Test Results       |  | > GitHub Repo       |  | > Calendario     |  |
|  +---------------------+  +---------------------+  +------------------+  |
|                                                                           |
+---------------------------------------------------------------------------+
|                        ACTIVIDAD DEL EQUIPO                               |
|                                                                           |
|  +-------------------------------------------------------------------+   |
|  | Miembro  | Rol                 | Tareas (Hecho) | Area principal  |   |
|  |----------|---------------------|----------------|-----------------|   |
|  | Robert   | Backend lead        | ~9             | Pipeline, demo  |   |
|  | Marcos   | Routes/Twilio       | ~9             | Audio, deploy   |   |
|  | Lucas    | KB/Testing          | ~9             | KB, assets      |   |
|  | Daniel   | Web/Video           | ~8             | Gradio, video   |   |
|  | Andrea   | Notion/Slides       | ~8             | Notion, coord.  |   |
|  +-------------------------------------------------------------------+   |
|  Fuente: Backlog DB filtrada por Owner, Estado=Hecho                     |
|                                                                           |
+---------------------------------------------------------------------------+
|                                                                           |
|  [PIE: Ultima actualizacion: 2026-02-13 | Generado por Agente B]        |
|                                                                           |
+===========================================================================+
```

---

## 2. Tarjetas KPI — Detalle de Metricas

Cada tarjeta KPI se implementa como un bloque `callout` dentro de una estructura de columnas de Notion (3 columnas por fila, 3 filas = 9 tarjetas KPI).

### Fila 1: Metricas de Calidad

| # | Nombre | Valor actual | Fuente | Icono sugerido | Formula / Metodo de calculo |
|---|--------|-------------|--------|----------------|----------------------------|
| K1 | **Tests totales** | **96** (91 passed + 5 xpassed) | Ejecucion `pytest tests/ -q` — salida verificada en `docs/07-evidence/artifacts/phase3/2026-02-13_0135/pytest-q.txt` | `checkmark_circle` (verde) | Estatico. Actualizar tras cada ejecucion de pytest. Desglose: 85 unit + 7 integration + 4 e2e. Resultado real: 91 passed + 5 xpassed = 96 total. |
| K2 | **Skills del pipeline** | **11** | Conteo de archivos en `src/core/skills/*.py` (excluyendo `__init__.py`): `detect_input`, `fetch_media`, `detect_lang`, `cache_match`, `kb_lookup`, `verify_response`, `convert_audio`, `send_response`, `llm_generate`, `tts`, `transcribe` | `gear` | Estatico. `ls src/core/skills/*.py \| grep -v __init__ \| wc -l` = 11 |
| K3 | **Entradas Notion** | **81** | Consulta API Notion a las 3 DBs: Backlog (43) + KB Tramites (12) + Demo & Testing (26) | `page_facing_up` | Rollup via API. Sumar `page_size` de cada DB query: `POST /v1/databases/{id}/query` para cada DB y sumar resultados. |

### Fila 2: Metricas de Producto

| # | Nombre | Valor actual | Fuente | Icono sugerido | Formula / Metodo de calculo |
|---|--------|-------------|--------|----------------|----------------------------|
| K4 | **Feature flags** | **9** | Archivo `src/core/config.py` — campos booleanos/enteros del dataclass `Config` | `control_knobs` | Estatico. Los 9 flags: `DEMO_MODE`, `LLM_LIVE`, `WHISPER_ON`, `LLM_TIMEOUT`, `WHISPER_TIMEOUT`, `OBSERVABILITY_ON`, `STRUCTURED_OUTPUT_ON`, `GUARDRAILS_ON`, `RAG_ENABLED` |
| K5 | **Tramites cubiertos** | **3** | KB Tramites DB (12 entradas / 4 campos por tramite = 3 tramites) | `clipboard` | Rollup. En KB Tramites DB: contar valores unicos de la propiedad `Tramite` (Title). Resultado: IMV, Empadronamiento, Tarjeta Sanitaria = 3 |
| K6 | **Idiomas** | **2** | Verificado en `src/core/skills/detect_lang.py` y `data/cache/demo_cache.json` (entradas con `idioma: "es"` y `idioma: "fr"`) | `globe_with_meridians` | Estatico. ES (espanol) + FR (frances) = 2 |

### Fila 3: Metricas de Infraestructura

| # | Nombre | Valor actual | Fuente | Icono sugerido | Formula / Metodo de calculo |
|---|--------|-------------|--------|----------------|----------------------------|
| K7 | **Entradas de cache** | **8** | Archivo `data/cache/demo_cache.json` — 8 objetos JSON. Verificable via `/health` endpoint (`cache_entries: 8`) | `file_cabinet` | Estatico. 8 entradas: `imv_es`, `empadronamiento_es`, `tarjeta_sanitaria_es`, `ahmed_empadronamiento_fr`, `fatima_tarjeta_fr`, `saludo_es`, `saludo_fr`, `maria_carta_vision`. De estas, 6 tienen `audio_file` (MP3). |
| K8 | **Componentes Health** | **8** | Endpoint `/health` — devuelve JSON con 8 campos en `components` | `heartbeat` | Estatico. Los 8: `whisper_loaded`, `whisper_enabled`, `ffmpeg_available`, `gemini_key_set`, `twilio_configured`, `cache_entries`, `demo_mode`, `llm_live` |
| K9 | **Gates completados** | **22/22** | Documento `docs/07-evidence/PHASE-STATUS.md` — tabla resumen de gates | `trophy` | Estatico. G0 + G1 + G2 + G3 + P2.1-P2.6 + P3.1-P3.6 + P3.Q1-P3.Q7 = 4 + 6 + 7 + 5 = 22 gates, todos PASS |

---

## 3. Vistas Embebidas de Bases de Datos

### 3.1 Backlog / Issues — Vista: Tareas Activas por Gate

- **DB ID:** `304c5a0f-372a-81de-92a8-f54c03b391c0`
- **Tipo de vista:** Board (Kanban)
- **Agrupar por:** `Gate` (valores: G0-Tooling, G1-Texto, G2-Audio, G3-Demo, Infra)
- **Filtro:**
  ```json
  {
    "filter": {
      "property": "Estado",
      "select": {
        "does_not_equal": "Hecho"
      }
    }
  }
  ```
- **Columnas visibles:** Titulo, Estado, Gate, Owner, Prioridad, Horas est.
- **Ordenar:** Prioridad ascendente (P0-demo primero)
- **Proposito:** Permite ver de un vistazo que tareas siguen activas o bloqueadas. Post-hackathon: la mayoria estaran en "Hecho" (42 de 43 actualmente), quedando solo 1 en Backlog.
- **Nota de implementacion:** Notion no soporta vistas embebidas con filtro personalizado via API. Se debe crear la vista manualmente en la UI de Notion y luego enlazar con un bloque `link_to_page` o `embed`. Alternativa via API: crear un bloque `child_database` inline con los datos filtrados, o usar un bloque de texto con enlace a la vista filtrada.

### 3.2 KB Tramites — Vista: Todos los Tramites con Estado

- **DB ID:** `304c5a0f-372a-81ff-9d45-c785e69f7335`
- **Tipo de vista:** Table
- **Filtro:** Ninguno (mostrar las 12 entradas)
- **Columnas visibles:** Tramite, Campo, Valor (truncado), Organismo, Estado, Fecha verificacion
- **Ordenar:** Tramite ascendente, luego Campo en orden (Descripcion > Requisitos > Documentos > Pasos)
- **Proposito:** Vista de referencia rapida para ver la cobertura completa de la base de conocimiento. Todas las 12 entradas estan en estado "Verificado".
- **Color condicional sugerido:**
  - `Verificado` = verde
  - `Pendiente` = amarillo
  - `Desactualizado` = rojo

### 3.3 Demo & Testing — Vista: Resultados con Fallos Resaltados

- **DB ID:** `304c5a0f-372a-810d-8767-d77efbd46bb2`
- **Tipo de vista:** Board agrupado por Gate
- **Filtro:** Ninguno (mostrar las 26 entradas)
- **Ordenar:** Fecha descendente (mas recientes primero)
- **Columnas visibles:** Test, Tipo, Input (truncado), Resultado, Gate, Fecha, Latencia (ms)
- **Color condicional:**
  - `Pasa` = verde
  - `Falla` = rojo (resaltar prominentemente)
  - `Pendiente` = gris
- **Proposito:** Panel de control de calidad. Actualmente las 26 entradas estan en "Pasa". Los fallos se veran inmediatamente en rojo si aparecen.
- **Filtro alternativo para vista de fallos:**
  ```json
  {
    "filter": {
      "property": "Resultado",
      "select": {
        "equals": "Falla"
      }
    }
  }
  ```

---

## 4. Bloques Callout — Mensajes de Estado

Cada callout se implementa como un bloque tipo `callout` de la API de Notion con icono, color y contenido.

### Callout 1: Estado Global de Tests

| Propiedad | Valor |
|-----------|-------|
| **Icono** | `white_check_mark` |
| **Color** | `green_background` |
| **Titulo** | Todos los 96 tests pasando |
| **Contenido** | 91 passed + 5 xpassed. Desglose: 85 unit, 7 integration, 4 e2e. Lint: 0 errores ruff. Ultima ejecucion: 2026-02-13. Evidencia: `docs/07-evidence/artifacts/phase3/2026-02-13_0135/pytest-q.txt` |

### Callout 2: Estado de Deploy

| Propiedad | Valor |
|-----------|-------|
| **Icono** | `rocket` |
| **Color** | `blue_background` |
| **Titulo** | Deploy: Render Frankfurt OK |
| **Contenido** | Servicio `civicaid-voice` en Render free tier, region Frankfurt. Docker build exitoso. Health check en `/health` devuelve 8 componentes. Cron warm-up cada 14 min via cron-job.org. URL: `https://civicaid-voice.onrender.com/health` |

### Callout 3: Seguridad

| Propiedad | Valor |
|-----------|-------|
| **Icono** | `shield` |
| **Color** | `green_background` |
| **Titulo** | Seguridad: 0 secretos en repositorio |
| **Contenido** | Escaneo P2.6 completo: 11 patrones de secretos verificados en todos los archivos rastreados por git. Cero secretos reales encontrados. `.env` en `.gitignore`. `render.yaml` usa `sync: false` para tokens sensibles. Validacion de firma Twilio activa (403 sin firma). |

### Callout 4: Fases Completadas

| Propiedad | Valor |
|-----------|-------|
| **Icono** | `trophy` |
| **Color** | `yellow_background` |
| **Titulo** | Todas las fases completadas: F0, F1, F2, F3 |
| **Contenido** | 22 gates verificados, todos PASS. Desde G0-Tooling hasta P3.Q7-Observability. Cero gates pendientes. Proyecto listo para demo en vivo ante jueces OdiseIA4Good. |

### Callout 5: Notion OS

| Propiedad | Valor |
|-----------|-------|
| **Icono** | `card_file_box` |
| **Color** | `purple_background` |
| **Titulo** | Notion: 81 entradas en 3 bases de datos |
| **Contenido** | Backlog: 43 entradas (42 Hecho, 1 Backlog). KB Tramites: 12 entradas (3 tramites x 4 campos, todas Verificado). Demo & Testing: 26 entradas (todas Pasa). Owners asignados al 97.7% del Backlog. |

---

## 5. Bloques de Navegacion — Enlaces Rapidos por Persona

Se implementan como 3 columnas, cada una con un bloque `callout` que contiene una lista de enlaces internos.

### Columna 1: Juez / Revisor del Hackathon

| Icono | `judge` / `scales` |
|-------|-----|
| **Color** | `orange_background` |
| **Titulo** | Para Jueces y Revisores |

**Enlaces:**

| Destino | Tipo de enlace | ID / Ruta |
|---------|---------------|-----------|
| Resumen Ejecutivo (1-pager) | Enlace a pagina | `docs/00-EXECUTIVE-SUMMARY.md` o pagina Notion equivalente |
| Demo Runbook (guion 6-8 min) | Enlace a pagina | `docs/03-runbooks/RUNBOOK-DEMO.md` |
| Estado de Fases | Enlace a pagina | `docs/07-evidence/PHASE-STATUS.md` |
| KB Tramites (que sabe Clara) | Enlace a DB | `304c5a0f-372a-81ff-9d45-c785e69f7335` |
| Resultados de Tests | Enlace a DB | `304c5a0f-372a-810d-8767-d77efbd46bb2` |
| Health Endpoint (Render) | URL externa | `https://civicaid-voice.onrender.com/health` |

### Columna 2: Desarrollador

| Icono | `technologist` / `wrench` |
|-------|-----|
| **Color** | `blue_background` |
| **Titulo** | Para Desarrolladores |

**Enlaces:**

| Destino | Tipo de enlace | ID / Ruta |
|---------|---------------|-----------|
| Arquitectura Tecnica | Enlace a pagina | `docs/02-architecture/ARCHITECTURE.md` |
| Plan de Tests | Enlace a pagina | `docs/04-testing/TEST-PLAN.md` |
| Deploy en Render | Enlace a pagina | `docs/05-ops/RENDER-DEPLOY.md` |
| Observability Quickstart | Enlace a pagina | `docs/05-ops/OBSERVABILITY-QUICKSTART.md` |
| Twilio Setup Guide | Enlace a pagina | `docs/06-integrations/TWILIO-SETUP-GUIDE.md` |
| Repositorio GitHub | URL externa | URL del repositorio |

### Columna 3: PM / Coordinador

| Icono | `bar_chart` / `clipboard` |
|-------|-----|
| **Color** | `green_background` |
| **Titulo** | Para PM y Coordinacion |

**Enlaces:**

| Destino | Tipo de enlace | ID / Ruta |
|---------|---------------|-----------|
| Backlog Kanban | Enlace a DB | `304c5a0f-372a-81de-92a8-f54c03b391c0` (vista Kanban por Estado) |
| Estado de Fases | Enlace a pagina | `docs/07-evidence/PHASE-STATUS.md` |
| Notion OS (documentacion) | Enlace a pagina | `docs/06-integrations/NOTION-OS.md` |
| Backlog por Owner | Enlace a DB | `304c5a0f-372a-81de-92a8-f54c03b391c0` (vista Tabla por Owner) |
| Calendario por Dia | Enlace a DB | `304c5a0f-372a-81de-92a8-f54c03b391c0` (vista Calendario) |
| Evidencia Fase 3 | Enlace a pagina | `docs/07-evidence/PHASE-3-EVIDENCE.md` |

---

## 6. Especificacion de Bloques para la API de Notion

A continuacion se detalla la estructura completa de bloques necesarios para crear la pagina Dashboard Home via la API de Notion (`POST /v1/pages` + `PATCH /v1/blocks/{id}/children`).

### 6.0 Crear la Pagina

```json
{
  "parent": {
    "page_id": "304c5a0f-372a-801f-995f-ce24036350ad"
  },
  "icon": {
    "type": "emoji",
    "emoji": "📊"
  },
  "cover": {
    "type": "external",
    "external": {
      "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200"
    }
  },
  "properties": {
    "title": [
      {
        "text": {
          "content": "Dashboard Home — CivicAid OS"
        }
      }
    ]
  }
}
```

### 6.1 Bloque Hero — Encabezado del Proyecto

```json
[
  {
    "object": "block",
    "type": "heading_1",
    "heading_1": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "CivicAid Voice / Clara" },
          "annotations": { "bold": true }
        }
      ],
      "color": "blue"
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Asistente conversacional de WhatsApp para personas vulnerables en Espana. Hackathon OdiseIA4Good — UDIT — Febrero 2026." },
          "annotations": { "italic": true, "color": "gray" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": {
            "content": "Health Endpoint",
            "link": { "url": "https://civicaid-voice.onrender.com/health" }
          },
          "annotations": { "bold": true }
        },
        {
          "type": "text",
          "text": { "content": "  |  " }
        },
        {
          "type": "text",
          "text": {
            "content": "Notion OS (raiz)",
            "link": { "url": "https://www.notion.so/CivicAid-OS-304c5a0f372a801f995fce24036350ad" }
          },
          "annotations": { "bold": true }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  }
]
```

### 6.2 Callout: Estado Global

```json
{
  "object": "block",
  "type": "callout",
  "callout": {
    "icon": { "type": "emoji", "emoji": "✅" },
    "color": "green_background",
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "ESTADO GLOBAL: " },
        "annotations": { "bold": true }
      },
      {
        "type": "text",
        "text": { "content": "Todos los 96 tests pasando (91 passed + 5 xpassed) | Deploy Render Frankfurt OK | 0 secretos | 0 errores lint | Fases F0-F3 COMPLETADAS | 22/22 gates PASS" }
      }
    ]
  }
}
```

### 6.3 Fila KPI 1 — Tests, Skills, Entradas Notion (3 columnas)

```json
{
  "object": "block",
  "type": "column_list",
  "column_list": {
    "children": [
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "🧪" },
                "color": "green_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Tests\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "96" },
                    "annotations": { "bold": true, "color": "green" }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\n91 passed + 5 xpassed\n85 unit | 7 integ | 4 e2e" }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "⚙️" },
                "color": "blue_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Skills del Pipeline\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "11" },
                    "annotations": { "bold": true, "color": "blue" }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\ndetect_input, fetch_media, detect_lang, cache_match, kb_lookup, llm_generate, verify_response, convert_audio, tts, transcribe, send_response" }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "📄" },
                "color": "purple_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Entradas Notion\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "81" },
                    "annotations": { "bold": true, "color": "purple" }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\nBacklog: 43 | KB: 12 | Testing: 26\n3 bases de datos" }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### 6.4 Fila KPI 2 — Feature Flags, Tramites, Idiomas

```json
{
  "object": "block",
  "type": "column_list",
  "column_list": {
    "children": [
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "🎛️" },
                "color": "yellow_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Feature Flags\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "9" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\nDEMO_MODE, LLM_LIVE, WHISPER_ON, LLM_TIMEOUT, WHISPER_TIMEOUT, OBSERVABILITY_ON, STRUCTURED_OUTPUT_ON, GUARDRAILS_ON, RAG_ENABLED" }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "📋" },
                "color": "orange_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Tramites Cubiertos\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "3" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\nIngreso Minimo Vital (IMV)\nEmpadronamiento\nTarjeta Sanitaria" }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "🌐" },
                "color": "gray_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Idiomas\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "2" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\nES — Espanol\nFR — Frances\nDeteccion automatica" }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### 6.5 Fila KPI 3 — Cache, Health, Gates

```json
{
  "object": "block",
  "type": "column_list",
  "column_list": {
    "children": [
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "🗄️" },
                "color": "brown_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Entradas de Cache\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "8" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\n6 con audio MP3 pregenerado\n2 saludos (ES, FR) sin audio\nFuente: demo_cache.json" }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "💓" },
                "color": "red_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Componentes Health\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "8" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\nwhisper_loaded, whisper_enabled, ffmpeg_available, gemini_key_set, twilio_configured, cache_entries, demo_mode, llm_live" }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "column",
        "column": {
          "children": [
            {
              "object": "block",
              "type": "callout",
              "callout": {
                "icon": { "type": "emoji", "emoji": "🏆" },
                "color": "yellow_background",
                "rich_text": [
                  {
                    "type": "text",
                    "text": { "content": "Gates Completados\n" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "22/22 PASS" },
                    "annotations": { "bold": true }
                  },
                  {
                    "type": "text",
                    "text": { "content": "\nG0-G3 (Fase 1)\nP2.1-P2.6 (Fase 2)\nP3.1-P3.6 + P3.Q1-Q7 (Fase 3)" }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### 6.6 Progreso de Fases (Tracker Visual)

```json
[
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Progreso de Fases" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "table",
    "table": {
      "table_width": 6,
      "has_column_header": true,
      "has_row_header": false,
      "children": [
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Fase" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Estado" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Inicio" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Cierre" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Tests" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Commit" }, "annotations": { "bold": true } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "F0 — Plan Maestro" } }],
              [{ "type": "text", "text": { "content": "COMPLETADA" }, "annotations": { "bold": true, "color": "green" } }],
              [{ "type": "text", "text": { "content": "2026-02-10" } }],
              [{ "type": "text", "text": { "content": "2026-02-11" } }],
              [{ "type": "text", "text": { "content": "—" } }],
              [{ "type": "text", "text": { "content": "—" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "F1 — MVP" } }],
              [{ "type": "text", "text": { "content": "COMPLETADA" }, "annotations": { "bold": true, "color": "green" } }],
              [{ "type": "text", "text": { "content": "2026-02-12" } }],
              [{ "type": "text", "text": { "content": "2026-02-12" } }],
              [{ "type": "text", "text": { "content": "32/32" } }],
              [{ "type": "text", "text": { "content": "c6a896e" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "F2 — Hardening" } }],
              [{ "type": "text", "text": { "content": "COMPLETADA" }, "annotations": { "bold": true, "color": "green" } }],
              [{ "type": "text", "text": { "content": "2026-02-12" } }],
              [{ "type": "text", "text": { "content": "2026-02-12" } }],
              [{ "type": "text", "text": { "content": "93/93" } }],
              [{ "type": "text", "text": { "content": "ec05382" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "F3 — Demo Ready" } }],
              [{ "type": "text", "text": { "content": "COMPLETADA" }, "annotations": { "bold": true, "color": "green" } }],
              [{ "type": "text", "text": { "content": "2026-02-12" } }],
              [{ "type": "text", "text": { "content": "2026-02-13" } }],
              [{ "type": "text", "text": { "content": "96/96" } }],
              [{ "type": "text", "text": { "content": "77d5f88" } }]
            ]
          }
        }
      ]
    }
  }
]
```

### 6.7 Encabezados de Secciones de Vistas Embebidas

```json
[
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Bases de Datos — Vistas Embebidas" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Backlog / Issues — Tareas Activas (no Hecho)" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "link_to_page",
    "link_to_page": {
      "type": "database_id",
      "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0"
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Vista sugerida: Kanban agrupado por Gate. Filtro: Estado != Hecho. Mostrar: Titulo, Estado, Gate, Owner, Prioridad." },
          "annotations": { "italic": true, "color": "gray" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "KB Tramites — Cobertura Completa" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "link_to_page",
    "link_to_page": {
      "type": "database_id",
      "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335"
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Vista sugerida: Tabla completa. Sin filtro. 12 entradas: 3 tramites x 4 campos. Todas en estado Verificado." },
          "annotations": { "italic": true, "color": "gray" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Demo & Testing — Resultados por Gate" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "link_to_page",
    "link_to_page": {
      "type": "database_id",
      "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2"
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Vista sugerida: Board agrupado por Gate. 26 entradas, todas Pasa. Resaltar fallos en rojo (condicional: Resultado = Falla)." },
          "annotations": { "italic": true, "color": "gray" }
        }
      ]
    }
  }
]
```

### 6.8 Navegacion por Persona (3 columnas)

```json
[
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Enlaces Rapidos por Persona" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "column_list",
    "column_list": {
      "children": [
        {
          "object": "block",
          "type": "column",
          "column": {
            "children": [
              {
                "object": "block",
                "type": "callout",
                "callout": {
                  "icon": { "type": "emoji", "emoji": "⚖️" },
                  "color": "orange_background",
                  "rich_text": [
                    {
                      "type": "text",
                      "text": { "content": "Juez / Revisor" },
                      "annotations": { "bold": true }
                    }
                  ],
                  "children": [
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Resumen Ejecutivo (1-pager)", "link": { "url": "https://www.notion.so/CivicAid-OS-304c5a0f372a801f995fce24036350ad" } } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Guion Demo (6-8 min)" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Estado de Fases" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "KB Tramites", "link": { "url": "https://notion.so/304c5a0f372a81ff9d45c785e69f7335" } } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Resultados de Tests", "link": { "url": "https://notion.so/304c5a0f372a810d8767d77efbd46bb2" } } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Health Endpoint", "link": { "url": "https://civicaid-voice.onrender.com/health" } } }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          }
        },
        {
          "object": "block",
          "type": "column",
          "column": {
            "children": [
              {
                "object": "block",
                "type": "callout",
                "callout": {
                  "icon": { "type": "emoji", "emoji": "🔧" },
                  "color": "blue_background",
                  "rich_text": [
                    {
                      "type": "text",
                      "text": { "content": "Desarrollador" },
                      "annotations": { "bold": true }
                    }
                  ],
                  "children": [
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Arquitectura Tecnica" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Plan de Tests" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Deploy en Render" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Observability Quickstart" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Twilio Setup Guide" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Repositorio GitHub" } }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          }
        },
        {
          "object": "block",
          "type": "column",
          "column": {
            "children": [
              {
                "object": "block",
                "type": "callout",
                "callout": {
                  "icon": { "type": "emoji", "emoji": "📊" },
                  "color": "green_background",
                  "rich_text": [
                    {
                      "type": "text",
                      "text": { "content": "PM / Coordinador" },
                      "annotations": { "bold": true }
                    }
                  ],
                  "children": [
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Backlog Kanban", "link": { "url": "https://notion.so/304c5a0f372a81de92a8f54c03b391c0" } } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Estado de Fases" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Notion OS (documentacion)" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Backlog por Owner" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Calendario por Dia" } }
                        ]
                      }
                    },
                    {
                      "object": "block",
                      "type": "bulleted_list_item",
                      "bulleted_list_item": {
                        "rich_text": [
                          { "type": "text", "text": { "content": "Evidencia Fase 3" } }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  }
]
```

### 6.9 Actividad del Equipo

```json
[
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Actividad del Equipo" }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "table",
    "table": {
      "table_width": 4,
      "has_column_header": true,
      "has_row_header": false,
      "children": [
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Miembro" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Rol" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Area Principal" }, "annotations": { "bold": true } }],
              [{ "type": "text", "text": { "content": "Estado" }, "annotations": { "bold": true } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Robert" } }],
              [{ "type": "text", "text": { "content": "Backend lead" } }],
              [{ "type": "text", "text": { "content": "Pipeline 11 skills, presentador demo" } }],
              [{ "type": "text", "text": { "content": "Activo" }, "annotations": { "color": "green" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Marcos" } }],
              [{ "type": "text", "text": { "content": "Routes / Twilio" } }],
              [{ "type": "text", "text": { "content": "Audio pipeline, deploy Render" } }],
              [{ "type": "text", "text": { "content": "Activo" }, "annotations": { "color": "green" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Lucas" } }],
              [{ "type": "text", "text": { "content": "KB / Testing" } }],
              [{ "type": "text", "text": { "content": "Investigacion KB, assets demo" } }],
              [{ "type": "text", "text": { "content": "Activo" }, "annotations": { "color": "green" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Daniel" } }],
              [{ "type": "text", "text": { "content": "Web / Video" } }],
              [{ "type": "text", "text": { "content": "Interfaz Gradio (backup), video" } }],
              [{ "type": "text", "text": { "content": "Activo" }, "annotations": { "color": "green" } }]
            ]
          }
        },
        {
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "type": "text", "text": { "content": "Andrea" } }],
              [{ "type": "text", "text": { "content": "Notion / Slides" } }],
              [{ "type": "text", "text": { "content": "CivicAid OS, coordinacion" } }],
              [{ "type": "text", "text": { "content": "Activo" }, "annotations": { "color": "green" } }]
            ]
          }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Fuente: Backlog DB filtrada por Owner (propiedad Select). Estado Hecho: 42 de 43 tareas (97.7%). Para ver la distribucion por persona, usar la vista 'Tabla por Owner' del Backlog." },
          "annotations": { "italic": true, "color": "gray" }
        }
      ]
    }
  }
]
```

### 6.10 Pie de Pagina

```json
[
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "type": "text",
          "text": { "content": "Ultima actualizacion: 2026-02-13 | CivicAid OS Dashboard Home | Hackathon OdiseIA4Good — UDIT" },
          "annotations": { "italic": true, "color": "gray" }
        }
      ]
    }
  }
]
```

---

## Resumen de Bloques — Orden Completo de Insercion

Para crear la pagina completa del Dashboard Home via la API de Notion, se deben insertar los bloques en el siguiente orden como hijos de la pagina creada en el paso 6.0:

| Orden | Seccion | Tipo de bloque principal | Referencia |
|-------|---------|-------------------------|------------|
| 1 | Hero: Titulo del proyecto | `heading_1` + `paragraph` + `paragraph` (enlaces) + `divider` | Seccion 6.1 |
| 2 | Callout: Estado global | `callout` (verde) | Seccion 6.2 |
| 3 | KPI Fila 1: Tests, Skills, Entradas | `column_list` con 3 columnas, cada una con `callout` | Seccion 6.3 |
| 4 | KPI Fila 2: Flags, Tramites, Idiomas | `column_list` con 3 columnas, cada una con `callout` | Seccion 6.4 |
| 5 | KPI Fila 3: Cache, Health, Gates | `column_list` con 3 columnas, cada una con `callout` | Seccion 6.5 |
| 6 | Progreso de fases | `divider` + `heading_2` + `table` (5 filas x 6 columnas) | Seccion 6.6 |
| 7 | Vistas embebidas: Backlog | `heading_3` + `link_to_page` (database) + `paragraph` | Seccion 6.7 |
| 8 | Vistas embebidas: KB Tramites | `heading_3` + `link_to_page` (database) + `paragraph` | Seccion 6.7 |
| 9 | Vistas embebidas: Testing | `heading_3` + `link_to_page` (database) + `paragraph` | Seccion 6.7 |
| 10 | Navegacion por persona | `divider` + `heading_2` + `column_list` (3 columnas con `callout` + listas) | Seccion 6.8 |
| 11 | Actividad del equipo | `divider` + `heading_2` + `table` (6 filas x 4 columnas) + `paragraph` | Seccion 6.9 |
| 12 | Pie de pagina | `divider` + `paragraph` | Seccion 6.10 |

**Total de bloques de primer nivel:** ~30 bloques (incluyendo dividers, headings, column_lists, tables, callouts, paragraphs y link_to_page).

**Nota sobre limitaciones de la API de Notion:**
- La API permite un maximo de 100 bloques hijos por llamada `PATCH /v1/blocks/{id}/children`.
- Los bloques `column_list` deben incluir sus `column` hijos en la misma llamada de creacion.
- Las vistas embebidas (`linked_database`) no estan disponibles via la API publica de Notion (version 2022-06-28). Se usa `link_to_page` con `database_id` como alternativa, lo cual enlaza a la base de datos completa. Los filtros y agrupaciones de vista deben configurarse manualmente en la UI de Notion despues de crear la pagina.
- Los colores condicionales por valor de propiedad (p.ej., rojo si Resultado=Falla) son una funcion de la UI de Notion y no de la API.

---

## Verificacion de Datos Reales

Todas las metricas de este documento han sido verificadas contra el codigo fuente y la documentacion existente:

| Metrica | Valor | Fuente de verificacion |
|---------|-------|----------------------|
| Tests totales | 96 (91 passed + 5 xpassed) | `docs/07-evidence/artifacts/phase3/2026-02-13_0135/pytest-q.txt` |
| Skills | 11 archivos | `src/core/skills/*.py` (excluyendo `__init__.py`) |
| Feature flags | 9 | `src/core/config.py` — dataclass Config |
| Entradas Notion | 81 (43+12+26) | `docs/06-integrations/NOTION-OS.md` seccion 4 |
| Entradas cache | 8 | `data/cache/demo_cache.json` — 8 objetos |
| Componentes health | 8 | `src/routes/health.py` — dict components |
| Tramites | 3 (IMV, Empadronamiento, Tarjeta Sanitaria) | KB Tramites DB y `data/cache/demo_cache.json` |
| Idiomas | 2 (ES, FR) | `data/cache/demo_cache.json` — campos idioma |
| Gates | 22/22 PASS | `docs/07-evidence/PHASE-STATUS.md` — tabla resumen |
| Deploy | Render free tier, Frankfurt | `render.yaml` — region: frankfurt, plan: free |
| Equipo | 5 miembros | `docs/00-EXECUTIVE-SUMMARY.md` |
| DB IDs | 3 IDs verificados | `docs/06-integrations/NOTION-OS.md` |
| Pagina raiz | 304c5a0f-372a-801f-995f-ce24036350ad | `docs/06-integrations/NOTION-OS.md` seccion 5 |

---

## Referencias

- Notion OS (documentacion completa): `docs/06-integrations/NOTION-OS.md`
- Estado de Fases: `docs/07-evidence/PHASE-STATUS.md`
- Resumen Ejecutivo: `docs/00-EXECUTIVE-SUMMARY.md`
- Configuracion: `src/core/config.py`
- Health endpoint: `src/routes/health.py`
- Cache: `data/cache/demo_cache.json`
- Skills: `src/core/skills/`
- Deploy: `render.yaml`
- Evidencia pytest: `docs/07-evidence/artifacts/phase3/2026-02-13_0135/pytest-q.txt`
