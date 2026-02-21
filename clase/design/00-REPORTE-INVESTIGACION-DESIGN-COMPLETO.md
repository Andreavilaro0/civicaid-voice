# REPORTE COMPLETO DE INVESTIGACION — Capa de Diseno Clara

> **Fecha:** 19 Feb 2026
> **Proyecto:** CivicAid Voice / Clara — Asistente WhatsApp para poblaciones vulnerables en Espana
> **Hackathon:** OdiseIA4Good 2026 — UDIT (23-25 Feb 2026)
> **Objetivo:** Investigacion exhaustiva sobre marca, frontend accesible, publicidad, mockups, videos y tendencias de diseno con enfoque en accesibilidad e impacto social

---

## INDICE

1. [Estrategia de Marca](#1-estrategia-de-marca)
2. [Paleta de Colores y Tipografia Accesible](#2-paleta-de-colores-y-tipografia-accesible)
3. [Frontend Accesible — WCAG 2.1 AAA](#3-frontend-accesible)
4. [Librerias UI y Tecnologias Recomendadas](#4-librerias-ui-y-tecnologias)
5. [Wireframes y Mockups](#5-wireframes-y-mockups)
6. [Patrones de Interaccion](#6-patrones-de-interaccion)
7. [Marketing y Publicidad de Impacto Social](#7-marketing-y-publicidad)
8. [Estrategia de Video y Prompts IA](#8-estrategia-de-video)
9. [Pitch Deck y Materiales Fisicos](#9-pitch-deck-y-materiales)
10. [Tendencias de Diseno 2025-2026](#10-tendencias-de-diseno)
11. [Diseno Civico y Referencias](#11-diseno-civico)
12. [Diseno Inclusivo Multicultural](#12-diseno-inclusivo)
13. [Herramientas Gratuitas](#13-herramientas)
14. [Fuentes Bibliograficas](#14-fuentes)

---

## 1. Estrategia de Marca

### 1.1 Identidad y Nombre

| Aspecto | Detalle |
|---|---|
| **Etimologia** | Del latin "clarus" — claro, brillante, luminoso |
| **Connotaciones** | Claridad, transparencia, luz, simplicidad, honestidad |
| **Fonetica** | Facil de pronunciar en espanol, frances, arabe e ingles |
| **Genero** | Femenino — evoca cercania, cuidado, confianza (respaldado por estudios UX de chatbots) |
| **Memorabilidad** | 5 letras, 2 silabas, universal |

### 1.2 Tagline

| # | Tagline | Idioma | Enfoque |
|---|---|---|---|
| 1 | **"Tu voz tiene poder"** | ES | Empoderamiento, accesibilidad por voz |
| 2 | "Tus derechos, en tu idioma" | ES | Multilingue, derechos sociales |
| 3 | "La voz que te acompana" | ES | Companerismo |
| 4 | "Votre voix, vos droits" | FR | Version francesa |
| 5 | "Porque entender no deberia ser un privilegio" | ES | Impacto social |

**Recomendacion:** "Tu voz tiene poder" como tagline principal.

### 1.3 Personalidad de Marca

| Rasgo | Descripcion | Lo que NO es |
|---|---|---|
| **Cercana** | Habla como una vecina que sabe del tema | No es burocrata |
| **Paciente** | Nunca se frustra, repite sin problema | No es condescendiente |
| **Clara** | Lenguaje simple, pasos concretos | No usa jerga burocratica |
| **Respetuosa** | Trata al usuario como adulto capaz | No infantiliza |
| **Proactiva** | Sugiere ayudas sin que se lo pidan | No es pasiva |
| **Multicultural** | Usa analogias del pais de origen | No asume una sola cultura |

### 1.4 Guia de Tono de Voz

| Situacion | Tono | Ejemplo |
|---|---|---|
| **Saludo** | Calido, acogedor | "Hola, soy Clara. Estoy aqui para ayudarte con tramites en Espana. Puedes hablarme o escribirme en tu idioma." |
| **Explicando proceso** | Claro, paso a paso | "Para pedir el IMV necesitas: 1) Estar empadronado. 2) Tener ingresos bajos. 3) Rellenar un formulario. Te explico cada paso?" |
| **Error** | Amable, sin culpa | "Perdona, no he entendido bien. Puedes repetirmelo con otras palabras?" |
| **Sugerencia proactiva** | Util, no invasiva | "Segun lo que me cuentas, podrias tener derecho al bono social electrico. Quieres que te explique?" |
| **Despedida** | Calida, puerta abierta | "Espero haberte ayudado. Si necesitas algo mas, aqui estoy. Mucho animo." |

### 1.5 Diseno Emocional

| Emocion Objetivo | Como se Logra |
|---|---|
| **Seguridad** | Lenguaje simple, sin jerga. Fuentes oficiales citadas. Nunca inventa datos |
| **Comprendido** | Detecta idioma automaticamente. Usa analogias culturales. Responde en su idioma |
| **Capaz** | Clara da herramientas, no caridad. "Puedes hacerlo, te explico como" |
| **No juzgado** | Nunca pregunta por estatus legal. No asume nivel educativo. Tono neutro y respetuoso |
| **Acompanado** | "Estoy aqui para ayudarte". Puerta siempre abierta. Sin presion de tiempo |

---

## 2. Paleta de Colores y Tipografia Accesible

### 2.1 Paleta Primaria (WCAG AAA)

**Criterios:** Ratio 7:1 para texto normal, seguro para daltonismo, psicologia del color (confianza + calidez), culturalmente neutro.

| Rol | Color | Hex | Uso | Ratio vs Blanco |
|---|---|---|---|---|
| **Primario** | Azul Confianza | `#1B5E7B` | Headers, botones primarios, links | 7.2:1 (AAA) |
| **Secundario** | Naranja Calido | `#D46A1E` | CTAs, acentos, iconos activos | 4.6:1 (AA Large) |
| **Acento** | Verde Esperanza | `#2E7D4F` | Exito, confirmaciones, checks | 5.8:1 (AAA Large) |
| **Fondo** | Blanco Suave | `#FAFAFA` | Fondo principal | — |
| **Texto** | Gris Oscuro | `#1A1A2E` | Texto cuerpo | 16.8:1 vs #FAFAFA |
| **Texto Secundario** | Gris Medio | `#4A4A5A` | Labels, texto auxiliar | 9.1:1 vs #FAFAFA |

### Paleta Extendida

| Rol | Hex | Uso |
|---|---|---|
| **Error** | `#C62828` | Mensajes de error |
| **Warning** | `#F9A825` | Avisos, plazos urgentes |
| **Info** | `#E3F2FD` | Fondos informativos |
| **Card BG** | `#F5F5F5` | Tarjetas, contenedores |
| **Borde** | `#E0E0E0` | Separadores |

### Justificacion del Color

- **Azul `#1B5E7B`**: Confianza institucional sin ser frio. Universalmente asociado con seguridad.
- **Naranja `#D46A1E`**: Anade calidez humana. Culturalmente positivo en Latinoamerica y Marruecos. Energia y accesibilidad.
- **Verde `#2E7D4F`**: Esperanza y crecimiento. Culturalmente positivo en el Islam (color sagrado). Para confirmaciones.

### Validacion Daltonismo

| Tipo | Azul | Naranja | Verde |
|---|---|---|---|
| Vision normal | Distinguible | Distinguible | Distinguible |
| Deuteranopia | OK | Amarillento | Oscurece |
| Protanopia | OK | Amarillento | Oscurece |
| Tritanopia | Rojizo | OK | OK |

**Regla:** Nunca usar color como unico medio para transmitir informacion.

### Psicologia del Color — Investigacion

| Color | Asociacion | Aplicacion en Clara |
|---|---|---|
| **Azul** | Confianza, seguridad — usado por gobiernos, bancos y tech | Color primario — evoca servicios publicos |
| **Naranja** | Entusiasmo, creatividad, calidez, diversion | Color secundario — humaniza la IA |
| **Verde** | Salud, esperanza, naturaleza, Islam (sagrado) | Confirmaciones — culturalmente positivo para audiencia marroqui |
| **Blanco** | Limpieza, claridad, espacio | Fondo — reduce carga cognitiva |
| **Gris oscuro** | Seriedad, legibilidad | Texto — mejor que negro puro para pantalla |

> **Fuentes:** UAE Design System, InsightsPsychology, HeartSpark Design, MockFlow

### 2.2 Tipografia

**Fuentes Seleccionadas (Google Fonts, gratuitas):**

| Uso | Fuente | Peso | Por que |
|---|---|---|---|
| **Titulares** | **Atkinson Hyperlegible Next** | Bold (700) | Disenada por el Braille Institute para baja vision. Exagera diferencias entre letras similares (I/l, 0/O). En 2025 se lanzo version Next con peso variable y set de caracteres expandido |
| **Cuerpo** | **Inter** | Regular (400), Medium (500) | Optimizada para pantallas. Espaciado generoso. Excelente legibilidad a tamanos grandes. Soporta 200+ idiomas |
| **Fallback** | **Noto Sans** | Regular (400) | Soporte universal de idiomas (1000+). Fallback para futuro arabe |

**Tamanos Minimos:**

| Elemento | Minimo | Recomendado | Line Height |
|---|---|---|---|
| Texto cuerpo (movil) | 18px | 20px | 1.6 |
| Texto cuerpo (desktop) | 18px | 20px | 1.5 |
| H1 | 32px | 36px | 1.3 |
| H2 | 24px | 28px | 1.3 |
| Botones | 18px | 20px | 1.0 |
| Labels/captions | 16px | 16px | 1.4 |

**Investigacion sobre Tipografia y Personas Mayores:**
- La presbicia afecta a la mayoria de personas mayores de 45 anos — requiere tamanos de fuente mas grandes
- Adultos de mediana edad indicaron que **18pt** es mas accesible
- El estilo **bold** tuvo mayor recuerdo que regular e italica tanto en adultos mayores como jovenes
- Fuentes **sans-serif** son recomendadas para lectura en pantalla

> **Fuentes:** PMC, Google Fonts, accessiBe, Section508.gov

### Reglas Tipograficas Accesibles

1. **Nunca** usar todo mayusculas para mas de 3-4 palabras
2. **Siempre** alinear a la izquierda (no justificar)
3. **Maximo** 70 caracteres por linea
4. **Contraste** minimo 7:1 para texto normal, 4.5:1 para texto grande (24px+)
5. **Peso** bold para titulares — mejora el recuerdo en personas mayores

---

## 3. Frontend Accesible — WCAG 2.1 AAA

### 3.1 Estandares WCAG

WCAG se organiza en 4 principios: **Perceptible, Operable, Comprensible y Robusto (POUR)**. Tres niveles: A (minimo), AA (intermedio), AAA (maximo).

- WCAG 2.1 incluye **78 criterios de exito**
- WCAG 2.2 incluye **87 criterios**: 32 Level A, 24 Level AA, 31 Level AAA
- **Nota importante:** No se recomienda AAA como requisito general para sitios completos porque no es posible satisfacer todos los criterios AAA para todo tipo de contenido. La recomendacion es apuntar a AAA donde sea factible y asegurar AA como minimo.

### Contraste Mejorado (SC 1.4.6 — AAA)
- Ratio **7:1 para texto normal** y **4.5:1 para texto grande**

### Nivel de Lectura (SC 3.1.5 — AAA)
- Cuando el texto requiere habilidad de lectura superior al nivel de educacion secundaria baja, debe proporcionarse contenido suplementario o version simplificada

### Cumplimiento Legal (2025-2026)
- La European Accessibility Act (EAA) entra en vigor en junio 2025
- Para cumplimiento legal en 2026, apuntar a WCAG 2.1 Level AA minimo
- WCAG 2.2 Level AA es el estandar recomendado

### 3.2 Checklist WCAG AAA para Clara

**Contraste y Color:**
- [ ] Ratio 7:1 para texto normal sobre fondo
- [ ] Ratio 4.5:1 para texto grande (24px+)
- [ ] Nunca usar color como unica forma de transmitir info
- [ ] Modo alto contraste disponible como toggle

**Navegacion y Teclado:**
- [ ] Todos los elementos interactivos accesibles con Tab
- [ ] Indicadores de foco visibles (outline 3px azul)
- [ ] Orden de tabulacion logico
- [ ] Sin trampas de teclado

**Lectores de Pantalla:**
- [ ] Todos los botones con aria-label descriptivo
- [ ] Imagenes con alt text significativo
- [ ] Regiones ARIA (main, nav, complementary)
- [ ] Anuncios dinamicos con aria-live

**Movimiento y Animaciones:**
- [ ] Respetar `prefers-reduced-motion`
- [ ] Sin contenido que parpadee >3 veces/segundo
- [ ] Animaciones opcionales

**Targets Tactiles:**
- [ ] Minimo 44x44px para todos los botones (AAA)
- [ ] Recomendado 64x64px para botones principales (elderly)
- [ ] Espacio minimo 8px entre targets adyacentes

### Investigacion sobre Touch Targets

| Plataforma | Tamano Minimo |
|---|---|
| Apple iOS | 44x44 points |
| Google Android | 48x48 dp |
| Microsoft | 44x44 pixels |
| WCAG 2.2 AA | 24x24 CSS pixels |
| WCAG 2.1 AAA | 44x44px |

Investigacion de la University of Maryland (2023): targets menores a 44x44px tienen **tasa de error 3x mayor**.

**Recomendacion para Clara:** Minimo **48x48px**, recomendado **64x64px** para acciones principales.

> **Fuentes:** W3C WAI, Smashing Magazine, AllAccessible

---

## 4. Librerias UI y Tecnologias

### 4.1 Librerias de Componentes React

| Libreria | Accesibilidad | Pros | Contras | Recomendacion |
|---|---|---|---|---|
| **React Aria (Adobe)** | AAA (la mejor) | Respaldado por investigacion Adobe, hooks, testing exhaustivo | Requiere construir UI propia | **Recomendado** para Clara |
| **Radix UI** | AAA | Headless, ARIA built-in, 35K+ GitHub stars | Desarrollo puede estar desacelerando | Excelente alternativa |
| **Shadcn/ui** | Muy buena (usa Radix) | Copy-paste, Tailwind | Requiere Tailwind setup | Mejor balance calidad/velocidad |
| **Chakra UI** | Muy buena | Temas, responsive, facil | Bundle mas grande | Buena para MVP rapido |
| **Gradio** (actual) | Limitada | Ya implementado, usa Svelte no React | Poca customizacion WCAG | OK para demo, migrar despues |

**Tendencia 2026:** 70% de crecimiento en adopcion de librerias **headless** vs styled.

**Recomendacion para hackathon:** Mantener Gradio para la demo web (ya funciona). Para el futuro, **React Aria** es la base recomendada.

### 4.2 Internacionalizacion (i18n)

| Feature | next-intl | react-i18next |
|---|---|---|
| Next.js App Router | Soporte nativo | No compatible |
| Server Components | Built-in | Requiere workarounds |
| Bundle Size | ~2KB | ~8KB |
| Routing | Built-in | Manual |
| 2026 Recomendacion | **Mejor opcion** | Mejor para proyectos legacy |

**Soporte RTL (arabe futuro):** i18next detecta direccionalidad via `i18n.dir()`.

**Recomendacion:** **next-intl** para proyecto Next.js en 2026.

### 4.3 Performance y PWA

- PWAs deben cargar en **menos de 2 segundos en 3G** mediante code splitting y lazy loading
- **Service workers** son el nucleo de funcionalidad offline
- **Cache-first strategies** fundamentales para velocidad y offline
- **Adaptive loading**: cargar elementos segun tipo de conexion del usuario

> **Fuentes:** Smashing Magazine, MDN, LogRocket, ATechnocrat

---

## 5. Wireframes y Mockups

### 5A. Pantalla de Bienvenida

```
+----------------------------------+
|                                  |
|         [Logo Clara]             |
|                                  |
|     "Tu voz tiene poder"         |
|                                  |
|  +----------------------------+  |
|  |   Te ayudo con tramites    |  |
|  |   sociales en Espana.      |  |
|  |   Habla o escribe en       |  |
|  |   tu idioma.               |  |
|  +----------------------------+  |
|                                  |
|  +--------+  +----------------+  |
|  | ES     |  | Francais  FR  |  |
|  |Espanol |  |               |  |
|  +--------+  +----------------+  |
|                                  |
|  +----------------------------+  |
|  |      EMPEZAR A HABLAR      |  |
|  |          [mic]             |  |
|  +----------------------------+  |
|                                  |
|  +----------------------------+  |
|  |   Prefiero escribir  [kb] |  |
|  +----------------------------+  |
|                                  |
+----------------------------------+
```

**Specs:** Logo 120px centrado | Tagline 28px Atkinson Bold | Descripcion 20px Inter Regular | Selector idioma 64x48px | Boton "Empezar" 100% ancho, 72px alto, azul `#1B5E7B`, texto blanco 22px | Boton "Escribir" 100% ancho, 56px alto, borde gris, 18px

### 5B. Interfaz de Chat

```
+----------------------------------+
|  [<-]  Clara          [ES v] [*] |
+----------------------------------+
|                                  |
|  +-------------------------+     |
|  | Hola, soy Clara.       |     |
|  | En que puedo ayudarte?  |     |
|  |                         |     |
|  | Puedo informarte sobre: |     |
|  | - Ingreso Minimo Vital  |     |
|  | - Empadronamiento       |     |
|  | - Tarjeta sanitaria     |     |
|  +-------------------------+     |
|                                  |
|         +---------------------+  |
|         | Que es el IMV?      |  |
|         +---------------------+  |
|                                  |
|  +-------------------------+     |
|  | El Ingreso Minimo Vital |     |
|  | es una ayuda mensual... |     |
|  |                         |     |
|  | [> Escuchar respuesta]  |     |
|  |                         |     |
|  | Fuente: seg-social.es   |     |
|  +-------------------------+     |
|                                  |
|  +----------------------------+  |
|  | Escribe tu pregunta...    |  |
|  +----------------------------+  |
|                                  |
|  +--------+ +--------+ +------+ |
|  |  [kb]  | |  [mic] | | [cam]| |
|  |Escribir| |  Voz   | | Foto | |
|  +--------+ +--------+ +------+ |
+----------------------------------+
```

**Specs:** Header 56px, azul oscuro | Burbujas Clara: `#E3F2FD`, radius 16px, padding 16px, max-width 85% | Burbujas usuario: `#1B5E7B`, texto blanco | Boton audio: verde `#2E7D4F` | Input: 56px, borde 2px `#E0E0E0`, font 18px | 3 botones: 64x64px cada uno

### 5C. Grabacion de Voz

```
+----------------------------------+
|                                  |
|         Habla ahora...           |
|                                  |
|     ~~~~~~~~~~~~~~~~             |
|     (onda de audio animada)      |
|                                  |
|           timer 0:05             |
|                                  |
|         +----------+             |
|         |   [mic]  |             |
|         |  96x96   |             |
|         +----------+             |
|        (pulsando = rojo)         |
|                                  |
|  +------------+ +-------------+  |
|  |  Cancelar  | |   Enviar    |  |
|  +------------+ +-------------+  |
|                                  |
+----------------------------------+
```

**Specs:** "Habla ahora" 28px | Onda: CSS animation, 4px, naranja `#D46A1E` | Timer: 24px monospace | Mic: 96x96px circular, rojo `#C62828` mientras graba | Cancelar/Enviar: 64px alto

### 5D. Subida de Documento

```
+----------------------------------+
|  [<-]  Subir documento           |
+----------------------------------+
|                                  |
|  +----------------------------+  |
|  |    Sube una foto de tu     |  |
|  |    documento o carta       |  |
|  |    Clara te explicara      |  |
|  |    que dice                |  |
|  +----------------------------+  |
|                                  |
|  +----------------------------+  |
|  |        [cam grande]        |  |
|  |   Toca para hacer foto     |  |
|  +----------------------------+  |
|                                  |
|  +----------------------------+  |
|  |  O elige de tu galeria [f] |  |
|  +----------------------------+  |
|                                  |
+----------------------------------+
```

### 5E. Respuesta con Audio

```
+----------------------------------+
|  +-------------------------+     |
|  | Clara                   |     |
|  |                         |     |
|  | He analizado tu         |     |
|  | documento. Es una       |     |
|  | comunicacion de la      |     |
|  | Seguridad Social...     |     |
|  |                         |     |
|  | +-------------------+   |     |
|  | | [>] ====o=== 1:23 |   |     |
|  | | Escuchar respuesta |   |     |
|  | +-------------------+   |     |
|  |                         |     |
|  | Fuente: seg-social.es   |     |
|  | Tel: 900 16 65 65       |     |
|  |                         |     |
|  | +---------++---------+  |     |
|  | |  Util   ||Mejorable|  |     |
|  | +---------++---------+  |     |
|  +-------------------------+     |
|                                  |
|  +----------------------------+  |
|  |  Preguntar otra cosa  [+] |  |
|  +----------------------------+  |
+----------------------------------+
```

---

## 6. Patrones de Interaccion

### Grabacion de Voz
- **Mecanismo:** Toggle (un toque para empezar, otro para parar) — NO press-and-hold (dificil para mayores)
- **Feedback visual:** Boton cambia a rojo + onda de audio + timer
- **Feedback auditivo:** Beep corto al empezar y al parar
- **Limite:** 60 segundos maximo, aviso a los 50s

### Reproduccion de Audio
- **Boton play:** 48x48px minimo
- **Barra de progreso:** Visible, con tiempo transcurrido/total
- **Velocidad:** 0.75x / 1x / 1.25x (mayores prefieren mas lento)
- **Auto-play:** NO. Siempre manual

### Estados de Carga
- **Procesando audio:** "Clara esta escuchando tu mensaje..." + ondas
- **Generando respuesta:** "Clara esta buscando informacion..." + spinner suave
- **Analizando documento:** "Clara esta leyendo tu documento..." + escaneo
- **Timeout (>15s):** "Esta tardando un poco mas de lo normal. Un momento..."

### Estados de Error
- **No entendio:** "Perdona, no he entendido bien. Puedes repetirmelo?"
- **Sin conexion:** "Parece que no hay conexion. Revisa tu wifi o datos moviles"
- **Servicio caido:** "Clara no esta disponible ahora. Intenta en unos minutos"
- **Todos con:** icono + mensaje + accion sugerida

### Patrones UX WhatsApp

| Patron | Clara lo implementa |
|---|---|
| **Saludo inmediato** (<5s) | ACK TwiML en <1s |
| **Botones rapidos** (3 max) | "IMV / Empadronamiento / Tarjeta sanitaria" |
| **Mensajes estructurados** | Pasos numerados, listas claras |
| **Emojis con moderacion** | 1-2 por mensaje, significativos |
| **Cierre con fuente** | "Mas info: seg-social.es" |

### Componentes Interactivos WhatsApp Business API

| Componente | Uso en Clara | Ejemplo |
|---|---|---|
| **Quick Reply Buttons** (max 3) | Opciones simples | "Si / No / Necesito ayuda" |
| **List Messages** (max 10) | Categorias de servicio | "Selecciona tu distrito" |
| **CTA Buttons** | Links directos | "Llamar servicios sociales" / "Abrir mapa" |
| **Formato texto** | Enfatizar info clave | Bold para plazos, italica para notas |

### Diseno para Personas Mayores — Investigacion Clave

- Usar **fuentes grandes y legibles**; permitir cambio de tamano dentro de la app
- Elementos principales grandes, faciles de ver, interfaz sin desorden
- **Espacio en blanco** reduce carga cognitiva
- Evitar gestos complejos de arrastre y precision
- Evitar labels flotantes; usar **labels estaticos**
- Sin limites de tiempo para tareas
- **Introducir informacion gradualmente**
- Agregar boton "Atras" ademas del del navegador
- En formularios, **una pregunta por pantalla**

> **Fuentes:** PMC/NIH, Nielsen Norman Group, Toptal, Smashing Magazine

---

## 7. Marketing y Publicidad de Impacto Social

### 7.1 Contexto Migratorio Espana 2025-2026

- Poblacion de Espana supero **49 millones** por primera vez en 2025
- Comunidad marroqui: **1,092,892 residentes** (la mayor comunidad extranjera)
- Latinoamericanos: ~48% de la poblacion nacida en el extranjero
- Extranjeros representan ~15% de cotizantes y ~10% de ingresos de la Seguridad Social
- En 2026, el sistema migratorio de Espana se **digitaliza completamente**
- Regularizacion extraordinaria aprobada para 500,000+ migrantes irregulares

> **Fuentes:** INE, VisaHQ, La Moncloa, OECD, Human Rights Watch

### 7.2 Campanas de Impacto Social

**Campana A: "Tu Voz Tiene Poder"**
- **Emocion:** Empoderamiento
- **Visual:** Close-ups de manos diversas sosteniendo telefonos con WhatsApp. Iluminacion dorada calida.
- **Mensaje:** Tu voz es suficiente. Sin formularios. Sin burocracia. Solo habla, y Clara escucha.
- **Hashtags:** #TuVozTienePoder #ClaraIA #InclusinDigital #AccesoParaTodos

**Campana B: "Nadie Se Queda Fuera"**
- **Emocion:** Empatia
- **Visual:** Split-screen. Izquierda: persona confusa ante papeleo (tonos grises). Derecha: misma persona sonriendo con telefono (tonos calidos).
- **Mensaje:** 12.7 millones de personas en Espana luchan por acceder a la ayuda que merecen.
- **Hashtags:** #NadieSeQuedaFuera #ClaraIA #ImpactoSocial #TechForGood

**Campana C: "Habla, Clara Escucha"**
- **Emocion:** Dignidad
- **Visual:** Diseno minimalista. Fondo blanco. Icono de microfono transformandose en mano que ayuda.
- **Mensaje:** No necesitas leer. No necesitas escribir. Solo habla.
- **Hashtags:** #HablaClaraEscucha #VoiceFirst #ClaraIA #IAParaTodos

### 7.3 Ejemplos de Posts por Plataforma

**Instagram (Carousel, 4 slides) — Campana A:**
1. Mano sosteniendo telefono con onda de voz. Texto: "Tu voz tiene poder."
2. Estadisticas: "3.2M inmigrantes. 9.5M mayores. 1 sola barrera: la burocracia."
3. Screenshot de Clara respondiendo en frances y espanol
4. CTA: "Clara entiende tu voz. En tu idioma."

**Twitter/X:** "78% de los mayores de 65 en Espana usan WhatsApp. Pero nadie les habla de las ayudas que merecen. Hasta ahora. Conoce a Clara. #TuVozTienePoder"

**LinkedIn:** Post largo sobre la brecha digital en servicios sociales. Dato: el sistema migratorio se digitaliza en 2026 mientras millones carecen de alfabetizacion digital. Clara como puente.

**TikTok:** Clip 10s de alguien luchando con formulario, luego notificacion WhatsApp, pantalla cambia a teal. "Maniana todo cambia."

### 7.4 Calendario de Contenido (1 Semana)

| Dia | Plataforma | Contenido |
|---|---|---|
| **Lunes** | IG Story + TW + LI | Teaser: "Algo esta llegando..." + stats |
| **Martes** | IG Reel + Carousel + TW + LI + TK | Lanzamiento oficial: video 30s + explicacion |
| **Miercoles** | IG Reel + TW | Historia de Ahmed (demo en frances) |
| **Jueves** | IG Carousel + LI | Historia de Maria (documento analizado) |
| **Viernes** | TK + IG | Behind the scenes: equipo en el hackathon |
| **Sabado** | IG + TW | Impacto: datos y testimonios |
| **Domingo** | LI + IG | Reflexion: "Porque entender no deberia ser un privilegio" |

### 7.5 Accesibilidad en Marketing Digital

**Checklist pre-publicacion:**
- Alt text en todas las imagenes
- Subtitulos quemados en todos los videos
- Contraste >= 4.5:1
- Fuente minima 16pt digital / 14pt print
- Capitalizar primera letra de cada palabra en hashtags (#TuVozTienePoder)
- Evitar "click aqui" sin descriptores
- Construir checkpoints de accesibilidad en el flujo de trabajo

> **Fuentes:** W3C WAI, A11y Collective, WCAG 2.1, Landbot

---

## 8. Estrategia de Video y Prompts IA

### 8.1 Tres Conceptos de Video

**Video A: Elevator Pitch (30 segundos) — "Conoce a Clara"**

| Tiempo | Escena | Visual | Audio |
|---|---|---|---|
| 0-5s | Hook | Pantalla negra, telefono suena | "En Espana, millones no acceden a las ayudas que merecen" |
| 5-10s | Problema | Cortes rapidos: mujer mayor confusa, inmigrante en oficina, cola larga | Cuerdas tensas |
| 10-18s | Solucion | WhatsApp abre. Nota de voz en frances. Clara responde | Musica cambia a esperanzadora |
| 18-25s | Features | Iconos animados: microfono, globo, documento, campana | Beat rapido |
| 25-30s | CTA | Logo Clara + fondo verde WhatsApp + QR | Acorde calido final |

**Video B: Demo de Producto (90 segundos) — "Clara en Accion"**

| Tiempo | Escena | Detalle |
|---|---|---|
| 0-10s | Contexto | Plano aereo de ciudad espanola + estadisticas |
| 10-25s | Ahmed | Joven senegaleses, carta que no entiende, graba nota de voz en frances |
| 25-45s | Ahmed usa Clara | Close-up del telefono: nota de voz -> respuesta de Clara en frances |
| 45-60s | Maria | Mujer mayor (74), mesa con papeles, foto de carta oficial enviada a Clara |
| 60-75s | Maria usa Clara | Clara lee documento, identifica complemento de pension, explica paso a paso |
| 75-85s | Impacto | Split screen: Ahmed con carta de aprobacion, Maria agradecida |
| 85-90s | CTA | Logo + stats + QR |

**Video C: Historia de Impacto Social (2 minutos) — "La Voz Que Faltaba"**

| Tiempo | Escena | Detalle |
|---|---|---|
| 0-15s | Apertura | Pan lento por oficina de servicios sociales. Cola larga. Luces fluorescentes |
| 15-30s | El muro | Close-ups: formularios en espanol legal, mano temblorosa, mujer pidiendo traduccion |
| 30-50s | Historias | Montaje: madre africana con facturas, hombre mayor comiendo solo, joven refugiado |
| 50-70s | La chispa | Alguien recibe WhatsApp: "Prueba Clara". Graba nota de voz |
| 70-100s | Clara en accion | Demo detallada: voz en frances, documento analizado, pasos por voz |
| 100-110s | Transformacion | Mismas personas mejoradas: carta aprobada, trabajador social, formacion laboral |
| 110-120s | Impacto | Data viz: mapa de Espana iluminandose. Contador animado |
| 120-130s | CTA | Logo + QR + "Clara. La voz que faltaba." |

### 8.2 Prompts para Video IA

**Runway Gen-3/Gen-4 (Free: ~40s de video):**

Prompt 1 — "La Cola" (4s):
> "35mm film grain, slow dolly shot moving along a long queue of people in a Spanish government office. Fluorescent overhead lighting. Diverse crowd: elderly with folders, young immigrants confused. Muted desaturated blues and grays. Shallow depth of field on tired faces."

Prompt 2 — "La Nota de Voz" (4s):
> "Close-up of weathered hands holding a smartphone. WhatsApp open. Finger presses microphone button. Warm kitchen background, golden afternoon light. 50mm lens, shallow depth of field. Mood shifts from uncertainty to hope. Slight camera push-in."

Prompt 3 — "Ahmed" (4s):
> "Medium shot of young African man mid-20s at small desk in modest apartment. Holds official letter, looking puzzled. Natural window light, warm tones. 35mm lens. Slight handheld documentary style."

Prompt 4 — "Maria" (4s):
> "Wide shot elderly Spanish woman, mid-70s, white hair, kitchen table with papers. Picks up smartphone and smiles slightly. Warm interior, Mediterranean tiles. 40mm lens, gentle push-in."

Prompt 5 — "Transformacion" (4s):
> "Close-up elderly woman's face breaking into genuine smile looking at phone. Tears of relief. Golden hour light. 85mm portrait lens, shallow depth of field. Slow motion 48fps."

**Pika AI (Free: ~3s clips):**

> "A glowing microphone icon slowly transforms into an open hand reaching out, teal and orange gradient, smooth 3D animation, particles of light"

> "Stack of bureaucratic papers dissolving into colorful particles that reform into a WhatsApp chat bubble, dreamy cinematic style"

### 8.3 Prompts para Musica IA (Suno)

Track 1 — "Hope Rising" (30s):
> "Uplifting acoustic guitar and soft piano instrumental, building from quiet to warm and hopeful. Light percussion at 15s. No vocals. Social impact video. Tempo 110 BPM. Warm, organic."

Track 2 — "Clara's Theme" (90s):
> "Gentle piano over ambient electronic pads, documentary underscore. Starts contemplative, builds with soft strings and subtle beat. Hopeful technology meets human warmth. No vocals. 85 BPM."

Track 3 — "La Voz Que Faltaba" (130s):
> "Solo cello opening, melancholy 30s. Piano joins, hopeful. At 60s full strings swell. Acoustic guitar at 90s. Climax at 100s full orchestra. Resolves gently. Film score. No vocals."

### 8.4 Prompts para Imagenes IA

Persona mayor:
> "Warm photorealistic image of elderly Spanish woman, 70 years old, silver hair, cozy kitchen, holding smartphone showing WhatsApp, smiling while listening to voice message. Soft natural lighting. Warm tones, teal and orange accents. Feeling: dignity, connection."

Inmigrante:
> "Warm photorealistic portrait of young Moroccan man, 30, casual clothing, simple apartment, recording voice note on WhatsApp. Expression: focused but hopeful. Warm lighting, orange and teal palette. Feeling: empowerment."

Contraste:
> "Split image: left = confusing government office with long queues and complex forms in gray tones, right = same person at home talking to phone with WhatsApp open, warm orange and teal, smiling."

### 8.5 Voiceover IA

- **ElevenLabs (Free):** Voz femenina espanola calida y madura. Lineas clave: "En Espana, millones de personas no acceden a las ayudas que merecen" / "Tu voz tiene poder"
- **Canva TTS:** Dentro del editor de video. Soporta espanol. Menor calidad pero ilimitado
- **Grabacion natural:** Miembros del equipo. OBS Studio + Audacity para limpiar audio

> **Fuentes:** PXZ, MyMagicPrompt, CrePal, Runway Help Center, GitHub awesome-ai-video-prompts, Soundverse

---

## 9. Pitch Deck y Materiales Fisicos

### 9.1 Pitch Deck (8 Slides)

| Slide | Titulo | Visual | Texto (max 30 palabras) |
|---|---|---|---|
| **1** | Cover | Logo Clara grande + tagline + imagen calida | "Clara — Tu voz tiene poder" |
| **2** | El Problema | Numero gigante "4.5M" + icono personas | "4.5 millones no acceden a ayudas por barreras de idioma y burocracia" |
| **3** | Clara | 4 iconos diferenciadores en grid | "Voz + Multilingue + Vision IA + Proactiva" |
| **4** | Demo Ahmed | Screenshot WA + bandera FR | DEMO EN VIVO: audio frances -> respuesta |
| **5** | Demo Maria | Screenshot web + foto carta | DEMO EN VIVO: foto documento -> explicacion |
| **6** | Arquitectura | Diagrama simple (3 cajas + flechas) | "Stack 0 EUR: Gemini + Whisper + Twilio" |
| **7** | Impacto | 3 numeros grandes con iconos | "3.2M inmigrantes / 9.5M mayores / 78% usan WA" |
| **8** | Cierre | Frase + QR + logo | "Porque entender no deberia ser un privilegio" |

**Specs slides:** 16:9, fondo blanco `#FAFAFA`, acento azul `#1B5E7B`, titulo 36pt Atkinson Bold, texto 20pt Inter Regular, max 30 palabras por slide, 1 idea por slide.

### 9.2 Poster A4

Estructura: cabecera con logo y tagline, 3 pasos visuales (Envia nota de voz -> Clara analiza -> Recibe orientacion), banda de stats de impacto, QR code 5x5cm en esquina inferior.

### 9.3 Roll-Up Banner (85x200cm)

Estructura vertical: logo grande arriba, mockup de telefono con conversacion WhatsApp en el centro, bloques de features, banda de estadisticas, QR 15x15cm abajo.

### 9.4 Estrategia QR

- Link directo WA: `https://wa.me/TELEFONO?text=Hola%20Clara`
- QR diferente por material (poster vs banner vs redes) para tracking
- **Siempre** acompanar QR con URL en texto o numero de telefono (accesibilidad)

---

## 10. Tendencias de Diseno 2025-2026

### 10.1 Accesibilidad Cognitiva y Diseno Simplificado

La industria va mas alla de accesibilidad solo para lectores de pantalla hacia **accesibilidad cognitiva**: reducir desorden visual, layouts consistentes, instrucciones simples, opciones para reducir animaciones. Incluye soporte para usuarios con ADHD, autismo, dislexia y baja alfabetizacion.

**Aplicacion:** Layouts consistentes y predecibles, limitar densidad de info a 1-2 ideas por pantalla, jerarquia visual clara con espacio en blanco generoso.

### 10.2 Interfaces Voice-First y Multimodales

La tecnologia de voz es central para usuarios con impedimentos motores o desafios de alfabetizacion. El mercado de asistentes de voz se proyecta en **USD 54.83 mil millones para 2033**.

### 10.3 Diseno Age-Inclusive

- Botones grandes y claramente etiquetados (minimo 48dp)
- Limitar opciones de menu a 3-5 maximo por interaccion
- Lenguaje conversacional familiar
- Opciones "atras" y "empezar de nuevo" en cada paso
- Testear con usuarios mayores reales

### 10.4 Fin de los Overlays de Accesibilidad

La industria se aleja de widgets overlay de accesibilidad. Expertos y defensores de discapacidad notan que raramente arreglan problemas reales. La accesibilidad verdadera debe construirse en el diseno core.

### 10.5 Interfaces Glassmorphism y Bento Grid

- **Glassmorphism:** Interfaces translucidas "glass-like" con backdrop blur y capas semi-transparentes
- **Bento Grid:** Layout modular con bloques de diferentes tamanos, como un bento japones

### 10.6 Interfaces Adaptativas y Generativas

Los productos IA modernos se mueven de "una interfaz para todos" hacia UIs **dinamicamente adaptativas**. Clara deberia adaptar complejidad de mensajes segun patrones de interaccion.

### 10.7 Asistencia Embebida y Ambiental

Los asistentes IA se mueven de novedad standalone a capas de servicio silenciosas dentro de herramientas familiares. Menos fanfarria, mas utilidad.

**Aplicacion:** Evitar lenguaje excesivamente "IA" ("Estoy alimentada por redes neuronales avanzadas..."). Usar tono natural ("Dejame buscar eso para ti"). Integrarse con comportamientos nativos de WhatsApp.

> **Fuentes:** Level Access, InSuit, ExcellentWebWorld, OscarChat, Prototypr, Visme, Promodo

---

## 11. Diseno Civico y Referencias

### 11.1 GOV.UK Design System — El Estandar de Oro

Los 10 Principios de Diseno del Gobierno UK:
1. Empezar con las necesidades del usuario
2. Hacer menos (solo lo que el gobierno debe hacer)
3. Disenar con datos
4. Hacer el trabajo dificil para que sea simple
5. Iterar, y luego iterar de nuevo
6. Esto es para todos
7. Entender el contexto
8. Construir servicios digitales, no sitios web
9. Ser consistente, no uniforme
10. Hacer las cosas abiertas

**Aplicacion para Clara:**
- Escribir a nivel de lectura de 6to grado o inferior
- Una cosa por pagina/mensaje: hacer una pregunta a la vez
- Proporcionar "que pasa despues" claro tras cada accion
- Testear primero con los usuarios mas excluidos

### 11.2 Decidim Barcelona

Plataforma open-source de democracia participativa escrita en Ruby on Rails. Principios: transparencia, trazabilidad, integridad, privacidad, seguridad, accesibilidad, soberania tecnologica.

**Accesibilidad:** Dialogo para ajustar modo oscuro, tipografia y tamano. Programa de mediacion digital en bibliotecas y centros civicos.

**Aplicacion:** Ofrecer guia de ajuste de fuente y contraste. Asociarse con bibliotecas y centros civicos para soporte presencial de Clara.

### 11.3 Code for America / Code for Europe

Non-profit de civic tech que coloca tecnologos y disenadores en ciudades para crear soluciones civicas.

**Aplicacion:** Mapear el journey real del usuario para acceder a servicios sociales en Espana. Identificar y eliminar pasos innecesarios y jerga. Disenar para el "happy path" pero manejar errores con gracia.

### 11.4 Framework de Civic Design Systems

Frameworks estructurados combinando diseno de interfaz, estandares de accesibilidad y patrones de usabilidad. Tendencia hacia herramientas hiperlocales y accesibles que encajan en habitos digitales diarios.

**Aplicacion:** Crear sistema de diseno Clara con plantillas de mensajes reutilizables. Estandarizar presentacion de info (direcciones, telefonos, horarios, requisitos). Progressive disclosure: info esencial primero, detalles bajo peticion.

### 11.5 Ejemplos Premiados de Diseno de Impacto Social

| Producto/Premio | Descripcion | Leccion para Clara |
|---|---|---|
| **Watch Duty** (Apple Design Award) | App de incendios forestales. Interfaz limpia y urgente | Priorizar claridad e inmediatez |
| **Speechify** (Apple Design Award) | Text-to-audio con VoiceOver | Output multimodal (texto + audio) |
| **Core77 Social Impact** | Impacto comunitario, comunidades subrepresentadas | Centrar diseno en la comunidad, no en la tecnologia |
| **Contentsquare Prize** | IA para accesibilidad, inclusion cognitiva | Usar IA para reducir barreras, no anadir complejidad |

> **Fuentes:** GOV.UK, Decidim.org, Code for America, CivicPatterns, Civic Tech Field Guide, Granicus, Apple Design Awards

---

## 12. Diseno Inclusivo Multicultural

### 12.1 Sensibilidad Cultural por Comunidad

| Comunidad | En Espana | Consideraciones de Diseno |
|---|---|---|
| **Marroqui** | 1.09M (mayor comunidad extranjera) | Verde sagrado en Islam. Evitar cerdo/alcohol en ilustraciones. Analogias con "wilaya". Frances como puente linguistico |
| **Latinoamericana** | ~48% de poblacion extranjera | Colores calidos bien recibidos. "Usted" vs "tu" segun pais. **Amarillo asociado con luto** en algunos paises |
| **Subsahariana** | Senegal, Mali, Nigeria | Colores primarios fuertes preferidos. Comunicacion oral (tradicion griot). Respeto por edad y comunidad |
| **Mayores espanoles** | 9.5M (65+) | Tamanos grandes. Sin anglicismos. Referencia a instituciones conocidas (Seguridad Social, Ayuntamiento) |

### 12.2 Simbolismo del Color por Region

- **Latinoamerica:** Prefieren simbolos tradicionales. Azul y blanco asociados con la Virgen Maria. Amarillo con luto. Tonos **dorados** universalmente aceptados.
- **Africa Subsahariana:** Colores primarios populares con tonos profundos. Culturas pueden preferir **tonos tierra** por conexion con naturaleza. Simbolos Adinkra (Sankofa = aprender del pasado).

### 12.3 Representacion Visual Inclusiva

- Usar ilustraciones que representen diversidad de etnias, edades y capacidades
- Evitar simbolos culturalmente especificos que no se traduzcan (ej: pulgar arriba es ofensivo en algunas culturas)
- Usar simbolos universales donde sea posible (casa = hogar, telefono = llamar, reloj = tiempo)
- **70% de audiencias** encuentran la apropiacion cultural poco atractiva

### 12.4 Librerias de Ilustracion Inclusiva (Gratuitas)

| Libreria | Estilo | Diversidad | URL |
|---|---|---|---|
| **Humaaans** | Semi-abstracto, mix-and-match | Alta | humaaans.com |
| **Open Peeps** | Hand-drawn, expresivo | Alta | openpeeps.com |
| **Blush** | Varios estilos, customizable | Alta | blush.design |
| **unDraw** | Flat, vectorial | Media | undraw.co |

### 12.5 Reglas para Ilustraciones

1. Diversidad de tonos de piel, edades, tipos de cuerpo
2. Sin estereotipos: no asociar pais con profesion/situacion
3. Contextos positivos: personas activas, sonrientes, con agencia
4. Evitar simbolos religiosos, imagenes politicas, estereotipos de pobreza
5. Consistencia de estilo en todos los materiales

### 12.6 Iconografia Universal

| Concepto | Material Icon | Emoji WA | Significado |
|---|---|---|---|
| Hablar/voz | `mic` | mic emoji | Grabar audio |
| Escribir | `keyboard` | keyboard emoji | Modo texto |
| Documento | `description` | page emoji | Subir foto |
| Idioma | `translate` | globe emoji | Cambiar idioma |
| Ayuda | `help_outline` | question emoji | Pedir ayuda |
| Exito | `check_circle` | check emoji | Confirmacion |
| Telefono | `phone` | phone emoji | Llamar para mas info |
| Web | `open_in_new` | link emoji | Ir a fuente oficial |

> **Fuentes:** ZillionDesigns, Cieden, FrontMatter, NumberAnalytics, Gapsy Studio, IxDF, Koos

---

## 13. Herramientas Gratuitas

### 13.1 Catalogo Completo

| Herramienta | Uso | Free Tier |
|---|---|---|
| **Canva** | Slides, posters, banners, video basico, QR | Ilimitado (basico) |
| **Figma** | UI mockups, slides avanzadas | 3 proyectos gratis |
| **CapCut** | Edicion video + auto-subtitulos ES/FR | 100% gratis |
| **OBS Studio** | Grabacion pantalla para demo backup | Open source |
| **Bing Image Creator** | Generar imagenes con DALL-E 3 | ~15 imagenes/dia |
| **Ideogram** | Imagenes con texto integrado | ~25/dia |
| **Runway** | Clips video IA 4s | ~40s gratis |
| **Pika** | Clips video IA estilizados 3s | Free tier disponible |
| **Suno** | Musica IA de fondo | ~10 canciones/dia |
| **ElevenLabs** | Voiceover IA en espanol | 10K caracteres/mes |
| **Audacity** | Edicion y limpieza de audio | Open source |

### 13.2 Testing de Accesibilidad

| Herramienta | Tipo | Que testea | Gratuita |
|---|---|---|---|
| **WebAIM Contrast Checker** | Web | Ratios de contraste | Si |
| **axe DevTools** | Chrome Extension | WCAG automatizado (70+ tests) | Si (basico) |
| **Lighthouse** | Chrome DevTools | Performance + Accesibilidad | Si |
| **WAVE** | Chrome Extension | Errores WCAG visuales | Si |
| **NVDA** | Desktop (Windows) | Screen reader | Si |
| **VoiceOver** | macOS/iOS built-in | Screen reader | Si |
| **Hemingway Editor** | Web | Nivel de lectura del texto | Si |
| **Guidepup** | Automatizacion | Tests con VoiceOver y NVDA | Si |
| **Accessible Palette** | Web | Sistemas de color accesibles | Si |

**Cobertura estimada:** NVDA + ANDI + testing manual de teclado captura ~90% de problemas criticos.

---

## 14. Fuentes Bibliograficas

### Accesibilidad y WCAG
- [WCAG 2.1 — W3C](https://www.w3.org/TR/WCAG21/)
- [WCAG 2.2 Target Size — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- [AllAccessible WCAG 2025 Guide](https://www.allaccessible.org/blog/color-contrast-accessibility-wcag-guide-2025)
- [Accessible Palette Tool](https://accessiblepalette.com/)
- [Section508.gov — Fonts and Typography](https://www.section508.gov/develop/fonts-typography/)
- [Older Users and Web Accessibility — W3C WAI](https://www.w3.org/WAI/older-users/)

### Tipografia y Fuentes
- [PMC — Font Size for Older Adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC9376262/)
- [Google Fonts — Accessibility in Typography](https://fonts.google.com/knowledge/readability_and_accessibility/)
- [accessiBe — ADA Compliant Fonts 2026](https://accessibe.com/blog/knowledgebase/ada-compliant-fonts)
- [Atkinson Hyperlegible — Wikipedia](https://en.wikipedia.org/wiki/Atkinson_Hyperlegible)
- [WebAbility — 7 Most Accessible Fonts 2026](https://www.webability.io/blog/most-accessible-fonts)

### Diseno Civico y Gobierno
- [GOV.UK Design System](https://design-system.service.gov.uk/)
- [GOV.UK Design Principles](https://www.gov.uk/guidance/government-design-principles)
- [Decidim Barcelona](https://decidim.org/)
- [Code for America](https://codeforamerica.org/about-us/)
- [CivicPatterns](http://civicpatterns.org/)
- [Civic Design Systems — MaxiomTech](https://www.maxiomtech.com/accessible-ux-civic-design-systems/)

### Tendencias de Diseno
- [Digital Accessibility Trends 2026 — InclusiveASL](https://inclusiveasl.com/accessibility/top-digital-accessibility-trends-to-watch-in-2026/)
- [State of Digital Accessibility 2025-2026 — Level Access](https://www.levelaccess.com/resources/state-of-digital-accessibility-report-2025-2026/)
- [UX/UI Design Trends 2026 — Prototypr](https://blog.prototypr.io/ux-ui-design-trends-for-2026)
- [AI Chatbot Trends 2026 — OscarChat](https://www.oscarchat.ai/blog/10-ai-chatbot-trends-2026/)
- [Tech Trends 2026 — Deloitte Insights](https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends.html)

### Chatbots y UX Conversacional
- [Chatbot UI/UX Best Practices — Lollypop](https://lollypop.design/blog/2025/january/chatbot-ui-ux-design-best-practices-examples/)
- [WhatsApp Bot Design — Landbot](https://landbot.io/blog/design-whatsapp-bot-dialogue)
- [Chatbot UI Examples — Eleken](https://www.eleken.co/blog-posts/chatbot-ui-examples)
- [Chatbot UX 2026 — LetsGroto](https://www.letsgroto.com/blog/ux-best-practices-for-ai-chatbots)

### Diseno para Mayores
- [Optimizing Mobile Design for Older Adults — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12350549/)
- [Usability for Senior Citizens — Nielsen Norman Group](https://www.nngroup.com/articles/usability-for-senior-citizens/)
- [UI Design for Older Adults — Toptal](https://www.toptal.com/designers/ui/ui-design-for-older-adults)
- [Designing for Older Adults — Smashing Magazine](https://www.smashingmagazine.com/2024/02/guide-designing-older-adults/)
- [IBM Accessible Design Aging Population](https://www.ibm.com/think/insights/accessible-design-aging-population)

### Confianza y Empatia en IA
- [Trust in Chatbot — SpringerOpen](https://fbj.springeropen.com/articles/10.1186/s43093-023-00288-z)
- [Perceived Empathy and Ethics — Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/08934215.2025.2519253)
- [AI Chatbot for Social Anxiety — ACM CHI 2025](https://dl.acm.org/doi/10.1145/3706598.3714286)

### Sensibilidad Cultural
- [Cultural Palette — ZillionDesigns](https://www.zilliondesigns.com/blog/infographics/understanding-the-cultural-palette/)
- [Color Symbolism — Cieden](https://cieden.com/book/sub-atomic/color/color-symbolism-and-meanings)
- [Cross-Cultural Design — Gapsy Studio](https://gapsystudio.com/blog/cross-cultural-design/)
- [Inclusive Illustrations — Atlassian](https://www.atlassian.com/blog/inside-atlassian/designing-inclusive-illustrations-at-atlassian)

### Migracion en Espana
- [INE — Continuous Population Statistics 2025](https://www.ine.es/dyngs/Prensa/en/ECP1T25.htm)
- [Immigration to Spain — Wikipedia](https://en.wikipedia.org/wiki/Immigration_to_Spain)
- [Spain Immigration Law 2026 — Jobbatical](https://www.jobbatical.com/blog/spain-immigration-law-updates)
- [Spain Regularisation 500K+ — VisaHQ](https://www.visahq.com/news/2026-01-26/es/)
- [World Report 2026: Spain — Human Rights Watch](https://www.hrw.org/world-report/2026/country-chapters/spain)

### Video y Marketing
- [Sora vs Runway vs Pika 2026 — PXZ](https://pxz.ai/blog/sora-vs-runway-vs-pika-best-ai-video-generator-2026-comparison)
- [AI Video Prompting — MyMagicPrompt](https://mymagicprompt.com/ai/covers-the-hottest-trend-in-ai-generative-video/)
- [Runway Gen-3 Prompting Guide](https://help.runwayml.com/hc/en-us/articles/30586818553107)
- [Suno AI Prompts 2026 — Soundverse](https://www.soundverse.ai/blog/article/how-to-write-effective-suno-ai-prompts-1314)
- [Nonprofit Pitch Deck — Pageon](https://www.pageon.ai/blog/nonprofit-pitch-deck)

### Hackathon
- [OdiseIA4Good](https://www.odiseia4good.org/en)
- [UDIT — OdiseIA4Good 2026](https://www.udit.es/en/udit-aliada-del-hackathon-internacional-odiseia4good-2026/)
- [How to Create a Hackathon Pitch — TAIKAI](https://taikai.network/en/blog/how-to-create-a-hackathon-pitch)

### Librerias UI
- [React UI Libraries 2025 — Makers Den](https://makersden.io/blog/react-ui-libs-2025-comparing-shadcn-radix-mantine-mui-chakra)
- [Best React Component Libraries 2026 — Builder.io](https://www.builder.io/blog/react-component-libraries-2026)
- [Humaaans](https://www.humaaans.com/)
- [Open Peeps](https://www.openpeeps.com/)
- [Material Design Icons](https://developers.google.com/fonts/docs/material_icons)

---

*Reporte compilado el 19 de febrero de 2026. Basado en investigacion de 5 agentes especializados con 30+ busquedas web y 80+ fuentes verificadas.*

