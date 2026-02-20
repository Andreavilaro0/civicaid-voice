# Q7 Rewrite — Incorporar Feedback de 7 Reviews Multi-Agente

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reescribir `docs/prompts/Q7-GRABACION-VOZ.md` incorporando 23 fixes de 7 reviews independientes (ux-heuristics, sonic-branding, web-typography, top-design, design-everyday-things, audience-research, ai-voice-design).

**Architecture:** Editar el prompt Q7 existente seccion por seccion. Cada Task modifica una zona del archivo. No se crea codigo nuevo — se modifica el codigo DENTRO del prompt markdown. El archivo resultante es un prompt mejorado que un agente ejecutara para crear el hook y componente de grabacion de voz.

**Tech Stack:** Markdown (prompt), TypeScript/React (codigo dentro del prompt), Tailwind CSS (clases dentro del prompt), Web Audio API (beeps dentro del prompt)

---

## Resumen de Reviews

| # | Skill | Score/Resultado | Fixes |
|---|-------|-----------------|-------|
| 1 | **ux-heuristics** | 7.5/10 | Focus trap, Escape key, double-tap protection, back-button |
| 2 | **sonic-branding** | Critical: amplitude envelope | Envelope en playBeep, warning beep 50s, Safari AudioContext, sine→triangle, 150→200ms |
| 3 | **web-typography** | 3 Priority-1 | Timer font tabular-nums, error text 20px, error buttons 18px, text-left error |
| 4 | **top-design** | 5.5/10 | Entry/exit animation, waveform scaleY, mic scale pulse, stagger reveal, blue→red transition, bar sizing, token hygiene |
| 5 | **design-everyday-things** | 15 issues | WhatsApp claim corregir, min recording 1s, onerror handler, icon signifiers, haptic, send confirmation, optimistic beep, stop() timeout |
| 6 | **audience-research** | Voz = canal PRIMARIO | Reframe rol prompt, Fatima illiteracy icons |
| 7 | **ai-voice-design** | Validado frecuencias | Haptic feedback, volume validation, waveform warmth |

---

## Mapa de Fixes

| ID | Issue | Origen | Severidad | Task |
|----|-------|--------|-----------|------|
| S1 | `playBeep()` sin amplitude envelope — hard start/stop = clicks | sonic-branding | **Critical** | 1 |
| S2 | Safari auto-stop beep fuera de user gesture — falla silenciosamente en iOS | sonic-branding | **High** | 1 |
| S3 | No hay warning beep a 50 segundos — solo visual | sonic-branding | **High** | 1 |
| S4 | `"sine"` → `"triangle"` para warmth; `150ms` → `200ms` para elderly | sonic-branding + ai-voice | **Medium** | 1 |
| S5 | No hay haptic feedback `navigator.vibrate()` | sonic + ai-voice + everyday | **Medium** | 1 |
| U1 | No hay Escape key handler para cerrar overlay | ux-heuristics | **Severity 2** | 2 |
| U2 | `aria-modal="true"` sin focus trap real — Tab escapa al fondo | ux-heuristics | **Severity 2** | 2 |
| U3 | No hay history.pushState — back button navega fuera en vez de cerrar | ux-heuristics + everyday | **Severity 2** | 2 |
| U4 | No hay double-tap protection — tremor envia grabacion de 0s | ux-heuristics + everyday | **Severity 2** | 2 |
| T1 | `font-mono` undefined en timer — fallback a system default | web-typography | **Priority 1** | 3 |
| T2 | Error text `text-body-sm` (18px) deberia ser `text-body` (20px) | web-typography | **Priority 1** | 3 |
| T3 | Error buttons `text-label` (16px) deberia ser `text-body-sm` (18px) | web-typography | **Priority 1** | 3 |
| T4 | Error text `text-center` — multi-linea centrado es dificil de leer | web-typography | **Priority 2** | 3 |
| D1 | Overlay sin entry/exit animation — hard cut | top-design | **4/10** | 4 |
| D2 | Waveform `animate-pulse` (opacity) — deberia ser `scaleY` (height) | top-design | **4/10** | 4 |
| D3 | `Math.random()` en JSX render — alturas re-randomize cada segundo | top-design + ux | **Bug** | 4 |
| D4 | Mic button `animate-pulse` (opacity) — deberia ser scale(1.05) | top-design | **5/10** | 4 |
| D5 | Waveform bars w-1 gap-1 demasiado estrecho; h-8 clips alturas | top-design | **Low** | 4 |
| D6 | Cancel hover rojo colisiona con mic rojo grabando | top-design | **Low** | 4 |
| D7 | Focus `focus:` en vez de `focus-visible:` — outline en cada tap | top-design | **Low** | 4 |
| E1 | Documentacion dice toggle es "igual a WhatsApp" — es FALSO | everyday | **Critical** | 5 |
| E2 | No hay `recorder.onerror` — fallo mid-recording silencioso | everyday | **High** | 5 |
| E3 | `stop()` Promise sin reject/timeout — UI puede congelarse | everyday | **Medium** | 5 |

