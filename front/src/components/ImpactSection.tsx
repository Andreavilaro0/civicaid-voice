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
    },
    after: {
      es: "¿Tienes pasaporte y contrato? Entonces puedes empadronarte.",
      fr: "Vous avez un passeport et un contrat ? Alors vous pouvez vous inscrire.",
      ar: "هل لديك جواز سفر وعقد؟ إذن يمكنك التسجيل.",
    },
  },
  {
    before: {
      es: "Llamar al 010, esperar 40 min, no entender",
      fr: "Appeler le 010, attendre 40 min, ne pas comprendre",
      ar: "الاتصال بـ 010، الانتظار 40 دقيقة، عدم الفهم",
    },
    after: {
      es: "Un audio de 30 segundos en tu idioma, a cualquier hora",
      fr: "Un audio de 30 secondes dans votre langue, à toute heure",
      ar: "رسالة صوتية من 30 ثانية بلغتك، في أي وقت",
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
};

const beforeLabel: Record<Language, string> = {
  es: "Antes",
  fr: "Avant",
  ar: "قبل",
};

const afterLabel: Record<Language, string> = {
  es: "Con Clara",
  fr: "Avec Clara",
  ar: "مع كلارا",
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
