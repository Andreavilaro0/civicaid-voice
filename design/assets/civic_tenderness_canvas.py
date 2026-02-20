"""
Civic Tenderness — Visual Philosophy Canvas for Clara
Generates a museum-quality composition expressing the intersection
of institutional structure and human warmth.
"""

import math
from PIL import Image, ImageDraw, ImageFont

# --- Canvas Setup ---
W, H = 2400, 3200  # Portrait, high-res
canvas = Image.new("RGB", (W, H), "#FAFAFA")
draw = ImageDraw.Draw(canvas)

# --- Palette ---
BLUE = "#1B5E7B"
ORANGE = "#D46A1E"
GREEN = "#2E7D4F"
BG = "#FAFAFA"
TEXT = "#1A1A2E"
TEXT_SEC = "#4A4A5A"
INFO = "#E3F2FD"
BORDER = "#E0E0E0"
CARD = "#F5F5F5"
BLUE_LIGHT = "#D0E8F2"
ORANGE_LIGHT = "#F5DCC4"
GREEN_LIGHT = "#D4EDDB"

# --- Fonts (macOS system fonts) ---
SYS = "/System/Library/Fonts"
SUP = f"{SYS}/Supplemental"

font_display_bold = ImageFont.truetype(f"{SUP}/Futura.ttc", 180, index=2)    # Futura Bold
font_display_md = ImageFont.truetype(f"{SUP}/Futura.ttc", 72, index=2)       # Futura Bold
font_body = ImageFont.truetype(f"{SYS}/HelveticaNeue.ttc", 28, index=0)      # Helvetica Neue Regular
font_body_italic = ImageFont.truetype(f"{SYS}/HelveticaNeue.ttc", 28, index=2)  # Italic
font_mono = ImageFont.truetype(f"{SYS}/Menlo.ttc", 20, index=0)              # Menlo Regular
font_mono_sm = ImageFont.truetype(f"{SYS}/Menlo.ttc", 16, index=0)           # Menlo Small
font_label = ImageFont.truetype(f"{SYS}/HelveticaNeue.ttc", 22, index=7)     # Light
font_label_bold = ImageFont.truetype(f"{SYS}/HelveticaNeue.ttc", 24, index=1)  # Bold
font_tagline = ImageFont.truetype(f"{SUP}/Georgia.ttf", 50)                   # Georgia serif
font_section = ImageFont.truetype(f"{SYS}/HelveticaNeue.ttc", 18, index=5)   # UltraLight


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_circle(cx, cy, r, fill=None, outline=None, width=1):
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=fill, outline=outline, width=width
    )


def draw_ring(cx, cy, r, color, width=2):
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=None, outline=color, width=width
    )


def draw_rounded_rect(x1, y1, x2, y2, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)


# ============================================================
# LAYER 1: Background texture — subtle grid suggesting bureaucratic forms
# ============================================================

# Very faint grid lines — the ghost of forms and documents
for x in range(0, W, 60):
    draw.line([(x, 0), (x, H)], fill="#F2F2F2", width=1)
for y in range(0, H, 60):
    draw.line([(0, y), (W, y)], fill="#F2F2F2", width=1)

# Slightly darker grid at larger intervals — structural backbone
for x in range(0, W, 300):
    draw.line([(x, 0), (x, H)], fill="#EBEBEB", width=1)
for y in range(0, H, 300):
    draw.line([(0, y), (W, y)], fill="#EBEBEB", width=1)


# ============================================================
# LAYER 2: Concentric rings — sound waves / voice emanating
# The subtle reference: a voice being heard for the first time
# ============================================================

# Main voice epicenter — positioned at golden ratio
voice_cx = int(W * 0.38)
voice_cy = int(H * 0.36)

# Concentric rings expanding outward — voice rippling through bureaucracy
# Refined: more gradual weight variation, subtle color rhythm
ring_colors = [
    (BLUE, 3), (BORDER, 1), ("#C8D8E0", 1),
    (BLUE, 2), (BORDER, 1), (ORANGE, 2),
    ("#D0D8DC", 1), (BLUE, 2), (BORDER, 1),
    (ORANGE, 1), (BORDER, 1), ("#C8D8E0", 1),
    (BLUE, 1), (BORDER, 1), (BORDER, 1),
    ("#D0D8DC", 1), (BORDER, 1), (BORDER, 1),
]
for i, (color, w) in enumerate(ring_colors):
    r = 80 + i * 52
    draw_ring(voice_cx, voice_cy, r, color, w)

# Central solid circle — the voice itself (refined layers)
draw_circle(voice_cx, voice_cy, 68, fill=BLUE)
draw_circle(voice_cx, voice_cy, 52, fill="#FAFAFA")
draw_circle(voice_cx, voice_cy, 38, fill=BLUE)
draw_circle(voice_cx, voice_cy, 26, fill="#FAFAFA")
draw_circle(voice_cx, voice_cy, 18, fill=ORANGE)


# ============================================================
# LAYER 3: Floating rounded rectangles — bureaucratic documents
# transformed into gentle, approachable cards
# ============================================================

