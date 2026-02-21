import { useEffect, useRef, useCallback } from "react";
import { Link } from "react-router-dom";

type Lang = "es" | "fr" | "ar";

interface MenuItem {
  href: string;
  label: string;
}

interface HamburgerMenuProps {
  isOpen: boolean;
  onClose: () => void;
  items: MenuItem[];
  lang: Lang;
}

export default function HamburgerMenu({ isOpen, onClose, items, lang }: HamburgerMenuProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  const firstLinkRef = useRef<HTMLAnchorElement>(null);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "Tab" && panelRef.current) {
        const focusable = panelRef.current.querySelectorAll<HTMLElement>(
          'a, button, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    },
    [onClose]
  );

  useEffect(() => {
    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      setTimeout(() => firstLinkRef.current?.focus(), 100);
    }
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-30" role="dialog" aria-modal="true" aria-label="Menu">
      <div
        className="absolute inset-0 bg-black/40"
        style={{ animation: "overlayFadeIn 0.2s ease-out" }}
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        ref={panelRef}
        className="menu-panel absolute top-0 start-0 h-full w-[300px] max-w-[80vw]
                   bg-white dark:bg-[#1a1f26] shadow-2xl flex flex-col"
        style={{ animation: "menuSlideIn 0.25s ease-out" }}
      >
        <div className="flex items-center justify-between p-4 border-b border-clara-border dark:border-[#2a2f36]">
          <span className="font-display font-bold text-h2 text-clara-blue">Clara</span>
          <button
            onClick={onClose}
            aria-label="Cerrar menu"
            className="w-touch-sm h-touch-sm flex items-center justify-center rounded-xl
                       hover:bg-clara-card dark:hover:bg-[#2a2f36] transition-colors
                       focus-visible:outline focus-visible:outline-[3px]
                       focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M18 6L6 18" />
              <path d="M6 6l12 12" />
            </svg>
          </button>
        </div>
        <nav className="flex-1 p-4">
          <ul className="flex flex-col gap-2">
            {items.map((item, i) => (
              <li key={item.href}>
                <Link
                  ref={i === 0 ? firstLinkRef : undefined}
                  to={`${item.href}?lang=${lang}`}
                  onClick={onClose}
                  className="flex items-center gap-3 px-4 py-3 min-h-touch-sm
                             rounded-xl text-body text-clara-text dark:text-[#e8e8ee]
                             hover:bg-clara-card dark:hover:bg-[#2a2f36] transition-colors
                             focus-visible:outline focus-visible:outline-[3px]
                             focus-visible:outline-clara-blue focus-visible:outline-offset-2"
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <div className="p-4 border-t border-clara-border dark:border-[#2a2f36]">
          <Link
            to={`/?lang=${lang}`}
            onClick={onClose}
            className="flex items-center gap-2 px-4 py-3 min-h-touch-sm
                       rounded-xl text-body-sm text-clara-text-secondary
                       hover:bg-clara-card dark:hover:bg-[#2a2f36] transition-colors
                       focus-visible:outline focus-visible:outline-[3px]
                       focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1" />
            </svg>
            Inicio
          </Link>
        </div>
      </div>
    </div>
  );
}
