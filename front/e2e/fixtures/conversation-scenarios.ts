/**
 * Realistic conversation scenarios for long-conversation E2E tests.
 *
 * Each scenario simulates a real user journey with Clara,
 * including correct factual information for accuracy checks.
 */

export interface MockTurn {
  /** User message to send */
  userMessage: string;
  /** Clara's mocked response */
  claraResponse: string;
  /** Source type from backend */
  source: "cache" | "llm" | "fallback";
  /** Simulated backend latency in ms */
  delayMs: number;
  /** Keywords that MUST appear in the response (accuracy check) */
  mustContain?: string[];
  /** Keywords that MUST NOT appear (misinformation check) */
  mustNotContain?: string[];
}

export interface ConversationScenario {
  name: string;
  language: string;
  turns: MockTurn[];
}

/* ──────────────────────────────────────────────────────────────── */
/*  Spanish: IMV deep-dive (10 turns)                               */
/* ──────────────────────────────────────────────────────────────── */

export const imvDeepDiveES: ConversationScenario = {
  name: "IMV deep-dive (ES)",
  language: "es",
  turns: [
    {
      userMessage: "¿Qué es el IMV?",
      claraResponse:
        "El Ingreso Minimo Vital (IMV) es una prestacion de la Seguridad Social que garantiza un nivel minimo de ingresos a quienes carecen de recursos economicos suficientes. Lo gestiona el INSS (Instituto Nacional de la Seguridad Social).\n\nPuedes solicitarlo si cumples los requisitos de edad, residencia y renta.",
      source: "llm",
      delayMs: 800,
      mustContain: ["Ingreso Minimo Vital", "Seguridad Social", "INSS"],
      mustNotContain: ["RMI", "comunidad autonoma"],
    },
    {
      userMessage: "¿Quién puede pedirlo?",
      claraResponse:
        "Para pedir el IMV necesitas:\n\n1. Tener entre 23 y 65 anos (o ser mayor de 18 con hijos a cargo)\n2. Residir en Espana de forma legal al menos 1 ano\n3. Estar en situacion de vulnerabilidad economica\n4. Estar inscrito como demandante de empleo\n\nSi eres victima de violencia de genero o trata, no se exige el periodo de residencia.",
      source: "llm",
      delayMs: 1200,
      mustContain: ["23", "65", "Residir", "demandante de empleo"],
      mustNotContain: ["10 anos de residencia"],
    },
    {
      userMessage: "¿Cuánto dinero dan?",
      claraResponse:
        "La cuantia del IMV en 2025 para un adulto solo es de aproximadamente 604 euros al mes. Esta cantidad aumenta segun el numero de personas en la unidad de convivencia:\n\n- 1 adulto: ~604 EUR/mes\n- 1 adulto + 1 menor: ~785 EUR/mes\n- 2 adultos + 1 menor: ~907 EUR/mes\n\nEstas cifras se actualizan cada ano con el IPC.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["604", "euros"],
      mustNotContain: ["1000 euros", "2000"],
    },
    {
      userMessage: "¿Dónde lo solicito?",
      claraResponse:
        "Puedes solicitar el IMV de varias formas:\n\n1. Online: A traves de la Sede Electronica de la Seguridad Social (sede.seg-social.gob.es)\n2. Presencial: En las oficinas del INSS con cita previa\n3. Por correo: Enviando el formulario a la direccion del INSS\n\nTe recomiendo la via online si tienes certificado digital o Cl@ve. Es la mas rapida.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Sede Electronica", "INSS", "cita previa"],
    },
    {
      userMessage: "¿Qué documentos necesito?",
      claraResponse:
        "Los documentos principales son:\n\n1. DNI/NIE de todos los miembros de la unidad de convivencia\n2. Certificado de empadronamiento colectivo\n3. Libro de familia o certificado de nacimiento\n4. Declaracion de la renta (IRPF) o certificado de no obligacion\n5. Certificado de demandante de empleo\n6. Numero de cuenta bancaria (IBAN)\n\nSi no tienes alguno, los servicios sociales de tu ayuntamiento pueden ayudarte.",
      source: "llm",
      delayMs: 1100,
      mustContain: ["DNI", "NIE", "empadronamiento", "IBAN"],
    },
    {
      userMessage: "No tengo certificado digital, ¿puedo hacerlo igual?",
      claraResponse:
        "Si, por supuesto. Sin certificado digital puedes:\n\n1. Pedir cita previa en el INSS llamando al 901 16 65 65 o al 91 541 25 30\n2. Ir a una oficina del INSS presencialmente\n3. Pedir ayuda en los servicios sociales de tu ayuntamiento, ellos pueden tramitarlo contigo\n\nTambien puedes obtener Cl@ve por videollamada desde tu movil, que te vale para muchos tramites online.",
      source: "llm",
      delayMs: 800,
      mustContain: ["cita previa", "servicios sociales"],
    },
    {
      userMessage: "¿Cuánto tarda en resolverse?",
      claraResponse:
        "El plazo legal para resolver la solicitud del IMV es de 6 meses desde que la presentas. En la practica:\n\n- Si esta todo correcto: 2-4 meses\n- Si faltan documentos: puede alargarse mas\n\nSi no recibes respuesta en 6 meses, se entiende como denegada por silencio administrativo, pero puedes reclamar.",
      source: "llm",
      delayMs: 700,
      mustContain: ["6 meses"],
    },
    {
      userMessage: "¿Es compatible con trabajar?",
      claraResponse:
        "Si! Desde la reforma de 2023, el IMV es compatible con el trabajo. Si empiezas a trabajar:\n\n- Durante el primer ano, no pierdes el IMV automaticamente\n- Se aplica una reduccion gradual: no te descuentan todo lo que ganas\n- El objetivo es que siempre te compense trabajar\n\nEsto se llama 'incentivo al empleo' y es una mejora importante respecto a antes.",
      source: "llm",
      delayMs: 900,
      mustContain: ["compatible", "trabajo"],
    },
    {
      userMessage: "Si me lo deniegan, ¿qué hago?",
      claraResponse:
        "Si te deniegan el IMV, tienes opciones:\n\n1. Reclamacion previa: Tienes 30 dias para presentar reclamacion ante el INSS\n2. Demanda judicial: Si la reclamacion falla, puedes ir al Juzgado de lo Social (es gratuito)\n3. Nueva solicitud: Si tu situacion cambia, puedes pedir de nuevo en cualquier momento\n\nLos servicios sociales o una asociacion como Cruz Roja o Caritas pueden asesorarte gratis.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["30 dias", "reclamacion", "Juzgado"],
    },
    {
      userMessage: "Muchas gracias Clara, me has ayudado mucho",
      claraResponse:
        "De nada! Me alegra haberte ayudado. Recuerda que estoy aqui siempre que lo necesites. Si tienes mas dudas sobre el IMV o cualquier otro tramite, no dudes en escribirme.\n\nMucho animo con tu solicitud!",
      source: "llm",
      delayMs: 500,
      mustContain: [],
    },
  ],
};

