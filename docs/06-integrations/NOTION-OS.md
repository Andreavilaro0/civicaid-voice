# NOTION OS — CivicAid Voice / Clara

> **Source of Truth** for project management, knowledge base, and test evidence.
> Every task, tramite, and test result lives here. If it's not in Notion, it didn't happen.

| Key | Value |
|---|---|
| **Workspace** | CivicAid OS |
| **Databases** | 3 (Backlog, KB Tramites, Demo & Testing) |
| **MCP** | `@notionhq/notion-mcp-server` via `~/.mcp.json` |
| **Token status** | BLOCKED — placeholder `ntn_****` (8 chars), needs regeneration |
| **Populate script** | `bash scripts/populate_notion.sh` (33 entries staged) |
| **Last verified** | 2026-02-12 |

---

## 0. How to Navigate (for third parties)

Welcome, judges and reviewers. Here's how to find what you need:

| You want to... | Go to... |
|---|---|
| See project progress | **Backlog / Issues** → Kanban by Estado |
| Understand what Clara knows | **KB Tramites** → Table by Tramite |
| Review test results | **Demo & Testing** → Board by Gate |
| Check a specific gate | Filter any DB by `Gate = G1-Texto` / `G2-Audio` / `G3-Demo` |
| See who owns what | **Backlog** → filter by `Owner` (Select field) |
| Find blockers | **Backlog** → filter `Estado = Bloqueado` |

**Quick links** (once populated):
- Backlog DB: `https://notion.so/304c5a0f372a81de92a8f54c03b391c0`
- KB Tramites DB: `https://notion.so/304c5a0f372a81ff9d45c785e69f7335`
- Testing DB: `https://notion.so/304c5a0f372a810d8767d77efbd46bb2`

---

## 1. Bases de Datos

### 1.1 Backlog / Issues

**Notion DB ID:** `304c5a0f-372a-81de-92a8-f54c03b391c0`

Sprint board for all tasks, issues, and deliverables.

| Propiedad | Tipo | Valores / Descripcion |
|---|---|---|
| **Titulo** | Title | Nombre descriptivo de la tarea |
| **Estado** | Select | `Backlog`, `En progreso`, `En review`, `Hecho`, `Bloqueado` |
| **Gate** | Select | `G0-Tooling`, `G1-Texto`, `G2-Audio`, `G3-Demo`, `Infra` |
| **Owner** | Select | `Robert`, `Marcos`, `Daniel`, `Andrea`, `Lucas` |
| **Prioridad** | Select | `P0-demo`, `P1`, `P2` |
| **Horas est.** | Number | 0.5 to 8 |
| **DoD** | Rich Text | Definition of Done — acceptance criteria |
| **Depende de** | Rich Text | Task IDs this depends on (e.g. "D1.1, D1.3") |
| **GitHub Issue** | URL | Link to corresponding GitHub issue |
| **Dia** | Select | `Dia 1`, `Dia 2`, `Dia 3` |

> **Workaround — Owner field:** Notion API `Person` type requires user IDs which are workspace-specific and hard to automate. We use `Select` with team member names instead. Functionally equivalent for filtering and Kanban grouping.

> **Workaround — Depende de field:** Notion API `Relation` type requires page IDs that don't exist until pages are created. We use `Rich Text` with task title references (e.g. "D1.1: Setup MCP") to express dependencies without circular creation issues. Can be upgraded to Relation after initial population.

**Estado values:**

| Estado | Meaning | Color |
|---|---|---|
| `Backlog` | Identified, not prioritized | Grey |
| `En progreso` | Active development | Yellow |
| `En review` | Pending review | Orange |
| `Hecho` | Completed and verified | Green |
| `Bloqueado` | Blocked by dependency | Red |

---

### 1.2 KB Tramites

**Notion DB ID:** `304c5a0f-372a-81ff-9d45-c785e69f7335`

Verified knowledge base for Spanish administrative procedures. **This is the source of truth that Clara uses to answer users.**

