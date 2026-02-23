import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";
import { COMO_USAR_PAGE } from "@/lib/i18n";
import {
  STEP_ILLUSTRATIONS,
  EXAMPLE_ICONS,
  LARGE_GUARANTEE_ICONS,
} from "@/components/welcome/ComoUsarIllustrations";

/* ── useInView — triggers once when element enters viewport ── */
function useInView(threshold = 0.1) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold]);

  return { ref, visible };
}

/* ── Main page content ── */
function ComoUsarContent({ lang }: { lang: Language }) {
  const navigate = useNavigate();
  const t = COMO_USAR_PAGE[lang];

  const empathy = useInView();
  const stepsView = useInView();
  const examples = useInView();
  const guarantees = useInView();
  const cta = useInView();

  return (
    <div className="flex flex-col gap-14 pb-8">

      {/* ══ Empathy hero — visual first ══ */}
      <div ref={empathy.ref} className="text-center flex flex-col items-center gap-3 pt-2">
        {/* Confusion → Clarity visual */}
        <div
          aria-hidden="true"
          style={{
            opacity: empathy.visible ? 1 : 0,
            transform: empathy.visible ? "scale(1)" : "scale(0.8)",
            transition: "opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.22,1,0.36,1)",
          }}
        >
          <svg width="120" height="60" viewBox="0 0 120 60" fill="none">
            {/* Confused scribble → Clara arcs */}
            <path d="M 8 30 Q 14 15, 22 30 Q 28 45, 36 28" stroke="#D46A1E" strokeWidth="2" strokeLinecap="round" opacity="0.35" />
            <path d="M 12 35 Q 18 20, 26 38" stroke="#D46A1E" strokeWidth="1.5" strokeLinecap="round" opacity="0.2" />
            {/* Arrow */}
            <path d="M 44 30 L 74 30" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
            <path d="M 68 24 L 76 30 L 68 36" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.3" />
            {/* Clara arcs — clarity */}
            <path d="M 88 30 A 8 8 0 0 1 104 30" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
            <path d="M 92 30 A 4 4 0 0 1 100 30" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.7" />
            <circle cx="96" cy="31" r="2.5" fill="#2E7D4F" />
          </svg>
        </div>

        <h2
          className="font-display font-bold text-clara-text leading-tight"
          style={{
            fontSize: "clamp(26px, 5vw, 36px)",
            letterSpacing: "-0.02em",
            opacity: empathy.visible ? 1 : 0,
            transform: empathy.visible ? "translateY(0)" : "translateY(16px)",
            transition: "opacity 0.7s ease-out 0.1s, transform 0.7s ease-out 0.1s",
          }}
        >
          {t.empathy_headline}
        </h2>

        <p
          className="text-clara-text-secondary leading-relaxed"
          style={{
            fontSize: "clamp(16px, 2.5vw, 19px)",
            maxWidth: "44ch",
            opacity: empathy.visible ? 1 : 0,
            transition: "opacity 0.7s ease-out 0.2s",
          }}
        >
          {t.empathy_sub}
        </p>
      </div>

      {/* ══ Steps — illustration-first cards ══ */}
      <div ref={stepsView.ref} className="flex flex-col gap-3">
        <h3
          className="font-display font-bold text-clara-text text-center mb-4"
          style={{
            fontSize: "clamp(22px, 4vw, 28px)",
            opacity: stepsView.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        >
          {t.steps_title}
        </h3>

        <div className="grid grid-cols-2 gap-4">
          {t.steps.map((step, i) => (
            <div
              key={i}
              className="glass-card flex flex-col items-center text-center p-4 gap-2"
              style={{
                borderRadius: 20,
                opacity: stepsView.visible ? 1 : 0,
                transform: stepsView.visible ? "translateY(0) scale(1)" : "translateY(24px) scale(0.95)",
                transition: `opacity 0.6s ease-out ${150 + i * 120}ms, transform 0.6s cubic-bezier(0.22,1,0.36,1) ${150 + i * 120}ms`,
              }}
            >
              {/* Large illustration */}
              <div
                style={{
                  animation: stepsView.visible ? `float 6s ease-in-out ${i * 0.5}s infinite` : "none",
                }}
              >
                {STEP_ILLUSTRATIONS[i]}
              </div>

              {/* Step number badge */}
              <div
                className="brand-gradient"
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: "50%",
                  color: "white",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: "var(--font-display)",
                  fontWeight: 700,
                  fontSize: 15,
                  flexShrink: 0,
                }}
                aria-hidden="true"
              >
                {i + 1}
              </div>

              {/* Text — supporting */}
              <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
                {step.title}
              </p>
              <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* ══ Example questions — icon + text ══ */}
      <div ref={examples.ref} className="flex flex-col gap-4">
        <h3
          className="font-display font-bold text-clara-text text-center"
          style={{
            fontSize: "clamp(20px, 4vw, 26px)",
            opacity: examples.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        >
          {t.examples_title}
        </h3>

        <div className="grid grid-cols-2 gap-3">
          {t.examples.map((q, i) => (
            <button
              key={i}
              onClick={() => navigate(`/chat?lang=${lang}&q=${encodeURIComponent(q)}`)}
              className="glass-card flex flex-col items-center text-center gap-2 p-4
                         hover:shadow-warm-hover cursor-pointer
                         focus-visible:outline focus-visible:outline-[3px]
                         focus-visible:outline-clara-blue focus-visible:outline-offset-2"
              style={{
                borderRadius: 16,
                border: "1px solid rgba(var(--clara-blue-rgb),0.1)",
                opacity: examples.visible ? 1 : 0,
                transform: examples.visible ? "translateY(0)" : "translateY(12px)",
                transition: `all 0.5s ease-out ${i * 80}ms`,
              }}
            >
              {/* Topic icon — large, visual */}
              <div style={{ opacity: 0.8 }}>
                {EXAMPLE_ICONS[i]}
              </div>
              <span className="text-clara-text leading-snug" style={{ fontSize: 14 }}>
                {q}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* ══ Guarantees — icon-first grid ══ */}
      <div ref={guarantees.ref} className="grid grid-cols-2 gap-3">
        {t.guarantees.map((g, i) => (
          <div
            key={i}
            className="flex flex-col items-center text-center gap-2 p-4 rounded-2xl"
            style={{
              background: "rgba(var(--clara-blue-rgb),0.03)",
              border: "1px solid rgba(var(--clara-blue-rgb),0.08)",
              opacity: guarantees.visible ? 1 : 0,
              transform: guarantees.visible ? "translateY(0)" : "translateY(10px)",
              transition: `opacity 0.45s ease-out ${150 + i * 80}ms, transform 0.45s ease-out ${150 + i * 80}ms`,
            }}
          >
            {LARGE_GUARANTEE_ICONS[g.icon]}
            <span className="font-medium text-clara-text" style={{ fontSize: 14 }}>
              {g.text}
            </span>
          </div>
        ))}
      </div>

      {/* ══ CTA ══ */}
      <div ref={cta.ref} className="flex flex-col items-center gap-4 text-center py-6">
        <h3
          className="font-display font-bold text-clara-text"
          style={{
            fontSize: "clamp(22px, 5vw, 30px)",
            opacity: cta.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        >
          {t.cta_headline}
        </h3>
        <p
          className="text-clara-text-secondary"
          style={{
            fontSize: "clamp(15px, 2vw, 18px)",
            opacity: cta.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.1s",
          }}
        >
          {t.cta_sub}
        </p>
        <button
          onClick={() => navigate(`/chat?lang=${lang}`)}
          className="brand-gradient font-display font-bold text-white rounded-full
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          style={{
            padding: "14px 36px",
            fontSize: 18,
            boxShadow: "0 4px 20px rgba(var(--clara-blue-rgb),0.3)",
            opacity: cta.visible ? 1 : 0,
            transform: cta.visible ? "scale(1)" : "scale(0.9)",
            transition: "opacity 0.5s ease-out 0.2s, transform 0.5s cubic-bezier(0.22,1,0.36,1) 0.2s",
            minHeight: 52,
          }}
        >
          {t.cta_button}
        </button>
      </div>
    </div>
  );
}

export default function ComoUsarPage() {
  return (
    <SubPageLayout slug="como-usar">
      {(lang) => <ComoUsarContent lang={lang} />}
    </SubPageLayout>
  );
}
