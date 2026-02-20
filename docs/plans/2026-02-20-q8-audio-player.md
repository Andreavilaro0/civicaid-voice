# Q8 Audio Player — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verificar, pulir y potenciar el Audio Player de Clara para que la demo del hackathon sea impresionante.

**Architecture:** El AudioPlayer ya esta implementado con singleton pattern, seekbar accesible, labels bilingues (ES/FR) y speed cycling. El plan se enfoca en verificacion, polish visual y enhancement para WOW factor.

**Tech Stack:** Next.js 16.1, React 19.2, TypeScript 5, Tailwind CSS 4, HTMLAudioElement API

---

## Estado Actual: Q8 YA IMPLEMENTADO

Los 3 archivos del spec Q8 existen y coinciden con la especificacion:

| Archivo | Estado | Notas |
|---------|--------|-------|
| `src/hooks/useAudioPlayer.ts` | COMPLETO | Singleton, 8 event listeners, speed cycling, seek |
| `src/components/ui/AudioPlayer.tsx` | COMPLETO | Play/pause/replay, seekbar, speed, error state, bilingual |
| `src/components/MessageList.tsx` | INTEGRADO | AudioPlayer renderizado dentro de ChatBubble |

**TypeScript:** Compila sin errores (`npx tsc --noEmit` = clean).

---

## Skills Relevantes para Enhancement

| Skill | Uso |
|-------|-----|
| `top-design` | Micro-animaciones: transicion play->pause, fill de barra con easing, hover magnetico |
| `ux-heuristics` | Validar "Maria test" — puede escuchar sin instrucciones? Trunk test en chat |
| `web-typography` | tabular-nums en tiempo, tamanos legibles a 20px+ |
| `sonic-branding` | Feedback auditivo sutil al tocar play (triangle wave 0.1s) |
| `design-everyday-things` | Modelo mental WhatsApp voice note — familiarity |
| `artifacts-builder` | Crear demo interactiva standalone del audio player |

---

### Task 1: Verificar build completo

**Files:**
- Check: `clara-web/` (full project)

**Step 1: Run build**

Run: `cd clara-web && npm run build`
Expected: Build succeeds without errors

**Step 2: Verify type safety**

Run: `cd clara-web && npx tsc --noEmit`
Expected: No errors (already verified = PASS)

**Step 3: Commit verification**

```bash
git add -A
git commit -m "verify: Q8 audio player implementation complete"
```

---

### Task 2: Animar la transicion play/pause/replay (top-design)

**Files:**
- Modify: `clara-web/src/components/ui/AudioPlayer.tsx`

**Que mejora:** Los iconos SVG cambian bruscamente. Agregar transicion CSS suave entre estados.

**Step 1: Agregar clase de transicion al contenedor de iconos**

Envolver los iconos SVG del boton play/pause en un `<span>` con:
```css
transition: transform 150ms cubic-bezier(0.16, 1, 0.3, 1), opacity 100ms;
```

**Step 2: Agregar scale feedback al tap**

El `active:scale-95` ya existe. Agregar `transition-transform` con expo-out easing para que el bounce back sea satisfactorio.

**Step 3: Animar el fill de la barra de progreso**

Cambiar el `transition-[width] duration-200 ease-linear` del fill a:
```css
transition: width 250ms cubic-bezier(0.16, 1, 0.3, 1);
```

Esto hace que el fill tenga un micro-ease que se siente mas organico.

**Step 4: Commit**

```bash
git add src/components/ui/AudioPlayer.tsx
git commit -m "polish: smooth icon transitions and progress bar easing"
```

---

### Task 3: Mejorar accesibilidad visual del seekbar (ux-heuristics)

**Files:**
- Modify: `clara-web/src/components/ui/AudioPlayer.tsx`

**Que mejora:** La seekbar no tiene thumb/indicator visual. Maria no sabe que puede tocarla.

**Step 1: Agregar thumb indicator**

Despues del fill `<div>`, agregar un circulo indicador de posicion:
```tsx
<div
  className="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-clara-green rounded-full
             shadow-sm opacity-0 group-hover:opacity-100 group-focus-visible:opacity-100
             transition-opacity duration-200"
  style={{ left: `calc(${progress}% - 8px)` }}
  aria-hidden="true"
/>
```

