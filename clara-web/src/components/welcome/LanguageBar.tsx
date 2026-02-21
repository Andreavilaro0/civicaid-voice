"use client";

type Lang = "es" | "fr" | "ar";

const languages: { code: Lang; label: string; short: string }[] = [
  { code: "es", label: "Espanol", short: "ES" },
  { code: "fr", label: "Francais", short: "FR" },
  { code: "ar", label: "\u0639\u0631\u0628\u064A", short: "AR" },
];

interface LanguageBarProps {
  lang: Lang;
  onChangeLang: (lang: Lang) => void;
}

export default function LanguageBar({ lang, onChangeLang }: LanguageBarProps) {
  return (
    <div
      role="radiogroup"
      aria-label="Seleccionar idioma"
      className="flex items-center gap-2"
    >
      {languages.map((l) => (
        <button
          key={l.code}
          role="radio"
          aria-checked={lang === l.code}
          onClick={() => onChangeLang(l.code)}
          className={`
            px-4 py-2 min-h-touch-sm rounded-xl text-body-sm font-medium
            border-2 transition-colors duration-150
            focus-visible:outline focus-visible:outline-[3px]
            focus-visible:outline-clara-blue focus-visible:outline-offset-2
            ${
              lang === l.code
                ? "bg-clara-blue text-white border-clara-blue"
                : "bg-white dark:bg-[#1a1f26] text-clara-text-secondary border-clara-border dark:border-[#2a2f36] hover:border-clara-blue/40"
            }
          `}
        >
          {l.short}
        </button>
      ))}
    </div>
  );
}
