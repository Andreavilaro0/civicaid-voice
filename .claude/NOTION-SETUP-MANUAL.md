# Notion Setup Manual — CivicAid OS

> Usar esta guia si el MCP de Notion no esta conectado (token pendiente).
> Cuando el token este listo, el subagent `notion-ops` puede automatizar todo esto.

---

## PASO 1: Crear la Integracion en Notion

1. Ir a https://www.notion.so/my-integrations
2. Click "New integration"
3. Nombre: `CivicAid Clara`
4. Logo: (opcional)
5. Associated workspace: seleccionar tu workspace
6. Capabilities: marcar "Read content", "Update content", "Insert content"
7. Click "Submit"
8. **Copiar el "Internal Integration Secret"** (empieza con `ntn_`)

## PASO 2: Configurar el Token

Pegar el token en 3 lugares:

```bash
# 1. En .env del proyecto
NOTION_TOKEN=ntn_XXXXXXXXXXXXXXXXXXXXXXXX

# 2. En ~/.mcp.json → notionApi → env → NOTION_TOKEN
# Editar: ~/.mcp.json
"NOTION_TOKEN": "ntn_XXXXXXXXXXXXXXXXXXXXXXXX"

# 3. En ~/.claude/settings.json → notion → env → OPENAPI_MCP_HEADERS
# Reemplazar NOTION_TOKEN_AQUI por el token real
```

## PASO 3: Crear la Pagina Principal

1. En Notion, crear nueva pagina: **"CivicAid OS"**
2. Compartir la pagina con la integracion:
   - Click "Share" (arriba derecha)
   - "Invite" → buscar "CivicAid Clara" → seleccionar
   - Permiso: "Can edit"

## PASO 4: Crear DB A — "Backlog / Issues"

Dentro de "CivicAid OS", crear Database - Full page:

| Propiedad | Tipo | Opciones |
|---|---|---|
| Titulo | Title | (default) |
| Estado | Select | `Backlog`, `En progreso`, `En review`, `Hecho`, `Bloqueado` |
| Gate | Select | `G0-Tooling`, `G1-Texto`, `G2-Audio`, `G3-Demo`, `Infra` |
| Owner | Person | (asignar del workspace) |
| Prioridad | Select | `P0-demo`, `P1`, `P2` |
| Horas est. | Number | formato: numero |
| DoD | Rich Text | (default) |
| Depende de | Relation | relacion a esta misma DB |
| GitHub Issue | URL | (default) |
| Dia | Select | `Dia 1`, `Dia 2`, `Dia 3` |

**Vistas a crear:**
1. "Kanban por Estado" → Board view, group by Estado
2. "Por Gate" → Board view, group by Gate
3. "Por Persona" → Table view, filter by Owner
4. "Timeline" → Calendar view, by Dia

## PASO 5: Crear DB B — "KB Tramites"

| Propiedad | Tipo | Opciones |
|---|---|---|
| Tramite | Title | (default) |
| Campo | Text | (default) |
| Valor | Rich Text | (default) |
| Fuente URL | URL | (default) |
| Organismo | Select | `Seguridad Social`, `Ayuntamiento Madrid`, `Comunidad de Madrid` |
| Estado | Select | `Verificado`, `Pendiente`, `Desactualizado` |
| Fecha verificacion | Date | (default) |
| Notas | Rich Text | (default) |

**Vistas:**
1. "Por Tramite" → Table, group by Tramite
2. "Pendientes" → Table, filter Estado = Pendiente
3. "Verificado" → Table, filter Estado = Verificado

## PASO 6: Crear DB C — "Demo & Testing"

| Propiedad | Tipo | Opciones |
|---|---|---|
| Test | Title | (default) |
| Tipo | Select | `Golden test`, `Edge case`, `Demo rehearsal`, `Latencia` |
| Input | Rich Text | (default) |
| Output esperado | Rich Text | (default) |
| Output real | Rich Text | (default) |
| Latencia (ms) | Number | formato: numero |
| Resultado | Select | `Pasa`, `Falla`, `Pendiente` |
| Gate | Select | `G1-Texto`, `G2-Audio`, `G3-Demo` |
| Fecha | Date | (default) |
| Notas | Rich Text | (default) |

**Vistas:**
1. "Por Gate" → Board, group by Gate
2. "Solo fallos" → Table, filter Resultado = Falla
3. "Demo Rehearsal" → Table, filter Tipo = Demo rehearsal

## PASO 7: Guardar los Database IDs

Para cada DB creada:
1. Abrir la DB en Notion (pagina completa)
2. Copiar la URL del navegador
3. El ID es la cadena de 32 caracteres hex despues del ultimo `/` y antes del `?`
   Ejemplo: `https://notion.so/CivicAid-OS/abc123def456...` → ID = `abc123def456...`
4. Pegar en `.env`:
   ```
   NOTION_DATABASE_ID_BACKLOG=abc123...
   NOTION_DATABASE_ID_KB=def456...
   NOTION_DATABASE_ID_TESTING=ghi789...
   ```
5. Pegar en `.claude/project-settings.json` en los campos "id" correspondientes

## PASO 8: Verificar Conexion MCP

Reiniciar Claude Code y ejecutar:
```
"Lista las bases de datos disponibles en mi Notion"
```

Si el MCP responde con las 3 DBs, la conexion funciona.
Si da error de autenticacion, verificar que el token es correcto y la pagina esta compartida con la integracion.

## PASO 9: Cargar Datos Iniciales

Una vez conectado, usar el subagent `notion-ops` para:
1. Popular DB Backlog con las tareas de FASE 1 (D1.1 a D3.12)
2. Popular DB KB con los datos de tramites verificados
3. Popular DB Testing con los 10 tests definidos (T1 a T10)
