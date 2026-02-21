# Frontend Media Content — Videos e Imagenes para Clara Web

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generar imagenes y videos con los MCP servers (kie-ai, fal-ai, elevenlabs, heygen) y agregarlos al frontend de Clara Web, especialmente en la pagina `/como-usar` que ya tiene un placeholder de video, y en las secciones que estan construidas pero no renderizadas (ImpactSection, stats strip).

**Architecture:** Usamos los 4 MCP servers para generar assets (imagenes hiperrealistas de personas, video clips animados, voiceover), los guardamos en `clara-web/public/media/`, y actualizamos los componentes React existentes para mostrarlos. La pagina `/como-usar` ya tiene un placeholder exacto para video. `ImpactSection.tsx` ya esta construido pero no se importa en ninguna pagina.

**Tech Stack:** Next.js 15 (App Router), Tailwind CSS, MCP servers (kie-ai, fal-ai, elevenlabs), FFmpeg (compose_video.py)

---

## Estado actual del frontend

| Pagina | Estado | Oportunidad |
|--------|--------|-------------|
| `/` (Welcome) | Completa — logo, greeting, mic, chips | Agregar imagenes de personas, stats strip |
| `/como-usar` | **Placeholder de video** (dashed box, "Video tutorial disponible pronto") | Reemplazar con video real + imagenes de pasos |
| `/quienes-somos` | Personas + before/after | Mejorar con fotos hiperrealistas de personas |
| `/chat` | Funcional | No necesita media |
| `ImpactSection.tsx` | **Construido pero NO renderizado en ninguna pagina** | Importar en welcome o quienes-somos |

## Assets existentes que podemos usar

- 7 retratos de personas en `design/branding/personas/` (maria, ahmed, fatima, fatou, youssef, aminata, omar)
- 10 mockups v3 en `design/mockups/` (escenas de uso de Clara)
- Pipeline de media en `scripts/media/` (7 scripts listos)
- Brand guide completa con colores, tipografia, tono

## Assets a generar

| Asset | Herramienta MCP | Destino |
|-------|----------------|---------|
| 4 imagenes "Como usar" (pasos 1-4) | fal-ai (Flux Pro) o kie-ai (OpenAI 4o) | `clara-web/public/media/steps/` |
| 3 imagenes personas hiperrealistas (Maria, Ahmed, Fatima) | fal-ai (Flux Pro) o kie-ai (Flux Kontext) | `clara-web/public/media/personas/` |
| Video tutorial 30s "Como usar Clara" | kie-ai (Kling v2.5 o Hailuo v2.3) | `clara-web/public/media/video/` |
| Voiceover para video tutorial | elevenlabs (eleven_multilingual_v2) | `clara-web/public/media/audio/` |
| 1 hero image (producto) | fal-ai (Flux Pro) | `clara-web/public/media/` |

---

## Task 1: Crear estructura de directorios para media

**Files:**
- Create: `clara-web/public/media/steps/` (directorio)
- Create: `clara-web/public/media/personas/` (directorio)
- Create: `clara-web/public/media/video/` (directorio)
- Create: `clara-web/public/media/audio/` (directorio)

**Step 1: Crear directorios**

```bash
mkdir -p clara-web/public/media/{steps,personas,video,audio}
```

**Step 2: Copiar assets existentes que ya son utiles**

```bash
# Copiar los mockups v3 mas relevantes como base
cp design/mockups/v3-01-maria-voice-message.png clara-web/public/media/personas/maria.png
cp design/mockups/v3-02-ahmed-night-shift.png clara-web/public/media/personas/ahmed.png
cp design/mockups/v3-03-fatima-family.png clara-web/public/media/personas/fatima.png
cp design/mockups/v3-08-product-hero.png clara-web/public/media/hero.png
```

**Step 3: Verificar**

```bash
ls -la clara-web/public/media/
ls -la clara-web/public/media/personas/
```

Expected: 4 directorios + 4 imagenes copiadas.

**Step 4: Commit**

```bash
git add clara-web/public/media/
git commit -m "feat(web): add media directory structure with initial persona images"
```

---

## Task 2: Generar imagenes de los 4 pasos "Como usar Clara"

