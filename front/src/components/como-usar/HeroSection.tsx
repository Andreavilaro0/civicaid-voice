import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { COMO_USAR_PAGE, COMO_USAR_EXTRA } from "@/lib/i18n";
import { useInView } from "@/hooks/useInView";
import { useTheme } from "@/contexts/ThemeContext";

interface HeroSectionProps {
  lang: Language;
}

export default function HeroSection({ lang }: HeroSectionProps) {
  const navigate = useNavigate();
  const t = COMO_USAR_PAGE[lang];
  const tx = COMO_USAR_EXTRA[lang];
  const { visible, ref } = useInView(0.2);
  const { resolved } = useTheme();
  const isDark = resolved === "dark";

  return (
    <section
      ref={ref}
      className="relative flex flex-col items-center justify-center text-center px-6 py-16 md:py-24 overflow-hidden"
      style={{
        background: isDark
          ? "linear-gradient(180deg, #1A1A2E 0%, #1E2240 40%, #1A2545 100%)"
          : "linear-gradient(180deg, #FAFAFA 0%, #E8F5F1 40%, #DCF0EC 100%)",
        minHeight: "70vh",
      }}
    >
      {/* Decorative dots */}
      <div
        className="dot-pulse absolute"
        style={{ top: "15%", left: "10%", width: 8, height: 8, borderRadius: "50%", background: "rgba(var(--clara-blue-rgb),0.2)" }}
        aria-hidden="true"
      />
      <div
        className="dot-pulse absolute"
        style={{ top: "25%", right: "12%", width: 6, height: 6, borderRadius: "50%", background: "rgba(var(--clara-orange-rgb),0.2)", animationDelay: "1s" }}
        aria-hidden="true"
      />
      <div
        className="dot-pulse absolute"
        style={{ bottom: "20%", left: "20%", width: 10, height: 10, borderRadius: "50%", background: "rgba(var(--clara-green-rgb),0.15)", animationDelay: "1.5s" }}
        aria-hidden="true"
      />

      {/* Day/night decorative arcs */}
      <div
        aria-hidden="true"
        style={{
          opacity: visible ? 1 : 0,
          transform: visible ? "scale(1)" : "scale(0.7)",
          transition: "opacity 0.9s ease-out, transform 0.9s cubic-bezier(0.22,1,0.36,1)",
        }}
      >
        <svg width="120" height="60" viewBox="0 0 120 60" fill="none">
          <path
            d="M 40 30 A 20 20 0 0 1 80 30"
            stroke={isDark ? "rgba(107,191,224,0.3)" : "rgba(45,106,90,0.25)"}
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M 48 30 A 12 12 0 0 1 72 30"
            stroke={isDark ? "rgba(107,191,224,0.5)" : "rgba(45,106,90,0.4)"}
            strokeWidth="2"
            strokeLinecap="round"
          />
          <circle cx="60" cy="32" r="3" fill={isDark ? "#6BBFE0" : "#2D6A5A"} opacity="0.7" />
          {isDark && (
            <>
              <circle cx="30" cy="15" r="1" fill="rgba(255,255,255,0.3)" />
              <circle cx="90" cy="10" r="1.5" fill="rgba(255,255,255,0.2)" />
              <circle cx="100" cy="40" r="1" fill="rgba(255,255,255,0.25)" />
            </>
          )}
        </svg>
      </div>

      {/* Headline */}
      <h2
        className="font-display font-bold text-clara-text leading-tight mt-4"
        style={{
          fontSize: "clamp(28px, 6vw, 42px)",
          letterSpacing: "-0.02em",
          maxWidth: "20ch",
          opacity: visible ? 1 : 0,
          transform: visible ? "translateY(0)" : "translateY(20px)",
          transition: "opacity 0.7s ease-out 0.15s, transform 0.7s ease-out 0.15s",
        }}
      >
        {t.empathy_headline}
      </h2>

      {/* Subtitle */}
      <p
        className="text-clara-text-secondary leading-relaxed mt-3"
        style={{
          fontSize: "clamp(16px, 2.5vw, 20px)",
          maxWidth: "44ch",
          opacity: visible ? 1 : 0,
          transition: "opacity 0.7s ease-out 0.3s",
        }}
      >
        {t.empathy_sub}
      </p>

      {/* Stat badge */}
      <div
        className="flex items-center gap-2 mt-5 px-4 py-2 rounded-full"
        style={{
          background: "rgba(var(--clara-blue-rgb),0.06)",
          border: "1px solid rgba(var(--clara-blue-rgb),0.10)",
          fontSize: "clamp(13px, 1.8vw, 15px)",
          opacity: visible ? 1 : 0,
          transform: visible ? "translateY(0)" : "translateY(8px)",
          transition: "opacity 0.6s ease-out 0.4s, transform 0.6s ease-out 0.4s",
        }}
      >
        <span
          style={{ width: 8, height: 8, borderRadius: "50%", background: "var(--color-clara-blue)", flexShrink: 0 }}
          aria-hidden="true"
        />
        <span className="text-clara-text-secondary font-medium">
          {tx.hero_stat}
        </span>
      </div>

      {/* Dual CTAs */}
      <div
        className="flex flex-wrap items-center justify-center gap-4 mt-8"
        style={{
          opacity: visible ? 1 : 0,
          transform: visible ? "translateY(0)" : "translateY(12px)",
          transition: "opacity 0.6s ease-out 0.45s, transform 0.6s ease-out 0.45s",
        }}
      >
        <button
          onClick={() => navigate(`/chat?lang=${lang}`)}
          className="brand-gradient btn-magnetic font-display font-bold text-white rounded-full
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          style={{
            padding: "14px 32px",
            fontSize: 18,
            boxShadow: "0 4px 20px rgba(var(--clara-blue-rgb),0.3)",
            minHeight: 52,
          }}
        >
          {tx.hero_talk_button}
        </button>
        <button
          onClick={() => {
            document.getElementById("bento-grid")?.scrollIntoView({ behavior: "smooth" });
          }}
          className="btn-magnetic font-display font-bold text-clara-blue rounded-full
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          style={{
            padding: "14px 32px",
            fontSize: 18,
            border: "2px solid rgba(var(--clara-blue-rgb),0.2)",
            background: "rgba(var(--clara-blue-rgb),0.04)",
            minHeight: 52,
          }}
        >
          {tx.hero_guide_button}
        </button>
      </div>
    </section>
  );
}