# Card cluster — upper right — documents becoming accessible
cards = [
    (1500, 180, 2200, 380, BLUE_LIGHT, BLUE),
    (1550, 420, 2150, 580, INFO, BLUE),
    (1450, 620, 2250, 820, CARD, BORDER),
    (1580, 860, 2180, 990, GREEN_LIGHT, GREEN),
]

for x1, y1, x2, y2, fill, outline in cards:
    draw_rounded_rect(x1, y1, x2, y2, 20, fill=fill, outline=outline, width=2)

# Small decorative lines inside cards — suggesting text/content (refined: varied widths)
for i, (x1, y1, x2, y2, _, col) in enumerate(cards):
    card_w = x2 - x1
    for j in range(4):
        lx1 = x1 + 28
        ly = y1 + 32 + j * 24
        # Vary line lengths for organic document feel
        lengths = [0.65, 0.45, 0.55, 0.30]
        lx2 = lx1 + int(card_w * lengths[j % 4])
        if ly < y2 - 18:
            draw.line([(lx1, ly), (lx2, ly)], fill=col, width=2)
    # Add a small accent dot on the first card line
    if i == 0:
        draw.ellipse([x2 - 50, y1 + 28, x2 - 38, y1 + 40], fill=ORANGE)


# ============================================================
# LAYER 4: Repeated small circles — a field of touch targets
# The generous, accessible interaction points Clara offers
# ============================================================

