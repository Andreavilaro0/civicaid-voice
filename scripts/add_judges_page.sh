#!/bin/bash
# Add "Para Jueces — Evaluacion Rapida" page to Notion CivicAid OS workspace
# Usage: bash scripts/add_judges_page.sh

set -euo pipefail

echo "=== Adding Judges Evaluation Page to Notion ==="

# Extract token from ~/.mcp.json
if command -v jq &> /dev/null; then
  NOTION_TOKEN=$(cat ~/.mcp.json | jq -r '.mcpServers.notionApi.env.NOTION_TOKEN')
else
  echo "ERROR: jq not found. Please install jq or set NOTION_TOKEN manually."
  exit 1
fi

if [ -z "$NOTION_TOKEN" ] || [ "$NOTION_TOKEN" = "null" ]; then
  echo "ERROR: NOTION_TOKEN not found in ~/.mcp.json"
  exit 1
fi

PARENT_PAGE_ID="304c5a0f-372a-801f-995f-ce24036350ad"

echo "Creating page under parent: $PARENT_PAGE_ID"

RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
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
}')

# Check for errors
if echo "$RESPONSE" | grep -q '"object":"error"'; then
  echo "ERROR: Failed to create page"
  echo "$RESPONSE" | python3 -m json.tool
  exit 1
fi

PAGE_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "")

if [ -n "$PAGE_ID" ]; then
  echo "SUCCESS: Page created with ID: $PAGE_ID"
  echo "View at: https://www.notion.so/${PAGE_ID//-/}"
else
  echo "Page created but could not extract ID"
  echo "$RESPONSE" | python3 -m json.tool
fi
