# Q2: Scaffolding Next.js — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q1 (Backend API Endpoint) puede ejecutarse en paralelo — Q2 NO depende de Q1.
> **Tiempo estimado:** 10-20 min

---

## PROMPT

### ROL Y SKILLS

Eres un ingeniero frontend senior especializado en accesibilidad y sistemas de diseno inclusivos. Tu tarea es crear el scaffolding completo del proyecto Next.js para **Clara**, una web app para personas vulnerables en Espana (mayores 65+, inmigrantes, personas con baja alfabetizacion digital).

**Skills OBLIGATORIAS (invoca con `/skill-name`):**

| Skill | Cuando usarla | Fase |
|-------|---------------|------|
| `/executing-plans` | Gobierna toda la ejecucion — sigue este prompt paso a paso | TODA |
| `/nextjs-developer` | Scaffolding, App Router, layout, configuracion Next.js | Fase Scaffolding |
| `/frontend-design` | Sistema de diseno, tokens CSS, Tailwind config | Fase Design Tokens |
| `/typescript-pro` | Tipado estricto en config files y layout | TODA |
| `/react-best-practices` | Estructura de componentes, patrones React | Fase Layout |
| `/verification-before-completion` | Checklist final antes del commit | Fase Final |

**Skills RECOMENDADAS (usa si detectas problemas):**

| Skill | Cuando usarla |
|-------|---------------|
| `/ux-heuristics` | Para validar decisiones de accesibilidad en el layout |
| `/design-trends-2026` | Si necesitas referencia de tendencias actuales |
| `/brand-guidelines` | Para validar que los tokens de marca son correctos |
| `/lighthouse-audit` | Si quieres validar performance/accesibilidad post-scaffold |
| `/systematic-debugging` | Si hay errores de compilacion al hacer `npm run dev` |
| `/top-design` | Para validar calidad del sistema de diseno |

### ESTRATEGIA MULTI-AGENTE

Este Q es mayormente secuencial (un paso depende del anterior), pero hay oportunidades de paralelismo:

```
FASE 1 — Scaffolding (secuencial, interactivo):
  Tu (principal): Ejecuta npx create-next-app + npm install

FASE 2 — Configuracion (puede ser paralelo en verificacion):
  Tu (principal): Escribe tailwind.config.ts, layout.tsx, globals.css

FASE 3 — Verificacion (paralelo):
  Agente A (Bash): npm run build (verifica que compila sin errores)
  Agente B (Bash): npx tsc --noEmit (verifica tipos TypeScript)
```

---

### CONTEXTO DEL PROYECTO

**Clara** es un asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar tramites del gobierno. Ya tiene un backend funcional en Flask. Tu trabajo es crear la estructura del proyecto frontend que consumira la API del backend.

**Usuarios objetivo — disena PARA ellos:**

| Persona | Edad | Contexto | Necesidades de UI |
|---------|------|----------|-------------------|
| **Maria** | 74 | Espanola, baja alfabetizacion digital, usa WhatsApp basico | Texto grande (20px+), botones enormes (64px), contraste AAA 7:1 |
| **Ahmed** | 28 | Senegales en Espana, habla frances | i18n ES/FR, lenguaje simple, sin jerga burocratica |
| **Fatima** | 45 | Marroqui, frances/arabe | Idioma configurable, iconos con labels de texto siempre |

**Arquitectura:**
```
[Frontend Next.js — tu trabajo]        [Backend Flask — ya existe]
clara-web/ (Vercel)           <--->    src/ (Render)
  POST /api/chat                       POST /api/chat
  (fetch desde el browser)             (pipeline: cache->KB->LLM->TTS)
```

El frontend vive en `clara-web/` dentro del mismo monorepo. Se deployara en Vercel (gratis). No toca el backend.

---

### ESPECIFICACIONES DE DISENO (SAGRADAS — no las cambies)

#### Paleta de Colores Clara

