# Tendencias de Diseno 2025-2026 & Referencias — Clara

> **Fecha:** 19 Feb 2026
> **Enfoque:** Civic tech, accesibilidad, impacto social, IA conversacional

---

## 1. Tendencias Relevantes para Clara

### 1A. Accesibilidad como Requisito Legal (No Opcional)

La European Accessibility Act (EAA) entra en vigor en junio 2025. Todos los servicios digitales en la UE deben cumplir WCAG 2.1 AA minimo. Clara ya esta disenada para AAA, lo que nos posiciona por delante de la regulacion.

**Aplicacion:** Comunicar en el pitch que Clara cumple EAA desde el dia 1. Diferenciador ante el jurado.

### 1B. Voice-First Interfaces

El 78% de mayores de 65 en Espana usa WhatsApp. La tendencia global es hacia interfaces que priorizan voz sobre texto, especialmente para poblaciones con baja alfabetizacion digital. Google, Apple y Meta estan invirtiendo en voice assistants conversacionales.

**Aplicacion:** Clara ES voice-first por diseno. No es un chatbot de texto al que le anadimos voz — es un asistente de voz al que le anadimos texto como fallback.

### 1C. Diseno Cognitivamente Accesible

Va mas alla de WCAG visual. Incluye: lenguaje simple, flujos predecibles, sin sorpresas, sin sobrecarga de opciones, feedback inmediato, recovery facil de errores. Investigaciones de IBM y W3C especificas para envejecimiento.

**Aplicacion:** Clara nunca da mas de 3 opciones. Siempre responde en menos de 200 palabras. Siempre ofrece un "siguiente paso" claro.

### 1D. IA Transparente y Etica

Post-AI Act de la UE, la tendencia es hacia IA que explica sus limitaciones: "No tengo esa informacion verificada" en lugar de inventar. Clara ya tiene guardrails anti-alucinacion y cita fuentes oficiales.

**Aplicacion:** Comunicar en el pitch: "Clara NUNCA inventa. Si no sabe, lo dice y te da el telefono oficial."

### 1E. Community-Centered Design

Diseno CON las comunidades, no PARA ellas. Los mejores productos civic tech (Code for America, GOV.UK) co-crean con usuarios reales. Aunque en un hackathon no hay tiempo para co-creacion completa, podemos mencionar que el diseno esta basado en datos reales de las comunidades.

**Aplicacion:** Los 3 casos demo (Ahmed, Maria, Fatima) estan basados en perfiles demograficos reales del INE.

---

## 2. Ejemplos de Referencia (Civic Tech con Buen Diseno)

### GOV.UK Design System (Reino Unido)

| Aspecto | Lo que hacen bien | Aplicacion para Clara |
|---|---|---|
| **Lenguaje** | "Content design" — todo en lenguaje de 9 anos | Clara habla para nivel de 12 anos |
| **Patrones** | Componentes reutilizables, accesibles | Nuestros botones grandes siguen este patron |
| **Principios** | "Start with user needs", "Do less" | Clara hace 1 cosa bien: orientar en tramites |
| **URL** | design-system.service.gov.uk | Referencia para el jurado |

### Decidim Barcelona (Espana)

| Aspecto | Lo que hacen bien | Aplicacion para Clara |
|---|---|---|
| **Participacion** | Plataforma de democracia participativa accesible | Concepto de "hacer la administracion accesible" |
| **Diseno** | UI limpia, multilingue (catalan, espanol, ingles) | Nuestro selector de idioma ES/FR |
| **Open source** | Codigo abierto, replicable | Clara podria ser open source post-hackathon |

### Code for America (EEUU)

| Aspecto | Lo que hacen bien | Aplicacion para Clara |
|---|---|---|
| **Mision** | "Government can work for the people, by the people, in the digital age" | Misma filosofia: gobierno accesible para todos |
| **GetCalFresh** | Simplifica solicitud de food stamps | Clara simplifica IMV y empadronamiento |
| **Datos** | Miden impacto con datos reales | Nuestros datos: 3.2M, 9.5M, 78% |

---

## 3. Patrones de Diseno WhatsApp

### Mejores Practicas de UX en WhatsApp Business

| Patron | Descripcion | Clara lo implementa |
|---|---|---|
| **Saludo inmediato** | Responder en <5s con mensaje de bienvenida | ACK TwiML en <1s |
| **Botones de respuesta rapida** | 3 opciones maximo, texto corto | "IMV / Empadronamiento / Tarjeta sanitaria" |
| **Mensajes estructurados** | Pasos numerados, listas claras | "1. Ve al ayuntamiento. 2. Lleva tu pasaporte..." |
| **Emojis con moderacion** | 1-2 por mensaje, significativos | Check para confirmacion, telefono para contacto |
| **Cierre con fuente** | Siempre citar la fuente oficial | "Mas info: seg-social.es" |
| **Templates aprobados** | Mensajes pre-aprobados por WhatsApp Business | Para futuro post-hackathon |

### Anti-Patrones (Lo que NO Hacer en WhatsApp)

- No enviar muros de texto (max 200 palabras)
- No usar menus complejos con numeros ("Escribe 1 para...")
- No enviar mensajes no solicitados (spam)
- No pedir datos sensibles (DNI, cuenta bancaria) por chat
- No usar lenguaje demasiado formal ni demasiado informal

---

## 4. Psicologia del Color para Confianza

### Investigacion Aplicada

| Color | Asociacion Universal | Aplicacion en Clara |
|---|---|---|
| **Azul** | Confianza, seguridad, institucionalidad | Color primario — evoca servicios publicos |
| **Naranja** | Calidez, energia, accesibilidad, creatividad | Color secundario — humaniza la IA |
| **Verde** | Esperanza, salud, naturaleza, Islam (sagrado) | Confirmaciones — culturalmente positivo para audiencia marroqui |
| **Blanco** | Limpieza, claridad, espacio | Fondo — reduce carga cognitiva |
| **Gris oscuro** | Seriedad, legibilidad | Texto — mejor que negro puro para pantalla |

