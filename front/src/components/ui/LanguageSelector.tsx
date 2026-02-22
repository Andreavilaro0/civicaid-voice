"use client";

import { useState } from "react";
import type { Language } from "@/lib/types";

interface LanguageSelectorProps {
  defaultLang?: Language;
  onChange?: (lang: Language) => void;
}

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
    <div role="radiogroup" aria-label="Seleccionar idioma" className="flex gap-3">
      {languages.map((lang) => (
        <button
          key={lang.code}
          role="radio"
          aria-checked={selected === lang.code}
          onClick={() => handleSelect(lang.code)}
          className={`
            flex items-center gap-2 px-4 py-3
            min-h-touch-sm rounded-xl font-body text-body-sm font-medium
            border-2 transition-colors duration-150
            ${selected === lang.code
              ? "border-clara-blue bg-clara-info text-clara-blue"
              : "border-clara-border bg-white text-clara-text-secondary"
            }
          `}
        >
          <span aria-hidden="true">{lang.short}</span>
          <span>{lang.label}</span>
        </button>
      ))}
    </div>
  );
}
