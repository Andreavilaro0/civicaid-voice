/* ================================================================== */
/*  i18n.ts — Strings centralizados trilingues (ES/FR/AR)             */
/*  Fuente: Brand book + CLARA-TONE-VOICE-GUIDE.md                   */
/* ================================================================== */

import type { Language } from "./types";

/* ------------------------------------------------------------------ */
/*  Landing page                                                      */
/* ------------------------------------------------------------------ */

export const LANDING: Record<Language, {
  greeting: string;
  tagline: [string, string];
  description: string;
  mic_label: string;
  topics_hint: string;
  cta_text: string;
  footer: string;
}> = {
  es: {
    greeting: "Hola, soy Clara",
    tagline: ["Tu voz", "tiene poder"],
    description: "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
    mic_label: "Toca para hablar",
    topics_hint: "O elige un tema:",
    cta_text: "Prefiero escribir",
    footer: "Gratuito · Confidencial · En tu idioma",
  },
  fr: {
    greeting: "Bonjour, je suis Clara",
    tagline: ["Ta voix", "a du pouvoir"],
    description: "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
    mic_label: "Appuie pour parler",
    topics_hint: "Ou choisis un sujet :",
    cta_text: "Je prefere ecrire",
    footer: "Gratuit · Confidentiel · Dans ta langue",
  },
  ar: {
    greeting: "مرحبا، أنا كلارا",
    tagline: ["صوتك", "له قوة"],
    description: "أساعدك في الإجراءات الاجتماعية في إسبانيا. تحدث أو اكتب بلغتك.",
    mic_label: "اضغط للتحدث",
    topics_hint: "أو اختر موضوعاً:",
    cta_text: "أفضل الكتابة",
    footer: "مجاني · سري · بلغتك",
  },
};

/* ------------------------------------------------------------------ */
/*  Topic chips (landing)                                             */
/* ------------------------------------------------------------------ */

