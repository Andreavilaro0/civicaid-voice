"""
CivicAid Voice / Clara — Sprint 3 Presentation
Design Philosophy: Civic Meridians
8 pages — museum-grade execution, dark field with luminous pathways.
"""

import math
import os
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- PATHS ---
OUT_PATH = os.path.join(os.path.dirname(__file__), "Sprint3_Presentacion.pdf")

# --- REGISTER FONTS ---
SYS = "/System/Library/Fonts/Supplemental"
LIB = "/Library/Fonts"
pdfmetrics.registerFont(TTFont("DINBold", os.path.join(SYS, "DIN Alternate Bold.ttf")))
pdfmetrics.registerFont(TTFont("DINCondBold", os.path.join(SYS, "DIN Condensed Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-R", os.path.join(SYS, "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-B", os.path.join(SYS, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-I", os.path.join(SYS, "Arial Italic.ttf")))
pdfmetrics.registerFont(TTFont("Verdana-R", os.path.join(SYS, "Verdana.ttf")))
pdfmetrics.registerFont(TTFont("Verdana-B", os.path.join(SYS, "Verdana Bold.ttf")))
pdfmetrics.registerFont(TTFont("Futura", os.path.join(SYS, "Futura.ttc")))
pdfmetrics.registerFont(TTFont("SourceCode", os.path.join(LIB, "SourceCodePro-Regular.ttf")))
pdfmetrics.registerFont(TTFont("SourceCodeBold", os.path.join(LIB, "SourceCodePro-Bold.ttf")))
pdfmetrics.registerFont(TTFont("SourceCodeLight", os.path.join(LIB, "SourceCodePro-Light.ttf")))
pdfmetrics.registerFont(TTFont("Georgia", os.path.join(SYS, "Georgia.ttf")))

# --- PALETTE: Civic Meridians ---
BG = HexColor("#080E1C")
BG2 = HexColor("#0C1428")
CARD = HexColor("#101C32")
CARD_HOVER = HexColor("#142240")
TEAL = HexColor("#2DD4A8")
TEAL_MID = HexColor("#1B9B78")
TEAL_DIM = HexColor("#134A3A")
TEAL_GLOW = HexColor("#3AEDC4")
AMBER = HexColor("#F5A623")
AMBER_DIM = HexColor("#9B6A15")
WHITE = HexColor("#ECF0F4")
WHITE70 = Color(0.93, 0.94, 0.96, alpha=0.70)
MUTED = HexColor("#6B7D94")
FAINT = HexColor("#2A3A50")
BLUE = HexColor("#4A8EF5")
CORAL = HexColor("#E8706A")

W, H = 960, 540  # 16:9 landscape


# ── PRIMITIVES ──────────────────────────────────────────────

def bg(c):
    """Deep atmospheric background with fine dot matrix."""
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Gradient overlay — darker at top
    for i in range(20):
        a = 0.04 * (1 - i / 20)
        c.setFillColor(Color(0, 0, 0, alpha=a))
        c.rect(0, H - (i + 1) * (H / 20), W, H / 20, fill=1, stroke=0)
    # Dot matrix
    c.setFillColor(Color(0.08, 0.12, 0.20, alpha=0.35))
    for x in range(15, int(W), 24):
        for y in range(15, int(H), 24):
            c.circle(x, y, 0.35, fill=1, stroke=0)


def meridians(c, seed=0, count=6, opacity=0.18):
    """Subtle orbital arcs — the invisible infrastructure."""
    c.saveState()
    for i in range(count):
        ang = seed + i * (360 / count)
        cx = W * 0.5 + math.cos(math.radians(ang)) * 280
        cy = H * 0.5 + math.sin(math.radians(ang)) * 180
        r = 100 + i * 35
        c.setStrokeColor(Color(0.10, 0.20, 0.32, alpha=opacity))
        c.setLineWidth(0.6)
        p = c.beginPath()
        p.arc(cx - r, cy - r, cx + r, cy + r, ang, ang + 55 + i * 5)
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()


def node(c, x, y, r, color=TEAL, glow=True):
    """Luminous node with concentric glow rings."""
    if glow:
        for ring in [3.5, 2.5, 1.8]:
            c.setFillColor(Color(color.red, color.green, color.blue, alpha=0.06))
            c.circle(x, y, r * ring, fill=1, stroke=0)
    c.setFillColor(color)
    c.circle(x, y, r, fill=1, stroke=0)
    # Bright center
    c.setFillColor(Color(min(1, color.red + 0.3), min(1, color.green + 0.3),
                         min(1, color.blue + 0.3), alpha=0.6))
    c.circle(x, y, r * 0.4, fill=1, stroke=0)


def line(c, x1, y1, x2, y2, color=FAINT, w=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x1, y1, x2, y2)


def arrow_line(c, x1, y1, x2, y2, color=TEAL_DIM, w=1.2):
    """Line with small triangular arrow at end."""
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x1, y1, x2 - 5, y2)
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(x2 - 5, y2 - 2.5)
    p.lineTo(x2 + 1, y2)
    p.lineTo(x2 - 5, y2 + 2.5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def card(c, x, y, w, h, fill_c=CARD):
    """Rounded card with subtle top-edge highlight."""
    c.setFillColor(fill_c)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
    # Top edge glow line
    c.setStrokeColor(Color(0.18, 0.30, 0.45, alpha=0.35))
    c.setLineWidth(0.5)
    c.line(x + 5, y + h, x + w - 5, y + h)


def pill(c, x, y, text, color=TEAL, font="SourceCode", size=6.5):
    """Colored pill label."""
    tw = pdfmetrics.stringWidth(text, font, size) + 12
    c.setFillColor(Color(color.red, color.green, color.blue, alpha=0.15))
    c.roundRect(x, y - 3, tw, 14, 3, fill=1, stroke=0)
    c.setStrokeColor(Color(color.red, color.green, color.blue, alpha=0.25))
    c.setLineWidth(0.4)
    c.roundRect(x, y - 3, tw, 14, 3, fill=0, stroke=1)
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x + 6, y, text)
    return tw


def section_label(c, text, y=None):
    """Section header label (teal uppercase mono)."""
    if y is None:
        y = H - 42
    c.setFillColor(TEAL)
    c.setFont("SourceCode", 7)
    c.drawString(60, y, text)


def title(c, text, y=None):
    """Main slide title."""
    if y is None:
        y = H - 78
    c.setFillColor(WHITE)
    c.setFont("DINBold", 30)
    c.drawString(60, y, text)


def page_num(c, num):
    """Page number in bottom right."""
    c.setFillColor(FAINT)
    c.setFont("SourceCodeLight", 6)
    c.drawRightString(W - 32, 22, f"{num:02d} / 08")


def footer_text(c, text):
    """Faint footer text."""
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(60, 22, text)


# ── SLIDE 1: PORTADA ────────────────────────────────────────

def slide_01(c):
    bg(c)
    meridians(c, seed=15, count=8, opacity=0.14)

    # Network constellation — upper right
    stars = [
        (520, 460, 3.5), (600, 420, 2.5), (710, 450, 4), (800, 410, 3),
        (870, 445, 2.5), (640, 490, 2), (760, 480, 3), (900, 470, 2),
        (550, 380, 2), (680, 370, 3), (790, 360, 2.5), (870, 380, 2),
        (620, 340, 2), (740, 330, 2.5), (850, 340, 2),
    ]
    # Connections
    conns = [(0,1),(1,2),(2,3),(3,4),(5,6),(6,7),(1,5),(2,6),(3,7),
             (8,9),(9,10),(10,11),(12,13),(13,14),(1,9),(3,10),(6,13)]
    for a, b in conns:
        c.setStrokeColor(Color(0.10, 0.28, 0.24, alpha=0.20))
        c.setLineWidth(0.5)
        mx = (stars[a][0] + stars[b][0]) / 2
        my = (stars[a][1] + stars[b][1]) / 2 + 20
        p = c.beginPath()
        p.moveTo(stars[a][0], stars[a][1])
        p.curveTo(stars[a][0], my, stars[b][0], my, stars[b][0], stars[b][1])
        c.drawPath(p, fill=0, stroke=1)
    for x, y, r in stars:
        node(c, x, y, r, color=TEAL_DIM)

    # Title cluster — left side
    node(c, 44, 322, 6, color=TEAL)
    c.setFillColor(WHITE)
    c.setFont("DINBold", 48)
    c.drawString(62, 300, "Clara")
    c.setFillColor(TEAL)
    c.setFont("Futura", 14)
    c.drawString(62, 278, "CivicAid Voice")
    c.setFillColor(MUTED)
    c.setFont("Georgia", 11)
    c.drawString(62, 256, "Traducimos la burocracia a tu lengua")

    # Thin horizontal rule
    line(c, 62, 240, 340, 240, color=FAINT, w=0.4)

    # KPI cards
    kpis = [("3.2M", "inmigrantes"), ("9.5M", "mayores de 65"),
            ("4.5M", "exclusion social"), ("78%", "usa WhatsApp")]
    for i, (num, lbl) in enumerate(kpis):
        bx = 62 + i * 128
        card(c, bx, 185, 118, 44)
        c.setFillColor(TEAL if i < 3 else AMBER)
        c.setFont("DINCondBold", 21)
        c.drawString(bx + 10, 206, num)
        c.setFillColor(MUTED)
        c.setFont("SourceCode", 6.5)
        c.drawString(bx + 10, 192, lbl)

    # Bottom info
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6.5)
    c.drawString(62, 158, "ODISEIA4GOOD HACKATHON  /  SPRINT 3  /  13 FEB 2026")
    c.setFont("SourceCodeLight", 6.5)
    c.drawString(62, 145, "UDIT  /  Taller de Proyectos II  /  Dr. Gustavo Bermejo Martin")
    c.setFillColor(MUTED)
    c.setFont("Verdana-R", 7.5)
    c.drawString(62, 125, "Robert (PM)  /  Marcos  /  Daniel  /  Andrea  /  Lucas")

    page_num(c, 1)


# ── SLIDE 2: FUNCIONALIDADES ────────────────────────────────

def slide_02(c):
    bg(c)
    meridians(c, seed=50, opacity=0.10)
    section_label(c, "01  FUNCIONALIDADES")
    title(c, "Que hace Clara hoy")

    features = [
        ("01", "Chat multilingue", "ES + FR", "Deteccion automatica de idioma\ncon langdetect", TEAL),
        ("02", "Voz STT + TTS", "Gemini + gTTS", "Audio entrada y salida\ncompleto en pipeline", TEAL),
        ("03", "Cache inteligente", "8 respuestas", "Respuesta en <2 segundos\ncon audio pre-generado", AMBER),
        ("04", "Pipeline 11 skills", "Modular", "Orquestador resiliente\ncon fallback automatico", AMBER),
    ]
    cw, ch, gap = 200, 135, 14
    sx = 60
    sy = H - 228

    for i, (num, ttl, tag, desc, col) in enumerate(features):
        x = sx + i * (cw + gap)
        card(c, x, sy, cw, ch)
        # Number
        c.setFillColor(col)
        c.setFont("DINCondBold", 36)
        c.drawString(x + 12, sy + ch - 40, num)
        # Title
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 10.5)
        c.drawString(x + 12, sy + ch - 60, ttl)
        # Pill
        pill(c, x + 12, sy + ch - 77, tag, color=col)
        # Desc (multiline)
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7)
        for j, dl in enumerate(desc.split("\n")):
            c.drawString(x + 12, sy + 22 - j * 11, dl)
        # Accent node
        node(c, x + cw - 14, sy + 14, 3, color=col)

    # Quality bar
    qy = sy - 48
    line(c, 60, qy + 18, W - 60, qy + 18, color=FAINT, w=0.3)
    c.setFillColor(TEAL_DIM)
    c.setFont("SourceCode", 6.5)
    c.drawString(60, qy + 24, "CALIDAD")

    quals = [
        ("Guardrails", "6 red team tests — 100% bloqueo", TEAL),
        ("96 tests", "85 unit + 7 integration + 4 e2e", TEAL),
        ("Observabilidad", "JSON logs + request_id + timings", TEAL),
    ]
    for i, (t, d, col) in enumerate(quals):
        qx = 60 + i * 290
        node(c, qx + 3, qy - 2, 3, color=col)
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 8)
        c.drawString(qx + 12, qy - 5, t)
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7)
        c.drawString(qx + 12, qy - 18, d)

    footer_text(c, "SPRINT 4:  Lector de documentos  /  Canal web  /  Elegibilidad proactiva")
    page_num(c, 2)


