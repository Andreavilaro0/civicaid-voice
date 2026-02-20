# FASE 1: Clara Web App Frontend — Plan de Implementacion Completo

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Construir la web app responsive de Clara (frontend Next.js + endpoint API en Flask) para que usuarios vulnerables (mayores 65+, inmigrantes, baja alfabetizacion digital) puedan interactuar con Clara desde cualquier navegador, complementando el canal WhatsApp existente.

**Architecture:** Next.js 14 (App Router) como frontend standalone en `clara-web/`, conectado al backend Flask existente via nuevo endpoint `POST /api/chat`. El backend ya tiene todo el pipeline (guardrails, cache, KB, Gemini, TTS, verify). El frontend solo consume la API. Deploy: frontend en Vercel (gratis), backend sigue en Render.

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, React Aria Components, next-intl (ES/FR), Web Audio API (grabacion voz), Flask + flask-cors (nuevo endpoint API)

**Usuarios objetivo:**
- **Maria**, 74 anos, espanola, baja alfabetizacion digital, usa WhatsApp basico
- **Ahmed**, 28 anos, senegales en Espana, habla frances, no entiende burocracia espanola
- **Fatima**, 45 anos, marroqui, idioma arabe/frances, necesita orientacion sobre ayudas

**Parametros de accesibilidad (WCAG AAA):**
- Texto cuerpo: 18-20px Inter, line-height 1.6
- Titulares: 28-36px Atkinson Hyperlegible Bold
- Botones principales: 64x64px minimo
- Contraste: 7:1 texto normal, 4.5:1 texto grande
- Focus indicators: outline 3px `#1B5E7B`
- Touch targets: 64px acciones principales, 48px secundarias
- Respetar `prefers-reduced-motion`
- Todo navegable con teclado (Tab), sin trampas

**Paleta Clara:**
| Rol | Hex | Tailwind |
|---|---|---|
| Primario (Azul Confianza) | `#1B5E7B` | `clara-blue` |
| Secundario (Naranja Calido) | `#D46A1E` | `clara-orange` |
| Acento (Verde Esperanza) | `#2E7D4F` | `clara-green` |
| Fondo | `#FAFAFA` | `clara-bg` |
| Texto Principal | `#1A1A2E` | `clara-text` |
| Texto Secundario | `#4A4A5A` | `clara-text-secondary` |
| Error | `#C62828` | `clara-error` |
| Warning | `#F9A825` | `clara-warning` |
| Info/Burbuja Clara | `#E3F2FD` | `clara-info` |
| Card BG | `#F5F5F5` | `clara-card` |
| Borde | `#E0E0E0` | `clara-border` |

---

## Inventario de Capacidades Claude

### Skills Relevantes

| Categoria | Skills Disponibles | Uso en este Plan |
|---|---|---|
| **Frontend Core** | `nextjs-developer`, `frontend-developer`, `react-expert`, `react-best-practices` | Construir web app |
| **Diseno UI** | `frontend-design`, `top-design`, `refactoring-ui`, `design-trends-2026`, `ux-heuristics` | Sistema de diseno |
| **TypeScript** | `typescript-pro` | Tipado estricto |
| **Testing** | `test-driven-development`, `webapp-testing`, `lighthouse-audit`, `playwright-expert` | TDD + testing accesibilidad |
| **Backend** | `fastapi-expert`, `python-pro` | Endpoint API Flask |
| **Deploy** | `render-deploy`, `docker-expert`, `vercel-automation` | Deploy frontend + backend |
| **Marca** | `brand-strategy`, `brand-voice`, `brand-guidelines` | Identidad Clara |
| **PWA** | `frontend-developer` | manifest, service worker |

### MCPs Conectados

| MCP | Uso en este Plan |
|---|---|
| **Notion** (claude.ai) | Tracking de progreso, documentar entregables |
| **Canva** (claude.ai) | Generar logo, brand kit, assets visuales |
| **Grafana** | Monitoreo post-deploy (fase final) |

### Estrategia Multi-Agente

El plan esta disenado para ejecutarse con **subagent-driven-development**:
- **Agente principal:** Coordina, revisa codigo, gestiona commits
- **Subagente backend** (Q1): `python-pro` — crea endpoint API + tests
- **Subagente frontend scaffolding** (Q2): `nextjs-developer` — scaffold + config
- **Subagente componentes** (Q3-Q4): `frontend-developer` + `react-expert` — UI components
- **Subagente chat** (Q5-Q6): `frontend-developer` — API client + chat interface
- **Subagente voz** (Q7): `frontend-developer` — Web Audio API
- **Subagente media** (Q8-Q9): `frontend-developer` — audio player + document upload
- **Subagente i18n+PWA** (Q10-Q11): `nextjs-developer` — internationalization + PWA
- **Subagente deploy** (Q12): `devops-engineer` — Vercel + CORS + env vars

**Paralelizacion:** Q1 y Q2 corren en paralelo. Q7, Q8 y Q9 corren en paralelo. Q10 y Q11 corren en paralelo.

---

## INDICE DE Qs

| Q | Nombre | Descripcion | Dependencias | Agente |
|---|--------|-------------|--------------|--------|
| Q1 | Backend API Endpoint | `POST /api/chat` y `GET /api/health` en Flask | Ninguna | backend |
| Q2 | Scaffolding Next.js | Proyecto, Tailwind paleta Clara, fonts | Ninguna | frontend |
| Q3 | Componentes Base | Button, ChatBubble, LanguageSelector, LoadingState | Q2 | frontend |
| Q4 | Pantalla de Bienvenida | Landing con logo, selector idioma, CTAs | Q3 | frontend |
| Q5 | Cliente API y Types | `lib/api.ts`, `lib/types.ts`, conexion front-back | Q1, Q2 | frontend |
| Q6 | Interfaz de Chat | MessageList, ChatInput, Header, conversacion | Q3, Q5 | frontend |
| Q7 | Grabacion de Voz | VoiceRecorder, Web Audio API, toggle mic | Q6 | frontend |
| Q8 | Audio Player | Reproductor play/pause, barra progreso, velocidad | Q6 | frontend |
| Q9 | Subida de Documento | DocumentUpload con camara y galeria | Q6 | frontend |
| Q10 | i18n (ES/FR) | next-intl, archivos mensajes, middleware | Q4, Q6 | frontend |
| Q11 | PWA y Responsive | manifest.json, service worker, test viewports | Q6 | frontend |
| Q12 | Deploy | Frontend Vercel, CORS config, env vars | Q1-Q11 | devops |

---

## Q1: Backend API Endpoint

> **Objetivo:** Crear endpoint REST que el frontend pueda consumir, reutilizando el pipeline existente de Clara sin duplicar logica.

**Files:**
- Create: `src/routes/api_chat.py`
- Modify: `src/app.py:31-45` (registrar blueprint + CORS)
- Modify: `requirements.txt` (agregar flask-cors)
- Create: `tests/unit/test_api_chat.py`

### Step 1: Agregar flask-cors a requirements.txt

Agregar al final de `requirements.txt`:
```
flask-cors==5.0.*
```

Run: `pip install flask-cors`

### Step 2: Escribir test para el endpoint

```python
# tests/unit/test_api_chat.py
"""Tests for POST /api/chat and GET /api/health API endpoints."""
import pytest
from unittest.mock import patch, MagicMock
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_api_health_returns_ok(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "features" in data


def test_api_chat_requires_text_or_audio(client):
    resp = client.post("/api/chat", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_api_chat_text_returns_response(client):
    with patch("src.routes.api_chat.cache") as mock_cache, \
         patch("src.routes.api_chat.detect_language", return_value="es"):
        mock_cache.match.return_value = MagicMock(
            hit=True,
            entry=MagicMock(respuesta="El IMV es una ayuda mensual.", audio_file=None)
        )
        resp = client.post("/api/chat", json={"text": "Que es el IMV?"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "response" in data
        assert data["source"] == "cache"


def test_api_chat_cors_headers(client):
    resp = client.options("/api/chat")
    assert resp.status_code in (200, 204)
```

Run: `pytest tests/unit/test_api_chat.py -v`
Expected: FAIL (module not found)

### Step 3: Crear `src/routes/api_chat.py`

