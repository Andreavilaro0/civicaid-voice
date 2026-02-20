# Q9 Document Upload — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear DocumentUpload — componente de subida de documento (camara + galeria) con preview, base64 encoding y overlay accesible, para que Maria pueda fotografiar una carta del gobierno y Clara se la explique.

**Architecture:** Overlay full-screen (patron identico a VoiceRecorder.tsx), dos inputs HTML ocultos (`capture="environment"` para camara, sin capture para galeria), FileReader para base64, preview con Cancel/Send. Integra con `useChat.send(text, undefined, imageBase64)` que ya soporta imagenes. LoadingContext `"reading"` ya definido.

**Tech Stack:** Next.js 16.1, React 19.2, TypeScript 5, Tailwind CSS 4, react-aria-components (Button), HTMLInputElement file API, FileReader API

---

## Estado Actual: Infraestructura LISTA

Todo el backend y hook layer ya soporta imagenes:

| Componente | Estado | Notas |
|-----------|--------|-------|
| `types.ts` — `ChatRequest.image_base64` | LISTO | Campo definido |
| `types.ts` — `LoadingContext = "reading"` | LISTO | Para animacion "Clara esta leyendo..." |
| `useChat.ts` — `send(text, audio?, image?)` | LISTO | Detecta `imageBase64` y usa `input_type: "image"` |
| `api.ts` — `sendMessage()` | LISTO | Incluye `image_base64` en request body |
| `chat/page.tsx` — `onOpenCamera` | STUB | `alert(comingSoon)` — reemplazar con overlay |
| `ChatInput.tsx` — boton Foto | LISTO | Ya llama `onOpenCamera()` |
| `Button.tsx` — componente UI | LISTO | `variant`, `icon`, `fullWidth`, react-aria |
| `VoiceRecorder.tsx` — patron referencia | LISTO | Overlay, focus trap, Escape, back button |

**Solo falta:** Crear `DocumentUpload.tsx` + conectar en `chat/page.tsx`.

---

## Skills Relevantes para Enhancement

| Skill | Uso |
|-------|-----|
| `ux-heuristics` | Maria test: botones 64px, texto 20px+, labels claros, error recovery |
| `design-everyday-things` | Modelo mental: camara del telefono es familiar, galeria es familiar — zero learning curve |
| `top-design` | Animaciones de entrada overlay, transicion a preview, easing expo-out |
| `web-typography` | tabular-nums no aplica aqui, pero Atkinson Hyperlegible en labels a 20px+ |
| `sonic-branding` | Feedback auditivo sutil al capturar foto (shutter click via Web Audio API) |

---

### Task 1: Crear DocumentUpload.tsx (componente base)

**Files:**
- Create: `clara-web/src/components/DocumentUpload.tsx`

**Step 1: Crear el archivo con estructura completa**

Crear `clara-web/src/components/DocumentUpload.tsx`:

```typescript
"use client";

import { useState, useRef, useEffect } from "react";
import type { Language } from "@/lib/types";
import Button from "@/components/ui/Button";

/* ------------------------------------------------------------------ */
/*  Props                                                              */
/* ------------------------------------------------------------------ */

interface DocumentUploadProps {
  visible: boolean;
  language: Language;
  onUpload: (imageBase64: string) => void;
  onCancel: () => void;
}

/* ------------------------------------------------------------------ */
/*  Labels bilingues                                                   */
/* ------------------------------------------------------------------ */

const labels = {
  es: {
    title: "Subir documento",
    desc: "Sube una foto de tu documento o carta. Clara te explicara que dice.",
    camera: "Hacer foto",
    gallery: "Elegir de galeria",
    cancel: "Cancelar",
    send: "Enviar a Clara",
    preview: "Vista previa del documento",
    change: "Cambiar foto",
    error_read: "No se pudo leer la imagen. Prueba con otra foto.",
    error_size: "La imagen es muy grande. Prueba con una foto mas pequena.",
  },
  fr: {
    title: "Envoyer un document",
    desc: "Envoie une photo de ton document ou courrier. Clara t'expliquera ce qu'il dit.",
    camera: "Prendre une photo",
    gallery: "Choisir dans la galerie",
    cancel: "Annuler",
    send: "Envoyer a Clara",
    preview: "Apercu du document",
    change: "Changer la photo",
    error_read: "Impossible de lire l'image. Essaie avec une autre photo.",
    error_size: "L'image est trop grande. Essaie avec une photo plus petite.",
  },
};

/** Max 10MB antes de base64 encoding */
const MAX_FILE_SIZE = 10 * 1024 * 1024;

/* ------------------------------------------------------------------ */
/*  Componente                                                        */
/* ------------------------------------------------------------------ */

export default function DocumentUpload({
  visible,
  language,
  onUpload,
  onCancel,
}: DocumentUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [base64, setBase64] = useState("");
  const [error, setError] = useState<string | null>(null);
  const cameraRef = useRef<HTMLInputElement>(null);
  const galleryRef = useRef<HTMLInputElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const t = labels[language];

  /* ---- Entry/exit animation (patron VoiceRecorder) ---- */
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (visible) setMounted(true);
  }, [visible]);

  function handleTransitionEnd() {
    if (!visible) setMounted(false);
  }

  /* ---- Escape key cierra overlay ---- */
  useEffect(() => {
    if (!mounted) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") handleCancel();
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  /* ---- Focus trap ---- */
  useEffect(() => {
    if (!mounted) return;
    const overlay = overlayRef.current;
    if (!overlay) return;

    const focusable = overlay.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length === 0) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
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
  }, [mounted, preview]); // re-run cuando cambia preview (botones cambian)

  /* ---- Android back button ---- */
  useEffect(() => {
    if (!mounted) return;
    history.pushState({ documentOverlay: true }, "");
    function onPopState() {
      handleCancel();
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  /* ---- File handling ---- */
  function handleFile(file: File) {
    setError(null);

    if (file.size > MAX_FILE_SIZE) {
      setError(t.error_size);
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      setPreview(result);
      setBase64(result.split(",")[1]);
    };
    reader.onerror = () => {
      setError(t.error_read);
    };
    reader.readAsDataURL(file);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    // Reset input para permitir re-seleccion del mismo archivo
    e.target.value = "";
  }

  function handleCancel() {
    setPreview(null);
    setBase64("");
    setError(null);
    onCancel();
  }

  function handleSend() {
    if (base64) onUpload(base64);
  }

  function handleChangePhoto() {
    setPreview(null);
    setBase64("");
    setError(null);
  }

  if (!mounted) return null;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 bg-clara-bg z-50 flex flex-col px-6 py-8"
      role="dialog"
      aria-label={t.title}
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
      {/* Header — boton atras + titulo */}
      <div className="flex items-center mb-6">
        <button
          onClick={handleCancel}
          aria-label={t.cancel}
          className="min-w-touch-sm min-h-touch-sm flex items-center justify-center
                     rounded-lg transition-colors duration-150
                     hover:bg-clara-card
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
          </svg>
        </button>
        <h2 className="font-display font-bold text-h2 text-clara-text ml-2">
          {t.title}
        </h2>
      </div>

      {/* Descripcion — amable, breve (ux-heuristics: get rid of half the words) */}
      <p className="text-body text-clara-text-secondary mb-8 leading-relaxed">
        {t.desc}
      </p>

      {/* Hidden file inputs */}
      <input
        ref={cameraRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleChange}
        className="hidden"
        aria-hidden="true"
        tabIndex={-1}
      />
      <input
        ref={galleryRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
        aria-hidden="true"
        tabIndex={-1}
      />

      {/* Error state */}
      {error && (
        <div role="alert" className="mb-6 p-4 bg-red-50 border-2 border-clara-error/20 rounded-xl">
          <p className="text-body text-clara-error">{error}</p>
        </div>
      )}

      {/* Estado: Preview de la imagen capturada */}
      {preview ? (
        <div className="flex-1 flex flex-col items-center justify-center">
          <div className="relative mb-6 w-full max-w-sm">
            <img
              src={preview}
              alt={t.preview}
              className="w-full max-h-[50vh] rounded-xl border-2 border-clara-border object-contain"
            />
          </div>

          {/* Acciones: Cambiar / Enviar */}
          <div className="flex gap-4 w-full max-w-sm">
            <Button
              variant="secondary"
              fullWidth
              onPress={handleChangePhoto}
            >
              {t.change}
            </Button>
            <Button
              variant="primary"
              fullWidth
              onPress={handleSend}
            >
              {t.send}
            </Button>
          </div>
        </div>
      ) : (
        /* Estado: Seleccion de fuente (camara o galeria) */
        <div className="flex-1 flex flex-col items-center justify-center gap-4 max-w-sm mx-auto w-full">
          {/* Boton Camara — grande, prominente (design-everyday-things: familiar camera metaphor) */}
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

          {/* Boton Galeria — secundario */}
          <Button
            variant="secondary"
            fullWidth
            onPress={() => galleryRef.current?.click()}
            icon={
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" />
              </svg>
            }
          >
            {t.gallery}
          </Button>

          {/* Cancelar — texto sutil */}
          <button
            onClick={handleCancel}
            className="mt-4 text-body-sm text-clara-text-secondary underline underline-offset-4
                       min-h-touch-sm flex items-center
                       hover:text-clara-text transition-colors duration-150
                       focus-visible:outline focus-visible:outline-[3px]
                       focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          >
            {t.cancel}
          </button>
        </div>
      )}
    </div>
  );
}
```

