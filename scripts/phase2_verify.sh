#!/usr/bin/env bash
# =============================================================
# phase2_verify.sh — Phase 2 verification script
# Runs: pytest, ruff lint, docker build + /health, optional Render check
# Usage: ./scripts/phase2_verify.sh [RENDER_URL]
# Example: ./scripts/phase2_verify.sh https://civicaid-voice.onrender.com
# =============================================================

set -uo pipefail

RENDER_URL="${1:-}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

report_pass() {
    echo "  => PASS"
    PASS_COUNT=$((PASS_COUNT + 1))
}

report_fail() {
    echo "  => FAIL"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

report_skip() {
    echo "  => SKIP"
    SKIP_COUNT=$((SKIP_COUNT + 1))
}

echo "============================================="
echo " CivicAid Voice — Phase 2 Verification"
echo " ${TIMESTAMP}"
echo "============================================="
echo ""

# --- 1. Pytest ---
echo ">>> Step 1: Running pytest..."
if pytest tests/ -v --tb=short; then
    report_pass
else
    report_fail
fi
echo ""

# --- 2. Ruff lint ---
echo ">>> Step 2: Running ruff lint..."
if ruff check src/ tests/ --select E,F,W --ignore E501; then
    report_pass
else
    report_fail
fi
echo ""

# --- 3. Docker build ---
echo ">>> Step 3: Docker build..."
if command -v docker &> /dev/null; then
    if docker build -t civicaid-voice:test . 2>&1 | tail -5; then
        report_pass

        # --- 4. Docker /health check ---
        echo ""
        echo ">>> Step 4: Docker container /health check..."
        CONTAINER_ID=$(docker run -d -p 5050:5000 \
            -e DEMO_MODE=true \
            -e LLM_LIVE=false \
            -e WHISPER_ON=false \
            -e TWILIO_ACCOUNT_SID=test \
            -e TWILIO_AUTH_TOKEN=test \
            -e GEMINI_API_KEY=test \
            civicaid-voice:test 2>/dev/null)

        if [ -n "$CONTAINER_ID" ]; then
            echo "  Container started: ${CONTAINER_ID:0:12}"
            sleep 3
            if curl -sf http://localhost:5050/health | python3 -m json.tool; then
                report_pass
            else
                echo "  /health did not respond"
                report_fail
            fi
            docker stop "$CONTAINER_ID" > /dev/null 2>&1
            docker rm "$CONTAINER_ID" > /dev/null 2>&1
        else
            echo "  Could not start container"
            report_fail
        fi
    else
        report_fail
        echo ""
        echo ">>> Step 4: Docker /health (skipped — build failed)"
        report_skip
    fi
else
    echo "  Docker not available"
    report_skip
    echo ""
    echo ">>> Step 4: Docker /health (skipped — no docker)"
    report_skip
fi
echo ""

# --- 5. Render /health (optional) ---
echo ">>> Step 5: Render /health check..."
if [ -n "$RENDER_URL" ]; then
    if curl -sf --max-time 15 "${RENDER_URL}/health" | python3 -m json.tool; then
        report_pass
    else
        echo "  Render /health did not respond at ${RENDER_URL}"
        report_fail
    fi
else
    echo "  No RENDER_URL provided (pass as first argument)"
    report_skip
fi
echo ""

# --- Summary ---
TOTAL=$((PASS_COUNT + FAIL_COUNT + SKIP_COUNT))
echo "============================================="
echo " VERIFICATION SUMMARY"
echo "============================================="
echo " PASS:  ${PASS_COUNT}"
echo " FAIL:  ${FAIL_COUNT}"
echo " SKIP:  ${SKIP_COUNT}"
echo " TOTAL: ${TOTAL}"
echo "============================================="

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo " RESULT: FAIL — ${FAIL_COUNT} step(s) failed"
    exit 1
else
    echo " RESULT: OK — all executed steps passed"
    exit 0
fi
