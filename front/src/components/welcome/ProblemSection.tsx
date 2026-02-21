import { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { PROBLEM_SECTION, IMPACT, BEFORE_AFTER } from "@/lib/i18n";

interface ProblemSectionProps {
  lang: Language;
}

function AnimatedCounter({ target, label }: { target: string; label: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [count, setCount] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.disconnect(); } },
      { threshold: 0.3 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!visible) return;
    const end = 4.5;
    const duration = 1200;
    const steps = 30;
    const increment = end / steps;
    let current = 0;
    const timer = setInterval(() => {
      current += increment;
      if (current >= end) { setCount(end); clearInterval(timer); return; }
      setCount(Math.round(current * 10) / 10);
    }, duration / steps);
    return () => clearInterval(timer);
  }, [visible]);

  return (
    <div ref={ref} className="text-center">
      <span className="impact-counter" aria-label={target}>
        {visible ? `${count}M` : "0M"}
      </span>
      <p className="text-body-sm text-clara-text-secondary mt-1 max-w-md mx-auto leading-relaxed">
        {label}
      </p>
    </div>
  );
}

export default function ProblemSection({ lang }: ProblemSectionProps) {
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

  const t = PROBLEM_SECTION[lang];

  return (
    <section
      ref={sectionRef}
      className="w-full py-12 px-6 bg-white dark:bg-[#1a1f26]"
      aria-labelledby="problem-title"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: "opacity 0.6s ease-out, transform 0.6s ease-out",
      }}
    >
      <div className="max-w-3xl mx-auto flex flex-col gap-8">
        <div className="text-center">
          <h2
            id="problem-title"
            className="font-display font-bold text-h1 text-clara-text dark:text-[#e8e8ee] mb-3"
          >
            {t.title}
          </h2>
          <p className="text-body text-clara-text-secondary leading-relaxed max-w-lg mx-auto">
            {t.subtitle}
          </p>
        </div>

        <AnimatedCounter target="4.5M" label={IMPACT[lang].counter_label} />

        {/* Before / After */}
        <div>
          <div className="flex gap-4 mb-3">
            <span className="flex-1 text-center font-display font-bold text-body-sm text-clara-orange">
              {IMPACT[lang].before_label}
            </span>
            <span className="flex-1 text-center font-display font-bold text-body-sm text-clara-green">
              {IMPACT[lang].after_label}
            </span>
          </div>
          <div className="flex flex-col gap-3">
            {BEFORE_AFTER[lang].slice(0, 2).map((row, i) => (
              <div key={i} className="before-after-grid">
                <div className="before-cell">{row.before}</div>
                <div className="after-cell">{row.after}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