Generar 4 imagenes que ilustren los pasos de la pagina `/como-usar`:
1. "Abre Clara" — manos abriendo WhatsApp en telefono
2. "Elige tu idioma" — pantalla con selector ES/FR/AR
3. "Habla o escribe" — persona grabando mensaje de voz
4. "Recibe tu respuesta" — persona leyendo respuesta de Clara con sonrisa

**Files:**
- Create: `clara-web/public/media/steps/step-1-open.png`
- Create: `clara-web/public/media/steps/step-2-language.png`
- Create: `clara-web/public/media/steps/step-3-speak.png`
- Create: `clara-web/public/media/steps/step-4-response.png`

**Step 1: Generar imagen paso 1 — "Abre Clara"**

Usar MCP tool `mcp__fal-ai__generate` o `mcp__kie-ai__flux_kontext_image` con prompt:

```
Close-up of hands holding a smartphone. The screen shows a WhatsApp conversation
being opened. Warm golden morning light from a window. Mediterranean kitchen
background slightly blurred. The hands belong to a middle-aged woman.
Photorealistic, documentary cinematic style. Warm golden lighting.
Shallow depth of field. Color palette includes warm tones with touches of
blue (#1B5E7B). Shot at eye level. Intimate, hopeful mood.
No text overlays, no watermarks. High quality.
```

**Step 2: Generar imagen paso 2 — "Elige tu idioma"**

```
Over-the-shoulder shot of a person looking at a phone screen showing language
options (Spanish, French, Arabic) as colorful pill buttons. The person's finger
hovers over one option. Soft warm lighting. Modern minimalist UI visible on screen.
Photorealistic, documentary cinematic style. Warm golden lighting.
Shallow depth of field. Intimate, hopeful mood. No text overlays, no watermarks.
High quality.
```

**Step 3: Generar imagen paso 3 — "Habla o escribe"**

```
Medium close-up of a young man of Senegalese descent holding his phone to his mouth,
recording a voice message on WhatsApp. He has a calm, focused expression.
He is sitting on a park bench in a Spanish city. Warm afternoon sunlight
filters through trees. Photorealistic, documentary cinematic style.
Warm golden lighting. Shallow depth of field. Color palette includes warm tones
with touches of blue (#1B5E7B) and orange (#D46A1E). Eye level.
Intimate, hopeful mood. No text overlays, no watermarks. High quality.
```

**Step 4: Generar imagen paso 4 — "Recibe tu respuesta"**

```
Medium shot of a woman reading a message on her phone with a relieved,
understanding smile. She is in a bright community center. Warm natural light.
Her expression shows the moment of "I understand now."
Photorealistic, documentary cinematic style. Warm golden lighting.
Shallow depth of field. Color palette includes warm tones with touches of
green (#2E7D4F) representing success/hope. Eye level.
Intimate, hopeful mood. No text overlays, no watermarks. High quality.
```

**Step 5: Descargar y guardar las imagenes generadas**

Mover los archivos generados a:
```bash
mv [generated_file_1] clara-web/public/media/steps/step-1-open.png
mv [generated_file_2] clara-web/public/media/steps/step-2-language.png
mv [generated_file_3] clara-web/public/media/steps/step-3-speak.png
mv [generated_file_4] clara-web/public/media/steps/step-4-response.png
```

**Step 6: Optimizar imagenes para web**

```bash
# Si sips esta disponible (macOS)
for f in clara-web/public/media/steps/*.png; do
  sips -Z 800 "$f"
done
```

**Step 7: Commit**

```bash
git add clara-web/public/media/steps/
git commit -m "feat(web): add step-by-step tutorial images for como-usar page"
```

---

## Task 3: Generar video tutorial "Como usar Clara" (30s)

Video corto mostrando el flujo completo de Clara: abrir WhatsApp -> hablar -> recibir respuesta.

**Files:**
- Create: `clara-web/public/media/video/como-usar-clara.mp4`
- Create: `clara-web/public/media/audio/voiceover-como-usar.mp3`

**Step 1: Generar voiceover con ElevenLabs**

Usar MCP tool `mcp__elevenlabs__text_to_speech` con:

```
text: "Usar Clara es muy facil. Primero, abre WhatsApp y escribe Hola Clara.
Luego, elige tu idioma: espanol, frances o arabe. Despues, habla o escribe
tu pregunta. Clara te responde al momento, paso a paso, con enlaces oficiales.
Asi de simple. Tu voz tiene poder."

voice_name: "Charlotte"  (o una voz femenina calida en español)
model_id: "eleven_multilingual_v2"
language: "es"
stability: 0.6
similarity_boost: 0.8
style: 0.3
speed: 0.9
output_directory: "clara-web/public/media/audio"
```

**Step 2: Generar clips de video con kie-ai**

Generar 4 clips de 5s cada uno usando `mcp__kie-ai__kling_video` o `mcp__kie-ai__hailuo_video`:

Clip 1 — Apertura (imagen paso 1 como base):
```
prompt: "Close-up of hands opening WhatsApp on a smartphone. Warm golden kitchen light.
The thumb taps the WhatsApp icon and a conversation opens. Smooth cinematic camera.
Documentary style. Warm tones with blue accents."
duration: "5"
aspect_ratio: "16:9"
```

Clip 2 — Grabando voz:
```
prompt: "A young man holds his phone and presses the voice message button in WhatsApp.
An orange waveform animation appears as he speaks. Park bench, afternoon sunlight.
Cinematic documentary style. Warm hopeful lighting."
duration: "5"
aspect_ratio: "16:9"
```

Clip 3 — Clara responde:
```
prompt: "Over-the-shoulder view of a phone screen showing a WhatsApp conversation.
A new message appears from Clara with clear text. The person scrolls and smiles.
Then an audio message with a play button appears. Warm lighting. Cinematic feel."
duration: "5"
aspect_ratio: "16:9"
```

Clip 4 — Cierre (compartir):
```
prompt: "A woman shows her phone to another person in a community center.
Both smile. The second person takes out their phone to save the number.
Warm golden light. Cinematic documentary. Hopeful mood."
duration: "5"
aspect_ratio: "16:9"
```

**Step 3: Verificar estado de los videos generados**

Usar `mcp__kie-ai__get_task_status` para cada task ID devuelto.
Los videos de kie-ai tardan 2-5 minutos en generarse.

**Step 4: Descargar videos y componer**

Una vez que los clips esten listos, usar el pipeline existente:

```bash
python scripts/media/compose_video.py \
  --clips clip1.mp4 clip2.mp4 clip3.mp4 clip4.mp4 \
  --audio clara-web/public/media/audio/voiceover-como-usar.mp3 \
  -o clara-web/public/media/video/como-usar-clara.mp4
```

**Step 5: Commit**

```bash
git add clara-web/public/media/video/ clara-web/public/media/audio/
git commit -m "feat(web): add tutorial video and voiceover for como-usar page"
```

---

## Task 4: Actualizar pagina `/como-usar` — reemplazar placeholder con video real

**Files:**
- Modify: `clara-web/src/app/como-usar/page.tsx`

**Step 1: Leer el archivo actual**

```bash
cat clara-web/src/app/como-usar/page.tsx
```

**Step 2: Escribir test visual (verificar que la pagina renderiza)**

No hay tests unitarios para las paginas de Next.js en este proyecto, asi que verificamos manualmente:

```bash
cd clara-web && npm run build
```

Expected: Build exitoso sin errores.

**Step 3: Reemplazar el placeholder de video**

Buscar el bloque actual (dashed border box con "Video tutorial disponible pronto") y reemplazarlo con:

```tsx
{/* Video tutorial */}
<div className="rounded-2xl overflow-hidden shadow-warm bg-white">
  <video
    controls
    preload="metadata"
    poster="/media/steps/step-1-open.png"
    className="w-full aspect-video"
    aria-label={
      lang === 'es' ? 'Video tutorial: como usar Clara' :
      lang === 'fr' ? 'Video tutoriel: comment utiliser Clara' :
      'فيديو تعليمي: كيفية استخدام كلارا'
    }
  >
    <source src="/media/video/como-usar-clara.mp4" type="video/mp4" />
    <p>
      {lang === 'es' ? 'Tu navegador no soporta video. ' :
       lang === 'fr' ? 'Votre navigateur ne supporte pas la video. ' :
       'متصفحك لا يدعم الفيديو. '}
      <a href="/media/video/como-usar-clara.mp4" className="text-clara-blue underline">
        {lang === 'es' ? 'Descargar video' :
         lang === 'fr' ? 'Telecharger la video' :
         'تحميل الفيديو'}
      </a>
    </p>
  </video>
</div>
```