### Combinaciones que Transmiten Confianza + Calidez

La combinacion azul + naranja es optima porque:
1. **Complementarios:** Alto contraste visual natural
2. **Balance emocional:** Azul = seguridad, naranja = cercanla
3. **Culturalmente seguro:** Sin connotaciones negativas en ninguna de las culturas objetivo
4. **Accesible:** Distinguible para la mayoria de tipos de daltonismo

---

## 5. Ilustracion Inclusiva

### Librerias Recomendadas (Gratuitas)

| Libreria | Estilo | Diversidad | URL |
|---|---|---|---|
| **Humaaans** | Semi-abstracto, mix-and-match | Alta (tonos piel, ropa, accesorios) | humaaans.com |
| **Open Peeps** | Hand-drawn, expresivo | Alta | openpeeps.com |
| **Blush** | Varios estilos, customizable | Alta | blush.design |
| **unDraw** | Flat, vectorial | Media (mas abstracto) | undraw.co |

### Reglas para Ilustraciones Inclusivas

1. **Diversidad** de tonos de piel, edades, tipos de cuerpo
2. **Sin estereotipos**: no asociar pais con profesion/situacion
3. **Contextos positivos**: personas activas, sonrientes, con agencia
4. **Evitar** hipanos (religious symbols, political imagery, poverty stereotypes)
5. **Consistencia** de estilo a traves de todos los materiales

---

## 6. Iconografia Universal

### Estandares Recomendados

| Sistema | Uso | Por que |
|---|---|---|
| **Material Design Icons** | UI web/app | 2000+ iconos, universal, Google standard |
| **ISO 7001** | Senaletica publica | Universalmente comprendidos sin texto |
| **Emoji Unicode** | WhatsApp | Ya conocidos por los usuarios |

### Iconos Clave para Clara

| Concepto | Icono Material | Emoji WA | Significado |
|---|---|---|---|
| Hablar/voz | `mic` | 🎤 | Grabar audio |
| Escribir | `keyboard` | ⌨️ | Modo texto |
| Documento | `description` | 📄 | Subir foto |
| Idioma | `translate` | 🌐 | Cambiar idioma |
| Ayuda | `help_outline` | ❓ | Pedir ayuda |
| Exito | `check_circle` | ✅ | Confirmacion |
| Telefono | `phone` | 📞 | Llamar para mas info |
| Web | `open_in_new` | 🔗 | Ir a fuente oficial |

---

## 7. Principios de Diseno Sintetizados para Clara

### Los 8 Principios

1. **Voz primero, texto segundo** — La interaccion principal es por voz. El texto es apoyo.
2. **Cero barreras de entrada** — No descargar app, no crear cuenta, no aprender interfaz nueva.
3. **Culturalmente consciente** — Analogias del pais de origen, idioma detectado automaticamente.
4. **Transparentemente limitada** — Clara dice cuando no sabe. Nunca inventa.
5. **Visualmente accesible** — AAA WCAG, 18px minimo, 44px botones, alto contraste.
6. **Cognitivamente simple** — Max 3 opciones, max 200 palabras, pasos numerados.
7. **Emocionalmente segura** — Nunca juzga, nunca presiona, siempre ofrece salida.
8. **Mediblemente impactante** — Datos reales, fuentes verificadas, impacto cuantificable.

---

## Fuentes Principales

- [Digital Accessibility Trends 2026 — InclusiveASL](https://inclusiveasl.com/accessibility/top-digital-accessibility-trends-to-watch-in-2026/)
- [State of Digital Accessibility 2025-2026 — Level Access](https://www.levelaccess.com/resources/state-of-digital-accessibility-report-2025-2026/)
- [IBM Accessible Design Aging Population](https://www.ibm.com/think/insights/accessible-design-aging-population)
- [GOV.UK Design System](https://design-system.service.gov.uk/)
- [GOV.UK Design Principles](https://www.gov.uk/guidance/government-design-principles)
- [Civic Design Systems — MaxiomTech](https://www.maxiomtech.com/accessible-ux-civic-design-systems/)
- [CivicPatterns](http://civicpatterns.org/)
- [Decidim Barcelona](https://decidim.org/)
- [Code for America](https://codeforamerica.org/about-us/)
- [WhatsApp Bot Design — Landbot](https://landbot.io/blog/design-whatsapp-bot-dialogue)
- [AI Chatbot Trends 2026 — OscarChat](https://www.oscarchat.ai/blog/10-ai-chatbot-trends-2026/)
- [UX/UI Design Trends 2026 — Prototypr](https://blog.prototypr.io/ux-ui-design-trends-for-2026)
- [Chatbot UI Examples — Eleken](https://www.eleken.co/blog-posts/chatbot-ui-examples)
- [Cross-Cultural Design — Gapsy Studio](https://gapsystudio.com/blog/cross-cultural-design/)
- [Inclusive Illustrations — Atlassian](https://www.atlassian.com/blog/inside-atlassian/designing-inclusive-illustrations-at-atlassian)
- [Humaaans](https://www.humaaans.com/)
- [Open Peeps](https://www.openpeeps.com/)
- [Material Design Icons](https://developers.google.com/fonts/docs/material_icons)
- [ISO 7001 Public Information Symbols](https://en.wikipedia.org/wiki/ISO_7001)
- [Accessible Palette Tool](https://accessiblepalette.com/)

---

*Documento generado el 19 de febrero de 2026.*
