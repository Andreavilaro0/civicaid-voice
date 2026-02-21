# Plan de Implementacion — Capa de Diseno Clara (8 Fases)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implementar toda la capa de diseno de Clara: web app responsive, mejoras WhatsApp/Twilio, identidad de marca, marketing, videos, pitch deck, materiales fisicos y testing de accesibilidad.

**Architecture:** Web app Next.js con React Aria para accesibilidad AAA, conectada al backend Flask existente via API. Twilio WhatsApp mejorado con botones interactivos y templates. Marca completa con Canva + Figma. Videos con IA (Runway, Suno, ElevenLabs).

**Tech Stack:** Next.js 14, React Aria, Tailwind CSS, next-intl, Canva MCP, Notion MCP, ElevenLabs, Runway, Suno, CapCut, Figma

---

## Inventario de Capacidades Disponibles

### MCPs Conectados

| MCP | Herramientas Clave | Uso en el Plan |
|---|---|---|
| **Notion** (claude.ai) | `notion-search`, `notion-create-pages`, `notion-update-page`, `notion-fetch` | Backlog tracking, documentar progreso, KB tramites |
| **Canva** (claude.ai) | `generate-design`, `search-designs`, `export-design`, `create-design-from-candidate`, `get-brand-kits` | Slides, posters, banners, social media, logo, QR |
| **Playwright** | `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_take_screenshot` | Testing visual de la web app, capturas de demo |
| **Grafana** | `query_prometheus`, `search_dashboards` | Monitoreo post-deploy (fase final) |

### Skills Relevantes de Claude

| Categoria | Skills | Uso |
|---|---|---|
| **Frontend** | `frontend-developer`, `nextjs-developer`, `react-expert`, `react-best-practices` | Construir web app responsive |
| **Diseno UI** | `frontend-design`, `top-design`, `refactoring-ui`, `design-trends-2026`, `ux-heuristics` | Sistema de diseno, wireframes a codigo |
| **Marca** | `brand-strategy`, `brand-voice`, `brand-guidelines`, `brand-voice-learner` | Identidad de marca completa |
| **Video/Audio** | `ai-video-prompting`, `ai-video-concept`, `storyboard`, `voiceover-direction`, `voice-design`, `ai-voice-design`, `elevenlabs` | Videos promocionales, voiceover |
| **Contenido** | `landing-page-copy`, `content-strategy`, `seo-content-writer`, `copywriting-classic` | Copy de la web y marketing |
| **Imagenes** | `generate-image`, `image-enhancer`, `infographics`, `canvas-design` | Imagenes AI, infografias |
| **Presentaciones** | `pptx`, `pptx-posters`, `google-slides` | Pitch deck |
| **Twilio/WA** | `twilio-communications`, `whatsapp-automation` | Mejoras al canal WhatsApp |
| **Accesibilidad** | `lighthouse-audit`, `webapp-testing` | Testing WCAG |
| **Notion** | `notion-automation`, `notion-template-business` | Tracking y documentacion |
| **Canva** | `canva-automation` | Generar disenos directamente |
| **Deploy** | `render-deploy`, `docker-expert`, `vercel-automation` | Deploy de la web app |

---

## FASE 1: Web App Frontend + Mejoras WhatsApp/Twilio

> **Prioridad:** MAXIMA — Es el producto visible para jueces y usuarios
> **Duracion estimada:** La mas larga — dedicar el mayor esfuerzo aqui
> **Skills:** `nextjs-developer`, `frontend-developer`, `react-expert`, `twilio-communications`, `whatsapp-automation`

### 1A. Web App Responsive (Cualquier Dispositivo)

**Objetivo:** Clara accesible desde navegador en movil, tablet y desktop. WCAG AA minimo, AAA donde sea posible.

**Stack recomendado:**
- **Next.js 14** (App Router) — SSR, performance, routing
- **React Aria** (Adobe) — Accesibilidad AAA nativa
- **Tailwind CSS** — Utility-first, responsive built-in
- **next-intl** — i18n ES/FR (futuro AR)
- **Deploy:** Vercel (gratis) o Render (ya usado por el backend)

**Pantallas a construir (basadas en wireframes del reporte):**

