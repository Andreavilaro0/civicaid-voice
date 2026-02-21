"use client";

import { useState } from "react";

interface LanguageSelectorProps {
  defaultLang?: "es" | "fr" | "ar";
  onChange?: (lang: "es" | "fr" | "ar") => void;
}

const languages = [
  { code: "es" as const, label: "Espanol", short: "ES" },
  { code: "fr" as const, label: "Francais", short: "FR" },
  { code: "ar" as const, label: "\u0639\u0631\u0628\u064A", short: "AR" },
];

export default function LanguageSelector({
  defaultLang = "es",
  onChange,
}: LanguageSelectorProps) {
  const [selected, setSelected] = useState(defaultLang);

  function handleSelect(code: "es" | "fr" | "ar") {
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
