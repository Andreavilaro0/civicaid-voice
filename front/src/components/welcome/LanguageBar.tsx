import { useRef, useEffect } from "react";
import type { Language } from "@/lib/types";

const languages: { code: Language; label: string; short: string; flag: string }[] = [
  { code: "es", label: "Español", short: "ES", flag: "🇪🇸" },
  { code: "en", label: "English", short: "EN", flag: "🇬🇧" },
  { code: "fr", label: "Français", short: "FR", flag: "🇫🇷" },
  { code: "pt", label: "Português", short: "PT", flag: "🇵🇹" },
  { code: "ro", label: "Română", short: "RO", flag: "🇷🇴" },
  { code: "ca", label: "Català", short: "CA", flag: "🏴" },
  { code: "zh", label: "中文", short: "中文", flag: "🇨🇳" },
  { code: "ar", label: "عربي", short: "AR", flag: "🇸🇦" },
];

interface LanguageBarProps {
  lang: Language;
  onChangeLang: (lang: Language) => void;
  /** Compact mode for navbar — shows only flag + code */
  compact?: boolean;
}

export default function LanguageBar({ lang, onChangeLang, compact = false }: LanguageBarProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const activeRef = useRef<HTMLButtonElement>(null);

  // Auto-scroll to active language button on mount and when language changes
  useEffect(() => {
    if (activeRef.current && scrollRef.current) {
      const container = scrollRef.current;
      const button = activeRef.current;
      const scrollLeft = button.offsetLeft - container.offsetWidth / 2 + button.offsetWidth / 2;
      container.scrollTo({ left: scrollLeft, behavior: "smooth" });
    }
  }, [lang]);

  return (
    <div
      ref={scrollRef}
      role="radiogroup"
      aria-label="Seleccionar idioma"
      className="lang-bar-scroll flex items-center gap-1.5 overflow-x-auto max-w-full"
    >
      {languages.map((l) => {
        const isActive = lang === l.code;
        return (
          <button
            key={l.code}
            ref={isActive ? activeRef : undefined}
            role="radio"
            aria-checked={isActive}
            aria-label={l.label}
            onClick={() => onChangeLang(l.code)}
            className={`
              lang-pill relative flex items-center gap-1.5 whitespace-nowrap flex-shrink-0
              rounded-full font-medium transition-all duration-200 select-none
              focus-visible:outline focus-visible:outline-[3px]
              focus-visible:outline-clara-blue focus-visible:outline-offset-2
              ${compact
                ? "px-2.5 py-1.5 text-[13px]"
                : "px-3.5 py-2 text-[14px] min-h-touch-sm"
              }
              ${isActive
                ? "bg-clara-blue text-white shadow-md shadow-clara-blue/25 lang-pill-active"
                : "bg-clara-card/80 text-clara-text-secondary border border-clara-border/50 hover:border-clara-blue/40 hover:bg-clara-card"
              }
            `}
          >
            <span className="text-[15px] leading-none" aria-hidden="true">{l.flag}</span>
            <span>{l.short}</span>
          </button>
        );
      })}
    </div>
  );
}