| Propiedad | Tipo | Valores / Descripcion |
|---|---|---|
| **Tramite** | Title | Tramite name (IMV, Empadronamiento, Tarjeta Sanitaria) |
| **Campo** | Select | `Descripcion`, `Requisitos`, `Documentos`, `Pasos` |
| **Valor** | Rich Text | Information content for this field |
| **Fuente URL** | URL | Official government source URL |
| **Organismo** | Select | `Seguridad Social`, `Ayuntamiento Madrid`, `Comunidad de Madrid` |
| **Estado** | Select | `Verificado`, `Pendiente`, `Desactualizado` |
| **Fecha verificacion** | Date | Last verification date |
| **Notas** | Rich Text | Internal notes, exceptions, edge cases |

**Coverage (3 tramites x 4 campos = 12 entries):**

| Tramite | Organismo | Campos | Estado |
|---|---|---|---|
| IMV | Seguridad Social | Descripcion, Requisitos, Documentos, Pasos | Verificado |
| Empadronamiento | Ayuntamiento Madrid | Descripcion, Requisitos, Documentos, Pasos | Verificado |
| Tarjeta Sanitaria | Comunidad de Madrid | Descripcion, Requisitos, Documentos, Pasos | Verificado |

---

### 1.3 Demo & Testing

**Notion DB ID:** `304c5a0f-372a-810d-8767-d77efbd46bb2`

Test execution log. Each row = one test run. Never overwrite — always create new rows.

| Propiedad | Tipo | Valores / Descripcion |
|---|---|---|
| **Test** | Title | Test ID (T1, T2, ..., T10) |
| **Tipo** | Select | `Golden test`, `Edge case`, `Demo rehearsal`, `Latencia` |
| **Input** | Rich Text | Exact test input |
| **Output esperado** | Rich Text | Expected output |
| **Output real** | Rich Text | Actual output |
| **Latencia (ms)** | Number | Response time in milliseconds |
| **Resultado** | Select | `Pasa`, `Falla`, `Pendiente` |
| **Gate** | Select | `G1-Texto`, `G2-Audio`, `G3-Demo` |
| **Fecha** | Date | Execution date |
| **Notas** | Rich Text | Observations, error logs |

**Test coverage (10 golden tests):**

| Test | Gate | What it validates |
|---|---|---|
| T1 | G1-Texto | Cache match — exact keyword |
| T2 | G1-Texto | Cache miss — no match |
| T3 | G1-Texto | Cache match — image type |
| T4 | G1-Texto | KB lookup — empadronamiento |
| T5 | G1-Texto | Language detection — French |
| T6 | G2-Audio | Webhook parse — text message |
| T7 | G2-Audio | Webhook parse — audio message |
| T8 | G2-Audio | Pipeline — text stub E2E |
| T9 | G2-Audio | WA text demo E2E |
| T10 | G2-Audio | WA audio demo stub E2E |

---

## 2. Vistas

### Backlog Views

| Vista | Tipo | Group by | Filtro |
|---|---|---|---|
| **Kanban por Estado** | Board | Estado | Ocultar Hecho > 7 dias |
| **Board por Gate** | Board | Gate | Solo Estado != Hecho |
| **Table por Owner** | Table | Owner | Todas |
| **Calendar por Dia** | Calendar | Dia | Solo con Dia asignado |

### KB Tramites Views

| Vista | Tipo | Filtro |
|---|---|---|
| **All Tramites** | Table | Ninguno |
| **Pendiente** | Table | Estado = Pendiente |
| **Verificado** | Table | Estado = Verificado |

### Demo & Testing Views

| Vista | Tipo | Group by / Filtro |
|---|---|---|
| **Board por Gate** | Board | Group: Gate |
| **Fallos** | Table | Resultado = Falla |
| **Demo rehearsal** | Table | Tipo = Demo rehearsal |

---

## 3. MCP Integration

### Token Configuration

**File:** `~/.mcp.json`

