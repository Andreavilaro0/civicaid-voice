#!/usr/bin/env bash
# =============================================================
# phase3_verify.sh — Phase 3 verification script (flag-based)
#
# Usage:
#   ./scripts/phase3_verify.sh [FLAGS]
#
# Flags:
#   --bootstrap     Create/activate .venv, install all deps (requirements.txt
#                   + requirements-dev.txt). Run this the first time or on a
#                   fresh clone to guarantee pytest + ruff are available.
#   --local         Run pytest + ruff lint
#   --docker        Docker build + container /health check
#   --render URL    Render /health + webhook 403 check
#   --twilio        Twilio WhatsApp smoke test
#   --notion        Notion API DB count verification
#   --all           Run everything (default if no flags given)
#   -h, --help      Show this help
#
# Examples:
#   ./scripts/phase3_verify.sh --bootstrap --local          # first-time setup + test
#   ./scripts/phase3_verify.sh --bootstrap --local --docker  # setup + test + docker
#   ./scripts/phase3_verify.sh --local                       # quick local check
#   ./scripts/phase3_verify.sh --render https://civicaid-voice.onrender.com
#   ./scripts/phase3_verify.sh --all                         # everything
#   ./scripts/phase3_verify.sh                               # same as --all
#
# Environment variables (for --render, --twilio, --notion):
#   RENDER_URL          — alternatively pass via --render URL
#   TWILIO_ACCOUNT_SID  — for Twilio smoke test
#   TWILIO_AUTH_TOKEN   — for Twilio smoke test
#   TWILIO_SANDBOX_FROM — WhatsApp sandbox number (default: whatsapp:+14155238886)
#   TWILIO_SMOKE_TO     — destination number for smoke test
#   NOTION_TOKEN        — for Notion API verification
# =============================================================

set -uo pipefail

# --- Defaults ---
BOOTSTRAP=false
RUN_LOCAL=false
RUN_DOCKER=false
RUN_RENDER=false
RUN_TWILIO=false
RUN_NOTION=false
RENDER_URL=""
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
STEP_NUM=0
TOTAL_STEPS=0
EVIDENCE_FILE="docs/07-evidence/phase3-verify-output.txt"

# --- Notion DB IDs ---
NOTION_BACKLOG_DB="304c5a0f-372a-81de-92a8-f54c03b391c0"
NOTION_KB_DB="304c5a0f-372a-81ff-9d45-c785e69f7335"
NOTION_TESTING_DB="304c5a0f-372a-810d-8767-d77efbd46bb2"

# --- Helpers ---
report_pass() {
    echo "  => PASS"
    PASS_COUNT=$((PASS_COUNT + 1))
}

report_fail() {
    echo "  => FAIL"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

report_skip() {
    echo "  => SKIP ($1)"
    SKIP_COUNT=$((SKIP_COUNT + 1))
}

next_step() {
    STEP_NUM=$((STEP_NUM + 1))
    echo ">>> Step ${STEP_NUM}/${TOTAL_STEPS}: $1"
}

show_help() {
    sed -n '2,/^# =====/p' "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

# Resolve a command: check PATH, then python3 -m fallback.
# Usage: resolve_cmd <name>  — sets RESOLVED_CMD or ""
resolve_cmd() {
    RESOLVED_CMD=""
    if command -v "$1" &> /dev/null; then
        RESOLVED_CMD="$1"
    elif python3 -m "$1" --version &> /dev/null 2>&1; then
        RESOLVED_CMD="python3 -m $1"
    fi
}

# --- Parse arguments ---
NO_MODE_FLAGS=true  # track if user passed any mode flags

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        --bootstrap|--install)
            BOOTSTRAP=true
            shift
            ;;
        --local)
            RUN_LOCAL=true
            NO_MODE_FLAGS=false
            shift
            ;;
        --docker)
            RUN_DOCKER=true
            NO_MODE_FLAGS=false
            shift
            ;;
        --render)
            RUN_RENDER=true
            NO_MODE_FLAGS=false
            if [ $# -ge 2 ] && [[ "$2" != --* ]]; then
                RENDER_URL="$2"
                shift 2
            else
                echo "ERROR: --render requires a URL argument"
                exit 1
            fi
            ;;
        --twilio)
            RUN_TWILIO=true
            NO_MODE_FLAGS=false
            shift
            ;;
        --notion)
            RUN_NOTION=true
            NO_MODE_FLAGS=false
            shift
            ;;
        --all)
            RUN_LOCAL=true
            RUN_DOCKER=true
            RUN_RENDER=true
            RUN_TWILIO=true
            RUN_NOTION=true
            NO_MODE_FLAGS=false
            shift
            ;;
        *)
            echo "Unknown flag: $1"
            echo "Run with --help for usage."
            exit 1
            ;;
    esac
