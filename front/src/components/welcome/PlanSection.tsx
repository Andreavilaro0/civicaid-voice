import React, { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { PLAN_SECTION } from "@/lib/i18n";

interface PlanSectionProps {
  lang: Language;
}

const AGREEMENT_ICONS: Record<string, React.ReactNode> = {
  free: (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <path d="M16 8h-6a2 2 0 100 4h4a2 2 0 010 4H8" />
      <path d="M12 18V6" />
    </svg>
  ),
  lock: (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0110 0v4" />
    </svg>
  ),
  "no-register": (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
      <circle cx="12" cy="7" r="4" />
      <line x1="2" y1="2" x2="22" y2="22" />
    </svg>
  ),
  clock: (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  ),
};

export default function PlanSection({ lang }: PlanSectionProps) {
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

  const t = PLAN_SECTION[lang];

  return (
    <section
      ref={sectionRef}
      className="w-full py-12 px-6 bg-white dark:bg-[#1a1f26]"
      aria-labelledby="plan-title"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: "opacity 0.6s ease-out, transform 0.6s ease-out",
      }}
    >
      <div className="max-w-3xl mx-auto flex flex-col gap-8">
        <h2
          id="plan-title"
          className="font-display font-bold text-h1 text-clara-text dark:text-[#e8e8ee] text-center"
        >
          {t.title}
        </h2>

        {/* 3 steps */}
        <div className="flex flex-col gap-4 max-w-md mx-auto w-full">
          {t.steps.map((step, i) => (
            <div
              key={i}
              className="flex items-center gap-4 p-4 bg-[#F0F7FA] dark:bg-[#141a20] rounded-2xl"
              style={{
                opacity: visible ? 1 : 0,
                transform: visible ? "translateX(0)" : "translateX(-16px)",
                transition: `opacity 0.5s ease-out ${i * 0.15}s, transform 0.5s ease-out ${i * 0.15}s`,
              }}
            >
              <span className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-clara-blue text-white font-display font-bold text-h2">
                {step.number}
              </span>
              <p className="text-body text-clara-text dark:text-[#e8e8ee] leading-snug">
                {step.text}
              </p>
            </div>
          ))}
        </div>

        {/* Agreements strip */}
        <div className="flex flex-wrap justify-center gap-6 mt-2">
          {t.agreements.map((agreement, i) => (
            <div
              key={i}
              className="flex flex-col items-center gap-2 text-clara-text-secondary"
              style={{
                opacity: visible ? 1 : 0,
                transition: `opacity 0.4s ease-out ${0.5 + i * 0.1}s`,
              }}
            >
              <span className="text-clara-blue">
                {AGREEMENT_ICONS[agreement.icon]}
              </span>
              <span className="text-label font-medium">{agreement.text}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
