#!/usr/bin/env bash
# populate_notion.sh — Populates the 3 CivicAid OS Notion databases
# Usage: bash scripts/populate_notion.sh
# Requires: NOTION_TOKEN in ~/.mcp.json or as env var

set -euo pipefail

# --- Extract token ---
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

# --- Verify token ---
echo "Verifying Notion API token..."
VERIFY=$(curl -s -o /dev/null -w "%{http_code}" \
  "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28")

if [ "$VERIFY" != "200" ]; then
  echo "ERROR: Notion API returned HTTP $VERIFY. Token is invalid."
  echo "Fix: Go to https://www.notion.so/my-integrations and regenerate the token."
  exit 1
fi
echo "Token OK."

# --- Database IDs ---
BACKLOG_DB="304c5a0f-372a-81de-92a8-f54c03b391c0"
KB_DB="304c5a0f-372a-81ff-9d45-c785e69f7335"
TEST_DB="304c5a0f-372a-810d-8767-d77efbd46bb2"

CREATED=0
FAILED=0

create_page() {
  local db_id="$1"
  local label="$2"
  local json_body="$3"

  RESP=$(curl -s -w "\n%{http_code}" -X POST "https://api.notion.com/v1/pages" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d "$json_body")

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" = "200" ]; then
    PAGE_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'][:8])" 2>/dev/null || echo "???")
    echo "  OK [$PAGE_ID] $label"
    CREATED=$((CREATED + 1))
  else
    echo "  FAIL ($HTTP_CODE) $label"
    FAILED=$((FAILED + 1))
  fi
}

# ============================================================
# BACKLOG (11 entries)
# ============================================================
echo ""
echo "=== Populating Backlog / Issues (11 entries) ==="