# ── SLIDE 3: ARQUITECTURA ───────────────────────────────────

def slide_03(c):
    bg(c)
    meridians(c, seed=95, opacity=0.10)
    section_label(c, "02  ARQUITECTURA")
    title(c, "Stack 100% gratuito")

    # Pipeline flow — centered horizontal
    py = H - 158
    pipe = [
        ("WhatsApp", 90, AMBER), ("Twilio", 210, TEAL), ("Flask", 330, TEAL),
        ("TwiML ACK", 460, TEAL_GLOW), ("Cache", 590, AMBER),
        ("Gemini", 720, TEAL), ("Respuesta", 860, TEAL_GLOW),
    ]
    # Connections
    for i in range(len(pipe) - 1):
        arrow_line(c, pipe[i][1] + 25, py, pipe[i+1][1] - 25, py, color=TEAL_DIM, w=1)
    # Nodes + labels
    for lbl, x, col in pipe:
        node(c, x, py, 7, color=col)
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 7.5)
        c.drawCentredString(x, py + 18, lbl)

    # ACK annotation
    c.setFillColor(TEAL_GLOW)
    c.setFont("SourceCode", 6)
    c.drawCentredString(460, py + 34, "<1 segundo")
    # Background thread branch
    line(c, 460, py - 10, 460, py - 38, color=TEAL_DIM, w=0.8)
    node(c, 460, py - 42, 3, color=TEAL_DIM, glow=False)
    c.setFillColor(MUTED)
    c.setFont("SourceCode", 6)
    c.drawCentredString(460, py - 55, "Background Thread")

    # Software stack — two columns
    ty = 182
    line(c, 60, ty + 8, 500, ty + 8, color=FAINT, w=0.3)
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(60, ty + 14, "SOFTWARE STACK")

    stack = [
        ("Python 3.11", "Lenguaje", TEAL), ("Flask 3.1", "Framework", TEAL),
        ("Gemini 1.5 Flash", "LLM + STT", TEAL), ("gTTS 2.5", "Text-to-Speech", TEAL),
        ("Twilio 9", "WhatsApp API", AMBER), ("Render", "Hosting (Frankfurt)", AMBER),
        ("Docker", "Container", AMBER), ("Pydantic 2", "Validacion", AMBER),
    ]
    for i, (name, role, col) in enumerate(stack):
        col_i = i // 4
        row_i = i % 4
        x = 60 + col_i * 260
        y = ty - 10 - row_i * 22
        node(c, x + 4, y + 3, 2.5, color=col, glow=False)
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 7.5)
        c.drawString(x + 14, y, name)
        c.setFillColor(MUTED)
        c.setFont("SourceCode", 6.5)
        c.drawString(x + 130, y + 1, role)

    # Right side: badges
    # Feature flags
    card(c, W - 215, 122, 175, 38, fill_c=CARD)
    c.setFillColor(AMBER)
    c.setFont("DINCondBold", 20)
    c.drawString(W - 203, 135, "9")
    c.setFillColor(MUTED)
    c.setFont("Verdana-R", 7.5)
    c.drawString(W - 183, 137, "feature flags configurables")

    # Cost badge
    card(c, W - 215, 68, 175, 42, fill_c=CARD)
    c.setFillColor(TEAL_GLOW)
    c.setFont("DINCondBold", 26)
    c.drawCentredString(W - 128, 82, "0 EUR/mes")
    c.setFillColor(MUTED)
    c.setFont("SourceCode", 5.5)
    c.drawCentredString(W - 128, 72, "coste total infraestructura")

    page_num(c, 3)


