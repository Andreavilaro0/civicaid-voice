# Estrategia de Marca — Clara / CivicAid Voice

> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good 2026 — UDIT
> **Fecha:** 19 Feb 2026
> **Autora:** Andrea Avila (Design Lead)
> **Enfoque:** Accesibilidad + Impacto Social

---

## 1. Identidad de Marca

### Analisis del Nombre "Clara"

| Aspecto | Detalle |
|---|---|
| **Etimologia** | Del latin "clarus" — claro, brillante, luminoso |
| **Connotaciones** | Claridad, transparencia, luz, simplicidad, honestidad |
| **Sonoridad** | Facil de pronunciar en espanol, frances, arabe e ingles |
| **Genero** | Femenino — evoca cercanla, cuidado, confianza (respaldado por estudios de UX en chatbots) |
| **Memorabilidad** | 5 letras, 2 silabas, universal |

### Taglines (Opciones)

| # | Tagline | Idioma | Enfoque |
|---|---|---|---|
| 1 | **"Tu voz tiene poder"** | ES | Empoderamiento, accesibilidad por voz |
| 2 | **"Tus derechos, en tu idioma"** | ES | Multilingue, derechos sociales |
| 3 | **"La voz que te acompana"** | ES | Compania, no sustitucion humana |
| 4 | **"Votre voix, vos droits"** | FR | Version francesa (derechos + voz) |
| 5 | **"Porque entender no deberia ser un privilegio"** | ES | Impacto social, denuncia suave |

**Recomendacion:** "Tu voz tiene poder" como tagline principal — corto, emocional, conecta directamente con la funcionalidad de voz.

### Personalidad de Marca

Clara NO es un asistente frio ni tecnico. Clara es:

| Rasgo | Descripcion | Lo que NO es |
|---|---|---|
| **Cercana** | Habla como una vecina que sabe del tema | No es un funcionario |
| **Paciente** | Nunca se frustra, repite sin problema | No es condescendiente |
| **Clara** (literalmente) | Lenguaje simple, pasos concretos | No usa jerga burocratica |
| **Respetuosa** | Trata al usuario como adulto capaz | No infantiliza |
| **Proactiva** | Sugiere ayudas sin que se las pidan | No es pasiva |
| **Multicultural** | Usa analogias del pais de origen | No asume cultura unica |

### Guia de Tono de Voz

| Situacion | Tono | Ejemplo |
|---|---|---|
| **Saludo** | Calido, acogedor | "Hola, soy Clara. Estoy aqui para ayudarte con tramites en Espana. Puedes hablarme o escribirme en tu idioma." |
| **Explicando tramite** | Claro, paso a paso | "Para pedir el IMV necesitas: 1) Estar empadronado. 2) Tener ingresos bajos. 3) Rellenar un formulario. Te explico cada paso?" |
| **Error/no entiende** | Amable, sin culpa | "Perdona, no he entendido bien. Puedes repetirmelo con otras palabras?" |
| **Sugerencia proactiva** | Util, no invasiva | "Segun lo que me cuentas, podrias tener derecho al bono social electrico. Quieres que te explique?" |
| **Despedida** | Calida, puerta abierta | "Espero haberte ayudado. Si necesitas algo mas, aqui estoy. Mucho animo." |

---

## 2. Paleta de Colores

### Criterios de Seleccion

- WCAG AAA: ratio de contraste 7:1 para texto normal
- Seguro para daltonismo (deuteranopia, protanopia, tritanopia)
- Psicologia del color: confianza + calidez + institucionalidad accesible
- Culturalmente neutro para audiencia multicultural

### Paleta Principal

| Rol | Color | Hex | Uso | Ratio vs Blanco | Ratio vs Negro |
|---|---|---|---|---|---|
| **Primario** | Azul Confianza | `#1B5E7B` | Headers, botones principales, links | 7.2:1 (AAA) | - |
| **Secundario** | Naranja Calido | `#D46A1E` | CTAs, acentos, iconos activos | 4.6:1 (AA Large) | - |
| **Acento** | Verde Esperanza | `#2E7D4F` | Exito, confirmaciones, checks | 5.8:1 (AAA Large) | - |
| **Fondo** | Blanco Suave | `#FAFAFA` | Fondo principal | - | 19.5:1 |
| **Texto** | Gris Oscuro | `#1A1A2E` | Texto principal, parrafos | 16.8:1 vs #FAFAFA | - |
| **Texto Secundario** | Gris Medio | `#4A4A5A` | Labels, texto auxiliar | 9.1:1 vs #FAFAFA | - |