| # | Pantalla | Archivo | Prioridad |
|---|---|---|---|
| 1 | **Bienvenida** | `app/page.tsx` | P0 — landing |
| 2 | **Chat** | `app/chat/page.tsx` | P0 — core |
| 3 | **Grabacion de voz** | `components/VoiceRecorder.tsx` | P0 — diferenciador |
| 4 | **Subida de documento** | `components/DocumentUpload.tsx` | P1 — feature secundaria |
| 5 | **Respuesta con audio** | `components/AudioResponse.tsx` | P0 — voice-first |

**Specs tecnicas de accesibilidad:**
- Texto cuerpo: 18-20px Inter Regular, line-height 1.6
- Titulares: 28-36px Atkinson Hyperlegible Bold
- Botones: minimo 64x64px (target elderly), con aria-label
- Contraste: 7:1 texto normal (AAA), 4.5:1 texto grande
- Touch targets: 64x64px acciones principales, 48x48px secundarias
- Focus indicators: outline 3px azul `#1B5E7B`
- `prefers-reduced-motion` respetado
- Teclado: todo navegable con Tab, sin trampas

**Conexion al backend:**
- La web app llama a un endpoint API del Flask backend (nuevo `/api/chat`)
- O: la web app usa el mismo pipeline pero via HTTP POST directo
- Alternativa hackathon: web app como interfaz standalone con Gemini directo

**Tareas:**

1. **Scaffolding Next.js**
   - `npx create-next-app@latest clara-web --typescript --tailwind --app`
   - Instalar: `react-aria-components`, `next-intl`
   - Configurar Google Fonts: Atkinson Hyperlegible Next + Inter
   - Configurar colores en `tailwind.config.ts` (paleta Clara)

