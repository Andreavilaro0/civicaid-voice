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
      fr: "Je veux juste savoir si j'ai droit à un médecin.",
      ar: "أريد فقط أن أعرف هل لي الحق في رؤية طبيب.",
      en: "I just want to know if I have the right to see a doctor.",
      pt: "Só quero saber se tenho direito a ver um médico.",
      ro: "Vreau doar să știu dacă am dreptul să văd un medic.",
      ca: "Només vull saber si tinc dret a veure un metge.",
      zh: "我只想知道我是否有权去看医生。",
    },
    accent: "border-l-[#D46A1E]",
  },
  {
    svgId: "persona-ahmed",
    name: "Ahmed, 34",
    origin: "Senegal",
    quote: {
      es: "Necesito algo que funcione de noche.",
      fr: "J'ai besoin de quelque chose qui marche la nuit.",
      ar: "أحتاج شيئاً يعمل في الليل.",
      en: "I've been waiting 3 months and nobody explains anything.",
      pt: "Espero há 3 meses e ninguém me explica nada.",
      ro: "Aștept de 3 luni și nimeni nu-mi explică nimic.",
      ca: "Porto 3 mesos esperant i ningú m'explica res.",
      zh: "我已经等了3个月，没有人给我解释任何事情。",
    },
    accent: "border-l-clara-blue",
  },
  {
    svgId: "persona-fatima",
    name: "Fátima, 42",
    origin: "Marruecos",
    quote: {
      es: "No quiero molestar, pero mis hijos necesitan un médico.",
      fr: "Je ne veux pas déranger, mais mes enfants ont besoin d'un médecin.",
      ar: "لا أريد الإزعاج، لكن أطفالي يحتاجون طبيباً.",
      en: "I can't read the forms, they're in legal Spanish.",
      pt: "Não consigo ler os formulários, estão em espanhol jurídico.",
      ro: "Nu pot citi formularele, sunt în spaniolă juridică.",
      ca: "No puc llegir els formularis, estan en espanyol jurídic.",
      zh: "我看不懂那些表格，都是法律西班牙语写的。",
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
      fr: "Un formulaire de 4 pages en espagnol juridique",
      ar: "استمارة من 4 صفحات بالإسبانية القانونية",
      en: "A 4-page form in legal Spanish",
      pt: "Um formulário de 4 páginas em espanhol jurídico",
      ro: "Un formular de 4 pagini în spaniolă juridică",
      ca: "Un formulari de 4 pàgines en espanyol jurídic",
      zh: "一份4页的法律西班牙语表格",
    },
    after: {
      es: "¿Tienes pasaporte y contrato? Entonces puedes empadronarte.",
      fr: "Vous avez un passeport et un contrat ? Alors vous pouvez vous inscrire.",
      ar: "هل لديك جواز سفر وعقد؟ إذن يمكنك التسجيل.",
      en: "Do you have a passport and a contract? Then you can register.",
      pt: "Tens passaporte e contrato? Então podes registar-te.",
      ro: "Ai pașaport și contract? Atunci te poți înregistra.",
      ca: "Tens passaport i contracte? Doncs pots empadronar-te.",
      zh: "你有护照和合同吗？那你就可以登记了。",
    },
  },
  {
    before: {
      es: "Llamar al 010, esperar 40 min, no entender",
      fr: "Appeler le 010, attendre 40 min, ne pas comprendre",
      ar: "الاتصال بـ 010، الانتظار 40 دقيقة، عدم الفهم",
      en: "Call 010, wait 40 min, not understand",
      pt: "Ligar para o 010, esperar 40 min, não entender",
      ro: "Sună la 010, așteaptă 40 min, nu înțelege",
      ca: "Trucar al 010, esperar 40 min, no entendre",
      zh: "拨打010，等待40分钟，听不懂",
    },
    after: {
      es: "Un audio de 30 segundos en tu idioma, a cualquier hora",
      fr: "Un audio de 30 secondes dans votre langue, à toute heure",
      ar: "رسالة صوتية من 30 ثانية بلغتك، في أي وقت",
      en: "A 30-second audio in your language, at any time",
      pt: "Um áudio de 30 segundos no teu idioma, a qualquer hora",
      ro: "Un audio de 30 de secunde în limba ta, la orice oră",
      ca: "Un àudio de 30 segons en el teu idioma, a qualsevol hora",
      zh: "一段30秒的母语音频，随时可用",
    },
  },
];

/* ------------------------------------------------------------------ */
/*  Localised strings                                                  */
/* ------------------------------------------------------------------ */

const impactText: Record<Language, string> = {
  es: "personas vulnerables en España no acceden a ayudas por barreras de idioma y burocracia",
  fr: "personnes vulnérables en Espagne n'accèdent pas aux aides à cause de barrières linguistiques",
  ar: "شخص ضعيف في إسبانيا لا يحصلون على المساعدات بسبب حواجز اللغة والبيروقراطية",
  en: "vulnerable people in Spain cannot access aid due to language and bureaucracy barriers",
  pt: "pessoas vulneráveis em Espanha não acedem a ajudas por barreiras de idioma e burocracia",
  ro: "persoane vulnerabile din Spania nu accesează ajutoarele din cauza barierelor lingvistice și birocratice",
  ca: "persones vulnerables a Espanya no accedeixen a ajudes per barreres d'idioma i burocràcia",
  zh: "在西班牙的弱势群体因语言和官僚障碍无法获得援助",
};

const beforeLabel: Record<Language, string> = {
  es: "Antes",
  fr: "Avant",
  ar: "قبل",
  en: "Before",
  pt: "Antes",
  ro: "Înainte",
  ca: "Abans",
  zh: "之前",
};

const afterLabel: Record<Language, string> = {
  es: "Con Clara",
  fr: "Avec Clara",
  ar: "مع كلارا",
  en: "With Clara",
  pt: "Com a Clara",
  ro: "Cu Clara",
  ca: "Amb la Clara",
  zh: "有了Clara",
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
        aria-label={
          language === "ar"
            ? "قصص المستخدمين"
            : language === "fr"
            ? "Histoires d'utilisateurs"
            : "Historias de usuarios"
        }
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
      <div className="space-y-2" role="table" aria-label={
        language === "ar"
        ? "قبل وبعد كلارا"
        : language === "fr"
        ? "Avant et après Clara"
        : "Antes y después de Clara"
      }>
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
