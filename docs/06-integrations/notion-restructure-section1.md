# SECCION 1 — SITEMAP NOTION: CivicAid OS

> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good — UDIT
> **Fecha:** 2026-02-13
> **Autora de seccion:** Andrea (Notion/Slides/Coordinacion)
> **Proposito:** Mapa completo del workspace Notion actual y propuesta de reestructuracion para mejorar navegabilidad, trazabilidad y experiencia de evaluacion.

---

## 1.1 Arbol Jerarquico — Estado Actual

El workspace **CivicAid OS** tiene actualmente 1 pagina raiz, 3 sub-paginas de fase y 3 bases de datos. Total: **81 entradas** distribuidas en 3 DBs.

```
CivicAid OS (Raiz)
│   ID: 304c5a0f-372a-801f-995f-ce24036350ad
│   Tipo: Page
│   Descripcion: Pagina raiz del workspace. Punto de entrada unico.
│
├── Clara Resumen Fase 0 + Fase 1
│   │   ID: 305c5a0f-372a-81c8-b609-cc5fe793bfe4
│   │   Tipo: Page
│   │   Descripcion: Resumen consolidado de planificacion (F0) e implementacion MVP (F1).
│   │              Contiene narrativa del plan maestro y cierre del MVP con 32 tests.
│   │
│   └── (sin sub-paginas conocidas)
│
├── Phase 2 — Hardening & Deploy
│   │   ID: 305c5a0f-372a-813b-8915-f7e6c21fd055
│   │   Tipo: Page
│   │   Descripcion: Documentacion del endurecimiento: deploy Render, Twilio pipeline,
│   │              cron warm-up, seguridad, observabilidad. 93 tests al cierre.
│   │
│   └── (sin sub-paginas conocidas)
│
├── Phase 3 — Demo Ready
│   │   ID: 305c5a0f-372a-818d-91a7-f59c22551350
│   │   Tipo: Page
│   │   Descripcion: Preparacion para demo en vivo. Guion 6-8 min, 2 momentos WOW,
│   │              QA Deep Audit, 96 tests finales (91 passed + 5 xpassed).
│   │
│   └── (sin sub-paginas conocidas)
│
├── Backlog / Issues
│   │   ID: 304c5a0f-372a-81de-92a8-f54c03b391c0
│   │   Tipo: Database
│   │   Entradas: 43 (42 Hecho, 1 Backlog)
│   │   Descripcion: Sprint board con todas las tareas, incidencias y entregables.
│   │              Propiedades: Titulo, Estado, Gate, Owner, Prioridad, Horas est.,
│   │              DoD, Depende de, GitHub Issue, Dia.
│   │
│   ├── [Vista] Kanban por Estado (Board — agrupado por Estado, oculta Hecho > 7 dias)
│   ├── [Vista] Board por Gate (Board — agrupado por Gate, solo Estado != Hecho)
│   ├── [Vista] Tabla por Owner (Table — agrupado por Owner, todas las entradas)
│   └── [Vista] Calendario por Dia (Calendar — agrupado por Dia, solo con Dia asignado)
│
├── KB Tramites
│   │   ID: 304c5a0f-372a-81ff-9d45-c785e69f7335
│   │   Tipo: Database
│   │   Entradas: 12 (3 tramites x 4 campos, todas en estado Verificado)
│   │   Descripcion: Base de conocimiento verificada. Fuente de verdad que Clara
│   │              usa para responder. Tramites: IMV, Empadronamiento, Tarjeta Sanitaria.
│   │              Propiedades: Tramite, Campo, Valor, Fuente URL, Organismo, Estado,
│   │              Fecha verificacion, Notas.
│   │
│   ├── [Vista] Todos los Tramites (Table — sin filtro)
│   ├── [Vista] Pendientes (Table — Estado = Pendiente)
│   └── [Vista] Verificados (Table — Estado = Verificado)
│
└── Demo & Testing
    │   ID: 304c5a0f-372a-810d-8767-d77efbd46bb2
    │   Tipo: Database
    │   Entradas: 26 (10 golden tests F1 + 6 tests F2 + 10 adicionales)
    │   Descripcion: Registro de ejecucion de tests. Cada fila = una ejecucion.
    │              Nunca se sobreescriben — siempre filas nuevas.
    │              Propiedades: Test, Tipo, Input, Output esperado, Output real,
    │              Latencia (ms), Resultado, Gate, Fecha, Notas.
    │
    ├── [Vista] Board por Gate (Board — agrupado por Gate)
    ├── [Vista] Fallos (Table — Resultado = Falla)
    └── [Vista] Demo rehearsal (Table — Tipo = Demo rehearsal)
```

