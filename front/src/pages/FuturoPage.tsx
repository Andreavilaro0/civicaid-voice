import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";
import { FUTURO_PAGE } from "@/lib/i18n";

/* ── useInView — fires once when element enters viewport ── */
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

/* ── Status badge colors (reused across languages) ── */
const STATUS_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  green: { bg: "rgba(46,125,79,0.08)", text: "#2E7D4F", border: "#2E7D4F" },
  blue: { bg: "rgba(27,94,123,0.08)", text: "#1B5E7B", border: "#1B5E7B" },
  orange: { bg: "rgba(212,106,30,0.08)", text: "#D46A1E", border: "#D46A1E" },
  muted: { bg: "rgba(74,74,90,0.06)", text: "#4A4A5A", border: "#4A4A5A" },
};
const STATUS_ORDER = ["green", "blue", "orange", "muted"] as const;

/* ── Step SVG icons (consistent with ComoUsarIllustrations) ── */
const ROADMAP_ICONS = [
  /* Languages — globe */
  <svg key="lang" width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
    <circle cx="24" cy="24" r="18" stroke="#2E7D4F" strokeWidth="1.5" opacity="0.3" />
    <ellipse cx="24" cy="24" rx="9" ry="18" stroke="#2E7D4F" strokeWidth="1" opacity="0.2" />
    <line x1="6" y1="24" x2="42" y2="24" stroke="#2E7D4F" strokeWidth="1" opacity="0.15" />
    <circle cx="24" cy="24" r="3" fill="#2E7D4F" opacity="0.5" />
  </svg>,
  /* Procedures — document */
  <svg key="proc" width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
    <rect x="12" y="6" width="24" height="36" rx="4" stroke="#1B5E7B" strokeWidth="1.5" opacity="0.3" />
    <line x1="18" y1="16" x2="30" y2="16" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.2" />
    <line x1="18" y1="22" x2="28" y2="22" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.15" />
    <line x1="18" y1="28" x2="26" y2="28" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.12" />
    <polyline points="20,34 23,37 30,30" stroke="#2E7D4F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.5" />
  </svg>,
  /* Partnerships — handshake */
  <svg key="part" width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
    <path d="M8 28 L16 20 L22 24 L28 18 L40 28" stroke="#D46A1E" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.35" />
    <circle cx="16" cy="20" r="3" fill="#D46A1E" opacity="0.15" />
    <circle cx="28" cy="18" r="3" fill="#1B5E7B" opacity="0.15" />
    <path d="M12 34 L24 34 L36 34" stroke="#D46A1E" strokeWidth="1" strokeLinecap="round" opacity="0.15" />
  </svg>,
  /* Mobile — phone */
  <svg key="app" width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
    <rect x="14" y="6" width="20" height="36" rx="4" stroke="#4A4A5A" strokeWidth="1.5" opacity="0.25" />
    <rect x="17" y="10" width="14" height="24" rx="2" fill="#4A4A5A" opacity="0.04" />
    <circle cx="24" cy="38" r="2" stroke="#4A4A5A" strokeWidth="1" opacity="0.2" />
    <path d="M21 22 A3 3 0 0 1 27 22" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
    <circle cx="24" cy="23" r="1.5" fill="#D46A1E" opacity="0.4" />
  </svg>,
];