**Notas de accesibilidad (ux-heuristics / design-everyday-things):**
- `role="dialog"`, `aria-modal="true"` — screen readers anuncian overlay
- Focus trap con Tab — teclado no escapa
- Escape cierra — salida de emergencia (Nielsen H3: User Control)
- Android back button cierra — expectativa natural
- Boton camara 72px alto — Maria puede tocarlo con temblor
- Error en `role="alert"` — screen reader anuncia inmediatamente
- `capture="environment"` — abre camara trasera directamente (design-everyday-things: natural mapping)
- Preview con `alt` descriptivo — accesible
- Reset de `e.target.value = ""` — permite re-seleccionar mismo archivo

**Step 2: Verificar que TypeScript compila**

Run: `cd clara-web && npx tsc --noEmit`
Expected: No errors

**Step 3: Commit**

```bash
git add clara-web/src/components/DocumentUpload.tsx
git commit -m "feat: add DocumentUpload component with camera, gallery, preview, and a11y overlay"
```

---

### Task 2: Integrar DocumentUpload en chat page

**Files:**
- Modify: `clara-web/src/app/chat/page.tsx`

**Step 1: Agregar import y estado**

En `chat/page.tsx`, agregar import de DocumentUpload:

```typescript
import DocumentUpload from "@/components/DocumentUpload";
```

Agregar estado `documentActive`:

```typescript
const [documentActive, setDocumentActive] = useState(false);
```

**Step 2: Reemplazar stub de onOpenCamera**

Cambiar:
```typescript
onOpenCamera={() => {
  // Q9 reemplazara con DocumentUpload
  alert(comingSoon[language]);
}}
```

Por:
```typescript
onOpenCamera={() => setDocumentActive(true)}
```

**Step 3: Agregar DocumentUpload overlay (junto a VoiceRecorder)**

Despues del `<VoiceRecorder>`, agregar:

```typescript
{/* DocumentUpload overlay — patron identico a VoiceRecorder */}
<DocumentUpload
  visible={documentActive}
  language={language}
  onUpload={(imageBase64) => {
    setDocumentActive(false);
    send("", undefined, imageBase64);
  }}
  onCancel={() => setDocumentActive(false)}
/>
```

**Step 4: Limpiar la constante comingSoon (ya no se usa)**

Eliminar:
```typescript
const comingSoon: Record<Language, string> = {
  es: "Esta funcion estara disponible pronto",
  fr: "Cette fonction sera bientot disponible",
};
```

**Step 5: Verificar TypeScript**

Run: `cd clara-web && npx tsc --noEmit`
Expected: No errors

**Step 6: Commit**

```bash
git add clara-web/src/app/chat/page.tsx
git commit -m "feat: integrate DocumentUpload overlay in chat page, replace camera stub"
```

---

### Task 3: Polish visual — animaciones y transiciones (top-design)

**Files:**
- Modify: `clara-web/src/components/DocumentUpload.tsx`
- Modify: `clara-web/src/app/globals.css`

**Que mejora:** La transicion entre estado "seleccion" y "preview" es abrupta. Agregar animacion suave.

**Step 1: Agregar keyframe para preview entrance en globals.css**

En `globals.css`, despues del keyframe `playHintPulse`, agregar:

```css
/* Document preview entrance — scale up from center */
@keyframes previewEnter {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}
```

**Step 2: Aplicar animacion al contenedor de preview en DocumentUpload.tsx**

En el `<div>` que envuelve la imagen preview, agregar estilo:

```tsx
<div
  className="relative mb-6 w-full max-w-sm"
  style={{ animation: "previewEnter 400ms cubic-bezier(0.16, 1, 0.3, 1)" }}
>
```

**Step 3: Agregar borde animado en estado preview**

Cambiar el borde de la imagen de `border-clara-border` a un borde verde que indica "listo para enviar":

```tsx
className="w-full max-h-[50vh] rounded-xl border-2 border-clara-green/50 object-contain shadow-lg shadow-clara-green/10"
```

**Step 4: Verificar TypeScript + build**

Run: `cd clara-web && npx tsc --noEmit`
Expected: No errors

**Step 5: Commit**

```bash
git add clara-web/src/components/DocumentUpload.tsx clara-web/src/app/globals.css
git commit -m "polish: smooth preview entrance animation and green ready-state border"
```

---

### Task 4: Feedback auditivo al capturar (sonic-branding)

