# Q8: Audio Player — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q6 (Chat Interface) debe estar completado. Verifica que existen `clara-web/src/components/MessageList.tsx` (con stub de audio en lineas 93-112), `clara-web/src/lib/types.ts` (con `AudioPlayback`), `clara-web/src/lib/api.ts` (con `resolveAudioUrl`), `clara-web/src/lib/constants.ts` (con `EASING`, `DURATION`, `COLORS`).
> **Tiempo estimado:** 15-20 min

---

## PROMPT

### ROL

Eres un **ingeniero frontend senior Y disenador de interaccion de audio** construyendo el reproductor que lleva la VOZ de Clara a las personas.

Esta NO es "otra barra de progreso con play/pause". Es el momento donde **Maria de 74 anos escucha por primera vez una respuesta hablada** que le explica que tiene derecho a 500 euros/mes. Maria no lee bien — sus ojos se cansan, el texto es pequeno. Pero escuchar? Escuchar es natural. Cuando Maria toca el boton verde de play y la voz calida de Clara comienza a explicarle sus derechos, ese es el momento donde la tecnologia se convierte en compania.

Ahmed habla frances y lee despacio en espanol. El audio le permite recibir la informacion en su idioma sin esforzarse en descifrar texto. La barra de progreso le muestra cuanto falta — no hay incertidumbre.

Fatima no es alfabetizada en espanol. El texto de las burbujas es inutil para ella sin el audio. El reproductor ES su interfaz principal con Clara. Si el boton de play no es obvio, si la barra no es tocable, si no sabe que puede volver a escuchar — Fatima pierde acceso a la informacion.

Tu trabajo sigue la filosofia de diseno **"Civic Tenderness"**:

> *"El verde (#2E7D4F) es el color de puertas que se abren, de tramites completados, de futuros desbloqueados."* El boton de play verde no es un control de audio — es la promesa de que la voz de Clara esta lista para ti.

**Principio critico de audio:** El reproductor vive DENTRO de la burbuja de Clara. No es un componente externo — es parte de la respuesta. Cuando Clara responde con audio, el reproductor aparece como extension natural del mensaje, como si Clara dijera "y si prefieres, aqui puedes escucharme".

### SKILLS OBLIGATORIAS