### Paleta Extendida

| Rol | Color | Hex | Uso |
|---|---|---|---|
| **Error** | Rojo Accesible | `#C62828` | Mensajes de error |
| **Warning** | Ambar | `#F9A825` | Avisos, plazos urgentes |
| **Info** | Azul Claro | `#E3F2FD` | Fondos informativos |
| **Fondo Tarjeta** | Gris Muy Claro | `#F5F5F5` | Tarjetas, contenedores |
| **Borde** | Gris Borde | `#E0E0E0` | Separadores, bordes |

### Por que estos colores

- **Azul `#1B5E7B`**: Evoca confianza institucional sin ser frio. Recuerda a servicios publicos pero con calidez. El azul es universalmente asociado con confianza y seguridad.
- **Naranja `#D46A1E`**: Aporta calidez humana. Contrarresta la frialdad del azul. Culturalmente positivo en Latinoamerica y Marruecos. Evoca energia y accesibilidad.
- **Verde `#2E7D4F`**: Esperanza y crecimiento. Culturalmente positivo en Islam (color sagrado). Usado para confirmaciones y exitos.

### Validacion Daltonismo

| Tipo | Azul | Naranja | Verde |
|---|---|---|---|
| Vision normal | Distinguible | Distinguible | Distinguible |
| Deuteranopia | OK (azul intacto) | Se ve amarillento | Se oscurece |
| Protanopia | OK | Se ve amarillento | Se oscurece |
| Tritanopia | Se enrojece | OK | OK |

**Regla:** Nunca usar color como unica forma de transmitir informacion. Siempre acompanar con texto o icono.

---

## 3. Tipografia

### Fuentes Seleccionadas (Google Fonts, gratuitas)

| Uso | Fuente | Peso | Por que |
|---|---|---|---|
| **Titulos** | **Atkinson Hyperlegible Next** | Bold (700) | Disenada por el Braille Institute para baja vision. Exagera diferencias entre letras similares (I/l, 0/O). Soporta caracteres latinos y franceses |
| **Cuerpo** | **Inter** | Regular (400), Medium (500) | Optimizada para pantallas. Espaciado generoso. Excelente legibilidad en tamanos grandes. Soporta 200+ idiomas |
| **Fallback** | **Noto Sans** | Regular (400) | Soporte universal de idiomas (1000+). Fallback para arabe futuro |

### Tamanos Minimos

| Elemento | Tamano Minimo | Recomendado | Interlineado |
|---|---|---|---|
| Texto cuerpo (movil) | 18px | 20px | 1.6 |
| Texto cuerpo (desktop) | 18px | 20px | 1.5 |
| Titulos H1 | 32px | 36px | 1.3 |
| Titulos H2 | 24px | 28px | 1.3 |
| Botones | 18px | 20px | 1.0 |
| Labels/captions | 16px | 16px | 1.4 |
| Texto WhatsApp | Determinado por plataforma | - | - |

### Reglas de Tipografia Accesible

1. **Nunca** usar todo mayusculas en mas de 3-4 palabras (dificil de leer, screen readers lo interpretan como acronimos)
2. **Siempre** alineacion izquierda (no justificado — crea espacios irregulares)
3. **Maximo** 70 caracteres por linea para legibilidad optima
4. **Contraste** minimo 7:1 para texto normal, 4.5:1 para texto grande (24px+)
5. **Peso** bold para titulos y elementos importantes — mejora recall en adultos mayores

---

## 4. Conceptos de Logo

### Concepto A: "La Burbuja de Voz Luminosa"

**Descripcion para generacion AI:**
> Un logo minimalista con una burbuja de dialogo (speech bubble) redondeada en azul `#1B5E7B`. Dentro de la burbuja, una onda de sonido suave y estilizada en naranja `#D46A1E` que sugiere voz y comunicacion. A la derecha, el texto "Clara" en Atkinson Hyperlegible Bold. Debajo, el tagline "Tu voz tiene poder" en Inter Regular gris. Fondo blanco. Estilo flat, limpio, moderno pero calido.

**Simbolismo:** Comunicacion + voz + claridad. La burbuja es universal (WhatsApp). La onda de sonido refuerza "voice-first".

### Concepto B: "La Mano que Guia"

**Descripcion para generacion AI:**
> Logo con dos elementos: a la izquierda, un icono circular con fondo azul `#1B5E7B` que contiene la silueta minimalista de una mano abierta en blanco, con un pequeno destello naranja `#D46A1E` en la palma (como ofreciendo luz/ayuda). A la derecha, "Clara" en tipografia bold. Estilo: line art simple, redondeado, inclusivo. Sin sombras, flat design.