**Files:**
- Modify: `clara-web/src/components/DocumentUpload.tsx`

**Que mejora:** Al seleccionar una imagen, un micro-sonido (shutter click) confirma que la foto se capturo. Util para Maria que puede no ver el cambio visual inmediatamente.

**Step 1: Agregar funcion de feedback auditivo**

Dentro del componente, antes de `handleFile`:

```typescript
/** Shutter click feedback via Web Audio API (sonic-branding) */
function playShutterFeedback() {
  if (typeof AudioContext === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = 1200;
    gain.gain.setValueAtTime(0.06, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
  } catch { /* silent fail */ }
}
```

**Step 2: Llamar feedback en handleFile exito**

En `reader.onload`, despues de `setBase64(...)`:

```typescript
reader.onload = () => {
  const result = reader.result as string;
  setPreview(result);
  setBase64(result.split(",")[1]);
  playShutterFeedback();
};
```

**Step 3: Commit**

```bash
git add clara-web/src/components/DocumentUpload.tsx
git commit -m "sonic: shutter click feedback on document capture"
```

---

### Task 5: Verificacion final — "Maria Test" + build

**Checklist de accesibilidad (manual):**

- [ ] Boton "Hacer foto" tiene 72px minimo de alto? (className `h-[72px]`)
- [ ] Boton "Elegir de galeria" tiene 64px minimo? (min-h-touch)
- [ ] Labels bilingues funcionan? (ES + FR)
- [ ] `capture="environment"` abre camara trasera en movil?
- [ ] Escape cierra overlay?
- [ ] Tab queda atrapado dentro del overlay? (focus trap)
- [ ] Android back button cierra overlay?
- [ ] Error de archivo grande muestra mensaje amable? (role="alert")
- [ ] Error de lectura muestra mensaje amable?
- [ ] Preview muestra imagen correcta?
- [ ] "Cambiar foto" vuelve a seleccion?
- [ ] "Enviar a Clara" llama onUpload con base64?
- [ ] focus-visible muestra outline de 3px?
- [ ] prefers-reduced-motion desactiva animaciones?
- [ ] LoadingState muestra "Clara esta leyendo tu documento..."?

**Step 1: Run build final**

Run: `cd clara-web && npm run build`
Expected: PASS

**Step 2: Run type check**

Run: `cd clara-web && npx tsc --noEmit`
Expected: No errors

**Step 3: Commit final**

```bash
git add -A
git commit -m "Q9: document upload verified — camera, gallery, preview, a11y overlay"
```

---

## Resumen de Archivos

| Archivo | Accion |
|---------|--------|
| `src/components/DocumentUpload.tsx` | Crear: overlay completo con camara, galeria, preview, a11y |
| `src/app/chat/page.tsx` | Modificar: integrar DocumentUpload, eliminar stub |
| `src/app/globals.css` | Modificar: agregar keyframe `previewEnter` |

## Infraestructura que YA EXISTE (no tocar)

| Archivo | Que provee |
|---------|-----------|
| `src/lib/types.ts` | `ChatRequest.image_base64`, `LoadingContext = "reading"` |
| `src/hooks/useChat.ts` | `send(text, audio?, image?)` — auto-detecta imagen |
| `src/lib/api.ts` | `sendMessage()` con `image_base64` en body |
| `src/components/ui/Button.tsx` | Componente react-aria con variantes |
| `src/components/VoiceRecorder.tsx` | Patron de referencia (overlay, focus trap) |

## Herramientas Gratuitas de Internet Usadas

| Herramienta | Uso |
|-------------|-----|
| HTML File API | `<input type="file" accept="image/*" capture="environment">` (nativo, gratis) |
| FileReader API | Conversion a base64 (nativo, gratis) |
| Web Audio API | Feedback auditivo shutter click (nativo, gratis) |
| Google Fonts CDN | Atkinson Hyperlegible (ya configurado) |

## Personas — Como Q9 Ayuda a Cada Una

| Persona | Escenario | Como DocumentUpload ayuda |
|---------|-----------|--------------------------|
| **Maria, 74** | Recibe carta del gobierno sobre IMV, no entiende las palabras | Hace foto con boton grande (72px), Clara le explica en lenguaje sencillo |
| **Ahmed, 28** | Tiene documento de empadronamiento en espanol, necesita entender | Sube foto desde galeria, Clara responde en frances |
| **Fatima, 45** | Recibe notificacion sanitaria para su hijo, no puede leer espanol | Hace foto directamente, Clara le explica paso a paso |

---

*Plan creado para OdiseIA4Good Hackathon, UDIT, Febrero 2026*
*Clara — Andrea Avila*
