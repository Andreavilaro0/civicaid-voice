# Referencia de Herramientas MCP — CivicAid Voice / Clara

> **Resumen en una linea:** Catalogo de servidores MCP utilizados en el proyecto, con configuracion, operaciones disponibles y ejemplos de uso practicos.

## Que es

MCP (Model Context Protocol) es el protocolo que permite a Claude Code interactuar con servicios externos como Notion, el sistema de archivos y GitHub. Cada servidor MCP expone un conjunto de herramientas que se pueden invocar directamente desde la conversacion con Claude Code.

## Para quien

- Desarrolladores que trabajan con Claude Code y necesitan interactuar con las bases de datos de Notion.
- El agente Notion Ops que gestiona el workspace CivicAid OS.
- Cualquier miembro del equipo que necesite automatizar operaciones sobre Notion, archivos o GitHub.

## Que incluye

- Lista de servidores MCP configurados: notionApi, filesystem, github.
- Para cada MCP: que hace, como se configura, operaciones disponibles y ejemplo de uso.
- Referencia al archivo de configuracion `~/.mcp.json`.

## Que NO incluye

- Tokens reales ni credenciales (solo referencias al archivo de configuracion).
- Servidores MCP de terceros no utilizados en el proyecto.
- Documentacion interna del protocolo MCP.

---

## Archivo de configuracion

Todos los servidores MCP se configuran en `~/.mcp.json`. Este archivo contiene las credenciales y la configuracion de arranque de cada servidor.

> **IMPORTANTE:** Nunca incluir tokens reales en documentacion ni en el repositorio. El archivo `~/.mcp.json` es local y no se versiona.

**Estructura general:**

```json
{
  "mcpServers": {
    "<nombre_servidor>": {
      "command": "<comando_de_arranque>",
      "args": ["<argumentos>"],
      "env": {
        "<VARIABLE>": "<valor>"
      }
    }
  }
}
```

Despues de modificar `~/.mcp.json`, es necesario **reiniciar Claude Code** para que los cambios surtan efecto.

---

## 1. notionApi — Servidor MCP de Notion

### Que hace

Proporciona acceso de lectura y escritura a las bases de datos y paginas del workspace de Notion **CivicAid OS**. Es el MCP principal del proyecto, utilizado para gestionar el Backlog, la KB de Tramites y los resultados de Testing.

### Configuracion

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

**Requisitos:**
- Node.js instalado (para `npx`).
- Token de integracion de Notion creado en [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations).
- La integracion debe tener acceso al workspace CivicAid OS.

### IDs de bases de datos

| Base de datos | Notion DB ID |
|---|---|
| Backlog / Issues | `304c5a0f-372a-81de-92a8-f54c03b391c0` |
| KB Tramites | `304c5a0f-372a-81ff-9d45-c785e69f7335` |
| Demo & Testing | `304c5a0f-372a-810d-8767-d77efbd46bb2` |

### Operaciones disponibles

| Operacion | Herramienta MCP | Descripcion |
|---|---|---|
| Buscar contenido | `mcp__notionApi__API-post-search` | Busca paginas y bases de datos por texto libre |
| Obtener base de datos | `mcp__notionApi__API-retrieve-a-database` | Recupera el schema y metadatos de una DB |
| Consultar base de datos | `mcp__notionApi__API-query-data-source` | Ejecuta consultas con filtros y ordenacion sobre una DB |
| Obtener pagina | `mcp__notionApi__API-retrieve-a-page` | Recupera las propiedades de una pagina |
| Crear pagina | `mcp__notionApi__API-post-page` | Crea una nueva pagina (fila) en una DB |
| Actualizar pagina | `mcp__notionApi__API-patch-page` | Modifica propiedades de una pagina existente |
| Obtener hijos de bloque | `mcp__notionApi__API-get-block-children` | Recupera el contenido interno de un bloque/pagina |
| Actualizar bloque | `mcp__notionApi__API-update-a-block` | Modifica el contenido de un bloque |
| Eliminar bloque | `mcp__notionApi__API-delete-a-block` | Marca un bloque como eliminado (archivado) |
| Obtener comentarios | `mcp__notionApi__API-retrieve-a-comment` | Lee los comentarios de una pagina |
| Crear comentario | `mcp__notionApi__API-create-a-comment` | Anade un comentario a una pagina |
| Obtener usuario actual | `mcp__notionApi__API-get-self` | Devuelve informacion del bot (integracion) |
| Listar usuarios | `mcp__notionApi__API-get-users` | Lista los usuarios del workspace |

### Ejemplos de uso

**Buscar entradas relacionadas con "IMV":**

```
Herramienta: mcp__notionApi__API-post-search
Parametros: {"query": "IMV"}
```

**Consultar todas las entradas del Backlog en estado "Hecho":**

```
Herramienta: mcp__notionApi__API-query-data-source
Parametros: {
  "database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0",
  "body": {
    "filter": {
      "property": "Estado",
      "select": {"equals": "Hecho"}
    }
  }
}
```

**Crear una nueva entrada en Demo & Testing:**