### Resumen cuantitativo del estado actual

| Metrica | Valor |
|---------|-------|
| Paginas (sin contar raiz) | 3 |
| Bases de datos | 3 |
| Entradas totales | 81 (43 Backlog + 12 KB + 26 Testing) |
| Vistas configuradas | 11 (4 Backlog + 3 KB + 3 Testing + 1 implica raiz) |
| Niveles de profundidad | 2 (raiz -> paginas/DBs) |
| Relaciones entre DBs | 0 (no hay propiedades Relation) |
| Dashboard centralizado | No existe |
| Pagina de navegacion rapida para jueces | No existe |

---

## 1.2 Diagnostico de la Estructura Actual

### Fortalezas

1. **Fuente de verdad unica:** Toda la informacion del proyecto vive en Notion. Si no esta en Notion, no ocurrio.
2. **Schemas bien definidos:** Las 3 DBs tienen propiedades claras con tipos correctos y valores Select estandarizados.
3. **Cobertura completa:** Las 81 entradas cubren el ciclo completo: planificacion, conocimiento y calidad.
4. **Vistas funcionales:** 11 vistas pre-configuradas para distintos modos de trabajo (Kanban, tabla, calendario).
5. **Automatizacion existente:** Script `populate_notion.sh` e integracion MCP para operaciones programaticas.

### Debilidades detectadas

| # | Problema | Impacto |
|---|----------|---------|
| D1 | Las 3 paginas de fase estan al mismo nivel que las DBs, sin jerarquia clara | Un juez no sabe por donde empezar. Las paginas y las DBs compiten por atencion en la barra lateral. |
| D2 | No existe un dashboard central con metricas agregadas | Para ver el estado del proyecto hay que abrir multiples paginas y DBs por separado. |
| D3 | No hay pagina de navegacion rapida para jueces | Los jueces (audiencia principal del hackathon) deben explorar sin guia. Pierden tiempo y no ven lo mas relevante. |
| D4 | Las DBs no estan relacionadas entre si (0 propiedades Relation) | No se puede trazar una tarea del Backlog a su test correspondiente en Demo & Testing, ni vincular un tramite de KB a las tareas que lo implementaron. |
| D5 | Las paginas de fase no estan agrupadas bajo un padre comun | Nomenclatura inconsistente: "Clara Resumen Fase 0 + Fase 1" vs "Phase 2 — Hardening & Deploy" (mezcla espanol/ingles). |
| D6 | No hay seccion de "Equipo" ni asignacion visual de roles | Los owners existen como Select en Backlog, pero no hay una vista de equipo con roles y responsabilidades. |
| D7 | No hay timeline o roadmap visual | La propiedad "Dia" existe pero no hay vista Gantt ni timeline que muestre la progresion temporal del proyecto. |

---

## 1.3 Propuesta de Reestructuracion — Arbol Jerarquico Nuevo

La estructura propuesta organiza el workspace en 5 secciones logicas bajo la raiz, agrupa las fases bajo un padre comun, anade un dashboard central y una pagina de navegacion rapida para jueces.

> **Convencion:** Los nodos marcados con `[NUEVO]` son paginas o elementos que no existen actualmente y se proponen crear. Los nodos sin marca existen actualmente y se reubican o mantienen en su posicion.

