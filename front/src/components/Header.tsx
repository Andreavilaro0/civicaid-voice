import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

const ariaLabels: Record<Language, { back: string; lang: string }> = {
  es: { back: "Volver al inicio", lang: "Idioma" },
  en: { back: "Back to home", lang: "Language" },
  fr: { back: "Retour à l'accueil", lang: "Langue" },
  pt: { back: "Voltar ao início", lang: "Idioma" },
  ro: { back: "Înapoi la pagina principală", lang: "Limba" },
  ca: { back: "Tornar a l'inici", lang: "Idioma" },
  zh: { back: "返回首页", lang: "语言" },
  ar: { back: "العودة إلى الرئيسية", lang: "اللغة" },
};

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const navigate = useNavigate();
  const labels = ariaLabels[language];

  return (
    <header
      className="
        sticky top-0 z-10
        flex items-center justify-between
        px-4 h-[56px]
        bg-white/80 dark:bg-[#0f1419]/80
        backdrop-blur-lg
        border-b border-clara-border/50 dark:border-[#2a2f36]/50
      "
    >
      {/* LEFT — Back button */}
      <button
        onClick={() => navigate("/")}
        aria-label={labels.back}
        className="
          flex items-center justify-center
          w-9 h-9 rounded-lg
          text-clara-text
          hover:bg-clara-card
          transition-colors duration-150
        "
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="currentColor"
          aria-hidden="true"
        >
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
        </svg>
      </button>

      {/* CENTER — Clara avatar + name */}
      <div className="flex items-center gap-2">
        {/* Avatar: 32x32 circle with voice arc SVG + orange dot + green online indicator */}
        <div className="relative w-8 h-8 flex-shrink-0">
          <div
            className="
              w-8 h-8 rounded-full
              bg-clara-blue
              flex items-center justify-center
              overflow-hidden
            "
          >
            <svg
              width="28"
              height="28"
              viewBox="0 0 80 80"
              fill="none"
              aria-hidden="true"
            >
              {/* Outer arc */}
              <path
                d="M 28 14 A 30 30 0 0 1 28 66"
                stroke="white"
                strokeWidth="4.5"
                strokeLinecap="round"
                fill="none"
                opacity="0.35"
              />
              {/* Middle arc */}
              <path
                d="M 28 23 A 20 20 0 0 1 28 57"
                stroke="white"
                strokeWidth="4.5"
                strokeLinecap="round"
                fill="none"
                opacity="0.65"
              />
              {/* Inner arc */}
              <path
                d="M 28 32 A 10 10 0 0 1 28 48"
                stroke="white"
                strokeWidth="4.5"
                strokeLinecap="round"
                fill="none"
                opacity="1"
              />
              {/* Orange dot */}
              <circle cx="28" cy="40" r="5.5" fill="#D46A1E" />
            </svg>
          </div>

          {/* Green online indicator */}
          <span
            aria-hidden="true"
            className="
              absolute bottom-0 right-0
              w-2.5 h-2.5 rounded-full
              bg-clara-green
              ring-2 ring-white dark:ring-[#0f1419]
            "
          />
        </div>

        <h1 className="font-display font-bold text-[18px] leading-none text-clara-text">
          Clara
        </h1>
      </div>

      {/* RIGHT — Language selector pill */}
      <select
        value={language}
        onChange={(e) => onLanguageChange(e.target.value as Language)}
        aria-label={labels.lang}
        className="
          bg-clara-card
          border border-clara-border
          rounded-full
          px-3 py-1.5
          text-[14px] font-medium
          text-clara-text
          cursor-pointer
          focus:outline-none
          focus:ring-2 focus:ring-clara-blue focus:ring-offset-1
          transition-colors duration-150
        "
      >
        <option value="es">ES</option>
        <option value="en">EN</option>
        <option value="fr">FR</option>
        <option value="pt">PT</option>
        <option value="ro">RO</option>
        <option value="ca">CA</option>
        <option value="zh">中文</option>
        <option value="ar">AR</option>
      </select>
    </header>
  );
}
