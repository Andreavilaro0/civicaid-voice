# Clara Web App — Experiencia Completa de Impacto

> **For Claude:** Ejecuta este plan en **team agent mode**. Crea el equipo `clara-webapp` con los agentes definidos abajo. Usa superpowers:executing-plans para coordinar.

**Goal:** Crear una web app single-page que sea la MEJOR DEMO del hackathon: logo animado con filosofia "Tender Resonance", chat funcional con voz, narrativa de impacto integrada (la historia de Maria), y diseño WCAG AAA que transmita "tu voz tiene poder". NO es solo un chat — es una experiencia que hace llorar a los jueces.

**Architecture:** `presentacion/clara-webapp-live.html` autocontenido (HTML/CSS/JS inline), GSAP 3.12 CDN, Web Speech API, fetch() a `POST /api/chat`. Mobile-first (390px), accesible, multilingue (ES/FR/AR).

**Tech Stack:** HTML5, CSS3, GSAP 3.12 (CDN), Lottie (CDN), Web Speech API, Fetch API, Flask endpoint

---

## LECTURA OBLIGATORIA ANTES DE EMPEZAR

Cada agente DEBE leer los archivos relevantes a su rol:

| Archivo | Contenido | Para quien |
|---------|-----------|------------|
| `design/branding/clara-brand-book.html` | **FUENTE MAESTRA** — SVGs logo+personas, CSS warm shadows/grainy texture, narrativa completa, E-V-I visual, before/after | **TODOS** |
| `design/branding/colores/PALETA-CLARA.md` | Tokens de color, WCAG AAA | design-agent, frontend-agent |
| `design/branding/tipografia/TIPOGRAFIA-CLARA.md` | Escala tipografica, fonts | design-agent, frontend-agent |
| `design/branding/guia-de-marca/BRAND-GUIDE-CLARA.md` | Guia de marca completa | design-agent, narrative-agent |
| `design/branding/logo/CIVIC-RESONANCE-PHILOSOPHY.md` | Filosofia del logo ondas | design-agent |
| `design/branding/logo/clara-logo.svg` | SVG del logo (version simplificada) | frontend-agent |
| `clara-web/design/civic-tenderness-visual-philosophy.md` | Filosofia visual "Tender Resonance" | design-agent, frontend-agent |
| `clara-web/design/MARKETING-CONTENT-STRATEGY-REPORT.md` | Estrategia contenido, StoryBrand | narrative-agent |
| `docs/08-marketing/CLARA-TONE-VOICE-GUIDE.md` | Guia tono voz Clara, E-V-I | narrative-agent, frontend-agent |
| `docs/08-marketing/NARRATIVA-JUECES-FASE4.md` | Narrativa para jueces | narrative-agent |
| `clara-web/design/design-research-report.md` | Research UX, elderly, accesibilidad | design-agent |
| `src/core/prompts/templates.py` | Templates de Clara (tono) | frontend-agent |
| `data/cache/demo_cache.json` | Respuestas demo Clara | frontend-agent |
| `src/routes/api_chat.py` | Endpoint existente | integration-agent |

---

## EQUIPO

Crea equipo **`clara-webapp`** con estos agentes:

| Nombre | subagent_type | Skills | Responsabilidad |
|--------|---------------|--------|-----------------|
| `design-agent` | general-purpose | web-typography, refactoring-ui, frontend-design | T1-T2: Design system CSS completo, layout, animaciones, filosofia Tender Resonance |
| `frontend-agent` | general-purpose | senior-fullstack, react-best-practices | T3-T6: HTML/CSS/JS del webapp, chat funcional, voz, accesibilidad |
| `narrative-agent` | general-purpose | brand-voice, copywriting-classic, storytelling-storybrand | T7-T8: Contenido narrativo, historia de Maria, microcopy, textos de impacto |
| `integration-agent` | general-purpose | senior-fullstack, test-master | T9-T10: Endpoint API, tests, integracion backend, verificacion final |

**Dependencias:**
- T1-T2 (design-agent) y T7-T8 (narrative-agent) corren EN PARALELO
- T3-T6 (frontend-agent) esperan a que T1-T2 y T7-T8 terminen
- T9-T10 (integration-agent) esperan a que T3-T6 terminen

---

## PRE-CHECK