```
CivicAid OS (Raiz)
│   ID: 304c5a0f-372a-801f-995f-ce24036350ad
│   Tipo: Page
│   Descripcion: Pagina raiz. Contiene callout de bienvenida, indice visual
│              con iconos y enlaces a las 5 secciones principales.
│
├── [NUEVO] Dashboard Home
│   │   Tipo: Page
│   │   Descripcion: Panel central con metricas agregadas del proyecto.
│   │              Punto de entrada principal para cualquier visitante.
│   │
│   │   Contenido propuesto:
│   │   - Callout con estado general: "Proyecto COMPLETADO — 4 fases, 96 tests, 81 entradas Notion"
│   │   - Bloque de metricas clave (callouts con numeros):
│   │     * 96 tests (91 passed + 5 xpassed)
│   │     * 11 skills en pipeline
│   │     * 9 feature flags
│   │     * 81 entradas en 3 DBs
│   │     * 3 tramites cubiertos (IMV, Empadronamiento, Tarjeta Sanitaria)
│   │     * 2 idiomas (ES, FR)
│   │   - Vista linked del Backlog filtrada por Estado != Hecho (tareas pendientes)
│   │   - Vista linked de Demo & Testing filtrada por Resultado = Falla (fallos activos)
│   │   - Vista linked de KB Tramites filtrada por Estado = Pendiente (tramites sin verificar)
│   │   - Tabla de equipo: Robert, Marcos, Lucas, Daniel, Andrea con roles
│   │   - Enlaces rapidos a: Deploy (Render), Repositorio (GitHub), Demo Runbook
│   │
│   └── (sin sub-paginas)
│
├── [NUEVO] Para Jueces — Navegacion Rapida
│   │   Tipo: Page
│   │   Descripcion: Pagina disenada exclusivamente para evaluadores del hackathon.
│   │              Muestra lo esencial en 2 minutos sin necesidad de explorar.
│   │
│   │   Contenido propuesto:
│   │   - Callout: "Bienvenidos, jueces. Esta pagina resume lo esencial de CivicAid Voice / Clara."
│   │   - Seccion "Que es Clara" — 3 frases con la propuesta de valor
│   │   - Seccion "Datos clave" — Tabla con metricas verificables:
│   │     * 96 tests automatizados
│   │     * 11 skills en pipeline
│   │     * 81 entradas en Notion (43 Backlog + 12 KB + 26 Testing)
│   │     * Deploy verificado en Render (Frankfurt, Docker, python:3.11-slim)
│   │     * 3 endpoints: /health (GET), /webhook (POST), /static/cache/* (MP3s)
│   │   - Seccion "Progreso por fases" — 4 filas con semaforo verde:
│   │     * F0 Plan Maestro — COMPLETADA
│   │     * F1 MVP (32 tests) — COMPLETADA
│   │     * F2 Hardening (93 tests) — COMPLETADA
│   │     * F3 Demo Ready (96 tests) — COMPLETADA
│   │   - Seccion "Donde verificar" — Tabla con comandos de verificacion
│   │   - Seccion "Demo en vivo" — Enlace al Runbook Demo con resumen del guion
│   │   - Seccion "Equipo" — Tabla con 5 miembros y sus roles
│   │   - Enlace directo a cada DB con descripcion de 1 linea
│   │
│   └── (sin sub-paginas)
│
├── [NUEVO] Fases del Proyecto (Grupo)
│   │   Tipo: Page
│   │   Descripcion: Contenedor que agrupa las 4 fases del proyecto bajo un padre
│   │              comun. Incluye un resumen visual con semaforo de estado.
│   │
│   ├── Clara Resumen Fase 0 + Fase 1
│   │       ID: 305c5a0f-372a-81c8-b609-cc5fe793bfe4
│   │       Tipo: Page (reubicada — antes hija directa de raiz)
│   │       Descripcion: Plan maestro (F0) e implementacion MVP (F1). 32 tests al cierre de F1.
│   │
│   ├── Phase 2 — Hardening & Deploy
│   │       ID: 305c5a0f-372a-813b-8915-f7e6c21fd055
│   │       Tipo: Page (reubicada — antes hija directa de raiz)
│   │       Descripcion: Endurecimiento, deploy Render, Twilio, seguridad. 93 tests.
│   │
│   └── Phase 3 — Demo Ready
│           ID: 305c5a0f-372a-818d-91a7-f59c22551350
│           Tipo: Page (reubicada — antes hija directa de raiz)
│           Descripcion: Demo en vivo, QA Deep Audit, ops reales. 96 tests finales.
│
├── Bases de Datos
│   │   Tipo: Seccion logica (las DBs se mantienen como hijas de la raiz pero
│   │         visualmente agrupadas mediante un heading + divider en la pagina raiz)
│   │
│   ├── Backlog / Issues
│   │   │   ID: 304c5a0f-372a-81de-92a8-f54c03b391c0
│   │   │   Tipo: Database
│   │   │   Entradas: 43 (42 Hecho, 1 Backlog)
│   │   │   Descripcion: Sprint board. Tareas, incidencias y entregables.
│   │   │   [NUEVO] Propiedad "Test vinculado": Relation -> Demo & Testing
│   │   │   [NUEVO] Propiedad "Tramite relacionado": Relation -> KB Tramites
│   │   │
│   │   ├── [Vista] Kanban por Estado (existente)
│   │   ├── [Vista] Board por Gate (existente)
│   │   ├── [Vista] Tabla por Owner (existente)
│   │   ├── [Vista] Calendario por Dia (existente)
│   │   ├── [NUEVO] [Vista] Timeline por Dia (Timeline — propiedad Dia, para roadmap visual)
│   │   └── [NUEVO] [Vista] Resumen para Jueces (Table — solo columnas: Titulo, Estado, Gate, Owner)
│   │
│   ├── KB Tramites
│   │   │   ID: 304c5a0f-372a-81ff-9d45-c785e69f7335
│   │   │   Tipo: Database
│   │   │   Entradas: 12 (3 tramites x 4 campos, todas Verificado)
│   │   │   Descripcion: Base de conocimiento verificada para respuestas de Clara.
│   │   │   [NUEVO] Propiedad "Tareas relacionadas": Relation -> Backlog / Issues
│   │   │
│   │   ├── [Vista] Todos los Tramites (existente)
│   │   ├── [Vista] Pendientes (existente)
│   │   ├── [Vista] Verificados (existente)
│   │   └── [NUEVO] [Vista] Por Organismo (Board — agrupado por Organismo)
│   │
│   └── Demo & Testing
│       │   ID: 304c5a0f-372a-810d-8767-d77efbd46bb2
│       │   Tipo: Database
│       │   Entradas: 26
│       │   Descripcion: Registro inmutable de ejecuciones de tests.
│       │   [NUEVO] Propiedad "Tarea origen": Relation -> Backlog / Issues
│       │
│       ├── [Vista] Board por Gate (existente)
│       ├── [Vista] Fallos (existente)
│       ├── [Vista] Demo rehearsal (existente)
│       ├── [NUEVO] [Vista] Cronologia (Table — ordenado por Fecha descendente)
│       └── [NUEVO] [Vista] Por Tipo (Board — agrupado por Tipo)
│
└── [NUEVO] Recursos y Referencias
        Tipo: Page
        Descripcion: Pagina auxiliar con enlaces utiles, documentacion externa
                   y guias de onboarding para nuevos miembros del equipo.

        Contenido propuesto:
        - Enlace al repositorio GitHub
        - Enlace a Render Dashboard
        - Enlace a Twilio Console
        - Enlace a cron-job.org
        - Tabla de feature flags (9 flags con nombre, descripcion y valor por defecto)
        - Tabla de endpoints (3: /health, /webhook, /static/cache/*)
        - Guia rapida MCP: como usar notionApi desde Claude Code
```

