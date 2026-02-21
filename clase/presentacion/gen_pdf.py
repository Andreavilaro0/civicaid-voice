#!/usr/bin/env python3
"""Generate Clara presentation as image-heavy PDF."""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = os.path.dirname(__file__)
W, H = 1920, 1080

# ── Colors ──
DARK = (10, 10, 10)
DARK2 = (18, 18, 18)
DARK3 = (30, 30, 30)
TRUST = (27, 94, 123)
HOPE = (46, 125, 79)
WARMTH = (212, 106, 30)
ALERT = (198, 40, 40)
WHITE = (250, 250, 249)
MUTED = (150, 150, 150)
LIGHT = (200, 200, 200)
BLUE_BUBBLE = (227, 242, 253)

# ── Fonts ──
FONT_DIR = "/System/Library/Fonts/Supplemental"
def font(name, size):
    try:
        return ImageFont.truetype(f"{FONT_DIR}/{name}", size)
    except:
        return ImageFont.load_default()

F_DISPLAY = lambda s: font("Georgia Bold.ttf", s)
F_SERIF = lambda s: font("Georgia.ttf", s)
F_SANS = lambda s: font("Arial.ttf", s)
F_SANS_B = lambda s: font("Arial Bold.ttf", s)
F_NARROW = lambda s: font("Arial Narrow.ttf", s)
F_NARROW_B = lambda s: font("Arial Narrow Bold.ttf", s)

slides = []

def new_slide(bg=DARK):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)

def rounded_rect(draw, xy, fill, radius=20):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def draw_glow(img, cx, cy, radius, color, alpha=30):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -2):
        a = int(alpha * (r / radius))
        od.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=(*color, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))

def draw_clara_logo(draw, cx, cy, scale=1.0, color=TRUST, dot_color=WARMTH):
    """Draw Clara logo (3 arcs + dot)."""
    s = scale
    # Outer arc
    for i, (r, op) in enumerate([(int(30*s), 90), (int(20*s), 160), (int(10*s), 255)]):
        c = tuple(int(v * op / 255) + int((10) * (1 - op / 255)) for v in color)
        draw.arc([cx - r, cy - r, cx + r, cy + r], -90, 90,
                 fill=c, width=max(2, int(4 * s)))
    # Center dot
    dr = int(5.5 * s)
    draw.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=dot_color)

def center_text(draw, text, y, fnt, color=WHITE):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=color)

def draw_phone(img, draw, px, py, pw, ph, messages, header_text="Clara"):
    """Draw a phone mockup with chat messages."""
    # Phone frame
    rounded_rect(draw, [px, py, px + pw, py + ph], fill=(28, 28, 30), radius=36)
    # Inner border
    rounded_rect(draw, [px + 2, py + 2, px + pw - 2, py + ph - 2], fill=(58, 58, 60), radius=35)
    rounded_rect(draw, [px + 4, py + 4, px + pw - 4, py + ph - 4], fill=(28, 28, 30), radius=34)

    # Screen
    sx, sy = px + 10, py + 10
    sw, sh = pw - 20, ph - 20
    rounded_rect(draw, [sx, sy, sx + sw, sy + sh], fill=(250, 250, 250), radius=28)

    # Header
    rounded_rect(draw, [sx, sy, sx + sw, sy + 52], fill=TRUST, radius=0)
    # Top corners
    draw.rounded_rectangle([sx, sy, sx + sw, sy + 30], radius=28, fill=TRUST)
    draw.text((sx + 16, sy + 18), f"←  {header_text}", font=F_SANS_B(16), fill=WHITE)
    draw.text((sx + sw - 55, sy + 18), "ES | FR", font=F_NARROW(12), fill=(200, 220, 240))

    # Messages
    my = sy + 60
    for is_user, text in messages:
        lines = text.split("\n")
        line_h = 16
        bh = len(lines) * line_h + 16
        max_bw = int(sw * 0.78)

        if is_user:
            bx = sx + sw - max_bw - 12
            bg = TRUST
            tc = WHITE
        else:
            bx = sx + 12
            bg = BLUE_BUBBLE
            tc = (26, 26, 26)

        # Measure actual width
        actual_w = max(draw.textbbox((0, 0), line, font=F_SANS(12))[2] for line in lines) + 24
        actual_w = min(actual_w, max_bw)

        if is_user:
            bx = sx + sw - actual_w - 12

        rounded_rect(draw, [bx, my, bx + actual_w, my + bh], fill=bg, radius=12)

        for j, line in enumerate(lines):
            draw.text((bx + 12, my + 8 + j * line_h), line, font=F_SANS(12), fill=tc)

        my += bh + 8
        if my > sy + sh - 50:
            break

    # Input bar
    iy = sy + sh - 44
    draw.rectangle([sx, iy, sx + sw, sy + sh], fill=(255, 255, 255))
    draw.line([(sx, iy), (sx + sw, iy)], fill=(230, 230, 230), width=1)
    rounded_rect(draw, [sx + 12, iy + 8, sx + sw - 50, iy + 36], fill=(245, 245, 245), radius=18)
    draw.text((sx + 24, iy + 14), "Escribe un mensaje...", font=F_SANS(11), fill=(180, 180, 180))