# ── SLIDE 4: PROCESOS ───────────────────────────────────────

def slide_04(c):
    bg(c)
    meridians(c, seed=140, opacity=0.08)
    section_label(c, "03  PROCESOS")
    title(c, "Flujo paso a paso")

    # --- Flujo A: Texto ---
    fa_y = H - 118
    c.setFillColor(TEAL)
    c.setFont("Verdana-B", 10)
    c.drawString(60, fa_y, "Flujo A  /  Texto WhatsApp")
    pill(c, 290, fa_y - 1, "<2s cache  /  4-8s LLM", color=FAINT, size=6)

    steps_a = ["Usuario escribe", "Twilio POST", "Valida firma",
               "TwiML ACK", "Cache / KB / LLM", "Respuesta"]
    sa_y = fa_y - 42
    sp = 142
    for i, s in enumerate(steps_a):
        x = 75 + i * sp
        col = TEAL_GLOW if i == 3 else (AMBER if i >= 4 else TEAL)
        node(c, x, sa_y, 5.5, color=col)
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.45))
        c.setFont("DINCondBold", 15)
        c.drawCentredString(x, sa_y + 16, str(i + 1))
        c.setFillColor(WHITE)
        c.setFont("SourceCode", 6)
        c.drawCentredString(x, sa_y - 15, s)
        if i < len(steps_a) - 1:
            arrow_line(c, x + 9, sa_y, x + sp - 9, sa_y, color=TEAL_DIM, w=0.8)

    # --- Flujo B: Audio ---
    fb_y = sa_y - 62
    c.setFillColor(AMBER)
    c.setFont("Verdana-B", 10)
    c.drawString(60, fb_y, "Flujo B  /  Audio WhatsApp")
    pill(c, 290, fb_y - 1, "6-12s total", color=FAINT, size=6)

    steps_b = ["Audio in", "Twilio POST", "Valida firma", "TwiML ACK",
               "Fetch audio", "Gemini STT", "Cache/KB/LLM", "Respuesta"]
    sb_y = fb_y - 40
    sp_b = 107
    for i, s in enumerate(steps_b):
        x = 68 + i * sp_b
        if i == 3: col = TEAL_GLOW
        elif i == 5: col = BLUE
        elif i >= 6: col = AMBER
        else: col = TEAL
        node(c, x, sb_y, 4.5, color=col)
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.4))
        c.setFont("DINCondBold", 12)
        c.drawCentredString(x, sb_y + 13, str(i + 1))
        c.setFillColor(WHITE)
        c.setFont("SourceCode", 5.5)
        c.drawCentredString(x, sb_y - 13, s)
        if i < len(steps_b) - 1:
            arrow_line(c, x + 7, sb_y, x + sp_b - 7, sb_y, color=TEAL_DIM, w=0.6)

    # TwiML ACK box
    bx_y = 38
    card(c, 60, bx_y, W - 120, 58, fill_c=CARD)
    # Left accent bar
    c.setFillColor(TEAL_GLOW)
    c.rect(60, bx_y, 3, 58, fill=1, stroke=0)
    c.setFont("Verdana-B", 9)
    c.drawString(78, bx_y + 40, "Patron TwiML ACK")
    c.setFillColor(MUTED)
    c.setFont("Verdana-R", 7.5)
    c.drawString(78, bx_y + 24,
                 "Respuesta HTTP 200 inmediata. Procesamiento en hilo de fondo. Envio final via Twilio REST.")
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(78, bx_y + 10,
                 "Sin este patron, el timeout de Twilio (15s) impediria procesar audio + LLM de forma fiable.")

    page_num(c, 4)


