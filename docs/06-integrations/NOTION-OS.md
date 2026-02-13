# NOTION OS — CivicAid Voice / Clara

> **Resumen en una linea:** Sistema operativo del proyecto en Notion con 3 bases de datos, 81 entradas y gestion completa de backlog, base de conocimiento y evidencia de tests.

## Que es

Notion es la fuente de verdad (source of truth) para la gestion del proyecto CivicAid Voice. Toda tarea, tramite y resultado de test vive aqui. Si no esta en Notion, no ocurrio. El workspace **CivicAid OS** centraliza la planificacion, el conocimiento verificado y la evidencia de calidad.

## Para quien

- Jueces y revisores del hackathon que necesitan evaluar el progreso del proyecto.
- Miembros del equipo que gestionan tareas, dependencias y prioridades.
- El agente Notion Ops que mantiene las bases de datos via MCP.

## Que incluye

- 3 bases de datos: Backlog / Issues, KB Tramites, Demo & Testing.
- 81 entradas en total (43 Backlog + 12 KB + 26 Testing).
- Schemas completos con propiedades, tipos y opciones de cada DB.
- Integracion con MCP (`notionApi`) para operaciones automatizadas.
- Script de poblacion: `bash scripts/populate_notion.sh`.

## Que NO incluye

- Tokens reales (nunca se incluyen en documentacion).
- Integraciones con herramientas externas mas alla de MCP.
- Plantillas de paginas personalizadas.

---

## Datos generales

| Clave | Valor |
|---|---|
| **Workspace** | CivicAid OS |
| **Bases de datos** | 3 (Backlog, KB Tramites, Demo & Testing) |
| **Paginas** | 3 (Clara Resumen Fase 0+1, Phase 2 Hardening & Deploy, Phase 3 Demo Ready) |
| **MCP** | `@notionhq/notion-mcp-server` via `~/.mcp.json` |
| **Token** | Configurado en `~/.mcp.json` (NUNCA incluir el valor real) |
| **Script de poblacion** | `bash scripts/populate_notion.sh` (33 entradas Fase 1) |
| **Total de entradas** | 81 en 3 DBs (43 Backlog, 12 KB, 26 Testing) |
| **Ultima verificacion** | 2026-02-12 |

---

## 1. Bases de datos

### 1.1 Backlog / Issues

**Notion DB ID:** `304c5a0f-372a-81de-92a8-f54c03b391c0`

Sprint board para todas las tareas, incidencias y entregables del proyecto.

**Schema de propiedades:**

| Propiedad | Tipo | Valores / Descripcion |
|---|---|---|
| **Titulo** | Title | Nombre descriptivo de la tarea |
| **Estado** | Select | `Backlog`, `En progreso`, `En review`, `Hecho`, `Bloqueado` |
| **Gate** | Select | `G0-Tooling`, `G1-Texto`, `G2-Audio`, `G3-Demo`, `Infra` |
| **Owner** | Select | `Robert`, `Marcos`, `Daniel`, `Andrea`, `Lucas` |
| **Prioridad** | Select | `P0-demo`, `P1`, `P2` |
| **Horas est.** | Number | 0.5 a 8 |
| **DoD** | Rich Text | Definicion de hecho — criterios de aceptacion |
| **Depende de** | Rich Text | IDs de tareas de las que depende (ej. "D1.1, D1.3") |
| **GitHub Issue** | URL | Enlace a la issue correspondiente en GitHub |
| **Dia** | Select | `Dia 1`, `Dia 2`, `Dia 3` |

**Valores de Estado:**

| Estado | Significado | Color |
|---|---|---|
| `Backlog` | Identificado, no priorizado | Gris |
| `En progreso` | Desarrollo activo | Amarillo |
| `En review` | Pendiente de revision | Naranja |
| `Hecho` | Completado y verificado | Verde |
| `Bloqueado` | Bloqueado por dependencia | Rojo |

> **Nota sobre Owner:** Se usa `Select` en lugar de `Person` porque el tipo Person de la API de Notion requiere IDs de usuario del workspace que son dificiles de automatizar. Funcionalmente equivalente para filtrado y agrupacion Kanban.

