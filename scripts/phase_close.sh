#!/usr/bin/env bash
# =============================================================
# phase_close.sh — Script de cierre de fase
# Genera evidencia automatica: tests, tree, checksums, health
# Uso: ./scripts/phase_close.sh [PHASE_NUMBER] [RENDER_URL]
# Ejemplo: ./scripts/phase_close.sh 1 https://civicaid-voice.onrender.com
# =============================================================

set -euo pipefail

PHASE="${1:-1}"
RENDER_URL="${2:-}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="docs/07-evidence/logs"
REPORT_FILE="docs/07-evidence/phase-${PHASE}-close-report.md"

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

EOF

# --- 1. Tests ---
echo ">>> Ejecutando tests..."
echo "## 1. Tests" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
if pytest tests/ -v --tb=short 2>&1 | tee -a "$REPORT_FILE"; then
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: PASS**" >> "$REPORT_FILE"
    echo ""
    echo "TESTS: PASS"
else
    echo '```' >> "$REPORT_FILE"
    echo "**Resultado: FAIL**" >> "$REPORT_FILE"
    echo ""
    echo "TESTS: FAIL"
fi
echo "" >> "$REPORT_FILE"

# --- 2. Tree ---
echo ">>> Generando arbol del proyecto..."
echo "## 2. Arbol del proyecto" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
find . -maxdepth 3 -not -path './.git/*' -not -path './__pycache__/*' -not -path './.pytest_cache/*' -not -name '__pycache__' -not -name '.pytest_cache' | sort >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 3. Checksums de docs ---
echo ">>> Calculando checksums de documentacion..."
echo "## 3. Checksums de documentacion" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
if [ -d "docs" ]; then
    find docs -name "*.md" -exec md5sum {} \; 2>/dev/null >> "$REPORT_FILE" || \
    find docs -name "*.md" -exec md5 {} \; 2>/dev/null >> "$REPORT_FILE"
fi
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 4. Health check ---
echo "## 4. Health check" >> "$REPORT_FILE"
if [ -n "$RENDER_URL" ]; then
    echo ">>> Verificando /health en ${RENDER_URL}..."
    echo "URL: ${RENDER_URL}/health" >> "$REPORT_FILE"
    echo '```json' >> "$REPORT_FILE"
    curl -s "${RENDER_URL}/health" 2>&1 | python3 -m json.tool >> "$REPORT_FILE" 2>&1 || echo "ERROR: No se pudo conectar" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
else
    echo "URL: No proporcionada (pasar como segundo argumento)" >> "$REPORT_FILE"
    echo "**TODO:** Ejecutar con URL de Render cuando este desplegado" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# --- 5. Git status ---
echo ">>> Estado de git..."
echo "## 5. Git" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
git log --oneline -10 2>&1 >> "$REPORT_FILE" || echo "Sin commits aun" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
git status --short 2>&1 >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- 6. Resumen ---
echo "## 6. Resumen" >> "$REPORT_FILE"
TOTAL_FILES=$(find . -maxdepth 4 -type f -not -path './.git/*' -not -path '*/__pycache__/*' -not -path '*/.pytest_cache/*' | wc -l | tr -d ' ')
TOTAL_TESTS=$(pytest tests/ --collect-only -q 2>/dev/null | tail -1 || echo "?")
echo "- Archivos totales: ${TOTAL_FILES}" >> "$REPORT_FILE"
echo "- Tests: ${TOTAL_TESTS}" >> "$REPORT_FILE"
echo "- Fecha: ${TIMESTAMP}" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo ""
echo "========================================="
echo " Reporte generado: ${REPORT_FILE}"
echo "========================================="