**Capa de Diseno (invoca ANTES de escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/frontend-design` | Layout del reproductor dentro de la burbuja, proporcion controles, responsive | Al planificar estructura |
| `/top-design` | Micro-interacciones: transicion play/pause, fill de barra, feedback de velocidad | Al definir animaciones |
| `/ux-heuristics` | Validar seekability, feedback de estado, prevencion de errores, carga | Al revisar flujo |
| `/design-everyday-things` | Mapeo del modelo mental de mensaje de voz WhatsApp que Maria ya conoce | Al decidir patrones |
| `/web-typography` | Tiempo con tabular-nums, label de velocidad, tamanos legibles | Al definir tipografia |
| `/sonic-branding` | Coherencia del reproductor con identidad sonora de Clara (triangle wave) | Al validar integracion |

**Capa de Ingenieria (invoca AL escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/react-expert` | Custom hook useAudioPlayer, refs, cleanup, singleton pattern | Al implementar hook |
| `/frontend-developer` | Tailwind, responsive dentro de burbuja, touch interactions | Al implementar componente |
| `/typescript-pro` | Props tipadas, AudioPlayback integration, event typing | Al tipar hook y componente |
| `/react-best-practices` | useCallback, useRef, useEffect cleanup, event listener management | Al disenar el hook |

**Capa de Verificacion (invoca DESPUES del codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/verification-before-completion` | Checklist final antes del commit | Al terminar todo |
| `/ux-heuristics` | Test: Maria puede escuchar audio sin instrucciones? | Review final |

### ESTRATEGIA MULTI-AGENTE

```
FASE 1 — Investigacion (paralelo):
  Agente A (Explore): Lee design/02-FRONTEND-ACCESIBLE.md — wireframe 3B linea 125 "[▶ Escuchar respuesta]", specs de boton audio
  Agente B (Explore): Lee clara-web/src/lib/types.ts — AudioPlayback interface, Message.audio field
  Agente C (Explore): Lee clara-web/src/lib/api.ts — resolveAudioUrl() helper
  Agente D (Explore): Lee clara-web/src/components/MessageList.tsx — stub de audio actual (lineas 93-112), labels bilingues

FASE 2 — Implementacion (secuencial estricto):
  Tu (principal):
    1. useAudioPlayer.ts (hook — HTMLAudioElement + singleton + estado)
    2. AudioPlayer.tsx (componente visual dentro de burbuja)
    3. Modificar MessageList.tsx (reemplazar stub con AudioPlayer)

FASE 3 — Verificacion (paralelo):
  Agente E (Bash): npm run build
  Agente F (Bash): npx tsc --noEmit
```

---

### CONTEXTO TECNICO

**Clara** ya tiene el chat funcionando (Q6) con un stub de audio. Estos recursos ya existen:

#### De Q5 — Types y API:

**AudioPlayback** (`clara-web/src/lib/types.ts`):
```typescript
export interface AudioPlayback {
  url: string;
  /** Duracion total en segundos (si disponible) */
  duration_s?: number;
  /** Estado de reproduccion */
  state: "idle" | "playing" | "paused";
}
```

**Message** incluye `audio?: AudioPlayback` — NO `audio_url: string`.

**resolveAudioUrl** (`clara-web/src/lib/api.ts`):
```typescript
/** Resuelve audio_url del backend a URL completa */
export function resolveAudioUrl(audioUrl: string | null): string | null {
  if (!audioUrl) return null;
  if (audioUrl.startsWith("http")) return audioUrl;
  return `${API_BASE_URL}${audioUrl}`;
}
```

#### De Q5 — Tokens de diseno:

**Easing** (`clara-web/src/lib/constants.ts`):
```typescript
export const EASING = {
  out: "cubic-bezier(0.16, 1, 0.3, 1)",    // Entradas
  in: "cubic-bezier(0.55, 0, 1, 0.45)",     // Salidas
  inOut: "cubic-bezier(0.65, 0, 0.35, 1)",  // Transformaciones
} as const;

export const DURATION = {
  instant: 150,  // Feedback inmediato
  normal: 300,   // Transiciones normales
  enter: 500,    // Entradas de elementos
  stagger: 80,   // Stagger entre elementos
} as const;
```

**Colores semanticos:**
```typescript
export const COLORS = {
  trust: "#1B5E7B",   // Azul — confianza
  warmth: "#D46A1E",  // Naranja — calidez
  hope: "#2E7D4F",    // Verde — esperanza, success
  alert: "#C62828",   // Error
} as const;
```

#### De Q6 — Stub actual en MessageList:

**MessageList.tsx** (lineas 93-112) — esto es lo que Q8 REEMPLAZA:
```typescript
{/* Audio stub — Q8 reemplazara con AudioPlayer */}
{msg.audio && (
  <button
    className="flex items-center gap-2 mt-2 px-3 py-2
               bg-white/60 rounded-lg text-clara-blue
               min-h-touch-sm hover:bg-white/80 transition-colors duration-150"
    aria-label={l.listen}
  >
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M8 5v14l11-7z" />
    </svg>
    <span className="text-[16px] font-medium">{l.listen}</span>
  </button>
)}
```

**Labels bilingues ya definidos** (linea 16-19):
```typescript
const labels: Record<Language, { conversation: string; source: string; listen: string }> = {
  es: { conversation: "Conversacion con Clara", source: "Fuente", listen: "Escuchar respuesta" },
  fr: { conversation: "Conversation avec Clara", source: "Source", listen: "Ecouter la reponse" },
};
```

#### De Q3 — ChatBubble:

El AudioPlayer se renderiza como **children** del ChatBubble de Clara:
```typescript
<ChatBubble sender="clara" timestamp="14:32">
  <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
  {/* AudioPlayer va AQUI — dentro del children */}
  <AudioPlayer ... />
  {/* Fuentes citadas van despues */}
</ChatBubble>
```

El ChatBubble de Clara tiene fondo `bg-clara-info` (#E3F2FD). El AudioPlayer debe contrastar bien sobre este fondo azul claro.

---

### ESPECIFICACION DE DISENO

#### Wireframe del AudioPlayer (dentro de burbuja Clara):

```
┌──────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────┐│
│  │                                              ││
│  │  ┌──────┐  ┌─────────────────────┐  ┌─────┐ ││
│  │  │  ▶   │  │ ████████░░░░░░░░░░░ │  │ 1x  │ ││
│  │  │      │  │ 0:12          0:45  │  │     │ ││
│  │  │ 48px │  │   seekable bar      │  │44px │ ││
│  │  │green │  │                     │  │green│ ││
│  │  └──────┘  └─────────────────────┘  └─────┘ ││
│  │                                              ││
│  └──────────────────────────────────────────────┘│
│                                                  │
│  bg-clara-green/10 (#2E7D4F at 10%)             │
│  rounded-xl, px-3 py-2.5                        │
└──────────────────────────────────────────────────┘
```

#### Specs detallados:

| Elemento | Spec | Razon |
|----------|------|-------|
| **Contenedor** | `bg-clara-green/10 rounded-xl px-3 py-2.5 mt-2` | Fondo verde suave sobre azul claro de burbuja. Verde = esperanza |
| **Boton play/pause** | `48x48px rounded-full bg-clara-green text-white` | 48px = min-h-touch-sm. Verde solido para maximo contraste |
| **Icono play** | SVG 24px, triangulo `M8 5v14l11-7z` | Triangulo clasico universal |
| **Icono pause** | SVG 24px, dos barras `M6 19h4V5H6v14zm8-14v14h4V5h-4z` | Swap instantaneo (no morph — simplicidad) |
| **Barra de progreso** | `h-2 rounded-full bg-clara-border` (track), `bg-clara-green` (fill) | 8px de alto para ser tocable. Track gris, fill verde |
| **Zona seekable** | `h-8 cursor-pointer` (area tactil invisible 32px sobre la barra de 8px) | Area de toque generosa para Maria |
| **Tiempo actual** | `text-[13px] tabular-nums text-clara-text-secondary` | tabular-nums para digitos estables. Gris secundario |
| **Tiempo total** | Igual que actual | Alineado a la derecha |
| **Boton velocidad** | `min-w-[44px] min-h-[44px] text-[14px] font-bold text-clara-green border border-clara-green/30 rounded-lg` | 44px minimo. Borde suave, texto bold verde |
| **Velocidades** | `[0.75, 1, 1.25]` — ciclo al tocar | 3 velocidades. 0.75x para Maria, 1.25x para Ahmed |

#### Estados del reproductor:

| Estado | Visual | Aria |
|--------|--------|------|
| **idle** | Icono play, barra vacia, "0:00 / 0:45" | `aria-label="Escuchar respuesta, 45 segundos"` |
| **loading** | Icono play disabled, barra con pulse animation | `aria-busy="true"` |
| **playing** | Icono pause, barra llenandose, tiempo avanza | `aria-label="Pausar audio"` |
| **paused** | Icono play, barra parcial, tiempo congelado | `aria-label="Continuar audio"` |
| **ended** | Icono replay (flecha circular), barra llena | `aria-label="Volver a escuchar"` |
| **error** | Icono play tachado, texto "Audio no disponible" | `role="alert"` |

---

### PASO 1 — Hook useAudioPlayer

**Crear** `clara-web/src/hooks/useAudioPlayer.ts`

**Responsabilidades:**
1. Gestionar una sola instancia de HTMLAudioElement
2. **Singleton global**: solo un audio reproduciendose a la vez en toda la app (si Maria toca play en mensaje 2, mensaje 1 se pausa automaticamente)
3. Exponer estado reactivo: isPlaying, progress (0-100), currentTime, duration, isLoading, hasError, hasEnded
4. Funciones: play, pause, togglePlay, seek(percent), cycleSpeed
5. Cleanup en unmount

```typescript
"use client";

import { useState, useRef, useEffect, useCallback } from "react";

/* ------------------------------------------------------------------ */
/*  Singleton: solo un audio a la vez en toda la app                  */
/* ------------------------------------------------------------------ */

let activePlayer: HTMLAudioElement | null = null;
let activeCleanup: (() => void) | null = null;

function claimPlayback(
  audio: HTMLAudioElement,
  cleanup: () => void,
): void {
  if (activePlayer && activePlayer !== audio) {
    activePlayer.pause();
    activeCleanup?.();
  }
  activePlayer = audio;
  activeCleanup = cleanup;
}

function releasePlayback(audio: HTMLAudioElement): void {
  if (activePlayer === audio) {
    activePlayer = null;
    activeCleanup = null;
  }
}

/* ------------------------------------------------------------------ */
/*  Velocidades                                                       */
/* ------------------------------------------------------------------ */

const SPEEDS = [0.75, 1, 1.25] as const;
type Speed = (typeof SPEEDS)[number];

/* ------------------------------------------------------------------ */
/*  Estado del reproductor                                            */
/* ------------------------------------------------------------------ */

interface PlayerState {
  isPlaying: boolean;
  isLoading: boolean;
  hasError: boolean;
  hasEnded: boolean;
  progress: number;       // 0-100
  currentTime: number;    // segundos
  duration: number;       // segundos
  speed: Speed;
}

const INITIAL_STATE: PlayerState = {
  isPlaying: false,
  isLoading: true,
  hasError: false,
  hasEnded: false,
  progress: 0,
  currentTime: 0,
  duration: 0,
  speed: 1,
};

/* ------------------------------------------------------------------ */
/*  Hook                                                              */
/* ------------------------------------------------------------------ */

export function useAudioPlayer(src: string) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [state, setState] = useState<PlayerState>(INITIAL_STATE);
  const speedIdxRef = useRef(1); // indice en SPEEDS

  // Crear audio element una sola vez
  useEffect(() => {
    const audio = new Audio();
    audio.preload = "metadata";
    audio.src = src;
    audioRef.current = audio;

    /* --- Event listeners --- */

    const onLoadedMetadata = () => {
      setState((s) => ({
        ...s,
        duration: audio.duration || 0,
        isLoading: false,
      }));
    };

    const onTimeUpdate = () => {
      const progress = audio.duration
        ? (audio.currentTime / audio.duration) * 100
        : 0;
      setState((s) => ({
        ...s,
        currentTime: audio.currentTime,
        progress,
      }));
    };

    const onPlay = () => {
      setState((s) => ({ ...s, isPlaying: true, hasEnded: false }));
    };

    const onPause = () => {
      setState((s) => ({ ...s, isPlaying: false }));
    };

    const onEnded = () => {
      setState((s) => ({
        ...s,
        isPlaying: false,
        hasEnded: true,
        progress: 100,
      }));
      releasePlayback(audio);
    };

    const onError = () => {
      setState((s) => ({
        ...s,
        isLoading: false,
        hasError: true,
        isPlaying: false,
      }));
      releasePlayback(audio);
    };

    const onWaiting = () => {
      setState((s) => ({ ...s, isLoading: true }));
    };

    const onCanPlay = () => {
      setState((s) => ({ ...s, isLoading: false }));
    };

    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("error", onError);
    audio.addEventListener("waiting", onWaiting);
    audio.addEventListener("canplay", onCanPlay);

    return () => {
      audio.pause();
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("error", onError);
      audio.removeEventListener("waiting", onWaiting);
      audio.removeEventListener("canplay", onCanPlay);
      releasePlayback(audio);
      audio.src = "";
      audioRef.current = null;
    };
  }, [src]);

  /* --- Acciones --- */

  const togglePlay = useCallback(async () => {
    const audio = audioRef.current;
    if (!audio || state.hasError) return;

    if (state.hasEnded) {
      audio.currentTime = 0;
    }

    if (audio.paused) {
      claimPlayback(audio, () => {
        setState((s) => ({ ...s, isPlaying: false }));
      });
      try {
        await audio.play();
      } catch {
        // Browser blocked autoplay — ignore, user will retry
      }
    } else {
      audio.pause();
    }
  }, [state.hasError, state.hasEnded]);

  const seek = useCallback((percent: number) => {
    const audio = audioRef.current;
    if (!audio || !audio.duration) return;
    const clamped = Math.max(0, Math.min(100, percent));
    audio.currentTime = (clamped / 100) * audio.duration;
    setState((s) => ({
      ...s,
      progress: clamped,
      currentTime: audio.currentTime,
      hasEnded: false,
    }));
  }, []);

  const cycleSpeed = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;
    const nextIdx = (speedIdxRef.current + 1) % SPEEDS.length;
    speedIdxRef.current = nextIdx;
    const newSpeed = SPEEDS[nextIdx];
    audio.playbackRate = newSpeed;
    setState((s) => ({ ...s, speed: newSpeed }));
  }, []);

  return {
    ...state,
    togglePlay,
    seek,
    cycleSpeed,
  };
}
```

**Decisiones de diseno del hook:**

1. **Singleton via modulo** (`activePlayer`): Si Maria toca play en un segundo mensaje, el primero se pausa automaticamente. Esto evita confusion de "dos voces hablando a la vez". Es el patron de WhatsApp.

2. **`new Audio()` en vez de `<audio>` JSX**: Permite crear el elemento sin renderizarlo en el DOM. Mas limpio para un hook headless.

3. **`onError` handler**: Si el URL es invalido o la red falla, `hasError = true` muestra estado de error en vez de spinner infinito.

4. **`onWaiting` / `onCanPlay`**: Detecta buffering mid-playback (red lenta) y muestra indicador de carga.

5. **Replay en `hasEnded`**: Si el audio termino y Maria toca play, se reinicia desde el principio.

6. **Cleanup completo**: En unmount, pausa audio, remueve listeners, libera singleton, limpia src.

---

### PASO 2 — Componente AudioPlayer

**Crear** `clara-web/src/components/ui/AudioPlayer.tsx`

```typescript
"use client";

