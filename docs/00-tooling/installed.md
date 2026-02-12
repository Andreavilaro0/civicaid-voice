# Tooling Instalado — CivicAid Voice / Clara

> Ultima actualizacion: 2026-02-12

## MCPs Activos

| MCP | Ubicacion | Estado | Comando de instalacion |
|---|---|---|---|
| notionApi | ~/.mcp.json | ✅ Activo (token real) | `npx claude-code-templates@latest --mcp=productivity/notion --yes` |
| grafana | ~/.mcp.json | ⚠️ Configurado (sin token real) | `npx claude-code-templates@latest --mcp=devtools/grafana --yes` |
| playwright | ~/.claude/settings.json | ✅ Activo | Pre-instalado |
| filesystem | ~/.claude/settings.json | ✅ Activo | Pre-instalado |
| github | ~/.claude/settings.json | ⚠️ Sin GITHUB_PERSONAL_ACCESS_TOKEN | Pre-instalado |

## Skills (15)

| # | Skill | Carpeta | Estado |
|---|---|---|---|
| 1 | canvas-design | ~/.claude/skills/canvas-design/ | ✅ |
| 2 | docker-expert | ~/.claude/skills/docker-expert/ | ✅ |
| 3 | executing-plans | ~/.claude/skills/executing-plans/ | ✅ |
| 4 | github-actions-creator | ~/.claude/skills/github-actions-creator/ | ✅ |
| 5 | notion-knowledge-capture | ~/.claude/skills/notion-knowledge-capture/ | ✅ |
| 6 | notion-template-business | ~/.claude/skills/notion-template-business/ | ✅ |
| 7 | obsidian-markdown | ~/.claude/skills/obsidian-markdown/ | ✅ |
| 8 | python-patterns | ~/.claude/skills/python-patterns/ | ✅ |
| 9 | react-best-practices | ~/.claude/skills/react-best-practices/ | ✅ |
| 10 | render-deploy | ~/.claude/skills/render-deploy/ | ✅ |
| 11 | senior-fullstack | ~/.claude/skills/senior-fullstack/ | ✅ |
| 12 | twilio-communications | ~/.claude/skills/twilio-communications/ | ✅ |
| 13 | webapp-testing | ~/.claude/skills/webapp-testing/ | ✅ |
| 14 | whisper | ~/.claude/skills/whisper/ | ✅ |
| 15 | writing-plans | ~/.claude/skills/writing-plans/ | ✅ |

## Agents

### Globales (~/.claude/agents/)
| Agent | Archivo | Estado |
|---|---|---|
| devops-engineer | devops-engineer.md | ✅ |
| machine-learning-engineer | machine-learning-engineer.md | ✅ |
| connection-agent | connection-agent.md | ✅ |
| content-curator | content-curator.md | ✅ |
| frontend-developer | frontend-developer.md | ✅ |

### Proyecto (.claude/agents/)
| Agent | Archivo | Proposito |
|---|---|---|
| notion-ops | notion-ops.md | Gestion de Notion workspace + 3 DBs |
| ci-bot | ci-bot.md | GitHub Actions CI/CD |
| twilio-integrator | twilio-integrator.md | Twilio sandbox config + payloads |

## Notion Workspace

| Recurso | ID | Estado |
|---|---|---|
| CivicAid OS (pagina) | 304c5a0f372a801f995fce24036350ad | ✅ |
| Backlog/Issues DB | 304c5a0f-372a-81de-92a8-f54c03b391c0 | ✅ 14 tareas |
| KB Tramites DB | 304c5a0f-372a-81ff-9d45-c785e69f7335 | ✅ Schema creado |
| Demo & Testing DB | 304c5a0f-372a-810d-8767-d77efbd46bb2 | ✅ 10 tests |
| Phase Releases DB | Pendiente creacion | ⏳ |

## Pendiente

- [ ] GITHUB_PERSONAL_ACCESS_TOKEN en ~/.claude/settings.json
- [ ] Grafana service account token (nice-to-have)
- [ ] Phase Releases DB en Notion