```bash
echo "=== PRE-CHECK ==="
PYTHONPATH=. python -m pytest tests/ -x -q --tb=no 2>&1 | tail -3
ruff check src/ tests/ --select E,F,W --ignore E501 2>&1 | tail -1
PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('BOOT OK')"
echo "=== PRE-CHECK DONE ==="
```

**ABORT si tests fallan o boot falla.**

---

## DESIGN SYSTEM TOKENS (Referencia Rapida)

```css
:root {
  /* Colors */
  --clara-blue: #1B5E7B;
  --clara-orange: #D46A1E;
  --clara-green: #2E7D4F;
  --clara-bg: #FAFAFA;
  --clara-card: #F5F5F5;
  --clara-bubble-clara: #E3F2FD;
  --clara-bubble-user: #1B5E7B;
  --clara-text-primary: #1A1A2E;
  --clara-text-secondary: #4A4A5A;
  --clara-border: #E0E0E0;
  --clara-error: #C62828;
  --clara-warning: #F9A825;

  /* Typography */
  --font-display: 'Atkinson Hyperlegible', sans-serif;
  --font-body: 'Inter', sans-serif;
  --fs-h1: 36px;
  --fs-h2: 28px;
  --fs-h3: 22px;
  --fs-body-lg: 20px;
  --fs-body: 18px;
  --fs-body-sm: 16px;
  --fs-button: 18px;
  --fs-caption: 14px;
  --lh-body: 1.6;
  --lh-heading: 1.2;

  /* Spacing */
  --radius-bubble: 16px;
  --radius-button: 16px;
  --radius-card: 16px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 40px;

  /* Shadows */
  --shadow-soft: 0 2px 12px rgba(27, 94, 123, 0.08);
  --shadow-float: 0 8px 32px rgba(27, 94, 123, 0.12);

  /* Brand Book warm shadows (replace flat borders) */
  --shadow-warm: 0 2px 20px rgba(27, 94, 123, 0.06), 0 0 0 1px rgba(224, 224, 224, 0.5);
  --shadow-warm-hover: 0 8px 30px rgba(27, 94, 123, 0.1), 0 0 0 1px rgba(224, 224, 224, 0.5);
}
```

---

## SVG ASSETS (Copiar directamente del Brand Book)

**FUENTE:** `design/branding/clara-brand-book.html` lineas 536-598

Incluir este bloque `<svg style="display:none">` al inicio del `<body>`. Contiene:

| Symbol ID | Que es | Donde usar |
|-----------|--------|------------|
| `#icon-blue` | Logo Clara (3 arcos azules + punto naranja) | Hero, favicon concept, header |
| `#icon-white` | Logo Clara variante blanca (para dark mode/fondos oscuros) | Dark mode hero, footer |
| `#persona-maria` | Retrato SVG ilustrado de Maria (58, Marruecos, fondo naranja, hijab) | Seccion impacto/personas |
| `#persona-ahmed` | Retrato SVG ilustrado de Ahmed (34, Senegal, fondo azul) | Seccion impacto/personas |
| `#persona-fatima` | Retrato SVG ilustrado de Fatima (42, Marruecos, fondo verde, hijab) | Seccion impacto/personas |

**Uso:** `<svg width="80" height="80"><use href="#icon-blue"/></svg>`

> **IMPORTANTE:** Estos SVGs son inline y production-ready. NO usar PNGs de personas/ — usar los SVG symbols del brand book que son mas ligeros y escalables.

---

## CSS PATTERNS DEL BRAND BOOK (Referencia para design-agent)

**Textura granular (2026 trend):**
```css
body::after {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none;
  z-index: 1000;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}
```

**Hero con resplandor calido:**
```css
.hero {
  background: radial-gradient(ellipse at 50% 60%, rgba(212,106,30,0.04) 0%, transparent 60%);
}
```

**Hover lift en cards:**
```css
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-warm-hover);
}
```

---

## T1: Design System CSS + Layout (design-agent)

**Leer primero:** clara-brand-book.html (FUENTE MAESTRA), PALETA-CLARA.md, TIPOGRAFIA-CLARA.md, civic-tenderness-visual-philosophy.md, design-research-report.md

**Output:** Bloque `<style>` completo para `presentacion/clara-webapp-live.html`

### Requisitos:

**Layout (mobile-first 390px):**
1. **Hero section** (pantalla completa): Logo SVG `<use href="#icon-blue"/>` centrado (120px), texto animado debajo, fondo con gradiente calido radial (ver CSS PATTERNS arriba)
2. **Impact strip** (post-animacion): Una frase de impacto con dato ("4.5 millones de personas vulnerables en Espana")
3. **Personas strip** (opcional, post-impact): 3 avatares SVG circulares (Maria/Ahmed/Fatima usando `#persona-maria`, etc.) con nombres y citas breves — muestra para QUIEN es Clara
4. **Chat section** (aparece tras hero): Burbujas Clara/usuario, scroll, max-width 480px centrado
5. **Input bar** (fija abajo): Campo texto + boton voz (56px, naranja pulsante) + boton enviar
6. **Footer** (sutil): "Hackathon OdiseIA4Good 2026 | Tu voz tiene poder"

**Filosofia visual Tender Resonance + Brand Book:**
- Formas organicas, radii 16-24px, CERO esquinas afiladas
- Espacio negativo generoso ("no te vamos a abrumar")
- Elementos flotan con gravedad natural, no grids rigidos
- Color como temperatura emocional: azul = confianza institucional, naranja = calidez humana
- Animacion de carga = circulo respirando a 60 BPM (1s ciclo)
- **Warm shadows** (del brand book): usar `--shadow-warm` en lugar de bordes planos
- **Textura granular** (del brand book): overlay sutil `body::after` con feTurbulence SVG noise
- **Hover lift** en cards/botones: `translateY(-2px)` + shadow intensificado
- **Blockquote estilo brand book**: border-left 4px naranja, fondo `#FFF8F0`, border-radius 0 8px 8px 0

**Responsive:**
```css
/* Mobile first (390px) */
/* Tablet (768px+): max-width 520px centrado */
/* Desktop (1024px+): max-width 480px, centrado con fondo difuminado */
```

**Dark mode:** Detectar `prefers-color-scheme: dark`, invertir backgrounds manteniendo AAA. Cambiar logo de `#icon-blue` a `#icon-white` (variante del brand book).

**Accesibilidad WCAG AAA:**
- Contraste 7:1 texto normal, 4.5:1 texto grande
- Touch targets 48px minimo (56px voz, 48px enviar)
- Focus outline 3px solid var(--clara-blue)
- `prefers-reduced-motion`: desactivar animaciones, mostrar todo instantaneo

---

## T2: Animaciones GSAP + Lottie (design-agent)

**Timeline de entrada (secuencia cinematografica):**

```
t=0.0s  Fondo: gradiente radial sutil aparece (opacity 0→1, 1.2s)
t=0.3s  Logo: scale 0.6→1, opacity 0→1 (0.8s, ease: back.out(1.7))
t=1.0s  Logo: empieza flotacion perpetua (y ±8px, 3s ciclo, ease: sine.inOut)
t=1.2s  Ondas del logo: pulsan en secuencia (opacity 35%→100%→35%, stagger 0.15s)
t=1.5s  Texto: "Hola, soy Clara" typewriter (0.04s/char, cursor parpadeante)
t=3.0s  Texto: fade a "Bonjour, je suis Clara" (crossfade 0.4s)
t=4.5s  Texto: fade a "مرحبا، أنا كلارا" (crossfade 0.4s, dir: RTL)
t=6.0s  Texto: fade a tagline "Tu voz tiene poder" (permanece, font-weight: bold)
t=6.5s  Impact strip: slide-up + counter animado "4.5M personas vulnerables"
t=7.0s  Personas strip: 3 chips con SVG avatares + citas (stagger 0.2s, fade-in + slide-up)
t=8.0s  Hero: slide-up suave, chat section aparece desde abajo
t=8.5s  Input bar: slide-up desde bottom
t=9.0s  Clara envia saludo automatico en chat (primera burbuja)
```

**Animacion de carga (mientras Clara "piensa"):**
- 3 circulos concentricos pulsando a ritmo cardiaco (1s ciclo)
- Color: var(--clara-blue) al 30% opacity
- Texto debajo: "Clara esta buscando esa informacion..."
- Transicion suave al aparecer burbuja de respuesta

**Animacion de grabacion de voz:**
- Boton mic: borde pulsa naranja→rojo, 1.5s ciclo
- Onda sonora animada dentro del boton (3 barras verticales oscilando)
- Contador de tiempo "0:03..." sutil

**prefers-reduced-motion:**
```javascript
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduced) { /* mostrar todo, skip timeline, solo transiciones opacity */ }
```

---