2. **Design tokens y componentes base**
   - `components/ui/Button.tsx` — 64x64px, aria-labels, focus ring
   - `components/ui/ChatBubble.tsx` — Clara (#E3F2FD) vs User (#1B5E7B)
   - `components/ui/LanguageSelector.tsx` — ES/FR toggle
   - `components/ui/LoadingState.tsx` — "Clara esta buscando..."

3. **Pantalla de Bienvenida**
   - Logo + tagline "Tu voz tiene poder"
   - Selector idioma (ES/FR)
   - Boton principal "Empezar a hablar" (72px alto, azul, mic icon)
   - Boton secundario "Prefiero escribir"
   - 100% responsive (mobile-first)

4. **Interfaz de Chat**
   - Header con back + "Clara" + language switcher + settings
   - Area de mensajes con scroll
   - Burbujas Clara (izquierda) y Usuario (derecha)
   - Boton "Escuchar respuesta" en burbujas Clara (audio player)
   - Fuente citada al final de cada respuesta
   - Input area: campo texto + 3 botones (Escribir/Voz/Foto) 64x64px

5. **Grabacion de Voz (DIFERENCIADOR CLAVE)**
   - Toggle mic (tap-to-start, tap-to-stop) — NO press-and-hold
   - Feedback visual: boton rojo + onda animada naranja + timer
   - Limite 60s con aviso a 50s
   - Botones Cancelar/Enviar debajo
   - Usar Web Audio API + MediaRecorder

6. **Subida de Documento**
   - HTML `<input type="file" accept="image/*" capture="environment">`
   - Preview de imagen antes de enviar
   - Drop zone para desktop
   - "Clara te explicara que dice"

7. **Audio Response Player**
   - Boton play 48x48px con barra de progreso
   - Tiempo transcurrido/total
   - Velocidad: 0.75x / 1x / 1.25x
   - NO auto-play

8. **i18n (ES/FR)**
   - Archivos `messages/es.json` y `messages/fr.json`
   - Configurar next-intl con middleware de locale
   - Todos los strings via `useTranslations()`

9. **PWA & Responsive**
   - `manifest.json` con iconos Clara
   - Service worker basico para offline shell
   - Meta viewport para mobile
   - Testar en 320px (movil basico), 768px (tablet), 1024px+ (desktop)

10. **Deploy**
    - Vercel: `vercel --prod` (gratis para proyectos personales)
    - O: Docker + Render (junto al backend)

### 1B. Mejoras al Canal WhatsApp/Twilio

**Objetivo:** Maximizar lo que Twilio WhatsApp Business API permite dentro del sandbox.

**Que se puede agregar a Twilio/WhatsApp:**

| Feature | Disponible en Sandbox | Disponible en Business | Implementacion |
|---|---|---|---|
| **Quick Reply Buttons** (3 max) | SI via API | SI | Enviar mensajes interactivos con `client.messages.create()` usando content SID |
| **List Messages** (10 items) | SI via API | SI | Menus de categorias de tramites |
| **CTA Buttons** (links/phone) | SI | SI | "Llamar a Seguridad Social" / "Abrir web oficial" |
| **Templates pre-aprobados** | NO (solo sandbox) | SI (requiere aprobacion) | Post-hackathon |
| **Stickers** | SI | SI | Sticker de Clara como branding |
| **Location sharing** | SI (recibir) | SI | "Envia tu ubicacion para encontrar tu oficina mas cercana" |
| **Formato texto enriquecido** | SI | SI | *bold*, _italic_, ~strikethrough~, ```code``` |
| **Media messages** | SI | SI | Imagenes, PDFs, audio |
| **Reactions** | NO en API | Futuro | — |

**Tareas de mejora Twilio:**

1. **Mensajes interactivos con botones**
   - Modificar `src/core/skills/send_response.py` para soportar `content_sid`
   - Crear templates en Twilio Content API:
     - Saludo: "Hola! Soy Clara. Como te puedo ayudar?" + 3 botones [IMV / Empadronamiento / Tarjeta sanitaria]
     - Post-respuesta: "Te fue util?" + 2 botones [Si, gracias / Tengo otra pregunta]
   - Parsear callbacks de botones en `webhook.py`

2. **List Messages para menu de tramites**
   - Cuando usuario escribe "menu" o "ayuda": enviar List Message con todos los tramites disponibles
   - Max 10 items con description corta por item

3. **CTA Buttons con links oficiales**
   - Al final de cada respuesta de tramite, incluir CTA button con link a web oficial
   - Ej: "Mas info en seg-social.es" como boton clickeable

4. **Formato enriquecido en respuestas**
   - Modificar `templates.py` para usar *bold* en titulos de pasos
   - Usar _italic_ para notas y aclaraciones
   - Numeracion clara: "1.", "2.", "3." para pasos

5. **Respuestas con media mejoradas**
   - Enviar infografias como imagen junto a la respuesta de texto
   - Enviar audio MP3 como media adjunta (ya soportado pero mejorar UX)

6. **Mensaje de bienvenida automatico mejorado**
   - Detectar primer mensaje del usuario
   - Enviar saludo personalizado con Quick Reply Buttons
   - Incluir instrucciones: "Puedes enviarme nota de voz, texto o foto de documento"

---

## FASE 2: Identidad de Marca

> **Prioridad:** ALTA — Define la imagen visual de todo lo demas
> **Skills:** `brand-strategy`, `brand-voice`, `brand-guidelines`, `canva-automation`
> **MCPs:** Canva (generar logo, brand kit), Notion (documentar guia)

### Tareas:

1. **Logo — Generar en Canva**
   - Usar MCP Canva: `generate-design` con prompt del Concepto A del reporte:
   > "Minimalist logo with rounded speech bubble in blue #1B5E7B. Inside, a soft stylized sound wave in orange #D46A1E. Next to it, 'Clara' in Atkinson Hyperlegible Bold. Below, 'Tu voz tiene poder' in Inter Regular gray. White background. Flat, clean, modern but warm."
   - Generar 3 variantes, seleccionar la mejor
   - Exportar en: SVG (web), PNG transparente (512px, 1024px), favicon (32x32, 192x192)

2. **Brand Kit en Canva**
   - Subir la paleta de colores Clara al brand kit de Canva
   - Primario: `#1B5E7B`, Secundario: `#D46A1E`, Acento: `#2E7D4F`
   - Fondos: `#FAFAFA`, `#F5F5F5`, `#E3F2FD`
   - Texto: `#1A1A2E`, `#4A4A5A`
   - Subir fuentes: Atkinson Hyperlegible, Inter

3. **Guia de Marca (1 pagina)**
   - Crear en Canva como infografia A4
   - Contenido: logo + uso correcto, paleta con hex codes, tipografia, tono de voz (5 bullets), do's y don'ts
   - Exportar como PDF

4. **Iconos y assets**
   - Descargar Material Design Icons (rounded) para los 8 conceptos clave
   - Descargar ilustraciones de Humaaans/Open Peeps para 3 personas (Ahmed, Maria, Fatima)
   - Crear mockup de telefono con conversacion WhatsApp en Canva

5. **Documentar en Notion**
   - Crear pagina "Brand Guide Clara" en Notion via MCP
   - Incluir: paleta, tipografia, tono, logo, assets

---

## FASE 3: Pitch Deck (8 Slides)

> **Prioridad:** ALTA — Presentacion ante jueces el 23-25 Feb
> **Skills:** `canva-automation`, `pptx`, `google-slides`, `infographics`
> **MCPs:** Canva

### Tareas:

1. **Crear presentacion en Canva** (16:9)
   - Usar template de pitch deck de Canva
   - Aplicar brand kit de Fase 2
   - 8 slides segun spec del reporte:
     - S1: Cover (logo + tagline + imagen)
     - S2: El Problema (4.5M + iconos)
     - S3: Clara (4 features en grid)
     - S4: Demo Ahmed (screenshot WA frances)
     - S5: Demo Maria (screenshot documento)
     - S6: Arquitectura (3 cajas + flechas)
     - S7: Impacto (3 numeros grandes)
     - S8: Cierre (frase + QR + logo)

2. **Capturar screenshots reales del demo**
   - Usar Playwright MCP para navegar la web app
   - Capturar: conversacion WA con nota de voz, respuesta Clara, documento analizado
   - Insertar en slides 4 y 5

3. **Generar QR code**
   - Link: `https://wa.me/NUMERO?text=Hola%20Clara`
   - Crear en Canva (app QR Code) o qr-code-generator.com
   - Insertar en slide 8

4. **Exportar**
   - PDF (para compartir)
   - PPTX (para editar si hay cambios last-minute)
   - Notas de presentador en cada slide

---

## FASE 4: Videos Promocionales

> **Skills:** `ai-video-prompting`, `ai-video-concept`, `storyboard`, `elevenlabs`, `voiceover-direction`

### Tareas:

1. **Video A: Elevator Pitch 30s**
   - Grabar demo real de la app con OBS Studio (screen recording)
   - Generar 2-3 clips IA con Runway usando prompts del reporte
   - Generar musica con Suno: "Hope Rising" (30s, acoustic)
   - Generar voiceover con ElevenLabs: lineas clave en espanol
   - Ensamblar en CapCut con subtitulos auto-generados

2. **Video B: Demo 90s**
   - Screen recording de ambos flujos: Ahmed (frances) y Maria (documento)
   - Narrar con voiceover o voz del equipo
   - Agregar texto overlay con estadisticas
   - Subtitulos en espanol

3. **Generar imagenes IA**
   - Bing Image Creator / Ideogram: 3-5 imagenes con prompts del reporte
   - Persona mayor, inmigrante, contraste burocracia vs Clara

4. **Generar musica IA**
   - Suno: 3 tracks (30s, 90s, 130s) con prompts del reporte
   - Seleccionar los mejores, descargar

---

## FASE 5: Campana de Redes Sociales

> **Skills:** `content-strategy`, `landing-page-copy`, `canva-automation`
> **MCPs:** Canva

### Tareas:

1. **Crear assets visuales en Canva**
   - 5 posts Instagram (1080x1080): 1 por cada dia del calendario
   - 3 stories Instagram (1080x1920): teaser + launch + CTA
   - 2 banners LinkedIn (1200x628)
   - 1 header Twitter (1500x500)

2. **Escribir copy para cada plataforma**
   - Usar textos del reporte seccion 7.3 como base
   - Adaptar tono por plataforma (profesional LI, casual IG, urgente TW)
   - Incluir alt text para TODAS las imagenes

3. **Preparar hashtags**
   - Principales: #ClaraIA #TuVozTienePoder #NadieSeQuedaFuera
   - Secundarios: #TechForGood #ImpactoSocial #OdiseIA4Good #IAParaTodos
   - CamelCase obligatorio para screen readers

4. **Programar publicaciones**
   - Crear calendario semanal en Notion via MCP
   - Si hay tiempo: programar con Buffer (free tier)

---

## FASE 6: Materiales Fisicos

> **Skills:** `canva-automation`, `pptx-posters`, `infographics`
> **MCPs:** Canva

### Tareas:

1. **Poster A4**
   - Crear en Canva con brand kit
   - Estructura: logo + tagline, 3 pasos con iconos, stats, QR
   - Exportar PDF Print (300 DPI)

2. **Roll-Up Banner (85x200cm)**
   - Crear en Canva con template roll-up
   - Logo grande arriba, phone mockup centro, features, stats, QR 15x15cm
   - Exportar PDF CMYK

3. **Tarjetas/Flyers**
   - Mini-tarjeta A6 con QR + "Habla con Clara" + instrucciones en 3 pasos
   - Version espanol y frances

---

## FASE 7: Testing de Accesibilidad

> **Skills:** `lighthouse-audit`, `webapp-testing`
> **MCPs:** Playwright

### Tareas:

1. **Lighthouse audit automatizado**
   - Correr Lighthouse en las 5 pantallas de la web app
   - Target: Performance >90, Accessibility >95, Best Practices >90
   - Documentar resultados y fixes

2. **axe DevTools scan**
   - Instalar axe extension en Chrome
   - Scan de cada pantalla
   - Fix: missing aria-labels, contrast issues, focus order

3. **Test manual con VoiceOver (macOS)**
   - Navegar toda la app solo con VoiceOver
   - Verificar: todos los botones anunciados, flujo logico, sin trampas
   - Documentar issues

4. **Test responsivo**
   - Usar Playwright para screenshot en 3 viewports: 320px, 768px, 1440px
   - Verificar que nada se rompe, botones accesibles, texto legible

5. **Test de contraste**
   - WebAIM Contrast Checker para toda la paleta
   - Verificar 7:1 (AAA) en texto normal
   - Verificar 4.5:1 en texto grande

6. **Test de lectura**
   - Hemingway Editor para todo el copy de la web
   - Target: Grade 6-8 (nivel B1 CEFR)

---

## FASE 8: Integracion Final y Preparacion Demo

> **Skills:** `render-deploy`, `docker-expert`
> **MCPs:** Notion, Playwright

### Tareas:

1. **Deploy final**
   - Web app: deploy a Vercel o Render
   - Backend: verificar que Render esta up-to-date
   - Verificar que WhatsApp sandbox funciona end-to-end

2. **Dry run del demo**
   - Preparar 3 flujos demo:
     - Ahmed: nota de voz en frances -> respuesta Clara
     - Maria: foto de carta -> Clara explica
     - Menu: "Que ayudas hay?" -> botones interactivos
   - Grabar backup en video por si falla algo en vivo

3. **Checklist pre-presentacion**
   - [ ] Web app cargando en <2s
   - [ ] WhatsApp respondiendo en <5s
   - [ ] Slides exportadas en PDF (backup)
   - [ ] Video backup en USB
   - [ ] QR codes testeados y funcionando
   - [ ] Poster/banner impresos (si aplica)
   - [ ] Bateria cargada, datos moviles, wifi alternativo

4. **Actualizar Notion**
   - Marcar todas las tareas completadas
   - Documentar lo entregado en cada fase
   - Link a todos los assets finales

5. **Actualizar documentacion**
   - Agregar al CLAUDE.md: paths de la web app, deploy URL
   - Actualizar docs index con nuevos documentos de design

---

## Orden de Ejecucion Recomendado

```
FASE 1A (Web App)     ████████████████████████  <- Mayor esfuerzo
FASE 1B (Twilio)      ████████████
FASE 2  (Marca)       ████████████████          <- Desbloquea Fases 3-6
FASE 3  (Pitch Deck)  ████████████
FASE 4  (Videos)      ████████████
FASE 5  (Redes)       ████████
FASE 6  (Materiales)  ██████
FASE 7  (Testing)     ██████████
FASE 8  (Demo)        ████████
```

**Dependencias:**
- Fase 2 (Marca) desbloquea Fases 3, 4, 5, 6 (necesitan logo, colores, brand kit)
- Fase 1A (Web App) desbloquea Fase 7 (testing) y Fase 3 (screenshots)
- Fase 7 puede correr en paralelo con Fases 4-6
- Fase 8 es la ultima — integra todo

**Paralelizacion sugerida:**
- **Andrea:** Fase 2 + Fase 3 + Fase 5 + Fase 6 (marca, slides, redes, materiales)
- **Daniel:** Fase 1A web app + Fase 4 videos
- **Robert/Marcos:** Fase 1B Twilio + Backend API para web app
- **Lucas:** Fase 7 testing + Fase 8 demo prep

---

*Plan creado el 19 de febrero de 2026. Basado en el Reporte de Investigacion de Diseno (00-REPORTE-INVESTIGACION-DESIGN-COMPLETO.md).*
