#!/usr/bin/env python3
"""
Clara — Tender Resonance Design Canvas  (v3 — museum-quality, refined)

"Ondas concentricas de una voz finalmente escuchada"

A3 Landscape — 420 x 297 mm
"""

import math, os, random
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W, H = landscape(A3)

TEAL   = HexColor('#1B5E7B')
ORANGE = HexColor('#D46A1E')
GREEN  = HexColor('#2E7D4F')
BG     = HexColor('#FAFAFA')
TDARK  = HexColor('#1A1A2E')

def tl(a):  return Color(0.106, 0.369, 0.482, alpha=a)
def og(a):  return Color(0.831, 0.416, 0.118, alpha=a)
def gn(a):  return Color(0.180, 0.490, 0.310, alpha=a)
def gy(a):  return Color(0.102, 0.102, 0.180, alpha=a)
def wh(a):  return Color(1, 1, 1, alpha=a)
def bl(a):  return Color(0.890, 0.949, 0.992, alpha=a)

FD = '/tmp/clara_fonts'
for n, f in {'IS':'InstrumentSans-Variable.ttf','ISI':'InstrumentSans-Italic-Variable.ttf',
             'Lo':'Lora-Variable.ttf','LoI':'Lora-Italic-Variable.ttf',
             'Wk':'WorkSans-Variable.ttf','It':'Italiana-Regular.ttf'}.items():
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, f)))

# ── primitives ──────────────────────────────────────────────────────
def dot(c,x,y,r,col):
    c.setFillColor(col); c.circle(x,y,r,stroke=0,fill=1)
def ring(c,x,y,r,col,w=0.5):
    c.setStrokeColor(col); c.setLineWidth(w); c.circle(x,y,r,stroke=1,fill=0)
def disc(c,x,y,r,col):
    c.setFillColor(col); c.circle(x,y,r,stroke=0,fill=1)
def rr(c,x,y,w,h,rad,fill=None,stroke=None,sw=0.5):
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    c.roundRect(x,y,w,h,rad, stroke=1 if stroke else 0, fill=1 if fill else 0)
def blob(c,cx,cy,br,col,sd=0,pts=72,v=0.15):
    c.setFillColor(col)
    p=c.beginPath()
    for i in range(pts+1):
        a=(2*math.pi*i)/pts
        rv=br*(1+v*0.5*math.sin(3*a+sd)+v*0.3*math.sin(5*a+sd*1.7)+v*0.2*math.sin(7*a+sd*2.3))
        x,y=cx+rv*math.cos(a),cy+rv*math.sin(a)
        if i==0: p.moveTo(x,y)
        else: p.lineTo(x,y)
    p.close(); c.drawPath(p,fill=1,stroke=0)
def farc(c,cx,cy,r,a0,sp,col,w=1):
    c.setStrokeColor(col); c.setLineWidth(w)
    c.arc(cx-r,cy-r,cx+r,cy+r,a0,sp)
def dring(c,cx,cy,r,col,w=0.5,d=(4,6)):
    c.setStrokeColor(col); c.setLineWidth(w); c.setDash(*d)
    c.circle(cx,cy,r,stroke=1,fill=0); c.setDash()
def gdisk(c,cx,cy,rm,cf,st=25):
    for i in range(st,0,-1):
        t=i/st; disc(c,cx,cy,rm*t,cf(t))

# ── icons ───────────────────────────────────────────────────────────
def i_house(c,cx,cy,s,col):
    c.setStrokeColor(col); c.setLineWidth(2.0); c.setLineCap(1); c.setLineJoin(1)
    p=c.beginPath()
    p.moveTo(cx-s*.5,cy+s*.02); p.lineTo(cx,cy+s*.52); p.lineTo(cx+s*.5,cy+s*.02)
    p.moveTo(cx-s*.38,cy+s*.02); p.lineTo(cx-s*.38,cy-s*.38); p.lineTo(cx+s*.38,cy-s*.38); p.lineTo(cx+s*.38,cy+s*.02)
    p.moveTo(cx-s*.1,cy-s*.38); p.lineTo(cx-s*.1,cy-s*.14); p.lineTo(cx+s*.1,cy-s*.14); p.lineTo(cx+s*.1,cy-s*.38)
    c.drawPath(p,fill=0,stroke=1)
def i_heart(c,cx,cy,s,col):
    c.setFillColor(col); s2=s*.42; p=c.beginPath()
    p.moveTo(cx,cy-s2*.3)
    p.curveTo(cx-s2*.6,cy+s2*.45,cx-s2*1.05,cy-s2*.08,cx,cy-s2*.88)
    p.curveTo(cx+s2*1.05,cy-s2*.08,cx+s2*.6,cy+s2*.45,cx,cy-s2*.3)
    p.close(); c.drawPath(p,fill=1,stroke=0)