```json
{
  "mcpServers": {
    "notionApi": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_REAL_TOKEN_HERE",
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ntn_REAL_TOKEN_HERE\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

### Database IDs (Reference)

| Database | Notion DB ID |
|---|---|
| **Backlog / Issues** | `304c5a0f-372a-81de-92a8-f54c03b391c0` |
| **KB Tramites** | `304c5a0f-372a-81ff-9d45-c785e69f7335` |
| **Demo & Testing** | `304c5a0f-372a-810d-8767-d77efbd46bb2` |

### Available MCP Operations

| Operation | MCP Tool | Example |
|---|---|---|
| Search | `mcp__notionApi__API-post-search` | `{"query": "IMV"}` |
| Retrieve DB | `mcp__notionApi__API-retrieve-a-database` | `{database_id: "304c5a0f..."}` |
| Query DB | `mcp__notionApi__API-post-database-query` | `{database_id: "...", body: {filter: ...}}` |
| Create page | `mcp__notionApi__API-post-page` | `{body: {parent: ..., properties: ...}}` |
| Update page | `mcp__notionApi__API-patch-page` | `{page_id: "...", body: {properties: ...}}` |

---

## 4. Population Status (2026-02-12)

### BLOCKER: Token Invalid

```
Token: ntn_**** (8 chars — placeholder, not a real token)
API response: 401 Unauthorized
All read/write operations fail until token is regenerated.
```

### To Unblock

```bash
# 1. Go to https://www.notion.so/my-integrations
# 2. Select "CivicAid Clara" integration
# 3. Regenerate the Internal Integration Secret
# 4. Update in ~/.mcp.json (both NOTION_TOKEN and OPENAPI_MCP_HEADERS)
# 5. Restart Claude Code
# 6. Run:
bash scripts/populate_notion.sh
```

### Manual curl Commands (if MCP still fails)

```bash
# Verify token
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" | python3 -m json.tool

# Retrieve Backlog DB schema
curl -s "https://api.notion.com/v1/databases/304c5a0f-372a-81de-92a8-f54c03b391c0" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" | python3 -m json.tool

# Query all Backlog entries
curl -s -X POST "https://api.notion.com/v1/databases/304c5a0f-372a-81de-92a8-f54c03b391c0/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

# Create a single Backlog entry (example)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "304c5a0f-372a-81de-92a8-f54c03b391c0"},
    "properties": {
      "Titulo": {"title": [{"text": {"content": "Test entry"}}]},
      "Estado": {"select": {"name": "Backlog"}},
      "Gate": {"select": {"name": "G0-Tooling"}},
      "Prioridad": {"select": {"name": "P2"}}
    }
  }'