/* ──────────────────────────────────────────────────────────────── */
/*  French: Empadronamiento (8 turns)                               */
/* ──────────────────────────────────────────────────────────────── */

export const empadronamientoFR: ConversationScenario = {
  name: "Empadronamiento (FR)",
  language: "fr",
  turns: [
    {
      userMessage: "Qu'est-ce que l'empadronamiento?",
      claraResponse:
        "L'empadronamiento est l'inscription au registre municipal (padron) de ta commune en Espagne. C'est obligatoire pour toute personne residant dans une commune.\n\nC'est la premiere demarche a faire quand tu arrives en Espagne car elle ouvre la porte a beaucoup d'autres droits.",
      source: "llm",
      delayMs: 900,
      mustContain: ["registre municipal", "padron", "obligatoire"],
    },
    {
      userMessage: "Pourquoi c'est important?",
      claraResponse:
        "L'empadronamiento est essentiel car il te permet:\n\n1. D'obtenir la carte sanitaire (acces aux soins gratuits)\n2. D'inscrire tes enfants a l'ecole\n3. De demander des aides sociales (IMV, etc.)\n4. De prouver ta residence en Espagne\n5. De voter aux elections municipales (citoyens UE)\n\nSans empadronamiento, tu ne peux presque rien faire administrativement.",
      source: "llm",
      delayMs: 800,
      mustContain: ["carte sanitaire", "ecole", "aides sociales"],
    },
    {
      userMessage: "Comment je fais pour m'inscrire?",
      claraResponse:
        "Pour t'empadronner, tu dois aller a ta mairie (Ayuntamiento) avec:\n\n1. Ton passeport ou carte d'identite\n2. Un document prouvant ton adresse: contrat de location, facture, ou declaration du proprietaire\n3. Si tu n'as pas de contrat: une declaration responsable du proprietaire\n\nDemande un rendez-vous (cita previa) sur le site de ta mairie. C'est gratuit et rapide.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["mairie", "passeport", "contrat"],
    },
    {
      userMessage: "Je n'ai pas de contrat de location, comment faire?",
      claraResponse:
        "Pas de souci, il y a des alternatives:\n\n1. Le proprietaire peut faire une 'declaracion responsable' (declaration attestant que tu vis chez lui)\n2. Tu peux presenter une facture a ton nom (eau, electricite, telephone)\n3. Dans certaines mairies, un voisin inscrit peut te parrainer\n\nVa aux services sociaux de ta mairie, ils connaissent les regles exactes de ta commune car chaque mairie a ses propres criteres.",
      source: "llm",
      delayMs: 900,
      mustContain: ["declaracion responsable", "facture", "services sociaux"],
    },
    {
      userMessage: "Combien de temps ca prend?",
      claraResponse:
        "L'empadronamiento est generalement immediat:\n\n- Si tu as tous les documents: tu repars avec le certificat le jour meme\n- Le rendez-vous dure 15-20 minutes\n\nCertaines grandes villes (Madrid, Barcelone) peuvent avoir des delais de 1-2 semaines pour obtenir un rendez-vous, mais la procedure elle-meme est rapide.",
      source: "llm",
      delayMs: 700,
      mustContain: ["immediat", "certificat"],
    },
    {
      userMessage: "Ca coute combien?",
      claraResponse:
        "L'empadronamiento est totalement gratuit. La mairie ne peut te demander aucun paiement pour cette demarche.\n\nLe certificat d'empadronamiento (volante de empadronamiento) est aussi gratuit la premiere fois. Certaines mairies facturent 1-3 EUR pour les copies supplementaires, mais la premiere est toujours gratuite.",
      source: "llm",
      delayMs: 600,
      mustContain: ["gratuit"],
      mustNotContain: ["50 euros", "100"],
    },
    {
      userMessage: "Et si je demenage?",
      claraResponse:
        "Si tu demenages dans la meme commune, tu dois faire un 'cambio de domicilio' (changement d'adresse) a la mairie. C'est la meme procedure.\n\nSi tu demenages dans une autre commune, tu dois t'empadronner dans la nouvelle mairie. L'ancienne inscription sera automatiquement annulee.\n\nFais-le dans les premiers jours apres ton demenagement.",
      source: "llm",
      delayMs: 800,
      mustContain: ["cambio de domicilio", "nouvelle mairie"],
    },
    {
      userMessage: "Merci beaucoup Clara!",
      claraResponse:
        "De rien! C'est un plaisir de t'aider. L'empadronamiento est vraiment la premiere etape pour s'installer en Espagne, alors bravo de t'en occuper.\n\nSi tu as d'autres questions sur les demarches, je suis la!",
      source: "llm",
      delayMs: 500,
      mustContain: [],
    },
  ],
};

