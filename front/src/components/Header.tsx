import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { ThemeToggleCompact } from "@/components/ui/ThemeToggle";
import LanguageBar from "@/components/welcome/LanguageBar";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

const ariaLabels: Record<Language, { back: string }> = {
  es: { back: "Volver al inicio" },
  en: { back: "Back to home" },
  fr: { back: "Retour a l'accueil" },
  pt: { back: "Voltar ao inicio" },
  ro: { back: "Inapoi la pagina principala" },
  ca: { back: "Tornar a l'inici" },
  zh: { back: "返回首页" },
  ar: { back: "العودة إلى الرئيسية" },
};

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const navigate = useNavigate();
  const labels = ariaLabels[language];

  return (
    <header className="sticky top-0 z-10 bg-clara-bg/80 backdrop-blur-lg border-b border-clara-border/50">
      <div className="flex items-center justify-between px-3 h-[56px]">
        {/* Back button */}
        <button
          onClick={() => navigate("/")}
          aria-label={labels.back}
          className="min-w-[48px] min-h-[48px] flex items-center justify-center rounded-full
                     text-clara-text hover:bg-clara-card transition-colors duration-150 flex-shrink-0"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M19 12H5" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
        </button>

        {/* Clara identity — avatar + name + status */}
        <div className="flex items-center gap-3 flex-shrink-0">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-clara-blue to-[#2980B9]
                            flex items-center justify-center shadow-sm">
              <svg width="22" height="22" viewBox="0 0 80 80" fill="none" aria-hidden="true">
                <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="white" strokeWidth="4.5"
                      strokeLinecap="round" fill="none" opacity="0.65" />
                <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="white" strokeWidth="4.5"
                      strokeLinecap="round" fill="none" opacity="1" />
                <circle cx="28" cy="40" r="5" style={{ fill: "var(--color-clara-orange)" }} />
              </svg>
            </div>
            {/* Online indicator */}
            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-clara-green
                            rounded-full border-2 border-clara-bg" />
          </div>
          <div>
            <h1 className="font-display font-bold text-[17px] text-clara-text leading-tight">Clara</h1>
            <p className="text-[13px] text-clara-green font-medium leading-tight">Online</p>
          </div>
        </div>

        {/* Theme toggle + Language bar */}
        <div className="flex items-center gap-1 flex-shrink-0">
          <ThemeToggleCompact />
          <LanguageBar lang={language} onChangeLang={onLanguageChange} compact />
        </div>
      </div>
    </header>
  );
}
