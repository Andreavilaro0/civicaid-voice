"use client";

import { useState } from "react";
import type { Language } from "@/lib/types";

interface LanguageSelectorProps {
  defaultLang?: Language;
  onChange?: (lang: Language) => void;
}

const languages: { code: Language; label: string; short: string }[] = [
  { code: "es", label: "Espanol", short: "ES" },
  { code: "en", label: "English", short: "EN" },
  { code: "fr", label: "Francais", short: "FR" },
  { code: "pt", label: "Portugues", short: "PT" },
  { code: "ro", label: "Romana", short: "RO" },
  { code: "ca", label: "Catala", short: "CA" },
  { code: "zh", label: "中文", short: "中文" },
  { code: "ar", label: "عربي", short: "AR" },
];

export default function LanguageSelector({
  defaultLang = "es",
  onChange,
}: LanguageSelectorProps) {
  const [selected, setSelected] = useState(defaultLang);

  function handleSelect(code: Language) {
    setSelected(code);
    onChange?.(code);
  }

  return (
    <div role="radiogroup" aria-label="Seleccionar idioma" className="flex gap-2 flex-wrap">
      {languages.map((lang) => (
        <button
          key={lang.code}
          role="radio"
          aria-checked={selected === lang.code}
          onClick={() => handleSelect(lang.code)}
          className={`
            flex items-center gap-1.5 px-3 py-2
            min-h-touch-sm rounded-full font-body text-[14px] font-medium
            border-2 transition-colors duration-150
            ${selected === lang.code
              ? "border-clara-blue bg-clara-blue text-white"
              : "border-clara-border bg-white text-clara-text-secondary hover:border-clara-blue hover:text-clara-blue"
            }
          `}
        >
          <span>{lang.short}</span>
        </button>
      ))}
    </div>
  );
}
