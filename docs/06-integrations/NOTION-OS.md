# NOTION OS — Workspace CivicAid

> **Workspace:** CivicAid OS
> **Bases de datos:** 4 (Backlog, KB Trámites, Demo & Testing, Phase Releases)
> **Integraciones:** MCP via Notion API

---

## 1. Bases de Datos

### 1.1 Backlog / Issues

**Notion DB ID:** `304c5a0f-372a-81de-92a8-f54c03b391c0`

Base de datos principal para gestión de tareas, issues y sprints del proyecto.

| Propiedad | Tipo | Descripción |
|---|---|---|
| **Titulo** | Title | Nombre descriptivo de la tarea o issue |
| **Estado** | Select | Estado actual: `Backlog`, `To Do`, `In Progress`, `Review`, `Done`, `Blocked` |
| **Gate** | Select | Gate al que pertenece: `G1`, `G2`, `G3` |
| **Owner** | Person | Miembro del equipo asignado |
| **Prioridad** | Select | Nivel de prioridad: `P0-Crítica`, `P1-Alta`, `P2-Media`, `P3-Baja` |
| **Horas est.** | Number | Estimación de horas de trabajo |
| **DoD** | Rich Text | Definition of Done — criterios de aceptación |
| **Dia** | Date | Fecha planificada (para timeline y sprints) |
| **GitHub Issue** | URL | Enlace al issue correspondiente en GitHub |
| **Depende de** | Relation | Relación con otras tareas de las que depende |

**Valores del campo Estado:**

| Estado | Significado | Color |
|---|---|---|
| `Backlog` | Identificada, no priorizada | Gris |
| `To Do` | Priorizada para el sprint actual | Azul |
| `In Progress` | En desarrollo activo | Amarillo |
| `Review` | Pendiente de revisión | Naranja |
| `Done` | Completada y verificada | Verde |
| `Blocked` | Bloqueada por dependencia externa | Rojo |

---

### 1.2 KB Trámites

**Notion DB ID:** `304c5a0f-372a-81ff-9d45-c785e69f7335`

Base de conocimiento con información verificada sobre trámites administrativos españoles. Esta es la fuente de verdad que Clara utiliza para responder a los usuarios.

| Propiedad | Tipo | Descripción |
|---|---|---|
| **Tramite** | Title | Nombre del trámite (ej. "Empadronamiento", "IMV") |
| **Campo** | Select | Tipo de información: `Descripcion`, `Requisitos`, `Documentos`, `Pasos`, `Plazo`, `Coste`, `Donde` |
| **Valor** | Rich Text | Contenido informativo del campo |
| **Fuente URL** | URL | Enlace a la fuente oficial de la información |
| **Organismo** | Select | Organismo responsable: `Seguridad Social`, `Ayuntamiento`, `Extranjería`, `SEPE`, `Otro` |
| **Estado** | Select | Estado de verificación: `Verificado`, `Pendiente`, `Desactualizado` |
| **Fecha verificacion** | Date | Última fecha en que se verificó la información |
| **Notas** | Rich Text | Notas internas, excepciones, casos especiales |

**Ejemplo de registros para IMV:**

| Tramite | Campo | Valor | Organismo |
|---|---|---|---|
| IMV | Descripcion | Prestación económica de la Seguridad Social para personas en vulnerabilidad | Seguridad Social |
| IMV | Requisitos | Residencia legal en España, edad 23-65, renta inferior a umbrales... | Seguridad Social |
| IMV | Documentos | DNI/NIE, certificado de empadronamiento, declaración de renta... | Seguridad Social |
| IMV | Pasos | 1. Reunir documentos 2. Solicitar en sede electrónica o presencial... | Seguridad Social |

---

### 1.3 Demo & Testing

**Notion DB ID:** `304c5a0f-372a-810d-8767-d77efbd46bb2`

Registro de todas las ejecuciones de tests y resultados de las demos. Cada fila es una ejecución de un test específico.

