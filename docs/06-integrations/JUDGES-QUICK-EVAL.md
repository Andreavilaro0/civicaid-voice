# Para Jueces — Evaluacion Rapida

> **Esta pagina resume CivicAid Voice / Clara en 2 minutos.**

## Que es Clara

Clara es un asistente WhatsApp que guia a personas vulnerables (inmigrantes, mayores, baja alfabetizacion) en tramites sociales en Espana. Responde por texto + audio en espanol y frances, usando solo informacion verificada de fuentes oficiales. No inventa, no alucina.

## Datos Clave

- **568 tests** (568 passed + 19 skipped + 5 xpassed) — `pytest tests/ -v`
- **26/26 quality gates** PASS (Fase 3 Q4 Production Hardening)
- **Fase 5 tono Clara**: amiga del ayuntamiento, patron E-V-I (Empatizar-Validar-Informar), sin emoji en ACKs
- **RAG pipeline** con hybrid BM25 + vector search — P@3 = 86%, 236 eval queries
- **Fallback chain**: PGVector -> JSON KB -> Directory (resiliente si DB cae)
- **Response cache** (LRU memory / Redis) para latencia <5ms en queries repetidas
- **Gemini TTS** (voz calida Sulafat) con fallback a gTTS
- **Vision** (Gemini 2.5 Flash) para documentos e imagenes, multilingual ES/FR
- 13 skills atomicos en el pipeline — `src/core/skills/`
- 50 feature flags con defaults seguros — `src/core/config.py`
- 8 tramites: IMV, Empadronamiento, Tarjeta Sanitaria, NIE/TIE, Desempleo, etc.
- 2 idiomas: Espanol + Frances — `detect_lang.py`
- Deploy: Render (Docker, free tier) — `curl /health`
- Admin API: `/admin/rag-metrics`, `/admin/staleness`, `/admin/satisfaction`

## Donde Verificar

- **Tests:** `pytest tests/ -v --tb=short` → 568 passed, 0 failed
- **Lint:** `ruff check src/ tests/ scripts/ --select E,F,W --ignore E501` → 0 errores
- **Health:** `curl localhost:5000/health` → JSON status: healthy
- **Docker RAG:** `docker compose up -d && python scripts/init_db.py` → PostgreSQL + pgvector
- **Ingestion:** `python scripts/run_ingestion.py --all --dry-run` → 8 tramites listados
- **Drift:** `python scripts/check_drift.py --all` → 8 procedures verificados
- **RAG Eval:** `python scripts/run_rag_eval.py` → P@3 >= 85% sobre 236 queries
- **Admin:** `curl -H "Authorization: Bearer $ADMIN_TOKEN" localhost:5000/admin/rag-metrics`

## Demo en Vivo — Momentos WOW

**WOW 1 — Texto Espanol:** Enviar 'Necesito ayuda con el IMV' por WhatsApp. Clara responde en <3s con guia paso a paso + audio.

**WOW 2 — Audio Frances:** Enviar nota de voz en frances preguntando por empadronamiento. Clara transcribe, detecta idioma, responde en frances con texto + audio.

**WOW 3 — Foto de Documento:** Enviar foto de una carta administrativa. Clara la analiza con Gemini Vision, identifica el tramite, y explica los pasos en lenguaje sencillo.

## Equipo

Robert (Backend lead, pipeline, demo) | Marcos (Routes, Twilio, deploy) | Lucas (KB, testing) | Daniel (Web, video) | Andrea (Notion, slides, coordination)

---

*Hackathon OdiseIA4Good — UDIT | Febrero 2026*

## Como Agregar Esta Pagina a Notion

### Opcion 1: Manualmente

1. Ir a la pagina raiz "CivicAid OS" en Notion: `https://www.notion.so/CivicAid-OS-304c5a0f372a801f995fce24036350ad`
2. Click en "+ New Page" dentro de esa pagina
3. Titulo: "Para Jueces — Evaluacion Rapida"
4. Copiar y pegar el contenido de arriba (Notion reconoce markdown)

### Opcion 2: Via Script (requiere jq instalado)

```bash
#!/bin/bash
# Agregar pagina "Para Jueces" al workspace CivicAid OS

NOTION_TOKEN=$(cat ~/.mcp.json | jq -r '.mcpServers.notionApi.env.NOTION_TOKEN')
PARENT_PAGE_ID="304c5a0f-372a-801f-995f-ce24036350ad"

curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
  "parent": {"page_id": "'"$PARENT_PAGE_ID"'"},
  "properties": {
    "title": {
      "title": [{"text": {"content": "Para Jueces — Evaluacion Rapida"}}]
    }
  },
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{
          "type": "text",
          "text": {"content": "Esta pagina resume CivicAid Voice / Clara en 2 minutos."},
          "annotations": {"bold": true}
        }]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Que es Clara"}}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{
          "text": {
            "content": "Clara es un asistente WhatsApp que guia a personas vulnerables (inmigrantes, mayores, baja alfabetizacion) en tramites sociales en Espana. Responde por texto + audio en espanol y frances, usando solo informacion verificada de fuentes oficiales. No inventa, no alucina."
          }
        }]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Datos Clave"}}]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "96 tests automatizados (91 passed + 5 xpassed) — pytest tests/ -v"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "11 skills atomicos en el pipeline — src/core/skills/"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "9 feature flags con defaults seguros — src/core/config.py"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "3 tramites: IMV, Empadronamiento, Tarjeta Sanitaria — data/tramites/"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "2 idiomas: Espanol + Frances — detect_lang.py"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "81 entries Notion: 43 Backlog + 12 KB + 26 Testing"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "Deploy: Render (Docker, free tier) — curl /health"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "Latencia cache HIT: ~2 segundos"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "22/22 gates PASS (Fases 0-3)"}
        }]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Donde Verificar"}}]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "Tests: pytest tests/ -v --tb=short → 96 passed (0 failed)"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "Lint: ruff check src/ tests/ → 0 errores"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "Health: curl localhost:5000/health → JSON status: healthy"}
        }]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{
          "text": {"content": "Docker: docker build -t civicaid . → Build exitoso"}
        }]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Demo en Vivo — Momentos WOW"}}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [
          {
            "text": {"content": "WOW 1 — Texto Espanol:"},
            "annotations": {"bold": true}
          },
          {
            "text": {"content": " Enviar '\''Necesito ayuda con el IMV'\'' por WhatsApp. Clara responde en <3s con guia paso a paso + audio."}
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
            "text": {"content": "WOW 2 — Audio Frances:"},
            "annotations": {"bold": true}
          },
          {
            "text": {"content": " Enviar nota de voz en frances preguntando por empadronamiento. Clara transcribe, detecta idioma, responde en frances con texto + audio."}
          }
        ]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Equipo"}}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{
          "text": {"content": "Robert (Backend lead, pipeline, demo) | Marcos (Routes, Twilio, deploy) | Lucas (KB, testing) | Daniel (Web, video) | Andrea (Notion, slides, coordination)"}
        }]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{
          "text": {"content": "Hackathon OdiseIA4Good — UDIT | Febrero 2026"},
          "annotations": {"italic": true}
        }]
      }
    }
  ]
}'
```

Save this script as `scripts/add_judges_page.sh` and make it executable with `chmod +x scripts/add_judges_page.sh`.
