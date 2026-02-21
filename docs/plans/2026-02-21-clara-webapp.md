# Clara Web App — Enhance Existing App + Demo de Impacto

> **For Claude:** Ejecuta este plan en **team agent mode**. Crea el equipo `clara-webapp` con 6 agentes. Usa superpowers:executing-plans para coordinar.

**Goal:** Mejorar la app Next.js EXISTENTE en `clara-web/` y crear un demo HTML standalone para el pitch. NO crear desde cero — ya hay 21 archivos fuente, componentes, hooks, API client, y design system.

---

## LO QUE YA EXISTE (NO recrear)

### Next.js App (`clara-web/`) — 21 archivos, ~102K

| Archivo | Que tiene | Estado |
|---------|-----------|--------|
| `src/app/page.tsx` (13K) | Landing: logo SVG, greeting ES/FR, mic button 120px, topic chips, language selector | FUNCIONAL |
| `src/app/chat/page.tsx` (2.5K) | Chat: Header + MessageList + ChatInput + VoiceRecorder + DocumentUpload | FUNCIONAL |
| `src/app/globals.css` (3.5K) | Tailwind v4, Clara palette, keyframes (waveBar, gentlePulse, logoRipple, fadeInUp, float) | FUNCIONAL |
| `src/app/layout.tsx` (1.4K) | Root: Atkinson Hyperlegible + Inter fonts, metadata, skip-to-content | FUNCIONAL |
| `tailwind.config.ts` (1.2K) | Clara colors, fonts, sizes, touch targets, bubble radius | FUNCIONAL |
| `src/components/ui/Button.tsx` | Generic button (primary/secondary) | FUNCIONAL |
| `src/components/ui/ChatBubble.tsx` | Chat bubble (user/clara) | FUNCIONAL |
| `src/components/ui/LoadingState.tsx` | 3 waveform bars (listening/thinking/reading) | FUNCIONAL |
| `src/components/ui/AudioPlayer.tsx` (9.8K) | Play/pause/speed/progress, bilingual labels | FUNCIONAL |
| `src/components/ui/LanguageSelector.tsx` (1.4K) | ES/FR toggle | NECESITA AR |
| `src/components/Header.tsx` (2.6K) | Clara logo + language selector | FUNCIONAL |
| `src/components/MessageList.tsx` (4.3K) | Auto-scroll, AudioPlayer integration | FUNCIONAL |
| `src/components/ChatInput.tsx` (6.1K) | Text/voice/image mode toggle | FUNCIONAL |
| `src/components/VoiceRecorder.tsx` (11K) | Web Audio API, 60s max, feedback beeps | FUNCIONAL |
| `src/components/DocumentUpload.tsx` (12K) | Camera/gallery, base64, size validation | FUNCIONAL |
| `src/hooks/useChat.ts` (7.5K) | Messages state, API calls, session_id, errors | FUNCIONAL |
| `src/hooks/useAudioRecorder.ts` (7.3K) | MediaRecorder wrapper, base64 encoding | FUNCIONAL |
| `src/hooks/useAudioPlayer.ts` (6.8K) | HTMLAudioElement wrapper | FUNCIONAL |
| `src/lib/api.ts` (7K) | HTTP client, POST /api/chat, timeout, errors | FUNCIONAL |
| `src/lib/types.ts` (4.6K) | TypeScript contracts (Language="es"\|"fr", ChatRequest, etc.) | NECESITA AR |
| `src/lib/constants.ts` (4K) | COLORS, EASING, DURATION, AUDIO_FEEDBACK | FUNCIONAL |

### Demo HTML (`presentacion/demo-webapp.html`) — 19K
- Phone frame mockup con chat interface
- Dark background con gradientes

### Brand Book (`design/branding/clara-brand-book.html`) — 1110 lineas
- SVG symbols: `#icon-blue`, `#icon-white`, `#persona-maria`, `#persona-ahmed`, `#persona-fatima`
- CSS: warm shadows, grainy texture, hero glow, hover lift, E-V-I cards, before/after grid

---

## GAP ANALYSIS — Lo que FALTA