export const TOPICS: Record<Language, { icon: string; label: string; speech: string }[]> = {
  es: [
    { icon: "coin", label: "Ayuda\neconomica", speech: "Ayuda economica" },
    { icon: "house", label: "Empadro-\nnamiento", speech: "Empadronamiento" },
    { icon: "health", label: "Salud", speech: "Tarjeta sanitaria" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE o TIE" },
  ],
  fr: [
    { icon: "coin", label: "Aide\nfinanciere", speech: "Aide financiere" },
    { icon: "house", label: "Inscription\nmunicipal", speech: "Inscription municipale" },
    { icon: "health", label: "Sante", speech: "Carte sanitaire" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE ou TIE" },
  ],
  ar: [
    { icon: "coin", label: "مساعدة\nمالية", speech: "المساعدة المالية" },
    { icon: "house", label: "تسجيل\nبلدي", speech: "التسجيل البلدي" },
    { icon: "health", label: "صحة", speech: "البطاقة الصحية" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE أو TIE" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Quick-reply chips (chat)                                          */
/* ------------------------------------------------------------------ */

export const QUICK_REPLIES: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "¿Cómo me empadrono?", "Tarjeta sanitaria"],
  fr: ["Qu'est-ce que le RMV?", "Comment s'inscrire?", "Carte sanitaire"],
  ar: ["ما هو الحد الأدنى للدخل؟", "كيف أسجل؟", "البطاقة الصحية"],
};

/* ------------------------------------------------------------------ */
/*  Impact section                                                    */
/* ------------------------------------------------------------------ */

export const IMPACT: Record<Language, {
  counter_label: string;
  before_label: string;
  after_label: string;
}> = {
  es: {
    counter_label: "personas vulnerables en España no acceden a ayudas",
    before_label: "Antes",
    after_label: "Con Clara",
  },
  fr: {
    counter_label: "personnes vulnérables en Espagne n'accèdent pas aux aides",
    before_label: "Avant",
    after_label: "Avec Clara",
  },
  ar: {
    counter_label: "أشخاص ضعفاء في إسبانيا لا يحصلون على المساعدات",
    before_label: "قبل",
    after_label: "مع كلارا",
  },
};

/* ------------------------------------------------------------------ */
/*  Personas (brand book)                                             */
/* ------------------------------------------------------------------ */

export const PERSONAS: {
  id: string;
  name: string;
  quote: Record<Language, string>;
}[] = [
  {
    id: "maria",
    name: "María, 58",
    quote: {
      es: "\"Solo quiero saber si tengo derecho a ver un médico.\"",
      fr: "\"Je veux juste savoir si j'ai droit à un médecin.\"",
      ar: "\"أريد فقط أن أعرف هل لي الحق في رؤية طبيب.\"",
    },
  },
  {
    id: "ahmed",
    name: "Ahmed, 34",
    quote: {
      es: "\"Llevo 3 meses esperando y nadie me explica nada.\"",
      fr: "\"Cela fait 3 mois que j'attends et personne ne m'explique rien.\"",
      ar: "\"انتظرت 3 أشهر ولم يشرح لي أحد شيئاً.\"",
    },
  },
  {
    id: "fatima",
    name: "Fátima, 42",
    quote: {
      es: "\"No puedo leer los formularios. Están en un español que no entiendo.\"",
      fr: "\"Je ne peux pas lire les formulaires. Ils sont dans un espagnol que je ne comprends pas.\"",
      ar: "\"لا أستطيع قراءة الاستمارات. مكتوبة بإسبانية لا أفهمها.\"",
    },
  },
];

/* ------------------------------------------------------------------ */
/*  Stats strip                                                       */
/* ------------------------------------------------------------------ */

export const STATS: Record<Language, { value: string; label: string }[]> = {
  es: [
    { value: "17", label: "CCAA" },
    { value: "3+", label: "idiomas" },
    { value: "8", label: "trámites" },
    { value: "<3s", label: "respuesta" },
  ],
  fr: [
    { value: "17", label: "régions" },
    { value: "3+", label: "langues" },
    { value: "8", label: "démarches" },
    { value: "<3s", label: "réponse" },
  ],
  ar: [
    { value: "17", label: "منطقة" },
    { value: "+3", label: "لغات" },
    { value: "8", label: "إجراءات" },
    { value: "<3ث", label: "استجابة" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Before/After rows                                                 */
/* ------------------------------------------------------------------ */

export const BEFORE_AFTER: Record<Language, { before: string; after: string }[]> = {
  es: [
    {
      before: "Un formulario de 4 páginas en español jurídico",
      after: "\"¿Tienes pasaporte y contrato? Entonces puedes empadronarte.\"",
    },
    {
      before: "Esperar 45 minutos en una cola para que te digan que falta un papel",
      after: "\"Necesitas: NIE + contrato. Los tienes? Perfecto, vamos paso a paso.\"",
    },
    {
      before: "Buscar en 5 webs diferentes sin entender nada",
      after: "\"El IMV es una ayuda de 604€/mes. Te cuento los requisitos.\"",
    },
  ],
  fr: [
    {
      before: "Un formulaire de 4 pages en espagnol juridique",
      after: "\"Tu as un passeport et un contrat? Alors tu peux t'inscrire.\"",
    },
    {
      before: "Attendre 45 minutes dans une file pour qu'on te dise qu'il manque un papier",
      after: "\"Il te faut: NIE + contrat. Tu les as? Parfait, allons-y étape par étape.\"",
    },
    {
      before: "Chercher sur 5 sites sans rien comprendre",
      after: "\"Le RMV est une aide de 604€/mois. Je t'explique les conditions.\"",
    },
  ],
  ar: [
    {
      before: "استمارة من 4 صفحات بالإسبانية القانونية",
      after: "\"هل لديك جواز سفر وعقد؟ إذن يمكنك التسجيل.\"",
    },
    {
      before: "الانتظار 45 دقيقة في الطابور ليقولوا لك أن ورقة ناقصة",
      after: "\"تحتاج: NIE + عقد. هل لديهما؟ ممتاز، هيا خطوة بخطوة.\"",
    },
    {
      before: "البحث في 5 مواقع مختلفة دون فهم أي شيء",
      after: "\"الحد الأدنى للدخل هو 604€/شهر. سأشرح لك الشروط.\"",
    },
  ],
};

/* ------------------------------------------------------------------ */
/*  Suggestion chips (welcome page — ChatGPT-style)                   */
/* ------------------------------------------------------------------ */

export const SUGGESTIONS: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "Empadronamiento", "Tarjeta sanitaria", "Renovar NIE"],
  fr: ["Qu'est-ce que le RMV?", "Inscription municipale", "Carte sanitaire", "Renouveler NIE"],
  ar: ["ما هو الحد الأدنى للدخل؟", "التسجيل البلدي", "البطاقة الصحية", "تجديد NIE"],
};

/* ------------------------------------------------------------------ */
/*  Prompt bar placeholder                                            */
/* ------------------------------------------------------------------ */

export const PROMPT_PLACEHOLDER: Record<Language, string> = {
  es: "Pregunta algo a Clara...",
  fr: "Pose une question à Clara...",
  ar: "...اسأل كلارا",
};

/* ------------------------------------------------------------------ */
/*  Hamburger menu items                                              */
/* ------------------------------------------------------------------ */

export const MENU_ITEMS: Record<Language, { href: string; label: string }[]> = {
  es: [
    { href: "/como-usar", label: "Cómo usar Clara" },
    { href: "/quienes-somos", label: "Quiénes somos" },
    { href: "/futuro", label: "El futuro de Clara" },
  ],
  fr: [
    { href: "/como-usar", label: "Comment utiliser Clara" },
    { href: "/quienes-somos", label: "Qui sommes-nous" },
    { href: "/futuro", label: "L'avenir de Clara" },
  ],
  ar: [
    { href: "/como-usar", label: "كيف تستخدم كلارا" },
    { href: "/quienes-somos", label: "من نحن" },
    { href: "/futuro", label: "مستقبل كلارا" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Problem section (SB7 §2)                                          */
/* ------------------------------------------------------------------ */

export const PROBLEM_SECTION: Record<Language, {
  title: string;
  subtitle: string;
}> = {
  es: {
    title: "El muro invisible",
    subtitle: "4.5 millones de personas vulnerables en España no acceden a las ayudas que les corresponden por barreras de idioma y burocracia.",
  },
  fr: {
    title: "Le mur invisible",
    subtitle: "4,5 millions de personnes vulnérables en Espagne n'accèdent pas aux aides auxquelles elles ont droit à cause des barrières linguistiques et bureaucratiques.",
  },
  ar: {
    title: "الجدار الخفي",
    subtitle: "4.5 مليون شخص ضعيف في إسبانيا لا يحصلون على المساعدات التي يستحقونها بسبب حواجز اللغة والبيروقراطية.",
  },
};

/* ------------------------------------------------------------------ */
/*  Guide section (SB7 §3–4)                                          */
/* ------------------------------------------------------------------ */

export const GUIDE_SECTION: Record<Language, {
  empathy: string;
  authority: string;
}> = {
  es: {
    empathy: "Sabemos lo que es sentarse en una oficina sin entender una palabra. Clara nació para que no tengas que pasar por eso sola.",
    authority: "Información verificada de fuentes oficiales. Respuestas claras, en tu idioma, cuando las necesitas.",
  },
  fr: {
    empathy: "Nous savons ce que c'est de s'asseoir dans un bureau sans comprendre un mot. Clara est née pour que tu n'aies pas à vivre ça seule.",
    authority: "Informations vérifiées à partir de sources officielles. Des réponses claires, dans ta langue, quand tu en as besoin.",
  },
  ar: {
    empathy: "نعرف ما يعنيه أن تجلس في مكتب دون أن تفهم كلمة واحدة. وُلدت كلارا لكي لا تمر بذلك وحدك.",
    authority: "معلومات موثقة من مصادر رسمية. إجابات واضحة، بلغتك، عندما تحتاجها.",
  },
};

/* ------------------------------------------------------------------ */
/*  Plan section (SB7 §4)                                             */
/* ------------------------------------------------------------------ */

export const PLAN_SECTION: Record<Language, {
  title: string;
  steps: { number: string; text: string }[];
  agreements: { icon: string; text: string }[];
}> = {
  es: {
    title: "Así de fácil",
    steps: [
      { number: "1", text: "Abre Clara desde tu móvil" },
      { number: "2", text: "Habla o escribe en tu idioma" },
      { number: "3", text: "Recibe pasos claros con links oficiales" },
    ],
    agreements: [
      { icon: "free", text: "Gratis" },
      { icon: "lock", text: "Confidencial" },
      { icon: "no-register", text: "Sin registro" },
      { icon: "clock", text: "24/7" },
    ],
  },
  fr: {
    title: "C'est aussi simple que ça",
    steps: [
      { number: "1", text: "Ouvre Clara depuis ton mobile" },
      { number: "2", text: "Parle ou écris dans ta langue" },
      { number: "3", text: "Reçois des étapes claires avec des liens officiels" },
    ],
    agreements: [
      { icon: "free", text: "Gratuit" },
      { icon: "lock", text: "Confidentiel" },
      { icon: "no-register", text: "Sans inscription" },
      { icon: "clock", text: "24/7" },
    ],
  },
  ar: {
    title: "بهذه البساطة",
    steps: [
      { number: "1", text: "افتح كلارا من هاتفك" },
      { number: "2", text: "تحدث أو اكتب بلغتك" },
      { number: "3", text: "احصل على خطوات واضحة مع روابط رسمية" },
    ],
    agreements: [
      { icon: "free", text: "مجاني" },
      { icon: "lock", text: "سري" },
      { icon: "no-register", text: "بدون تسجيل" },
      { icon: "clock", text: "24/7" },
    ],
  },
};

/* ------------------------------------------------------------------ */
/*  Success section (SB7 §7)                                          */
/* ------------------------------------------------------------------ */

export const SUCCESS_SECTION: Record<Language, {
  quote: string;
  tagline: [string, string];
  transformation_from: string;
  transformation_to: string;
}> = {
  es: {
    quote: "Entender tus derechos no debería ser un privilegio.",
    tagline: ["Tu voz", "tiene poder"],
    transformation_from: "Confundida, excluida, con miedo al sistema",
    transformation_to: "Informada, empoderada, ejerciendo sus derechos",
  },
  fr: {
    quote: "Comprendre tes droits ne devrait pas être un privilège.",
    tagline: ["Ta voix", "a du pouvoir"],
    transformation_from: "Confuse, exclue, effrayée par le système",
    transformation_to: "Informée, autonome, exerçant ses droits",
  },
  ar: {
    quote: "فهم حقوقك لا ينبغي أن يكون امتيازاً.",
    tagline: ["صوتك", "له قوة"],
    transformation_from: "مرتبكة، مُستبعدة، خائفة من النظام",
    transformation_to: "مُطّلعة، ممكّنة، تمارس حقوقها",
  },
};

/* ------------------------------------------------------------------ */
/*  Second CTA (SB7 §5)                                               */
/* ------------------------------------------------------------------ */

export const SECOND_CTA: Record<Language, {
  headline: string;
  mic_label: string;
}> = {
  es: {
    headline: "Habla con Clara ahora",
    mic_label: "Pulsa para hablar",
  },
  fr: {
    headline: "Parle avec Clara maintenant",
    mic_label: "Appuie pour parler",
  },
  ar: {
    headline: "تحدث مع كلارا الآن",
    mic_label: "اضغط للتحدث",
  },
};

/* ------------------------------------------------------------------ */
/*  Footer                                                            */
/* ------------------------------------------------------------------ */

export const FOOTER_SECTION: Record<Language, {
  credits: string;
  links: { href: string; label: string }[];
}> = {
  es: {
    credits: "Hecho con amor en OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "Cómo usar" },
      { href: "/quienes-somos", label: "Quiénes somos" },
      { href: "/futuro", label: "Futuro" },
    ],
  },
  fr: {
    credits: "Fait avec amour à OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "Comment utiliser" },
      { href: "/quienes-somos", label: "Qui sommes-nous" },
      { href: "/futuro", label: "Avenir" },
    ],
  },
  ar: {
    credits: "صُنع بحب في OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "كيف تستخدم" },
      { href: "/quienes-somos", label: "من نحن" },
      { href: "/futuro", label: "المستقبل" },
    ],
  },
};

/* ------------------------------------------------------------------ */
/*  Quienes Somos — SB7 narrative (E-V-I pattern)                     */
/* ------------------------------------------------------------------ */

export const QUIENES_SOMOS_STORY: Record<Language, {
  empatizar: { title: string; body: string; stat: string };
  validar: { title: string; body: string; closing: string };
  momento: { title: string; body: string };
  equipo: {
    title: string;
    intro: string;
    members: { name: string; role: string }[];
  };
  cta: { title: string; body: string; button: string };
}> = {
  es: {
    empatizar: {
      title: "Esto no deberia ser tan dificil",
      body: "Sabemos lo que es sentarse en una oficina publica sin entender una palabra. Ese nudo en el estomago cuando te dan un formulario de cuatro paginas en espanol juridico. Ese miedo a preguntar porque no quieres molestar. Esa sensacion de que el sistema no fue hecho para ti.",
      stat: "No estas sola. 4.5 millones de personas en Espana pasan por esto cada dia.",
    },
    validar: {
      title: "Entender tus derechos no deberia ser un privilegio",
      body: "Si vives en Espana, tienes derechos. Derecho a la sanidad. Derecho al empadronamiento. Derecho a ayudas economicas si las necesitas. Pero acceder a ellos requiere navegar un laberinto de formularios, webs y oficinas que no fueron disenados pensando en ti.",
      closing: "Eso no esta bien.",
    },
    momento: {
      title: "Por eso existe Clara",
      body: "En febrero de 2026, cinco personas nos sentamos en un hackathon con una pregunta: Y si pudieras acceder a tus derechos simplemente hablando?\n\nNo queriamos construir otro chatbot. Queriamos construir algo que funcionara como funciona la vida real: le cuentas a alguien tu situacion, y esa persona te dice exactamente que hacer, paso a paso, en tu idioma.\n\nAsi nacio Clara.",
    },
    equipo: {
      title: "Quienes somos",
      intro: "No somos los heroes de esta historia — los heroes sois vosotros.",
      members: [
        { name: "Andrea", role: "Creadora de Clara" },
      ],
    },
    cta: {
      title: "Tu voz tiene poder",
      body: "Clara esta lista para ayudarte. Habla o escribe en tu idioma.",
      button: "Habla con Clara ahora",
    },
  },
  fr: {
    empatizar: {
      title: "Ca ne devrait pas etre aussi difficile",
      body: "Nous savons ce que c'est de s'asseoir dans un bureau public sans comprendre un mot. Ce noeud dans l'estomac quand on te donne un formulaire de quatre pages en espagnol juridique. Cette peur de demander parce que tu ne veux pas deranger.",
      stat: "Tu n'es pas seule. 4,5 millions de personnes en Espagne vivent ca chaque jour.",
    },
    validar: {
      title: "Comprendre tes droits ne devrait pas etre un privilege",
      body: "Si tu vis en Espagne, tu as des droits. Droit a la sante. Droit a l'inscription municipale. Droit aux aides economiques si tu en as besoin. Mais y acceder exige de naviguer un labyrinthe de formulaires et de bureaux qui n'ont pas ete concus pour toi.",
      closing: "Ce n'est pas normal.",
    },
    momento: {
      title: "C'est pour ca que Clara existe",
      body: "En fevrier 2026, cinq personnes se sont assises a un hackathon avec une question: Et si tu pouvais acceder a tes droits simplement en parlant?\n\nNous ne voulions pas construire un autre chatbot. Nous voulions construire quelque chose qui fonctionne comme la vraie vie: tu racontes ta situation, et on te dit exactement quoi faire, etape par etape, dans ta langue.\n\nC'est ainsi que Clara est nee.",
    },
    equipo: {
      title: "Qui sommes-nous",
      intro: "Nous ne sommes pas les heros de cette histoire — les heros, c'est vous.",
      members: [
        { name: "Andrea", role: "Creatrice de Clara" },
      ],
    },
    cta: {
      title: "Ta voix a du pouvoir",
      body: "Clara est prete a t'aider. Parle ou ecris dans ta langue.",
      button: "Parle avec Clara maintenant",
    },
  },
  ar: {
    empatizar: {
      title: "لا ينبغي أن يكون الأمر بهذه الصعوبة",
      body: "نعرف ما يعنيه أن تجلس في مكتب حكومي دون أن تفهم كلمة واحدة. تلك العقدة في المعدة عندما يعطونك استمارة من أربع صفحات بالإسبانية القانونية. ذلك الخوف من السؤال لأنك لا تريد أن تزعج أحداً.",
      stat: "لست وحدك. 4.5 مليون شخص في إسبانيا يمرون بهذا كل يوم.",
    },
    validar: {
      title: "فهم حقوقك لا ينبغي أن يكون امتيازاً",
      body: "إذا كنت تعيش في إسبانيا، لديك حقوق. الحق في الرعاية الصحية. الحق في التسجيل البلدي. الحق في المساعدات الاقتصادية إذا كنت بحاجة إليها. لكن الوصول إليها يتطلب التنقل في متاهة من الاستمارات والمواقع والمكاتب التي لم تُصمم من أجلك.",
      closing: "هذا ليس عدلاً.",
    },
    momento: {
      title: "لهذا وُلدت كلارا",
      body: "في فبراير 2026، جلس خمسة أشخاص في هاكاثون مع سؤال واحد: ماذا لو كان بإمكانك الوصول إلى حقوقك بمجرد التحدث؟\n\nلم نكن نريد بناء روبوت محادثة آخر. أردنا بناء شيء يعمل كما تعمل الحياة الحقيقية: تحكي وضعك، ويقول لك أحدهم بالضبط ماذا تفعل، خطوة بخطوة، بلغتك.\n\nهكذا وُلدت كلارا.",
    },
    equipo: {
      title: "من نحن",
      intro: "لسنا أبطال هذه القصة — الأبطال أنتم.",
      members: [
        { name: "Andrea", role: "صانعة كلارا" },
      ],
    },
    cta: {
      title: "صوتك له قوة",
      body: "كلارا جاهزة لمساعدتك. تحدث أو اكتب بلغتك.",
      button: "تحدث مع كلارا الآن",
    },
  },
};

/* ------------------------------------------------------------------ */
/*  Sub-page titles                                                   */
/* ------------------------------------------------------------------ */

export const SUB_PAGE_TITLES: Record<Language, Record<string, string>> = {
  es: {
    "como-usar": "Cómo usar Clara",
    "quienes-somos": "Quiénes somos",
    "futuro": "El futuro de Clara",
  },
  fr: {
    "como-usar": "Comment utiliser Clara",
    "quienes-somos": "Qui sommes-nous",
    "futuro": "L'avenir de Clara",
  },
  ar: {
    "como-usar": "كيف تستخدم كلارا",
    "quienes-somos": "من نحن",
    "futuro": "مستقبل كلارا",
  },
};
