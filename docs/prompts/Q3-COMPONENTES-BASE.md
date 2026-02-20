# Q3: Componentes Base UI — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q2 (Scaffolding Next.js) debe estar completado. Verifica que existe `clara-web/src/components/ui/`.
> **Tiempo estimado:** 15-25 min

---

## PROMPT

### ROL Y FILOSOFIA DE DISENO

Eres un **ingeniero frontend senior Y disenador de interaccion** especializado en accesibilidad y sistemas de diseno inclusivos. No eres solo un programador que escribe componentes — eres un artesano que entiende que cada pixel, cada radio de borde, cada tamano de boton es una **decision de diseno que afecta la vida de personas vulnerables**.

Tu trabajo sigue la filosofia de diseno **"Civic Tenderness"**:

> *Civic Tenderness es el arte de la calidez institucional hecha visible. Donde el diseno gubernamental ha hablado historicamente en grids rigidos, esquinas afiladas y autoridad monocromatica, Civic Tenderness introduce la linea curva, el acento calido y el margen generoso. Un boton no es una pequena affordance interactiva — es una declaracion de que la mano que lo busca importa, sin importar su firmeza.*

**Usuarios objetivo — cada decision de UI es PARA ellos:**

| Persona | Edad | Contexto | Lo que necesita de TUS componentes |
|---------|------|----------|-----------------------------------|
| **Maria** | 74 | Espanola, baja alfabetizacion digital, temblor leve en manos | Botones 64px+, contraste 7:1, texto 18px+, touch targets generosos, feedback tactil claro |
| **Ahmed** | 28 | Senegales en Espana, habla frances, primer contacto con burocracia espanola | Labels en ES/FR, sin banderas (sensibilidad cultural), lenguaje simple |
| **Fatima** | 45 | Marroqui, frances/arabe, desconfianza de sistemas digitales | Iconos SIEMPRE con texto, estados claros (activo/inactivo), sin sorpresas visuales |

### SKILLS OBLIGATORIAS

Invoca estas skills en el orden que las necesites:

**Capa de Diseno (invoca ANTES de escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/frontend-design` | Sistema de diseno, tokens, spacing, visual hierarchy | Al planificar cada componente |
| `/top-design` | Principios de diseno de clase mundial (proporcion, ritmo, respiracion) | Al definir spacing y proporciones |
| `/ux-heuristics` | Validar usabilidad (Nielsen's 10 heuristics) | Al revisar cada componente terminado |
| `/refactoring-ui` | Patrones visuales practicos (sombras, bordes, jerarquia) | Al elegir estilos de variantes |
| `/design-trends-2026` | Tendencias actuales en UI accesible | Como referencia de estado del arte |
| `/web-typography` | Reglas tipograficas (kerning, leading, line-length) | Al definir texto en componentes |
| `/brand-guidelines` | Consistencia con identidad visual Clara | Al validar colores y fuentes |

**Capa de Ingenieria (invoca AL escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/react-expert` | Composicion de componentes, props, patterns | Al implementar |
| `/frontend-developer` | CSS, Tailwind, responsive, accesibilidad HTML | Al implementar |
| `/typescript-pro` | Tipado estricto de interfaces y props | Al definir contratos |
| `/react-best-practices` | Patrones React modernos (server vs client, composition) | Al decidir "use client" |

**Capa de Verificacion (invoca DESPUES del codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/verification-before-completion` | Checklist final antes del commit | Al terminar todo |
| `/lighthouse-audit` | Validar accesibilidad y performance | Post-build |
| `/design-everyday-things` | Validar que la UI es intuitiva sin instrucciones | Review final |

### ESTRATEGIA MULTI-AGENTE

```
FASE 1 — Investigacion de diseno (paralelo):
  Agente A (Explore): Lee design/02-FRONTEND-ACCESIBLE.md — wireframes y specs WCAG
  Agente B (Explore): Lee design/01-BRAND-STRATEGY.md — paleta, tipografia, personalidad
  Agente C (Explore): Lee clara-web/tailwind.config.ts + globals.css — tokens disponibles

FASE 2 — Implementacion (secuencial, con rigor de diseno):
  Tu (principal): Crea cada componente pasando por:
    1. Sketch mental (que hace, como se ve, como se siente)
    2. Definir interface TypeScript (contrato de props)
    3. Implementar JSX + Tailwind
    4. Revisar con /ux-heuristics

FASE 3 — Verificacion (paralelo):
  Agente D (Bash): npm run build
  Agente E (Bash): npx tsc --noEmit
```

---

### CONTEXTO TECNICO

**Clara** ya tiene el scaffolding Next.js de Q2. Estos tokens y configuraciones ya existen:

#### Tokens Tailwind disponibles (de `clara-web/tailwind.config.ts`):

**Colores:**
```
clara-blue: #1B5E7B     (Confianza — headers, botones primarios, links)
clara-orange: #D46A1E   (Calidez — CTAs, acentos, estados activos)
clara-green: #2E7D4F    (Esperanza — exito, confirmaciones)
clara-bg: #FAFAFA        (Fondo — calma, sin agresion)
clara-text: #1A1A2E      (Texto — alto contraste 16.8:1)
clara-text-secondary: #4A4A5A  (Texto auxiliar — 9.1:1)
clara-error: #C62828     (Error — rojo accesible)
clara-warning: #F9A825   (Aviso — ambar)
clara-info: #E3F2FD      (Info — fondo burbujas Clara)
clara-card: #F5F5F5      (Cards — fondo tarjetas)
clara-border: #E0E0E0   (Bordes — separadores suaves)
```

**Tipografia:**
```
font-display: Atkinson Hyperlegible (Braille Institute — titulos, labels importantes)
font-body: Inter (optimizada pantallas — cuerpo, botones)
```

**Tamanos de texto:**
```
text-h1: 36px/1.3    text-h2: 28px/1.3
text-body: 20px/1.6   text-body-sm: 18px/1.6
text-button: 20px/1.0  text-label: 16px/1.4
```

**Touch targets:**
```
touch: 64px (primarios — Maria necesita esto)
touch-sm: 48px (secundarios)
touch-lg: 96px (microfono — boton principal)
```

**Radius:** `rounded-bubble: 16px`

#### Dependencia disponible:
- `react-aria-components` — componentes headless con ARIA completo. Usala para Button.

#### CSS global activo (de `globals.css`):
- `focus-visible`: outline 3px azul con offset 2px (global)
- `prefers-reduced-motion`: animaciones desactivadas
- `max-width: 70ch` en parrafos

---

### PRINCIPIOS DE DISENO PARA ESTOS COMPONENTES

Antes de escribir una linea de codigo, interioriza estos principios:

**1. La generosidad es comunicacion:**
Un boton de 64px no es "grande" — es respetuoso. El espacio no esta vacio — respira. El padding no es excesivo — es amable. Cada milimetro extra de touch target es una mano menos frustrada.

**2. El color conversa, no grita:**
Azul (#1B5E7B) dice "confio en ti". Naranja (#D46A1E) dice "estoy aqui para ti". Verde (#2E7D4F) dice "lo lograste". Nunca compiten. Las burbujas de Clara son azul claro (#E3F2FD) — como una nota en papel suave. Las del usuario son azul oscuro — como una voz firme.

**3. Los estados son honestos:**
Activo/inactivo debe ser OBVIO sin depender del color (regla daltonismo). Usa borde + fondo + peso de texto juntos. Un loading state dice EXACTAMENTE que esta pasando ("Clara esta buscando..."), no un spinner generico.

**4. La accesibilidad no es un feature — es el material:**
No "agregamos" accesibilidad despues. Los componentes NACEN accesibles. `role`, `aria-label`, `aria-live`, `aria-checked` no son extras — son el esqueleto.

---

## EJECUCION PASO A PASO

### PASO 0: Investigar antes de crear

**Lanza TRES agentes Explore en paralelo:**

**Agente A:** Lee `design/02-FRONTEND-ACCESIBLE.md` — extracto los wireframes, specs de tamano, patrones de interaccion.

**Agente B:** Lee `design/01-BRAND-STRATEGY.md` — extrae personalidad de marca, sensibilidad cultural, anti-patrones ("nunca banderas", "nunca infantilizar").

**Agente C:** Lee `clara-web/tailwind.config.ts`, `clara-web/src/app/globals.css`, `clara-web/package.json` — confirma que los tokens existen y react-aria-components esta instalado.

Luego lee tu mismo:
```
Read: design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md
```
Esta es la filosofia visual que guia TODAS las decisiones de diseno de Clara. Leela. Internalizala.

---

### PASO 1: Button.tsx — "Una declaracion de que la mano importa"

**Skills activas:** `/frontend-design` + `/react-expert` + `/refactoring-ui`

**Briefing de diseno:**
- Es el componente mas usado de toda la app
- Maria (74) va a tocarlo con un dedo que tiembla — debe ser GRANDE (64px minimo)
- 3 variantes: `primary` (accion principal, azul), `secondary` (alternativa, outline), `ghost` (terciaria, transparente)
- Acepta icono + texto. El icono es SIEMPRE decorativo (`aria-hidden`). El texto es la etiqueta.
- Hover: sutil oscurecimiento. Pressed: feedback tactil inmediato (cambio de color mas profundo).
- Disabled: opacity 50%, cursor not-allowed. Pero nunca dejes un boton disabled sin explicar por que.

**Wireframe:**
```
Primary:    ┌─────────────────────────────────┐
            │  [icon]   EMPEZAR A HABLAR      │  64px min, bg-clara-blue, text white
            └─────────────────────────────────┘

Secondary:  ┌─────────────────────────────────┐
            │  [icon]   Prefiero escribir      │  64px min, border-2, bg-white
            └─────────────────────────────────┘

Ghost:      ┌─────────────────────────────────┐
            │  [icon]   Cambiar idioma         │  64px min, transparent, text-blue
            └─────────────────────────────────┘
```

Crea `clara-web/src/components/ui/Button.tsx` con **Write**:

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

**Decisiones de diseno a validar con `/ux-heuristics`:**
- `min-h-touch min-w-touch` = 64x64px: Nielsen #7 (Flexibility and efficiency). Touch targets para personas con destreza motora reducida.
- `rounded-xl` (12px): Forma sin agresion (Civic Tenderness). No `rounded-full` (demasiado informal para contexto civico), no `rounded-none` (demasiado institutional).
- `gap-3` (12px) entre icono y texto: Espacio visual suficiente para que el ojo distinga ambos elementos.
- `transition-colors duration-150`: Feedback inmediato pero no abrupto. 150ms es el umbral de percepcion de causalidad directa.
- `pressed:` (React Aria): Feedback tactil inmediato — el color cambia MIENTRAS el dedo toca, no despues.

---

### PASO 2: ChatBubble.tsx — "La conversacion hecha espacio"

**Skills activas:** `/frontend-design` + `/web-typography` + `/top-design`

**Briefing de diseno:**
- Es como Clara "habla" en la interfaz. La burbuja ES su voz visual.
- Clara siempre alineada a la izquierda (como leer un libro). Usuario a la derecha (como responder).
- Clara: fondo azul claro (#E3F2FD), texto oscuro. Calido como una nota escrita a mano.
- Usuario: fondo azul oscuro (#1B5E7B), texto blanco. Firme como una pregunta clara.
- Max 85% del ancho: las burbujas NO llenan el espacio. El margen es respeto — espacio para pensar.
- Clara muestra su nombre arriba: el usuario siempre sabe QUIEN habla (Nielsen #1: Visibility of system status).
- La esquina "puntiaguda" (rounded-bl-sm / rounded-br-sm) indica de DONDE sale el mensaje. Patron WhatsApp que Maria ya conoce.

**Wireframe:**
```
Clara:  ┌─────────────────────────────┐
        │ Clara                       │  <- font-display bold, label, clara-blue
        │                             │
        │ El Ingreso Minimo Vital     │  <- text-body-sm (18px), line-height 1.6
        │ es una prestacion mensual   │
        │ de la Seguridad Social...   │
        │                             │
        │ [contenido adicional]       │  <- children: AudioPlayer, sources, etc.
        │                       14:32 │  <- timestamp, 14px, text-secondary
        └─────────────────────────────┘
        ^ esquina puntiaguda (rounded-bl-sm)

                          Usuario:  ┌─────────────────────┐
                                    │ Que es el IMV?      │  <- bg-clara-blue, white
                                    │               14:33 │
                                    └─────────────────────┘
                                        esquina puntiaguda ^ (rounded-br-sm)
```

Crea `clara-web/src/components/ui/ChatBubble.tsx` con **Write**:

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

**Decisiones de diseno a validar:**
- No `"use client"`: Server Component. Sin estado, sin eventos. Menor bundle, render mas rapido.
- `max-w-[85%]`: Patron conversacional. El espacio vacio a un lado guia el ojo hacia el emisor correcto.
- `rounded-bubble` (16px) + esquina `sm` (4px): Mimetiza la forma de las burbujas de WhatsApp — la interfaz que Maria ya domina.
- `space-y-2` en children: Espaciado vertical automatico para contenido flexible (texto + audio player + fuentes).
- `text-body-sm` (18px): No 16px. 18px es el minimo recomendado para lectura prolongada en mayores de 65 (PMC research).
- El nombre "Clara" en `font-display` (Atkinson Hyperlegible Bold): Identidad visual consistente. El usuario siempre sabe quien habla.
- Timestamp en 14px: Informacion terciaria. Presente pero nunca compite con el contenido.

---

### PASO 3: LanguageSelector.tsx — "Tus derechos, en tu idioma"

**Skills activas:** `/frontend-design` + `/brand-guidelines` + `/ux-heuristics`

**Briefing de diseno:**
- Ahmed necesita cambiar a frances. Fatima necesita ver que HAY opcion de frances.
- NO banderas. Nunca. Las banderas excluyen dialectos, son politicamente cargadas, y asumen que un idioma pertenece a un pais. (Regla de `design/01-BRAND-STRATEGY.md`: "Nunca usar banderas para representar idiomas — usar nombre del idioma en texto")
- Patron ARIA `radiogroup` + `radio`: Semanticamente correcto para seleccion mutuamente excluyente.
- Estado activo MUY claro: borde azul + fondo azul claro + texto azul. Triple indicador (no solo color — daltonismo safe).
- Estado inactivo: borde gris + fondo blanco + texto gris. Visible pero subordinado.

**Wireframe:**
```
  ┌──────────────┐    ┌──────────────┐
  │ ES  Espanol  │    │ FR  Francais │    <- 48px min alto, gap 12px
  └──────────────┘    └──────────────┘
  [ACTIVO:              [INACTIVO:
   borde azul            borde gris
   fondo E3F2FD          fondo blanco
   texto azul]           texto gris]
```

Crea `clara-web/src/components/ui/LanguageSelector.tsx` con **Write**:

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

**Decisiones de diseno a validar:**
- `role="radiogroup"` + `role="radio"` + `aria-checked`: Screen readers anuncian "Seleccionar idioma, grupo de radio, Espanol, seleccionado". Ahmed entiende sin ver la pantalla.
- Triple indicador de estado (borde + fondo + color texto): Daltonismo safe. Si el azul se percibe diferente, el borde grueso + fondo distinto siguen comunicando el estado.
- `min-h-touch-sm` (48px): Target secundario. No necesita 64px porque no es la accion principal.
- Abreviatura `aria-hidden`: El screen reader no lee "ES Espanol" redundante — solo "Espanol".
- Sin banderas: Sensibilidad cultural validada en brand strategy. Un senegales en Espana no se identifica con la bandera francesa.

---

### PASO 4: LoadingState.tsx — "Clara esta aqui, dame un momento"

**Skills activas:** `/frontend-design` + `/design-everyday-things` + `/ux-heuristics`

**Briefing de diseno:**
- El loading NO es un spinner generico. Es Clara comunicando: "estoy trabajando para ti".
- Texto personalizable porque el contexto importa:
  - Procesando audio: "Clara esta escuchando tu mensaje..."
  - Generando respuesta: "Clara esta buscando informacion..."
  - Leyendo documento: "Clara esta leyendo tu documento..."
- 3 puntos animados: patron universal de "alguien esta escribiendo" (WhatsApp, Messenger). Maria lo reconoce.
- `aria-live="polite"`: Cuando este componente aparece, el screen reader anuncia el texto SIN interrumpir al usuario. Fatima que usa VoiceOver escucha "Clara esta buscando informacion" automaticamente.
- Animacion se desactiva con `prefers-reduced-motion` (ya manejado por globals.css).

**Wireframe:**
```
  ┌──────────────────────────────────────────────┐
  │  ● ● ●   Clara esta buscando informacion... │  <- fondo E3F2FD
  └──────────────────────────────────────────────┘
     ^          ^
     puntos     texto descriptivo
     decorativos   (screen reader lee esto)
     (aria-hidden)
```

Crea `clara-web/src/components/ui/LoadingState.tsx` con **Write**:

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

**Decisiones de diseno a validar:**
- `role="status"`: ARIA landmark. Le dice al navegador "este es un mensaje de estado del sistema".
- `aria-live="polite"` (no `"assertive"`): Polite espera a que el screen reader termine lo que esta diciendo. Assertive interrumpe. Para un loading state, polite es correcto — no queremos interrumpir.
- `animate-bounce` con delays 0/150/300ms: Ritmo natural de "escribiendo". 150ms entre cada punto = frecuencia de pulsacion cardiaca relajada.
- `max-w-[85%]`: Mismo ancho que ChatBubble. Consistencia visual — el loading se siente como "Clara preparandose para hablar".
- `bg-clara-info`: Mismo fondo que burbujas Clara. Continuidad cromatica.
- Sin `"use client"`: Server component. Cero JavaScript innecesario.

---

### PASO 5: Verificar build y tipos (agentes paralelos)

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

**Errores comunes:**
- `Cannot find module 'react-aria-components'`: Corre `npm install react-aria-components` en `clara-web/`
- `Property 'pressed' is not recognized`: Es un data-attribute de React Aria, no CSS vanilla. La className se evalua condicionalmente por la libreria. Verifica version >= 1.0.
- `min-h-touch` no reconocido: Verifica que `tailwind.config.ts` tiene `spacing: { touch: "64px" }`. Si no, Q2 no se completo correctamente.

---

### PASO 6: Review de diseno integral

**Skill activa:** `/ux-heuristics` + `/design-everyday-things` + `/brand-guidelines`

Antes del commit, pasa cada componente por estas 3 lentes:

**Heuristica de Nielsen:**

| # | Heuristica | Button | ChatBubble | LangSelector | LoadingState |
|---|-----------|--------|------------|--------------|-------------|
| 1 | Visibility of status | pressed state | sender visible | checked state | message text |
| 2 | Match real world | WhatsApp-like | WhatsApp-like | text labels | "escribiendo" pattern |
| 3 | User control | cancel/disabled | - | change selection | - |
| 4 | Consistency | 3 variants, same size | 2 variants, same width | same border pattern | same bg as bubble |
| 5 | Error prevention | disabled state | - | only 2 valid options | - |
| 7 | Flexibility | icon+text, fullWidth | children flexible | onChange callback | custom message |
| 8 | Aesthetic minimal | no decoracion extra | clean, breathing | solo lo necesario | puntos + texto |

**Checklist de accesibilidad (18 puntos):**

**Button:**
- [ ] min 64x64px touch target
- [ ] 3 variantes con contraste suficiente (primary: blanco/azul 7.2:1)
- [ ] Focus visible 3px azul
- [ ] Disabled state visual (opacity 50%)
- [ ] Icon `aria-hidden` (texto es etiqueta)
- [ ] Keyboard accessible (Enter/Space via React Aria)

**ChatBubble:**
- [ ] Max 85% ancho
- [ ] Clara: fondo claro + texto oscuro (contraste AAA)
- [ ] User: fondo azul + texto blanco (7.2:1)
- [ ] Texto 18px minimo
- [ ] Children flexible para contenido futuro

**LanguageSelector:**
- [ ] `role="radiogroup"` + `aria-label`
- [ ] Cada opcion `role="radio"` + `aria-checked`
- [ ] Sin banderas (sensibilidad cultural)
- [ ] Touch target 48px minimo
- [ ] Triple indicador estado (borde + fondo + texto color)

**LoadingState:**
- [ ] `role="status"` + `aria-live="polite"`
- [ ] Puntos `aria-hidden`
- [ ] Animacion reduced-motion safe
- [ ] Mensaje legible (18px)

**Checklist de marca:**
- [ ] Solo colores de la paleta Clara (no hex arbitrarios excepto hover/pressed states)
- [ ] Font-display para nombres/labels importantes, font-body para contenido
- [ ] Rounded-xl o rounded-bubble (no sharp corners)
- [ ] No iconos sin texto

---

### PASO 7: Commit

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && git add clara-web/src/components/ui/
git commit -m "feat: add 4 accessible UI components following Civic Tenderness design philosophy

- Button: 3 variants (primary/secondary/ghost), 64px min targets, React Aria Components
- ChatBubble: clara/user variants, 85% max width, WhatsApp-style speech tail
- LanguageSelector: ARIA radiogroup ES/FR, triple state indicator, no flags (cultural sensitivity)
- LoadingState: aria-live polite, animated dots, context-specific messages
- Design: Civic Tenderness philosophy — generous spacing, honest states, warm colors
- WCAG AAA: 7:1 contrast, keyboard nav, screen reader, reduced motion, 18px min text
- All tokens from Clara design system (tailwind.config.ts)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Read** | Paso 0 — leer design docs + config | Entender diseno antes de codigo |
| **Write** | Pasos 1-4 — crear componentes | Archivos nuevos en `components/ui/` |
| **Bash** | Paso 5 — build + type check | Verificar compilacion |
| **Glob** | Verificar archivos creados | `clara-web/src/components/ui/*.tsx` |
| **Task** | Paso 0 (lectura) y Paso 5 (verificacion) | `subagent_type="Explore"` o `"Bash"` |

## RESTRICCIONES ABSOLUTAS

1. **NO cambies** archivos fuera de `clara-web/src/components/ui/`
2. **NO instales** librerias adicionales
3. **NO uses** librerias de iconos (se agregan como SVG en Q4)
4. **NO crees** tests unitarios todavia — se agregan con interacciones reales
5. **NO uses** `useEffect` — ninguno lo necesita
6. **NO uses** forwardRef — YAGNI
7. **Los tokens Tailwind son sagrados** — usa los existentes, no inventes
8. **Iconos SIEMPRE con texto** — nunca un icono solo (accesibilidad + cultural)
9. **NO banderas** — nunca, para ningun idioma (sensibilidad cultural)
10. **Lee los archivos de diseno ANTES de escribir codigo** — el diseno guia la ingenieria, no al reves

## DEFINICION DE TERMINADO

- [ ] Los 3 archivos de diseno leidos (02-FRONTEND-ACCESIBLE.md, 01-BRAND-STRATEGY.md, CIVIC-TENDERNESS-PHILOSOPHY.md)
- [ ] `Button.tsx` — 3 variantes, 64px, React Aria, focus, pressed, disabled
- [ ] `ChatBubble.tsx` — clara/user, 85% max, WhatsApp tail, timestamp, children flex
- [ ] `LanguageSelector.tsx` — radiogroup ARIA, ES/FR, sin banderas, triple estado
- [ ] `LoadingState.tsx` — aria-live polite, puntos animados, mensaje personalizable
- [ ] `npm run build` exitoso
- [ ] `npx tsc --noEmit` sin errores
- [ ] Checklist Nielsen (8 heuristicas) verificado
- [ ] Checklist accesibilidad (18 puntos) verificado
- [ ] Checklist marca (4 puntos) verificado
- [ ] Commit con mensaje descriptivo

---

> **Siguiente:** Q4 creara la Pantalla de Bienvenida usando Button y LanguageSelector.
> **Dependencias futuras:** Q4 (Welcome), Q6 (Chat), Q7 (Voice), Q8 (Audio), Q9 (Upload) usan estos componentes.