# ── SLIDE 5: VENTAJAS Y LIMITACIONES ────────────────────────

def slide_05(c):
    bg(c)
    meridians(c, seed=185, opacity=0.08)
    section_label(c, "04-05  VENTAJAS Y LIMITACIONES")
    title(c, "Pros y contras honestos")

    top = H - 115
    # Divider
    line(c, W / 2, top + 8, W / 2, 48, color=FAINT, w=0.4)

    # ─ Left: Ventajas ─
    lx = 60
    c.setFillColor(TEAL)
    c.setFont("Verdana-B", 10)
    c.drawString(lx, top, "Ventajas")

    ventajas = [
        ("Accesible", "WhatsApp + audio para quien no sabe leer"),
        ("Multilingue", "ES + FR nativos, deteccion automatica"),
        ("Coste cero", "Render + Gemini + gTTS = 0 EUR/mes"),
        ("Cache rapido", "8 respuestas pre-calculadas en <2s"),
        ("96 tests", "Battle-tested: unit + integration + e2e"),
        ("Guardrails", "Pre-check + post-check, 6 red team OK"),
    ]
    for i, (t, d) in enumerate(ventajas):
        vy = top - 28 - i * 44
        node(c, lx + 5, vy + 4, 3.5, color=TEAL)
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 8.5)
        c.drawString(lx + 18, vy, t)
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7)
        c.drawString(lx + 18, vy - 14, d)

    # ─ Right: Limitaciones ─
    rx = W / 2 + 25
    c.setFillColor(AMBER)
    c.setFont("Verdana-B", 10)
    c.drawString(rx, top, "Limitaciones")
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(rx + 105, top + 2, "con mitigacion")

    limits = [
        ("KB estatica", "3 JSONs", "RAG flag preparado, extensible"),
        ("Gemini API", "Dependencia", "Cache-first + fallback templates"),
        ("Cold start", "~30s", "Cron cada 14 min activo"),
        ("Sandbox", "Requiere join", "Migracion trivial: 1 variable"),
        ("2 idiomas", "ES + FR", "Extensible por configuracion"),
        ("Sin web", "Solo WhatsApp", "Canal web en Sprint 4"),
    ]
    for i, (t, tag, mit) in enumerate(limits):
        vy = top - 28 - i * 44
        node(c, rx + 5, vy + 4, 3.5, color=AMBER)
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 8.5)
        c.drawString(rx + 18, vy, t)
        # Tag pill beside title
        tw = pdfmetrics.stringWidth(t, "Verdana-B", 8.5)
        pill(c, rx + 22 + tw, vy - 1, tag, color=AMBER)
        # Mitigation
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7)
        c.drawString(rx + 18, vy - 14, mit)

    # Footer
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6.5)
    c.drawCentredString(W / 2, 30, "Todas las limitaciones son del prototipo, no de la arquitectura")
    page_num(c, 5)