/* ── Main content ── */
function FuturoContent({ lang }: { lang: Language }) {
  const navigate = useNavigate();
  const t = FUTURO_PAGE[lang];

  const hero = useInView();
  const roadmapView = useInView();
  const vision = useInView();
  const cta = useInView();

  return (
    <div className="flex flex-col gap-14 pb-8">

      {/* ══ SB7 Hero — empathy opening (Character + Problem) ══ */}
      <div ref={hero.ref} className="text-center flex flex-col items-center gap-4 pt-2">
        {/* Voice arc decorative */}
        <div
          aria-hidden="true"
          style={{
            opacity: hero.visible ? 1 : 0,
            transform: hero.visible ? "scale(1)" : "scale(0.8)",
            transition: "opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.22,1,0.36,1)",
          }}
        >
          <svg width="80" height="40" viewBox="0 0 80 40" fill="none">
            <path d="M 20 30 A 20 20 0 0 1 60 30" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.3" />
            <path d="M 28 30 A 12 12 0 0 1 52 30" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
            <path d="M 34 30 A 6 6 0 0 1 46 30" stroke="#2E7D4F" strokeWidth="2" strokeLinecap="round" opacity="0.7" />
            <circle cx="40" cy="31" r="2.5" fill="#D46A1E" />
          </svg>
        </div>

        <h2
          className="font-display font-bold text-clara-text dark:text-[#e8e8ee] leading-tight"
          style={{
            fontSize: "clamp(26px, 5vw, 36px)",
            letterSpacing: "-0.02em",
            opacity: hero.visible ? 1 : 0,
            transform: hero.visible ? "translateY(0)" : "translateY(16px)",
            transition: "opacity 0.7s ease-out 0.1s, transform 0.7s ease-out 0.1s",
          }}
        >
          {t.hero_headline}
        </h2>

        <p
          className="text-clara-text-secondary dark:text-[#a0a0b0] leading-relaxed"
          style={{
            fontSize: "clamp(16px, 2.5vw, 19px)",
            maxWidth: "48ch",
            opacity: hero.visible ? 1 : 0,
            transition: "opacity 0.7s ease-out 0.25s",
          }}
        >
          {t.hero_sub}
        </p>
      </div>

      {/* ══ Roadmap — benefit-first cards (Guide + Plan) ══ */}
      <div ref={roadmapView.ref} className="flex flex-col gap-3">
        <h3
          className="font-display font-bold text-clara-text dark:text-[#e8e8ee] text-center mb-4"
          style={{
            fontSize: "clamp(22px, 4vw, 28px)",
            opacity: roadmapView.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        >
          {t.roadmap_title}
        </h3>

        <div className="flex flex-col gap-4">
          {t.roadmap.map((item, i) => {
            const colorKey = STATUS_ORDER[i] ?? "muted";
            const colors = STATUS_COLORS[colorKey];
            return (
              <div
                key={item.title}
                style={{
                  background: "white",
                  borderRadius: "20px",
                  borderLeft: `4px solid ${colors.border}`,
                  padding: "clamp(20px, 3vw, 28px)",
                  boxShadow: "0 2px 16px rgba(0,0,0,0.04), 0 0 0 1px rgba(27,94,123,0.04)",
                  opacity: roadmapView.visible ? 1 : 0,
                  transform: roadmapView.visible ? "translateY(0)" : "translateY(20px)",
                  transition: `opacity 0.6s ease-out ${150 + i * 120}ms, transform 0.6s cubic-bezier(0.22,1,0.36,1) ${150 + i * 120}ms`,
                }}
              >
                <div className="flex items-start gap-4">
                  {/* SVG icon */}
                  <div
                    className="flex-shrink-0"
                    style={{
                      animation: roadmapView.visible ? `float 6s ease-in-out ${i * 0.5}s infinite` : "none",
                    }}
                  >
                    {ROADMAP_ICONS[i]}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <h4 className="font-display font-bold text-clara-text dark:text-[#e8e8ee]" style={{ fontSize: "clamp(17px, 2.5vw, 20px)" }}>
                        {item.title}
                      </h4>
                      <span
                        style={{
                          fontSize: "11px",
                          fontWeight: 600,
                          letterSpacing: "0.06em",
                          padding: "3px 10px",
                          borderRadius: "20px",
                          background: colors.bg,
                          color: colors.text,
                        }}
                      >
                        {item.status}
                      </span>
                    </div>
                    <p
                      className="text-clara-text-secondary dark:text-[#a0a0b0] leading-relaxed"
                      style={{ fontSize: "clamp(15px, 2vw, 17px)", margin: 0 }}
                    >
                      {item.benefit}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ══ Vision — success picture (SB7 #7 Success) ══ */}
      <div ref={vision.ref} className="flex flex-col items-center text-center gap-4">
        {/* Orange divider accent */}
        <div
          aria-hidden="true"
          style={{
            width: "48px",
            height: "2px",
            background: "#D46A1E",
            opacity: vision.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        />

        <h3
          className="font-display font-bold text-clara-text dark:text-[#e8e8ee]"
          style={{
            fontSize: "clamp(22px, 4.5vw, 30px)",
            opacity: vision.visible ? 1 : 0,
            transform: vision.visible ? "translateY(0)" : "translateY(12px)",
            transition: "opacity 0.7s ease-out 0.1s, transform 0.7s ease-out 0.1s",
          }}
        >
          {t.vision_headline}
        </h3>

        <p
          className="text-clara-text-secondary dark:text-[#a0a0b0] leading-relaxed"
          style={{
            fontSize: "clamp(16px, 2.5vw, 19px)",
            maxWidth: "44ch",
            fontStyle: "italic",
            opacity: vision.visible ? 1 : 0,
            transition: "opacity 0.7s ease-out 0.2s",
          }}
        >
          {t.vision_text}
        </p>
      </div>

      {/* ══ CTA — call to action (SB7 #5) ══ */}
      <div ref={cta.ref} className="flex flex-col items-center gap-4 text-center py-4">
        <h3
          className="font-display font-bold text-clara-text dark:text-[#e8e8ee]"
          style={{
            fontSize: "clamp(22px, 5vw, 30px)",
            opacity: cta.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        >
          {t.cta_headline}
        </h3>
        <p
          className="text-clara-text-secondary dark:text-[#a0a0b0]"
          style={{
            fontSize: "clamp(15px, 2vw, 18px)",
            maxWidth: "40ch",
            opacity: cta.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.1s",
          }}
        >
          {t.cta_sub}
        </p>
        <button
          onClick={() => navigate(`/chat?lang=${lang}`)}
          className="font-display font-bold text-white rounded-full
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          style={{
            background: "linear-gradient(135deg, #1B5E7B, #134a5f)",
            padding: "14px 36px",
            fontSize: 18,
            boxShadow: "0 4px 20px rgba(27,94,123,0.3)",
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

export default function FuturoPage() {
  return (
    <SubPageLayout slug="futuro">
      {(lang) => <FuturoContent lang={lang} />}
    </SubPageLayout>
  );
}
