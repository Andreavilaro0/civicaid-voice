import type { Language } from "@/lib/types";

const languages: { code: Language; label: string; short: string }[] = [
  { code: "es", label: "Español", short: "ES" },
  { code: "en", label: "English", short: "EN" },
  { code: "fr", label: "Français", short: "FR" },
  { code: "pt", label: "Português", short: "PT" },
  { code: "ro", label: "Română", short: "RO" },
  { code: "ca", label: "Català", short: "CA" },
  { code: "zh", label: "中文", short: "中文" },
  { code: "ar", label: "عربي", short: "AR" },
];

interface LanguageBarProps {
  lang: Language;
  onChangeLang: (lang: Language) => void;
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
