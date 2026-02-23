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

  const t = SUCCESS_SECTION[lang];

  return (
    <section
      ref={sectionRef}
      className="section-viewport"
      style={{ background: "var(--color-clara-surface-1)" }}
      aria-labelledby="success-quote"
    >
      {/* ── Floating voice arcs (consistent with Guide/Personas sections) ── */}
      <svg
        aria-hidden="true"
        style={{
          position: "absolute",
          top: "5%",
          right: "-6%",
          width: "clamp(200px, 30vw, 400px)",
          height: "clamp(200px, 30vw, 400px)",
          opacity: 0.06,
          animation: visible ? "float 12s ease-in-out infinite" : "none",
          pointerEvents: "none",
        }}
        viewBox="0 0 200 200"
        fill="none"
      >
        <circle cx="100" cy="100" r="90" stroke="#1B5E7B" strokeWidth="1" />
        <circle cx="100" cy="100" r="65" stroke="#1B5E7B" strokeWidth="0.8" />
        <circle cx="100" cy="100" r="40" stroke="#2E7D4F" strokeWidth="0.6" />
      </svg>
      <svg
        aria-hidden="true"
        style={{
          position: "absolute",
          bottom: "8%",
          left: "-4%",
          width: "clamp(160px, 22vw, 300px)",
          height: "clamp(160px, 22vw, 300px)",
          opacity: 0.04,
          animation: visible ? "float 9s ease-in-out 2s infinite" : "none",
          pointerEvents: "none",
        }}
        viewBox="0 0 200 200"
        fill="none"
      >
        <circle cx="100" cy="100" r="80" stroke="#D46A1E" strokeWidth="0.8" />
        <circle cx="100" cy="100" r="55" stroke="#D46A1E" strokeWidth="0.6" />
      </svg>

      <div className="relative w-full max-w-5xl mx-auto flex flex-col items-center gap-12 px-6">

        {/* ── Before / After cards — matches Personas border-l pattern ── */}
        <div className="w-full success-grid" style={{ display: "grid", gridTemplateColumns: "1fr", gap: "clamp(16px, 3vw, 24px)" }}>

          {/* BEFORE card */}
          <div
            className={visible ? "split-before" : ""}
            style={{
              opacity: visible ? undefined : 0,
              position: "relative",
              background: "var(--color-clara-card)",
              borderRadius: "20px",
              borderLeft: "4px solid #D46A1E",
              padding: "clamp(24px, 4vw, 36px) clamp(24px, 4vw, 32px)",
              boxShadow: "0 2px 16px rgba(0,0,0,0.04), 0 0 0 1px rgba(var(--clara-blue-rgb),0.04)",
            }}
            aria-label="Before Clara"
          >
            {/* Oversized decorative × (like Personas' 120px quote marks) */}
            <span
              aria-hidden="true"
              className="font-display"
              style={{
                position: "absolute",
                top: "8px",
                right: "16px",
                fontSize: "clamp(80px, 12vw, 120px)",
                fontWeight: 800,
                lineHeight: 1,
                color: "rgba(var(--clara-orange-rgb),0.07)",
                pointerEvents: "none",
                userSelect: "none",
              }}
            >
              &#215;
            </span>

            <div className="relative">
              <span
                className="font-display"
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  fontSize: "11px",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                  color: "#D46A1E",
                  marginBottom: "12px",
                }}
              >
                Antes
              </span>
              <p
                className="font-display"
                style={{
                  fontSize: "clamp(18px, 3vw, 24px)",
                  fontWeight: 600,
                  lineHeight: 1.45,
                  color: "var(--color-clara-text)",
                  margin: 0,
                }}
              >
                {t.transformation_from}
              </p>
            </div>
          </div>

          {/* AFTER card */}
          <div
            className={visible ? "split-after" : ""}
            style={{
              opacity: visible ? undefined : 0,
              position: "relative",
              background: "var(--color-clara-card)",
              borderRadius: "20px",
              borderLeft: "4px solid #2E7D4F",
              padding: "clamp(24px, 4vw, 36px) clamp(24px, 4vw, 32px)",
              boxShadow: "0 2px 16px rgba(0,0,0,0.04), 0 0 0 1px rgba(var(--clara-blue-rgb),0.04)",
            }}
            aria-label="After Clara"
          >
            {/* Oversized decorative arrow */}
            <span
              aria-hidden="true"
              className="font-display"
              style={{
                position: "absolute",
                top: "8px",
                right: "16px",
                fontSize: "clamp(80px, 12vw, 120px)",
                fontWeight: 800,
                lineHeight: 1,
                color: "rgba(var(--clara-green-rgb),0.07)",
                pointerEvents: "none",
                userSelect: "none",
              }}
            >
              &#10132;
            </span>

            <div className="relative">
              <span
                className="font-display"
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  fontSize: "11px",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                  color: "#2E7D4F",
                  marginBottom: "12px",
                }}
              >
                Con Clara
              </span>
              <p
                className="font-display"
                style={{
                  fontSize: "clamp(18px, 3vw, 24px)",
                  fontWeight: 600,
                  lineHeight: 1.45,
                  color: "var(--color-clara-text)",
                  margin: 0,
                }}
              >
                {t.transformation_to}
              </p>
            </div>
          </div>
        </div>

        {/* ── Orange divider accent (like GuideSection) ── */}
        <div
          aria-hidden="true"
          style={{
            width: "48px",
            height: "2px",
            background: "#D46A1E",
            opacity: visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.5s",
          }}
        />

        {/* ── Quote — emotional centerpiece with decorative marks ── */}
        <div
          style={{
            position: "relative",
            maxWidth: "720px",
            width: "100%",
          }}
        >
          {/* Large decorative open-quote (120px like Personas) */}
          <span
            aria-hidden="true"
            className="font-display"
            style={{
              position: "absolute",
              top: "clamp(-20px, -3vw, -32px)",
              left: "clamp(-8px, -1.5vw, -16px)",
              fontSize: "clamp(100px, 16vw, 160px)",
              fontWeight: 800,
              lineHeight: 1,
              color: "rgba(var(--clara-blue-rgb),0.08)",
              pointerEvents: "none",
              userSelect: "none",
            }}
          >
            &ldquo;
          </span>

          <blockquote
            id="success-quote"
            className={`epiphany-quote font-display font-bold text-center leading-tight${visible ? " revealed" : ""}`}
            style={{
              position: "relative",
              color: "var(--color-clara-text)",
            }}
          >
            {t.quote}
          </blockquote>
        </div>

        {/* ── Tagline ── */}
        <p
          className="font-display font-bold text-center leading-tight"
          style={{
            fontSize: "clamp(36px, 7vw, 56px)",
            animation: visible ? "float 5s ease-in-out infinite" : "none",
            opacity: visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.9s",
          }}
          aria-label={`${t.tagline[0]} ${t.tagline[1]}`}
        >
          <span style={{ color: "var(--color-clara-blue)" }}>{t.tagline[0]} </span>
          <span style={{ color: "var(--color-clara-orange)" }}>{t.tagline[1]}</span>
        </p>
      </div>
    </section>
  );
}