---

## 1.4 Tabla Comparativa — Estructura Actual vs Propuesta

| Aspecto | Estado Actual | Propuesta | Mejora |
|---------|---------------|-----------|--------|
| **Paginas totales** | 4 (1 raiz + 3 fases) | 8 (1 raiz + Dashboard + Para Jueces + Grupo Fases + 3 fases + Recursos) | +4 paginas funcionales |
| **Bases de datos** | 3 | 3 (mismas, con propiedades nuevas) | Sin cambio en cantidad, mejora en relaciones |
| **Relaciones entre DBs** | 0 | 3 (Backlog <-> Testing, Backlog <-> KB, Testing <-> Backlog) | Trazabilidad completa tarea-test-tramite |
| **Vistas totales** | 11 | 16 (11 existentes + 5 nuevas) | +5 vistas especializadas |
| **Dashboard central** | No existe | Si — metricas, estado, enlaces rapidos | Reduccion de tiempo para entender el estado |
| **Pagina para jueces** | No existe | Si — contenido curado en 2 minutos | Experiencia de evaluacion optimizada |
| **Agrupacion de fases** | Plana (3 paginas sueltas al nivel raiz) | Jerarquica (3 paginas bajo "Fases del Proyecto") | Sidebar mas limpia, jerarquia logica |
| **Profundidad maxima** | 2 niveles (raiz -> paginas/DBs) | 3 niveles (raiz -> Fases -> F0+F1/F2/F3) | Organizacion mas clara sin exceso de profundidad |
| **Nomenclatura** | Inconsistente (mezcla espanol/ingles) | Estandarizada en espanol | Coherencia linguistica |
| **Onboarding/recursos** | No existe | Pagina con enlaces, flags, endpoints | Autoservicio para nuevos miembros |
| **Vistas para jueces** | No existe (deben explorar toda la DB) | Vista "Resumen para Jueces" en Backlog (columnas reducidas) | Menos ruido, foco en lo esencial |
| **Vista cronologica Testing** | No existe | Vista ordenada por Fecha descendente | Historial de calidad visible de un vistazo |
| **Vista por Organismo (KB)** | No existe | Board agrupado por Seguridad Social / Ayuntamiento / Comunidad | Visualizacion por entidad gubernamental |

