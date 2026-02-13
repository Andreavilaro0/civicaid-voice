# SECCION 7: PLAN DE IMPLEMENTACION EN NOTION

> **Proyecto:** CivicAid Voice / Clara
> **Documento padre:** Plan de Reestructuracion del Workspace Notion
> **Autor:** Agent F (Notion Ops / Implementation Planner)
> **Fecha:** 2026-02-13
> **Tiempo estimado total:** 45 minutos
> **Prerequisitos:** Token Notion configurado en `~/.mcp.json`, servidor MCP `notionApi` activo, Claude Code reiniciado tras configuracion

---

## Indice

1. [Fase 0: Auditoria](#fase-0-auditoria-5-min) (5 min)
2. [Fase 1: Crear estructura nueva](#fase-1-crear-estructura-nueva-15-min) (15 min)
3. [Fase 2: Enriquecer DBs](#fase-2-enriquecer-dbs-10-min) (10 min)
4. [Fase 3: Poblar contenido](#fase-3-poblar-contenido-10-min) (10 min)
5. [Fase 4: Verificacion](#fase-4-verificacion-5-min) (5 min)
6. [Matriz de Riesgos](#matriz-de-riesgos)
7. [Script de Automatizacion (backup curl)](#script-de-automatizacion-backup-curl)

---

## IDs de Referencia (datos reales)

| Recurso | ID de Notion |
|---|---|
| **CivicAid OS (raiz)** | `304c5a0f-372a-801f-995f-ce24036350ad` |
| **Backlog / Issues DB** | `304c5a0f-372a-81de-92a8-f54c03b391c0` |
| **KB Tramites DB** | `304c5a0f-372a-81ff-9d45-c785e69f7335` |
| **Demo & Testing DB** | `304c5a0f-372a-810d-8767-d77efbd46bb2` |
| **Pagina Fase 0+1** | `305c5a0f-372a-81c8-b609-cc5fe793bfe4` |
| **Pagina Fase 2** | `305c5a0f-372a-813b-8915-f7e6c21fd055` |
| **Pagina Fase 3** | `305c5a0f-372a-818d-91a7-f59c22551350` |

---

## Fase 0: Auditoria (5 min)

**Objetivo:** Verificar el estado actual del workspace antes de cualquier modificacion. Confirmar que todas las bases de datos, paginas y entradas existen y son accesibles. Establecer un punto de referencia para rollback.

---

### Paso 0.1 — Verificar conectividad del token

**Descripcion:** Confirmar que el token de Notion esta activo y tiene permisos de lectura/escritura.

**Herramienta MCP:** `mcp__notionApi__API-get-self`

**Payload:**
```json
{}
```

**Respuesta esperada:**
```json
{
  "object": "user",
  "id": "<bot_id>",
  "type": "bot",
  "name": "CivicAid Integration",
  "bot": {
    "owner": { "type": "workspace", "workspace": true }
  }
}
```

**Criterio Go/No-go:** Si `object` != `"user"` o HTTP != 200, PARAR. Regenerar token en https://www.notion.so/my-integrations y actualizar `~/.mcp.json`.

**Rollback:** No aplica (operacion de solo lectura).

---

### Paso 0.2 — Verificar pagina raiz CivicAid OS

**Descripcion:** Confirmar que la pagina raiz existe y es accesible.

**Herramienta MCP:** `mcp__notionApi__API-retrieve-a-page`

**Payload:**
```json
{
  "page_id": "304c5a0f-372a-801f-995f-ce24036350ad"
}
```

**Respuesta esperada:**
```json
{
  "object": "page",
  "id": "304c5a0f-372a-801f-995f-ce24036350ad",
  "parent": { "type": "workspace", "workspace": true },
  "properties": {
    "title": {
      "title": [{ "text": { "content": "CivicAid OS" } }]
    }
  }
}
```

**Criterio Go/No-go:** Si `object` != `"page"`, la pagina raiz no existe o no esta compartida con la integracion. PARAR y compartir manualmente desde Notion web.

**Rollback:** No aplica (operacion de solo lectura).

---

### Paso 0.3 — Verificar las 3 bases de datos existentes

**Descripcion:** Confirmar que las 3 DBs existen, son accesibles y tienen los schemas esperados.

**Herramienta MCP:** `mcp__notionApi__API-retrieve-a-database` (ejecutar 3 veces)

**Payload 0.3a — Backlog:**
```json
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0"
}
```

**Payload 0.3b — KB Tramites:**
```json
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335"
}
```

**Payload 0.3c — Demo & Testing:**
```json
{
  "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2"
}
```

**Respuesta esperada (para cada una):**
```json
{
  "object": "database",
  "id": "<db_id>",
  "title": [{ "text": { "content": "<nombre_db>" } }],
  "properties": { "...schemas completos..." }
}
```

**Criterio Go/No-go:** Las 3 DBs deben responder con `object: "database"`. Si alguna falla, verificar que la integracion tiene acceso.

**Rollback:** No aplica (operacion de solo lectura).

---

### Paso 0.4 — Contar entradas en cada DB

**Descripcion:** Consultar cada DB sin filtros para contar el total de entradas y confirmar los numeros esperados (43 + 12 + 26 = 81).

**Herramienta MCP:** `mcp__notionApi__API-query-data-source` (ejecutar 3 veces)

**Payload 0.4a — Backlog:**
```json
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {}
}
```

**Payload 0.4b — KB Tramites:**
```json
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335",
  "body": {}
}
```

**Payload 0.4c — Demo & Testing:**
```json
{
  "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2",
  "body": {}
}
```

**Respuesta esperada:** Cada respuesta tiene un campo `results` (array). Contar `results.length`:

| DB | Entradas esperadas |
|---|---|
| Backlog | 43 |
| KB Tramites | 12 |
| Demo & Testing | 26 |
| **Total** | **81** |

**Nota:** Si la DB tiene mas de 100 entradas, la API pagina. Usar `has_more` y `next_cursor` para obtener todas. Con 81 entradas totales no deberia ser necesario paginar.

**Criterio Go/No-go:** Si los totales difieren significativamente de lo esperado, investigar antes de continuar. Diferencias menores (+-2) pueden ser entradas de prueba y son aceptables.

**Rollback:** No aplica (operacion de solo lectura).

---

### Paso 0.5 — Verificar paginas de fase existentes

**Descripcion:** Confirmar que las 3 paginas de fase existen.

**Herramienta MCP:** `mcp__notionApi__API-retrieve-a-page` (ejecutar 3 veces)

**Payload 0.5a — Fase 0+1:**
```json
{
  "page_id": "305c5a0f-372a-81c8-b609-cc5fe793bfe4"
}
```

**Payload 0.5b — Fase 2:**
```json
{
  "page_id": "305c5a0f-372a-813b-8915-f7e6c21fd055"
}
```

**Payload 0.5c — Fase 3:**
```json
{
  "page_id": "305c5a0f-372a-818d-91a7-f59c22551350"
}
```

**Respuesta esperada:** Cada una devuelve `"object": "page"` con el titulo correcto.

**Criterio Go/No-go:** Si alguna pagina no existe, anotar y ajustar el plan (no bloquea la reestructuracion).

**Rollback:** No aplica (operacion de solo lectura).

---

### Paso 0.6 — Obtener bloques hijos de la pagina raiz

**Descripcion:** Obtener la lista de bloques y sub-paginas actuales de CivicAid OS para entender la estructura actual y planificar donde insertar los nuevos elementos.

**Herramienta MCP:** `mcp__notionApi__API-get-block-children`

**Payload:**
```json
{
  "block_id": "304c5a0f-372a-801f-995f-ce24036350ad"
}
```

**Respuesta esperada:** Lista de bloques hijos incluyendo las 3 DBs inline y las 3 paginas de fase.

**Criterio Go/No-go:** La respuesta confirma el layout actual. Proceder si se obtiene un resultado valido.

**Rollback:** No aplica (operacion de solo lectura).

---

### Resumen Fase 0 — Tabla de verificacion

| # | Check | Herramienta | Resultado esperado | Go/No-go |
|---|---|---|---|---|
| 0.1 | Token activo | `API-get-self` | `object: "user"` | Bloquea si falla |
| 0.2 | Pagina raiz | `API-retrieve-a-page` | `object: "page"` | Bloquea si falla |
| 0.3 | 3 DBs accesibles | `API-retrieve-a-database` x3 | `object: "database"` x3 | Bloquea si alguna falla |
| 0.4 | 81 entradas | `API-query-data-source` x3 | 43 + 12 + 26 | Advierte si difiere |
| 0.5 | 3 paginas de fase | `API-retrieve-a-page` x3 | `object: "page"` x3 | No bloquea |
| 0.6 | Estructura actual | `API-get-block-children` | Lista de hijos | No bloquea |

**Decision:** Si los checks 0.1, 0.2 y 0.3 pasan: **GO**. Si alguno falla: **NO-GO** hasta resolverlo.

---

## Fase 1: Crear estructura nueva (15 min)

**Objetivo:** Crear las nuevas paginas que enriquecen el workspace: Dashboard Home, "Para Jueces" (guia de navegacion), y un contenedor padre para agrupar las paginas de fases.

---

### Paso 1.1 — Crear pagina "Dashboard Home"

**Descripcion:** Pagina principal que sirve como punto de entrada al workspace. Contendra callouts con metricas clave, enlaces a las 3 DBs, estado del proyecto y enlaces rapidos.

**Herramienta MCP:** `mcp__notionApi__API-post-page`

**Payload:**
```json
{
  "body": {
    "parent": {
      "page_id": "304c5a0f-372a-801f-995f-ce24036350ad"
    },
    "icon": {
      "type": "emoji",
      "emoji": "🏠"
    },
    "properties": {
      "title": {
        "title": [
          {
            "text": {
              "content": "Dashboard Home"
            }
          }
        ]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "🎯" },
          "color": "blue_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "CivicAid Voice / Clara — Asistente conversacional de WhatsApp para tramites de servicios sociales en Espana. 3 tramites, 2 idiomas, 96 tests, 11 skills."
              }
            }
          ]
        }
      },
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
              "text": { "content": "Estado del Proyecto" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "✅" },
          "color": "green_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "TODAS LAS FASES COMPLETADAS — Fase 0 (Plan), Fase 1 (MVP), Fase 2 (Hardening), Fase 3 (Demo Ready). 22 gates PASS. 81 entradas en Notion. 96 tests automatizados."
              }
            }
          ]
        }
      },
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
              "text": { "content": "Metricas Clave" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "table",
        "table": {
          "table_width": 2,
          "has_column_header": true,
          "has_row_header": false,
          "children": [
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Metrica" } }],
                  [{ "type": "text", "text": { "content": "Valor" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Tests automatizados" } }],
                  [{ "type": "text", "text": { "content": "96 (91 passed + 5 xpassed)" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Skills en pipeline" } }],
                  [{ "type": "text", "text": { "content": "11" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Feature flags" } }],
                  [{ "type": "text", "text": { "content": "9" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Entradas cache" } }],
                  [{ "type": "text", "text": { "content": "8 (6 con audio MP3)" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Tramites cubiertos" } }],
                  [{ "type": "text", "text": { "content": "3 (IMV, Empadronamiento, Tarjeta Sanitaria)" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Idiomas" } }],
                  [{ "type": "text", "text": { "content": "2 (Espanol, Frances)" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Entradas Notion" } }],
                  [{ "type": "text", "text": { "content": "81 en 3 DBs" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Gates completados" } }],
                  [{ "type": "text", "text": { "content": "22/22 PASS" } }]
                ]
              }
            }
          ]
        }
      },
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
              "text": { "content": "Bases de Datos" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Backlog / Issues",
                "link": { "url": "https://notion.so/304c5a0f372a81de92a8f54c03b391c0" }
              },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — 43 entradas. Sprint board con tareas, estados, gates y owners." }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "KB Tramites",
                "link": { "url": "https://notion.so/304c5a0f372a81ff9d45c785e69f7335" }
              },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — 12 entradas. Base de conocimiento verificada con 3 tramites x 4 campos." }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Demo & Testing",
                "link": { "url": "https://notion.so/304c5a0f372a810d8767d77efbd46bb2" }
              },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — 26 entradas. Registro de ejecucion de tests con inputs, outputs y resultados." }
            }
          ]
        }
      },
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
              "text": { "content": "Equipo" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "table",
        "table": {
          "table_width": 2,
          "has_column_header": true,
          "has_row_header": false,
          "children": [
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Persona" } }],
                  [{ "type": "text", "text": { "content": "Rol" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Robert" } }],
                  [{ "type": "text", "text": { "content": "Backend lead, pipeline, presentador de demo" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Marcos" } }],
                  [{ "type": "text", "text": { "content": "Routes, Twilio, deploy, pipeline de audio" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Lucas" } }],
                  [{ "type": "text", "text": { "content": "Investigacion KB, testing, assets de demo" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Daniel" } }],
                  [{ "type": "text", "text": { "content": "Web Gradio (backup), video" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Andrea" } }],
                  [{ "type": "text", "text": { "content": "Notion, slides, coordinacion" } }]
                ]
              }
            }
          ]
        }
      },
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
              "text": { "content": "Deploy y Verificacion" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "🌐" },
          "color": "purple_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Deploy: https://civicaid-voice.onrender.com\nHealth: https://civicaid-voice.onrender.com/health\nRepositorio: GitHub civicaid-voice\nCron warm-up: cada 14 min via cron-job.org"
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:**
```json
{
  "object": "page",
  "id": "<NUEVO_DASHBOARD_ID>",
  "parent": { "page_id": "304c5a0f-372a-801f-995f-ce24036350ad" }
}
```

**Verificacion:** Guardar el `id` de la respuesta como `DASHBOARD_HOME_ID` para pasos posteriores. Luego verificar:

```
Herramienta: mcp__notionApi__API-retrieve-a-page
Payload: { "page_id": "<DASHBOARD_HOME_ID>" }
```

**Rollback:** Si falla la creacion, verificar que la pagina raiz acepta hijos (`parent.page_id` correcto). Si se creo con errores, archivar con `mcp__notionApi__API-update-a-block` poniendo `archived: true`.

---

### Paso 1.2 — Crear pagina "Para Jueces"

**Descripcion:** Pagina de navegacion guiada para jueces y revisores del hackathon. Ofrece una guia paso a paso de que ver y donde encontrarlo en el workspace.

**Herramienta MCP:** `mcp__notionApi__API-post-page`

**Payload:**
```json
{
  "body": {
    "parent": {
      "page_id": "304c5a0f-372a-801f-995f-ce24036350ad"
    },
    "icon": {
      "type": "emoji",
      "emoji": "🧑‍⚖️"
    },
    "properties": {
      "title": {
        "title": [
          {
            "text": {
              "content": "Para Jueces — Guia de Navegacion"
            }
          }
        ]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "👋" },
          "color": "yellow_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Bienvenidos al workspace de CivicAid Voice / Clara. Esta pagina os guia por los elementos clave del proyecto para que podais evaluarlo de forma eficiente."
              }
            }
          ]
        }
      },
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
              "text": { "content": "Que es Clara" }
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
                "content": "Clara es un asistente conversacional de WhatsApp que ayuda a personas vulnerables en Espana a navegar tramites de servicios sociales. Responde en el idioma del usuario (espanol y frances), entiende texto y voz, y da informacion verificada sobre tramites reales: Ingreso Minimo Vital (IMV), Empadronamiento y Tarjeta Sanitaria."
              }
            }
          ]
        }
      },
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
              "text": { "content": "Recorrido recomendado (5 minutos)" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Dashboard Home" },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — Vision general del proyecto, metricas clave y estado de todas las fases." }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Backlog / Issues" },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — Ver el Kanban por Estado para entender el progreso. 43 tareas, 42 completadas." }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "KB Tramites" },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — Explorar la base de conocimiento que usa Clara. 12 entradas verificadas contra fuentes oficiales del gobierno." }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Demo & Testing" },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — Ver los 26 tests ejecutados, agrupados por gate (G1-Texto, G2-Audio, G3-Demo). Todos pasan." }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Paginas de Fase" },
              "annotations": { "bold": true }
            },
            {
              "type": "text",
              "text": { "content": " — Documentacion de progreso de cada fase (0+1, 2, 3). Cada pagina detalla gates y evidencia." }
            }
          ]
        }
      },
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
              "text": { "content": "Que evaluar" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "table",
        "table": {
          "table_width": 3,
          "has_column_header": true,
          "has_row_header": false,
          "children": [
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Aspecto" } }],
                  [{ "type": "text", "text": { "content": "Donde verlo" } }],
                  [{ "type": "text", "text": { "content": "Dato clave" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Progreso del proyecto" } }],
                  [{ "type": "text", "text": { "content": "Backlog > Kanban por Estado" } }],
                  [{ "type": "text", "text": { "content": "42/43 tareas Hecho" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Conocimiento de Clara" } }],
                  [{ "type": "text", "text": { "content": "KB Tramites" } }],
                  [{ "type": "text", "text": { "content": "3 tramites x 4 campos, todos Verificado" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Calidad / Testing" } }],
                  [{ "type": "text", "text": { "content": "Demo & Testing > Board por Gate" } }],
                  [{ "type": "text", "text": { "content": "26 tests, todos Pasa" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Organizacion del equipo" } }],
                  [{ "type": "text", "text": { "content": "Backlog > Tabla por Owner" } }],
                  [{ "type": "text", "text": { "content": "5 miembros, owners asignados" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Rigor tecnico" } }],
                  [{ "type": "text", "text": { "content": "Paginas de fase (gates)" } }],
                  [{ "type": "text", "text": { "content": "22 gates PASS con evidencia" } }]
                ]
              }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "divider",
        "divider": {}
      },
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "🔗" },
          "color": "gray_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Deploy en vivo: https://civicaid-voice.onrender.com/health\nRepositorio: disponible en GitHub\nDocumentacion completa: 36 archivos en /docs/"
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:**
```json
{
  "object": "page",
  "id": "<NUEVO_PARA_JUECES_ID>",
  "parent": { "page_id": "304c5a0f-372a-801f-995f-ce24036350ad" }
}
```

**Verificacion:** Guardar `id` como `PARA_JUECES_ID`. Verificar con `API-retrieve-a-page`.

**Rollback:** Archivar con `API-update-a-block` si se creo con errores.

---

### Paso 1.3 — Crear pagina contenedora "Fases del Proyecto"

**Descripcion:** Pagina contenedora que agrupa las 3 paginas de fase existentes. Sirve como indice de fases con resumen de estado.

**Herramienta MCP:** `mcp__notionApi__API-post-page`

**Payload:**
```json
{
  "body": {
    "parent": {
      "page_id": "304c5a0f-372a-801f-995f-ce24036350ad"
    },
    "icon": {
      "type": "emoji",
      "emoji": "📋"
    },
    "properties": {
      "title": {
        "title": [
          {
            "text": {
              "content": "Fases del Proyecto"
            }
          }
        ]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "📌" },
          "color": "blue_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Indice de todas las fases del proyecto CivicAid Voice / Clara. Cada fase tiene su pagina detallada con gates, evidencia y entregables."
              }
            }
          ]
        }
      },
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
              "text": { "content": "Estado de Fases" }
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
                  [{ "type": "text", "text": { "content": "Fase" } }],
                  [{ "type": "text", "text": { "content": "Estado" } }],
                  [{ "type": "text", "text": { "content": "Gates" } }],
                  [{ "type": "text", "text": { "content": "Fecha cierre" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Fase 0 + Fase 1 — Plan + MVP" } }],
                  [{ "type": "text", "text": { "content": "COMPLETADA" } }],
                  [{ "type": "text", "text": { "content": "G0, G1, G2, G3 — PASS" } }],
                  [{ "type": "text", "text": { "content": "2026-02-12" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Fase 2 — Hardening & Deploy" } }],
                  [{ "type": "text", "text": { "content": "COMPLETADA" } }],
                  [{ "type": "text", "text": { "content": "P2.1-P2.6 — PASS" } }],
                  [{ "type": "text", "text": { "content": "2026-02-12" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Fase 3 — Demo Ready" } }],
                  [{ "type": "text", "text": { "content": "COMPLETADA" } }],
                  [{ "type": "text", "text": { "content": "P3.1-P3.6, QA Deep — PASS" } }],
                  [{ "type": "text", "text": { "content": "2026-02-13" } }]
                ]
              }
            }
          ]
        }
      },
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
              "text": { "content": "Enlaces a paginas de fase" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Fase 0 + Fase 1 — Plan Maestro + MVP",
                "link": { "url": "https://www.notion.so/305c5a0f372a81c8b609cc5fe793bfe4" }
              },
              "annotations": { "bold": true }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Fase 2 — Hardening & Deploy",
                "link": { "url": "https://www.notion.so/Phase-2-Hardening-Deploy-305c5a0f372a813b8915f7e6c21fd055" }
              },
              "annotations": { "bold": true }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Fase 3 — Demo Ready",
                "link": { "url": "https://www.notion.so/Phase-3-Demo-Ready-305c5a0f372a818d91a7f59c22551350" }
              },
              "annotations": { "bold": true }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:**
```json
{
  "object": "page",
  "id": "<NUEVO_FASES_CONTAINER_ID>",
  "parent": { "page_id": "304c5a0f-372a-801f-995f-ce24036350ad" }
}
```

**Verificacion:** Guardar `id` como `FASES_CONTAINER_ID`. Verificar con `API-retrieve-a-page`.

**Rollback:** Archivar con `API-update-a-block` si se creo con errores.

---

### Paso 1.4 — Verificar estructura creada en Fase 1

**Descripcion:** Confirmar que las 3 nuevas paginas existen como hijas de CivicAid OS.

**Herramienta MCP:** `mcp__notionApi__API-get-block-children`

**Payload:**
```json
{
  "block_id": "304c5a0f-372a-801f-995f-ce24036350ad"
}
```

**Respuesta esperada:** Los hijos de CivicAid OS ahora deben incluir:
- Las 3 DBs existentes (Backlog, KB, Testing)
- Las 3 paginas de fase existentes (F0+1, F2, F3)
- Las 3 nuevas paginas: Dashboard Home, Para Jueces, Fases del Proyecto

**Criterio de exito:** 6+ bloques hijos, incluyendo los 3 nuevos.

---

### Resumen Fase 1 — Tabla de ejecucion

| # | Paso | Herramienta | Pagina creada | Tiempo est. |
|---|---|---|---|---|
| 1.1 | Dashboard Home | `API-post-page` | Dashboard Home | 5 min |
| 1.2 | Para Jueces | `API-post-page` | Para Jueces — Guia de Navegacion | 4 min |
| 1.3 | Fases del Proyecto | `API-post-page` | Fases del Proyecto (contenedor) | 4 min |
| 1.4 | Verificacion | `API-get-block-children` | (verificacion) | 2 min |

---

## Fase 2: Enriquecer DBs (10 min)

**Objetivo:** Anadir nuevas propiedades a las bases de datos existentes para mejorar la trazabilidad y navegabilidad. Crear relaciones entre DBs cuando la API lo permita.

**Nota importante sobre la API de Notion:** La API de Notion (version 2022-06-28) **no soporta la creacion de vistas (views) programaticamente**. Las vistas solo se pueden crear desde la interfaz web de Notion. Lo que si se puede hacer via API es:
- Anadir propiedades a DBs existentes (`PATCH /databases/{id}`)
- Crear relaciones entre DBs (tipo `relation`)
- Modificar propiedades de paginas existentes

---

### Paso 2.1 — Anadir propiedad "Fase" al Backlog

**Descripcion:** Anadir una propiedad `Select` llamada "Fase" para filtrar tareas por fase del proyecto. Actualmente solo existe "Gate" y "Dia", pero no una agrupacion por fase.

**Herramienta MCP:** `mcp__notionApi__API-patch-page` no sirve para esto. Se necesita actualizar la DB directamente.

**Nota:** La API de Notion soporta `PATCH /databases/{database_id}` para modificar el schema. Sin embargo, la herramienta MCP disponible es `mcp__notionApi__API-retrieve-a-database` (solo lectura). Si el MCP no expone una operacion de update de DB, este paso debe hacerse via **curl directo** o **manualmente desde Notion web**.

**Via curl (backup):**
```bash
curl -X PATCH "https://api.notion.com/v1/databases/304c5a0f-372a-81de-92a8-f54c03b391c0" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Fase": {
        "select": {
          "options": [
            { "name": "F0-Plan", "color": "gray" },
            { "name": "F1-MVP", "color": "blue" },
            { "name": "F2-Hardening", "color": "orange" },
            { "name": "F3-Demo", "color": "green" }
          ]
        }
      }
    }
  }'
```

**Respuesta esperada:** HTTP 200 con el schema actualizado incluyendo la nueva propiedad.

**Rollback:** Eliminar la propiedad via `PATCH` con `"Fase": null` en el body de properties.

---

### Paso 2.2 — Anadir propiedad "Categoria" a KB Tramites

**Descripcion:** Anadir una propiedad `Select` llamada "Categoria" para clasificar tramites por area tematica. Facilita la navegacion para jueces.

**Via curl (backup):**
```bash
curl -X PATCH "https://api.notion.com/v1/databases/304c5a0f-372a-81ff-9d45-c785e69f7335" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Categoria": {
        "select": {
          "options": [
            { "name": "Prestaciones economicas", "color": "green" },
            { "name": "Registro civil", "color": "blue" },
            { "name": "Sanidad", "color": "red" }
          ]
        }
      }
    }
  }'
```

**Respuesta esperada:** HTTP 200 con el schema actualizado.

**Rollback:** `"Categoria": null` en el body de properties via PATCH.

---

### Paso 2.3 — Anadir propiedad "Ejecutor" a Demo & Testing

**Descripcion:** Anadir una propiedad `Select` llamada "Ejecutor" para registrar quien ejecuto cada test. Complementa la informacion existente.

**Via curl (backup):**
```bash
curl -X PATCH "https://api.notion.com/v1/databases/304c5a0f-372a-810d-8767-d77efbd46bb2" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Ejecutor": {
        "select": {
          "options": [
            { "name": "Robert", "color": "blue" },
            { "name": "Marcos", "color": "orange" },
            { "name": "Lucas", "color": "green" },
            { "name": "Daniel", "color": "purple" },
            { "name": "Andrea", "color": "pink" },
            { "name": "Automatico", "color": "gray" }
          ]
        }
      }
    }
  }'
```

**Respuesta esperada:** HTTP 200 con schema actualizado.

**Rollback:** `"Ejecutor": null` en properties.

---

### Paso 2.4 — Crear relacion Backlog <-> Demo & Testing

**Descripcion:** Crear una propiedad de tipo `relation` en el Backlog que enlace a Demo & Testing. Permite ver que tests cubren cada tarea.

**Via curl (backup):**
```bash
curl -X PATCH "https://api.notion.com/v1/databases/304c5a0f-372a-81de-92a8-f54c03b391c0" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Tests relacionados": {
        "relation": {
          "database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2",
          "single_property": {}
        }
      }
    }
  }'
```

**Respuesta esperada:** HTTP 200. La DB Backlog tendra una nueva columna "Tests relacionados" que es una relation a Demo & Testing.

**Rollback:** `"Tests relacionados": null` en properties.

---

### Paso 2.5 — Poblar las nuevas propiedades en entradas existentes

**Descripcion:** Actualizar entradas existentes del Backlog para llenar la propiedad "Fase". Esto se hace via `mcp__notionApi__API-patch-page` o via `mcp__notionApi__API-query-data-source` (para obtener IDs) + `API-patch-page` (para actualizar).

**Estrategia:** Consultar el Backlog agrupado por Gate, y asignar Fase segun la correspondencia:

| Gate | Fase |
|---|---|
| G0-Tooling | F0-Plan |
| G1-Texto | F1-MVP |
| G2-Audio | F1-MVP |
| G3-Demo | F3-Demo |
| Infra | F2-Hardening |

**Paso 2.5a — Obtener todas las entradas del Backlog:**

**Herramienta MCP:** `mcp__notionApi__API-query-data-source`

**Payload:**
```json
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {}
}
```

**Paso 2.5b — Para cada entrada, actualizar con la Fase correcta:**

**Herramienta MCP:** `mcp__notionApi__API-patch-page`

**Payload (ejemplo para una entrada con Gate=G1-Texto):**
```json
{
  "page_id": "<PAGE_ID_DE_LA_ENTRADA>",
  "body": {
    "properties": {
      "Fase": {
        "select": {
          "name": "F1-MVP"
        }
      }
    }
  }
}
```

**Nota:** Se necesita iterar sobre las 43 entradas. En la practica, agrupar por Gate y hacer batch:
- G0-Tooling -> F0-Plan (estimado: ~5 entradas)
- G1-Texto -> F1-MVP (estimado: ~15 entradas)
- G2-Audio -> F1-MVP (estimado: ~10 entradas)
- Infra -> F2-Hardening (estimado: ~8 entradas)
- G3-Demo -> F3-Demo (estimado: ~5 entradas)

**Respuesta esperada por cada update:** HTTP 200 con la pagina actualizada.

**Rollback:** Revertir con `"Fase": null` en cada pagina actualizada, o eliminar la propiedad completa de la DB (Paso 2.1 rollback).

---

### Paso 2.6 — Poblar "Categoria" en KB Tramites

**Descripcion:** Actualizar las 12 entradas de KB con la categoria correspondiente.

**Herramienta MCP:** `mcp__notionApi__API-query-data-source` + `API-patch-page`

**Paso 2.6a — Obtener entradas:**
```json
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335",
  "body": {}
}
```

**Paso 2.6b — Actualizar cada entrada:**

| Tramite | Categoria |
|---|---|
| IMV | Prestaciones economicas |
| Empadronamiento | Registro civil |
| Tarjeta Sanitaria | Sanidad |

**Payload (ejemplo para IMV):**
```json
{
  "page_id": "<PAGE_ID_ENTRADA_IMV>",
  "body": {
    "properties": {
      "Categoria": {
        "select": {
          "name": "Prestaciones economicas"
        }
      }
    }
  }
}
```

**Respuesta esperada:** HTTP 200 por cada actualizacion.

**Rollback:** Revertir cada entrada con `"Categoria": null`.

---

### Paso 2.7 — Crear vistas recomendadas (manual en Notion web)

**Descripcion:** Las vistas NO se pueden crear via API. Se deben crear manualmente en la interfaz web de Notion. A continuacion la lista de vistas a crear:

**Backlog — Vistas nuevas:**

| Vista | Tipo | Agrupar por | Filtro | Proposito |
|---|---|---|---|---|
| Board por Fase | Board | Fase | Ninguno | Vision de progreso por fase |
| Timeline | Timeline | Dia | Solo con Dia asignado | Vista temporal del proyecto |

**KB Tramites — Vistas nuevas:**

| Vista | Tipo | Agrupar por | Filtro | Proposito |
|---|---|---|---|---|
| Por Categoria | Board | Categoria | Ninguno | Navegacion por area tematica |
| Por Organismo | Board | Organismo | Ninguno | Navegacion por fuente |

**Demo & Testing — Vistas nuevas:**

| Vista | Tipo | Agrupar por | Filtro | Proposito |
|---|---|---|---|---|
| Por Ejecutor | Table | Ejecutor | Ninguno | Ver quien ejecuto cada test |
| Resumen | Table | Ninguno | Solo ultimo test de cada tipo | Vista limpia para jueces |

**Instrucciones para crear vistas manualmente:**
1. Abrir la DB en Notion web
2. Clic en `+` junto al nombre de la vista actual
3. Seleccionar tipo de vista (Board, Table, Timeline)
4. Configurar "Group by" y filtros segun la tabla anterior
5. Renombrar la vista

---

### Resumen Fase 2 — Tabla de ejecucion

| # | Paso | Metodo | Descripcion | Tiempo est. |
|---|---|---|---|---|
| 2.1 | Propiedad Fase en Backlog | curl / manual | Nueva propiedad Select | 1 min |
| 2.2 | Propiedad Categoria en KB | curl / manual | Nueva propiedad Select | 1 min |
| 2.3 | Propiedad Ejecutor en Testing | curl / manual | Nueva propiedad Select | 1 min |
| 2.4 | Relacion Backlog<->Testing | curl / manual | Nueva propiedad Relation | 1 min |
| 2.5 | Poblar Fase (43 entradas) | MCP `API-patch-page` | Asignar fase a cada tarea | 3 min |
| 2.6 | Poblar Categoria (12 entradas) | MCP `API-patch-page` | Asignar categoria a cada KB | 1 min |
| 2.7 | Crear vistas | Manual (Notion web) | 6 nuevas vistas | 2 min |

---

## Fase 3: Poblar contenido (10 min)

**Objetivo:** Anadir contenido adicional a las paginas creadas en Fase 1, y enriquecer las paginas de fase existentes con bloques informativos.

---

### Paso 3.1 — Anadir bloques de arquitectura al Dashboard Home

**Descripcion:** Anadir un bloque con el diagrama de arquitectura simplificado al Dashboard Home creado en el Paso 1.1.

**Herramienta MCP:** `mcp__notionApi__API-patch-block-children`

**Payload:**
```json
{
  "block_id": "<DASHBOARD_HOME_ID>",
  "body": {
    "children": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Arquitectura" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "code",
        "code": {
          "language": "plain text",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Usuario WhatsApp --> Twilio --> Flask /webhook --> TwiML ACK (<1s)\n                                               --> Hilo de fondo:\n                                                 cache_match --> HIT --> Twilio REST --> Usuario\n                                                 cache_match --> MISS --> KB + Gemini --> Twilio REST --> Usuario"
              }
            }
          ]
        }
      },
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
              "text": { "content": "Stack Tecnologico" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "table",
        "table": {
          "table_width": 2,
          "has_column_header": true,
          "has_row_header": false,
          "children": [
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Componente" } }],
                  [{ "type": "text", "text": { "content": "Tecnologia" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Lenguaje" } }],
                  [{ "type": "text", "text": { "content": "Python 3.11" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Framework" } }],
                  [{ "type": "text", "text": { "content": "Flask" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Canal" } }],
                  [{ "type": "text", "text": { "content": "Twilio WhatsApp Sandbox" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Transcripcion" } }],
                  [{ "type": "text", "text": { "content": "Gemini (primario) / Whisper base (local)" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "LLM" } }],
                  [{ "type": "text", "text": { "content": "Gemini 1.5 Flash" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Text-to-Speech" } }],
                  [{ "type": "text", "text": { "content": "gTTS" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "KB" } }],
                  [{ "type": "text", "text": { "content": "JSON estatico (3 ficheros verificados)" } }]
                ]
              }
            },
            {
              "type": "table_row",
              "table_row": {
                "cells": [
                  [{ "type": "text", "text": { "content": "Deploy" } }],
                  [{ "type": "text", "text": { "content": "Render (free tier) + Docker" } }]
                ]
              }
            }
          ]
        }
      },
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
              "text": { "content": "Documentacion" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "📚" },
          "color": "gray_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "36 archivos de documentacion en /docs/\n- 00-EXECUTIVE-SUMMARY.md — Resumen ejecutivo (1-pager)\n- 01-phases/ — Planes de cada fase (F0-F3)\n- 02-architecture/ — Arquitectura tecnica\n- 03-runbooks/ — Procedimientos operativos\n- 04-testing/ — Plan de tests y evals\n- 05-ops/ — Deploy y observabilidad\n- 06-integrations/ — Notion, Twilio, MCP\n- 07-evidence/ — Evidencia de cada fase"
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:** HTTP 200 con los nuevos bloques creados como hijos del Dashboard.

**Verificacion:**
```json
{
  "block_id": "<DASHBOARD_HOME_ID>"
}
```
con `API-get-block-children` para confirmar que todos los bloques se anadieron.

**Rollback:** Usar `API-update-a-block` con `archived: true` en cada bloque anadido, usando los IDs devueltos en la respuesta de creacion.

---

### Paso 3.2 — Anadir contenido de impacto social al Dashboard Home

**Descripcion:** Anadir una seccion de impacto social que refuerce la narrativa para jueces.

**Herramienta MCP:** `mcp__notionApi__API-patch-block-children`

**Payload:**
```json
{
  "block_id": "<DASHBOARD_HOME_ID>",
  "body": {
    "children": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Impacto Social" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "💙" },
          "color": "blue_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "3,2 millones de inmigrantes en Espana.\n40% no completa tramites por barrera idiomatica.\n9,5 millones de personas mayores con dificultad digital.\nWhatsApp: 95% de penetracion en Espana.\nCoste por consulta: 0,002 EUR (cache) a 0,01 EUR (LLM)."
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:** HTTP 200.

**Rollback:** Archivar bloques con `API-update-a-block`.

---

### Paso 3.3 — Enriquecer pagina Fase 3 con resumen de cierre

**Descripcion:** Anadir bloques de resumen de cierre a la pagina Phase 3 existente.

**Herramienta MCP:** `mcp__notionApi__API-patch-block-children`

**Payload:**
```json
{
  "block_id": "305c5a0f-372a-818d-91a7-f59c22551350",
  "body": {
    "children": [
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
              "text": { "content": "Resumen de Cierre — Fase 3" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "🏁" },
          "color": "green_background",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "Fase 3 COMPLETADA el 2026-02-13.\n\n1. Twilio WhatsApp Real — Sandbox configurado, signature validation activa\n2. Deploy & Ops — Render estable (avg 166ms), cron 14 min, runbook 8 escenarios\n3. QA & Evidence — phase3_verify.sh, 93/93 tests, ruff clean\n4. Logging JSON — JSONFormatter con request_id + timings\n5. Notion OS — 81 entradas, owners asignados (97.7%), Phase 3 page\n6. Demo — Guion 6-8 min con WOW 1+2, 1-pager, 8 riesgos mitigados\n7. QA Deep Audit — 12 contradicciones detectadas, 11 corregidas, 0 secretos"
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:** HTTP 200.

**Rollback:** Archivar bloques anadidos.

---

### Paso 3.4 — Anadir bloque de verificacion rapida a la pagina "Para Jueces"

**Descripcion:** Anadir una seccion con comandos de verificacion para que un juez tecnico pueda verificar claims.

**Herramienta MCP:** `mcp__notionApi__API-patch-block-children`

**Payload:**
```json
{
  "block_id": "<PARA_JUECES_ID>",
  "body": {
    "children": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
          "rich_text": [
            {
              "type": "text",
              "text": { "content": "Verificacion rapida (para jueces tecnicos)" }
            }
          ]
        }
      },
      {
        "object": "block",
        "type": "code",
        "code": {
          "language": "bash",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "# Health check del deploy en Render\ncurl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool\n\n# Verificar que los audios MP3 son accesibles\ncurl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3\n\n# Ejecutar los 96 tests automatizados\npytest tests/ -v --tb=short\n\n# Verificar lint limpio\nruff check src/ tests/ --select E,F,W --ignore E501"
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Respuesta esperada:** HTTP 200.

**Rollback:** Archivar bloques anadidos.

---

### Resumen Fase 3 — Tabla de ejecucion

| # | Paso | Herramienta | Pagina destino | Contenido anadido | Tiempo est. |
|---|---|---|---|---|---|
| 3.1 | Arquitectura + Stack | `API-patch-block-children` | Dashboard Home | Diagrama, tabla stack, docs | 3 min |
| 3.2 | Impacto social | `API-patch-block-children` | Dashboard Home | Callout con datos | 2 min |
| 3.3 | Cierre Fase 3 | `API-patch-block-children` | Phase 3 page | Resumen de cierre | 2 min |
| 3.4 | Verificacion jueces | `API-patch-block-children` | Para Jueces | Comandos de verificacion | 3 min |

---

## Fase 4: Verificacion (5 min)

**Objetivo:** Confirmar que toda la reestructuracion se aplico correctamente. Verificar conteos, estructura y contenido.

---

### Paso 4.1 — Verificar estructura de hijos de CivicAid OS

**Herramienta MCP:** `mcp__notionApi__API-get-block-children`

**Payload:**
```json
{
  "block_id": "304c5a0f-372a-801f-995f-ce24036350ad"
}
```

**Esperado:** Los hijos incluyen (entre otros):
- Dashboard Home (nueva)
- Para Jueces (nueva)
- Fases del Proyecto (nueva)
- 3 DBs existentes
- 3 paginas de fase existentes

**Criterio de exito:** Al menos 6 bloques hijos identificables.

---

### Paso 4.2 — Verificar que Dashboard Home tiene contenido

**Herramienta MCP:** `mcp__notionApi__API-get-block-children`

**Payload:**
```json
{
  "block_id": "<DASHBOARD_HOME_ID>"
}
```

**Esperado:** Multiples bloques incluyendo callouts, tablas, heading_2, dividers y listas. Minimo 15 bloques hijos.

**Criterio de exito:** `results.length >= 15`.

---

### Paso 4.3 — Verificar que "Para Jueces" tiene contenido

**Herramienta MCP:** `mcp__notionApi__API-get-block-children`

**Payload:**
```json
{
  "block_id": "<PARA_JUECES_ID>"
}
```

**Esperado:** Bloques de callout, tabla, lista numerada, codigo. Minimo 10 bloques hijos.

**Criterio de exito:** `results.length >= 10`.

---

### Paso 4.4 — Verificar que los conteos de DBs no cambiaron

**Herramienta MCP:** `mcp__notionApi__API-query-data-source` (3 veces)

**Payloads:** Identicos a los del Paso 0.4.

**Esperado:**

| DB | Entradas antes | Entradas despues |
|---|---|---|
| Backlog | 43 | 43 (sin cambio en conteo, solo nuevas propiedades) |
| KB Tramites | 12 | 12 |
| Demo & Testing | 26 | 26 |
| **Total** | **81** | **81** |

**Criterio de exito:** Los conteos son iguales. Si hay diferencia, investigar.

---

### Paso 4.5 — Verificar nuevas propiedades en DBs

**Herramienta MCP:** `mcp__notionApi__API-retrieve-a-database` (3 veces)

**Payloads:** Identicos a los del Paso 0.3.

**Esperado:**
- Backlog: propiedades incluyen `Fase` (select) y `Tests relacionados` (relation)
- KB Tramites: propiedades incluyen `Categoria` (select)
- Demo & Testing: propiedades incluyen `Ejecutor` (select)

**Criterio de exito:** Las nuevas propiedades aparecen en el schema de cada DB.

---

### Paso 4.6 — Verificar que las propiedades estan pobladas

**Herramienta MCP:** `mcp__notionApi__API-query-data-source`

**Payload (verificar Fase en Backlog):**
```json
{
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {
    "filter": {
      "property": "Fase",
      "select": {
        "is_not_empty": true
      }
    }
  }
}
```

**Esperado:** `results.length == 43` (todas las entradas tienen Fase asignada).

**Payload (verificar Categoria en KB):**
```json
{
  "database_id": "304c5a0f-372a-81ff-9d45-c785e69f7335",
  "body": {
    "filter": {
      "property": "Categoria",
      "select": {
        "is_not_empty": true
      }
    }
  }
}
```

**Esperado:** `results.length == 12`.

---

### Paso 4.7 — Busqueda global de verificacion

**Herramienta MCP:** `mcp__notionApi__API-post-search`

**Payload:**
```json
{
  "query": "Dashboard Home"
}
```

**Esperado:** Al menos 1 resultado con el titulo "Dashboard Home".

**Payload adicional:**
```json
{
  "query": "Para Jueces"
}
```

**Esperado:** Al menos 1 resultado con el titulo "Para Jueces — Guia de Navegacion".

---

### Checklist de Verificacion Final

| # | Verificacion | Herramienta | Criterio | Estado |
|---|---|---|---|---|
| 4.1 | Estructura raiz tiene 6+ hijos | `API-get-block-children` | `results.length >= 6` | [ ] |
| 4.2 | Dashboard Home tiene 15+ bloques | `API-get-block-children` | `results.length >= 15` | [ ] |
| 4.3 | Para Jueces tiene 10+ bloques | `API-get-block-children` | `results.length >= 10` | [ ] |
| 4.4 | 81 entradas totales sin cambio | `API-query-data-source` x3 | 43 + 12 + 26 = 81 | [ ] |
| 4.5 | Nuevas propiedades en schemas | `API-retrieve-a-database` x3 | Fase, Categoria, Ejecutor | [ ] |
| 4.6 | Propiedades pobladas | `API-query-data-source` + filtro | 43 + 12 con valor | [ ] |
| 4.7 | Nuevas paginas buscables | `API-post-search` x2 | Dashboard + Para Jueces | [ ] |

**Criterio de exito global:** Los 7 checks pasan. Si alguno falla, consultar la seccion de rollback del paso correspondiente.

---

## Matriz de Riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigacion | Deteccion |
|---|---|---|---|---|---|
| R1 | Token Notion expirado o sin permisos | Baja | Critico (bloquea todo) | Verificar en Paso 0.1 antes de hacer nada. Regenerar token si falla. | Paso 0.1 |
| R2 | Pagina raiz no compartida con integracion | Baja | Critico | Compartir manualmente desde Notion web: Settings > Connections > Add CivicAid Integration | Paso 0.2 |
| R3 | API rate limit (3 requests/segundo) | Media | Medio | Espaciar peticiones. No hacer mas de 2 llamadas por segundo. Backoff exponencial si se recibe HTTP 429. | Cualquier paso |
| R4 | Payload JSON invalido | Baja | Bajo | Validar JSON antes de enviar. Los payloads de este documento estan pre-validados. | Error HTTP 400 |
| R5 | Bloque creado con contenido incorrecto | Baja | Bajo | Verificar despues de cada paso. Archivar el bloque con `archived: true` y recrear. | Pasos de verificacion |
| R6 | Propiedad de DB ya existe con ese nombre | Baja | Bajo | La API de Notion hace upsert: si la propiedad ya existe, la actualiza. No se duplica. | Paso 2.x |
| R7 | Paginas de fase no accesibles (permisos) | Baja | Medio | Verificar en Paso 0.5. Si no son accesibles, omitir el Paso 3.3 (enriquecer Fase 3). | Paso 0.5 |
| R8 | MCP server no expone operacion PATCH databases | Media | Medio | Usar curl directo como backup (scripts incluidos). O crear propiedades manualmente en Notion web. | Paso 2.1 |
| R9 | Notion API cambia entre versiones | Muy baja | Medio | Todo este plan usa `Notion-Version: 2022-06-28`, que es estable. No usar headers de version mas reciente sin probar. | N/A |
| R10 | Error al poblar 43 entradas con Fase (batch grande) | Media | Bajo | Hacer en grupos de 10. Si una falla, continuar con las demas. Registrar las fallidas para reintentar. | Paso 2.5 |

---

## Tiempo Estimado Total

| Fase | Descripcion | Tiempo |
|---|---|---|
| Fase 0 | Auditoria y verificacion | 5 min |
| Fase 1 | Crear estructura nueva (3 paginas) | 15 min |
| Fase 2 | Enriquecer DBs (propiedades + poblacion) | 10 min |
| Fase 3 | Poblar contenido (bloques en paginas) | 10 min |
| Fase 4 | Verificacion final | 5 min |
| **Total** | | **45 min** |

**Prerequisitos antes de iniciar:**
1. Token Notion configurado en `~/.mcp.json` con permisos de lectura/escritura
2. Servidor MCP `notionApi` activo (Claude Code reiniciado tras configuracion)
3. Las 3 DBs y la pagina raiz compartidas con la integracion en Notion web
4. Node.js instalado (para `npx` y el servidor MCP)

---

## Script de Automatizacion (backup curl)

Script bash completo que ejecuta todos los pasos via curl directo a la API de Notion, como alternativa al MCP. Util si el MCP no esta disponible o como verificacion independiente.

**Archivo:** `scripts/notion_restructure.sh`

```bash
#!/usr/bin/env bash
# notion_restructure.sh — Reestructura el workspace CivicAid OS en Notion
# Ejecuta TODOS los pasos de la Seccion 7 del plan de implementacion
# Usage: bash scripts/notion_restructure.sh
# Prerequisito: NOTION_TOKEN configurado en ~/.mcp.json o como env var

set -euo pipefail

# ============================================================
# CONFIGURACION
# ============================================================

# --- Extraer token ---
if [ -z "${NOTION_TOKEN:-}" ]; then
  NOTION_TOKEN=$(python3 -c "
import json
with open('$HOME/.mcp.json') as f:
    d = json.load(f)
print(d['mcpServers']['notionApi']['env'].get('NOTION_TOKEN',''))
" 2>/dev/null || echo "")
fi

if [ -z "$NOTION_TOKEN" ]; then
  echo "ERROR: No NOTION_TOKEN found. Set it in ~/.mcp.json or export NOTION_TOKEN=ntn_xxx"
  exit 1
fi

NOTION_API="https://api.notion.com/v1"
NOTION_VERSION="2022-06-28"

# IDs conocidos
ROOT_PAGE="304c5a0f-372a-801f-995f-ce24036350ad"
BACKLOG_DB="304c5a0f-372a-81de-92a8-f54c03b391c0"
KB_DB="304c5a0f-372a-81ff-9d45-c785e69f7335"
TEST_DB="304c5a0f-372a-810d-8767-d77efbd46bb2"
FASE01_PAGE="305c5a0f-372a-81c8-b609-cc5fe793bfe4"
FASE2_PAGE="305c5a0f-372a-813b-8915-f7e6c21fd055"
FASE3_PAGE="305c5a0f-372a-818d-91a7-f59c22551350"

# Contadores
CREATED=0
UPDATED=0
FAILED=0

# Funcion helper para llamadas a la API
notion_api() {
  local method="$1"
  local endpoint="$2"
  local data="${3:-}"
  local label="${4:-$endpoint}"

  if [ "$method" = "GET" ]; then
    RESP=$(curl -s -w "\n%{http_code}" \
      "${NOTION_API}${endpoint}" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: $NOTION_VERSION")
  else
    RESP=$(curl -s -w "\n%{http_code}" -X "$method" \
      "${NOTION_API}${endpoint}" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: $NOTION_VERSION" \
      -H "Content-Type: application/json" \
      -d "$data")
  fi

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" = "200" ]; then
    echo "  OK [$HTTP_CODE] $label"
    return 0
  else
    echo "  FAIL [$HTTP_CODE] $label"
    echo "  Response: $(echo "$BODY" | head -c 200)"
    return 1
  fi
}

# ============================================================
# FASE 0: AUDITORIA
# ============================================================
echo ""
echo "=========================================="
echo "FASE 0: AUDITORIA (verificacion previa)"
echo "=========================================="

echo ""
echo "--- Paso 0.1: Verificar token ---"
notion_api GET "/users/me" "" "Token verification" || {
  echo "FATAL: Token invalido. Regenerar en https://www.notion.so/my-integrations"
  exit 1
}

echo ""
echo "--- Paso 0.2: Verificar pagina raiz ---"
notion_api GET "/pages/$ROOT_PAGE" "" "CivicAid OS root page" || {
  echo "FATAL: Pagina raiz no accesible. Compartir con la integracion."
  exit 1
}

echo ""
echo "--- Paso 0.3: Verificar 3 DBs ---"
notion_api GET "/databases/$BACKLOG_DB" "" "Backlog DB" || exit 1
notion_api GET "/databases/$KB_DB" "" "KB Tramites DB" || exit 1
notion_api GET "/databases/$TEST_DB" "" "Demo & Testing DB" || exit 1

echo ""
echo "--- Paso 0.4: Contar entradas ---"
for DB_ID in "$BACKLOG_DB" "$KB_DB" "$TEST_DB"; do
  RESP=$(curl -s -X POST "${NOTION_API}/databases/${DB_ID}/query" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: $NOTION_VERSION" \
    -H "Content-Type: application/json" \
    -d '{}')
  COUNT=$(echo "$RESP" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('results',[])))" 2>/dev/null || echo "?")
  echo "  DB $DB_ID: $COUNT entradas"
done

echo ""
echo "FASE 0: COMPLETADA - todos los checks pasan"
echo ""

# ============================================================
# FASE 1: CREAR ESTRUCTURA NUEVA
# ============================================================
echo "=========================================="
echo "FASE 1: CREAR ESTRUCTURA NUEVA"
echo "=========================================="

echo ""
echo "--- Paso 1.1: Crear Dashboard Home ---"
DASHBOARD_RESP=$(curl -s -X POST "${NOTION_API}/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: $NOTION_VERSION" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "page_id": "'"$ROOT_PAGE"'" },
    "icon": { "type": "emoji", "emoji": "🏠" },
    "properties": {
      "title": { "title": [{ "text": { "content": "Dashboard Home" } }] }
    },
    "children": [
      {
        "object": "block", "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "🎯" },
          "color": "blue_background",
          "rich_text": [{ "type": "text", "text": { "content": "CivicAid Voice / Clara — Asistente conversacional de WhatsApp para tramites de servicios sociales en Espana. 3 tramites, 2 idiomas, 96 tests, 11 skills." } }]
        }
      },
      { "object": "block", "type": "divider", "divider": {} },
      {
        "object": "block", "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "✅" },
          "color": "green_background",
          "rich_text": [{ "type": "text", "text": { "content": "TODAS LAS FASES COMPLETADAS — F0 (Plan), F1 (MVP), F2 (Hardening), F3 (Demo Ready). 22 gates PASS. 81 entradas Notion. 96 tests." } }]
        }
      }
    ]
  }')

DASHBOARD_ID=$(echo "$DASHBOARD_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','FAIL'))" 2>/dev/null || echo "FAIL")
if [ "$DASHBOARD_ID" != "FAIL" ]; then
  echo "  OK Dashboard Home creado: $DASHBOARD_ID"
  CREATED=$((CREATED + 1))
else
  echo "  FAIL al crear Dashboard Home"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 1.2: Crear Para Jueces ---"
JUECES_RESP=$(curl -s -X POST "${NOTION_API}/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: $NOTION_VERSION" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "page_id": "'"$ROOT_PAGE"'" },
    "icon": { "type": "emoji", "emoji": "🧑‍⚖️" },
    "properties": {
      "title": { "title": [{ "text": { "content": "Para Jueces — Guia de Navegacion" } }] }
    },
    "children": [
      {
        "object": "block", "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "👋" },
          "color": "yellow_background",
          "rich_text": [{ "type": "text", "text": { "content": "Bienvenidos al workspace de CivicAid Voice / Clara. Esta pagina os guia por los elementos clave del proyecto para evaluarlo de forma eficiente." } }]
        }
      },
      { "object": "block", "type": "divider", "divider": {} },
      {
        "object": "block", "type": "paragraph",
        "paragraph": {
          "rich_text": [{ "type": "text", "text": { "content": "Clara es un asistente de WhatsApp que ayuda a personas vulnerables a navegar tramites de servicios sociales en Espana. Responde en espanol y frances, con texto y voz, usando informacion verificada." } }]
        }
      }
    ]
  }')

JUECES_ID=$(echo "$JUECES_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','FAIL'))" 2>/dev/null || echo "FAIL")
if [ "$JUECES_ID" != "FAIL" ]; then
  echo "  OK Para Jueces creado: $JUECES_ID"
  CREATED=$((CREATED + 1))
else
  echo "  FAIL al crear Para Jueces"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 1.3: Crear Fases del Proyecto ---"
FASES_RESP=$(curl -s -X POST "${NOTION_API}/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: $NOTION_VERSION" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "page_id": "'"$ROOT_PAGE"'" },
    "icon": { "type": "emoji", "emoji": "📋" },
    "properties": {
      "title": { "title": [{ "text": { "content": "Fases del Proyecto" } }] }
    },
    "children": [
      {
        "object": "block", "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "📌" },
          "color": "blue_background",
          "rich_text": [{ "type": "text", "text": { "content": "Indice de todas las fases del proyecto CivicAid Voice / Clara." } }]
        }
      },
      { "object": "block", "type": "divider", "divider": {} },
      {
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [{ "type": "text", "text": { "content": "Fase 0 + Fase 1 — Plan Maestro + MVP — COMPLETADA" }, "annotations": { "bold": true } }]
        }
      },
      {
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [{ "type": "text", "text": { "content": "Fase 2 — Hardening & Deploy — COMPLETADA" }, "annotations": { "bold": true } }]
        }
      },
      {
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {
          "rich_text": [{ "type": "text", "text": { "content": "Fase 3 — Demo Ready — COMPLETADA" }, "annotations": { "bold": true } }]
        }
      }
    ]
  }')

FASES_ID=$(echo "$FASES_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','FAIL'))" 2>/dev/null || echo "FAIL")
if [ "$FASES_ID" != "FAIL" ]; then
  echo "  OK Fases del Proyecto creado: $FASES_ID"
  CREATED=$((CREATED + 1))
else
  echo "  FAIL al crear Fases del Proyecto"
  FAILED=$((FAILED + 1))
fi

# ============================================================
# FASE 2: ENRIQUECER DBs
# ============================================================
echo ""
echo "=========================================="
echo "FASE 2: ENRIQUECER DBs"
echo "=========================================="

echo ""
echo "--- Paso 2.1: Anadir propiedad Fase al Backlog ---"
if notion_api PATCH "/databases/$BACKLOG_DB" '{
  "properties": {
    "Fase": {
      "select": {
        "options": [
          { "name": "F0-Plan", "color": "gray" },
          { "name": "F1-MVP", "color": "blue" },
          { "name": "F2-Hardening", "color": "orange" },
          { "name": "F3-Demo", "color": "green" }
        ]
      }
    }
  }
}' "Propiedad Fase en Backlog"; then
  UPDATED=$((UPDATED + 1))
else
  FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 2.2: Anadir propiedad Categoria a KB ---"
if notion_api PATCH "/databases/$KB_DB" '{
  "properties": {
    "Categoria": {
      "select": {
        "options": [
          { "name": "Prestaciones economicas", "color": "green" },
          { "name": "Registro civil", "color": "blue" },
          { "name": "Sanidad", "color": "red" }
        ]
      }
    }
  }
}' "Propiedad Categoria en KB"; then
  UPDATED=$((UPDATED + 1))
else
  FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 2.3: Anadir propiedad Ejecutor a Testing ---"
if notion_api PATCH "/databases/$TEST_DB" '{
  "properties": {
    "Ejecutor": {
      "select": {
        "options": [
          { "name": "Robert", "color": "blue" },
          { "name": "Marcos", "color": "orange" },
          { "name": "Lucas", "color": "green" },
          { "name": "Daniel", "color": "purple" },
          { "name": "Andrea", "color": "pink" },
          { "name": "Automatico", "color": "gray" }
        ]
      }
    }
  }
}' "Propiedad Ejecutor en Testing"; then
  UPDATED=$((UPDATED + 1))
else
  FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 2.4: Relacion Backlog <-> Testing ---"
if notion_api PATCH "/databases/$BACKLOG_DB" '{
  "properties": {
    "Tests relacionados": {
      "relation": {
        "database_id": "'"$TEST_DB"'",
        "single_property": {}
      }
    }
  }
}' "Relacion Backlog-Testing"; then
  UPDATED=$((UPDATED + 1))
else
  FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 2.5: Poblar Fase en entradas del Backlog ---"
echo "  Obteniendo entradas del Backlog..."
BACKLOG_ENTRIES=$(curl -s -X POST "${NOTION_API}/databases/${BACKLOG_DB}/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: $NOTION_VERSION" \
  -H "Content-Type: application/json" \
  -d '{}')

# Extraer IDs y Gates, luego asignar Fase
echo "$BACKLOG_ENTRIES" | python3 -c "
import sys, json

data = json.load(sys.stdin)
gate_to_fase = {
    'G0-Tooling': 'F0-Plan',
    'G1-Texto': 'F1-MVP',
    'G2-Audio': 'F1-MVP',
    'G3-Demo': 'F3-Demo',
    'Infra': 'F2-Hardening'
}

for page in data.get('results', []):
    page_id = page['id']
    gate_prop = page.get('properties', {}).get('Gate', {}).get('select', {})
    gate_name = gate_prop.get('name', '') if gate_prop else ''
    fase = gate_to_fase.get(gate_name, 'F1-MVP')
    print(f'{page_id}|{gate_name}|{fase}')
" 2>/dev/null | while IFS='|' read -r PAGE_ID GATE FASE; do
  curl -s -o /dev/null -w "" -X PATCH "${NOTION_API}/pages/${PAGE_ID}" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: $NOTION_VERSION" \
    -H "Content-Type: application/json" \
    -d '{
      "properties": {
        "Fase": { "select": { "name": "'"$FASE"'" } }
      }
    }'
  echo "  Actualizado: Gate=$GATE -> Fase=$FASE (${PAGE_ID:0:8}...)"
  sleep 0.4  # Rate limiting
done

echo ""
echo "--- Paso 2.6: Poblar Categoria en KB Tramites ---"
KB_ENTRIES=$(curl -s -X POST "${NOTION_API}/databases/${KB_DB}/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: $NOTION_VERSION" \
  -H "Content-Type: application/json" \
  -d '{}')

echo "$KB_ENTRIES" | python3 -c "
import sys, json

data = json.load(sys.stdin)
tramite_to_cat = {
    'IMV': 'Prestaciones economicas',
    'Empadronamiento': 'Registro civil',
    'Tarjeta Sanitaria': 'Sanidad'
}

for page in data.get('results', []):
    page_id = page['id']
    title_arr = page.get('properties', {}).get('Tramite', {}).get('title', [])
    tramite = title_arr[0]['text']['content'] if title_arr else ''
    cat = tramite_to_cat.get(tramite, '')
    if cat:
        print(f'{page_id}|{tramite}|{cat}')
" 2>/dev/null | while IFS='|' read -r PAGE_ID TRAMITE CAT; do
  curl -s -o /dev/null -w "" -X PATCH "${NOTION_API}/pages/${PAGE_ID}" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: $NOTION_VERSION" \
    -H "Content-Type: application/json" \
    -d '{
      "properties": {
        "Categoria": { "select": { "name": "'"$CAT"'" } }
      }
    }'
  echo "  Actualizado: $TRAMITE -> Categoria=$CAT (${PAGE_ID:0:8}...)"
  sleep 0.4
done

# ============================================================
# FASE 3: POBLAR CONTENIDO
# ============================================================
echo ""
echo "=========================================="
echo "FASE 3: POBLAR CONTENIDO"
echo "=========================================="

if [ "$DASHBOARD_ID" != "FAIL" ]; then
  echo ""
  echo "--- Paso 3.1: Anadir bloques al Dashboard Home ---"
  notion_api PATCH "/blocks/$DASHBOARD_ID/children" '{
    "children": [
      {
        "object": "block", "type": "heading_2",
        "heading_2": { "rich_text": [{ "type": "text", "text": { "content": "Impacto Social" } }] }
      },
      {
        "object": "block", "type": "callout",
        "callout": {
          "icon": { "type": "emoji", "emoji": "💙" },
          "color": "blue_background",
          "rich_text": [{ "type": "text", "text": { "content": "3,2 millones de inmigrantes en Espana. 40% no completa tramites por barrera idiomatica. WhatsApp: 95% de penetracion. Coste: 0,002-0,01 EUR/consulta." } }]
        }
      }
    ]
  }' "Contenido adicional Dashboard" || FAILED=$((FAILED + 1))
fi

echo ""
echo "--- Paso 3.2: Anadir resumen cierre a Fase 3 ---"
notion_api PATCH "/blocks/$FASE3_PAGE/children" '{
  "children": [
    { "object": "block", "type": "divider", "divider": {} },
    {
      "object": "block", "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "🏁" },
        "color": "green_background",
        "rich_text": [{ "type": "text", "text": { "content": "Fase 3 COMPLETADA 2026-02-13. Twilio real, Deploy estable, 93/93 tests, logging JSON, 81 entradas Notion, Demo WOW 1+2, QA Deep audit PASS." } }]
      }
    }
  ]
}' "Resumen cierre Fase 3" || FAILED=$((FAILED + 1))

