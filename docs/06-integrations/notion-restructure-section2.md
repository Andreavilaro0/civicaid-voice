# SECCION 2: SCHEMA DE BASES DE DATOS

> **Documento de reestructuracion de Notion OS — CivicAid Voice / Clara**
>
> **Autor:** Agent F — Notion Ops / DB Engineer
>
> **Fecha:** 2026-02-13
>
> **Resumen en una linea:** Definicion completa de los schemas de las 3 bases de datos existentes, propuesta de una 4a DB (Sprint Log), relaciones entre DBs, formulas Notion y ejemplos de API MCP — todo basado en datos reales del proyecto.

---

## Indice de la seccion

1. [2.1 Base de datos: Backlog / Issues](#21-base-de-datos-backlog--issues)
2. [2.2 Base de datos: KB Tramites](#22-base-de-datos-kb-tramites)
3. [2.3 Base de datos: Demo & Testing](#23-base-de-datos-demo--testing)
4. [2.4 Propuesta de 4a DB: Sprint Log / Changelog](#24-propuesta-de-4a-db-sprint-log--changelog)
5. [2.5 Relaciones entre bases de datos](#25-relaciones-entre-bases-de-datos)
6. [2.6 Formulas Notion para campos calculados](#26-formulas-notion-para-campos-calculados)
7. [2.7 Ejemplos de API MCP por base de datos](#27-ejemplos-de-api-mcp-por-base-de-datos)

---

## 2.1 Base de datos: Backlog / Issues

**Notion DB ID:** `304c5a0f-372a-81de-92a8-f54c03b391c0`

**Proposito:** Sprint board para todas las tareas, incidencias y entregables del proyecto CivicAid Voice. Cada fila representa una unidad de trabajo asignada a un miembro del equipo, vinculada a un gate de calidad y con criterios de aceptacion definidos.

### 2.1.1 Tabla completa de propiedades (schema actual)

| # | Propiedad | Tipo Notion | Opciones / Valores | Obligatorio? | Descripcion |
|---|-----------|-------------|-------------------|--------------|-------------|
| 1 | **Titulo** | Title | Texto libre | Si | Nombre descriptivo de la tarea. Convencion: verbo + objeto (ej. "Implementar cache-first con 8 entries + MP3") |
| 2 | **Estado** | Select | `Backlog`, `En progreso`, `En review`, `Hecho`, `Bloqueado` | Si | Estado actual del ciclo de vida de la tarea |
| 3 | **Gate** | Select | `G0-Tooling`, `G1-Texto`, `G2-Audio`, `G3-Demo`, `Infra` | Si | Gate de calidad al que pertenece la tarea |
| 4 | **Owner** | Select | `Robert`, `Marcos`, `Daniel`, `Andrea`, `Lucas` | No | Responsable de la tarea. Se usa Select en lugar de Person porque la API de Notion requiere IDs de usuario del workspace para el tipo Person, lo cual complica la automatizacion via MCP |
| 5 | **Prioridad** | Select | `P0-demo`, `P1`, `P2` | Si | Nivel de prioridad. P0-demo = critico para la demo del hackathon |
| 6 | **Horas est.** | Number | Rango: 0.5 a 8 | No | Estimacion de esfuerzo en horas |
| 7 | **DoD** | Rich Text | Texto libre | Si | Definition of Done — criterios de aceptacion que deben cumplirse para marcar como Hecho |
| 8 | **Depende de** | Rich Text | Referencias por nombre (ej. "D1.1, D1.3") | No | Dependencias con otras tareas. Se usa Rich Text en lugar de Relation porque las paginas de destino deben existir antes de crear la relacion |
| 9 | **GitHub Issue** | URL | URL completa a la issue de GitHub | No | Enlace a la issue correspondiente en el repositorio `civicaid-voice` |
| 10 | **Dia** | Select | `Dia 1`, `Dia 2`, `Dia 3` | No | Dia del hackathon en que se planifica ejecutar la tarea |

**Detalle de valores de Estado:**

| Estado | Significado | Color Notion | Criterio de transicion |
|--------|-------------|--------------|----------------------|
| `Backlog` | Identificado, pendiente de asignacion | Gris | Creacion inicial |
| `En progreso` | Desarrollo activo por el owner | Amarillo | Owner comienza trabajo |
| `En review` | Codigo listo, pendiente de revision | Naranja | PR abierto o DoD en verificacion |
| `Hecho` | Completado, verificado y cerrado | Verde | DoD cumplido, tests pasan |
| `Bloqueado` | No se puede avanzar por dependencia externa | Rojo | Registrar motivo en Notas o DoD |

### 2.1.2 Conteo actual de entradas (verificado 2026-02-12)

| Metrica | Valor |
|---------|-------|
| **Total de entradas** | 43 |
| **Estado Hecho** | 42 |
| **Estado Backlog** | 1 |
| **% completado** | 97.7% |

**Desglose por Gate:**

| Gate | Entradas | Estado predominante |
|------|----------|-------------------|
| G0-Tooling | ~4 | Todas Hecho |
| G1-Texto | ~8 | Todas Hecho |
| G2-Audio | ~8 | Todas Hecho |
| G3-Demo | ~5 | Todas Hecho |
| Infra | ~6 | 5 Hecho, 1 Backlog |
| P2.x (Fase 2) | ~6 | Todas Hecho |
| P3.x (Fase 3) | ~6 | Todas Hecho |

**Desglose por Owner (del 97.7% con owner asignado):**

| Owner | Responsabilidades principales |
|-------|------------------------------|
| Robert | Pipeline, skills, arquitectura |
| Marcos | Testing, integracion, QA |
| Lucas | Validacion, evals, red team |
| Daniel | Deploy, ops, infraestructura |
| Andrea | Coordinacion, Notion, documentacion |

### 2.1.3 Propiedades nuevas recomendadas

| # | Propiedad | Tipo | Opciones | Justificacion |
|---|-----------|------|----------|---------------|
| 11 | **Fase** | Select | `F0-Plan`, `F1-MVP`, `F2-Hardening`, `F3-Demo` | Permite filtrar tareas por fase sin depender solo del Gate. Una tarea de Gate G1-Texto puede pertenecer a F1 o F2. Actualmente no hay forma de distinguirlo |
| 12 | **Fecha inicio** | Date | Fecha ISO | Permite calcular duracion real de cada tarea y generar metricas de velocidad del equipo |
| 13 | **Fecha cierre** | Date | Fecha ISO | Complementa Fecha inicio para medir lead time. Actualmente solo tenemos "Dia" (Dia 1/2/3) que es impreciso |
| 14 | **Commit SHA** | Rich Text | Hash corto (7 chars) | Enlaza la tarea con el commit que la resuelve. Complementa GitHub Issue para trazabilidad directa al codigo |
| 15 | **Esfuerzo real** | Number | Horas (decimal) | Comparar con Horas est. para calibrar estimaciones futuras. Util para retrospectivas |
| 16 | **Etiquetas** | Multi-select | `bug`, `feature`, `docs`, `refactor`, `test`, `ops`, `security` | Clasificacion transversal a los gates. Permite analisis de donde se invierte el esfuerzo (ej. "cuanto tiempo dedicamos a docs vs codigo") |

### 2.1.4 Vistas recomendadas

| # | Vista | Tipo | Agrupar por | Filtro | Ordenar por | Proposito |
|---|-------|------|-------------|--------|-------------|-----------|
| 1 | **Kanban por Estado** | Board | Estado | Ocultar Hecho > 7 dias | Prioridad DESC | Vista principal de trabajo diario. Muestra el flujo de tareas |
| 2 | **Board por Gate** | Board | Gate | Estado != Hecho | Prioridad DESC | Ver progreso por gate de calidad. Util para verificar que se cumplen los gates |
| 3 | **Tabla por Owner** | Table | Owner | Todas | Estado ASC, Gate ASC | Carga de trabajo por persona. Revisar que nadie este sobrecargado |
| 4 | **Calendario por Dia** | Calendar | Dia | Solo con Dia asignado | — | Planificacion temporal del hackathon (3 dias) |
| 5 | **Tabla por Fase** | Table | Fase (nuevo) | Todas | Gate ASC, Prioridad DESC | Retrospectiva por fase. Ver que se hizo en cada iteracion |
| 6 | **Tareas bloqueadas** | Table | — | Estado = Bloqueado | Fecha cierre ASC | Vista de alertas. Identificar cuellos de botella rapidamente |
| 7 | **Burndown por Gate** | Table | Gate | Estado = Hecho | Fecha cierre ASC | Generar grafica de progreso acumulado por gate |

### 2.1.5 Ejemplo de entradas reales

**Entrada 1 — Tarea G0 completada:**

| Propiedad | Valor |
|-----------|-------|
| Titulo | Setup MCP + skills + agents |
| Estado | Hecho |
| Gate | G0-Tooling |
| Owner | Robert |
| Prioridad | P0-demo |
| Horas est. | 2 |
| DoD | 15 skills, 8 agents, MCPs instalados |
| Dia | Dia 1 |

**Entrada 2 — Tarea G1 completada:**

| Propiedad | Valor |
|-----------|-------|
| Titulo | Implementar cache-first con 8 entries + MP3 |
| Estado | Hecho |
| Gate | G1-Texto |
| Owner | Robert |
| Prioridad | P0-demo |
| Horas est. | 3 |
| DoD | Cache match funciona, 6 MP3 generados, tests T1-T3 pasan |
| Dia | Dia 1 |

**Entrada 3 — Tarea Infra en Backlog:**

| Propiedad | Valor |
|-----------|-------|
| Titulo | Deploy a Render + configurar Twilio webhook |
| Estado | Backlog |
| Gate | Infra |
| Owner | Daniel |
| Prioridad | P0-demo |
| Horas est. | 1 |
| DoD | Render deploy OK, Twilio webhook apunta a URL real, /health 200 |
| Dia | Dia 2 |

---

## 2.2 Base de datos: KB Tramites

**Notion DB ID:** `304c5a0f-372a-81ff-9d45-c785e69f7335`

**Proposito:** Base de conocimiento verificada para tramites administrativos espanoles. Es la fuente de verdad que Clara utiliza para responder a los usuarios sobre IMV, Empadronamiento y Tarjeta Sanitaria. Cada entrada cubre un campo especifico (Descripcion, Requisitos, Documentos, Pasos) de un tramite concreto.

### 2.2.1 Tabla completa de propiedades (schema actual)

| # | Propiedad | Tipo Notion | Opciones / Valores | Obligatorio? | Descripcion |
|---|-----------|-------------|-------------------|--------------|-------------|
| 1 | **Tramite** | Title | `IMV`, `Empadronamiento`, `Tarjeta Sanitaria` | Si | Nombre del tramite administrativo. Solo 3 valores posibles en la version actual |
| 2 | **Campo** | Select | `Descripcion`, `Requisitos`, `Documentos`, `Pasos` | Si | Tipo de informacion que contiene esta entrada. Cada tramite tiene exactamente 4 campos |
| 3 | **Valor** | Rich Text | Texto informativo extenso | Si | Contenido real del campo. Es la informacion que Clara devuelve al usuario |
| 4 | **Fuente URL** | URL | URL oficial gubernamental | Si | Enlace a la pagina oficial de donde se obtuvo la informacion. Garantiza trazabilidad |
| 5 | **Organismo** | Select | `Seguridad Social`, `Ayuntamiento Madrid`, `Comunidad de Madrid` | Si | Organismo publico responsable del tramite |
| 6 | **Estado** | Select | `Verificado`, `Pendiente`, `Desactualizado` | Si | Estado de verificacion del contenido. Solo se usa informacion `Verificado` en produccion |
| 7 | **Fecha verificacion** | Date | Fecha ISO | Si | Ultima fecha en que se verifico la informacion contra la fuente oficial |
| 8 | **Notas** | Rich Text | Texto libre | No | Notas internas: excepciones, casos especiales, matices no incluidos en Valor |

### 2.2.2 Conteo actual de entradas (verificado 2026-02-12)

| Metrica | Valor |
|---------|-------|
| **Total de entradas** | 12 |
| **Estado Verificado** | 12 (100%) |
| **Cobertura** | 3 tramites x 4 campos = 12 (cobertura completa) |

**Desglose por tramite:**

| Tramite | Organismo | Campos cubiertos | Estado | Fuente URL |
|---------|-----------|-----------------|--------|------------|
| IMV | Seguridad Social | Descripcion, Requisitos, Documentos, Pasos | 4/4 Verificado | `seg-social.es/wps/portal/...` |
| Empadronamiento | Ayuntamiento Madrid | Descripcion, Requisitos, Documentos, Pasos | 4/4 Verificado | `madrid.es/portales/.../Empadronamiento` |
| Tarjeta Sanitaria | Comunidad de Madrid | Descripcion, Requisitos, Documentos, Pasos | 4/4 Verificado | `comunidad.madrid/servicios/salud/tarjeta-sanitaria` |

### 2.2.3 Propiedades nuevas recomendadas

| # | Propiedad | Tipo | Opciones | Justificacion |
|---|-----------|------|----------|---------------|
| 9 | **Idioma** | Select | `es`, `fr`, `ar`, `en` | Clara soporta espanol y frances. La KB actual solo tiene contenido en espanol. Permitiria tener traducciones verificadas de cada campo para cada tramite |
| 10 | **Version** | Number | Entero autoincremental | Permite rastrear revisiones del contenido. Cuando se actualiza un Valor, se incrementa la version en lugar de perder el historico |
| 11 | **Autor verificacion** | Select | `Robert`, `Marcos`, `Daniel`, `Andrea`, `Lucas` | Saber quien verifico la informacion contra la fuente oficial. Responsabilidad y auditoria |
| 12 | **Proxima revision** | Date | Fecha ISO | Los datos gubernamentales cambian. Programar cuando revisar cada entrada (ej. cada 3 meses). Formula: `Fecha verificacion + 90 dias` |
| 13 | **Confianza** | Select | `Alta`, `Media`, `Baja` | Nivel de confianza en la precision del contenido. "Alta" = verificado directamente en la web oficial. "Media" = fuente secundaria. "Baja" = informacion parcial |
| 14 | **Palabras clave** | Rich Text | Lista de keywords separados por coma | Keywords que Clara usa para matchear consultas del usuario con este campo. Facilita depuracion del sistema de cache/KB lookup |

### 2.2.4 Vistas recomendadas

| # | Vista | Tipo | Agrupar por | Filtro | Ordenar por | Proposito |
|---|-------|------|-------------|--------|-------------|-----------|
| 1 | **Todos los Tramites** | Table | — | Ninguno | Tramite ASC, Campo ASC | Vista general para navegacion completa |
| 2 | **Por Tramite** | Board | Tramite | Ninguno | Campo ASC | Vision agrupada: ver los 4 campos de cada tramite juntos |
| 3 | **Pendientes de verificacion** | Table | — | Estado = Pendiente OR Estado = Desactualizado | Fecha verificacion ASC | Alerta de contenido que necesita atencion |
| 4 | **Verificados** | Table | — | Estado = Verificado | Fecha verificacion DESC | Vista de confianza: todo lo que esta al dia |
| 5 | **Por Organismo** | Board | Organismo | Ninguno | Tramite ASC | Vista institucional: que tenemos de cada organismo |
| 6 | **Proximos a caducar** | Table | — | Proxima revision (nuevo) < hoy + 30 dias | Proxima revision ASC | Alerta proactiva de contenido que esta por caducar |

### 2.2.5 Ejemplo de entradas reales

**Entrada 1 — IMV Descripcion:**

| Propiedad | Valor |
|-----------|-------|
| Tramite | IMV |
| Campo | Descripcion |
| Valor | Prestacion economica dirigida a prevenir el riesgo de pobreza y exclusion social. Cuantia: 604-1148 EUR/mes segun unidad familiar. |
| Fuente URL | `https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-8d06-4645-bde7-05374ee42ac7` |
| Organismo | Seguridad Social |
| Estado | Verificado |
| Fecha verificacion | 2024-12-01 |

**Entrada 2 — Empadronamiento Pasos:**

| Propiedad | Valor |
|-----------|-------|
| Tramite | Empadronamiento |
| Campo | Pasos |
| Valor | 1. Cita previa (madrid.es/padron o tel 010). 2. Acudir OAC con documentos. 3. Rellenar hoja padronal. 4. Volante en el acto. |
| Fuente URL | `https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Empadronamiento` |
| Organismo | Ayuntamiento Madrid |
| Estado | Verificado |
| Fecha verificacion | 2024-12-01 |

**Entrada 3 — Tarjeta Sanitaria Requisitos:**

| Propiedad | Valor |
|-----------|-------|
| Tramite | Tarjeta Sanitaria |
| Campo | Requisitos |
| Valor | Afiliados Seg Social. Pensionistas. Desempleados. Empadronados sin recursos. Menores. Embarazadas. Urgencias: derecho para TODOS. |
| Fuente URL | `https://www.comunidad.madrid/servicios/salud/tarjeta-sanitaria` |
| Organismo | Comunidad de Madrid |
| Estado | Verificado |
| Fecha verificacion | 2024-12-01 |

---

## 2.3 Base de datos: Demo & Testing

**Notion DB ID:** `304c5a0f-372a-810d-8767-d77efbd46bb2`

**Proposito:** Registro de ejecucion de tests y ensayos de demo. Cada fila es una ejecucion unica — nunca se sobreescriben filas anteriores, siempre se crean nuevas. Sirve como evidencia de calidad del proyecto ante jueces y revisores.

### 2.3.1 Tabla completa de propiedades (schema actual)

| # | Propiedad | Tipo Notion | Opciones / Valores | Obligatorio? | Descripcion |
|---|-----------|-------------|-------------------|--------------|-------------|
| 1 | **Test** | Title | ID del test (ej. "T1 — Cache Match Keyword Exacto") | Si | Identificador unico del test con descripcion breve |
| 2 | **Tipo** | Select | `Golden test`, `Edge case`, `Demo rehearsal`, `Latencia` | Si | Clasificacion del test segun su proposito |
| 3 | **Input** | Rich Text | Entrada exacta del test | Si | Los datos de entrada utilizados en la ejecucion |
| 4 | **Output esperado** | Rich Text | Salida esperada | Si | El resultado que se espera obtener segun la especificacion |
| 5 | **Output real** | Rich Text | Salida obtenida | Si | El resultado que realmente se obtuvo en la ejecucion |
| 6 | **Latencia (ms)** | Number | Entero positivo | No | Tiempo de respuesta en milisegundos. Critico para tests de tipo Latencia |
| 7 | **Resultado** | Select | `Pasa`, `Falla`, `Pendiente` | Si | Resultado de la ejecucion del test |
| 8 | **Gate** | Select | `G1-Texto`, `G2-Audio`, `G3-Demo` | Si | Gate de calidad que valida este test |
| 9 | **Fecha** | Date | Fecha ISO | Si | Fecha en que se ejecuto el test |
| 10 | **Notas** | Rich Text | Texto libre | No | Observaciones, logs de error, contexto adicional |

**Detalle de valores de Tipo:**

| Tipo | Proposito | Ejemplo |
|------|-----------|---------|
| `Golden test` | Tests fundamentales que deben pasar siempre. Definen el comportamiento correcto del sistema | T1 — Cache Match Keyword Exacto |
| `Edge case` | Casos limite y situaciones atipicas que prueban la robustez | Texto vacio, idioma no soportado |
| `Demo rehearsal` | Ejecuciones reales de los escenarios de demo | WOW 1 (texto IMV), WOW 2 (audio) |
| `Latencia` | Mediciones de rendimiento para verificar que se cumplen los SLAs | Respuesta cache < 100ms, LLM < 6s |

### 2.3.2 Conteo actual de entradas (verificado 2026-02-12)

| Metrica | Valor |
|---------|-------|
| **Total de entradas** | 26 |
| **Resultado Pasa** | 26 (100%) |
| **Resultado Falla** | 0 |
| **Resultado Pendiente** | 0 |

**Desglose por origen:**

| Grupo | Tests | Gate | Descripcion |
|-------|-------|------|-------------|
| Golden tests Fase 1 | T1-T10 (10 entradas) | G1-Texto, G2-Audio | Tests fundamentales del MVP: cache, KB, idioma, webhook, pipeline, E2E |
| Tests Fase 2 | T2.1-T2.6 (6 entradas) | G1-Texto, G2-Audio | Validacion firma Twilio, /health, cron, Notion, phase2_verify, secretos |
| Tests adicionales Fase 3 | 10 entradas | G3-Demo | Tests de demo rehearsal, latencia, QA deep audit |

**Desglose por Gate:**

| Gate | Entradas | Resultado |
|------|----------|-----------|
| G1-Texto | ~10 | 100% Pasa |
| G2-Audio | ~10 | 100% Pasa |
| G3-Demo | ~6 | 100% Pasa |

### 2.3.3 Propiedades nuevas recomendadas

| # | Propiedad | Tipo | Opciones | Justificacion |
|---|-----------|------|----------|---------------|
| 11 | **Fase** | Select | `F1-MVP`, `F2-Hardening`, `F3-Demo` | Permite filtrar tests por fase. Actualmente la unica forma de saber a que fase pertenece un test es por su ID (T1-T10 = F1, T2.x = F2) lo cual no es intuitivo |
| 12 | **Ejecutado por** | Select | `Robert`, `Marcos`, `Lucas`, `Daniel`, `Andrea`, `CI/CD` | Registrar quien ejecuto el test. "CI/CD" para ejecuciones automaticas. Responsabilidad y auditoria |
| 13 | **Entorno** | Select | `Local`, `Docker`, `Render`, `CI` | Saber en que entorno se ejecuto el test. Un test puede pasar en local y fallar en Docker |
| 14 | **Archivo test** | Rich Text | Ruta relativa (ej. `tests/unit/test_cache.py`) | Enlace directo al archivo de test en el repositorio. Permite a un revisor ir directamente al codigo |
| 15 | **Duracion total (ms)** | Number | Entero | Diferente de Latencia: mide el tiempo total de ejecucion del test, no solo la latencia de la respuesta |
| 16 | **Tarea relacionada** | Relation | -> Backlog / Issues | Vincular el test con la tarea del backlog que valida. Cierra el ciclo tarea -> implementacion -> test -> evidencia |

### 2.3.4 Vistas recomendadas

| # | Vista | Tipo | Agrupar por | Filtro | Ordenar por | Proposito |
|---|-------|------|-------------|--------|-------------|-----------|
| 1 | **Board por Gate** | Board | Gate | Ninguno | Test ASC | Vista principal: progreso de tests por gate de calidad |
| 2 | **Fallos** | Table | — | Resultado = Falla | Fecha DESC | Alerta de regresiones. Vista critica para el equipo |
| 3 | **Demo rehearsal** | Table | — | Tipo = Demo rehearsal | Fecha DESC | Historial de ensayos de demo para el hackathon |
| 4 | **Latencia** | Table | — | Tipo = Latencia | Latencia (ms) DESC | Identificar tests lentos. Verificar SLAs de rendimiento |
| 5 | **Por Fase** | Board | Fase (nuevo) | Ninguno | Test ASC | Vision historica: que tests se anadieron en cada fase |
| 6 | **Timeline** | Timeline | — | Ninguno | Fecha ASC | Cronologia de ejecuciones. Ver cuando se ejecutaron los tests |
| 7 | **Pendientes** | Table | — | Resultado = Pendiente | Fecha ASC | Tests definidos pero no ejecutados. Lista de trabajo pendiente |

### 2.3.5 Ejemplo de entradas reales

**Entrada 1 — Golden test G1 (Fase 1):**

| Propiedad | Valor |
|-----------|-------|
| Test | T1 — Cache Match Keyword Exacto |
| Tipo | Golden test |
| Input | message=Que es el IMV?, lang=es, TEXT |
| Output esperado | hit=True, id=imv_es |
| Output real | hit=True, id=imv_es |
| Latencia (ms) | — |
| Resultado | Pasa |
| Gate | G1-Texto |
| Fecha | 2026-02-12 |
| Notas | test_t1 PASS |

**Entrada 2 — Test Fase 2 (Twilio):**

| Propiedad | Valor |
|-----------|-------|
| Test | T2.1 — Validacion firma webhook Twilio |
| Tipo | Golden test |
| Input | POST /webhook sin firma Twilio valida |
| Output esperado | HTTP 403 Forbidden |
| Output real | HTTP 403 Forbidden |
| Latencia (ms) | — |
| Resultado | Pasa |
| Gate | G2-Audio |
| Fecha | 2026-02-12 |
| Notas | Signature validation activa en produccion |

**Entrada 3 — E2E Demo flow:**

| Propiedad | Valor |
|-----------|-------|
| Test | T9 — WA Text Demo E2E |
| Tipo | Golden test |
| Input | POST /webhook Que es el IMV? |
| Output esperado | HTTP 200, cache hit imv_es |
| Output real | HTTP 200, cache hit imv_es |
| Latencia (ms) | — |
| Resultado | Pasa |
| Gate | G2-Audio |
| Fecha | 2026-02-12 |
| Notas | test_t9 PASS |

---

## 2.4 Propuesta de 4a DB: Sprint Log / Changelog

### 2.4.1 Justificacion

Actualmente el proyecto carece de un registro cronologico de cambios. La informacion sobre que se hizo, cuando y por quien esta dispersa en:
- Commits de Git (dificiles de consumir para no-desarrolladores)
- Entradas del Backlog (describen tareas, no cambios)
- Documentos de evidencia (narrativos, no estructurados)

Una base de datos **Sprint Log / Changelog** centraliza la cronologia de cambios del proyecto con granularidad suficiente para:
1. **Jueces y revisores:** Entender la evolucion del proyecto dia a dia sin leer commits.
2. **Equipo:** Retrospectivas basadas en datos reales, no en memoria.
3. **Trazabilidad:** Vincular cada cambio con su commit, tarea y archivos afectados.
4. **Transparencia:** Demostrar que el proyecto se construyo incrementalmente (no de golpe la noche antes).

### 2.4.2 Schema propuesto

| # | Propiedad | Tipo Notion | Opciones / Valores | Obligatorio? | Descripcion |
|---|-----------|-------------|-------------------|--------------|-------------|
| 1 | **Cambio** | Title | Texto descriptivo corto | Si | Resumen del cambio en una linea (ej. "Pipeline de 11 skills funcional con tests T1-T10") |
| 2 | **Fecha** | Date | Fecha + hora ISO | Si | Momento exacto del cambio |
| 3 | **Fase** | Select | `F0-Plan`, `F1-MVP`, `F2-Hardening`, `F3-Demo` | Si | Fase del proyecto en la que ocurrio el cambio |
| 4 | **Autor** | Select | `Robert`, `Marcos`, `Daniel`, `Andrea`, `Lucas` | Si | Persona que realizo el cambio |
| 5 | **Tipo de cambio** | Multi-select | `feature`, `bugfix`, `refactor`, `docs`, `test`, `ops`, `security`, `config` | Si | Clasificacion del tipo de cambio. Multi-select porque un cambio puede ser "feature + test" |
| 6 | **Detalle** | Rich Text | Texto libre | No | Descripcion detallada del cambio con contexto |
| 7 | **Commit SHA** | Rich Text | Hash corto (7 chars, ej. "c6a896e") | No | Hash del commit de Git asociado al cambio |
| 8 | **Archivos afectados** | Rich Text | Lista de rutas relativas | No | Archivos principales creados o modificados (ej. "src/core/pipeline.py, tests/unit/test_cache.py") |
| 9 | **Tarea relacionada** | Relation | -> Backlog / Issues | No | Vinculo con la tarea del backlog que origino este cambio |
| 10 | **Impacto** | Select | `Alto`, `Medio`, `Bajo` | No | Nivel de impacto del cambio en el sistema. "Alto" = cambio en arquitectura, "Medio" = nueva funcionalidad, "Bajo" = ajuste menor |

### 2.4.3 Vistas recomendadas

| # | Vista | Tipo | Agrupar por | Filtro | Ordenar por | Proposito |
|---|-------|------|-------------|--------|-------------|-----------|
| 1 | **Timeline cronologico** | Timeline | — | Ninguno | Fecha ASC | Vista principal: evolucion temporal del proyecto |
| 2 | **Por Fase** | Board | Fase | Ninguno | Fecha ASC | Ver que cambios se hicieron en cada fase |
| 3 | **Por Autor** | Table | Autor | Ninguno | Fecha DESC | Contribuciones de cada miembro del equipo |
| 4 | **Por Tipo** | Board | Tipo de cambio | Ninguno | Fecha DESC | Analisis de distribucion de esfuerzo |
| 5 | **Solo Alto Impacto** | Table | — | Impacto = Alto | Fecha ASC | Decisiones arquitectonicas y cambios criticos |

### 2.4.4 Ejemplo de entradas propuestas (basadas en datos reales del proyecto)

**Entrada 1 — Cierre Fase 1:**

| Propiedad | Valor |
|-----------|-------|
| Cambio | Pipeline de 11 skills funcional — MVP completado |
| Fecha | 2026-02-12 |
| Fase | F1-MVP |
| Autor | Robert |
| Tipo de cambio | feature |
| Detalle | Pipeline orquestador con 11 skills: detect_input, fetch_media, convert_audio, transcribe, detect_lang, cache_match, kb_lookup, llm_generate, verify_response, tts, send_response. Patron TwiML ACK implementado. 32 tests pasan. |
| Commit SHA | c6a896e |
| Archivos afectados | src/core/pipeline.py, src/core/skills/*.py, src/core/models.py |
| Impacto | Alto |

**Entrada 2 — Cierre Fase 2:**

| Propiedad | Valor |
|-----------|-------|
| Cambio | Hardening completo — 93 tests, guardrails, observability, deploy Render |
| Fecha | 2026-02-12 |
| Fase | F2-Hardening |
| Autor | Marcos |
| Tipo de cambio | test, security, ops |
| Detalle | +61 tests nuevos (93 total). Guardrails pre/post con PII redaction. Observabilidad con RequestContext y JSON logs. Deploy Render con Docker verificado. Secretos escaneados. |
| Commit SHA | ec05382 |
| Archivos afectados | src/core/guardrails.py, src/utils/observability.py, tests/unit/test_guardrails.py, tests/unit/test_redteam.py |
| Impacto | Alto |

**Entrada 3 — Cierre Fase 3:**

| Propiedad | Valor |
|-----------|-------|
| Cambio | Demo Ready — Twilio real, QA deep audit, 96 tests, Notion 81 entradas |
| Fecha | 2026-02-13 |
| Fase | F3-Demo |
| Autor | Andrea |
| Tipo de cambio | ops, docs, test |
| Detalle | Twilio sandbox real configurado. phase3_verify.sh con 7 pasos. 96 tests (91 passed + 5 xpassed). 81 entradas Notion verificadas por API. Guion demo 6-8 min con WOW 1 + WOW 2. +3 tests transcribe. |
| Commit SHA | 77d5f88 |
| Archivos afectados | scripts/phase3_verify.sh, tests/unit/test_transcribe.py, docs/06-integrations/NOTION-OS.md |
| Impacto | Alto |

---

## 2.5 Relaciones entre bases de datos

### 2.5.1 Diagrama de relaciones

```
+-------------------+       Relation        +--------------------+
|                   |  "Tarea relacionada"   |                    |
|  Backlog / Issues |<-----------------------|  Demo & Testing    |
|  (43 entradas)    |                        |  (26 entradas)     |
|                   |<-----------------------|                    |
+-------------------+       Relation         +--------------------+
        ^               "Tarea relacionada"
        |
        | Relation "Tarea relacionada"
        |
+-------------------+
|                   |
|  Sprint Log       |
|  (propuesta)      |
|                   |
+-------------------+

+-------------------+
|                   |
|  KB Tramites      |--- (independiente, referenciada por texto)
|  (12 entradas)    |
|                   |
+-------------------+
```

### 2.5.2 Relaciones propuestas (sustituyen Rich Text por Relations)

| # | Desde DB | Propiedad origen | Hacia DB | Tipo actual | Tipo propuesto | Justificacion |
|---|----------|-----------------|----------|-------------|---------------|---------------|
| 1 | **Backlog** | Depende de | **Backlog** (auto-relacion) | Rich Text | Relation (self) | Actualmente se escriben referencias como "D1.1, D1.3" en texto plano. Con una Relation self, Notion muestra las dependencias como enlaces clicables y permite navegacion bidireccional |
| 2 | **Demo & Testing** | (nueva) Tarea relacionada | **Backlog** | No existe | Relation | Vincular cada test con la tarea del backlog que valida. Permite ver desde una tarea todos sus tests asociados (bidireccional) |
| 3 | **Sprint Log** | Tarea relacionada | **Backlog** | N/A (DB nueva) | Relation | Vincular cada cambio del changelog con su tarea de origen. Cierra el ciclo planificacion -> ejecucion -> registro |
| 4 | **Demo & Testing** | (nueva) KB referenciada | **KB Tramites** | No existe | Relation | Tests como T4 (KB Lookup Empadronamiento) validan contenido especifico de la KB. La relacion permite ver que tests cubren cada entrada de KB |

### 2.5.3 Consideraciones tecnicas para implementar relaciones

**Limitacion actual:** Las relaciones en la API de Notion requieren que las paginas de destino ya existan con sus IDs. Esto significa que:

1. **No se puede crear una relacion al crear la pagina de origen** si la pagina de destino no existe todavia.
2. **Solucion recomendada:** Crear todas las paginas primero, luego ejecutar un segundo paso que establece las relaciones usando `mcp__notionApi__API-patch-page` con los IDs obtenidos en la creacion.
3. **Script de poblacion:** Modificar `scripts/populate_notion.sh` para ejecutarse en 2 pasadas: (1) crear paginas y guardar IDs, (2) establecer relaciones.

**Nota sobre la relacion Backlog -> Backlog (self):** Las self-relations en Notion crean dos propiedades en la misma DB (ej. "Depende de" y "Dependencia de"). Esto es correcto y deseable: permite ver tanto "de que dependo" como "quien depende de mi".

---

## 2.6 Formulas Notion para campos calculados

### 2.6.1 Formulas para Backlog / Issues

**Formula 1: % Completado por Gate**

Nota: Esta formula se aplica como filtro/agrupacion, no como propiedad de la pagina individual. La forma de implementarla en Notion es creando una vista agrupada por Gate y usando la funcion de agregacion "Percent where Estado = Hecho". Alternativamente, se puede crear una pagina resumen con formulas de linked databases.

Para una propiedad individual que indique si la tarea esta completada (util para porcentajes):

```
Nombre: Completada
Formula: if(prop("Estado") == "Hecho", true, false)
Tipo resultado: Checkbox
```

**Formula 2: Dias desde creacion**

```
Nombre: Dias activa
Formula: if(prop("Estado") != "Hecho", dateBetween(now(), prop("Fecha inicio"), "days"), 0)
Tipo resultado: Number
Uso: Identificar tareas estancadas (> 2 dias activas en un hackathon = alerta)
```

**Formula 3: Desviacion de estimacion**

Requiere la propiedad nueva "Esfuerzo real":

```
Nombre: Desviacion (h)
Formula: if(prop("Esfuerzo real") > 0, prop("Esfuerzo real") - prop("Horas est."), 0)
Tipo resultado: Number
Uso: Positivo = tardo mas de lo estimado. Negativo = tardo menos. Calibracion de estimaciones
```

**Formula 4: Etiqueta de urgencia**

```
Nombre: Urgencia
Formula: if(prop("Estado") == "Bloqueado", "BLOQUEADO", if(prop("Prioridad") == "P0-demo" and prop("Estado") != "Hecho", "URGENTE", if(prop("Prioridad") == "P1" and prop("Estado") != "Hecho", "Normal", "OK")))
Tipo resultado: Text
Uso: Identificacion visual rapida de tareas que requieren atencion inmediata
```

### 2.6.2 Formulas para KB Tramites

**Formula 5: Dias desde verificacion**

```
Nombre: Dias sin verificar
Formula: dateBetween(now(), prop("Fecha verificacion"), "days")
Tipo resultado: Number
Uso: Alerta de contenido obsoleto. Si > 90 dias, revisar contra fuente oficial
```

**Formula 6: Estado de frescura**

```
Nombre: Frescura
Formula: if(dateBetween(now(), prop("Fecha verificacion"), "days") < 30, "Fresco", if(dateBetween(now(), prop("Fecha verificacion"), "days") < 90, "Aceptable", "Revisar"))
Tipo resultado: Text
Uso: Semaforo visual de la vigencia del contenido. "Fresco" = verde, "Aceptable" = amarillo, "Revisar" = rojo
```

**Formula 7: Proxima revision automatica**

```
Nombre: Proxima revision (calculada)
Formula: dateAdd(prop("Fecha verificacion"), 90, "days")
Tipo resultado: Date
Uso: Calcula automaticamente cuando deberia revisarse cada entrada (90 dias tras ultima verificacion)
```

### 2.6.3 Formulas para Demo & Testing

**Formula 8: Dias desde ultima ejecucion**

```
Nombre: Dias sin ejecutar
Formula: dateBetween(now(), prop("Fecha"), "days")
Tipo resultado: Number
Uso: Identificar tests que llevan mucho sin ejecutarse. En un hackathon, > 1 dia sin ejecutar es significativo
```

**Formula 9: Coincidencia output**

```
Nombre: Output coincide
Formula: if(prop("Output esperado") == prop("Output real"), true, false)
Tipo resultado: Checkbox
Uso: Verificacion rapida de que el output real matchea el esperado. Complementa Resultado (que puede ser manual)
```

**Formula 10: Indicador de latencia**

```
Nombre: Latencia OK
Formula: if(empty(prop("Latencia (ms)")), "N/A", if(prop("Latencia (ms)") < 1000, "Rapido", if(prop("Latencia (ms)") < 6000, "Aceptable", "Lento")))
Tipo resultado: Text
Uso: Semaforo de rendimiento. "Rapido" < 1s (cache). "Aceptable" < 6s (LLM). "Lento" > 6s (problema)
```

### 2.6.4 Formulas para Sprint Log (propuesta)

**Formula 11: Dias desde el cambio**

```
Nombre: Antiguedad
Formula: dateBetween(now(), prop("Fecha"), "days")
Tipo resultado: Number
Uso: Perspectiva temporal de los cambios
```

---

## 2.7 Ejemplos de API MCP por base de datos

Todos los ejemplos usan las herramientas MCP de `@notionhq/notion-mcp-server` disponibles en Claude Code. Los IDs de las bases de datos son los reales del proyecto.

### 2.7.1 Backlog / Issues

**Crear una nueva tarea:**

```json
// Herramienta: mcp__notionApi__API-post-page
{
  "body": {
    "parent": {
      "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0"
    },
    "properties": {
      "Titulo": {
        "title": [{"text": {"content": "Implementar relaciones entre DBs de Notion"}}]
      },
      "Estado": {
        "select": {"name": "Backlog"}
      },
      "Gate": {
        "select": {"name": "Infra"}
      },
      "Owner": {
        "select": {"name": "Andrea"}
      },
      "Prioridad": {
        "select": {"name": "P2"}
      },
      "Horas est.": {
        "number": 1.5
      },
      "DoD": {
        "rich_text": [{"text": {"content": "3 relaciones establecidas entre Backlog, Testing y Sprint Log"}}]
      },
      "Dia": {
        "select": {"name": "Dia 3"}
      }
    }
  }
}
```

**Consultar tareas bloqueadas:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {
    "filter": {
      "property": "Estado",
      "select": {
        "equals": "Bloqueado"
      }
    },
    "sorts": [
      {
        "property": "Prioridad",
        "direction": "ascending"
      }
    ]
  }
}
```

**Consultar tareas por Gate con estado pendiente:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {
    "filter": {
      "and": [
        {
          "property": "Gate",
          "select": {
            "equals": "G1-Texto"
          }
        },
        {
          "property": "Estado",
          "select": {
            "does_not_equal": "Hecho"
          }
        }
      ]
    }
  }
}
```

**Actualizar una tarea a Hecho:**

```json
// Herramienta: mcp__notionApi__API-patch-page
{
  "page_id": "<PAGE_ID>",
  "body": {
    "properties": {
      "Estado": {
        "select": {"name": "Hecho"}
      }
    }
  }
}
```

**Consultar tareas por Owner:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {
    "filter": {
      "property": "Owner",
      "select": {
        "equals": "Robert"
      }
    },
    "sorts": [
      {
        "property": "Gate",
        "direction": "ascending"
      }
    ]
  }
}
```

### 2.7.2 KB Tramites

**Crear una nueva entrada de KB:**

```json
// Herramienta: mcp__notionApi__API-post-page
{
  "body": {
    "parent": {
      "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335"
    },
    "properties": {
      "Tramite": {
        "title": [{"text": {"content": "IMV"}}]
      },
      "Campo": {
        "select": {"name": "Descripcion"}
      },
      "Valor": {
        "rich_text": [{"text": {"content": "Prestacion economica dirigida a prevenir el riesgo de pobreza y exclusion social. Cuantia: 604-1148 EUR/mes segun unidad familiar."}}]
      },
      "Fuente URL": {
        "url": "https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-8d06-4645-bde7-05374ee42ac7"
      },
      "Organismo": {
        "select": {"name": "Seguridad Social"}
      },
      "Estado": {
        "select": {"name": "Verificado"}
      },
      "Fecha verificacion": {
        "date": {"start": "2024-12-01"}
      }
    }
  }
}
```

**Consultar todos los campos de un tramite:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335",
  "body": {
    "filter": {
      "property": "Tramite",
      "title": {
        "equals": "IMV"
      }
    },
    "sorts": [
      {
        "property": "Campo",
        "direction": "ascending"
      }
    ]
  }
}
```

**Consultar entradas pendientes de verificacion:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335",
  "body": {
    "filter": {
      "or": [
        {
          "property": "Estado",
          "select": {
            "equals": "Pendiente"
          }
        },
        {
          "property": "Estado",
          "select": {
            "equals": "Desactualizado"
          }
        }
      ]
    }
  }
}
```

**Actualizar fecha de verificacion:**

```json
// Herramienta: mcp__notionApi__API-patch-page
{
  "page_id": "<PAGE_ID>",
  "body": {
    "properties": {
      "Fecha verificacion": {
        "date": {"start": "2026-02-13"}
      },
      "Estado": {
        "select": {"name": "Verificado"}
      }
    }
  }
}
```

**Consultar por organismo:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335",
  "body": {
    "filter": {
      "property": "Organismo",
      "select": {
        "equals": "Seguridad Social"
      }
    }
  }
}
```

### 2.7.3 Demo & Testing

**Crear un nuevo registro de test:**

```json
// Herramienta: mcp__notionApi__API-post-page
{
  "body": {
    "parent": {
      "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2"
    },
    "properties": {
      "Test": {
        "title": [{"text": {"content": "T3.1 — Whisper flag consistency"}}]
      },
      "Tipo": {
        "select": {"name": "Golden test"}
      },
      "Input": {
        "rich_text": [{"text": {"content": "WHISPER_ON=false, GEMINI_API_KEY presente"}}]
      },
      "Output esperado": {
        "rich_text": [{"text": {"content": "get_whisper_model() devuelve None"}}]
      },
      "Output real": {
        "rich_text": [{"text": {"content": "get_whisper_model() devuelve None"}}]
      },
      "Resultado": {
        "select": {"name": "Pasa"}
      },
      "Gate": {
        "select": {"name": "G3-Demo"}
      },
      "Fecha": {
        "date": {"start": "2026-02-13"}
      },
      "Notas": {
        "rich_text": [{"text": {"content": "test_whisper_model_none_when_disabled PASS"}}]
      }
    }
  }
}
```

**Consultar tests que fallan:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2",
  "body": {
    "filter": {
      "property": "Resultado",
      "select": {
        "equals": "Falla"
      }
    },
    "sorts": [
      {
        "property": "Fecha",
        "direction": "descending"
      }
    ]
  }
}
```

**Consultar tests por Gate y tipo:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2",
  "body": {
    "filter": {
      "and": [
        {
          "property": "Gate",
          "select": {
            "equals": "G2-Audio"
          }
        },
        {
          "property": "Tipo",
          "select": {
            "equals": "Golden test"
          }
        }
      ]
    }
  }
}
```

**Actualizar resultado de un test:**

```json
// Herramienta: mcp__notionApi__API-patch-page
{
  "page_id": "<PAGE_ID>",
  "body": {
    "properties": {
      "Resultado": {
        "select": {"name": "Pasa"}
      },
      "Output real": {
        "rich_text": [{"text": {"content": "hit=True, id=imv_es"}}]
      },
      "Latencia (ms)": {
        "number": 45
      }
    }
  }
}
```

**Consultar tests de demo rehearsal ordenados por fecha:**

```json
// Herramienta: mcp__notionApi__API-query-data-source
{
  "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2",
  "body": {
    "filter": {
      "property": "Tipo",
      "select": {
        "equals": "Demo rehearsal"
      }
    },
    "sorts": [
      {
        "property": "Fecha",
        "direction": "descending"
      }
    ]
  }
}
```

### 2.7.4 Sprint Log (propuesta — crear la DB primero)

**Crear la base de datos Sprint Log:**

Para crear una nueva base de datos en Notion via MCP, se usa `mcp__notionApi__API-post-page` con un parent de tipo page (la pagina raiz CivicAid OS). Sin embargo, la API de Notion MCP no expone directamente `POST /v1/databases`. La alternativa es:

1. Crear la DB manualmente en Notion bajo la pagina CivicAid OS (`304c5a0f-372a-801f-995f-ce24036350ad`).
2. Configurar el schema con las 10 propiedades definidas en la seccion 2.4.2.
3. Anotar el DB ID generado.
4. Usar la API MCP para poblar entradas.

**Crear una entrada en Sprint Log (una vez creada la DB):**

```json
// Herramienta: mcp__notionApi__API-post-page
{
  "body": {
    "parent": {
      "database_id": "<SPRINT_LOG_DB_ID>"
    },
    "properties": {
      "Cambio": {
        "title": [{"text": {"content": "Pipeline de 11 skills funcional — MVP completado"}}]
      },
      "Fecha": {
        "date": {"start": "2026-02-12"}
      },
      "Fase": {
        "select": {"name": "F1-MVP"}
      },
      "Autor": {
        "select": {"name": "Robert"}
      },
      "Tipo de cambio": {
        "multi_select": [{"name": "feature"}]
      },
      "Detalle": {
        "rich_text": [{"text": {"content": "Pipeline orquestador con 11 skills implementado. Patron TwiML ACK. 32 tests pasan. Cache-first con 8 entradas + 6 MP3."}}]
      },
      "Commit SHA": {
        "rich_text": [{"text": {"content": "c6a896e"}}]
      },
      "Archivos afectados": {
        "rich_text": [{"text": {"content": "src/core/pipeline.py, src/core/skills/*.py, src/core/models.py, data/cache/demo_cache.json"}}]
      },
      "Impacto": {
        "select": {"name": "Alto"}
      }
    }
  }
}
```

### 2.7.5 Operaciones MCP de consulta transversal

**Buscar en todo el workspace:**

```json
// Herramienta: mcp__notionApi__API-post-search
{
  "body": {
    "query": "IMV",
    "filter": {
      "value": "page",
      "property": "object"
    },
    "sort": {
      "direction": "descending",
      "timestamp": "last_edited_time"
    }
  }
}
```

**Obtener el schema de una base de datos:**

```json
// Herramienta: mcp__notionApi__API-retrieve-a-database
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0"
}
```

**Verificar el total de entradas de una DB (paginacion):**

```json
// Herramienta: mcp__notionApi__API-query-data-source
// Nota: La API devuelve maximo 100 resultados por pagina.
// Para DBs con < 100 entradas (nuestro caso: 43, 12, 26), una sola llamada es suficiente.
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {}
}
// El campo "results" del response contiene un array. Su longitud es el total de entradas.
```

---

## Resumen de la seccion

| Aspecto | Estado actual | Mejora propuesta |
|---------|--------------|-----------------|
| **Bases de datos** | 3 DBs, 81 entradas totales | +1 DB (Sprint Log), ~85+ entradas |
| **Propiedades Backlog** | 10 propiedades | +6 nuevas (Fase, Fecha inicio, Fecha cierre, Commit SHA, Esfuerzo real, Etiquetas) |
| **Propiedades KB** | 8 propiedades | +6 nuevas (Idioma, Version, Autor verificacion, Proxima revision, Confianza, Palabras clave) |
| **Propiedades Testing** | 10 propiedades | +6 nuevas (Fase, Ejecutado por, Entorno, Archivo test, Duracion total, Tarea relacionada) |
| **Relaciones** | 0 (todo Rich Text) | 4 relaciones (Backlog self, Testing->Backlog, Sprint Log->Backlog, Testing->KB) |
| **Formulas** | 0 | 11 formulas calculadas |
| **Vistas** | 10 vistas basicas | 26 vistas especializadas |
| **Ejemplos MCP** | 5 operaciones genericas | 20+ ejemplos especificos con filtros y payloads reales |

---

## Referencias

- Schema actual: [`docs/06-integrations/NOTION-OS.md`](./NOTION-OS.md)
- Script de poblacion: [`scripts/populate_notion.sh`](../../scripts/populate_notion.sh)
- Arquitectura: [`docs/02-architecture/ARCHITECTURE.md`](../02-architecture/ARCHITECTURE.md)
- Plan de testing: [`docs/04-testing/TEST-PLAN.md`](../04-testing/TEST-PLAN.md)
- Estado de fases: [`docs/07-evidence/PHASE-STATUS.md`](../07-evidence/PHASE-STATUS.md)
- API de Notion: [https://developers.notion.com](https://developers.notion.com)
- Referencia MCP: [`docs/06-integrations/MCP-TOOLS-REFERENCE.md`](./MCP-TOOLS-REFERENCE.md)