/* ──────────────────────────────────────────────────────────────── */
/*  English: Health card + mixed topics (8 turns)                   */
/* ──────────────────────────────────────────────────────────────── */

export const healthCardEN: ConversationScenario = {
  name: "Health card + mixed (EN)",
  language: "en",
  turns: [
    {
      userMessage: "How do I get a health card in Spain?",
      claraResponse:
        "To get a health card (tarjeta sanitaria) in Spain, you need to:\n\n1. Be registered in the municipal census (empadronamiento)\n2. Go to your local health center (centro de salud)\n3. Bring your passport/NIE, empadronamiento certificate, and Social Security number (if you have one)\n\nThe card gives you access to free public healthcare (medico de cabecera, urgencias, specialists).",
      source: "llm",
      delayMs: 1000,
      mustContain: ["tarjeta sanitaria", "empadronamiento", "centro de salud"],
    },
    {
      userMessage: "What if I don't have a Social Security number?",
      claraResponse:
        "No problem! You can still get healthcare access. Since 2023, the 'prestacion sanitaria' covers everyone registered in the padron, regardless of immigration status.\n\nGo to your centro de salud with your empadronamiento and passport. They will assign you a doctor. The process has been simplified specifically to ensure nobody is left without healthcare.",
      source: "llm",
      delayMs: 800,
      mustContain: ["padron", "centro de salud"],
    },
    {
      userMessage: "Is it really free?",
      claraResponse:
        "Yes, public healthcare in Spain is free at the point of use for registered residents. This includes:\n\n- Primary care (medico de cabecera)\n- Emergency services (urgencias)\n- Specialist referrals\n- Hospital stays\n- Mental health services\n\nPrescription medicines have a co-payment (small percentage), but people with low income may pay 0% or a reduced amount.",
      source: "llm",
      delayMs: 900,
      mustContain: ["free", "Primary care", "Emergency"],
      mustNotContain: ["insurance required", "private only"],
    },
    {
      userMessage: "How long does it take to get the card?",
      claraResponse:
        "The temporary card (tarjeta provisional) is usually issued on the spot or within a few days. The permanent plastic card arrives by mail in 2-4 weeks.\n\nThe important thing is that you can start using healthcare services as soon as they assign you a doctor, even before the physical card arrives.",
      source: "llm",
      delayMs: 700,
      mustContain: ["provisional"],
    },
    {
      userMessage: "Can my children also get it?",
      claraResponse:
        "Absolutely! All children living in Spain are entitled to healthcare, regardless of their parents' legal status. You need:\n\n1. Child's passport or birth certificate\n2. Family's empadronamiento\n3. Go to the centro de salud\n\nChildren automatically get assigned a pediatrician (pediatra). Vaccinations and check-ups are completely free.",
      source: "llm",
      delayMs: 800,
      mustContain: ["children", "pediatr"],
    },
    {
      userMessage: "Now I want to ask about something different. What is the NIE?",
      claraResponse:
        "The NIE (Numero de Identidad de Extranjero) is a unique identification number for foreigners in Spain. You need it for almost everything:\n\n- Opening a bank account\n- Signing a work contract\n- Renting an apartment\n- Tax declarations\n\nYou can get it at the Policia Nacional office (Oficina de Extranjeria) with an appointment.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["Numero de Identidad de Extranjero", "Policia Nacional"],
    },
    {
      userMessage: "How do I get an appointment for the NIE?",
      claraResponse:
        "To get an appointment for the NIE:\n\n1. Go to sede.administracionespublicas.gob.es\n2. Select your province\n3. Choose 'Policia - Certificados y asignacion de NIE'\n4. Pick a date and time\n\nAppointments can be hard to find in big cities. Try checking early in the morning (8-9 AM) when new slots are released. Some people use alert services to get notified of availability.",
      source: "llm",
      delayMs: 900,
      mustContain: ["sede", "province"],
    },
    {
      userMessage: "Thank you so much Clara, you've been incredibly helpful!",
      claraResponse:
        "You're very welcome! I'm glad I could help. Remember, I'm here whenever you need assistance with any administrative process in Spain.\n\nGood luck with your health card and NIE! You've got this!",
      source: "llm",
      delayMs: 500,
      mustContain: [],
    },
  ],
};