---

### Task 1: Fix S1-S5 — playBeep() con Amplitude Envelope + Warning Beep + Haptic

**Files:**
- Modify: `docs/prompts/Q7-GRABACION-VOZ.md` — seccion PASO 1 (useAudioRecorder.ts), funcion `playBeep()` y timer auto-stop

**Problema:**
La funcion `playBeep()` actual crea un OscillatorNode y lo arranca/para sin envelope de amplitud. Esto produce un "click" audible al inicio y fin de cada beep — como encender y apagar una luz de golpe en vez de un fade. Para Civic Tenderness ("rounded corners for sound"), los beeps necesitan 20ms de attack ramp y 30ms de release ramp. Ademas, Safari bloquea AudioContext fuera de user gesture (el auto-stop a 60s usa setInterval, NO user gesture). Y no hay beep de aviso a 50s.

**Step 1: Localizar `playBeep()` en el prompt**

Buscar en el prompt (lineas ~288-309):
```typescript
function playBeep(params: AudioFeedbackParams): void {
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = params.type;
    osc.frequency.value = params.frequency;
    gain.gain.value = 0.3; // volumen suave — no asustar a Maria

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + params.duration / 1000);

    // Cleanup AudioContext despues del beep
    osc.onended = () => ctx.close();
  } catch {
    // AudioContext no soportado — silencio graceful
  }
}
```

**Step 2: Reemplazar con version con envelope + AudioContext reusable + haptic**

```typescript
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
```

**Step 3: Actualizar constantes AUDIO_FEEDBACK en la seccion CONTEXTO TECNICO**

Buscar (lineas ~90-97):
```typescript
export const AUDIO_FEEDBACK: Record<string, AudioFeedbackParams> = {
  recordStart: { frequency: 440, duration: 150, type: "sine" },
  recordStop: { frequency: 349, duration: 150, type: "sine" },
  messageSent: { frequency: 523, duration: 100, type: "sine" },
};
```

Reemplazar con:
```typescript
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
```

> **Nota:** Estas tres frecuencias (349Hz F4 + 440Hz A4 + 523Hz C5) forman una triada de Fa Mayor — la paleta tonal accidental de Clara. Calida, estable, resuelta.

**Step 4: Agregar warning beep al timer (50s) y usar AudioContext compartido**

Buscar en el timer dentro de `start()` (lineas ~375-389):
```typescript
timerRef.current = setInterval(() => {
  setState((prev) => {
    const next = prev.seconds + 1;
    if (next >= MAX_RECORDING_SECONDS) {
      cleanup();
      playBeep(AUDIO_FEEDBACK.recordStop);
      return { ...prev, isRecording: false, seconds: next };
    }
    return {
      ...prev,
      seconds: next,
      isWarning: next >= RECORDING_WARNING_SECONDS,
    };
  });
}, 1000);
```

Reemplazar con:
```typescript
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
```

**Step 5: Actualizar tabla de decisiones de arquitectura**

