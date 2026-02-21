# Videos Promocionales Clara — Guia Completa de Produccion con IA (2026)

> Reporte de investigacion para Fase 4 del plan de diseno.
> Compilado: 21 febrero 2026 | OdiseIA4Good — UDIT Madrid

---

## Indice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Toolkit Recomendado ($0-50)](#2-toolkit-recomendado)
3. [Herramientas de Video IA — Comparativa](#3-herramientas-de-video-ia)
4. [Voces y Narracion IA](#4-voces-y-narracion-ia)
5. [Musica IA](#5-musica-ia)
6. [Edicion y Postproduccion](#6-edicion-y-postproduccion)
7. [Grabacion de Pantalla (Demo)](#7-grabacion-de-pantalla)
8. [Prompt Engineering para Video IA](#8-prompt-engineering-para-video-ia)
9. [10 Prompts Especificos para Clara](#9-prompts-especificos-para-clara)
10. [Estructura de Videos Ganadores de Hackathon](#10-estructura-videos-ganadores)
11. [Guion del Video de 90 Segundos](#11-guion-90-segundos)
12. [Storytelling Emocional — Tecnica Before/After](#12-storytelling-before-after)
13. [Musica y Emocion](#13-musica-y-emocion)
14. [Etica: Representar Vulnerabilidad con Dignidad](#14-etica-y-dignidad)
15. [Color Grading para la Marca Clara](#15-color-grading)
16. [Diseno de Sonido](#16-diseno-de-sonido)
17. [Subtitulos y Accesibilidad](#17-subtitulos-y-accesibilidad)
18. [Video Multilingue (ES/FR/AR)](#18-video-multilingue)
19. [Formatos de Exportacion por Plataforma](#19-formatos-exportacion)
20. [Timeline de Produccion (2 dias)](#20-timeline-produccion)
21. [Errores Fatales a Evitar](#21-errores-fatales)
22. [Referencias y Fuentes](#22-referencias)

---

## 1. Resumen Ejecutivo

Clara necesita 3 videos para el hackathon OdiseIA4Good 2026:

| Video | Duracion | Uso |
|-------|----------|-----|
| **A: Elevator Pitch** | 30 segundos | Redes sociales, hook emocional |
| **B: Demo Completo** | 90 segundos | Presentacion a jueces |
| **C: Clips Sociales** | 15 segundos | Instagram Reels, TikTok |

**Coste total recomendado: $5/mes** (ElevenLabs Starter). Todo lo demas es gratis.

**Principio rector:** Clara es calida, humana, esperanzadora. Los videos NO deben parecer un demo corporativo. Deben sentirse como un mini-documental sobre personas reales ejerciendo sus derechos.

---

## 2. Toolkit Recomendado

### Stack Gratuito ($5/mes)

| Necesidad | Herramienta | Coste | Funcion |
|-----------|-------------|-------|---------|
| B-roll video IA | **Kling AI** | Gratis (66 creditos/dia) | Escenas emocionales |
| B-roll extra | **Runway Gen-4 Turbo** | Gratis (125 creditos unicos) | 2-3 tomas hero |
| Voz narracion | **ElevenLabs** | $5/mes | Voz calida ES/FR |
| Voz backup | **Gemini TTS** | Gratis (ya en el stack) | Audio programatico |
| Musica fondo | **Suno v4** | Gratis (50 creditos/dia) | Guitarra acustica + piano |
| Grabacion pantalla | **OBS Studio** | Gratis | Demo WhatsApp |
| Edicion video | **CapCut** | Gratis | Montaje + auto-subtitulos |
| Edicion transcripcion | **Descript** | Gratis (tier limitado) | Limpieza narracion demo |
| Clips sociales | **Opus Clip** | Gratis (60 creditos/mes) | Auto-generar clips 15s |
| Graficos/branding | **Canva** | Gratis | Titulos, lower thirds |

---

## 3. Herramientas de Video IA

### Comparativa Detallada

| Herramienta | Calidad | Duracion Max | Free Tier | Precio | Veredicto Clara |
|-------------|---------|-------------|-----------|--------|----------------|
| **Kling AI** | Excelente caras, 1080p | 5-10s (free), 3min (paid) | **66 creditos/dia** (refresh diario!) | Desde $6.99/mes | **TOP PICK** — mejor free tier |
| **Runway Gen-4** | Profesional, mejor control camara | ~10s | 125 creditos unicos (~25s video) | $15-35/mes | Secundario — creditos limitados |
| **Sora 2** | Top realismo, fisica | 5-25s | **Ninguno** (suspendido ene 2026) | $20-200/mes | Demasiado caro. Skip. |
| **Pika 2.5** | Bueno estilizado | ~5s | 80 creditos/mes, **480p** | $8/mes | 480p gratis = inutilizable |
| **Luma Dream Machine** | Artistico, coherente | ~5s | **Solo imagenes** (no video gratis) | $9.99/mes | Sin video gratis. Skip. |
| **Veo 3 (Google)** | Excelente, audio nativo | ~8s | Requiere Google AI Pro ($19.99) | $19.99/mes | Bueno pero requiere suscripcion |
| **Hailuo AI** | Cinematico, rapido | ~6s | Limitado | $14.99/mes | Backup decente |
| **WAN 2.1 (Alibaba)** | Alto, open source | Variable | **Open source** (self-host) | $0 | Interesante si hay GPU disponible |

### Recomendacion

- **Primario: Kling AI** — generar 1-2 clips/dia durante varios dias antes del hackathon
- **Secundario: Runway Gen-4 Turbo** — usar los 125 creditos unicos para 2-3 tomas hero planificadas

---

## 4. Voces y Narracion IA

| Herramienta | Calidad ES/FR | Free Tier | Precio | Veredicto |
|-------------|---------------|-----------|--------|-----------|
| **ElevenLabs** | Excelente ambos | ~10 min/mes | **$5/mes** (30K chars) | **TOP PICK** — mejor calidad, clonar voz Clara |
| **Gemini TTS** | Bueno ambos | Gratis (API) | Pay-per-use | **Secundario** — ya esta en el stack |
| **Murf AI** | Bueno, variedad acentos | Trial limitado | $19/mes | Backup si ElevenLabs no convence |
| **LMNT** | **Malo en espanol** | 15K chars gratis | $10/mes | **Evitar** — pronunciacion pobre en ES |
| **PlayHT** | N/A | **CERRADO** dic 2025 | N/A | No disponible |

### Configuracion para la Voz de Clara

Con ElevenLabs:
- Seleccionar voz femenina calida, registro medio
- Stability: media (variacion natural)
- Similarity: alta (consistencia)
- Estilo: empatico, calmado, reconfortante
- **NO:** robotico, corporativo, rapido

---

## 5. Musica IA

| Herramienta | Calidad | Free Tier | Precio | Veredicto |
|-------------|---------|-----------|--------|-----------|
| **Suno v4** | La mejor | **50 creditos/dia** (refresh!) | $10/mes (comercial) | **TOP PICK** — generosisimo |
| **Udio** | Alta, generos especificos | 100/mes + 10/dia | Planes pagos | Backup si Suno no da el tono |
| **Stable Audio** | Ambiente/SFX | 10 creditos unicos | Creditos | Solo para efectos de sonido |

### Prompt Recomendado para Suno

```
Soft acoustic guitar with gentle piano, warm hopeful documentary background,
emotional but uplifting, no vocals, Spanish Mediterranean influence,
gentle strings entering gradually, 60 seconds
```

**NO:** "corporate ukulele", "tech startup energy", "upbeat pop"

---

## 6. Edicion y Postproduccion

| Herramienta | Funcion | Free | Veredicto Clara |
|-------------|---------|------|-----------------|
| **CapCut** | Edicion completa, auto-subtitulos | Si | **Principal** — subtitulos ES/FR automaticos |
| **Descript** | Edicion por transcripcion | Tier limitado | **Para Video B** (demo con narracion) |
| **Opus Clip** | Repurpose largo->corto | 60 creditos/mes | **Para clips sociales** — auto-genera 15s |
| **Canva** | Graficos, templates | Si | **Titulos y graficos de marca** |
| **DaVinci Resolve** | Color grading profesional | Si | Si se necesita color grading avanzado |

---

## 7. Grabacion de Pantalla

| Herramienta | Coste | Veredicto |
|-------------|-------|-----------|
| **OBS Studio** | **Gratis**, open source | **Principal** — sin watermark, sin limite |
| **Loom** | Free tier | Para comunicacion interna del equipo |
| **Screen Studio** | $29/mes (solo macOS) | Hermoso pero caro. Solo si alguien ya lo tiene. |

### Tips para la Grabacion del Demo

- Grabar en un **telefono fisico** (no simulador) para autenticidad
- Grabar a **60fps**, luego reducir a 80% velocidad = mas cinematico
- Usar conversacion WhatsApp **limpia y curada** con mensajes realistas
- Preparar el demo con **modo avion** (evitar notificaciones reales)

---

## 8. Prompt Engineering para Video IA

### Estructura de un Prompt Efectivo

```
[Movimiento camara] + [Descripcion sujeto] + [Accion/Movimiento] +
[Entorno/Escenario] + [Iluminacion/Mood] + [Estilo/Estetica]
```

### Principios Clave

1. **Ser especifico sobre el movimiento.** "Camera slowly dollies forward" no solo "moving shot"
2. **Una accion por clip.** Multiples acciones confunden al modelo
3. **Especificar duracion y ritmo.** "Slow, contemplative" vs "dynamic, fast-paced"
4. **Usar lenguaje cinematico.** "Shallow depth of field", "golden hour", "handheld documentary"
5. **Incluir tono emocional.** "Hopeful", "intimate", "determined"
6. **Consistencia entre tomas.** Usar las mismas keywords de estilo en cada prompt
7. **Generar imagen primero.** Image-to-video da mas control que text-to-video
8. **Iterar en lotes.** Generar 3-4 variaciones de cada toma, elegir la mejor

### Negative Prompts (donde se soporte)

```
No text overlays, no watermarks, no distortion, no extra fingers,
not corporate, not stock photo aesthetic
```

---

## 9. Prompts Especificos para Clara

### Prompt 1 — Opening Hook (Emocional)
```
Slow dolly-in on the face of a middle-aged woman of North African descent,
sitting at a kitchen table in a modest Spanish apartment. She is looking at
her phone with a hopeful, relieved expression. Warm golden morning light
streams through a window with sheer curtains. Shallow depth of field.
Documentary cinematic style. Color palette: warm tones with touches of
blue (#1B5E7B). Intimate, hopeful mood. 4 seconds.
```

### Prompt 2 — Interaccion WhatsApp (Close-up)
```
Extreme close-up of hands holding a smartphone. The screen shows a WhatsApp
conversation with green message bubbles. The person's thumb taps a voice
message button and begins recording. Warm soft lighting. Shallow depth of
field. The hands belong to a young Latino man. Smooth, steady camera.
Realistic style. 4 seconds.
```

### Prompt 3 — Ciudad Espanola (Establishing Shot)
```
Wide aerial shot slowly descending over a diverse Spanish neighborhood,
showing a mix of old and modern buildings, small shops with multilingual
signs, people walking on sunny streets. Mediterranean sunlight. Warm color
grading with blue (#1B5E7B) sky tones. Cinematic drone footage style.
Hopeful, vibrant mood. 5 seconds.
```

### Prompt 4 — Oficina Gobierno
```
Medium shot of a young woman of Sub-Saharan African descent standing in
line at a Spanish government office. She looks uncertain but then glances
at her phone and smiles slightly. Fluorescent office lighting mixed with
natural light from large windows. Documentary photography style. Muted
colors with warm highlights. 4 seconds.
```

### Prompt 5 — Momento de Grabacion de Voz
```
Over-the-shoulder shot of a person speaking into their phone in a quiet
park. We see the phone screen with a voice waveform animation. Dappled
sunlight through trees. Green foliage in background (#2E7D4F). Shallow
depth of field. Peaceful, empowering mood. Camera slowly pushes in.
Cinematic style. 4 seconds.
```

### Prompt 6 — Celebracion Familiar (Resultado)
```
Medium wide shot of a small immigrant family in a Spanish apartment,
celebrating together. A woman holds up an official document with joy.
A child hugs her. Warm interior lighting with orange (#D46A1E) accent
tones from a table lamp. Slightly handheld camera for documentary feel.
Genuine emotion, hopeful and warm. 5 seconds.
```

### Prompt 7 — Fondo Abstracto (Para Texto)
```
Smooth animated abstract background with flowing gradients transitioning
between deep blue (#1B5E7B), warm orange (#D46A1E), and forest green
(#2E7D4F). Subtle particle effects floating upward like fireflies.
Gentle organic motion. Clean, modern, calming. Perfect for text overlay.
Minimal style. 4 seconds.
```

### Prompt 8 — Montaje Multilingue
```
Split-screen showing three different people each speaking into their
phones in different settings: a kitchen, a park bench, a bus stop. Each
person represents a different origin — Latin American, North African,
West African. Natural lighting in each scene. Documentary style. Warm
color grading. Camera is static in each frame. Authentic, diverse,
inclusive mood. 5 seconds.
```

### Prompt 9 — Tecnologia Encuentra Humanidad
```
Slow tracking shot across a wooden desk showing a smartphone next to a
cup of tea, a handwritten note in Spanish, and a small plant. The phone
screen gently illuminates. Morning light. Overhead angle, slowly moving
left to right. Warm tones, cozy atmosphere. ASMR-like intimate quality.
Shallow depth of field. 4 seconds.
```

### Prompt 10 — Cierre / Call to Action
```
Wide shot of a diverse group of people walking together on a sunlit
Spanish street, seen from behind. They walk toward a bright horizon.
Golden hour lighting creates long shadows. Cinematic slow motion. Warm
color palette with blue sky. Hopeful, forward-looking, united. The
camera slowly rises. 5 seconds.
```

---

## 10. Estructura de Videos Ganadores de Hackathon

### Formato 30 Segundos (Social)

| Segundo | Contenido | Proposito |
|---------|-----------|-----------|
| 0-3 | **Pattern interrupt** — voz real, cara confusa, formulario ilegible | Parar el scroll |
| 3-10 | **El dolor** — "10 millones de inmigrantes. 2 de cada 3 no navegan el papeleo." | Estadistica demoledora |
| 10-20 | **El momento magico** — alguien habla en frances en WhatsApp, Clara responde en frances | Show, don't tell |
| 20-27 | **Tagline + logo** — "Tu voz tiene poder" | Resonancia emocional |
| 27-30 | **QR code o URL** | Call to action |

### Formato 90 Segundos (Jueces)

| Segundo | Contenido | Rubrica OdiseIA |
|---------|-----------|-----------------|
| 0-5 | **Hook** — "Ahmed acaba de llegar a Espana. No habla espanol." | Elevator Pitch (40%) |
| 5-20 | **Escalar el problema** — "10M inmigrantes. 67% con barreras." | Social Entities (25%) |
| 20-30 | **Presentar Clara** — "Asistente WhatsApp que escucha tu voz y explica tus derechos" | Elevator Pitch (40%) |
| 30-35 | **Por que WhatsApp** — "33M usuarios en Espana. Sin descargar nada." | Elevator Pitch (40%) |
| 35-60 | **DEMO EN VIVO** — WOW 1 (texto ES) + WOW 2 (voz FR -> respuesta FR) | Prototype Demo (25%) |
| 60-75 | **Credibilidad** — "Fuentes verificadas. 532 tests. Desplegado y funcionando." | Prototype Demo (25%) |
| 75-85 | **Open source** — "Cualquier ayuntamiento puede desplegar Clara manana. Gratis. Siempre." | Sustainability (10%) |
| 85-90 | **Tagline + QR** — "Tu voz tiene poder." | Todas |

### Lo que Buscan los Jueces (OdiseIA4Good)

Basado en los ganadores de 2025 (Dilo Facil, GaIA, Radar de Vulnerabilidad):

1. **Resonancia emocional sobre sofisticacion tecnica** — los ganadores construyen pitches alrededor de historias humanas, no arquitectura de software
2. **Demo funcionando** — los jueces quieren verlo funcionar, no oir como podria funcionar
3. **Impacto cuantificable** — "19.5 millones de usuarios potenciales. Coste por consulta: 0.2 centimos. Licencia: cero."
4. **Conexion clara problema-solucion** — la cadena causal debe ser obvia

---

## 11. Guion del Video de 90 Segundos

```
[0:00-0:03] PANTALLA NEGRA. Sonido de telefono sonando sin respuesta.
             Musica de espera burocratica.
             Texto: "En Espana viven casi 10 millones de inmigrantes."

[0:03-0:08] Cortes rapidos: formularios gobierno, colas largas, web en
             espanol denso.
             Texto: "67% han sufrido barreras burocraticas."
             Musica: piano suelto, sombreo (tono menor).

[0:08-0:12] Close-up de mano sosteniendo telefono, perdida.
             Texto: "Si no hablas el idioma... te quedas fuera."

[0:12-0:15] TRANSICION. Sonido notificacion WhatsApp. Pantalla se ilumina.
             La mano abre WhatsApp. Escribe: "Hola Clara."
             Musica cambia: esperanzadora, ascendente.

[0:15-0:20] Voz del presentador: "Nosotros construimos a Clara."
             Breve toma del equipo o presentador.

[0:20-0:25] "Una asistente de WhatsApp que te explica tus derechos.
             En tu idioma. Con tu voz."

[0:25-0:30] WOW 1: "Que es el IMV?" escrito en WhatsApp.
             Clara responde al instante. Camara muestra el texto claro.
             Reproducir audio de respuesta 3-4 segundos.

[0:30-0:55] WOW 2: Alguien graba nota de voz EN FRANCES preguntando
             sobre empadronamiento. Clara responde EN FRANCES con texto
             Y audio.
             ESTE ES EL MOMENTO MAGICO. Dejarlo respirar.
             Mostrar la reaccion de la persona.
             Texto overlay: "Espanol. Frances. Voz. Texto. 24 horas."

[0:55-1:05] Montaje rapido de datos clave:
             "33 millones usan WhatsApp en Espana. Sin descargar nada."
             "Informacion verificada del gobierno. No inventa."
             "532 pruebas automatizadas. Desplegada y funcionando."

[1:05-1:15] "Todo el codigo es abierto y gratuito.
             Cualquier ayuntamiento puede desplegar Clara manana.
             Sin pagar un euro. Para siempre."

[1:15-1:25] Volver a la persona del inicio. Ahora entiende.
             Sonrie. Comparte el numero de Clara con alguien mas.
             Musica: resuelta, piano pacifico.

[1:25-1:30] PANTALLA NEGRA. Texto blanco, centrado:
             "Tu voz tiene poder."
             QR debajo. "Prueba Clara ahora."
             Equipo + OdiseIA4Good 2026 + UDIT Madrid.
```

---

## 12. Storytelling Before/After

### ANTES (primeros 20-30 segundos)

- **Color:** Desaturado, tonos frios (grises, azules). Camara ligeramente temblorosa.
- **Sonido:** Ruido ambiental — oficina burocratica, papeles, telefono sonando sin respuesta, voz grabada "pulse 3 para espanol."
- **Visuales:**
  - Formulario gobierno en espanol juridico denso, camara zoom lento
  - Persona scrolleando infinitamente web gobierno en su telefono
  - Cola larga en oficina municipal
  - Texto: "67% de inmigrantes enfrentan barreras burocraticas"

### TRANSICION (2-3 segundos)

- Sonido notificacion WhatsApp. Telefono se ilumina.
- La persona abre WhatsApp. Escribe "Hola Clara" o graba nota de voz.
- Musica cambia.

### DESPUES (30-40 segundos)

- **Color:** Tonos calidos (ambar, luz dorada). Camara estable.
- **Sonido:** Musica suave, esperanzadora (piano + cuerdas). Voz de Clara respondiendo.
- **Visuales:**
  - Conversacion WhatsApp llenandose de instrucciones claras
  - La persona asintiendo, entendiendo
  - Reproduciendo audio de Clara y sonriendo
  - Split screen: IZQUIERDA = formulario incomprensible, DERECHA = explicacion de Clara
  - Texto: "Tu voz tiene poder"

### Principio Clave: Fortalezas, No Victimismo

Clara NO salva personas — Clara ayuda a las personas a salvarse a si mismas. "Tu voz tiene poder." El "antes" debe ser breve y honesto, pero el "despues" debe ser mas largo, calido, y lleno de agencia.

---

## 13. Musica y Emocion

### Progresion de Mood

| Fase | Tempo | Instrumentos | Tono |
|------|-------|-------------|------|
| Problema (0-20s) | 60-80 BPM | Piano solo, menor | Reflexivo, sombrio |
| Transicion (20-50s) | 80-100 BPM | Piano + cuerdas suaves | Esperanzador, ascendente |
| Demo (50-80s) | 90-110 BPM | Piano + cuerdas + percusion ligera | Confiado, calido |
| Cierre (80-90s) | 70-80 BPM | Piano solo, nota sostenida | Resuelto, pacifico |

### Fuentes Gratuitas

- **Bensound** (bensound.com) — "Breath" y tracks emocionales de documentales
- **Scott Holmes Music** (scottholmesmusic.com) — Musica emocional gratis
- **Pixabay Music** — Buscar "Documentary Piano Emotional Strings"
- **Suno v4** (gratis) — Generar con prompt personalizado

### Regla Critica

La musica **NUNCA** debe competir con la voz de Clara. Durante cualquier seccion donde suena la respuesta de Clara (audio WhatsApp), la musica debe bajar a casi-silencio. La estrella es la voz de Clara respondiendo.

---

## 14. Etica: Representar Vulnerabilidad con Dignidad

### El Problema del "Poverty Porn 2.0"

Segun The Lancet Global Health y Fairpicture, imagenes IA que replican "la intensidad emocional y gramatica visual del poverty porn" son un peligro real. Incluso sin personas reales representadas, el dano es real.

### Reglas para Clara

**HACER:**
- Revelar uso de IA transparentemente (requerido por EU AI Act desde agosto 2026)
- Centrar agencia, no victimismo — personas tomando decisiones, navegando, teniendo exito
- Usar visuales no-figurativos (mapas, diagramas, metaforas) para representar dificultades
- Mostrar **individuos, no multitudes** — una persona usando su telefono, no una cola en una oficina
- Mostrar **momentos mundanos y dignos** — mesa de cocina, parque, commute

**NO HACER:**
- **Nunca usar IA para fabricar sufrimiento humano**
- **Nunca generar caras IA** para representar poblaciones vulnerables especificas
- **Nunca usar imagenes sensacionalistas** para generar respuesta emocional
- **Nunca usar accesorios culturales como unico identificador** (panuelos, maletas, vallas)

### Tecnicas Cinematograficas Dignificantes

- **Camara a nivel de ojos** — nunca disparar hacia abajo. Encuadre a nivel = igualdad.
- **Planos medios y close-ups de manos** — manos en el telefono, sosteniendo documentos. Las manos cuentan historias de competencia y accion.
- **Profundidad de campo suave** en caras durante momentos emocionales — intimidad sin voyeurismo.
- **Iluminacion natural calida** — evitar luz institucional que codifica "burocracia" o "interrogatorio".
- **Movimiento** — sujetos caminando con proposito, no sentados esperando. Movimiento = agencia.

### Modelo Participativo

Considerar dar telefonos a 3-4 usuarios reales de Clara y pedirles grabar su propio "momento de alivio" — cuando entendieron algo, cuando se sintieron menos solos. Este material auto-dirigido tiene una autenticidad que ningun equipo de produccion puede fabricar.

---

## 15. Color Grading para la Marca Clara

### Paleta Clara en Terminos de Color Grading

| Color | Hex | Rol en Color Grading |
|-------|-----|---------------------|
| Azul Confianza | #1B5E7B | Sombras, fondos, confianza |
| Naranja Calidez | #D46A1E | Highlights, calidez piel, energia |
| Verde Esperanza | #2E7D4F | Acentos, naturaleza, resolucion |

### Estructura de Nodos DaVinci Resolve

1. **Correccion Base** — Balance blancos ~5600K (luz dia calida), normalizar exposicion
2. **Proteccion Tonos Piel** — Aislar con qualifier, anadir calidez (+5-10 vector naranja). Critico para diversidad de tonos de piel.
3. **Push Sombras (Clara Blue)** — Lift wheel hacia azul-teal, targetando #1B5E7B. Sutil.
4. **Push Highlights (Clara Orange)** — Gain wheel hacia naranja calido, targetando #D46A1E. Calidez dorada.
5. **Tinte Medios Tonos (Clara Green)** — Gamma wheel muy sutil hacia verde #2E7D4F (5-10%).
6. **Look Final / LUT** — Film emulation suave (Kodak 2383), reducir opacidad LUT a 40-60%, grano sutil.

### LUTs Recomendados

- **CineWarm LUT** (MyCREATIVEfx) — gratis, calido y suave
- **Kodak 2383 Film Print** — clasico calido cinematico
- **Evitar:** LUTs frios/clinicos, alto contraste, desaturados "thriller"

---

## 16. Diseno de Sonido

### Paleta Sonora Clara

**Sonidos de Conexion:**
- Notificacion WhatsApp (universalmente reconocido para la audiencia de Clara)
- Indicador "grabando" de nota de voz
- Vibracion suave de telefono en mesa
- "Swoosh" de mensaje enviado
- "Pop" de mensaje recibido

**Sonidos del Dia a Dia:**
- Hervidor hirviendo (domesticidad, hogar, calma)
- Sonidos calle espanola — trafico distante, ninos jugando (vida, no caos)
- Puerta abriendose (acceso, bienvenida)
- Pasos en acera (movimiento con proposito, agencia)

**Sonidos de Alivio y Esperanza:**
- Exhalacion profunda (tension liberandose)
- Risa pequena, genuina
- Pajaros manana (nuevo comienzo)

**Evitar:**
- Swells orquestrales dramaticos
- Latidos de corazon aislados
- Llantos o sonidos de angustia
- Sirenas, alarmas
- Musica "etnica" estereotipada

### Principio: Silencio como Herramienta

Usar silencio o casi-silencio ANTES de momentos clave. Cuando Clara responde en el idioma de alguien por primera vez, un breve momento de silencio antes del audio crea anticipacion y peso emocional.

---

## 17. Subtitulos y Accesibilidad

### Herramientas de Auto-Subtitulos

| Herramienta | Espanol | Frances | Coste |
|-------------|---------|---------|-------|
| **CapCut Auto Captions** | Excelente | Bueno | Gratis |
| **Whisper (OpenAI)** | Excelente | Excelente | Gratis (local) |
| **Descript** | Excelente | Bueno | Free tier |

### Workflow Recomendado

1. Grabar/generar voiceover en espanol
2. Pasar por **Whisper** (ya en el proyecto) para generar SRT preciso
3. Importar SRT en **CapCut** para estilizar y ajustar timing
4. Duplicar y traducir para version francesa con Claude o DeepL
5. Estilizar: texto blanco, fondo semi-transparente oscuro, fuente calida sans-serif

### Especificaciones Subtitulos

- Maximo 2 lineas por subtitulo
- Maximo 42 caracteres por linea (37 para arabe)
- Tiempo minimo display: 1.5 segundos
- Fuente: Sans-serif clara (Noto Sans para soporte multilingue)
- Tamano minimo: 28px a 1080p
- Incluir sonidos no-verbales: [telefono vibra], [mensaje enviado], [voz de Clara]

### Checklist Accesibilidad

- [ ] Subtitulos quemados (open captions) para redes sociales
- [ ] Archivos SRT/VTT separados para YouTube/LinkedIn
- [ ] Contraste alto texto (WCAG AA 4.5:1)
- [ ] Sin contenido que flashee >3 veces/segundo
- [ ] Audio sin picos repentinos (rango dinamico comprimido)
- [ ] Version baja resolucion (480p) para conexiones lentas
- [ ] Video comprensible SIN audio (storytelling visual)

---

## 18. Video Multilingue (ES/FR/AR)

### Estrategia de Tres Niveles

**Nivel 1: Storytelling Visual Universal**
- Disenar el video para ser comprensible SIN audio
- Usar metaforas visuales universales: telefono iluminandose, puerta abriendose, camino despejandose

**Nivel 2: Subtitulos (metodo principal)**
- Pistas separadas para espanol (default), frances, y arabe
- Subtitulos multilingues pueden aumentar views hasta 40%

**Nivel 3: Versiones Voice-Over**
- Pistas de voz separadas por idioma
- Espanol: acento castellano para credibilidad institucional, con calidez
- Frances: frances estandar, evitar marcadores regionales
- Arabe: MSA para comprension amplia, o considerar Darija para audiencia marroqui en Espana

### Requisitos Tecnicos Arabe

- Texto RTL (right-to-left) — configurar explicitamente en software de edicion
- Fuente con soporte ligaduras arabes (Noto Sans Arabic)
- Revision por linguista nativo para tono, no solo precision

---

## 19. Formatos de Exportacion por Plataforma

### YouTube / Presentacion

| Setting | Valor |
|---------|-------|
| Resolucion | 1920x1080 |
| Aspect Ratio | 16:9 |
| Frame Rate | 24fps (cinematico) o 30fps |
| Codec | H.264 |
| Bitrate | 10-12 Mbps |
| Audio | AAC, 320kbps, stereo |
| Max archivo para slides | <100MB |

### Instagram Reels / TikTok

| Setting | Valor |
|---------|-------|
| Resolucion | 1080x1920 |
| Aspect Ratio | 9:16 |
| Frame Rate | 30fps |
| Codec | H.264 |
| Bitrate | 5-8 Mbps |
| Zona segura | Centro 1080x1420 (top/bottom cubiertos por UI) |

### LinkedIn

| Setting | Valor |
|---------|-------|
| Resolucion | 1920x1080 (16:9) o 1080x1080 (1:1) |
| Frame Rate | 30fps |
| Nota | 1:1 ocupa mas espacio en el feed |

### Resumen Exportaciones

| Video | YouTube/Slides | Reels/TikTok | LinkedIn |
|-------|---------------|-------------|----------|
| 90s Completo | 16:9 1080p | 9:16 1080x1920 | 1:1 1080x1080 |
| 30s Highlight | 16:9 1080p | 9:16 1080x1920 | 1:1 1080x1080 |
| 15s Teaser | — | 9:16 1080x1920 | — |

---

## 20. Timeline de Produccion (2 Dias)

### Dia 1: Pre-Produccion + Generacion de Assets (6-8 horas)

| Bloque | Duracion | Tarea | Quien |
|--------|----------|-------|-------|
| Manana 1 | 1.5h | Escribir guiones 3 videos (90s, 30s, 15s). El 30s y 15s son subsets del 90s. | Persona 1 |
| Manana 2 | 1.5h | Generar imagenes IA de referencia. Enviar lote de 15-20 prompts a Kling/Runway. | Persona 1 |
| Manana 2 | 1.5h | Grabar demos pantalla de WhatsApp con Clara (3-4 conversaciones diferentes). | Persona 2 |
| Tarde 1 | 2h | Revisar outputs IA. Re-generar clips fallidos. Generar voiceover con ElevenLabs. | Persona 1 |
| Tarde 1 | 2h | Buscar musica (Suno/Pixabay). Crear assets de marca en Canva (logo animations, lower-thirds). | Persona 2 |
| Tarde 2 | 1h | Organizar assets en carpetas. Backup. | Ambos |

### Dia 2: Edicion + Exportacion (6-8 horas)

| Bloque | Duracion | Tarea | Quien |
|--------|----------|-------|-------|
| Manana 1 | 3h | Editar video 90s en CapCut: voiceover, clips, texto, transiciones, musica. | Persona 1 |
| Manana 1 | 1.5h | Generar clips IA faltantes. Ayudar con prep. | Persona 2 |
| Mediodia | 1h | Revisar corte de 90s juntos. Notar cambios. | Ambos |
| Tarde 1 | 1h | Revisar video 90s. Anadir subtitulos (auto-generar + correccion manual). | Persona 1 |
| Tarde 1 | 1.5h | Crear version 30s (re-editar del timeline 90s). Crear version 15s. | Persona 2 |
| Tarde 2 | 1h | Exportar todas versiones en todos formatos. | Persona 1 |
| Tarde 2 | 0.5h | Quality check en dispositivos/plataformas reales. | Persona 2 |

### Optimizaciones de Ruta Critica

1. **Escribir guion 90s primero.** Los 30s y 15s son subsets estrictos.
2. **Empezar generacion IA temprano** — clips toman 1-5 min, y se necesitan 2-3 intentos por toma.
3. **No perfeccionar clips individuales.** Si un clip es 70% bueno, usarlo. Color grading y musica cubren imperfecciones.
4. **Pre-hacer templates de marca** (intro card, end card, lower-third) para solo drop-in.

---

## 21. Errores Fatales a Evitar

1. **Empezar con explicacion tecnica** — "Construimos una app Flask con Whisper y Gemini..." pierde la audiencia en 3 segundos. Empezar con Ahmed. Con Maria. Con el sentimiento.

2. **Demo demasiado largo o lento** — Mostrar la magia (voz in, respuesta out) en <30 segundos.

3. **Audio de mala calidad** — El problema #1. Un video con contenido genial pero audio apagado pierde contra un proyecto simple con sonido limpio. Usar mic de solapa o grabar en cuarto silencioso.

4. **Sin declaracion clara del problema** — "Construimos un chatbot IA" NO es una declaracion de problema. "67% de inmigrantes en Espana no pueden navegar la burocracia que les daria acceso a salud" SI lo es.

5. **Demasiadas features** — Mostrar UNA o DOS cosas bien. WOW 1 (texto espanol) + WOW 2 (voz frances -> respuesta frances). No intentar tambien mostrar analisis de imagenes, outputs estructurados, seleccion motor TTS, y pipeline RAG.

6. **Olvidar demo la parte dificil** — La nota de voz en frances obteniendo respuesta en frances ES el video. No saltarla.

7. **Sin humano en el video** — Un screencast con voiceover es mas debil que screencast intercalado con cara de persona.

8. **Esperar hasta ultimo minuto** — Grabar con tiempo de sobra. Subir a YouTube puede tomar horas.

9. **No alinear con criterios de jueces** — Rubrica: Elevator Pitch 40%, Social Entities 25%, Prototype Demo 25%, Sustainability 10%. Cada segundo debe mapear a uno de estos.

10. **Sin call to action** — El video termina y los jueces piensan "que bonito." Sin tagline fuerte y QR, se pierde el momentum emocional.

---

## 22. Referencias y Fuentes

### Herramientas de Video IA
- [Best AI Video Generators 2026 — WaveSpeedAI](https://wavespeed.ai/blog/posts/best-ai-video-generators-2026/)
- [Sora vs Runway vs Pika 2026 — PXZ AI](https://pxz.ai/blog/sora-vs-runway-vs-pika-best-ai-video-generator-2026-comparison)
- [Best 12 AI Video Generators — CyberLink](https://www.cyberlink.com/blog/cool-video-effects/4396/best-ai-video-generator)
- [Kling AI Complete Guide 2026](https://aitoolanalysis.com/kling-ai-complete-guide/)
- [ElevenLabs Pricing — SaaSworthy](https://www.saasworthy.com/product/elevenlabs-io/pricing)
- [Suno AI Pricing 2026](https://musicmake.ai/blog/suno-ai-pricing-plans-2026)

### Hackathon Video Strategy
- [Creating the Best Demo Video for a Hackathon](https://tips.hackathon.com/article/creating-the-best-demo-video-for-a-hackathon-what-to-know)
- [Nader Dabit: How to Give a Killer Pitch](https://gist.github.com/dabit3/caef5eee4753dd7d23767bc31e70da28)
- [AngelHack: 10 Tips to Rock Your Hackathon Demo](https://angelhack.com/blog/10-tips-to-help-you-rock-your-next-hackathon-demo/)
- [TAIKAI: How to Create a Winning Hackathon Pitch](https://taikai.network/en/blog/how-to-create-a-hackathon-pitch)
- [Kavisha Mathur: The Hackathon Insider Playbook (8x Winner)](https://medium.com/codetodeploy/the-hackathon-insider-playbook-from-a-8x-winner-de83d138bab5)

### Storytelling Social Impact
- [Happy Productions: Social Impact Video Storytelling](https://www.happyproductions.me/resources-blog/social-impact-video-storytelling)
- [Happy Productions: 10 Nonprofit Videos That Raised Millions](https://www.happyproductions.me/resources-blog/10-powerful-nonprofit-video-examples-raised-millions)
- [Leon Animations: Best Nonprofit Videos](https://www.leonanimations.com/blogs/best-nonprofit-videos-of-all-time-inspiring-stories-and-campaigns)
- [CauseVox: 10 Powerful Nonprofit Videos](https://www.causevox.com/blog/10-powerful-nonprofit-videos-to-inspire-you/)

### Etica e Imagenes IA
- [The Lancet: Avoiding Poverty Porn 2.0](https://www.thelancet.com/journals/langlo/article/PIIS2214-109X(25)00313-4/fulltext)
- [Fairpicture: White Paper on Poverty Porn in the Era of Generative AI](https://fairpicture.org/stories/white-paper-poverty-porn-in-the-era-of-generative-ai/)
- [Migration Policy Institute: Visual Portrayals of Migrants](https://www.migrationpolicy.org/article/visual-portrayals-migration)
- [WITNESS Media Lab: Storytelling for Immigrant Justice](https://lab.witness.org/storytelling-strategies-for-immigrant-justice-in-the-u-s/)
- [EU AI Act Article 50: Transparency Obligations](https://artificialintelligenceact.eu/article/50/)

### Color Grading y Sonido
- [Adobe: Orange and Teal Color Grading](https://www.adobe.com/creativecloud/video/hub/features/why-use-orange-teal-grading.html)
- [RawFilm: Perfect Skin Tones in DaVinci Resolve](https://blog.raw.film/advanced-tutorial-how-to-create-perfect-skin-tones-in-davinci-resolve/)
- [FilmSound.org: Michel Chion on Empathetic Sound](http://www.filmsound.org/chion/empath.htm)

### Subtitulos y Accesibilidad
- [accessiBe: ADA Video Compliance 2026](https://accessibe.com/blog/knowledgebase/ada-compliance-for-videos)
- [3Play Media: WCAG Captioning Requirements](https://www.3playmedia.com/blog/wcag-2-0-requirements-for-video-captioning-and-audio-description/)
- [Aglatech14: Multilingual Subtitles](https://www.aglatech14.com/en/how-to-make-your-videos-accessible-with-multilingual-subtitles/)

### Ganadores OdiseIA4Good 2025
- [OdiseIA4Good Votaciones](https://www.odiseia4good.org/en/votaciones)
- [OdiseIA Blog: GaIA — De la Idea al Impacto](https://www.odiseia.org/post/de-la-idea-al-impacto-el-camino-de-gaia-un-asistente-contra-la-soledad-nacido-en-un-hackathon-en)

---

*Clara — Tu voz tiene poder.*
*OdiseIA4Good 2026 — UDIT Madrid*