# ── SLIDE 6: PROTOTIPO Y ESCALABILIDAD ──────────────────────

def slide_06(c):
    bg(c)
    meridians(c, seed=230, opacity=0.08)
    section_label(c, "06-07  PROTOTIPO Y ESCALABILIDAD")
    title(c, "De prototipo a producto")

    # URL card
    card(c, 60, H - 180, 420, 78, fill_c=CARD)
    c.setFillColor(TEAL)
    c.rect(60, H - 180, 3, 78, fill=1, stroke=0)  # Accent bar
    c.setFont("SourceCodeBold", 9)
    c.drawString(78, H - 118, "civicaid-voice.onrender.com")
    c.setFillColor(MUTED)
    c.setFont("Verdana-R", 7)
    c.drawString(78, H - 135, "/health  ->  8 componentes OK  |  cache_entries: 8  |  tramites: 3")
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(78, H - 150, "twilio_configured: true  |  demo_mode: true  |  guardrails_on: true")
    # LIVE badge
    c.setFillColor(TEAL_MID)
    c.roundRect(410, H - 132, 48, 18, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("SourceCodeBold", 7)
    c.drawCentredString(434, H - 127, "LIVE")

    # Scalability table
    tt = H - 215
    line(c, 60, tt + 4, W - 60, tt + 4, color=FAINT, w=0.3)
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(60, tt + 10, "ESCALABILIDAD")

    # Col headers
    cols_h = [("Aspecto", 60), ("Hoy (0 EUR)", 230), ("Futuro (~200 EUR)", 500)]
    for lbl, x in cols_h:
        c.setFillColor(MUTED)
        c.setFont("SourceCode", 6.5)
        c.drawString(x, tt - 14, lbl)
    line(c, 60, tt - 18, W - 60, tt - 18, color=FAINT, w=0.3)

    rows = [
        ("Servidor", "Render free (512 MB)", "GCP Cloud Run (auto-scale)"),
        ("LLM", "Gemini 1.5 Flash free", "Gemini Pro fine-tuned"),
        ("KB", "3 JSONs estaticos", "RAG + vector DB (Pinecone)"),
        ("Idiomas", "2 (ES, FR)", "6+ con fine-tuning"),
        ("Canales", "WhatsApp sandbox", "WhatsApp Business + Web + Telegram"),
        ("Usuarios", "~10 concurrentes", "10,000+"),
        ("Tests", "96 automatizados", "200+ con CI/CD"),
    ]
    for i, (asp, now, fut) in enumerate(rows):
        ry = tt - 32 - i * 19
        if i % 2 == 0:
            c.setFillColor(Color(0.04, 0.08, 0.15, alpha=0.5))
            c.rect(55, ry - 4, W - 115, 17, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Verdana-R", 7)
        c.drawString(60, ry, asp)
        c.setFillColor(TEAL)
        c.setFont("SourceCode", 6.5)
        c.drawString(230, ry + 1, now)
        c.setFillColor(AMBER)
        c.setFont("SourceCode", 6.5)
        c.drawString(500, ry + 1, fut)

    # Cost projection row
    cy = 48
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(60, cy + 18, "COSTE PROYECTADO")
    costs = [("<100 users", "0 EUR", TEAL), ("1K users", "~50 EUR", AMBER),
             ("10K users", "~200 EUR", AMBER), ("100K users", "~1,500 EUR", CORAL)]
    for i, (scale, cost, col) in enumerate(costs):
        cx = 80 + i * 215
        card(c, cx, cy - 5, 195, 20, fill_c=CARD)
        c.setFillColor(MUTED)
        c.setFont("SourceCode", 6.5)
        c.drawString(cx + 8, cy, scale)
        c.setFillColor(col)
        c.setFont("Verdana-B", 8)
        c.drawRightString(cx + 187, cy, cost)

    page_num(c, 6)


# ── SLIDE 7: PUNTOS DESTACABLES ─────────────────────────────

def slide_07(c):
    bg(c)
    meridians(c, seed=275, opacity=0.08)
    section_label(c, "08  PUNTOS DESTACABLES")
    title(c, "Lo que nos hace diferentes")

    # 3 persona cards
    personas = [
        ("Maria", "ES", "45 anos, espanola, vulnerabilidad economica",
         "IMV: requisitos, cuantias, telefonos", TEAL),
        ("Ahmed", "FR", "32 anos, inmigrante marroqui, francofono",
         "Audio FR -> respuesta completa en frances", AMBER),
        ("Laura", "ES", "28 anos, recien mudada a Madrid",
         "Tarjeta sanitaria en <2 segundos", TEAL),
    ]
    cw, ch = 275, 100
    sy = H - 200

    for i, (name, lang, profile, result, col) in enumerate(personas):
        x = 60 + i * (cw + 12)
        card(c, x, sy, cw, ch)
        c.setFillColor(col)
        c.rect(x, sy, 3, ch, fill=1, stroke=0)  # Left accent bar
        # Name
        c.setFont("DINBold", 20)
        c.drawString(x + 14, sy + ch - 28, name)
        # Lang pill
        nw = pdfmetrics.stringWidth(name, "DINBold", 20)
        pill(c, x + 18 + nw, sy + ch - 29, lang, color=col)
        # Profile
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7)
        c.drawString(x + 14, sy + ch - 46, profile)
        # Result
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 7.5)
        c.drawString(x + 14, sy + 16, result)
        # Node
        node(c, x + cw - 14, sy + ch - 18, 3.5, color=col)

    # KPI row
    ky = sy - 50
    line(c, 60, ky + 14, W - 60, ky + 14, color=FAINT, w=0.3)
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawString(60, ky + 20, "SPRINT 3 EN NUMEROS")

    kpis = [("0", "EUR/mes", TEAL), ("1", "canal", TEAL), ("2", "idiomas", TEAL),
            ("3", "tramites", AMBER), ("11", "skills", AMBER),
            ("16", "commits", BLUE), ("96", "tests", TEAL_GLOW), ("36h", "desarrollo", AMBER)]
    for i, (num, lbl, col) in enumerate(kpis):
        kx = 68 + i * 109
        card(c, kx, ky - 30, 98, 40, fill_c=CARD)
        c.setFillColor(col)
        c.setFont("DINCondBold", 22)
        c.drawCentredString(kx + 49, ky - 6, num)
        c.setFillColor(MUTED)
        c.setFont("SourceCode", 6)
        c.drawCentredString(kx + 49, ky - 22, lbl)

    # Momento WOW
    wy = ky - 70
    c.setFillColor(TEAL_GLOW)
    c.setFont("Verdana-B", 10)
    c.drawString(60, wy, "Momento WOW")
    node(c, 66, wy - 22, 3.5, color=TEAL)
    c.setFillColor(WHITE)
    c.setFont("Verdana-R", 8)
    c.drawString(80, wy - 25, "WOW 1  /  Texto: respuesta verificada en <3 segundos")
    node(c, 66, wy - 44, 3.5, color=AMBER)
    c.setFillColor(WHITE)
    c.setFont("Verdana-R", 8)
    c.drawString(80, wy - 47, "WOW 2  /  Audio frances: transcripcion + respuesta en frances con audio")

    footer_text(c, "DATOS INE:  3.2M inmigrantes  |  9.5M mayores 65  |  4.5M exclusion  |  78% WhatsApp")
    page_num(c, 7)