import { useCallback, useRef } from "react";
import { useAudioPlayer } from "@/hooks/useAudioPlayer";
import type { Language } from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Labels bilingues                                                  */
/* ------------------------------------------------------------------ */

const labels = {
  es: {
    play: "Escuchar respuesta",
    playWithDuration: (d: string) => `Escuchar respuesta, ${d}`,
    pause: "Pausar audio",
    resume: "Continuar audio",
    replay: "Volver a escuchar",
    speed: (s: number) => `Velocidad ${s} equis`,
    error: "Audio no disponible",
    loading: "Cargando audio...",
  },
  fr: {
    play: "Ecouter la reponse",
    playWithDuration: (d: string) => `Ecouter la reponse, ${d}`,
    pause: "Mettre en pause",
    resume: "Reprendre l'audio",
    replay: "Reecouter",
    speed: (s: number) => `Vitesse ${s} fois`,
    error: "Audio non disponible",
    loading: "Chargement de l'audio...",
  },
} as const;

/* ------------------------------------------------------------------ */
/*  Utilidad: formatear tiempo                                        */
/* ------------------------------------------------------------------ */

function formatTime(seconds: number): string {
  if (!isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

/* ------------------------------------------------------------------ */
/*  Props                                                             */
/* ------------------------------------------------------------------ */

interface AudioPlayerProps {
  /** URL resuelta del audio (ya procesada con resolveAudioUrl) */
  src: string;
  /** Idioma para labels bilingues */
  language: Language;
}

/* ------------------------------------------------------------------ */
/*  Componente                                                        */
/* ------------------------------------------------------------------ */

export default function AudioPlayer({ src, language }: AudioPlayerProps) {
  const {
    isPlaying,
    isLoading,
    hasError,
    hasEnded,
    progress,
    currentTime,
    duration,
    speed,
    togglePlay,
    seek,
    cycleSpeed,
  } = useAudioPlayer(src);

  const progressBarRef = useRef<HTMLDivElement>(null);
  const l = labels[language];

  /* --- Seek al hacer click/touch en la barra --- */

  const handleSeek = useCallback(
    (e: React.MouseEvent<HTMLDivElement> | React.TouchEvent<HTMLDivElement>) => {
      const bar = progressBarRef.current;
      if (!bar || !duration) return;

      let clientX: number;
      if ("touches" in e) {
        clientX = e.touches[0].clientX;
      } else {
        clientX = e.clientX;
      }

      const rect = bar.getBoundingClientRect();
      const percent = ((clientX - rect.left) / rect.width) * 100;
      seek(percent);
    },
    [seek, duration],
  );

  /* --- Keyboard en la barra de progreso --- */

  const handleProgressKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "ArrowRight") {
        e.preventDefault();
        seek(Math.min(100, progress + 5)); // +5%
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        seek(Math.max(0, progress - 5)); // -5%
      }
    },
    [seek, progress],
  );

  /* --- Aria label dinamico para play/pause --- */

  const playButtonLabel = (() => {
    if (hasError) return l.error;
    if (hasEnded) return l.replay;
    if (isPlaying) return l.pause;
    if (progress > 0) return l.resume;
    if (duration > 0) return l.playWithDuration(formatTime(duration));
    return l.play;
  })();

  /* --- Estado de error --- */

  if (hasError) {
    return (
      <div
        className="flex items-center gap-3 bg-clara-alert/10 rounded-xl px-3 py-2.5 mt-2"
        role="alert"
      >
        <div className="min-w-[48px] min-h-[48px] flex items-center justify-center
                        bg-clara-text-secondary/20 rounded-full">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"
               className="text-clara-text-secondary" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-2h2v2h-2zm0-4V7h2v6h-2z" />
          </svg>
        </div>
        <span className="text-[16px] text-clara-text-secondary">{l.error}</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3 bg-clara-green/10 rounded-xl px-3 py-2.5 mt-2">
      {/* ---- Boton Play/Pause ---- */}
      <button
        onClick={togglePlay}
        disabled={isLoading && !isPlaying}
        aria-label={playButtonLabel}
        className="min-w-[48px] min-h-[48px] flex items-center justify-center
                   bg-clara-green text-white rounded-full shrink-0
                   hover:bg-[#256B42] active:scale-95
                   transition-[background-color,transform] duration-150
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-green focus-visible:outline-offset-2
                   disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading && !isPlaying ? (
          /* Spinner de carga — 3 dots animados */
          <div className="flex gap-1" aria-hidden="true">
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse [animation-delay:150ms]" />
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse [animation-delay:300ms]" />
          </div>
        ) : hasEnded ? (
          /* Icono replay */
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" />
          </svg>
        ) : isPlaying ? (
          /* Icono pause */
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
          </svg>
        ) : (
          /* Icono play */
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M8 5v14l11-7z" />
          </svg>
        )}
      </button>

      {/* ---- Barra de progreso + tiempo ---- */}
      <div className="flex-1 min-w-0">
        {/* Zona seekable — area tactil de 32px, barra visual de 8px */}
        <div
          ref={progressBarRef}
          role="slider"
          aria-label={language === "es" ? "Progreso del audio" : "Progression de l'audio"}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(progress)}
          tabIndex={0}
          onClick={handleSeek}
          onTouchStart={handleSeek}
          onKeyDown={handleProgressKeyDown}
          className="relative h-8 flex items-center cursor-pointer group
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-green focus-visible:outline-offset-1
                     rounded"
        >
          {/* Track */}
          <div className="w-full h-2 bg-clara-border rounded-full overflow-hidden">
            {/* Fill */}
            <div
              className="h-full bg-clara-green rounded-full transition-[width] duration-200 ease-linear"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Tiempo */}
        <div className="flex justify-between text-[13px] text-clara-text-secondary -mt-1">
          <span className="tabular-nums">{formatTime(currentTime)}</span>
          <span className="tabular-nums">{formatTime(duration)}</span>
        </div>
      </div>

      {/* ---- Boton velocidad ---- */}
      <button
        onClick={cycleSpeed}
        aria-label={l.speed(speed)}
        className="min-w-[44px] min-h-[44px] flex items-center justify-center shrink-0
                   text-[14px] font-bold text-clara-green tabular-nums
                   border border-clara-green/30 rounded-lg
                   hover:bg-clara-green/10 active:scale-95
                   transition-[background-color,transform] duration-150
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-green focus-visible:outline-offset-2"
      >
        {speed}x
      </button>
    </div>
  );
}
```

**Decisiones de diseno del componente:**

1. **Swap de iconos (no morph)**: Play → Pause → Replay son iconos distintos con swap instantaneo. Morph animations serian confusas para Maria — ella necesita ver claramente "triangulo = puedo escuchar" y "dos barras = esta sonando".

2. **Barra seekable con zona tactil de 32px**: La barra visible es 8px (`h-2`), pero la zona de click/touch es 32px (`h-8`). Para Maria con temblor, poder tocar "cerca de la barra" y que funcione es critico.

3. **Keyboard navigation en barra**: `role="slider"` con `ArrowLeft`/`ArrowRight` para navegar ±5%. Tab llega a la barra. Cumple WCAG 2.1.

4. **Estado `hasEnded` con icono replay**: Cuando el audio termina, el boton cambia a icono de replay (flecha circular). Maria ve inmediatamente que puede volver a escuchar. No es ambiguo.

5. **Estado de error dedicado**: Si la URL falla, se muestra un contenedor rojo suave con "Audio no disponible" en vez de un spinner infinito o un boton roto.

6. **Loading con dots**: Mientras carga metadata, 3 dots animados dentro del boton verde (no un spinner generico). Coherente con LoadingState de Clara.

7. **`tabular-nums`** en tiempos y velocidad: Los numeros no saltan cuando cambian (0:09 → 0:10). Inter tiene soporte nativo.

8. **`active:scale-95`** en botones: Feedback tactil al tocar. Sutil pero confirma la accion.

9. **`focus-visible:outline`** con 3px verde: Visible para navegacion por teclado, no aparece al hacer click. Coherente con Q7.

10. **`prefers-reduced-motion`**: La transicion de la barra usa `duration-200 ease-linear`. Si el usuario tiene `prefers-reduced-motion: reduce`, Tailwind automaticamente desactiva la transition (`motion-reduce:transition-none` podria agregarse si es necesario, pero `ease-linear` en la barra es funcional, no decorativo — NO se debe desactivar).

---

### PASO 3 — Integrar en MessageList

**Modificar** `clara-web/src/components/MessageList.tsx`

#### 3a. Agregar import (al inicio del archivo):

```typescript
import AudioPlayer from "@/components/ui/AudioPlayer";
import { resolveAudioUrl } from "@/lib/api";
```

#### 3b. Agregar `language` a labels que necesita AudioPlayer:

El componente ya recibe `language` como prop — no hay cambio necesario.

#### 3c. Reemplazar el stub de audio (lineas 93-112):

**BORRAR** todo el bloque:
```typescript
{/* Audio stub — Q8 reemplazara con AudioPlayer */}
{msg.audio && (
  <button
    className="flex items-center gap-2 mt-2 px-3 py-2
               bg-white/60 rounded-lg text-clara-blue
               min-h-touch-sm hover:bg-white/80 transition-colors duration-150"
    aria-label={l.listen}
  >
    <svg ... />
    <span ...>{l.listen}</span>
  </button>
)}
```

**REEMPLAZAR** con:
```typescript
{/* Audio player — reproduccion de respuesta de Clara */}
{msg.audio && msg.audio.url && (
  <AudioPlayer
    src={resolveAudioUrl(msg.audio.url) || msg.audio.url}
    language={language}
  />
)}
```

**Nota critica sobre tipos:** El campo `msg.audio` es `AudioPlayback | undefined`. AudioPlayback tiene `url: string`. Usamos `resolveAudioUrl()` para resolver URLs relativas del backend (`/static/cache/imv.mp3` → `http://localhost:5000/static/cache/imv.mp3`).