**Step 4: Agregar imagenes a cada paso**

Actualizar las 4 tarjetas de pasos para incluir las imagenes generadas:

```tsx
{/* Paso 1 */}
<div className="bg-white rounded-2xl shadow-warm overflow-hidden">
  <img
    src="/media/steps/step-1-open.png"
    alt={lang === 'es' ? 'Manos abriendo WhatsApp' :
         lang === 'fr' ? 'Mains ouvrant WhatsApp' :
         'فتح واتساب'}
    className="w-full h-48 object-cover"
    loading="lazy"
  />
  <div className="p-6">
    {/* existing step content */}
  </div>
</div>
```

Repetir para pasos 2, 3, 4 con sus respectivas imagenes.

**Step 5: Verificar build**

```bash
cd clara-web && npm run build
```

Expected: Build exitoso.

**Step 6: Commit**

```bash
git add clara-web/src/app/como-usar/page.tsx
git commit -m "feat(web): replace video placeholder with real tutorial video and step images"
```

---

## Task 5: Agregar imagenes de personas a `/quienes-somos`

**Files:**
- Modify: `clara-web/src/app/quienes-somos/page.tsx`

**Step 1: Leer el archivo actual**

```bash
cat clara-web/src/app/quienes-somos/page.tsx
```

**Step 2: Actualizar chips de personas con fotos reales**

Reemplazar los SVG placeholder avatars con las imagenes reales de personas:

```tsx
{/* Persona: Maria */}
<div className="persona-chip">
  <img
    src="/media/personas/maria.png"
    alt="Maria"
    className="w-16 h-16 rounded-full object-cover flex-shrink-0"
    loading="lazy"
  />
  <div>
    <p className="font-bold font-atkinson">{persona.name}</p>
    <p className="text-sm text-clara-text-secondary italic">"{persona.quote}"</p>
  </div>
</div>
```

**Step 3: Verificar build**

```bash
cd clara-web && npm run build
```

**Step 4: Commit**

```bash
git add clara-web/src/app/quienes-somos/page.tsx
git commit -m "feat(web): add real persona photos to quienes-somos page"
```

---

## Task 6: Activar ImpactSection en la pagina de bienvenida

El componente `ImpactSection.tsx` ya esta construido con:
- Contador de impacto ("4.5M")
- Chips de 3 personas (Maria, Ahmed, Fatima)
- Grid before/after

Pero NO se importa en ninguna pagina.

**Files:**
- Modify: `clara-web/src/app/page.tsx`

**Step 1: Leer ImpactSection.tsx para confirmar su API**

```bash
cat clara-web/src/components/ImpactSection.tsx
```

**Step 2: Importar ImpactSection en la pagina de bienvenida**

Agregar debajo del PromptBar y antes del footer:

```tsx
import ImpactSection from '@/components/ImpactSection';

// ... dentro del JSX, despues de PromptBar y antes del footer:
<ImpactSection lang={lang} />
```

**Step 3: Verificar build**

```bash
cd clara-web && npm run build
```

**Step 4: Commit**

```bash
git add clara-web/src/app/page.tsx
git commit -m "feat(web): activate ImpactSection on welcome page"
```

---

## Task 7: Generar video de pitch 90s para el hackathon

Este es el video principal para jueces. Usa la estructura del guion de produccion.

**Files:**
- Create: `design/videos/output/pitch-90s.mp4`
- Create: `design/videos/output/voiceover-pitch-90s.mp3`

**Step 1: Generar voiceover del pitch 90s con ElevenLabs**

Usar `mcp__elevenlabs__text_to_speech`:

```
text: "Ahmed acaba de llegar a Espana. No habla espanol. Necesita registrarse
en su ciudad para tener derechos, pero el formulario tiene 47 campos, todos en
espanol. Casi diez millones de inmigrantes viven en Espana. Dos de cada tres
han sufrido barreras burocraticas. Si no hablas el idioma, te quedas fuera.

Nosotros construimos a Clara. Una asistente de WhatsApp que escucha tu voz en
tu idioma y te explica tus derechos paso a paso. Sin descargar nada. Sin
formularios. Sin esperar.

Treinta y tres millones de personas usan WhatsApp en Espana. Clara esta donde
ellos ya estan.

Informacion verificada del gobierno. Quinientas treinta y dos pruebas
automatizadas. Desplegada y funcionando.

Todo el codigo es abierto y gratuito. Cualquier ayuntamiento puede desplegar
Clara manana. Sin pagar un euro. Para siempre.

Tu voz tiene poder."

model_id: "eleven_multilingual_v2"
language: "es"
stability: 0.55
similarity_boost: 0.8
style: 0.35
speed: 0.85
output_directory: "design/videos/output"
```

**Step 2: Generar clips de video con kie-ai (6-8 clips)**

Usar `mcp__kie-ai__kling_video` o `mcp__kie-ai__hailuo_video`:

| # | Prompt | Segundos | Seccion |
|---|--------|----------|---------|
| 1 | "Phone ringing unanswered on a desk in a cold government office. Fluorescent lights. Desaturated, cold tones. Documentary style." | 5 | Hook |
| 2 | "Fast montage: close-up of dense government forms, long queue at office, website with small text. Cold blue-grey tones. Handheld camera feel." | 5 | Problema |
| 3 | "Close-up of a hand holding a phone. The screen lights up with a WhatsApp notification. Warm light begins to enter the frame. Transition from cold to warm tones." | 5 | Transicion |
| 4 | "Over-the-shoulder of person typing 'Hola Clara' in WhatsApp. The response appears. The person leans in to read. Warm golden lighting. Hopeful mood." | 5 | Clara |
| 5 | "A young man records a voice message on WhatsApp at night. Warm lamp light on his face. He presses send and waits. A response appears. He smiles with relief." | 5 | Demo |
| 6 | "Fast montage of data visualizations and code on screens. Professional, clean. Then: diverse hands pressing phone mic buttons. Blue and green tones." | 5 | Credibilidad |
| 7 | "Diverse group of people walking together on a sunlit Spanish street toward a bright horizon. Golden hour. Slow motion. Cinematic. Hopeful piano mood." | 5 | Cierre |

**Step 3: Componer video final**

```bash
mkdir -p design/videos/output

python scripts/media/compose_video.py \
  --clips hook.mp4 problema.mp4 transicion.mp4 clara.mp4 demo.mp4 credibilidad.mp4 cierre.mp4 \
  --audio design/videos/output/voiceover-pitch-90s.mp3 \
  --title "Tu voz tiene poder" \
  --subtitle "Clara | OdiseIA4Good 2026" \
  -o design/videos/output/pitch-90s.mp4
```

**Step 4: Commit**

```bash
git add design/videos/output/
git commit -m "feat(video): generate 90s pitch video with voiceover and persona clips"
```

---

## Task 8: Regenerar scripts de video del media pipeline

Actualizar los scripts del pipeline para usar los MCP servers directamente en vez de solo APIs REST.

**Files:**
- Modify: `scripts/media/generate_image.py` — agregar presets para los 4 pasos de "como-usar"
- Modify: `scripts/media/generate_voiceover.py` — agregar preset `como-usar-30s`
- Modify: `scripts/media/pipeline.py` — agregar modo `--preset como-usar-30s`

**Step 1: Agregar presets de imagenes para pasos**

En `scripts/media/generate_image.py`, agregar al dict `PRESETS`:

```python
"step-1-open": {
    "prompt": "Close-up of hands holding a smartphone opening WhatsApp. "
              "Warm golden morning light from a window. Mediterranean kitchen. "
              "The hands belong to a middle-aged woman.",
    "output": "clara-web/public/media/steps/step-1-open.png",
},
"step-2-language": {
    "prompt": "Over-the-shoulder shot of a person looking at phone screen "
              "showing language options as colorful pill buttons. Soft warm lighting.",
    "output": "clara-web/public/media/steps/step-2-language.png",
},
"step-3-speak": {
    "prompt": "Medium close-up of a young man of Senegalese descent holding "
              "phone to his mouth recording a voice message. Park bench in Spanish city. "
              "Warm afternoon sunlight through trees.",
    "output": "clara-web/public/media/steps/step-3-speak.png",
},
"step-4-response": {
    "prompt": "Medium shot of a woman reading a message on her phone with a "
              "relieved understanding smile. Bright community center. Warm natural light. "
              "Her expression shows 'I understand now.'",
    "output": "clara-web/public/media/steps/step-4-response.png",
},
```