def i_coin(c,cx,cy,s,col):
    c.setStrokeColor(col); c.setLineWidth(2.0); c.setLineCap(1)
    p=c.beginPath()
    p.moveTo(cx-s*.35,cy-s*.18)
    p.curveTo(cx-s*.28,cy+s*.08,cx+s*.28,cy+s*.08,cx+s*.35,cy-s*.18)
    c.drawPath(p,fill=0,stroke=1)
    c.circle(cx,cy+s*.30,s*.19,stroke=1,fill=0)
    c.setFont('IS',s*.20); c.setFillColor(col)
    c.drawCentredString(cx+.5,cy+s*.23,'\u20AC')
def i_doc(c,cx,cy,s,col):
    c.setStrokeColor(col); c.setLineWidth(2.0); c.setLineCap(1)
    p=c.beginPath()
    p.moveTo(cx-s*.25,cy+s*.42); p.lineTo(cx+s*.1,cy+s*.42); p.lineTo(cx+s*.3,cy+s*.22)
    p.lineTo(cx+s*.3,cy-s*.42); p.lineTo(cx-s*.25,cy-s*.42); p.close()
    c.drawPath(p,fill=0,stroke=1)
    p2=c.beginPath()
    p2.moveTo(cx+s*.1,cy+s*.42); p2.lineTo(cx+s*.1,cy+s*.22); p2.lineTo(cx+s*.3,cy+s*.22)
    c.drawPath(p2,fill=0,stroke=1)
    c.setLineWidth(1.3)
    for dy in [.10,-.04,-.18]:
        c.line(cx-s*.14,cy+s*dy,cx+s*(.16 if dy!=-.18 else .06),cy+s*dy)
def i_shield(c,cx,cy,s,col):
    c.setStrokeColor(col); c.setLineWidth(2.0); c.setLineCap(1); c.setLineJoin(1)
    p=c.beginPath()
    p.moveTo(cx,cy+s*.45); p.lineTo(cx-s*.35,cy+s*.25); p.lineTo(cx-s*.35,cy-s*.05)
    p.curveTo(cx-s*.35,cy-s*.38,cx,cy-s*.52,cx,cy-s*.52)
    p.curveTo(cx,cy-s*.52,cx+s*.35,cy-s*.38,cx+s*.35,cy-s*.05)
    p.lineTo(cx+s*.35,cy+s*.25); p.close()
    c.drawPath(p,fill=0,stroke=1)
    c.setLineWidth(2.2); p2=c.beginPath()
    p2.moveTo(cx-s*.13,cy-s*.02); p2.lineTo(cx-s*.02,cy-s*.15); p2.lineTo(cx+s*.17,cy+s*.12)
    c.drawPath(p2,fill=0,stroke=1)
def i_speech(c,cx,cy,s,col):
    c.setStrokeColor(col); c.setLineWidth(2.0); c.setLineCap(1)
    c.roundRect(cx-s*.35,cy-s*.02,s*.7,s*.42,s*.13,stroke=1,fill=0)
    p=c.beginPath()
    p.moveTo(cx-s*.1,cy-s*.02); p.lineTo(cx-s*.22,cy-s*.30); p.lineTo(cx+s*.08,cy-s*.02)
    c.drawPath(p,fill=0,stroke=1)
def i_people(c,cx,cy,s,col):
    """Two-person community icon with gentle, organic feel."""
    c.setStrokeColor(col); c.setLineWidth(1.8); c.setLineCap(1); c.setLineJoin(1)
    # Person 1 (left, slightly larger)
    c.circle(cx-s*.14, cy+s*.22, s*.13, stroke=1, fill=0)
    p=c.beginPath()
    p.moveTo(cx-s*.32, cy-s*.10)
    p.curveTo(cx-s*.32, cy+s*.05, cx+s*.04, cy+s*.05, cx+s*.04, cy-s*.10)
    c.drawPath(p,fill=0,stroke=1)
    # Person 2 (right, slightly smaller — perspective)
    c.circle(cx+s*.16, cy+s*.18, s*.11, stroke=1, fill=0)
    p2=c.beginPath()
    p2.moveTo(cx+s*.02, cy-s*.14)
    p2.curveTo(cx+s*.02, cy+s*.0, cx+s*.30, cy+s*.0, cx+s*.30, cy-s*.14)
    c.drawPath(p2,fill=0,stroke=1)
    # Connection arc between them (warmth)
    c.setLineWidth(1.0)
    farc(c,cx,cy-s*.20,s*.22,20,140,Color(col.red,col.green,col.blue,alpha=col.alpha*0.4),0.8)

def i_wave(c,cx,cy,s,col):
    """Sound wave / audio waveform icon."""
    c.setStrokeColor(col); c.setLineWidth(1.8); c.setLineCap(1)
    # Center bar
    c.line(cx, cy-s*.25, cx, cy+s*.25)
    # Side bars with decreasing height
    for dx, h in [(s*.12, .18), (s*.24, .12), (s*.36, .06)]:
        c.line(cx-dx, cy-s*h, cx-dx, cy+s*h)
        c.line(cx+dx, cy-s*h, cx+dx, cy+s*h)


