import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { ThemeToggleCompact } from "@/components/ui/ThemeToggle";
import LanguageBar from "@/components/welcome/LanguageBar";

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
}

const ariaLabels: Record<Language, { back: string; menu: string; closeMenu: string }> = {
  es: { back: "Volver al inicio", menu: "Abrir menu", closeMenu: "Cerrar menu" },
  en: { back: "Back to home", menu: "Open menu", closeMenu: "Close menu" },
  fr: { back: "Retour a l'accueil", menu: "Ouvrir le menu", closeMenu: "Fermer le menu" },
  pt: { back: "Voltar ao inicio", menu: "Abrir menu", closeMenu: "Fechar menu" },
  ro: { back: "Inapoi la pagina principala", menu: "Deschide meniul", closeMenu: "Inchide meniul" },
  ca: { back: "Tornar a l'inici", menu: "Obrir menu", closeMenu: "Tancar menu" },
  zh: { back: "返回首页", menu: "打开菜单", closeMenu: "关闭菜单" },
  ar: { back: "العودة إلى الرئيسية", menu: "فتح القائمة", closeMenu: "إغلاق القائمة" },
};

const languageNames: Record<Language, string> = {
  es: "Español", en: "English", fr: "Français", pt: "Português",
  ro: "Română", ca: "Català", zh: "中文", ar: "عربي",
};

/** Teal rounded-square mascot avatar matching the reference design */
function ClaraMascotAvatar() {
  return (
    <div
      className="w-10 h-10 rounded-2xl bg-clara-blue flex items-center justify-center shadow-sm"
      aria-hidden="true"
    >
      <svg width="22" height="22" viewBox="0 0 32 32" fill="none">
        <rect x="6" y="4" width="20" height="18" rx="6" stroke="white" strokeWidth="1.8" fill="none" />
        <circle cx="12" cy="13" r="2" fill="white" />
        <circle cx="20" cy="13" r="2" fill="white" />
        <path d="M11 18 Q16 22 21 18" stroke="white" strokeWidth="1.6" strokeLinecap="round" fill="none" />
        <line x1="16" y1="4" x2="16" y2="1" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="16" cy="0.5" r="1.2" fill="white" />
        <rect x="2" y="10" width="4" height="6" rx="2" fill="white" opacity="0.7" />
        <rect x="26" y="10" width="4" height="6" rx="2" fill="white" opacity="0.7" />
      </svg>
    </div>
  );
}

export default function Header({ language, onLanguageChange }: HeaderProps) {
  const navigate = useNavigate();
  const labels = ariaLabels[language];
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const menuBtnRef = useRef<HTMLButtonElement>(null);

  const closeMenu = useCallback(() => setMenuOpen(false), []);

  // Close menu on Escape
  useEffect(() => {
    if (!menuOpen) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") closeMenu();
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [menuOpen, closeMenu]);

  // Close menu on outside click
  useEffect(() => {
    if (!menuOpen) return;
    function onClick(e: MouseEvent) {
      if (
        menuRef.current && !menuRef.current.contains(e.target as Node) &&
        menuBtnRef.current && !menuBtnRef.current.contains(e.target as Node)
      ) {
        closeMenu();
      }
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [menuOpen, closeMenu]);

  return (
    <header className="sticky top-0 z-20 bg-white/90 dark:bg-[#1a1a2e]/90 backdrop-blur-xl border-b border-clara-border/40">
      <div className="flex items-center justify-between px-3 h-[56px]">
        {/* Left: Back button */}
        <button
          onClick={() => navigate("/")}
          aria-label={labels.back}
          className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-xl
                     text-clara-text-secondary hover:bg-clara-card transition-colors duration-150 flex-shrink-0"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M19 12H5" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
        </button>

        {/* Center: Clara identity */}
        <div className="flex items-center gap-2.5 flex-shrink-0">
          <ClaraMascotAvatar />
          <div className="min-w-0">
            <h1 className="font-display font-bold text-[17px] text-clara-text leading-tight">Clara</h1>
            <div className="flex items-center gap-1.5">
              <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
              <p className="text-[12px] text-emerald-600 dark:text-emerald-400 font-medium leading-tight">
                {languageNames[language]}
              </p>
            </div>
          </div>
        </div>

        {/* Right: Theme toggle (always visible) + Hamburger menu button */}
        <div className="flex items-center gap-0.5 flex-shrink-0">
          <ThemeToggleCompact />

          {/* Hamburger button */}
          <button
            ref={menuBtnRef}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label={menuOpen ? labels.closeMenu : labels.menu}
            aria-expanded={menuOpen}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-xl
                       text-clara-text-secondary hover:bg-clara-card transition-colors duration-150"
          >
            {menuOpen ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                   strokeWidth="2.5" strokeLinecap="round" aria-hidden="true">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                   strokeWidth="2.5" strokeLinecap="round" aria-hidden="true">
                <line x1="4" y1="7" x2="20" y2="7" />
                <line x1="4" y1="12" x2="20" y2="12" />
                <line x1="4" y1="17" x2="20" y2="17" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Dropdown menu panel */}
      {menuOpen && (
        <>
          {/* Overlay */}
          <div
            className="fixed inset-0 top-[56px] bg-black/20 z-10"
            style={{ animation: "overlayFadeIn 0.2s ease-out" }}
            onClick={closeMenu}
            aria-hidden="true"
          />

          {/* Menu panel */}
          <div
            ref={menuRef}
            className="absolute top-[56px] left-0 right-0 z-20
                       bg-white dark:bg-[#1a1a2e] border-b border-clara-border/40
                       shadow-lg px-4 py-4 space-y-4"
            style={{ animation: "fadeInUp 0.2s ease-out" }}
            role="menu"
          >
            {/* Language selector — full-size pills */}
            <div>
              <p className="text-[12px] font-medium text-clara-text-secondary uppercase tracking-wider mb-2">
                {language === "en" ? "Language" : language === "fr" ? "Langue" : language === "ar" ? "اللغة" : language === "zh" ? "语言" : "Idioma"}
              </p>
              <LanguageBar
                lang={language}
                onChangeLang={(lang) => {
                  onLanguageChange(lang);
                  closeMenu();
                }}
              />
            </div>
          </div>
        </>
      )}
    </header>
  );
}
