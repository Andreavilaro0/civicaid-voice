import { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { SUCCESS_SECTION } from "@/lib/i18n";

interface SuccessSectionProps {
  lang: Language;
}

export default function SuccessSection({ lang }: SuccessSectionProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.disconnect(); } },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const t = SUCCESS_SECTION[lang];

  return (
    <section
      ref={sectionRef}
      className="w-full py-16 px-6 bg-[#FAFAFA] dark:bg-[#0f1419]"
      aria-labelledby="success-quote"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: "opacity 0.6s ease-out, transform 0.6s ease-out",
      }}
    >
      <div className="max-w-3xl mx-auto flex flex-col items-center gap-6 text-center">
        {/* Transformation: from → to */}
        <div className="flex flex-col sm:flex-row items-center gap-3 sm:gap-6 text-body-sm">
          <span className="px-4 py-2 rounded-full bg-clara-orange/10 text-clara-orange font-medium">
            {t.transformation_from}
          </span>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
               className="text-clara-green flex-shrink-0 rotate-90 sm:rotate-0" aria-hidden="true">
            <path d="M5 12h14" />
            <path d="M12 5l7 7-7 7" />
          </svg>
          <span className="px-4 py-2 rounded-full bg-clara-green/10 text-clara-green font-medium">
            {t.transformation_to}
          </span>
        </div>

        {/* Philosophical quote */}
        <blockquote
          id="success-quote"
          className="font-display font-bold text-h2 md:text-h1 text-clara-text dark:text-[#e8e8ee] leading-tight max-w-lg"
        >
          &ldquo;{t.quote}&rdquo;
        </blockquote>

        {/* Tagline repetition */}
        <p className="font-display font-bold text-[28px] md:text-[36px] leading-tight">
          <span className="text-clara-blue">{t.tagline[0]} </span>
          <span className="text-clara-orange">{t.tagline[1]}</span>
        </p>
      </div>
    </section>
  );
}
