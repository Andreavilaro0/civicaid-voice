"use client";

/**
 * ImpactSection — narrative component that communicates Clara's social impact.
 *
 * Renders three sections:
 *   1. Impact counter  — "4.5M" stat with localised description
 *   2. Personas strip  — three illustrated user portraits with name + quote
 *   3. Before / After  — side-by-side comparison of the pre-Clara vs post-Clara
 *                        experience for two key bureaucratic pain-points
 *
 * Usage:
 *   import ImpactSection from "@/components/ImpactSection";
 *   <ImpactSection language="es" />
 *
 * Requires SvgDefs to be rendered somewhere in the tree so that the persona
 * SVG <use> references (#persona-maria, etc.) resolve correctly.
 */

import type { Language } from "@/lib/types";

interface ImpactSectionProps {
  language: Language;
}

/* ------------------------------------------------------------------ */
/*  Persona data                                                       */
/* ------------------------------------------------------------------ */

interface PersonaData {
  svgId: string;
  name: string;
  origin: string;
  quote: Record<Language, string>;
  /** Tailwind border-left colour class — must be a complete utility class */
  accent: string;
}

const personas: PersonaData[] = [
  {
    svgId: "persona-maria",
    name: "María, 58",
    origin: "Marruecos",
    quote: {
      es: "Solo quiero saber si tengo derecho a ver un médico.",
      en: "I just want to know if I have the right to see a doctor.",
      fr: "Je veux juste savoir si j'ai droit à un médecin.",
      pt: "Só quero saber se tenho direito a ver um médico.",
      ro: "Vreau doar să știu dacă am dreptul să văd un medic.",
      ca: "Només vull saber si tinc dret a veure un metge.",
      zh: "我只想知道我是否有权看医生。",
      ar: "أريد فقط أن أعرف هل لي الحق في رؤية طبيب.",
    },
    accent: "border-l-[#D46A1E]",
  },
  {
    svgId: "persona-ahmed",
    name: "Ahmed, 34",
    origin: "Senegal",
    quote: {
      es: "Necesito algo que funcione de noche.",
      en: "I need something that works at night.",
      fr: "J'ai besoin de quelque chose qui marche la nuit.",
      pt: "Preciso de algo que funcione à noite.",
      ro: "Am nevoie de ceva care funcționează noaptea.",
      ca: "Necessito alguna cosa que funcioni de nit.",
      zh: "我需要一个晚上也能用的东西。",
      ar: "أحتاج شيئاً يعمل في الليل.",
    },
    accent: "border-l-clara-blue",
  },
  {
    svgId: "persona-fatima",
    name: "Fátima, 42",
    origin: "Marruecos",
    quote: {
      es: "No quiero molestar, pero mis hijos necesitan un médico.",
      en: "I don't want to bother anyone, but my children need a doctor.",
      fr: "Je ne veux pas déranger, mais mes enfants ont besoin d'un médecin.",
      pt: "Não quero incomodar, mas os meus filhos precisam de um médico.",
      ro: "Nu vreau să deranjez, dar copiii mei au nevoie de un medic.",
      ca: "No vull molestar, però els meus fills necessiten un metge.",
      zh: "我不想打扰别人，但我的孩子们需要看医生。",
      ar: "لا أريد الإزعاج، لكن أطفالي يحتاجون طبيباً.",
    },
    accent: "border-l-clara-green",
  },
];

/* ------------------------------------------------------------------ */
/*  Before / After data                                                */
/* ------------------------------------------------------------------ */

interface BeforeAfterRow {
  before: Record<Language, string>;
  after: Record<Language, string>;
}

const beforeAfter: BeforeAfterRow[] = [
  {
    before: {
      es: "Un formulario de 4 páginas en español jurídico",
      en: "A 4-page form in legal Spanish",
      fr: "Un formulaire de 4 pages en espagnol juridique",
      pt: "Um formulário de 4 páginas em espanhol jurídico",
      ro: "Un formular de 4 pagini în spaniolă juridică",
      ca: "Un formulari de 4 pàgines en castellà jurídic",
      zh: "4页法律西班牙语表格",
      ar: "استمارة من 4 صفحات بالإسبانية القانونية",
    },
    after: {
      es: "¿Tienes pasaporte y contrato? Entonces puedes empadronarte.",
      en: "Do you have a passport and a contract? Then you can register.",
      fr: "Vous avez un passeport et un contrat ? Alors vous pouvez vous inscrire.",
      pt: "Tens passaporte e contrato? Então podes registar-te.",
      ro: "Ai pașaport și contract? Atunci te poți înregistra.",
      ca: "Tens passaport i contracte? Doncs pots empadronar-te.",
      zh: "你有护照和合同吗？那你可以注册。",
      ar: "هل لديك جواز سفر وعقد؟ إذن يمكنك التسجيل.",
    },
  },
  {
    before: {
      es: "Llamar al 010, esperar 40 min, no entender",
      en: "Call 010, wait 40 min, don't understand",
      fr: "Appeler le 010, attendre 40 min, ne pas comprendre",
      pt: "Ligar para o 010, esperar 40 min, não entender",
      ro: "Sună la 010, așteaptă 40 min, nu înțelege",
      ca: "Trucar al 010, esperar 40 min, no entendre",
      zh: "拨打010，等40分钟，听不懂",
      ar: "الاتصال بـ 010، الانتظار 40 دقيقة، عدم الفهم",
    },
    after: {
      es: "Un audio de 30 segundos en tu idioma, a cualquier hora",
      en: "A 30-second audio in your language, anytime",
      fr: "Un audio de 30 secondes dans votre langue, à toute heure",
      pt: "Um áudio de 30 segundos no teu idioma, a qualquer hora",
      ro: "Un audio de 30 secunde în limba ta, oricând",
      ca: "Un àudio de 30 segons en el teu idioma, a qualsevol hora",
      zh: "一段30秒的音频，用你的语言，随时可用",
      ar: "رسالة صوتية من 30 ثانية بلغتك، في أي وقت",
    },
  },
];

