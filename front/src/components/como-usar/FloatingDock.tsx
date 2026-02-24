import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { COMO_USAR_EXTRA } from "@/lib/i18n";
import { IconList } from "@/components/welcome/ComoUsarIllustrations";

const LANGUAGES: { code: Language; label: string }[] = [
  { code: "es", label: "ES" },
  { code: "en", label: "EN" },
  { code: "fr", label: "FR" },
  { code: "pt", label: "PT" },
  { code: "ro", label: "RO" },
  { code: "ca", label: "CA" },
  { code: "zh", label: "中文" },
  { code: "ar", label: "عربي" },
];

interface FloatingDockProps {
  lang: Language;
  setLang: (l: Language) => void;
}

export default function FloatingDock({ lang, setLang }: FloatingDockProps) {
  const navigate = useNavigate();
  const tx = COMO_USAR_EXTRA[lang];
  const [visible, setVisible] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Show dock after scrolling past hero (roughly 60vh)
  useEffect(() => {
    function onScroll() {
      const threshold = window.innerHeight * 1.0;
      setVisible(window.scrollY > threshold);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    if (!langOpen) return;
    function onClick(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setLangOpen(false);
      }
    }
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, [langOpen]);

  return (
    <nav
      className="como-usar-dock"
      data-visible={visible ? "true" : "false"}
      role="navigation"
      aria-label="Quick actions"
    >
      {/* Hablar button */}
      <button
        onClick={() => navigate(`/chat?lang=${lang}`)}
        className="btn-magnetic flex items-center gap-2 rounded-full font-display font-bold text-white
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        style={{
          padding: "10px 20px",
          fontSize: 14,
          background: "var(--color-clara-blue)",
          minHeight: 44,
        }}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <rect x="9" y="2" width="6" height="11" rx="3" />
          <path d="M5 10a7 7 0 0014 0" />
          <line x1="12" y1="17" x2="12" y2="21" />
        </svg>
        {tx.dock_talk}
      </button>

      {/* Guia button */}
      <button
        onClick={() => {
          document.getElementById("bento-grid")?.scrollIntoView({ behavior: "smooth" });
        }}
        className="btn-magnetic flex items-center gap-2 rounded-full font-display font-medium text-clara-text
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        style={{
          padding: "10px 18px",
          fontSize: 14,
          background: "rgba(var(--clara-blue-rgb),0.06)",
          border: "1px solid rgba(var(--clara-blue-rgb),0.12)",
          minHeight: 44,
        }}
      >
        <IconList />
        {tx.dock_guide}
      </button>

      {/* Idioma dropdown */}
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setLangOpen(!langOpen)}
          className="btn-magnetic flex items-center gap-2 rounded-full font-display font-medium text-clara-text
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          style={{
            padding: "10px 18px",
            fontSize: 14,
            background: "rgba(var(--clara-blue-rgb),0.06)",
            border: "1px solid rgba(var(--clara-blue-rgb),0.12)",
            minHeight: 44,
          }}
          aria-expanded={langOpen}
          aria-haspopup="listbox"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10" />
            <ellipse cx="12" cy="12" rx="4" ry="10" />
            <line x1="2" y1="12" x2="22" y2="12" />
          </svg>
          {tx.dock_language}
        </button>

        {langOpen && (
          <div
            role="listbox"
            className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 flex flex-wrap justify-center gap-1 p-2 rounded-2xl glass-card"
            style={{
              minWidth: 200,
            }}
          >
            {LANGUAGES.map((l) => (
              <button
                key={l.code}
                role="option"
                aria-selected={l.code === lang}
                onClick={() => {
                  setLang(l.code);
                  setLangOpen(false);
                }}
                className="rounded-full font-display font-medium transition-colors
                           focus-visible:outline focus-visible:outline-[3px]
                           focus-visible:outline-clara-blue focus-visible:outline-offset-2"
                style={{
                  padding: "6px 14px",
                  fontSize: 13,
                  minHeight: 36,
                  background: l.code === lang ? "var(--color-clara-blue)" : "transparent",
                  color: l.code === lang ? "white" : "var(--color-clara-text)",
                }}
              >
                {l.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