**Step 2: Agregar preset de voiceover**

En `scripts/media/generate_voiceover.py`, agregar al dict `NARRATION_SCRIPTS`:

```python
"como-usar-30s": {
    "lang": "es",
    "text": (
        "Usar Clara es muy facil. "
        "Primero, abre WhatsApp y escribe Hola Clara. "
        "Luego, elige tu idioma: espanol, frances o arabe. "
        "Despues, habla o escribe tu pregunta. "
        "Clara te responde al momento, paso a paso, con enlaces oficiales. "
        "Asi de simple. Tu voz tiene poder."
    ),
},
```

**Step 3: Agregar modo pipeline**

En `scripts/media/pipeline.py`, agregar al dict de presets:

```python
"como-usar-30s": {
    "images": ["step-1-open", "step-2-language", "step-3-speak", "step-4-response"],
    "voiceover": "como-usar-30s",
    "output": "clara-web/public/media/video/como-usar-clara.mp4",
},
```

**Step 4: Verificar que los scripts siguen funcionando**

```bash
python scripts/media/generate_image.py --list-presets
python scripts/media/generate_voiceover.py --list-presets
python scripts/media/pipeline.py --help
```

**Step 5: Commit**

```bash
git add scripts/media/generate_image.py scripts/media/generate_voiceover.py scripts/media/pipeline.py
git commit -m "feat(media): add como-usar presets to image, voiceover, and pipeline scripts"
```

---

## Task 9: Optimizar imagenes para web (WebP + lazy loading)

**Files:**
- Modify: `clara-web/next.config.ts` — habilitar optimizacion de imagenes
- Modify: Todos los componentes que usen `<img>` — cambiar a `next/image`

**Step 1: Leer next.config.ts actual**

```bash
cat clara-web/next.config.ts
```

**Step 2: Actualizar next.config.ts**

Asegurar que el config permite imagenes locales de `public/media/`:

```typescript
const nextConfig = {
  images: {
    formats: ['image/webp', 'image/avif'],
  },
};
```

**Step 3: Actualizar componentes para usar next/image**

En cada componente que use `<img>` para nuestras imagenes, cambiar a:

```tsx
import Image from 'next/image';

<Image
  src="/media/steps/step-1-open.png"
  alt="Manos abriendo WhatsApp"
  width={800}
  height={450}
  className="w-full h-48 object-cover"
  loading="lazy"
/>
```

**Step 4: Verificar build**

```bash
cd clara-web && npm run build
```

**Step 5: Commit**

```bash
git add clara-web/next.config.ts clara-web/src/
git commit -m "feat(web): optimize images with next/image WebP conversion and lazy loading"
```

---

## Resumen de dependencias entre tasks

```
Task 1 (directorios) ──┐
                        ├── Task 2 (imagenes pasos) ──── Task 4 (actualizar /como-usar)
                        ├── Task 3 (video tutorial) ──── Task 4
                        └── Task 5 (fotos personas en /quienes-somos)

Task 6 (activar ImpactSection) — independiente

Task 7 (video pitch 90s) — independiente

Task 8 (regenerar scripts pipeline) — independiente

Task 9 (optimizar imagenes) — depende de Tasks 2, 4, 5
```

## Orden recomendado de ejecucion

1. **Task 1** — Directorios + copiar assets existentes (2 min)
2. **Task 2** — Generar imagenes con MCP (10 min, las generaciones tardan)
3. **Task 3** — Generar video + voiceover con MCP (15 min, en paralelo con Task 2)
4. **Task 4** — Actualizar `/como-usar` con video e imagenes (5 min)
5. **Task 5** — Fotos en `/quienes-somos` (5 min)
6. **Task 6** — Activar ImpactSection (3 min)
7. **Task 7** — Video pitch 90s (20 min, puede ser en paralelo)
8. **Task 8** — Regenerar scripts pipeline (10 min)
9. **Task 9** — Optimizar imagenes para web (5 min)

**Total estimado:** ~45 min ejecucion secuencial, ~30 min con paralelismo.
