# Phase 4 — UX & Accessibility Analysis for Clara

**Author:** Agent A — UX & Accessibility Lead
**Date:** 2026-02-13
**Status:** Research & Design (no code changes)
**Scope:** Response tone, accessibility, multilingual UX, conversation flow redesign

---

## Table of Contents

1. [Web Research Findings](#1-web-research-findings)
2. [User Personas](#2-user-personas)
3. [Three Response Style Proposals](#3-three-response-style-proposals)
4. [Conversation Flow Templates](#4-conversation-flow-templates-sin-jerga)
5. [Clarification System](#5-clarification-system)
6. [Risks](#6-risks)
7. [Success Criteria](#7-success-criteria)

---

## 1. Web Research Findings

### Reference 1: UNHCR + Turn.io — WhatsApp for Refugees

**Source:** [UNHCR Turn.io WhatsApp Case Study](https://www.turn.io/case-studies/to-help-build-a-better-future-for-refugees-unhcrs-chat-services-suit-their-preferences-meet-their-needs-and-safeguard-their-data)

**What they did:** UNHCR deployed WhatsApp-based chatbots through Turn.io in multiple countries (Algeria, Ecuador, Brazil) to provide refugees with information about asylum procedures, registration, healthcare, education, and GBV support. The system was built on WhatsApp Business API with privacy-first design.

**What worked:**
- In Ecuador, ALL text-based messages were converted to audio to serve visually impaired users and those with literacy challenges — this is directly relevant to Clara's gTTS pipeline.
- In Latin America, voice and audio notes were commonly used and so these were included as a primary interaction mode, not an afterthought.
- Country-specific contextualization with user testing in each locale was essential — one-size-fits-all failed.
- Triage system combined automated responses with human-assisted responses for complex cases.

**What we can learn for Clara:**
- Audio output should be the DEFAULT, not optional. Every response should have an audio companion sent alongside text.
- Localize by community, not just by language. A Moroccan user in Madrid has different needs than a Colombian user in Barcelona.
- Build a clear escalation path: bot -> human agent. Even "call this number" is an escalation.

### Reference 2: UNHCR La Chama — Combating Misinformation via WhatsApp

**Source:** [UNHCR La Chama Chatbot](https://www.unhcr.org/digitalstrategy/case-studies/one-message-at-a-time-la-chama-chatbot-combats-falsehoods/)

**What they did:** La Chama is a WhatsApp chatbot launched in 2021 in Boa Vista, Brazil, serving 10,000+ displaced Venezuelans. It provides verified, timely information to combat misinformation about immigration procedures and rights.

**What worked:**
- Named persona ("La Chama") with a relatable identity for the target community.
- Focus on combating specific false rumors ("they'll deport you if you register") with gentle corrections.
- Messaging designed for people who distrust authorities.

**What we can learn for Clara:**
- Clara's persona needs warmth and cultural familiarity. "Clara" is a good name but the tone in the current templates is robotic.
- Explicitly address common fears: "No te van a deportar por empadronarte" (they won't deport you for registering).
- Proactive myth-busting should be part of the conversation flow, not reactive.

### Reference 3: MITRE Chatbot Accessibility Playbook

**Source:** [MITRE Chatbot Accessibility Playbook](https://mitre.github.io/chatbot-accessibility-playbook/)

**What they did:** MITRE created a comprehensive playbook with checklists for designing and developing accessible chatbots for U.S. federal government services. It covers WCAG compliance, cognitive accessibility (W3C COGA TF recommendations), and specific guidance for screen readers, keyboard-only users, and people with cognitive disabilities.

**Key guidelines:**
- Use simple messages: say exactly what you mean. Avoid poetic, metaphorical, or ambiguous language.
- Target a lower secondary education reading level.
- Never use figures of speech, idioms, exaggerations, or turns of phrase.
- Provide the same information through multiple channels (text + audio).
- Allow users to control the pace of information delivery — do not dump everything at once.
- Use consistent vocabulary throughout all interactions (don't call the same thing by different names).

**What we can learn for Clara:**
- The current system prompt says "nivel persona de 12 anos" which aligns with MITRE's "lower secondary education level" — but the cached responses do NOT follow this (e.g., "silencio administrativo desestimatorio" is university-level language).
- Need a jargon dictionary that maps legal terms to plain language equivalents.
- Consistent vocabulary: always call "empadronamiento" the same thing, with a parenthetical explanation the first time: "empadronamiento (registro en tu ciudad)."

### Reference 4: Chatbots in Humanitarian Contexts — Practitioner Experiences

**Source:** [CEA Hub — Chatbots in Humanitarian Contexts (PDF)](https://communityengagementhub.org/wp-content/uploads/sites/2/2023/06/20230623_CEA_Chatbots.pdf)

**What they did:** A cross-organizational study of chatbot deployments in humanitarian settings, compiling lessons from UNHCR, UNICEF U-Report, Red Cross, and other agencies. The report covers design principles, failure modes, and best practices for reaching vulnerable populations through messaging platforms.

**Key findings:**
- Users often test the bot with "hello" or a random word before trusting it. The greeting flow is critical for setting expectations.
- Users who receive an error or confusing response on their first interaction rarely come back.
- Multi-step flows that require users to remember previous messages fail for low-literacy users.
- Chatbots that offer numbered menu options (press 1, 2, 3) perform much better for low-literacy users than free-text input.

**What we can learn for Clara:**
- The greeting response is the most important message Clara sends. It must set expectations, build trust, and make the next action crystal clear.
- Numbered menus reduce cognitive load. "Escribe 1, 2 o 3" is more accessible than "Sobre que te gustaria saber?"
- Never ask open-ended questions to users who may struggle to articulate their needs.

### Reference 5: Arabic RTL Chatbots and Multilingual UX

**Sources:**
- [Engati — Arabic Chatbot Guide](https://www.engati.ai/blog/arabic-chatbots)
- [Axis SoftMedia — RTL Chatbots](https://www.axissoftmedia.com/service-details/rtl-chatbots)
- [Invent — Multilingual AI Agents Best Practices 2025](https://www.useinvent.com/blog/how-to-build-effective-multilingual-ai-agents-2025-best-practices-guide)

**Key considerations for Arabic support:**
- Arabic is NOT one language. Moroccan Arabic (Darija) is the most relevant dialect for Spain's immigrant population, and it differs significantly from Modern Standard Arabic (MSA). Gulf Arabic, Egyptian, and Levantine are distinct languages in practice.
- WhatsApp handles RTL text rendering natively — Clara does not need to worry about RTL layout. The platform manages script direction.
- However, code-switching is extremely common: a Moroccan user might start in Darija, switch to French, then to Spanish, all in one conversation. The language detection system must handle this gracefully.
- Culturally sensitive expressions matter: greetings, politeness markers, and religious phrases (Bismillah, Inshallah) should be recognized and respected, not treated as noise.

**What we can learn for Clara:**
- For Arabic (Darija) support, Gemini 1.5 Flash already has reasonable Arabic capability, but the keyword detection in `detect_lang.py` has zero Arabic keywords. This needs an `_AR_KEYWORDS` set.
- WhatsApp handles RTL natively, so the main work is in language detection + response generation, not rendering.
- Code-switching detection is the hardest problem. A pragmatic approach: detect the dominant language per message, respond in that language, and always offer "Puedo hablar en espanol / Je parle francais / ana nahki bel 3arabiya" as a menu option.

---

## 2. User Personas

### Persona Table

| # | Name | Age | Origin | Languages | Tech Level | Primary Fear | Preferred I/O | Key Need |
|---|------|-----|--------|-----------|------------|-------------|---------------|----------|
| 1 | **Ahmed** | 32 | Morocco | Darija, French, basic Spanish | Medium (uses WhatsApp daily) | Deportation, losing papers, being scammed | Voice notes in, text + audio out | Clear steps for empadronamiento without a rental contract |
| 2 | **Carmen** | 74 | Spain | Spanish | Low (has WhatsApp but daughter set it up) | Making a mistake, "breaking" the phone | Voice notes in, audio out | Help renewing tarjeta sanitaria after moving neighborhoods |
| 3 | **Mamadou** | 28 | Senegal | Wolof, French, no Spanish | Low-medium (uses WhatsApp for calls) | Not understanding official letters, bureaucratic rejection | Voice notes in French, audio out | Understanding an official letter about IMV status |
| 4 | **Elena** | 45 | Spain | Spanish | High (uses screen reader JAWS daily) | Inaccessible information, being patronized | Text in, text out (screen reader optimized) | Requesting IMV online, needs accessible step-by-step |
| 5 | **David** | 38 | Colombia | Spanish | Medium | Mishearing information, missing phone calls | Text in, text out (avoids audio) | Getting tarjeta sanitaria after arriving with a work visa |
| 6 | **Fatima** | 41 | Syria | Arabic, basic French, no Spanish | Low (WhatsApp via family member) | Everything — does not trust institutions, past trauma | Voice in Arabic, audio + text out | Empadronamiento + tarjeta sanitaria for herself and 3 children |

### Detailed Persona Profiles

#### Persona 1 — Ahmed (Immigrant, recently arrived)

**Background:** Arrived in Madrid 4 months ago from Casablanca. Works informally in construction. Lives with 3 other Moroccan men in a shared flat. The landlord refuses to put his name on the rental contract.

**Tech behavior:** Uses WhatsApp constantly — voice notes, photos, video calls with family. Comfortable with technology but everything is in French or Darija. Has never interacted with a chatbot.

**Fears:** "If I go to register (empadronar), will they check my papers? Will they call the police?" Has heard conflicting stories from friends. One friend was successfully empadronado without a contract; another says it is impossible.

**What Clara must do:** Reassure that empadronamiento is a RIGHT even without a contract. Explain the "declaracion responsable" in simple terms. Give the exact address and phone number. Offer the information in French.

**Failure mode:** If Clara uses terms like "declaracion responsable del titular de la vivienda" without explanation, Ahmed will not understand and will give up.

#### Persona 2 — Carmen (Elderly, low tech literacy)

**Background:** Lives alone in Vallecas, Madrid. Her husband died 2 years ago. Her daughter helped her install WhatsApp. She sends voice notes to her grandchildren but has never typed a message longer than "ok."

**Tech behavior:** Knows how to send voice notes and photos. Cannot type well — arthritic fingers, small keyboard. Reads very slowly. Gets confused by long messages and scrolls past important information.

**Fears:** "I'm going to press the wrong thing and delete everything." Afraid of official-sounding language because it reminds her of tax paperwork she doesn't understand.

**What Clara must do:** Send very short messages (3 lines maximum). Always send an audio response. Use "usted" (formal you) but in warm, grandmother-friendly language. Never ask her to type; suggest she send a voice note instead.

**Failure mode:** If Clara sends a 200-word response with numbered steps and bold text, Carmen will not read it and will call her daughter instead.

#### Persona 3 — Mamadou (Low literacy, French-speaking)

**Background:** Arrived from Dakar 8 months ago. Completed primary school in Wolof; reads French with difficulty. Works in agriculture in Murcia. Does not speak Spanish beyond "hola" and "gracias."

**Tech behavior:** Uses WhatsApp mainly for audio calls and voice notes. Can navigate the app but does not read long messages. Prefers audio in all interactions.

**Fears:** Receiving an official letter he cannot read. Being rejected for a tramite because he didn't understand a requirement.

**What Clara must do:** Detect French immediately. Keep text responses under 80 words. ALWAYS send audio alongside text. Use analogies to Senegalese/French bureaucracy ("c'est comme quand tu vas a la mairie au Senegal"). Never assume literacy.

**Failure mode:** If Clara sends a text-only response in Spanish with legal terms, Mamadou will not engage again.

#### Persona 4 — Elena (Blind, screen reader user)

**Background:** Born in Madrid. Lost her sight at age 30 due to retinitis pigmentosa. Is a professional translator. Uses iPhone with VoiceOver and JAWS on her computer. Fully independent and tech-savvy.

**Tech behavior:** Expert WhatsApp user. Types quickly with the accessibility keyboard. Screen reader reads every message aloud. Understands complex information but needs it structured for linear audio consumption.

**Fears:** Being patronized. Receiving information in a format that doesn't work with her screen reader (images of text, PDFs without alt text). Emoji-heavy messages that VoiceOver reads as "smiling face with open mouth" repeatedly.

**What Clara must do:** Minimize emojis (VoiceOver reads each one aloud, interrupting the flow). Structure responses as numbered lists — screen readers handle these well. Avoid using bold text with asterisks (**word**) because some screen readers read the asterisks. Use plain numbered lists instead. Never send critical information ONLY as an image.

**Failure mode:** Current template "Un momento, estoy procesando tu mensaje... (hourglass emoji)" — VoiceOver reads this as "Un momento, estoy procesando tu mensaje punto punto punto reloj de arena" which is confusing and slow.

#### Persona 5 — David (Deaf/hard of hearing)

**Background:** Colombian, arrived in Madrid with a work visa 2 months ago. Profoundly deaf since birth. Communicates in written Spanish and Colombian Sign Language (LSC). Does not use audio at all.

**Tech behavior:** Excellent with text and visual content. Uses WhatsApp text exclusively. Fast reader. Dislikes being offered audio alternatives he cannot use.

**Fears:** Missing important information delivered by phone. Being told "call this number" as the only option when he physically cannot call.

**What Clara must do:** Never suggest "call this number" as the ONLY option — always include a text/web alternative first. Provide online URLs alongside phone numbers. Use clear, structured text. Do not send audio-only responses without text.

**Failure mode:** Current `llm_fail` template says "Prueba de nuevo en unos segundos, o consulta directamente en: IMV: 900 20 22 22" — David CANNOT call. This is exclusionary.

#### Persona 6 — Fatima (Anxious, distrustful, Arabic-speaking)

**Background:** Syrian refugee who arrived via family reunification. Speaks Arabic (Levantine) and basic French learned in Lebanon. No Spanish. Has three children aged 4, 7, and 11. Her husband works double shifts and is unreachable during the day.

**Tech behavior:** Can use WhatsApp but only with help from her 11-year-old, who reads and translates for her. Sends voice notes in Arabic.

**Fears:** Deep distrust of institutions based on war experiences. Afraid that registering will put her family on a list. Afraid that asking for help will be seen as weakness or grounds for having children taken away.

**What Clara must do:** Be extraordinarily gentle. Never use institutional language. Frame everything as a right, not a favor. Explain that empadronamiento PROTECTS the family. Offer Arabic + French. Send audio in Arabic if possible. Keep messages to 2-3 sentences maximum.

**Failure mode:** If Clara's first response feels bureaucratic or cold, Fatima will delete the chat and never try again.

---

## 3. Three Response Style Proposals

### Idea A: Ultra-Short Mode

**Concept:** Every response is maximum 3 lines + a prompt to ask for more detail. Uses numbered menu options for navigation. Designed for Personas 2 (Carmen), 3 (Mamadou), and 6 (Fatima).

**Example — IMV Query:**
```
Clara: El IMV es una ayuda de dinero del gobierno para personas con pocos recursos.

Puede ser hasta 604 euros al mes.

Escribe 1 para saber como pedirlo
Escribe 2 para saber que papeles necesitas
Escribe 3 para que te lea la respuesta en audio
```

**Example — Greeting:**
```
Clara: Hola, soy Clara. Te ayudo con tramites en Espana.

Escribe 1 - Ayuda de dinero (IMV)
Escribe 2 - Registro en tu ciudad (empadronamiento)
Escribe 3 - Ir al medico (tarjeta sanitaria)
```

| Dimension | Assessment |
|-----------|------------|
| **Pros** | Lowest cognitive load. Works for all literacy levels. Fast to read. Screen reader friendly (numbered lists). Reduces anxiety ("I only need to read 3 lines"). |
| **Cons** | May feel too transactional. Loses warmth. Multi-step conversations take longer. Advanced users (Elena) may find it patronizing. |
| **Implementation complexity** | LOW — modify `system_prompt.py` rules + restructure `demo_cache.json` entries. Add numbered-option parsing to pipeline. |
| **Accessibility score** | 9/10 — excellent for low literacy, screen readers, elderly. Minus 1 for lacking emotional warmth. |

### Idea B: Guided Step-by-Step Mode

**Concept:** Clara breaks every answer into micro-steps, delivering one step at a time and waiting for the user to say "siguiente" (next) or "ok" before continuing. Includes empathetic openers and closers. Designed for Personas 1 (Ahmed), 2 (Carmen), and 6 (Fatima).

**Example — IMV Query (multi-message flow):**
```
Clara: Entiendo que necesitas informacion sobre el IMV. Es normal tener dudas, es un tramite importante pero yo te voy a ir guiando paso a paso.

Primero te explico que es. El IMV es una ayuda de dinero que da el gobierno a personas que tienen pocos ingresos. Es tu derecho pedirlo.

Escribe "ok" o envia un audio y sigo con el siguiente paso.
```
*(User sends "ok")*
```
Clara: Bien. Para pedir el IMV necesitas cumplir estos requisitos:

1. Tener entre 23 y 65 anos (si tienes hijos menores, puede ser antes)
2. Llevar al menos 1 ano viviendo en Espana
3. Tener ingresos bajos

Escribe "ok" para seguir con los papeles que necesitas.
```

| Dimension | Assessment |
|-----------|------------|
| **Pros** | Most empathetic. Pacing controlled by user — no information overload. Each message is small and digestible. Builds trust through confirmation loops. |
| **Cons** | Slowest interaction mode — getting full information requires 4-6 messages. Requires conversation state management (tracking where the user is in the flow). May frustrate advanced users. |
| **Implementation complexity** | HIGH — requires conversation state tracking (new `ConversationState` model + Redis or in-memory store), turn-by-turn flow engine, "ok"/"siguiente" intent detection. |
| **Accessibility score** | 8/10 — excellent for anxious and low-literacy users. Minus 2 because multi-turn flows can lose context for users with cognitive challenges, and require the user to remember they're in a "flow." |

### Idea C: Adaptive Mode

**Concept:** Clara detects the user type from the first 1-2 interactions and adapts her response style. Detection signals: language, message length, input type (text vs. audio), vocabulary complexity, response time. She starts with a "medium" default and adjusts. Designed for ALL personas.

**Detection logic:**
- Audio input + short messages -> SHORT mode (Personas 2, 3, 6)
- Text input + complex vocabulary -> DETAILED mode (Persona 4)
- Language = French or Arabic -> MULTILINGUAL mode + SHORT by default
- Error/retry pattern detected -> SIMPLIFIED mode with reassurance
- User explicitly requests "mas detalle" -> switch to DETAILED for that answer

**Example — Default first interaction:**
```
Clara: Hola! Soy Clara. Estoy aqui para ayudarte con tramites en Espana.

Te puedo ayudar con:
1 - Ayuda de dinero (IMV)
2 - Registro en tu ciudad (empadronamiento)
3 - Tarjeta para ir al medico (tarjeta sanitaria)

Puedes escribir, o enviar un audio. Como prefieras.
```

**If user sends a voice note in French, Clara adapts:**
```
Clara: Bonjour! Je suis Clara. Je suis la pour t'aider.

Tu veux des infos sur:
1 - Aide financiere (IMV)
2 - Inscription a la mairie (empadronamiento)
3 - Carte de sante (tarjeta sanitaria)

Envoie un audio ou ecris. Comme tu preferes.
```

**If user sends detailed text in Spanish, Clara gives more:**
```
Clara: Hola! Soy Clara, tu asistente para tramites de servicios sociales en Espana.

Puedo ayudarte con informacion verificada sobre:
1. Ingreso Minimo Vital (IMV) — prestacion economica para personas en situacion de vulnerabilidad
2. Empadronamiento — registro obligatorio en tu municipio, necesario para acceder a servicios publicos
3. Tarjeta Sanitaria — acceso al sistema publico de salud

Dime sobre que quieres saber, o preguntame directamente.
```

| Dimension | Assessment |
|-----------|------------|
| **Pros** | Best of both worlds. Does not patronize advanced users. Automatically simplifies for those who need it. Handles multilingual users naturally. Future-proof — adding new adaptation rules is incremental. |
| **Cons** | Detection can be wrong (false adaptation). More complex to test and verify. Risk of inconsistent experience if adaptation oscillates. Cold start problem: first message must be "medium" which is not optimal for any specific persona. |
| **Implementation complexity** | MEDIUM-HIGH — requires a `UserProfile` or `InteractionStyle` model, detection heuristics in pipeline (input_type + language + message length), and style parameter passed to `system_prompt.py`. Does NOT require persistent state — can adapt per-message based on current input signals. |
| **Accessibility score** | 8.5/10 — potentially the best score because it adapts, but the detection errors could harm the experience for the users who need accessibility most. |

### Comparison Summary

| Criterion | Idea A: Ultra-Short | Idea B: Step-by-Step | Idea C: Adaptive |
|-----------|---------------------|----------------------|-------------------|
| Cognitive load | Lowest | Low (per message) | Variable |
| Warmth/empathy | Low | Highest | Medium-High |
| Implementation effort | Low | High | Medium-High |
| Time to full answer | Medium (2 messages) | High (4-6 messages) | Low-Medium (1-2 messages) |
| Works for ALL personas | Mostly (except Elena) | Mostly (except David) | Yes |
| Testability | Easy | Hard (stateful) | Medium |
| Accessibility score | 9/10 | 8/10 | 8.5/10 |
| Risk of patronizing | Low | Medium | Low |

### Recommendation: Hybrid A+C (Ultra-Short Default with Adaptive Escalation)

**Justification:**

The recommended approach is to implement Idea A (Ultra-Short) as the DEFAULT mode, with Idea C's detection logic as an ENHANCEMENT layer. This means:

1. Every first response is ultra-short with numbered options (safe for all personas).
2. If the user demonstrates advanced vocabulary or asks for more detail, Clara expands.
3. If the user sends audio, Clara always responds with audio + short text.
4. Language adaptation happens automatically per-message (no persistent state needed).

This hybrid avoids the high implementation cost of Idea B's conversation state tracking while capturing most of the benefit of Idea C's adaptation. The ultra-short default ensures that the most vulnerable users (who are least likely to give Clara a second chance) get the most accessible experience on their FIRST interaction.

**Implementation path:**
1. (LOW effort) Rewrite `system_prompt.py` to enforce ultra-short rules.
2. (LOW effort) Rewrite `templates.py` with empathetic, jargon-free templates.
3. (LOW effort) Restructure `demo_cache.json` with numbered-option responses.
4. (MEDIUM effort) Add `detect_style()` heuristic in pipeline (input_type + language + text length).
5. (MEDIUM effort) Add Arabic keywords to `detect_lang.py`.
6. (HIGH effort, Phase 5) Add conversation state for full step-by-step flows.

---

## 4. Conversation Flow Templates (Sin Jerga)

These templates replace the current technical, jargon-heavy responses with plain-language versions. All text is written at a "persona de 12 anos" reading level. Legal terms are always followed by a parenthetical explanation.

### 4.1 Greeting + Detection

**Current (problematic):**
```
Hola! Soy Clara, tu asistente para tramites de servicios sociales en Espana.

Puedo ayudarte con:
1. Ingreso Minimo Vital (IMV) — ayuda economica
2. Empadronamiento — registro en tu municipio
3. Tarjeta Sanitaria — acceso a la sanidad publica

Sobre que te gustaria saber?
```

**Proposed (sin jerga):**
```
Hola! Soy Clara. Estoy aqui para ayudarte.

Puedo darte informacion sobre:
1 - Ayuda de dinero del gobierno (IMV)
2 - Registrarte en tu ciudad (empadronamiento)
3 - Conseguir tu tarjeta para ir al medico

Escribe 1, 2 o 3. O preguntame lo que necesites.
```

**Why it is better:**
- "Ayuda de dinero" instead of "ayuda economica" — concrete, not abstract.
- "Registrarte en tu ciudad" instead of "registro en tu municipio" — "municipio" is formal Spanish.
- "Conseguir tu tarjeta para ir al medico" instead of "acceso a la sanidad publica" — describes the OUTCOME, not the system.
- "Escribe 1, 2 o 3" — reduces the cognitive load of open-ended "sobre que te gustaria saber?"
- No emojis — screen reader friendly.

### 4.2 Simple Definition — IMV

**Current (problematic, from demo_cache.json):**
```
El Ingreso Minimo Vital (IMV) es una prestacion de la Seguridad Social que
garantiza un nivel minimo de ingresos a quienes se encuentran en situacion
de vulnerabilidad economica.
```

**Proposed (sin jerga):**
```
El IMV es una ayuda de dinero que te da el gobierno cada mes si tienes
pocos ingresos. Es como un sueldo minimo para que puedas cubrir lo basico:
comida, alquiler, gastos del dia a dia.

No es un prestamo. No tienes que devolverlo.
```

**Why it is better:**
- "Prestacion de la Seguridad Social" -> "ayuda de dinero que te da el gobierno" — removes institutional jargon.
- "Garantiza un nivel minimo de ingresos" -> "como un sueldo minimo para que puedas cubrir lo basico" — uses a relatable analogy.
- "No es un prestamo. No tienes que devolverlo." — addresses a common fear among immigrant users who confuse it with a loan.

### 4.3 Requirements — IMV (with analogies)

**Current (problematic):**
```
Requisitos principales:
1. Tener entre 23 y 65 anos (o ser menor con hijos a cargo)
2. Residir legalmente en Espana desde hace al menos 1 ano
3. Estar en situacion de vulnerabilidad economica
4. Estar inscrito como demandante de empleo
```

**Proposed (sin jerga):**
```
Para pedir el IMV necesitas:

1. Tener entre 23 y 65 anos
   (Si tienes hijos pequenos, puede ser antes de los 23)

2. Llevar 1 ano viviendo en Espana con papeles
   (Da igual el tipo de permiso. Lo importante es que lleves 1 ano aqui)

3. Tener ingresos bajos
   (El gobierno mira cuanto dinero entra en tu casa cada mes)

4. Estar apuntado en la oficina de empleo
   (Es gratis y se puede hacer por internet)

Quieres saber que papeles necesitas? Escribe SI.
```

**Why it is better:**
- Each requirement has a parenthetical EXPLANATION in everyday language.
- "Residir legalmente" -> "viviendo en Espana con papeles" — users understand "papeles."
- "Situacion de vulnerabilidad economica" -> "tener ingresos bajos" — plain language.
- "Demandante de empleo" -> "apuntado en la oficina de empleo" — uses the phrase people actually use in conversation.
- Ends with a clear, actionable prompt: "Escribe SI."

### 4.4 Documents Needed — Empadronamiento (with "bring X, like when you...")

**Current (problematic):**
```
Documentos necesarios:
1. DNI, NIE o pasaporte en vigor
2. Contrato de alquiler o escritura de la vivienda
3. Si no tienes contrato: declaracion responsable del titular + su DNI
```

**Proposed (sin jerga):**
```
Que tienes que llevar para empadronarte:

1. Tu pasaporte o tu NIE (el documento con tu foto que usas para identificarte)

2. Tu contrato de alquiler (el papel que firmaste cuando alquilaste tu piso)

3. Si NO tienes contrato: no pasa nada. Puedes llevar al dueno del piso contigo para que firme un papel diciendo que vives ahi. O le puedes pedir que escriba una carta y la firme.

IMPORTANTE: Empadronarte es tu DERECHO. No te pueden decir que no, aunque no tengas contrato. Si te ponen problemas, llama al 010 y explica la situacion.
```

**Why it is better:**
- "DNI, NIE o pasaporte en vigor" -> "tu pasaporte o tu NIE (el documento con tu foto...)" — parenthetical makes it concrete.
- "Contrato de alquiler o escritura de la vivienda" -> "el papel que firmaste cuando alquilaste tu piso" — uses relatable description.
- "Declaracion responsable del titular" -> "llevar al dueno del piso contigo para que firme un papel" — the legal term is replaced with the actual action the person needs to take.
- The "IMPORTANTE" block addresses fear directly.

### 4.5 Where To Go + Hours + Phone

**Proposed template:**
```
Donde tienes que ir:

Oficina de Atencion al Ciudadano (OAC)
Es como una ventanilla del ayuntamiento donde hacen estos tramites.

Para encontrar la mas cercana a tu casa:
- Entra en madrid.es/padron
- O llama al 010 (desde Madrid) o 915 298 210

ANTES de ir: pide cita por internet o por telefono. Sin cita, puede que tengas que esperar mucho.

Horario: De lunes a viernes, por la manana (cada oficina tiene horarios un poco diferentes).
```

### 4.6 Costs + Timeframes

**Proposed template:**
```
El empadronamiento es GRATIS. No tienes que pagar nada.

Te dan el certificado en el momento, el mismo dia que vas.

Si necesitas un certificado de empadronamiento mas tarde (para otro tramite), puedes pedirlo por internet o en la oficina. Tambien es gratis.
```

### 4.7 Closing with Reassurance

**Current (no closing template exists):**
The current system has no closing or reassurance template.

**Proposed:**
```
Eso es todo lo que necesitas saber por ahora. Si te surge alguna duda cuando estes haciendo el tramite, escribeme otra vez. Estoy aqui para ayudarte.

Mucho animo. Estos tramites parecen complicados pero se pueden hacer. Tu puedes.
```

**French version:**
```
C'est tout ce que tu dois savoir pour le moment. Si tu as une question quand tu fais la demarche, ecris-moi. Je suis la pour t'aider.

Courage. Ces demarches semblent compliquees mais c'est faisable. Tu vas y arriver.
```

### 4.8 Official Links (always with context)

**Proposed:**
```
Aqui tienes el enlace oficial:
https://www.seg-social.es/imv

Este enlace es de la pagina del gobierno. Es seguro.

Si necesitas ayuda con la pagina web, escribeme y te voy guiando.
```

### 4.9 Full Template Set for Phase 4

| Template Key | Current (ES) | Proposed (ES) |
|-------------|-------------|---------------|
| `ack_text` | "Un momento, estoy procesando tu mensaje... (hourglass)" | "Un momento, estoy buscando la informacion." |
| `ack_audio` | "Estoy escuchando tu audio... (headphones)" | "Estoy escuchando tu audio. Dame unos segundos." |
| `fallback_generic` | "Ahora mismo puedo ayudarte con el Ingreso Minimo Vital, empadronamiento y tarjeta sanitaria." | "Puedo ayudarte con: 1 - Ayuda de dinero (IMV), 2 - Registrarte en tu ciudad, 3 - Tarjeta del medico. Escribe 1, 2 o 3." |
| `whisper_fail` | "No pude entender tu audio. Podrias escribir tu pregunta?" | "No pude escuchar bien tu audio. Puedes intentar de nuevo? Habla despacio y cerca del telefono." |
| `llm_fail` | "Hubo un problema al procesar tu consulta. Prueba de nuevo... IMV: 900 20 22 22" | "Ahora mismo tengo un problema tecnico. Puedes intentar en unos minutos. Si es urgente: IMV - 900 20 22 22 (llamada gratis), Empadronamiento - 010, Medico - 900 102 112. Tambien puedes ir a la oficina mas cercana." |
| `closing` | *(does not exist)* | "Si tienes mas dudas, escribeme cuando quieras. Estoy aqui para ayudarte. Mucho animo." |
| `confusion` | *(does not exist)* | "No estoy segura de haberte entendido bien. Puedes decirme con otras palabras que necesitas? O escribe 1 para ayuda de dinero, 2 para registro en tu ciudad, 3 para tarjeta del medico." |
| `lang_switch` | *(does not exist)* | "Veo que prefieres hablar en [idioma]. Ningun problema, te respondo en [idioma] a partir de ahora." |

---

## 5. Clarification System

### 5.1 Design Principle: Maximum 1 Question Per Message

Clara must NEVER ask more than one question in a single message. Multiple questions overwhelm low-literacy users and create ambiguity about which question to answer.

**Bad (current pattern):**
```
No pude entender tu audio. Podrias escribir tu pregunta? O prefieresque te llame? Necesitas que busque otra cosa?
```

**Good (proposed):**
```
No pude escuchar bien tu audio. Puedes intentar de nuevo?
```

If the retry also fails:
```
Sigo sin poder escucharte. Puedes escribir lo que necesitas? Aunque sea una palabra.
```

### 5.2 Confusion Detection Signals

Clara should detect confusion based on these signals:

| Signal | Detection Method | Response |
|--------|-----------------|----------|
| Very short message after a long response | `len(user_msg) < 5` after Clara sent > 100 words | "No se si me explique bien. Quieres que te lo explique de otra forma?" |
| Question mark after Clara's response | User replies with "?" | "Te lo explico de nuevo de forma mas sencilla." + simplified version |
| "No entiendo" / "No comprendo" / "Que?" | Keyword match: `no entiendo, que es eso, no se, que quieres decir` | Rephrase the previous response at an even simpler level |
| Same question repeated | Similarity > 0.8 with previous user message | "Creo que ya hablamos de esto. Te lo explico diferente esta vez." |
| Language switch mid-conversation | `detect_language(msg) != previous_language` | Switch response language + "Veo que prefieres hablar en [idioma]. Ningun problema." |
| Long silence then simple greeting | > 24h gap + "hola" message | Treat as new conversation, restart greeting flow |

### 5.3 "No Entendi" Handling — Progressive Simplification

When a user indicates they did not understand, Clara applies progressive simplification:

**Level 1 (Normal response):**
```
Para pedir el IMV necesitas llevar 1 ano viviendo en Espana con papeles.
```

**Level 2 (After "no entendi"):**
```
Para pedir esta ayuda de dinero, necesitas haber vivido en Espana por lo menos 12 meses. Y necesitas tener un permiso (NIE o similar).
```

**Level 3 (After second "no entendi"):**
```
Necesitas vivir en Espana 1 ano. Con permiso. Entonces puedes pedir el dinero.
```

**Level 4 (After third "no entendi"):**
```
Te recomiendo llamar al 900 20 22 22. Es gratis. Te ayudan por telefono en tu idioma.
```

### 5.4 Language Switching Mid-Conversation

**Detection:** Use `detect_language()` on every incoming message. If the detected language changes:

**Flow:**
1. Detect new language.
2. If new language is in supported set (es, fr, ar): switch immediately, send acknowledgment.
3. If new language is NOT supported: respond in the user's previous language with "Lo siento, solo puedo hablar en espanol y frances. Puedes escribirme en alguno de estos idiomas?"
4. For Arabic (Phase 4 new): respond in Modern Standard Arabic with a note that Darija is understood but responses will be in MSA.

**Template:**
```
# When switching from ES to FR:
"Je vois que tu preferes parler en francais. Pas de probleme! A partir de maintenant, je te reponds en francais."

# When switching from FR to ES:
"Veo que prefieres hablar en espanol. Ningun problema, sigo en espanol."

# When Arabic detected (new in Phase 4):
"مرحبا! أنا كلارا. أستطيع مساعدتك بالعربية."
("Marhaba! Ana Clara. Astati3 musa3adatak bil 3arabiya.")
```

---

## 6. Risks

### Risk Matrix

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | **Oversimplification** — Removing legal terms causes users to miss critical requirements (e.g., "1 ano de residencia legal" simplified to "vivir en Espana 1 ano" might make someone without legal residence think they qualify) | HIGH | HIGH | Always include the precise requirement in a parenthetical. "Vivir en Espana 1 ano con permiso (NIE, pasaporte sellado, o permiso de residencia)." Add a verification prompt: "Tienes un permiso para vivir en Espana (NIE o similar)?" |
| R2 | **Patronizing users** — Ultra-short mode may offend educated or tech-savvy users (Elena persona) who feel Clara is "talking down" to them | MEDIUM | MEDIUM | Implement the adaptive escalation from Idea C. If a user writes a complex, well-structured question, respond at a matching level. Include a hidden trigger: "Puedes darme mas detalle" switches to detailed mode. |
| R3 | **Arabic support complexity** — Darija is not well-supported by most NLP tools. Gemini has better Arabic than langdetect, but keyword detection for Darija is hard because of transliteration (users write Arabic in Latin characters: "3lach", "kifach") | HIGH | MEDIUM | Phase 1 of Arabic: detect Arabic script in `detect_lang.py`, route to Gemini for language processing. Phase 2: add Latin-transliterated Darija keywords. Phase 3: full Darija support via fine-tuned prompts. |
| R4 | **Privacy — User profiling** — Adaptive mode requires analyzing user behavior (input type, language, message length). Even without storing personal data, users might feel surveilled | LOW | HIGH | Clara adapts based on the CURRENT message only, not stored profiles. No user data is persisted between sessions. Add transparency: "Veo que me has enviado un audio, asi que te respondo tambien con audio" — explain WHY the adaptation is happening. |
| R5 | **Emoji accessibility** — Current templates use emojis (hourglass, headphones). Screen readers read these as full descriptions, interrupting the flow | HIGH | LOW | Remove ALL emojis from templates. Replace with plain text markers: "(hourglass)" -> nothing, "(headphones)" -> nothing. If visual markers are needed, use Unicode characters like bullet points or dashes. |
| R6 | **False confidence from simplification** — User thinks they understand the process, goes to the office, but is rejected because they misunderstood a simplified requirement | MEDIUM | HIGH | Always end requirement explanations with "Si no estas seguro de algo, preguntame antes de ir a la oficina." Add a checklist summary before the "where to go" section: "Antes de ir, asegurate de tener: [list]." |
| R7 | **WhatsApp 2026 policy** — Meta has prohibited general-purpose AI chatbots on WhatsApp Business Platform starting January 15, 2026. Clara must comply as a structured support bot, not a general-purpose AI | MEDIUM | CRITICAL | Clara is already scoped to 3 specific tramites and is not a general-purpose chatbot. However, the system prompt must enforce strict topic boundaries. The guardrails system already handles this. Document compliance rationale for Meta review. |
| R8 | **Audio generation quality in Arabic** — gTTS Arabic pronunciation may be poor for Darija, and MSA pronunciation may feel foreign to Darija speakers | HIGH | MEDIUM | Phase 4: use gTTS with `ar` locale for MSA. Evaluate quality with native speakers. If inadequate, Phase 5: evaluate alternatives (Azure Cognitive Services, Google Cloud TTS with WaveNet). |

### Risk Priority

**Must mitigate before Phase 4 launch:** R1 (oversimplification), R5 (emoji accessibility), R7 (WhatsApp policy).

**Mitigate during Phase 4:** R2 (patronizing), R4 (privacy), R6 (false confidence).

**Accept and plan for Phase 5:** R3 (Arabic complexity), R8 (Arabic audio quality).

---

## 7. Success Criteria

### Quantitative Criteria (PASS/FAIL)

| # | Criterion | Metric | PASS Threshold | FAIL Threshold | How to Measure |
|---|-----------|--------|---------------|----------------|----------------|
| S1 | **Response readability** | Flesch-Kincaid Grade Level (adapted for Spanish) | Grade <= 6 (12-year-old level) for ALL cached responses | Any response > Grade 8 | Automated readability scoring on all `demo_cache.json` entries + system prompt outputs |
| S2 | **Jargon elimination** | Count of legal/institutional terms used WITHOUT parenthetical explanation | 0 unexplained terms per response | > 2 unexplained terms in any response | Automated scan against a jargon dictionary (list of ~50 terms: "prestacion", "empadronamiento", "vulnerabilidad economica", etc.) |
| S3 | **Emoji count** | Number of emojis in templates and cached responses | 0 emojis in ack/error templates. Max 1 emoji in greeting (optional). | > 1 emoji in any non-greeting template | Automated emoji regex scan |
| S4 | **Response length** | Word count of first response to any query | <= 80 words (ultra-short mode default) | > 150 words in first response | Automated word count on all response paths |
| S5 | **Audio companion** | Percentage of responses with audio file available | 100% of cached responses have audio | < 80% of cached responses have audio | Audit `demo_cache.json` for null `audio_file` entries |
| S6 | **Language detection (Arabic)** | Arabic script detection accuracy | >= 90% on test set of 20 Arabic messages | < 70% | Unit tests with Arabic test cases in `tests/unit/` |
| S7 | **Numbered options** | Percentage of menu-style responses that use numbered options (1, 2, 3) instead of open-ended questions | 100% of menu prompts use numbers | Any menu prompt uses open-ended "que quieres?" without numbers | Manual audit of all templates + cached responses |
| S8 | **Deaf-accessible error handling** | Percentage of error templates that include a web/text alternative (not just phone numbers) | 100% of error templates include a URL or text-based alternative alongside any phone number | Any error template with phone number as ONLY option | Manual audit of `templates.py` |
| S9 | **Clarification system** | Maximum questions per Clara message | <= 1 question per message | > 1 question in any template or cached response | Automated question-mark counting per response block |
| S10 | **Persona coverage** | Test scenarios covering all 6 personas | >= 1 end-to-end test per persona (6 total) | < 4 personas covered | New test file `tests/e2e/test_persona_flows.py` |

### Qualitative Criteria (Evaluated by Team)

| # | Criterion | Evaluator | Method |
|---|-----------|-----------|--------|
| Q1 | Tone feels warm and human, not robotic | Andrea + 2 non-team members | Read 10 response samples, rate warmth 1-5. PASS: average >= 3.5 |
| Q2 | No response feels patronizing | Elena-persona tester (tech-savvy user) | Review all responses in DETAILED mode. Flag any that feel condescending. PASS: 0 flags |
| Q3 | French responses feel natural | Native French speaker review | Read all FR templates. PASS: no awkward/machine-translated phrasing flagged |
| Q4 | Reassurance messages reduce anxiety | 3 test users from target demographic | Ask "how did this make you feel?" after test interaction. PASS: all report feeling "helped" or "reassured" |

### Phase 4 Definition of Done

All of the following must be true:

- [ ] S1-S10 quantitative criteria PASS
- [ ] Q1-Q4 qualitative criteria PASS
- [ ] `templates.py` rewritten with new templates (all 3 languages: ES, FR, AR placeholder)
- [ ] `system_prompt.py` updated with ultra-short rules + adaptive escalation instructions
- [ ] `demo_cache.json` restructured with sin-jerga responses + numbered options
- [ ] `detect_lang.py` updated with Arabic keyword set (`_AR_KEYWORDS`)
- [ ] New template keys added: `closing`, `confusion`, `lang_switch`
- [ ] All existing tests pass (96+ tests)
- [ ] New tests added for personas (>= 6 new test cases)
- [ ] Emoji audit passed (0 emojis in non-greeting templates)
- [ ] Ruff lint clean

---

## Appendix A: Jargon Dictionary (Terms to Always Explain)

This dictionary should be used by Clara and by the `verify_response` skill to ensure legal terms are always accompanied by plain-language explanations.

| Legal/Institutional Term | Plain Language (ES) | Plain Language (FR) |
|--------------------------|--------------------|--------------------|
| Prestacion | Ayuda de dinero | Aide financiere |
| Ingreso Minimo Vital | Ayuda de dinero del gobierno (IMV) | Aide financiere du gouvernement (IMV) |
| Empadronamiento | Registro en tu ciudad | Inscription a la mairie |
| Padron municipal | Lista de personas que viven en una ciudad | Liste des habitants de la ville |
| Tarjeta sanitaria | Tarjeta para ir al medico | Carte pour aller chez le medecin |
| Vulnerabilidad economica | Tener pocos ingresos | Avoir peu de revenus |
| Residencia legal | Tener permiso para vivir en Espana (papeles) | Avoir un permis de sejour |
| Demandante de empleo | Apuntado en la oficina de empleo | Inscrit au bureau d'emploi |
| Certificado de empadronamiento | Papel que dice donde vives | Document qui dit ou tu habites |
| Silencio administrativo | Si el gobierno no te responde en [plazo] | Si le gouvernement ne repond pas dans [delai] |
| Declaracion responsable | Un papel firmado por el dueno del piso | Un document signe par le proprietaire |
| Unidad de convivencia | Las personas que viven contigo en tu casa | Les personnes qui vivent avec toi |
| Escritura de la vivienda | Papeles de propiedad del piso | Acte de propriete du logement |
| Cita previa | Reservar un dia y una hora para ir | Prendre rendez-vous |
| Sede electronica | Pagina web del gobierno para hacer tramites | Site web du gouvernement pour les demarches |
| Certificado digital | Una clave especial para usar paginas del gobierno | Un code special pour les sites du gouvernement |
| Comunidad autonoma | Region de Espana (como Madrid, Cataluna...) | Region d'Espagne (comme Madrid, Catalogne...) |

## Appendix B: Screen Reader Optimization Guidelines

For Persona 4 (Elena) and any user with a screen reader:

1. **No emojis in functional templates.** VoiceOver reads "(hourglass)" as "reloj de arena" which interrupts flow.
2. **Use numbered lists, not bullet points.** Screen readers navigate numbered lists more predictably.
3. **Avoid bold markers with asterisks.** WhatsApp renders `**bold**` but some screen readers read the asterisks. Use CAPS for emphasis sparingly: "IMPORTANTE" instead of "**Importante**".
4. **Keep URLs at the END of messages.** Screen readers read URLs character by character. Placing them mid-sentence is disruptive.
5. **One idea per line.** Line breaks help screen reader users navigate with "next line" gestures.
6. **Avoid tables or complex formatting.** WhatsApp doesn't support tables; if information would be in a table, use a numbered list instead.

## Appendix C: Arabic Support Roadmap

### Phase 4 (Minimal Viable Arabic)

- Add `_AR_KEYWORDS` to `detect_lang.py` with Arabic-script keywords: `مساعدة، طبيب، تسجيل، بطاقة، أحتاج`
- Add Arabic templates to `templates.py` for greeting, ack, and fallback
- System prompt instructs Gemini to respond in MSA when Arabic is detected
- gTTS Arabic (`ar` locale) for audio responses
- NO Darija-specific support yet

### Phase 5 (Enhanced Arabic)

- Add Latin-transliterated Darija keywords: `3lach, kifach, wach, bghit, dyal`
- Evaluate Gemini's Darija comprehension with test set
- Community-reviewed response templates in Darija
- Evaluate alternative TTS for Arabic quality

### Phase 6 (Full Arabic)

- Darija-specific response templates
- Arabic-specific cultural analogies in KB
- Arabic-speaking community validation
- Bi-directional language switching (AR <-> ES, AR <-> FR)

---

## Sources

- [UNHCR Turn.io WhatsApp Case Study](https://www.turn.io/case-studies/to-help-build-a-better-future-for-refugees-unhcrs-chat-services-suit-their-preferences-meet-their-needs-and-safeguard-their-data)
- [UNHCR La Chama Chatbot](https://www.unhcr.org/digitalstrategy/case-studies/one-message-at-a-time-la-chama-chatbot-combats-falsehoods/)
- [MITRE Chatbot Accessibility Playbook](https://mitre.github.io/chatbot-accessibility-playbook/)
- [CEA Hub — Chatbots in Humanitarian Contexts (PDF)](https://communityengagementhub.org/wp-content/uploads/sites/2/2023/06/20230623_CEA_Chatbots.pdf)
- [UNHCR Innovation — Meeting Communities Where They Are](https://medium.com/unhcr-innovation-service/meeting-communities-where-they-are-the-increasing-preference-of-messaging-apps-3338ee9ee957)
- [Engati — Arabic Chatbot Guide](https://www.engati.ai/blog/arabic-chatbots)
- [Axis SoftMedia — RTL Chatbots](https://www.axissoftmedia.com/service-details/rtl-chatbots)
- [Invent — Multilingual AI Agents Best Practices 2025](https://www.useinvent.com/blog/how-to-build-effective-multilingual-ai-agents-2025-best-practices-guide)
- [Botpress — Chatbots for Government 2026](https://botpress.com/blog/chatbots-for-government)
- [Parallel HQ — Chatbot UX Design Guide 2025](https://www.parallelhq.com/blog/chatbot-ux-design)
- [Make Things Accessible — Chatbots and Web Accessibility](https://www.makethingsaccessible.com/guides/chatbots-and-web-accessibility-addressing-usability-issues-and-embracing-inclusive-design/)
- [BOIA — Five Key Accessibility Considerations for Chatbots](https://www.boia.org/blog/five-key-accessibility-considerations-for-chatbots)
- [LetsGroto — AI Chatbot UX 2026 Best Practices](https://www.letsgroto.com/blog/ux-best-practices-for-ai-chatbots)
- [Smashing Magazine — How to Design for Deaf People](https://www.smashingmagazine.com/2025/12/how-design-for-with-deaf-people/)
- [Respond.io — WhatsApp 2026 AI Policy Explained](https://respond.io/blog/whatsapp-general-purpose-chatbots-ban)
- [ACM — Chatbots for Migrant Workers Healthcare Needs](https://dl.acm.org/doi/10.1145/3610106)
- [engageSPARK — Humanitarian AI Chatbots](https://www.engagespark.com/humanitarian-ai-chatbots/)
- [InnoCaption — AI for Deaf and Hard of Hearing](https://www.innocaption.com/recentnews/ai-helps-deaf-hard-of-hearing-community)
- [CPWD — How AI Is Changing Accessibility](https://www.cpwd.org/blog/how-ai-is-changing-accessibility-progress-challenges-and-the-path-ahead)