/* ------------------------------------------------------------------ */
/*  Localised strings                                                  */
/* ------------------------------------------------------------------ */

const impactText: Record<Language, string> = {
  es: "personas vulnerables en España no acceden a ayudas por barreras de idioma y burocracia",
  en: "vulnerable people in Spain don't access benefits due to language barriers and bureaucracy",
  fr: "personnes vulnérables en Espagne n'accèdent pas aux aides à cause de barrières linguistiques",
  pt: "pessoas vulneráveis em Espanha não acedem a ajudas por barreiras de idioma e burocracia",
  ro: "persoane vulnerabile din Spania nu accesează ajutoarele din cauza barierelor lingvistice și birocratice",
  ca: "persones vulnerables a Espanya no accedeixen a ajudes per barreres d'idioma i burocràcia",
  zh: "西班牙的弱势群体因语言障碍和官僚主义无法获得援助",
  ar: "شخص ضعيف في إسبانيا لا يحصلون على المساعدات بسبب حواجز اللغة والبيروقراطية",
};

const beforeLabel: Record<Language, string> = {
  es: "Antes",
  en: "Before",
  fr: "Avant",
  pt: "Antes",
  ro: "Înainte",
  ca: "Abans",
  zh: "之前",
  ar: "قبل",
};

const afterLabel: Record<Language, string> = {
  es: "Con Clara",
  en: "With Clara",
  fr: "Avec Clara",
  pt: "Com Clara",
  ro: "Cu Clara",
  ca: "Amb Clara",
  zh: "有了Clara",
  ar: "مع كلارا",
};

/* ------------------------------------------------------------------ */
/*  Aria labels                                                        */
/* ------------------------------------------------------------------ */

const userStoriesLabel: Record<Language, string> = {
  es: "Historias de usuarios",
  en: "User stories",
  fr: "Histoires d'utilisateurs",
  pt: "Histórias de utilizadores",
  ro: "Povești ale utilizatorilor",
  ca: "Històries d'usuaris",
  zh: "用户故事",
  ar: "قصص المستخدمين",
};

const comparisonLabel: Record<Language, string> = {
  es: "Antes y después de Clara",
  en: "Before and after Clara",
  fr: "Avant et après Clara",
  pt: "Antes e depois da Clara",
  ro: "Înainte și după Clara",
  ca: "Abans i després de Clara",
  zh: "Clara之前和之后",
  ar: "قبل وبعد كلارا",
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function ImpactSection({ language }: ImpactSectionProps) {
  return (
    <div
      className="w-full max-w-[380px] mx-auto px-4 py-6 space-y-6"
      style={{
        animation: "fadeInUp 0.6s ease-out both",
        animationDelay: "0.4s",
      }}
    >
      {/* ── Impact counter ── */}
      <div className="text-center">
        <span className="impact-counter" aria-label="4.5 millones">
          4.5M
        </span>
        <p className="text-body-sm text-clara-text-secondary mt-1 max-w-[300px] mx-auto">
          {impactText[language]}
        </p>
      </div>

      {/* ── Personas strip ── */}
      <div
        className="flex flex-col gap-3"
        role="list"
        aria-label={userStoriesLabel[language]}
      >
        {personas.map((p) => (
          <div
            key={p.svgId}
            role="listitem"
            className={`persona-chip ${p.accent} border-l-4`}
          >
            <svg
              width="48"
              height="48"
              className="flex-shrink-0 rounded-full"
              aria-hidden="true"
            >
              <use href={`#${p.svgId}`} />
            </svg>
            <div className="min-w-0">
              <p className="font-display font-bold text-[16px] text-clara-text">
                {p.name}{" "}
                <span className="font-normal text-clara-text-secondary">
                  — {p.origin}
                </span>
              </p>
              <p className="text-[16px] text-clara-text-secondary italic leading-snug mt-0.5">
                &ldquo;{p.quote[language]}&rdquo;
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* ── Before / After comparison ── */}
      <div className="space-y-2" role="table" aria-label={comparisonLabel[language]}>
        {/* Header row */}
        <div className="before-after-grid" role="row">
          <p
            className="text-[13px] font-semibold uppercase tracking-wider text-[#D46A1E]"
            role="columnheader"
          >
            {beforeLabel[language]}
          </p>
          <p
            className="text-[13px] font-semibold uppercase tracking-wider text-[#2E7D4F]"
            role="columnheader"
          >
            {afterLabel[language]}
          </p>
        </div>

        {/* Data rows */}
        {beforeAfter.map((row, i) => (
          <div key={i} className="before-after-grid" role="row">
            <div className="before-cell" role="cell">
              {row.before[language]}
            </div>
            <div className="after-cell" role="cell">
              {row.after[language]}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
