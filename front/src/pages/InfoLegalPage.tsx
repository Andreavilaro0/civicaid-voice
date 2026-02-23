import { useEffect, useRef, useState } from "react";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";
import { LEGAL_PAGE } from "@/lib/i18n";

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

/* ── Section accent colors — rotating per card (like FuturoPage status colors) ── */
const SECTION_ACCENTS = [
  { border: "var(--color-clara-blue)", bg: "rgba(var(--clara-blue-rgb),0.06)", iconBg: "rgba(var(--clara-blue-rgb),0.10)" },
  { border: "var(--color-clara-green)", bg: "rgba(var(--clara-green-rgb),0.05)", iconBg: "rgba(var(--clara-green-rgb),0.10)" },
  { border: "var(--color-clara-orange)", bg: "rgba(var(--clara-orange-rgb),0.05)", iconBg: "rgba(var(--clara-orange-rgb),0.10)" },
  { border: "var(--color-clara-blue)", bg: "rgba(var(--clara-blue-rgb),0.06)", iconBg: "rgba(var(--clara-blue-rgb),0.10)" },
  { border: "var(--color-clara-green)", bg: "rgba(var(--clara-green-rgb),0.05)", iconBg: "rgba(var(--clara-green-rgb),0.10)" },
  { border: "var(--color-clara-orange)", bg: "rgba(var(--clara-orange-rgb),0.05)", iconBg: "rgba(var(--clara-orange-rgb),0.10)" },
  { border: "var(--color-clara-blue)", bg: "rgba(var(--clara-blue-rgb),0.06)", iconBg: "rgba(var(--clara-blue-rgb),0.10)" },
] as const;

/* ── Section icons (48x48 — matching FuturoPage icon size) ── */
const SECTION_ICONS: Record<string, React.ReactNode> = {
  ai: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <rect x="8" y="14" width="32" height="22" rx="5" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <circle cx="18" cy="25" r="3.5" fill="currentColor" opacity="0.5" />
      <circle cx="30" cy="25" r="3.5" fill="currentColor" opacity="0.5" />
      <path d="M16 8v6M32 8v6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <path d="M24 36v5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <path d="M20 36h8" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.15" />
    </svg>
  ),
  data: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <ellipse cx="24" cy="12" rx="14" ry="5" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <path d="M10 12v10c0 2.76 6.27 5 14 5s14-2.24 14-5V12" stroke="currentColor" strokeWidth="1.5" opacity="0.25" />
      <path d="M10 22v10c0 2.76 6.27 5 14 5s14-2.24 14-5V22" stroke="currentColor" strokeWidth="1.5" opacity="0.2" />
      <circle cx="24" cy="22" r="2" fill="currentColor" opacity="0.4" />
    </svg>
  ),
  services: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <circle cx="14" cy="34" r="5" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <circle cx="34" cy="34" r="5" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <circle cx="24" cy="14" r="5" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <path d="M20 17L16 30M28 17L32 30" stroke="currentColor" strokeWidth="1" opacity="0.15" />
      <path d="M19 34h10" stroke="currentColor" strokeWidth="1" opacity="0.15" />
      <circle cx="24" cy="14" r="2" fill="currentColor" opacity="0.35" />
    </svg>
  ),
  clock: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <circle cx="24" cy="24" r="16" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <circle cx="24" cy="24" r="12" stroke="currentColor" strokeWidth="1" opacity="0.1" />
      <path d="M24 14v10l6 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.5" />
      <circle cx="24" cy="24" r="2" fill="currentColor" opacity="0.4" />
    </svg>
  ),
  rights: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <circle cx="24" cy="24" r="16" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <path d="M15 24l5 5 13-13" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.5" />
    </svg>
  ),
  handshake: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M8 24 L16 16 L24 22 L32 14 L40 24" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.35" />
      <circle cx="16" cy="16" r="3" fill="currentColor" opacity="0.15" />
      <circle cx="32" cy="14" r="3" fill="currentColor" opacity="0.15" />
      <path d="M16 32 L24 26 L32 32" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.25" />
    </svg>
  ),
  shield: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M24 4L8 12v10c0 9.5 6.8 18.4 16 20.5 9.2-2.1 16-11 16-20.5V12L24 4z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" opacity="0.3" />
      <path d="M18 24l4 4 8-8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.5" />
      <circle cx="24" cy="24" r="2" fill="currentColor" opacity="0.15" />
    </svg>
  ),
};