---

### PASO 4 — Verificar build

```bash
cd clara-web && npm run build
```

Debe compilar sin errores.

```bash
npx tsc --noEmit
```

Debe pasar sin errores de tipos.

---

### PASO 5 — Test manual

```bash
cd clara-web && npm run dev
```

Abrir `http://localhost:3000/chat`. Enviar pregunta que devuelva audio (ej: "Que es el IMV?" si el backend tiene cache con audio).

**Checklist de Maria (74 anos, temblor):**

| # | Test | Esperado |
|---|------|----------|
| 1 | Burbuja de Clara muestra reproductor | Barra verde suave visible debajo del texto |
| 2 | Boton play es verde, grande, circular | 48px, verde solido, icono triangulo blanco |
| 3 | Tocar play → audio suena | Voz de Clara se escucha. Icono cambia a pause |
| 4 | Tocar pause → audio se detiene | Silencio. Icono vuelve a play. Barra queda parcial |
| 5 | Barra de progreso avanza | Fill verde crece de izquierda a derecha suavemente |
| 6 | Tiempo se actualiza | "0:12 / 0:45" — numeros estables (no saltan) |
| 7 | Tocar barra → seek | Audio salta a posicion tocada. Barra se ajusta |
| 8 | Boton velocidad cicla | "0.75x" → "1x" → "1.25x" → "0.75x" |
| 9 | Audio termina → icono replay | Flecha circular. Barra llena al 100% |
| 10 | Tocar replay → audio reinicia | Audio desde el principio. Barra vuelve a 0% |
| 11 | Play en mensaje 2 → mensaje 1 se pausa | Solo un audio suena a la vez |
| 12 | Tab navega a play, barra, velocidad | Outline verde 3px en cada control |
| 13 | Space/Enter en play → toggle | Funciona identico a click |
| 14 | ArrowLeft/Right en barra → seek | Avanza/retrocede 5% |
| 15 | URL invalida → error | "Audio no disponible" en contenedor rojo suave |

