import { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { GUIDE_SECTION, STATS } from "@/lib/i18n";

interface GuideSectionProps {
  lang: Language;
}

export default function GuideSection({ lang }: GuideSectionProps) {
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

  const t = GUIDE_SECTION[lang];

  return (
    <section
      ref={sectionRef}
      className="w-full py-12 px-6 bg-[#F0F7FA] dark:bg-[#141a20]"
      aria-labelledby="guide-title"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: "opacity 0.6s ease-out, transform 0.6s ease-out",
      }}
    >
      <div className="max-w-3xl mx-auto flex flex-col gap-8 text-center">
        <div>
          <h2
            id="guide-title"
            className="font-display font-bold text-h2 text-clara-blue mb-3"
          >
            Clara
          </h2>
          <p className="text-body text-clara-text-secondary leading-relaxed max-w-lg mx-auto italic">
            {t.empathy}
          </p>
        </div>

        <p className="text-body-sm text-clara-text dark:text-[#e8e8ee] leading-relaxed max-w-lg mx-auto">
          {t.authority}
        </p>

        {/* Stats strip */}
        <div className="stats-strip">
          {STATS[lang].map((stat, i) => (
            <div
              key={i}
              className="stat-item"
              style={{
                opacity: visible ? 1 : 0,
                transform: visible ? "translateY(0)" : "translateY(12px)",
                transition: `opacity 0.4s ease-out ${0.2 + i * 0.1}s, transform 0.4s ease-out ${0.2 + i * 0.1}s`,
              }}
            >
              <div className="stat-number">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