done

# Default: --all when no mode flags given
if $NO_MODE_FLAGS; then
    RUN_LOCAL=true
    RUN_DOCKER=true
    RUN_RENDER=true
    RUN_TWILIO=true
    RUN_NOTION=true
fi

# =============================================
# BOOTSTRAP: venv + deps
# =============================================
if $BOOTSTRAP; then
    echo ">>> Bootstrap: setting up environment..."

    if [ -n "${VIRTUAL_ENV:-}" ]; then
        echo "  Using active venv: ${VIRTUAL_ENV}"
    else
        if [ ! -d ".venv" ]; then
            echo "  Creating .venv..."
            python3 -m venv .venv || { echo "FATAL: cannot create venv (python3 -m venv failed)"; exit 1; }
        fi
        echo "  Activating .venv..."
        # shellcheck disable=SC1091
        source .venv/bin/activate
    fi

    echo "  Installing requirements.txt..."
    pip install -q -r requirements.txt

    if [ -f requirements-dev.txt ]; then
        echo "  Installing requirements-dev.txt..."
        pip install -q -r requirements-dev.txt
    fi

    echo "  Bootstrap complete. python=$(which python3) pytest=$(which pytest 2>/dev/null || echo 'n/a') ruff=$(which ruff 2>/dev/null || echo 'n/a')"
    echo ""
fi

# =============================================
# Pre-flight: verify required tools for --local
# =============================================
if $RUN_LOCAL; then
    resolve_cmd pytest
    PYTEST_CMD="$RESOLVED_CMD"
    resolve_cmd ruff
    RUFF_CMD="$RESOLVED_CMD"

    if [ -z "$PYTEST_CMD" ]; then
        echo "FATAL: pytest not found."
        echo "  Fix: run with --bootstrap, or manually: pip install -r requirements-dev.txt"
        exit 1
    fi
    if [ -z "$RUFF_CMD" ]; then
        echo "FATAL: ruff not found."
        echo "  Fix: run with --bootstrap, or manually: pip install -r requirements-dev.txt"
        exit 1
    fi
fi

# --- Count total steps ---
if $RUN_LOCAL; then TOTAL_STEPS=$((TOTAL_STEPS + 2)); fi   # pytest + ruff
if $RUN_DOCKER; then TOTAL_STEPS=$((TOTAL_STEPS + 2)); fi  # build + health
if $RUN_RENDER; then TOTAL_STEPS=$((TOTAL_STEPS + 2)); fi  # health + webhook 403
if $RUN_TWILIO; then TOTAL_STEPS=$((TOTAL_STEPS + 1)); fi  # smoke test
if $RUN_NOTION; then TOTAL_STEPS=$((TOTAL_STEPS + 1)); fi  # DB count

# --- Capture output ---
mkdir -p "$(dirname "$EVIDENCE_FILE")"
exec > >(tee "$EVIDENCE_FILE") 2>&1

echo "============================================="
echo " CivicAid Voice — Phase 3 Verification"
echo " ${TIMESTAMP}"
echo "============================================="
echo " Flags: bootstrap=${BOOTSTRAP} local=${RUN_LOCAL} docker=${RUN_DOCKER} render=${RUN_RENDER} twilio=${RUN_TWILIO} notion=${RUN_NOTION}"
echo ""

# =============================================
# LOCAL: pytest + ruff
# =============================================
if $RUN_LOCAL; then

    # --- Pytest ---
    next_step "Running pytest..."
    if $PYTEST_CMD tests/ -v --tb=short; then
        report_pass
    else
        report_fail
    fi
    echo ""

    # --- Ruff lint ---
    next_step "Running ruff lint..."
    if $RUFF_CMD check src/ tests/ --select E,F,W --ignore E501; then
        report_pass
    else
        echo "  (lint errors found — check output above)"
        report_fail
    fi
    echo ""
fi

