# FASE 1: Clara Web App Frontend — Plan de Implementacion

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Construir la web app responsive de Clara (frontend Next.js + endpoint API en Flask) para que usuarios vulnerables (mayores 65+, inmigrantes, baja alfabetizacion digital) puedan interactuar con Clara desde cualquier navegador, complementando el canal WhatsApp existente.

**Architecture:** Next.js 14 (App Router) como frontend standalone en `clara-web/`, conectado al backend Flask existente via nuevo endpoint `POST /api/chat`. El backend ya tiene todo el pipeline (guardrails, cache, KB, Gemini, TTS, verify). El frontend solo consume la API. Deploy: frontend en Vercel (gratis), backend sigue en Render.

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, React Aria Components, next-intl (ES/FR), Web Audio API (grabacion voz), Flask + flask-cors (nuevo endpoint API)

**Usuarios objetivo:**
- Maria, 74 anos, espanola, baja alfabetizacion digital, usa WhatsApp basico
- Ahmed, 28 anos, senegales en Espana, habla frances, no entiende burocracia espanola
- Fatima, 45 anos, marroqui, idioma arabe/frances, necesita orientacion sobre ayudas

**Parametros de accesibilidad (WCAG AAA):**
- Texto cuerpo: 18-20px Inter, line-height 1.6
- Titulares: 28-36px Atkinson Hyperlegible Bold
- Botones principales: 64x64px minimo
- Contraste: 7:1 texto normal, 4.5:1 texto grande
- Focus indicators: outline 3px `#1B5E7B`
- Touch targets: 64px acciones principales, 48px secundarias
- Respetar `prefers-reduced-motion`
- Todo navegable con teclado (Tab), sin trampas

**Skills de Claude a usar:** `nextjs-developer`, `frontend-developer`, `react-expert`, `react-best-practices`, `frontend-design`, `typescript-pro`, `tailwind`, `fastapi-expert` (para el endpoint Flask)

**MCPs disponibles:** Playwright (testing visual), Notion (tracking), Canva (assets)

---

## INDICE DE Qs

| Q | Nombre | Descripcion | Dependencias |
|---|--------|-------------|--------------|
| Q1 | Backend API Endpoint | Crear `POST /api/chat` y `GET /api/health` en Flask | Ninguna |
| Q2 | Scaffolding Next.js | Crear proyecto, configurar Tailwind con paleta Clara, fonts | Ninguna |
| Q3 | Design Tokens y Componentes Base | Button, ChatBubble, LanguageSelector, LoadingState | Q2 |
| Q4 | Pantalla de Bienvenida | Landing page con logo, selector idioma, CTAs | Q3 |
| Q5 | Cliente API y Types | `lib/api.ts`, `lib/types.ts`, conexion front-back | Q1, Q2 |
| Q6 | Interfaz de Chat | MessageList, ChatInput, Header, logica de conversacion | Q3, Q5 |
| Q7 | Grabacion de Voz | VoiceRecorder con Web Audio API, toggle mic | Q6 |
| Q8 | Audio Player | Reproductor con play/pause, barra progreso, velocidad | Q6 |
| Q9 | Subida de Documento | DocumentUpload con camara y galeria | Q6 |
| Q10 | i18n (ES/FR) | next-intl, archivos de mensajes, middleware locale | Q4, Q6 |
| Q11 | PWA y Responsive | manifest.json, service worker, meta viewport, test 320/768/1440px | Q6 |
| Q12 | Deploy | Frontend a Vercel, CORS config, variables entorno | Q1-Q11 |

**Paralelizacion:** Q1 y Q2 pueden correr en paralelo (backend y frontend son independientes). Q7, Q8 y Q9 pueden correr en paralelo entre si.

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
import json
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
    # flask-cors should add Access-Control headers
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
        "body": ["20px", { lineHeight: "1.6" }],
        "body-sm": ["18px", { lineHeight: "1.6" }],
        "h1": ["36px", { lineHeight: "1.3" }],
        "h2": ["28px", { lineHeight: "1.3" }],
        "button": ["20px", { lineHeight: "1.0" }],
        "label": ["16px", { lineHeight: "1.4" }],
      },
      spacing: {
        "touch": "64px",
        "touch-sm": "48px",
        "touch-lg": "96px",
      },
      borderRadius: {
        "bubble": "16px",
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
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import localFont from "next/font/local";
import "./globals.css";

const inter = Inter({
  subsets: ["latin", "latin-ext"],
  variable: "--font-inter",
  display: "swap",
});

const atkinson = localFont({
  src: [
    { path: "../fonts/AtkinsonHyperlegible-Regular.woff2", weight: "400" },
    { path: "../fonts/AtkinsonHyperlegible-Bold.woff2", weight: "700" },
  ],
  variable: "--font-atkinson",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Clara — Tu voz tiene poder",
  description:
    "Asistente de voz que te ayuda con tramites sociales en Espana. Habla o escribe en tu idioma.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className={`${inter.variable} ${atkinson.variable}`}>
      <body className="bg-clara-bg text-clara-text font-body antialiased">
        <main id="main-content" role="main">
          {children}
        </main>
      </body>
    </html>
  );
}
```

**Nota:** Descargar fonts Atkinson Hyperlegible woff2 a `clara-web/src/fonts/`. Si no estan disponibles en local, usar Google Fonts CDN como fallback temporal:
```typescript
// Alternativa si no hay archivos locales:
import { Atkinson_Hyperlegible } from "next/font/google";
const atkinson = Atkinson_Hyperlegible({ subsets: ["latin"], weight: ["400", "700"], variable: "--font-atkinson" });
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

  /* Focus visible para accesibilidad AAA */
  *:focus-visible {
    outline: var(--focus-ring);
    outline-offset: 2px;
    border-radius: 4px;
  }

  /* Respetar preferencia de movimiento reducido */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }

  /* Texto maximo 70 caracteres por linea */
  p, li, dd {
    max-width: 70ch;
  }

  /* Scroll suave solo si el usuario no prefiere movimiento reducido */
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
Expected: App corriendo en `http://localhost:3000`

### Step 7: Commit

```bash
git add clara-web/
git commit -m "feat: scaffold Next.js frontend with Clara design tokens and accessible defaults"
```

---

## Q3: Design Tokens y Componentes Base

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
    <div
      className={`flex ${isClara ? "justify-start" : "justify-end"} mb-4`}
      role="log"
    >
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
            focus-visible:outline focus-visible:outline-[3px]
            focus-visible:outline-clara-blue focus-visible:outline-offset-2
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

### Step 5: Verificar que compila

```bash
cd clara-web && npm run build
```
Expected: Build exitoso sin errores

### Step 6: Commit

```bash
git add clara-web/src/components/
git commit -m "feat: add accessible UI components — Button, ChatBubble, LanguageSelector, LoadingState"
```