Agregar filas:

| Decision | Razon | Skill |
|----------|-------|-------|
| Amplitude envelope 20ms attack + 30ms release | Sin envelope, OscillatorNode produce clicks audibles. "Rounded corners for sound" = Civic Tenderness aplicado al audio | sonic-branding |
| `getAudioContext()` compartido | Safari bloquea `new AudioContext()` fuera de user gesture. Al reusar el contexto creado en `start()` (user tap), el auto-stop a 60s puede emitir beep sin fallar | sonic-branding |
| `"triangle"` en vez de `"sine"` | Onda triangular tiene armonicos impares que la hacen mas calida y "organica" — consistente con la estetica de Civic Tenderness vs. sine puro que suena a tono de laboratorio | ai-voice-design |
| 200ms en vez de 150ms | Umbral de percepcion para adultos mayores (presbycusis) necesita duracion ligeramente mayor. 200ms es perceptible pero no intrusivo | ai-voice-design |
| `navigator.vibrate(50)` en playBeep | Tercer canal sensorial: visual + auditivo + tactil. Maria siente el feedback incluso si no oye bien. No soportado en iOS (documentado) | design-everyday-things |
| Warning beep doble-pulso a 50s | Solo aviso visual es insuficiente — Maria puede estar mirando al techo mientras habla. Doble pulso = "atencion" sin ser alarma | sonic-branding |
| `recordWarning` como nueva constante | Patron estandar: cada evento sonoro tiene su propia entrada en AUDIO_FEEDBACK. Escalable si se agregan mas eventos | sonic-branding |

**Step 6: Commit**

```bash
git add docs/prompts/Q7-GRABACION-VOZ.md
git commit -m "fix(Q7): amplitude envelope, shared AudioContext, warning beep, haptic, triangle waveform"
```

---

### Task 2: Fix U1-U4 — Focus Trap, Escape Key, Back Button, Double-Tap Protection

**Files:**
- Modify: `docs/prompts/Q7-GRABACION-VOZ.md` — seccion PASO 2 (VoiceRecorder.tsx), funcion `handleToggle()`, overlay div, y imports

**Problema:**
El overlay declara `aria-modal="true"` pero NO implementa focus trap real. Tab key permite navegar al contenido detras del overlay. No hay Escape handler. El boton back del browser navega fuera en vez de cerrar overlay. Un double-tap accidental (tremor) envia grabacion de 0 segundos.

**Step 1: Agregar Escape key handler y focus trap**

Buscar la funcion `handleToggle()` (lineas ~544-551) y agregar ANTES de ella:

```typescript
const overlayRef = useRef<HTMLDivElement>(null);

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
```

**Step 2: Agregar double-tap protection en handleToggle()**

Buscar (lineas ~544-551):
```typescript
async function handleToggle() {
  if (isRecording) {
    const base64 = await stop();
    if (base64) onRecordingComplete(base64);
  } else {
    await start();
  }
}
```

Reemplazar con:
```typescript
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
```

**Step 3: Agregar `ref={overlayRef}` al div del overlay**

Buscar (linea ~572):
```typescript
<div
  className="fixed inset-0 bg-clara-bg z-50 flex flex-col items-center justify-center px-6"
  role="dialog"
```

Reemplazar con:
```typescript
<div
  ref={overlayRef}
  className="fixed inset-0 bg-clara-bg z-50 flex flex-col items-center justify-center px-6"
  role="dialog"
```

**Step 4: Actualizar imports del componente**

Buscar:
```typescript
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
```

Reemplazar con:
```typescript
import { useRef, useEffect } from "react";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
```

**Step 5: Actualizar tabla de decisiones y checklists**

Agregar a la tabla de decisiones de diseno:

| Decision | Razon | Heuristica |
|----------|-------|------------|
| Escape key cierra overlay | `aria-modal` requiere escape route. Maria o su nieto pueden usar teclado | Nielsen #3, WCAG 2.1.1 |
| Focus trap con querySelectorAll | Tab no escapa detras del overlay. Sin libreria externa (zero deps) | WCAG 2.4.3, ux-heuristics |
| `history.pushState` + popstate | En Android, el boton back navega fuera si no interceptamos. Overlay se cierra limpiamente | ux-heuristics, design-everyday-things |
| Guard `seconds < 1` en toggle | Maria con temblor puede hacer double-tap. Sin guard, envia 0s de audio → Whisper retorna basura | ux-heuristics (H5: error prevention) |
| `first.focus()` al montar | Focus va directo al primer boton interactivo. Screen reader anuncia el overlay inmediatamente | WCAG 2.4.3 |

Agregar al checklist de accesibilidad:
- [ ] Escape key cierra overlay (keydown listener)
- [ ] Focus trap activo — Tab no escapa al fondo
- [ ] Back button (Android) cierra overlay via popstate
- [ ] Double-tap < 1s descarta en vez de enviar

**Step 6: Commit**

```bash
git add docs/prompts/Q7-GRABACION-VOZ.md
git commit -m "fix(Q7): focus trap, Escape handler, back-button popstate, double-tap guard"
```

---

### Task 3: Fix T1-T4 — Timer Font, Error Text Sizing, Error Alignment

**Files:**
- Modify: `docs/prompts/Q7-GRABACION-VOZ.md` — seccion PASO 2 (VoiceRecorder.tsx), timer `<p>`, error `<div>`

**Problema:**
`font-mono` en el timer no esta definido en el tema — cae a system default que puede NO tener tabular nums. Error text a 18px es demasiado pequeno para contenido primario de error. Botones de error a 16px estan por debajo del minimo del design system. Error centrado multi-linea es dificil de leer.

**Step 1: Fix timer font — tabular-nums en vez de font-mono**

Buscar (lineas ~604-613):
```typescript
<p
  className={`font-mono text-[24px] mb-8 ${
    isWarning
      ? "text-clara-error font-bold"
      : "text-clara-text-secondary"
  }`}
  aria-live="polite"
>
```

Reemplazar con:
```typescript
<p
  className={`font-body text-[24px] tabular-nums mb-8 ${
    isWarning
      ? "text-clara-error font-bold"
      : "text-clara-text-secondary"
  }`}
  aria-live="polite"
>
```

> **Nota:** `tabular-nums` es una OpenType feature nativa de Inter (font-body). Cada digito ocupa el mismo ancho — el timer no "salta". Sin necesidad de cargar fuente monospace adicional.

**Step 2: Fix error text sizing — 18px → 20px**

Buscar (lineas ~672-674):
```typescript
<p className="text-clara-error text-body-sm mb-4">
  {t.mic_error}
</p>
```

Reemplazar con:
```typescript
<p className="text-clara-error text-body text-left mb-4">
  {t.mic_error}
</p>
```

> Cambios: `text-body-sm` → `text-body` (20px), `text-center` heredado → `text-left` explicito.

**Step 3: Fix error buttons sizing — 16px → 18px**

Buscar (lineas ~676-693):
```typescript
<button
  onClick={() => start()}
  className="px-4 min-h-touch-sm bg-clara-blue text-white rounded-lg
             text-label font-medium hover:bg-[#164d66]
             transition-colors duration-150"
>
  {t.try_again}
</button>
<button
  onClick={onCancel}
  className="px-4 min-h-touch-sm border-2 border-clara-border rounded-lg
             text-label font-medium text-clara-text-secondary
             hover:border-clara-blue hover:text-clara-blue
             transition-colors duration-150"
>
  {t.use_text}
</button>
```

Reemplazar ambos `text-label` con `text-body-sm`:
```typescript
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
```

> Cambios: `text-label` (16px) → `text-body-sm` (18px). Tambien agrego `focus-visible:outline` que faltaba en estos botones.

**Step 4: Fix error container alignment**

Buscar (linea ~671):
```typescript
<div role="alert" className="mt-6 text-center max-w-sm">
```