| Propiedad | Tipo | Descripción |
|---|---|---|
| **Test** | Title | Identificador del test (ej. "T1", "T2", ..., "T10") |
| **Tipo** | Select | Tipo de test: `Unit`, `Integration`, `E2E`, `Manual` |
| **Input** | Rich Text | Datos de entrada del test |
| **Output esperado** | Rich Text | Resultado esperado según el test plan |
| **Output real** | Rich Text | Resultado obtenido en la ejecución |
| **Latencia ms** | Number | Tiempo de respuesta en milisegundos |
| **Resultado** | Select | `PASS`, `FAIL`, `SKIP`, `ERROR` |
| **Gate** | Select | Gate al que pertenece: `G1`, `G2` |
| **Fecha** | Date | Fecha de ejecución del test |
| **Notas** | Rich Text | Observaciones, errores encontrados, logs relevantes |

---

### 1.4 Phase Releases (Nueva)

Base de datos para rastrear las fases del proyecto y sus releases.

| Propiedad | Tipo | Descripción |
|---|---|---|
| **Phase** | Title | Nombre de la fase (ej. "Phase 1 — Cache + KB", "Phase 2 — Whisper + Audio") |
| **Status** | Select | `Planning`, `In Progress`, `Testing`, `Released`, `Rolled Back` |
| **Start date** | Date | Fecha de inicio de la fase |
| **End date** | Date | Fecha de fin (real o estimada) |
| **Commit SHA** | Rich Text | Hash del commit de Git asociado al release |
| **Render URL** | URL | URL del despliegue en Render para esta fase |
| **Tests pass?** | Checkbox | Indica si todos los tests del gate correspondiente pasaron |
| **Notes** | Rich Text | Notas sobre la release, cambios destacados, incidencias |
| **Owner** | Person | Responsable de la fase |

---

## 2. Vistas

### 2.1 Kanban por Estado

Vista principal para el trabajo diario. Agrupa las tareas por su estado actual.

**Configuración:**
- **Tipo:** Board
- **Group by:** Estado
- **Columnas:** Backlog → To Do → In Progress → Review → Done → Blocked
- **Filtro:** Ocultar tareas con Estado = `Done` de hace más de 7 días
- **Orden:** Prioridad (P0 primero)

### 2.2 Board por Gate

Vista para planificación de sprints y seguimiento de progreso por gate.

**Configuración:**
- **Tipo:** Board
- **Group by:** Gate
- **Columnas:** G1, G2, G3
- **Filtro:** Solo tareas con Estado distinto de `Done`
- **Orden:** Prioridad, luego Horas est.

### 2.3 Timeline por Día

Vista de Gantt para visualizar la planificación temporal del hackathon.

**Configuración:**
- **Tipo:** Timeline
- **Date property:** Dia
- **Group by:** Gate
- **Filtro:** Solo tareas con Dia asignado

---

## 3. Rutina Diaria

Seguir esta rutina al inicio y al final de cada sesión de trabajo:

### Al Inicio del Día

1. **Revisar el Kanban** — Ver qué tareas están `In Progress` y `Blocked`.
2. **Mover tareas** — Pasar tareas de `To Do` a `In Progress` según prioridad.
3. **Verificar dependencias** — Revisar el campo `Depende de` para tareas bloqueadas.
4. **Actualizar estados** — Si algo se completó fuera de Notion, actualizar a `Done`.

### Durante el Desarrollo

5. **Actualizar estado** — Cuando empiezas una tarea, moverla a `In Progress`.
6. **Registrar bloqueos** — Si algo te bloquea, mover a `Blocked` y añadir nota.
7. **Log de tests** — Después de ejecutar tests, registrar resultados en la DB Demo & Testing:
   - Crear una fila por cada test ejecutado.
   - Rellenar `Output real`, `Latencia ms`, `Resultado`.
   - Si falla, detallar el error en `Notas`.

### Al Final del Día

8. **Mover completadas** — Pasar tareas terminadas a `Done`.
9. **Actualizar Phase Releases** — Si se hizo deploy, actualizar el commit SHA y marcar tests.
10. **Preparar el siguiente día** — Mover las tareas prioritarias a `To Do`.

---

## 4. Integración MCP (Model Context Protocol)

CivicAid utiliza la integración MCP de Notion para que Claude pueda leer y escribir en las bases de datos directamente.

