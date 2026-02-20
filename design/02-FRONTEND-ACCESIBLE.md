# Frontend Accesible & Mockups — Clara

> **Fecha:** 19 Feb 2026
> **Enfoque:** WCAG 2.1 AAA, usuarios vulnerables, elderly-first

---

## 1. Checklist WCAG 2.1 AAA para Clara

### Contraste y Color
- [ ] Ratio 7:1 para texto normal sobre fondo
- [ ] Ratio 4.5:1 para texto grande (24px+)
- [ ] Nunca usar color como unica forma de transmitir info
- [ ] Modo alto contraste disponible como toggle

### Navegacion y Teclado
- [ ] Todos los elementos interactivos accesibles con Tab
- [ ] Indicadores de foco visibles (outline 3px azul)
- [ ] Orden de tabulacion logico (arriba-abajo, izquierda-derecha)
- [ ] Sin trampas de teclado

### Lectores de Pantalla
- [ ] Todos los botones con aria-label descriptivo
- [ ] Imagenes con alt text significativo
- [ ] Regiones ARIA (main, nav, complementary)
- [ ] Anuncios dinamicos con aria-live para mensajes nuevos

### Movimiento y Animaciones
- [ ] Respetar `prefers-reduced-motion`
- [ ] Sin contenido que parpadee >3 veces/segundo
- [ ] Animaciones opcionales, no esenciales para la funcion

### Targets Tactiles
- [ ] Minimo 44x44px para todos los botones (AAA)
- [ ] Recomendado 64x64px para botones principales (elderly)
- [ ] Espacio minimo 8px entre targets adyacentes

---

## 2. Librerias UI Recomendadas

| Libreria | Accesibilidad | Pros | Contras | Recomendacion |
|---|---|---|---|---|
| **Radix UI** | Excelente (ARIA built-in) | Headless, flexible, ligero | Requiere styling propio | Ideal para app custom |
| **Chakra UI** | Muy buena | Temas, responsive, facil | Bundle mas grande | Buena para MVP rapido |
| **Shadcn/ui** | Muy buena (usa Radix) | Copy-paste, Tailwind | Requiere Tailwind setup | Mejor balance calidad/velocidad |
| **Gradio** (actual) | Limitada | Ya implementado | Poca customizacion visual | OK para demo, migrar despues |

**Recomendacion para hackathon:** Mantener Gradio para la demo web (ya funciona). Para materiales de marketing y el futuro, disenar mockups con el sistema visual de Clara usando Figma/Canva.

---

## 3. Pantallas Clave — Wireframes

### 3A. Pantalla de Bienvenida

```
┌──────────────────────────────────┐
│                                  │
│         [Logo Clara]             │
│                                  │
│     "Tu voz tiene poder"         │
│                                  │
│  ┌────────────────────────────┐  │
│  │                            │  │
│  │   Te ayudo con tramites    │  │
│  │   sociales en Espana.      │  │
│  │   Habla o escribe en       │  │
│  │   tu idioma.               │  │
│  │                            │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────┐  ┌────────────────┐  │
│  │ ES     │  │ Francais  FR  │  │
│  │Espanol │  │               │  │
│  └────────┘  └────────────────┘  │
│                                  │
│  ┌────────────────────────────┐  │
│  │                            │  │
│  │      EMPEZAR A HABLAR      │  │
│  │          [🎤 mic]          │  │
│  │                            │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────────────────────────┐  │
│  │   Prefiero escribir  [⌨]  │  │
│  └────────────────────────────┘  │
│                                  │
└──────────────────────────────────┘
```

**Especificaciones:**
- Logo: 120px ancho centrado
- Tagline: 28px Atkinson Hyperlegible Bold
- Descripcion: 20px Inter Regular, max 3 lineas
- Selector idioma: botones 64x48px con texto + abreviatura
- Boton "Empezar": 100% ancho, 72px alto, azul `#1B5E7B`, texto blanco 22px
- Boton "Escribir": 100% ancho, 56px alto, borde gris, texto 18px

### 3B. Interfaz de Chat

