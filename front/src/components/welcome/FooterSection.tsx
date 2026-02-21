import { Link } from "react-router-dom";
import type { Language } from "@/lib/types";
import { FOOTER_SECTION } from "@/lib/i18n";

interface FooterSectionProps {
  lang: Language;
}

export default function FooterSection({ lang }: FooterSectionProps) {
  const t = FOOTER_SECTION[lang];

  return (
    <footer className="w-full py-8 px-6 bg-white dark:bg-[#1a1f26] border-t border-clara-border dark:border-[#2a2f36]">
      <div className="max-w-3xl mx-auto flex flex-col items-center gap-4">
        <nav className="flex flex-wrap justify-center gap-4" aria-label="Footer links">
          {t.links.map((link) => (
            <Link
              key={link.href}
              to={`${link.href}?lang=${lang}`}
              className="text-body-sm text-clara-blue hover:text-[#134a5f] underline underline-offset-4
                         transition-colors focus-visible:outline focus-visible:outline-[3px]
                         focus-visible:outline-clara-blue focus-visible:outline-offset-2
                         min-h-touch-sm flex items-center"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <p className="text-label text-clara-text-secondary/60 text-center">
          {t.credits}
        </p>
      </div>
    </footer>
  );
}
