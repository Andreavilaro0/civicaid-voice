# Prompt Engineering Guide: Hyperrealistic Visual Assets for Clara

> Project: CivicAid Voice / Clara - Social impact project for immigrants in Spain
> Date: February 2026
> Purpose: Generate photorealistic images and videos for presentations, pitch decks, social media, and marketing

---

## Table of Contents

1. [The Master Prompt Formula](#1-the-master-prompt-formula)
2. [Model-Specific Keywords & Strategies](#2-model-specific-keywords--strategies)
3. [Negative Prompts (Anti-Artifact Arsenal)](#3-negative-prompts-anti-artifact-arsenal)
4. [Camera, Lens & Film Stock Reference Library](#4-camera-lens--film-stock-reference-library)
5. [Lighting Techniques Reference](#5-lighting-techniques-reference)
6. [Copy-Paste Prompt Templates for Clara](#6-copy-paste-prompt-templates-for-clara)
7. [Video Prompt Engineering](#7-video-prompt-engineering)
8. [Common Mistakes & How to Avoid Them](#8-common-mistakes--how-to-avoid-them)
9. [Inclusive Representation Guidelines](#9-inclusive-representation-guidelines)
10. [Advanced Techniques & Workflows](#10-advanced-techniques--workflows)
11. [Recommended Tool Selection by Use Case](#11-recommended-tool-selection-by-use-case)

---

## 1. The Master Prompt Formula

### The 8-Point Shot Grammar Framework

Every photorealistic prompt should contain these elements in order of priority:

```
[Subject & Action] + [Emotional Energy] + [Setting/Environment] + [Camera & Lens] +
[Lighting] + [Film Stock / Color Science] + [Composition] + [Technical Quality Tags]
```

### Detailed Breakdown

| Element | Purpose | Example |
|---------|---------|---------|
| **Subject & Action** | Who, what they look like, what they are doing | "A 35-year-old Moroccan woman wearing a sage green hijab, smiling while reading her phone" |
| **Emotional Energy** | The feeling/mood of the scene | "expression of quiet relief and hope" |
| **Setting/Environment** | Where, time of day, background details | "sitting on a park bench in a sun-dappled plaza in Madrid, spring afternoon" |
| **Camera & Lens** | Equipment specification triggers realism | "shot on Canon EOS R5, 85mm f/1.4 lens" |
| **Lighting** | Specific lighting setup or natural light | "soft golden hour sidelight, Rembrandt lighting pattern on face" |
| **Film Stock / Color Science** | Color palette and texture | "Kodak Portra 400 film emulation, warm skin tones" |
| **Composition** | Framing, angle, depth of field | "medium close-up, shallow depth of field, bokeh background" |
| **Technical Quality Tags** | Resolution and realism markers | "photorealistic, ultra-detailed, 8K, natural skin texture with visible pores" |

### Why Order Matters

The closer a word is to the BEGINNING of the prompt, the more influence it has on the generation. Always lead with your subject and their action, not with technical specifications.

---

## 2. Model-Specific Keywords & Strategies

### Midjourney V7 (Best for: Emotional mood, cinematic portraits)

**What works:**
- Natural language descriptions (not keyword salad)
- Detailed visual descriptions of clothing, age, ethnicity, emotion
- Camera types and settings as natural language
- Style references via `--sref [URL]` for consistent aesthetic across images
- `--style raw` for less stylized, more photographic output
- Aspect ratios: `--ar 4:5` (Instagram portrait), `--ar 16:9` (presentation), `--ar 3:2` (classic photo)

**Keywords that trigger photorealism:**
- "editorial photograph", "documentary photograph", "candid photograph"
- "natural light portrait", "environmental portrait"
- "photographed by [real photographer name]" (e.g., Steve McCurry, Sebastiao Salgado)
- Avoid: "photorealistic" or "hyperrealistic" (counterintuitively, MJ responds better to detailed descriptions)

**V7 Strengths:** Superior hand anatomy, natural skin textures, better coherence for complex scenes.

### FLUX 1.1 Pro / FLUX Dev (Best for: Technical accuracy, DSLR-quality output)

**What works:**
- Technical camera specifications get excellent results
- Structured prompts with clear sections
- Longer, more detailed prompts (300+ characters)
- Film stock references significantly affect output quality
- Excellent at following precise instructions

**Keywords that trigger photorealism:**
- "DSLR photograph", "professional photograph", "press photograph"
- "raw photograph", "unedited photograph"
- "natural skin texture", "visible skin pores", "subsurface scattering"
- "film grain", "lens imperfections", "chromatic aberration"

**FLUX Strengths:** Images look like they came from a DSLR camera. Unmatched technical precision. Best for hero shots and final production assets.

**FLUX Weakness:** Skin can sometimes appear plastic-like. Counter this with: "imperfect skin, natural skin texture, visible pores, subtle skin blemishes"

### ChatGPT / GPT-4o Image Generation (Best for: Iterative refinement, complex instructions)

**What works:**
- Long paragraph-style prompts with multi-turn editing
- Conversational refinement ("make the lighting warmer", "add more wrinkles to his hands")
- Excellent at understanding complex compositional instructions
- Good at text rendering on screens/phones

**Keywords that trigger photorealism:**
- "photograph taken with...", "photo captured during..."
- "editorial photography style", "National Geographic style"
- "VSCO film filter", "analog photography aesthetic"

### Google Imagen 3 (Best for: Diverse representation, ethical generation)

**What works:**
- Clear, descriptive natural language
- Specific cultural and contextual details
- Good at generating diverse faces without stereotyping
- Strong text rendering capability

**Keywords that trigger photorealism:**
- "documentary photography", "photojournalistic style"
- "real people", "authentic moment", "unstaged"
- "available light photography"

### DALL-E 3 (Best for: Precise prompt adherence, complex scenes)

**What works:**
- Very long, detailed descriptions
- Understands complex spatial relationships
- Best at following multi-element instructions precisely
- Good for before/after compositions when described carefully

---

## 3. Negative Prompts (Anti-Artifact Arsenal)

Negative prompts tell the AI what to EXCLUDE. They are essential for Stable Diffusion/FLUX and useful as guidance notes for other models.

### Universal Negative Prompt (Copy-Paste Ready)

```
worst quality, low quality, low resolution, blurry, out of focus, jpeg artifacts,
compression artifacts, noise, pixelated, deformed, distorted, disfigured, mutated,
bad anatomy, wrong anatomy, extra limbs, missing limbs, floating limbs,
disconnected limbs, malformed hands, extra fingers, missing fingers, fused fingers,
too many fingers, long neck, mutated hands, poorly drawn face, poorly drawn hands,
mutation, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch,
cartoon, drawing, anime, illustration, painting, digital art, text, watermark,
signature, border, frame
```

### Category-Specific Negative Prompts

**For Faces (Critical):**
```
deformed face, distorted face, asymmetrical face, bad teeth, yellow teeth,
crooked teeth, unnatural smile, creepy smile, dead eyes, lifeless eyes,
doll eyes, crossed eyes, wall eyes, misaligned features, uncanny valley,
plastic face, waxy face, mannequin, double chin artifact
```

**For Hands (The Hardest Part):**
```
bad hands, malformed hands, wrong number of fingers, extra fingers,
missing fingers, fused fingers, webbed fingers, too long fingers,
too short fingers, deformed fingers, mutated hands, poorly drawn hands,
extra hands, twisted fingers, unnatural palm, broken wrist
```

**For Skin Realism:**
```
plastic skin, waxy skin, poreless skin, airbrushed, overly smooth skin,
silicon skin, doll skin, mannequin skin, rubber skin, unrealistic skin color,
unnatural skin tone, shiny skin, glossy skin
```

**For Maintaining Photo-Realism (No Art Styles):**
```
cartoon, anime, illustration, painting, drawing, sketch, 3d render,
cgi, digital art, unrealistic, artificial, fantasy, surreal, abstract,
oversaturated, overexposed, HDR overdone, oversharpened
```

### Weighted Negative Prompts (For Stable Diffusion/FLUX)

Use weight syntax to emphasize critical exclusions:
```
(deformed hands:1.4), (extra fingers:1.4), (plastic skin:1.3),
(blurry:1.2), (cartoon:1.5), (illustration:1.5), (painting:1.5),
(bad anatomy:1.3), (disfigured face:1.4)
```

> Tip: Do not over-weight everything above 1.5 -- it can cause unexpected artifacts. Reserve 1.4-1.5 for your biggest problem areas (usually hands and faces).

---

## 4. Camera, Lens & Film Stock Reference Library

AI models associate specific camera/lens combinations with professional, high-fidelity images. Using them activates the visual patterns the model learned from millions of real photographs taken with these tools.

### Camera Bodies (What They Trigger)

| Camera | Visual Association | Best For |
|--------|-------------------|----------|
| Canon EOS R5 | Clean, sharp, vibrant colors | Portraits, product shots |
| Sony A7 IV | Neutral colors, excellent dynamic range | Documentary, street |
| Nikon Z8 | Rich detail, warm tones | Portraits, editorial |
| Leica M11 | Distinctive rendering, 3D pop, micro-contrast | Street, editorial |
| Fujifilm X-T5 | Film-like colors, retro aesthetic | Candid, lifestyle |
| Hasselblad X2D | Medium format look, shallow DOF, ultra-detail | Portraits, fashion |
| Ricoh GR III | Gritty, contrasty street look | Street, documentary |
| Phase One IQ4 | Ultra-high resolution studio look | Product, beauty |

### Lens Specifications (What They Trigger)

| Lens | Visual Effect | Best For |
|------|--------------|----------|
| 24mm f/1.4 | Wide environmental context, slight distortion | Scene-setting, environments |
| 35mm f/1.4 | Natural perspective, slight bokeh | Documentary, street, candid |
| 50mm f/1.2 | Classic "human eye" perspective, beautiful bokeh | General portraits, candid |
| 85mm f/1.4 | Flattering compression, creamy bokeh | Portrait headshots, emotional close-ups |
| 105mm f/2.8 | Tight framing, smooth background | Beauty, detail shots |
| 135mm f/2 | Strong compression, dreamy separation | Emotional portraits |
| 70-200mm f/2.8 | Versatile telephoto compression | Candid from distance, events |

### Film Stock References (Color Science)

| Film Stock | Color Character | Best For Clara |
|------------|----------------|----------------|
| **Kodak Portra 400** | Warm, peachy skin tones, soft pastels, fine grain | Portraits of people -- BEST for diverse skin tones |
| **Kodak Portra 160** | Finer grain, more subtle warmth, lower contrast | Studio-like portraits, beauty shots |
| **Kodak Portra 800** | More grain, warm push in low light | Indoor scenes, evening scenarios |
| **Fuji Pro 400H** | Cool-neutral, light and airy, pastel greens/blues | Bright daytime scenes, hopeful mood |
| **Kodak Gold 200** | Nostalgic warmth, saturated yellows/reds, grain | Warm everyday scenes, community shots |
| **Kodak Ektar 100** | High saturation, vivid colors, ultra-fine grain | Landscape scenes, vibrant settings |
| **Cinestill 800T** | Tungsten-balanced, halation around highlights, moody | Night scenes, emotional drama |
| **Ilford HP5 Plus** | Black and white, high contrast, documentary feel | Dramatic B&W documentary portraits |
| **Fujifilm Superia 400** | Consumer warmth, everyday nostalgia | Casual, everyday life scenes |
| **Kodak Tri-X 400** | Classic B&W, rich tones, iconic grain | Photojournalistic B&W |

### Combining Camera + Lens + Film Stock (Example)

```
shot on Canon EOS R5, 85mm f/1.4 lens, Kodak Portra 400 film emulation,
natural skin tones, fine film grain, shallow depth of field
```

This combination is the "golden standard" for photorealistic AI portraits with natural, flattering skin tones.

---

## 5. Lighting Techniques Reference

### Named Lighting Patterns

| Technique | Description | Emotional Association |
|-----------|-------------|---------------------|
| **Rembrandt lighting** | Triangle of light on shadow side of face | Dramatic, intimate, serious |
| **Butterfly lighting** | Light directly above, creates butterfly shadow under nose | Beauty, elegance, flattering |
| **Split lighting** | Light on exactly half the face | Drama, mystery, duality |
| **Loop lighting** | Small shadow from nose to cheek, 30-45 degrees | Natural, approachable, editorial |
| **Broad lighting** | Lit side of face toward camera | Open, friendly, welcoming |
| **Short lighting** | Shadow side toward camera | Slimming, moody, contemplative |
| **Rim lighting** | Backlight creating edge glow around subject | Separation, drama, hero moment |
| **Three-point lighting** | Key + fill + back | Professional, broadcast, clean |

### Natural Light Keywords

| Keyword | Effect |
|---------|--------|
| **golden hour** | Warm, orange-tinged sidelight (sunrise/sunset) |
| **blue hour** | Cool, melancholic twilight |
| **overcast soft light** | Even, shadowless, flattering for all skin tones |
| **dappled light** | Light filtered through trees/leaves, natural |
| **window light** | Soft directional light, intimate indoor feeling |
| **harsh midday sun** | Strong shadows, gritty realism |
| **backlit** | Silhouette or halo effect, ethereal |
| **available light** | Whatever light exists, documentary authenticity |

### For Clara Specifically

Best lighting combinations for diverse skin tones:
- **Kodak Portra 400 + golden hour + Rembrandt lighting** = warm, dignified portraits
- **Overcast soft light + Fuji Pro 400H** = even, flattering for all skin tones
- **Window light + 85mm f/1.4** = intimate, documentary feel
- **Available light + Kodak Gold 200** = authentic everyday moments

---

## 6. Copy-Paste Prompt Templates for Clara

### TEMPLATE A: Documentary Portrait of an Immigrant

**For Midjourney V7:**
```
Editorial photograph of a 40-year-old Moroccan woman wearing a dusty rose hijab
and a simple wool coat, sitting in a municipal office waiting room in Madrid. She
is looking down at her smartphone screen with an expression of cautious hope, the
glow of the screen illuminating her face. Other people wait on plastic chairs in
the soft fluorescent background. Shot on Canon EOS R5, 85mm f/1.4, Kodak Portra
400 film emulation, shallow depth of field, available light from overhead
fluorescents mixed with window light, environmental portrait, documentary
photography style, natural skin texture with visible pores and subtle expression
lines, authentic and unstaged --ar 4:5 --style raw
```

**For FLUX:**
```
Documentary photograph of a 40-year-old Moroccan woman wearing a dusty rose hijab
and a simple wool coat, sitting in a municipal office waiting room in Madrid, Spain.
She looks at her smartphone with an expression of cautious hope, screen glow on her
face. Background: other people on plastic chairs, fluorescent lighting, government
posters on walls. Canon EOS R5, 85mm f/1.4 lens, Kodak Portra 400 color science,
shallow depth of field with bokeh background, natural skin texture with visible
pores, subtle expression lines around eyes, fine film grain, no retouching,
environmental portrait, documentary photography, photojournalistic, authentic
```

**For ChatGPT/GPT-4o:**
```
Create a photorealistic editorial photograph in documentary style. The subject is
a 40-year-old Moroccan woman wearing a dusty rose hijab and a simple wool coat.
She is sitting on a plastic chair in a municipal office waiting room in Madrid.
She is looking at her smartphone screen with cautious hope -- you can see the
screen glow illuminating her face softly. The background shows other people
waiting, fluorescent overhead lights, and government informational posters. The
photo should look like it was shot on a Canon EOS R5 with an 85mm f/1.4 lens,
using Kodak Portra 400 film. Shallow depth of field. Natural, imperfect skin
texture. Available light. The mood should be intimate and hopeful, like a
National Geographic documentary portrait. No retouching, no airbrushing.
```

---

### TEMPLATE B: Senegalese Man Using WhatsApp

**For Midjourney V7:**
```
Candid photograph of a 30-year-old Senegalese man with dark skin, short hair,
wearing a bright orange high-visibility construction vest over a grey hoodie,
sitting on a bench outside a building site during his lunch break. He is typing
on his phone with a slight smile, WhatsApp open on screen. Background shows
scaffolding and a Spanish city street. Shot on Sony A7 IV, 35mm f/1.4, Kodak
Portra 400, natural overcast daylight, documentary style, photojournalistic,
environmental portrait, natural skin texture, authentic --ar 3:2 --style raw
```

**For FLUX:**
```
Photojournalistic candid photograph. A 30-year-old Senegalese man with dark
skin and short hair sits on a metal bench outside a construction site during
lunch. He wears an orange high-visibility vest over a grey hoodie. He types on
his smartphone, slight smile, WhatsApp conversation visible on screen.
Background: scaffolding, Spanish city street, parked van with tools. Sony A7 IV,
35mm f/1.4, Kodak Portra 400, overcast daylight, documentary photography,
natural unretouched skin texture, imperfect details, fine grain, authentic moment
```

---

### TEMPLATE C: Hands-on-Phone Close-Up

**For Midjourney V7:**
```
Extreme close-up photograph of a woman's hands holding a smartphone, the screen
showing a WhatsApp conversation with a green chat bubble containing Spanish text
about "ayuda" and a friendly bot avatar. The hands have natural brown skin with
visible lines, short practical nails, a thin gold ring on one finger. Warm
golden afternoon light from a window. Shot on Canon EOS R5, 105mm f/2.8 macro,
Kodak Portra 160, ultra-shallow depth of field, sharp focus on hands and screen,
soft bokeh background of a kitchen table with a coffee cup --ar 4:5 --style raw
```

**For FLUX:**
```
Macro close-up photograph of brown-skinned woman's hands holding a smartphone.
Screen shows a WhatsApp conversation with green chat bubbles and a friendly
avatar icon. Hands have natural texture: visible lines, short nails, thin gold
ring. Warm window light from the left side. Kitchen table background with coffee
cup, out of focus. Canon EOS R5, 105mm f/2.8, Kodak Portra 160, ultra-shallow
depth of field, photorealistic, natural skin detail, fine grain texture
```

---

### TEMPLATE D: Before/After Transformation Scene

**For Midjourney V7 (generate each side separately, composite later):**

**BEFORE (confusion/overwhelm):**
```
Documentary photograph of a young Latin American woman in her late 20s sitting
alone at a kitchen table in a small apartment, surrounded by scattered official
Spanish government papers and envelopes. She rests her forehead on one hand,
looking overwhelmed and confused. The papers have official stamps and red text.
A basic phone sits face-down on the table. Dim overhead kitchen light, evening,
cluttered small apartment. Shot on Leica M11, 35mm f/1.4, Kodak Portra 800,
available light, documentary style, melancholic mood, natural skin, authentic
--ar 3:2 --style raw
```

**AFTER (relief/empowerment):**
```
Documentary photograph of the same young Latin American woman in her late 20s,
now sitting upright and smiling at her smartphone screen in the same small
apartment kitchen. The government papers are now organized in a neat folder. She
has a cup of tea beside her. Morning window light streams in warmly. She looks
relieved, confident, in control. Shot on Leica M11, 35mm f/1.4, Kodak Portra
400, warm window light, documentary style, hopeful mood, natural skin, authentic
--ar 3:2 --style raw
```

**For ChatGPT/GPT-4o (can do split-frame):**
```
Create a photorealistic before-and-after comparison in a single image, split
vertically down the middle with a thin white divider line.

LEFT SIDE (BEFORE): A young Latin American woman, late 20s, sits alone at a
small kitchen table looking overwhelmed. She rests her forehead on her hand.
Scattered official Spanish government papers surround her. Dim kitchen light,
evening. She looks stressed and lost. Desaturated, slightly cool color grading.

RIGHT SIDE (AFTER): The same woman, same kitchen, but now she sits upright and
smiles at her smartphone. Papers are organized in a folder. Morning sunlight
streams through a window. She looks relieved and empowered. Warm, golden color
grading.

Both sides should look like documentary photographs shot on Kodak Portra 400.
The transformation should feel emotionally powerful and authentic.
```

---

### TEMPLATE E: Community/Social Impact Scene

**For Midjourney V7:**
```
Documentary photograph of a diverse group of immigrants at a community center in
Barcelona. A Moroccan woman in a green hijab, a Senegalese man in a blue
sweater, a young Romanian woman, and an elderly Pakistani man sit around a table
with smartphones and papers, helping each other. One person points at a phone
screen while others lean in attentively. Community center setting with
fluorescent lights, informational posters on walls, plastic chairs and folding
tables. Shot on Nikon Z8, 24mm f/1.4, Kodak Gold 200, natural indoor light,
wide environmental group portrait, documentary style, warm and connected mood,
natural skin textures, candid moment --ar 16:9 --style raw
```

---

### TEMPLATE F: Product Hero Shot - Mobile App on Phone

**For Midjourney V7:**
```
Product photography of a modern smartphone displaying a WhatsApp-style chat
interface with a friendly AI assistant named Clara. The phone is held at a
slight angle on a clean white marble surface, with soft morning light from the
left creating gentle shadows. A coffee cup and a small plant are artfully placed
in the background, out of focus. The screen shows green chat bubbles with
Spanish text and a warm purple assistant avatar. Shot on Phase One IQ4, 80mm
f/2.8, clean studio lighting with soft fill, commercial product photography,
minimalist, premium feel --ar 4:5
```

**For FLUX:**
```
Commercial product photograph of a smartphone lying at a 15-degree angle on
white marble. Screen displays a WhatsApp-style chat interface with green user
bubbles and purple assistant bubbles labeled "Clara". Soft directional studio
light from upper left, subtle shadow beneath phone. Background: defocused
coffee cup and small succulent plant. Phase One IQ4, 80mm f/2.8, commercial
product photography, clean, modern, minimalist, sharp focus on screen, premium
brand aesthetic
```

---

### TEMPLATE G: Emotional Close-Up (Tears of Relief)

**For Midjourney V7:**
```
Intimate portrait photograph of a 50-year-old North African man with weathered
skin, short grey beard, and deep brown eyes, looking at his smartphone screen
with tears welling in his eyes and a trembling smile. His expression shows
profound relief -- he just received good news. He wears a simple collared shirt.
Background is a blurred park with trees. Shot on Sony A7 IV, 135mm f/2, Kodak
Portra 400, golden hour sidelight catching the moisture in his eyes, extreme
shallow depth of field, tight close-up crop from chest up, documentary
photography, raw emotion, natural skin with every wrinkle and pore visible,
no retouching, authentic --ar 4:5 --style raw
```

**For FLUX:**
```
Emotional close-up portrait photograph. A 50-year-old North African man with
weathered brown skin, short grey beard, deep brown eyes. He looks at his phone
screen, tears forming in his eyes, trembling relieved smile. Simple collared
shirt. Blurred park background with green trees. Sony A7 IV, 135mm f/2, Kodak
Portra 400, golden hour sidelight, shallow depth of field, tight crop from
chest up, visible tears catching the light, every wrinkle and pore visible,
documentary photography, raw authentic emotion, no airbrushing, no retouching
```

---

### TEMPLATE H: Woman Receiving Help at Government Office

**For Midjourney V7:**
```
Documentary photograph in a Spanish government office (oficina de extranjeria).
A 35-year-old Sub-Saharan African woman sits across from a civil servant at a
desk with a computer monitor and stacks of forms. She is showing her phone
screen to the civil servant, pointing at something on it. The civil servant
leans forward with interest. Both women have natural expressions of engagement.
Institutional interior with fluorescent lights, numbered ticket dispenser,
other people waiting in background. Shot on Fujifilm X-T5, 23mm f/2, Kodak
Portra 400, available fluorescent and window light, wide environmental
documentary photograph, candid, authentic --ar 16:9 --style raw
```

---

## 7. Video Prompt Engineering

### Veo 3.1 (Google) -- Best for Realistic People & Dialogue

**Prompt Formula:**
```
[Cinematography/Camera] + [Subject with traits] + [Action verb phrase] +
[Context: location, time, weather] + [Style & Ambiance] + [Audio cues]
```

**Optimal length:** 3-6 sentences, 100-150 words.

**Key rules:**
- Point the camera FIRST
- Use simple, concrete verbs
- Include audio descriptions (dialogue, ambient sounds)
- Specify duration (4s, 6s, or 8s) and aspect ratio

**Camera Movement Keywords for Veo 3.1:**
- `slow dolly in` -- gradual approach, builds intimacy
- `slow dolly out` -- reveals context, pulls away
- `tracking shot following subject` -- movement alongside subject
- `slow pan left/right` -- scanning a scene
- `crane shot ascending` -- dramatic reveal from low to high
- `static wide shot` -- stability, establishing context
- `handheld camera` -- documentary urgency, authenticity
- `POV shot` -- first-person perspective
- `over-the-shoulder shot` -- conversation framing
- `close-up with rack focus` -- shifting attention between elements

**Example Prompt for Clara (Veo 3.1):**
```
Medium close-up, slow dolly in; A 35-year-old Moroccan woman wearing a sage
hijab sits on a park bench in Madrid, golden afternoon light warming her face.
She looks at her smartphone, scrolling through a WhatsApp conversation. Her
expression shifts from uncertainty to a gentle, relieved smile as she reads a
message. She whispers to herself: "Lo entiendo ahora." Documentary style,
natural skin tones, Kodak Portra warmth. Audio: distant children playing in
the park, birds, a soft exhale of relief. Duration: 8s; AR: 9:16.
```

**Example Prompt -- Community Scene (Veo 3.1):**
```
Wide shot, slow pan right; Three immigrants -- a Senegalese man, a Moroccan
woman in hijab, and a young Latin American man -- sit at a community center
table. They lean toward a shared smartphone screen, pointing and discussing.
The Moroccan woman smiles and nods confidently. The Senegalese man gives a
thumbs up. Documentary style, available fluorescent light mixed with window
light, authentic body language. Audio: multilingual murmur in Spanish and
Arabic, chair scraping, distant laughter. Duration: 8s; AR: 16:9.
```

### Runway Gen-4 / Gen-4 Turbo -- Best for Character Consistency

**Key Advantage:** Reference image system maintains character appearance across different shots.

**Workflow:**
1. Generate a still portrait in Midjourney/FLUX first
2. Upload as character reference in Runway Gen-4
3. Write motion prompt describing what happens

**Prompt Structure:**
```
[Shot type and camera movement]. [Subject does action] in [setting].
[Lighting and mood]. [Specific motion details].
```

**Example Prompt (Runway Gen-4):**
```
Medium shot, slight handheld movement. A woman in a rose hijab walks through
a busy Spanish market, carrying a bag of groceries in one hand and checking
her phone in the other. She pauses, reads a message, and her face brightens
with a smile. Late afternoon natural light, golden tones, documentary feel.
Subtle crowd movement in background.
```

### Kling 3.0 -- Best for Multi-Shot Sequences

**Key Advantage:** Multi-shot storyboard system with up to 6 camera cuts in a single generation.

**Prompt Structure (Multi-Shot):**
```
Shot 1: [Wide establishing] -- [Description]
Shot 2: [Medium] -- [Description]
Shot 3: [Close-up] -- [Description]
```

**Example Prompt (Kling 3.0):**
```
Shot 1: Wide shot of a small Madrid apartment. A woman sits at a kitchen
table with papers spread around her, looking at her phone with worry.
Shot 2: Over-the-shoulder medium shot. Her phone screen shows a WhatsApp
conversation with "Clara" -- a new message appears with helpful information.
Shot 3: Close-up on her face as relief washes over her features. She closes
her eyes briefly and exhales. Warm kitchen light.
Documentary style, natural lighting, authentic emotion.
```

### Sora 2 (OpenAI) -- Best for Complex Narrative Scenes

**Key Advantage:** Up to 25 seconds, complex character interactions, narrative coherence.

**Example Prompt (Sora 2):**
```
A Moroccan woman in her 30s wearing a green hijab enters a Spanish government
office looking anxious. She approaches a counter, shows papers to a clerk.
The clerk frowns and shakes her head. The woman's face falls. She steps aside,
takes out her phone, and opens WhatsApp. She types a message and waits. A reply
appears. She reads it carefully, her expression changing from confusion to
understanding. She smiles, takes a breath, and confidently approaches the counter
again with new information. The clerk reviews it and nods approvingly. The woman
exhales with visible relief. Shot in documentary style, available office lighting,
handheld camera, natural and authentic performances.
```

---

## 8. Common Mistakes & How to Avoid Them

### What Makes AI Images Look Fake

| Problem | Cause | Solution |
|---------|-------|----------|
| **Overly smooth skin** | Default AI rendering removes imperfections | Add "natural skin texture, visible pores, subtle blemishes, imperfect skin, subsurface scattering" |
| **Weird/extra fingers** | Diffusion model limitation | Use Midjourney V7 (best hands); add "anatomically correct hands" to prompt; fix via inpainting |
| **Dead/glassy eyes** | Lack of eye detail specification | Add "natural catchlights in eyes, realistic iris detail, lively eyes, moist eyes" |
| **Too-perfect symmetry** | AI defaults to idealized faces | Add "slight facial asymmetry, natural and imperfect, candid expression" |
| **Plastic/waxy look** | Over-smoothing in generation | Use film stock references; add "matte skin, film grain, natural lighting imperfections" |
| **Uncanny teeth** | Difficulty rendering dental details | Add "natural teeth" or avoid open-mouth smiles; fix in post |
| **Over-saturated colors** | Default model tendency | Add "muted color palette, natural color grading, desaturated" |
| **"AI glow" / bloom** | Excessive highlight rendering | Add "no bloom, no glow, natural highlights, matte finish" |
| **Background incoherence** | Detail loss outside focal subject | Describe background specifically; use "coherent background, realistic environment" |
| **Clothing anomalies** | Fabric rendering issues | Describe clothing materials specifically: "cotton, wool, denim" not just "shirt" |
| **Too-clean environments** | AI defaults to pristine scenes | Add "lived-in, natural wear, slightly messy, realistic environment" |

### The "AI Tell" Checklist -- Signs of Artificial Generation

Before using any generated image, check for these:
1. Fingers/hands -- count them, check proportions
2. Ears -- symmetry, proper attachment
3. Background text -- usually garbled
4. Teeth -- often too perfect or malformed
5. Hair at edges -- sometimes melts into background
6. Skin around eyes -- can look painted
7. Fabric patterns -- may shift/warp illogically
8. Reflections -- often inconsistent with scene
9. Shadows -- direction may be inconsistent
10. Jewelry/accessories -- often melted or floating

---

## 9. Inclusive Representation Guidelines

### Principles for Ethical, Non-Stereotypical Representation

**DO:**
- Describe specific individuals, not categories ("a 35-year-old Moroccan woman with warm brown eyes and a thoughtful expression" NOT "an Arab woman")
- Show people in empowered, dignified positions (reading, learning, helping others, working)
- Include professional and everyday contexts (offices, kitchens, parks, transit)
- Specify clothing naturally and respectfully (specific colors and materials, not just "traditional dress")
- Show agency: people DOING things, making decisions, using technology
- Include environmental details that show integration (Spanish street signs, local shops)
- Vary ages, body types, and expressions within each community represented

**DO NOT:**
- Use only poverty or crisis imagery -- show full lives, not just struggles
- Rely on single visual markers to indicate ethnicity (avoid reducing identity to one clothing item)
- Over-exoticize or romanticize cultural dress
- Show people only as passive recipients of help
- Use "diverse" or "multicultural" as sole descriptors (be specific about who is in the scene)
- Group all people from a region into one visual stereotype
- Sexualize any subjects, especially women from specific cultural backgrounds

### Specific Prompting Tips for Diversity

Instead of: `"African immigrant"`
Use: `"A 28-year-old Senegalese man with dark brown skin, close-cropped hair, wearing a blue fleece jacket and jeans"`

Instead of: `"Muslim woman"`
Use: `"A 40-year-old Moroccan woman wearing a sage green cotton hijab and a warm brown wool coat, reading glasses pushed up on her head"`

Instead of: `"Hispanic immigrant"`
Use: `"A young Colombian woman in her early 20s with medium brown skin, long dark hair in a ponytail, wearing a university backpack and denim jacket"`

### Representing the Clara User Journey

Show the FULL emotional spectrum:
1. **Confusion** -- not helplessness. Show someone actively trying but facing bureaucratic complexity.
2. **Discovery** -- finding Clara, curiosity mixed with skepticism.
3. **Learning** -- engaging with information, asking follow-up questions.
4. **Relief** -- understanding what to do next.
5. **Empowerment** -- confidently taking action with new knowledge.
6. **Community** -- sharing knowledge, helping others.

---

## 10. Advanced Techniques & Workflows

### 10.1 Img2Img Workflow (Sketch to Photorealistic)

**Purpose:** Start with a rough composition sketch or low-quality image, then refine to photorealistic.

**Workflow:**
1. Create a rough sketch or wireframe of the scene (even hand-drawn)
2. Use img2img with denoising strength 0.55-0.65 for major transformation
3. Add detailed prompt with all photorealistic keywords
4. Iterate with lower denoising (0.3-0.4) to refine details
5. Final pass with denoising 0.15-0.25 for subtle refinement

**Settings:**
- Initial transformation: Denoising 0.55-0.65 (major change while keeping composition)
- Refinement: Denoising 0.30-0.45 (enhance details, keep structure)
- Polish: Denoising 0.10-0.25 (subtle texture and light improvement)

### 10.2 ControlNet for Consistent Characters

**Purpose:** Maintain the same person across multiple images (essential for before/after, storytelling).

**Workflow with OpenPose + IP-Adapter FaceID:**
1. Generate your "hero" character portrait in the best possible quality
2. Extract the face using IP-Adapter FaceID Plus v2
3. Use OpenPose ControlNet to define body pose for each new scene
4. Combine: IP-Adapter (face consistency) + OpenPose (pose control) + text prompt (scene)
5. Settings: IP-Adapter strength 0.6-0.8, ControlNet strength 0.7-0.9, CFG 5-9, 20-30 steps

**For Clara's use case:**
- Generate one "base" portrait of each character (Moroccan woman, Senegalese man, etc.)
- Use that as IP-Adapter reference for all subsequent scenes featuring that character
- This ensures the SAME person appears in before/after, in different settings, in community scenes

### 10.3 Midjourney Style References (--sref)

**Purpose:** Maintain consistent visual style across all images.

**Workflow:**
1. Find or generate one image with the EXACT visual style you want (color grading, mood, grain)
2. Use `--sref [URL]` in all subsequent prompts
3. This copies the style without copying the content
4. Combine with `--cref [URL]` for character reference consistency

**Example:**
```
Editorial photograph of a Moroccan woman in a Madrid metro station, documentary
style --sref https://example.com/your-style-reference.jpg --cref https://example.com/character-ref.jpg --ar 4:5 --style raw
```

### 10.4 Seed Management for Variations

**Purpose:** Generate slight variations of the same scene.

**In Midjourney:**
- Use `--seed [number]` to reproduce similar results
- React with the envelope emoji to get seed numbers from generated images
- Same seed + similar prompt = similar composition with variations

**In Stable Diffusion/FLUX:**
- Lock seed number and vary only small prompt elements
- Useful for generating multiple angles of the same scene

### 10.5 Inpainting for Fixing Problem Areas

**Purpose:** Fix hands, faces, eyes, or text without regenerating the entire image.

**Workflow:**
1. Generate your full image
2. Identify problem areas (usually hands, eyes, or background details)
3. Mask ONLY the problem area
4. Write a focused prompt for just that area (e.g., "natural human hand with five fingers, holding a smartphone, realistic skin texture")
5. Use denoising 0.4-0.6 for the inpainted area
6. Match lighting and color temperature to the rest of the image

**Priority inpainting areas for Clara images:**
- Hands holding phones (most common issue)
- Eyes (fix glassy/dead look)
- Phone screens (fix garbled text -- or composite real screenshots)
- Background text on signs (fix or remove)

### 10.6 Upscaling Workflows

**Purpose:** Take AI-generated images from 1024x1024 to print-ready resolution.

**Recommended Pipeline:**
1. **Generate** at native resolution (1024x1024 or 1536x1024)
2. **Upscale 2x** with Real-ESRGAN (preserves detail, removes artifacts)
3. **Upscale further** with SD img2img at denoising 0.15-0.25 (adds realistic detail)
4. **Final polish** with Topaz Gigapixel AI or Real-ESRGAN x4 for print

**Tool Recommendations:**
| Tool | Best For | Notes |
|------|----------|-------|
| Real-ESRGAN | General upscaling, open-source gold standard | Free, GPU-accelerated |
| Topaz Gigapixel AI | Maximum quality upscaling | Paid, best results |
| Topaz Photo AI | Combined denoising + upscaling | Paid, good for noisy images |
| SD Upscale (AUTOMATIC1111) | Adding detail during upscaling | Free, requires SD setup |
| Magnific AI | AI-powered "hallucinated" detail enhancement | Paid, impressive results |

**Production workflow for Clara:**
```
Generate (1024px) -> Real-ESRGAN 2x (2048px) -> SD img2img polish (2048px) -> Real-ESRGAN 4x (4096px)
```

### 10.7 Composite Workflow for Phone Screens

**Problem:** AI models cannot reliably render readable text on phone screens.

**Solution:**
1. Generate the image with a BLANK or GENERIC phone screen
2. Create actual Clara UI screenshots separately (from Figma or real app)
3. Use Photoshop/GIMP to composite the real screenshot onto the phone screen
4. Match perspective, add screen reflection/glare overlay
5. This produces the most realistic phone-in-hand shots

---

## 11. Recommended Tool Selection by Use Case

| Use Case | Best Tool | Runner-Up | Why |
|----------|-----------|-----------|-----|
| Portrait headshots | Midjourney V7 | FLUX 1.1 Pro | Best emotional quality, solved hand problem |
| Documentary scenes | FLUX 1.1 Pro | Midjourney V7 | DSLR-quality, technical precision |
| Product/app mockups | ChatGPT (GPT-4o) | FLUX | Good text rendering, iterative refinement |
| Before/after splits | ChatGPT (GPT-4o) | Midjourney (separate) | Can composite in single image |
| Community group shots | Midjourney V7 | Google Imagen 3 | Multi-person coherence |
| Emotional close-ups | Midjourney V7 | FLUX | Emotional lighting, mood |
| Video -- talking person | Veo 3.1 | Sora 2 | Best lip sync, body language |
| Video -- narrative scene | Sora 2 | Kling 3.0 | 25s duration, narrative coherence |
| Video -- multi-shot | Kling 3.0 | Runway Gen-4 | 6 camera cuts, consistent characters |
| Video -- character consistency | Runway Gen-4 | Kling 3.0 | Reference image system |
| Video -- product demo | Runway Gen-4 | Veo 3.1 | Clean, controlled output |

### Recommended Workflow for Clara's Visual Asset Production

**Phase 1: Character Design**
1. Generate 3-4 "base characters" in Midjourney V7 (diverse immigrant profiles)
2. Save seeds and use `--cref` for character consistency
3. Create high-quality reference portraits for each character

**Phase 2: Scene Generation**
1. Use FLUX for technical/product shots (app mockups, phone close-ups)
2. Use Midjourney for emotional/documentary scenes
3. Use ChatGPT for before/after comparisons and iterative complex scenes

**Phase 3: Video Production**
1. Use Midjourney base images as references for Runway Gen-4 video
2. Use Veo 3.1 for dialogue/emotional scenes
3. Use Kling 3.0 for multi-shot storytelling sequences

**Phase 4: Post-Production**
1. Inpaint any hand/face/eye artifacts
2. Composite real Clara UI onto phone screens
3. Upscale with Real-ESRGAN for print materials
4. Color grade for consistency across all assets

---

## Quick Reference: Realism Booster Keywords

Copy-paste these into ANY prompt to boost realism:

```
photorealistic, natural skin texture with visible pores, subtle skin imperfections,
realistic eye reflections, natural catchlights, fine film grain, Kodak Portra 400,
shot on Canon EOS R5, 85mm f/1.4, shallow depth of field, natural available light,
editorial photography, documentary style, unstaged, authentic, no retouching,
no airbrushing, RAW photograph
```

---

## Sources & Further Reading

- [AI Prompt Box - Midjourney Engineering Guide 2026](https://aipromptbox.in/blog/best-midjourney-prompts-engineering-guide-2026.html)
- [StockImg - Advanced Prompt Techniques for Hyper-Realistic Results](https://stockimg.ai/blog/prompts/advanced-prompt-techniques-getting-hyper-realistic-results-from-your-ai-photo-generator)
- [Creative Possible - The Cinematic AI Prompt Method: Cameras, Lenses & Film Stocks](https://creativepossible.substack.com/p/the-cinematic-ai-prompt-method-cameras)
- [DesignHero - 7 Prompts for Professional Realism (FLUX & Midjourney)](https://blog.designhero.tv/ai-art-direction-prompts-flux-midjourney/)
- [PXZ - 150+ Negative Prompts for Realistic AI Images](https://pxz.ai/blog/best-negative-prompts-for-realistic-ai-images)
- [ClickUp - 120+ Stable Diffusion Negative Prompts](https://clickup.com/blog/stable-diffusion-negative-prompts/)
- [Google Cloud - Ultimate Prompting Guide for Veo 3.1](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- [SkyWork - 26 Essential Veo 3.1 Prompt Patterns](https://skywork.ai/blog/veo-3-1-prompt-patterns-shot-lists-camera-moves-lighting-cues/)
- [Medium - How to Control Next-Gen Video AI: Runway, Kling, Veo, Sora](https://medium.com/@creativeaininja/how-to-actually-control-next-gen-video-ai-runway-kling-veo-and-sora-prompting-strategies-92ef0055658b)
- [NowadAIs - Master AI Character Consistency Guide 2026](https://www.nowadais.com/ai-character-consistency-guide-consistent-visual/)
- [SkyWork - Consistent Characters in AI Scenes (2025)](https://skywork.ai/blog/how-to-consistent-characters-ai-scenes-prompt-patterns-2025/)
- [Articulate - How to Create Inclusive AI Images](https://www.articulate.com/blog/how-to-create-inclusive-ai-images-a-guide-to-bias-free-prompting/)
- [Brookings - Diversity Failures in AI Image Generation](https://www.brookings.edu/articles/rendering-misrepresentation-diversity-failures-in-ai-image-generation/)
- [SkyWork - Product Mockup Prompts for Midjourney 2025](https://skywork.ai/blog/product-mockup-prompts-midjourney-2025/)
- [TrueFan - Master Cinematic AI Video Prompts 2026](https://www.truefan.ai/blogs/cinematic-ai-video-prompts-2026)
- [TeamDay - 15 AI Video Models Tested February 2026](https://www.teamday.ai/blog/best-ai-video-models-2026)
- [Tom's Guide - Midjourney vs Flux](https://www.tomsguide.com/ai/ai-image-video/midjourney-vs-flux-7-prompts-to-find-the-best-ai-image-model)
- [Promptaa - 7 Keywords to Make Images Less Fake Looking](https://promptaa.com/blog/prompt-key-words-to-make-images-less-fake-looking)
- [Let's Enhance - AI Image Upscalers 2026](https://letsenhance.io/blog/all/best-ai-image-upscalers/)
