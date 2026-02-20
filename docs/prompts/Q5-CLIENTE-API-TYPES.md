# Q5: Cliente API, Types y Constants — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q2 (Scaffolding Next.js) debe estar completado. Verifica que `clara-web/` existe con `package.json`.
> **Tiempo estimado:** 12-18 min

---

## PROMPT

### ROL

Eres un **ingeniero de plataforma frontend** especializado en contratos TypeScript, clientes HTTP y sistemas de diseno programatico. Tu trabajo en este Q es construir la **capa de datos Y la infraestructura de diseno** que conecta el frontend Next.js con el backend Flask de Clara. No creas UI — creas los **cimientos tipados** sobre los que Q6 a Q12 construiran.

Cada tipo que definas, cada funcion que exportes, cada constante que establezcas sera consumida por al menos 3 componentes futuros. Si un tipo esta mal, el error se propaga en cascada. Si un error HTTP no se maneja bien, Maria (74 anos) ve una pantalla rota. Si las constantes de animacion no existen, cada Q inventa las suyas y la app se siente desconectada.

**Los "usuarios" de este Q son los futuros Qs y las personas que usan Clara:**

| Consumidor | Que necesita de tu codigo | Consecuencia si falla |
|------------|--------------------------|----------------------|
| **Q6 (Chat)** | `sendMessage()`, `Message`, `ChatResponse`, `Language`, `getErrorMessage()` | El chat no puede enviar/recibir ni mostrar errores humanos |
| **Q7 (Voice)** | `ChatRequest.audio_base64`, `ApiInputType`, `AUDIO_FEEDBACK`, `generateSessionId()` | La grabacion de voz no se envia, sin beeps de feedback |
| **Q8 (Audio)** | `AudioPlayback`, `resolveAudioUrl()`, `DURATION`, `EASING` | No se puede reproducir la respuesta de Clara con buena UX |
| **Q9 (Upload)** | `ChatRequest.image_base64`, `ApiInputType` | Los documentos no se pueden analizar |
| **Q10 (i18n)** | `Language` type, `getErrorMessage()` bilingue | El multiidioma se rompe, errores sin traducir |

### SKILLS OBLIGATORIAS