```
┌──────────────────────────────────┐
│  [←]  Clara          [ES ▾] [⚙] │
├──────────────────────────────────┤
│                                  │
│  ┌─────────────────────────┐     │
│  │ Hola, soy Clara.       │     │
│  │ En que puedo ayudarte?  │     │
│  │                         │     │
│  │ Puedo informarte sobre: │     │
│  │ • Ingreso Minimo Vital  │     │
│  │ • Empadronamiento       │     │
│  │ • Tarjeta sanitaria     │     │
│  └─────────────────────────┘     │
│                                  │
│         ┌─────────────────────┐  │
│         │ Que es el IMV?      │  │
│         └─────────────────────┘  │
│                                  │
│  ┌─────────────────────────┐     │
│  │ El Ingreso Minimo Vital │     │
│  │ es una ayuda mensual... │     │
│  │                         │     │
│  │ [▶ Escuchar respuesta]  │     │
│  │                         │     │
│  │ Fuente: seg-social.es   │     │
│  └─────────────────────────┘     │
│                                  │
│  ┌────────────────────────────┐  │
│  │ Escribe tu pregunta...    │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────┐ ┌────────┐ ┌──────┐ │
│  │  [⌨]  │ │  [🎤]  │ │ [📷] │ │
│  │Escribir│ │  Voz   │ │ Foto │ │
│  └────────┘ └────────┘ └──────┘ │
└──────────────────────────────────┘
```

**Especificaciones:**
- Header: 56px alto, azul oscuro
- Burbujas Clara: fondo `#E3F2FD`, borde-radius 16px, padding 16px, max-width 85%
- Burbujas usuario: fondo `#1B5E7B`, texto blanco, alineado derecha
- Boton audio: verde `#2E7D4F`, icono play 24px, texto "Escuchar respuesta" 16px
- Input: 56px alto, borde 2px `#E0E0E0`, font 18px
- 3 botones inferiores: cada uno 64x64px, icono 28px + label 14px debajo

### 3C. Grabacion de Voz

```
┌──────────────────────────────────┐
│                                  │
│                                  │
│         Habla ahora...           │
│                                  │
│     ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋          │
│     (onda de audio animada)      │
│                                  │
│           ⏱ 0:05                 │
│                                  │
│         ┌──────────┐             │
│         │          │             │
│         │   [🎤]   │             │
│         │  GRANDE  │             │
│         │  96x96   │             │
│         │          │             │
│         └──────────┘             │
│        (pulsando = rojo)         │
│                                  │
│  ┌────────────┐ ┌─────────────┐  │
│  │  Cancelar  │ │   Enviar    │  │
│  │    [✕]     │ │    [→]      │  │
│  └────────────┘ └─────────────┘  │
│                                  │
└──────────────────────────────────┘
```

**Especificaciones:**
- Texto "Habla ahora": 28px, centro
- Onda audio: CSS animation, 4px lineas, naranja `#D46A1E`
- Timer: 24px monospace
- Boton microfono: 96x96px circular, rojo `#C62828` mientras graba, pulse animation
- Botones Cancelar/Enviar: 64px alto, 45% ancho cada uno

### 3D. Subida de Documento

```
┌──────────────────────────────────┐
│  [←]  Subir documento            │
├──────────────────────────────────┤
│                                  │
│  ┌────────────────────────────┐  │
│  │                            │  │
│  │    Sube una foto de tu     │  │
│  │    documento o carta       │  │
│  │                            │  │
│  │    Clara te explicara      │  │
│  │    que dice                │  │
│  │                            │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────────────────────────┐  │
│  │                            │  │
│  │                            │  │
│  │        [📷 grande]         │  │
│  │                            │  │
│  │   Toca para hacer foto     │  │
│  │                            │  │
│  │                            │  │
│  └────────────────────────────┘  │
│        (zona de drop tambien)    │
│                                  │
│  ┌────────────────────────────┐  │
│  │  O elige de tu galeria [📁]│  │
│  └────────────────────────────┘  │
│                                  │
└──────────────────────────────────┘
```

### 3E. Respuesta con Audio