# Search across all shared pages
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "CivicAid"}'
```

### Staged Data Summary

| Database | Entries | Status |
|---|---|---|
| Backlog / Issues | 11 staged | Pending — token invalid |
| KB Tramites | 12 staged | Pending — token invalid |
| Demo & Testing | 10 staged | Pending — token invalid |
| **Total** | **33 staged** | **Ready in `scripts/populate_notion.sh`** |

---

## 5. Staged Entries (Full Reference)

### Backlog (11 entries)

| # | Titulo | Estado | Gate | Owner | Prioridad | Dia |
|---|---|---|---|---|---|---|
| D1.1 | Setup MCP + skills + agents | Hecho | G0-Tooling | — | P0-demo | Dia 1 |
| D1.2 | Crear Notion CivicAid OS (3 DBs) | Hecho | G0-Tooling | — | P0-demo | Dia 1 |
| D1.3 | Implementar cache-first con 8 entries + MP3 | Hecho | G1-Texto | — | P0-demo | Dia 1 |
| D1.4 | Cargar KB con 3 tramites verificados | Hecho | G1-Texto | — | P0-demo | Dia 1 |
| D1.5 | Implementar deteccion de idioma | Hecho | G1-Texto | — | P1 | Dia 1 |
| D1.6 | Implementar /webhook para Twilio WA | Hecho | G2-Audio | — | P0-demo | Dia 1 |
| D1.7 | Pipeline orquestador (texto + audio + fallback) | Hecho | G2-Audio | — | P0-demo | Dia 1 |
| D1.8 | Integrar Whisper con timeout y OGG-WAV | Hecho | G2-Audio | — | P0-demo | Dia 1 |
| D2.1 | Dockerfile + render.yaml + CI workflow | En progreso | Infra | — | P0-demo | Dia 2 |
| D2.2 | Deploy a Render + configurar Twilio webhook | Backlog | Infra | — | P0-demo | Dia 2 |
| D3.1 | Demo rehearsal + video backup + screenshots | Backlog | G3-Demo | — | P0-demo | Dia 3 |

### KB Tramites (12 entries)

| Tramite | Campo | Organismo | Estado | Fuente |
|---|---|---|---|---|
| IMV | Descripcion | Seguridad Social | Verificado | seg-social.es |
| IMV | Requisitos | Seguridad Social | Verificado | seg-social.es |
| IMV | Documentos | Seguridad Social | Verificado | seg-social.es |
| IMV | Pasos | Seguridad Social | Verificado | seg-social.es |
| Empadronamiento | Descripcion | Ayuntamiento Madrid | Verificado | madrid.es |
| Empadronamiento | Requisitos | Ayuntamiento Madrid | Verificado | madrid.es |
| Empadronamiento | Documentos | Ayuntamiento Madrid | Verificado | madrid.es |
| Empadronamiento | Pasos | Ayuntamiento Madrid | Verificado | madrid.es |
| Tarjeta Sanitaria | Descripcion | Comunidad de Madrid | Verificado | comunidad.madrid |
| Tarjeta Sanitaria | Requisitos | Comunidad de Madrid | Verificado | comunidad.madrid |
| Tarjeta Sanitaria | Documentos | Comunidad de Madrid | Verificado | comunidad.madrid |
| Tarjeta Sanitaria | Pasos | Comunidad de Madrid | Verificado | comunidad.madrid |

### Demo & Testing (10 entries)

| Test | Tipo | Gate | Input (summary) | Resultado |
|---|---|---|---|---|
| T1 — Cache Match Keyword Exacto | Golden test | G1-Texto | "Que es el IMV?" | Pasa |
| T2 — Cache Match Sin Match | Golden test | G1-Texto | "Que tiempo hace?" | Pasa |
| T3 — Cache Match Imagen Demo | Golden test | G1-Texto | IMAGE type message | Pasa |
| T4 — KB Lookup Empadronamiento | Golden test | G1-Texto | "necesito empadronarme" | Pasa |
| T5 — Detect Language Frances | Golden test | G1-Texto | "Bonjour, comment faire?" | Pasa |
| T6 — Webhook Parse Text | Golden test | G2-Audio | POST Body=Hola, NumMedia=0 | Pasa |
| T7 — Webhook Parse Audio | Golden test | G2-Audio | POST NumMedia=1, audio/ogg | Pasa |
| T8 — Pipeline Text Stub | Golden test | G2-Audio | IncomingMessage "Que es el IMV?" | Pasa |
| T9 — WA Text Demo E2E | Golden test | G2-Audio | POST /webhook "Que es el IMV?" | Pasa |
| T10 — WA Audio Demo Stub E2E | Golden test | G2-Audio | POST /webhook audio/ogg stub | Pasa |

---

## 6. Rules

1. **Never delete records** — mark as `Hecho` or `Desactualizado` instead.
2. **One row per test execution** — never overwrite previous results.
3. **Link GitHub Issues** — every Backlog task should reference its GH issue.
4. **Verify KB periodically** — check `Fecha verificacion` for stale data.
5. **Use Depende de** — write task IDs (e.g. "D1.1, D1.3") to express dependencies.
6. **Owner = Select** — use team member names, not Notion Person IDs.
7. **Notion is Source of Truth** — local files mirror Notion, not the other way around.

---

## 7. Daily Routine

### Start of Day
1. Review Kanban → check `En progreso` and `Bloqueado` items.
2. Move tasks from `Backlog` to `En progreso` by priority.
3. Check `Depende de` for blocked items.

### During Development
4. Update `Estado` when starting work.
5. Log blockers immediately → `Bloqueado` + note.
6. After tests → create rows in Demo & Testing with `Output real`, `Latencia`, `Resultado`.

### End of Day
7. Move completed items to `Hecho`.
8. Push any new test results to Demo & Testing.
9. Prepare next day's priorities.

---

> **Last updated:** 2026-02-12 — Token still blocked. 33 entries staged in `scripts/populate_notion.sh`. Run script after token regeneration.
