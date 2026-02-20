# Q7: Grabacion de Voz — Prompt Definitivo para Claude Code

> **Instrucciones:** Copia y pega TODO este contenido como primer mensaje en una nueva sesion de Claude Code.
> **Directorio de trabajo:** `/Users/andreaavila/Documents/hakaton/civicaid-voice`
> **Prerequisito:** Q5 (API Client + Constants) y Q6 (Chat Interface) deben estar completados. Verifica que existen `clara-web/src/lib/constants.ts` (con `AUDIO_FEEDBACK`, `MAX_RECORDING_SECONDS`), `clara-web/src/hooks/useChat.ts`, `clara-web/src/app/chat/page.tsx`.
> **Tiempo estimado:** 20-30 min

---

## PROMPT

### ROL

Eres un **ingeniero frontend senior Y disenador de interaccion de audio** construyendo la **via de entrada PRIMARIA** de Clara: la voz. Para Maria de 74 anos, Ahmed que escribe frances en teclado espanol, y Fatima que no es alfabetizada en espanol — escribir es el fallback. Hablar es lo natural.

Esta NO es "otra pantalla de grabacion". Es el momento donde **Maria de 74 anos va a hablar por primera vez con un sistema digital** y descubrir que la entiende. Maria no puede escribir rapido — sus dedos tiemblan, las teclas son pequenas, la autocorreccion la confunde. Pero hablar? Hablar es lo mas natural que existe. Cuando Maria toca el boton de microfono y escucha el beep suave que confirma "te estoy escuchando", cuando ve la onda naranja que se mueve con su voz, cuando el timer le dice cuanto lleva — ese es el momento donde la tecnologia desaparece y solo queda una persona pidiendo ayuda.

Ahmed habla frances con acento senegales. Escribir en frances en un teclado espanol es frustrante. Pero hablar? Ahmed habla su frances y Clara lo entiende. La grabacion de voz elimina la barrera del teclado.

Fatima no es alfabetizada en espanol — no puede escribir su pregunta, pero puede hablarla perfectamente. El mecanismo es **toggle**: un toque para empezar, otro para parar. Es diferente a WhatsApp (press-and-hold), pero MEJOR para manos que tiemblan. Las instrucciones explicitas ("Toca para grabar" / "Toca para parar") guian el nuevo patron.

Tu trabajo sigue la filosofia de diseno **"Civic Tenderness"**:

> *"Cada elemento lleva el peso de la necesidad — construido, al final, para la persona." El boton del microfono no es una affordance — es una declaracion de que la mano que lo toca importa, sin importar su firmeza.*

**Principio critico de voz:** La comunicacion es *"ondas concentricas de una voz que finalmente es escuchada"*. La onda animada naranja no es decoracion — es la representacion visual de que la voz de Maria esta siendo capturada. El beep no es un sonido de sistema — es Clara diciendo "estoy aqui".

### SKILLS OBLIGATORIAS