create_page "$BACKLOG_DB" "G0: Setup MCP + skills + agents" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Setup MCP + skills + agents"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G0-Tooling"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 2},
    "DoD": {"rich_text": [{"text": {"content": "15 skills, 8 agents, MCPs instalados"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G0: Crear Notion CivicAid OS" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Crear Notion CivicAid OS (3 DBs)"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G0-Tooling"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 1},
    "DoD": {"rich_text": [{"text": {"content": "3 databases creadas con schemas completos"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G1: Cache-first" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Implementar cache-first con 8 entries + MP3"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G1-Texto"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 3},
    "DoD": {"rich_text": [{"text": {"content": "Cache match funciona, 6 MP3 generados, tests T1-T3 pasan"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G1: KB Tramites" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Cargar KB con 3 tramites verificados"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G1-Texto"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 2},
    "DoD": {"rich_text": [{"text": {"content": "IMV, Empadronamiento, Tarjeta Sanitaria en JSON + test T4 pasa"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G1: Language detection" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Implementar deteccion de idioma"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G1-Texto"}},
    "Prioridad": {"select": {"name": "P1"}},
    "Horas est.": {"number": 1},
    "DoD": {"rich_text": [{"text": {"content": "Detecta ES, FR, EN, AR. Test T5 pasa"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G2: Webhook endpoint" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Implementar /webhook para Twilio WA"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G2-Audio"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 2},
    "DoD": {"rich_text": [{"text": {"content": "Parsea texto y audio correctamente. Tests T6-T7 pasan"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G2: Pipeline orchestrator" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Pipeline orquestador (texto + audio + fallback)"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G2-Audio"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 4},
    "DoD": {"rich_text": [{"text": {"content": "Pipeline completo con audio+text+fallback flows. Test T8 pasa"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "G2: Whisper integration" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Integrar Whisper con timeout y OGG-WAV"}}]},
    "Estado": {"select": {"name": "Hecho"}},
    "Gate": {"select": {"name": "G2-Audio"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 2},
    "DoD": {"rich_text": [{"text": {"content": "ThreadPoolExecutor + WHISPER_TIMEOUT, pydub lazy import"}}]},
    "Dia": {"select": {"name": "Dia 1"}}
  }
}'

create_page "$BACKLOG_DB" "Infra: Docker + Render + CI" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Dockerfile + render.yaml + CI workflow"}}]},
    "Estado": {"select": {"name": "En progreso"}},
    "Gate": {"select": {"name": "Infra"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 2},
    "DoD": {"rich_text": [{"text": {"content": "Docker build OK, render.yaml creado, CI pendiente verificar"}}]},
    "Dia": {"select": {"name": "Dia 2"}}
  }
}'

create_page "$BACKLOG_DB" "Infra: Deploy Render" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Deploy a Render + configurar Twilio webhook"}}]},
    "Estado": {"select": {"name": "Backlog"}},
    "Gate": {"select": {"name": "Infra"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 1},
    "DoD": {"rich_text": [{"text": {"content": "Render deploy OK, Twilio webhook apunta a URL real, /health 200"}}]},
    "Dia": {"select": {"name": "Dia 2"}}
  }
}'

create_page "$BACKLOG_DB" "G3: Demo rehearsal" '{
  "parent": {"database_id": "'"$BACKLOG_DB"'"},
  "properties": {
    "Titulo": {"title": [{"text": {"content": "Demo rehearsal + video backup + screenshots"}}]},
    "Estado": {"select": {"name": "Backlog"}},
    "Gate": {"select": {"name": "G3-Demo"}},
    "Prioridad": {"select": {"name": "P0-demo"}},
    "Horas est.": {"number": 2},
    "DoD": {"rich_text": [{"text": {"content": "Rehearsal completado, video grabado, screenshots listos"}}]},
    "Dia": {"select": {"name": "Dia 3"}}
  }
}'

# ============================================================
# KB TRAMITES (12 entries)
# ============================================================
echo ""
echo "=== Populating KB Tramites (12 entries) ==="

# IMV
for CAMPO in Descripcion Requisitos Documentos Pasos; do
  case $CAMPO in
    Descripcion) VALOR="Prestacion economica dirigida a prevenir el riesgo de pobreza y exclusion social. Cuantia: 604-1148 EUR/mes segun unidad familiar." ;;
    Requisitos) VALOR="23-65 anos. Residencia legal en Espana 1 ano. Vulnerabilidad economica. Demandante de empleo. No administrador sociedad mercantil." ;;
    Documentos) VALOR="DNI/NIE de todos los miembros. Certificado empadronamiento. Libro familia. Declaracion renta. Certificado bancario. Demandante empleo." ;;
    Pasos) VALOR="1. Reunir documentos. 2. Solicitar en sede.seg-social.gob.es (cert digital/clave), presencial CAISS (cita previa), o tel 900 20 22 22. Plazo: 6 meses." ;;
  esac
  create_page "$KB_DB" "IMV - $CAMPO" '{
    "parent": {"database_id": "'"$KB_DB"'"},
    "properties": {
      "Tramite": {"title": [{"text": {"content": "IMV"}}]},
      "Campo": {"rich_text": [{"text": {"content": "'"$CAMPO"'"}}]},
      "Valor": {"rich_text": [{"text": {"content": "'"$VALOR"'"}}]},
      "Fuente URL": {"url": "https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-8d06-4645-bde7-05374ee42ac7"},
      "Organismo": {"select": {"name": "Seguridad Social"}},
      "Estado": {"select": {"name": "Verificado"}},
      "Fecha verificacion": {"date": {"start": "2024-12-01"}}
    }
  }'
done

# Empadronamiento
for CAMPO in Descripcion Requisitos Documentos Pasos; do
  case $CAMPO in
    Descripcion) VALOR="Registro obligatorio en el municipio donde resides. Puerta de acceso a sanidad, educacion, servicios sociales. Es un DERECHO." ;;
    Requisitos) VALOR="Vivir en el municipio. Documento de identidad (DNI, NIE, pasaporte). Acreditar vivienda. NO se necesita permiso de residencia." ;;
    Documentos) VALOR="DNI (espanoles), NIE+pasaporte (UE), Pasaporte (no UE). Menores: libro familia. Vivienda: contrato alquiler o escritura." ;;
    Pasos) VALOR="1. Cita previa (madrid.es/padron o tel 010). 2. Acudir OAC con documentos. 3. Rellenar hoja padronal. 4. Volante en el acto." ;;
  esac
  create_page "$KB_DB" "Empadronamiento - $CAMPO" '{
    "parent": {"database_id": "'"$KB_DB"'"},
    "properties": {
      "Tramite": {"title": [{"text": {"content": "Empadronamiento"}}]},
      "Campo": {"rich_text": [{"text": {"content": "'"$CAMPO"'"}}]},
      "Valor": {"rich_text": [{"text": {"content": "'"$VALOR"'"}}]},
      "Fuente URL": {"url": "https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Empadronamiento"},
      "Organismo": {"select": {"name": "Ayuntamiento Madrid"}},
      "Estado": {"select": {"name": "Verificado"}},
      "Fecha verificacion": {"date": {"start": "2024-12-01"}}
    }
  }'
done

# Tarjeta Sanitaria
for CAMPO in Descripcion Requisitos Documentos Pasos; do
  case $CAMPO in
    Descripcion) VALOR="Acredita derecho a asistencia sanitaria publica. Acceso a medico familia, pediatra, urgencias, especialistas, medicamentos." ;;
    Requisitos) VALOR="Afiliados Seg Social. Pensionistas. Desempleados. Empadronados sin recursos. Menores. Embarazadas. Urgencias: derecho para TODOS." ;;
    Documentos) VALOR="Certificado empadronamiento (menos 3 meses). DNI/NIE/pasaporte. Num afiliacion Seg Social. Menores: libro familia + DNI padre." ;;
    Pasos) VALOR="1. Ir Centro Salud cercano (madrid.org/cs). 2. Alta en admision con documentos. 3. Asignacion medico. 4. Tarjeta provisional inmediata." ;;
  esac
  create_page "$KB_DB" "Tarjeta Sanitaria - $CAMPO" '{
    "parent": {"database_id": "'"$KB_DB"'"},
    "properties": {
      "Tramite": {"title": [{"text": {"content": "Tarjeta Sanitaria"}}]},
      "Campo": {"rich_text": [{"text": {"content": "'"$CAMPO"'"}}]},
      "Valor": {"rich_text": [{"text": {"content": "'"$VALOR"'"}}]},
      "Fuente URL": {"url": "https://www.comunidad.madrid/servicios/salud/tarjeta-sanitaria"},
      "Organismo": {"select": {"name": "Comunidad de Madrid"}},
      "Estado": {"select": {"name": "Verificado"}},
      "Fecha verificacion": {"date": {"start": "2024-12-01"}}
    }
  }'
done

# ============================================================
# DEMO & TESTING (10 entries: T1-T10)
# ============================================================
echo ""
echo "=== Populating Demo & Testing (10 entries) ==="

declare -a TESTS=(
  'T1 — Cache Match Keyword Exacto|Golden test|message=Que es el IMV?, lang=es, TEXT|hit=True, id=imv_es|hit=True, id=imv_es|Pasa|G1-Texto|test_t1 PASS'
  'T2 — Cache Match Sin Match|Golden test|message=Que tiempo hace?, lang=es, TEXT|hit=False|hit=False|Pasa|G1-Texto|test_t2 PASS'
  'T3 — Cache Match Imagen Demo|Golden test|message=empty, lang=es, IMAGE|hit=True, id=maria_carta_vision|hit=True, id=maria_carta_vision|Pasa|G1-Texto|test_t3 PASS'
  'T4 — KB Lookup Empadronamiento|Golden test|query=necesito empadronarme, lang=es|tramite=empadronamiento|tramite=empadronamiento|Pasa|G1-Texto|test_t4 PASS'
  'T5 — Detect Language Frances|Golden test|text=Bonjour, comment faire?|lang=fr|lang=fr|Pasa|G1-Texto|test_t5 PASS'
  'T6 — Webhook Parse Text|Golden test|POST Body=Hola, NumMedia=0|input_type=TEXT, message=Hola|input_type=TEXT, message=Hola|Pasa|G2-Audio|test_t6 PASS'
  'T7 — Webhook Parse Audio|Golden test|POST NumMedia=1, audio/ogg|input_type=AUDIO|input_type=AUDIO|Pasa|G2-Audio|test_t7 PASS'
  'T8 — Pipeline Text Stub|Golden test|IncomingMessage Que es el IMV? TEXT|Twilio send con IMV info|Twilio send con IMV info|Pasa|G2-Audio|test_t8 PASS'
  'T9 — WA Text Demo E2E|Golden test|POST /webhook Que es el IMV?|HTTP 200, cache hit imv_es|HTTP 200, cache hit imv_es|Pasa|G2-Audio|test_t9 PASS'
  'T10 — WA Audio Demo Stub E2E|Golden test|POST /webhook audio/ogg stub|Pipeline AUDIO type|Pipeline AUDIO type|Pasa|G2-Audio|test_t10 PASS'
)

for entry in "${TESTS[@]}"; do
  IFS='|' read -r TEST_NAME TIPO INPUT OUTPUT_ESP OUTPUT_REAL RESULTADO GATE NOTAS <<< "$entry"
  create_page "$TEST_DB" "$TEST_NAME" '{
    "parent": {"database_id": "'"$TEST_DB"'"},
    "properties": {
      "Test": {"title": [{"text": {"content": "'"$TEST_NAME"'"}}]},
      "Tipo": {"select": {"name": "'"$TIPO"'"}},
      "Input": {"rich_text": [{"text": {"content": "'"$INPUT"'"}}]},
      "Output esperado": {"rich_text": [{"text": {"content": "'"$OUTPUT_ESP"'"}}]},
      "Output real": {"rich_text": [{"text": {"content": "'"$OUTPUT_REAL"'"}}]},
      "Resultado": {"select": {"name": "'"$RESULTADO"'"}},
      "Gate": {"select": {"name": "'"$GATE"'"}},
      "Fecha": {"date": {"start": "2026-02-12"}},
      "Notas": {"rich_text": [{"text": {"content": "'"$NOTAS"'"}}]}
    }
  }'
done

# ============================================================
# Summary
# ============================================================
echo ""
echo "=== DONE ==="
echo "Created: $CREATED"
echo "Failed:  $FAILED"
echo "Total:   $((CREATED + FAILED))"