# ── SLIDE 8: SCRUM + CRITERIOS ──────────────────────────────

def slide_08(c):
    bg(c)
    meridians(c, seed=320, opacity=0.08)
    section_label(c, "SPRINT REVIEW + CRITERIOS DEL JURADO")
    title(c, "Scrum y evaluacion")

    # ─ Left: Checkpoints timeline ─
    lx = 60
    cy = H - 115
    c.setFillColor(MUTED)
    c.setFont("SourceCode", 6)
    c.drawString(lx, cy, "CHECKPOINTS")

    sprints = [
        ("S1", "30 Ene", "Planificacion", "COMPLETADO", TEAL),
        ("S2", "6 Feb", "Doc tecnico + repo", "COMPLETADO", TEAL),
        ("S3", "13 Feb", "MVP + doc v2", "HOY", TEAL_GLOW),
        ("S4", "20 Feb", "Demo final", "PROXIMO", FAINT),
    ]
    for i, (sp, date, goal, status, col) in enumerate(sprints):
        sy = cy - 24 - i * 34
        node(c, lx + 6, sy + 4, 4.5, color=col)
        if i < len(sprints) - 1:
            line(c, lx + 6, sy - 2, lx + 6, sy - 26, color=TEAL_DIM, w=0.7)
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 8.5)
        c.drawString(lx + 20, sy, f"{sp}  /  {date}")
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7.5)
        c.drawString(lx + 145, sy, goal)
        pill(c, lx + 290, sy - 1, status, color=col)

    # ─ Changes vs Sprint 2 ─
    chg_y = cy - 170
    c.setFillColor(AMBER)
    c.setFont("SourceCode", 6.5)
    c.drawString(lx, chg_y, "CAMBIOS VS SPRINT 2")

    cambios = [
        ("Web + WhatsApp", "Solo WhatsApp (web Sprint 4)"),
        ("Whisper small", "Gemini Flash transcription"),
        ("HuggingFace", "Render.com (Docker)"),
        ("4 idiomas", "2 probados (ES, FR)"),
        ("Mockup", "Producto real desplegado"),
        ("0 tests", "96 tests"),
    ]
    for i, (antes, ahora) in enumerate(cambios):
        ry = chg_y - 16 - i * 16
        c.setFillColor(FAINT)
        c.setFont("SourceCode", 6.5)
        c.drawString(lx + 8, ry, antes)
        c.setFillColor(TEAL_DIM)
        c.setFont("SourceCode", 6.5)
        tw_a = pdfmetrics.stringWidth(antes, "SourceCode", 6.5)
        c.drawString(lx + 14 + tw_a, ry, "->")
        c.setFillColor(WHITE)
        c.setFont("SourceCode", 6.5)
        c.drawString(lx + 190, ry, ahora)

    # ─ Right: Jury criteria cards ─
    rx = W / 2 + 35
    # Divider
    line(c, W / 2 + 15, H - 105, W / 2 + 15, 40, color=FAINT, w=0.4)

    jy = H - 115
    c.setFillColor(MUTED)
    c.setFont("SourceCode", 6)
    c.drawString(rx, jy, "CRITERIOS DEL JURADO")

    criteria = [
        ("30%", "Innovacion", "Pipeline 11 skills + TwiML ACK\n+ guardrails + evals automatizadas", TEAL),
        ("30%", "Impacto Social", "WhatsApp audio para no alfabetizados\n+ multilingue nativo ES/FR", AMBER),
        ("20%", "Viabilidad", "Desplegado en Render, 96 tests PASS\n0 EUR, Docker, /health OK", TEAL),
        ("20%", "Presentacion", "Demo en vivo WhatsApp\n+ WOW texto + WOW audio frances", AMBER),
    ]
    card_h = 72
    for i, (pct, name, evidence, col) in enumerate(criteria):
        ey = jy - 28 - i * (card_h + 8)
        card(c, rx, ey, W / 2 - 75, card_h, fill_c=CARD)
        c.setFillColor(col)
        c.rect(rx, ey, 3, card_h, fill=1, stroke=0)  # Left accent
        # Percentage
        c.setFont("DINCondBold", 28)
        c.drawString(rx + 12, ey + card_h - 32, pct)
        # Name
        c.setFillColor(WHITE)
        c.setFont("Verdana-B", 10.5)
        c.drawString(rx + 62, ey + card_h - 25, name)
        # Evidence (multiline)
        c.setFillColor(MUTED)
        c.setFont("Verdana-R", 7)
        for j, el in enumerate(evidence.split("\n")):
            c.drawString(rx + 62, ey + card_h - 42 - j * 11, el)

    # Footer
    c.setFillColor(FAINT)
    c.setFont("SourceCode", 6)
    c.drawCentredString(W / 2, 22, "CivicAid Voice / Clara  —  UDIT  —  OdiseIA4Good 2026")
    page_num(c, 8)


# ── MAIN ────────────────────────────────────────────────────

def main():
    c = canvas.Canvas(OUT_PATH, pagesize=(W, H))
    c.setTitle("CivicAid Voice / Clara — Sprint 3")
    c.setAuthor("Equipo Clara — UDIT")
    c.setSubject("Presentacion academica Sprint 3 — Taller de Proyectos II")

    slides = [slide_01, slide_02, slide_03, slide_04,
              slide_05, slide_06, slide_07, slide_08]
    for i, fn in enumerate(slides):
        fn(c)
        if i < len(slides) - 1:
            c.showPage()
    c.save()
    print(f"PDF generado: {OUT_PATH}")
    print(f"Paginas: {len(slides)}")
    print(f"Tamano: {os.path.getsize(OUT_PATH) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