| Rol | Hex | Token Tailwind | Ratio Contraste |
|-----|-----|----------------|-----------------|
| Primario (Azul Confianza) | `#1B5E7B` | `clara-blue` | 7.2:1 vs blanco (AAA) |
| Secundario (Naranja Calido) | `#D46A1E` | `clara-orange` | 4.6:1 vs blanco (AA Large) |
| Acento (Verde Esperanza) | `#2E7D4F` | `clara-green` | 5.8:1 vs blanco (AAA Large) |
| Fondo | `#FAFAFA` | `clara-bg` | - |
| Texto Principal | `#1A1A2E` | `clara-text` | 16.8:1 vs #FAFAFA |
| Texto Secundario | `#4A4A5A` | `clara-text-secondary` | 9.1:1 vs #FAFAFA |
| Error | `#C62828` | `clara-error` | - |
| Warning | `#F9A825` | `clara-warning` | - |
| Info / Burbuja Clara | `#E3F2FD` | `clara-info` | - |
| Card BG | `#F5F5F5` | `clara-card` | - |
| Borde | `#E0E0E0` | `clara-border` | - |

**Validado para daltonismo** (deuteranopia, protanopia, tritanopia). Nunca usar color como unica forma de transmitir info.

#### Tipografia

| Uso | Fuente | Google Fonts | Pesos | Por que |
|-----|--------|-------------|-------|---------|
| **Titulos** | Atkinson Hyperlegible | `Atkinson_Hyperlegible` | 400, 700 | Disenada por Braille Institute para baja vision |
| **Cuerpo** | Inter | `Inter` | 400, 500 | Optimizada para pantallas, 200+ idiomas |

| Elemento | Tamano | Line-Height | Token Tailwind |
|----------|--------|-------------|----------------|
| H1 | 36px | 1.3 | `text-h1` |
| H2 | 28px | 1.3 | `text-h2` |
| Body | 20px | 1.6 | `text-body` |
| Body Small | 18px | 1.6 | `text-body-sm` |
| Button | 20px | 1.0 | `text-button` |
| Label | 16px | 1.4 | `text-label` |

#### Spacing / Touch Targets

| Token | Valor | Uso |
|-------|-------|-----|
| `touch` | 64px | Botones principales (minimo para mayores) |
| `touch-sm` | 48px | Botones secundarios |
| `touch-lg` | 96px | Boton microfono grabando |
| `bubble` | 16px | Border-radius burbujas de chat |

#### Accesibilidad WCAG AAA

- Focus indicators: outline 3px `#1B5E7B`, offset 2px
- `prefers-reduced-motion`: desactivar TODAS las animaciones
- Skip to content link ("Ir al contenido principal")
- `max-width: 70ch` en parrafos para legibilidad optima
- `maximumScale: 5` en viewport (NUNCA `user-scalable=no`)
- Todo navegable con Tab, sin trampas de teclado
- `lang="es"` en html tag

---

### ESTRUCTURA FINAL DE ARCHIVOS (lo que debe existir al terminar Q2)

```
clara-web/
  src/
    app/
      layout.tsx          # Root layout con fonts + metadata + skip link + ARIA
      page.tsx            # Placeholder (se reemplaza en Q4)
      globals.css         # Tailwind + tokens CSS + focus + reduced-motion
      chat/
        page.tsx          # Placeholder (se reemplaza en Q6)
    components/           # Vacio (se llena en Q3)
      ui/
    lib/                  # Vacio (se llena en Q5)
    messages/             # Vacio (se llena en Q10)
  public/
    icons/                # Vacio (se llena despues)
  tailwind.config.ts      # Paleta Clara completa
  next.config.ts          # Config basica (futuro: next-intl)
  tsconfig.json           # Generado por create-next-app
  package.json            # Next.js + react-aria-components + next-intl
```

---

## EJECUCION PASO A PASO

### PASO 0: Verificar que no existe el directorio

Antes de crear nada, verifica:

```bash
ls -la /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web 2>/dev/null && echo "YA EXISTE" || echo "NO EXISTE — OK"
```

- Si **YA EXISTE**: lee su `package.json` para entender que hay. No borres — pregunta al usuario.
- Si **NO EXISTE**: continua al Paso 1.