| Gap | Donde | Prioridad |
|-----|-------|-----------|
| Arabic (AR) language + RTL | types.ts, LanguageSelector, page.tsx, content objects | ALTA |
| GSAP cinematic entrance | page.tsx (landing) | ALTA |
| Impact narrative (4.5M, personas, before/after) | Nuevo componente o seccion en page.tsx | ALTA |
| Brand book SVG personas (Maria/Ahmed/Fatima) | Nuevo componente | MEDIA |
| Dark mode (`prefers-color-scheme`) | globals.css + layout.tsx | MEDIA |
| Warm shadows + grainy texture | globals.css | MEDIA |
| Quick-reply chips post-saludo | ChatInput o MessageList | ALTA |
| OG tags completos | layout.tsx metadata | BAJA |
| Standalone pitch demo HTML | `presentacion/clara-webapp-live.html` | ALTA |

---

## LECTURA OBLIGATORIA

| Archivo | Para quien |
|---------|------------|
| `design/branding/clara-brand-book.html` | **TODOS** — SVGs, CSS patterns, narrativa |
| `clara-web/src/app/page.tsx` | design-agent, frontend-agent, animation-agent |
| `clara-web/src/app/globals.css` | design-agent |
| `clara-web/tailwind.config.ts` | design-agent |
| `clara-web/src/lib/types.ts` | i18n-agent, frontend-agent |
| `clara-web/src/components/ui/LanguageSelector.tsx` | i18n-agent |
| `clara-web/src/app/chat/page.tsx` | frontend-agent |
| `clara-web/src/hooks/useChat.ts` | frontend-agent |
| `clara-web/src/lib/constants.ts` | frontend-agent, animation-agent |
| `design/branding/colores/PALETA-CLARA.md` | design-agent |
| `design/branding/tipografia/TIPOGRAFIA-CLARA.md` | design-agent |
| `clara-web/design/civic-tenderness-visual-philosophy.md` | design-agent, animation-agent |
| `docs/08-marketing/CLARA-TONE-VOICE-GUIDE.md` | narrative-agent |
| `docs/08-marketing/NARRATIVA-JUECES-FASE4.md` | narrative-agent |
| `clara-web/design/MARKETING-CONTENT-STRATEGY-REPORT.md` | narrative-agent |
| `presentacion/demo-webapp.html` | demo-agent |
| `src/routes/api_chat.py` | qa-agent |

---

## EQUIPO — 6 Agentes

| Nombre | subagent_type | Responsabilidad |
|--------|---------------|-----------------|
| `design-agent` | frontend-developer | T1: Enhance globals.css + tailwind con brand book patterns |
| `i18n-agent` | general-purpose | T2: Add Arabic + RTL across all files |
| `animation-agent` | frontend-developer | T3: GSAP entrance sequence on landing page |
| `narrative-agent` | general-purpose | T4: Impact content, personas component, before/after, microcopy |
| `frontend-agent` | frontend-developer | T5-T7: Wire everything into Next.js pages + standalone demo |
| `qa-agent` | general-purpose | T8: Tests, accessibility audit, gates, commit |

**Dependencias:**
```
Fase 1 (paralelo): T1 + T2 + T4 (design + i18n + narrative)
Fase 2 (paralelo): T3 + T5 (animation + frontend wiring) — esperan Fase 1
Fase 3:            T6 (standalone demo) — espera Fase 2
Fase 4:            T7-T8 (quick-reply + QA) — espera Fase 3
```

---

## PRE-CHECK

```bash
echo "=== PRE-CHECK ==="
cd clara-web && npm run build 2>&1 | tail -5
cd .. && PYTHONPATH=. python -m pytest tests/ -x -q --tb=no 2>&1 | tail -3
ruff check src/ tests/ --select E,F,W --ignore E501 2>&1 | tail -1
echo "=== PRE-CHECK DONE ==="
```

---

## T1: Design System Enhancement (design-agent)

**MODIFY** (no crear): `clara-web/src/app/globals.css` y `clara-web/tailwind.config.ts`

### 1a: globals.css — Agregar brand book CSS patterns

Agregar DESPUES de las keyframes existentes:

```css
/* ── Brand Book: Warm Shadows ── */
.shadow-warm {
  box-shadow: 0 2px 20px rgba(27,94,123,0.06), 0 0 0 1px rgba(224,224,224,0.5);
}
.shadow-warm-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(27,94,123,0.1), 0 0 0 1px rgba(224,224,224,0.5);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* ── Brand Book: Grainy Texture Overlay (2026 trend) ── */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1000;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

/* ── Dark Mode ── */
@media (prefers-color-scheme: dark) {
  :root {
    --color-clara-bg: #0f1419;
    --color-clara-text: #e8e8ee;
    --color-clara-text-secondary: #a0a0b0;
    --color-clara-card: #1a1f26;
    --color-clara-border: #2a2f36;
    --color-clara-info: #1a2a3a;
  }
}

/* ── Persona chip component ── */
.persona-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 2px 20px rgba(27,94,123,0.06);
}

/* ── Before/After grid ── */
.before-after-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.before-cell {
  padding: 12px 16px;
  background: rgba(212,106,30,0.06);
  border-radius: 8px;
  border-left: 3px solid #D46A1E;
}
.after-cell {
  padding: 12px 16px;
  background: rgba(46,125,79,0.06);
  border-radius: 8px;
  border-left: 3px solid #2E7D4F;
}
```

