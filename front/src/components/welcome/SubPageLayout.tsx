import { useSearchParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import type { Language } from "@/lib/types";
import { SUB_PAGE_TITLES } from "@/lib/i18n";
import LanguageBar from "./LanguageBar";

interface SubPageLayoutProps {
  slug: string;
  children: (lang: Language) => React.ReactNode;
}

export default function SubPageLayout({ slug, children }: SubPageLayoutProps) {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialLang = (searchParams.get("lang") as Language) || "es";
  const [lang, setLang] = useState<Language>(initialLang);

  useEffect(() => {
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.documentElement.lang = lang;
  }, [lang]);

  const title = SUB_PAGE_TITLES[lang]?.[slug] ?? slug;

  return (
    <div className="min-h-screen bg-gradient-to-b from-clara-bg via-[#F0F7FA] to-[#E8F1F5]">
      <header className="sticky top-0 z-10 bg-white/80 dark:bg-[#0f1419]/80 backdrop-blur-md border-b border-clara-border dark:border-[#2a2f36]">
        <div className="max-w-3xl mx-auto flex items-center justify-between px-4 py-3">
          <button
            onClick={() => navigate(`/?lang=${lang}`)}
            aria-label="Volver al inicio"
            className="w-touch-sm h-touch-sm flex items-center justify-center rounded-xl
                       hover:bg-clara-card dark:hover:bg-[#2a2f36] transition-colors
                       focus-visible:outline focus-visible:outline-[3px]
                       focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M19 12H5" />
              <path d="M12 19l-7-7 7-7" />
            </svg>
          </button>
          <h1 className="font-display font-bold text-h2 text-clara-text dark:text-[#e8e8ee] text-center flex-1">
            {title}
          </h1>
          <LanguageBar lang={lang} onChangeLang={setLang} />
        </div>
      </header>
      <main className="max-w-3xl mx-auto px-6 py-8">
        {children(lang)}
      </main>
      <footer className="text-center py-6 text-label text-clara-text-secondary/60">
        Clara &mdash; Tu voz tiene poder
      </footer>
    </div>
  );
}
