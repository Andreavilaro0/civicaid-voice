# Q6: Interfaz de Chat — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q3 (Componentes Base), Q4 (Bienvenida) y Q5 (API Client + Types) deben estar completados. Verifica que existen `clara-web/src/lib/api.ts`, `clara-web/src/lib/types.ts`, `clara-web/src/components/ui/ChatBubble.tsx`.
> **Tiempo estimado:** 25-35 min

---

## PROMPT

### ROL

Eres un **ingeniero frontend senior, disenador de interaccion Y arquitecto de conversaciones** construyendo la pantalla mas importante de toda la aplicacion: el chat donde Clara habla con personas vulnerables.

Esta NO es "otra pantalla de chat". Es el **unico lugar donde una persona de 74 anos con temblor en las manos va a descubrir que tiene derecho a 500€/mes de ayuda que no sabia que existia**. Es donde un inmigrante senegales de 28 anos va a entender en frances como empadronarse en Espana. Es donde una mujer marroqui de 45 anos va a sentir, quizas por primera vez, que un sistema digital fue construido para ella.

Cada burbuja que aparece, cada animacion de carga, cada mensaje de error — todo comunica: "estamos aqui, te escuchamos, esto es para ti."

Tu trabajo sigue la filosofia de diseno **"Civic Tenderness"**:

> *La comunicacion es "ondas concentricas de una voz que finalmente es escuchada". El espacio respira. La quietud es poder. Cada elemento lleva el peso de la necesidad — construido, al final, para la persona.*

**Usuarios objetivo — el chat es su UNICO canal de ayuda:**

| Persona | Edad | Contexto | Lo que necesita del CHAT |
|---------|------|----------|--------------------------|
| **Maria** | 74 | Espanola, baja alfabetizacion digital, temblor leve | Burbujas grandes y legibles. Texto 18px+. Auto-scroll suave. Input con boton de enviar VISIBLE (no solo Enter). Loading que diga QUE pasa, no spinner generico |
| **Ahmed** | 28 | Senegales en Espana, habla frances | Respuestas en frances. Selector de idioma accesible. Fuentes citadas con links. Error messages en su idioma |
| **Fatima** | 45 | Marroqui, frances/arabe, desconfianza digital | Saber SIEMPRE quien habla (Clara vs yo). Loading honesto ("buscando informacion..."). Errores que sugieren accion, no codigos |

### SKILLS OBLIGATORIAS

