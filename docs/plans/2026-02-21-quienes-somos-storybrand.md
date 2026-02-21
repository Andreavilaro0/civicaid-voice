# QuienesSomos StoryBrand Rewrite — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite QuienesSomosPage from a flat "about" page into an emotional SB7 narrative that positions the team as GUIDE (not hero), using E-V-I pattern.

**Architecture:** Replace inline content objects in QuienesSomosPage.tsx with new i18n strings in `QUIENES_SOMOS_STORY`. Add scroll-reveal animations via IntersectionObserver. Structure: Empatizar → Validar → Momento → Autoridad → Equipo → CTA.

**Tech Stack:** React 18, TypeScript, Tailwind CSS, existing i18n pattern, IntersectionObserver

---

## StoryBrand Narrative Content (from SB7 analysis)

### ES — Spanish

**Section 1 "Empatizar":**
- Title: "Esto no deberia ser tan dificil"
- Body: "Sabemos lo que es sentarse en una oficina publica sin entender una palabra. Ese nudo en el estomago cuando te dan un formulario de cuatro paginas en espanol juridico. Ese miedo a preguntar porque no quieres molestar. Esa sensacion de que el sistema no fue hecho para ti."
- Stat: "No estas sola. 4.5 millones de personas en Espana pasan por esto cada dia."

**Section 2 "Validar":**
- Title: "Entender tus derechos no deberia ser un privilegio"
- Body: "Si vives en Espana, tienes derechos. Derecho a la sanidad. Derecho al empadronamiento. Derecho a ayudas economicas si las necesitas. Pero acceder a ellos requiere navegar un laberinto de formularios, webs y oficinas que no fueron disenados pensando en ti."
- Closing: "Eso no esta bien."

**Section 3 "El Momento":**
- Title: "Por eso existe Clara"
- Body: "En febrero de 2026, cinco personas nos sentamos en un hackathon con una pregunta: Y si pudieras acceder a tus derechos simplemente hablando? No queriamos construir otro chatbot. Queriamos construir algo que funcionara como funciona la vida real: le cuentas a alguien tu situacion, y esa persona te dice exactamente que hacer, paso a paso, en tu idioma. Asi nacio Clara."

**Section 4 "Equipo":**
- Title: "Quienes somos"
- Intro: "Somos un equipo de 5 personas que cree que la tecnologia debe servir a quien mas la necesita. No somos los heroes de esta historia — los heroes sois vosotros."
- Members: Robert/La inteligencia detras de cada respuesta, Marcos/La voz que conecta Clara contigo, Lucas/La informacion que hace que cada respuesta sea correcta, Daniel/La experiencia que hace que todo sea facil de usar, Andrea/La coordinacion que mantiene todo en marcha

**Section 5 "CTA":**
- Title: "Tu voz tiene poder"
- Body: "Clara esta lista para ayudarte. Habla o escribe en tu idioma."
- Button: "Habla con Clara ahora"

### FR — French

**Section 1:** Title: "Ca ne devrait pas etre aussi difficile" / Body: "Nous savons ce que c'est de s'asseoir dans un bureau public sans comprendre un mot. Ce noeud dans l'estomac quand on te donne un formulaire de quatre pages en espagnol juridique. Cette peur de demander parce que tu ne veux pas deranger." / Stat: "Tu n'es pas seule. 4,5 millions de personnes en Espagne vivent ca chaque jour."

**Section 2:** Title: "Comprendre tes droits ne devrait pas etre un privilege" / Body: "Si tu vis en Espagne, tu as des droits. Droit a la sante. Droit a l'inscription municipale. Droit aux aides economiques si tu en as besoin. Mais y acceder exige de naviguer un labyrinthe de formulaires et de bureaux qui n'ont pas ete concus pour toi." / Closing: "Ce n'est pas normal."