### 1b: tailwind.config.ts — Add dark mode + shadow tokens

Agregar en `extend`:
```typescript
boxShadow: {
  warm: '0 2px 20px rgba(27,94,123,0.06), 0 0 0 1px rgba(224,224,224,0.5)',
  'warm-hover': '0 8px 30px rgba(27,94,123,0.1), 0 0 0 1px rgba(224,224,224,0.5)',
},
```

---

## T2: Arabic + RTL Support (i18n-agent)

**MODIFY** estos archivos existentes:

### 2a: `src/lib/types.ts`
```typescript
// CAMBIAR:
export type Language = "es" | "fr";
// A:
export type Language = "es" | "fr" | "ar";
```

### 2b: `src/components/ui/LanguageSelector.tsx`
Agregar boton "AR" al selector. Al seleccionar AR, emitir evento para que layout cambie `dir="rtl"`.

### 2c: `src/app/page.tsx`
Agregar bloque `ar` al objeto `content`:
```typescript
ar: {
  greeting: "مرحبا، أنا كلارا",
  tagline: ["صوتك", "له قوة"],
  description: "أساعدك في الإجراءات الاجتماعية في إسبانيا. تحدث أو اكتب بلغتك.",
  mic_label: "اضغط للتحدث",
  topics_hint: "أو اختر موضوعاً:",
  topics: [
    { icon: "coin", label: "مساعدة\nمالية", speech: "المساعدة المالية" },
    { icon: "house", label: "تسجيل\nبلدي", speech: "التسجيل البلدي" },
    { icon: "health", label: "صحة", speech: "البطاقة الصحية" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE أو TIE" },
  ],
  cta_text: "أفضل الكتابة",
  welcome_speech: "مرحبا، أنا كلارا. اضغط الزر الكبير لتتحدث معي.",
  footer: "مجاني · سري · بلغتك",
},
```

### 2d: `src/app/layout.tsx`
Agregar prop `dir` dinamico. Usar cookie o searchParam para detectar AR y setear `dir="rtl"`.

### 2e: `src/hooks/useChat.ts`
Agregar saludo AR al welcome message. Agregar `ar-SA` como lang para Speech API.

### 2f: `src/app/globals.css`
Agregar:
```css
[dir="rtl"] .chat-bubble-user { border-radius: 16px 4px 16px 16px; }
[dir="rtl"] .chat-bubble-clara { border-radius: 4px 16px 16px 16px; }
```

---

## T3: GSAP Entrance Sequence (animation-agent)

**MODIFY:** `clara-web/src/app/page.tsx`

### 3a: Agregar GSAP via CDN en layout.tsx o como next/script
```typescript
import Script from 'next/script';
// En el JSX:
<Script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" strategy="beforeInteractive" />
```

### 3b: Reemplazar las CSS animations actuales con GSAP timeline

En `page.tsx`, agregar useEffect con timeline:

```typescript
useEffect(() => {
  if (typeof gsap === 'undefined') return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) return; // CSS fallback handles it

  const tl = gsap.timeline();
  tl.from('.hero-logo', { scale: 0.6, opacity: 0, duration: 0.8, ease: 'back.out(1.7)' })
    .to('.hero-logo', { y: -8, duration: 3, ease: 'sine.inOut', repeat: -1, yoyo: true }, '+=0.2')
    .from('.greeting-text', { opacity: 0, y: 20, duration: 0.6 }, '-=2.8')
    .from('.tagline-text', { opacity: 0, y: 20, duration: 0.6 }, '-=2.2')
    .from('.description-text', { opacity: 0, y: 20, duration: 0.6 }, '-=1.8')
    .from('.mic-button', { scale: 0, duration: 0.5, ease: 'back.out(2)' }, '-=1.2')
    .from('.topic-chips > *', { opacity: 0, y: 15, stagger: 0.1, duration: 0.4 }, '-=0.8');
}, []);
```

