/* ================================================================== */
/*  i18n.ts — Strings centralizados 8 idiomas                        */
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
  en: {
    greeting: "Hi, I'm Clara",
    tagline: ["Your voice", "has power"],
    description: "I help you with social services in Spain. Speak or type in your language.",
    mic_label: "Tap to speak",
    topics_hint: "Or choose a topic:",
    cta_text: "I prefer to type",
    footer: "Free · Confidential · In your language",
  },
  pt: {
    greeting: "Ola, sou a Clara",
    tagline: ["A tua voz", "tem poder"],
    description: "Ajudo-te com tramites sociais em Espanha. Fala ou escreve na tua lingua.",
    mic_label: "Toca para falar",
    topics_hint: "Ou escolhe um tema:",
    cta_text: "Prefiro escrever",
    footer: "Gratuito · Confidencial · Na tua lingua",
  },
  ro: {
    greeting: "Buna, sunt Clara",
    tagline: ["Vocea ta", "are putere"],
    description: "Te ajut cu procedurile sociale din Spania. Vorbeste sau scrie in limba ta.",
    mic_label: "Apasa pentru a vorbi",
    topics_hint: "Sau alege un subiect:",
    cta_text: "Prefer sa scriu",
    footer: "Gratuit · Confidential · In limba ta",
  },
  ca: {
    greeting: "Hola, soc la Clara",
    tagline: ["La teva veu", "te poder"],
    description: "T'ajudo amb tramits socials a Espanya. Parla o escriu en la teva llengua.",
    mic_label: "Toca per parlar",
    topics_hint: "O tria un tema:",
    cta_text: "Prefereixo escriure",
    footer: "Gratuit · Confidencial · En la teva llengua",
  },
  zh: {
    greeting: "你好，我是Clara",
    tagline: ["你的声音", "有力量"],
    description: "我帮助你办理西班牙的社会事务。用你的语言说话或打字。",
    mic_label: "点击说话",
    topics_hint: "或选择一个主题：",
    cta_text: "我更喜欢打字",
    footer: "免费 · 保密 · 用你的语言",
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
  en: [
    { icon: "coin", label: "Financial\nhelp", speech: "Financial help" },
    { icon: "house", label: "City\nregistration", speech: "Municipal registration" },
    { icon: "health", label: "Health", speech: "Health card" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE or TIE" },
  ],
  pt: [
    { icon: "coin", label: "Ajuda\nfinanceira", speech: "Ajuda financeira" },
    { icon: "house", label: "Inscricao\nmunicipal", speech: "Inscricao municipal" },
    { icon: "health", label: "Saude", speech: "Cartao de saude" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE ou TIE" },
  ],
  ro: [
    { icon: "coin", label: "Ajutor\nfinanciar", speech: "Ajutor financiar" },
    { icon: "house", label: "Inregistrare\nmunicipala", speech: "Inregistrare municipala" },
    { icon: "health", label: "Sanatate", speech: "Card de sanatate" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE sau TIE" },
  ],
  ca: [
    { icon: "coin", label: "Ajuda\neconomica", speech: "Ajuda economica" },
    { icon: "house", label: "Empadro-\nnament", speech: "Empadronament" },
    { icon: "health", label: "Salut", speech: "Targeta sanitaria" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE o TIE" },
  ],
  zh: [
    { icon: "coin", label: "经济\n援助", speech: "经济援助" },
    { icon: "house", label: "市政\n登记", speech: "市政登记" },
    { icon: "health", label: "健康", speech: "医疗卡" },
    { icon: "doc", label: "NIE/TIE", speech: "NIE或TIE" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Quick-reply chips (chat)                                          */
/* ------------------------------------------------------------------ */

export const QUICK_REPLIES: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "¿Cómo me empadrono?", "Tarjeta sanitaria"],
  fr: ["Qu'est-ce que le RMV?", "Comment s'inscrire?", "Carte sanitaire"],
  ar: ["ما هو الحد الأدنى للدخل؟", "كيف أسجل؟", "البطاقة الصحية"],
  en: ["What is the IMV?", "How do I register?", "Health card"],
  pt: ["O que e o IMV?", "Como me inscrevo?", "Cartao de saude"],
  ro: ["Ce este IMV?", "Cum ma inregistrez?", "Card de sanatate"],
  ca: ["Que es l'IMV?", "Com m'empadrono?", "Targeta sanitaria"],
  zh: ["什么是最低收入？", "如何登记？", "医疗卡"],
};

/* ------------------------------------------------------------------ */
/*  Impact section                                                    */
/* ------------------------------------------------------------------ */

export const IMPACT: Record<Language, {
  counter_label: string;
  before_label: string;
  after_label: string;
}> = {
  es: { counter_label: "personas vulnerables en España no acceden a ayudas", before_label: "Antes", after_label: "Con Clara" },
  fr: { counter_label: "personnes vulnérables en Espagne n'accèdent pas aux aides", before_label: "Avant", after_label: "Avec Clara" },
  ar: { counter_label: "أشخاص ضعفاء في إسبانيا لا يحصلون على المساعدات", before_label: "قبل", after_label: "مع كلارا" },
  en: { counter_label: "vulnerable people in Spain don't access benefits", before_label: "Before", after_label: "With Clara" },
  pt: { counter_label: "pessoas vulneraveis em Espanha nao acedem a ajudas", before_label: "Antes", after_label: "Com a Clara" },
  ro: { counter_label: "persoane vulnerabile din Spania nu acceseaza ajutoare", before_label: "Inainte", after_label: "Cu Clara" },
  ca: { counter_label: "persones vulnerables a Espanya no accedeixen a ajudes", before_label: "Abans", after_label: "Amb Clara" },
  zh: { counter_label: "西班牙弱势群体无法获得援助", before_label: "之前", after_label: "有了Clara" },
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
      en: "\"I just want to know if I have the right to see a doctor.\"",
      pt: "\"So quero saber se tenho direito a ver um medico.\"",
      ro: "\"Vreau doar sa stiu daca am dreptul sa vad un medic.\"",
      ca: "\"Nomes vull saber si tinc dret a veure un metge.\"",
      zh: "\"我只想知道我是否有权看医生。\"",
    },
  },
  {
    id: "ahmed",
    name: "Ahmed, 34",
    quote: {
      es: "\"Llevo 3 meses esperando y nadie me explica nada.\"",
      fr: "\"Cela fait 3 mois que j'attends et personne ne m'explique rien.\"",
      ar: "\"انتظرت 3 أشهر ولم يشرح لي أحد شيئاً.\"",
      en: "\"I've been waiting 3 months and nobody explains anything.\"",
      pt: "\"Espero ha 3 meses e ninguem me explica nada.\"",
      ro: "\"Astept de 3 luni si nimeni nu imi explica nimic.\"",
      ca: "\"Fa 3 mesos que espero i ningu m'explica res.\"",
      zh: "\"我等了3个月，没有人给我解释任何事情。\"",
    },
  },
  {
    id: "fatima",
    name: "Fátima, 42",
    quote: {
      es: "\"No puedo leer los formularios. Están en un español que no entiendo.\"",
      fr: "\"Je ne peux pas lire les formulaires. Ils sont dans un espagnol que je ne comprends pas.\"",
      ar: "\"لا أستطيع قراءة الاستمارات. مكتوبة بإسبانية لا أفهمها.\"",
      en: "\"I can't read the forms. They're in a Spanish I don't understand.\"",
      pt: "\"Nao consigo ler os formularios. Estao num espanhol que nao entendo.\"",
      ro: "\"Nu pot citi formularele. Sunt intr-o spaniola pe care nu o inteleg.\"",
      ca: "\"No puc llegir els formularis. Estan en un castella que no entenc.\"",
      zh: "\"我看不懂那些表格。它们用的是我不懂的西班牙语。\"",
    },
  },
];

/* ------------------------------------------------------------------ */
/*  Stats strip                                                       */
/* ------------------------------------------------------------------ */

export const STATS: Record<Language, { value: string; label: string }[]> = {
  es: [{ value: "17", label: "CCAA" }, { value: "8+", label: "idiomas" }, { value: "8", label: "trámites" }, { value: "<3s", label: "respuesta" }],
  fr: [{ value: "17", label: "régions" }, { value: "8+", label: "langues" }, { value: "8", label: "démarches" }, { value: "<3s", label: "réponse" }],
  ar: [{ value: "17", label: "منطقة" }, { value: "+8", label: "لغات" }, { value: "8", label: "إجراءات" }, { value: "<3ث", label: "استجابة" }],
  en: [{ value: "17", label: "regions" }, { value: "8+", label: "languages" }, { value: "8", label: "procedures" }, { value: "<3s", label: "response" }],
  pt: [{ value: "17", label: "regioes" }, { value: "8+", label: "idiomas" }, { value: "8", label: "tramites" }, { value: "<3s", label: "resposta" }],
  ro: [{ value: "17", label: "regiuni" }, { value: "8+", label: "limbi" }, { value: "8", label: "proceduri" }, { value: "<3s", label: "raspuns" }],
  ca: [{ value: "17", label: "CCAA" }, { value: "8+", label: "idiomes" }, { value: "8", label: "tramits" }, { value: "<3s", label: "resposta" }],
  zh: [{ value: "17", label: "地区" }, { value: "8+", label: "语言" }, { value: "8", label: "手续" }, { value: "<3秒", label: "响应" }],
};

/* ------------------------------------------------------------------ */
/*  Before/After rows                                                 */
/* ------------------------------------------------------------------ */

export const BEFORE_AFTER: Record<Language, { before: string; after: string }[]> = {
  es: [
    { before: "Un formulario de 4 páginas en español jurídico", after: "\"¿Tienes pasaporte y contrato? Entonces puedes empadronarte.\"" },
    { before: "Esperar 45 minutos en una cola para que te digan que falta un papel", after: "\"Necesitas: NIE + contrato. Los tienes? Perfecto, vamos paso a paso.\"" },
    { before: "Buscar en 5 webs diferentes sin entender nada", after: "\"El IMV es una ayuda de 604€/mes. Te cuento los requisitos.\"" },
  ],
  fr: [
    { before: "Un formulaire de 4 pages en espagnol juridique", after: "\"Tu as un passeport et un contrat? Alors tu peux t'inscrire.\"" },
    { before: "Attendre 45 minutes dans une file pour qu'on te dise qu'il manque un papier", after: "\"Il te faut: NIE + contrat. Tu les as? Parfait, allons-y étape par étape.\"" },
    { before: "Chercher sur 5 sites sans rien comprendre", after: "\"Le RMV est une aide de 604€/mois. Je t'explique les conditions.\"" },
  ],
  ar: [
    { before: "استمارة من 4 صفحات بالإسبانية القانونية", after: "\"هل لديك جواز سفر وعقد؟ إذن يمكنك التسجيل.\"" },
    { before: "الانتظار 45 دقيقة في الطابور ليقولوا لك أن ورقة ناقصة", after: "\"تحتاج: NIE + عقد. هل لديهما؟ ممتاز، هيا خطوة بخطوة.\"" },
    { before: "البحث في 5 مواقع مختلفة دون فهم أي شيء", after: "\"الحد الأدنى للدخل هو 604€/شهر. سأشرح لك الشروط.\"" },
  ],
  en: [
    { before: "A 4-page form in legal Spanish", after: "\"Do you have a passport and contract? Then you can register.\"" },
    { before: "Waiting 45 minutes in line to be told you're missing a document", after: "\"You need: NIE + contract. Got them? Perfect, let's go step by step.\"" },
    { before: "Searching 5 different websites without understanding anything", after: "\"The IMV is a benefit of 604€/month. Let me tell you the requirements.\"" },
  ],
  pt: [
    { before: "Um formulario de 4 paginas em espanhol juridico", after: "\"Tens passaporte e contrato? Entao podes inscrever-te.\"" },
    { before: "Esperar 45 minutos numa fila para te dizerem que falta um papel", after: "\"Precisas: NIE + contrato. Tens? Perfeito, vamos passo a passo.\"" },
    { before: "Procurar em 5 sites diferentes sem perceber nada", after: "\"O IMV e uma ajuda de 604€/mes. Conto-te os requisitos.\"" },
  ],
  ro: [
    { before: "Un formular de 4 pagini in spaniola juridica", after: "\"Ai pasaport si contract? Atunci te poti inregistra.\"" },
    { before: "Sa astepti 45 de minute la coada ca sa ti se spuna ca lipseste un document", after: "\"Ai nevoie de: NIE + contract. Le ai? Perfect, hai pas cu pas.\"" },
    { before: "Sa cauti pe 5 site-uri diferite fara sa intelegi nimic", after: "\"IMV este un ajutor de 604€/luna. Iti spun conditiile.\"" },
  ],
  ca: [
    { before: "Un formulari de 4 pagines en castella juridic", after: "\"Tens passaport i contracte? Doncs pots empadronar-te.\"" },
    { before: "Esperar 45 minuts a una cua perque et diguin que falta un paper", after: "\"Necessites: NIE + contracte. Els tens? Perfecte, anem pas a pas.\"" },
    { before: "Buscar en 5 webs diferents sense entendre res", after: "\"L'IMV es una ajuda de 604€/mes. T'explico els requisits.\"" },
  ],
  zh: [
    { before: "一份4页的法律西班牙语表格", after: "\"你有护照和合同吗？那你就可以登记了。\"" },
    { before: "排队等45分钟却被告知少了一份文件", after: "\"你需要：NIE + 合同。有了吗？好的，我们一步步来。\"" },
    { before: "在5个不同网站上搜索却什么都看不懂", after: "\"IMV是每月604€的援助。让我告诉你条件。\"" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Suggestion chips (welcome page — ChatGPT-style)                   */
/* ------------------------------------------------------------------ */

export const SUGGESTIONS: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "Empadronamiento", "Tarjeta sanitaria", "Renovar NIE"],
  fr: ["Qu'est-ce que le RMV?", "Inscription municipale", "Carte sanitaire", "Renouveler NIE"],
  ar: ["ما هو الحد الأدنى للدخل؟", "التسجيل البلدي", "البطاقة الصحية", "تجديد NIE"],
  en: ["What is the IMV?", "Municipal registration", "Health card", "Renew NIE"],
  pt: ["O que e o IMV?", "Inscricao municipal", "Cartao de saude", "Renovar NIE"],
  ro: ["Ce este IMV?", "Inregistrare municipala", "Card de sanatate", "Reinnoire NIE"],
  ca: ["Que es l'IMV?", "Empadronament", "Targeta sanitaria", "Renovar NIE"],
  zh: ["什么是IMV？", "市政登记", "医疗卡", "续签NIE"],
};

/* ------------------------------------------------------------------ */
/*  Prompt bar placeholder                                            */
/* ------------------------------------------------------------------ */

export const PROMPT_PLACEHOLDER: Record<Language, string> = {
  es: "Pregunta algo a Clara...",
  fr: "Pose une question à Clara...",
  ar: "...اسأل كلارا",
  en: "Ask Clara something...",
  pt: "Pergunta algo a Clara...",
  ro: "Intreaba-o pe Clara...",
  ca: "Pregunta alguna cosa a Clara...",
  zh: "问Clara一些事情...",
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
  en: [
    { href: "/como-usar", label: "How to use Clara" },
    { href: "/quienes-somos", label: "About us" },
    { href: "/futuro", label: "The future of Clara" },
  ],
  pt: [
    { href: "/como-usar", label: "Como usar a Clara" },
    { href: "/quienes-somos", label: "Quem somos" },
    { href: "/futuro", label: "O futuro da Clara" },
  ],
  ro: [
    { href: "/como-usar", label: "Cum se utilizeaza Clara" },
    { href: "/quienes-somos", label: "Cine suntem" },
    { href: "/futuro", label: "Viitorul Clara" },
  ],
  ca: [
    { href: "/como-usar", label: "Com utilitzar Clara" },
    { href: "/quienes-somos", label: "Qui som" },
    { href: "/futuro", label: "El futur de Clara" },
  ],
  zh: [
    { href: "/como-usar", label: "如何使用Clara" },
    { href: "/quienes-somos", label: "关于我们" },
    { href: "/futuro", label: "Clara的未来" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Sub-page titles                                                   */
/* ------------------------------------------------------------------ */

export const SUB_PAGE_TITLES: Record<Language, Record<string, string>> = {
  es: { "como-usar": "Cómo usar Clara", "quienes-somos": "Quiénes somos", "futuro": "El futuro de Clara" },
  fr: { "como-usar": "Comment utiliser Clara", "quienes-somos": "Qui sommes-nous", "futuro": "L'avenir de Clara" },
  ar: { "como-usar": "كيف تستخدم كلارا", "quienes-somos": "من نحن", "futuro": "مستقبل كلارا" },
  en: { "como-usar": "How to use Clara", "quienes-somos": "About us", "futuro": "The future of Clara" },
  pt: { "como-usar": "Como usar a Clara", "quienes-somos": "Quem somos", "futuro": "O futuro da Clara" },
  ro: { "como-usar": "Cum se utilizeaza Clara", "quienes-somos": "Cine suntem", "futuro": "Viitorul Clara" },
  ca: { "como-usar": "Com utilitzar Clara", "quienes-somos": "Qui som", "futuro": "El futur de Clara" },
  zh: { "como-usar": "如何使用Clara", "quienes-somos": "关于我们", "futuro": "Clara的未来" },
};