/* ── LegalSection — individual observe for staggered per-card reveal ── */
function LegalSection({
  section,
  index,
}: {
  section: { icon: string; heading: string; paragraphs: string[] };
  index: number;
}) {
  const { ref, visible } = useInView(0.1);
  const accent = SECTION_ACCENTS[index];

  return (
    <div
      ref={ref}
      className="glass-card"
      style={{
        borderLeft: `4px solid ${accent.border}`,
        padding: "clamp(20px, 3vw, 28px)",
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: `opacity 0.6s ease-out ${150 + index * 120}ms, transform 0.6s cubic-bezier(0.22,1,0.36,1) ${150 + index * 120}ms`,
      }}
    >
      <div className="flex items-start gap-4">
        {/* Icon with soft background circle + float animation */}
        <div
          className="flex-shrink-0 flex items-center justify-center text-clara-blue"
          style={{
            width: 56,
            height: 56,
            borderRadius: "50%",
            background: accent.iconBg,
            animation: visible ? `float 6s ease-in-out ${index * 0.5}s infinite` : "none",
          }}
        >
          {SECTION_ICONS[section.icon] ?? SECTION_ICONS.shield}
        </div>

        <div className="flex-1 min-w-0">
          {/* Section number + heading */}
          <div className="flex items-center gap-2.5 mb-3 flex-wrap">
            <span
              className="brand-gradient flex-shrink-0"
              style={{
                width: 26,
                height: 26,
                borderRadius: "50%",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: "var(--font-display)",
                fontWeight: 700,
                fontSize: 12,
              }}
              aria-hidden="true"
            >
              {index + 1}
            </span>
            <h3
              className="font-display font-bold text-clara-text"
              style={{ fontSize: "clamp(17px, 2.5vw, 20px)" }}
            >
              {section.heading}
            </h3>
          </div>

          {section.paragraphs.map((p, j) => (
            <p
              key={j}
              className="text-clara-text-secondary leading-relaxed mb-2 last:mb-0"
              style={{ fontSize: "clamp(15px, 2vw, 17px)" }}
            >
              {p}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ── Main content ── */
function InfoLegalContent({ lang }: { lang: Language }) {
  const t = LEGAL_PAGE[lang];
  const hero = useInView();

  return (
    <div className="flex flex-col gap-10 pb-8">

      {/* ══ Hero — trust visual (shield + Clara arcs) ══ */}
      <div ref={hero.ref} className="text-center flex flex-col items-center gap-4 pt-2">
        {/* Decorative shield with Clara voice arcs */}
        <div
          aria-hidden="true"
          style={{
            opacity: hero.visible ? 1 : 0,
            transform: hero.visible ? "scale(1)" : "scale(0.8)",
            transition: "opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.22,1,0.36,1)",
          }}
        >
          <svg width="100" height="80" viewBox="0 0 100 80" fill="none">
            {/* Shield outline */}
            <path
              d="M50 8 L22 20 v16 c0 16 11.5 31 28 35 16.5-4 28-19 28-35 V20 L50 8z"
              stroke="var(--color-clara-blue)"
              strokeWidth="1.5"
              fill="none"
              opacity="0.15"
            />
            <path
              d="M50 16 L30 25 v12 c0 12 8.5 23 20 26 11.5-3 20-14 20-26 V25 L50 16z"
              stroke="var(--color-clara-blue)"
              strokeWidth="1.5"
              fill="none"
              opacity="0.25"
            />
            {/* Clara voice arcs inside shield */}
            <path d="M42 36 A10 10 0 0 1 42 52" stroke="var(--color-clara-blue)" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
            <path d="M42 40 A6 6 0 0 1 42 48" stroke="var(--color-clara-blue)" strokeWidth="2" strokeLinecap="round" opacity="0.7" />
            <circle cx="42" cy="44" r="2.5" fill="#D46A1E" />
            {/* Checkmark */}
            <path d="M52 40 l4 4 8-8" stroke="#2E7D4F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.5" />
          </svg>
        </div>

        <p
          className="text-clara-text-secondary leading-relaxed"
          style={{
            fontSize: "clamp(16px, 2.5vw, 19px)",
            maxWidth: "48ch",
            opacity: hero.visible ? 1 : 0,
            transform: hero.visible ? "translateY(0)" : "translateY(16px)",
            transition: "opacity 0.7s ease-out 0.15s, transform 0.7s ease-out 0.15s",
          }}
        >
          {t.intro}
        </p>

        <p
          className="text-clara-text-secondary/60"
          style={{
            fontSize: "13px",
            fontStyle: "italic",
            opacity: hero.visible ? 1 : 0,
            transition: "opacity 0.7s ease-out 0.25s",
          }}
        >
          {t.last_updated}
        </p>

        {/* Orange divider accent (like FuturoPage vision section) */}
        <div
          aria-hidden="true"
          style={{
            width: "48px",
            height: "2px",
            background: "#D46A1E",
            opacity: hero.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.3s",
          }}
        />
      </div>

      {/* ══ 7 Legal sections ══ */}
      <div className="flex flex-col gap-4">
        {t.sections.map((section, i) => (
          <LegalSection key={section.icon} section={section} index={i} />
        ))}
      </div>
    </div>
  );
}

export default function InfoLegalPage() {
  return (
    <SubPageLayout slug="info-legal">
      {(lang) => <InfoLegalContent lang={lang} />}
    </SubPageLayout>
  );
}