# ============================================================
# FASE 4: VERIFICACION
# ============================================================
echo ""
echo "=========================================="
echo "FASE 4: VERIFICACION"
echo "=========================================="

echo ""
echo "--- Verificar hijos de CivicAid OS ---"
notion_api GET "/blocks/$ROOT_PAGE/children" "" "Hijos de CivicAid OS"

echo ""
echo "--- Verificar entradas (conteo final) ---"
TOTAL=0
for DB_ID in "$BACKLOG_DB" "$KB_DB" "$TEST_DB"; do
  RESP=$(curl -s -X POST "${NOTION_API}/databases/${DB_ID}/query" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: $NOTION_VERSION" \
    -H "Content-Type: application/json" \
    -d '{}')
  COUNT=$(echo "$RESP" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('results',[])))" 2>/dev/null || echo "0")
  TOTAL=$((TOTAL + COUNT))
  echo "  DB ${DB_ID:0:8}...: $COUNT entradas"
done
echo "  TOTAL: $TOTAL entradas (esperado: 81)"

echo ""
echo "--- Buscar nuevas paginas ---"
for QUERY in "Dashboard Home" "Para Jueces" "Fases del Proyecto"; do
  RESP=$(curl -s -X POST "${NOTION_API}/search" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: $NOTION_VERSION" \
    -H "Content-Type: application/json" \
    -d '{"query": "'"$QUERY"'"}')
  FOUND=$(echo "$RESP" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('results',[])))" 2>/dev/null || echo "0")
  echo "  Busqueda '$QUERY': $FOUND resultados"