### 3c: Multilingual typewriter (en hero, antes del tagline)

Agregar estado que cicla por 3 saludos: "Hola, soy Clara" → "Bonjour, je suis Clara" → "مرحبا، أنا كلارا" → tagline final.

---

## T4: Impact Narrative Content (narrative-agent)

**CREAR:** `clara-web/src/components/ImpactSection.tsx`

Componente React que incluye:

### 4a: Impact counter
```tsx
<div className="text-center py-6">
  <span className="font-display text-[48px] font-bold text-clara-blue">4.5M</span>
  <p className="text-body-sm text-clara-text-secondary">
    personas vulnerables en España no acceden a ayudas
  </p>
</div>
```

### 4b: Personas strip (usar SVGs del brand book)
```tsx
const personas = [
  { id: 'maria', name: 'María, 58', quote: { es: '"Solo quiero saber si tengo derecho a ver un médico."', fr: '"Je veux juste savoir si j\'ai droit à un médecin."', ar: '"أريد فقط أن أعرف هل لي الحق في رؤية طبيب."' }},
  { id: 'ahmed', name: 'Ahmed, 34', quote: { ... }},
  { id: 'fatima', name: 'Fátima, 42', quote: { ... }},
];
```

### 4c: Before/After comparison
Grid naranja/verde del brand book seccion "Voz Primero":
- Antes: "Un formulario de 4 páginas en español jurídico"
- Con Clara: "¿Tienes pasaporte y contrato? Entonces puedes empadronarte."
(3 filas total)

### 4d: SVG Defs component
**CREAR:** `clara-web/src/components/SvgDefs.tsx`
Copiar los `<symbol>` del brand book (lineas 536-598) como componente React.

### 4e: Microcopy trilingue
**CREAR:** `clara-web/src/lib/i18n.ts`
Centralizar TODOS los strings en un objeto `Record<Language, {...}>` para ES/FR/AR.

### 4f: Quick-reply chips data
```typescript
export const QUICK_REPLIES: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "¿Cómo me empadrono?", "Tarjeta sanitaria"],
  fr: ["Qu'est-ce que le RMV?", "Comment s'inscrire?", "Carte sanitaire"],
  ar: ["ما هو الحد الأدنى للدخل؟", "كيف أسجل؟", "البطاقة الصحية"],
};
```

---

## T5: Wire Into Next.js Pages (frontend-agent)

**MODIFY** archivos existentes para integrar T1-T4:

### 5a: `page.tsx` — Landing page enhancements
1. Import `SvgDefs` y renderizar al inicio del body
2. Import `ImpactSection` y renderizar ENTRE hero y mic button
3. Agregar clases CSS para GSAP targeting (`.hero-logo`, `.greeting-text`, etc.)
4. Agregar multilingual typewriter al greeting
5. Integrar dark mode logo switch (`#icon-blue` / `#icon-white`)

### 5b: `chat/page.tsx` — Quick-reply chips
1. Agregar quick-reply chips debajo del primer mensaje de Clara
2. Al click: `send(chipText)` — se envia como mensaje del usuario
3. Chips desaparecen despues del primer envio

### 5c: `MessageList.tsx` — Quick-reply rendering
Agregar prop `onQuickReply` y renderizar chips como botones pill debajo del welcome message.

### 5d: `layout.tsx` — OG tags + dir support
1. Mejorar metadata con OG tags completos
2. Agregar dynamic `dir` attribute support

---

## T6: Standalone Demo HTML (frontend-agent)

**CREAR:** `presentacion/clara-webapp-live.html`

Single-file HTML autocontenido para el pitch. COPIAR estructura de `presentacion/demo-webapp.html` como BASE, luego agregar:

1. SVG defs del brand book (logo + personas)
2. GSAP CDN + entrance timeline (logo → typewriter → impact → personas → chat)
3. Chat funcional con `fetch()` a `/api/chat`
4. Web Speech API (tap-to-start)
5. Quick-reply chips
6. 3 idiomas (ES/FR/AR + RTL)
7. Impact section (4.5M + personas + before/after)
8. Brand book CSS (warm shadows, grainy texture, hero glow)
9. Dark mode + reduced-motion

> Este archivo es para presentacion — NO necesita Next.js, NO necesita build step.

---

## T7: Final Polish (frontend-agent)