## T3: HTML estructura + Chat UI (frontend-agent)

**Leer primero:** Output de T1 (CSS), clara-brand-book.html (SVG symbols), templates.py, demo_cache.json

**Crear:** `presentacion/clara-webapp-live.html`

**Estructura HTML5:**
```html
<!DOCTYPE html>
<html lang="es" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#1B5E7B">
  <meta property="og:title" content="Clara — Tu voz tiene poder">
  <meta property="og:description" content="Asistente gratuito para tramites del gobierno espanol. Texto, voz, imagenes. ES/FR/AR.">
  <title>Clara — Tu voz tiene poder</title>
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <!-- GSAP -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>/* T1 output aqui */</style>
</head>
<body>
  <!-- SVG DEFS — copiar de clara-brand-book.html lineas 536-598 -->
  <svg xmlns="http://www.w3.org/2000/svg" style="display:none">
    <symbol id="icon-blue" viewBox="0 0 80 80"><!-- 3 arcos + punto naranja --></symbol>
    <symbol id="icon-white" viewBox="0 0 80 80"><!-- variante blanca --></symbol>
    <symbol id="persona-maria" viewBox="0 0 64 64"><!-- retrato ilustrado --></symbol>
    <symbol id="persona-ahmed" viewBox="0 0 64 64"><!-- retrato ilustrado --></symbol>
    <symbol id="persona-fatima" viewBox="0 0 64 64"><!-- retrato ilustrado --></symbol>
  </svg>

  <!-- HERO -->
  <section id="hero" class="hero" aria-label="Bienvenida">
    <svg class="hero-icon" width="120" height="120"><use href="#icon-blue"/></svg>
    <!-- Texto animado multilingue -->
    <!-- Impact counter -->
  </section>

  <!-- PERSONAS STRIP (opcional — muestra para QUIEN es Clara) -->
  <section id="personas" class="personas-strip" aria-label="Personas que Clara ayuda">
    <div class="persona-chip">
      <svg width="48" height="48"><use href="#persona-maria"/></svg>
      <span>"Solo quiero saber si tengo derecho a ver un medico."</span>
    </div>
    <div class="persona-chip">
      <svg width="48" height="48"><use href="#persona-ahmed"/></svg>
      <span>"Necesito algo que funcione de noche."</span>
    </div>
    <div class="persona-chip">
      <svg width="48" height="48"><use href="#persona-fatima"/></svg>
      <span>"No quiero molestar, pero mis hijos necesitan un medico."</span>
    </div>
  </section>

  <!-- CHAT -->
  <main id="chatArea" class="chat-area" role="log" aria-live="polite" aria-label="Conversacion con Clara">
    <!-- Burbujas se insertan via JS -->
  </main>

  <!-- INPUT -->
  <footer id="inputBar" class="input-bar" aria-label="Escribe o habla tu pregunta">
    <!-- Selector idioma (ES/FR/AR) -->
    <!-- Campo texto -->
    <!-- Boton voz (56px, naranja, aria-label) -->
    <!-- Boton enviar -->
  </footer>

  <script>/* T2 animaciones + T4 chat + T5 voz */</script>
</body>
</html>
```

**Burbujas de chat:**
- Clara (izquierda): fondo var(--clara-bubble-clara), border-radius 16px, con "tail" CSS apuntando izquierda
- Usuario (derecha): fondo var(--clara-bubble-user), texto blanco, tail derecha
- Timestamp sutil debajo (font-size 12px, color var(--clara-text-secondary))
- Una idea por burbuja, max-width 85%

**Selector de idioma:**
- 3 botones pill: ES (default activo), FR, AR
- Al cambiar: actualiza `<html lang>` y `dir` (AR = rtl), placeholder input, recognition.lang
- Transicion suave entre idiomas

---

## T4: Chat funcional — API integration (frontend-agent)

**Funcion sendMessage():**
```javascript
async function sendMessage(text) {
  if (!text.trim()) return;
  addBubble(text, 'user');
  inputEl.value = '';
  const loadingId = showLoading(); // circulos respirando

  try {
    const API_URL = location.hostname === 'localhost'
      ? 'http://localhost:5000/api/chat'
      : '/api/chat';
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, language: currentLang }),
    });
    const data = await res.json();
    removeLoading(loadingId);

    // Burbuja con animacion de entrada (slide-up 20px + fade)
    addBubble(
      data.response || 'No he podido procesar tu mensaje. Puedes intentar de nuevo, o llama al 060.',
      'clara'
    );
  } catch {
    removeLoading(loadingId);
    addBubble(
      'No he podido conectar con el servidor. Puedes intentar en unos segundos, o llama al 060.',
      'clara'
    );
  }
}
```