### Diagrama de transicion

```
ACTUAL                                  PROPUESTO
─────────                               ─────────

CivicAid OS                             CivicAid OS
  ├── Fase 0+1 (Page)                     ├── Dashboard Home [NUEVO]
  ├── Phase 2 (Page)                      ├── Para Jueces [NUEVO]
  ├── Phase 3 (Page)                      ├── Fases del Proyecto [NUEVO]
  ├── Backlog (DB, 43)                    │     ├── Fase 0+1 (reubicada)
  ├── KB Tramites (DB, 12)                │     ├── Fase 2 (reubicada)
  └── Demo & Testing (DB, 26)            │     └── Fase 3 (reubicada)
                                          ├── Backlog (DB, 43) + Relations [NUEVO]
                                          ├── KB Tramites (DB, 12) + Relations [NUEVO]
                                          ├── Demo & Testing (DB, 26) + Relations [NUEVO]
                                          └── Recursos y Referencias [NUEVO]

Paginas:     4                            Paginas:     8  (+4)
DBs:         3                            DBs:         3  (=)
Vistas:     11                            Vistas:     16  (+5)
Relations:   0                            Relations:   3  (+3)
Entradas:   81                            Entradas:   81  (=)
```

---

## 1.5 Flujos de Navegacion por Persona

### Persona 1: Juez del Hackathon

**Contexto:** Tiene 5-10 minutos para evaluar el proyecto. No conoce la arquitectura. Busca evidencia de calidad, impacto social y solidez tecnica.

```
ENTRADA: Abrir enlace compartido a CivicAid OS
│
├─ Paso 1: Llega a la pagina raiz CivicAid OS
│           Ve callout de bienvenida con indice visual de 5 secciones.
│           Identifica inmediatamente "Para Jueces".
│
├─ Paso 2: Abre "Para Jueces — Navegacion Rapida"
│           Lee en 2 minutos:
│           - Que es Clara (3 frases)
│           - Datos clave: 96 tests, 11 skills, 81 entradas Notion
│           - Progreso por fases: 4 fases COMPLETADAS (semaforo verde)
│           - Equipo: 5 miembros con roles
│
├─ Paso 3 (opcional): Quiere profundizar en calidad
│           Hace clic en enlace directo a Demo & Testing
│           Ve Board por Gate: todos los tests agrupados por G1/G2/G3
│           Confirma: 26 ejecuciones registradas, ninguna en Falla
│
├─ Paso 4 (opcional): Quiere ver progreso de tareas
│           Hace clic en enlace directo a Backlog / Issues
│           Usa vista "Resumen para Jueces" (Titulo, Estado, Gate, Owner)
│           Confirma: 42 de 43 tareas en Hecho
│
└─ Paso 5 (opcional): Quiere ver que sabe Clara
            Hace clic en enlace directo a KB Tramites
            Ve Todos los Tramites: 12 entradas, 3 tramites, todas Verificado
            Verifica fuentes oficiales en columna "Fuente URL"
```