**Capa de Arquitectura (invoca ANTES de escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/typescript-pro` | Tipado estricto, discriminated unions, generics, exhaustive checks | Al definir TODOS los tipos |
| `/api-designer` | Patrones de cliente HTTP, error handling, contratos API | Al disenar api.ts |
| `/owasp-security` | Validacion de inputs, prevencion XSS, sanitizacion | Al manejar datos del backend |

**Capa de Ingenieria (invoca AL escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/react-best-practices` | Patrones de estado, custom hooks, data fetching | Al disenar la API para hooks futuros |
| `/frontend-developer` | Buenas practicas frontend, env vars, build config | Al configurar constants y .env |
| `/top-design` | Constantes de motion/timing que habilitan diseno 10/10 en Q6-Q12 | Al definir EASING y DURATION |

**Capa de Verificacion (invoca DESPUES del codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/verification-before-completion` | Checklist final antes del commit | Al terminar todo |
| `/test-driven-development` | Verificar que los tipos compilan correctamente | Post-build |

### ESTRATEGIA MULTI-AGENTE

```
FASE 1 — Investigacion del backend (paralelo):
  Agente A (Explore): Lee src/routes/api_chat.py — POST /api/chat y GET /api/health (request/response shapes reales)
  Agente B (Explore): Lee src/core/models.py — dataclasses Python (InputType, FinalResponse, etc.)
  Agente C (Explore): Lee src/app.py — CORS config, blueprints, FRONTEND_URL default

FASE 2 — Implementacion (secuencial):
  Tu (principal):
    1. types.ts (contratos TypeScript espejando backend + tipos UI)
    2. constants.ts (configuracion + motion + audio feedback)
    3. api.ts (cliente HTTP + helpers + error messages i18n)
    4. .env.local + .env.example

FASE 3 — Verificacion (paralelo):
  Agente D (Bash): npm run build
  Agente E (Bash): npx tsc --noEmit
```

---

### CONTEXTO TECNICO

#### Backend existente — el servidor Flask que ya funciona:

**Endpoint principal:** `POST /api/chat`
**Archivo:** `src/routes/api_chat.py`

Request body (lo que el backend REALMENTE lee):
```python
text = (data.get("text") or "").strip()       # Acepta null/empty
language = data.get("language", "es")           # Default "es"
input_type_str = data.get("input_type", "text") # "text" | "audio" | "image"
audio_b64 = data.get("audio_base64")            # Base64 string o null
```

Response (200):
```json
{
  "response": "string",
  "source": "cache | llm | fallback | guardrail",
  "language": "es | fr",
  "duration_ms": 1234,
  "audio_url": "string | null",
  "sources": [{"name": "string", "url": "string"}]
}
```

Errores:
- `400`: `{"error": "text or audio_base64 required"}` — ni texto ni audio enviado
- `422`: `{"error": "audio_transcription_failed"}` — Whisper no pudo transcribir
- `500`: `{"error": "audio_processing_error"}` — error interno procesando audio

**Endpoint health:** `GET /api/health`

Response (200):
```json
{
  "status": "ok",
  "features": {
    "whisper": true,
    "llm": true,
    "guardrails": true,
    "demo_mode": false
  }
}
```

**CORS:** Configurado en `src/app.py` lineas 49-53 para `http://localhost:3000` (y `FRONTEND_URL` env var). Rutas `/api/*` habilitadas.

**Audio estatico:** `GET /static/cache/<filename>` — sirve MP3s desde `data/cache/`. El backend construye URLs completas: `{AUDIO_BASE_URL}/{filename}`.

**IMPORTANTE — Mismatch a evitar:**
El backend usa `input_type: "audio"` pero la UI habla de "voz" / "voice". Son dominios diferentes:
- **UI concept**: `InputMode = "text" | "voice" | "image"` (lo que el usuario elige)
- **API concept**: `ApiInputType = "text" | "audio" | "image"` (lo que el backend recibe)
Q7 debe mapear `"voice" → "audio"` al llamar `sendMessage()`.

---

### PRINCIPIOS DE INGENIERIA PARA ESTA CAPA

**1. Los tipos son documentacion viva:**
Un tipo TypeScript bien definido es mejor que 10 paginas de docs. Cuando un futuro Q importe `ChatResponse`, el IDE le dice exactamente que campos tiene, cuales son opcionales, y cuales son los valores posibles.

**2. Los errores son conversaciones, no codigos:**
Cuando `sendMessage()` falla, Clara no puede quedarse callada. Cada error del backend tiene un equivalente humano EN CADA IDIOMA:
- `400` → "Necesito que me digas o envies algo" / "J'ai besoin que tu me dises quelque chose"
- `422` → "No he podido entender el audio, puedes repetir?" / "Je n'ai pas pu comprendre l'audio"
- `500` → "Algo ha salido mal, intenta de nuevo" / "Quelque chose s'est mal passe"
- `network` → "Parece que no hay conexion" / "Il semble qu'il n'y ait pas de connexion"
Q5 EXPORTA esta funcion. Q6 la consume. No se reinventa.

**3. El cliente es defensivo, no optimista:**
Asume que el backend puede devolver JSON malformado (proxy 502 devolviendo HTML), que la red puede fallar, que `audio_url` puede ser relativa o null. Valida, tipea, y maneja cada caso.

**4. Las constantes son un solo lugar de verdad:**
`API_BASE_URL`, `EASING`, `DURATION`, `AUDIO_FEEDBACK` — se definen UNA vez. Ningun futuro Q hardcodea valores. Si algo cambia, se cambia en un solo lugar.

**5. La motion tiene DNA consistente:**
Las animaciones de Q6 (burbujas), Q7 (waveform), Q8 (audio player) deben sentirse como parte del mismo sistema. Los easing curves y duraciones se definen aqui, no se inventan en cada componente.

---

## EJECUCION PASO A PASO

### PASO 0: Investigar el backend real

**Lanza TRES agentes Explore en paralelo:**

**Agente A:** Lee `src/routes/api_chat.py` — extrae el request/response shape REAL. Confirma: que campos lee el backend? como construye `audio_url`? que errores devuelve?

**Agente B:** Lee `src/core/models.py` — extrae `InputType` enum (`TEXT`, `AUDIO`, `IMAGE`). Los tipos TypeScript deben ESPEJAR estos contratos.

**Agente C:** Lee `src/app.py` — confirma que `api_bp` esta registrado, que CORS esta habilitado para `/api/*`, y que `FRONTEND_URL` default es `http://localhost:3000`.

---

### PASO 1: types.ts — "El contrato entre frontend y backend"

**Skills activas:** `/typescript-pro` + `/api-designer` + `/top-design`

**Briefing de arquitectura:**
Este archivo define: (a) tipos que cruzan la frontera frontend↔backend, (b) tipos internos del estado UI, (c) tipos de soporte para motion, audio y errores. Cada tipo debe usar `type` para uniones literales e `interface` para objetos. JSDoc en campos no obvios.

Crea `clara-web/src/lib/types.ts` con **Write**:

```typescript
/* ================================================================== */
/*  types.ts — Contratos TypeScript para Clara                        */
/*  Fuente de verdad: src/routes/api_chat.py + src/core/models.py     */
/* ================================================================== */

/* ------------------------------------------------------------------ */
/*  Primitivos                                                        */
/* ------------------------------------------------------------------ */

/** Idiomas soportados en Fase 1 */
export type Language = "es" | "fr";

/** Modos de entrada — concepto UI (lo que el usuario elige) */
export type InputMode = "text" | "voice" | "image";

/**
 * Tipos de entrada — concepto API (lo que el backend recibe).
 * IMPORTANTE: "voice" (UI) se mapea a "audio" (API).
 * Q7 debe hacer: input_type: mode === "voice" ? "audio" : mode
 */
export type ApiInputType = "text" | "audio" | "image";

/** Quien envia el mensaje en el chat */
export type MessageSender = "clara" | "user";

/** Origenes de la respuesta del backend */
export type ResponseSource = "cache" | "llm" | "fallback" | "guardrail";

/* ------------------------------------------------------------------ */
/*  API Request / Response                                            */
/* ------------------------------------------------------------------ */

/** POST /api/chat — request body */
export interface ChatRequest {
  /**
   * Texto del usuario. Requerido para input_type="text".
   * Para audio: pasar "" — el backend transcribe con Whisper.
   * Para image: pasar descripcion o "".
   */
  text: string;
  language: Language;
  input_type: ApiInputType;
  /** Audio grabado codificado en base64. Solo cuando input_type="audio" */
  audio_base64?: string | null;
  /** Imagen de documento codificada en base64. Solo cuando input_type="image" */
  image_base64?: string | null;
  /** Identificador de sesion para continuidad de conversacion */
  session_id: string;
}

/** POST /api/chat — response body (200 OK) */
export interface ChatResponse {
  response: string;
  audio_url: string | null;
  source: ResponseSource;
  language: Language;
  duration_ms: number;
  sources: Source[];
}

/** Fuente de informacion citada por Clara */
export interface Source {
  name: string;
  url: string;
}

/** GET /api/health — response body */
export interface HealthResponse {
  status: "ok";
  features: {
    whisper: boolean;
    llm: boolean;
    guardrails: boolean;
    demo_mode: boolean;
  };
}

/* ------------------------------------------------------------------ */
/*  Estado interno del chat (UI)                                      */
/* ------------------------------------------------------------------ */

/** Contexto de carga — determina QUE mensaje y animacion mostrar */
export type LoadingContext = "listening" | "thinking" | "reading";

/**
 * Metadata para reproduccion de audio (Q8 AudioPlayer).
 * Mas rico que un simple string URL.
 */
export interface AudioPlayback {
  url: string;
  /** Duracion total en segundos (si disponible) */
  duration_s?: number;
  /** Estado de reproduccion */
  state: "idle" | "playing" | "paused";
}

/** Un mensaje en la conversacion (local, no se envia al backend) */
export interface Message {
  id: string;
  sender: MessageSender;
  text: string;
  /** Audio de la respuesta de Clara (Q8 lo renderiza) */
  audio?: AudioPlayback;
  sources?: Source[];
  timestamp: Date;
  /**
   * Contexto de carga — si presente, se muestra LoadingState en vez de texto.
   * "listening" = "Clara esta escuchando..."
   * "thinking" = "Clara esta buscando informacion..."
   * "reading" = "Clara esta leyendo tu documento..."
   */
  loading?: LoadingContext;
}

/* ------------------------------------------------------------------ */
/*  Errores tipados                                                   */
/* ------------------------------------------------------------------ */

/** Categorias de error — determina icono y estilo visual */
export type ErrorCategory = "network" | "audio" | "server" | "timeout";

/** Accion sugerida al usuario tras un error */
export type ErrorAction = "retry" | "wait" | "check_connection" | "try_text";

/** Parametros para feedback auditivo via Web Audio API */
export interface AudioFeedbackParams {
  frequency: number;
  duration: number;
  type: OscillatorType;
}
```

**Decisiones de tipado:**

| Decision | Razon | Skill |
|----------|-------|-------|
| `InputMode` ("voice") vs `ApiInputType` ("audio") separados | Evita bug en Q7: el UI dice "voice", el backend espera "audio". Separar obliga al mapping explicito | senior-fullstack P0 |
| `LoadingContext` en vez de `boolean` | Habilita 3 estados visuales distintos (listening/thinking/reading). top-design: "loading states are designed, not afterthoughts" | top-design P1 |
| `AudioPlayback` interface en vez de `audio_url: string` | Q8 necesita mas que una URL — necesita estado de reproduccion y duracion para UX rica | algorithmic-art P2 |
| `ErrorCategory` + `ErrorAction` types | Habilita estados de error disenados: icono + mensaje + boton de accion | top-design P2 |
| `AudioFeedbackParams` interface | Q7 usa beeps de grabacion. Tipo centralizado en vez de magic numbers | audio-logo P2 |
| JSDoc exhaustivo en `ChatRequest.text` | Explica que para audio se pasa "". Sin esto, Q7 dev no sabe que hacer | senior-fullstack P2 |
| `Message.loading?: LoadingContext` (no `boolean`) | Un campo, tres expresiones visuales. YAGNI-compatible pero design-forward | top-design |

---

### PASO 2: constants.ts — "Un solo lugar de verdad"

**Skills activas:** `/frontend-developer` + `/top-design` + `/audio-logo-design`

Crea `clara-web/src/lib/constants.ts` con **Write**:

```typescript
/* ================================================================== */
/*  constants.ts — Configuracion centralizada para Clara Web          */
/* ================================================================== */

import type { AudioFeedbackParams } from "./types";

/* ------------------------------------------------------------------ */
/*  API                                                               */
/* ------------------------------------------------------------------ */

/**
 * URL base del backend Flask.
 * Dev: http://localhost:5000 | Prod: NEXT_PUBLIC_API_URL en Render/Vercel
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

/** Timeout para requests al backend (ms). Generoso para conexiones lentas */
export const API_TIMEOUT_MS = 30_000;

/* ------------------------------------------------------------------ */
/*  Colores — nombres semanticos, no genericos                       */
/*  "Civic Tenderness: el color conversa, no grita"                  */
/* ------------------------------------------------------------------ */

/**
 * Paleta Clara para uso fuera de Tailwind (canvas, SVG dinamico, Web Audio viz).
 * Para CSS: usar tokens Tailwind (bg-clara-blue, text-clara-orange, etc.)
 */
export const COLORS = {
  trust: "#1B5E7B",      // Azul — confianza, headers, primary
  warmth: "#D46A1E",     // Naranja — calidez, CTAs, active
  hope: "#2E7D4F",       // Verde — esperanza, success
  alert: "#C62828",      // Error — honesto, no alarmante
  caution: "#F9A825",    // Warning — atencion necesaria
} as const;

/* ------------------------------------------------------------------ */
/*  Motion — lenguaje de animacion consistente                       */
/*  "Civic Tenderness: calido, sin prisa, nunca abrupto"             */
/* ------------------------------------------------------------------ */

/** Easing curves — expo out se siente calido y fisico */
export const EASING = {
  /** Elementos que entran (burbujas, cards, modals) */
  out: "cubic-bezier(0.16, 1, 0.3, 1)",
  /** Elementos que salen (dismiss, close) */
  in: "cubic-bezier(0.55, 0, 1, 0.45)",
  /** Elementos que se transforman (hover, pressed) */
  inOut: "cubic-bezier(0.65, 0, 0.35, 1)",
} as const;

/** Duraciones en ms — generosas para usuarios mayores */
export const DURATION = {
  /** Feedback inmediato (pressed, hover) */
  instant: 150,
  /** Transiciones normales (color, border) */
  normal: 300,
  /** Entradas de elementos (bubble appear, card slide) */
  enter: 500,
  /** Stagger entre elementos secuenciales (burbujas de chat) */
  stagger: 80,
} as const;

/* ------------------------------------------------------------------ */
/*  Audio feedback — DNA sonora de Clara                             */
/*  Patron Mastercard: misma identidad en todos los touchpoints      */
/* ------------------------------------------------------------------ */

/** Frecuencias para feedback auditivo via Web Audio API */
export const AUDIO_FEEDBACK: Record<string, AudioFeedbackParams> = {
  /** Beep al iniciar grabacion — nota ascendente, invitacion */
  recordStart: { frequency: 440, duration: 150, type: "sine" },
  /** Beep al parar grabacion — nota descendente, confirmacion */
  recordStop: { frequency: 349, duration: 150, type: "sine" },
  /** Sonido sutil de mensaje enviado */
  messageSent: { frequency: 523, duration: 100, type: "sine" },
};

/* ------------------------------------------------------------------ */
/*  Limites funcionales                                              */
/* ------------------------------------------------------------------ */

/** Limites de grabacion de voz — spec design/02-FRONTEND-ACCESIBLE.md */
export const MAX_RECORDING_SECONDS = 60;
export const RECORDING_WARNING_SECONDS = 50;
```

**Decisiones:**

| Decision | Razon | Skill |
|----------|-------|-------|
| Nombres semanticos: `trust`, `warmth`, `hope` | Self-documenting. Un dev no usa `COLORS.trust` para un error por accidente | top-design |
| `EASING` con expo out | Expo out se siente fisico, como una mano colocando algo suavemente. top-design: "custom easing is mandatory" | top-design |
| `DURATION.instant = 150` | 150ms = umbral de percepcion de causalidad directa. Maria siente que el boton responde | top-design |
| `DURATION.enter = 500` | Civic Tenderness: "unhurried". 500ms no es lento — es calido. Una app de tech usa 200ms | top-design |
| `AUDIO_FEEDBACK` con frecuencias | Q7 genera beeps via Web Audio API (zero dependencies). Tono consistente = identidad sonora | audio-logo |
| Sin `MAX_IMAGE_SIZE_BYTES` | YAGNI. Q9 definira su propia estrategia de upload | senior-fullstack |

---

### PASO 3: api.ts — "El mensajero entre Clara y el mundo"

**Skills activas:** `/api-designer` + `/typescript-pro` + `/owasp-security`

Crea `clara-web/src/lib/api.ts` con **Write**:

```typescript
/* ================================================================== */
/*  api.ts — Cliente HTTP para el backend Flask de Clara              */
/*  Fuente: POST /api/chat, GET /api/health (src/routes/api_chat.py)  */
/* ================================================================== */

import { API_BASE_URL, API_TIMEOUT_MS } from "./constants";
import type {
  ChatRequest,
  ChatResponse,
  HealthResponse,
  Language,
  ErrorCategory,
  ErrorAction,
} from "./types";

/* ------------------------------------------------------------------ */
/*  Error tipado                                                      */
/* ------------------------------------------------------------------ */

/**
 * Error de API con codigo HTTP, categoria y accion sugerida.
 *
 * Codigos conocidos del backend:
 * - 400: "text or audio_base64 required"
 * - 422: "audio_transcription_failed"
 * - 500: "audio_processing_error"
 * - 0: error de red / timeout (fetch fallo)
 */
export class ApiError extends Error {
  public readonly category: ErrorCategory;
  public readonly suggestedAction: ErrorAction;

  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";

    // Clasificar automaticamente
    if (status === 0) {
      this.category = message === "request_timeout" ? "timeout" : "network";
      this.suggestedAction = message === "request_timeout" ? "wait" : "check_connection";
    } else if (status === 422) {
      this.category = "audio";
      this.suggestedAction = "try_text";
    } else {
      this.category = "server";
      this.suggestedAction = "retry";
    }
  }
}

/* ------------------------------------------------------------------ */
/*  Fetch con timeout                                                 */
/* ------------------------------------------------------------------ */

async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeoutMs: number = API_TIMEOUT_MS,
): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError(0, "request_timeout");
    }
    throw new ApiError(0, "network_error");
  } finally {
    clearTimeout(timer);
  }
}

/* ------------------------------------------------------------------ */
/*  Funciones publicas — API                                          */
/* ------------------------------------------------------------------ */

/**
 * Envia un mensaje al backend de Clara.
 *
 * @example
 * const response = await sendMessage({
 *   text: "Que es el IMV?",
 *   language: "es",
 *   input_type: "text",
 *   session_id: "web_m2k8f_a7x3",
 * });
 */
export async function sendMessage(
  request: ChatRequest,
): Promise<ChatResponse> {
  const res = await fetchWithTimeout(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: "unknown_error" }));
    throw new ApiError(res.status, body.error || "request_failed");
  }

  // Defensive: guard against proxy/CDN returning 200 with non-JSON
  try {
    return await res.json();
  } catch {
    throw new ApiError(200, "invalid_response");
  }
}

/**
 * Verifica el estado del backend y sus features habilitadas.
 *
 * @example
 * const health = await checkHealth();
 * if (health.features.whisper) { /* voz disponible *\/ }
 */
export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetchWithTimeout(
    `${API_BASE_URL}/api/health`,
    { method: "GET" },
    5_000,
  );

  if (!res.ok) {
    throw new ApiError(res.status, "health_check_failed");
  }

  try {
    return await res.json();
  } catch {
    throw new ApiError(200, "invalid_response");
  }
}

/* ------------------------------------------------------------------ */
/*  Helpers publicos                                                  */
/* ------------------------------------------------------------------ */

/**
 * Genera un session ID unico y legible.
 * Patron: web_{timestamp_base36}_{random_4chars}
 *
 * @example generateSessionId() // "web_m2k8f_a7x3"
 */
export function generateSessionId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).slice(2, 6);
  return `web_${timestamp}_${random}`;
}

/**
 * Resuelve audio_url del backend a URL completa.
 * Maneja: null, URL relativa, URL absoluta.
 *
 * @example
 * resolveAudioUrl(null)                    // null
 * resolveAudioUrl("/static/cache/imv.mp3") // "http://localhost:5000/static/cache/imv.mp3"
 * resolveAudioUrl("https://cdn.example/a") // "https://cdn.example/a"
 */
export function resolveAudioUrl(audioUrl: string | null): string | null {
  if (!audioUrl) return null;
  if (audioUrl.startsWith("http")) return audioUrl;
  return `${API_BASE_URL}${audioUrl}`;
}

/**
 * Traduce un ApiError a mensaje humano en el idioma del usuario.
 * Q6 llama esto en el catch de sendMessage().
 *
 * @example
 * catch (error) {
 *   if (error instanceof ApiError) {
 *     showError(getErrorMessage(error, currentLang));
 *   }
 * }
 */
export function getErrorMessage(
  error: ApiError,
  lang: Language,
): { message: string; action: ErrorAction; actionLabel: string } {
  const messages: Record<Language, Record<ErrorCategory, {
    message: string;
    actionLabel: string;
  }>> = {
    es: {
      network: {
        message: "Parece que no hay conexion. Revisa tu wifi o datos moviles.",
        actionLabel: "Reintentar",
      },
      timeout: {
        message: "Esta tardando mas de lo normal. Un momento...",
        actionLabel: "Esperar",
      },
      audio: {
        message: "No he podido entender el audio. Puedes repetir o escribir?",
        actionLabel: "Escribir",
      },
      server: {
        message: "Algo ha salido mal. Intenta de nuevo.",
        actionLabel: "Reintentar",
      },
    },
    fr: {
      network: {
        message: "Il semble qu'il n'y ait pas de connexion. Verifie ton wifi.",
        actionLabel: "Reessayer",
      },
      timeout: {
        message: "Cela prend plus de temps que prevu. Un moment...",
        actionLabel: "Attendre",
      },
      audio: {
        message: "Je n'ai pas pu comprendre l'audio. Peux-tu repeter ou ecrire?",
        actionLabel: "Ecrire",
      },
      server: {
        message: "Quelque chose s'est mal passe. Reessaie.",
        actionLabel: "Reessayer",
      },
    },
  };

  const display = messages[lang][error.category];
  return {
    message: display.message,
    action: error.suggestedAction,
    actionLabel: display.actionLabel,
  };
}
```

**Decisiones de arquitectura:**

| Decision | Razon | Skill |
|----------|-------|-------|
| `res.json()` envuelto en `try/catch` en AMBOS paths | P0: si un proxy/CDN devuelve 200 con HTML, no explota con error sin tipar | senior-fullstack |
| `ApiError` con `category` + `suggestedAction` auto-clasificados | Q6 no necesita hacer switch por status code. Importa `error.category` y renderiza | top-design |
| `getErrorMessage()` exportado con i18n ES/FR | P1: Q6 llama UNA funcion, recibe mensaje + accion + label. No reinventa | senior-fullstack |
| `resolveAudioUrl()` exportado | P1: Q8 no adivina si la URL es relativa o absoluta. Resolucion centralizada | senior-fullstack |
| `generateSessionId()` exportado | P2: Q6 importa en vez de inventar. Formato legible para debugging | algorithmic-art |
| `actionLabel` en getErrorMessage | top-design: el boton de accion en el error state necesita texto bilingue | top-design |
| No retry automatico | El retry lo decide Q6 via el `suggestedAction`. El API client no asume idempotencia | senior-fullstack |
| Health check con timeout 5s | Fail fast. Si /api/health tarda >5s, el backend esta caido | api-designer |

---

### PASO 4: Archivos de entorno

**Skill activa:** `/frontend-developer`

Crea `clara-web/.env.local` con **Write**:

```
# Backend Flask local — Clara API
NEXT_PUBLIC_API_URL=http://localhost:5000
```

Crea `clara-web/.env.example` con **Write**:

```
# Clara Web — Variables de entorno
# Copia este archivo a .env.local y ajusta los valores

# URL del backend Flask de Clara
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Verifica .gitignore:**

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && grep -q ".env.local" .gitignore || echo ".env.local" >> .gitignore
```

---

### PASO 5: Verificar build y tipos (agentes paralelos)

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
| `Cannot find name 'fetch'` | Falta lib DOM en tsconfig | Verifica `"lib": ["dom", "dom.iterable", "esnext"]` (Next.js default) |
| `Cannot find name 'OscillatorType'` | Falta lib DOM (Web Audio API types) | Mismo fix — lib DOM incluye Web Audio |
| `Module '"./types"' has no exported member 'X'` | Typo en import | Verifica que nombres exportados coinciden |
| `Type 'string' is not assignable to type 'Language'` | useState sin tipar | `useState<Language>("es")` |

---

### PASO 6: Verificacion de integridad del contrato

**Skill activa:** `/api-designer` + `/typescript-pro`

**Checklist de contrato backend ↔ frontend (15 puntos):**

**types.ts ↔ Backend:**
- [ ] `ChatRequest.text: string` → backend: `(data.get("text") or "").strip()` ✓
- [ ] `ChatRequest.language: Language` → backend: `data.get("language", "es")` ✓
- [ ] `ChatRequest.input_type: ApiInputType` → backend: `"text" | "audio" | "image"` ✓
- [ ] `ApiInputType` usa "audio" (NO "voice") — coincide con backend ✓
- [ ] `ChatRequest.audio_base64` → backend: `data.get("audio_base64")` ✓
- [ ] `ChatResponse.response: string` → backend: `response` key ✓
- [ ] `ChatResponse.source: ResponseSource` → backend: `"cache"|"llm"|"fallback"|"guardrail"` ✓
- [ ] `ChatResponse.audio_url: string | null` → backend: `audio_url` key ✓
- [ ] `ChatResponse.sources: Source[]` → backend: `[{name, url}]` ✓
- [ ] `HealthResponse.features` → backend: `{whisper, llm, guardrails, demo_mode}` ✓

**api.ts ↔ Endpoints:**
- [ ] `sendMessage()` → `POST /api/chat` con `Content-Type: application/json` ✓
- [ ] `checkHealth()` → `GET /api/health` ✓
- [ ] `API_BASE_URL` → default `http://localhost:5000` (= Flask `app.run(port=5000)`) ✓
- [ ] CORS → backend permite `http://localhost:3000` (= Next.js dev) ✓

**Helpers:**
- [ ] `resolveAudioUrl()` maneja null, relativa y absoluta ✓
- [ ] `getErrorMessage()` cubre 4 categorias x 2 idiomas = 8 mensajes ✓
- [ ] `generateSessionId()` produce formato `web_xxxxx_xxxx` ✓

**Checklist de seguridad (5 puntos):**
- [ ] No hay API keys ni tokens hardcodeados
- [ ] `API_BASE_URL` via env var, no hardcodeada en prod
- [ ] `.env.local` en `.gitignore`
- [ ] `ApiError` no expone stack traces del backend
- [ ] No hay `eval()`, `innerHTML`, ni `dangerouslySetInnerHTML`

**Checklist de diseno (4 puntos):**
- [ ] `EASING` con custom cubic-bezier (no `ease` ni `linear`)
- [ ] `DURATION` generosas para usuarios mayores (150ms instant, 500ms enter)
- [ ] `COLORS` con nombres semanticos (trust/warmth/hope)
- [ ] `AUDIO_FEEDBACK` con frecuencias relacionadas (misma familia tonal)

---

### PASO 7: Commit

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && git add clara-web/src/lib/ clara-web/.env.local clara-web/.env.example clara-web/.gitignore
git commit -m "feat: add typed API client, design constants, and i18n error system for Clara

- types.ts: Language, InputMode, ApiInputType (voice→audio mapping), ChatRequest/Response,
  HealthResponse, Message, LoadingContext, AudioPlayback, ErrorCategory, AudioFeedbackParams
- api.ts: sendMessage() + checkHealth() with timeout and defensive JSON parsing,
  ApiError with auto-categorization, getErrorMessage() ES/FR, resolveAudioUrl(),
  generateSessionId()
- constants.ts: API config, semantic COLORS (trust/warmth/hope), EASING (expo curves),
  DURATION (generous for elderly), AUDIO_FEEDBACK (Web Audio beeps)
- .env.local + .env.example for backend URL configuration
- Contract verified against src/routes/api_chat.py (POST /api/chat, GET /api/health)
- CORS-compatible (localhost:3000 → localhost:5000)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Read** | Paso 0 — leer rutas backend + models.py + app.py | Entender contrato REAL |
| **Write** | Pasos 1-4 — crear types.ts, constants.ts, api.ts, .env files | Archivos nuevos en `lib/` |
| **Bash** | Paso 5 — build + type check | Verificar compilacion |
| **Grep** | Paso 4 — verificar .gitignore | Confirmar .env.local excluido |
| **Task** | Paso 0 (lectura paralela) y Paso 5 (verificacion paralela) | `subagent_type="Explore"` o `"Bash"` |

## RESTRICCIONES ABSOLUTAS

1. **NO cambies** archivos del backend (`src/`) — solo creas archivos en `clara-web/src/lib/`
2. **NO cambies** componentes de Q3 ni pagina de Q4
3. **NO instales** librerias adicionales — fetch es nativo, TS types ya estan
4. **NO uses** axios, ky, ni wrappers de fetch — `fetch` nativo + `fetchWithTimeout` es suficiente
5. **NO agregues** retry automatico — el retry es decision de Q6 via `suggestedAction`
6. **NO agregues** cache en el cliente (React Query) — YAGNI para Fase 1
7. **NO hardcodees** URLs — todo via `API_BASE_URL`
8. **NO crees** tests unitarios — los tipos se validan con `tsc --noEmit` y el build
9. **Los tipos deben ESPEJAR el backend** — si el backend cambia, types.ts cambia
10. **NO agregues** autenticacion — la API es abierta (protegida por CORS). Auth es Fase 2
11. **`InputMode` es para UI, `ApiInputType` es para API** — nunca mezclarlos

## DEFINICION DE TERMINADO

**Backend investigado:**
- [ ] `api_chat.py`, `models.py`, `app.py` leidos y confirmados

**Archivos creados:**
- [ ] `clara-web/src/lib/types.ts` — 14+ tipos/interfaces (Language, InputMode, ApiInputType, MessageSender, ResponseSource, ChatRequest, ChatResponse, Source, HealthResponse, LoadingContext, AudioPlayback, Message, ErrorCategory, ErrorAction, AudioFeedbackParams)
- [ ] `clara-web/src/lib/constants.ts` — API_BASE_URL, COLORS (semanticos), EASING (custom curves), DURATION (generosas), AUDIO_FEEDBACK (beeps), recording limits
- [ ] `clara-web/src/lib/api.ts` — sendMessage(), checkHealth(), ApiError (auto-categorized), getErrorMessage() ES/FR, resolveAudioUrl(), generateSessionId()
- [ ] `clara-web/.env.local` — NEXT_PUBLIC_API_URL
- [ ] `clara-web/.env.example` — template documentado

**Verificaciones:**
- [ ] `.env.local` en `.gitignore`
- [ ] `npm run build` exitoso
- [ ] `npx tsc --noEmit` sin errores
- [ ] Checklist contrato (17 puntos) verificado
- [ ] Checklist seguridad (5 puntos) verificado
- [ ] Checklist diseno (4 puntos) verificado
- [ ] Commit con mensaje descriptivo

---

> **Siguiente:** Q6 usara `sendMessage()`, `Message`, `getErrorMessage()`, `generateSessionId()`, `EASING`, `DURATION` para construir la interfaz de chat.
> **Dependencias:** Este Q solo depende de Q2. Pero Q6-Q12 dependen TODOS de este Q — es la columna vertebral de datos de la app.
