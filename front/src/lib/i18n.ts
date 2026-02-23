/* ================================================================== */
/*  i18n.ts — Strings centralizados (ES/EN/FR/PT/RO/CA/ZH/AR)        */
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
  en: {
    greeting: "Hi, I'm Clara",
    tagline: ["Your voice", "has power"],
    description: "I help you with social procedures in Spain. Speak or write in your language.",
    mic_label: "Tap to speak",
    topics_hint: "Or choose a topic:",
    cta_text: "I prefer to write",
    footer: "Free · Confidential · In your language",
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
  pt: {
    greeting: "Olá, sou Clara",
    tagline: ["A tua voz", "tem poder"],
    description: "Ajudo-te com trâmites sociais em Espanha. Fala ou escreve no teu idioma.",
    mic_label: "Toca para falar",
    topics_hint: "Ou escolhe um tema:",
    cta_text: "Prefiro escrever",
    footer: "Gratuito · Confidencial · No teu idioma",
  },
  ro: {
    greeting: "Bună, sunt Clara",
    tagline: ["Vocea ta", "are putere"],
    description: "Te ajut cu proceduri sociale în Spania. Vorbește sau scrie în limba ta.",
    mic_label: "Apasă pentru a vorbi",
    topics_hint: "Sau alege un subiect:",
    cta_text: "Prefer să scriu",
    footer: "Gratuit · Confidențial · În limba ta",
  },
  ca: {
    greeting: "Hola, soc Clara",
    tagline: ["La teva veu", "té poder"],
    description: "T'ajudo amb tràmits socials a Espanya. Parla o escriu en el teu idioma.",
    mic_label: "Toca per parlar",
    topics_hint: "O tria un tema:",
    cta_text: "Prefereixo escriure",
    footer: "Gratuït · Confidencial · En el teu idioma",
  },
  zh: {
    greeting: "你好，我是Clara",
    tagline: ["你的声音", "有力量"],
    description: "我帮你处理西班牙的社会事务。用你的语言说话或写字。",
    mic_label: "点击说话",
    topics_hint: "或选择一个主题：",
    cta_text: "我更想打字",
    footer: "免费 · 保密 · 用你的语言",
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
    { icon: "coin", label: "Ayudas\neconómicas", speech: "Ayudas economicas como IMV, pensiones o subsidios" },
    { icon: "house", label: "Vivienda y\nregistro", speech: "Empadronamiento y bono social electrico" },
    { icon: "health", label: "Salud y\nfamilia", speech: "Tarjeta sanitaria, baja maternidad y dependencia" },
    { icon: "doc", label: "Extranjería", speech: "NIE, TIE, arraigo y reagrupacion familiar" },
  ],
  en: [
    { icon: "coin", label: "Financial\naid", speech: "Financial aid like minimum income, pensions or subsidies" },
    { icon: "house", label: "Housing &\nregistration", speech: "Municipal registration and electricity social bonus" },
    { icon: "health", label: "Health &\nfamily", speech: "Health card, parental leave and dependency" },
    { icon: "doc", label: "Immigration", speech: "NIE, TIE, residency and family reunification" },
  ],
  fr: [
    { icon: "coin", label: "Aides\nfinancières", speech: "Aides financieres comme le RMV, pensions ou allocations" },
    { icon: "house", label: "Logement et\ninscription", speech: "Inscription municipale et bon social electrique" },
    { icon: "health", label: "Santé et\nfamille", speech: "Carte sanitaire, conge maternite et dependance" },
    { icon: "doc", label: "Immigration", speech: "NIE, TIE, enracinement et regroupement familial" },
  ],
  pt: [
    { icon: "coin", label: "Ajudas\nfinanceiras", speech: "Ajudas financeiras como rendimento minimo, pensoes ou subsidios" },
    { icon: "house", label: "Habitação e\nregisto", speech: "Empadronamento e bonus social eletrico" },
    { icon: "health", label: "Saúde e\nfamília", speech: "Cartao de saude, licenca parental e dependencia" },
    { icon: "doc", label: "Imigração", speech: "NIE, TIE, arraigo e reagrupamento familiar" },
  ],
  ro: [
    { icon: "coin", label: "Ajutor\nfinanciar", speech: "Ajutoare financiare precum venitul minim, pensii sau subventii" },
    { icon: "house", label: "Locuință și\nînregistrare", speech: "Inregistrare municipala si bonusul social electric" },
    { icon: "health", label: "Sănătate și\nfamilie", speech: "Card de sanatate, concediu parental si dependenta" },
    { icon: "doc", label: "Imigrație", speech: "NIE, TIE, arraigo si reintregirea familiei" },
  ],
  ca: [
    { icon: "coin", label: "Ajudes\neconòmiques", speech: "Ajudes economiques com l'IMV, pensions o subsidis" },
    { icon: "house", label: "Habitatge i\nregistre", speech: "Empadronament i bo social electric" },
    { icon: "health", label: "Salut i\nfamília", speech: "Targeta sanitaria, baixa maternitat i dependencia" },
    { icon: "doc", label: "Estrangeria", speech: "NIE, TIE, arrelament i reagrupament familiar" },
  ],
  zh: [
    { icon: "coin", label: "经济\n援助", speech: "经济援助，如最低收入、养老金或补贴" },
    { icon: "house", label: "住房与\n登记", speech: "市政登记和电力社会补贴" },
    { icon: "health", label: "健康与\n家庭", speech: "医疗卡、产假和护理依赖" },
    { icon: "doc", label: "移民", speech: "NIE、TIE、扎根居留和家庭团聚" },
  ],
  ar: [
    { icon: "coin", label: "مساعدات\nمالية", speech: "المساعدات المالية مثل الحد الأدنى للدخل والمعاشات والإعانات" },
    { icon: "house", label: "سكن\nوتسجيل", speech: "التسجيل البلدي والمكافأة الاجتماعية للكهرباء" },
    { icon: "health", label: "صحة\nوعائلة", speech: "البطاقة الصحية وإجازة الأمومة والرعاية" },
    { icon: "doc", label: "هجرة", speech: "NIE وTIE والإقامة ولم شمل الأسرة" },
  ],
};

/* ------------------------------------------------------------------ */
/*  Quick-reply chips (chat)                                          */
/* ------------------------------------------------------------------ */