/* ──────────────────────────────────────────────────────────────── */
/*  Arabic: Short conversation to test RTL + language (4 turns)     */
/* ──────────────────────────────────────────────────────────────── */

export const rtlArabic: ConversationScenario = {
  name: "RTL Arabic conversation",
  language: "ar",
  turns: [
    {
      userMessage: "ما هو الحد الأدنى للدخل؟",
      claraResponse:
        "الحد الأدنى للدخل (IMV) هو إعانة من الضمان الاجتماعي تضمن حداً أدنى من الدخل للأشخاص الذين لا يملكون موارد اقتصادية كافية.\n\nيمكنك التقديم إذا كنت تعيش في إسبانيا بشكل قانوني لمدة سنة واحدة على الأقل.",
      source: "llm",
      delayMs: 900,
      mustContain: ["الضمان الاجتماعي", "إسبانيا"],
    },
    {
      userMessage: "كيف أسجل في البلدية؟",
      claraResponse:
        "للتسجيل في البلدية (empadronamiento)، اذهب إلى مقر البلدية (Ayuntamiento) مع:\n\n1. جواز سفرك أو بطاقة هويتك\n2. عقد إيجار أو فاتورة باسمك\n3. أو تصريح من صاحب المنزل\n\nالتسجيل مجاني وسريع. احجز موعداً مسبقاً (cita previa) عبر موقع البلدية.",
      source: "llm",
      delayMs: 800,
      mustContain: ["البلدية", "جواز سفر"],
    },
    {
      userMessage: "هل يمكنني الحصول على رعاية صحية؟",
      claraResponse:
        "نعم! يمكنك الحصول على البطاقة الصحية (tarjeta sanitaria) مجاناً. تحتاج إلى:\n\n1. أن تكون مسجلاً في البلدية\n2. اذهب إلى المركز الصحي (centro de salud) القريب منك\n3. أحضر جواز سفرك وشهادة التسجيل\n\nالرعاية الصحية العامة مجانية في إسبانيا لجميع المقيمين المسجلين.",
      source: "llm",
      delayMs: 800,
      mustContain: ["البطاقة الصحية", "مجان"],
    },
    {
      userMessage: "شكراً جزيلاً كلارا!",
      claraResponse:
        "عفواً! سعيدة بمساعدتك. أنا هنا دائماً إذا احتجت أي مساعدة في الإجراءات الإدارية في إسبانيا.\n\nبالتوفيق!",
      source: "llm",
      delayMs: 400,
      mustContain: [],
    },
  ],
};