### 7a: Footer
Agregar a `page.tsx`:
```
"Clara es un bien público digital. Código abierto, información verificada, cero costo."
"Hackathon OdiseIA4Good 2026 — UDIT Madrid"
```

### 7b: Stats strip (opcional)
4 numeros del brand book: 17 CCAA | 3+ idiomas | 8 tramites | <3s respuesta

---

## T8: QA + Verification + Commit (qa-agent)

### 8a: Verify backend endpoint
Leer `src/routes/api_chat.py`. Confirmar POST /api/chat con CORS. Si falta CORS, agregar.

### 8b: Run tests
```bash
cd clara-web && npm run build
cd .. && PYTHONPATH=. python -m pytest tests/ -x -q --tb=no
ruff check src/ tests/ --select E,F,W --ignore E501
```

### 8c: Accessibility audit
- [ ] `role="log"` + `aria-live="polite"` en chat
- [ ] Todos los botones: `aria-label` descriptivo
- [ ] Focus visible: 3px solid clara-blue
- [ ] `<html lang>` cambia con selector
- [ ] `<html dir="rtl">` cuando AR
- [ ] Contraste 7:1 todas las combinaciones
- [ ] Touch targets: 48px minimo
- [ ] `prefers-reduced-motion` funciona
- [ ] `prefers-color-scheme: dark` funciona
- [ ] Zoom 200% no rompe

### 8d: Gates de verificacion

| Gate | Verificar | Esperado |
|------|-----------|----------|
| G1 | `npm run build` en clara-web/ | Build success |
| G2 | `pytest tests/ -x -q` | 568+ passed |
| G3 | `ruff check` | Clean |
| G4 | types.ts tiene `"ar"` en Language | SI |
| G5 | LanguageSelector tiene 3 botones (ES/FR/AR) | SI |
| G6 | globals.css tiene `prefers-color-scheme: dark` | SI |
| G7 | globals.css tiene grainy texture `body::after` | SI |
| G8 | page.tsx importa GSAP y tiene timeline | SI |
| G9 | `clara-webapp-live.html` existe y tiene >300 lineas | SI |
| G10 | Demo HTML tiene `role="log"` y `aria-live` | SI |

### 8e: Commits

```bash
# Next.js enhancements
git add clara-web/
git commit -m "feat(clara-web): add Arabic/RTL, GSAP animations, impact narrative, dark mode, brand book CSS

- Arabic language + RTL layout support (third language)
- GSAP cinematic entrance: logo float, multilingual typewriter, staggered reveals
- Impact section: 4.5M counter, persona SVG avatars with quotes, before/after grid
- Dark mode via prefers-color-scheme with AAA contrast
- Brand book CSS: warm shadows, grainy texture overlay, hover lift
- Quick-reply chips in chat for faster demo flow
- SVG defs from brand book (logo blue/white + 3 persona portraits)
- Centralized i18n strings for ES/FR/AR

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# Standalone demo
git add presentacion/clara-webapp-live.html
git commit -m "feat: add standalone clara-webapp-live demo for hackathon pitch

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Resumen

| Fase | Agente(s) | Tasks | Paralelo |
|------|-----------|-------|----------|
| 1 | design-agent + i18n-agent + narrative-agent | T1 + T2 + T4 | SI (3 en paralelo) |
| 2 | animation-agent + frontend-agent | T3 + T5 | SI (2 en paralelo) |
| 3 | frontend-agent | T6 (standalone demo) | NO |
| 4 | frontend-agent + qa-agent | T7 + T8 | SI |

**Total: 8 tasks, 6 agentes, 4 fases**

## Criterios de Exito

- [ ] Next.js app compila (`npm run build`)
- [ ] 3 idiomas funcionales (ES/FR/AR) con RTL correcto
- [ ] GSAP entrance: logo float → typewriter multilingue → impact reveal
- [ ] Impact section: 4.5M counter + 3 SVG personas con citas
- [ ] Before/After: comparacion naranja/verde
- [ ] Quick-reply chips en chat
- [ ] Dark mode automatico (logo white variant)
- [ ] Brand book CSS: warm shadows, grainy texture, hover lift
- [ ] Chat funcional conectado a /api/chat
- [ ] Voz funcional (Web Speech API, 3 idiomas)
- [ ] Standalone demo HTML funcional
- [ ] WCAG AAA (contraste, focus, aria, reduced-motion, RTL)
- [ ] Backend tests pasan (568+)
- [ ] Mobile-first, perfecto en 390px