# ════════════════════════════════════════════
# SLIDE 1: COVER
# ════════════════════════════════════════════
img, d = new_slide()
draw_glow(img, 400, 300, 350, TRUST, 20)
draw_glow(img, 1500, 700, 300, WARMTH, 15)
d = ImageDraw.Draw(img)

center_text(d, "Andrea Avila", 100, F_NARROW(18), MUTED)
draw_clara_logo(d, W // 2, 280, scale=3.5)
center_text(d, "Clara", 380, F_DISPLAY(120), WHITE)
center_text(d, "Tu voz tiene poder", 520, F_SERIF(36), MUTED)

# Pills
pills = ["WhatsApp-first", "Voz + Texto + Foto", "ES / FR"]
total_w = sum(d.textbbox((0, 0), p, font=F_SANS(16))[2] + 40 for p in pills) + 30 * (len(pills) - 1)
px = (W - total_w) // 2
for pill in pills:
    tw = d.textbbox((0, 0), pill, font=F_SANS(16))[2] + 40
    rounded_rect(d, [px, 640, px + tw, 680], fill=DARK2, radius=20)
    d.rounded_rectangle([px, 640, px + tw, 680], radius=20, outline=DARK3, width=1)
    d.text((px + 20, 648), pill, font=F_SANS(16), fill=LIGHT)
    px += tw + 30

center_text(d, "OdiseIA4Good  ·  UDIT  ·  Febrero 2026", 900, F_NARROW(16), MUTED)
slides.append(img)


# ════════════════════════════════════════════
# SLIDE 2: PROBLEMA
# ════════════════════════════════════════════
img, d = new_slide()
draw_glow(img, W // 2, 350, 400, WARMTH, 20)
d = ImageDraw.Draw(img)

center_text(d, "EL PROBLEMA", 60, F_NARROW_B(16), MUTED)
center_text(d, "11.4M", 140, F_DISPLAY(140), WARMTH)
center_text(d, "personas en riesgo de exclusion social en Espana", 310, F_SANS(26), LIGHT)

# Stat cards
stats = [
    ("73%", "no completa tramites\npor barreras digitales", ALERT),
    ("40%", "no habla espanol\ncomo lengua materna", TRUST),
    ("87%", "usa WhatsApp\na diario", HOPE),
]
for i, (num, label, color) in enumerate(stats):
    cx = 260 + i * 500
    rounded_rect(d, [cx, 430, cx + 400, 630], fill=DARK2, radius=20)
    d.rounded_rectangle([cx, 430, cx + 400, 630], radius=20, outline=DARK3, width=1)
    # Color bar top
    d.rounded_rectangle([cx, 430, cx + 400, 438], radius=0, fill=color)

    nf = F_DISPLAY(64)
    nb = d.textbbox((0, 0), num, font=nf)
    nw = nb[2] - nb[0]
    d.text((cx + (400 - nw) // 2, 450), num, font=nf, fill=color)

    lines = label.split("\n")
    for j, line in enumerate(lines):
        lb = d.textbbox((0, 0), line, font=F_SANS(16))
        lw = lb[2] - lb[0]
        d.text((cx + (400 - lw) // 2, 545 + j * 22), line, font=F_SANS(16), fill=MUTED)

center_text(d, "Las ayudas existen. Entre el papel y la persona hay un muro.", 720, F_SERIF(24), (120, 120, 120))

# Visual: wall metaphor
for i in range(20):
    bx = 200 + i * 76
    rounded_rect(d, [bx, 810, bx + 70, 850], fill=DARK3, radius=4)
for i in range(19):
    bx = 238 + i * 76
    rounded_rect(d, [bx, 860, bx + 70, 900], fill=DARK3, radius=4)
center_text(d, "FORMULARIOS    IDIOMAS    BUROCRACIA    DIGITAL", 920, F_NARROW(14), (80, 80, 80))

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 3: PERSONAS
# ════════════════════════════════════════════
img, d = new_slide()

center_text(d, "PARA QUIEN ES CLARA", 40, F_NARROW_B(16), MUTED)

personas = [
    ("Maria", "74 anos", "Le tiemblan las manos", "No puede teclear bien", "Quiere saber del IMV", "NOTA DE VOZ", WARMTH),
    ("Ahmed", "28 anos", "Habla frances", "Todo esta en espanol", "Necesita empadronarse", "BILINGUE", TRUST),
    ("Fatima", "45 anos", "Habla, no lee espanol", "Necesita tarjeta sanitaria", "Para su hijo", "AUDIO", HOPE),
]

for i, (name, age, l1, l2, l3, tag, color) in enumerate(personas):
    cx = 120 + i * 580
    # Card
    rounded_rect(d, [cx, 100, cx + 520, 580], fill=DARK2, radius=24)
    d.rounded_rectangle([cx, 100, cx + 520, 580], radius=24, outline=DARK3, width=1)

    # Avatar circle
    acx, acy = cx + 80, 200
    d.ellipse([acx - 45, acy - 45, acx + 45, acy + 45], fill=(*color, ))
    d.text((acx - 18, acy - 22), name[0], font=F_DISPLAY(40), fill=WHITE)

    # Name + age
    d.text((acx + 65, 170), name, font=F_SANS_B(28), fill=WHITE)
    d.text((acx + 65, 210), age, font=F_SANS(18), fill=MUTED)

    # Details
    for j, line in enumerate([l1, l2, l3]):
        d.text((cx + 40, 290 + j * 40), "·", font=F_SANS(20), fill=color)
        d.text((cx + 60, 290 + j * 40), line, font=F_SANS(20), fill=LIGHT)

    # Tag
    tw = d.textbbox((0, 0), tag, font=F_NARROW_B(14))[2] + 24
    rounded_rect(d, [cx + 40, 480, cx + 40 + tw, 515], fill=DARK, radius=16)
    d.rounded_rectangle([cx + 40, 480, cx + 40 + tw, 515], radius=16, outline=color, width=1)
    d.text((cx + 52, 488), tag, font=F_NARROW_B(14), fill=color)

# Bottom text
center_text(d, "Clara se adapta a las personas.", 640, F_SERIF(28), WARMTH)

# More vulnerable types
more_types = [
    "Mayores solos", "Inmigrantes sin idioma", "Violencia de genero",
    "Sin hogar", "Discapacidad", "Analfabetismo funcional"
]
mt_text = "  ·  ".join(more_types)
center_text(d, mt_text, 720, F_NARROW(16), (80, 80, 80))

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 4: USER JOURNEY
# ════════════════════════════════════════════
img, d = new_slide()

center_text(d, "EJEMPLO: MARIA SOLICITA EL IMV", 40, F_NARROW_B(16), MUTED)

steps = [
    ("1", "Abre WhatsApp", "Lo que ya tiene\nen el movil", WARMTH),
    ("2", "Nota de voz", '"Quiero saber\ndel IMV"', HOPE),
    ("3", "Whisper + Gemini", "Transcribe,\nentiende, busca", TRUST),
    ("4", "Respuesta + audio", "Texto claro\n+ nota de voz", HOPE),
    ("5", "Sabe que hacer", "Paso concreto\npara manana", HOPE),
]

# Timeline
d.line([(180, 300), (1740, 300)], fill=DARK3, width=3)

for i, (num, label, desc, color) in enumerate(steps):
    cx = 180 + i * 390

    # Circle
    d.ellipse([cx - 45, 255, cx + 45, 345], fill=DARK, outline=color, width=3)
    nb = d.textbbox((0, 0), num, font=F_DISPLAY(36))
    nw = nb[2] - nb[0]
    d.text((cx - nw // 2, 270), num, font=F_DISPLAY(36), fill=color)

    # Label
    lb = d.textbbox((0, 0), label, font=F_SANS_B(20))
    lw = lb[2] - lb[0]
    d.text((cx - lw // 2, 370), label, font=F_SANS_B(20), fill=WHITE)

    # Desc
    lines = desc.split("\n")
    for j, line in enumerate(lines):
        db = d.textbbox((0, 0), line, font=F_SANS(16))
        dw = db[2] - db[0]
        d.text((cx - dw // 2, 410 + j * 22), line, font=F_SANS(16), fill=MUTED)

    # Arrow
    if i < len(steps) - 1:
        ax = cx + 150
        d.polygon([(ax, 295), (ax + 15, 300), (ax, 305)], fill=color)

center_text(d, "< 30 segundos  ·  Sin apps  ·  Sin formularios  ·  Sin esperas", 540, F_SANS(20), (100, 100, 100))

# Bottom: more use cases visual
use_cases = [
    ("IMV", WARMTH), ("Empadronamiento", TRUST), ("Tarjeta sanitaria", HOPE),
    ("NIE / TIE", TRUST), ("Reagrupacion familiar", WARMTH), ("Ayudas vivienda", HOPE),
    ("Becas", TRUST), ("016 violencia", ALERT),
]
ucx = 200
for uc, color in use_cases:
    tw = d.textbbox((0, 0), uc, font=F_NARROW(15))[2] + 28
    rounded_rect(d, [ucx, 680, ucx + tw, 712], fill=DARK2, radius=16)
    d.rounded_rectangle([ucx, 680, ucx + tw, 712], radius=16, outline=color, width=1)
    d.text((ucx + 14, 688), uc, font=F_NARROW(15), fill=color)
    ucx += tw + 14

center_text(d, "8 bases de conocimiento verificadas con fuentes oficiales", 780, F_NARROW(14), (70, 70, 70))

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 5: DEMO WHATSAPP
# ════════════════════════════════════════════
img, d = new_slide()
draw_glow(img, 1300, 500, 350, HOPE, 15)
d = ImageDraw.Draw(img)

d.text((120, 60), "DEMO", font=F_NARROW_B(16), fill=MUTED)
d.text((120, 120), "Clara en", font=F_DISPLAY(60), fill=WHITE)
d.text((120, 200), "WhatsApp", font=F_DISPLAY(60), fill=WARMTH)

features = [
    ("✓", "Texto, voz o foto de documento"),
    ("✓", "Espanol y frances automatico"),
    ("✓", "Audio para quienes no leen"),
    ("✓", "Guardrails de seguridad"),
    ("✓", "Fuentes oficiales verificadas"),
]
for i, (icon, text) in enumerate(features):
    y = 340 + i * 44
    d.text((140, y), icon, font=F_SANS_B(20), fill=HOPE)
    d.text((180, y), text, font=F_SANS(20), fill=LIGHT)

messages = [
    (False, "Hola, soy Clara. Estoy aqui\npara ayudarte con tramites."),
    (True, "Quiero saber que es el IMV"),
    (False, "El IMV es una ayuda economica\npara personas con pocos recursos.\nPuede ser 604-1.200€/mes.\n\n▶ Escuchar respuesta  0:34"),
    (True, "🎙 Nota de voz 0:05"),
    (False, "Para solicitarlo necesitas:\n1. DNI/NIE\n2. Empadronamiento\n3. Declaracion renta"),
]

draw_phone(img, ImageDraw.Draw(img), 1000, 40, 380, 700, messages)

# Bottom note
center_text(d, "90% de los adultos en Espana tienen WhatsApp. Clara llega donde las apps no llegan.", 850, F_NARROW(16), (80, 80, 80))

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 6: DEMO WEB APP
# ════════════════════════════════════════════
img, d = new_slide()
draw_glow(img, 500, 500, 350, TRUST, 15)
d = ImageDraw.Draw(img)

d.text((1050, 60), "INTERFAZ ACCESIBLE", font=F_NARROW_B(16), fill=MUTED)
d.text((1050, 120), "Clara Web", font=F_DISPLAY(60), fill=WHITE)

d.text((1050, 240), "Para trabajadoras sociales,", font=F_SANS(22), fill=MUTED)
d.text((1050, 272), "ONGs y mediadores comunitarios.", font=F_SANS(22), fill=MUTED)

web_features = [
    ("✓", "WCAG AA accesible"),
    ("✓", "Grabacion de voz integrada"),
    ("✓", "Mobile-first"),
    ("✓", "Selector de idioma ES / FR"),
]
for i, (icon, text) in enumerate(web_features):
    y = 360 + i * 44
    d.text((1070, y), icon, font=F_SANS_B(20), fill=HOPE)
    d.text((1110, y), text, font=F_SANS(20), fill=LIGHT)

web_msgs = [
    (False, "Bienvenido/a. Soy Clara,\ntu asistente para tramites."),
    (True, "Como pido la tarjeta sanitaria?"),
    (False, "Para la tarjeta sanitaria:\n\n✅ Empadronamiento\n✅ Pasaporte o NIE\n✅ Centro de salud\n\n▶ Escuchar  0:28"),
]

draw_phone(img, ImageDraw.Draw(img), 200, 40, 380, 700, web_msgs, "Clara Web")

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 7: ARQUITECTURA
# ════════════════════════════════════════════
img, d = new_slide()

center_text(d, "COMO FUNCIONA", 40, F_NARROW_B(16), MUTED)
center_text(d, "Arquitectura", 80, F_DISPLAY(48), WHITE)

nodes = [
    ("WhatsApp\n+ Web", "Texto / Voz\nFoto", HOPE),
    ("Twilio", "Mensajeria\nsegura", TRUST),
    ("Whisper", "Voz → Texto\nOpenAI", WARMTH),
    ("Gemini\n1.5 Flash", "IA generativa\n+ Contexto", TRUST),
    ("KB + RAG", "8 bases\nverificadas", HOPE),
    ("Respuesta", "Texto + Audio\n+ Fuentes", HOPE),
]

for i, (name, desc, color) in enumerate(nodes):
    cx = 100 + i * 290
    # Box
    rounded_rect(d, [cx, 220, cx + 220, 370], fill=DARK2, radius=16)
    d.rounded_rectangle([cx, 220, cx + 220, 370], radius=16, outline=color, width=2)

    # Name
    lines = name.split("\n")
    for j, line in enumerate(lines):
        lb = d.textbbox((0, 0), line, font=F_SANS_B(18))
        lw = lb[2] - lb[0]
        d.text((cx + (220 - lw) // 2, 260 + j * 24), line, font=F_SANS_B(18), fill=WHITE)

    # Desc
    dlines = desc.split("\n")
    for j, line in enumerate(dlines):
        lb = d.textbbox((0, 0), line, font=F_SANS(13))
        lw = lb[2] - lb[0]
        d.text((cx + (220 - lw) // 2, 395 + j * 18), line, font=F_SANS(13), fill=MUTED)

    # Arrow
    if i < len(nodes) - 1:
        ax = cx + 225
        d.line([(ax, 295), (ax + 50, 295)], fill=DARK3, width=2)
        d.polygon([(ax + 45, 290), (ax + 55, 295), (ax + 45, 300)], fill=MUTED)

# Tech pills
techs = ["Python + Flask", "Docker", "Render", "PostgreSQL + pgvector",
         "React + TypeScript", "469 tests", "11 skills", "8 KBs"]
tx = 250
for tech in techs:
    tw = d.textbbox((0, 0), tech, font=F_NARROW(15))[2] + 28
    rounded_rect(d, [tx, 520, tx + tw, 555], fill=DARK2, radius=14)
    d.rounded_rectangle([tx, 520, tx + tw, 555], radius=14, outline=DARK3, width=1)
    d.text((tx + 14, 528), tech, font=F_NARROW(15), fill=MUTED)
    tx += tw + 12

# Extra: guardrails + pipeline
center_text(d, "Pipeline de 11 skills  ·  Guardrails pre/post  ·  Observabilidad  ·  Cache inteligente", 620, F_NARROW(15), (60, 60, 60))

# Bottom diagram: fallback chain
center_text(d, "Cadena de respaldo", 700, F_SANS_B(18), LIGHT)
chain = ["PGVector + BM25", "→", "JSON KB", "→", "Directorio", "→", "Respuesta segura"]
cx = 450
for item in chain:
    if item == "→":
        d.text((cx, 760), item, font=F_SANS(20), fill=MUTED)
        cx += 40
    else:
        tw = d.textbbox((0, 0), item, font=F_SANS(16))[2] + 24
        rounded_rect(d, [cx, 750, cx + tw, 785], fill=DARK2, radius=10)
        d.text((cx + 12, 758), item, font=F_SANS(16), fill=TRUST)
        cx += tw + 16

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 8: IMPACTO
# ════════════════════════════════════════════
img, d = new_slide()
draw_glow(img, W // 2, 300, 400, HOPE, 15)
d = ImageDraw.Draw(img)

center_text(d, "IMPACTO", 40, F_NARROW_B(16), MUTED)

impact_stats = [
    ("2B", "usuarios WhatsApp\nen el mundo", HOPE),
    ("0€", "coste para\nel usuario", TRUST),
    ("<30s", "respuesta\ncon fuentes", WARMTH),
    ("24/7", "disponible\nsiempre", ALERT),
]

for i, (num, label, color) in enumerate(impact_stats):
    cx = 100 + i * 440
    rounded_rect(d, [cx, 100, cx + 380, 320], fill=DARK2, radius=20)
    d.rounded_rectangle([cx, 100, cx + 380, 320], radius=20, outline=DARK3, width=1)
    d.rectangle([cx, 100, cx + 380, 108], fill=color)

    nf = F_DISPLAY(72)
    nb = d.textbbox((0, 0), num, font=nf)
    nw = nb[2] - nb[0]
    d.text((cx + (380 - nw) // 2, 120), num, font=nf, fill=color)

    lines = label.split("\n")
    for j, line in enumerate(lines):
        lb = d.textbbox((0, 0), line, font=F_SANS(16))
        lw = lb[2] - lb[0]
        d.text((cx + (380 - lw) // 2, 230 + j * 22), line, font=F_SANS(16), fill=MUTED)

# Roadmap
roadmap = [
    ("HOY", "IMV, empadronamiento\nsanitaria, NIE/TIE", HOPE),
    ("MANANA", "Todas las CCAA\nde Espana", TRUST),
    ("FUTURO", "LATAM, refugiados\ncualquier idioma", WARMTH),
]
for i, (phase, desc, color) in enumerate(roadmap):
    cx = 250 + i * 500
    # Phase label
    pb = d.textbbox((0, 0), phase, font=F_SANS_B(24))
    pw = pb[2] - pb[0]
    d.text((cx + (300 - pw) // 2, 400), phase, font=F_SANS_B(24), fill=color)

    lines = desc.split("\n")
    for j, line in enumerate(lines):
        lb = d.textbbox((0, 0), line, font=F_SANS(16))
        lw = lb[2] - lb[0]
        d.text((cx + (300 - lw) // 2, 440 + j * 22), line, font=F_SANS(16), fill=MUTED)

    if i < 2:
        d.text((cx + 330, 420), "→", font=F_SANS(30), fill=MUTED)

# Category design quote
center_text(d, "Clara crea una nueva categoria: Civic Tenderness.", 560, F_SERIF(26), WARMTH)
center_text(d, "No compite con chatbots. Redefine como la tecnologia sirve a personas vulnerables.", 610, F_SANS(18), (100, 100, 100))

# Bottom: amplification message
center_text(d, "Clara no reemplaza a los trabajadores sociales. Los amplifica.", 720, F_SERIF(22), LIGHT)

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 9: USOS VULNERABLES
# ════════════════════════════════════════════
img, d = new_slide()

center_text(d, "USOS PARA PERSONAS VULNERABLES", 30, F_NARROW_B(16), MUTED)

use_cases_detail = [
    ("Mayores solos", "IMV, pensiones,\nteleasistencia, citas medicas", "VOZ", WARMTH),
    ("Inmigrantes", "Empadronamiento, NIE,\nreagrupacion familiar", "BILINGUE", TRUST),
    ("Violencia de genero", "016, ordenes proteccion,\nayudas de emergencia", "SEGURO", ALERT),
    ("Sin hogar", "Comedores, albergues,\nrenta social, padrón", "WHATSAPP", HOPE),
    ("Discapacidad", "Certificado, grado,\nayudas tecnicas", "AUDIO", TRUST),
    ("Analfabetismo", "Cualquier tramite\npaso a paso oral", "VOZ 100%", WARMTH),
]

for i, (name, desc, mode, color) in enumerate(use_cases_detail):
    col = i % 3
    row = i // 3
    cx = 80 + col * 600
    cy = 90 + row * 370

    # Card
    rounded_rect(d, [cx, cy, cx + 540, cy + 320], fill=DARK2, radius=20)
    d.rounded_rectangle([cx, cy, cx + 540, cy + 320], radius=20, outline=color, width=2)

    # Color accent bar
    d.rectangle([cx + 20, cy + 20, cx + 26, cy + 80], fill=color)

    # Name
    d.text((cx + 42, cy + 25), name, font=F_SANS_B(26), fill=WHITE)

    # Desc
    lines = desc.split("\n")
    for j, line in enumerate(lines):
        d.text((cx + 42, cy + 80 + j * 28), line, font=F_SANS(18), fill=LIGHT)

    # How Clara helps
    d.text((cx + 42, cy + 170), "Clara ayuda con:", font=F_NARROW(14), fill=MUTED)

    # Mode tag
    tw = d.textbbox((0, 0), mode, font=F_NARROW_B(14))[2] + 24
    rounded_rect(d, [cx + 42, cy + 250, cx + 42 + tw, cy + 282], fill=DARK, radius=14)
    d.rounded_rectangle([cx + 42, cy + 250, cx + 42 + tw, cy + 282], radius=14, outline=color, width=1)
    d.text((cx + 54, cy + 257), mode, font=F_NARROW_B(14), fill=color)

    # Interaction visual
    d.ellipse([cx + 430, cy + 240, cx + 510, cy + 300], fill=(*color,), outline=None)
    d.text((cx + 452, cy + 255), "💬", font=F_SANS(22), fill=WHITE)

slides.append(img)


# ════════════════════════════════════════════
# SLIDE 10: CIERRE
# ════════════════════════════════════════════
img, d = new_slide()
draw_glow(img, W // 2, 400, 500, TRUST, 20)
draw_glow(img, W // 2 + 200, 500, 300, WARMTH, 15)
d = ImageDraw.Draw(img)

# Team
team = [
    ("R", "Robert", "Backend", TRUST),
    ("M", "Marcos", "Deploy", HOPE),
    ("L", "Lucas", "KB + Tests", WARMTH),
    ("D", "Daniel", "Video", TRUST),
    ("A", "Andrea", "Coord", WARMTH),
]

for i, (initial, name, role, color) in enumerate(team):
    cx = 460 + i * 200
    # Circle
    d.ellipse([cx, 160, cx + 65, 225], fill=DARK2, outline=color, width=2)
    ib = d.textbbox((0, 0), initial, font=F_DISPLAY(28))
    iw = ib[2] - ib[0]
    d.text((cx + (65 - iw) // 2, 175), initial, font=F_DISPLAY(28), fill=color)

    nb = d.textbbox((0, 0), name, font=F_SANS(14))
    nw = nb[2] - nb[0]
    d.text((cx + (65 - nw) // 2, 235), name, font=F_SANS(14), fill=LIGHT)

    rb = d.textbbox((0, 0), role, font=F_NARROW(11))
    rw = rb[2] - rb[0]
    d.text((cx + (65 - rw) // 2, 255), role, font=F_NARROW(11), fill=MUTED)

# Big quote
center_text(d, "Tu voz tiene poder.", 380, F_DISPLAY(90), WHITE)

# Logo
draw_clara_logo(d, W // 2, 580, scale=2.5)

center_text(d, "Clara", 630, F_DISPLAY(36), TRUST)

center_text(d, "OdiseIA4Good  ·  UDIT  ·  Febrero 2026", 900, F_NARROW(16), MUTED)

slides.append(img)


# ════════════════════════════════════════════
# SAVE PDF
# ════════════════════════════════════════════
pdf_path = os.path.join(OUT, "Clara-Presentacion.pdf")
slides[0].save(pdf_path, "PDF", resolution=150.0, save_all=True, append_images=slides[1:])
print(f"PDF saved: {pdf_path}")
print(f"Pages: {len(slides)}")
print(f"Size: {os.path.getsize(pdf_path) / 1024:.0f} KB")

# Also save individual PNGs for reference
png_dir = os.path.join(OUT, "slides")
os.makedirs(png_dir, exist_ok=True)
for i, s in enumerate(slides):
    s.save(os.path.join(png_dir, f"slide_{i+1:02d}.png"), quality=95)
print(f"PNGs saved: {png_dir}/")