done

# ============================================================
# RESUMEN
# ============================================================
echo ""
echo "=========================================="
echo "RESUMEN"
echo "=========================================="
echo "Paginas creadas: $CREATED"
echo "DBs actualizadas: $UPDATED"
echo "Fallos: $FAILED"
echo ""
if [ "$FAILED" -eq 0 ]; then
  echo "RESULTADO: EXITO — Reestructuracion completada"
else
  echo "RESULTADO: PARCIAL — Revisar los fallos arriba"
fi
echo ""
echo "IDs de paginas creadas:"
echo "  Dashboard Home: $DASHBOARD_ID"
echo "  Para Jueces: $JUECES_ID"
echo "  Fases del Proyecto: $FASES_ID"
```

---

## Notas finales

### Orden de ejecucion

El plan esta disenado para ejecutarse secuencialmente. Cada fase depende de la anterior:

```
Fase 0 (Auditoria)
  |
  v  [Go/No-go]
Fase 1 (Crear estructura)
  |
  v  [IDs de nuevas paginas]
Fase 2 (Enriquecer DBs)
  |
  v  [Propiedades y datos poblados]
Fase 3 (Poblar contenido)
  |
  v  [Contenido en paginas]
Fase 4 (Verificacion)
  |
  v  [Checklist completada]