**Tiempo estimado:** 2 minutos (flujo rapido) a 5 minutos (con profundizacion).

---

### Persona 2: Desarrollador del Equipo

**Contexto:** Miembro activo del equipo (Robert, Marcos, Lucas, Daniel o Andrea). Necesita ver sus tareas, actualizar estado y consultar la KB para verificar respuestas de Clara.

```
ENTRADA: Abrir CivicAid OS desde favoritos o sidebar de Notion
│
├─ Paso 1: Dashboard Home
│           Ve metricas actuales del proyecto de un vistazo.
│           Revisa vista linked de Backlog filtrada por Estado != Hecho
│           → Identifica si hay tareas pendientes asignadas a el/ella.
│
├─ Paso 2a: Trabajo en tareas (camino habitual)
│           Abre Backlog / Issues
│           Usa vista "Tabla por Owner" filtrando por su nombre
│           Actualiza estado de sus tareas (En progreso -> En review -> Hecho)
│           Rellena DoD y enlaza GitHub Issue
│
├─ Paso 2b: Consulta de conocimiento
│           Abre KB Tramites
│           Busca el tramite relevante (ej. IMV)
│           Verifica que los datos coinciden con la fuente oficial
│           Si detecta dato obsoleto: cambia Estado a "Desactualizado"
│
├─ Paso 3: Registro de tests
│           Abre Demo & Testing
│           Crea nueva fila con: Test ID, Tipo, Input, Output esperado/real,
│           Latencia, Resultado, Gate, Fecha
│           [CON RELACION NUEVA] Vincula a la tarea del Backlog que genero el test
│
└─ Paso 4: Contexto de fase
            Abre Fases del Proyecto -> selecciona la fase relevante
            Lee que se hizo, que se verifico y cuales fueron los entregables
```

**Tiempo estimado:** 1-2 minutos para check diario, 5-10 minutos para actualizacion completa.

---

### Persona 3: PM / Coordinadora (Andrea)

**Contexto:** Gestiona el workspace Notion, coordina al equipo, prepara presentaciones y asegura que la informacion este actualizada y completa. Necesita vision global y capacidad de drill-down.

```
ENTRADA: Abrir CivicAid OS desde sidebar
│
├─ Paso 1: Dashboard Home — Vision global
│           Revisa metricas agregadas: 81 entradas, 96 tests, estado general
│           Revisa vistas linked:
│           - Backlog: tareas pendientes (objetivo: 0 pendientes)
│           - Testing: fallos activos (objetivo: 0 fallos)
│           - KB: tramites sin verificar (objetivo: 0 pendientes)
│
├─ Paso 2: Backlog — Seguimiento de equipo
│           Abre Backlog / Issues
│           Usa vista "Kanban por Estado" para ver el flujo global
│           Usa vista "Board por Gate" para verificar progreso por gate
│           Filtra por Owner para revisar carga de cada miembro:
│           - Robert (Backend lead)
│           - Marcos (Routes/Twilio)
│           - Lucas (KB/Testing)
│           - Daniel (Web/Video)
│
├─ Paso 3: Trazabilidad tarea-test (con relaciones nuevas)
│           Desde una tarea del Backlog, hace clic en "Test vinculado"
│           → Navega directamente a la ejecucion de test en Demo & Testing
│           Verifica que el test paso y que la latencia es aceptable
│           Desde el test, hace clic en "Tarea origen"
│           → Regresa al Backlog para verificar DoD
│
├─ Paso 4: Preparacion de presentaciones
│           Abre "Para Jueces" para revisar que la informacion sea correcta
│           Verifica que los datos clave coinciden con los datos reales de las DBs
│           Actualiza si hay cambios de ultimo momento
│
├─ Paso 5: Verificacion de KB
│           Abre KB Tramites
│           Revisa "Fecha verificacion" de cada entrada
│           Si alguna tiene fecha > 30 dias, marca para re-verificacion
│           Verifica que las 12 entradas (3 tramites x 4 campos) estan completas
│
└─ Paso 6: Documentacion de fase
            Abre Fases del Proyecto -> Phase 3 — Demo Ready
            Actualiza con ultimos resultados de la demo
            Registra decisiones y observaciones finales
```

