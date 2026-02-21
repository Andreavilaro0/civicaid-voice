"use client";

import { useRouter } from "next/navigation";
import type { Language } from "@/lib/types";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

const ariaLabels: Record<Language, { back: string; lang: string }> = {
  es: { back: "Volver al inicio", lang: "Idioma" },
  fr: { back: "Retour a l'accueil", lang: "Langue" },
  ar: { back: "العودة إلى الرئيسية", lang: "اللغة" },
};

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const router = useRouter();
  const labels = ariaLabels[language];

  return (
    <header className="sticky top-0 z-10 flex items-center justify-between px-4 h-[56px] bg-clara-blue text-white">
      {/* Boton atras */}
      <button
        onClick={() => router.push("/")}
        aria-label={labels.back}
        className="min-w-touch-sm min-h-touch-sm flex items-center justify-center rounded-lg
                   hover:bg-white/10 transition-colors duration-150"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="currentColor"
          aria-hidden="true"
        >
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
        </svg>
      </button>

      {/* Titulo con icono */}
      <div className="flex items-center gap-2">
        <svg width="28" height="28" viewBox="0 0 80 80" fill="none" aria-hidden="true">
          <path d="M 28 14 A 30 30 0 0 1 28 66" stroke="white" strokeWidth="4.5"
                strokeLinecap="round" fill="none" opacity="0.35" />
          <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="white" strokeWidth="4.5"
                strokeLinecap="round" fill="none" opacity="0.65" />
          <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="white" strokeWidth="4.5"
                strokeLinecap="round" fill="none" opacity="1" />
          <circle cx="28" cy="40" r="5.5" fill="#D46A1E" />
        </svg>
        <h1 className="font-display font-bold text-[20px]">Clara</h1>
      </div>

      {/* Selector de idioma */}
      <select
        value={language}
        onChange={(e) => onLanguageChange(e.target.value as Language)}
        aria-label={labels.lang}
        className="bg-white/20 text-white border border-white/30 rounded-lg
                   px-2 py-1 text-label font-medium min-h-touch-sm
                   focus:outline focus:outline-[3px] focus:outline-white focus:outline-offset-2"
      >
        <option value="es" className="text-clara-text">
          ES
        </option>
        <option value="fr" className="text-clara-text">
          FR
        </option>
        <option value="ar" className="text-clara-text">
          AR
        </option>
      </select>
    </header>
  );
}