**Saludo automatico post-animacion (t=8.5s):**
```javascript
const GREETINGS = {
  es: 'Hola, soy Clara. Estoy aqui para ayudarte con tramites y ayudas del gobierno espanol.\n\nPuedo ayudarte con:\n— *Ingreso Minimo Vital* (ayuda economica)\n— *Empadronamiento* (registrarte en tu municipio)\n— *Tarjeta sanitaria* (acceso a sanidad publica)\n\nSobre que te gustaria saber?',
  fr: 'Bonjour, je suis Clara. Je suis la pour vous aider avec les demarches administratives en Espagne.\n\nJe peux vous aider avec:\n— *Revenu Minimum Vital* (aide economique)\n— *Inscription municipale* (enregistrement)\n— *Carte sanitaire* (acces sante publique)\n\nComment puis-je vous aider?',
  ar: 'مرحبا، أنا كلارا. أنا هنا لمساعدتك في الإجراءات الحكومية في إسبانيا.\n\nيمكنني مساعدتك في:\n— الحد الأدنى للدخل\n— التسجيل البلدي\n— البطاقة الصحية\n\nماذا تحتاج؟',
};
```

**Quick-reply chips (post-saludo):**
3 botones debajo del saludo de Clara para acelerar la demo:
- "Que es el IMV?" / "Qu'est-ce que le RMV?" / "ما هو الحد الأدنى للدخل؟"
- "Como me empadrono?" / "Comment s'inscrire?" / "كيف أسجل؟"
- "Tarjeta sanitaria" / "Carte sanitaire" / "البطاقة الصحية"

Al hacer click, se envia como mensaje del usuario.

---

## T5: Entrada por voz — Web Speech API (frontend-agent)