export const QUICK_REPLIES: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "Bono social eléctrico", "Reagrupación familiar", "Baja por nacimiento"],
  en: ["What is the IMV?", "Electricity social bonus", "Family reunification", "Parental leave"],
  fr: ["Qu'est-ce que le RMV?", "Bon social électrique", "Regroupement familial", "Congé parental"],
  pt: ["O que é o IMV?", "Bónus social elétrico", "Reagrupamento familiar", "Licença parental"],
  ro: ["Ce este VMI?", "Bonus social electric", "Reîntregirea familiei", "Concediu parental"],
  ca: ["Què és l'IMV?", "Bo social elèctric", "Reagrupament familiar", "Baixa per naixement"],
  zh: ["什么是最低生活保障？", "电力社会补贴", "家庭团聚", "产假"],
  ar: ["ما هو الحد الأدنى للدخل؟", "المكافأة الاجتماعية للكهرباء", "لم شمل الأسرة", "إجازة الولادة"],
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
  en: {
    counter_label: "vulnerable people in Spain don't access benefits",
    before_label: "Before",
    after_label: "With Clara",
  },
  fr: {
    counter_label: "personnes vulnérables en Espagne n'accèdent pas aux aides",
    before_label: "Avant",
    after_label: "Avec Clara",
  },
  pt: {
    counter_label: "pessoas vulneráveis em Espanha não acedem a ajudas",
    before_label: "Antes",
    after_label: "Com Clara",
  },
  ro: {
    counter_label: "persoane vulnerabile din Spania nu accesează ajutoare",
    before_label: "Înainte",
    after_label: "Cu Clara",
  },
  ca: {
    counter_label: "persones vulnerables a Espanya no accedeixen a ajudes",
    before_label: "Abans",
    after_label: "Amb Clara",
  },
  zh: {
    counter_label: "西班牙的弱势群体无法获得援助",
    before_label: "之前",
    after_label: "有了Clara",
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
      en: "\"I just want to know if I have the right to see a doctor.\"",
      fr: "\"Je veux juste savoir si j'ai droit à un médecin.\"",
      pt: "\"Só quero saber se tenho direito a ver um médico.\"",
      ro: "\"Vreau doar să știu dacă am dreptul să văd un medic.\"",
      ca: "\"Només vull saber si tinc dret a veure un metge.\"",
      zh: "\"我只想知道我是否有权看医生。\"",
      ar: "\"أريد فقط أن أعرف هل لي الحق في رؤية طبيب.\"",
    },
  },
  {
    id: "ahmed",
    name: "Ahmed, 34",
    quote: {
      es: "\"Llevo 3 meses esperando y nadie me explica nada.\"",
      en: "\"I've been waiting 3 months and nobody explains anything to me.\"",
      fr: "\"Cela fait 3 mois que j'attends et personne ne m'explique rien.\"",
      pt: "\"Espero há 3 meses e ninguém me explica nada.\"",
      ro: "\"Aștept de 3 luni și nimeni nu îmi explică nimic.\"",
      ca: "\"Porto 3 mesos esperant i ningú m'explica res.\"",
      zh: "\"我已经等了3个月，没人跟我解释任何事。\"",
      ar: "\"انتظرت 3 أشهر ولم يشرح لي أحد شيئاً.\"",
    },
  },
  {
    id: "fatima",
    name: "Fátima, 42",
    quote: {
      es: "\"No puedo leer los formularios. Están en un español que no entiendo.\"",
      en: "\"I can't read the forms. They're in a Spanish I don't understand.\"",
      fr: "\"Je ne peux pas lire les formulaires. Ils sont dans un espagnol que je ne comprends pas.\"",
      pt: "\"Não consigo ler os formulários. Estão num espanhol que não entendo.\"",
      ro: "\"Nu pot citi formularele. Sunt într-o spaniolă pe care nu o înțeleg.\"",
      ca: "\"No puc llegir els formularis. Estan en un castellà que no entenc.\"",
      zh: "\"我看不懂表格。它们是用我不懂的西班牙语写的。\"",
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
    { value: "8", label: "idiomas" },
    { value: "23", label: "trámites" },
    { value: "<3s", label: "respuesta" },
  ],
  en: [
    { value: "17", label: "regions" },
    { value: "8", label: "languages" },
    { value: "23", label: "procedures" },
    { value: "<3s", label: "response" },
  ],
  fr: [
    { value: "17", label: "régions" },
    { value: "8", label: "langues" },
    { value: "23", label: "démarches" },
    { value: "<3s", label: "réponse" },
  ],
  pt: [
    { value: "17", label: "regiões" },
    { value: "8", label: "idiomas" },
    { value: "23", label: "trâmites" },
    { value: "<3s", label: "resposta" },
  ],
  ro: [
    { value: "17", label: "regiuni" },
    { value: "8", label: "limbi" },
    { value: "23", label: "proceduri" },
    { value: "<3s", label: "răspuns" },
  ],
  ca: [
    { value: "17", label: "CCAA" },
    { value: "8", label: "idiomes" },
    { value: "23", label: "tràmits" },
    { value: "<3s", label: "resposta" },
  ],
  zh: [
    { value: "17", label: "地区" },
    { value: "8", label: "语言" },
    { value: "23", label: "手续" },
    { value: "<3秒", label: "响应" },
  ],
  ar: [
    { value: "17", label: "منطقة" },
    { value: "8", label: "لغات" },
    { value: "23", label: "إجراءات" },
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
  en: [
    {
      before: "A 4-page form in legal Spanish",
      after: "\"Do you have a passport and a contract? Then you can register.\"",
    },
    {
      before: "Waiting 45 minutes in a queue to be told a paper is missing",
      after: "\"You need: NIE + contract. Got them? Perfect, let's go step by step.\"",
    },
    {
      before: "Searching 5 different websites without understanding anything",
      after: "\"The IMV is a 604€/month benefit. Let me tell you the requirements.\"",
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
  pt: [
    {
      before: "Um formulário de 4 páginas em espanhol jurídico",
      after: "\"Tens passaporte e contrato? Então podes registar-te.\"",
    },
    {
      before: "Esperar 45 minutos numa fila para que digam que falta um papel",
      after: "\"Precisas de: NIE + contrato. Tens? Perfeito, vamos passo a passo.\"",
    },
    {
      before: "Procurar em 5 sites diferentes sem entender nada",
      after: "\"O IMV é uma ajuda de 604€/mês. Vou contar-te os requisitos.\"",
    },
  ],
  ro: [
    {
      before: "Un formular de 4 pagini în spaniolă juridică",
      after: "\"Ai pașaport și contract? Atunci te poți înregistra.\"",
    },
    {
      before: "Așteptarea 45 de minute la coadă pentru a ți se spune că lipsește un document",
      after: "\"Ai nevoie de: NIE + contract. Le ai? Perfect, mergem pas cu pas.\"",
    },
    {
      before: "Căutarea pe 5 site-uri diferite fără a înțelege nimic",
      after: "\"VMI este un ajutor de 604€/lună. Îți spun condițiile.\"",
    },
  ],
  ca: [
    {
      before: "Un formulari de 4 pàgines en castellà jurídic",
      after: "\"Tens passaport i contracte? Doncs pots empadronar-te.\"",
    },
    {
      before: "Esperar 45 minuts en una cua perquè et diguin que falta un paper",
      after: "\"Necessites: NIE + contracte. Els tens? Perfecte, anem pas a pas.\"",
    },
    {
      before: "Buscar en 5 webs diferents sense entendre res",
      after: "\"L'IMV és una ajuda de 604€/mes. Et dic els requisits.\"",
    },
  ],
  zh: [
    {
      before: "4页法律西班牙语表格",
      after: "\"你有护照和合同吗？那你可以注册。\"",
    },
    {
      before: "排队等45分钟被告知缺少文件",
      after: "\"你需要：NIE + 合同。都有了吗？完美，我们一步一步来。\"",
    },
    {
      before: "在5个不同网站搜索却什么都看不懂",
      after: "\"IMV是每月604欧元的补助。让我告诉你条件。\"",
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
  es: ["¿Qué es el IMV?", "Pensiones no contributivas", "Bono social eléctrico", "Reagrupación familiar"],
  en: ["What is the IMV?", "Non-contributory pensions", "Electricity social bonus", "Family reunification"],
  fr: ["Qu'est-ce que le RMV?", "Pensions non contributives", "Bon social électrique", "Regroupement familial"],
  pt: ["O que é o IMV?", "Pensões não contributivas", "Bónus social elétrico", "Reagrupamento familiar"],
  ro: ["Ce este VMI?", "Pensii necontributive", "Bonus social electric", "Reîntregirea familiei"],
  ca: ["Què és l'IMV?", "Pensions no contributives", "Bo social elèctric", "Reagrupament familiar"],
  zh: ["什么是最低生活保障？", "非缴费型养老金", "电力社会补贴", "家庭团聚"],
  ar: ["ما هو الحد الأدنى للدخل؟", "المعاشات غير الاشتراكية", "المكافأة الاجتماعية للكهرباء", "لم شمل الأسرة"],
};

/* ------------------------------------------------------------------ */
/*  Prompt bar placeholder                                            */
/* ------------------------------------------------------------------ */

export const PROMPT_PLACEHOLDER: Record<Language, string> = {
  es: "Pregunta algo a Clara...",
  en: "Ask Clara something...",
  fr: "Pose une question à Clara...",
  pt: "Pergunta algo à Clara...",
  ro: "Întreabă-o pe Clara...",
  ca: "Pregunta alguna cosa a Clara...",
  zh: "问Clara一些问题...",
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
    { href: "/info-legal", label: "Info legal" },
  ],
  en: [
    { href: "/como-usar", label: "How to use Clara" },
    { href: "/quienes-somos", label: "About us" },
    { href: "/futuro", label: "The future of Clara" },
    { href: "/info-legal", label: "Legal info" },
  ],
  fr: [
    { href: "/como-usar", label: "Comment utiliser Clara" },
    { href: "/quienes-somos", label: "Qui sommes-nous" },
    { href: "/futuro", label: "L'avenir de Clara" },
    { href: "/info-legal", label: "Infos légales" },
  ],
  pt: [
    { href: "/como-usar", label: "Como usar Clara" },
    { href: "/quienes-somos", label: "Quem somos" },
    { href: "/futuro", label: "O futuro da Clara" },
    { href: "/info-legal", label: "Info legal" },
  ],
  ro: [
    { href: "/como-usar", label: "Cum folosești Clara" },
    { href: "/quienes-somos", label: "Cine suntem" },
    { href: "/futuro", label: "Viitorul Clarei" },
    { href: "/info-legal", label: "Info legale" },
  ],
  ca: [
    { href: "/como-usar", label: "Com usar Clara" },
    { href: "/quienes-somos", label: "Qui som" },
    { href: "/futuro", label: "El futur de Clara" },
    { href: "/info-legal", label: "Info legal" },
  ],
  zh: [
    { href: "/como-usar", label: "如何使用Clara" },
    { href: "/quienes-somos", label: "关于我们" },
    { href: "/futuro", label: "Clara的未来" },
    { href: "/info-legal", label: "法律信息" },
  ],
  ar: [
    { href: "/como-usar", label: "كيف تستخدم كلارا" },
    { href: "/quienes-somos", label: "من نحن" },
    { href: "/futuro", label: "مستقبل كلارا" },
    { href: "/info-legal", label: "المعلومات القانونية" },
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
  en: {
    title: "The invisible wall",
    subtitle: "4.5 million vulnerable people in Spain don't access the benefits they're entitled to due to language barriers and bureaucracy.",
  },
  fr: {
    title: "Le mur invisible",
    subtitle: "4,5 millions de personnes vulnérables en Espagne n'accèdent pas aux aides auxquelles elles ont droit à cause des barrières linguistiques et bureaucratiques.",
  },
  pt: {
    title: "O muro invisível",
    subtitle: "4,5 milhões de pessoas vulneráveis em Espanha não acedem às ajudas a que têm direito por barreiras linguísticas e burocráticas.",
  },
  ro: {
    title: "Zidul invizibil",
    subtitle: "4,5 milioane de persoane vulnerabile din Spania nu accesează ajutoarele la care au dreptul din cauza barierelor lingvistice și birocratice.",
  },
  ca: {
    title: "El mur invisible",
    subtitle: "4,5 milions de persones vulnerables a Espanya no accedeixen a les ajudes que els corresponen per barreres d'idioma i burocràcia.",
  },
  zh: {
    title: "隐形的墙",
    subtitle: "西班牙450万弱势群体因语言障碍和官僚主义无法获得他们应得的援助。",
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
  en: {
    empathy: "We know what it's like to sit in an office without understanding a word. Clara was born so you don't have to go through that alone.",
    authority: "Verified information from official sources. Clear answers, in your language, when you need them.",
  },
  fr: {
    empathy: "Nous savons ce que c'est de s'asseoir dans un bureau sans comprendre un mot. Clara est née pour que tu n'aies pas à vivre ça seule.",
    authority: "Informations vérifiées à partir de sources officielles. Des réponses claires, dans ta langue, quand tu en as besoin.",
  },
  pt: {
    empathy: "Sabemos o que é sentar-se num escritório sem entender uma palavra. Clara nasceu para que não tenhas que passar por isso sozinha.",
    authority: "Informação verificada de fontes oficiais. Respostas claras, no teu idioma, quando precisas.",
  },
  ro: {
    empathy: "Știm ce înseamnă să stai într-un birou fără să înțelegi un cuvânt. Clara s-a născut pentru ca tu să nu treci prin asta singură.",
    authority: "Informații verificate din surse oficiale. Răspunsuri clare, în limba ta, când ai nevoie.",
  },
  ca: {
    empathy: "Sabem el que és seure en una oficina sense entendre una paraula. Clara va néixer perquè no hagis de passar per això sola.",
    authority: "Informació verificada de fonts oficials. Respostes clares, en el teu idioma, quan les necessitis.",
  },
  zh: {
    empathy: "我们知道坐在办公室里一个字都听不懂是什么感觉。Clara的诞生就是为了让你不必独自面对。",
    authority: "来自官方来源的经过验证的信息。用你的语言，在你需要的时候，给你清晰的答案。",
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
  en: {
    title: "It's that easy",
    steps: [
      { number: "1", text: "Open Clara from your phone" },
      { number: "2", text: "Speak or write in your language" },
      { number: "3", text: "Get clear steps with official links" },
    ],
    agreements: [
      { icon: "free", text: "Free" },
      { icon: "lock", text: "Confidential" },
      { icon: "no-register", text: "No registration" },
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
  pt: {
    title: "É assim tão fácil",
    steps: [
      { number: "1", text: "Abre Clara no teu telemóvel" },
      { number: "2", text: "Fala ou escreve no teu idioma" },
      { number: "3", text: "Recebe passos claros com links oficiais" },
    ],
    agreements: [
      { icon: "free", text: "Gratuito" },
      { icon: "lock", text: "Confidencial" },
      { icon: "no-register", text: "Sem registo" },
      { icon: "clock", text: "24/7" },
    ],
  },
  ro: {
    title: "Atât de simplu",
    steps: [
      { number: "1", text: "Deschide Clara de pe telefonul tău" },
      { number: "2", text: "Vorbește sau scrie în limba ta" },
      { number: "3", text: "Primește pași clari cu linkuri oficiale" },
    ],
    agreements: [
      { icon: "free", text: "Gratuit" },
      { icon: "lock", text: "Confidențial" },
      { icon: "no-register", text: "Fără înregistrare" },
      { icon: "clock", text: "24/7" },
    ],
  },
  ca: {
    title: "Així de fàcil",
    steps: [
      { number: "1", text: "Obre Clara des del teu mòbil" },
      { number: "2", text: "Parla o escriu en el teu idioma" },
      { number: "3", text: "Rep passos clars amb enllaços oficials" },
    ],
    agreements: [
      { icon: "free", text: "Gratuït" },
      { icon: "lock", text: "Confidencial" },
      { icon: "no-register", text: "Sense registre" },
      { icon: "clock", text: "24/7" },
    ],
  },
  zh: {
    title: "就是这么简单",
    steps: [
      { number: "1", text: "在手机上打开Clara" },
      { number: "2", text: "用你的语言说话或写字" },
      { number: "3", text: "获得清晰的步骤和官方链接" },
    ],
    agreements: [
      { icon: "free", text: "免费" },
      { icon: "lock", text: "保密" },
      { icon: "no-register", text: "无需注册" },
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
  en: {
    quote: "Understanding your rights shouldn't be a privilege.",
    tagline: ["Your voice", "has power"],
    transformation_from: "Confused, excluded, afraid of the system",
    transformation_to: "Informed, empowered, exercising their rights",
  },
  fr: {
    quote: "Comprendre tes droits ne devrait pas être un privilège.",
    tagline: ["Ta voix", "a du pouvoir"],
    transformation_from: "Confuse, exclue, effrayée par le système",
    transformation_to: "Informée, autonome, exerçant ses droits",
  },
  pt: {
    quote: "Entender os teus direitos não deveria ser um privilégio.",
    tagline: ["A tua voz", "tem poder"],
    transformation_from: "Confusa, excluída, com medo do sistema",
    transformation_to: "Informada, empoderada, exercendo os seus direitos",
  },
  ro: {
    quote: "Înțelegerea drepturilor tale nu ar trebui să fie un privilegiu.",
    tagline: ["Vocea ta", "are putere"],
    transformation_from: "Confuză, exclusă, cu frică de sistem",
    transformation_to: "Informată, împuternicită, exercitându-și drepturile",
  },
  ca: {
    quote: "Entendre els teus drets no hauria de ser un privilegi.",
    tagline: ["La teva veu", "té poder"],
    transformation_from: "Confusa, exclosa, amb por del sistema",
    transformation_to: "Informada, empoderada, exercint els seus drets",
  },
  zh: {
    quote: "了解你的权利不应该是一种特权。",
    tagline: ["你的声音", "有力量"],
    transformation_from: "困惑、被排斥、害怕制度",
    transformation_to: "知情、赋权、行使自己的权利",
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
  en: {
    headline: "Talk to Clara now",
    mic_label: "Tap to speak",
  },
  fr: {
    headline: "Parle avec Clara maintenant",
    mic_label: "Appuie pour parler",
  },
  pt: {
    headline: "Fala com Clara agora",
    mic_label: "Toca para falar",
  },
  ro: {
    headline: "Vorbește cu Clara acum",
    mic_label: "Apasă pentru a vorbi",
  },
  ca: {
    headline: "Parla amb Clara ara",
    mic_label: "Toca per parlar",
  },
  zh: {
    headline: "现在和Clara对话",
    mic_label: "点击说话",
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
      { href: "/info-legal", label: "Info legal" },
    ],
  },
  en: {
    credits: "Made with love at OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "How to use" },
      { href: "/quienes-somos", label: "About us" },
      { href: "/futuro", label: "Future" },
      { href: "/info-legal", label: "Legal info" },
    ],
  },
  fr: {
    credits: "Fait avec amour à OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "Comment utiliser" },
      { href: "/quienes-somos", label: "Qui sommes-nous" },
      { href: "/futuro", label: "Avenir" },
      { href: "/info-legal", label: "Infos légales" },
    ],
  },
  pt: {
    credits: "Feito com amor no OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "Como usar" },
      { href: "/quienes-somos", label: "Quem somos" },
      { href: "/futuro", label: "Futuro" },
      { href: "/info-legal", label: "Info legal" },
    ],
  },
  ro: {
    credits: "Făcut cu dragoste la OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "Cum folosești" },
      { href: "/quienes-somos", label: "Cine suntem" },
      { href: "/futuro", label: "Viitor" },
      { href: "/info-legal", label: "Info legale" },
    ],
  },
  ca: {
    credits: "Fet amb amor a OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "Com usar" },
      { href: "/quienes-somos", label: "Qui som" },
      { href: "/futuro", label: "Futur" },
      { href: "/info-legal", label: "Info legal" },
    ],
  },
  zh: {
    credits: "在OdiseIA4Good 2026用爱制作",
    links: [
      { href: "/como-usar", label: "如何使用" },
      { href: "/quienes-somos", label: "关于我们" },
      { href: "/futuro", label: "未来" },
      { href: "/info-legal", label: "法律信息" },
    ],
  },
  ar: {
    credits: "صُنع بحب في OdiseIA4Good 2026",
    links: [
      { href: "/como-usar", label: "كيف تستخدم" },
      { href: "/quienes-somos", label: "من نحن" },
      { href: "/futuro", label: "المستقبل" },
      { href: "/info-legal", label: "المعلومات القانونية" },
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
  en: {
    empatizar: {
      title: "This shouldn't be so hard",
      body: "We know what it's like to sit in a public office without understanding a word. That knot in your stomach when they hand you a four-page form in legal Spanish. That fear of asking because you don't want to bother anyone. That feeling that the system wasn't made for you.",
      stat: "You're not alone. 4.5 million people in Spain go through this every day.",
    },
    validar: {
      title: "Understanding your rights shouldn't be a privilege",
      body: "If you live in Spain, you have rights. The right to healthcare. The right to municipal registration. The right to financial assistance if you need it. But accessing them requires navigating a maze of forms, websites, and offices that were not designed with you in mind.",
      closing: "That's not right.",
    },
    momento: {
      title: "That's why Clara exists",
      body: "In February 2026, five of us sat down at a hackathon with one question: What if you could access your rights simply by talking?\n\nWe didn't want to build another chatbot. We wanted to build something that works the way real life works: you tell someone your situation, and that person tells you exactly what to do, step by step, in your language.\n\nThat's how Clara was born.",
    },
    equipo: {
      title: "Who we are",
      intro: "We're not the heroes of this story — you are.",
      members: [
        { name: "Andrea", role: "Creator of Clara" },
      ],
    },
    cta: {
      title: "Your voice has power",
      body: "Clara is ready to help you. Speak or write in your language.",
      button: "Talk to Clara now",
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
  pt: {
    empatizar: {
      title: "Isto não devia ser tão difícil",
      body: "Sabemos o que é sentar-se num serviço público sem entender uma palavra. Aquele nó no estômago quando te dão um formulário de quatro páginas em espanhol jurídico. Aquele medo de perguntar porque não queres incomodar. Aquela sensação de que o sistema não foi feito para ti.",
      stat: "Não estás sozinha. 4,5 milhões de pessoas em Espanha passam por isto todos os dias.",
    },
    validar: {
      title: "Entender os teus direitos não deveria ser um privilégio",
      body: "Se vives em Espanha, tens direitos. Direito à saúde. Direito ao empadronamento. Direito a ajudas económicas se precisares. Mas aceder a eles exige navegar um labirinto de formulários, sites e serviços que não foram pensados para ti.",
      closing: "Isso não está certo.",
    },
    momento: {
      title: "Por isso existe Clara",
      body: "Em fevereiro de 2026, cinco pessoas sentámo-nos num hackathon com uma pergunta: E se pudesses aceder aos teus direitos simplesmente falando?\n\nNão queríamos construir mais um chatbot. Queríamos construir algo que funcionasse como funciona a vida real: contas a alguém a tua situação, e essa pessoa diz-te exatamente o que fazer, passo a passo, no teu idioma.\n\nAssim nasceu Clara.",
    },
    equipo: {
      title: "Quem somos",
      intro: "Não somos os heróis desta história — os heróis são vocês.",
      members: [
        { name: "Andrea", role: "Criadora de Clara" },
      ],
    },
    cta: {
      title: "A tua voz tem poder",
      body: "Clara está pronta para te ajudar. Fala ou escreve no teu idioma.",
      button: "Fala com Clara agora",
    },
  },
  ro: {
    empatizar: {
      title: "Asta nu ar trebui să fie atât de greu",
      body: "Știm ce înseamnă să stai într-un birou public fără să înțelegi un cuvânt. Acel nod în stomac când ți se dă un formular de patru pagini în spaniolă juridică. Frica de a întreba pentru că nu vrei să deranjezi. Sentimentul că sistemul nu a fost creat pentru tine.",
      stat: "Nu ești singură. 4,5 milioane de oameni din Spania trec prin asta în fiecare zi.",
    },
    validar: {
      title: "Înțelegerea drepturilor tale nu ar trebui să fie un privilegiu",
      body: "Dacă locuiești în Spania, ai drepturi. Dreptul la sănătate. Dreptul la înregistrare municipală. Dreptul la ajutoare financiare dacă ai nevoie. Dar accesarea lor necesită navigarea unui labirint de formulare, site-uri și birouri care nu au fost concepute cu tine în minte.",
      closing: "Asta nu este corect.",
    },
    momento: {
      title: "De aceea există Clara",
      body: "În februarie 2026, cinci oameni s-au așezat la un hackathon cu o întrebare: Ce-ar fi dacă ai putea accesa drepturile tale pur și simplu vorbind?\n\nNu voiam să construim un alt chatbot. Voiam să construim ceva care funcționează așa cum funcționează viața reală: îi spui cuiva situația ta, și acea persoană îți spune exact ce să faci, pas cu pas, în limba ta.\n\nAstfel s-a născut Clara.",
    },
    equipo: {
      title: "Cine suntem",
      intro: "Nu suntem eroii acestei povești — eroii sunteți voi.",
      members: [
        { name: "Andrea", role: "Creatoarea Clarei" },
      ],
    },
    cta: {
      title: "Vocea ta are putere",
      body: "Clara este gata să te ajute. Vorbește sau scrie în limba ta.",
      button: "Vorbește cu Clara acum",
    },
  },
  ca: {
    empatizar: {
      title: "Això no hauria de ser tan difícil",
      body: "Sabem el que és seure en una oficina pública sense entendre una paraula. Aquell nus a l'estómac quan et donen un formulari de quatre pàgines en castellà jurídic. Aquella por de preguntar perquè no vols molestar. Aquella sensació que el sistema no va ser fet per a tu.",
      stat: "No estàs sola. 4,5 milions de persones a Espanya passen per això cada dia.",
    },
    validar: {
      title: "Entendre els teus drets no hauria de ser un privilegi",
      body: "Si vius a Espanya, tens drets. Dret a la sanitat. Dret a l'empadronament. Dret a ajudes econòmiques si les necessites. Però accedir-hi requereix navegar un laberint de formularis, webs i oficines que no van ser dissenyats pensant en tu.",
      closing: "Això no està bé.",
    },
    momento: {
      title: "Per això existeix Clara",
      body: "Al febrer de 2026, cinc persones ens vam asseure en un hackathon amb una pregunta: I si poguessis accedir als teus drets simplement parlant?\n\nNo volíem construir un altre chatbot. Volíem construir alguna cosa que funcionés com funciona la vida real: expliques a algú la teva situació, i aquella persona et diu exactament què fer, pas a pas, en el teu idioma.\n\nAixí va néixer Clara.",
    },
    equipo: {
      title: "Qui som",
      intro: "No som els herois d'aquesta història — els herois sou vosaltres.",
      members: [
        { name: "Andrea", role: "Creadora de Clara" },
      ],
    },
    cta: {
      title: "La teva veu té poder",
      body: "Clara està llesta per ajudar-te. Parla o escriu en el teu idioma.",
      button: "Parla amb Clara ara",
    },
  },
  zh: {
    empatizar: {
      title: "这不应该这么难",
      body: "我们知道坐在公共办公室里一个字都听不懂是什么感觉。当他们递给你一份四页法律西班牙语表格时，胃里那种紧绷感。那种不敢开口问问题的恐惧，因为不想麻烦别人。那种感觉——这个系统根本不是为你设计的。",
      stat: "你并不孤单。西班牙每天有450万人经历同样的事情。",
    },
    validar: {
      title: "了解你的权利不应该是一种特权",
      body: "如果你住在西班牙，你就有权利。享有医疗保健的权利。办理市政登记的权利。在需要时获得经济援助的权利。但要获得这些权利，你需要穿越一个由表格、网站和办公室组成的迷宫，而这一切都不是为你设计的。",
      closing: "这不公平。",
    },
    momento: {
      title: "这就是Clara存在的原因",
      body: "2026年2月，五个人坐在一个黑客马拉松上，带着一个问题：如果你只需开口说话就能获得自己的权利呢？\n\n我们不想再造一个聊天机器人。我们想造一个像真实生活一样运作的东西：你把自己的情况告诉它，它就一步一步地、用你的语言，告诉你该怎么做。\n\nClara就这样诞生了。",
    },
    equipo: {
      title: "我们是谁",
      intro: "我们不是这个故事的英雄——你们才是。",
      members: [
        { name: "Andrea", role: "Clara的创造者" },
      ],
    },
    cta: {
      title: "你的声音有力量",
      body: "Clara已准备好帮助你。用你的语言说话或写字。",
      button: "现在和Clara对话",
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

/* ------------------------------------------------------------------ */
/*  Como Usar page — StoryBrand SB7 narrative                         */
/* ------------------------------------------------------------------ */

export const COMO_USAR_PAGE: Record<Language, {
  empathy_headline: string;
  empathy_sub: string;
  steps_title: string;
  steps: { title: string; desc: string }[];
  examples_title: string;
  examples: string[];
  guarantees: { icon: string; text: string }[];
  cta_headline: string;
  cta_sub: string;
  cta_button: string;
}> = {
  es: {
    empathy_headline: "No necesitas entender el sistema",
    empathy_sub: "Solo habla. Clara te guía paso a paso, en tu idioma, con información oficial verificada.",
    steps_title: "Así funciona",
    steps: [
      { title: "Abre Clara", desc: "Desde tu móvil o computadora. Sin descargas, sin registro." },
      { title: "Elige tu idioma", desc: "Español, francés, árabe y más. Clara te entiende." },
      { title: "Habla o escribe", desc: "Pulsa el micrófono para hablar, o escribe tu pregunta." },
      { title: "Recibe tu respuesta", desc: "Pasos claros, links oficiales, en tu idioma. Sin letra pequeña." },
    ],
    examples_title: "Puedes preguntarle cosas como",
    examples: [
      "¿Qué necesito para el empadronamiento?",
      "¿Cómo solicito el Ingreso Mínimo Vital?",
      "¿Qué documentos piden para la tarjeta sanitaria?",
      "¿Cómo renuevo mi NIE?",
    ],
    guarantees: [
      { icon: "free", text: "100% gratuito" },
      { icon: "lock", text: "Tu información es privada" },
      { icon: "no-register", text: "Sin registro ni datos personales" },
      { icon: "clock", text: "Disponible 24/7" },
    ],
    cta_headline: "¿Tienes una duda?",
    cta_sub: "No esperes más. Clara está lista para ayudarte.",
    cta_button: "Habla con Clara",
  },
  en: {
    empathy_headline: "You don't need to understand the system",
    empathy_sub: "Just speak. Clara guides you step by step, in your language, with verified official information.",
    steps_title: "How it works",
    steps: [
      { title: "Open Clara", desc: "From your phone or computer. No downloads, no registration." },
      { title: "Choose your language", desc: "Spanish, French, Arabic and more. Clara understands you." },
      { title: "Speak or write", desc: "Press the mic to speak, or type your question." },
      { title: "Get your answer", desc: "Clear steps, official links, in your language. No fine print." },
    ],
    examples_title: "You can ask things like",
    examples: [
      "What do I need for municipal registration?",
      "How do I apply for the Minimum Vital Income?",
      "What documents are needed for the health card?",
      "How do I renew my NIE?",
    ],
    guarantees: [
      { icon: "free", text: "100% free" },
      { icon: "lock", text: "Your information is private" },
      { icon: "no-register", text: "No registration or personal data" },
      { icon: "clock", text: "Available 24/7" },
    ],
    cta_headline: "Have a question?",
    cta_sub: "Don't wait any longer. Clara is ready to help you.",
    cta_button: "Talk to Clara",
  },
  fr: {
    empathy_headline: "Tu n'as pas besoin de comprendre le système",
    empathy_sub: "Parle, tout simplement. Clara te guide étape par étape, dans ta langue, avec des informations officielles vérifiées.",
    steps_title: "Comment ça marche",
    steps: [
      { title: "Ouvre Clara", desc: "Depuis ton téléphone ou ordinateur. Sans téléchargement, sans inscription." },
      { title: "Choisis ta langue", desc: "Espagnol, français, arabe et plus. Clara te comprend." },
      { title: "Parle ou écris", desc: "Appuie sur le micro pour parler, ou écris ta question." },
      { title: "Reçois ta réponse", desc: "Des étapes claires, des liens officiels, dans ta langue. Sans petites lignes." },
    ],
    examples_title: "Tu peux lui demander par exemple",
    examples: [
      "De quoi ai-je besoin pour l'inscription municipale ?",
      "Comment demander le Revenu Minimum Vital ?",
      "Quels documents pour la carte sanitaire ?",
      "Comment renouveler mon NIE ?",
    ],
    guarantees: [
      { icon: "free", text: "100% gratuit" },
      { icon: "lock", text: "Tes informations sont privées" },
      { icon: "no-register", text: "Sans inscription ni données personnelles" },
      { icon: "clock", text: "Disponible 24h/24, 7j/7" },
    ],
    cta_headline: "Tu as une question ?",
    cta_sub: "N'attends plus. Clara est prête à t'aider.",
    cta_button: "Parle avec Clara",
  },
  pt: {
    empathy_headline: "Não precisas de entender o sistema",
    empathy_sub: "Fala apenas. Clara guia-te passo a passo, no teu idioma, com informação oficial verificada.",
    steps_title: "Como funciona",
    steps: [
      { title: "Abre Clara", desc: "Desde o telemóvel ou computador. Sem descargas, sem registo." },
      { title: "Escolhe o teu idioma", desc: "Espanhol, francês, árabe e mais. Clara compreende-te." },
      { title: "Fala ou escreve", desc: "Carrega no microfone para falar, ou escreve a tua pergunta." },
      { title: "Recebe a tua resposta", desc: "Passos claros, links oficiais, no teu idioma. Sem letras pequenas." },
    ],
    examples_title: "Podes perguntar coisas como",
    examples: [
      "O que preciso para o empadronamento?",
      "Como peço o Rendimento Mínimo Vital?",
      "Que documentos pedem para o cartão de saúde?",
      "Como renovo o meu NIE?",
    ],
    guarantees: [
      { icon: "free", text: "100% gratuito" },
      { icon: "lock", text: "A tua informação é privada" },
      { icon: "no-register", text: "Sem registo nem dados pessoais" },
      { icon: "clock", text: "Disponível 24/7" },
    ],
    cta_headline: "Tens uma dúvida?",
    cta_sub: "Não esperes mais. Clara está pronta para te ajudar.",
    cta_button: "Fala com Clara",
  },
  ro: {
    empathy_headline: "Nu trebuie să înțelegi sistemul",
    empathy_sub: "Doar vorbește. Clara te ghidează pas cu pas, în limba ta, cu informații oficiale verificate.",
    steps_title: "Cum funcționează",
    steps: [
      { title: "Deschide Clara", desc: "De pe telefon sau computer. Fără descărcări, fără înregistrare." },
      { title: "Alege limba ta", desc: "Spaniolă, franceză, arabă și altele. Clara te înțelege." },
      { title: "Vorbește sau scrie", desc: "Apasă microfonul pentru a vorbi, sau scrie întrebarea ta." },
      { title: "Primește răspunsul", desc: "Pași clari, linkuri oficiale, în limba ta. Fără scris mic." },
    ],
    examples_title: "Poți întreba lucruri precum",
    examples: [
      "Ce am nevoie pentru înregistrarea municipală?",
      "Cum aplic pentru Venitul Minim Vital?",
      "Ce documente sunt necesare pentru cardul de sănătate?",
      "Cum îmi reînnoiesc NIE-ul?",
    ],
    guarantees: [
      { icon: "free", text: "100% gratuit" },
      { icon: "lock", text: "Informațiile tale sunt private" },
      { icon: "no-register", text: "Fără înregistrare sau date personale" },
      { icon: "clock", text: "Disponibil 24/7" },
    ],
    cta_headline: "Ai o întrebare?",
    cta_sub: "Nu mai aștepta. Clara este gata să te ajute.",
    cta_button: "Vorbește cu Clara",
  },
  ca: {
    empathy_headline: "No necessites entendre el sistema",
    empathy_sub: "Només parla. Clara et guia pas a pas, en el teu idioma, amb informació oficial verificada.",
    steps_title: "Així funciona",
    steps: [
      { title: "Obre Clara", desc: "Des del mòbil o l'ordinador. Sense descàrregues, sense registre." },
      { title: "Tria el teu idioma", desc: "Castellà, francès, àrab i més. Clara t'entén." },
      { title: "Parla o escriu", desc: "Prem el micròfon per parlar, o escriu la teva pregunta." },
      { title: "Rep la teva resposta", desc: "Passos clars, enllaços oficials, en el teu idioma. Sense lletra petita." },
    ],
    examples_title: "Pots preguntar-li coses com",
    examples: [
      "Què necessito per a l'empadronament?",
      "Com sol·licito l'Ingrés Mínim Vital?",
      "Quins documents demanen per a la targeta sanitària?",
      "Com renovo el meu NIE?",
    ],
    guarantees: [
      { icon: "free", text: "100% gratuït" },
      { icon: "lock", text: "La teva informació és privada" },
      { icon: "no-register", text: "Sense registre ni dades personals" },
      { icon: "clock", text: "Disponible 24/7" },
    ],
    cta_headline: "Tens un dubte?",
    cta_sub: "No esperis més. Clara està preparada per ajudar-te.",
    cta_button: "Parla amb Clara",
  },
  zh: {
    empathy_headline: "你不需要了解这个系统",
    empathy_sub: "只需开口说话。Clara会用你的语言，一步步引导你，提供经过验证的官方信息。",
    steps_title: "使用方法",
    steps: [
      { title: "打开Clara", desc: "在手机或电脑上。无需下载，无需注册。" },
      { title: "选择你的语言", desc: "西班牙语、法语、阿拉伯语等。Clara能听懂你。" },
      { title: "说话或打字", desc: "按下麦克风说话，或输入你的问题。" },
      { title: "获得回答", desc: "清晰的步骤，官方链接，用你的语言。没有小字条款。" },
    ],
    examples_title: "你可以这样问",
    examples: [
      "市政登记需要什么？",
      "如何申请最低生活保障？",
      "健康卡需要哪些文件？",
      "如何续签NIE？",
    ],
    guarantees: [
      { icon: "free", text: "100%免费" },
      { icon: "lock", text: "你的信息是私密的" },
      { icon: "no-register", text: "无需注册或个人数据" },
      { icon: "clock", text: "全天候24/7" },
    ],
    cta_headline: "有疑问吗？",
    cta_sub: "不要再等了。Clara已经准备好帮助你。",
    cta_button: "和Clara对话",
  },
  ar: {
    empathy_headline: "لا تحتاج لفهم النظام",
    empathy_sub: "فقط تحدث. كلارا ترشدك خطوة بخطوة، بلغتك، بمعلومات رسمية موثقة.",
    steps_title: "كيف يعمل",
    steps: [
      { title: "افتح كلارا", desc: "من هاتفك أو حاسوبك. بدون تحميل، بدون تسجيل." },
      { title: "اختر لغتك", desc: "الإسبانية والفرنسية والعربية والمزيد. كلارا تفهمك." },
      { title: "تحدث أو اكتب", desc: "اضغط على الميكروفون للتحدث، أو اكتب سؤالك." },
      { title: "احصل على إجابتك", desc: "خطوات واضحة، روابط رسمية، بلغتك. بدون شروط خفية." },
    ],
    examples_title: "يمكنك أن تسأل أشياء مثل",
    examples: [
      "ما الذي أحتاجه للتسجيل البلدي؟",
      "كيف أتقدم بطلب للحد الأدنى من الدخل؟",
      "ما المستندات المطلوبة للبطاقة الصحية؟",
      "كيف أجدد NIE الخاص بي؟",
    ],
    guarantees: [
      { icon: "free", text: "مجاني 100%" },
      { icon: "lock", text: "معلوماتك خاصة" },
      { icon: "no-register", text: "بدون تسجيل أو بيانات شخصية" },
      { icon: "clock", text: "متاح 24/7" },
    ],
    cta_headline: "لديك سؤال؟",
    cta_sub: "لا تنتظر أكثر. كلارا جاهزة لمساعدتك.",
    cta_button: "تحدث مع كلارا",
  },
};

/* ══════════════════════════════════════════════════════════════════
   FUTURO PAGE — StoryBrand: user is hero, Clara grows FOR them
   ══════════════════════════════════════════════════════════════════ */
export const FUTURO_PAGE: Record<Language, {
  hero_headline: string;
  hero_sub: string;
  roadmap_title: string;
  roadmap: { title: string; benefit: string; status: string }[];
  vision_headline: string;
  vision_text: string;
  cta_headline: string;
  cta_sub: string;
  cta_button: string;
}> = {
  es: {
    hero_headline: "Esto es solo el comienzo",
    hero_sub: "Clara nacio para que nadie se quede sin informacion por no hablar el idioma o no entender el sistema. Pero todavia hay personas a las que no llegamos. Cada paso que damos es para ti.",
    roadmap_title: "Lo que viene — para ti",
    roadmap: [
      { title: "Mas idiomas", benefit: "Para que nadie quede fuera por su idioma. Rumano, ucraniano, chino y mas — porque cada persona merece entender.", status: "Proximo" },
      { title: "Mas tramites", benefit: "Asilo, homologacion de titulos, reagrupacion familiar. Los tramites que mas te preocupan, explicados con claridad.", status: "En desarrollo" },
      { title: "Alianzas reales", benefit: "Que tu ayuntamiento, tu ONG, tu trabajadora social conozcan a Clara. Para que la ayuda llegue donde hace falta.", status: "Explorando" },
      { title: "App sin conexion", benefit: "Porque no siempre hay wifi. Una app que funcione offline, en tu bolsillo, cuando la necesites.", status: "Futuro" },
    ],
    vision_headline: "El futuro que imaginamos",
    vision_text: "Un dia, cualquier persona que llegue a Espana podra preguntar y recibir una respuesta clara, en su idioma, sin miedo. Ese es el mundo que estamos construyendo. Contigo.",
    cta_headline: "Tu voz construye ese futuro",
    cta_sub: "Cada pregunta que haces nos ayuda a mejorar. Cada idioma que pedis, lo priorizamos. Clara crece contigo.",
    cta_button: "Habla con Clara",
  },
  en: {
    hero_headline: "This is just the beginning",
    hero_sub: "Clara was born so nobody is left without information because they don't speak the language or don't understand the system. But there are still people we can't reach. Every step we take is for you.",
    roadmap_title: "What's coming — for you",
    roadmap: [
      { title: "More languages", benefit: "So no one is left out because of their language. Romanian, Ukrainian, Chinese and more — because everyone deserves to understand.", status: "Next" },
      { title: "More procedures", benefit: "Asylum, diploma recognition, family reunification. The procedures that worry you most, explained clearly.", status: "In development" },
      { title: "Real partnerships", benefit: "So your municipality, your NGO, your social worker knows Clara. So help reaches where it's needed.", status: "Exploring" },
      { title: "Offline app", benefit: "Because there's not always wifi. An app that works offline, in your pocket, when you need it.", status: "Future" },
    ],
    vision_headline: "The future we imagine",
    vision_text: "One day, anyone who arrives in Spain will be able to ask a question and receive a clear answer, in their language, without fear. That's the world we're building. With you.",
    cta_headline: "Your voice builds that future",
    cta_sub: "Every question you ask helps us improve. Every language you request, we prioritize. Clara grows with you.",
    cta_button: "Talk to Clara",
  },
  fr: {
    hero_headline: "Ce n'est que le debut",
    hero_sub: "Clara est nee pour que personne ne reste sans information par barriere linguistique ou bureaucratique. Mais il y a encore des personnes que nous n'atteignons pas. Chaque pas est pour toi.",
    roadmap_title: "Ce qui arrive — pour toi",
    roadmap: [
      { title: "Plus de langues", benefit: "Pour que personne ne soit exclu a cause de sa langue. Roumain, ukrainien, chinois et plus — parce que chacun merite de comprendre.", status: "Prochain" },
      { title: "Plus de demarches", benefit: "Asile, reconnaissance de diplomes, regroupement familial. Les demarches qui te preoccupent le plus, expliquees clairement.", status: "En cours" },
      { title: "Partenariats reels", benefit: "Pour que ta mairie, ton ONG, ton assistant social connaisse Clara. Pour que l'aide arrive la ou il faut.", status: "Exploration" },
      { title: "App hors ligne", benefit: "Parce qu'il n'y a pas toujours de wifi. Une app qui fonctionne hors ligne, dans ta poche, quand tu en as besoin.", status: "Futur" },
    ],
    vision_headline: "Le futur que nous imaginons",
    vision_text: "Un jour, toute personne arrivant en Espagne pourra poser une question et recevoir une reponse claire, dans sa langue, sans peur. C'est le monde que nous construisons. Avec toi.",
    cta_headline: "Ta voix construit ce futur",
    cta_sub: "Chaque question que tu poses nous aide a nous ameliorer. Chaque langue demandee, nous la priorisons. Clara grandit avec toi.",
    cta_button: "Parle avec Clara",
  },
  pt: {
    hero_headline: "Isto e so o inicio",
    hero_sub: "Clara nasceu para que ninguem fique sem informacao por nao falar o idioma ou nao entender o sistema. Mas ainda ha pessoas que nao alcancamos. Cada passo e para ti.",
    roadmap_title: "O que vem — para ti",
    roadmap: [
      { title: "Mais idiomas", benefit: "Para que ninguem fique de fora por causa do idioma. Romeno, ucraniano, chines e mais — porque todos merecem entender.", status: "Proximo" },
      { title: "Mais tramites", benefit: "Asilo, reconhecimento de diplomas, reagrupamento familiar. Os tramites que mais te preocupam, explicados com clareza.", status: "Em desenvolvimento" },
      { title: "Parcerias reais", benefit: "Para que a tua camara, a tua ONG, o teu assistente social conheca Clara. Para que a ajuda chegue onde faz falta.", status: "A explorar" },
      { title: "App offline", benefit: "Porque nem sempre ha wifi. Uma app que funcione offline, no teu bolso, quando precisares.", status: "Futuro" },
    ],
    vision_headline: "O futuro que imaginamos",
    vision_text: "Um dia, qualquer pessoa que chegue a Espanha podera perguntar e receber uma resposta clara, no seu idioma, sem medo. Esse e o mundo que estamos a construir. Contigo.",
    cta_headline: "A tua voz constroi esse futuro",
    cta_sub: "Cada pergunta que fazes ajuda-nos a melhorar. Cada idioma que pedes, priorizamos. Clara cresce contigo.",
    cta_button: "Fala com Clara",
  },
  ro: {
    hero_headline: "Acesta e doar inceputul",
    hero_sub: "Clara s-a nascut pentru ca nimeni sa nu ramana fara informatii din cauza limbii sau a sistemului. Dar inca sunt persoane pe care nu le putem ajunge. Fiecare pas e pentru tine.",
    roadmap_title: "Ce urmeaza — pentru tine",
    roadmap: [
      { title: "Mai multe limbi", benefit: "Ca nimeni sa nu fie exclus din cauza limbii. Romana, ucraineana, chineza si altele — fiindca fiecare merita sa inteleaga.", status: "Urmatorul" },
      { title: "Mai multe proceduri", benefit: "Azil, recunoasterea diplomelor, reunificarea familiei. Procedurile care te preocupa cel mai mult, explicate clar.", status: "In dezvoltare" },
      { title: "Parteneriate reale", benefit: "Ca primaria ta, ONG-ul tau, asistentul tau social sa cunoasca Clara. Ca ajutorul sa ajunga unde e nevoie.", status: "Explorare" },
      { title: "App offline", benefit: "Fiindca nu e intotdeauna wifi. O aplicatie care functioneaza offline, in buzunar, cand ai nevoie.", status: "Viitor" },
    ],
    vision_headline: "Viitorul pe care il imaginam",
    vision_text: "Intr-o zi, oricine ajunge in Spania va putea pune o intrebare si primi un raspuns clar, in limba sa, fara frica. Aceasta e lumea pe care o construim. Cu tine.",
    cta_headline: "Vocea ta construieste acel viitor",
    cta_sub: "Fiecare intrebare pe care o pui ne ajuta sa ne imbunatatim. Fiecare limba ceruta o prioritizam. Clara creste cu tine.",
    cta_button: "Vorbeste cu Clara",
  },
  ca: {
    hero_headline: "Aixo es nomes el principi",
    hero_sub: "Clara va neixer perque ningu es quedi sense informacio per no parlar l'idioma o no entendre el sistema. Pero encara hi ha persones a les quals no arribem. Cada pas es per a tu.",
    roadmap_title: "El que ve — per a tu",
    roadmap: [
      { title: "Mes idiomes", benefit: "Perque ningu quedi fora pel seu idioma. Romanes, ucraines, xines i mes — perque tothom mereix entendre.", status: "Proxim" },
      { title: "Mes tramits", benefit: "Asil, homologacio de titols, reagrupament familiar. Els tramits que mes et preocupen, explicats amb claredat.", status: "En desenvolupament" },
      { title: "Aliances reals", benefit: "Que el teu ajuntament, la teva ONG, la teva treballadora social conegui Clara. Perque l'ajuda arribi on cal.", status: "Explorant" },
      { title: "App sense connexio", benefit: "Perque no sempre hi ha wifi. Una app que funcioni offline, a la teva butxaca, quan la necessitis.", status: "Futur" },
    ],
    vision_headline: "El futur que imaginem",
    vision_text: "Un dia, qualsevol persona que arribi a Espanya podra preguntar i rebre una resposta clara, en el seu idioma, sense por. Aquest es el mon que estem construint. Amb tu.",
    cta_headline: "La teva veu construeix aquest futur",
    cta_sub: "Cada pregunta que fas ens ajuda a millorar. Cada idioma que demanes, el prioritzem. Clara creix amb tu.",
    cta_button: "Parla amb Clara",
  },
  zh: {
    hero_headline: "这仅仅是开始",
    hero_sub: "Clara的诞生是为了让每个人不因语言障碍或不了解系统而缺少信息。但仍有我们触及不到的人。我们走的每一步都是为了你。",
    roadmap_title: "即将到来 — 为了你",
    roadmap: [
      { title: "更多语言", benefit: "让每个人不因语言而被排除在外。罗马尼亚语、乌克兰语、中文等 — 因为每个人都值得理解。", status: "即将推出" },
      { title: "更多手续", benefit: "庇护、学历认证、家庭团聚。最让你担心的手续，清晰地解释给你。", status: "开发中" },
      { title: "真正的合作", benefit: "让你的市政厅、你的NGO、你的社工认识Clara。让帮助到达需要的地方。", status: "探索中" },
      { title: "离线应用", benefit: "因为不总是有wifi。一个离线工作的应用，在你口袋里，在你需要时。", status: "未来" },
    ],
    vision_headline: "我们想象的未来",
    vision_text: "有一天，任何来到西班牙的人都能用自己的语言提问并得到清晰的回答，没有恐惧。这就是我们正在建设的世界。与你一起。",
    cta_headline: "你的声音构建这个未来",
    cta_sub: "你提出的每个问题都帮助我们改进。你请求的每种语言，我们都会优先处理。Clara与你一起成长。",
    cta_button: "与Clara对话",
  },
  ar: {
    hero_headline: "هذه مجرد البداية",
    hero_sub: "ولدت كلارا حتى لا يبقى أحد بدون معلومات بسبب حاجز اللغة أو عدم فهم النظام. لكن لا يزال هناك أشخاص لا نصل إليهم. كل خطوة نخطوها هي من أجلك.",
    roadmap_title: "ما هو قادم — من أجلك",
    roadmap: [
      { title: "المزيد من اللغات", benefit: "حتى لا يُستبعد أحد بسبب لغته. الرومانية والأوكرانية والصينية وغيرها — لأن الجميع يستحق أن يفهم.", status: "قريبا" },
      { title: "المزيد من الإجراءات", benefit: "اللجوء، معادلة الشهادات، لم الشمل العائلي. الإجراءات التي تقلقك أكثر، موضحة بوضوح.", status: "قيد التطوير" },
      { title: "شراكات حقيقية", benefit: "حتى تعرف بلديتك ومنظمتك غير الحكومية وأخصائيتك الاجتماعية كلارا. حتى تصل المساعدة حيث تحتاج.", status: "استكشاف" },
      { title: "تطبيق بدون إنترنت", benefit: "لأنه ليس هناك دائماً واي فاي. تطبيق يعمل بدون اتصال، في جيبك، عندما تحتاجه.", status: "المستقبل" },
    ],
    vision_headline: "المستقبل الذي نتخيله",
    vision_text: "يوماً ما، أي شخص يصل إلى إسبانيا سيتمكن من طرح سؤال والحصول على إجابة واضحة، بلغته، بدون خوف. هذا هو العالم الذي نبنيه. معك.",
    cta_headline: "صوتك يبني هذا المستقبل",
    cta_sub: "كل سؤال تطرحه يساعدنا على التحسن. كل لغة تطلبها نعطيها الأولوية. كلارا تكبر معك.",
    cta_button: "تحدث مع كلارا",
  },
};

export const SUB_PAGE_TITLES: Record<Language, Record<string, string>> = {
  es: {
    "como-usar": "Cómo usar Clara",
    "quienes-somos": "Quiénes somos",
    "futuro": "El futuro de Clara",
    "info-legal": "Info legal",
  },
  en: {
    "como-usar": "How to use Clara",
    "quienes-somos": "About us",
    "futuro": "The future of Clara",
    "info-legal": "Legal info",
  },
  fr: {
    "como-usar": "Comment utiliser Clara",
    "quienes-somos": "Qui sommes-nous",
    "futuro": "L'avenir de Clara",
    "info-legal": "Infos légales",
  },
  pt: {
    "como-usar": "Como usar Clara",
    "quienes-somos": "Quem somos",
    "futuro": "O futuro da Clara",
    "info-legal": "Info legal",
  },
  ro: {
    "como-usar": "Cum folosești Clara",
    "quienes-somos": "Cine suntem",
    "futuro": "Viitorul Clarei",
    "info-legal": "Info legale",
  },
  ca: {
    "como-usar": "Com usar Clara",
    "quienes-somos": "Qui som",
    "futuro": "El futur de Clara",
    "info-legal": "Info legal",
  },
  zh: {
    "como-usar": "如何使用Clara",
    "quienes-somos": "关于我们",
    "futuro": "Clara的未来",
    "info-legal": "法律信息",
  },
  ar: {
    "como-usar": "كيف تستخدم كلارا",
    "quienes-somos": "من نحن",
    "futuro": "مستقبل كلارا",
    "info-legal": "المعلومات القانونية",
  },
};

/* ------------------------------------------------------------------ */
/*  Legal page — EU AI Act Art. 50 + GDPR transparency                */
/* ------------------------------------------------------------------ */

export const LEGAL_PAGE: Record<Language, {
  intro: string;
  last_updated: string;
  sections: {
    icon: string;
    heading: string;
    paragraphs: string[];
  }[];
}> = {
  es: {
    intro: "Clara se compromete con la transparencia. Aqui explicamos como funciona nuestra inteligencia artificial y como protegemos tus datos.",
    last_updated: "Ultima actualizacion: febrero 2026",
    sections: [
      {
        icon: "ai",
        heading: "Clara es inteligencia artificial",
        paragraphs: [
          "Soy un sistema de inteligencia artificial, no una persona. Mis respuestas son generadas automaticamente por modelos de lenguaje.",
          "La informacion que proporciono es orientativa y no sustituye el asesoramiento profesional de abogados, trabajadores sociales u organismos oficiales.",
          "Un equipo humano supervisa mi funcionamiento y actualiza mi base de conocimiento periodicamente.",
        ],
      },
      {
        icon: "data",
        heading: "Que datos procesamos",
        paragraphs: [
          "Procesamos el texto y audio que nos envias unicamente para generar respuestas a tus consultas.",
          "No almacenamos documentos de identidad (DNI, NIE, pasaporte) ni datos bancarios.",
          "Las sesiones de conversacion son temporales y no se vinculan a perfiles permanentes.",
        ],
      },
      {
        icon: "services",
        heading: "Servicios de terceros",
        paragraphs: [
          "Utilizamos Google (Gemini) para procesamiento de lenguaje, ElevenLabs para sintesis de voz, y Meta para la comunicacion por WhatsApp.",
          "Solo compartimos los datos minimos necesarios para que estos servicios funcionen.",
          "Puedes consultar sus politicas de privacidad en sus respectivos sitios web.",
        ],
      },
      {
        icon: "clock",
        heading: "Conservacion de datos",
        paragraphs: [
          "El audio que envias se procesa de forma transitoria y no se almacena permanentemente.",
          "No creamos perfiles permanentes de usuarios ni historiales de conversacion a largo plazo.",
          "No utilizamos cookies de seguimiento ni tecnologias de rastreo publicitario.",
        ],
      },
      {
        icon: "rights",
        heading: "Tus derechos",
        paragraphs: [
          "Puedes dejar de usar Clara en cualquier momento sin necesidad de justificacion.",
          "Tienes derecho a solicitar informacion sobre el tratamiento de tus datos.",
          "Puedes reclamar ante la Agencia Espanola de Proteccion de Datos (AEPD) si consideras que tus derechos han sido vulnerados.",
        ],
      },
      {
        icon: "handshake",
        heading: "Consentimiento",
        paragraphs: [
          "Al usar Clara, aceptas el procesamiento de datos descrito en esta pagina para poder ofrecerte respuestas.",
          "Puedes retirar tu consentimiento en cualquier momento simplemente dejando de usar el servicio.",
        ],
      },
      {
        icon: "shield",
        heading: "Proteccion especial",
        paragraphs: [
          "Clara esta disenada pensando en personas en situacion de vulnerabilidad.",
          "No realizamos perfilado de usuarios ni tomamos decisiones automatizadas con efectos legales.",
          "Nuestro desarrollo sigue los principios de OdiseIA4Good para una IA responsable e inclusiva.",
        ],
      },
    ],
  },
  en: {
    intro: "Clara is committed to transparency. Here we explain how our artificial intelligence works and how we protect your data.",
    last_updated: "Last updated: February 2026",
    sections: [
      {
        icon: "ai",
        heading: "Clara is artificial intelligence",
        paragraphs: [
          "I am an artificial intelligence system, not a person. My responses are automatically generated by language models.",
          "The information I provide is for guidance only and does not replace professional advice from lawyers, social workers, or official bodies.",
          "A human team oversees my operation and periodically updates my knowledge base.",
        ],
      },
      {
        icon: "data",
        heading: "What data we process",
        paragraphs: [
          "We process the text and audio you send us solely to generate responses to your queries.",
          "We do not store identity documents (DNI, NIE, passport) or banking details.",
          "Conversation sessions are temporary and are not linked to permanent profiles.",
        ],
      },
      {
        icon: "services",
        heading: "Third-party services",
        paragraphs: [
          "We use Google (Gemini) for language processing, ElevenLabs for voice synthesis, and Meta for WhatsApp communication.",
          "We only share the minimum data necessary for these services to function.",
          "You can consult their privacy policies on their respective websites.",
        ],
      },
      {
        icon: "clock",
        heading: "Data retention",
        paragraphs: [
          "Audio you send is processed transiently and is not permanently stored.",
          "We do not create permanent user profiles or long-term conversation histories.",
          "We do not use tracking cookies or advertising tracking technologies.",
        ],
      },
      {
        icon: "rights",
        heading: "Your rights",
        paragraphs: [
          "You can stop using Clara at any time without needing to justify it.",
          "You have the right to request information about the processing of your data.",
          "You can file a complaint with the Spanish Data Protection Agency (AEPD) if you believe your rights have been violated.",
        ],
      },
      {
        icon: "handshake",
        heading: "Consent",
        paragraphs: [
          "By using Clara, you accept the data processing described on this page in order to receive responses.",
          "You can withdraw your consent at any time simply by stopping use of the service.",
        ],
      },
      {
        icon: "shield",
        heading: "Special protection",
        paragraphs: [
          "Clara is designed with vulnerable people in mind.",
          "We do not profile users or make automated decisions with legal effects.",
          "Our development follows OdiseIA4Good principles for responsible and inclusive AI.",
        ],
      },
    ],
  },
  fr: {
    intro: "Clara s'engage pour la transparence. Nous expliquons ici comment fonctionne notre intelligence artificielle et comment nous protegeons vos donnees.",
    last_updated: "Derniere mise a jour : fevrier 2026",
    sections: [
      {
        icon: "ai",
        heading: "Clara est une intelligence artificielle",
        paragraphs: [
          "Je suis un systeme d'intelligence artificielle, pas une personne. Mes reponses sont generees automatiquement par des modeles de langage.",
          "Les informations que je fournis sont indicatives et ne remplacent pas les conseils professionnels d'avocats, de travailleurs sociaux ou d'organismes officiels.",
          "Une equipe humaine supervise mon fonctionnement et met a jour ma base de connaissances periodiquement.",
        ],
      },
      {
        icon: "data",
        heading: "Quelles donnees nous traitons",
        paragraphs: [
          "Nous traitons le texte et l'audio que vous nous envoyez uniquement pour generer des reponses a vos questions.",
          "Nous ne stockons pas les documents d'identite (DNI, NIE, passeport) ni les coordonnees bancaires.",
          "Les sessions de conversation sont temporaires et ne sont pas liees a des profils permanents.",
        ],
      },
      {
        icon: "services",
        heading: "Services tiers",
        paragraphs: [
          "Nous utilisons Google (Gemini) pour le traitement du langage, ElevenLabs pour la synthese vocale, et Meta pour la communication WhatsApp.",
          "Nous ne partageons que les donnees minimales necessaires au fonctionnement de ces services.",
          "Vous pouvez consulter leurs politiques de confidentialite sur leurs sites respectifs.",
        ],
      },
      {
        icon: "clock",
        heading: "Conservation des donnees",
        paragraphs: [
          "L'audio que vous envoyez est traite de maniere transitoire et n'est pas stocke de maniere permanente.",
          "Nous ne creons pas de profils d'utilisateurs permanents ni d'historiques de conversation a long terme.",
          "Nous n'utilisons pas de cookies de suivi ni de technologies de tracage publicitaire.",
        ],
      },
      {
        icon: "rights",
        heading: "Vos droits",
        paragraphs: [
          "Vous pouvez cesser d'utiliser Clara a tout moment sans avoir a vous justifier.",
          "Vous avez le droit de demander des informations sur le traitement de vos donnees.",
          "Vous pouvez deposer une plainte aupres de l'Agence espagnole de protection des donnees (AEPD) si vous estimez que vos droits ont ete violes.",
        ],
      },
      {
        icon: "handshake",
        heading: "Consentement",
        paragraphs: [
          "En utilisant Clara, vous acceptez le traitement des donnees decrit sur cette page afin de recevoir des reponses.",
          "Vous pouvez retirer votre consentement a tout moment en cessant simplement d'utiliser le service.",
        ],
      },
      {
        icon: "shield",
        heading: "Protection speciale",
        paragraphs: [
          "Clara est concue en pensant aux personnes en situation de vulnerabilite.",
          "Nous ne profilons pas les utilisateurs et ne prenons pas de decisions automatisees ayant des effets juridiques.",
          "Notre developpement suit les principes d'OdiseIA4Good pour une IA responsable et inclusive.",
        ],
      },
    ],
  },
  pt: {
    intro: "Clara compromete-se com a transparencia. Aqui explicamos como funciona a nossa inteligencia artificial e como protegemos os teus dados.",
    last_updated: "Ultima atualizacao: fevereiro 2026",
    sections: [
      {
        icon: "ai",
        heading: "Clara e inteligencia artificial",
        paragraphs: [
          "Sou um sistema de inteligencia artificial, nao uma pessoa. As minhas respostas sao geradas automaticamente por modelos de linguagem.",
          "A informacao que forneco e orientativa e nao substitui o aconselhamento profissional de advogados, assistentes sociais ou organismos oficiais.",
          "Uma equipa humana supervisiona o meu funcionamento e atualiza a minha base de conhecimento periodicamente.",
        ],
      },
      {
        icon: "data",
        heading: "Que dados processamos",
        paragraphs: [
          "Processamos o texto e audio que nos envias unicamente para gerar respostas as tuas consultas.",
          "Nao armazenamos documentos de identidade (DNI, NIE, passaporte) nem dados bancarios.",
          "As sessoes de conversacao sao temporarias e nao estao vinculadas a perfis permanentes.",
        ],
      },
      {
        icon: "services",
        heading: "Servicos de terceiros",
        paragraphs: [
          "Utilizamos Google (Gemini) para processamento de linguagem, ElevenLabs para sintese de voz, e Meta para comunicacao por WhatsApp.",
          "So partilhamos os dados minimos necessarios para o funcionamento destes servicos.",
          "Podes consultar as suas politicas de privacidade nos respetivos sites.",
        ],
      },
      {
        icon: "clock",
        heading: "Conservacao de dados",
        paragraphs: [
          "O audio que envias e processado de forma transitoria e nao e armazenado permanentemente.",
          "Nao criamos perfis permanentes de utilizadores nem historicos de conversacao a longo prazo.",
          "Nao utilizamos cookies de rastreamento nem tecnologias de rastreio publicitario.",
        ],
      },
      {
        icon: "rights",
        heading: "Os teus direitos",
        paragraphs: [
          "Podes deixar de usar Clara a qualquer momento sem necessidade de justificacao.",
          "Tens o direito de solicitar informacao sobre o tratamento dos teus dados.",
          "Podes reclamar junto da Agencia Espanhola de Protecao de Dados (AEPD) se consideras que os teus direitos foram violados.",
        ],
      },
      {
        icon: "handshake",
        heading: "Consentimento",
        paragraphs: [
          "Ao usar Clara, aceitas o processamento de dados descrito nesta pagina para receber respostas.",
          "Podes retirar o teu consentimento a qualquer momento simplesmente deixando de usar o servico.",
        ],
      },
      {
        icon: "shield",
        heading: "Protecao especial",
        paragraphs: [
          "Clara foi desenhada a pensar em pessoas em situacao de vulnerabilidade.",
          "Nao realizamos perfilagem de utilizadores nem tomamos decisoes automatizadas com efeitos legais.",
          "O nosso desenvolvimento segue os principios da OdiseIA4Good para uma IA responsavel e inclusiva.",
        ],
      },
    ],
  },
  ro: {
    intro: "Clara se angajeaza pentru transparenta. Aici explicam cum functioneaza inteligenta noastra artificiala si cum protejam datele tale.",
    last_updated: "Ultima actualizare: februarie 2026",
    sections: [
      {
        icon: "ai",
        heading: "Clara este inteligenta artificiala",
        paragraphs: [
          "Sunt un sistem de inteligenta artificiala, nu o persoana. Raspunsurile mele sunt generate automat de modele de limbaj.",
          "Informatiile pe care le ofer sunt orientative si nu inlocuiesc consilierea profesionala a avocatilor, asistentilor sociali sau organismelor oficiale.",
          "O echipa umana supravegheaza functionarea mea si actualizeaza periodic baza mea de cunostinte.",
        ],
      },
      {
        icon: "data",
        heading: "Ce date procesam",
        paragraphs: [
          "Procesam textul si audio-ul pe care ni le trimiti exclusiv pentru a genera raspunsuri la intrebarile tale.",
          "Nu stocam documente de identitate (DNI, NIE, pasaport) sau date bancare.",
          "Sesiunile de conversatie sunt temporare si nu sunt legate de profiluri permanente.",
        ],
      },
      {
        icon: "services",
        heading: "Servicii terte",
        paragraphs: [
          "Folosim Google (Gemini) pentru procesarea limbajului, ElevenLabs pentru sinteza vocala si Meta pentru comunicarea WhatsApp.",
          "Partajam doar datele minime necesare functionarii acestor servicii.",
          "Poti consulta politicile lor de confidentialitate pe site-urile respective.",
        ],
      },
      {
        icon: "clock",
        heading: "Pastrarea datelor",
        paragraphs: [
          "Audio-ul pe care il trimiti este procesat tranzitoriu si nu este stocat permanent.",
          "Nu cream profiluri permanente de utilizatori si nici istorice de conversatii pe termen lung.",
          "Nu folosim cookie-uri de urmarire sau tehnologii de urmarire publicitara.",
        ],
      },
      {
        icon: "rights",
        heading: "Drepturile tale",
        paragraphs: [
          "Poti inceta sa folosesti Clara oricand fara a fi nevoie de justificare.",
          "Ai dreptul de a solicita informatii despre prelucrarea datelor tale.",
          "Poti depune o plangere la Agentia Spaniola de Protectie a Datelor (AEPD) daca consideri ca drepturile tale au fost incalcate.",
        ],
      },
      {
        icon: "handshake",
        heading: "Consimtamant",
        paragraphs: [
          "Prin utilizarea Clara, accepti prelucrarea datelor descrisa pe aceasta pagina pentru a primi raspunsuri.",
          "Poti retrage consimtamantul oricand, pur si simplu incetand sa folosesti serviciul.",
        ],
      },
      {
        icon: "shield",
        heading: "Protectie speciala",
        paragraphs: [
          "Clara este conceputa avand in vedere persoanele aflate in situatii vulnerabile.",
          "Nu profilam utilizatorii si nu luam decizii automate cu efecte juridice.",
          "Dezvoltarea noastra urmeaza principiile OdiseIA4Good pentru o IA responsabila si incluziva.",
        ],
      },
    ],
  },
  ca: {
    intro: "Clara es compromet amb la transparencia. Aqui expliquem com funciona la nostra intelligencia artificial i com protegim les teves dades.",
    last_updated: "Ultima actualitzacio: febrer 2026",
    sections: [
      {
        icon: "ai",
        heading: "Clara es intelligencia artificial",
        paragraphs: [
          "Soc un sistema d'intelligencia artificial, no una persona. Les meves respostes son generades automaticament per models de llenguatge.",
          "La informacio que proporciono es orientativa i no substitueix l'assessorament professional d'advocats, treballadors socials o organismes oficials.",
          "Un equip huma supervisa el meu funcionament i actualitza la meva base de coneixement periodicament.",
        ],
      },
      {
        icon: "data",
        heading: "Quines dades processem",
        paragraphs: [
          "Processem el text i l'audio que ens envies unicament per generar respostes a les teves consultes.",
          "No emmagatzemem documents d'identitat (DNI, NIE, passaport) ni dades bancaries.",
          "Les sessions de conversacio son temporals i no estan vinculades a perfils permanents.",
        ],
      },
      {
        icon: "services",
        heading: "Serveis de tercers",
        paragraphs: [
          "Utilitzem Google (Gemini) per al processament del llenguatge, ElevenLabs per a la sintesi de veu, i Meta per a la comunicacio per WhatsApp.",
          "Nomes compartim les dades minimes necessaries perque aquests serveis funcionin.",
          "Pots consultar les seves politiques de privacitat als seus respectius llocs web.",
        ],
      },
      {
        icon: "clock",
        heading: "Conservacio de dades",
        paragraphs: [
          "L'audio que envies es processa de manera transitoria i no s'emmagatzema permanentment.",
          "No creem perfils permanents d'usuaris ni historials de conversacio a llarg termini.",
          "No utilitzem galetes de seguiment ni tecnologies de rastrejament publicitari.",
        ],
      },
      {
        icon: "rights",
        heading: "Els teus drets",
        paragraphs: [
          "Pots deixar d'utilitzar Clara en qualsevol moment sense necessitat de justificacio.",
          "Tens dret a sollicitar informacio sobre el tractament de les teves dades.",
          "Pots reclamar davant l'Agencia Espanyola de Proteccio de Dades (AEPD) si consideres que els teus drets han estat vulnerats.",
        ],
      },
      {
        icon: "handshake",
        heading: "Consentiment",
        paragraphs: [
          "En utilitzar Clara, acceptes el processament de dades descrit en aquesta pagina per poder rebre respostes.",
          "Pots retirar el teu consentiment en qualsevol moment simplement deixant d'utilitzar el servei.",
        ],
      },
      {
        icon: "shield",
        heading: "Proteccio especial",
        paragraphs: [
          "Clara esta dissenyada pensant en persones en situacio de vulnerabilitat.",
          "No realitzem perfilatge d'usuaris ni prenem decisions automatitzades amb efectes legals.",
          "El nostre desenvolupament segueix els principis d'OdiseIA4Good per a una IA responsable i inclusiva.",
        ],
      },
    ],
  },
  zh: {
    intro: "Clara致力于透明度。在这里我们解释我们的人工智能如何工作以及我们如何保护您的数据。",
    last_updated: "最后更新：2026年2月",
    sections: [
      {
        icon: "ai",
        heading: "Clara是人工智能",
        paragraphs: [
          "我是一个人工智能系统，不是真人。我的回答由语言模型自动生成。",
          "我提供的信息仅供参考，不能替代律师、社工或官方机构的专业建议。",
          "一个人工团队监督我的运行并定期更新我的知识库。",
        ],
      },
      {
        icon: "data",
        heading: "我们处理哪些数据",
        paragraphs: [
          "我们处理您发送的文字和音频，仅用于生成对您咨询的回答。",
          "我们不存储身份证件（DNI、NIE、护照）或银行信息。",
          "对话会话是临时的，不会与永久个人资料关联。",
        ],
      },
      {
        icon: "services",
        heading: "第三方服务",
        paragraphs: [
          "我们使用Google（Gemini）进行语言处理，ElevenLabs进行语音合成，Meta用于WhatsApp通信。",
          "我们只共享这些服务运行所需的最少数据。",
          "您可以在各自的网站上查阅它们的隐私政策。",
        ],
      },
      {
        icon: "clock",
        heading: "数据保留",
        paragraphs: [
          "您发送的音频会被临时处理，不会被永久存储。",
          "我们不创建永久用户档案或长期对话记录。",
          "我们不使用跟踪cookie或广告跟踪技术。",
        ],
      },
      {
        icon: "rights",
        heading: "您的权利",
        paragraphs: [
          "您可以随时停止使用Clara，无需任何理由。",
          "您有权要求了解您的数据处理情况。",
          "如果您认为您的权利受到侵犯，可以向西班牙数据保护局（AEPD）投诉。",
        ],
      },
      {
        icon: "handshake",
        heading: "同意",
        paragraphs: [
          "使用Clara即表示您接受本页所述的数据处理以获得回答。",
          "您可以随时通过停止使用服务来撤回同意。",
        ],
      },
      {
        icon: "shield",
        heading: "特殊保护",
        paragraphs: [
          "Clara的设计考虑到了弱势群体的需求。",
          "我们不进行用户画像，也不做出具有法律效力的自动化决定。",
          "我们的开发遵循OdiseIA4Good的负责任和包容性AI原则。",
        ],
      },
    ],
  },
  ar: {
    intro: "تلتزم كلارا بالشفافية. نشرح هنا كيف يعمل ذكاؤنا الاصطناعي وكيف نحمي بياناتك.",
    last_updated: "آخر تحديث: فبراير 2026",
    sections: [
      {
        icon: "ai",
        heading: "كلارا ذكاء اصطناعي",
        paragraphs: [
          "أنا نظام ذكاء اصطناعي، لست شخصاً حقيقياً. إجاباتي يتم إنشاؤها تلقائياً بواسطة نماذج لغوية.",
          "المعلومات التي أقدمها إرشادية ولا تحل محل الاستشارة المهنية من المحامين أو الأخصائيين الاجتماعيين أو الجهات الرسمية.",
          "فريق بشري يشرف على عملي ويحدث قاعدة معارفي بشكل دوري.",
        ],
      },
      {
        icon: "data",
        heading: "ما هي البيانات التي نعالجها",
        paragraphs: [
          "نعالج النص والصوت الذي ترسله فقط لإنشاء ردود على استفساراتك.",
          "لا نخزن وثائق الهوية (DNI، NIE، جواز السفر) أو البيانات المصرفية.",
          "جلسات المحادثة مؤقتة ولا ترتبط بملفات تعريف دائمة.",
        ],
      },
      {
        icon: "services",
        heading: "خدمات الطرف الثالث",
        paragraphs: [
          "نستخدم Google (Gemini) لمعالجة اللغة، وElevenLabs لتوليد الصوت، وMeta للتواصل عبر WhatsApp.",
          "نشارك فقط الحد الأدنى من البيانات اللازمة لعمل هذه الخدمات.",
          "يمكنك الاطلاع على سياسات الخصوصية الخاصة بهم على مواقعهم.",
        ],
      },
      {
        icon: "clock",
        heading: "الاحتفاظ بالبيانات",
        paragraphs: [
          "الصوت الذي ترسله يُعالج بشكل مؤقت ولا يُخزن بشكل دائم.",
          "لا ننشئ ملفات تعريف دائمة للمستخدمين أو سجلات محادثات طويلة الأمد.",
          "لا نستخدم ملفات تعريف الارتباط للتتبع أو تقنيات التتبع الإعلاني.",
        ],
      },
      {
        icon: "rights",
        heading: "حقوقك",
        paragraphs: [
          "يمكنك التوقف عن استخدام كلارا في أي وقت دون الحاجة إلى تبرير.",
          "لديك الحق في طلب معلومات حول معالجة بياناتك.",
          "يمكنك تقديم شكوى لدى وكالة حماية البيانات الإسبانية (AEPD) إذا كنت تعتقد أن حقوقك قد انتُهكت.",
        ],
      },
      {
        icon: "handshake",
        heading: "الموافقة",
        paragraphs: [
          "باستخدام كلارا، فإنك توافق على معالجة البيانات الموصوفة في هذه الصفحة لتلقي الردود.",
          "يمكنك سحب موافقتك في أي وقت ببساطة عن طريق التوقف عن استخدام الخدمة.",
        ],
      },
      {
        icon: "shield",
        heading: "حماية خاصة",
        paragraphs: [
          "تم تصميم كلارا مع مراعاة الأشخاص في أوضاع هشة.",
          "لا نقوم بتصنيف المستخدمين ولا نتخذ قرارات آلية ذات آثار قانونية.",
          "يتبع تطويرنا مبادئ OdiseIA4Good من أجل ذكاء اصطناعي مسؤول وشامل.",
        ],
      },
    ],
  },
};