Reemplazar con:
```typescript
<div role="alert" className="mt-6 text-left max-w-sm">
```

**Step 5: Actualizar wireframe y decisiones**

Actualizar la tabla de decisiones con:

| Decision | Razon | Skill |
|----------|-------|-------|
| `font-body tabular-nums` en timer | Inter tiene OpenType `tnum`. Cada digito mismo ancho = timer estable. Sin fuente mono extra | web-typography |
| Error text 20px (`text-body`) | Contenido primario de error merece tamano completo. 18px demasiado pequeno para texto que Maria DEBE leer | web-typography |
| Error buttons 18px (`text-body-sm`) | 16px esta por debajo del minimo funcional del design system para botones de accion | web-typography |
| Error `text-left` | Texto multi-linea centrado es mas dificil de leer — los ojos pierden el inicio de cada linea | web-typography |

**Step 6: Commit**

```bash
git add docs/prompts/Q7-GRABACION-VOZ.md
git commit -m "fix(Q7): timer tabular-nums, error text 20px, error buttons 18px, text-left alignment"
```

---

### Task 4: Fix D1-D7 — Entry/Exit Animation, Waveform scaleY, Mic Scale Pulse, Token Hygiene

**Files:**
- Modify: `docs/prompts/Q7-GRABACION-VOZ.md` — seccion PASO 2 (VoiceRecorder.tsx), overlay div, waveform bars, mic button, globals.css notes

**Problema:**
El overlay aparece/desaparece con hard cut (conditional render). La onda usa `animate-pulse` (opacity) cuando deberia usar `scaleY` (height). `Math.random()` en JSX se re-ejecuta cada render. El mic pulsa opacity cuando deberia pulsar scale. Focus usa `focus:` en vez de `focus-visible:`. Cancel hover rojo colisiona con mic rojo.

**Step 1: Agregar keyframes CSS requeridos**

Agregar una nueva seccion despues de "Decisiones de diseno" en PASO 2, o como nota al inicio:

```
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

**Step 2: Fix overlay entry/exit — reemplazar conditional render**

Buscar en PASO 3, page.tsx (lineas ~853-862):
```typescript
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

Reemplazar con:
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

Y en VoiceRecorder.tsx, agregar `visible` a props:
```typescript
interface VoiceRecorderProps {
  visible: boolean;
  language: Language;
  onRecordingComplete: (audioBase64: string) => void;
  onCancel: () => void;
}
```

Y reemplazar el root div del overlay:
```typescript
// Early return si no visible Y animacion completada
const [mounted, setMounted] = useState(false);

useEffect(() => {
  if (visible) setMounted(true);
}, [visible]);

function handleTransitionEnd() {
  if (!visible) setMounted(false);
}

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
```

**Step 3: Fix waveform — scaleY + useMemo + bar sizing**

Buscar (lineas ~583-599):
```typescript
{isRecording && (
  <div
    className="flex items-center gap-1 mb-6 h-8"
    aria-hidden="true"
  >
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
```

Reemplazar con:
```typescript
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
```

Y agregar fuera del componente (despues de `labels`):
```typescript
/** Alturas seeded una sola vez — no re-randomize en cada render */
const BAR_HEIGHTS = Array.from({ length: 12 }, () => 16 + Math.random() * 20);
```

> Cambios: `animate-pulse` (opacity) → keyframe `waveBar` (scaleY). `Math.random()` movido fuera del render. `items-center` → `items-end` (barras crecen desde abajo). `gap-1` → `gap-1.5`, `w-1` → `w-1.5`, `h-8` → `h-10`. Duration 0.6s → 1.2s (50 BPM breathing rhythm).

**Step 4: Fix mic button — scale pulse + focus-visible + inline transition**

Buscar (lineas ~616-640):
```typescript
<button
  onClick={handleToggle}
  aria-label={isRecording ? t.tap_stop : t.tap_start}
  className={`
    w-touch-lg h-touch-lg rounded-full flex items-center justify-center
    transition-colors duration-200 mb-10
    focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2
    ${
      isRecording
        ? "bg-clara-error animate-pulse"
        : "bg-clara-blue hover:bg-[#164d66]"
    }
  `}
>
```

