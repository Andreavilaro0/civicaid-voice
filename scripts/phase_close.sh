#!/usr/bin/env bash
# =============================================================
# phase_close.sh — Script de cierre de fase
# Genera evidencia automatica: tests, lint, tree, checksums,
# docker build, health, git status, gate summary
# Uso: ./scripts/phase_close.sh [PHASE_NUMBER] [RENDER_URL]
# Ejemplo: ./scripts/phase_close.sh 1 https://civicaid-voice.onrender.com
# =============================================================

set -uo pipefail

PHASE="${1:-1}"
RENDER_URL="${2:-}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="docs/07-evidence/logs"
REPORT_FILE="docs/07-evidence/phase-${PHASE}-close-report.md"

# Gate tracking variables
GATE_G0="FAIL"
GATE_G1="FAIL"
GATE_G2="FAIL"
GATE_G3="SKIP"
TESTS_PASS=false
LINT_PASS=false
DOCKER_PASS=false

mkdir -p "$REPORT_DIR"

echo "========================================="
echo " CivicAid Voice — Cierre de Fase ${PHASE}"
echo " ${TIMESTAMP}"
echo "========================================="
echo ""

# --- Header del reporte ---
cat > "$REPORT_FILE" << EOF
# Reporte de Cierre — Fase ${PHASE}

> Generado automaticamente: ${TIMESTAMP}
> Comando: \`./scripts/phase_close.sh ${PHASE} ${RENDER_URL:-N/A}\`

---

## 0. Machine Info

\`\`\`
EOF

echo ">>> Recopilando info de maquina..."
{
    echo "Date:    $(date)"
    echo "Host:    $(uname -a)"
    echo "Python:  $(python3 --version 2>&1)"
    echo "Docker:  $(docker --version 2>&1 || echo 'not installed')"
    echo "Git:     $(git --version 2>&1)"
    echo "Ruff:    $(ruff --version 2>&1 || echo 'not installed')"
} >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 1. Tests ---
echo ">>> Ejecutando tests..."
echo "## 1. Tests" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
if pytest tests/ -v --tb=short 2>&1 | tee -a "$REPORT_FILE"; then
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: PASS**" >> "$REPORT_FILE"
    TESTS_PASS=true
    echo ""
    echo "TESTS: PASS"
else
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: FAIL**" >> "$REPORT_FILE"
    echo ""
    echo "TESTS: FAIL"
fi
echo "" >> "$REPORT_FILE"

# --- 2. Lint (ruff) ---
echo ">>> Ejecutando ruff lint..."
echo "## 2. Lint (ruff)" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
if ruff check src/ tests/ --select E,F,W --ignore E501 2>&1 | tee -a "$REPORT_FILE"; then
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: PASS**" >> "$REPORT_FILE"
    LINT_PASS=true
    echo ""
    echo "LINT: PASS"
else
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: FAIL**" >> "$REPORT_FILE"
    echo ""
    echo "LINT: FAIL"
fi
echo "" >> "$REPORT_FILE"

# --- 3. Tree ---
echo ">>> Generando arbol del proyecto..."
echo "## 3. Arbol del proyecto" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
find . -maxdepth 3 -not -path './.git/*' -not -path './__pycache__/*' -not -path './.pytest_cache/*' -not -name '__pycache__' -not -name '.pytest_cache' -not -path './.venv/*' -not -path './venv/*' | sort >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 4. Checksums de docs ---
echo ">>> Calculando checksums de documentacion..."
echo "## 4. Checksums de documentacion" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
if [ -d "docs" ]; then
    find docs -name "*.md" -exec md5sum {} \; 2>/dev/null >> "$REPORT_FILE" || \
    find docs -name "*.md" -exec md5 {} \; 2>/dev/null >> "$REPORT_FILE"
fi
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 5. Docker build verification ---
echo ">>> Verificando Docker build..."
echo "## 5. Docker Build" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
if docker build -t civicaid-voice:test . 2>&1 | tail -20 | tee -a "$REPORT_FILE"; then
    DOCKER_PASS=true
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: PASS**" >> "$REPORT_FILE"
    echo ""
    echo "DOCKER BUILD: PASS"
else
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: FAIL**" >> "$REPORT_FILE"
    echo ""
    echo "DOCKER BUILD: FAIL"
fi
echo "" >> "$REPORT_FILE"

# --- 6. Health check ---
echo "## 6. Health check" >> "$REPORT_FILE"
HEALTH_OK=false
if [ -n "$RENDER_URL" ]; then
    echo ">>> Verificando /health en ${RENDER_URL}..."
    echo "URL: ${RENDER_URL}/health" >> "$REPORT_FILE"
    echo '```json' >> "$REPORT_FILE"
    if curl -sf "${RENDER_URL}/health" 2>&1 | python3 -m json.tool >> "$REPORT_FILE" 2>&1; then
        HEALTH_OK=true
    else
        echo "ERROR: No se pudo conectar" >> "$REPORT_FILE"
    fi
    echo '```' >> "$REPORT_FILE"