**Capa de Diseno (invoca ANTES de escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/frontend-design` | Layout de pantalla de grabacion, composicion overlay, zona de controles | Al planificar estructura |
| `/top-design` | Animacion de onda de audio, choreografia de entrada del overlay, pulse del mic | Al definir animaciones |
| `/ux-heuristics` | Validar toggle vs press-and-hold, feedback de estado, prevencion de errores | Al revisar flujo de interaccion |
| `/design-everyday-things` | Mapeo del modelo mental WhatsApp (audio message) que Maria ya tiene | Al decidir patrones |
| `/web-typography` | Texto "Habla ahora" legible, timer tabular-nums, labels de botones | Al definir tipografia |
| `/brand-guidelines` | Consistencia con identidad Clara, onda naranja como acento calido | Al validar colores y tono |
| `/sonic-branding` | Beeps de recordStart/recordStop como identidad sonora de Clara | Al implementar audio feedback |

**Capa de Ingenieria (invoca AL escribir codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/react-expert` | Custom hook con MediaRecorder, refs, cleanup, Promise<string> | Al implementar useAudioRecorder |
| `/frontend-developer` | CSS animations, z-index overlay, responsive, transition choreography | Al implementar VoiceRecorder |
| `/typescript-pro` | Tipado estricto, interface RecorderState, Promise typing | Al tipar hook y componente |
| `/react-best-practices` | useCallback, useRef, useEffect cleanup, memory leak prevention | Al disenar el hook |

**Capa de Verificacion (invoca DESPUES del codigo):**

| Skill | Proposito | Cuando |
|-------|-----------|--------|
| `/verification-before-completion` | Checklist final antes del commit | Al terminar todo |
| `/lighthouse-audit` | Validar accesibilidad del overlay y controles | Post-build |
| `/ux-heuristics` | Test: Maria puede grabar sin instrucciones? | Review final |

### ESTRATEGIA MULTI-AGENTE

```
FASE 1 — Investigacion (paralelo):
  Agente A (Explore): Lee design/02-FRONTEND-ACCESIBLE.md — wireframe 3C (grabacion), specs de tamano, patron de interaccion de voz
  Agente B (Explore): Lee design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md — la onda como "voz finalmente escuchada"
  Agente C (Explore): Lee clara-web/src/lib/constants.ts — AUDIO_FEEDBACK, MAX_RECORDING_SECONDS, RECORDING_WARNING_SECONDS, EASING, DURATION
  Agente D (Explore): Lee clara-web/src/app/chat/page.tsx + clara-web/src/components/ChatInput.tsx — stubs actuales de voz (alert), onStartVoice, activeMode

FASE 2 — Implementacion (secuencial estricto):
  Tu (principal):
    1. useAudioRecorder.ts (hook — MediaRecorder + timer + base64)
    2. VoiceRecorder.tsx (overlay full-screen + onda + mic + controles)
    3. Modificar chat/page.tsx (integrar VoiceRecorder, reemplazar alert stub)

FASE 3 — Verificacion (paralelo):
  Agente E (Bash): npm run build
  Agente F (Bash): npx tsc --noEmit
```

---

### CONTEXTO TECNICO

**Clara** ya tiene el chat funcionando (Q6). Estos recursos ya existen:

#### De Q5 — Constants de audio:

**Constants** (`clara-web/src/lib/constants.ts`):
```typescript
// Audio feedback — beeps via Web Audio API (zero dependencies)
export const AUDIO_FEEDBACK: Record<string, AudioFeedbackParams> = {
  /** Beep al iniciar — A4 ascendente, triangulo calido, 200ms */
  recordStart: { frequency: 440, duration: 200, type: "triangle" },
  /** Beep al parar — F4 descendente, triangulo calido, 200ms */
  recordStop: { frequency: 349, duration: 200, type: "triangle" },
  /** Beep de aviso a 50s — doble pulso A4, urgencia suave */
  recordWarning: { frequency: 440, duration: 120, type: "triangle" },
  /** Sonido sutil de mensaje enviado — C5 */
  messageSent: { frequency: 523, duration: 100, type: "triangle" },
};

export const MAX_RECORDING_SECONDS = 60;
export const RECORDING_WARNING_SECONDS = 50;

// Motion
EASING.out  = "cubic-bezier(0.16, 1, 0.3, 1)"   // entrada de elementos
DURATION.enter   = 500    // entrada de elementos
DURATION.normal  = 300    // transiciones
```

**Types** (`clara-web/src/lib/types.ts`):
```typescript
interface AudioFeedbackParams {
  frequency: number;
  duration: number;
  type: OscillatorType;
}
```

#### De Q6 — Chat (lo que este Q reemplaza):

**Stubs actuales** en `clara-web/src/app/chat/page.tsx`:
```typescript
// ESTO es lo que Q7 reemplaza:
onStartVoice={() => {
  alert(comingSoon[language]);  // → VoiceRecorder real
}}

// send() ya acepta audioBase64:
send(text: string, audioBase64?: string, imageBase64?: string)
```

**ChatInput** (`clara-web/src/components/ChatInput.tsx`):
```typescript
interface ChatInputProps {
  onStartVoice: () => void;  // Q7 conecta esto a setVoiceActive(true)
  activeMode?: "text" | "voice" | "photo";  // Q7 pasa "voice" cuando graba
  // ... otros props
}
```

**useChat.ts** — el hook ya soporta audio:
```typescript
// Cuando Q7 envia audio:
send("", audioBase64);
// → inputType = "audio", loadingContext = "listening"
// → Burbuja usuario muestra "🎤"
// → Loading: "Clara esta escuchando tu mensaje..."
```

#### De Q6 — LoadingContext para voz:
```typescript
const loadingMessages = {
  es: { listening: "Clara esta escuchando tu mensaje..." },
  fr: { listening: "Clara ecoute ton message..." },
};
```

#### Tailwind tokens disponibles:
```
Colores: clara-blue, clara-orange, clara-green, clara-bg, clara-text, clara-text-secondary,
         clara-error, clara-warning, clara-border
Fuentes: font-display (Atkinson Hyperlegible), font-body (Inter)
Texto: text-h2 (28px), text-body (20px), text-body-sm (18px), text-button (20px), text-label (16px)
Touch: touch (64px), touch-sm (48px), touch-lg (96px)
```

#### Wireframe 3C (design/02-FRONTEND-ACCESIBLE.md):
```
┌──────────────────────────────────┐
│                                  │
│         Habla ahora...           │  28px, font-display
│                                  │
│     ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋          │  onda naranja animada
│                                  │
│           ⏱ 0:05                 │  24px tabular-nums
│                                  │
│         ┌──────────┐             │
│         │          │             │
│         │   [🎤]   │             │  96x96px circular
│         │  GRANDE  │             │  rojo cuando graba
│         │          │             │  pulse animation
│         └──────────┘             │
│                                  │
│  ┌────────────┐ ┌─────────────┐  │
│  │  Cancelar  │ │   Enviar    │  │  64px alto, ~45% ancho
│  └────────────┘ └─────────────┘  │
│                                  │
└──────────────────────────────────┘
```

**Especificaciones del wireframe:**
- Texto "Habla ahora": 28px (text-h2), centro, font-display
- Onda audio: CSS animation, barras de 4px ancho, naranja `clara-orange` (#D46A1E)
- Timer: 24px tabular-nums (font-body)
- Boton microfono: 96x96px (touch-lg) circular, rojo `clara-error` (#C62828) mientras graba, pulse animation
- Botones Cancelar/Enviar: 64px (touch) alto, ~45% ancho cada uno

---

### PRINCIPIOS DE DISENO PARA VOZ

**1. Toggle, NO press-and-hold — esto no es negociable:**
Maria tiene temblor en las manos. Press-and-hold (mantener presionado) es fisicamente dificil para ella. El mecanismo es **toggle**: un toque para empezar a grabar, otro toque para parar.

> **NOTA IMPORTANTE:** Este es un modelo DIFERENTE al de WhatsApp (que usa press-and-hold). Clara usa toggle porque: (1) press-and-hold requiere fuerza sostenida que el temblor interrumpe, (2) toggle permite manos libres durante la grabacion, (3) cancel explicito es mas seguro que soltar-por-accidente. Maria necesitara aprender este nuevo patron, por eso las instrucciones son explicitas ("Toca para grabar" / "Toca para parar").

Flujo:
1. Maria toca "Voz" en ChatInput → aparece overlay
2. Maria toca el mic grande → empieza a grabar (beep ascendente)
3. Maria habla
4. Maria toca el mic de nuevo → para (beep descendente)
5. Se envia automaticamente al parar (o Maria toca "Enviar")

**2. Feedback multisensorial — visual + auditivo + textual:**
Maria necesita SABER que esta grabando. No basta con un icono rojo. Tres canales:
- **Visual:** Boton rojo + onda animada + timer corriendo
- **Auditivo:** Beep al empezar (440Hz, ascendente = "empieza"), beep al parar (349Hz, descendente = "listo")
- **Textual:** "Habla ahora..." cambia a "Toca para parar" — descripcion explicita

**3. Overlay full-screen — sin distracciones:**
La grabacion es un **momento dedicado**. No es un popover ni un bottom sheet. Es una pantalla completa que dice "ahora solo importa tu voz". Fondo `clara-bg` (no negro, no blur — calido y seguro). z-50 sobre todo. Clara desaparece visualmente y solo queda la interfaz de escucha.

**4. El limite de 60 segundos es proteccion, no restriccion:**
Backend Whisper tiene timeout. 60 segundos es generoso para una pregunta. A los 50 segundos, el timer se pone rojo y el texto avisa. A los 60, para automaticamente y envia. Maria no se queda grabando sin saber que se acabo.

**5. El error de microfono es una conversacion:**
Si Maria niega permiso de microfono (o el browser no soporta), NO mostrar un alert. Mostrar un error amable dentro del overlay: "No se pudo acceder al microfono. Asegurate de dar permiso en tu navegador." Incluir boton "Probar de nuevo" o "Escribir en su lugar".

**6. La onda animada es la promesa de que te escuchamos:**
12 barras naranja que pulsan con ritmo stagger. Cada barra tiene delay diferente para simular movimiento organico. No es un visualizer real del audio (demasiado complejo, innecesario). Es una **representacion simbolica** de "tu voz esta siendo capturada". Las ondas son las "ondas concentricas de una voz finalmente escuchada" de Civic Tenderness.

**7. Web Audio API para beeps — zero dependencies:**
Los beeps usan OscillatorNode (Web Audio API nativo). No cargar archivos MP3. Q5 definio las frecuencias en `AUDIO_FEEDBACK`. Crear una funcion `playBeep()` que usa AudioContext + OscillatorNode.

**8. Cancel es siempre posible — nunca atrapar al usuario:**
El boton "Cancelar" esta siempre visible. No hay momento donde Maria no pueda salir. Cancelar descarta la grabacion sin enviar. El boton "atras" del navegador tambien cierra el overlay (no romper la navegacion).

---

## EJECUCION PASO A PASO

### PASO 0: Investigar antes de crear

**Lanza CUATRO agentes Explore en paralelo:**

**Agente A:** Lee `design/02-FRONTEND-ACCESIBLE.md` — extrae wireframe 3C (grabacion de voz), specs de tamano (96px mic, 64px botones, 28px titulo), patron de interaccion toggle.

**Agente B:** Lee `design/assets/CIVIC-TENDERNESS-PHILOSOPHY.md` — internaliza: "ondas concentricas de una voz que finalmente es escuchada". El boton del microfono es "una declaracion de que la mano que lo toca importa".

**Agente C:** Lee `clara-web/src/lib/constants.ts` — confirma `AUDIO_FEEDBACK` (recordStart: 440Hz, recordStop: 349Hz), `MAX_RECORDING_SECONDS` (60), `RECORDING_WARNING_SECONDS` (50), `EASING`, `DURATION`.

**Agente D:** Lee `clara-web/src/app/chat/page.tsx` + `clara-web/src/components/ChatInput.tsx` — confirma: `onStartVoice` prop, `send("", audioBase64)` ya funciona, `activeMode` prop existe, el `alert()` stub a reemplazar.

---

### PASO 1: useAudioRecorder.ts — "El oido de Clara"

**Skills activas:** `/react-best-practices` + `/typescript-pro` + `/react-expert`

**Briefing de arquitectura:**
Este hook encapsula toda la complejidad de MediaRecorder: permisos, chunks, timer, conversion a base64, cleanup de streams. El componente VoiceRecorder solo ve: `isRecording`, `seconds`, `isWarning`, `error`, `start()`, `stop()`, `cancel()`.

**Decisiones clave ANTES de escribir:**
- `start()` es async — pide permiso de microfono
- `stop()` retorna `Promise<string>` — base64 del audio
- `cancel()` descarta todo sin retornar audio
- Timer con `setInterval(1000)` — actualiza `seconds` cada segundo
- Warning a `RECORDING_WARNING_SECONDS` (50s) — `isWarning: true`
- Auto-stop a `MAX_RECORDING_SECONDS` (60s) — llama cleanup
- MIME: `audio/webm;codecs=opus` preferido, fallback `audio/webm`
- `recorder.start(100)` — chunks cada 100ms para no perder audio
- Cleanup en `useEffect` return — NUNCA dejar stream abierto
- Beep con `playBeep()` helper que usa Web Audio API

Crea `clara-web/src/hooks/useAudioRecorder.ts` con **Write**:

```typescript
"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import {
  AUDIO_FEEDBACK,
  MAX_RECORDING_SECONDS,
  RECORDING_WARNING_SECONDS,
} from "@/lib/constants";
import type { AudioFeedbackParams } from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Audio feedback — Web Audio API beep (zero dependencies)            */
/* ------------------------------------------------------------------ */

/** AudioContext reusable — reusar evita Safari "user gesture" policy en auto-stop */
let sharedAudioCtx: AudioContext | null = null;

function getAudioContext(): AudioContext {
  if (!sharedAudioCtx || sharedAudioCtx.state === "closed") {
    sharedAudioCtx = new AudioContext();
  }
  // Resume si esta suspendido (Safari policy)
  if (sharedAudioCtx.state === "suspended") {
    sharedAudioCtx.resume();
  }
  return sharedAudioCtx;
}

function playBeep(params: AudioFeedbackParams): void {
  try {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const now = ctx.currentTime;
    const dur = params.duration / 1000;

    osc.type = params.type;
    osc.frequency.value = params.frequency;

    // Amplitude envelope — "rounded corners for sound" (Civic Tenderness)
    // 20ms attack ramp: silence → 0.3 (no click al inicio)
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.3, now + 0.02);
    // 30ms release ramp: 0.3 → silence (no click al final)
    gain.gain.linearRampToValueAtTime(0, now + dur);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + dur + 0.01); // +10ms buffer para release

    // Haptic feedback — tercer canal sensorial (no soportado en iOS Safari)
    if (navigator.vibrate) navigator.vibrate(50);
  } catch {
    // AudioContext no soportado — silencio graceful
  }
}

/* ------------------------------------------------------------------ */
/*  Estado del recorder                                                */
/* ------------------------------------------------------------------ */

interface RecorderState {
  isRecording: boolean;
  seconds: number;
  isWarning: boolean;
  error: string | null;
}

/* ------------------------------------------------------------------ */
/*  Hook                                                              */
/* ------------------------------------------------------------------ */

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

  /* ---- Cleanup: para grabacion + cierra tracks ---- */
  const cleanup = useCallback(() => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    mediaRecorderRef.current?.stream
      .getTracks()
      .forEach((track) => track.stop());
  }, []);

  /* ---- Cleanup al desmontar — NUNCA dejar stream abierto ---- */
  useEffect(() => {
    return cleanup;
  }, [cleanup]);

  /* ---- Start: pide microfono, inicia grabacion ---- */
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

      // Handler de error mid-recording (stream interrumpido, bluetooth desconectado, etc.)
      recorder.onerror = () => {
        cleanup();
        setState((prev) => ({
          ...prev,
          isRecording: false,
          error: "recording_interrupted",
        }));
      };

      recorder.start(100); // chunks cada 100ms
      playBeep(AUDIO_FEEDBACK.recordStart); // beep ascendente — "te escucho"
      setState({ isRecording: true, seconds: 0, isWarning: false, error: null });

      // Timer: cada segundo actualiza counter, warning beep a 50s, auto-stop a 60s
      timerRef.current = setInterval(() => {
        setState((prev) => {
          const next = prev.seconds + 1;
          if (next >= MAX_RECORDING_SECONDS) {
            cleanup();
            playBeep(AUDIO_FEEDBACK.recordStop); // AudioContext compartido — funciona en Safari
            return { ...prev, isRecording: false, seconds: next };
          }
          // Warning beep a 50s — doble pulso para atencion auditiva
          if (next === RECORDING_WARNING_SECONDS) {
            playBeep(AUDIO_FEEDBACK.recordWarning);
            setTimeout(() => playBeep(AUDIO_FEEDBACK.recordWarning), 250);
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

  /* ---- Stop: para grabacion, retorna base64 ---- */
  const stop = useCallback((): Promise<string> => {
    return new Promise((resolve) => {
      const recorder = mediaRecorderRef.current;
      if (!recorder || recorder.state !== "recording") {
        resolve("");
        return;
      }

      // Timeout: si conversion tarda > 5s, algo fallo
      const timeout = setTimeout(() => {
        cleanup();
        setState((prev) => ({ ...prev, isRecording: false, error: "Error al procesar audio" }));
        resolve("");
      }, 5000);

      recorder.onstop = async () => {
        try {
          if (timerRef.current) clearInterval(timerRef.current);
          const blob = new Blob(chunksRef.current, { type: "audio/webm" });
          const buffer = await blob.arrayBuffer();
          const base64 = btoa(
            new Uint8Array(buffer).reduce(
              (data, byte) => data + String.fromCharCode(byte),
              ""
            )
          );
          clearTimeout(timeout);
          setState((prev) => ({ ...prev, isRecording: false }));
          recorder.stream.getTracks().forEach((track) => track.stop());
          resolve(base64);
        } catch {
          clearTimeout(timeout);
          cleanup();
          setState((prev) => ({ ...prev, isRecording: false, error: "Error al procesar audio" }));
          resolve(""); // resolve vacio, no reject — overlay cierra limpiamente
        }
      };

      playBeep(AUDIO_FEEDBACK.recordStop); // beep descendente — "listo"
      recorder.stop();
    });
  }, [cleanup]);

  /* ---- Cancel: descarta todo sin enviar ---- */
  const cancel = useCallback(() => {
    cleanup();
    chunksRef.current = [];
    setState({ isRecording: false, seconds: 0, isWarning: false, error: null });
  }, [cleanup]);

  return { ...state, start, stop, cancel };
}
```

**Decisiones de arquitectura:**

| Decision | Razon | Skill |
|----------|-------|-------|
| `playBeep()` con amplitude envelope 20ms attack + 30ms release | Sin envelope, OscillatorNode produce clicks audibles. "Rounded corners for sound" = Civic Tenderness aplicado al audio | sonic-branding |
| `getAudioContext()` compartido | Safari bloquea `new AudioContext()` fuera de user gesture. Al reusar el contexto creado en `start()` (user tap), el auto-stop a 60s puede emitir beep sin fallar | sonic-branding |
| `"triangle"` en vez de `"sine"` | Onda triangular tiene armonicos impares que la hacen mas calida y "organica" — consistente con Civic Tenderness vs. sine puro que suena a tono de laboratorio | ai-voice-design |
| 200ms en vez de 150ms | Umbral de percepcion para adultos mayores (presbycusis) necesita duracion ligeramente mayor. 200ms es perceptible pero no intrusivo | ai-voice-design |
| `navigator.vibrate(50)` en playBeep | Tercer canal sensorial: visual + auditivo + tactil. Maria siente el feedback incluso si no oye bien. No soportado en iOS (documentado) | design-everyday-things |
| Warning beep doble-pulso a 50s | Solo aviso visual es insuficiente — Maria puede estar mirando al techo mientras habla. Doble pulso = "atencion" sin ser alarma | sonic-branding |
| `recordWarning` como nueva constante | Patron estandar: cada evento sonoro tiene su propia entrada en AUDIO_FEEDBACK. Escalable si se agregan mas eventos | sonic-branding |
| `try/catch` en playBeep | AudioContext puede fallar (Safari policy, user gesture). Silencio graceful | error prevention |
| `recorder.start(100)` | Chunks cada 100ms. Si el usuario para rapido, no se pierde audio. Tradeoff: mas chunks pero mas seguro | senior-fullstack |
| `audio/webm;codecs=opus` con fallback | Opus es el mejor codec para voz. No todos los browsers lo soportan. Fallback a webm generico | api-designer |
| `stop()` retorna `Promise<string>` | El componente hace `await stop()` → obtiene base64 → envia. Flujo lineal, sin callbacks anidados | react-best-practices |
| Beep en `start()` despues de `recorder.start()` | Beep solo suena si la grabacion realmente empezo. Si falla el permiso, no hay beep falso | error prevention |
| Beep en `stop()` antes de `recorder.stop()` | Feedback inmediato al tocar. El beep suena MIENTRAS se procesa el audio, no despues | ux-heuristics (H1: status) |
| Auto-stop a 60s con beep | Proteccion contra grabacion infinita. Whisper tiene timeout. Maria escucha el beep y sabe que se paro | design-everyday-things |
| `isWarning` a 50s | 10 segundos de aviso. Timer se pone rojo. Suficiente para terminar la frase | ux-heuristics (H5: error prevention) |
| `setState` en catch sin try-text | El error de microfono se muestra EN el overlay. VoiceRecorder lo renderiza | ux-heuristics (H9) |
| `cleanup` en useEffect return | Si el usuario navega fuera durante grabacion, el stream se cierra. NUNCA dejar mic abierto | react-best-practices, privacy |

---

### PASO 2: VoiceRecorder.tsx — "Tu voz tiene poder"

**Skills activas:** `/frontend-design` + `/top-design` + `/ux-heuristics` + `/brand-guidelines`

**Briefing de diseno:**
Overlay full-screen. Calido, no amenazante. El microfono es el protagonista. La onda es el feedback. El timer es la transparencia. Cancel siempre visible.

**CSS adicional requerido en `clara-web/src/app/globals.css`:**
```css
/* Waveform bars — scaleY breathing rhythm (50 BPM ≈ heartbeat) */
@keyframes waveBar {
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(1); }
}

/* Mic button — gentle scale breathing (30 BPM ≈ calm) */
@keyframes gentlePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Respect reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .animate-waveBar,
  .animate-gentlePulse {
    animation: none !important;
  }
}
```

**Wireframe confirmado:**
```
+------------------------------------------+
|                                          |
|         Habla ahora...                   |  28px, font-display, bold
|                                          |
|     ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋                  |  12 barras naranja, stagger
|                                          |
|           0:05                           |  24px tabular-nums, aria-live
|                                          |
|         [      🎤      ]                 |  96x96 circular, rojo si graba
|                                          |
|    [  Cancelar  ]   [  Enviar  ]         |  64px alto, flex gap
|                                          |
|    (error aqui si falla microfono)       |  text-clara-error, role=alert
+------------------------------------------+
```

Crea `clara-web/src/components/VoiceRecorder.tsx` con **Write**:

```typescript
"use client";

import { useState, useRef, useEffect } from "react";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import type { Language } from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Props                                                              */
/* ------------------------------------------------------------------ */

interface VoiceRecorderProps {
  visible: boolean;
  language: Language;
  onRecordingComplete: (audioBase64: string) => void;
  onCancel: () => void;
}

/* ------------------------------------------------------------------ */
/*  Labels bilingues                                                   */
/* ------------------------------------------------------------------ */

/** Alturas seeded una sola vez — no re-randomize en cada render */
const BAR_HEIGHTS = Array.from({ length: 12 }, () => 16 + Math.random() * 20);

const labels = {
  es: {
    speak: "Habla ahora...",
    cancel: "Cancelar",
    send: "Enviar",
    warning: "Quedan pocos segundos",
    tap_start: "Toca para grabar",
    tap_stop: "Toca para parar",
    mic_error: "No se pudo acceder al microfono. Asegurate de dar permiso en tu navegador.",
    try_again: "Probar de nuevo",
    use_text: "Escribir en su lugar",
    recording_interrupted: "La grabacion se interrumpio. Intenta de nuevo.",
  },
  fr: {
    speak: "Parle maintenant...",
    cancel: "Annuler",
    send: "Envoyer",
    warning: "Il reste peu de secondes",
    tap_start: "Appuie pour enregistrer",
    tap_stop: "Appuie pour arreter",
    mic_error: "Impossible d'acceder au micro. Assure-toi de donner la permission dans ton navigateur.",
    try_again: "Reessayer",
    use_text: "Ecrire a la place",
    recording_interrupted: "L'enregistrement a ete interrompu. Reessaye.",
  },
};

/* ------------------------------------------------------------------ */
/*  Componente                                                        */
/* ------------------------------------------------------------------ */

export default function VoiceRecorder({
  visible,
  language,
  onRecordingComplete,
  onCancel,
}: VoiceRecorderProps) {
  const { isRecording, seconds, isWarning, error, start, stop, cancel } =
    useAudioRecorder();
  const t = labels[language];
  const overlayRef = useRef<HTMLDivElement>(null);

  /* ---- Entry/exit animation — mount/unmount con transicion ---- */
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (visible) setMounted(true);
  }, [visible]);

  function handleTransitionEnd() {
    if (!visible) setMounted(false);
  }

  /* ---- Escape key cierra overlay ---- */
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        handleCancel();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  /* ---- Focus trap: Tab no escapa del overlay ---- */
  useEffect(() => {
    const overlay = overlayRef.current;
    if (!overlay) return;

    const focusable = overlay.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length === 0) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    // Focus el primer boton al montar
    first.focus();

    function trapFocus(e: KeyboardEvent) {
      if (e.key !== "Tab") return;
      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }

    overlay.addEventListener("keydown", trapFocus);
    return () => overlay.removeEventListener("keydown", trapFocus);
  }, []);

  /* ---- Back button cierra overlay (Android) ---- */
  useEffect(() => {
    history.pushState({ voiceOverlay: true }, "");
    function onPopState() {
      handleCancel();
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  /* ---- Toggle: tap para empezar, tap para parar ---- */
  async function handleToggle() {
    if (isRecording) {
      // Guard: grabacion < 1s = probable double-tap accidental (tremor)
      if (seconds < 1) return;
      const base64 = await stop();
      if (base64) onRecordingComplete(base64);
    } else {
      await start();
    }
  }

  /* ---- Cancel: descarta grabacion y cierra overlay ---- */
  function handleCancel() {
    cancel();
    onCancel();
  }

  /* ---- Send: para y envia (cuando ya esta grabando) ---- */
  async function handleSend() {
    const base64 = await stop();
    if (base64) onRecordingComplete(base64);
  }

  /* ---- Timer display ---- */
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const timeDisplay = `${minutes}:${secs.toString().padStart(2, "0")}`;

  if (!mounted) return null;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 bg-clara-bg z-50 flex flex-col items-center justify-center px-6"
      role="dialog"
      aria-label={isRecording ? t.speak : t.tap_start}
      aria-modal="true"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "scale(1)" : "scale(0.97)",
        transition: visible
          ? "opacity 500ms cubic-bezier(0.16, 1, 0.3, 1), transform 500ms cubic-bezier(0.16, 1, 0.3, 1)"
          : "opacity 300ms cubic-bezier(0.55, 0, 1, 0.45)",
        pointerEvents: visible ? "auto" : "none",
      }}
      onTransitionEnd={handleTransitionEnd}
    >
      {/* Titulo — cambia segun estado */}
      <p className="font-display font-bold text-h2 text-clara-text mb-8 text-center">
        {isRecording ? t.speak : t.tap_start}
      </p>

      {/* Onda de audio animada — 12 barras naranja con scaleY breathing */}
      {isRecording && (
        <div
          className="flex items-end gap-1.5 mb-6 h-10"
          aria-hidden="true"
        >
          {BAR_HEIGHTS.map((h, i) => (
            <span
              key={i}
              className="w-1.5 bg-clara-orange rounded-full"
              style={{
                height: `${h}px`,
                transformOrigin: "bottom",
                animation: `waveBar 1.2s ease-in-out ${i * 80}ms infinite`,
              }}
            />
          ))}
        </div>
      )}

      {/* Timer — tabular-nums, rojo cuando warning */}
      <p
        className={`font-body text-[24px] tabular-nums mb-8 ${
          isWarning
            ? "text-clara-error font-bold"
            : "text-clara-text-secondary"
        }`}
        aria-live="polite"
      >
        {timeDisplay}
        {isWarning && <span className="sr-only">{t.warning}</span>}
      </p>

      {/* Boton microfono grande — 96x96px, toggle */}
      <button
        onClick={handleToggle}
        aria-label={isRecording ? t.tap_stop : t.tap_start}
        className="w-touch-lg h-touch-lg rounded-full flex items-center justify-center mb-10
                   focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        style={{
          backgroundColor: isRecording ? "#C62828" : "#1B5E7B",
          transition: "background-color 300ms cubic-bezier(0.16, 1, 0.3, 1)",
          animation: isRecording ? "gentlePulse 2s ease-in-out infinite" : "none",
        }}
      >
        <svg
          width="48"
          height="48"
          viewBox="0 0 24 24"
          fill="white"
          aria-hidden="true"
        >
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
                     hover:border-clara-text hover:text-clara-text
                     transition-colors duration-150
                     focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          {t.cancel}
        </button>
        {isRecording && (
          <button
            onClick={handleSend}
            aria-label={t.send}
            className="flex-1 h-touch bg-clara-green text-white rounded-xl
                       text-button font-medium hover:bg-[#256940]
                       transition-colors duration-150
                       focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-green focus-visible:outline-offset-2"
          >
            {t.send}
          </button>
        )}
      </div>

      {/* Error de microfono — amable, con opciones */}
      {error && (
        <div role="alert" className="mt-6 text-left max-w-sm">
          <p className="text-clara-error text-body text-left mb-4">
            {t.mic_error}
          </p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={() => start()}
              className="px-4 min-h-touch-sm bg-clara-blue text-white rounded-lg
                         text-body-sm font-medium hover:bg-[#164d66]
                         transition-colors duration-150
                         focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
            >
              {t.try_again}
            </button>
            <button
              onClick={onCancel}
              className="px-4 min-h-touch-sm border-2 border-clara-border rounded-lg
                         text-body-sm font-medium text-clara-text-secondary
                         hover:border-clara-blue hover:text-clara-blue
                         transition-colors duration-150
                         focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
            >
              {t.use_text}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
```

**Decisiones de diseno:**

| Decision | Razon | Heuristica |
|----------|-------|------------|
| Escape key cierra overlay | `aria-modal` requiere escape route. Maria o su nieto pueden usar teclado | Nielsen #3, WCAG 2.1.1 |
| Focus trap con querySelectorAll | Tab no escapa detras del overlay. Sin libreria externa (zero deps) | WCAG 2.4.3, ux-heuristics |
| `history.pushState` + popstate | En Android, el boton back navega fuera si no interceptamos. Overlay se cierra limpiamente | ux-heuristics, design-everyday-things |
| Guard `seconds < 1` en toggle | Maria con temblor puede hacer double-tap. Sin guard, envia 0s de audio → Whisper retorna basura | ux-heuristics (H5: error prevention) |
| `first.focus()` al montar | Focus va directo al primer boton interactivo. Screen reader anuncia el overlay inmediatamente | WCAG 2.4.3 |
| `fixed inset-0 z-50` | Full-screen overlay. Grabacion es momento dedicado. Sin distracciones | top-design (minimalism) |
| `bg-clara-bg` (no black, no blur) | Fondo calido (#FAFAFA), no amenazante. Negro asusta. Blur sugiere "algo escondido" | Civic Tenderness |
| `role="dialog" aria-modal="true"` | Screen reader anuncia como dialogo. Focus atrapado logicamente | WCAG 1.3.1 |
| `aria-label` dinamico | Cambia entre "Toca para grabar" y "Habla ahora" segun estado | Nielsen #1 (status) |
| `text-h2` (28px) titulo | Spec del wireframe 3C. Grande, legible, font-display (Atkinson Hyperlegible) | web-typography, wireframe |
| 12 barras con stagger 80ms | Efecto organico de onda. Alturas pre-calculadas fuera del render. `waveBar` scaleY = metafora de nivel de audio | top-design, Civic Tenderness |
| `font-body tabular-nums text-[24px]` timer | Inter tiene OpenType `tnum`. Cada digito mismo ancho = timer estable. Sin fuente mono extra | web-typography |
| Error text 20px (`text-body`) | Contenido primario de error merece tamano completo. 18px demasiado pequeno para texto que Maria DEBE leer | web-typography |
| Error buttons 18px (`text-body-sm`) | 16px esta por debajo del minimo funcional del design system para botones de accion | web-typography |
| Error `text-left` | Texto multi-linea centrado es mas dificil de leer — los ojos pierden el inicio de cada linea | web-typography |
| `aria-live="polite"` en timer | Screen reader anuncia cambios de tiempo sin interrumpir | WCAG 4.1.3 |
| `sr-only` warning text | Cuando isWarning, screen reader dice "Quedan pocos segundos". Visual: timer rojo | a11y |
| `w-touch-lg h-touch-lg` (96x96px) | Spec wireframe. Boton ENORME. Maria puede tocarlo con temblor. Es una "declaracion" | Civic Tenderness, WCAG 2.5.8 |
| Entry fade+scale(0.97→1) 500ms | Hard cut es desorientante para Maria. Scale 3% = "respirar a la existencia". Usa `EASING.out` existente | top-design |
| Exit fade 300ms sin scale | Salida rapida pero no snap. Maria quiere volver al chat. Usa `EASING.in` | top-design |
| `waveBar` scaleY 1.2s | 50 BPM = ritmo cercano a latido cardiaco. Barras crecen en height, no parpadean en opacity. Metafora universal de "nivel de audio" | top-design |
| `BAR_HEIGHTS` fuera de render | `Math.random()` en JSX re-randomiza cada segundo (timer setState). Bug visual. Const externa = alturas estables | top-design, ux-heuristics |
| `gentlePulse` scale(1.05) 2s | 30 BPM = mas lento que waveform = ritmo en capas. 5% scale en 96px = 4.8px expansion. Perceptible, no agresivo. "El mic respira" | top-design |
| `focus-visible:` en vez de `focus:` | `focus:` muestra outline en CADA tap (molesto para touch). `focus-visible:` solo para keyboard (correcto) | top-design |
| Cancel hover `clara-text` no `clara-error` | Rojo en hover Cancel colisiona con mic rojo grabando. Dos rojos compiten | top-design |
| `items-end` en waveform container | Barras crecen desde abajo (equalizer metaphor), no desde centro | top-design |
| Rojo `#C62828` + gentlePulse cuando graba | Rojo universal = "grabando". Scale pulse = vivo, activo. Sin pulse cuando idle (azul) | design-everyday-things |
| `bg-clara-blue` cuando idle | Azul de confianza = "listo para grabar". Consistente con boton enviar del chat | brand-guidelines |
| Focus visible con `outline-[3px]` | En overlay blanco, el outline azul contrasta bien. 3px para visibilidad maxima | WCAG 2.4.7 |
| Enviar solo aparece `isRecording` | Antes de grabar: solo "Cancelar" (simple). Grabando: "Cancelar" + "Enviar" (opciones claras) | ux-heuristics (H8: minimalism) |
| `h-touch` (64px) en Cancelar/Enviar | Spec wireframe. Touch targets generosos. Textos en `text-button` (20px) | wireframe, WCAG |
| Error con `role="alert"` | Anuncio inmediato a screen reader cuando falla microfono | WCAG 4.1.3 |
| Error con 2 botones: "Probar" + "Escribir" | Siempre hay salida. Maria puede reintentar O cambiar a texto. Nunca atrapada | Nielsen #3 (freedom), ux-heuristics (H9) |
| `min-h-touch-sm` (48px) en botones error | Touch targets accesibles incluso en mensajes de error | WCAG 2.5.8 |
| Labels `text-label` (16px) en botones error | Minimo tipografico para texto funcional. No 14px | web-typography |
| Tono error amable | "Asegurate de dar permiso" no "PERMISSION_DENIED". Companera, no sistema | category-design |
| `onCancel` en "Escribir en su lugar" | Maria vuelve al chat y puede escribir. Transicion suave, no error dead-end | ux-heuristics (H3) |
| `text-center` en overlay | Composicion centrada — grabacion es un momento simetrico, enfocado. Diferente al chat (asimetrico) | top-design |

---

### PASO 3: Integrar en chat/page.tsx — "Conectar la voz al chat"

**Skills activas:** `/react-expert` + `/nextjs-developer`

**Briefing:**
Reemplazar el `alert()` stub con VoiceRecorder real. Agregar estado `voiceActive`. Pasar `activeMode="voice"` a ChatInput cuando grabando.

Modificar `clara-web/src/app/chat/page.tsx` con **Edit**:

**Cambio 1:** Agregar import de VoiceRecorder al inicio:
```typescript
import VoiceRecorder from "@/components/VoiceRecorder";
```

**Cambio 2:** Agregar estado `voiceActive` dentro de `ChatContent()`:
```typescript
const [voiceActive, setVoiceActive] = useState(false);
```
(agregar `useState` al import de React si no esta)

**Cambio 3:** Reemplazar el `onStartVoice` stub:
```typescript
// ANTES:
onStartVoice={() => {
  alert(comingSoon[language]);
}}

// DESPUES:
onStartVoice={() => setVoiceActive(true)}
```

**Cambio 4:** Agregar `activeMode` prop a ChatInput:
```typescript
<ChatInput
  onSendText={(text) => send(text)}
  onStartVoice={() => setVoiceActive(true)}
  onOpenCamera={() => {
    alert(comingSoon[language]);
  }}
  disabled={isLoading}
  language={language}
  activeMode={voiceActive ? "voice" : "text"}
/>
```

**Cambio 5:** Renderizar VoiceRecorder con `visible` prop (siempre montado, animacion entry/exit), ANTES del cierre `</div>`:
```typescript
<VoiceRecorder
  visible={voiceActive}
  language={language}
  onRecordingComplete={(audioBase64) => {
    setVoiceActive(false);
    send("", audioBase64);
  }}
  onCancel={() => setVoiceActive(false)}
/>
```

**El page.tsx modificado completo:**

```typescript
"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Header from "@/components/Header";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import VoiceRecorder from "@/components/VoiceRecorder";
import { useChat } from "@/hooks/useChat";
import type { Language } from "@/lib/types";

const comingSoon: Record<Language, string> = {
  es: "Esta funcion estara disponible pronto",
  fr: "Cette fonction sera bientot disponible",
};

function ChatContent() {
  const searchParams = useSearchParams();
  const initialLang = (searchParams.get("lang") as Language) || "es";
  const [voiceActive, setVoiceActive] = useState(false);
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
        onStartVoice={() => setVoiceActive(true)}
        onOpenCamera={() => {
          // Q9 reemplazara con DocumentUpload
          alert(comingSoon[language]);
        }}
        disabled={isLoading}
        language={language}
        activeMode={voiceActive ? "voice" : "text"}
      />

      {/* VoiceRecorder overlay — siempre montado, visible prop controla animacion */}
      <VoiceRecorder
        visible={voiceActive}
        language={language}
        onRecordingComplete={(audioBase64) => {
          setVoiceActive(false);
          send("", audioBase64);
        }}
        onCancel={() => setVoiceActive(false)}
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
| `useState(false)` para voiceActive | Simple toggle. No useRef — necesitamos re-render para mostrar/ocultar overlay | react-best-practices |
| `send("", audioBase64)` en onRecordingComplete | useChat detecta audioBase64 → inputType="audio", loadingContext="listening". Burbuja usuario muestra 🎤 | Q6 contract |
| `setVoiceActive(false)` ANTES de `send()` | Cierra overlay inmediatamente. El loading aparece en el chat. Maria no espera en overlay | UX pattern |
| `activeMode={voiceActive ? "voice" : "text"}` | ChatInput muestra boton "Voz" como activo (borde naranja + fondo) cuando overlay abierto | ux-heuristics (H1: status) |
| VoiceRecorder DESPUES de ChatInput en DOM | `z-50` pone overlay encima. Pero en DOM esta al final — mejor para accessibility tree order | a11y |
| `visible` prop en vez de conditional render | Entry/exit animation requiere que el componente este montado para animar la salida. `mounted` state interno maneja unmount post-transicion | top-design, performance |
| `comingSoon` solo para Foto (Q9) | Voz ya no es stub. Foto sigue siendo stub hasta Q9 | incremental delivery |

---

### PASO 4: Verificar build y tipos (agentes paralelos)

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
| `Cannot find module '@/hooks/useAudioRecorder'` | Archivo no creado o path incorrecto | Verificar que `useAudioRecorder.ts` esta en `clara-web/src/hooks/` |
| `Property 'recordStart' does not exist on type 'Record<string, AudioFeedbackParams>'` | Q5 constants.ts usa Record<string, ...> — acceso con dot notation funciona | Verificar que AUDIO_FEEDBACK exporta correctamente en constants.ts |
| `Type 'AudioFeedbackParams' is not exported from '@/lib/types'` | Q5 puede haber definido AudioFeedbackParams solo en constants | Verificar types.ts contiene `interface AudioFeedbackParams`. Si no, definirla inline en useAudioRecorder |
| `Cannot find name 'NodeJS'` | Tipo de setInterval difiere en browser vs Node | Usar `ReturnType<typeof setInterval>` en vez de `NodeJS.Timeout` |
| `Property 'close' does not exist on type 'AudioContext'` | TypeScript strict puede no incluir close() | Agregar `as any` al close() o verificar tsconfig lib incluye `dom` |

---

### PASO 5: Test funcional manual

**Skill activa:** `/design-everyday-things` + `/ux-heuristics`

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice/clara-web && npm run dev
```

**Checklist de flujo — "El test de Maria":**

1. **Abrir** `/chat?lang=es` → ver chat con mensaje de bienvenida
2. **Tocar** boton "Voz" (naranja) → aparece overlay de grabacion
3. **Verificar** texto "Toca para grabar" centrado
4. **Verificar** boton microfono azul grande (96x96px) centrado
5. **Verificar** solo boton "Cancelar" visible (no "Enviar" todavia)
6. **Tocar** boton microfono → **escuchar beep ascendente** (440Hz)
7. **Verificar** texto cambia a "Habla ahora..."
8. **Verificar** onda naranja aparece (12 barras pulsando)
9. **Verificar** timer empieza a correr: 0:01, 0:02, 0:03...
10. **Verificar** boton microfono ahora es ROJO con pulse
11. **Verificar** boton "Enviar" verde aparece junto a "Cancelar"
12. **Hablar** algo al microfono
13. **Tocar** boton microfono de nuevo → **escuchar beep descendente** (349Hz)
14. **Verificar** overlay se cierra
15. **Verificar** burbuja usuario con 🎤 aparece en el chat
16. **Verificar** loading: "Clara esta escuchando tu mensaje..."
17. **Repetir** — esta vez tocar "Enviar" en lugar del mic → mismo resultado
18. **Repetir** — esta vez tocar "Cancelar" → overlay cierra SIN enviar
19. **Cambiar** idioma a FR → repetir → textos en frances

**Test de error de microfono:**
20. **Denegar** permiso de microfono cuando el browser pregunte
21. **Verificar** error amable aparece: "No se pudo acceder al microfono..."
22. **Verificar** dos botones: "Probar de nuevo" + "Escribir en su lugar"
23. **Tocar** "Escribir en su lugar" → vuelve al chat

---

### PASO 6: Review de diseno integral

**Skill activa:** `/ux-heuristics` + `/design-everyday-things` + `/brand-guidelines`

**Heuristica de Nielsen — Grabacion de voz:**

| # | Heuristica | Como se cumple |
|---|-----------|----------------|
| 1 | Visibility of system status | Timer corriendo + onda animada + beeps + texto "Habla ahora" + mic rojo. 4 canales de feedback |
| 2 | Match between system and real world | Toggle = mejora accesible sobre WhatsApp (press-and-hold). Instrucciones explicitas compensan la diferencia. Microfono = icono universal. "Habla ahora" = lenguaje natural |
| 3 | User control and freedom | Cancel siempre visible. "Escribir en su lugar" como escape. Overlay cierra al enviar |
| 4 | Consistency and standards | Mismos colores (clara-blue, clara-orange, clara-error), touch targets (touch-lg, touch), tokens que Q3-Q6 |
| 5 | Error prevention | Toggle evita press-and-hold. Warning a 50s previene corte inesperado. Auto-stop a 60s con beep |
| 6 | Recognition rather than recall | "Toca para grabar" / "Toca para parar" — instruccion explicita. No solo iconos |
| 7 | Flexibility and efficiency | Toggle rapido para expertos. Boton "Enviar" separado para quienes quieren revisar antes |
| 8 | Aesthetic and minimalist design | Solo 4 elementos: titulo + onda + timer + mic. Fondo limpio. Sin decoracion |
| 9 | Help users recover from errors | Error mic con 2 opciones: reintentar o cambiar a texto. Tono amable, no tecnico |
| 10 | Help and documentation | "Toca para grabar" ES la documentacion. Auto-explicativo |

**Checklist de accesibilidad (20 puntos):**

**Overlay:**
- [ ] `role="dialog"` + `aria-modal="true"`
- [ ] `aria-label` dinamico (estado actual)
- [ ] `z-50` sobre todo el contenido
- [ ] `bg-clara-bg` (fondo calido, no negro)

**Microfono:**
- [ ] `w-touch-lg h-touch-lg` (96x96px) — touch target enorme
- [ ] `aria-label` bilingue cambia con estado (grabar/parar)
- [ ] Focus visible con `outline-[3px]`
- [ ] Contraste color: blanco sobre azul (idle) y rojo (grabando)

**Timer:**
- [ ] `aria-live="polite"` — screen reader anuncia tiempo
- [ ] `sr-only` warning text cuando llega a 50s
- [ ] `font-body tabular-nums` para numeros estables (no saltan)
- [ ] Texto 24px legible

**Controles:**
- [ ] Cancelar siempre visible con `h-touch` (64px)
- [ ] Enviar solo cuando grabando (minimiza confusion)
- [ ] Ambos botones con `aria-label` bilingue
- [ ] Focus visible en ambos botones
- [ ] `text-button` (20px) en labels de botones

**Error de microfono:**
- [ ] `role="alert"` para anuncio inmediato
- [ ] Mensaje amable en idioma del usuario
- [ ] Dos opciones: "Probar de nuevo" + "Escribir en su lugar"
- [ ] Touch targets `min-h-touch-sm` (48px) en botones de error

**Interaccion (nuevos — post-review de 7 skills):**
- [ ] Escape key cierra overlay (keydown listener)
- [ ] Focus trap activo — Tab cicla dentro del overlay
- [ ] Back button (Android) cierra overlay via popstate
- [ ] Double-tap < 1s no envia grabacion (guard en handleToggle)
- [ ] `focus-visible:` en todos los botones (no `focus:`)
- [ ] `recorder.onerror` handler — fallo mid-recording muestra error
- [ ] `stop()` con timeout 5s — UI nunca se congela
- [ ] Entry/exit animation con prefers-reduced-motion respetado

**Checklist de marca (10 puntos):**
- [ ] Onda naranja (`clara-orange`) = calidez, invitacion a hablar
- [ ] Mic azul (`clara-blue`) idle = confianza = "listo para ti"
- [ ] Mic rojo (`clara-error`) grabando = universal "activo, grabando"
- [ ] Enviar verde (`clara-green`) = esperanza, accion positiva
- [ ] Font-display (Atkinson Hyperlegible) en titulo = legibilidad maxima
- [ ] Beeps con amplitude envelope (20ms attack, 30ms release) — sin clicks
- [ ] Tono error companero: "Asegurate de dar permiso" no "PERMISSION_DENIED"
- [ ] Waveform scaleY breathing (1.2s, 50 BPM) — no opacity pulse
- [ ] Mic button gentlePulse scale (2s, 30 BPM) — ritmo en capas
- [ ] Beeps triangle wave (calido) en vez de sine (frio)

**Checklist de integracion con Q5 y Q6 (11 puntos):**
- [ ] `AUDIO_FEEDBACK.recordStart` (440Hz) usado al iniciar grabacion
- [ ] `AUDIO_FEEDBACK.recordStop` (349Hz) usado al parar grabacion
- [ ] `AUDIO_FEEDBACK.recordWarning` definido en constants.ts
- [ ] Warning beep doble-pulso a 50 segundos
- [ ] `navigator.vibrate(50)` como feedback tactil en cada beep
- [ ] `MAX_RECORDING_SECONDS` (60) como limite de auto-stop
- [ ] `RECORDING_WARNING_SECONDS` (50) como umbral de warning
- [ ] `send("", audioBase64)` conecta con useChat correctamente
- [ ] LoadingContext "listening" activado automaticamente por useChat
- [ ] `activeMode="voice"` pasado a ChatInput cuando overlay abierto
- [ ] `alert()` stub de Q6 reemplazado con VoiceRecorder real

---

### PASO 7: Commit

```bash
cd /Users/andreaavila/Documents/hakaton/civicaid-voice && git add clara-web/src/hooks/useAudioRecorder.ts clara-web/src/components/VoiceRecorder.tsx clara-web/src/app/chat/page.tsx
git commit -m "feat: add voice recording — toggle mic, animated wave, audio beeps, 60s limit

- useAudioRecorder.ts: MediaRecorder hook with base64 conversion, timer,
  auto-stop at 60s, warning double-pulse at 50s, Web Audio API beeps with
  amplitude envelope (triangle wave, 440Hz start, 349Hz stop, 440Hz warning),
  shared AudioContext, recorder.onerror handler, stop() with 5s timeout,
  navigator.vibrate haptic feedback, stream cleanup on unmount
- VoiceRecorder.tsx: full-screen overlay with entry/exit CSS transitions,
  96x96 toggle mic button with gentlePulse animation, 12-bar orange waveform
  with scaleY breathing, tabular-nums timer, focus trap + Escape key + back
  button (popstate), double-tap guard, bilingual labels (ES/FR), error text
  20px text-left with focus-visible buttons
- chat/page.tsx: VoiceRecorder always mounted with visible prop (no conditional
  render), replacing alert() stub, activeMode='voice' to ChatInput
- globals.css: @keyframes waveBar, gentlePulse, prefers-reduced-motion
- Consumes Q5: AUDIO_FEEDBACK (incl. recordWarning), MAX_RECORDING_SECONDS,
  RECORDING_WARNING_SECONDS, AudioFeedbackParams
- Consumes Q6: send() with audioBase64, LoadingContext 'listening',
  activeMode prop, onStartVoice callback
- WCAG: role=dialog, aria-live timer, aria-labels bilingual, 96px touch target,
  focus-visible (not focus:), focus trap, Escape, back button, role=alert on error
- Design: Civic Tenderness — voice as empowerment, warm orange waveform,
  gentle triangle beeps with envelope, toggle for trembling hands

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## HERRAMIENTAS CLAUDE CODE

| Herramienta | Cuando | Notas |
|-------------|--------|-------|
| **Read** | Paso 0 — leer design docs + constants + page.tsx actual | Entender antes de codear |
| **Write** | Pasos 1-2 — crear hook y componente | 2 archivos nuevos |
| **Edit** | Paso 3 — modificar page.tsx (5 cambios) | O Write si prefieres reescribir completo |
| **Bash** | Paso 4 — build + type check | Verificar compilacion |
| **Glob** | Verificar archivos creados | `clara-web/src/hooks/useAudioRecorder.ts`, `clara-web/src/components/VoiceRecorder.tsx` |
| **Task** | Paso 0 (lectura paralela) y Paso 4 (verificacion paralela) | `subagent_type="Explore"` o `"Bash"` |

---

## RESTRICCIONES

| Restriccion | Razon |
|-------------|-------|
| NO press-and-hold | Demasiado dificil para Maria (temblor, destreza). Toggle SIEMPRE |
| NO visualizer real de audio | AnalyserNode + FFT es complejo y no aporta a Maria. Barras animadas simbolicas son suficientes |
| NO auto-play beeps sin interaccion | Web Audio API requiere user gesture para AudioContext. Los beeps se disparan dentro de event handlers |
| NO guardar audio en localStorage | Privacy. El audio se convierte a base64 y se envia. No persiste en el dispositivo |
| NO cargar archivos MP3 para beeps | Web Audio API OscillatorNode genera todo. Zero dependencies, zero network requests |
| NO modificar useChat.ts | El hook ya soporta `send("", audioBase64)`. No necesita cambios |
| NO modificar ChatInput.tsx | El componente ya tiene `onStartVoice` y `activeMode`. No necesita cambios |
| NO modificar useAudioRecorder despues de Paso 1 | El hook es una unidad testeable. VoiceRecorder es el consumer, no el editor |
| Texto minimo 16px (`text-label`) | Web-typography review: 14px falla contraste WCAG para personas mayores |
| Touch targets minimo 48px (`touch-sm`) | WCAG 2.5.8. Excepto el mic que es 96px (touch-lg) |

## DEFINICION DE TERMINADO (post-review de 7 skills)

Q7 esta **completo** cuando:

1. ✅ `useAudioRecorder.ts` con playBeep envelope, AudioContext compartido, warning beep, onerror, stop timeout
2. ✅ `VoiceRecorder.tsx` con entry/exit animation, waveform scaleY, gentlePulse, focus trap, Escape, back-button, double-tap guard
3. ✅ `page.tsx` con visible prop (no conditional render), VoiceRecorder siempre montado
4. ✅ `globals.css` con @keyframes waveBar, gentlePulse, prefers-reduced-motion
5. ✅ Timer con font-body tabular-nums, no font-mono
6. ✅ Error text 20px text-left, error buttons 18px con focus-visible
7. ✅ Documentacion NO dice "igual a WhatsApp"
8. ✅ AUDIO_FEEDBACK incluye recordWarning
9. ✅ Build sin errores, types sin errores
10. ✅ Test de Maria pasa los 23 puntos del checklist