```python
"""POST /api/chat — REST API for web frontend. Reuses existing pipeline synchronously."""

import time
import base64
import logging
from flask import Blueprint, request, jsonify
from src.core.config import config
from src.core.models import InputType
from src.core import cache
from src.core.skills.detect_lang import detect_language
from src.core.skills.kb_lookup import kb_lookup
from src.core.skills.llm_generate import llm_generate
from src.core.skills.verify_response import verify_response
from src.core.prompts.templates import get_template

logger = logging.getLogger("clara")
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    language = data.get("language", "es")
    input_type_str = data.get("input_type", "text")
    audio_b64 = data.get("audio_base64")

    if not text and not audio_b64:
        return jsonify({"error": "text or audio_base64 required"}), 400

    start = time.time()

    # --- Audio transcription ---
    if input_type_str == "audio" and audio_b64:
        try:
            from src.core.skills.transcribe import transcribe
            audio_bytes = base64.b64decode(audio_b64)
            transcript = transcribe(audio_bytes, "audio/webm")
            if transcript.success and transcript.text:
                text = transcript.text
                language = transcript.language
            else:
                return jsonify({"error": "audio_transcription_failed"}), 422
        except Exception as e:
            logger.error("API audio error: %s", e)
            return jsonify({"error": "audio_processing_error"}), 500

    # --- Guardrails pre-check ---
    if config.GUARDRAILS_ON:
        from src.core.guardrails import pre_check
        guard = pre_check(text)
        if not guard.safe:
            elapsed = int((time.time() - start) * 1000)
            return jsonify({
                "response": guard.modified_text or "No puedo ayudar con ese tema.",
                "source": "guardrail", "language": language,
                "duration_ms": elapsed, "audio_url": None, "sources": []
            })

    # --- Detect language ---
    if input_type_str == "text":
        language = detect_language(text)

    # --- Cache match ---
    cache_result = cache.match(text, language, InputType.TEXT)
    if cache_result.hit and cache_result.entry:
        elapsed = int((time.time() - start) * 1000)
        audio_url = None
        if cache_result.entry.audio_file and config.AUDIO_BASE_URL:
            audio_url = f"{config.AUDIO_BASE_URL.rstrip('/')}/{cache_result.entry.audio_file}"
        return jsonify({
            "response": cache_result.entry.respuesta,
            "source": "cache", "language": language,
            "duration_ms": elapsed, "audio_url": audio_url, "sources": []
        })

    # --- Demo mode ---
    if config.DEMO_MODE:
        elapsed = int((time.time() - start) * 1000)
        return jsonify({
            "response": get_template("fallback_generic", language),
            "source": "fallback", "language": language,
            "duration_ms": elapsed, "audio_url": None, "sources": []
        })

    # --- KB + LLM ---
    kb_context = kb_lookup(text, language)
    llm_resp = llm_generate(text, language, kb_context)
    verified = verify_response(llm_resp.text, kb_context)

    if config.STRUCTURED_OUTPUT_ON:
        from src.core.models_structured import parse_structured_response
        parsed, display = parse_structured_response(verified)
        if parsed:
            verified = display

    if config.GUARDRAILS_ON:
        from src.core.guardrails import post_check
        verified = post_check(verified)

    # --- TTS ---
    audio_url = None
    try:
        from src.core.skills.tts import text_to_audio
        audio_url = text_to_audio(verified, language)
    except Exception:
        pass

    # --- Build sources ---
    sources = []
    if kb_context and kb_context.fuente_url:
        sources.append({"name": kb_context.tramite, "url": kb_context.fuente_url})

    elapsed = int((time.time() - start) * 1000)
    return jsonify({
        "response": verified,
        "source": "llm" if llm_resp.success else "fallback",
        "language": language, "duration_ms": elapsed,
        "audio_url": audio_url, "sources": sources,
    })


@api_bp.route("/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "ok",
        "features": {
            "whisper": config.WHISPER_ON,
            "llm": config.LLM_LIVE,
            "guardrails": config.GUARDRAILS_ON,
            "demo_mode": config.DEMO_MODE,
        }
    })
```

### Step 4: Registrar blueprint y CORS en `src/app.py`

Agregar despues de la linea `app.register_blueprint(admin_bp)`:

```python
from src.routes.api_chat import api_bp
app.register_blueprint(api_bp)

# CORS for web frontend
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Step 5: Correr tests

Run: `pytest tests/unit/test_api_chat.py -v`
Expected: PASS (4 tests)

### Step 6: Test manual

Run: `curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"text": "Que es el IMV?"}'`
Expected: JSON con `response`, `source`, `language`

### Step 7: Commit

```bash
git add src/routes/api_chat.py src/app.py requirements.txt tests/unit/test_api_chat.py
git commit -m "feat: add REST API endpoint POST /api/chat for web frontend"
```

---

## Q2: Scaffolding Next.js

> **Objetivo:** Crear el proyecto frontend con la configuracion de Clara (colores, fuentes, estructura).

**Files:**
- Create: `clara-web/` (proyecto completo via create-next-app)
- Modify: `clara-web/tailwind.config.ts` (paleta Clara)
- Modify: `clara-web/src/app/layout.tsx` (fonts Atkinson + Inter)
- Modify: `clara-web/src/app/globals.css` (tokens CSS)

### Step 1: Crear proyecto Next.js

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice
npx create-next-app@latest clara-web --typescript --tailwind --app --src-dir --no-eslint --no-import-alias
```

Cuando pregunte: Use App Router? **Yes**. Customize import alias? **No**.

### Step 2: Instalar dependencias

```bash
cd clara-web
npm install react-aria-components next-intl
```

### Step 3: Configurar Tailwind con paleta Clara

Reemplazar `clara-web/tailwind.config.ts`:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        clara: {
          blue: "#1B5E7B",
          orange: "#D46A1E",
          green: "#2E7D4F",
          bg: "#FAFAFA",
          text: "#1A1A2E",
          "text-secondary": "#4A4A5A",
          error: "#C62828",
          warning: "#F9A825",
          info: "#E3F2FD",
          card: "#F5F5F5",
          border: "#E0E0E0",
        },
      },
      fontFamily: {
        display: ['"Atkinson Hyperlegible"', "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
      },
      fontSize: {
        body: ["20px", { lineHeight: "1.6" }],
        "body-sm": ["18px", { lineHeight: "1.6" }],
        h1: ["36px", { lineHeight: "1.3" }],
        h2: ["28px", { lineHeight: "1.3" }],
        button: ["20px", { lineHeight: "1.0" }],
        label: ["16px", { lineHeight: "1.4" }],
      },
      spacing: {
        touch: "64px",
        "touch-sm": "48px",
        "touch-lg": "96px",
      },
      borderRadius: {
        bubble: "16px",
      },
    },
  },
  plugins: [],
};

export default config;
```

### Step 4: Configurar fonts en layout.tsx

Reemplazar `clara-web/src/app/layout.tsx`:

```typescript
import type { Metadata, Viewport } from "next";
import { Inter, Atkinson_Hyperlegible } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin", "latin-ext"],
  variable: "--font-inter",
  display: "swap",
});

const atkinson = Atkinson_Hyperlegible({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-atkinson",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Clara — Tu voz tiene poder",
  description:
    "Asistente de voz que te ayuda con tramites sociales en Espana. Habla o escribe en tu idioma.",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  themeColor: "#1B5E7B",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className={`${inter.variable} ${atkinson.variable}`}>
      <body className="bg-clara-bg text-clara-text font-body antialiased min-h-screen">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:bg-clara-blue focus:text-white focus:px-4 focus:py-2 focus:rounded"
        >
          Ir al contenido principal
        </a>
        <main id="main-content" role="main">
          {children}
        </main>
      </body>
    </html>
  );
}
```

### Step 5: Configurar globals.css

Reemplazar `clara-web/src/app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-clara-blue: #1B5E7B;
    --color-clara-orange: #D46A1E;
    --color-clara-green: #2E7D4F;
    --focus-ring: 3px solid var(--color-clara-blue);
  }

  *:focus-visible {
    outline: var(--focus-ring);
    outline-offset: 2px;
    border-radius: 4px;
  }

  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }

  p, li, dd {
    max-width: 70ch;
  }

  @media (prefers-reduced-motion: no-preference) {
    html {
      scroll-behavior: smooth;
    }
  }
}
```