# Bottom-left field — hexagonal grid of touch targets (refined: precise hex packing)
touch_positions = []
hex_spacing_x = 72
hex_spacing_y = 62
for row in range(7):
    for col in range(9):
        x = 140 + col * hex_spacing_x + (row % 2) * (hex_spacing_x // 2)
        y = 2080 + row * hex_spacing_y
        if x < W * 0.52 and y < 2560:
            touch_positions.append((x, y))

for i, (x, y) in enumerate(touch_positions):
    r = 20
    if i % 11 == 0:
        draw_circle(x, y, r + 2, fill=ORANGE)
    elif i % 7 == 0:
        draw_circle(x, y, r, fill=GREEN)
    elif i % 4 == 0:
        draw_circle(x, y, r, fill=BLUE)
    elif i % 3 == 0:
        draw_ring(x, y, r, BLUE, 2)
    else:
        draw_ring(x, y, r, BORDER, 1)


# ============================================================
# LAYER 5: Horizontal bars — a sonogram-like pattern
# Voice frequencies visualized, the sound of someone speaking
# ============================================================

# Refined: denser, more precise waveform with smoother frequency curve
bar_start_y = 1700
bar_x = 1300
bar_count = 42
for i in range(bar_count):
    # Composite sine wave — vocal frequency pattern
    t = i / bar_count
    amplitude = (
        math.sin(i * 0.35) * 0.5 +
        math.sin(i * 0.18) * 0.35 +
        math.sin(i * 0.7) * 0.15
    )
    bar_h = int(abs(amplitude) * 85) + 6
    bar_y_center = bar_start_y + 180

    bx = bar_x + i * 24
    if bx > W - 140:
        break

    # Color transitions smoothly across the waveform
    if t < 0.55:
        color = BLUE
    elif t < 0.75:
        color = ORANGE
    else:
        color = GREEN

    draw_rounded_rect(
        bx, bar_y_center - bar_h,
        bx + 10, bar_y_center + bar_h,
        5, fill=color
    )


# ============================================================
# LAYER 6: Three large chromatic fields — the palette signature
# Blue (trust) | Orange (warmth) | Green (hope)
# ============================================================

# Bottom section — three monumental color blocks
block_y = 2700
block_h = 220
block_w = 580
gap = 60
total = 3 * block_w + 2 * gap
start_x = (W - total) // 2

# Blue block
draw_rounded_rect(start_x, block_y, start_x + block_w, block_y + block_h, 16, fill=BLUE)
# Orange block
draw_rounded_rect(start_x + block_w + gap, block_y, start_x + 2*block_w + gap, block_y + block_h, 16, fill=ORANGE)
# Green block
draw_rounded_rect(start_x + 2*(block_w + gap), block_y, start_x + 3*block_w + 2*gap, block_y + block_h, 16, fill=GREEN)

# Labels under blocks — whisper-quiet
draw.text((start_x + block_w // 2, block_y + block_h + 25), "confianza", font=font_label, fill=TEXT_SEC, anchor="mt")
draw.text((start_x + block_w + gap + block_w // 2, block_y + block_h + 25), "calidez", font=font_label, fill=TEXT_SEC, anchor="mt")
draw.text((start_x + 2*(block_w + gap) + block_w // 2, block_y + block_h + 25), "esperanza", font=font_label, fill=TEXT_SEC, anchor="mt")


# ============================================================
# LAYER 7: Typography — minimal, integrated, essential
# ============================================================

# Main title — monumental, top-left
draw.text((140, 100), "Clara", font=font_display_bold, fill=BLUE)

# Tagline — positioned with breathing room
draw.text((145, 310), "Tu voz tiene poder", font=font_tagline, fill=TEXT_SEC)

# Scientific reference markers — tiny labels that suggest systematic study
markers = [
    (voice_cx + 75, voice_cy - 320, "fig.01 — ondas de voz"),
    (1480, 140, "fig.02 — documentos accesibles"),
    (1330, 1660, "fig.03 — frecuencias de voz"),
    (100, 2060, "fig.04 — puntos de contacto"),
    (start_x - 10, block_y - 30, "fig.05 — sistema cromatico"),
]

for mx, my, label in markers:
    draw.text((mx, my), label, font=font_mono_sm, fill=TEXT_SEC)


# Manifesto line — bottom area, restrained
manifesto_y = 3020
draw.text(
    (W // 2, manifesto_y),
    "Civic Tenderness",
    font=font_display_md,
    fill=BLUE,
    anchor="mt"
)
draw.text(
    (W // 2, manifesto_y + 85),
    "the visual language of a system that remembers it serves people",
    font=font_body_italic,
    fill=TEXT_SEC,
    anchor="mt"
)


# ============================================================
# LAYER 8: Connecting lines — delicate threads between elements
# Suggesting the connections Clara builds between person and system
# ============================================================

# Refined: dotted arc path from voice center toward documents
for i in range(12):
    t = i / 11.0
    sx = voice_cx + 300
    sy = voice_cy - 80
    ex = 1480
    ey = 480
    mx = (sx + ex) / 2 + 80
    my = (sy + ey) / 2 - 180

    x = (1-t)**2 * sx + 2*(1-t)*t * mx + t**2 * ex
    y = (1-t)**2 * sy + 2*(1-t)*t * my + t**2 * ey
    r = 2 if i % 2 == 0 else 1
    draw_circle(int(x), int(y), r, fill="#C8C8C8")

# Thin axis lines from voice center
draw.line([(voice_cx + 68, voice_cy), (voice_cx + 180, voice_cy)], fill="#D8D8D8", width=1)
draw.line([(voice_cx, voice_cy + 68), (voice_cx, voice_cy + 160)], fill="#D8D8D8", width=1)

# Delicate vertical connector from rings down to bar chart
for i in range(8):
    y = voice_cy + 520 + i * 45
    if y < bar_start_y + 160:
        draw_circle(voice_cx + 420, y, 1, fill="#D0D0D0")


# ============================================================
# LAYER 9: Margin reference system — the scientific diagram feel
# ============================================================

# Left margin markers
for i in range(12):
    y = 400 + i * 230
    if y < H - 300:
        draw.line([(40, y), (70, y)], fill=BORDER, width=1)
        draw.text((75, y - 8), f"{i+1:02d}", font=font_mono_sm, fill="#D0D0D0")

# Bottom margin — color hex codes
hex_labels = [
    (start_x + 30, block_y + 100, "#1B5E7B"),
    (start_x + block_w + gap + 30, block_y + 100, "#D46A1E"),
    (start_x + 2*(block_w + gap) + 30, block_y + 100, "#2E7D4F"),
]
for hx, hy, label in hex_labels:
    draw.text((hx, hy), label, font=font_mono, fill="#FFFFFF")


# ============================================================
# LAYER 10: Section label — top right corner
# ============================================================

draw.text((W - 140, 60), "01 / 01", font=font_section, fill=BORDER, anchor="rt")
draw.text((W - 140, 85), "2026", font=font_section, fill=BORDER, anchor="rt")


# ============================================================
# REFINEMENT PASS — polish, spacing, cohesion
# ============================================================

# Subtle outer border — the frame
draw_rounded_rect(30, 30, W - 30, H - 30, 0, outline="#E8E8E8", width=1)

# Inner margin lines — breathing room
draw.line([(100, 80), (100, H - 80)], fill="#F0F0F0", width=1)
draw.line([(W - 100, 80), (W - 100, H - 80)], fill="#F0F0F0", width=1)

# Thin horizontal separator above color blocks
draw.line([(start_x, block_y - 60), (start_x + total, block_y - 60)], fill="#E8E8E8", width=1)

# Thin horizontal separator below tagline
draw.line([(145, 380), (700, 380)], fill="#E0E0E0", width=1)

# Small decorative mark — top left accent
draw.line([(140, 90), (180, 90)], fill=ORANGE, width=3)

# Bottom right corner mark — edition signature
draw.text((W - 140, H - 70), "CivicAid Voice", font=font_section, fill="#D0D0D0", anchor="rt")
draw.text((W - 140, H - 48), "OdiseIA4Good 2026", font=font_section, fill="#D0D0D0", anchor="rt")


# ============================================================
# SAVE
# ============================================================

output_path = "/Users/andreaavila/Documents/hakaton/civicaid-voice/design/assets/civic-tenderness-canvas.png"
canvas.save(output_path, "PNG", quality=95)
print(f"Canvas saved to: {output_path}")
print(f"Dimensions: {W}x{H}px")
