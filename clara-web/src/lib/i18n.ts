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