# =============================================
# DOCKER: build + /health
# =============================================
if $RUN_DOCKER; then

    # --- Docker build ---
    next_step "Docker build..."
    if ! command -v docker &> /dev/null; then
        report_skip "docker not available"
        echo ""
        next_step "Docker container /health check..."
        report_skip "docker not available"
    else
        if docker build -t civicaid-voice:phase3 . 2>&1 | tail -5; then
            report_pass

            # --- Docker /health check ---
            echo ""
            next_step "Docker container /health check..."

            # Clean up any previous container on port 5060
            docker rm -f civicaid-verify 2>/dev/null || true

            CONTAINER_ID=$(docker run -d --name civicaid-verify -p 5060:5000 \
                -e DEMO_MODE=true \
                -e LLM_LIVE=false \
                -e WHISPER_ON=false \
                -e TWILIO_ACCOUNT_SID=test \
                -e TWILIO_AUTH_TOKEN=test \
                -e GEMINI_API_KEY=test \
                civicaid-voice:phase3 2>/dev/null)

            if [ -n "$CONTAINER_ID" ]; then
                echo "  Container started: ${CONTAINER_ID:0:12}"
                sleep 4
                HEALTH_RESPONSE=$(curl -sf http://localhost:5060/health 2>/dev/null)
                if [ -n "$HEALTH_RESPONSE" ]; then
                    echo "$HEALTH_RESPONSE" | python3 -m json.tool
                    CACHE_ENTRIES=$(echo "$HEALTH_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('components',{}).get('cache_entries',0))" 2>/dev/null)
                    if [ "${CACHE_ENTRIES:-0}" -ge 8 ]; then
                        echo "  cache_entries=${CACHE_ENTRIES} >= 8"
                        report_pass
                    else
                        echo "  cache_entries=${CACHE_ENTRIES} < 8"
                        report_fail
                    fi
                else
                    echo "  /health did not respond"
                    report_fail
                fi
                docker stop civicaid-verify > /dev/null 2>&1
                docker rm civicaid-verify > /dev/null 2>&1
            else
                echo "  Could not start container"
                report_fail
            fi
        else
            report_fail
            echo ""
            next_step "Docker /health (skipped — build failed)"
            report_skip "build failed"
        fi
    fi
    echo ""
fi

# =============================================
# RENDER: /health + webhook 403
# =============================================
if $RUN_RENDER; then

    # --- Render /health ---
    next_step "Render /health check..."
    if [ -n "$RENDER_URL" ]; then
        RENDER_RESPONSE=$(curl -sf --max-time 60 "${RENDER_URL}/health" 2>/dev/null)
        if [ -n "$RENDER_RESPONSE" ]; then
            echo "$RENDER_RESPONSE" | python3 -m json.tool
            report_pass
        else
            echo "  Render /health did not respond at ${RENDER_URL}"
            report_fail
        fi
    else
        report_skip "no RENDER_URL (use --render URL)"
    fi
    echo ""

    # --- Render webhook 403 ---
    next_step "Render webhook signature enforcement..."
    if [ -n "$RENDER_URL" ]; then
        HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" -X POST "${RENDER_URL}/webhook" -d "Body=test" 2>/dev/null)
        if [ "$HTTP_CODE" = "403" ]; then
            echo "  POST /webhook without signature => HTTP ${HTTP_CODE} (correctly rejected)"
            report_pass
        elif [ "$HTTP_CODE" = "000" ]; then
            echo "  Render not reachable"
            report_fail
        else
            echo "  POST /webhook without signature => HTTP ${HTTP_CODE} (expected 403)"
            report_fail
        fi
    else
        report_skip "no RENDER_URL"
    fi
    echo ""
fi

# =============================================
# TWILIO: smoke test
# =============================================
if $RUN_TWILIO; then

    next_step "Twilio WhatsApp smoke test..."
    TWILIO_SID="${TWILIO_ACCOUNT_SID:-}"
    TWILIO_TOKEN="${TWILIO_AUTH_TOKEN:-}"
    TWILIO_FROM="${TWILIO_SANDBOX_FROM:-whatsapp:+14155238886}"
    TWILIO_TO="${TWILIO_SMOKE_TO:-}"

    if [ -n "$TWILIO_SID" ] && [ -n "$TWILIO_TOKEN" ] && [ -n "$TWILIO_TO" ] && [ "$TWILIO_SID" != "test" ]; then
        echo "  Sending smoke test to ${TWILIO_TO}..."
        TWILIO_RESPONSE=$(curl -sf -X POST \
            "https://api.twilio.com/2010-04-01/Accounts/${TWILIO_SID}/Messages.json" \
            -u "${TWILIO_SID}:${TWILIO_TOKEN}" \
            --data-urlencode "From=${TWILIO_FROM}" \
            --data-urlencode "To=${TWILIO_TO}" \
            --data-urlencode "Body=[SMOKE TEST] Clara phase3_verify.sh — $(date '+%H:%M:%S')" \
            2>/dev/null)
        if echo "$TWILIO_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); assert d.get('sid','').startswith('SM')" 2>/dev/null; then
            MSG_SID=$(echo "$TWILIO_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['sid'])" 2>/dev/null)
            echo "  Message queued: ${MSG_SID}"
            report_pass
        else
            echo "  Twilio API returned error:"
            echo "$TWILIO_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$TWILIO_RESPONSE"
            report_fail
        fi
    else
        if [ -z "$TWILIO_SID" ] || [ "$TWILIO_SID" = "test" ]; then
            report_skip "TWILIO_ACCOUNT_SID not set or is 'test'"
        elif [ -z "$TWILIO_TO" ]; then
            report_skip "TWILIO_SMOKE_TO not set"
        else
            report_skip "Twilio credentials incomplete"
        fi
    fi
    echo ""
fi

# =============================================
# NOTION: API DB count verification
# =============================================
if $RUN_NOTION; then

    next_step "Notion API DB count verification..."
    NOTION_TK="${NOTION_TOKEN:-}"

    if [ -z "$NOTION_TK" ]; then
        report_skip "NOTION_TOKEN not set"
    else
        NOTION_TOTAL=0
        NOTION_OK=true

        # Query Backlog DB
        BACKLOG_COUNT=$(curl -sf -X POST \
            "https://api.notion.com/v1/databases/${NOTION_BACKLOG_DB}/query" \
            -H "Authorization: Bearer ${NOTION_TK}" \
            -H "Notion-Version: 2022-06-28" \
            -H "Content-Type: application/json" \
            -d '{"page_size": 100}' 2>/dev/null \
            | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null)
        if [ -z "$BACKLOG_COUNT" ]; then
            echo "  Backlog DB query failed"
            NOTION_OK=false
        else
            echo "  Backlog DB:     ${BACKLOG_COUNT} entries (expected 43)"
            NOTION_TOTAL=$((NOTION_TOTAL + BACKLOG_COUNT))
        fi

        # Query KB Tramites DB
        KB_COUNT=$(curl -sf -X POST \
            "https://api.notion.com/v1/databases/${NOTION_KB_DB}/query" \
            -H "Authorization: Bearer ${NOTION_TK}" \
            -H "Notion-Version: 2022-06-28" \
            -H "Content-Type: application/json" \
            -d '{"page_size": 100}' 2>/dev/null \
            | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null)
        if [ -z "$KB_COUNT" ]; then
            echo "  KB Tramites DB: query failed"
            NOTION_OK=false
        else
            echo "  KB Tramites DB: ${KB_COUNT} entries (expected 12)"
            NOTION_TOTAL=$((NOTION_TOTAL + KB_COUNT))
        fi

        # Query Testing DB
        TESTING_COUNT=$(curl -sf -X POST \
            "https://api.notion.com/v1/databases/${NOTION_TESTING_DB}/query" \
            -H "Authorization: Bearer ${NOTION_TK}" \
            -H "Notion-Version: 2022-06-28" \
            -H "Content-Type: application/json" \
            -d '{"page_size": 100}' 2>/dev/null \
            | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null)
        if [ -z "$TESTING_COUNT" ]; then
            echo "  Testing DB:     query failed"
            NOTION_OK=false
        else
            echo "  Testing DB:     ${TESTING_COUNT} entries (expected 26)"
            NOTION_TOTAL=$((NOTION_TOTAL + TESTING_COUNT))
        fi

        if $NOTION_OK; then
            echo "  TOTAL: ${NOTION_TOTAL} entries (expected 81)"
            if [ "$NOTION_TOTAL" -ge 81 ]; then
                report_pass
            else
                echo "  Total entries below expected 81"
                report_fail
            fi
        else
            report_fail
        fi
    fi
    echo ""
fi

# =============================================
# SUMMARY
# =============================================
TOTAL=$((PASS_COUNT + FAIL_COUNT + SKIP_COUNT))
echo "============================================="
echo " PHASE 3 VERIFICATION SUMMARY"
echo "============================================="
echo " PASS:  ${PASS_COUNT}"
echo " FAIL:  ${FAIL_COUNT}"
echo " SKIP:  ${SKIP_COUNT}"
echo " TOTAL: ${TOTAL}"
echo "============================================="
echo " Evidence saved to: ${EVIDENCE_FILE}"
echo "============================================="

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo " RESULT: FAIL — ${FAIL_COUNT} step(s) failed"
    exit 1
else
    echo " RESULT: OK — all executed steps passed"
    exit 0
fi