# ════════════════════════════════════════════════════════════════════
def generate(path):
    c = canvas.Canvas(path, pagesize=landscape(A3))
    c.setTitle("Clara \u2014 Tender Resonance")

    # ── BG ──────────────────────────────────────────────────────────
    c.setFillColor(BG); c.rect(0,0,W,H,stroke=0,fill=1)

    # Warm wash bottom-left (lighter than v2)
    for i in range(50):
        t=i/50.0
        c.setFillColor(og(0.018*(1-t)**1.5))
        c.rect(0, t*H*0.40, W*0.55, H*0.40/50, stroke=0, fill=1)

    # Cool wash top-right
    for i in range(40):
        t=i/40.0
        c.setFillColor(tl(0.015*(1-t)**1.3))
        c.rect(W*0.45, H-t*H*0.30, W*0.55, H*0.30/40, stroke=0, fill=1)

    # Green whisper bottom-right
    for i in range(30):
        t=i/30.0
        c.setFillColor(gn(0.008*(1-t)))
        c.rect(W*0.6, t*H*0.20, W*0.4, H*0.20/30, stroke=0, fill=1)

    # ── ATMOSPHERIC BLOBS ───────────────────────────────────────────
    blob(c, W*.07, H*.30, 100, og(0.025), sd=0.7)
    blob(c, W*.88, H*.75, 90, tl(0.020), sd=2.5)
    blob(c, W*.50, H*.90, 60, gn(0.015), sd=5.3)
    blob(c, W*.78, H*.10, 70, og(0.015), sd=4.1)
    blob(c, W*.18, H*.82, 80, bl(0.20), sd=1.2)
    blob(c, W*.38, H*.20, 110, bl(0.08), sd=6.1)
    blob(c, W*.82, H*.48, 85, bl(0.06), sd=7.2)
    blob(c, W*.60, H*.68, 65, og(0.010), sd=9.3)
    blob(c, W*.25, H*.70, 50, tl(0.012), sd=8.8)
    blob(c, W*.92, H*.28, 55, gn(0.012), sd=3.2)

    # ── PRIMARY VOICE RIPPLES ───────────────────────────────────────
    VX, VY = W*0.31, H*0.54

    # Very subtle radial glow (much lighter than v2)
    gdisk(c, VX, VY, 240, lambda t: tl(0.018*t**2.5), st=35)

    # Main concentric rings — the voice expanding
    for i in range(26):
        r = 52 + i * 28
        pr = i/26.0
        a = 0.048 * (1-pr)**1.3
        w = 0.6 + 1.0 * (1-pr)
        ring(c, VX, VY, r, tl(a), w)

    # Warm interleaved rings
    for i in range(16):
        r = 68 + i * 38
        ring(c, VX, VY, r, og(0.018*(1-i/16.0)), 0.35)

    # Dashed texture rings
    for i in range(7):
        r = 100 + i * 60
        dring(c, VX, VY, r, tl(0.028*(1-i/7.0)), 0.3, (3, 8+i*2))

    # ── SECONDARY RIPPLES — community ──────────────────────────────
    CX, CY = W*0.74, H*0.36

    gdisk(c, CX, CY, 150, lambda t: gn(0.014*t**2.5), st=25)

    for i in range(18):
        r = 35 + i * 24
        a = 0.035*(1-i/18.0)**1.3
        ring(c, CX, CY, r, gn(a), 0.5+0.7*(1-i/18.0))

    for i in range(6):
        r = 55 + i * 35
        dring(c, CX, CY, r, gn(0.020*(1-i/6.0)), 0.25, (2,10+i*2))

    # ── TERTIARY RIPPLES — hope ────────────────────────────────────
    HX, HY = W*0.56, H*0.80

    gdisk(c, HX, HY, 100, lambda t: og(0.012*t**2), st=18)

    for i in range(10):
        r = 28 + i * 22
        ring(c, HX, HY, r, og(0.028*(1-i/10.0)), 0.4)

    # ── SMALL RIPPLE — bottom left — Maria's voice ─────────────────
    MRX, MRY = W*0.12, H*0.32
    gdisk(c, MRX, MRY, 80, lambda t: og(0.010*t**2), st=12)
    for i in range(10):
        r = 15 + i * 13
        ring(c, MRX, MRY, r, og(0.030*(1-i/10.0)**1.2), 0.35+0.3*(1-i/10.0))
    # A few dashed rings
    for i in range(3):
        dring(c, MRX, MRY, 50+i*30, og(0.018*(1-i/3.0)), 0.25, (2,8))

    # ── SMALL RIPPLE — Ahmed's area ────────────────────────────────
    ARX, ARY = W*0.08, H*0.16
    for i in range(6):
        r = 12 + i * 10
        ring(c, ARX, ARY, r, gn(0.022*(1-i/6.0)), 0.25)

    # ── TINY RIPPLE — Fatima's area ──────────────────────────────────
    FRX, FRY = W*0.20, H*0.08
    for i in range(5):
        r = 10 + i * 8
        ring(c, FRX, FRY, r, tl(0.018*(1-i/5.0)), 0.2)

    # ── ARC FRAGMENTS ───────────────────────────────────────────────
    frags = [
        (VX,VY,150,10,72,tl(0.12),1.4),
        (VX,VY,195,195,48,tl(0.09),1.1),
        (VX,VY,240,98,38,tl(0.07),0.8),
        (VX,VY,285,308,32,og(0.08),0.9),
        (VX,VY,335,48,52,tl(0.05),0.6),
        (VX,VY,385,158,42,gn(0.04),0.5),
        (VX,VY,440,265,28,tl(0.03),0.4),
        (VX,VY,500,80,22,og(0.025),0.35),
        (VX,VY,560,190,18,tl(0.02),0.3),
        (CX,CY,120,38,58,gn(0.10),1.2),
        (CX,CY,165,178,42,gn(0.07),0.9),
        (CX,CY,210,280,35,tl(0.05),0.7),
        (CX,CY,258,12,28,gn(0.04),0.5),
        (HX,HY,95,22,48,og(0.08),0.9),
        (HX,HY,135,165,32,og(0.06),0.6),
        (HX,HY,175,285,28,tl(0.04),0.5),
        (MRX,MRY,70,40,50,og(0.06),0.5),
        (MRX,MRY,100,200,35,og(0.04),0.4),
        (ARX,ARY,45,60,55,gn(0.05),0.4),
        (FRX,FRY,35,10,45,tl(0.04),0.3),
    ]
    for cx,cy,r,a0,sp,col,w in frags:
        farc(c,cx,cy,r,a0,sp,col,w)

    # ── GHOST RINGS ─────────────────────────────────────────────────
    for i in range(9):
        ring(c, W*.46, H*.49, 320+i*50, tl(0.008*(1-i/9.0)), 0.22)

    # ── GRAVITATIONAL THREADS ───────────────────────────────────────
    c.setLineCap(1)

    # Voice center -> cards
    c.setStrokeColor(tl(0.05)); c.setLineWidth(0.45)
    p=c.beginPath()
    p.moveTo(VX+48,VY+5)
    p.curveTo(VX+140,VY+35, W*.44,H*.60, W*.53,H*.62)
    c.drawPath(p,fill=0,stroke=1)

    # Voice -> community
    c.setStrokeColor(tl(0.035)); c.setLineWidth(0.35)
    p=c.beginPath()
    p.moveTo(VX+42,VY-15)
    p.curveTo(W*.48,H*.42, W*.60,H*.37, CX-40,CY)
    c.drawPath(p,fill=0,stroke=1)

    # Voice -> trust
    c.setStrokeColor(tl(0.03)); c.setLineWidth(0.3)
    p=c.beginPath()
    p.moveTo(VX+38,VY+20)
    p.curveTo(W*.50,H*.74, W*.74,H*.80, W*.87,H*.82)
    c.drawPath(p,fill=0,stroke=1)

    # Maria ripple -> voice center
    c.setStrokeColor(og(0.04)); c.setLineWidth(0.3)
    p=c.beginPath()
    p.moveTo(MRX+20,MRY+10)
    p.curveTo(W*.18,H*.42, W*.24,H*.50, VX-45,VY-5)
    c.drawPath(p,fill=0,stroke=1)

    # Ahmed area -> voice center (faint)
    c.setStrokeColor(gn(0.03)); c.setLineWidth(0.25)
    p=c.beginPath()
    p.moveTo(ARX+20,ARY+15)
    p.curveTo(W*.12,H*.28, W*.20,H*.44, VX-42,VY-18)
    c.drawPath(p,fill=0,stroke=1)

    # Fatima area -> voice center (faintest)
    c.setStrokeColor(tl(0.025)); c.setLineWidth(0.2)
    p=c.beginPath()
    p.moveTo(FRX+15,FRY+12)
    p.curveTo(W*.22,H*.15, W*.26,H*.35, VX-38,VY-25)
    c.drawPath(p,fill=0,stroke=1)

    # ── ACCENT DOTS ─────────────────────────────────────────────────
    random.seed(42)
    for _ in range(40):
        dot(c, random.uniform(W*.04,W*.96), random.uniform(H*.04,H*.96),
            random.uniform(1.0,3.2), [tl,og,gn][random.randint(0,2)](random.uniform(.03,.10)))

    for x,y,r,col in [
        (W*.16,H*.68,3.8,tl(.18)), (W*.23,H*.63,2.6,og(.16)),
        (W*.84,H*.86,4.2,og(.10)), (W*.60,H*.07,3.3,tl(.14)),
        (W*.44,H*.73,2.8,gn(.10)), (W*.37,H*.93,3.2,gn(.12)),
        (W*.76,H*.94,2.5,tl(.08)), (W*.09,H*.11,3.0,og(.10)),
        (W*.50,H*.50,2.0,og(.06)), (W*.68,H*.15,2.5,gn(.08)),
    ]:
        dot(c,x,y,r,col)


    # ══════════════════════════════════════════════════════════════════
    #  FOREGROUND
    # ══════════════════════════════════════════════════════════════════

    # ── "C" LOGO ────────────────────────────────────────────────────
    # Softer glow
    gdisk(c,VX,VY,58, lambda t: tl(0.035*t**2), st=18)

    disc(c,VX,VY,42,wh(0.96))
    disc(c,VX,VY,40,wh(1))

    ring(c,VX,VY,40,tl(0.60),2.5)
    ring(c,VX,VY,48,tl(0.16),0.7)
    ring(c,VX,VY,54,tl(0.07),0.35)

    # Broken decorative arcs
    for a0,sp in [(15,40),(95,28),(175,45),(268,32)]:
        farc(c,VX,VY,54,a0,sp,tl(0.10),0.5)

    # "C"
    c.setFillColor(TEAL)
    c.setFont('Lo',42)
    c.drawCentredString(VX-1, VY-14, 'C')

    dot(c, VX+15, VY+7, 4.2, ORANGE)

    # wordmark
    c.setFillColor(gy(0.82))
    c.setFont('IS',14)
    c.drawCentredString(VX, VY-60, 'clara')

    c.setFillColor(gy(0.40))
    c.setFont('Wk',7)
    c.drawCentredString(VX, VY-74, 'asistente de voz c\u00edvica')

    # ── ANCHOR PHRASE ───────────────────────────────────────────────
    PX, PY = W*0.31, H*0.24

    blob(c, PX, PY+5, 80, og(0.018), sd=8.4)

    c.setFillColor(TDARK)
    c.setFont('LoI',30)
    c.drawCentredString(PX, PY, 'Tu voz tiene poder')

    # Underline with fade
    c.setStrokeColor(og(0.40)); c.setLineWidth(1.1); c.setLineCap(1)
    c.line(PX-95,PY-14, PX+95,PY-14)
    for i in range(12):
        t=i/12.0
        c.setStrokeColor(og(0.40*(1-t))); c.setLineWidth(1.1*(1-t))
        c.line(PX-95-i*3,PY-14, PX-95-(i+1)*3,PY-14)
        c.line(PX+95+i*3,PY-14, PX+95+(i+1)*3,PY-14)

    c.setFillColor(gy(0.50))
    c.setFont('LoI',9.5)
    c.drawCentredString(PX, PY-30, 'ondas conc\u00e9ntricas de una voz finalmente escuchada')

    # ── TOPIC CARDS ─────────────────────────────────────────────────
    cards = [
        dict(lb='Vivienda',          su='Ayuda de vivienda',         ic=i_house, co=TEAL,   tf=tl, x=W*.535,y=H*.60, a=1.0),
        dict(lb='Tarjeta Sanitaria', su='Acceso a salud',            ic=i_heart, co=ORANGE, tf=og, x=W*.685,y=H*.64, a=-0.6),
        dict(lb='IMV',               su='Ingreso m\u00ednimo vital', ic=i_coin,  co=GREEN,  tf=gn, x=W*.585,y=H*.41, a=0.3),
        dict(lb='Empadronamiento',   su='Registro municipal',        ic=i_doc,   co=TEAL,   tf=tl, x=W*.745,y=H*.44, a=-0.8),
    ]

    cw,ch,cr = 120,105,15

    for cd in cards:
        cx,cy = cd['x'],cd['y']
        c.saveState()
        c.translate(cx+cw/2,cy+ch/2); c.rotate(cd['a']); c.translate(-(cx+cw/2),-(cy+ch/2))

        # Shadow layers
        rr(c,cx+3,cy-4,cw,ch,cr,fill=Color(0,0,0,alpha=0.04))
        rr(c,cx+1.5,cy-2,cw,ch,cr,fill=Color(0,0,0,alpha=0.025))

        # Body
        rr(c,cx,cy,cw,ch,cr,fill=wh(1),stroke=Color(0,0,0,alpha=0.06),sw=0.5)

        # Color tint strip
        c.saveState()
        p=c.beginPath(); p.roundRect(cx,cy,cw,ch,cr)
        c.clipPath(p,stroke=0,fill=0)
        c.setFillColor(cd['tf'](0.07))
        c.rect(cx, cy+ch*.65, cw, ch*.35, stroke=0, fill=1)
        for gi in range(6):
            c.setFillColor(cd['tf'](0.07*(1-gi/6.0)))
            c.rect(cx, cy+ch*.65-gi*2, cw, 2, stroke=0, fill=1)
        c.restoreState()

        # Icon bg
        disc(c, cx+cw/2, cy+ch*.67, 17, cd['tf'](0.05))

        # Icon
        cd['ic'](c, cx+cw/2, cy+ch*.67, 28, cd['co'])

        # Label
        c.setFillColor(gy(0.80))
        c.setFont('IS',10)
        c.drawCentredString(cx+cw/2, cy+23, cd['lb'])

        # Sub
        c.setFillColor(gy(0.35))
        c.setFont('Wk',6.5)
        c.drawCentredString(cx+cw/2, cy+12, cd['su'])

        # Bottom accent
        c.setStrokeColor(cd['tf'](0.10)); c.setLineWidth(0.5)
        c.line(cx+18, cy+5, cx+cw-18, cy+5)

        c.restoreState()

    # ── TRUST BADGES ────────────────────────────────────────────────
    TX,TY = W*.885, H*.82
    gdisk(c,TX,TY,34,lambda t:bl(.30*t),st=12)
    disc(c,TX,TY,27,wh(.92)); i_shield(c,TX,TY,23,TEAL)
    ring(c,TX,TY,29,tl(.14),.45)
    c.setFillColor(gy(.48)); c.setFont('Wk',6.5)
    c.drawCentredString(TX,TY-36,'Datos protegidos')
    c.setFillColor(gy(.26)); c.setFont('LoI',5.5)
    c.drawCentredString(TX,TY-46,'Tu informaci\u00f3n es tuya')

    VBX,VBY = W*.885, H*.62
    gdisk(c,VBX,VBY,34,lambda t:gn(.06*t),st=12)
    disc(c,VBX,VBY,27,wh(.92)); i_speech(c,VBX,VBY,23,GREEN)
    ring(c,VBX,VBY,29,gn(.14),.45)
    c.setFillColor(gy(.48)); c.setFont('Wk',6.5)
    c.drawCentredString(VBX,VBY-36,'Habla, yo escucho')
    c.setFillColor(gy(.26)); c.setFont('LoI',5.5)
    c.drawCentredString(VBX,VBY-46,'Sin prisa, sin juicio')

    # ── THIRD BADGE: Comunidad ──────────────────────────────────────
    CBX,CBY = W*.885, H*.42
    gdisk(c,CBX,CBY,34,lambda t:og(.06*t),st=12)
    disc(c,CBX,CBY,27,wh(.92)); i_people(c,CBX,CBY,23,ORANGE)
    ring(c,CBX,CBY,29,og(.14),.45)
    c.setFillColor(gy(.48)); c.setFont('Wk',6.5)
    c.drawCentredString(CBX,CBY-36,'Cerca de ti')
    c.setFillColor(gy(.26)); c.setFont('LoI',5.5)
    c.drawCentredString(CBX,CBY-46,'Siempre accesible')

    # ── PERSONA WHISPERS ────────────────────────────────────────────
    blob(c, W*.14, H*.37, 42, og(.018), sd=9.1)
    blob(c, W*.09, H*.15, 38, gn(.018), sd=10.2)
    blob(c, W*.20, H*.08, 35, tl(.015), sd=11.5)

    personas = [
        (W*.10, H*.375, 'Mar\u00eda, 74',             'manos que tiemblan, voz que no',       og(.45), og(.25)),
        (W*.06, H*.150, 'Ahmed, Dakar \u2192 Madrid',  'entre idiomas, buscando un puente',    gn(.45), gn(.25)),
        (W*.17, H*.070, 'Fatima',                       'las letras no, pero la voz s\u00ed',   tl(.45), tl(.25)),
    ]
    for x,y,nm,ds,nc,dc in personas:
        dot(c,x-7,y+3,3,nc)
        c.setFillColor(nc); c.setFont('LoI',8.5)
        c.drawString(x,y,nm)
        c.setFillColor(dc); c.setFont('LoI',6.5)
        c.drawString(x,y-13,ds)

    # ── DESIGN PRINCIPLES — right column ────────────────────────────
    concepts = [
        ('Ondas conc\u00e9ntricas',       'Voice ripples expanding outward',  tl(.50)),
        ('Ritmo biol\u00f3gico',           'Resting heartbeat pace',           og(.50)),
        ('Espacio generoso',               'Room to breathe, room to think',   gn(.50)),
        ('Color como temperatura',         'Emotional warmth through hue',     tl(.50)),
        ('Tipograf\u00eda compa\u00f1era', 'Quiet companionship in every word', og(.50)),
    ]

    COX,COY = W*.875, H*.28
    rr(c, COX-55, COY-len(concepts)*32+12, 160, len(concepts)*32+8, 7, fill=wh(.40))

    c.setFillColor(gy(.25)); c.setFont('Wk',5.5)
    c.drawString(COX-48, COY+10, 'PRINCIPIOS DE DISE\u00d1O')
    c.setStrokeColor(tl(.08)); c.setLineWidth(.3)
    c.line(COX-48, COY+6, COX+98, COY+6)

    for i,(es,en,dc) in enumerate(concepts):
        y=COY-i*32
        dot(c,COX-48,y+2,3.2,dc)
        c.setFillColor(gy(.75)); c.setFont('IS',8)
        c.drawString(COX-40,y,es)
        c.setFillColor(gy(.28)); c.setFont('LoI',6)
        c.drawString(COX-40,y-11,en)

    # ── HEARTBEAT ───────────────────────────────────────────────────
    HBX,HBY = W*.04, H*.52
    HBL = W*.085

    c.setStrokeColor(og(.18)); c.setLineWidth(1.1); c.setLineCap(1)
    p=c.beginPath()
    for i in range(101):
        t=i/100
        x=HBX+t*HBL
        if .32<t<.38: yo=13*math.sin((t-.32)/.06*math.pi)
        elif .40<t<.48: yo=-9*math.sin((t-.40)/.08*math.pi)+17*math.sin((t-.40)/.08*math.pi*2)
        elif .50<t<.56: yo=6*math.sin((t-.50)/.06*math.pi)
        else: yo=0
        if i==0: p.moveTo(x,HBY+yo)
        else: p.lineTo(x,HBY+yo)
    c.drawPath(p,fill=0,stroke=1)

    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawCentredString(HBX+HBL/2, HBY-18, 'ritmo biol\u00f3gico')

    # ── INTERACTION RIPPLE DEMO ─────────────────────────────────────
    IRX,IRY = W*.53, H*.82

    c.setFillColor(gy(.20)); c.setFont('Wk',5.5)
    c.drawCentredString(IRX+25, IRY+48, 'voice interaction ripple')

    for i in range(7):
        r=6+i*6.5
        ring(c,IRX,IRY,r, og(.28*(1-i/7.0)**1.5), max(1.6-i*.2,.3))
    dot(c,IRX,IRY,4.5,ORANGE)

    # Response ripple
    for i in range(5):
        ring(c,IRX+70,IRY+3,r:=4+i*5, tl(.14*(1-i/5.0)), .7)
    dot(c,IRX+70,IRY+3,2.8,tl(.40))

    c.setFillColor(gy(.16)); c.setFont('Wk',4.5)
    c.drawCentredString(IRX,IRY-26,'voz')
    c.drawCentredString(IRX+70,IRY-22,'respuesta')

    # Connecting curve between voice and response
    c.setStrokeColor(gy(.10)); c.setLineWidth(.5); c.setLineCap(1)
    p=c.beginPath()
    p.moveTo(IRX+22,IRY+1)
    p.curveTo(IRX+32,IRY+6, IRX+40,IRY+6, IRX+48,IRY+3)
    c.drawPath(p,fill=0,stroke=1)
    # Arrowhead (tiny, elegant)
    p2=c.beginPath()
    p2.moveTo(IRX+44,IRY+6); p2.lineTo(IRX+50,IRY+3); p2.lineTo(IRX+44,IRY+0)
    c.drawPath(p2,fill=0,stroke=1)

    # ── TYPOGRAPHY SPECIMEN ─────────────────────────────────────────
    TPX,TPY = W*.35, H*.065

    rr(c, TPX-8, TPY-12, 140, 54, 5, fill=wh(.50))

    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(TPX, TPY+32, 'TIPOGRAF\u00cdA')
    c.setStrokeColor(tl(.08)); c.setLineWidth(.25)
    c.line(TPX,TPY+28, TPX+120,TPY+28)

    c.setFillColor(gy(.55)); c.setFont('LoI',11)
    c.drawString(TPX, TPY+14, 'Lora Italic')
    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(TPX+72,TPY+16, '\u2014 voz po\u00e9tica')

    c.setFillColor(gy(.55)); c.setFont('IS',10)
    c.drawString(TPX, TPY, 'Instrument Sans')
    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(TPX+92,TPY+1, '\u2014 etiquetas')

    c.setFillColor(gy(.55)); c.setFont('Wk',9)
    c.drawString(TPX, TPY-13, 'Work Sans')
    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(TPX+60,TPY-12, '\u2014 sistema')

    # ── COLOR PALETTE ───────────────────────────────────────────────
    SPX,SPY = W*.55, H*.06

    rr(c, SPX-8, SPY-10, 158, 38, 5, fill=wh(.50))

    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(SPX, SPY+18, 'PALETA DE COLOR')
    c.setStrokeColor(tl(.08)); c.setLineWidth(.25)
    c.line(SPX,SPY+14, SPX+138,SPY+14)

    swatches = [
        (TEAL,'#1B5E7B','Confianza'), (ORANGE,'#D46A1E','Calidez'),
        (GREEN,'#2E7D4F','Esperanza'), (HexColor('#E3F2FD'),'#E3F2FD','Info'),
        (HexColor('#FAFAFA'),'#FAFAFA','Fondo'),
    ]
    for i,(col,hx,nm) in enumerate(swatches):
        sx=SPX+i*28
        c.setFillColor(col); c.setStrokeColor(Color(0,0,0,alpha=.08)); c.setLineWidth(.4)
        c.circle(sx+7,SPY+2,7,stroke=1,fill=1)
        c.setFillColor(gy(.25)); c.setFont('Wk',3.5)
        c.drawCentredString(sx+7,SPY-9,hx)

    # ── LANGUAGES ───────────────────────────────────────────────────
    LX,LY = W*.08, H*.90

    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(LX, LY+12, 'IDIOMAS')

    for i,(lang,lc) in enumerate([('ES',TEAL),('FR',GREEN),('AR',ORANGE),('EN',tl(.4))]):
        lx=LX+i*28
        fc=Color(lc.red,lc.green,lc.blue,alpha=.08)
        sc=Color(lc.red,lc.green,lc.blue,alpha=.22)
        tc=Color(lc.red,lc.green,lc.blue,alpha=.65)
        rr(c,lx,LY-3,22,14,7,fill=fc,stroke=sc,sw=.4)
        c.setFillColor(tc); c.setFont('IS',6.5)
        c.drawCentredString(lx+11,LY,lang)

    # ── PHILOSOPHY STATEMENT ────────────────────────────────────────
    PSX,PSY = W*.445, H*.22

    rr(c, PSX-10, PSY-52, 185, 78, 8, fill=wh(.65))
    dot(c, PSX+168, PSY+16, 2.2, tl(.18))

    c.setFillColor(gy(.22)); c.setFont('Wk',5)
    c.drawString(PSX, PSY+14, 'FILOSOF\u00cdA')
    c.setStrokeColor(tl(.08)); c.setLineWidth(.25)
    c.line(PSX,PSY+10, PSX+160,PSY+10)

    c.setFillColor(gy(.52))
    c.setFont('LoI',8)
    c.drawString(PSX, PSY-2, 'La tecnolog\u00eda c\u00edvica debe sentirse como')
    c.drawString(PSX, PSY-14, 'una mano c\u00e1lida extendida, no un formulario.')
    c.drawString(PSX, PSY-26, 'Cada p\u00edxel, un gesto de cuidado.')

    c.setFillColor(gy(.28)); c.setFont('LoI',6.5)
    c.drawString(PSX, PSY-42, 'Every wave is a promise of listening.')

    # ── HEADER ──────────────────────────────────────────────────────
    c.setFillColor(gy(.52)); c.setFont('IS',8)
    c.drawString(30, H-30, 'CLARA  \u00B7  CIVIC AID VOICE ASSISTANT')
    c.setStrokeColor(tl(.20)); c.setLineWidth(.5)
    c.line(30,H-37,235,H-37)

    c.setFillColor(TEAL); c.setFont('It',19)
    c.drawRightString(W-30, H-34, 'Tender Resonance')
    c.setFillColor(gy(.25)); c.setFont('Wk',6.5)
    c.drawRightString(W-30, H-47, 'Design Philosophy Canvas  \u00B7  2026')
    dot(c, W-30, H-53, 1.8, tl(.22))

    # ── FOOTER ──────────────────────────────────────────────────────
    c.setFillColor(gy(.20)); c.setFont('Wk',5.5)
    c.drawString(30, 18, 'Clara  \u00B7  Civic Aid Voice Assistant  \u00B7  Design System v1.0')
    c.setFillColor(gy(.25)); c.setFont('LoI',6.5)
    c.drawRightString(W-30, 18, 'Cada onda es una promesa de escucha')

    # ── SUBTLE AUDIO WAVEFORM — bottom edge ─────────────────────────
    # Very faint sound wave running along the bottom — the voice medium
    c.setStrokeColor(tl(0.035)); c.setLineWidth(0.4); c.setLineCap(1)
    random.seed(77)
    wave_y = 38
    p=c.beginPath()
    for i in range(200):
        x = W*0.08 + (W*0.84) * i/200
        # Gentle wave with some variation
        amp = 3 + 5 * abs(math.sin(i*0.05)) * random.uniform(0.5,1.0)
        y = wave_y + amp * math.sin(i*0.15 + random.uniform(-0.3,0.3))
        if i==0: p.moveTo(x,y)
        else: p.lineTo(x,y)
    c.drawPath(p,fill=0,stroke=1)

    # Second waveform layer, slightly offset
    c.setStrokeColor(og(0.020)); c.setLineWidth(0.3)
    random.seed(88)
    p2=c.beginPath()
    for i in range(200):
        x = W*0.08 + (W*0.84) * i/200
        amp = 2 + 4 * abs(math.sin(i*0.07+1.5)) * random.uniform(0.4,1.0)
        y = wave_y + amp * math.sin(i*0.18 + 0.7 + random.uniform(-0.2,0.2))
        if i==0: p2.moveTo(x,y)
        else: p2.lineTo(x,y)
    c.drawPath(p2,fill=0,stroke=1)

    # ── FRAME & MARKS ───────────────────────────────────────────────
    m=15
    c.setStrokeColor(tl(.05)); c.setLineWidth(.25)
    c.roundRect(m,m,W-2*m,H-2*m,3,stroke=1,fill=0)

    mk=13
    c.setStrokeColor(tl(.10)); c.setLineWidth(.4)
    for x1,y1,x2,y2 in [
        (m-6,H-m,m-6+mk,H-m),(m,H-m+6,m,H-m+6-mk),
        (W-m+6,H-m,W-m+6-mk,H-m),(W-m,H-m+6,W-m,H-m+6-mk),
        (m-6,m,m-6+mk,m),(m,m-6,m,m-6+mk),
        (W-m+6,m,W-m+6-mk,m),(W-m,m-6,W-m,m-6+mk),
    ]:
        c.line(x1,y1,x2,y2)

    # ── AMBIENT DUST ────────────────────────────────────────────────
    random.seed(137)
    for _ in range(60):
        dot(c, random.uniform(W*.02,W*.98), random.uniform(H*.02,H*.98),
            random.uniform(.3,.8), [tl,og,gn][random.randint(0,2)](random.uniform(.012,.035)))

    # ════════════════════════════════════════════════════════════════
    c.save()
    print(f"Saved: {path}")
    print(f"Size: {W:.0f}x{H:.0f} pts = {W/mm:.0f}x{H/mm:.0f} mm")


if __name__ == '__main__':
    d='/Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/design'
    os.makedirs(d,exist_ok=True)
    generate(os.path.join(d,'clara-tender-resonance.pdf'))
