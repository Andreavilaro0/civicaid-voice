#!/usr/bin/env python3
"""Generate extra visual assets for Clara presentation — standalone PNGs."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1920, 1080
OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

# ── Fonts ──
def font(name, size):
    paths = [
        f"/System/Library/Fonts/{name}.ttc",
        f"/System/Library/Fonts/Supplemental/{name}.ttf",
        f"/System/Library/Fonts/{name}.ttf",
        f"/Library/Fonts/{name}.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)

DISPLAY = font("Georgia", 72)
DISPLAY_SM = font("Georgia", 52)
DISPLAY_XS = font("Georgia", 40)
TITLE = font("Arial", 36)
BODY = font("Arial", 22)
BODY_SM = font("Arial", 18)
BODY_XS = font("Arial", 15)
LABEL = font("Arial", 14)
BIG_NUM = font("Georgia", 120)
MED_NUM = font("Georgia", 72)

# ── Colors ──
BG = (10, 10, 10)
TRUST = (27, 94, 123)
HOPE = (46, 125, 79)
WARMTH = (212, 106, 30)
ALERT = (198, 40, 40)
WHITE = (250, 250, 249)
MUTED = (150, 150, 150)
CARD_BG = (22, 22, 22)
CARD_BORDER = (40, 40, 40)

def rgba(color, alpha):
    return color + (alpha,)

def draw_glow(img, cx, cy, radius, color, alpha=25):
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    for i in range(radius, 0, -2):
        a = int(alpha * (i / radius))
        od.ellipse([cx-i, cy-i, cx+i, cy+i], fill=rgba(color, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))

def draw_clara_logo(draw, cx, cy, scale=1.0, color=TRUST, dot_color=WARMTH):
    for i, (r, op) in enumerate([(30,90), (20,170), (10,255)]):
        r2 = int(r * scale)
        c = tuple(int(v * op / 255) for v in color)
        # Draw arcs as series of dots
        for deg in range(-90, 91, 3):
            rad = math.radians(deg)
            x = cx + int(r2 * math.cos(rad))
            y = cy + int(r2 * math.sin(rad))
            s = max(1, int(2.5 * scale))
            draw.ellipse([x-s, y-s, x+s, y+s], fill=c)
    ds = int(5.5 * scale)
    draw.ellipse([cx-ds, cy-ds, cx+ds, cy+ds], fill=dot_color)

def draw_rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    if fill:
        draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
        draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
        draw.pieslice([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=fill)
        draw.pieslice([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=fill)
        draw.pieslice([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=fill)
        draw.pieslice([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0+radius, y0, x1-radius, y0], fill=outline, width=width)
        draw.line([x0+radius, y1, x1-radius, y1], fill=outline, width=width)
        draw.line([x0, y0+radius, x0, y1-radius], fill=outline, width=width)
        draw.line([x1, y0+radius, x1, y1-radius], fill=outline, width=width)

def draw_phone(img, draw, px, py, pw, ph, messages, header="Clara", header_color=TRUST):
    """Draw a phone mockup with messages."""
    # Phone body
    draw_rounded_rect(draw, [px, py, px+pw, py+ph], 32, fill=(28, 28, 30))
    # Inner border
    draw_rounded_rect(draw, [px+2, py+2, px+pw-2, py+ph-2], 30, outline=(58, 58, 60), width=1)
    # Screen
    sx, sy = px + 8, py + 8
    sw, sh = pw - 16, ph - 16
    draw_rounded_rect(draw, [sx, sy, sx+sw, sy+sh], 24, fill=(250, 250, 250))
    # Header
    hh = 56
    draw_rounded_rect(draw, [sx, sy, sx+sw, sy+hh], 24, fill=header_color)
    draw.rectangle([sx, sy+24, sx+sw, sy+hh], fill=header_color)
    draw.text((sx + 16, sy + 18), f"← {header}", fill=WHITE, font=BODY_SM)
    # Messages
    cy = sy + hh + 12
    for role, text in messages:
        is_clara = role == "clara"
        bubble_color = (227, 242, 253) if is_clara else header_color
        text_color = (26, 26, 26) if is_clara else WHITE
        max_w = int(sw * 0.72)
        # Wrap text
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = f"{line} {w}".strip()
            bbox = draw.textbbox((0, 0), test, font=BODY_XS)
            if bbox[2] - bbox[0] > max_w - 24:
                if line: lines.append(line)
                line = w
            else:
                line = test
        if line: lines.append(line)
        bh = len(lines) * 20 + 16
        if is_clara:
            bx = sx + 12
        else:
            bx = sx + sw - max_w - 12
        if cy + bh + 8 > sy + sh - 50:
            break
        draw_rounded_rect(draw, [bx, cy, bx + max_w, cy + bh], 12, fill=bubble_color)
        for i, l in enumerate(lines):
            draw.text((bx + 12, cy + 8 + i * 20), l, fill=text_color, font=BODY_XS)
        cy += bh + 8


# ═══════════════════════════════════════════════
# IMAGE 1: WhatsApp Demo — Maria (Elderly, Voice)
# ═══════════════════════════════════════════════
def img_whatsapp_maria():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_glow(img, 400, 540, 300, TRUST, 20)
    draw = ImageDraw.Draw(img)

    # Title side
    draw.text((80, 80), "DEMO", fill=MUTED, font=LABEL)
    draw.text((80, 110), "Maria, 74 anos", fill=WHITE, font=DISPLAY_SM)
    draw.text((80, 175), "Nota de voz → Respuesta con audio", fill=WARMTH, font=TITLE)
    # Feature list
    features = [
        ("Le tiemblan las manos — no puede teclear", WARMTH),
        ("Manda nota de voz en WhatsApp", HOPE),
        ("Whisper transcribe automaticamente", TRUST),
        ("Clara responde en texto + audio", HOPE),
        ("Lenguaje claro, solo el siguiente paso", WHITE),
    ]
    for i, (f, c) in enumerate(features):
        y = 260 + i * 48
        draw.ellipse([80, y+6, 94, y+20], fill=c)
        draw.text((110, y), f, fill=(200,200,200), font=BODY)

    # Phone mockup
    messages = [
        ("clara", "Hola Maria, soy Clara. Puedes escribirme o enviarme una nota de voz."),
        ("user", "🎤 Nota de voz 0:05"),
        ("clara", "He escuchado tu pregunta sobre el IMV. El Ingreso Minimo Vital es una ayuda de 604-1.200€/mes."),
        ("clara", "Para solicitarlo necesitas: DNI, empadronamiento y declaracion de renta."),
        ("clara", "🔊 Audio respuesta — 0:28"),
        ("user", "Y donde lo pido?"),
        ("clara", "Puedes pedirlo en tu oficina de la Seguridad Social. Llama al 900 20 22 22 para pedir cita."),
    ]
    draw_phone(img, draw, 1050, 60, 340, 660, messages, "Clara 💚")

    # Bottom tag
    draw.text((80, 980), "WhatsApp · Whisper · Gemini 1.5 Flash", fill=(80,80,80), font=LABEL)
    draw.text((80, 1000), "< 30 segundos de respuesta", fill=HOPE, font=BODY_SM)

    img.save(os.path.join(OUT, "demo_whatsapp_maria.png"))
    print("✓ demo_whatsapp_maria.png")


# ═══════════════════════════════════════════════
# IMAGE 2: WhatsApp Demo — Ahmed (French Speaker)
# ═══════════════════════════════════════════════
def img_whatsapp_ahmed():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_glow(img, 1500, 540, 300, TRUST, 20)
    draw = ImageDraw.Draw(img)

    draw.text((80, 80), "DEMO · MULTILINGUE", fill=MUTED, font=LABEL)
    draw.text((80, 110), "Ahmed, 28 anos", fill=WHITE, font=DISPLAY_SM)
    draw.text((80, 175), "Habla en frances → Clara responde en frances", fill=TRUST, font=TITLE)

    features = [
        ("Viene de Senegal, habla frances", TRUST),
        ("Necesita empadronarse", HOPE),
        ("Escribe en frances", TRUST),
        ("Clara detecta el idioma automaticamente", WARMTH),
        ("Responde en frances sin pedirlo", HOPE),
    ]
    for i, (f, c) in enumerate(features):
        y = 260 + i * 48
        draw.ellipse([80, y+6, 94, y+20], fill=c)
        draw.text((110, y), f, fill=(200,200,200), font=BODY)

    messages = [
        ("user", "Bonjour, je veux m'inscrire au padron municipal"),
        ("clara", "Bonjour Ahmed! Pour vous inscrire au padron, vous devez aller a la mairie avec:"),
        ("clara", "1. Passeport ou carte d'identite\n2. Contrat de location\n3. Formulaire de demande"),
        ("user", "Ou est la mairie la plus proche?"),
        ("clara", "Vous pouvez chercher votre mairie sur sede.gob.es. Voulez-vous que je vous aide avec les documents?"),
        ("clara", "🔊 Audio en francais — 0:22"),
    ]
    draw_phone(img, draw, 1050, 60, 340, 660, messages, "Clara 🇫🇷")

    draw.text((80, 700), "Deteccion automatica de idioma", fill=TRUST, font=DISPLAY_XS)
    draw.text((80, 760), "Clara detecta que Ahmed escribe en frances", fill=(120,120,120), font=BODY)
    draw.text((80, 795), "y responde en frances sin que lo pida.", fill=(120,120,120), font=BODY)
    draw.text((80, 845), "ES · FR · (pronto mas idiomas)", fill=WARMTH, font=BODY_SM)

    img.save(os.path.join(OUT, "demo_whatsapp_ahmed.png"))
    print("✓ demo_whatsapp_ahmed.png")


# ═══════════════════════════════════════════════
# IMAGE 3: Web App Demo — Social Worker View
# ═══════════════════════════════════════════════
def img_webapp_demo():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_glow(img, 960, 400, 400, HOPE, 15)
    draw = ImageDraw.Draw(img)

    draw.text((80, 50), "INTERFAZ WEB", fill=MUTED, font=LABEL)
    draw.text((80, 80), "Clara Web", fill=WHITE, font=DISPLAY_SM)
    draw.text((80, 150), "Para trabajadoras sociales y ONGs", fill=HOPE, font=TITLE)

    # Browser mockup
    bx, by, bw, bh = 80, 220, 1760, 780
    draw_rounded_rect(draw, [bx, by, bx+bw, by+bh], 16, fill=(30, 30, 32))
    # Browser bar
    draw_rounded_rect(draw, [bx, by, bx+bw, by+40], 16, fill=(45, 45, 48))
    draw.rectangle([bx, by+16, bx+bw, by+40], fill=(45, 45, 48))
    # Traffic lights
    for i, c in enumerate([(255,95,86), (255,189,46), (39,201,63)]):
        draw.ellipse([bx+16+i*22, by+12, bx+28+i*22, by+24], fill=c)
    # URL bar
    draw_rounded_rect(draw, [bx+100, by+8, bx+600, by+32], 8, fill=(60,60,64))
    draw.text((bx+115, by+11), "clara.civicaid.es", fill=(160,160,160), font=BODY_XS)

    # Content area
    cx, cy = bx + 10, by + 50
    cw = bw - 20

    # Sidebar
    sw = 260
    draw.rectangle([cx, cy, cx+sw, by+bh-10], fill=(20, 22, 24))
    # Sidebar logo
    draw_clara_logo(draw, cx+40, cy+35, scale=0.8)
    draw.text((cx+60, cy+22), "Clara", fill=WHITE, font=BODY)
    draw.text((cx+60, cy+44), "Panel Asistente", fill=MUTED, font=BODY_XS)
    # Sidebar menu
    menu = ["Conversaciones", "Usuarios", "Base de conocimiento", "Estadisticas", "Configuracion"]
    for i, m in enumerate(menu):
        my = cy + 90 + i * 42
        c = HOPE if i == 0 else (80, 80, 80)
        if i == 0:
            draw.rectangle([cx, my-4, cx+sw, my+30], fill=(46, 125, 79, 20))
        draw.text((cx + 20, my), m, fill=c, font=BODY_SM)

    # Main content
    mx = cx + sw + 20
    mw = cw - sw - 30
    # Conversation header
    draw.text((mx, cy + 10), "Conversacion con Fatima", fill=WHITE, font=TITLE)
    draw.text((mx, cy + 50), "Tarjeta sanitaria · Hace 2 min", fill=MUTED, font=BODY_XS)
    # Messages
    msgs = [
        ("user", "Necesito tarjeta sanitaria para mi hijo"),
        ("clara", "Para la tarjeta sanitaria de tu hijo necesitas:\n✅ Tu NIE o pasaporte\n✅ Empadronamiento\n✅ Libro de familia o partida nacimiento\nVe al centro de salud mas cercano."),
        ("user", "🎤 Nota de voz — 0:08"),
        ("clara", "Entiendo, quieres saber los horarios. Los centros de salud atienden de 8:00 a 20:00.\n🔊 Audio — 0:15"),
    ]
    my = cy + 85
    for role, text in msgs:
        is_clara = role == "clara"
        bg_c = (35, 45, 55) if is_clara else (27, 94, 123)
        tx_c = (220, 220, 220) if is_clara else WHITE
        lines = text.split("\n")
        th = len(lines) * 20 + 16
        if is_clara:
            bx2 = mx + 10
        else:
            bx2 = mx + mw - 450
        draw_rounded_rect(draw, [bx2, my, bx2 + 440, my + th], 10, fill=bg_c)
        for j, l in enumerate(lines):
            draw.text((bx2 + 12, my + 8 + j * 20), l, fill=tx_c, font=BODY_XS)
        my += th + 10

    # Input bar at bottom
    iy = by + bh - 60
    draw_rounded_rect(draw, [mx, iy, mx+mw, iy+40], 20, fill=(35, 35, 38))
    draw.text((mx + 50, iy + 10), "Escribe o habla...", fill=(100,100,100), font=BODY_SM)
    # Mic icon
    draw.ellipse([mx+10, iy+8, mx+34, iy+32], fill=HOPE)
    draw.text((mx+15, iy+10), "🎤", font=BODY_XS)

    img.save(os.path.join(OUT, "demo_webapp.png"))
    print("✓ demo_webapp.png")


# ═══════════════════════════════════════════════
# IMAGE 4: Architecture Diagram (detailed)
# ═══════════════════════════════════════════════
def img_architecture():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((W//2 - 100, 30), "ARQUITECTURA", fill=MUTED, font=LABEL)
    draw.text((W//2 - 200, 55), "Como funciona Clara", fill=WHITE, font=DISPLAY_XS)

    # Nodes
    nodes = [
        (160, 450, 200, 130, "Usuario", "WhatsApp\nVoz · Texto · Foto", HOPE, "📱"),
        (460, 450, 180, 130, "Twilio", "Mensajeria\nWebhook", TRUST, "📡"),
        (740, 300, 200, 130, "Whisper", "Voz → Texto\nOpenAI", WARMTH, "🎤"),
        (740, 580, 200, 130, "Vision", "Foto → Texto\nGemini", WARMTH, "📷"),
        (1060, 450, 200, 130, "Gemini\n1.5 Flash", "Motor IA\nContexto + Tono", TRUST, "🧠"),
        (1360, 300, 200, 130, "KB + RAG", "8 bases\npgvector", HOPE, "📚"),
        (1360, 580, 200, 130, "Guardrails", "Seguridad\nPre/Post", ALERT, "🛡️"),
        (1660, 450, 200, 130, "Respuesta", "Texto + Audio\nMultilingue", HOPE, "✅"),
    ]

    # Draw connections
    connections = [
        (0, 1), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (4, 6), (5, 7), (6, 7)
    ]
    for a, b in connections:
        ax = nodes[a][0] + nodes[a][2]
        ay = nodes[a][1] + nodes[a][3] // 2
        bx = nodes[b][0]
        by = nodes[b][1] + nodes[b][3] // 2
        draw.line([(ax, ay), (bx, by)], fill=(60, 60, 60), width=2)
        # Arrow
        dx, dy = bx - ax, by - ay
        d = max(1, (dx**2 + dy**2) ** 0.5)
        ux, uy = dx / d, dy / d
        ax2, ay2 = bx - ux * 10, by - uy * 10
        draw.polygon([
            (bx, by),
            (int(ax2 - uy * 5), int(ay2 + ux * 5)),
            (int(ax2 + uy * 5), int(ay2 - ux * 5)),
        ], fill=(80, 80, 80))

    # Draw nodes
    for x, y, w, h, name, desc, color, icon in nodes:
        draw_rounded_rect(draw, [x, y, x+w, y+h], 16, fill=(18, 20, 22), outline=color, width=2)
        draw.text((x + 14, y + 10), icon, fill=WHITE, font=BODY)
        draw.text((x + 42, y + 12), name, fill=WHITE, font=BODY_SM)
        for i, line in enumerate(desc.split("\n")):
            draw.text((x + 14, y + 42 + i * 20), line, fill=MUTED, font=BODY_XS)

    # Bottom tech pills
    techs = ["Python 3.11", "Flask", "Docker", "Render", "PostgreSQL", "pgvector", "469 tests"]
    tx = 300
    for t in techs:
        tw = len(t) * 10 + 24
        draw_rounded_rect(draw, [tx, 950, tx+tw, 980], 12, fill=(25, 25, 28), outline=(50, 50, 55))
        draw.text((tx + 12, 955), t, fill=MUTED, font=BODY_XS)
        tx += tw + 12

    # Time label
    draw.text((W//2 - 120, 890), "< 30 segundos end-to-end", fill=WARMTH, font=BODY)
    draw.text((W//2 - 140, 920), "No es un demo. Es un producto.", fill=HOPE, font=BODY_SM)

    img.save(os.path.join(OUT, "architecture_diagram.png"))
    print("✓ architecture_diagram.png")


# ═══════════════════════════════════════════════
# IMAGE 5: Impact Infographic
# ═══════════════════════════════════════════════
def img_impact():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_glow(img, 960, 300, 500, HOPE, 12)
    draw = ImageDraw.Draw(img)

    draw.text((W//2 - 50, 30), "IMPACTO", fill=MUTED, font=LABEL)
    draw.text((W//2 - 250, 60), "Numeros que importan", fill=WHITE, font=DISPLAY_SM)

    # Big stats row
    stats = [
        ("11.4M", "personas en riesgo\nde exclusion social", WARMTH),
        ("2B", "usuarios WhatsApp\nen el mundo", TRUST),
        ("87%", "adultos en Espana\nusan WhatsApp", HOPE),
        ("0€", "coste para\nel usuario", WARMTH),
    ]
    for i, (num, label, color) in enumerate(stats):
        x = 120 + i * 440
        y = 180
        draw.text((x, y), num, fill=color, font=MED_NUM)
        for j, l in enumerate(label.split("\n")):
            draw.text((x, y + 80 + j * 24), l, fill=MUTED, font=BODY)

    # Divider
    draw.line([(100, 420), (W-100, 420)], fill=(30, 30, 30), width=1)

    # Roadmap
    draw.text((W//2 - 80, 450), "ESCALABILIDAD", fill=MUTED, font=LABEL)
    phases = [
        ("HOY", "IMV, empadronamiento\ntarjeta sanitaria, NIE/TIE", HOPE, True),
        ("→", "", (50,50,50), False),
        ("MANANA", "Todas las CCAA\nde Espana", TRUST, True),
        ("→", "", (50,50,50), False),
        ("FUTURO", "LATAM, refugiados\ncualquier idioma", WARMTH, True),
    ]
    px = 180
    for label, desc, color, is_box in phases:
        if is_box:
            draw_rounded_rect(draw, [px, 500, px+320, 620], 16, fill=(18, 20, 22), outline=color, width=2)
            draw.text((px + 20, 515), label, fill=color, font=BODY)
            for j, l in enumerate(desc.split("\n")):
                draw.text((px + 20, 550 + j * 22), l, fill=(160, 160, 160), font=BODY_SM)
            px += 340
        else:
            draw.text((px + 10, 545), "→", fill=(60,60,60), font=DISPLAY_XS)
            px += 60

    # Bottom quote
    draw.text((W//2 - 350, 700), '"Clara no reemplaza a los trabajadores sociales.', fill=(160,160,160), font=BODY)
    draw.text((W//2 - 290, 735), 'Los amplifica."', fill=WARMTH, font=BODY)

    # Key differentiators
    diffs = [
        ("Coste marginal ≈ 0", "Llegar a una persona mas no cuesta nada"),
        ("Sin instalar nada", "WhatsApp ya esta en el movil"),
        ("Multi-idioma", "Frances hoy, arabe y mas manana"),
        ("469 tests", "Cuando la info es critica, no puedes fallar"),
    ]
    for i, (title, desc) in enumerate(diffs):
        x = 120 + (i % 4) * 430
        y = 820
        draw_rounded_rect(draw, [x, y, x + 400, y + 90], 12, fill=(18, 20, 22), outline=(40, 40, 42))
        draw.text((x + 16, y + 12), title, fill=HOPE, font=BODY_SM)
        draw.text((x + 16, y + 38), desc, fill=(130, 130, 130), font=BODY_XS)

    img.save(os.path.join(OUT, "impact_infographic.png"))
    print("✓ impact_infographic.png")


# ═══════════════════════════════════════════════
# IMAGE 6: Persona Cards (visual)
# ═══════════════════════════════════════════════
def img_personas():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((W//2 - 120, 30), "PARA QUIEN ES CLARA", fill=MUTED, font=LABEL)
    draw.text((W//2 - 350, 60), "Tres personas. Un problema comun.", fill=WHITE, font=DISPLAY_XS)

    personas = [
        ("Maria", "74 anos", "Espanola", "Le tiemblan las manos.\nNo puede teclear bien.\nNo entiende formularios.", "Nota de voz\nIMV", WARMTH, "👵"),
        ("Ahmed", "28 anos", "Senegal → Espana", "Habla frances.\n2 anos en Espana.\nNecesita empadronarse.", "Bilingue ES/FR\nEmpadronamiento", TRUST, "👨"),
        ("Fatima", "45 anos", "Marruecos → Espana", "Habla pero no lee\nen espanol. Necesita\ntarjeta sanitaria hijo.", "Audio respuesta\nTarjeta sanitaria", HOPE, "👩"),
    ]

    for i, (name, age, origin, problem, solution, color, emoji) in enumerate(personas):
        x = 100 + i * 590
        y = 150
        w, h = 540, 780

        # Card
        draw_rounded_rect(draw, [x, y, x+w, y+h], 20, fill=(16, 18, 20), outline=color, width=2)

        # Top color bar
        draw_rounded_rect(draw, [x, y, x+w, y+100], 20, fill=color)
        draw.rectangle([x, y+20, x+w, y+100], fill=color)

        # Avatar circle
        draw.ellipse([x+w//2-35, y+65, x+w//2+35, y+135], fill=(30, 30, 32), outline=color, width=2)
        draw.text((x+w//2-12, y+80), emoji, fill=WHITE, font=TITLE)

        # Name & age
        draw.text((x + w//2 - 60, y + 150), name, fill=WHITE, font=TITLE)
        draw.text((x + w//2 + 10, y + 158), age, fill=MUTED, font=BODY_SM)
        draw.text((x + w//2 - 60, y + 192), origin, fill=color, font=BODY_SM)

        # Divider
        draw.line([(x+30, y+230), (x+w-30, y+230)], fill=(40, 40, 42))

        # Problem
        draw.text((x + 30, y + 250), "SITUACION", fill=MUTED, font=LABEL)
        for j, l in enumerate(problem.split("\n")):
            draw.text((x + 30, y + 275 + j * 26), l, fill=(180, 180, 180), font=BODY)

        # Divider
        draw.line([(x+30, y+440), (x+w-30, y+440)], fill=(40, 40, 42))

        # Solution
        draw.text((x + 30, y + 460), "CLARA AYUDA CON", fill=MUTED, font=LABEL)
        for j, l in enumerate(solution.split("\n")):
            draw.text((x + 30, y + 488 + j * 28), l, fill=color, font=BODY)

        # Quote
        draw_rounded_rect(draw, [x+20, y+h-130, x+w-20, y+h-20], 12, fill=(25, 28, 30))
        quotes = {
            "Maria": '"Solo quiero saber que\nhacer manana por la manana."',
            "Ahmed": '"Je ne comprends pas\nles formulaires en espagnol."',
            "Fatima": '"No se por donde\nempezar."',
        }
        for j, l in enumerate(quotes[name].split("\n")):
            draw.text((x + 40, y + h - 115 + j * 22), l, fill=(140, 140, 140), font=BODY_SM)

    # Bottom
    draw.text((W//2 - 300, 970), "El sistema no esta disenado para ellas.", fill=(100,100,100), font=BODY)
    draw.text((W//2 - 60, 1000), "Nosotros si.", fill=WARMTH, font=BODY)

    img.save(os.path.join(OUT, "personas_cards.png"))
    print("✓ personas_cards.png")


# ═══════════════════════════════════════════════
# IMAGE 7: 6 Vulnerable Population Use Cases
# ═══════════════════════════════════════════════
def img_vulnerable_uses():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((W//2 - 130, 25), "CLARA PARA CADA SITUACION", fill=MUTED, font=LABEL)
    draw.text((W//2 - 280, 55), "6 realidades. Una solucion.", fill=WHITE, font=DISPLAY_XS)

    cases = [
        ("👵", "Mayores solos", "Nota de voz para pedir cita\nmedica o preguntar pensiones", WARMTH),
        ("🌍", "Inmigrantes sin idioma", "Hablan en frances o arabe,\nClara responde en su idioma", TRUST),
        ("🛡️", "Violencia de genero", "Info segura sobre ordenes de\nproteccion y recursos", ALERT),
        ("🏠", "Sin hogar", "Guia para acceder a albergues,\ncomedores y ayudas emergencia", HOPE),
        ("♿", "Discapacidad", "Interfaz por voz, sin necesidad\nde teclear ni leer pantalla", TRUST),
        ("📖", "Analfabetismo funcional", "Todo por voz: pregunta hablando,\nrecibe respuesta en audio", WARMTH),
    ]

    for i, (icon, title, desc, color) in enumerate(cases):
        col = i % 3
        row = i // 3
        x = 100 + col * 590
        y = 140 + row * 420
        w, h = 550, 370

        draw_rounded_rect(draw, [x, y, x+w, y+h], 20, fill=(16, 18, 20), outline=color, width=2)

        # Top accent line
        draw.rectangle([x+20, y+2, x+120, y+4], fill=color)

        # Icon
        draw.text((x + 30, y + 30), icon, fill=WHITE, font=DISPLAY_XS)
        draw.text((x + 80, y + 36), title, fill=color, font=TITLE)

        # Description
        for j, l in enumerate(desc.split("\n")):
            draw.text((x + 30, y + 100 + j * 28), l, fill=(170, 170, 170), font=BODY)

        # Example interaction
        draw_rounded_rect(draw, [x+20, y+h-150, x+w-20, y+h-20], 12, fill=(25, 28, 30))
        draw.text((x + 35, y + h - 140), "Ejemplo:", fill=MUTED, font=LABEL)
        examples = {
            "Mayores solos": '"Quiero pedir cita con\nmi medico de cabecera"',
            "Inmigrantes sin idioma": '"Je veux m\'inscrire\nau padron municipal"',
            "Violencia de genero": '"Necesito informacion sobre\nordenes de proteccion"',
            "Sin hogar": '"Donde puedo dormir\nesta noche?"',
            "Discapacidad": '🎤 "Como pido la tarjeta\nde discapacidad?"',
            "Analfabetismo funcional": '🎤 "Que papeles necesito\npara el medico?"',
        }
        for j, l in enumerate(examples[title].split("\n")):
            draw.text((x + 35, y + h - 118 + j * 22), l, fill=(140, 140, 140), font=BODY_SM)

    # Category design tag
    draw.text((W//2 - 250, 995), "Clara crea una nueva categoria:", fill=(100,100,100), font=BODY_SM)
    draw.text((W//2 + 30, 995), "Civic Tenderness", fill=WARMTH, font=BODY_SM)
    draw.text((W//2 - 150, 1025), "Calidez institucional por diseno", fill=(70,70,70), font=BODY_XS)

    img.save(os.path.join(OUT, "vulnerable_uses.png"))
    print("✓ vulnerable_uses.png")


# ═══════════════════════════════════════════════
# IMAGE 8: Before/After — Maria's Journey
# ═══════════════════════════════════════════════
def img_before_after():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((W//2 - 100, 25), "EL CAMBIO", fill=MUTED, font=LABEL)

    # BEFORE side
    bx = 80
    draw_rounded_rect(draw, [bx, 80, bx+840, 1000], 20, fill=(20, 14, 14), outline=ALERT, width=2)
    draw.text((bx + 30, 100), "ANTES", fill=ALERT, font=DISPLAY_XS)
    draw.text((bx + 180, 112), "Sin Clara", fill=(120, 60, 60), font=BODY)

    before_steps = [
        ("1", "Llamo a una oficina", "Le dijeron que esperara", "📞", (60,60,60)),
        ("2", "Llamo a otra oficina", "No era la correcta", "📞", (60,60,60)),
        ("3", "Entro en una web", "No entendia las palabras", "💻", (60,60,60)),
        ("4", "Formulario de 12 paginas", "No sabe que campos rellenar", "📋", (60,60,60)),
        ("5", "Maria se rindio", "Nunca cobro la ayuda", "😔", ALERT),
    ]
    for i, (num, title, desc, icon, color) in enumerate(before_steps):
        y = 200 + i * 150
        draw.ellipse([bx+30, y, bx+60, y+30], fill=color)
        draw.text((bx+39, y+3), num, fill=WHITE, font=BODY_XS)
        draw.text((bx+80, y), icon + " " + title, fill=(180,180,180), font=BODY)
        draw.text((bx+80, y+30), desc, fill=(100,100,100), font=BODY_SM)
        if i < 4:
            draw.line([(bx+45, y+35), (bx+45, y+145)], fill=(40,40,40), width=1)

    draw.text((bx + 80, 950), "Resultado: Maria no cobra el IMV", fill=ALERT, font=BODY_SM)

    # AFTER side
    ax = 1000
    draw_rounded_rect(draw, [ax, 80, ax+840, 1000], 20, fill=(14, 20, 16), outline=HOPE, width=2)
    draw.text((ax + 30, 100), "DESPUES", fill=HOPE, font=DISPLAY_XS)
    draw.text((ax + 230, 112), "Con Clara", fill=(60, 120, 70), font=BODY)

    after_steps = [
        ("1", "Abre WhatsApp", "Lo que ya tiene en el movil", "📱", HOPE),
        ("2", "Manda nota de voz", '"Quiero saber del IMV"', "🎤", HOPE),
        ("3", "Clara responde en 30s", "Texto claro + audio", "💬", HOPE),
        ("4", "Sabe que hacer manana", "Paso concreto y telefono", "✅", HOPE),
        ("5", "Maria cobra el IMV", "604€/mes que le corresponden", "🎉", WARMTH),
    ]
    for i, (num, title, desc, icon, color) in enumerate(after_steps):
        y = 200 + i * 150
        draw.ellipse([ax+30, y, ax+60, y+30], fill=color)
        draw.text((ax+39, y+3), num, fill=WHITE, font=BODY_XS)
        draw.text((ax+80, y), icon + " " + title, fill=(200,220,200), font=BODY)
        draw.text((ax+80, y+30), desc, fill=(120,140,120), font=BODY_SM)
        if i < 4:
            draw.line([(ax+45, y+35), (ax+45, y+145)], fill=(40,60,40), width=1)

    draw.text((ax + 80, 950), "Resultado: Maria cobra 604€/mes", fill=HOPE, font=BODY_SM)

    img.save(os.path.join(OUT, "before_after.png"))
    print("✓ before_after.png")


# ═══════════════════════════════════════════════
# IMAGE 9: Team + Civic Tenderness
# ═══════════════════════════════════════════════
def img_team_closing():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_glow(img, W//2, H//2, 400, WARMTH, 15)
    draw = ImageDraw.Draw(img)

    # Logo
    draw_clara_logo(draw, W//2, 180, scale=3.0)

    draw.text((W//2 - 60, 280), "Clara", fill=WHITE, font=DISPLAY)

    # Quote
    draw.text((W//2 - 250, 400), '"Tu voz tiene poder."', fill=WARMTH, font=DISPLAY_XS)

    # Team
    team = [
        ("Robert", "Backend Lead", TRUST),
        ("Marcos", "Deploy + Twilio", HOPE),
        ("Lucas", "KB + 469 Tests", WARMTH),
        ("Daniel", "Video", TRUST),
        ("Andrea", "Coordinacion", WARMTH),
    ]
    for i, (name, role, color) in enumerate(team):
        x = 220 + i * 300
        y = 540
        draw.ellipse([x, y, x+70, y+70], fill=color)
        initial = name[0]
        draw.text((x+22, y+15), initial, fill=WHITE, font=TITLE)
        draw.text((x+5, y+85), name, fill=WHITE, font=BODY_SM)
        draw.text((x+5, y+108), role, fill=MUTED, font=BODY_XS)

    # Bottom
    draw.text((W//2 - 320, 750), "La tecnologia mas poderosa del mundo", fill=(120,120,120), font=BODY)
    draw.text((W//2 - 380, 790), "es la que hace que una persona de 74 anos", fill=(120,120,120), font=BODY)
    draw.text((W//2 - 380, 830), "sienta que el sistema — por fin — ", fill=(120,120,120), font=BODY)
    draw.text((W//2 + 110, 830), "la esta escuchando.", fill=WARMTH, font=BODY)

    draw.text((W//2 - 200, 920), "OdiseIA4Good · UDIT · Febrero 2026", fill=(60,60,60), font=BODY_SM)
    draw.text((W//2 - 150, 960), "Civic Tenderness by Design", fill=HOPE, font=BODY_SM)

    img.save(os.path.join(OUT, "team_closing.png"))
    print("✓ team_closing.png")


# ═══════════════════════════════════════════════
# IMAGE 10: Cover Slide
# ═══════════════════════════════════════════════
def img_cover():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_glow(img, W//2 - 100, H//2, 400, TRUST, 20)
    draw_glow(img, W//2 + 200, H//2 + 100, 300, WARMTH, 12)
    draw = ImageDraw.Draw(img)

    draw.text((W//2 - 60, 100), "Andrea Avila", fill=MUTED, font=BODY)

    # Big logo
    draw_clara_logo(draw, W//2, 280, scale=4.0, color=TRUST)

    # Title
    draw.text((W//2 - 100, 400), "Clara", fill=WHITE, font=font("Georgia", 96))

    # Subtitle
    draw.text((W//2 - 350, 530), "Asistente conversacional que ayuda a", fill=(160,160,160), font=BODY)
    draw.text((W//2 - 350, 565), "personas vulnerables a navegar ayudas del gobierno", fill=(160,160,160), font=BODY)

    # Pills
    pills = ["WhatsApp-first", "Voz + Texto + Foto", "ES / FR", "Civic Tenderness"]
    px = W//2 - 350
    for p in pills:
        pw = len(p) * 11 + 30
        draw_rounded_rect(draw, [px, 640, px+pw, 674], 17, fill=(20, 22, 24), outline=(50, 50, 55))
        draw.text((px + 15, 648), p, fill=(160, 160, 160), font=BODY_SM)
        px += pw + 14

    draw.text((W//2 - 160, 800), "OdiseIA4Good · UDIT · Febrero 2026", fill=(60,60,60), font=BODY_SM)

    img.save(os.path.join(OUT, "cover.png"))
    print("✓ cover.png")


# ═══════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print("Generando imagenes extra para Clara...\n")
    img_cover()
    img_whatsapp_maria()
    img_whatsapp_ahmed()
    img_webapp_demo()
    img_architecture()
    img_impact()
    img_personas()
    img_vulnerable_uses()
    img_before_after()
    img_team_closing()
    print(f"\n✅ 10 imagenes guardadas en: {OUT}/")