### Step 6: Verificar que compila

```bash
cd clara-web && npm run dev
```
Expected: App corriendo en `http://localhost:3000` sin errores

### Step 7: Commit

```bash
git add clara-web/
git commit -m "feat: scaffold Next.js frontend with Clara design tokens and accessible defaults"
```

---

## Q3: Componentes Base

> **Objetivo:** Crear los 4 componentes UI reutilizables con accesibilidad AAA integrada.

**Files:**
- Create: `clara-web/src/components/ui/Button.tsx`
- Create: `clara-web/src/components/ui/ChatBubble.tsx`
- Create: `clara-web/src/components/ui/LanguageSelector.tsx`
- Create: `clara-web/src/components/ui/LoadingState.tsx`

### Step 1: Button.tsx — Boton accesible 64px

```typescript
"use client";

import { Button as AriaButton } from "react-aria-components";
import type { ButtonProps as AriaButtonProps } from "react-aria-components";

type Variant = "primary" | "secondary" | "ghost";

interface ButtonProps extends AriaButtonProps {
  variant?: Variant;
  icon?: React.ReactNode;
  fullWidth?: boolean;
}

const variantStyles: Record<Variant, string> = {
  primary:
    "bg-clara-blue text-white hover:bg-[#164d66] pressed:bg-[#123f54]",
  secondary:
    "bg-white text-clara-text border-2 border-clara-border hover:border-clara-blue pressed:bg-clara-card",
  ghost:
    "bg-transparent text-clara-blue hover:bg-clara-info pressed:bg-clara-card",
};

export default function Button({
  variant = "primary",
  icon,
  fullWidth = false,
  children,
  className = "",
  ...props
}: ButtonProps) {
  return (
    <AriaButton
      className={`
        inline-flex items-center justify-center gap-3
        min-h-touch min-w-touch px-6
        rounded-xl font-body text-button font-medium
        transition-colors duration-150
        focus-visible:outline focus-visible:outline-[3px]
        focus-visible:outline-clara-blue focus-visible:outline-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantStyles[variant]}
        ${fullWidth ? "w-full" : ""}
        ${className}
      `}
      {...props}
    >
      {icon && <span aria-hidden="true">{icon}</span>}
      {children}
    </AriaButton>
  );
}
```

### Step 2: ChatBubble.tsx

```typescript
interface ChatBubbleProps {
  sender: "clara" | "user";
  children: React.ReactNode;
  timestamp?: string;
}

export default function ChatBubble({ sender, children, timestamp }: ChatBubbleProps) {
  const isClara = sender === "clara";

  return (
    <div className={`flex ${isClara ? "justify-start" : "justify-end"} mb-4`}>
      <div
        className={`
          max-w-[85%] px-4 py-3 rounded-bubble text-body-sm
          ${isClara
            ? "bg-clara-info text-clara-text rounded-bl-sm"
            : "bg-clara-blue text-white rounded-br-sm"
          }
        `}
      >
        {isClara && (
          <p className="font-display font-bold text-label text-clara-blue mb-1">
            Clara
          </p>
        )}
        <div className="space-y-2">{children}</div>
        {timestamp && (
          <p className="text-[14px] text-clara-text-secondary mt-2 text-right">
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
}
```

### Step 3: LanguageSelector.tsx

```typescript
"use client";

import { useState } from "react";

interface LanguageSelectorProps {
  defaultLang?: "es" | "fr";
  onChange?: (lang: "es" | "fr") => void;
}

const languages = [
  { code: "es" as const, label: "Espanol", short: "ES" },
  { code: "fr" as const, label: "Francais", short: "FR" },
];

export default function LanguageSelector({
  defaultLang = "es",
  onChange,
}: LanguageSelectorProps) {
  const [selected, setSelected] = useState(defaultLang);

  function handleSelect(code: "es" | "fr") {
    setSelected(code);
    onChange?.(code);
  }

  return (
    <div role="radiogroup" aria-label="Seleccionar idioma" className="flex gap-3">
      {languages.map((lang) => (
        <button
          key={lang.code}
          role="radio"
          aria-checked={selected === lang.code}
          onClick={() => handleSelect(lang.code)}
          className={`
            flex items-center gap-2 px-4 py-3
            min-h-touch-sm rounded-xl font-body text-body-sm font-medium
            border-2 transition-colors duration-150
            ${selected === lang.code
              ? "border-clara-blue bg-clara-info text-clara-blue"
              : "border-clara-border bg-white text-clara-text-secondary"
            }
          `}
        >
          <span aria-hidden="true">{lang.short}</span>
          <span>{lang.label}</span>
        </button>
      ))}
    </div>
  );
}
```

### Step 4: LoadingState.tsx

```typescript
interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({
  message = "Clara esta buscando informacion...",
}: LoadingStateProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="flex items-center gap-3 px-4 py-3 bg-clara-info rounded-bubble max-w-[85%]"
    >
      <div className="flex gap-1" aria-hidden="true">
        <span className="w-2 h-2 bg-clara-blue rounded-full animate-bounce [animation-delay:0ms]" />
        <span className="w-2 h-2 bg-clara-blue rounded-full animate-bounce [animation-delay:150ms]" />
        <span className="w-2 h-2 bg-clara-blue rounded-full animate-bounce [animation-delay:300ms]" />
      </div>
      <p className="text-body-sm text-clara-text-secondary">{message}</p>
    </div>
  );
}
```

### Step 5: Verificar build

Run: `cd clara-web && npm run build`
Expected: Build exitoso

### Step 6: Commit

```bash
git add clara-web/src/components/ui/
git commit -m "feat: add accessible UI components — Button, ChatBubble, LanguageSelector, LoadingState"
```

---

## Q4: Pantalla de Bienvenida

> **Objetivo:** Landing page que muestra logo, tagline, selector de idioma y dos CTAs principales: "Empezar a hablar" y "Prefiero escribir". Mobile-first, accesible WCAG AAA.

**Files:**
- Modify: `clara-web/src/app/page.tsx`
- Create: `clara-web/public/icons/mic.svg`
- Create: `clara-web/public/icons/keyboard.svg`

**Wireframe de referencia** (de `design/02-FRONTEND-ACCESIBLE.md`):
```
+----------------------------------+
|         [Logo Clara]             |
|     "Tu voz tiene poder"        |
|   Te ayudo con tramites          |
|   sociales en Espana.            |
|  [ES Espanol]  [FR Francais]    |
|  [  EMPEZAR A HABLAR  [mic]  ]  |
|  [  Prefiero escribir  [kb]  ]  |
+----------------------------------+
```

### Step 1: Crear iconos SVG

Crear `clara-web/public/icons/mic.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
```

Crear `clara-web/public/icons/keyboard.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M20 5H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/></svg>
```

### Step 2: Implementar pagina de bienvenida

Reemplazar `clara-web/src/app/page.tsx`:

```typescript
"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Button from "@/components/ui/Button";
import LanguageSelector from "@/components/ui/LanguageSelector";
import Image from "next/image";

export default function WelcomePage() {
  const router = useRouter();
  const [lang, setLang] = useState<"es" | "fr">("es");

  const content = {
    es: {
      tagline: "Tu voz tiene poder",
      description: "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
      cta_voice: "Empezar a hablar",
      cta_text: "Prefiero escribir",
    },
    fr: {
      tagline: "Ta voix a du pouvoir",
      description: "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
      cta_voice: "Commencer a parler",
      cta_text: "Je prefere ecrire",
    },
  };

  const t = content[lang];

  function goToChat(mode: "voice" | "text") {
    router.push(`/chat?lang=${lang}&mode=${mode}`);
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
      {/* Logo placeholder — 120px */}
      <div
        className="w-[120px] h-[120px] bg-clara-blue rounded-full flex items-center justify-center mb-6"
        aria-label="Logo de Clara"
      >
        <span className="text-white font-display font-bold text-h1">C</span>
      </div>

      {/* Tagline */}
      <h1 className="font-display font-bold text-h1 text-clara-blue text-center mb-4">
        {t.tagline}
      </h1>

      {/* Descripcion */}
      <p className="text-body text-clara-text-secondary text-center max-w-md mb-8">
        {t.description}
      </p>

      {/* Selector de idioma */}
      <div className="mb-10">
        <LanguageSelector defaultLang={lang} onChange={setLang} />
      </div>

      {/* CTAs */}
      <div className="w-full max-w-md space-y-4">
        <Button
          variant="primary"
          fullWidth
          onPress={() => goToChat("voice")}
          aria-label={t.cta_voice}
          icon={
            <Image src="/icons/mic.svg" alt="" width={28} height={28} aria-hidden="true" />
          }
          className="h-[72px] text-[22px]"
        >
          {t.cta_voice}
        </Button>

        <Button
          variant="secondary"
          fullWidth
          onPress={() => goToChat("text")}
          aria-label={t.cta_text}
          icon={
            <Image src="/icons/keyboard.svg" alt="" width={28} height={28} aria-hidden="true" />
          }
          className="h-[56px]"
        >
          {t.cta_text}
        </Button>
      </div>
    </div>
  );
}
```