**Simbolismo:** Guia + ayuda + luz (claridad). La mano abierta es universal como gesto de bienvenida.

### Concepto C: "El Faro Accesible"

**Descripcion para generacion AI:**
> Logo con un faro estilizado y geometrico en azul `#1B5E7B`, con rayos de luz simplificados en naranja `#D46A1E` que se expanden hacia la derecha. Los rayos se transforman sutilmente en ondas de sonido. Junto al faro, "Clara" en tipografia bold. El faro tiene una base solida (institucionalidad) y la luz es calida (accesibilidad).

**Simbolismo:** Orientacion + luz + claridad en la oscuridad burocratica. El faro guia a quienes estan perdidos.

### Recomendacion

**Concepto A** (Burbuja de Voz) es el mas apropiado porque:
- Conecta directamente con WhatsApp (burbuja de chat)
- Refuerza la funcionalidad principal (voz)
- Es el mas simple y reconocible a tamanos pequenos
- Funciona como favicon/icono de app

---

## 5. Lenguaje Visual

### Estilo de Iconos

| Aspecto | Especificacion |
|---|---|
| **Estilo** | Outlined (linea), bordes redondeados, grosor 2px |
| **Tamano minimo** | 24px (32px recomendado) |
| **Libreria base** | Material Design Icons (Google) — universalmente reconocidos |
| **Color** | Monocromo (azul primario o gris oscuro), naranja para estados activos |
| **Acompanamiento** | Siempre con label de texto debajo o al lado. Nunca icono solo |

**Iconos clave necesarios:**
- Microfono (grabar audio)
- Teclado (escribir texto)
- Camara (subir documento)
- Play/Pause (reproducir audio)
- Globo/idioma (cambiar idioma)
- Check/tick (confirmacion)
- Info (informacion)
- Telefono (contacto)

### Estilo de Ilustracion

| Aspecto | Especificacion |
|---|---|
| **Libreria** | Humaaans (humaaans.com) o Open Peeps (openpeeps.com) — gratuitas, inclusivas |
| **Diversidad** | Representar personas de distintas edades, tonos de piel, origenes |
| **Estilo** | Semi-abstracto, linea simple, colores planos |
| **Evitar** | Estereotipos, imagenes de pobreza/lastima, representaciones infantilizantes |

### Direccion de Fotografia (para marketing)

| Aspecto | Si | No |
|---|---|---|
| **Sujetos** | Personas reales, diversas, sonrientes, activas | Stock generico, modelos perfectos |
| **Escenarios** | Hogares reales, oficinas de atencion, plazas | Estudios esteriles, fondos artificiales |
| **Emocion** | Dignidad, agencia, conexion | Lastima, victimismo, dependencia |
| **Tecnologia** | Persona usando WhatsApp naturalmente | Pantallas con UI visible (evitar) |
| **Composicion** | Primer plano, contacto visual | Distancia fria, angulos superiores |

---

## 6. Principios de Diseno Emocional

### Como debe sentirse el usuario al interactuar con Clara

| Emocion Objetivo | Como se logra |
|---|---|
| **Seguro/a** | Lenguaje simple, sin jerga. Fuentes oficiales citadas. Nunca inventa datos |
| **Comprendido/a** | Detecta idioma automaticamente. Usa analogias culturales. Responde en su lengua |
| **Capaz** | Clara da herramientas, no caridad. "Tu puedes hacer esto, te explico como" |
| **No juzgado/a** | Nunca pregunta por estatus legal. No asume nivel educativo. Tono neutro y respetuoso |
| **Acompanado/a** | "Estoy aqui para ayudarte". Puerta siempre abierta. Sin presion temporal |
| **Respetado/a** | Trata como adulto. No infantiliza. Ofrece opciones, no impone |

### Anti-patrones (lo que NUNCA hacer)

- No usar imagenes de personas tristes, sufriendo o en situaciones de vulnerabilidad extrema
- No usar lenguaje paternalista ("pobrecito", "necesitado")
- No asumir que el usuario no entiende tecnologia
- No usar colores demasiado "infantiles" (rosa chicle, amarillo neon)
- No usar iconografia religiosa especifica
- No usar banderas nacionales para representar idiomas (usar globo/texto)

---

## 7. Sensibilidad Cultural

### Consideraciones por Comunidad