> **Nota sobre Depende de:** Se usa `Rich Text` en lugar de `Relation` porque el tipo Relation requiere IDs de pagina que no existen hasta que se crean las paginas. Se escriben referencias por nombre de tarea (ej. "D1.1: Setup MCP").

---

### 1.2 KB Tramites

**Notion DB ID:** `304c5a0f-372a-81ff-9d45-c785e69f7335`

Base de conocimiento verificada para tramites administrativos espanoles. **Es la fuente de verdad que Clara usa para responder a los usuarios.**

**Schema de propiedades:**

| Propiedad | Tipo | Valores / Descripcion |
|---|---|---|
| **Tramite** | Title | Nombre del tramite (IMV, Empadronamiento, Tarjeta Sanitaria) |
| **Campo** | Select | `Descripcion`, `Requisitos`, `Documentos`, `Pasos` |
| **Valor** | Rich Text | Contenido informativo del campo |
| **Fuente URL** | URL | URL oficial de la fuente gubernamental |
| **Organismo** | Select | `Seguridad Social`, `Ayuntamiento Madrid`, `Comunidad de Madrid` |
| **Estado** | Select | `Verificado`, `Pendiente`, `Desactualizado` |
| **Fecha verificacion** | Date | Fecha de la ultima verificacion |
| **Notas** | Rich Text | Notas internas, excepciones, casos especiales |

**Cobertura (3 tramites x 4 campos = 12 entradas):**

| Tramite | Organismo | Campos | Estado |
|---|---|---|---|
| IMV | Seguridad Social | Descripcion, Requisitos, Documentos, Pasos | Verificado |
| Empadronamiento | Ayuntamiento Madrid | Descripcion, Requisitos, Documentos, Pasos | Verificado |
| Tarjeta Sanitaria | Comunidad de Madrid | Descripcion, Requisitos, Documentos, Pasos | Verificado |

---

### 1.3 Demo & Testing

**Notion DB ID:** `304c5a0f-372a-810d-8767-d77efbd46bb2`

Registro de ejecucion de tests. Cada fila es una ejecucion. Nunca se sobreescriben filas anteriores — siempre se crean nuevas.

**Schema de propiedades:**

| Propiedad | Tipo | Valores / Descripcion |
|---|---|---|
| **Test** | Title | ID del test (T1, T2, ..., T10, T2.1, ..., T2.6) |
| **Tipo** | Select | `Golden test`, `Edge case`, `Demo rehearsal`, `Latencia` |
| **Input** | Rich Text | Entrada exacta del test |
| **Output esperado** | Rich Text | Salida esperada |
| **Output real** | Rich Text | Salida obtenida |
| **Latencia (ms)** | Number | Tiempo de respuesta en milisegundos |
| **Resultado** | Select | `Pasa`, `Falla`, `Pendiente` |
| **Gate** | Select | `G1-Texto`, `G2-Audio`, `G3-Demo` |
| **Fecha** | Date | Fecha de ejecucion |
| **Notas** | Rich Text | Observaciones, logs de error |

**Cobertura de tests (10 golden tests Fase 1 + 6 tests Fase 2 + 10 adicionales = 26 entradas):**

| Test | Gate | Que valida |
|---|---|---|
| T1 | G1-Texto | Cache match — palabra clave exacta |
| T2 | G1-Texto | Cache miss — sin coincidencia |
| T3 | G1-Texto | Cache match — tipo imagen |
| T4 | G1-Texto | KB lookup — empadronamiento |
| T5 | G1-Texto | Deteccion de idioma — frances |
| T6 | G2-Audio | Parseo webhook — mensaje de texto |
| T7 | G2-Audio | Parseo webhook — mensaje de audio |
| T8 | G2-Audio | Pipeline — texto stub E2E |
| T9 | G2-Audio | Demo WA texto E2E |
| T10 | G2-Audio | Demo WA audio stub E2E |
| T2.1 | G2-Audio | Validacion firma webhook Twilio |
| T2.2 | G1-Texto | Endpoint /health en Render |
| T2.3 | G1-Texto | Cron warm-up mantiene servicio activo |
| T2.4 | G1-Texto | DBs Notion pobladas con Fase 2 |
| T2.5 | G1-Texto | phase2_verify.sh pasa todos los checks |
| T2.6 | G1-Texto | Sin secretos en el repositorio |