**Tiempo estimado:** 5 minutos para check rapido, 15-20 minutos para revision completa pre-demo.

---

## 1.6 Inventario Completo de Nodos — Referencia Tecnica

### Nodos Existentes (verificados)

| # | Nombre | Tipo | ID | Padre | Entradas | Estado |
|---|--------|------|----|-------|----------|--------|
| 1 | CivicAid OS | Page (raiz) | `304c5a0f-372a-801f-995f-ce24036350ad` | Workspace | — | Activa |
| 2 | Clara Resumen Fase 0 + Fase 1 | Page | `305c5a0f-372a-81c8-b609-cc5fe793bfe4` | CivicAid OS | — | Activa |
| 3 | Phase 2 — Hardening & Deploy | Page | `305c5a0f-372a-813b-8915-f7e6c21fd055` | CivicAid OS | — | Activa |
| 4 | Phase 3 — Demo Ready | Page | `305c5a0f-372a-818d-91a7-f59c22551350` | CivicAid OS | — | Activa |
| 5 | Backlog / Issues | Database | `304c5a0f-372a-81de-92a8-f54c03b391c0` | CivicAid OS | 43 | Activa |
| 6 | KB Tramites | Database | `304c5a0f-372a-81ff-9d45-c785e69f7335` | CivicAid OS | 12 | Activa |
| 7 | Demo & Testing | Database | `304c5a0f-372a-810d-8767-d77efbd46bb2` | CivicAid OS | 26 | Activa |

### Nodos Propuestos (nuevos)

| # | Nombre | Tipo | Padre propuesto | Justificacion |
|---|--------|------|-----------------|---------------|
| 8 | Dashboard Home | Page | CivicAid OS | Panel central con metricas, vistas linked y enlaces rapidos |
| 9 | Para Jueces — Navegacion Rapida | Page | CivicAid OS | Experiencia curada para evaluadores del hackathon |
| 10 | Fases del Proyecto | Page | CivicAid OS | Contenedor para agrupar las 3 paginas de fase |
| 11 | Recursos y Referencias | Page | CivicAid OS | Onboarding, enlaces externos, configuracion de referencia |

### Vistas Existentes (11 totales)

| # | Vista | Base de datos | Tipo | Filtro/Agrupacion |
|---|-------|---------------|------|-------------------|
| V1 | Kanban por Estado | Backlog | Board | Agrupado por Estado, oculta Hecho > 7 dias |
| V2 | Board por Gate | Backlog | Board | Agrupado por Gate, solo Estado != Hecho |
| V3 | Tabla por Owner | Backlog | Table | Agrupado por Owner, todas |
| V4 | Calendario por Dia | Backlog | Calendar | Propiedad Dia, solo con Dia asignado |
| V5 | Todos los Tramites | KB Tramites | Table | Sin filtro |
| V6 | Pendientes | KB Tramites | Table | Estado = Pendiente |
| V7 | Verificados | KB Tramites | Table | Estado = Verificado |
| V8 | Board por Gate | Demo & Testing | Board | Agrupado por Gate |
| V9 | Fallos | Demo & Testing | Table | Resultado = Falla |
| V10 | Demo rehearsal | Demo & Testing | Table | Tipo = Demo rehearsal |

### Vistas Propuestas (5 nuevas)