### Step 3: Verificar visualmente

Run: `cd clara-web && npm run dev`
Abrir `http://localhost:3000`, verificar:
- Logo centrado
- Tagline en Atkinson Hyperlegible Bold 36px
- Selector idioma funcional (cambiar a FR cambia textos)
- Boton "Empezar a hablar" azul 72px con icono mic
- Boton "Prefiero escribir" outline 56px
- Responsive: probar en 320px, 768px, 1440px

### Step 4: Commit

```bash
git add clara-web/src/app/page.tsx clara-web/public/icons/
git commit -m "feat: add Welcome page with language selector and accessible CTAs"
```

---

## Q5: Cliente API y Types

> **Objetivo:** Crear el cliente HTTP y los tipos TypeScript para conectar frontend con backend.

**Files:**
- Create: `clara-web/src/lib/types.ts`
- Create: `clara-web/src/lib/api.ts`
- Create: `clara-web/src/lib/constants.ts`

### Step 1: Types (contratos TypeScript)

Crear `clara-web/src/lib/types.ts`:

```typescript
export type Language = "es" | "fr";
export type InputMode = "text" | "voice" | "image";
export type MessageSender = "clara" | "user";

export interface ChatRequest {
  text: string;
  language: Language;
  input_type: "text" | "audio" | "image";
  audio_base64?: string | null;
  image_base64?: string | null;
  session_id: string;
}

export interface ChatResponse {
  response: string;
  audio_url: string | null;
  source: "cache" | "llm" | "fallback" | "guardrail";
  language: Language;
  duration_ms: number;
  sources: Array<{ name: string; url: string }>;
}

export interface HealthResponse {
  status: "ok";
  features: {
    whisper: boolean;
    llm: boolean;
    guardrails: boolean;
    demo_mode: boolean;
  };
}

export interface Message {
  id: string;
  sender: MessageSender;
  text: string;
  audio_url?: string | null;
  sources?: Array<{ name: string; url: string }>;
  timestamp: Date;
  loading?: boolean;
}
```

### Step 2: Constants

Crear `clara-web/src/lib/constants.ts`:

```typescript
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export const COLORS = {
  blue: "#1B5E7B",
  orange: "#D46A1E",
  green: "#2E7D4F",
  error: "#C62828",
} as const;

export const MAX_RECORDING_SECONDS = 60;
export const RECORDING_WARNING_SECONDS = 50;
```

### Step 3: API Client

Crear `clara-web/src/lib/api.ts`:

```typescript
import { API_BASE_URL } from "./constants";
import type { ChatRequest, ChatResponse, HealthResponse } from "./types";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export async function sendMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "unknown" }));
    throw new ApiError(res.status, error.error || "request_failed");
  }

  return res.json();
}

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/api/health`);
  if (!res.ok) throw new ApiError(res.status, "health_check_failed");
  return res.json();
}
```

### Step 4: Crear archivo .env.local

Crear `clara-web/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Step 5: Verificar build

Run: `cd clara-web && npm run build`
Expected: Build exitoso

### Step 6: Commit

```bash
git add clara-web/src/lib/ clara-web/.env.local
git commit -m "feat: add API client, TypeScript types, and constants for Clara backend"
```

---

## Q6: Interfaz de Chat

> **Objetivo:** Construir la pantalla principal de chat con MessageList, ChatInput, Header y logica de conversacion. Esta es la pantalla CORE del producto.

**Files:**
- Create: `clara-web/src/app/chat/page.tsx`
- Create: `clara-web/src/components/Header.tsx`
- Create: `clara-web/src/components/MessageList.tsx`
- Create: `clara-web/src/components/ChatInput.tsx`
- Create: `clara-web/src/hooks/useChat.ts`

**Wireframe** (de `design/02-FRONTEND-ACCESIBLE.md`):
```
+----------------------------------+
|  [<-]  Clara          [ES v] [*] |
+----------------------------------+
|  [Clara] Hola, soy Clara...     |
|         [User] Que es el IMV?   |
|  [Clara] El IMV es una ayuda... |
|         [> Escuchar respuesta]  |
|         Fuente: seg-social.es   |
+----------------------------------+
|  Escribe tu pregunta...         |
|  [Escribir] [Voz] [Foto]       |
+----------------------------------+
```

### Step 1: useChat hook

Crear `clara-web/src/hooks/useChat.ts`:

```typescript
"use client";

import { useState, useCallback, useRef } from "react";
import { sendMessage } from "@/lib/api";
import type { Message, Language, ChatResponse } from "@/lib/types";

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

export function useChat(initialLang: Language = "es") {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState<Language>(initialLang);
  const sessionId = useRef(`web_${generateId()}`);

  const addWelcome = useCallback(() => {
    const welcome: Record<Language, string> = {
      es: "Hola, soy Clara. Estoy aqui para ayudarte con tramites en Espana. Puedes hablarme o escribirme en tu idioma.\n\nPuedo informarte sobre:\n- Ingreso Minimo Vital\n- Empadronamiento\n- Tarjeta sanitaria\n- Y mas tramites",
      fr: "Bonjour, je suis Clara. Je suis la pour t'aider avec les demarches en Espagne. Tu peux me parler ou m'ecrire dans ta langue.\n\nJe peux t'informer sur :\n- Revenu Minimum Vital\n- Inscription municipale\n- Carte sanitaire\n- Et d'autres demarches",
    };
    setMessages([
      {
        id: generateId(),
        sender: "clara",
        text: welcome[language],
        timestamp: new Date(),
      },
    ]);
  }, [language]);

  const send = useCallback(
    async (text: string, audioBase64?: string) => {
      const userMsg: Message = {
        id: generateId(),
        sender: "user",
        text: text || "(nota de voz)",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMsg]);

      const loadingMsg: Message = {
        id: generateId(),
        sender: "clara",
        text: "",
        timestamp: new Date(),
        loading: true,
      };
      setMessages((prev) => [...prev, loadingMsg]);
      setIsLoading(true);

      try {
        const response: ChatResponse = await sendMessage({
          text,
          language,
          input_type: audioBase64 ? "audio" : "text",
          audio_base64: audioBase64 || null,
          image_base64: null,
          session_id: sessionId.current,
        });

        const claraMsg: Message = {
          id: generateId(),
          sender: "clara",
          text: response.response,
          audio_url: response.audio_url,
          sources: response.sources,
          timestamp: new Date(),
        };

        setMessages((prev) =>
          prev.filter((m) => m.id !== loadingMsg.id).concat(claraMsg)
        );
      } catch {
        const errorMsg: Message = {
          id: generateId(),
          sender: "clara",
          text:
            language === "fr"
              ? "Desole, je n'ai pas pu traiter ta demande. Reessaie."
              : "Perdona, no he podido procesar tu mensaje. Intentalo de nuevo.",
          timestamp: new Date(),
        };
        setMessages((prev) =>
          prev.filter((m) => m.id !== loadingMsg.id).concat(errorMsg)
        );
      } finally {
        setIsLoading(false);
      }
    },
    [language]
  );

  return { messages, isLoading, language, setLanguage, send, addWelcome };
}
```

### Step 2: Header.tsx

Crear `clara-web/src/components/Header.tsx`:

```typescript
"use client";

import { useRouter } from "next/navigation";
import type { Language } from "@/lib/types";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const router = useRouter();

  return (
    <header className="sticky top-0 z-10 flex items-center justify-between px-4 h-[56px] bg-clara-blue text-white">
      <button
        onClick={() => router.push("/")}
        aria-label="Volver al inicio"
        className="min-w-touch-sm min-h-touch-sm flex items-center justify-center rounded-lg"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
        </svg>
      </button>

      <h1 className="font-display font-bold text-[20px]">Clara</h1>

      <div className="flex items-center gap-2">
        <select
          value={language}
          onChange={(e) => onLanguageChange(e.target.value as Language)}
          aria-label="Idioma"
          className="bg-white/20 text-white border border-white/30 rounded-lg px-2 py-1 text-label font-medium"
        >
          <option value="es" className="text-clara-text">ES</option>
          <option value="fr" className="text-clara-text">FR</option>
        </select>
      </div>
    </header>
  );
}
```

### Step 3: MessageList.tsx

Crear `clara-web/src/components/MessageList.tsx`:

```typescript
"use client";

import { useEffect, useRef } from "react";
import ChatBubble from "@/components/ui/ChatBubble";
import LoadingState from "@/components/ui/LoadingState";
import type { Message, Language } from "@/lib/types";

interface MessageListProps {
  messages: Message[];
  language: Language;
}

const loadingMessages: Record<Language, string> = {
  es: "Clara esta buscando informacion...",
  fr: "Clara cherche des informations...",
};

export default function MessageList({ messages, language }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-6 space-y-2"
      role="log"
      aria-label="Conversacion con Clara"
      aria-live="polite"
    >
      {messages.map((msg) =>
        msg.loading ? (
          <LoadingState key={msg.id} message={loadingMessages[language]} />
        ) : (
          <ChatBubble
            key={msg.id}
            sender={msg.sender}
            timestamp={msg.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          >
            <p className="whitespace-pre-wrap">{msg.text}</p>
            {msg.sources && msg.sources.length > 0 && (
              <p className="text-[14px] mt-2 opacity-80">
                Fuente:{" "}
                {msg.sources.map((s, i) => (
                  <a
                    key={i}
                    href={s.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline"
                  >
                    {s.name}
                  </a>
                ))}
              </p>
            )}
          </ChatBubble>
        )
      )}
      <div ref={bottomRef} />
    </div>
  );
}
```

### Step 4: ChatInput.tsx

Crear `clara-web/src/components/ChatInput.tsx`:

```typescript
"use client";

import { useState, useRef } from "react";
import type { Language } from "@/lib/types";

interface ChatInputProps {
  onSendText: (text: string) => void;
  onStartVoice: () => void;
  onOpenCamera: () => void;
  disabled: boolean;
  language: Language;
}

const placeholders: Record<Language, string> = {
  es: "Escribe tu pregunta...",
  fr: "Ecris ta question...",
};

export default function ChatInput({
  onSendText,
  onStartVoice,
  onOpenCamera,
  disabled,
  language,
}: ChatInputProps) {
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;
    onSendText(trimmed);
    setText("");
    inputRef.current?.focus();
  }

  return (
    <div className="sticky bottom-0 bg-white border-t border-clara-border px-4 py-3 space-y-3">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={placeholders[language]}
          disabled={disabled}
          aria-label={placeholders[language]}
          className="flex-1 h-[56px] px-4 border-2 border-clara-border rounded-xl
                     text-body-sm font-body bg-white
                     focus:border-clara-blue focus:outline-none
                     disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={disabled || !text.trim()}
          aria-label={language === "fr" ? "Envoyer" : "Enviar"}
          className="min-w-touch min-h-touch bg-clara-blue text-white rounded-xl
                     flex items-center justify-center
                     disabled:opacity-50"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </form>

      <div className="flex gap-3 justify-center">
        <button
          onClick={() => inputRef.current?.focus()}
          disabled={disabled}
          aria-label={language === "fr" ? "Ecrire" : "Escribir"}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-border text-clara-text-secondary
                     hover:border-clara-blue hover:text-clara-blue
                     disabled:opacity-50"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20 5H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z" />
          </svg>
          <span className="text-[14px] mt-1">{language === "fr" ? "Ecrire" : "Escribir"}</span>
        </button>

        <button
          onClick={onStartVoice}
          disabled={disabled}
          aria-label={language === "fr" ? "Enregistrer la voix" : "Grabar voz"}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-orange text-clara-orange
                     hover:bg-clara-orange hover:text-white
                     disabled:opacity-50"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
          </svg>
          <span className="text-[14px] mt-1">{language === "fr" ? "Voix" : "Voz"}</span>
        </button>

        <button
          onClick={onOpenCamera}
          disabled={disabled}
          aria-label={language === "fr" ? "Photo" : "Foto"}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-border text-clara-text-secondary
                     hover:border-clara-blue hover:text-clara-blue
                     disabled:opacity-50"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
          </svg>
          <span className="text-[14px] mt-1">{language === "fr" ? "Photo" : "Foto"}</span>
        </button>
      </div>
    </div>
  );
}
```

### Step 5: Chat page

Crear `clara-web/src/app/chat/page.tsx`:

```typescript
"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Header from "@/components/Header";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import { useChat } from "@/hooks/useChat";
import type { Language } from "@/lib/types";

export default function ChatPage() {
  const searchParams = useSearchParams();
  const initialLang = (searchParams.get("lang") as Language) || "es";
  const { messages, isLoading, language, setLanguage, send, addWelcome } =
    useChat(initialLang);
  const [voiceActive, setVoiceActive] = useState(false);

  useEffect(() => {
    addWelcome();
  }, [addWelcome]);

  return (
    <div className="flex flex-col h-screen bg-clara-bg">
      <Header language={language} onLanguageChange={setLanguage} />
      <MessageList messages={messages} language={language} />
      <ChatInput
        onSendText={(text) => send(text)}
        onStartVoice={() => setVoiceActive(true)}
        onOpenCamera={() => {
          /* Q9 */
        }}
        disabled={isLoading}
        language={language}
      />
    </div>
  );
}
```

### Step 6: Verificar flujo completo

Run: `cd clara-web && npm run dev`
1. Abrir `http://localhost:3000` — ver bienvenida
2. Click "Empezar a hablar" o "Prefiero escribir" — navegar a /chat
3. Ver mensaje de bienvenida de Clara
4. Escribir "Que es el IMV?" y enviar
5. Ver loading state, luego respuesta (si backend esta corriendo) o error amigable

### Step 7: Commit

```bash
git add clara-web/src/app/chat/ clara-web/src/components/Header.tsx clara-web/src/components/MessageList.tsx clara-web/src/components/ChatInput.tsx clara-web/src/hooks/
git commit -m "feat: add Chat page with message list, input, header, and useChat hook"
```

---

## Q7: Grabacion de Voz

> **Objetivo:** Implementar grabacion de audio con Web Audio API. Mecanismo toggle (tap-to-start, tap-to-stop), NO press-and-hold (dificil para mayores con problemas de destreza). Feedback visual: boton rojo + onda animada + timer.

**Files:**
- Create: `clara-web/src/components/VoiceRecorder.tsx`
- Create: `clara-web/src/hooks/useAudioRecorder.ts`
- Modify: `clara-web/src/app/chat/page.tsx` (integrar VoiceRecorder)

### Step 1: useAudioRecorder hook

Crear `clara-web/src/hooks/useAudioRecorder.ts`:

```typescript
"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import { MAX_RECORDING_SECONDS, RECORDING_WARNING_SECONDS } from "@/lib/constants";

interface RecorderState {
  isRecording: boolean;
  seconds: number;
  isWarning: boolean;
  error: string | null;
}

export function useAudioRecorder() {
  const [state, setState] = useState<RecorderState>({
    isRecording: false,
    seconds: 0,
    isWarning: false,
    error: null,
  });

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const cleanup = useCallback(() => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    mediaRecorderRef.current?.stream
      .getTracks()
      .forEach((track) => track.stop());
  }, []);

  useEffect(() => {
    return cleanup;
  }, [cleanup]);

  const start = useCallback(async () => {
    try {
      chunksRef.current = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
          ? "audio/webm;codecs=opus"
          : "audio/webm",
      });
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.start(100);
      setState({ isRecording: true, seconds: 0, isWarning: false, error: null });

      timerRef.current = setInterval(() => {
        setState((prev) => {
          const next = prev.seconds + 1;
          if (next >= MAX_RECORDING_SECONDS) {
            cleanup();
            return { ...prev, isRecording: false, seconds: next };
          }
          return {
            ...prev,
            seconds: next,
            isWarning: next >= RECORDING_WARNING_SECONDS,
          };
        });
      }, 1000);
    } catch {
      setState((prev) => ({
        ...prev,
        error: "No se pudo acceder al microfono",
      }));
    }
  }, [cleanup]);

  const stop = useCallback((): Promise<string> => {
    return new Promise((resolve) => {
      const recorder = mediaRecorderRef.current;
      if (!recorder || recorder.state !== "recording") {
        resolve("");
        return;
      }

      recorder.onstop = async () => {
        if (timerRef.current) clearInterval(timerRef.current);
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const buffer = await blob.arrayBuffer();
        const base64 = btoa(
          new Uint8Array(buffer).reduce(
            (data, byte) => data + String.fromCharCode(byte),
            ""
          )
        );
        setState((prev) => ({ ...prev, isRecording: false }));
        recorder.stream.getTracks().forEach((track) => track.stop());
        resolve(base64);
      };

      recorder.stop();
    });
  }, []);

  const cancel = useCallback(() => {
    cleanup();
    chunksRef.current = [];
    setState({ isRecording: false, seconds: 0, isWarning: false, error: null });
  }, [cleanup]);

  return { ...state, start, stop, cancel };
}
```

### Step 2: VoiceRecorder.tsx

Crear `clara-web/src/components/VoiceRecorder.tsx`:

```typescript
"use client";

import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import type { Language } from "@/lib/types";

interface VoiceRecorderProps {
  language: Language;
  onRecordingComplete: (audioBase64: string) => void;
  onCancel: () => void;
}

const labels = {
  es: {
    speak: "Habla ahora...",
    cancel: "Cancelar",
    send: "Enviar",
    warning: "Quedan pocos segundos",
    tap_start: "Toca para grabar",
    tap_stop: "Toca para parar",
  },
  fr: {
    speak: "Parle maintenant...",
    cancel: "Annuler",
    send: "Envoyer",
    warning: "Il reste peu de secondes",
    tap_start: "Appuie pour enregistrer",
    tap_stop: "Appuie pour arreter",
  },
};

export default function VoiceRecorder({
  language,
  onRecordingComplete,
  onCancel,
}: VoiceRecorderProps) {
  const { isRecording, seconds, isWarning, error, start, stop, cancel } =
    useAudioRecorder();
  const t = labels[language];

  async function handleToggle() {
    if (isRecording) {
      const base64 = await stop();
      if (base64) onRecordingComplete(base64);
    } else {
      await start();
    }
  }

  function handleCancel() {
    cancel();
    onCancel();
  }

  async function handleSend() {
    const base64 = await stop();
    if (base64) onRecordingComplete(base64);
  }

  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const timeDisplay = `${minutes}:${secs.toString().padStart(2, "0")}`;

  return (
    <div className="fixed inset-0 bg-clara-bg z-50 flex flex-col items-center justify-center px-6">
      <p className="font-display font-bold text-h2 text-clara-text mb-8">
        {isRecording ? t.speak : t.tap_start}
      </p>

      {/* Onda de audio animada */}
      {isRecording && (
        <div className="flex items-center gap-1 mb-6 h-8" aria-hidden="true">
          {Array.from({ length: 12 }).map((_, i) => (
            <span
              key={i}
              className="w-1 bg-clara-orange rounded-full animate-pulse"
              style={{
                height: `${12 + Math.random() * 20}px`,
                animationDelay: `${i * 80}ms`,
                animationDuration: "0.6s",
              }}
            />
          ))}
        </div>
      )}

      {/* Timer */}
      <p
        className={`font-mono text-[24px] mb-8 ${isWarning ? "text-clara-error font-bold" : "text-clara-text-secondary"}`}
        aria-live="polite"
      >
        {timeDisplay}
        {isWarning && <span className="sr-only">{t.warning}</span>}
      </p>

      {/* Boton microfono grande 96x96px */}
      <button
        onClick={handleToggle}
        aria-label={isRecording ? t.tap_stop : t.tap_start}
        className={`
          w-touch-lg h-touch-lg rounded-full flex items-center justify-center
          transition-colors duration-200 mb-10
          ${isRecording
            ? "bg-clara-error animate-pulse"
            : "bg-clara-blue hover:bg-[#164d66]"
          }
        `}
      >
        <svg width="48" height="48" viewBox="0 0 24 24" fill="white" aria-hidden="true">
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
          <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
        </svg>
      </button>

      {/* Cancelar / Enviar */}
      <div className="flex gap-4 w-full max-w-sm">
        <button
          onClick={handleCancel}
          aria-label={t.cancel}
          className="flex-1 h-touch bg-white border-2 border-clara-border rounded-xl
                     text-button font-medium text-clara-text-secondary
                     hover:border-clara-error hover:text-clara-error"
        >
          {t.cancel}
        </button>
        {isRecording && (
          <button
            onClick={handleSend}
            aria-label={t.send}
            className="flex-1 h-touch bg-clara-green text-white rounded-xl
                       text-button font-medium hover:bg-[#256940]"
          >
            {t.send}
          </button>
        )}
      </div>

      {error && (
        <p role="alert" className="mt-4 text-clara-error text-body-sm">
          {error}
        </p>
      )}
    </div>
  );
}
```

### Step 3: Integrar en chat page

Modificar `clara-web/src/app/chat/page.tsx` — agregar estado y render condicional del VoiceRecorder:

Despues de `const [voiceActive, setVoiceActive] = useState(false);` ya existente, agregar el render:

```typescript
// Dentro del return, antes de </div> final:
{voiceActive && (
  <VoiceRecorder
    language={language}
    onRecordingComplete={(audioBase64) => {
      setVoiceActive(false);
      send("", audioBase64);
    }}
    onCancel={() => setVoiceActive(false)}
  />
)}
```

Y agregar el import:
```typescript
import VoiceRecorder from "@/components/VoiceRecorder";
```

### Step 4: Verificar

Run: `cd clara-web && npm run dev`
1. Ir a /chat
2. Click boton "Voz" -> se abre pantalla de grabacion
3. Click mic grande -> empieza a grabar (pide permiso de microfono)
4. Timer corre, onda animada visible
5. Click mic de nuevo -> para y envia
6. Verificar boton Cancelar cierra sin enviar

### Step 5: Commit

```bash
git add clara-web/src/components/VoiceRecorder.tsx clara-web/src/hooks/useAudioRecorder.ts clara-web/src/app/chat/page.tsx
git commit -m "feat: add voice recorder with toggle mic, animated wave, timer, and 60s limit"
```

---

## Q8: Audio Player

> **Objetivo:** Reproductor de audio integrado en burbujas de Clara. Play/pause, barra de progreso, velocidad (0.75x/1x/1.25x). NO auto-play.

**Files:**
- Create: `clara-web/src/components/ui/AudioPlayer.tsx`
- Modify: `clara-web/src/components/MessageList.tsx` (integrar AudioPlayer)

### Step 1: AudioPlayer.tsx

Crear `clara-web/src/components/ui/AudioPlayer.tsx`:

```typescript
"use client";

import { useState, useRef, useEffect } from "react";

interface AudioPlayerProps {
  src: string;
  label?: string;
}

const SPEEDS = [0.75, 1, 1.25] as const;

export default function AudioPlayer({
  src,
  label = "Escuchar respuesta",
}: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [speedIdx, setSpeedIdx] = useState(1);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const onTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
      setProgress(audio.duration ? (audio.currentTime / audio.duration) * 100 : 0);
    };
    const onLoadedMetadata = () => setDuration(audio.duration);
    const onEnded = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("ended", onEnded);

    return () => {
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("ended", onEnded);
    };
  }, []);

  function togglePlay() {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  }

  function cycleSpeed() {
    const next = (speedIdx + 1) % SPEEDS.length;
    setSpeedIdx(next);
    if (audioRef.current) audioRef.current.playbackRate = SPEEDS[next];
  }

  function formatTime(s: number): string {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${sec.toString().padStart(2, "0")}`;
  }

  return (
    <div className="flex items-center gap-3 bg-clara-green/10 rounded-xl px-3 py-2 mt-2">
      <audio ref={audioRef} src={src} preload="metadata" />

      <button
        onClick={togglePlay}
        aria-label={isPlaying ? "Pausar audio" : label}
        className="min-w-touch-sm min-h-touch-sm flex items-center justify-center
                   bg-clara-green text-white rounded-full"
      >
        {isPlaying ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M8 5v14l11-7z" />
          </svg>
        )}
      </button>

      <div className="flex-1">
        <div className="w-full h-2 bg-clara-border rounded-full overflow-hidden">
          <div
            className="h-full bg-clara-green rounded-full transition-all duration-200"
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="flex justify-between text-[12px] text-clara-text-secondary mt-1">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      <button
        onClick={cycleSpeed}
        aria-label={`Velocidad ${SPEEDS[speedIdx]}x`}
        className="min-w-[44px] min-h-[44px] text-[14px] font-bold text-clara-green
                   border border-clara-green rounded-lg"
      >
        {SPEEDS[speedIdx]}x
      </button>
    </div>
  );
}
```

### Step 2: Integrar en MessageList

Modificar `clara-web/src/components/MessageList.tsx` — dentro del ChatBubble de Clara, despues del texto, renderizar AudioPlayer si hay audio_url:

Agregar import:
```typescript
import AudioPlayer from "@/components/ui/AudioPlayer";
```

Dentro del map de mensajes, despues de `<p className="whitespace-pre-wrap">{msg.text}</p>`, agregar:

```typescript
{msg.audio_url && (
  <AudioPlayer
    src={msg.audio_url}
    label={language === "fr" ? "Ecouter la reponse" : "Escuchar respuesta"}
  />
)}
```

### Step 3: Verificar

Run: `cd clara-web && npm run dev`
Enviar pregunta que devuelva audio_url (ej: desde cache). Verificar:
- Boton play 48px verde visible
- Click play -> audio suena, barra progresa
- Click boton velocidad -> cicla 0.75x, 1x, 1.25x
- NO auto-play

### Step 4: Commit

```bash
git add clara-web/src/components/ui/AudioPlayer.tsx clara-web/src/components/MessageList.tsx
git commit -m "feat: add AudioPlayer with play/pause, progress bar, and speed control"
```

---

## Q9: Subida de Documento

> **Objetivo:** Subida de foto (camara o galeria) para que Clara analice documentos. HTML `<input type="file" accept="image/*" capture="environment">`.

**Files:**
- Create: `clara-web/src/components/DocumentUpload.tsx`
- Modify: `clara-web/src/app/chat/page.tsx` (integrar DocumentUpload)

### Step 1: DocumentUpload.tsx

Crear `clara-web/src/components/DocumentUpload.tsx`:

```typescript
"use client";

import { useState, useRef } from "react";
import type { Language } from "@/lib/types";
import Button from "@/components/ui/Button";

interface DocumentUploadProps {
  language: Language;
  onUpload: (imageBase64: string) => void;
  onCancel: () => void;
}

const labels = {
  es: {
    title: "Subir documento",
    desc: "Sube una foto de tu documento o carta. Clara te explicara que dice.",
    camera: "Hacer foto",
    gallery: "Elegir de galeria",
    cancel: "Cancelar",
    send: "Enviar a Clara",
    preview: "Vista previa del documento",
  },
  fr: {
    title: "Envoyer un document",
    desc: "Envoie une photo de ton document ou courrier. Clara t'expliquera ce qu'il dit.",
    camera: "Prendre une photo",
    gallery: "Choisir dans la galerie",
    cancel: "Annuler",
    send: "Envoyer a Clara",
    preview: "Apercu du document",
  },
};

export default function DocumentUpload({
  language,
  onUpload,
  onCancel,
}: DocumentUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [base64, setBase64] = useState<string>("");
  const cameraRef = useRef<HTMLInputElement>(null);
  const galleryRef = useRef<HTMLInputElement>(null);
  const t = labels[language];

  function handleFile(file: File) {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      setPreview(result);
      setBase64(result.split(",")[1]);
    };
    reader.readAsDataURL(file);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }

  return (
    <div className="fixed inset-0 bg-clara-bg z-50 flex flex-col px-6 py-8">
      <div className="flex items-center mb-6">
        <button
          onClick={onCancel}
          aria-label={t.cancel}
          className="min-w-touch-sm min-h-touch-sm flex items-center justify-center"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
          </svg>
        </button>
        <h2 className="font-display font-bold text-h2 ml-2">{t.title}</h2>
      </div>

      <p className="text-body text-clara-text-secondary mb-8">{t.desc}</p>

      {preview ? (
        <div className="flex-1 flex flex-col items-center">
          <img
            src={preview}
            alt={t.preview}
            className="max-h-[50vh] rounded-xl border-2 border-clara-border object-contain mb-6"
          />
          <div className="flex gap-4 w-full max-w-sm">
            <Button
              variant="secondary"
              fullWidth
              onPress={() => { setPreview(null); setBase64(""); }}
            >
              {t.cancel}
            </Button>
            <Button
              variant="primary"
              fullWidth
              onPress={() => onUpload(base64)}
            >
              {t.send}
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex flex-col items-center gap-4">
          <input
            ref={cameraRef}
            type="file"
            accept="image/*"
            capture="environment"
            onChange={handleChange}
            className="hidden"
            aria-hidden="true"
          />
          <input
            ref={galleryRef}
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="hidden"
            aria-hidden="true"
          />

          <Button
            variant="primary"
            fullWidth
            onPress={() => cameraRef.current?.click()}
            icon={
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
                <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
              </svg>
            }
            className="h-[72px]"
          >
            {t.camera}
          </Button>

          <Button
            variant="secondary"
            fullWidth
            onPress={() => galleryRef.current?.click()}
          >
            {t.gallery}
          </Button>
        </div>
      )}
    </div>
  );
}
```

### Step 2: Integrar en chat page

Modificar `clara-web/src/app/chat/page.tsx`:

Agregar estado:
```typescript
const [cameraActive, setCameraActive] = useState(false);
```

Actualizar `onOpenCamera`:
```typescript
onOpenCamera={() => setCameraActive(true)}
```

Agregar render condicional:
```typescript
{cameraActive && (
  <DocumentUpload
    language={language}
    onUpload={(imageBase64) => {
      setCameraActive(false);
      send("(documento enviado)", imageBase64);
    }}
    onCancel={() => setCameraActive(false)}
  />
)}
```

Import:
```typescript
import DocumentUpload from "@/components/DocumentUpload";
```

### Step 3: Commit

```bash
git add clara-web/src/components/DocumentUpload.tsx clara-web/src/app/chat/page.tsx
git commit -m "feat: add DocumentUpload with camera capture, gallery picker, and preview"
```

---

## Q10: i18n (ES/FR)

> **Objetivo:** Internacionalizacion completa con next-intl. Todos los strings via archivos de mensajes. Middleware de locale.

**Files:**
- Create: `clara-web/src/messages/es.json`
- Create: `clara-web/src/messages/fr.json`
- Create: `clara-web/src/i18n/request.ts`
- Modify: `clara-web/next.config.ts`

### Step 1: Archivos de mensajes

Crear `clara-web/src/messages/es.json`:

```json
{
  "welcome": {
    "tagline": "Tu voz tiene poder",
    "description": "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
    "cta_voice": "Empezar a hablar",
    "cta_text": "Prefiero escribir"
  },
  "chat": {
    "placeholder": "Escribe tu pregunta...",
    "send": "Enviar",
    "write": "Escribir",
    "voice": "Voz",
    "photo": "Foto",
    "loading": "Clara esta buscando informacion...",
    "error": "Perdona, no he podido procesar tu mensaje. Intentalo de nuevo.",
    "source": "Fuente"
  },
  "voice": {
    "speak_now": "Habla ahora...",
    "tap_start": "Toca para grabar",
    "tap_stop": "Toca para parar",
    "cancel": "Cancelar",
    "send": "Enviar",
    "warning": "Quedan pocos segundos"
  },
  "document": {
    "title": "Subir documento",
    "description": "Sube una foto de tu documento o carta. Clara te explicara que dice.",
    "camera": "Hacer foto",
    "gallery": "Elegir de galeria",
    "cancel": "Cancelar",
    "send": "Enviar a Clara"
  },
  "audio": {
    "listen": "Escuchar respuesta",
    "pause": "Pausar audio",
    "speed": "Velocidad"
  },
  "a11y": {
    "skip_to_content": "Ir al contenido principal",
    "back": "Volver al inicio",
    "language": "Idioma",
    "conversation": "Conversacion con Clara"
  }
}
```

Crear `clara-web/src/messages/fr.json`:

```json
{
  "welcome": {
    "tagline": "Ta voix a du pouvoir",
    "description": "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
    "cta_voice": "Commencer a parler",
    "cta_text": "Je prefere ecrire"
  },
  "chat": {
    "placeholder": "Ecris ta question...",
    "send": "Envoyer",
    "write": "Ecrire",
    "voice": "Voix",
    "photo": "Photo",
    "loading": "Clara cherche des informations...",
    "error": "Desole, je n'ai pas pu traiter ta demande. Reessaie.",
    "source": "Source"
  },
  "voice": {
    "speak_now": "Parle maintenant...",
    "tap_start": "Appuie pour enregistrer",
    "tap_stop": "Appuie pour arreter",
    "cancel": "Annuler",
    "send": "Envoyer",
    "warning": "Il reste peu de secondes"
  },
  "document": {
    "title": "Envoyer un document",
    "description": "Envoie une photo de ton document ou courrier. Clara t'expliquera ce qu'il dit.",
    "camera": "Prendre une photo",
    "gallery": "Choisir dans la galerie",
    "cancel": "Annuler",
    "send": "Envoyer a Clara"
  },
  "audio": {
    "listen": "Ecouter la reponse",
    "pause": "Mettre en pause",
    "speed": "Vitesse"
  },
  "a11y": {
    "skip_to_content": "Aller au contenu principal",
    "back": "Retour a l'accueil",
    "language": "Langue",
    "conversation": "Conversation avec Clara"
  }
}
```

### Step 2: Configurar next-intl

Crear `clara-web/src/i18n/request.ts`:

```typescript
import { getRequestConfig } from "next-intl/server";