---

### PASO 6 — Commit

```bash
git add \
  clara-web/src/hooks/useAudioPlayer.ts \
  clara-web/src/components/ui/AudioPlayer.tsx \
  clara-web/src/components/MessageList.tsx

git commit -m "feat(Q8): add AudioPlayer with play/pause, seekable progress, speed control

- useAudioPlayer hook with singleton pattern (one audio at a time)
- AudioPlayer component: play/pause/replay, seekable bar (32px touch zone),
  speed cycle (0.75x/1x/1.25x), bilingual labels (es/fr)
- Replaces stub in MessageList with full player inside Clara bubbles
- Error state, loading dots, ended→replay, keyboard nav (Arrow seek)
- tabular-nums for stable time display, focus-visible outlines
- Uses resolveAudioUrl(), COLORS.hope green, bg-clara-green/10 container"
```

---

## CHECKLIST DE ACCESIBILIDAD

| # | Requisito | Implementacion |
|---|-----------|----------------|
| 1 | Touch targets 48px+ | Play: 48px, Speed: 44px, Seek zone: 32px alto |
| 2 | Keyboard navigable | Tab order: play → progress slider → speed. Space/Enter toggle |
| 3 | Screen reader labels | Aria-labels bilingues dinamicos por estado |
| 4 | Progress slider ARIA | `role="slider"`, `aria-valuenow`, `aria-valuemin/max` |
| 5 | Error anunciado | `role="alert"` en estado de error |
| 6 | Loading anunciado | `disabled` en boton + dots visuales |
| 7 | Focus visible | 3px outline verde, offset 2px |
| 8 | Color no es unica info | Iconos (play/pause/replay) cambian de forma, no solo color |
| 9 | Contraste | Verde #2E7D4F sobre bg-clara-green/10 = ratio 5.2:1+ |
| 10 | prefers-reduced-motion | Barra usa ease-linear (funcional). Botones: transition instantanea ya es 150ms |

---

## DEFINICION DE TERMINADO

Q8 esta **completo** cuando:

1. `useAudioPlayer.ts` con singleton, error handling, seek, speed, ended
2. `AudioPlayer.tsx` con play/pause/replay, seekable bar, speed cycle, error state, bilingual labels
3. `MessageList.tsx` reemplaza stub con `<AudioPlayer>` usando `resolveAudioUrl()`
4. Singleton funciona: play en mensaje N pausa mensaje N-1
5. Barra seekable por click/touch Y por teclado (ArrowLeft/Right)
6. Tiempo con `tabular-nums` (digitos estables)
7. Focus-visible 3px verde en TODOS los controles interactivos
8. Error state muestra "Audio no disponible" (no spinner infinito)
9. Build sin errores, types sin errores
10. Test de Maria pasa los 15 puntos del checklist