Reemplazar con:
```typescript
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
```

> Cambios: `animate-pulse` (opacity) → `gentlePulse` (scale 1.05). Transicion de color via inline style para interpolacion real blue→red. `focus:` → `focus-visible:` (no outline en tap). Hardcoded `hover:bg-[#164d66]` removido (en overlay no necesita hover — el boton ES la accion principal).

**Step 5: Fix Cancel hover y focus-visible en todos los botones**

Buscar en Cancel button (lineas ~647-652):
```typescript
hover:border-clara-error hover:text-clara-error
```

Reemplazar con:
```typescript
hover:border-clara-text hover:text-clara-text
```

Y reemplazar `focus:outline` con `focus-visible:outline` en Cancelar y Enviar:
```typescript
focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2
```

**Step 6: Actualizar tablas de decisiones y notas**

Agregar:

| Decision | Razon | Skill |
|----------|-------|-------|
| Entry fade+scale(0.97→1) 500ms | Hard cut es desorientante para Maria. Scale 3% = "respirar a la existencia". Usa `EASING.out` existente | top-design |
| Exit fade 300ms sin scale | Salida rapida pero no snap. Maria quiere volver al chat. Usa `EASING.in` | top-design |
| `waveBar` scaleY 1.2s | 50 BPM = ritmo cercano a latido cardiaco. Barras crecen en height, no parpadean en opacity. Metafora universal de "nivel de audio" | top-design |
| `BAR_HEIGHTS` fuera de render | `Math.random()` en JSX re-randomiza cada segundo (timer setState). Bug visual. useMemo o const externa = alturas estables | top-design, ux-heuristics |
| `gentlePulse` scale(1.05) 2s | 30 BPM = mas lento que waveform = ritmo en capas. 5% scale en 96px = 4.8px expansion. Perceptible, no agresivo. Metafora: "el mic respira" | top-design |
| `focus-visible:` en vez de `focus:` | `focus:` muestra outline en CADA tap (molesto para touch). `focus-visible:` solo para keyboard (correcto) | top-design |
| Cancel hover `clara-text` no `clara-error` | Rojo en hover Cancel colisiona con mic rojo grabando. Dos rojos compiten | top-design |
| `items-end` en waveform container | Barras crecen desde abajo (equalizer metaphor), no desde centro | top-design |

**Step 7: Commit**

```bash
git add docs/prompts/Q7-GRABACION-VOZ.md
git commit -m "fix(Q7): entry/exit animation, waveform scaleY, mic gentlePulse, focus-visible, bar sizing"
```

---

### Task 5: Fix E1-E3 — Corregir Claim WhatsApp, onerror Handler, stop() Timeout

**Files:**
- Modify: `docs/prompts/Q7-GRABACION-VOZ.md` — seccion PRINCIPIOS DE DISENO, PASO 1 (useAudioRecorder.ts)

**Problema:**
La documentacion dice que toggle es "el mismo modelo que WhatsApp" — esto es FALSO (WhatsApp usa press-and-hold). El MediaRecorder no tiene `onerror` handler — fallo mid-recording es silencioso. La Promise de `stop()` no tiene reject ni timeout — puede congelar UI.

**Step 1: Corregir claim WhatsApp en PRINCIPIOS DE DISENO**

Buscar (lineas ~200-201):
```
**1. Toggle, NO press-and-hold — esto no es negociable:**
Maria tiene temblor en las manos. Press-and-hold (mantener presionado) es fisicamente dificil para ella. El mecanismo es **toggle**: un toque para empezar a grabar, otro toque para parar. Es el mismo modelo que WhatsApp (nota de voz), que Maria ya usa.
```