export default getRequestConfig(async () => {
  const locale = "es";
  return {
    locale,
    messages: (await import(`../messages/${locale}.json`)).default,
  };
});
```

### Step 3: Configurar next.config

Modificar `clara-web/next.config.ts`:

```typescript
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

const nextConfig = {};

export default withNextIntl(nextConfig);
```

### Step 4: Verificar build

Run: `cd clara-web && npm run build`
Expected: Build exitoso

### Step 5: Commit

```bash
git add clara-web/src/messages/ clara-web/src/i18n/ clara-web/next.config.ts
git commit -m "feat: add i18n with next-intl — Spanish and French message files"
```

**Nota:** La integracion completa de `useTranslations()` en cada componente se hace refactorizando los strings hardcodeados de Q4-Q9. Esto se puede hacer progresivamente.

---

## Q11: PWA y Responsive

> **Objetivo:** Convertir la web app en PWA instalable con manifest, service worker basico, y verificar responsive en 3 viewports.

**Files:**
- Create: `clara-web/public/manifest.json`
- Create: `clara-web/public/icons/icon-192.png`
- Create: `clara-web/public/icons/icon-512.png`

### Step 1: manifest.json

Crear `clara-web/public/manifest.json`:

```json
{
  "name": "Clara — Tu voz tiene poder",
  "short_name": "Clara",
  "description": "Asistente de voz para tramites sociales en Espana",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FAFAFA",
  "theme_color": "#1B5E7B",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

### Step 2: Crear iconos placeholder

Usar Canva MCP para generar icono de Clara (circulo azul `#1B5E7B` con "C" blanca en Atkinson Bold), o crear placeholder de color solido por ahora.

### Step 3: Test responsive

Verificar manualmente o con DevTools en 3 viewports:
- **320px** (movil basico) — todo el contenido visible, botones 64px tocan bordes sin overflow
- **768px** (tablet) — contenido centrado con max-width
- **1440px** (desktop) — contenido centrado, max-width ~640px para chat

### Step 4: Commit

```bash
git add clara-web/public/manifest.json clara-web/public/icons/
git commit -m "feat: add PWA manifest and app icons for installable web app"
```

---

## Q12: Deploy

> **Objetivo:** Deploy completo. Frontend en Vercel (gratis), backend en Render (ya existe). Configurar CORS, env vars, verificar end-to-end.

**Files:**
- Modify: `clara-web/.env.local` -> `.env.production`
- Modify: `src/routes/api_chat.py` (CORS origin restringido en prod)

### Step 1: Preparar frontend para deploy

Crear `clara-web/.env.production`:

```
NEXT_PUBLIC_API_URL=https://civicaid-voice.onrender.com
```

### Step 2: Deploy a Vercel

```bash
cd clara-web
npx vercel --prod
```

Seguir prompts: nombre del proyecto "clara-web", directorio raiz ".", framework "Next.js".

Configurar env var en Vercel dashboard:
- `NEXT_PUBLIC_API_URL` = URL del backend en Render

### Step 3: Actualizar CORS en backend

Modificar `src/app.py` — cambiar CORS de `"*"` a URL especifica en produccion:

```python
frontend_origins = os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
CORS(app, resources={r"/api/*": {"origins": frontend_origins}})
```

Agregar `FRONTEND_URL` a Render env vars: la URL de Vercel.

### Step 4: Agregar FRONTEND_URL a Render

En Render dashboard, agregar:
```
FRONTEND_URL=https://clara-web.vercel.app
```

### Step 5: Test end-to-end

1. Abrir URL de Vercel en movil
2. Verificar: bienvenida carga, selector idioma funciona
3. Ir a chat, enviar "Que es el IMV?"
4. Verificar: respuesta llega del backend, audio reproducible
5. Probar grabacion de voz (requiere HTTPS — Vercel lo tiene)
6. Probar subida de foto

### Step 6: Commit

```bash
git add src/app.py clara-web/.env.production
git commit -m "feat: configure production deploy — Vercel frontend + Render backend with CORS"
```

---

## Resumen de Entregables

| # | Entregable | Verificacion |
|---|---|---|
| 1 | `POST /api/chat` funcional | `curl` devuelve JSON con response |
| 2 | `GET /api/health` funcional | Status 200 con features |
| 3 | Web app carga en <2s | Lighthouse Performance >90 |
| 4 | Pantalla bienvenida | Logo + tagline + 2 CTAs + selector idioma |
| 5 | Chat funcional | Enviar texto -> recibir respuesta Clara |
| 6 | Grabacion de voz | Toggle mic -> grabar -> enviar -> transcripcion |
| 7 | Audio player | Play/pause + barra + velocidad |
| 8 | Subida documento | Foto camara/galeria -> preview -> enviar |
| 9 | i18n ES/FR | Todos los strings traducidos |
| 10 | PWA instalable | manifest.json + iconos + standalone |
| 11 | Responsive | 320px / 768px / 1440px sin overflow |
| 12 | Deploy prod | Vercel + Render CORS configurado |
| 13 | WCAG AAA | Contraste 7:1, botones 64px, focus 3px, aria-labels |

## Orden de Ejecucion

```
Q1 (Backend API)  ████████  <- paralelo con Q2
Q2 (Scaffolding)  ████████  <- paralelo con Q1
Q3 (Componentes)  ██████
Q4 (Bienvenida)   ████
Q5 (API Client)   ████      <- depende de Q1+Q2
Q6 (Chat)         ██████████████  <- core, el mas largo
Q7 (Voz)          ████████  <- paralelo con Q8, Q9
Q8 (Audio)        ██████    <- paralelo con Q7, Q9
Q9 (Documento)    ██████    <- paralelo con Q7, Q8
Q10 (i18n)        ████      <- paralelo con Q11
Q11 (PWA)         ████      <- paralelo con Q10
Q12 (Deploy)      ████████  <- ultimo, integra todo
```

---

*Plan creado el 20 de febrero de 2026. Basado en: `design/00-REPORTE-INVESTIGACION-DESIGN-COMPLETO.md`, `design/01-BRAND-STRATEGY.md`, `design/02-FRONTEND-ACCESIBLE.md`, `design/FASE1-Q1-PROMPT.md`, `design/PLAN-8-FASES-DESIGN.md`. Para usuarios: Maria (74, espanola), Ahmed (28, senegales), Fatima (45, marroqui).*