---

### PASO 1: Crear proyecto Next.js

**Skill activa:** `/nextjs-developer`

Ejecuta con **Bash**:

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && npx create-next-app@latest clara-web --typescript --tailwind --app --src-dir --no-eslint --no-import-alias
```

**Notas sobre las flags:**
- `--typescript`: TypeScript obligatorio
- `--tailwind`: Tailwind CSS preconfigurado
- `--app`: App Router (no Pages Router)
- `--src-dir`: Codigo en `src/` (consistente con el backend)
- `--no-eslint`: Evitar conflictos, usaremos config propia despues
- `--no-import-alias`: Sin alias `@/` para simplicidad

Si `create-next-app` hace preguntas interactivas, responde:
- Use App Router? **Yes**
- Customize import alias? **No**

**Verificacion:** Debe existir `clara-web/package.json` con `"next"` como dependencia.

---

### PASO 2: Instalar dependencias adicionales

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npm install react-aria-components next-intl
```

**Por que estas dos:**
- `react-aria-components`: Componentes headless con ARIA completo integrado. Usados por Adobe. Manejan focus management, keyboard navigation, screen reader support. Para Q3+.
- `next-intl`: Internacionalizacion ES/FR con soporte de App Router. Para Q10.

**Verificacion:** Ambas deben aparecer en `package.json` bajo `dependencies`.

---

### PASO 3: Configurar Tailwind con paleta Clara

**Skill activa:** `/frontend-design`

Lee primero el archivo generado por create-next-app:
```
Read: clara-web/tailwind.config.ts
```

Luego **reemplazalo completamente** con **Write**:

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

**Por que cada decision:**
- `colors.clara.*`: Paleta validada para WCAG AAA y daltonismo
- `fontFamily.display`: Atkinson Hyperlegible — disenada por Braille Institute para baja vision
- `fontFamily.body`: Inter — optimizada para pantallas, soporta 200+ idiomas
- `fontSize.body: 20px`: Recomendado para mayores 65+ (investigacion PMC)
- `spacing.touch: 64px`: Target minimo Braille Institute para elderly
- `borderRadius.bubble: 16px`: Para burbujas de chat tipo WhatsApp

---

### PASO 4: Configurar fonts y layout

**Skill activa:** `/nextjs-developer` + `/react-best-practices`

Lee primero:
```
Read: clara-web/src/app/layout.tsx
```

Luego **reemplazalo completamente** con **Write**:

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

**Decisiones de accesibilidad en el layout:**
- `lang="es"`: Screen readers saben en que idioma leer
- `display: "swap"`: Texto visible inmediatamente, sin flash de fuente invisible
- `maximumScale: 5`: Permite zoom hasta 5x (NUNCA `user-scalable=no`)
- Skip link (`sr-only focus:not-sr-only`): Visible solo con teclado, salta al contenido
- `role="main"` + `id="main-content"`: ARIA landmark para navegacion rapida
- `antialiased`: Mejora renderizado de fuentes en macOS/iOS

---

### PASO 5: Configurar globals.css

Lee primero:
```
Read: clara-web/src/app/globals.css
```