Reemplazar con:
```
**1. Toggle, NO press-and-hold — esto no es negociable:**
Maria tiene temblor en las manos. Press-and-hold (mantener presionado) es fisicamente dificil para ella. El mecanismo es **toggle**: un toque para empezar a grabar, otro toque para parar.

> **NOTA IMPORTANTE:** Este es un modelo DIFERENTE al de WhatsApp (que usa press-and-hold). Clara usa toggle porque: (1) press-and-hold requiere fuerza sostenida que el temblor interrumpe, (2) toggle permite manos libres durante la grabacion, (3) cancel explicito es mas seguro que soltar-por-accidente. Maria necesitara aprender este nuevo patron, por eso las instrucciones son explicitas ("Toca para grabar" / "Toca para parar").
```

Tambien buscar en la tabla de Nielsen (linea ~965):
```
| 2 | Match between system and real world | Toggle = modelo WhatsApp. Microfono = icono universal. "Habla ahora" = lenguaje natural |
```

Reemplazar con:
```
| 2 | Match between system and real world | Toggle = mejora accesible sobre WhatsApp (press-and-hold). Instrucciones explicitas compensan la diferencia. Microfono = icono universal. "Habla ahora" = lenguaje natural |
```

**Step 2: Agregar onerror handler al MediaRecorder**

Buscar en `start()`, despues de `recorder.ondataavailable` (lineas ~366-368):
```typescript
recorder.ondataavailable = (e) => {
  if (e.data.size > 0) chunksRef.current.push(e.data);
};
```

Agregar justo despues:
```typescript
recorder.ondataavailable = (e) => {
  if (e.data.size > 0) chunksRef.current.push(e.data);
};

// Handler de error mid-recording (stream interrumpido, bluetooth desconectado, etc.)
recorder.onerror = () => {
  cleanup();
  setState((prev) => ({
    ...prev,
    isRecording: false,
    error: "La grabacion se interrumpio. Intenta de nuevo.",
  }));
};
```

Y agregar label bilingue para este error en `labels`:
```typescript
const labels = {
  es: {
    // ... existentes ...
    recording_interrupted: "La grabacion se interrumpio. Intenta de nuevo.",
  },
  fr: {
    // ... existentes ...
    recording_interrupted: "L'enregistrement a ete interrompu. Reessaye.",
  },
};
```

**Step 3: Agregar reject + timeout a stop() Promise**

Buscar `stop()` (lineas ~399-425):
```typescript
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

    playBeep(AUDIO_FEEDBACK.recordStop);
    recorder.stop();
  });
}, []);
```

Reemplazar con:
```typescript
const stop = useCallback((): Promise<string> => {
  return new Promise((resolve, reject) => {
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

    playBeep(AUDIO_FEEDBACK.recordStop);
    recorder.stop();
  });
}, [cleanup]);
```

**Step 4: Actualizar tabla de decisiones**

| Decision | Razon | Skill |
|----------|-------|-------|
| Corregir claim WhatsApp | Documentacion incorrecta puede propagarse a training materials. Toggle es MEJOR para tremor, pero es DIFERENTE de WhatsApp | design-everyday-things |
| `recorder.onerror` | Sin handler, fallo mid-recording (bluetooth, tab background iOS) es silencioso. Audio corrupto se envia | design-everyday-things |
| `stop()` con try/catch + timeout 5s | Promise sin reject puede congelar overlay indefinidamente. 5s timeout = fallback graceful. Resolve("") en vez de reject = overlay siempre cierra | design-everyday-things |

**Step 5: Commit**

```bash
git add docs/prompts/Q7-GRABACION-VOZ.md
git commit -m "fix(Q7): correct WhatsApp claim, add onerror handler, add stop() timeout"
```

---

### Task 6: Actualizar ROL, Checklists, y Definition of Done

**Files:**
- Modify: `docs/prompts/Q7-GRABACION-VOZ.md` — seccion ROL (reframe), checklists finales

**Problema:**
El ROL describe la voz como "la segunda via de entrada mas importante". El audience research revela que para Maria/Ahmed/Fatima, la voz es la via PRIMARIA — escribir es el fallback. Los checklists no incluyen los nuevos items de las 7 reviews.