**Capa de Diseno (invoca ANTES de escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/frontend-design` | Layout de chat, spacing, composicion de burbujas, zona de input | Al planificar estructura de pagina |
| `/top-design` | Ritmo vertical del chat, choreografia de entrada de burbujas, motion design | Al definir animaciones y transiciones |
| `/ux-heuristics` | Validar usabilidad: visibilidad de estado, feedback, consistencia | Al revisar cada componente terminado |
| `/refactoring-ui` | Jerarquia visual: header vs chat vs input, enfasis en lo importante | Al balancear las 3 zonas de pantalla |
| `/web-typography` | Tipografia en burbujas, legibilidad en chat, tamanos de fuente | Al definir texto en mensajes |
| `/brand-guidelines` | Consistencia con identidad Clara, tono conversacional | Al validar colores y copy |
| `/design-everyday-things` | Mapeo natural del modelo mental de "chat" que Maria ya tiene (WhatsApp) | Al decidir patrones de interaccion |

**Capa de Ingenieria (invoca AL escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/react-expert` | Composicion de componentes, custom hooks, manejo de estado | Al implementar useChat y page.tsx |
| `/frontend-developer` | CSS, Tailwind, responsive, sticky positioning, scroll | Al implementar layout y estilos |
| `/nextjs-developer` | App Router, "use client", searchParams, Suspense | Al estructurar la pagina |
| `/typescript-pro` | Tipado estricto, consumo de types.ts, generics | Al tipar useChat y props |
| `/react-best-practices` | Patrones de estado, useCallback, useRef, optimizaciones | Al disenar el hook de chat |

**Capa de Verificacion (invoca DESPUES del codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/verification-before-completion` | Checklist final antes del commit | Al terminar todo |
| `/lighthouse-audit` | Validar accesibilidad y performance | Post-build |
| `/design-everyday-things` | Test de 3 segundos: Maria entiende el chat sin instrucciones? | Review final |

### ESTRATEGIA MULTI-AGENTE

```
FASE 1 — Investigacion (paralelo):
  Agente A (Explore): Lee design/02-FRONTEND-ACCESIBLE.md — wireframe 3B (chat), 3C (voz), interaction patterns
  Agente B (Explore): Lee design/01-BRAND-STRATEGY.md — tono de Clara, anti-patrones, emociones objetivo
  Agente C (Explore): Lee clara-web/src/lib/types.ts + api.ts + constants.ts — contratos Q5
  Agente D (Explore): Lee clara-web/src/components/ui/ChatBubble.tsx + LoadingState.tsx — API de componentes Q3

FASE 2 — Implementacion (secuencial estricto):
  Tu (principal):
    1. useChat.ts (hook central — estado + logica)
    2. Header.tsx (navegacion + idioma)
    3. MessageList.tsx (lista de mensajes + auto-scroll)
    4. ChatInput.tsx (entrada de texto + botones de modo)
    5. chat/page.tsx (composicion de todo)

FASE 3 — Verificacion (paralelo):
  Agente E (Bash): npm run build
  Agente F (Bash): npx tsc --noEmit
```

---

### CONTEXTO TECNICO

**Clara** ya tiene scaffolding (Q2), componentes base (Q3), bienvenida (Q4) y capa de datos (Q5). Estos recursos ya existen:

#### De Q3 — Componentes base:

**ChatBubble** (`clara-web/src/components/ui/ChatBubble.tsx`):
```typescript
interface ChatBubbleProps {
  sender: "clara" | "user";
  children: React.ReactNode;
  timestamp?: string;
}
// Uso:
// <ChatBubble sender="clara" timestamp="14:32">
//   <p>El IMV es...</p>
//   {/* children flexible: texto, audio, fuentes */}
// </ChatBubble>
```
- Clara: fondo `#E3F2FD`, texto oscuro, esquina inferior izquierda puntiaguda, nombre "Clara" en bold
- Usuario: fondo `#1B5E7B`, texto blanco, esquina inferior derecha puntiaguda
- Max 85% ancho, rounded-bubble (16px), texto 18px

**LoadingState** (`clara-web/src/components/ui/LoadingState.tsx`):
```typescript
interface LoadingStateProps {
  message?: string;  // Default: "Clara esta buscando informacion..."
}
// Uso: <LoadingState message="Clara esta escuchando tu mensaje..." />
```
- 3 puntos animados + mensaje descriptivo
- `role="status"` + `aria-live="polite"`
- Mismo fondo y ancho que ChatBubble

**Button** (`clara-web/src/components/ui/Button.tsx`):
```typescript
interface ButtonProps extends AriaButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  icon?: React.ReactNode;
  fullWidth?: boolean;
}
```

#### De Q5 — Capa de datos:

**API client** (`clara-web/src/lib/api.ts`):
```typescript
// Funciones disponibles:
sendMessage(request: ChatRequest): Promise<ChatResponse>
checkHealth(): Promise<HealthResponse>
generateSessionId(): string          // "web_m2k8f_a7x3"
resolveAudioUrl(url: string | null): string | null
getErrorMessage(error: ApiError, lang: Language): { message: string; action: ErrorAction; actionLabel: string }

// Error class:
class ApiError extends Error {
  status: number;
  category: ErrorCategory;      // "network" | "audio" | "server" | "timeout"
  suggestedAction: ErrorAction;  // "retry" | "wait" | "check_connection" | "try_text"
}
```

**Types** (`clara-web/src/lib/types.ts`):
```typescript
type Language = "es" | "fr";
type InputMode = "text" | "voice" | "image";        // concepto UI
type ApiInputType = "text" | "audio" | "image";      // concepto API
type MessageSender = "clara" | "user";
type LoadingContext = "listening" | "thinking" | "reading";
type ErrorCategory = "network" | "audio" | "server" | "timeout";
type ErrorAction = "retry" | "wait" | "check_connection" | "try_text";

interface ChatRequest {
  text: string; language: Language; input_type: ApiInputType;
  audio_base64?: string | null; image_base64?: string | null; session_id: string;
}
interface ChatResponse {
  response: string; audio_url: string | null; source: ResponseSource;
  language: Language; duration_ms: number; sources: Source[];
}
interface AudioPlayback { url: string; duration_s?: number; state: "idle" | "playing" | "paused"; }
interface Message {
  id: string; sender: MessageSender; text: string;
  audio?: AudioPlayback; sources?: Source[]; timestamp: Date;
  loading?: LoadingContext;
  error?: {                    // accion estructurada para errores
    action: ErrorAction;
    actionLabel: string;
  };
}
interface Source { name: string; url: string; }
```

**Constants** (`clara-web/src/lib/constants.ts`):
```typescript
EASING.out  = "cubic-bezier(0.16, 1, 0.3, 1)"   // entrada de burbujas
EASING.in   = "cubic-bezier(0.55, 0, 1, 0.45)"   // salida
EASING.inOut = "cubic-bezier(0.65, 0, 0.35, 1)"  // transformacion

DURATION.instant = 150    // feedback inmediato
DURATION.normal  = 300    // transiciones
DURATION.enter   = 500    // entrada de elementos
DURATION.stagger = 80     // stagger entre burbujas

COLORS.trust  = "#1B5E7B"  // azul
COLORS.warmth = "#D46A1E"  // naranja
COLORS.hope   = "#2E7D4F"  // verde
```

#### De Q4 — Navegacion:
La pantalla de bienvenida navega a `/chat?lang=es` o `/chat?lang=fr` segun la seleccion del usuario. El chat debe leer `lang` de los search params.

#### Tailwind tokens disponibles:
```
Colores: clara-blue, clara-orange, clara-green, clara-bg, clara-text, clara-text-secondary,
         clara-error, clara-warning, clara-info, clara-card, clara-border
Fuentes: font-display (Atkinson Hyperlegible), font-body (Inter)
Texto: text-h1 (36px), text-h2 (28px), text-body (20px), text-body-sm (18px), text-button (20px), text-label (16px)
Touch: touch (64px), touch-sm (48px), touch-lg (96px)
Radius: rounded-bubble (16px)
```

---

### PRINCIPIOS DE DISENO PARA EL CHAT

**1. El modelo mental es WhatsApp, no un chatbot corporativo:**
Maria usa WhatsApp. Ahmed usa WhatsApp. Fatima usa WhatsApp. El chat de Clara debe sentirse como WhatsApp, no como un formulario de soporte tecnico. Burbujas a izquierda/derecha, input abajo, scroll vertical, timestamps discretos. No reinventar el modelo mental mas exitoso de la historia de la comunicacion digital.

**2. Las tres zonas de pantalla tienen jerarquia clara:**
```
+--- HEADER (56px) ---- zona de control ---+
|  [<-] Clara                    [ES v]    |  <- fija, NO scrollea
+------------------------------------------+
|                                          |
|  MESSAGES — zona de conversacion         |  <- scrolleable, flex-1
|  (esto ocupa todo el espacio disponible) |
|                                          |
+------------------------------------------+
|  INPUT — zona de accion                  |  <- fija, sticky bottom
|  [texto...] [enviar]                     |
|  [Escribir] [Voz] [Foto]                |
+------------------------------------------+
```
Header + Input son fijos. Messages scrollea entre ellos. Es el patron de TODAS las apps de chat. No innovar aqui.

**3. Loading states son transparentes y honestos:**
Q5 definio `LoadingContext` con 3 estados. Usarlos:
- `"thinking"` → "Clara esta buscando informacion..." (default al enviar texto)
- `"listening"` → "Clara esta escuchando tu mensaje..." (cuando Q7 envia audio)
- `"reading"` → "Clara esta leyendo tu documento..." (cuando Q9 envia imagen)
Maria no entiende un spinner. Maria entiende "Clara esta buscando informacion".

**4. Los errores son conversaciones, no pantallas rojas:**
Q5 exporta `getErrorMessage()`. Los errores se muestran DENTRO de una burbuja de Clara, como si Clara dijera: "Perdona, no he podido conectarme. Revisa tu wifi." Con un **boton de accion real** (no texto plano): "Reintentar" / "Escribir" / "Esperar". El error es PARTE de la conversacion, no un modal que asusta.

El tono de los errores refuerza que Clara es una **companera, no un sistema**:
- "Perdona, algo no ha ido bien. Sigo aqui contigo." (no "Error 500")
- "No he podido conectarme. Revisa tu wifi y vuelve a intentarlo." (no "ECONNREFUSED")
- "Necesito un momento. Intenta de nuevo en unos segundos." (no "Timeout")

Clara nunca se disculpa con lenguaje corporativo ("Lamentamos las molestias"). Clara habla como una persona que realmente quiere ayudar.

**5. Auto-scroll es suave, no teleport:**
Cada nuevo mensaje scrollea al fondo con `behavior: "smooth"`. Pero si el usuario ha scrolleado hacia arriba (leyendo mensajes anteriores), NO forzar scroll — respetar su posicion.

**6. La entrada de texto prioriza el envio visible:**
Maria no sabe que Enter envia. El boton de enviar debe ser VISIBLE: 64x64px, azul, con icono de flecha. Enter tambien funciona, pero el boton es la affordance principal.

**7. Los 3 botones de modo son puertas, no decoracion:**
Escribir, Voz, Foto — cada uno con icono + texto. Son el "menu" de como interactuar. Voz y Foto son stubs para Q7/Q9 pero visualmente presentes desde ahora para que Maria los descubra. El boton "Escribir" muestra estado ACTIVO (borde azul, fondo sutil) para indicar el modo actual.

**8. La primera respuesta exitosa es el "category moment":**
La primera vez que Clara responde con informacion util — con fuentes, con claridad, quizas con audio — es el momento donde Maria pasa de "otro chatbot" a "esto me sirve". Este momento debe sentirse **completo**: texto legible con `leading-relaxed`, fuentes citadas en `text-label` (16px), boton de audio presente (aunque sea stub). La burbuja de respuesta no es solo informacion — es la promesa cumplida de "los tramites no deberian ser tan complicados, y mira: acabo de demostrartelo". Cada componente de la burbuja (texto + fuentes + audio) trabaja junto para crear esa sensacion de "esto es para mi".

---

## EJECUCION PASO A PASO

### PASO 0: Investigar antes de crear

**Lanza CUATRO agentes Explore en paralelo:**

**Agente A:** Lee `design/02-FRONTEND-ACCESIBLE.md` — extrae wireframe 3B (chat), specs de tamano, patrones de interaccion (auto-scroll, loading, errores).

**Agente B:** Lee `design/01-BRAND-STRATEGY.md` — extrae tono de Clara en conversacion, emociones objetivo (segura, comprendida, capaz, no juzgada, acompanada, respetada), anti-patrones.

**Agente C:** Lee `clara-web/src/lib/types.ts`, `clara-web/src/lib/api.ts`, `clara-web/src/lib/constants.ts` — confirma las funciones y tipos disponibles de Q5. Especial atencion a: `sendMessage()`, `getErrorMessage()`, `resolveAudioUrl()`, `generateSessionId()`, `LoadingContext`, `Message`, `EASING`, `DURATION`.

**Agente D:** Lee `clara-web/src/components/ui/ChatBubble.tsx`, `clara-web/src/components/ui/LoadingState.tsx`, `clara-web/src/components/ui/Button.tsx` — confirma API de props de los componentes Q3.

Luego lee tu mismo:
```
Read: design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md
```
Internalizala: "ondas concentricas de una voz que finalmente es escuchada."

---

### PASO 1: useChat.ts — "El corazon de la conversacion"

**Skills activas:** `/react-best-practices` + `/typescript-pro` + `/react-expert`

**Briefing de arquitectura:**
Este hook es el **cerebro** del chat. Maneja: lista de mensajes, estado de carga, idioma, session ID, envio de mensajes, manejo de errores. Todo lo que la UI necesita, este hook lo provee.

**Decisiones clave ANTES de escribir:**
- Usa `generateSessionId()` de Q5 (no reinventar)
- Usa `LoadingContext` de Q5 (no `loading: boolean`)
- Usa `getErrorMessage()` de Q5 (no strings inline)
- Usa `resolveAudioUrl()` de Q5 para audio URLs
- `send()` acepta `audioBase64` como segundo argumento (Q7 lo usara)
- `send()` acepta `imageBase64` como tercer argumento (Q9 lo usara)
- No retry automatico — el retry lo hace la UI via `retryLast()`

Crea `clara-web/src/hooks/useChat.ts` con **Write**:

```typescript
"use client";

import { useState, useCallback, useRef } from "react";
import {
  sendMessage,
  generateSessionId,
  resolveAudioUrl,
  getErrorMessage,
  ApiError,
} from "@/lib/api";
import type {
  Message,
  Language,
  ChatResponse,
  LoadingContext,
  ApiInputType,
  AudioPlayback,
  ErrorAction,
} from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Helpers internos                                                   */
/* ------------------------------------------------------------------ */

function createId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

/* ------------------------------------------------------------------ */
/*  Mensajes de bienvenida                                            */
/* ------------------------------------------------------------------ */

const welcomeMessages: Record<Language, string> = {
  es: "Hola, soy Clara.\n\nLos tramites no deberian ser tan complicados. Estoy aqui para ayudarte a entenderlos, paso a paso, en tu idioma.\n\nPreguntame sobre el Ingreso Minimo Vital, el empadronamiento, la tarjeta sanitaria, o lo que necesites.",
  fr: "Bonjour, je suis Clara.\n\nLes demarches ne devraient pas etre si compliquees. Je suis la pour t'aider a les comprendre, etape par etape, dans ta langue.\n\nDemande-moi sur le Revenu Minimum Vital, l'inscription municipale, la carte sanitaire, ou ce dont tu as besoin.",
};

/* ------------------------------------------------------------------ */
/*  Loading messages por contexto                                      */
/* ------------------------------------------------------------------ */

const loadingMessages: Record<Language, Record<LoadingContext, string>> = {
  es: {
    listening: "Clara esta escuchando tu mensaje...",
    thinking: "Clara esta buscando informacion...",
    reading: "Clara esta leyendo tu documento...",
  },
  fr: {
    listening: "Clara ecoute ton message...",
    thinking: "Clara cherche des informations...",
    reading: "Clara lit ton document...",
  },
};

/* ------------------------------------------------------------------ */
/*  Hook                                                              */
/* ------------------------------------------------------------------ */

export interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  language: Language;
  setLanguage: (lang: Language) => void;
  send: (text: string, audioBase64?: string, imageBase64?: string) => Promise<void>;
  addWelcome: () => void;
  retryLast: () => void;
  getLoadingMessage: (context: LoadingContext) => string;
}

export function useChat(initialLang: Language = "es"): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState<Language>(initialLang);
  const sessionId = useRef(generateSessionId());
  const lastRequestRef = useRef<{
    text: string;
    audioBase64?: string;
    imageBase64?: string;
  } | null>(null);
  const isSendingRef = useRef(false);
  const initialLangRef = useRef<Language>(initialLang);
  const hasWelcomedRef = useRef(false);

  const getLoadingMessage = useCallback(
    (context: LoadingContext) => loadingMessages[language][context],
    [language],
  );

  const addWelcome = useCallback(() => {
    if (hasWelcomedRef.current) return;
    hasWelcomedRef.current = true;
    setMessages([
      {
        id: createId(),
        sender: "clara",
        text: welcomeMessages[initialLangRef.current],
        timestamp: new Date(),
      },
    ]);
  }, []); // sin dependencias — solo ejecuta una vez, usa ref para idioma

  const send = useCallback(
    async (text: string, audioBase64?: string, imageBase64?: string) => {
      // Guard sincronico contra double-submit (Maria tiene temblor en las manos)
      if (isSendingRef.current) return;
      isSendingRef.current = true;

      // Guardar request para posible retry
      lastRequestRef.current = { text, audioBase64, imageBase64 };

      // Determinar tipo de input y contexto de carga
      let inputType: ApiInputType = "text";
      let loadingContext: LoadingContext = "thinking";

      if (audioBase64) {
        inputType = "audio";
        loadingContext = "listening";
      } else if (imageBase64) {
        inputType = "image";
        loadingContext = "reading";
      }

      // Agregar mensaje del usuario
      const userMsg: Message = {
        id: createId(),
        sender: "user",
        text: text || (audioBase64 ? "🎤" : "📷"),
        timestamp: new Date(),
      };

      // Agregar loading placeholder de Clara
      const loadingMsgId = createId();
      const loadingMsg: Message = {
        id: loadingMsgId,
        sender: "clara",
        text: "",
        timestamp: new Date(),
        loading: loadingContext,
      };

      setMessages((prev) => [...prev, userMsg, loadingMsg]);
      setIsLoading(true);

      try {
        const response: ChatResponse = await sendMessage({
          text,
          language,
          input_type: inputType,
          audio_base64: audioBase64 || null,
          image_base64: imageBase64 || null,
          session_id: sessionId.current,
        });

        // Construir AudioPlayback si hay audio
        const resolvedUrl = resolveAudioUrl(response.audio_url);
        const audio: AudioPlayback | undefined = resolvedUrl
          ? { url: resolvedUrl, state: "idle" }
          : undefined;

        const claraMsg: Message = {
          id: createId(),
          sender: "clara",
          text: response.response,
          audio,
          sources: response.sources,
          timestamp: new Date(),
        };

        // Reemplazar loading con respuesta real
        setMessages((prev) =>
          prev.filter((m) => m.id !== loadingMsgId).concat(claraMsg),
        );
      } catch (err) {
        // Error → burbuja de Clara con mensaje humano + boton de accion REAL
        let errorText: string;
        let errorAction: ErrorAction = "retry";
        let actionLabel: string;

        if (err instanceof ApiError) {
          const errInfo = getErrorMessage(err, language);
          errorText = errInfo.message;
          errorAction = errInfo.action;
          actionLabel = errInfo.actionLabel;
        } else {
          errorText =
            language === "fr"
              ? "Desolee, quelque chose s'est mal passe."
              : "Perdona, algo no ha ido bien. Sigo aqui contigo.";
          actionLabel = language === "fr" ? "Reessayer" : "Reintentar";
        }

        const errorMsg: Message = {
          id: createId(),
          sender: "clara",
          text: errorText,
          timestamp: new Date(),
          error: { action: errorAction, actionLabel },
        };

        setMessages((prev) =>
          prev.filter((m) => m.id !== loadingMsgId).concat(errorMsg),
        );
      } finally {
        setIsLoading(false);
        isSendingRef.current = false;
      }
    },
    [language],
  );

  const retryLast = useCallback(() => {
    if (lastRequestRef.current) {
      const { text, audioBase64, imageBase64 } = lastRequestRef.current;
      send(text, audioBase64, imageBase64);
    }
  }, [send]);

  return {
    messages,
    isLoading,
    language,
    setLanguage,
    send,
    addWelcome,
    retryLast,
    getLoadingMessage,
  };
}
```

**Decisiones de arquitectura:**

| Decision | Razon | Skill |
|----------|-------|-------|
| `generateSessionId()` de Q5 | No reinventar. Session ID consistente en todo el sistema | DRY |
| `LoadingContext` en vez de `boolean` | 3 estados visuales distintos: listening/thinking/reading. El LoadingState de Q3 recibe el mensaje correcto | top-design, Q5 |
| `getErrorMessage()` de Q5 | Errores i18n sin duplicar logica. Error dentro de burbuja = parte de la conversacion | senior-fullstack |
| `resolveAudioUrl()` de Q5 | Maneja URLs null, relativas, absolutas. Q8 lo agradecera | senior-fullstack |
| `retryLast()` expuesto | El UI renderiza un boton "Reintentar" en errores via `onRetry` prop. Esta funcion permite reenviar sin re-tipar | ux-heuristics |
| `lastRequestRef` con useRef | Ref, no state — no causa re-renders. Solo se lee al retry | react-best-practices |
| `loadingMessages` bidimensional | `language × context` = 6 mensajes. Clara siempre dice EXACTAMENTE que esta haciendo | design-everyday-things |
| `text: text \|\| (audioBase64 ? "🎤" : "📷")` | Mensaje del usuario siempre tiene texto visual. Audio muestra mic, foto muestra camara | ux-heuristics |
| No retry automatico | El retry es decision del USUARIO. Clara dice "Reintentar" y el usuario decide | api-designer |
| `send()` con 3 args opcionales | Q7 pasa `audioBase64`, Q9 pasa `imageBase64`. Interfaz estable para futuros Qs | YAGNI-compatible |
| `hasWelcomedRef` guard | Previene que cambiar idioma borre la conversacion. `addWelcome` solo se ejecuta una vez al montar. Sin esto, cambiar idioma en Header recrea `addWelcome` → `useEffect` la llama → wipe | react-best-practices (P0) |
| `isSendingRef` sincronico | `setState` es async — segundo tap de Maria llega antes del re-render. `useRef` es sincronico = bloqueo inmediato contra double-submit | react-best-practices (P2) |
| Error como dato estructurado | `msg.error = { action, actionLabel }` permite renderizar un BOTON real clickeable. Antes era texto `[Reintentar]` que Maria no sabia que era una accion | ux-heuristics (H9), react-best-practices (P3) |
| Eliminar `formatTimestamp()` | Dead code: timestamps se formatean en MessageList via `toLocaleTimeString()`. No hay consumidores de esta funcion | DRY (P1) |
| Tono companero en errores | "Sigo aqui contigo" en vez de "Algo ha salido mal". Clara es companera, no sistema | category-design |

---

### PASO 2: Header.tsx — "Navegacion honesta"

**Skills activas:** `/frontend-design` + `/refactoring-ui` + `/ux-heuristics`

**Briefing de diseno:**
- 56px de alto, fondo azul (`clara-blue`), texto blanco
- Boton "atras" a la izquierda → vuelve a la bienvenida (`/`)
- Titulo "Clara" centrado — el usuario sabe DONDE esta
- Selector de idioma a la derecha — compacto, `<select>` nativo (Maria lo conoce)
- Sticky top — SIEMPRE visible durante el scroll

**Wireframe:**
```
+--------------------------------------------------+
|  [<-]         Clara                    [ES v]    |  56px, sticky top
+--------------------------------------------------+
```

Crea `clara-web/src/components/Header.tsx` con **Write**:

```typescript
"use client";

import { useRouter } from "next/navigation";
import type { Language } from "@/lib/types";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

const ariaLabels: Record<Language, { back: string; lang: string }> = {
  es: { back: "Volver al inicio", lang: "Idioma" },
  fr: { back: "Retour a l'accueil", lang: "Langue" },
};

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const router = useRouter();
  const labels = ariaLabels[language];

  return (
    <header className="sticky top-0 z-10 flex items-center justify-between px-4 h-[56px] bg-clara-blue text-white">
      {/* Boton atras */}
      <button
        onClick={() => router.push("/")}
        aria-label={labels.back}
        className="min-w-touch-sm min-h-touch-sm flex items-center justify-center rounded-lg
                   hover:bg-white/10 transition-colors duration-150"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="currentColor"
          aria-hidden="true"
        >
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
        </svg>
      </button>

      {/* Titulo */}
      <h1 className="font-display font-bold text-[20px]">Clara</h1>

      {/* Selector de idioma */}
      <select
        value={language}
        onChange={(e) => onLanguageChange(e.target.value as Language)}
        aria-label={labels.lang}
        className="bg-white/20 text-white border border-white/30 rounded-lg
                   px-2 py-1 text-label font-medium min-h-touch-sm
                   focus:outline focus:outline-[3px] focus:outline-white focus:outline-offset-2"
      >
        <option value="es" className="text-clara-text">
          ES
        </option>
        <option value="fr" className="text-clara-text">
          FR
        </option>
      </select>
    </header>
  );
}
```

**Decisiones de diseno:**

| Decision | Razon | Heuristica |
|----------|-------|------------|
| `sticky top-0 z-10` | Header siempre visible. Maria no pierde el boton "atras" | Nielsen #3: User control |
| `h-[56px]` | Spec de wireframe 3B. Compacto pero con touch targets suficientes | Design spec |
| `<select>` nativo | Maria sabe usar selects del telefono. Custom dropdowns confunden | Design-everyday-things |
| `min-h-touch-sm` (48px) en boton y select | Touch targets accesibles en zona compacta | WCAG 2.5.8 |
| `hover:bg-white/10` | Feedback visual sutil sobre fondo oscuro. No agresivo | Civic Tenderness |
| `aria-label` bilingue | Screen reader dice "Volver al inicio" o "Retour a l'accueil" segun idioma actual | A11y |
| `options` con `text-clara-text` | El dropdown nativo del OS muestra texto oscuro legible | Cross-browser |
| Focus blanco (no azul) | Sobre fondo azul, el outline azul no se ve. Blanco contrasta | WCAG 2.4.7 |

---

### PASO 3: MessageList.tsx — "La conversacion hecha espacio"

**Skills activas:** `/frontend-design` + `/top-design` + `/react-best-practices`

**Briefing de diseno:**
- Zona scrolleable entre Header y ChatInput
- `role="log"` + `aria-live="polite"` → screen readers anuncian nuevos mensajes
- Auto-scroll al fondo con `behavior: "smooth"` en CADA nuevo mensaje
- Pero si el usuario scrolleo manualmente hacia arriba, NO forzar scroll (respetar su posicion)
- Cada mensaje renderiza ChatBubble (Q3) o LoadingState (Q3)
- Fuentes citadas se muestran DENTRO de la burbuja como links clickeables
- Audio URL se pasa como children (Q8 lo renderizara; por ahora solo texto "[Escuchar]")

**Wireframe:**
```
+------------------------------------------+
|                                          |
|  [Clara] Hola, soy Clara...             |  <- burbuja clara, izquierda
|                                14:30    |
|                                          |
|         [User] Que es el IMV?            |  <- burbuja user, derecha
|                          14:31           |
|                                          |
|  [Clara] El IMV es una ayuda...          |
|         > Escuchar respuesta             |  <- audio stub (Q8)
|         Fuente: seg-social.es            |  <- link clickeable
|                                14:31    |
|                                          |
|  [● ● ●  Clara esta buscando info...]   |  <- LoadingState
|                                          |
|  <div ref=bottom />                      |  <- anchor scroll
+------------------------------------------+
```

Crea `clara-web/src/components/MessageList.tsx` con **Write**:

```typescript
"use client";

import { useEffect, useRef, useCallback } from "react";
import ChatBubble from "@/components/ui/ChatBubble";
import LoadingState from "@/components/ui/LoadingState";
import type { Message, Language, LoadingContext } from "@/lib/types";

interface MessageListProps {
  messages: Message[];
  language: Language;
  getLoadingMessage: (context: LoadingContext) => string;
  onRetry: () => void;
}

/** Labels bilingues para la lista */
const labels: Record<Language, { conversation: string; source: string; listen: string }> = {
  es: { conversation: "Conversacion con Clara", source: "Fuente", listen: "Escuchar respuesta" },
  fr: { conversation: "Conversation avec Clara", source: "Source", listen: "Ecouter la reponse" },
};

export default function MessageList({
  messages,
  language,
  getLoadingMessage,
  onRetry,
}: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const userScrolledRef = useRef(false);

  // Detectar si el usuario scrolleo hacia arriba manualmente
  const handleScroll = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    userScrolledRef.current = distanceFromBottom > 100;
  }, []);

  // Auto-scroll al fondo si el usuario no ha scrolleado manualmente
  useEffect(() => {
    if (!userScrolledRef.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const l = labels[language];

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto px-4 py-6 space-y-2"
      role="log"
      aria-label={l.conversation}
      aria-live="polite"
    >
      {messages.map((msg) =>
        msg.loading ? (
          <LoadingState
            key={msg.id}
            message={getLoadingMessage(msg.loading)}
          />
        ) : (
          <ChatBubble
            key={msg.id}
            sender={msg.sender}
            timestamp={msg.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          >
            {/* Texto del mensaje — leading-relaxed para legibilidad, balance en Clara */}
            <p
              className="whitespace-pre-wrap leading-relaxed"
              style={msg.sender === "clara" ? { textWrap: "balance" } : undefined}
            >
              {msg.text}
            </p>

            {/* Boton de accion en errores — REAL button, no texto plano */}
            {msg.error && (
              <button
                onClick={onRetry}
                className="mt-3 px-4 py-2 bg-clara-blue text-white rounded-lg
                           text-label font-medium min-h-touch-sm
                           hover:bg-[#164d66] transition-colors duration-150
                           focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2"
              >
                {msg.error.actionLabel}
              </button>
            )}

            {/* Audio stub — Q8 reemplazara con AudioPlayer */}
            {msg.audio && (
              <button
                className="flex items-center gap-2 mt-2 px-3 py-2
                           bg-white/60 rounded-lg text-clara-blue
                           min-h-touch-sm hover:bg-white/80 transition-colors duration-150"
                aria-label={l.listen}
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
                <span className="text-[16px] font-medium">{l.listen}</span>
              </button>
            )}

            {/* Fuentes citadas */}
            {msg.sources && msg.sources.length > 0 && (
              <p className="text-label mt-2 text-clara-text-secondary">
                {l.source}:{" "}
                {msg.sources.map((s, i) => (
                  <span key={i}>
                    {i > 0 && ", "}
                    <a
                      href={s.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline hover:opacity-100"
                    >
                      {s.name}
                    </a>
                  </span>
                ))}
              </p>
            )}
          </ChatBubble>
        ),
      )}
      <div ref={bottomRef} />
    </div>
  );
}
```

**Decisiones de diseno:**

| Decision | Razon | Heuristica |
|----------|-------|------------|
| `role="log"` | ARIA landmark para chat. Screen readers anuncian como registro de conversacion | ARIA best practice |
| `aria-live="polite"` | Nuevos mensajes se anuncian SIN interrumpir lo que el usuario esta leyendo | Nielsen #1 |
| Auto-scroll condicional | Si Maria scrolleo para releer, no la sacamos de su posicion. Respeto al control del usuario | Nielsen #3 |
| `distanceFromBottom > 100` | Umbral de 100px. Si esta casi al fondo, auto-scroll. Si scrolleo arriba significativamente, respetar | UX pattern |
| Audio stub con boton | Q8 lo reemplazara con AudioPlayer completo. Por ahora hay affordance visual | Incremental delivery |
| `target="_blank" rel="noopener noreferrer"` | Fuentes abren en nueva pestana. Seguro (noopener). Maria no pierde el chat | OWASP + UX |
| `whitespace-pre-wrap` | Preserva saltos de linea de Clara (listas con `\n-`). Sin esto, todo seria un bloque | Typography |
| Labels bilingues | "Fuente" vs "Source", "Escuchar" vs "Ecouter". Todo respeta el idioma seleccionado | i18n |
| `getLoadingMessage()` pasado como prop | El hook useChat lo provee. MessageList no importa logica de loading — solo la renderiza | Separation of concerns |
| `space-y-2` | Spacing uniforme entre burbujas. No `gap` (overflow scroll + gap tienen edge cases) | CSS best practice |
| `onRetry` como prop | MessageList no importa logica de retry — solo la invoca. El boton real llama `retryLast()` del hook via prop | react-best-practices (P3) |
| `leading-relaxed` en `<p>` | Line-height 1.625 para respuestas de Clara de 4-6 lineas. Sin esto, texto apretado para ojos de 74 anos | web-typography (T3) |
| `text-label` en fuentes citadas | 16px minimo para texto funcional. 14px con opacity-80 no cumple contraste WCAG para Maria | web-typography (T1) |
| `textWrap: "balance"` en Clara | Evita palabras huerfanas en ultima linea. Detalle de craft que hace cada respuesta mas compuesta | web-typography (T6) |
| Boton error real con `min-h-touch-sm` | Touch target 48px. Focus visible. Clara blue consistente con boton enviar. Maria puede TOCAR "Reintentar" | ux-heuristics (U1/U6) |

---

### PASO 4: ChatInput.tsx — "Tu voz importa"

**Skills activas:** `/frontend-design` + `/ux-heuristics` + `/refactoring-ui`

**Briefing de diseno:**
- Zona fija al fondo de la pantalla
- **Linea 1:** Input de texto + boton de enviar (64x64px, azul, icono flecha)
- **Linea 2:** 3 botones de modo — Escribir (focus input), Voz (Q7 stub), Foto (Q9 stub)
- Enter envia, pero el BOTON es la affordance principal (Maria no sabe de Enter)
- Input 56px de alto, placeholder bilingue
- Boton enviar deshabilitado si el texto esta vacio
- Los 3 botones de modo tienen icono + texto (nunca icono solo)
- Voz: borde naranja (el acento calido, la invitacion)
- Foto y Escribir: borde gris (secundarios)

**Wireframe:**
```
+--------------------------------------------------+
|  [Escribe tu pregunta...              ] [ENVIAR]  |  input 56px + boton 64px
|                                                    |
|  [⌨ Escribir]    [🎤 Voz]       [📷 Foto]       |  3 botones 64px, icono+texto
+--------------------------------------------------+
```

Crea `clara-web/src/components/ChatInput.tsx` con **Write**:

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
  activeMode?: "text" | "voice" | "photo"; // modo activo actual (default: "text")
}

const placeholders: Record<Language, string> = {
  es: "Escribe tu pregunta...",
  fr: "Ecris ta question...",
};

const modeLabels: Record<Language, { write: string; voice: string; photo: string; send: string }> = {
  es: { write: "Escribir", voice: "Voz", photo: "Foto", send: "Enviar" },
  fr: { write: "Ecrire", voice: "Voix", photo: "Photo", send: "Envoyer" },
};

export default function ChatInput({
  onSendText,
  onStartVoice,
  onOpenCamera,
  disabled,
  language,
  activeMode = "text",
}: ChatInputProps) {
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const l = modeLabels[language];

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
      {/* Linea 1: Input + Enviar */}
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
                     disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={disabled || !text.trim()}
          aria-label={l.send}
          className="min-w-touch min-h-touch bg-clara-blue text-white rounded-xl
                     flex items-center justify-center
                     hover:bg-[#164d66] transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </form>

      {/* Linea 2: 3 botones de modo */}
      <div className="flex gap-3 justify-center">
        {/* Escribir — focus al input, muestra estado activo */}
        <button
          type="button"
          onClick={() => inputRef.current?.focus()}
          disabled={disabled}
          aria-label={l.write}
          aria-pressed={activeMode === "text"}
          className={`flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed
                     ${activeMode === "text"
                       ? "border-clara-blue text-clara-blue bg-clara-blue/5 font-medium"
                       : "border-clara-border text-clara-text-secondary hover:border-clara-blue hover:text-clara-blue"
                     }`}
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M20 5H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z" />
          </svg>
          <span className="text-label mt-1">{l.write}</span>
        </button>

        {/* Voz — stub para Q7 */}
        <button
          type="button"
          onClick={onStartVoice}
          disabled={disabled}
          aria-label={l.voice}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-orange text-clara-orange
                     hover:bg-clara-orange hover:text-white
                     transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
          </svg>
          <span className="text-label mt-1">{l.voice}</span>
        </button>

        {/* Foto — stub para Q9 */}
        <button
          type="button"
          onClick={onOpenCamera}
          disabled={disabled}
          aria-label={l.photo}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-border text-clara-text-secondary
                     hover:border-clara-blue hover:text-clara-blue
                     transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
          </svg>
          <span className="text-label mt-1">{l.photo}</span>
        </button>
      </div>
    </div>
  );
}
```

**Decisiones de diseno:**

| Decision | Razon | Heuristica |
|----------|-------|------------|
| Boton enviar 64x64px VISIBLE | Maria no sabe que Enter envia. El boton azul con flecha es la affordance principal | Design-everyday-things |
| Input 56px | Spec de wireframe. Lo suficientemente alto para touch comodo sin dominar la pantalla | Design spec |
| `disabled \|\| !text.trim()` en submit | No enviar mensajes vacios. Boton gris = "necesitas escribir algo" | Nielsen #5: Error prevention |
| Voz con `border-clara-orange` | Destaca visualmente. El naranja dice "calidez, invitacion a hablar". Los otros son gris | Civic Tenderness |
| `type="button"` en mode buttons | Prevenir submit del form al tocar Escribir/Voz/Foto | HTML semantics |
| Icono 28px + texto 14px | Icono grande para reconocimiento visual, texto pequeno para claridad. Nunca icono solo | A11y + Brand |
| `hover:bg-clara-orange hover:text-white` en Voz | Feedback visual: al hover, el boton se "llena" de naranja. Invitacion a probar | top-design |
| `inputRef.current?.focus()` en Escribir | Accion directa: toca "Escribir" → el cursor aparece en el input. Sin intermediarios | UX directa |
| `sticky bottom-0` | Siempre visible. Maria nunca pierde el input. Patron de TODAS las apps de chat | UX pattern |
| Labels bilingues en `modeLabels` | Todo: placeholder, botones, aria-labels respeta el idioma. Ahmed lee "Voix" en frances | i18n |
| `text-label` (16px) en labels de modo | 14px era demasiado pequeno para texto funcional. 16px cumple minimo tipografico para Maria | web-typography (T2) |
| `activeMode` con estado visual | Escribir muestra borde azul + fondo sutil cuando activo. Maria ve DONDE esta. Q7/Q9 cambiaran `activeMode` a "voice"/"photo" | ux-heuristics (U3) |
| `aria-pressed` en modo activo | Screen reader anuncia "Escribir, presionado" — accesibilidad para modo actual | WCAG 4.1.2 |
| Botones `<button>` raw, no `Button` Q3 | `Button` Q3 es `flex-row`. Mode buttons son `flex-col` (icono arriba + texto abajo). Forzar Button requeriria variant inexistente. Clases consistentes con design system | ux-heuristics (U4) + pragmatismo |

---

### PASO 5: chat/page.tsx — "La sala de conversacion"

**Skills activas:** `/nextjs-developer` + `/react-expert` + `/frontend-developer`

**Briefing de arquitectura:**
- `"use client"` — estado, hooks, interactividad
- Lee `lang` de `searchParams` (Q4 navega con `?lang=es`)
- Composicion: Header + MessageList + ChatInput, layout `h-screen flex flex-col`
- `addWelcome()` en `useEffect` al montar — Clara saluda inmediatamente
- Voz y Foto son stubs: por ahora muestran `alert()` bilingue ("Disponible pronto" / "Bientot disponible")

Crea `clara-web/src/app/chat/page.tsx` con **Write**:

```typescript
"use client";

import { useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Header from "@/components/Header";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import { useChat } from "@/hooks/useChat";
import type { Language } from "@/lib/types";

const comingSoon: Record<Language, string> = {
  es: "Esta funcion estara disponible pronto",
  fr: "Cette fonction sera bientot disponible",
};

function ChatContent() {
  const searchParams = useSearchParams();
  const initialLang = (searchParams.get("lang") as Language) || "es";
  const {
    messages,
    isLoading,
    language,
    setLanguage,
    send,
    addWelcome,
    retryLast,
    getLoadingMessage,
  } = useChat(initialLang);

  // Clara saluda al entrar — solo una vez (addWelcome tiene guard interno)
  useEffect(() => {
    addWelcome();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col h-screen bg-clara-bg">
      <Header language={language} onLanguageChange={setLanguage} />

      <MessageList
        messages={messages}
        language={language}
        getLoadingMessage={getLoadingMessage}
        onRetry={retryLast}
      />

      <ChatInput
        onSendText={(text) => send(text)}
        onStartVoice={() => {
          // Q7 reemplazara con VoiceRecorder
          alert(comingSoon[language]);
        }}
        onOpenCamera={() => {
          // Q9 reemplazara con DocumentUpload
          alert(comingSoon[language]);
        }}
        disabled={isLoading}
        language={language}
      />
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense>
      <ChatContent />
    </Suspense>
  );
}
```

**Decisiones de arquitectura:**

| Decision | Razon | Heuristica |
|----------|-------|------------|
| `Suspense` wrapper | `useSearchParams()` requiere Suspense en Next.js App Router. Sin esto, build falla | Next.js requirement |
| `ChatContent` extraido | Componente interno que usa hooks. El export es un wrapper con Suspense | Next.js pattern |
| `addWelcome()` en `useEffect([])` | Clara saluda al montar. `[]` deps + guard interno `hasWelcomedRef` = nunca re-ejecuta. Cambiar idioma NO borra conversacion | Nielsen #1 + react-best-practices (P0) |
| `alert()` para stubs | Minimo viable. Q7/Q9 reemplazaran con componentes reales. Alert es honesto: "pronto" | Incremental delivery |
| `h-screen flex flex-col` | Layout de chat clasico: header(fijo) + messages(scroll) + input(fijo). Ocupa toda la pantalla | UX pattern |
| `bg-clara-bg` | Fondo `#FAFAFA`. Calido, no agresivo. No blanco puro | Civic Tenderness |
| Props pasados sin destructuring extra | Cada componente recibe exactamente lo que necesita. Sin over-engineering | YAGNI |
| `(searchParams.get("lang") as Language) \|\| "es"` | Default "es" si no hay param. Seguro — Language es union literal | TypeScript |

---

### PASO 6: Verificar build y tipos (agentes paralelos)

**Skill activa:** `/verification-before-completion` + `/test-driven-development`

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
| `Module '"@/lib/api"' has no exported member 'generateSessionId'` | Q5 no se completo | Verifica que `api.ts` exporta `generateSessionId` |
| `Type '"listening"' is not assignable to type 'boolean'` | `LoadingState` de Q3 espera `boolean` pero pasamos `LoadingContext` | Q3's LoadingState no usa `loading` directamente — useChat maneja el mapeo. Verificar que `msg.loading` se pasa como prop de `message` al LoadingState |
| `Cannot find module '@/components/Header'` | Path incorrecto | Verificar que Header esta en `components/Header.tsx`, no en `components/ui/Header.tsx` |
| `'useSearchParams' must be wrapped in Suspense` | Next.js App Router requirement | Ya manejado con Suspense wrapper en page.tsx |
| `Property 'audio' does not exist on type 'Message'` | Q5 types.ts usa `audio?: AudioPlayback` | Verificar que `Message` tiene campo `audio` (no `audio_url`) |

---

### PASO 7: Test funcional manual

**Skill activa:** `/design-everyday-things`

Si el backend esta corriendo (`bash scripts/run-local.sh`), verifica el flujo completo:

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npm run dev
```

**Checklist de flujo:**

1. **Abrir** `http://localhost:3000` → ver pantalla de bienvenida (Q4)
2. **Click** "Empezar a hablar" o "Prefiero escribir" → navega a `/chat?lang=es`
3. **Verificar** mensaje de bienvenida de Clara aparece automaticamente
4. **Escribir** "Que es el IMV?" → tocar boton enviar (azul)
5. **Verificar** loading: "Clara esta buscando informacion..." con puntos animados
6. **Verificar** respuesta de Clara aparece en burbuja azul claro
7. **Verificar** timestamp en cada burbuja
8. **Verificar** fuentes citadas (si las hay) son links clickeables
9. **Cambiar** idioma a FR en header → Clara entiende frances
10. **Scroll** hacia arriba → escribir nuevo mensaje → verificar que NO fuerza scroll
11. **Tocar** "Voz" → alert "Esta funcion estara disponible pronto"
12. **Tocar** "Foto" → alert similar

**Si el backend NO esta corriendo:**
- Escribir mensaje → verificar que aparece error amigable de Clara: "Parece que no hay conexion..."
- NO pantalla rota, NO error tecnico visible

---

### PASO 8: Review de diseno integral

**Skill activa:** `/ux-heuristics` + `/design-everyday-things` + `/brand-guidelines`

**Heuristica de Nielsen — Chat completo:**

| # | Heuristica | Como se cumple |
|---|-----------|----------------|
| 1 | Visibility of system status | Loading muestra QUE hace Clara. Timestamp en cada mensaje. Header fijo con titulo |
| 2 | Match between system and real world | Patron WhatsApp. Burbujas izq/der. Input abajo. Auto-scroll. Maria lo reconoce |
| 3 | User control and freedom | Boton atras en header. Scroll libre. No forzar posicion. Stubs honestos ("pronto") |
| 4 | Consistency and standards | Mismos colores, bordes, touch targets que Q3/Q4. Font-display para Clara, font-body para contenido |
| 5 | Error prevention | Submit deshabilitado si vacio. `isSendingRef` previene double-submit sincronicamente. Stubs en vez de features rotas |
| 6 | Recognition rather than recall | Primera respuesta muestra TODO lo que Clara puede hacer (texto + fuentes + audio stub). Maria no tiene que adivinar — lo ve |
| 7 | Flexibility and efficiency | Enter para power users + boton para Maria. 3 modos de input visibles |
| 8 | Aesthetic and minimalist design | Solo 3 zonas claras. Sin decoracion extra. Espacio respira. `text-wrap: balance` en Clara |
| 9 | Help users recognize and recover from errors | Errores dentro de burbuja con **boton real clickeable** "Reintentar". `retryLast()` se conecta via prop. Tono companero: "Sigo aqui contigo" |
| 10 | Help and documentation | Clara SE explica: "Los tramites no deberian ser tan complicados... Preguntame sobre..." |

**Checklist de accesibilidad (22 puntos):**

**Header:**
- [ ] Boton atras con `aria-label` bilingue
- [ ] Select idioma con `aria-label` bilingue
- [ ] Focus visible (outline blanco sobre fondo azul)
- [ ] Touch targets 48px minimo
- [ ] `sticky top-0` — siempre accesible

**MessageList:**
- [ ] `role="log"` + `aria-live="polite"`
- [ ] Screen reader anuncia nuevos mensajes automaticamente
- [ ] Auto-scroll suave (no teleport)
- [ ] Auto-scroll respeta posicion manual del usuario
- [ ] Texto 18px minimo en burbujas
- [ ] Links de fuentes con `target="_blank" rel="noopener noreferrer"`
- [ ] `whitespace-pre-wrap` preserva listas de Clara

**ChatInput:**
- [ ] Input con `aria-label` bilingue
- [ ] Input 56px alto — touch target suficiente
- [ ] Boton enviar 64x64px con `aria-label`
- [ ] Boton enviar disabled cuando vacio (error prevention)
- [ ] 3 botones de modo con icono + texto (nunca icono solo)
- [ ] Cada boton con `aria-label` bilingue
- [ ] Boton Voz con borde naranja (destaca visualmente)
- [ ] `type="button"` en botones de modo (no submit accidental)
- [ ] `sticky bottom-0` — siempre accesible
- [ ] `aria-pressed` en boton de modo activo (U3)
- [ ] Mode button labels en `text-label` (16px), no 14px (T2)

**Typography (web-typography):**
- [ ] Line-height `leading-relaxed` (1.625) en texto de burbujas (T3)
- [ ] Source links en `text-label` (16px) con `text-clara-text-secondary` (T1)
- [ ] `text-wrap: balance` en burbujas de Clara (T6)

**Error Recovery (ux-heuristics):**
- [ ] Error action es boton real clickeable con `min-h-touch-sm` (U1/U6)
- [ ] `retryLast()` conectado via `onRetry` prop (P3)
- [ ] Double-submit bloqueado por `isSendingRef` sincronico (P2/U5)

**Checklist de marca (9 puntos):**
- [ ] Clara saluda con POV: "Los tramites no deberian ser tan complicados" (no lista features)
- [ ] Nombre "Clara" visible en header y en cada burbuja suya
- [ ] Solo colores de paleta Clara (no hex arbitrarios excepto hover states)
- [ ] Font-display para "Clara" (brand), font-body para contenido
- [ ] Tono de error companero: "Sigo aqui contigo" (no corporativo ni tecnico)
- [ ] Fuentes citadas — Clara siempre muestra de donde viene la informacion
- [ ] Welcome message enmarca villano (burocracia), no capacidades (category-design)
- [ ] Primera respuesta exitosa se siente completa: texto + fuentes + audio stub (category moment)
- [ ] Errores sugieren accion con boton real, no texto entre corchetes

**Checklist de integracion con Q5 (8 puntos):**
- [ ] `sendMessage()` llamado correctamente con `ChatRequest` completo
- [ ] `generateSessionId()` usado para session ID (no reinventado)
- [ ] `getErrorMessage()` usado para errores i18n (no strings inline)
- [ ] `resolveAudioUrl()` usado para audio URLs
- [ ] `LoadingContext` usado para estados de carga (no `boolean`)
- [ ] `Message` interface respetada para todo el estado
- [ ] `EASING` y `DURATION` importables (usados en animaciones futuras, presentes en el sistema)
- [ ] `Language` type usado en todos los componentes

---

### PASO 9: Commit

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && git add clara-web/src/hooks/useChat.ts clara-web/src/components/Header.tsx clara-web/src/components/MessageList.tsx clara-web/src/components/ChatInput.tsx clara-web/src/app/chat/
git commit -m "feat: add chat interface — Clara's core conversation screen

- useChat.ts: conversation hook with LoadingContext (3 states), i18n error messages
  via getErrorMessage(), generateSessionId() from Q5, retryLast() for error recovery
- Header.tsx: sticky navigation with back button, language selector, bilingual labels
- MessageList.tsx: role=log with aria-live, smart auto-scroll (respects manual scroll),
  audio stub for Q8, source links, bilingual labels
- ChatInput.tsx: text input + 64px send button + 3 mode buttons (write/voice/photo),
  voice stub for Q7, photo stub for Q9, bilingual placeholders and labels
- chat/page.tsx: page composition with Suspense, welcome message on mount,
  reads lang from searchParams (Q4 navigation)
- Consumes Q5: sendMessage(), getErrorMessage(), resolveAudioUrl(), generateSessionId()
- Consumes Q3: ChatBubble, LoadingState, Button
- WCAG AAA: aria-live log, bilingual aria-labels, 18px+ text, 64px touch targets
- Design: Civic Tenderness — WhatsApp-like pattern, honest loading, errors as conversation

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Read** | Paso 0 — leer design docs + config + Q3/Q5 | Entender antes de codear |
| **Write** | Pasos 1-5 — crear hook, componentes, pagina | 5 archivos nuevos |
| **Bash** | Paso 6 — build + type check | Verificar compilacion |
| **Glob** | Verificar archivos creados | `clara-web/src/hooks/*.ts`, `clara-web/src/components/*.tsx` |
| **Task** | Paso 0 (lectura paralela) y Paso 6 (verificacion paralela) | `subagent_type="Explore"` o `"Bash"` |

## RESTRICCIONES ABSOLUTAS

1. **NO cambies** archivos de Q3 (`components/ui/`), Q4 (`app/page.tsx`), ni Q5 (`lib/`)
2. **NO cambies** archivos del backend (`src/`)
3. **NO instales** librerias adicionales — todo se construye con lo que Q2 instalo
4. **NO uses** React Query, SWR, ni librerias de fetching — `useChat` es suficiente
5. **NO implementes** grabacion de voz (Q7) ni upload de fotos (Q9) — solo stubs con `alert()`
6. **NO implementes** AudioPlayer real (Q8) — solo boton stub "[Escuchar]"
7. **NO uses** `useEffect` para fetching — el fetch ocurre en `send()` via callback
8. **Los tipos de Q5 son sagrados** — usa `Message`, `Language`, `LoadingContext` tal cual estan definidos
9. **Errores DENTRO de burbujas** — nunca modals, nunca toasts, nunca pantallas rojas
10. **Iconos SIEMPRE con texto** en botones de modo — nunca icono solo
11. **NO `alert()` excepto en stubs** — los stubs de Voz/Foto son los unicos usos validos de alert
12. **Lee los archivos de diseno y Q5 ANTES de escribir codigo** — el diseno y los tipos guian la ingenieria
13. **NO retry automatico** — el retry es decision del usuario, no del sistema

## DEFINICION DE TERMINADO

**Investigacion:**
- [ ] `design/02-FRONTEND-ACCESIBLE.md` leido (wireframe 3B, interaction patterns)
- [ ] `design/01-BRAND-STRATEGY.md` leido (tono Clara, emociones objetivo)
- [ ] `design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md` leida
- [ ] Q5 types.ts, api.ts, constants.ts leidos y confirmados
- [ ] Q3 ChatBubble, LoadingState, Button leidos y confirmados

**Archivos creados:**
- [ ] `clara-web/src/hooks/useChat.ts` — estado de conversacion, send(), retryLast(), getLoadingMessage(), welcome
- [ ] `clara-web/src/components/Header.tsx` — sticky header, back, language select, bilingual
- [ ] `clara-web/src/components/MessageList.tsx` — role=log, auto-scroll smart, loading states, audio stub, sources
- [ ] `clara-web/src/components/ChatInput.tsx` — input + send + 3 mode buttons, bilingual
- [ ] `clara-web/src/app/chat/page.tsx` — page composition, Suspense, welcome on mount

**Verificaciones:**
- [ ] `npm run build` exitoso
- [ ] `npx tsc --noEmit` sin errores
- [ ] Test funcional manual (12 pasos) — si backend disponible
- [ ] Checklist Nielsen (10 heuristicas) verificado
- [ ] Checklist accesibilidad (28 puntos) verificado
- [ ] Checklist marca (9 puntos) verificado
- [ ] Checklist integracion Q5 (8 puntos) verificado
- [ ] P0 verificado: cambiar idioma NO borra la conversacion
- [ ] P2 verificado: tap rapido doble NO envia mensaje duplicado
- [ ] P3 verificado: error muestra boton real "Reintentar" (no texto plano)
- [ ] T1 verificado: source links son 16px legibles
- [ ] T3 verificado: texto en burbujas tiene line-height 1.625
- [ ] Commit con mensaje descriptivo

---

> **Dependencia Q5:** Este Q requiere que `Message` en `types.ts` tenga campo opcional `error?: { action: ErrorAction; actionLabel: string }`. Si Q5 no lo incluye, el implementador debe agregarlo a `types.ts` como primer paso antes de useChat.

> **Nota T4 (para Q3):** ChatBubble usa `max-w-[85%]`. En pantallas anchas (tablet/desktop), esto puede crear lineas de 80+ caracteres. Considerar agregar `max-w-prose` (65ch) como cap adicional en ChatBubble: `max-w-[min(85%,_65ch)]`. Este cambio va en Q3, no en Q6.

> **Siguiente:** Q7 reemplazara el `alert()` del boton Voz con `VoiceRecorder` + `useAudioRecorder` y cambiara `activeMode` a "voice". Q8 reemplazara el boton "[Escuchar]" con `AudioPlayer`. Ambos consumiran `EASING`, `DURATION`, `AUDIO_FEEDBACK` de Q5.
> **Dependencias:** Este Q depende de Q3 (componentes), Q4 (navegacion), Q5 (API + types). Q7, Q8, Q9 dependen de este Q.

> **Reviews incorporadas:** react-best-practices (P0-P3), category-design (CD1-CD3), web-typography (T1-T7), ux-heuristics (U1-U6). Total: 15 fixes aplicados.