---

## 2. Vistas

### Vistas del Backlog

| Vista | Tipo | Agrupar por | Filtro |
|---|---|---|---|
| **Kanban por Estado** | Board | Estado | Ocultar Hecho > 7 dias |
| **Board por Gate** | Board | Gate | Solo Estado != Hecho |
| **Tabla por Owner** | Table | Owner | Todas |
| **Calendario por Dia** | Calendar | Dia | Solo con Dia asignado |

### Vistas de KB Tramites

| Vista | Tipo | Filtro |
|---|---|---|
| **Todos los Tramites** | Table | Ninguno |
| **Pendientes** | Table | Estado = Pendiente |
| **Verificados** | Table | Estado = Verificado |

### Vistas de Demo & Testing

| Vista | Tipo | Agrupar por / Filtro |
|---|---|---|
| **Board por Gate** | Board | Agrupar: Gate |
| **Fallos** | Table | Resultado = Falla |
| **Demo rehearsal** | Table | Tipo = Demo rehearsal |

---

## 3. Integracion MCP

### Configuracion del token

**Archivo:** `~/.mcp.json`

```json
{
  "mcpServers": {
    "notionApi": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "<TU_TOKEN_AQUI>",
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer <TU_TOKEN_AQUI>\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

> **IMPORTANTE:** Nunca incluir el token real en documentacion ni en el repositorio. El token se configura unicamente en `~/.mcp.json` y se necesita reiniciar Claude Code despues de modificarlo.

### IDs de las bases de datos (referencia)

| Base de datos | Notion DB ID |
|---|---|
| **Backlog / Issues** | `304c5a0f-372a-81de-92a8-f54c03b391c0` |
| **KB Tramites** | `304c5a0f-372a-81ff-9d45-c785e69f7335` |
| **Demo & Testing** | `304c5a0f-372a-810d-8767-d77efbd46bb2` |

### Operaciones MCP disponibles

| Operacion | Herramienta MCP | Ejemplo |
|---|---|---|
| Buscar | `mcp__notionApi__API-post-search` | `{"query": "IMV"}` |
| Obtener DB | `mcp__notionApi__API-retrieve-a-database` | `{database_id: "304c5a0f..."}` |
| Consultar DB | `mcp__notionApi__API-query-data-source` | `{database_id: "...", body: {filter: ...}}` |
| Crear pagina | `mcp__notionApi__API-post-page` | `{body: {parent: ..., properties: ...}}` |
| Actualizar pagina | `mcp__notionApi__API-patch-page` | `{page_id: "...", body: {properties: ...}}` |

---

## 4. Como poblar las bases de datos

### Script automatico

```bash
bash scripts/populate_notion.sh
```

El script realiza las siguientes acciones:
1. Extrae el token de `~/.mcp.json` (o de la variable de entorno `NOTION_TOKEN`).
2. Verifica el token contra la API de Notion.
3. Crea 11 entradas en Backlog (Fase 1).
4. Crea 12 entradas en KB Tramites (3 tramites x 4 campos).
5. Crea 10 entradas en Demo & Testing (T1-T10).
6. Muestra un resumen con entradas creadas y fallidas.

### Estado de poblacion (2026-02-12, post Fase 3)

| Base de datos | Total | Desglose | Estado |
|---|---|---|---|
| Backlog / Issues | 43 | 42 Hecho, 1 Backlog | Poblada + owners |
| KB Tramites | 12 | 12 Verificado | Poblada |
| Demo & Testing | 26 | 26 Pasa | Poblada + actualizada |
| **Total** | **81** | | **Todas pobladas y verificadas** |

### Verificacion manual via curl

```bash
# Verificar token (sustituir $NOTION_TOKEN por el valor real)
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" | python3 -m json.tool

# Consultar todas las entradas del Backlog
curl -s -X POST "https://api.notion.com/v1/databases/304c5a0f-372a-81de-92a8-f54c03b391c0/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