| # | Vista | Base de datos | Tipo | Filtro/Agrupacion | Justificacion |
|---|-------|---------------|------|-------------------|---------------|
| V11 | Timeline por Dia | Backlog | Timeline | Propiedad Dia | Roadmap visual del proyecto |
| V12 | Resumen para Jueces | Backlog | Table | Solo columnas: Titulo, Estado, Gate, Owner | Menos ruido para evaluadores |
| V13 | Por Organismo | KB Tramites | Board | Agrupado por Organismo | Vision por entidad gubernamental |
| V14 | Cronologia | Demo & Testing | Table | Ordenado por Fecha desc | Historial de calidad cronologico |
| V15 | Por Tipo | Demo & Testing | Board | Agrupado por Tipo | Separar golden tests, edge cases, demo rehearsals, latencia |

### Relaciones Propuestas (3 nuevas)

| # | Desde DB | Propiedad nueva | Hacia DB | Tipo | Uso |
|---|----------|----------------|----------|------|-----|
| R1 | Backlog / Issues | Test vinculado | Demo & Testing | Relation (bidireccional) | Trazar tarea -> test que la valida |
| R2 | Backlog / Issues | Tramite relacionado | KB Tramites | Relation (bidireccional) | Vincular tarea -> tramite que implementa |
| R3 | Demo & Testing | Tarea origen | Backlog / Issues | Relation (bidireccional, inversa de R1) | Desde un test, ir a la tarea que lo origino |

> **Nota sobre R2:** KB Tramites recibe automaticamente la propiedad inversa "Tareas relacionadas" al crear la relacion bidireccional R2.

---

## 1.7 Orden de Implementacion Recomendado

| Paso | Accion | Complejidad | Dependencia |
|------|--------|-------------|-------------|
| 1 | Crear pagina "Fases del Proyecto" como hija de CivicAid OS | Baja | Ninguna |
| 2 | Mover las 3 paginas de fase bajo "Fases del Proyecto" | Baja | Paso 1 |
| 3 | Crear propiedad Relation R1 (Backlog <-> Demo & Testing) | Media | Ninguna |
| 4 | Crear propiedad Relation R2 (Backlog <-> KB Tramites) | Media | Ninguna |
| 5 | Poblar relaciones R1 y R2 en las 43 entradas del Backlog | Alta | Pasos 3, 4 |
| 6 | Crear las 5 vistas nuevas (V11-V15) | Media | Ninguna |
| 7 | Crear pagina "Dashboard Home" con metricas y vistas linked | Media | Pasos 3, 4, 6 |
| 8 | Crear pagina "Para Jueces — Navegacion Rapida" | Baja | Ninguna |
| 9 | Crear pagina "Recursos y Referencias" | Baja | Ninguna |
| 10 | Actualizar pagina raiz con callout + indice visual | Baja | Pasos 1, 7, 8, 9 |

**Estimacion total:** 2-3 horas de trabajo con MCP automatizado para crear paginas y propiedades, mas trabajo manual para poblar relaciones y disenar el layout visual del Dashboard y la pagina Para Jueces.

---

## 1.8 Resumen Ejecutivo de la Seccion

| Metrica | Actual | Propuesto | Delta |
|---------|--------|-----------|-------|
| Paginas | 4 | 8 | +4 |
| Bases de datos | 3 | 3 | = |
| Entradas en DBs | 81 | 81 | = |
| Vistas | 11 | 16 | +5 |
| Relaciones entre DBs | 0 | 3 | +3 |
| Flujos de navegacion documentados | 1 (tabla basica) | 3 (Juez, Dev, PM) | +2 |
| Tiempo medio para entender el proyecto (juez) | 10+ min (sin guia) | 2-5 min (con "Para Jueces") | -50% a -80% |
| Trazabilidad tarea-test-tramite | Nula | Completa (bidireccional) | De 0 a 100% |

**Conclusion:** La reestructuracion no modifica ninguna entrada existente ni elimina contenido. Anade 4 paginas, 5 vistas y 3 relaciones que transforman un workspace plano en un sistema navegable con flujos claros por persona. El mayor impacto es la experiencia para jueces: pasar de "explorar sin guia" a "ver lo esencial en 2 minutos".

---

> **Siguiente seccion:** Seccion 2 — Schemas y Propiedades de cada DB (detalle de campos, tipos, valores y reglas de cada base de datos).
>
> **Documento de referencia:** [`docs/06-integrations/NOTION-OS.md`](./NOTION-OS.md) — Estado actual completo del workspace Notion.