/* ──────────────────────────────────────────────────────────────── */
/*  Chinese: Registration (4 turns)                                 */
/* ──────────────────────────────────────────────────────────────── */

export const registrationZH: ConversationScenario = {
  name: "Registration (ZH)",
  language: "zh",
  turns: [
    {
      userMessage: "什么是居民登记？",
      claraResponse:
        "居民登记（empadronamiento）是在西班牙市政厅（Ayuntamiento）的户籍登记。这是住在西班牙的每个人都必须做的。\n\n这是你到达西班牙后的第一件事，因为它是获得其他权利的基础。",
      source: "llm",
      delayMs: 800,
      mustContain: ["居民登记", "市政厅"],
    },
    {
      userMessage: "需要什么文件？",
      claraResponse:
        "你需要准备：\n\n1. 护照或身份证\n2. 住址证明：租赁合同、水电费单据，或房东声明\n3. 填写申请表（在市政厅领取）\n\n建议先在市政厅网站预约（cita previa），这样不用排队等候。",
      source: "llm",
      delayMs: 700,
      mustContain: ["护照", "租赁合同"],
    },
    {
      userMessage: "登记后能享受什么服务？",
      claraResponse:
        "登记后你可以：\n\n1. 申请医疗卡（tarjeta sanitaria）享受免费医疗\n2. 孩子可以入学\n3. 申请社会援助（如最低生活保障IMV）\n4. 证明你在西班牙的居住\n5. 欧盟公民可参加市政选举\n\n几乎所有行政手续都需要居民登记证明。",
      source: "llm",
      delayMs: 900,
      mustContain: ["医疗卡", "入学"],
    },
    {
      userMessage: "谢谢Clara！",
      claraResponse:
        "不客气！很高兴能帮到你。如果你还有其他关于西班牙行政手续的问题，随时来问我。\n\n祝你一切顺利！",
      source: "llm",
      delayMs: 400,
      mustContain: [],
    },
  ],
};

/* ──────────────────────────────────────────────────────────────── */
/*  Stress test: Rapid 15-turn conversation (ES)                    */
/* ──────────────────────────────────────────────────────────────── */

export const stressTestES: ConversationScenario = {
  name: "Stress test 15 turns (ES)",
  language: "es",
  turns: Array.from({ length: 15 }, (_, i) => ({
    userMessage: `Pregunta numero ${i + 1}: ¿Puedes explicarme mas sobre los tramites sociales?`,
    claraResponse: `Respuesta ${i + 1}: Los tramites sociales en Espana incluyen el empadronamiento, la tarjeta sanitaria, el IMV, el NIE y muchos mas. Cada uno tiene sus propios requisitos y plazos. ¿Sobre cual te gustaria saber mas?`,
    source: "llm" as const,
    delayMs: 300 + Math.floor(Math.random() * 500),
    mustContain: [`Respuesta ${i + 1}`],
  })),
};

/* ──────────────────────────────────────────────────────────────── */
/*  Export all scenarios                                             */
/* ──────────────────────────────────────────────────────────────── */

export const ALL_SCENARIOS: ConversationScenario[] = [
  imvDeepDiveES,
  empadronamientoFR,
  healthCardEN,
  rtlArabic,
  registrationZH,
  stressTestES,
];