# Buscar en todas las paginas compartidas
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "CivicAid"}'
```

### Verificacion via MCP

Desde Claude Code con el MCP de Notion activo:

1. **Buscar:** Usar `mcp__notionApi__API-post-search` con `{"query": "IMV"}` para verificar que las entradas existen.
2. **Consultar DB:** Usar `mcp__notionApi__API-retrieve-a-database` con el ID del Backlog para ver el schema.
3. **Contar entradas:** Consultar cada DB y contar resultados para verificar los totales (43 + 12 + 26 = 81).

---

## 5. Paginas de Notion

| Pagina | ID | Padre |
|---|---|---|
| CivicAid OS (raiz) | `304c5a0f-372a-801f-995f-ce24036350ad` | Workspace |
| Clara Resumen Fase 0 + Fase 1 | `305c5a0f-372a-81c8-b609-cc5fe793bfe4` | CivicAid OS |
| Phase 2 — Hardening & Deploy | `305c5a0f-372a-813b-8915-f7e6c21fd055` | CivicAid OS |
| Phase 3 — Demo Ready | `305c5a0f-372a-818d-91a7-f59c22551350` | CivicAid OS |

**Enlaces rapidos:**
- CivicAid OS (raiz): `https://www.notion.so/CivicAid-OS-304c5a0f372a801f995fce24036350ad`
- Pagina Fase 2: `https://www.notion.so/Phase-2-Hardening-Deploy-305c5a0f372a813b8915f7e6c21fd055`
- Pagina Fase 3: `https://www.notion.so/Phase-3-Demo-Ready-305c5a0f372a818d91a7f59c22551350`
- Backlog DB: `https://notion.so/304c5a0f372a81de92a8f54c03b391c0`
- KB Tramites DB: `https://notion.so/304c5a0f372a81ff9d45c785e69f7335`
- Testing DB: `https://notion.so/304c5a0f372a810d8767d77efbd46bb2`

---

## 6. Navegacion para terceros (jueces y revisores)

| Quieres... | Ve a... |
|---|---|
| Ver progreso del proyecto | **Backlog / Issues** > Kanban por Estado |
| Entender que sabe Clara | **KB Tramites** > Tabla por Tramite |
| Revisar resultados de tests | **Demo & Testing** > Board por Gate |
| Filtrar por gate especifico | Filtrar cualquier DB por `Gate = G1-Texto` / `G2-Audio` / `G3-Demo` |
| Ver quien es responsable | **Backlog** > filtrar por `Owner` |
| Encontrar bloqueos | **Backlog** > filtrar `Estado = Bloqueado` |

---

## 7. Reglas de uso

1. **Nunca borrar registros** — marcar como `Hecho` o `Desactualizado`.
2. **Una fila por ejecucion de test** — nunca sobreescribir resultados anteriores.
3. **Enlazar GitHub Issues** — toda tarea del Backlog debe referenciar su issue de GitHub.
4. **Verificar KB periodicamente** — revisar `Fecha verificacion` para datos obsoletos.
5. **Usar Depende de** — escribir IDs de tareas (ej. "D1.1, D1.3") para expresar dependencias.
6. **Owner = Select** — usar nombres de miembros del equipo, no IDs de Notion Person.
7. **Notion es la fuente de verdad** — los archivos locales reflejan Notion, no al reves.

---

## Como se verifica

| # | Verificacion | Como |
|---|---|---|
| 1 | Token activo | `curl https://api.notion.com/v1/users/me` devuelve 200 |
| 2 | 3 DBs existen | Consultar cada DB ID y recibir schema |
| 3 | 81 entradas totales | Consultar cada DB y sumar: 43 + 12 + 26 = 81 |
| 4 | KB completa | 12 entradas: 3 tramites x 4 campos, todas en estado Verificado |
| 5 | Script funciona | `bash scripts/populate_notion.sh` ejecuta sin errores |

## Referencias

- Script de poblacion: `scripts/populate_notion.sh`
- Configuracion MCP: `~/.mcp.json`
- Documentacion MCP: `docs/06-integrations/MCP-TOOLS-REFERENCE.md`
- Documentacion API Notion: [https://developers.notion.com](https://developers.notion.com)