**Step 1: Reframe el ROL**

Buscar (linea ~14):
```
Eres un **ingeniero frontend senior Y disenador de interaccion de audio** construyendo la segunda via de entrada mas importante de Clara: la voz.
```

Reemplazar con:
```
Eres un **ingeniero frontend senior Y disenador de interaccion de audio** construyendo la **via de entrada PRIMARIA** de Clara: la voz. Para Maria de 74 anos, Ahmed que escribe frances en teclado espanol, y Fatima que no es alfabetizada en espanol — escribir es el fallback. Hablar es lo natural.
```

**Step 2: Agregar items al checklist de accesibilidad (20 pts → 28 pts)**

Agregar despues del bloque existente de "Error de microfono":

```markdown
**Interaccion (nuevos):**
- [ ] Escape key cierra overlay (keydown listener)
- [ ] Focus trap activo — Tab cicla dentro del overlay
- [ ] Back button (Android) cierra overlay via popstate
- [ ] Double-tap < 1s no envia grabacion (guard en handleToggle)
- [ ] `focus-visible:` en todos los botones (no `focus:`)
- [ ] `recorder.onerror` handler — fallo mid-recording muestra error
- [ ] `stop()` con timeout 5s — UI nunca se congela
- [ ] Entry/exit animation con prefers-reduced-motion respetado
```

**Step 3: Agregar items al checklist de marca (7 pts → 10 pts)**

```markdown
- [ ] Beeps con amplitude envelope (20ms attack, 30ms release) — sin clicks
- [ ] Waveform scaleY breathing (1.2s, 50 BPM) — no opacity pulse
- [ ] Mic button gentlePulse scale (2s, 30 BPM) — ritmo en capas
```

**Step 4: Agregar items al checklist de integracion (8 pts → 11 pts)**

```markdown
- [ ] `AUDIO_FEEDBACK.recordWarning` definido en constants.ts
- [ ] Warning beep doble-pulso a 50 segundos
- [ ] `navigator.vibrate(50)` como feedback tactil en cada beep
```

**Step 5: Actualizar Definition of Done**

Agregar al final del prompt:

```markdown
### DEFINITION OF DONE ACTUALIZADA (post-review de 7 skills)

El Q7 esta completo cuando:
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
```

**Step 6: Commit**

```bash
git add docs/prompts/Q7-GRABACION-VOZ.md
git commit -m "fix(Q7): reframe voice as primary channel, update checklists with 7-review findings"
```

---

## Orden de Ejecucion

```
Task 1 (playBeep + envelope + warning beep + haptic)
  ↓
Task 2 (focus trap + Escape + back-button + double-tap)
  ↓
Task 3 (timer font + error sizing + alignment)
  ↓
Task 4 (entry/exit animation + waveform scaleY + mic pulse + token hygiene)
  ↓
Task 5 (WhatsApp claim + onerror + stop timeout)
  ↓
Task 6 (ROL reframe + checklists + DoD)
```

Cada Task es un commit independiente. No hay dependencias cruzadas — se pueden ejecutar en cualquier orden, pero el orden sugerido va de infraestructura (audio engine) → interaccion → tipografia → animacion → documentacion → meta.

---

## Resumen de Impacto

| Metrica | Antes (Q7 original) | Despues (con 7 reviews) |
|---------|---------------------|------------------------|
| **UX Heuristics** | 7.5/10 | ~9/10 |
| **Top Design** | 5.5/10 | ~8.9/10 |
| **Sonic Quality** | Clicks audibles | Envelope suave, paleta tonal F Mayor |
| **Typography** | font-mono undefined | tabular-nums, sizing correcto |
| **Accessibility** | 20 checklist items | 28 checklist items |
| **Error Handling** | Sin onerror, sin timeout | onerror + 5s timeout + try/catch |
| **Documentation** | Claim WhatsApp incorrecto | Corregido con justificacion |
| **Feedback Channels** | 2 (visual + audio) | 3 (visual + audio + tactil) |