```
┌──────────────────────────────────┐
│                                  │
│  ┌─────────────────────────┐     │
│  │ Clara                   │     │
│  │                         │     │
│  │ He analizado tu         │     │
│  │ documento. Es una       │     │
│  │ comunicacion de la      │     │
│  │ Seguridad Social...     │     │
│  │                         │     │
│  │ ┌───────────────────┐   │     │
│  │ │ [▶] ━━━━━○━━━ 1:23│   │     │
│  │ │ Escuchar respuesta │   │     │
│  │ └───────────────────┘   │     │
│  │                         │     │
│  │ Fuente: seg-social.es   │     │
│  │ Tel: 900 16 65 65       │     │
│  │                         │     │
│  │ ┌─────────┐┌─────────┐ │     │
│  │ │   👍    ││   👎    │ │     │
│  │ │  Util   ││Mejorable│ │     │
│  │ └─────────┘└─────────┘ │     │
│  └─────────────────────────┘     │
│                                  │
│  ┌────────────────────────────┐  │
│  │  Preguntar otra cosa  [+] │  │
│  └────────────────────────────┘  │
│                                  │
└──────────────────────────────────┘
```

---

## 4. Patrones de Interaccion

### Grabacion de Voz
- **Mecanismo:** Toggle (un toque para empezar, otro para parar) — NO press-and-hold (dificil para mayores con problemas de destreza)
- **Feedback visual:** Boton cambia a rojo + onda de audio + timer
- **Feedback auditivo:** Beep corto al empezar y al parar
- **Limite:** 60 segundos maximo, aviso a los 50s

### Reproduccion de Audio
- **Boton play:** 48x48px minimo, icono triangulo claro
- **Barra de progreso:** Visible, con tiempo transcurrido/total
- **Velocidad:** Control 0.75x / 1x / 1.25x (mayores prefieren mas lento)
- **Auto-play:** NO. Siempre manual

### Estados de Carga
- **Procesando audio:** "Clara esta escuchando tu mensaje..." + animacion de ondas
- **Generando respuesta:** "Clara esta buscando informacion..." + spinner suave
- **Analizando documento:** "Clara esta leyendo tu documento..." + animacion de escaneo
- **Timeout (>15s):** "Esta tardando un poco mas de lo normal. Un momento..."

### Estados de Error
- **No entendio:** "Perdona, no he entendido bien. Puedes repetirmelo?"
- **Sin conexion:** "Parece que no hay conexion. Revisa tu wifi o datos moviles"
- **Servicio caido:** "Clara no esta disponible ahora. Intenta en unos minutos"
- **Todos con:** icono + mensaje + accion sugerida

---

## 5. Herramientas de Testing de Accesibilidad

| Herramienta | Tipo | Que testea | Gratuita |
|---|---|---|---|
| **WebAIM Contrast Checker** | Web | Ratios de contraste | Si |
| **axe DevTools** | Extension Chrome | WCAG automatizado | Si (basico) |
| **Lighthouse** | Chrome DevTools | Performance + Accesibilidad | Si |
| **WAVE** | Extension Chrome | Errores WCAG visuales | Si |
| **NVDA** | Desktop (Windows) | Screen reader | Si |
| **VoiceOver** | macOS/iOS built-in | Screen reader | Si |
| **Hemingway Editor** | Web | Nivel de lectura del texto | Si |

---

## Fuentes

- [WCAG 2.2 Target Size — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- [GOV.UK Design System](https://design-system.service.gov.uk/)
- [Chatbot UX Best Practices 2026 — Groto](https://www.letsgroto.com/blog/ux-best-practices-for-ai-chatbots)
- [WhatsApp Bot Design — Landbot](https://landbot.io/blog/design-whatsapp-bot-dialogue)
- [Material Design 3 Accessibility](https://m3.material.io/foundations/designing/structure)
- [Civic Design Systems — MaxiomTech](https://www.maxiomtech.com/accessible-ux-civic-design-systems/)
- [Decidim Barcelona](https://decidim.org/)

---

*Documento generado el 19 de febrero de 2026.*
