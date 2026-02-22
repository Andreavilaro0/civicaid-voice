import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

const LANG_OPTIONS: { value: Language; label: string }[] = [
  { value: "es", label: "ES" },
  { value: "en", label: "EN" },
  { value: "fr", label: "FR" },
  { value: "pt", label: "PT" },
  { value: "ro", label: "RO" },
  { value: "ca", label: "CA" },
  { value: "zh", label: "中文" },
  { value: "ar", label: "AR" },
];

const ariaLabels: Record<Language, { back: string; lang: string }> = {
  es: { back: "Volver al inicio", lang: "Idioma" },
  en: { back: "Back to home", lang: "Language" },
  fr: { back: "Retour a l'accueil", lang: "Langue" },
  pt: { back: "Voltar ao inicio", lang: "Idioma" },
  ro: { back: "Inapoi la pagina principala", lang: "Limba" },
  ca: { back: "Tornar a l'inici", lang: "Idioma" },
  zh: { back: "返回首页", lang: "语言" },
  ar: { back: "العودة إلى الرئيسية", lang: "اللغة" },
};

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const navigate = useNavigate();
  const labels = ariaLabels[language];

  return (
    <header className="sticky top-0 z-10 bg-white/80 dark:bg-[#0f1419]/80 backdrop-blur-lg border-b border-clara-border/50 dark:border-[#2a2f36]/50">
      <div className="flex items-center justify-between px-4 h-[64px]">
        {/* Back button */}
        <button
          onClick={() => navigate("/")}
          aria-label={labels.back}
          className="min-w-[48px] min-h-[48px] flex items-center justify-center rounded-full
                     text-clara-text hover:bg-clara-card dark:hover:bg-[#1a1f26] transition-colors duration-150"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M19 12H5" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
        </button>

        {/* Clara identity — avatar + name + status */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-clara-blue to-[#2980B9]
                            flex items-center justify-center shadow-sm">
              <svg width="22" height="22" viewBox="0 0 80 80" fill="none" aria-hidden="true">
                <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="white" strokeWidth="4.5"
                      strokeLinecap="round" fill="none" opacity="0.65" />
                <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="white" strokeWidth="4.5"
                      strokeLinecap="round" fill="none" opacity="1" />
                <circle cx="28" cy="40" r="5" fill="#D46A1E" />
              </svg>
            </div>
            {/* Online indicator */}
            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-clara-green
                            rounded-full border-2 border-white dark:border-[#0f1419]" />
          </div>
          <div>
            <h1 className="font-display font-bold text-[17px] text-clara-text dark:text-[#e8e8ee] leading-tight">Clara</h1>
            <p className="text-[13px] text-clara-green font-medium leading-tight">Online</p>
          </div>
        </div>

        {/* Language selector */}
        <select
          value={language}
          onChange={(e) => onLanguageChange(e.target.value as Language)}
          aria-label={labels.lang}
          className="bg-clara-card dark:bg-[#1a1f26] text-clara-text dark:text-[#e8e8ee] border border-clara-border dark:border-[#2a2f36] rounded-full
                     px-3 py-1.5 text-[14px] font-medium min-h-[48px]
                     focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2
                     appearance-none cursor-pointer transition-colors duration-150"
          style={{ backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='%234A4A5A'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E\")", backgroundRepeat: "no-repeat", backgroundPosition: "right 8px center", paddingRight: "28px" }}
        >
          {LANG_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </header>
  );
}