```
Herramienta: mcp__notionApi__API-post-page
Parametros: {
  "body": {
    "parent": {"database_id": "304c5a0f-372a-810d-8767-d77efbd46bb2"},
    "properties": {
      "Test": {"title": [{"text": {"content": "T11 — Nuevo test"}}]},
      "Tipo": {"select": {"name": "Golden test"}},
      "Resultado": {"select": {"name": "Pendiente"}},
      "Gate": {"select": {"name": "G1-Texto"}},
      "Fecha": {"date": {"start": "2026-02-12"}}
    }
  }
}
```

**Actualizar el estado de una tarea a "Hecho":**

```
Herramienta: mcp__notionApi__API-patch-page
Parametros: {
  "page_id": "<ID_DE_LA_PAGINA>",
  "body": {
    "properties": {
      "Estado": {"select": {"name": "Hecho"}}
    }
  }
}
```

---

## 2. filesystem — Servidor MCP del sistema de archivos

### Que hace

Proporciona acceso de lectura al sistema de archivos local. Permite a Claude Code explorar la estructura de directorios y leer archivos sin necesidad de usar comandos bash.

### Configuracion

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/<usuario>/Documents/hakaton/civicaid-voice"]
    }
  }
}
```

**Nota:** El ultimo argumento es la ruta raiz del proyecto. Solo se permiten operaciones dentro de esa ruta.

### Operaciones disponibles

| Operacion | Herramienta MCP | Descripcion |
|---|---|---|
| Listar directorio | `mcp__filesystem__list_directory` | Lista archivos y carpetas de un directorio |
| Leer archivo | `mcp__filesystem__read_file` | Lee el contenido de un archivo |
| Buscar archivos | `mcp__filesystem__search_files` | Busca archivos por patron en el nombre |

### Ejemplo de uso

**Listar la estructura de `src/core/`:**

```
Herramienta: mcp__filesystem__list_directory
Parametros: {"path": "src/core/"}
```

---

## 3. github — Servidor MCP de GitHub

### Que hace

Proporciona acceso a la API de GitHub para gestionar repositorios, issues, pull requests y acciones de CI/CD. Complementa el uso del CLI `gh` para operaciones que se realizan desde Claude Code.

### Configuracion

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "<TU_TOKEN_AQUI>"
      }
    }
  }
}
```

**Requisitos:**
- Token de acceso personal de GitHub (PAT) con permisos de lectura/escritura sobre el repositorio.
- Tambien se puede usar el CLI `gh` directamente como alternativa.

### Operaciones disponibles

| Operacion | Herramienta MCP | Descripcion |
|---|---|---|
| Obtener repositorio | Consulta de metadatos del repo | Informacion general del repositorio |
| Listar issues | Consulta de issues abiertas/cerradas | Gestion de incidencias |
| Crear issue | Creacion de nueva issue | Reporte de bugs o tareas |
| Obtener PR | Consulta de pull request | Revision de codigo |

> **Nota:** Para la mayoria de operaciones de GitHub en CivicAid Voice se prefiere el CLI `gh` (disponible en bash) por su mayor flexibilidad. El MCP de GitHub es complementario.

### Ejemplo de uso

**Alternativa recomendada via CLI:**

```bash
# Listar issues abiertas
gh issue list --repo civicaid-voice

# Ver detalles de un PR
gh pr view 1

# Crear una issue
gh issue create --title "Bug: ..." --body "Descripcion..."
```

---

## Resolucion de problemas comunes

### El servidor MCP no arranca

| Causa | Solucion |
|---|---|
| Node.js no instalado | Instalar Node.js v18+ |
| Token invalido o expirado | Regenerar token en la plataforma correspondiente |
| Archivo `~/.mcp.json` con formato JSON invalido | Validar con `python3 -m json.tool ~/.mcp.json` |
| Claude Code no detecta los cambios | Reiniciar Claude Code despues de modificar `~/.mcp.json` |

### Error "Unauthorized" al usar notionApi

| Causa | Solucion |
|---|---|
| Token de Notion expirado | Regenerar en [notion.so/my-integrations](https://www.notion.so/my-integrations) |
| Integracion sin acceso al workspace | Compartir las paginas/DBs con la integracion desde Notion |
| `OPENAPI_MCP_HEADERS` desactualizado | Actualizar ambas ocurrencias del token en `~/.mcp.json` |

---

## Como se verifica

| # | Verificacion | Como |
|---|---|---|
| 1 | notionApi funciona | Ejecutar busqueda MCP con `{"query": "CivicAid"}` y recibir resultados |
| 2 | Bases de datos accesibles | Consultar cada DB ID y obtener su schema |
| 3 | Escritura funciona | Crear una pagina de prueba y verificar en Notion web |
| 4 | `~/.mcp.json` valido | `python3 -m json.tool ~/.mcp.json` sin errores |

## Referencias

- Configuracion MCP: `~/.mcp.json`
- Notion OS: `docs/06-integrations/NOTION-OS.md`
- Documentacion MCP: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- API Notion: [https://developers.notion.com](https://developers.notion.com)
- Servidor MCP Notion: [https://www.npmjs.com/package/@notionhq/notion-mcp-server](https://www.npmjs.com/package/@notionhq/notion-mcp-server)