### Configuración del Token

El token de Notion se configura en el archivo de configuración MCP:

**Archivo:** `~/.mcp.json`

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ntn_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

**IMPORTANTE:** Reemplazar `ntn_XXXX...` con el token real de la integración de Notion. Nunca subir este archivo al repositorio.

### IDs de las Bases de Datos

Los IDs de las bases de datos se configuran en el archivo de settings del proyecto:

**Archivo:** `project-settings.json` (o `.claude/settings.json`)

```json
{
  "notion": {
    "databases": {
      "backlog": "304c5a0f-372a-81de-92a8-f54c03b391c0",
      "kb_tramites": "304c5a0f-372a-81ff-9d45-c785e69f7335",
      "testing": "304c5a0f-372a-810d-8767-d77efbd46bb2"
    }
  }
}
```

### Operaciones MCP Disponibles

Con la integración MCP, Claude puede ejecutar estas operaciones directamente:

| Operación | Descripción | Ejemplo de uso |
|---|---|---|
| Leer base de datos | Consultar registros con filtros | "Muéstrame las tareas bloqueadas del G1" |
| Crear registro | Añadir nuevas tareas o resultados de tests | "Crea una tarea para implementar el cache" |
| Actualizar registro | Cambiar estado, owner, prioridad | "Marca T1 como PASS con latencia 45ms" |
| Buscar | Buscar por texto en cualquier DB | "Busca el trámite de empadronamiento en la KB" |

### Verificar la Integración

Para verificar que la integración MCP funciona correctamente:

1. Asegurar que `~/.mcp.json` tiene el token correcto.
2. Verificar que la integración de Notion tiene acceso a las 4 bases de datos.
3. Probar con una consulta simple: pedir a Claude que liste las tareas del Backlog.

---

## 5. Estructura de IDs — Referencia Rápida

| Base de Datos | Notion DB ID |
|---|---|
| **Backlog / Issues** | `304c5a0f-372a-81de-92a8-f54c03b391c0` |
| **KB Trámites** | `304c5a0f-372a-81ff-9d45-c785e69f7335` |
| **Demo & Testing** | `304c5a0f-372a-810d-8767-d77efbd46bb2` |
| **Phase Releases** | _(crear y añadir ID aquí)_ |

**Formato de ID en API:** Para usar en la API de Notion, el ID se puede usar con o sin guiones. Ambos formatos son válidos:
- Con guiones: `304c5a0f-372a-81de-92a8-f54c03b391c0`
- Sin guiones: `304c5a0f372a81de92a8f54c03b391c0`

---

## 6. Buenas Prácticas

1. **Nunca borrar registros** — Marcar como `Done` o `Desactualizado`, pero no eliminar. Mantener el historial.
2. **Un registro por test por ejecución** — No sobrescribir resultados anteriores. Crear nueva fila para cada ejecución.
3. **Vincular GitHub Issues** — Siempre que se cree una tarea, crear el issue correspondiente en GitHub y vincular con URL.
4. **Verificar la KB periódicamente** — La información de trámites puede cambiar. Revisar el campo `Fecha verificacion`.
5. **Usar Depende de** — Modelar las dependencias explícitamente para evitar bloqueos no previstos.
6. **Phase Releases como checkpoint** — Cada deploy a Render debe tener un registro en Phase Releases con el commit SHA correspondiente.

---

## 7. Estado de Sincronizacion (2026-02-12)

> **BLOCKER:** El token de Notion en `~/.mcp.json` retorna `401 Unauthorized`.
> Todas las operaciones de lectura/escritura fallan hasta que se regenere el token.

### Estado actual de las DBs

| Base de Datos | Entries | Estado |
|---|---|---|
| Backlog / Issues | 0 | Pendiente — token invalido |
| KB Tramites | 0 | Pendiente — token invalido |
| Demo & Testing | 0 | Pendiente — token invalido |
| Phase Releases | N/A | DB no creada aun |

### Datos preparados para poblar (ejecutar `scripts/populate_notion.sh`)

**Backlog (11 entries):**