**Section 3:** Title: "C'est pour ca que Clara existe" / Body: "En fevrier 2026, cinq personnes se sont assises a un hackathon avec une question: Et si tu pouvais acceder a tes droits simplement en parlant? Nous ne voulions pas construire un autre chatbot. Nous voulions construire quelque chose qui fonctionne comme la vraie vie: tu racontes ta situation, et on te dit exactement quoi faire, etape par etape, dans ta langue. C'est ainsi que Clara est nee."

**Section 4:** Title: "Qui sommes-nous" / Intro: "Nous sommes une equipe de 5 personnes qui croit que la technologie doit servir ceux qui en ont le plus besoin. Nous ne sommes pas les heros de cette histoire — les heros, c'est vous."

**Section 5:** Title: "Ta voix a du pouvoir" / Body: "Clara est prete a t'aider. Parle ou ecris dans ta langue." / Button: "Parle avec Clara maintenant"

### AR — Arabic

**Section 1:** Title: "لا ينبغي أن يكون الأمر بهذه الصعوبة" / Body: "نعرف ما يعنيه أن تجلس في مكتب حكومي دون أن تفهم كلمة واحدة. تلك العقدة في المعدة عندما يعطونك استمارة من أربع صفحات بالإسبانية القانونية. ذلك الخوف من السؤال لأنك لا تريد أن تزعج أحداً." / Stat: "لست وحدك. 4.5 مليون شخص في إسبانيا يمرون بهذا كل يوم."

**Section 2:** Title: "فهم حقوقك لا ينبغي أن يكون امتيازاً" / Body: "إذا كنت تعيش في إسبانيا، لديك حقوق. الحق في الرعاية الصحية. الحق في التسجيل البلدي. الحق في المساعدات الاقتصادية إذا كنت بحاجة إليها. لكن الوصول إليها يتطلب التنقل في متاهة من الاستمارات والمواقع والمكاتب التي لم تُصمم من أجلك." / Closing: "هذا ليس عدلاً."

**Section 3:** Title: "لهذا وُلدت كلارا" / Body: "في فبراير 2026، جلس خمسة أشخاص في هاكاثون مع سؤال واحد: ماذا لو كان بإمكانك الوصول إلى حقوقك بمجرد التحدث؟ لم نكن نريد بناء روبوت محادثة آخر. أردنا بناء شيء يعمل كما تعمل الحياة الحقيقية: تحكي وضعك، ويقول لك أحدهم بالضبط ماذا تفعل، خطوة بخطوة، بلغتك. هكذا وُلدت كلارا."

**Section 4:** Title: "من نحن" / Intro: "نحن فريق من 5 أشخاص يؤمن بأن التكنولوجيا يجب أن تخدم من يحتاجها أكثر. لسنا أبطال هذه القصة — الأبطال أنتم."

**Section 5:** Title: "صوتك له قوة" / Body: "كلارا جاهزة لمساعدتك. تحدث أو اكتب بلغتك." / Button: "تحدث مع كلارا الآن"

---

## Tasks

### Task 1: Add i18n strings

**Files:**
- Modify: `front/src/lib/i18n.ts`

**Step 1:** Add `QUIENES_SOMOS_STORY` export with all ES/FR/AR content from above.

**Step 2:** Run `npx tsc --noEmit` — expect PASS.

### Task 2: Rewrite QuienesSomosPage

**Files:**
- Modify: `front/src/pages/QuienesSomosPage.tsx`

**Step 1:** Replace inline content with `QUIENES_SOMOS_STORY` import. Add 6 sections with IntersectionObserver fade-in. Add CTA button linking to `/chat`. Alternating backgrounds (white / #FAFAFA / #F0F7FA).

**Step 2:** Run `npx tsc --noEmit` — expect PASS.

**Step 3:** Run `npm run build` — expect PASS.

### Task 3: Verify

**Step 1:** `npm run dev` and check all 3 languages.
**Step 2:** Verify RTL for Arabic.
**Step 3:** Verify CTA button navigates to chat.