```

### Principios de operacion

1. **Nunca borrar, siempre archivar.** Si algo sale mal, usar `archived: true` en lugar de eliminar.
2. **Verificar despues de cada paso.** No acumular pasos sin confirmar que los anteriores funcionaron.
3. **Rate limiting.** No mas de 3 peticiones por segundo a la API de Notion. Espaciar con `sleep 0.4`.
4. **Idempotencia.** Los pasos de creacion de propiedades en DBs son idempotentes (la API hace upsert). Los pasos de creacion de paginas NO son idempotentes (crearian duplicados si se ejecutan dos veces).
5. **Fallback manual.** Si el MCP no expone una operacion necesaria, usar curl directo o la interfaz web de Notion.

### Mantenimiento post-reestructuracion

Despues de completar la reestructuracion:

1. Actualizar `docs/06-integrations/NOTION-OS.md` con los nuevos IDs de paginas creadas.
2. Anadir los nuevos IDs a la seccion "Paginas de Notion" del documento.
3. Verificar que el script `scripts/populate_notion.sh` sigue funcionando (no debe romper nada).
4. Crear las vistas manuales listadas en el Paso 2.7 desde Notion web.
5. Compartir las nuevas paginas con el equipo si es necesario.

---

## Referencias

- Documento Notion OS actual: `docs/06-integrations/NOTION-OS.md`
- Referencia MCP: `docs/06-integrations/MCP-TOOLS-REFERENCE.md`
- Script de poblacion: `scripts/populate_notion.sh`
- Configuracion MCP: `~/.mcp.json`
- API Notion (oficial): https://developers.notion.com
- Estado de fases: `docs/07-evidence/PHASE-STATUS.md`
- Resumen ejecutivo: `docs/00-EXECUTIVE-SUMMARY.md`