| Titulo | Estado | Gate | Prioridad | Dia |
|---|---|---|---|---|
| Setup MCP + skills + agents | Hecho | G0-Tooling | P0-demo | Dia 1 |
| Crear Notion CivicAid OS (3 DBs) | Hecho | G0-Tooling | P0-demo | Dia 1 |
| Implementar cache-first con 8 entries + MP3 | Hecho | G1-Texto | P0-demo | Dia 1 |
| Cargar KB con 3 tramites verificados | Hecho | G1-Texto | P0-demo | Dia 1 |
| Implementar deteccion de idioma | Hecho | G1-Texto | P1 | Dia 1 |
| Implementar /webhook para Twilio WA | Hecho | G2-Audio | P0-demo | Dia 1 |
| Pipeline orquestador (texto + audio + fallback) | Hecho | G2-Audio | P0-demo | Dia 1 |
| Integrar Whisper con timeout y OGG-WAV | Hecho | G2-Audio | P0-demo | Dia 1 |
| Dockerfile + render.yaml + CI workflow | En progreso | Infra | P0-demo | Dia 2 |
| Deploy a Render + configurar Twilio webhook | Backlog | Infra | P0-demo | Dia 2 |
| Demo rehearsal + video backup + screenshots | Backlog | G3-Demo | P0-demo | Dia 3 |

**KB Tramites (12 entries):**

| Tramite | Campo | Organismo | Estado |
|---|---|---|---|
| IMV | Descripcion | Seguridad Social | Verificado |
| IMV | Requisitos | Seguridad Social | Verificado |
| IMV | Documentos | Seguridad Social | Verificado |
| IMV | Pasos | Seguridad Social | Verificado |
| Empadronamiento | Descripcion | Ayuntamiento Madrid | Verificado |
| Empadronamiento | Requisitos | Ayuntamiento Madrid | Verificado |
| Empadronamiento | Documentos | Ayuntamiento Madrid | Verificado |
| Empadronamiento | Pasos | Ayuntamiento Madrid | Verificado |
| Tarjeta Sanitaria | Descripcion | Comunidad de Madrid | Verificado |
| Tarjeta Sanitaria | Requisitos | Comunidad de Madrid | Verificado |
| Tarjeta Sanitaria | Documentos | Comunidad de Madrid | Verificado |
| Tarjeta Sanitaria | Pasos | Comunidad de Madrid | Verificado |

**Demo & Testing (10 entries — T1-T10):**

| Test | Tipo | Gate | Resultado | Fecha |
|---|---|---|---|---|
| T1 — Cache Match Keyword Exacto | Golden test | G1-Texto | Pasa | 2026-02-12 |
| T2 — Cache Match Sin Match | Golden test | G1-Texto | Pasa | 2026-02-12 |
| T3 — Cache Match Imagen Demo | Golden test | G1-Texto | Pasa | 2026-02-12 |
| T4 — KB Lookup Empadronamiento | Golden test | G1-Texto | Pasa | 2026-02-12 |
| T5 — Detect Language Frances | Golden test | G1-Texto | Pasa | 2026-02-12 |
| T6 — Webhook Parse Text | Golden test | G2-Audio | Pasa | 2026-02-12 |
| T7 — Webhook Parse Audio | Golden test | G2-Audio | Pasa | 2026-02-12 |
| T8 — Pipeline Text Stub | Golden test | G2-Audio | Pasa | 2026-02-12 |
| T9 — WA Text Demo E2E | Golden test | G2-Audio | Pasa | 2026-02-12 |
| T10 — WA Audio Demo Stub E2E | Golden test | G2-Audio | Pasa | 2026-02-12 |

### Para desbloquear

1. Ir a https://www.notion.so/my-integrations
2. Seleccionar la integracion "CivicAid Clara"
3. Regenerar el Internal Integration Secret
4. Actualizar en `~/.mcp.json` (campo `NOTION_TOKEN` y dentro de `OPENAPI_MCP_HEADERS`)
5. Reiniciar Claude Code
6. Ejecutar: `bash scripts/populate_notion.sh`

---

> **Nota:** Esta documentacion refleja el estado actual del workspace. A medida que el proyecto evolucione, actualizar esta guia con nuevas bases de datos, vistas o integraciones.