**Deteccion y configuracion:**
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const hasVoice = !!SpeechRecognition;
if (!hasVoice) voiceBtn.style.display = 'none';
```

**toggleVoice():**
- Tap para iniciar, tap para parar (NO mantener pulsado — diseño elderly-friendly)
- `recognition.lang` cambia con selector idioma (es-ES, fr-FR, ar-SA)
- `interimResults: true` — muestra transcripcion parcial en el input
- Al finalizar: envia automaticamente via sendMessage()

**Feedback visual durante grabacion:**
- Boton mic: borde pulsa naranja/rojo (CSS animation)
- Contador de tiempo "0:03" aparece junto al boton
- Input muestra transcripcion parcial en tiempo real (italic, color secondary)

**Error handling (tono Clara):**
- `no-speech`: no hacer nada (silencioso)
- Otros errores: "No he podido escucharte. Puedes intentar de nuevo, o si prefieres, escribe tu pregunta."

---

## T6: Accesibilidad + Responsive final (frontend-agent)

**Checklist WCAG AAA:**
- [ ] `role="log"` + `aria-live="polite"` en chat
- [ ] Todos los botones: `aria-label` descriptivo
- [ ] Focus visible: outline 3px solid var(--clara-blue) con offset 2px
- [ ] Tab order: lang selector → chat → input → voice → send
- [ ] `<html lang="es">` cambia dinamicamente con selector
- [ ] `<html dir="rtl">` cuando AR seleccionado
- [ ] Contraste 7:1 verificado en TODAS las combinaciones
- [ ] Touch targets: 48px minimo, 56px voz
- [ ] `prefers-reduced-motion` desactiva GSAP timeline
- [ ] `prefers-color-scheme: dark` activa modo oscuro
- [ ] Zoom 200% no rompe layout
- [ ] Screen reader: burbujas anuncian "Clara dice:" o "Tu dijiste:"

**Responsive:**
```css
@media (min-width: 768px) { .container { max-width: 520px; margin: 0 auto; } }
@media (min-width: 1024px) { body { background: linear-gradient(135deg, #f0f4f8, #fafafa); } .container { max-width: 480px; } }
```

---

## T7: Contenido narrativo — La Historia de Maria + Barreras (narrative-agent)

**Leer primero:** clara-brand-book.html (FUENTE MAESTRA — seccion "Historia", "Filosofia", "Voz Primero"), CLARA-TONE-VOICE-GUIDE.md, MARKETING-CONTENT-STRATEGY-REPORT.md, NARRATIVA-JUECES-FASE4.md

**Output:** Textos para integrar en el HTML.

### 7a: Impact strip (aparece en hero, t=6.5s)

Texto que aparece con counter animado:
```
"4.5 millones de personas vulnerables en Espana no acceden a ayudas por barreras de idioma y burocracia."
```

### 7b: Personas strip (aparece en hero, t=7.0s — usa SVG portraits)

3 chips horizontales con avatar SVG + cita real del brand book:
- **Maria (58, Marruecos):** "Solo quiero saber si tengo derecho a ver un medico."
- **Ahmed (34, Senegal):** "Necesito algo que funcione de noche."
- **Fatima (42, Marruecos):** "No quiero molestar, pero mis hijos necesitan un medico."

> Estas citas vienen directamente del brand book seccion "Personas". Usar las SVG personas `#persona-maria`, `#persona-ahmed`, `#persona-fatima` como avatares.

### 7c: Before/After comparison (aparece debajo de personas o como modal "Ver impacto")

Formato del brand book seccion "Voz Primero" — grid 2 columnas naranja/verde:

| Antes (naranja) | Con Clara (verde) |
|-----------------|------------------|
| "Un formulario de 4 paginas en espanol juridico" | "Tienes pasaporte y contrato? Entonces puedes empadronarte." |
| "Acreditar residencia efectiva mediante certificado de convivencia" | "Necesitas demostrar que vives ahi. Puede ser un recibo de luz." |
| "Llamar al 010, esperar 40 min, no entender la respuesta" | "Un audio de 30 segundos en tu idioma, a cualquier hora" |

### 7d: Microcopy de la interfaz

| Elemento | ES | FR | AR |
|----------|----|----|-----|
| Placeholder input | "Escribe tu pregunta o habla..." | "Ecrivez ou parlez..." | "...اكتب أو تحدث" |
| Boton voz label | "Hablar con Clara" | "Parler a Clara" | "تحدث مع كلارا" |
| Boton enviar label | "Enviar" | "Envoyer" | "إرسال" |
| Loading | "Clara esta buscando..." | "Clara cherche..." | "...كلارا تبحث" |
| Error conexion | "No he podido conectar. Puedes intentar en unos segundos, o llama al 060." | "Je n'ai pas pu me connecter. Reessayez ou appelez le 060." | "لم أستطع الاتصال. حاول مرة أخرى أو اتصل بـ 060." |

### 7e: Footer inspiracional

```
"Clara es un bien publico digital. Codigo abierto, informacion verificada, cero costo."
"Hackathon OdiseIA4Good 2026 — UDIT Madrid"
```

### 7f: Estadisticas (del brand book — para impact section o footer)

| Stat | Valor | Label |
|------|-------|-------|
| CCAA cubiertas | 17 | Comunidades autonomas |
| Idiomas | 3+ | Idiomas soportados |
| Tramites | 8 | En la base de conocimiento |
| Respuesta | <3s | Tiempo de respuesta |

### 7g: Demo script para jueces (5 preguntas que impresionan)

Secuencia de preguntas para la demo en vivo:
1. **"Que es el IMV?"** → Clara responde con empatia + pasos claros (patron E-V-I visible)
2. **Cambiar a FR → "Comment s'inscrire a la mairie?"** → Clara responde en frances
3. **Enviar nota de voz en espanol** → Transcripcion + respuesta
4. **"Tengo una carta que no entiendo"** → Clara pide la foto (vision flow)
5. **"Gracias Clara"** → Cierre calido: "Mucho animo con tu tramite"

---

## T8: OG Tags + SEO + Social Sharing (narrative-agent)

```html
<!-- Open Graph -->
<meta property="og:title" content="Clara — Tu voz tiene poder">
<meta property="og:description" content="Asistente gratuito WhatsApp para tramites en Espana. Texto, voz, imagenes. Espanol, frances, arabe.">
<meta property="og:type" content="website">
<meta property="og:image" content="presentacion/images/cover.png">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Clara — Tu voz tiene poder">
<meta name="twitter:description" content="4.5M personas vulnerables. Una asistente que habla su idioma.">
```

---

## T9: Verificar endpoint API + Tests (integration-agent)

**Step 1: Verificar que `src/routes/api_chat.py` existe y funciona**

Leer el archivo. Si ya existe y tiene POST /api/chat con CORS, SKIP. Si no existe o falta CORS, crear/arreglar.

**Step 2: Escribir tests**

```python
# tests/unit/test_api_chat_webapp.py
def test_api_chat_returns_json():
    """POST /api/chat with valid message returns JSON response."""

def test_api_chat_cors_headers():
    """Response includes Access-Control-Allow-Origin."""

def test_api_chat_empty_message_400():
    """POST /api/chat with empty message returns 400."""

def test_api_chat_options_preflight():
    """OPTIONS /api/chat returns CORS preflight headers."""
```

**Step 3: Ejecutar tests**
```bash
PYTHONPATH=. python -m pytest tests/unit/test_api_chat_webapp.py -v --tb=short
```

---

## T10: Verificacion final + Commit (integration-agent)

### Gates de verificacion:

| Gate | Comando | Esperado |
|------|---------|----------|
| G1 | `python -m pytest tests/ -x -q --tb=no \| tail -3` | 568+ passed, 0 failed |
| G2 | `ruff check src/ tests/ --select E,F,W --ignore E501` | All checks passed |
| G3 | `PYTHONPATH=. python -c "from src.app import create_app; app = create_app(); print('OK')"` | OK |
| G4 | Verificar `clara-webapp-live.html` existe y tiene >200 lineas | Existe |
| G5 | Verificar HTML tiene `role="log"` y `aria-live="polite"` | Presente |
| G6 | Verificar HTML tiene `prefers-reduced-motion` | Presente |
| G7 | Verificar HTML tiene GSAP CDN script tag | Presente |
| G8 | Verificar HTML tiene `lang="es"` en html tag | Presente |
| G9 | Verificar HTML tiene `og:title` meta tag | Presente |

### Commits (en orden):

```bash
# Si se modifico api_chat.py o app.py
git add src/routes/api_chat.py src/app.py tests/unit/test_api_chat_webapp.py
git commit -m "feat: add/update /api/chat endpoint for webapp integration"

# El webapp
git add presentacion/clara-webapp-live.html
git commit -m "feat: add clara-webapp-live — animated landing + chat + voice + impact narrative

- Tender Resonance design: organic forms, breathing animations, WCAG AAA
- GSAP entrance sequence: logo float, multilingual typewriter, impact counter
- Functional chat connected to /api/chat with quick-reply chips
- Web Speech API voice input (tap-to-start, elderly-friendly)
- Trilingual support: ES, FR, AR (with RTL)
- Impact strip: 4.5M stat with counter animation
- Dark mode + reduced-motion support
- Mobile-first responsive (390px → 768px → 1024px)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Resumen

| Fase | Agente | Tasks | Paralelo |
|------|--------|-------|----------|
| 1 | design-agent | T1-T2: CSS system + animaciones | SI (con narrative) |
| 1 | narrative-agent | T7-T8: Contenido + OG tags | SI (con design) |
| 2 | frontend-agent | T3-T6: HTML + chat + voz + a11y | Espera Fase 1 |
| 3 | integration-agent | T9-T10: Tests + gates + commit | Espera Fase 2 |

**Total: 10 tasks, 4 agentes, 3 fases**

## Criterios de Exito

- [ ] Logo SVG inline (`#icon-blue`) flota con ondas pulsando (filosofia Tender Resonance)
- [ ] Secuencia multilingue typewriter (ES → FR → AR → tagline)
- [ ] Counter animado "4.5M personas vulnerables"
- [ ] **Personas strip**: 3 SVG avatares (Maria/Ahmed/Fatima) con citas reales del brand book
- [ ] **Before/After**: comparacion visual naranja/verde del impacto de Clara
- [ ] Chat funcional: enviar pregunta → recibir respuesta de Clara
- [ ] Voz funcional: tap mic → hablar → transcripcion → respuesta
- [ ] Quick-reply chips aceleran la demo
- [ ] 3 idiomas con cambio fluido (incluyendo RTL para arabe)
- [ ] Dark mode automatico (logo cambia a `#icon-white`)
- [ ] **Brand book CSS**: warm shadows, textura granular sutil, hover lift, hero radial glow
- [ ] WCAG AAA (contraste, focus, aria, reduced-motion)
- [ ] Mobile-first, se ve perfecto en 390px
- [ ] Tests pasan (568+)
- [ ] Un juez que lo vea dice "wow"