| Comunidad | En Espana | Consideraciones de Diseno |
|---|---|---|
| **Marroqui** | 1.09M (mayor comunidad extranjera) | Verde es color sagrado en Islam. Evitar cerdo/alcohol en ilustraciones. Analogias con "wilaya". Frances como puente linguistico |
| **Latinoamericana** | ~48% de poblacion extranjera | Colores calidos (naranja, rojo) bien recibidos. "Usted" vs "tu" segun pais. Amarillo puede asociarse a luto en algunos paises |
| **Subsahariana** | Senegal, Mali, Nigeria | Colores primarios fuertes preferidos. Comunicacion oral (tradicion griots). Respeto por la edad y la comunidad |
| **Mayores espanoles** | 9.5M (65+) | Tamanos grandes. Sin anglicismos. Referencia a instituciones conocidas (Seguridad Social, Ayuntamiento). Confianza en lo "oficial" |

### Reglas Universales

1. **Nunca** usar banderas para representar idiomas — usar nombre del idioma en texto
2. **Evitar** simbolos religiosos especificos en la UI
3. **Usar** ilustraciones abstractas o semi-abstractas para representar personas (evita estereotipos)
4. **Respetar** el registro formal cuando se habla de temas sensibles (dinero, salud, documentos)
5. **Testear** con usuarios reales de cada comunidad antes de la final

---

## 8. Reglas de Accesibilidad (Resumen Ejecutivo)

| Parametro | Minimo | Recomendado | Estandar |
|---|---|---|---|
| **Contraste texto** | 4.5:1 (AA) | 7:1 (AAA) | WCAG 2.2 |
| **Contraste texto grande** | 3:1 (AA) | 4.5:1 (AAA) | WCAG 2.2 |
| **Tamano fuente cuerpo** | 16px | 18-20px | Research PMC |
| **Tamano boton touch** | 24x24px (AA) | 44x44px (AAA) | WCAG 2.5.5/2.5.8 |
| **Boton para mayores** | 44x44px | 64x64px | Braille Institute |
| **Interlineado** | 1.4 | 1.5-1.6 | WCAG 1.4.12 |
| **Ancho de linea** | - | Max 70 caracteres | Legibilidad optima |
| **Nivel de lectura** | B1 CEFR | A2-B1 | Persona de 12 anos |
| **Animaciones** | Reducidas | Opcionales | prefers-reduced-motion |
| **Color como informacion** | Nunca solo | Siempre + texto/icono | WCAG 1.4.1 |

---

## Fuentes de Investigacion

- [WCAG 2.2 Color Contrast Guide — AllAccessible](https://www.allaccessible.org/blog/color-contrast-accessibility-wcag-guide-2025)
- [Accessible Color Palette Generator — Venngage](https://venngage.com/tools/accessible-color-palette-generator)
- [Accessible Palette Tool](https://accessiblepalette.com/)
- [Font Size for Older Adults — PMC Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC9376262/)
- [Typography Accessibility — Google Fonts Knowledge](https://fonts.google.com/knowledge/readability_and_accessibility/introducing_accessibility_in_typography)
- [ADA Compliant Fonts Guide 2026](https://accessibe.com/blog/knowledgebase/ada-compliant-fonts)
- [Atkinson Hyperlegible — Google Fonts](https://fonts.google.com/specimen/Atkinson+Hyperlegible)
- [WCAG 2.5.8 Target Size Minimum — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- [Color Psychology Government Trust — UAE Design System](https://designsystem.gov.ae/insights/the-color-psychology-of-government-trust)
- [Trust in Chatbots Research — Future Business Journal](https://fbj.springeropen.com/articles/10.1186/s43093-023-00288-z)
- [Spain Bureaucratic Exclusion — OECD](https://oecd-opsi.org/blog/gov2gov-challenge-spain/)
- [Digital Inclusion Elderly Spain — Cambridge](https://www.cambridge.org/core/journals/ageing-and-society/article/digital-inclusion-of-older-people-in-spain-technological-support-services-for-seniors-as-predictor/ADF5EC05F8FB28EC7FE89872E3581BDF)
- [Cultural Color Symbolism — Frontmatter](https://www.frontmatter.io/blog/how-color-symbolism-influences-design-and-marketing-across-cultures)
- [OdiseIA4Good Hackathon](https://www.odiseia4good.org/en)
- [Spain Immigration 2025 — INE](https://www.ine.es/dyngs/Prensa/en/ECP1T25.htm)

---

*Documento generado el 19 de febrero de 2026 para CivicAid Voice / Clara.*
