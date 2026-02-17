"""
CivicAid Voice / Clara — Sprint 3 Documento Tecnico PDF
Design: Civic Meridians — clean dark pages, teal/amber accents.
~14 pages, all content from Sprint3_DocTecnico.md
"""

import math
import os
import textwrap
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = os.path.join(os.path.dirname(__file__), "Sprint3_DocTecnico.pdf")

# Fonts
SYS = "/System/Library/Fonts/Supplemental"
LIB = "/Library/Fonts"
pdfmetrics.registerFont(TTFont("DINBold", os.path.join(SYS, "DIN Alternate Bold.ttf")))
pdfmetrics.registerFont(TTFont("DINCondBold", os.path.join(SYS, "DIN Condensed Bold.ttf")))
pdfmetrics.registerFont(TTFont("Verdana-R", os.path.join(SYS, "Verdana.ttf")))
pdfmetrics.registerFont(TTFont("Verdana-B", os.path.join(SYS, "Verdana Bold.ttf")))
pdfmetrics.registerFont(TTFont("Georgia", os.path.join(SYS, "Georgia.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-I", os.path.join(SYS, "Georgia Italic.ttf")))
pdfmetrics.registerFont(TTFont("Futura", os.path.join(SYS, "Futura.ttc")))
pdfmetrics.registerFont(TTFont("SC", os.path.join(LIB, "SourceCodePro-Regular.ttf")))
pdfmetrics.registerFont(TTFont("SCBold", os.path.join(LIB, "SourceCodePro-Bold.ttf")))
pdfmetrics.registerFont(TTFont("SCLight", os.path.join(LIB, "SourceCodePro-Light.ttf")))

# Palette
BG = HexColor("#080E1C")
CARD = HexColor("#101C32")
TEAL = HexColor("#2DD4A8")
TEAL_DIM = HexColor("#134A3A")
TEAL_GLOW = HexColor("#3AEDC4")
AMBER = HexColor("#F5A623")
WHITE = HexColor("#ECF0F4")
MUTED = HexColor("#6B7D94")
FAINT = HexColor("#2A3A50")
BLUE = HexColor("#4A8EF5")
CORAL = HexColor("#E8706A")

W, H = A4  # 595 x 842

# Margins
ML, MR, MT, MB = 50, 50, 55, 50


class DocBuilder:
    """Helper for multi-page document with automatic page breaks."""

    def __init__(self):
        self.c = canvas.Canvas(OUT, pagesize=A4)
        self.c.setTitle("CivicAid Voice / Clara — Documento Tecnico Sprint 3")
        self.c.setAuthor("Equipo Clara — UDIT")
        self.y = H - MT
        self.page = 0
        self._new_page()

    def _bg(self):
        self.c.setFillColor(BG)
        self.c.rect(0, 0, W, H, fill=1, stroke=0)
        # Dot matrix
        self.c.setFillColor(Color(0.08, 0.12, 0.20, alpha=0.25))
        for x in range(15, int(W), 20):
            for y_ in range(15, int(H), 20):
                self.c.circle(x, y_, 0.3, fill=1, stroke=0)
        # Meridian arcs
        self.c.saveState()
        for i in range(4):
            ang = self.page * 40 + i * 90
            cx = W * 0.5 + math.cos(math.radians(ang)) * 200
            cy = H * 0.5 + math.sin(math.radians(ang)) * 300
            r = 150 + i * 50
            self.c.setStrokeColor(Color(0.10, 0.20, 0.32, alpha=0.10))
            self.c.setLineWidth(0.5)
            p = self.c.beginPath()
            p.arc(cx - r, cy - r, cx + r, cy + r, ang, ang + 50)
            self.c.drawPath(p, fill=0, stroke=1)
        self.c.restoreState()

    def _new_page(self):
        if self.page > 0:
            self.c.showPage()
        self.page += 1
        self._bg()
        self.y = H - MT
        # Page number
        self.c.setFillColor(FAINT)
        self.c.setFont("SCLight", 6)
        self.c.drawRightString(W - MR, 25, f"{self.page}")
        # Footer line
        self.c.setStrokeColor(FAINT)
        self.c.setLineWidth(0.3)
        self.c.line(ML, 35, W - MR, 35)

    def _check(self, needed=30):
        if self.y < MB + needed:
            self._new_page()

    def space(self, h=12):
        self.y -= h
        self._check()

    def section_num(self, num, text):
        """Section header: 01 FUNCIONALIDADES"""
        self._check(50)
        self.space(18)
        self.c.setFillColor(TEAL)
        self.c.setFont("SC", 8)
        self.c.drawString(ML, self.y, num)
        self.y -= 22
        self.c.setFillColor(WHITE)
        self.c.setFont("DINBold", 22)
        self.c.drawString(ML, self.y, text)
        self.y -= 8
        # Underline
        self.c.setStrokeColor(TEAL_DIM)
        self.c.setLineWidth(0.5)
        self.c.line(ML, self.y, ML + 200, self.y)
        self.y -= 14

    def subsection(self, text):
        self._check(30)
        self.space(8)
        self.c.setFillColor(TEAL)
        self.c.setFont("Verdana-B", 10)
        self.c.drawString(ML, self.y, text)
        self.y -= 16

    def para(self, text, font="Verdana-R", size=8, color=MUTED, wrap=85):
        lines = []
        for raw_line in text.split("\n"):
            lines.extend(textwrap.wrap(raw_line, wrap) if raw_line.strip() else [""])
        for l in lines:
            self._check(14)
            self.c.setFillColor(color)
            self.c.setFont(font, size)
            self.c.drawString(ML, self.y, l)
            self.y -= 12

    def bold_para(self, text, wrap=85):
        self.para(text, font="Verdana-B", size=8, color=WHITE, wrap=wrap)

    def mono(self, text, size=7, color=MUTED):
        for l in text.split("\n"):
            self._check(12)
            self.c.setFillColor(color)
            self.c.setFont("SC", size)
            self.c.drawString(ML + 10, self.y, l)
            self.y -= 11

    def table(self, headers, rows, col_widths=None):
        """Simple table with header row and data rows."""
        n_cols = len(headers)
        total_w = W - ML - MR
        if col_widths is None:
            col_widths = [total_w / n_cols] * n_cols

        self._check(20 + len(rows) * 15)

        # Header
        x = ML
        self.c.setFillColor(Color(0.06, 0.10, 0.18, alpha=0.6))
        self.c.rect(ML - 2, self.y - 4, total_w + 4, 14, fill=1, stroke=0)
        for i, h in enumerate(headers):
            self.c.setFillColor(MUTED)
            self.c.setFont("SCBold", 6.5)
            self.c.drawString(x, self.y, h)
            x += col_widths[i]
        self.y -= 16

        # Rows
        for ri, row in enumerate(rows):
            self._check(15)
            if ri % 2 == 0:
                self.c.setFillColor(Color(0.04, 0.07, 0.14, alpha=0.4))
                self.c.rect(ML - 2, self.y - 4, total_w + 4, 14, fill=1, stroke=0)
            x = ML
            for i, cell in enumerate(row):
                col = WHITE if i == 0 else (TEAL if i == 1 else AMBER)
                self.c.setFillColor(col)
                self.c.setFont("SC", 6.5)
                # Truncate if too wide
                max_chars = int(col_widths[i] / 4)
                txt = cell[:max_chars] if len(cell) > max_chars else cell
                self.c.drawString(x, self.y, txt)
                x += col_widths[i]
            self.y -= 14

    def bullet(self, text, color=TEAL):
        self._check(14)
        # Node bullet
        self.c.setFillColor(color)
        self.c.circle(ML + 5, self.y + 3, 2.5, fill=1, stroke=0)
        self.c.setFillColor(WHITE)
        self.c.setFont("Verdana-R", 7.5)
        # Wrap long bullets
        lines = textwrap.wrap(text, 80)
        for j, l in enumerate(lines):
            self.c.setFillColor(WHITE if j == 0 else MUTED)
            self.c.drawString(ML + 16, self.y, l)
            self.y -= 12

    def kpi_row(self, kpis):
        """Row of KPI badges. kpis = [(num, label, color), ...]"""
        self._check(50)
        self.space(6)
        n = len(kpis)
        bw = min(60, (W - ML - MR) / n - 6)
        for i, (num, lbl, col) in enumerate(kpis):
            x = ML + i * (bw + 8)
            self.c.setFillColor(CARD)
            self.c.roundRect(x, self.y - 8, bw, 34, 4, fill=1, stroke=0)
            self.c.setFillColor(col)
            self.c.setFont("DINCondBold", 16)
            self.c.drawCentredString(x + bw / 2, self.y + 8, num)
            self.c.setFillColor(MUTED)
            self.c.setFont("SC", 5.5)
            self.c.drawCentredString(x + bw / 2, self.y - 4, lbl)
        self.y -= 42

    def card_block(self, title_text, body_lines, color=TEAL):
        """Highlighted card block."""
        self._check(20 + len(body_lines) * 12)
        h = 18 + len(body_lines) * 12
        self.c.setFillColor(CARD)
        self.c.roundRect(ML, self.y - h + 14, W - ML - MR, h, 4, fill=1, stroke=0)
        self.c.setFillColor(color)
        self.c.rect(ML, self.y - h + 14, 3, h, fill=1, stroke=0)
        self.c.setFont("Verdana-B", 8)
        self.c.drawString(ML + 12, self.y, title_text)
        self.y -= 14
        for bl in body_lines:
            self.c.setFillColor(MUTED)
            self.c.setFont("SC", 6.5)
            self.c.drawString(ML + 12, self.y, bl)
            self.y -= 12
        self.y -= 4

    def save(self):
        self.c.save()
        sz = os.path.getsize(OUT)
        print(f"PDF generado: {OUT}")
        print(f"Paginas: {self.page}")
        print(f"Tamano: {sz / 1024:.0f} KB")


def build():
    d = DocBuilder()

    # ═══════════════════ PORTADA ═══════════════════
    d.space(80)
    d.c.setFillColor(TEAL)
    d.c.setFont("SC", 8)
    d.c.drawString(ML, d.y, "ODISEIA4GOOD HACKATHON  /  SPRINT 3")
    d.y -= 30
    d.c.setFillColor(WHITE)
    d.c.setFont("DINBold", 40)
    d.c.drawString(ML, d.y, "Clara")
    d.y -= 28
    d.c.setFillColor(TEAL)
    d.c.setFont("Futura", 16)
    d.c.drawString(ML, d.y, "CivicAid Voice")
    d.y -= 22
    d.c.setFillColor(MUTED)
    d.c.setFont("Georgia-I", 12)
    d.c.drawString(ML, d.y, "Traducimos la burocracia a tu lengua")
    d.y -= 30
    d.c.setStrokeColor(FAINT)
    d.c.setLineWidth(0.4)
    d.c.line(ML, d.y, W - MR, d.y)
    d.y -= 20

    d.para("Equipo: Robert Promes (PM), Marcos, Daniel, Andrea, Lucas", color=WHITE)
    d.para("UDIT — Taller de Proyectos II — Dr. Gustavo Bermejo Martin")
    d.para("13 de febrero de 2026")
    d.space(20)

    d.kpi_row([("3.2M", "inmigrantes", TEAL), ("9.5M", "mayores 65", TEAL),
               ("4.5M", "exclusion", TEAL), ("78%", "WhatsApp", AMBER)])

    d.space(20)
    # Index table
    d.subsection("Indice con cruce de criterios")
    d.table(
        ["Seccion", "Contenido", "Criterio"],
        [
            ["01 Funcionalidades", "Que hace Clara hoy", "Innovacion (30%)"],
            ["02 Arquitectura", "Stack tecnico", "Viabilidad (20%)"],
            ["03 Procesos", "Flujos paso a paso", "Innovacion (30%)"],
            ["04 Ventajas", "Por que funciona", "Impacto Social (30%)"],
            ["05 Desventajas", "Limitaciones honestas", "Viabilidad (20%)"],
            ["06 Prototipo", "Lo que el jurado vera", "Presentacion (20%)"],
            ["07 Escalabilidad", "Prototipo a producto", "Viabilidad (20%)"],
            ["08 Destacables", "Lo diferente", "Impacto Social (30%)"],
            ["Criterios", "Punto por punto", "Todos (100%)"],
            ["Scrum", "Sprint review", "Presentacion (20%)"],
        ],
        col_widths=[160, 170, 165],
    )

    # ═══════════════════ 01 FUNCIONALIDADES ═══════════════════
    d.section_num("01  FUNCIONALIDADES", "Que hace Clara hoy")
    d.para("Clara es un asistente conversacional WhatsApp-first que guia a personas vulnerables a traves de tramites de servicios sociales en Espana.")
    d.space(6)

    d.subsection("Funcionalidades CORE (desplegadas)")
    d.table(
        ["#", "Funcionalidad", "Detalle", "Estado"],
        [
            ["1", "Chat multilingue", "ES + FR, deteccion automatica", "Operativo"],
            ["2", "Voz STT + TTS", "Gemini Flash + gTTS", "Operativo"],
            ["3", "Cache inteligente", "8 respuestas, <2s", "Operativo"],
            ["4", "Pipeline 11 skills", "Orquestador modular", "Operativo"],
        ],
        col_widths=[30, 130, 210, 125],
    )
    d.space(6)

    d.subsection("Funcionalidades de CALIDAD (Sprint 3)")
    d.bullet("Guardrails de seguridad — pre-check y post-check, 6 red team tests con 100% bloqueo")
    d.bullet("Observabilidad — JSON logs estructurados con request_id y timings por stage")
    d.bullet("Evaluaciones automatizadas — 16 casos en 4 sets con scripts/run_evals.py")
    d.space(6)

    d.subsection("Proxima fase (Sprint 4)")
    d.bullet("Lector de documentos — analisis de imagenes con vision LLM", color=AMBER)
    d.bullet("Canal web — interfaz web en desarrollo, WhatsApp prioridad", color=AMBER)
    d.bullet("Elegibilidad proactiva — requiere persistencia de sesion", color=AMBER)

    # ═══════════════════ 02 ARQUITECTURA ═══════════════════
    d.section_num("02  ARQUITECTURA", "Stack 100% gratuito")

    d.subsection("Patron TwiML ACK (diferencial tecnico)")
    d.para("El patron TwiML ACK separa la respuesta HTTP (rapida) del envio del mensaje (asincrono):")
    d.card_block("TwiML ACK — 4 pasos", [
        "1. Twilio envia POST a /webhook",
        "2. Flask responde HTTP 200 con TwiML vacio en <1 segundo",
        "3. Hilo de fondo procesa: cache, LLM, audio",
        "4. Resultado enviado via Twilio REST API",
        "",
        "Garantiza que Twilio nunca recibe timeout (15s max).",
    ], color=TEAL_GLOW)
    d.space(6)

    d.subsection("Pipeline de 11 skills")
    d.table(
        ["#", "Skill", "Archivo", "Funcion"],
        [
            ["1", "detect_input", "detect_input.py", "Clasifica tipo entrada"],
            ["2", "fetch_media", "fetch_media.py", "Descarga multimedia"],
            ["3", "convert_audio", "convert_audio.py", "Convierte formatos audio"],
            ["4", "transcribe", "transcribe.py", "Transcribe via Gemini"],
            ["5", "detect_lang", "detect_lang.py", "Detecta idioma (ES/FR)"],
            ["6", "cache_match", "cache_match.py", "Busca en cache keywords"],
            ["7", "kb_lookup", "kb_lookup.py", "Busca en 3 KBs"],
            ["8", "llm_generate", "llm_generate.py", "Genera con Gemini Flash"],
            ["9", "verify_response", "verify_response.py", "Verifica vs KB"],
            ["10", "tts", "tts.py", "Texto a audio (gTTS)"],
            ["11", "send_response", "send_response.py", "Envia via Twilio REST"],
        ],
        col_widths=[25, 110, 130, 230],
    )
    d.space(6)

    d.subsection("Software stack")
    d.table(
        ["Componente", "Tecnologia", "Coste"],
        [
            ["Lenguaje", "Python 3.11", "Gratis"],
            ["Framework", "Flask 3.1 + Gunicorn 21", "Gratis"],
            ["LLM + STT", "Gemini 1.5 Flash", "Gratis (free tier)"],
            ["TTS", "gTTS 2.5", "Gratis"],
            ["WhatsApp", "Twilio 9 (sandbox)", "Gratis"],
            ["Hosting", "Render.com (Frankfurt)", "Gratis (free)"],
            ["Container", "Docker (Python 3.11-slim)", "Gratis"],
            ["Deteccion idioma", "langdetect 1.0", "Gratis"],
            ["Validacion", "Pydantic 2.x", "Gratis"],
        ],
        col_widths=[140, 200, 155],
    )
    d.space(6)

    d.subsection("9 Feature Flags")
    d.table(
        ["Flag", "Default", "Efecto"],
        [
            ["DEMO_MODE", "false", "Cache-only, skip LLM tras miss"],
            ["LLM_LIVE", "true", "Habilita Gemini"],
            ["WHISPER_ON", "true", "Habilita transcripcion audio"],
            ["LLM_TIMEOUT", "6s", "Timeout maximo Gemini"],
            ["WHISPER_TIMEOUT", "12s", "Timeout transcripcion"],
            ["GUARDRAILS_ON", "true", "Guardrails de contenido"],
            ["STRUCTURED_OUTPUT_ON", "false", "Salida estructurada JSON"],
            ["OBSERVABILITY_ON", "true", "Metricas y trazas"],
            ["RAG_ENABLED", "false", "RAG (pendiente)"],
        ],
        col_widths=[160, 80, 255],
    )

    # ═══════════════════ 03 PROCESOS ═══════════════════
    d.section_num("03  PROCESOS", "Flujo paso a paso")

    d.subsection("Flujo A: Texto WhatsApp")
    d.card_block("6 pasos — Tiempo: <2s (cache) | 4-8s (LLM)", [
        "1. Usuario escribe mensaje en WhatsApp",
        "2. Twilio envia POST a /webhook con Body, From, To",
        "3. Flask valida firma X-Twilio-Signature (seguridad)",
        "4. Flask responde TwiML vacio (ACK <1 segundo)",
        "5. Hilo de fondo: guardrails -> detecta idioma -> cache -> KB -> LLM -> verify -> gTTS",
        "6. Twilio REST envia respuesta al usuario",
    ])
    d.space(6)

    d.subsection("Flujo B: Audio WhatsApp")
    d.card_block("8 pasos — Tiempo: 6-12s", [
        "1. Usuario graba audio en WhatsApp",
        "2. Twilio POST con MediaUrl0, MediaContentType0, NumMedia=1",
        "3. Flask valida firma X-Twilio-Signature",
        "4. Flask responde TwiML vacio (ACK <1 segundo)",
        "5. Descarga audio + Gemini Flash transcripcion (STT)",
        "6. Detecta idioma del texto transcrito",
        "7. Cache match -> KB lookup -> Gemini -> Verify -> gTTS",
        "8. Twilio REST envia respuesta texto + audio",
    ], color=AMBER)

    # ═══════════════════ 04 VENTAJAS ═══════════════════
    d.section_num("04  VENTAJAS", "Por que Clara funciona")

    ventajas = [
        ("Accesible sin alfabetizacion digital", "WhatsApp (78% de Espana) + mensajes de voz. No requiere instalar nada."),
        ("Multilingue nativo", "Deteccion automatica ES/FR. Extensible cambiando config."),
        ("Coste cero de operacion", "Render free + Gemini free + gTTS free + Twilio sandbox."),
        ("Cache inteligente", "8 respuestas pre-calculadas en <2s con audio pre-generado."),
        ("96 tests automatizados", "85 unit + 7 integration + 4 e2e + evals + red team."),
        ("Guardrails de seguridad", "Pre-check y post-check. 6 red team tests: 100% bloqueo."),
        ("Pipeline resiliente", "TwiML ACK + cache-first + fallback + thread protection."),
    ]
    for t, desc in ventajas:
        d.bullet(f"{t} — {desc}")

    # ═══════════════════ 05 DESVENTAJAS ═══════════════════
    d.section_num("05  DESVENTAJAS", "Limitaciones honestas")

    d.table(
        ["Limitacion", "Impacto", "Mitigacion"],
        [
            ["KB estatica (3 JSONs)", "Solo 3 tramites", "RAG flag preparado, extensible"],
            ["Dependencia Gemini API", "Sin Gemini no hay STT/LLM", "Cache-first + fallback templates"],
            ["Cold start Render", "~30s primer request", "Cron cada 14 min activo"],
            ["Twilio Sandbox", "Requiere join por usuario", "Migracion trivial (1 variable)"],
            ["Sin persistencia sesion", "No recuerda previos", "Redis/DB sin cambiar pipeline"],
            ["Solo 2 idiomas probados", "ES+FR, no EN/AR", "Extensible por config"],
            ["Canal web en desarrollo", "Solo WhatsApp hoy", "Web para Sprint 4"],
        ],
        col_widths=[155, 145, 195],
    )
    d.space(6)
    d.para("Nota: Todas las limitaciones son del prototipo, no de la arquitectura. El diseno modular permite superar cada una sin reescribir codigo.", color=WHITE)

    d.space(6)
    d.subsection("Matriz de riesgos")
    d.table(
        ["Riesgo", "Probabilidad", "Impacto", "Mitigacion"],
        [
            ["Gemini API down", "Baja", "Alto", "Cache-first + fallback"],
            ["Cold start en demo", "Media", "Alto", "Cron 14 min"],
            ["Twilio sandbox expira", "Baja", "Medio", "Re-join 30s"],
            ["Alucinacion LLM", "Media", "Alto", "Guardrails + verify + KB"],
            ["Audio no transcrito", "Baja", "Medio", "Fallback idioma"],
            ["Pico de trafico", "Baja", "Medio", "Escalable con plan pago"],
        ],
        col_widths=[125, 90, 75, 205],
    )

    # ═══════════════════ 06 PROTOTIPO ═══════════════════
    d.section_num("06  PROTOTIPO", "Lo que el jurado vera")

    d.card_block("URL de produccion", [
        "https://civicaid-voice.onrender.com",
        "",
        'GET /health -> {"status":"healthy","cache_entries":8,"tramites_loaded":3,',
        '  "twilio_configured":true,"demo_mode":true,"guardrails_on":true}',
    ], color=TEAL_GLOW)
    d.space(6)

    d.subsection("Tabla de funcionalidades")
    d.table(
        ["Funcionalidad", "Disponible", "Detalle"],
        [
            ["Chat texto ES", "SI", "3 tramites en espanol"],
            ["Chat texto FR", "SI", "3 tramites en frances"],
            ["Audio entrada", "SI", "Gemini Flash STT"],
            ["Audio salida", "SI", "gTTS MP3"],
            ["Cache inteligente", "SI", "8 respuestas + 6 MP3s"],
            ["Guardrails", "SI", "Pre + post check"],
            ["Canal web", "NO", "Sprint 4"],
            ["Lector docs", "NO", "Sprint 4"],
        ],
        col_widths=[160, 80, 255],
    )
    d.space(6)

    d.subsection("3 casos de demo")
    d.bullet("Maria (ES, 45) — IMV: escribe 'Como solicito el ingreso minimo vital?' -> requisitos + cuantias + telefonos")
    d.bullet("Ahmed (FR, 32) — Empadronamiento: audio en frances -> Clara transcribe, detecta FR, responde en frances", color=AMBER)
    d.bullet("Laura (ES, 28) — Tarjeta sanitaria: 'Necesito la tarjeta sanitaria' -> documentos + donde ir + telefonos")

    # ═══════════════════ 07 ESCALABILIDAD ═══════════════════
    d.section_num("07  ESCALABILIDAD", "De prototipo a producto")

    d.table(
        ["Aspecto", "Hoy (0 EUR)", "Produccion (~200 EUR)"],
        [
            ["Servidor", "Render free (512MB)", "GCP Cloud Run"],
            ["LLM", "Gemini Flash free", "Gemini Pro fine-tuned"],
            ["Transcripcion", "Gemini Flash", "Whisper large / Gemini Pro"],
            ["TTS", "gTTS", "Google Cloud TTS"],
            ["KB", "3 JSONs", "RAG + vector DB"],
            ["Idiomas", "2 (ES, FR)", "6+"],
            ["Canal", "WhatsApp sandbox", "WA Business + Web + Telegram"],
            ["Persistencia", "Sin estado", "Redis / PostgreSQL"],
            ["Tests", "96", "200+ con CI/CD"],
        ],
        col_widths=[120, 185, 190],
    )
    d.space(6)

    d.subsection("Coste proyectado")
    d.table(
        ["Escala", "Usuarios/mes", "Coste"],
        [
            ["Prototipo", "<100", "0 EUR"],
            ["Piloto ONG", "1,000", "~50 EUR"],
            ["Municipio", "10,000", "~200 EUR"],
            ["CCAA", "100,000", "~1,500 EUR"],
        ],
        col_widths=[165, 165, 165],
    )

    # ═══════════════════ 08 DESTACABLES ═══════════════════
    d.section_num("08  PUNTOS DESTACABLES", "Lo que nos hace diferentes")

    d.subsection("Sprint 3 en numeros")
    d.kpi_row([("0", "EUR/mes", TEAL), ("16", "commits", BLUE), ("96", "tests", TEAL_GLOW),
               ("11", "skills", AMBER), ("9", "flags", AMBER), ("36h", "dev", AMBER),
               ("3", "KBs", TEAL), ("8", "cache", TEAL)])
    d.space(6)

    d.subsection("3 personas reales")
    d.bold_para("Maria (ES) — 45 anos, vulnerabilidad. No sabe navegar webs. Escribe a Clara por WhatsApp y recibe pasos exactos para IMV.")
    d.bold_para("Ahmed (FR) — 32 anos, inmigrante francofono. Envia audio en frances, Clara responde en su idioma.")
    d.bold_para("Laura (ES) — 28 anos, mudada. En 2 segundos tiene info completa de tarjeta sanitaria.")
    d.space(4)

    d.subsection("Datos INE")
    d.bullet("3.2 millones de inmigrantes en Espana")
    d.bullet("9.5 millones de mayores de 65 anos")
    d.bullet("4.5 millones en riesgo de exclusion social")
    d.bullet("78% de la poblacion usa WhatsApp a diario", color=AMBER)

    # ═══════════════════ CRITERIOS JURADO ═══════════════════
    d.section_num("CRITERIOS", "Cruce con el jurado")

    d.table(
        ["Criterio (peso)", "Evidencia clave"],
        [
            ["Innovacion (30%)", "Pipeline 11 skills + TwiML ACK + guardrails + evals"],
            ["Impacto Social (30%)", "WhatsApp audio no-lectores + multilingue ES/FR"],
            ["Viabilidad (20%)", "Desplegado, 96 tests, 0 EUR, Docker, /health"],
            ["Presentacion (20%)", "Demo vivo WhatsApp + WOW texto + WOW audio FR"],
        ],
        col_widths=[150, 345],
    )

    # ═══════════════════ SCRUM ═══════════════════
    d.section_num("SCRUM", "Sprint Review")

    d.subsection("Checkpoints")
    d.table(
        ["Sprint", "Fecha", "Objetivo", "Estado"],
        [
            ["S1", "30 Ene", "Planificacion", "COMPLETADO"],
            ["S2", "6 Feb", "Doc tecnico + repo", "COMPLETADO"],
            ["S3", "13 Feb", "MVP + doc v2", "EN CURSO (hoy)"],
            ["S4", "20 Feb", "Demo final", "PROXIMO"],
        ],
        col_widths=[60, 80, 200, 155],
    )
    d.space(6)

    d.subsection("Cambios vs Sprint 2")
    d.table(
        ["Sprint 2 decia", "Sprint 3 corrige", "Razon"],
        [
            ["Web + WhatsApp", "Solo WhatsApp", "Web en Sprint 4"],
            ["Whisper small", "Gemini Flash STT", "RAM Render free tier"],
            ["HuggingFace Spaces", "Render.com Docker", "Decision de deploy"],
            ["4 idiomas", "2 probados (ES, FR)", "Solo 2 con tests/evals"],
            ["Mockup", "URL real desplegada", "Producto EXISTE"],
            ["0 tests", "96 tests", "Desarrollo Sprint 3"],
        ],
        col_widths=[140, 145, 210],
    )
    d.space(6)

    d.subsection("Herramientas del equipo")
    d.table(
        ["Herramienta", "Quien", "Para que"],
        [
            ["Claude Code", "Robert, Marcos", "Dev, arquitectura, testing"],
            ["Gemini 1.5 Flash", "Producto", "LLM + transcripcion audio"],
            ["Perplexity", "Lucas", "Investigacion tramites"],
            ["Figma", "Andrea", "Wireframes, slides"],
            ["GitHub", "Equipo", "Repo + Issues (16 commits)"],
            ["Docker", "Robert, Marcos", "Containerizacion"],
            ["Render", "Robert, Marcos", "Deploy produccion"],
            ["Notion", "Andrea, equipo", "Dashboard (81 entradas, 3 DBs)"],
        ],
        col_widths=[120, 120, 255],
    )
    d.space(6)

    d.subsection("Organizacion del equipo")
    d.table(
        ["Persona", "Rol", "Sprint 3"],
        [
            ["Robert", "PM + Backend", "Pipeline, deploy, demo presenter"],
            ["Marcos", "Routes + Twilio", "Audio pipeline, webhook, Render"],
            ["Lucas", "KB + Testing", "Investigacion, datos demo"],
            ["Daniel", "Web + Video", "Canal web (Sprint 4), video backup"],
            ["Andrea", "Notion + Slides", "Dashboard, presentacion, docs"],
        ],
        col_widths=[90, 120, 285],
    )

    d.space(20)
    d.c.setStrokeColor(FAINT)
    d.c.setLineWidth(0.4)
    d.c.line(ML, d.y, W - MR, d.y)
    d.y -= 14
    d.para("Documento generado el 13 de febrero de 2026 — Sprint 3, CivicAid Voice / Clara", color=FAINT, size=7)
    d.para("UDIT — Taller de Proyectos II — Dr. Gustavo Bermejo Martin", color=FAINT, size=7)

    d.save()


if __name__ == "__main__":
    build()