Esto aparece al hover/focus, indicando que la barra es interactiva.

**Step 2: Agregar hint visual en estado idle**

Si `progress === 0` y no esta playing, mostrar una animacion sutil de pulso en el boton play para invitar a Maria a tocarlo.

**Step 3: Commit**

```bash
git add src/components/ui/AudioPlayer.tsx
git commit -m "a11y: seekbar thumb indicator and idle play hint"
```

---

### Task 4: Feedback auditivo sutil (sonic-branding)

**Files:**
- Modify: `clara-web/src/hooks/useAudioPlayer.ts`

**Que mejora:** Al tocar play, un micro-sonido (click suave) confirma la accion. Especialmente util para Maria que puede no ver el cambio visual inmediatamente.

**Step 1: Agregar haptic/audio feedback**

En `togglePlay()`, antes de `audio.play()`, llamar a un feedback sutil via Web Audio API:
```typescript
function playClickFeedback() {
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "triangle";
    osc.frequency.value = 800;
    gain.gain.value = 0.05;
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
  } catch { /* silent fail */ }
}
```

Envolver en `if (typeof AudioContext !== 'undefined')` y respetar `prefers-reduced-motion`.

**Step 2: Commit**

```bash
git add src/hooks/useAudioPlayer.ts
git commit -m "sonic: subtle click feedback on play action"
```

---

### Task 5: Demo standalone del Audio Player (artifacts-builder)

**Files:**
- Create: `presentacion/demo-audioplayer.html`

**Que mejora:** Una demo interactiva standalone que muestra el audio player funcionando con datos de ejemplo, para la presentacion del hackathon.

**Step 1: Crear HTML self-contained**

Un HTML con el AudioPlayer renderizado mostrando 3 escenarios:
1. Maria escuchando respuesta sobre IMV (espanol)
2. Ahmed escuchando en frances
3. Estado de error graceful

Incluir audio de ejemplo (puede ser un simple sine wave generado con Web Audio API).

**Step 2: Estilizar con la misma paleta Clara**

Usar los mismos colores: `#2E7D4F` (green), `#1B5E7B` (blue), `#FAFAFA` (bg).
Fuente: Atkinson Hyperlegible via Google Fonts CDN.

**Step 3: Commit**

```bash
git add presentacion/demo-audioplayer.html
git commit -m "demo: standalone audio player showcase for hackathon"
```

---

### Task 6: Verificacion final — "Maria Test"

**Checklist de accesibilidad (manual):**

- [ ] Boton play tiene 48x48px minimo?  (min-w-[48px] min-h-[48px])
- [ ] Seekbar tiene zona tactil de 32px?  (h-8)
- [ ] Labels bilingues funcionan?  (ES + FR)
- [ ] ArrowLeft/Right mueven seekbar?  (5% increment)
- [ ] focus-visible muestra outline?  (3px green)
- [ ] Error state muestra mensaje amable?  (role="alert")
- [ ] Speed cycling funciona? (0.75x -> 1x -> 1.25x)
- [ ] Solo un audio a la vez? (singleton claimPlayback)
- [ ] prefers-reduced-motion desactiva animaciones?

**Step 1: Run build final**

Run: `cd clara-web && npm run build`
Expected: PASS

**Step 2: Commit final**

```bash
git add -A
git commit -m "Q8: audio player verified and polished for hackathon demo"
```

---

## Resumen de Archivos

| Archivo | Accion |
|---------|--------|
| `src/hooks/useAudioPlayer.ts` | Modificar: agregar click feedback |
| `src/components/ui/AudioPlayer.tsx` | Modificar: thumb indicator, animaciones |
| `presentacion/demo-audioplayer.html` | Crear: demo standalone |

## Herramientas Gratuitas de Internet Usadas

| Herramienta | Uso |
|-------------|-----|
| Google Fonts CDN | Atkinson Hyperlegible (gratis) |
| Web Audio API | Feedback auditivo sin archivos MP3 |
| Web Speech API | Ya usado en welcome page |

---

*Plan creado para OdiseIA4Good Hackathon, UDIT, Febrero 2026*
*Clara — Andrea Avila*
