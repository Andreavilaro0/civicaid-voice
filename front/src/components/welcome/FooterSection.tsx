import { Link } from "react-router-dom";
import type { Language } from "@/lib/types";
import { FOOTER_SECTION } from "@/lib/i18n";

interface FooterSectionProps {
  lang: Language;
}

export default function FooterSection({ lang }: FooterSectionProps) {
  const t = FOOTER_SECTION[lang];

  return (
    <footer className="relative w-full bg-clara-card">
      {/* Wave separator */}
      <div className="section-wave" aria-hidden="true">
        <svg viewBox="0 0 1200 48" preserveAspectRatio="none">
          <path
            d="M0 24 C 200 0, 400 48, 600 24 C 800 0, 1000 48, 1200 24 L1200 48 L0 48 Z"
            fill="currentColor"
            className="text-clara-card"
          />
        </svg>
      </div>

      <div className="px-6 pb-10 pt-4">
        <div className="max-w-3xl mx-auto flex flex-col items-center gap-5">
          {/* Clara mini logo */}
          <div className="footer-logo-shimmer flex items-center gap-2 mb-1" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 80 80" fill="none">
              <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="#1B5E7B" strokeWidth="3" strokeLinecap="round" opacity="0.5" />
              <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="#1B5E7B" strokeWidth="3" strokeLinecap="round" opacity="0.8" />
              <circle cx="28" cy="40" r="4" fill="#D46A1E" />
            </svg>
            <span className="font-display font-bold text-body-sm text-clara-text-secondary/50">Clara</span>
          </div>

          <nav className="flex flex-wrap justify-center gap-3" aria-label="Footer links">
            {t.links.map((link) => (
              <Link
                key={link.href}
                to={`${link.href}?lang=${lang}`}
                className="footer-link-pill focus-visible:outline focus-visible:outline-[3px]
                           focus-visible:outline-clara-blue focus-visible:outline-offset-2"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <p className="text-label text-clara-text-secondary/50 text-center">
            {t.credits}
          </p>
        </div>
      </div>
    </footer>
  );
}
