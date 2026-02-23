import React, { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { PLAN_SECTION } from "@/lib/i18n";

interface PlanSectionProps {
  lang: Language;
}

const AGREEMENT_ICONS: Record<string, React.ReactNode> = {
  free: (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <path d="M16 8h-6a2 2 0 100 4h4a2 2 0 010 4H8" />
      <path d="M12 18V6" />
    </svg>
  ),
  lock: (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0110 0v4" />
    </svg>
  ),
  "no-register": (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
      <circle cx="12" cy="7" r="4" />
      <line x1="2" y1="2" x2="22" y2="22" />
    </svg>
  ),
  clock: (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
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
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const t = PLAN_SECTION[lang];

  return (
    <section
      ref={sectionRef}
      className="relative w-full py-20 px-6 bg-clara-card overflow-hidden"
      aria-labelledby="plan-title"
    >
      {/* Decorative voice arcs — reinforcing Clara's sonic identity */}
      <div className="voice-arc-decorative" aria-hidden="true" style={{ top: "20%", left: "-50px", animationDelay: "1.5s" }}>
        <svg width="90" height="90" viewBox="0 0 80 80" fill="none" style={{ opacity: 0.5 }}>
          <path d="M 50 20 A 22 22 0 0 1 50 60" stroke="var(--color-clara-blue)" strokeWidth="1.5" strokeLinecap="round" opacity="0.25" />
          <path d="M 44 28 A 14 14 0 0 1 44 52" stroke="var(--color-clara-blue)" strokeWidth="1.5" strokeLinecap="round" opacity="0.4" />
          <circle cx="38" cy="40" r="2" fill="var(--color-clara-orange)" opacity="0.5" />
        </svg>
      </div>
      <div className="voice-arc-decorative" aria-hidden="true" style={{ bottom: "10%", right: "-30px", animationDelay: "4s" }}>
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" style={{ opacity: 0.35, transform: "scaleX(-1)" }}>
          <path d="M 50 22 A 20 20 0 0 1 50 58" stroke="var(--color-clara-green)" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
          <path d="M 44 30 A 12 12 0 0 1 44 50" stroke="var(--color-clara-green)" strokeWidth="1.5" strokeLinecap="round" opacity="0.45" />
          <circle cx="38" cy="40" r="2" fill="var(--color-clara-orange)" opacity="0.5" />
        </svg>
      </div>

      <div className="relative max-w-5xl mx-auto flex flex-col gap-14">

        {/* Section title */}
        <h2
          id="plan-title"
          className="font-display font-bold text-h1 text-clara-text text-center heading-tight"
          style={{
            opacity: visible ? 1 : 0,
            transform: visible ? "translateY(0)" : "translateY(20px)",
            transition: "opacity 0.7s ease-out, transform 0.7s ease-out",
          }}
        >
          {t.title}
        </h2>

        {/* ── Desktop: horizontal timeline / Mobile: vertical stack ── */}
        <div className="relative">

          {/* Horizontal connector line — desktop only, sits between the cards */}
          <div
            className="hidden md:block absolute"
            style={{ top: "40px", left: "calc(16.666% + 40px)", right: "calc(16.666% + 40px)" }}
            aria-hidden="true"
          >
            <div
              className={`step-connector-h${visible ? " revealed" : ""}`}
              style={{ animationDelay: "0.4s" }}
            />
          </div>

          {/* Cards row */}
          <div className="flex flex-col gap-5 md:flex-row md:items-start md:gap-8">
            {t.steps.map((step, i) => (
              <div
                key={i}
                className="flex-1 flex flex-col items-center text-center gap-5"
                style={{
                  opacity: visible ? 1 : 0,
                  animation: visible
                    ? `stepSlideUp 0.65s cubic-bezier(0.22, 1, 0.36, 1) ${0.2 + i * 0.18}s both`
                    : "none",
                }}
              >
                {/* Step number — mega circle */}
                <div
                  className="step-number-mega relative z-10"
                  aria-hidden="true"
                >
                  {step.number}
                </div>

                {/* Vertical connector — mobile only */}
                {i < t.steps.length - 1 && (
                  <div
                    className="block md:hidden w-0.5 h-8 bg-gradient-to-b from-clara-blue/20 to-clara-blue/5 rounded-full"
                    aria-hidden="true"
                    style={{
                      animation: visible
                        ? `drawLine 0.6s ease-out ${0.3 + i * 0.18}s both`
                        : "none",
                    }}
                  />
                )}

                {/* Card body */}
                <div className="glass-card w-full p-6 flex flex-col items-center gap-3">
                  <p className="text-body text-clara-text leading-snug">
                    {step.text}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Guarantee badges ── */}
        <div
          className="flex flex-wrap justify-center gap-4"
          style={{
            opacity: visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.75s",
          }}
        >
          {t.agreements.map((agreement, i) => (
            <div
              key={i}
              className={`guarantee-badge${visible ? " badge-shimmer" : ""}`}
              style={{
                opacity: visible ? 1 : 0,
                transform: visible ? "translateY(0)" : "translateY(10px)",
                transition: `opacity 0.45s ease-out ${0.8 + i * 0.12}s, transform 0.45s ease-out ${0.8 + i * 0.12}s`,
                // Stagger the shimmer animation per badge
                ...(visible ? { "--shimmer-delay": `${0.9 + i * 0.15}s` } as React.CSSProperties : {}),
              }}
            >
              <span className="text-clara-blue flex-shrink-0">
                {AGREEMENT_ICONS[agreement.icon]}
              </span>
              <span className="text-body-sm font-medium text-clara-text">
                {agreement.text}
              </span>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