Luego **reemplazalo completamente** con **Write**:

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

  /* Focus indicator global — WCAG AAA visible focus */
  *:focus-visible {
    outline: var(--focus-ring);
    outline-offset: 2px;
    border-radius: 4px;
  }

  /* Reduced motion — desactivar TODAS las animaciones */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }

  /* Max line width para legibilidad optima */
  p, li, dd {
    max-width: 70ch;
  }

  /* Smooth scroll solo si el usuario no tiene reduced motion */
  @media (prefers-reduced-motion: no-preference) {
    html {
      scroll-behavior: smooth;
    }
  }
}
```

**Por que cada regla:**
- `focus-visible` (no `focus`): Solo muestra outline con teclado, no con click
- `prefers-reduced-motion`: Obligatorio WCAG 2.3.3. Personas con vestibular disorders
- `max-width: 70ch`: Optimo para legibilidad (investigacion tipografica)
- `scroll-behavior: smooth`: Solo si no hay reduced-motion

---

### PASO 6: Crear pagina placeholder y directorios

Crea el page.tsx placeholder para que la home page muestre algo significativo:

Lee primero:
```
Read: clara-web/src/app/page.tsx
```

Luego **reemplazalo completamente** con **Write**:

```typescript
export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 text-center">
      <h1 className="font-display text-h1 font-bold text-clara-blue mb-4">
        Clara
      </h1>
      <p className="font-display text-h2 text-clara-text mb-6">
        Tu voz tiene poder
      </p>
      <p className="text-body text-clara-text-secondary max-w-md">
        Asistente de voz que te ayuda con tramites sociales en Espana.
        Habla o escribe en tu idioma.
      </p>
      <div className="mt-8 flex gap-4">
        <div className="w-4 h-4 rounded-full bg-clara-blue" />
        <div className="w-4 h-4 rounded-full bg-clara-orange" />
        <div className="w-4 h-4 rounded-full bg-clara-green" />
      </div>
      <p className="mt-8 text-label text-clara-text-secondary">
        Scaffolding completo — Q3 agregara los componentes.
      </p>
    </div>
  );
}
```

Crea el placeholder para `/chat`:

```bash
mkdir -p /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/app/chat
```

Crea `clara-web/src/app/chat/page.tsx` con **Write**:

```typescript
export default function ChatPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="font-display text-h2 font-bold text-clara-blue">
        Chat con Clara
      </h1>
      <p className="text-body text-clara-text-secondary mt-4">
        Interfaz de chat — se implementa en Q6.
      </p>
    </div>
  );
}
```

Crea los directorios vacios que los Qs futuros necesitaran:

```bash
mkdir -p /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/components/ui
mkdir -p /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/lib
mkdir -p /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/messages
mkdir -p /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/public/icons
```

Crea archivos `.gitkeep` en cada uno para que Git los trackee:

```bash
touch /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/components/ui/.gitkeep
touch /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/lib/.gitkeep
touch /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/src/messages/.gitkeep
touch /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web/public/icons/.gitkeep
```

---

### PASO 7: Verificar que compila (usa agentes paralelos)

**Skill activa:** `/verification-before-completion`

**Lanza DOS comandos en paralelo con el Task tool (subagent_type="Bash"):**

**Comando 1 — Build completo:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npm run build
```
**Esperado:** Build exitoso sin errores. Output termina con "Compiled successfully" o similar.

**Comando 2 — Type check:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npx tsc --noEmit
```
**Esperado:** Sin errores de TypeScript.

**Si hay errores de compilacion:**
- Activa `/systematic-debugging`
- Lee el error completo
- Los errores mas comunes:
  - `Atkinson_Hyperlegible` no encontrado: Verifica que la importacion sea `from "next/font/google"` y el nombre sea exacto
  - Tailwind no reconoce tokens: Verifica que `tailwind.config.ts` tiene la extension `.ts` (no `.js`)
  - Tipo `Viewport` no encontrado: Requiere Next.js 14+ (si es 13, usa `export const metadata` con `viewport` nested)

---

### PASO 8: Test visual rapido (opcional pero recomendado)

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npm run dev &
sleep 5
curl -s http://localhost:3000 | head -20
kill %1
```

Deberia retornar HTML con:
- `<html lang="es">`
- Classes CSS de las fonts (`--font-inter`, `--font-atkinson`)
- Titulo "Clara"

**Si no puedes levantar el servidor:** El build exitoso del Paso 7 es suficiente.

---

### PASO 9: Verificacion de accesibilidad basica

**Skill activa:** `/ux-heuristics`

Verifica mentalmente antes del commit:

- [ ] `<html lang="es">` presente en layout
- [ ] Skip link ("Ir al contenido principal") presente
- [ ] `role="main"` + `id="main-content"` en `<main>`
- [ ] `maximumScale: 5` (no `user-scalable=no`)
- [ ] `focus-visible` global en globals.css
- [ ] `prefers-reduced-motion` respetado en globals.css
- [ ] `max-width: 70ch` en parrafos
- [ ] Fonts con `display: "swap"` (no flash invisible)
- [ ] `themeColor: "#1B5E7B"` para PWA
- [ ] Paleta completa de 11 colores en Tailwind config
- [ ] 6 tamanos de fuente definidos (h1, h2, body, body-sm, button, label)
- [ ] 3 tamanos tactiles definidos (touch, touch-sm, touch-lg)

---

### PASO 10: Commit

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && git add clara-web/
git commit -m "feat: scaffold Next.js 14 frontend with Clara design tokens and WCAG AAA defaults

- Next.js 14 (App Router, TypeScript, Tailwind CSS, src dir)
- Clara palette: 11 tokens (#1B5E7B blue, #D46A1E orange, #2E7D4F green, etc.)
- Fonts: Atkinson Hyperlegible (Braille Institute) + Inter (body)
- Accessibility: skip link, focus-visible, prefers-reduced-motion, 70ch max width
- Touch targets: 64px primary, 48px secondary, 96px mic button
- Dependencies: react-aria-components (ARIA), next-intl (i18n)
- Placeholder pages: / (home) and /chat
- Directory structure ready for Q3-Q12 components

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE A USAR

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Bash** | Para `npx create-next-app`, `npm install`, `npm run build`, `git commit` | Comandos de terminal |
| **Read** | Antes de reemplazar archivos generados por create-next-app | OBLIGATORIO |
| **Write** | Para reemplazar `tailwind.config.ts`, `layout.tsx`, `globals.css`, `page.tsx` | Archivos nuevos/reemplazo completo |
| **Glob** | Para verificar estructura del proyecto despues del scaffold | Ej: `clara-web/src/**/*.tsx` |
| **Task** | Para lanzar agentes de verificacion paralelos en Paso 7 | `subagent_type="Bash"` |

## RESTRICCIONES ABSOLUTAS

1. **NO modifiques** nada fuera de `clara-web/` — el backend en `src/` es territorio separado
2. **NO cambies** la paleta de colores — esta validada para WCAG AAA y daltonismo
3. **NO cambies** las fuentes — Atkinson Hyperlegible es critica para baja vision
4. **NO uses** `user-scalable=no` ni `maximum-scale=1` — los usuarios NECESITAN hacer zoom
5. **NO instales** librerias de UI adicionales (no shadcn, no chakra) — usamos React Aria Components (headless)
6. **NO crees** componentes UI todavia — eso es Q3. Solo estructura y configuracion
7. **Los tamanos de fuente y touch targets son sagrados** — estan basados en investigacion medica (PMC) y el Braille Institute
8. **SIEMPRE** lee un archivo antes de reemplazarlo con Write

## DEFINICION DE TERMINADO

- [ ] `clara-web/` creado con Next.js 14, TypeScript, Tailwind, App Router, src dir
- [ ] `react-aria-components` y `next-intl` instalados como dependencias
- [ ] `tailwind.config.ts` con paleta Clara completa (11 colores) + 6 font sizes + 3 touch targets + bubble radius
- [ ] `layout.tsx` con Atkinson Hyperlegible + Inter fonts, skip link, ARIA landmarks, viewport accesible
- [ ] `globals.css` con focus-visible, prefers-reduced-motion, 70ch max-width, smooth scroll condicional
- [ ] `page.tsx` con placeholder mostrando titulo + tagline + paleta
- [ ] `chat/page.tsx` con placeholder
- [ ] Directorios `components/ui/`, `lib/`, `messages/`, `public/icons/` creados
- [ ] `npm run build` exitoso sin errores
- [ ] `npx tsc --noEmit` sin errores de tipos
- [ ] Commit con mensaje descriptivo

---

> **Siguiente paso despues de Q2:** El prompt Q3 creara los 4 componentes base (Button, ChatBubble, LanguageSelector, LoadingState) dentro de `clara-web/src/components/ui/`.
