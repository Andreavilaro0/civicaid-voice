# Q4: Pantalla de Bienvenida — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q3 (Componentes Base) debe estar completado. Verifica que existen `Button.tsx`, `LanguageSelector.tsx` en `clara-web/src/components/ui/`.
> **Tiempo estimado:** 15-20 min

---

## PROMPT

### ROL Y FILOSOFIA DE DISENO

Eres un **ingeniero frontend senior, disenador de interaccion Y director de arte** para la primera pantalla que un usuario vulnerable vera en su vida al usar esta app. Esta no es "una landing page" — es una **puerta de entrada a un sistema que fue construido para ellos**. Es la primera impresion. Es el momento donde Maria (74 anos, manos temblorosas) decide si confiar o cerrar la app. Donde Ahmed (28, senegales, primer contacto con burocracia espanola) decide si este sistema lo incluye. Donde Fatima (45, marroqui, desconfianza de lo digital) decide si esto es diferente de todo lo que la ha excluido antes.

Tu trabajo sigue la filosofia de diseno **"Civic Tenderness"**:

> *Civic Tenderness es el arte de la calidez institucional hecha visible. Cada composicion debe aparecer como si un maestro artesano hubiera pasado horas deliberando si una esquina debe ser redondeada doce grados o dieciseis — porque en esta filosofia, esa diferencia es la diferencia entre exclusion y abrazo. El espacio no esta vacio — respira. La generosidad del margen es comunicacion. El elemento mas importante ocupa el espacio mas generoso.*

**Usuarios objetivo — esta pantalla es su PRIMERA interaccion:**

| Persona | Edad | Contexto | Lo que necesita de esta pantalla |
|---------|------|----------|----------------------------------|
| **Maria** | 74 | Espanola, baja alfabetizacion digital, temblor leve | Debe entender EN 3 SEGUNDOS que hacer. Botones ENORMES. Texto simple. Sin opciones confusas |
| **Ahmed** | 28 | Senegales en Espana, habla frances | Debe ver INMEDIATAMENTE que puede usar frances. El selector de idioma es visible sin scroll |
| **Fatima** | 45 | Marroqui, frances/arabe, desconfianza digital | Debe sentir CALIDEZ, no formalidad burocratica. Texto humano, no institucional. Iconos claros |

### SKILLS OBLIGATORIAS

Invoca estas skills en el orden que las necesites:

**Capa de Diseno (invoca ANTES de escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/frontend-design` | Layout, spacing, visual hierarchy, responsive breakpoints | Al planificar la estructura de la pagina |
| `/top-design` | Proporciones, ritmo vertical, respiracion, centro de gravedad visual | Al definir el flujo visual logo→tagline→CTA |
| `/ux-heuristics` | Validar usabilidad (Nielsen's 10 heuristics) | Al revisar la pagina terminada |
| `/refactoring-ui` | Jerarquia de botones, peso visual, enfasis/de-enfasis | Al distinguir CTA primario vs secundario |
| `/design-trends-2026` | Patrones modernos de welcome/onboarding accesible | Como referencia de estado del arte |
| `/web-typography` | Escala tipografica hero, tagline, body — ritmo vertical | Al definir tamanos y spacing de texto |
| `/brand-guidelines` | Primera impresion = impresion de marca. Consistencia absoluta | Al validar cada eleccion visual |

**Capa de Ingenieria (invoca AL escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/react-expert` | Composicion, estado, props, children | Al implementar la pagina |
| `/frontend-developer` | Responsive, Tailwind, accesibilidad HTML, semantic markup | Al implementar estilos y estructura |
| `/nextjs-developer` | App Router, metadata, page.tsx, client/server boundaries | Al estructurar la pagina Next.js |
| `/typescript-pro` | Tipado de content map, router, lang | Al tipar la logica de idioma |

**Capa de Verificacion (invoca DESPUES del codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/verification-before-completion` | Checklist final antes del commit | Al terminar todo |
| `/lighthouse-audit` | Validar accesibilidad, performance, SEO | Post-build |
| `/design-everyday-things` | Validar que un usuario nuevo entiende la pagina SIN instrucciones | Review final |

### ESTRATEGIA MULTI-AGENTE

```
FASE 1 — Investigacion de contexto (paralelo):
  Agente A (Explore): Lee design/02-FRONTEND-ACCESIBLE.md → wireframe 3A (Pantalla de Bienvenida), specs
  Agente B (Explore): Lee design/01-BRAND-STRATEGY.md → personalidad, tono saludo, anti-patrones
  Agente C (Explore): Lee design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md → filosofia visual
  Agente D (Explore): Lee clara-web/src/components/ui/Button.tsx + LanguageSelector.tsx → API de los componentes Q3

FASE 2 — Implementacion (secuencial):
  Tu (principal):
    1. Crear iconos SVG (mic, keyboard)
    2. Implementar WelcomePage con composicion vertical
    3. Responsive review (320px, 768px, 1440px)

FASE 3 — Verificacion (paralelo):
  Agente E (Bash): npm run build
  Agente F (Bash): npx tsc --noEmit
```

---

### CONTEXTO TECNICO

**Clara** ya tiene el scaffolding Next.js (Q2) y los componentes base (Q3). Estos recursos ya existen:

#### Componentes disponibles de Q3:

**Button** (`clara-web/src/components/ui/Button.tsx`):
```typescript
interface ButtonProps extends AriaButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  icon?: React.ReactNode;
  fullWidth?: boolean;
}
// Uso: <Button variant="primary" fullWidth icon={<Icon />} onPress={handler}>Label</Button>
```

**LanguageSelector** (`clara-web/src/components/ui/LanguageSelector.tsx`):
```typescript
interface LanguageSelectorProps {
  defaultLang?: "es" | "fr";
  onChange?: (lang: "es" | "fr") => void;
}
// Uso: <LanguageSelector defaultLang="es" onChange={setLang} />
```

#### Tokens Tailwind disponibles (de `clara-web/tailwind.config.ts`):

**Colores:**
```
clara-blue: #1B5E7B     (Confianza — headers, botones primarios)
clara-orange: #D46A1E   (Calidez — CTAs, acentos)
clara-green: #2E7D4F    (Esperanza — exito, confirmaciones)
clara-bg: #FAFAFA        (Fondo — calma)
clara-text: #1A1A2E      (Texto — 16.8:1 contraste)
clara-text-secondary: #4A4A5A  (Texto auxiliar — 9.1:1)
clara-info: #E3F2FD      (Info — fondos suaves)
clara-border: #E0E0E0   (Bordes)
```

**Tipografia:**
```
font-display: Atkinson Hyperlegible (titulos, tagline, nombres)
font-body: Inter (cuerpo, botones, descripciones)
```

**Tamanos de texto:**
```
text-h1: 36px/1.3    text-h2: 28px/1.3
text-body: 20px/1.6   text-body-sm: 18px/1.6
text-button: 20px/1.0  text-label: 16px/1.4
```

**Touch targets:**
```
touch: 64px    touch-sm: 48px    touch-lg: 96px
```

**Radius:** `rounded-bubble: 16px`, `rounded-xl: 12px`

---

### PRINCIPIOS DE DISENO PARA ESTA PANTALLA

Esta es la pantalla mas importante de toda la app. No porque sea la mas compleja, sino porque es la unica que TODOS los usuarios veran. Los principios:

**1. La regla de los 3 segundos:**
Maria llega a esta pantalla. En 3 segundos debe entender: (a) que es Clara, (b) que puede hacer, (c) como empezar. Si en 3 segundos no lo entiende, cierra la app y pierde acceso a ayuda que necesita. Cada elemento visual debe pasar el test: "contribuye a los 3 segundos o es ruido?"

**2. Centro de gravedad visual — el CTA:**
El ojo recorre la pagina de arriba a abajo. Logo → tagline → descripcion → idioma → **EMPEZAR**. El boton primario es el destino final del recorrido visual. Todo lo anterior es contexto; el boton es la accion. Debe ser el elemento con mayor peso visual (tamano + color + posicion).

**3. Jerarquia por tamano, no por cantidad:**
No necesitamos 10 opciones. Necesitamos 2 caminos claros:
- **"Empezar a hablar"** — para quien quiere voz (primario, grande, azul, con icono mic)
- **"Prefiero escribir"** — para quien prefiere texto (secundario, mas discreto, outline)
La diferencia de tamano entre ambos botones (72px vs 56px) comunica jerarquia sin necesidad de leer.

**4. El idioma es visible SIN scroll:**
Ahmed abre la app. Si tiene que hacer scroll para encontrar "Francais", podria pensar que la app solo funciona en espanol y cerrarla. El LanguageSelector debe estar visible en la viewport inicial (above the fold) en TODOS los dispositivos, incluido un telefono de 320px.

**5. Espacio = respeto:**
Un fondo limpio (#FAFAFA), margenes amplios, elementos separados con respiracion. Civic Tenderness: "Vast fields of soft, nearly-white ground establish a canvas of calm against which concentrated chromatic moments emerge with the quiet authority of lighthouses."

---

## EJECUCION PASO A PASO

### PASO 0: Investigar antes de crear

**Lanza CUATRO agentes Explore en paralelo:**

**Agente A:** Lee `design/02-FRONTEND-ACCESIBLE.md` — extrae el wireframe 3A (Pantalla de Bienvenida), specs de tamano (logo 120px, tagline 28px, boton 72px/56px, selector 64x48px).

**Agente B:** Lee `design/01-BRAND-STRATEGY.md` — extrae personalidad de Clara (cercana, paciente, respetuosa), tono de saludo ("Hola, soy Clara. Estoy aqui para ayudarte..."), anti-patrones ("no infantilizar", "no asumir nivel educativo").

**Agente C:** Lee `design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md` — interioriza la filosofia visual completa.

**Agente D:** Lee `clara-web/src/components/ui/Button.tsx` y `clara-web/src/components/ui/LanguageSelector.tsx` — extrae la interfaz exacta de props para usarlos correctamente.

---

### PASO 1: Crear iconos SVG — "El lenguaje visual mas universal"

**Skills activas:** `/frontend-design` + `/brand-guidelines`

**Briefing de diseno:**
- Los iconos SIEMPRE van acompanados de texto (regla de accesibilidad + cultural de Clara)
- Aqui son decorativos (`aria-hidden="true"`) porque el texto del boton ya comunica la accion
- Estilo: filled (no outline) para maximo reconocimiento a distancia
- Tamano: viewBox 24x24, se renderizan a 28x28 en el boton
- Color: `currentColor` — heredan del boton (blanco en primary, oscuro en secondary)
- Son SVG estaticos en `/public/icons/` — no necesitan ser componentes React

**Wireframe:**
```
  [mic.svg]      [keyboard.svg]

   ┌──┐             ┌──────┐
   │()│             │ ┌──┐ │
   │  │             │ │  │ │
   └┤├┘             │ └──┘ │
    ││              └──────┘
    ──
```

Crea `clara-web/public/icons/mic.svg` con **Write**:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
```

Crea `clara-web/public/icons/keyboard.svg` con **Write**:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M20 5H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/></svg>
```

**Decisiones de diseno:**
- `fill="currentColor"` no `fill="#FFFFFF"`: El icono hereda el color del contexto. En boton primario (blanco), en secundario (oscuro). Un unico SVG sirve para ambos.
- `viewBox="0 0 24 24"` con `width/height 28`: Ligeramente mas grande que el estandar 24px para mejorar visibilidad en contexto elderly-first.
- Paths del conjunto Material Design: universalmente reconocidos. Maria conoce el icono de microfono de WhatsApp. Fatima reconoce el teclado de cualquier app.

---

### PASO 2: Implementar pagina de bienvenida — "La puerta de entrada"

**Skills activas:** `/frontend-design` + `/top-design` + `/react-expert` + `/nextjs-developer` + `/web-typography`

**Briefing de diseno:**
Esta pagina es un **eje vertical centrado**. Todo fluye de arriba a abajo, centrado, con respiracion generosa entre secciones. La composicion visual es:

```
          ZONA DE IDENTIDAD
              ┌─────┐
              │  C  │         <- Logo: circulo 120px, azul, "C" blanco
              └─────┘
        "Tu voz tiene poder"  <- Tagline: Atkinson Bold, 36px, azul

    Te ayudo con tramites     <- Descripcion: Inter Regular, 20px, gris
    sociales en Espana.         max 2-3 lineas, max-w-md
    Habla o escribe en          Lenguaje calido, NO burocratico
    tu idioma.

      ZONA DE CONFIGURACION
     [ES Espanol] [FR Francais] <- LanguageSelector de Q3

          ZONA DE ACCION
  ┌───────────────────────────┐
  │  [mic]  EMPEZAR A HABLAR  │ <- Button primary, 72px, fullWidth
  └───────────────────────────┘
  ┌───────────────────────────┐
  │  [kb]   Prefiero escribir │ <- Button secondary, 56px, fullWidth
  └───────────────────────────┘
```

**Ritmo vertical (spacing):**
```
top padding:     py-12 (48px) — espacio para respirar, la app no "empieza" abruptamente
logo → tagline:  mb-6 (24px) — relacion cercana, identidad unitaria
tagline → desc:  mb-4 (16px) — flujo narrativo: "quien soy" → "que hago"
desc → lang:     mb-8 (32px) — separacion de zona: de "leer" a "configurar"
lang → CTAs:     mb-10 (40px) — pausa antes de la accion. Respiracion Civic Tenderness
CTA1 → CTA2:    space-y-4 (16px) — unidos visualmente como grupo, separados para touch
```

**Wireframe completo (mobile 375px):**
```
┌─────────────────────────────────────┐
│              px-6 (24px sides)      │
│                                     │
│              ┌───────┐              │
│              │       │              │
│              │   C   │  120x120     │
│              │       │  bg-clara-blue│
│              └───────┘  rounded-full│
│                                     │
│       "Tu voz tiene poder"          │
│        font-display bold            │
│        text-h1 (36px)               │
│        text-clara-blue              │
│        text-center                  │
│                                     │
│    Te ayudo con tramites sociales   │
│    en Espana. Habla o escribe en    │
│    tu idioma.                       │
│        text-body (20px)             │
│        text-clara-text-secondary    │
│        text-center max-w-md         │
│                                     │
│     ┌────────┐  ┌────────────┐      │
│     │ES      │  │FR Francais │      │
│     │Espanol │  │            │      │
│     └────────┘  └────────────┘      │
│                                     │
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │  [mic] EMPEZAR A HABLAR    │ 72px│
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  [kb]  Prefiero escribir   │ 56px│
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

Reemplaza `clara-web/src/app/page.tsx` con **Write**:

```typescript
"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Button from "@/components/ui/Button";
import LanguageSelector from "@/components/ui/LanguageSelector";
import Image from "next/image";

/* ------------------------------------------------------------------ */
/*  Content map: cada idioma tiene su set de textos.                  */
/*  Estructura tipada para que TS avise si falta una key.             */
/* ------------------------------------------------------------------ */
type Lang = "es" | "fr";

interface WelcomeContent {
  tagline: string;
  description: string;
  cta_voice: string;
  cta_text: string;
}

const content: Record<Lang, WelcomeContent> = {
  es: {
    tagline: "Tu voz tiene poder",
    description:
      "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
    cta_voice: "Empezar a hablar",
    cta_text: "Prefiero escribir",
  },
  fr: {
    tagline: "Ta voix a du pouvoir",
    description:
      "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
    cta_voice: "Commencer a parler",
    cta_text: "Je prefere ecrire",
  },
};

/* ------------------------------------------------------------------ */
/*  WelcomePage — la primera pantalla que el usuario ve                */
/* ------------------------------------------------------------------ */
export default function WelcomePage() {
  const router = useRouter();
  const [lang, setLang] = useState<Lang>("es");

  const t = content[lang];

  function goToChat(mode: "voice" | "text") {
    router.push(`/chat?lang=${lang}&mode=${mode}`);
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
      {/* ---- ZONA DE IDENTIDAD ---- */}

      {/* Logo placeholder — circulo 120px con "C" */}
      <div
        className="w-[120px] h-[120px] bg-clara-blue rounded-full flex items-center justify-center mb-6"
        role="img"
        aria-label="Logo de Clara"
      >
        <span className="text-white font-display font-bold text-[48px] leading-none select-none">
          C
        </span>
      </div>

      {/* Tagline — lo primero que se lee */}
      <h1 className="font-display font-bold text-h1 text-clara-blue text-center mb-4">
        {t.tagline}
      </h1>

      {/* Descripcion — calida, directa, sin jerga */}
      <p className="text-body text-clara-text-secondary text-center max-w-md mb-8 leading-relaxed">
        {t.description}
      </p>

      {/* ---- ZONA DE CONFIGURACION ---- */}

      {/* Selector de idioma — visible sin scroll */}
      <div className="mb-10">
        <LanguageSelector defaultLang={lang} onChange={setLang} />
      </div>

      {/* ---- ZONA DE ACCION ---- */}

      <div className="w-full max-w-md space-y-4">
        {/* CTA primario — "Empezar a hablar" */}
        <Button
          variant="primary"
          fullWidth
          onPress={() => goToChat("voice")}
          aria-label={t.cta_voice}
          icon={
            <Image
              src="/icons/mic.svg"
              alt=""
              width={28}
              height={28}
              aria-hidden="true"
            />
          }
          className="h-[72px] text-[22px]"
        >
          {t.cta_voice}
        </Button>

        {/* CTA secundario — "Prefiero escribir" */}
        <Button
          variant="secondary"
          fullWidth
          onPress={() => goToChat("text")}
          aria-label={t.cta_text}
          icon={
            <Image
              src="/icons/keyboard.svg"
              alt=""
              width={28}
              height={28}
              aria-hidden="true"
            />
          }
          className="h-[56px]"
        >
          {t.cta_text}
        </Button>
      </div>
    </main>
  );
}
```

**Decisiones de diseno a validar con `/ux-heuristics` + `/top-design` + `/refactoring-ui`:**

| Decision | Razon | Heuristica |
|----------|-------|------------|
| `<main>` en vez de `<div>` | Landmark semantico. Screen readers anuncian "main region". Estructura ARIA correcta | Nielsen #4: Consistency and standards |
| `role="img"` en logo | El circulo con "C" es una imagen semantica, no decoracion. Screen readers leen "Logo de Clara" | Nielsen #1: Visibility of system status |
| Logo 120x120px, no mas grande | Proporcion con pantalla movil 375px: ocupa ~32% del ancho. Prominente sin dominar. El CTA es el destino visual, no el logo | Top design: centro de gravedad |
| `text-[48px]` en "C" | Proporcion aurea respecto al circulo de 120px. La letra llena el espacio sin tocar bordes | Typography: optical sizing |
| Tagline en `text-h1` (36px) Atkinson Bold | Es el headline de la pagina. Atkinson Hyperlegible Bold garantiza legibilidad maxima. Azul refuerza identidad | Brand: font-display para titulos |
| Descripcion en `text-body` (20px) Inter | Cuerpo de texto. Inter es la fuente de lectura. 20px supera el minimo 18px para mayores | Typography: body vs display |
| `max-w-md` en descripcion | Limita a ~28rem ≈ 448px ≈ ~55 caracteres por linea. Debajo del optimo 70ch pero correcto para texto centrado corto | Typography: line-length |
| `leading-relaxed` (1.625) en descripcion | Interlineado generoso para lectura comoda. Supera el minimo WCAG 1.5 | WCAG 1.4.12 |
| `mb-6` → `mb-4` → `mb-8` → `mb-10` | Ritmo vertical progresivo. Espaciado crece hacia abajo, creando "gravedad" que guia al CTA | Top design: vertical rhythm |
| `h-[72px]` en CTA primario | 72px > 64px (touch target). 8px extra de generosidad. Maria puede tocarlo con el pulgar entero | Civic Tenderness: generosity |
| `h-[56px]` en CTA secundario | 56px > 48px (touch-sm). Suficiente para tocar bien, pero visualmente subordinado al primario | Refactoring UI: de-emphasis |
| `text-[22px]` en CTA primario | 2px mas que `text-button` (20px). El boton principal tiene mayor peso tipografico | Refactoring UI: visual weight |
| `space-y-4` (16px) entre CTAs | Suficiente separacion para evitar toques accidentales (>8px minimo WCAG) pero lo bastante juntos para leer como grupo | WCAG 2.5.8 + Gestalt: proximity |
| Contenido i18n como `Record<Lang, WelcomeContent>` | Tipado estricto. Si se agrega un idioma, TS obliga a agregar TODOS los textos. Sin keys faltantes | TypeScript: exhaustive types |
| `router.push(\`/chat?lang=${lang}&mode=${mode}\`)` | La ruta incluye idioma y modo. El chat page sabe como arrancar sin re-preguntar. Sin friction | UX: reduce clicks to goal |

---

### PASO 3: Verificacion responsive — "Funciona en el telefono de Maria"

**Skill activa:** `/frontend-developer` + `/lighthouse-audit`

Run: `cd clara-web && npm run dev`

Abre `http://localhost:3000` y verifica en estos breakpoints:

**320px (telefono viejo, min width):**
```
Verificar:
- [ ] Todo el contenido visible sin scroll horizontal
- [ ] Logo, tagline, descripcion, selector idioma, AMBOS botones visibles sin scroll vertical
- [ ] Botones no se salen del viewport
- [ ] Texto no se trunca
- [ ] Padding lateral 24px (px-6) suficiente
```

**375px (iPhone SE / telefono comun Maria):**
```
Verificar:
- [ ] Composicion centrada y equilibrada
- [ ] Selector idioma y botones "above the fold" (Ahmed ve "Francais" sin scroll)
- [ ] 72px del CTA primario se siente grande y confiable
- [ ] Diferencia de tamano entre botones es clara
```

**768px (tablet):**
```
Verificar:
- [ ] max-w-md limita el ancho — no se estira a toda la pantalla
- [ ] Centrado vertical (justify-center) funciona bien con mas espacio
- [ ] Proporciones se mantienen elegantes
```

**1440px (desktop):**
```
Verificar:
- [ ] La pagina sigue centrada, no "flota" perdida en espacio enorme
- [ ] min-h-screen centrado verticalmente
- [ ] max-w-md mantiene el contenido acotado
```

**Prueba de idioma:**
```
- [ ] Seleccionar FR: tagline, descripcion, y AMBOS botones cambian a frances
- [ ] Seleccionar ES de vuelta: todo vuelve a espanol
- [ ] El estado de LanguageSelector (visual) coincide con el idioma mostrado
```

---

### PASO 4: Verificar build y tipos (agentes paralelos)

**Skill activa:** `/verification-before-completion`

**Lanza DOS comandos en paralelo (Task tool, subagent_type="Bash"):**

**Comando 1 — Build:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npm run build
```

**Comando 2 — Type check:**
```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npx tsc --noEmit
```

**Errores comunes y soluciones:**

| Error | Causa | Solucion |
|-------|-------|----------|
| `Cannot find module '@/components/ui/Button'` | Q3 no se completo | Verifica que `clara-web/src/components/ui/Button.tsx` existe |
| `Module not found: Can't resolve 'next/navigation'` | Next.js no instalado | Corre `npm install` en `clara-web/` |
| `Type 'string' is not assignable to type 'Lang'` | useState sin tipar | Asegurar `useState<Lang>("es")` |
| `Image component not working with SVG` | Next.js Image config | Agregar `dangerouslyAllowSVG: true` a `next.config.ts` o usar `<img>` en vez de `<Image>` para SVGs locales |

**Si el Image component da problemas con SVGs**, reemplaza `<Image>` por `<img>` (los SVGs son estaticos locales, no necesitan optimizacion de Next.js):
```typescript
// En vez de:
<Image src="/icons/mic.svg" alt="" width={28} height={28} aria-hidden="true" />
// Usar:
<img src="/icons/mic.svg" alt="" width={28} height={28} aria-hidden="true" />
```

---

### PASO 5: Review de diseno integral

**Skill activa:** `/ux-heuristics` + `/design-everyday-things` + `/brand-guidelines`

**Heuristica de Nielsen aplicada a la Pantalla de Bienvenida:**

| # | Heuristica | Como se cumple | Evidencia |
|---|-----------|----------------|-----------|
| 1 | Visibility of system status | Idioma seleccionado visualmente claro (triple indicador), boton pressed state | LanguageSelector `aria-checked`, Button `pressed:` |
| 2 | Match between system and real world | "Tu voz tiene poder" — lenguaje humano, no tecnico. "Tramites sociales" — vocabulario que Maria usa | Textos en `content` object |
| 3 | User control and freedom | Puede cambiar idioma libremente. Dos opciones (voz/texto), no una obligada | LanguageSelector + 2 CTAs |
| 4 | Consistency and standards | Usa componentes Q3 (misma visual en toda la app). Patron welcome universal | Button + LanguageSelector reutilizados |
| 5 | Error prevention | Solo 2 idiomas validos (TS). Solo 2 modos validos. No hay input libre que pueda fallar | TypeScript `Lang`, `"voice" | "text"` |
| 6 | Recognition rather than recall | Opciones visibles, no ocultas en menus. Iconos + texto en cada boton | Mic icon + "Empezar a hablar" |
| 7 | Flexibility and efficiency | Voice para quien prefiere hablar. Text para quien prefiere escribir. Idioma configurable | 2 CTAs + LanguageSelector |
| 8 | Aesthetic and minimalist design | Solo lo esencial: logo, tagline, descripcion, idioma, 2 acciones. Cero decoracion innecesaria | Composicion vertical limpia |
| 10 | Help and documentation | La descripcion ES la ayuda: "Te ayudo con tramites sociales. Habla o escribe en tu idioma." | Texto de descripcion |

**Test de "3 segundos" (Don Norman, The Design of Everyday Things):**

| Segundo | Que debe entender el usuario | Elemento responsable |
|---------|------------------------------|---------------------|
| 1 | "Esto es Clara" | Logo + nombre implicito en tagline |
| 2 | "Me ayuda con tramites, puedo hablar o escribir" | Descripcion |
| 3 | "Toco el boton grande azul para empezar" | CTA primario (max peso visual) |

**Checklist de accesibilidad (14 puntos):**

**Estructura:**
- [ ] `<main>` como landmark principal
- [ ] `<h1>` unico en la pagina (tagline)
- [ ] Logo con `role="img"` y `aria-label`

**Touch y motor:**
- [ ] CTA primario: 72px alto (supera 64px touch target)
- [ ] CTA secundario: 56px alto (supera 48px touch-sm)
- [ ] Espacio entre CTAs: 16px (supera 8px WCAG 2.5.8)
- [ ] LanguageSelector: 48px min (touch-sm)

**Visual:**
- [ ] Contraste tagline: azul #1B5E7B sobre #FAFAFA = 7.2:1 (AAA)
- [ ] Contraste descripcion: gris #4A4A5A sobre #FAFAFA = 9.1:1 (AAA)
- [ ] Texto minimo: 20px body (supera 18px elderly minimum)
- [ ] Alineacion centrada (coherente con composicion vertical)

**Idioma y cultura:**
- [ ] Selector idioma sin banderas (sensibilidad cultural)
- [ ] Textos ES y FR completos y naturales
- [ ] Tono calido, no burocratico (personalidad Clara)

**Checklist de marca:**
- [ ] Solo colores de paleta Clara
- [ ] Font-display (Atkinson) en tagline, font-body (Inter) en descripcion
- [ ] Formas redondeadas (circulo logo, rounded-xl botones)
- [ ] Iconos acompanados de texto (mic + "Empezar a hablar")

---

### PASO 6: Commit

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && git add clara-web/src/app/page.tsx clara-web/public/icons/
git commit -m "feat: add Welcome page with Civic Tenderness design — first user touchpoint

- WelcomePage: vertical centered composition (logo → tagline → lang → CTAs)
- SVG icons: mic.svg + keyboard.svg (Material Design, currentColor)
- i18n: ES/FR content map with TypeScript exhaustive typing
- CTAs: 'Empezar a hablar' (voice, 72px) + 'Prefiero escribir' (text, 56px)
- Uses Q3 components: Button (React Aria) + LanguageSelector (ARIA radiogroup)
- Responsive: verified 320px → 1440px, above-the-fold on all viewports
- Route: navigates to /chat?lang={lang}&mode={voice|text}
- WCAG AAA: semantic landmarks, 7:1 contrast, 72px touch, screen reader ready
- Design: Civic Tenderness — generous spacing, calm background, warm typography

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Read** | Paso 0 — leer design docs + componentes Q3 | Entender contexto antes de codigo |
| **Write** | Pasos 1-2 — crear SVGs y page.tsx | Archivos nuevos/modificados |
| **Bash** | Paso 3 (dev server) y Paso 4 (build + types) | Verificar visual y compilacion |
| **Glob** | Verificar archivos creados | `clara-web/public/icons/*.svg`, `clara-web/src/app/page.tsx` |
| **Task** | Paso 0 (lectura paralela) y Paso 4 (verificacion paralela) | `subagent_type="Explore"` o `"Bash"` |

## RESTRICCIONES ABSOLUTAS

1. **NO cambies** componentes de Q3 (`Button.tsx`, `LanguageSelector.tsx`, etc.)
2. **NO cambies** `tailwind.config.ts` ni `globals.css` (ya estan correctos de Q2)
3. **NO instales** librerias adicionales — todo lo necesario ya esta
4. **NO agregues** mas idiomas (solo ES/FR en Fase 1)
5. **NO crees** un componente WelcomePage separado — es directamente `page.tsx` (Next.js convention)
6. **NO uses** `useEffect` — no hay side effects en esta pagina
7. **NO uses** fetch ni API calls — esta es una pagina estatica de bienvenida
8. **NO agregues** animaciones al logo o tagline (YAGNI, y `prefers-reduced-motion` las deshabilitaria)
9. **Iconos SIEMPRE con texto** en botones — nunca un icono solo
10. **Los tokens Tailwind son sagrados** — usa los existentes, no inventes hex colors

## DEFINICION DE TERMINADO

- [ ] Los 3 archivos de diseno leidos + 2 componentes Q3 revisados
- [ ] `clara-web/public/icons/mic.svg` — microfono, filled, currentColor
- [ ] `clara-web/public/icons/keyboard.svg` — teclado, filled, currentColor
- [ ] `clara-web/src/app/page.tsx` — WelcomePage con logo, tagline, descripcion, LanguageSelector, 2 CTAs
- [ ] Cambiar a FR cambia TODOS los textos (tagline, descripcion, ambos botones)
- [ ] CTA "Empezar a hablar" navega a `/chat?lang=es&mode=voice`
- [ ] CTA "Prefiero escribir" navega a `/chat?lang=es&mode=text`
- [ ] Responsive: 320px, 375px, 768px, 1440px — todo visible, nada se rompe
- [ ] Selector idioma + ambos CTAs "above the fold" en 320px
- [ ] `npm run build` exitoso
- [ ] `npx tsc --noEmit` sin errores
- [ ] Checklist Nielsen (9 heuristicas) verificado
- [ ] Checklist accesibilidad (14 puntos) verificado
- [ ] Checklist marca (4 puntos) verificado
- [ ] Commit con mensaje descriptivo

---

> **Siguiente:** Q5 creara el Cliente API y Types para conectar frontend con backend.
> **Dependencias:** Esta pagina usa componentes de Q3. La ruta `/chat` que genera sera implementada en Q6.