else
    echo "URL: No proporcionada (pasar como segundo argumento)" >> "$REPORT_FILE"
    echo "**TODO:** Ejecutar con URL de Render cuando este desplegado" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# --- 7. Git status ---
echo ">>> Estado de git..."
echo "## 7. Git" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
git log --oneline -10 2>&1 >> "$REPORT_FILE" || echo "Sin commits aun" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
git status --short 2>&1 >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 8. Gate summary ---
echo ">>> Evaluando gates..."

# G0 Tooling: check if agents/skills config exists
if [ -d ".claude/agents" ] && [ "$(ls -A .claude/agents/ 2>/dev/null)" ]; then
    GATE_G0="PASS"
fi

# G1 Texto: tests pass + lint pass
if $TESTS_PASS && $LINT_PASS; then
    GATE_G1="PASS"
fi

# G2 Audio: tests pass (audio tests are part of the test suite)
if $TESTS_PASS; then
    GATE_G2="PASS"
fi

# G3 Demo: Render URL responds
if [ -n "$RENDER_URL" ]; then
    if $HEALTH_OK; then
        GATE_G3="PASS"
    else
        GATE_G3="FAIL"
    fi
fi

TOTAL_FILES=$(find . -maxdepth 4 -type f -not -path './.git/*' -not -path '*/__pycache__/*' -not -path '*/.pytest_cache/*' -not -path './.venv/*' -not -path './venv/*' | wc -l | tr -d ' ')
TOTAL_TESTS=$(pytest tests/ --collect-only -q 2>/dev/null | tail -1 || echo "?")

echo "## 8. Gate Summary — Phase ${PHASE}" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Gate | Description       | Status |" >> "$REPORT_FILE"
echo "|------|-------------------|--------|" >> "$REPORT_FILE"
echo "| G0   | Tooling (agents)  | ${GATE_G0} |" >> "$REPORT_FILE"
echo "| G1   | Texto (tests+lint)| ${GATE_G1} |" >> "$REPORT_FILE"
echo "| G2   | Audio (tests)     | ${GATE_G2} |" >> "$REPORT_FILE"
echo "| G3   | Demo (Render)     | ${GATE_G3} |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "- Archivos totales: ${TOTAL_FILES}" >> "$REPORT_FILE"
echo "- Tests: ${TOTAL_TESTS}" >> "$REPORT_FILE"
echo "- Docker build: $(if $DOCKER_PASS; then echo PASS; else echo FAIL; fi)" >> "$REPORT_FILE"
echo "- Fecha: ${TIMESTAMP}" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo ""
echo "========================================="
echo " GATE SUMMARY — Phase ${PHASE}"
echo "========================================="
echo " G0 Tooling (agents):   ${GATE_G0}"
echo " G1 Texto (tests+lint): ${GATE_G1}"
echo " G2 Audio (tests):      ${GATE_G2}"
echo " G3 Demo (Render):      ${GATE_G3}"
echo " Docker build:          $(if $DOCKER_PASS; then echo PASS; else echo FAIL; fi)"
echo "========================================="
echo " Reporte generado: ${REPORT_FILE}"
echo "========================================="
