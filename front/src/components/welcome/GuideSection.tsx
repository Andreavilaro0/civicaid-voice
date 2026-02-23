import { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { GUIDE_SECTION, STATS } from "@/lib/i18n";

interface GuideSectionProps {
  lang: Language;
}

// Stat progress percentages — visual fill fraction per stat (0–1)
const STAT_FILL: number[] = [1, 0.6, 0.8, 0.95];

// SVG circle constants: r=45, circumference = 2*PI*45 ≈ 283
const CIRCUMFERENCE = 283;

interface StatRingProps {
  value: string;
  label: string;
  fill: number;
  visible: boolean;
  delay: number;
}

function StatRing({ value, label, fill, visible, delay }: StatRingProps) {
  const ringRef = useRef<SVGCircleElement>(null);

  // Compute stroke color based on index position via fill fraction
  const strokeColor = fill >= 0.85 ? "var(--color-clara-green)" : "var(--color-clara-blue)";

  return (
    <div className="flex flex-col items-center gap-2">
      {/* SVG ring container — 100x100 viewBox */}
      <div className="relative" style={{ width: 120, height: 120 }}>
        <svg
          viewBox="0 0 100 100"
          width="120"
          height="120"
          aria-hidden="true"
          className={`stat-ring${visible ? " revealed" : ""}`}
          style={{ overflow: "visible" }}
        >
          {/* Background track circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="4"
            className="text-clara-blue/10"
            style={{ color: "rgba(var(--clara-blue-rgb),0.1)" }}
          />
          {/* Progress circle — animated by .stat-ring.revealed via CSS ringDraw */}
          <circle
            ref={ringRef}
            cx="50"
            cy="50"
            r="45"
            className="ring-progress"
            stroke={strokeColor}
            strokeWidth="4"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={
              visible ? CIRCUMFERENCE - fill * CIRCUMFERENCE : CIRCUMFERENCE
            }
            transform="rotate(-90 50 50)"
            style={{
              transition: visible
                ? `stroke-dashoffset 1.2s cubic-bezier(0.22, 1, 0.36, 1) ${delay}ms`
                : "none",
            }}
          />
        </svg>

        {/* Stat value centered inside the ring */}
        <div
          className="absolute inset-0 flex items-center justify-center"
          style={{
            opacity: visible ? 1 : 0,
            transition: `opacity 0.5s ease-out ${delay + 200}ms`,
          }}
        >
          <span
            className="font-display font-bold text-clara-blue leading-none"
            style={{ fontSize: 28 }}
            aria-label={value}
          >
            {value}
          </span>
        </div>
      </div>

      {/* Label below ring */}
      <span
        className="uppercase tracking-widest text-clara-text-secondary text-center"
        style={{
          fontSize: 14,
          opacity: visible ? 1 : 0,
          transform: visible ? "translateY(0)" : "translateY(8px)",
          transition: `opacity 0.5s ease-out ${delay + 300}ms, transform 0.5s ease-out ${delay + 300}ms`,
        }}
      >
        {label}
      </span>
    </div>
  );
}

export default function GuideSection({ lang }: GuideSectionProps) {
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

  const t = GUIDE_SECTION[lang];
  const stats = STATS[lang];

  return (
    <section
      ref={sectionRef}
      className="relative w-full py-20 px-6 bg-clara-surface-1 overflow-hidden"
      aria-labelledby="guide-title"
    >
      {/* Watermark — giant Clara voice arcs SVG, 5% opacity, slowly rotating */}
      <div
        aria-hidden="true"
        className="pointer-events-none select-none absolute inset-0 flex items-center justify-center"
        style={{
          opacity: 0.05,
          animation: "float 12s ease-in-out infinite",
          zIndex: 0,
        }}
      >
        <svg
          width="600"
          height="600"
          viewBox="0 0 200 200"
          fill="none"
          style={{ transform: "rotate(0deg)" }}
        >
          {/* Concentric voice arc rings — Clara's sonic identity */}
          <circle cx="100" cy="100" r="20" stroke="currentColor" strokeWidth="1.5" className="text-clara-blue" />
          <circle cx="100" cy="100" r="40" stroke="currentColor" strokeWidth="1.2" className="text-clara-blue" />
          <circle cx="100" cy="100" r="60" stroke="currentColor" strokeWidth="1" className="text-clara-blue" />
          <circle cx="100" cy="100" r="80" stroke="currentColor" strokeWidth="0.8" className="text-clara-blue" />
          <circle cx="100" cy="100" r="95" stroke="currentColor" strokeWidth="0.6" className="text-clara-blue" />
          {/* Arc slices suggesting sound wave directionality */}
          <path
            d="M 100 100 m -12 0 a 12 12 0 1 1 24 0"
            stroke="currentColor"
            strokeWidth="2"
            fill="none"
            className="text-clara-orange"
          />
          <circle cx="100" cy="100" r="4" fill="currentColor" className="text-clara-orange" />
        </svg>
      </div>

      {/* Radial glow behind content */}
      <div
        aria-hidden="true"
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] pointer-events-none"
        style={{
          background:
            "radial-gradient(circle, rgba(var(--clara-blue-rgb),0.07) 0%, transparent 65%)",
          zIndex: 0,
        }}
      />

      {/* Decorative voice arcs — Clara's sonic identity */}
      <div className="voice-arc-decorative" aria-hidden="true" style={{ top: "10%", right: "-60px", animationDelay: "0s" }}>
        <svg width="120" height="120" viewBox="0 0 80 80" fill="none" style={{ opacity: 0.6 }}>
          <path d="M 50 15 A 28 28 0 0 1 50 65" stroke="var(--color-clara-blue)" strokeWidth="1.5" strokeLinecap="round" opacity="0.2" />
          <path d="M 44 24 A 18 18 0 0 1 44 56" stroke="var(--color-clara-blue)" strokeWidth="1.5" strokeLinecap="round" opacity="0.35" />
          <path d="M 38 33 A 8 8 0 0 1 38 47" stroke="var(--color-clara-blue)" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
          <circle cx="34" cy="40" r="2.5" fill="var(--color-clara-orange)" opacity="0.6" />
        </svg>
      </div>
      <div className="voice-arc-decorative" aria-hidden="true" style={{ bottom: "15%", left: "-40px", animationDelay: "3s" }}>
        <svg width="100" height="100" viewBox="0 0 80 80" fill="none" style={{ opacity: 0.4, transform: "scaleX(-1)" }}>
          <path d="M 50 20 A 22 22 0 0 1 50 60" stroke="var(--color-clara-green)" strokeWidth="1.5" strokeLinecap="round" opacity="0.25" />
          <path d="M 44 28 A 14 14 0 0 1 44 52" stroke="var(--color-clara-green)" strokeWidth="1.5" strokeLinecap="round" opacity="0.4" />
          <circle cx="38" cy="40" r="2.5" fill="var(--color-clara-orange)" opacity="0.5" />
        </svg>
      </div>

      {/* Main content — constrained width, relative to sit above watermark */}
      <div className="relative max-w-5xl mx-auto" style={{ zIndex: 1 }}>
        {/* ── Split-screen layout ── */}
        <div className="flex flex-col md:flex-row md:items-center md:gap-16">

          {/* Left column — Clara name + empathy quote */}
          <div
            className="md:w-1/2 flex flex-col gap-6 mb-12 md:mb-0"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? "translateX(0)" : "translateX(-32px)",
              transition:
                "opacity 0.8s cubic-bezier(0.22, 1, 0.36, 1), transform 0.8s cubic-bezier(0.22, 1, 0.36, 1)",
            }}
          >
            {/* "Clara" — gigantic gradient display name */}
            <h2
              id="guide-title"
              className="font-display font-bold text-gradient-warm leading-none tracking-tight"
              style={{
                fontSize: "clamp(64px, 10vw, 120px)",
                letterSpacing: "-0.03em",
              }}
            >
              Clara
            </h2>

            {/* Clara 3D — interactive Spline scene */}
            <div
              className="relative mx-auto md:mx-0"
              style={{
                width: "clamp(200px, 28vw, 320px)",
                height: "clamp(200px, 28vw, 320px)",
                borderRadius: "24px",
                overflow: "hidden",
                opacity: visible ? 1 : 0,
                transform: visible ? "scale(1)" : "scale(0.9)",
                transition: "opacity 0.8s ease-out 0.3s, transform 0.8s cubic-bezier(0.22,1,0.36,1) 0.3s",
              }}
            >
              <spline-viewer
                url="https://prod.spline.design/MZxWfrLie5x-h-U9/scene.splinecode"
                background="rgba(0,0,0,0)"
                loading="lazy"
                style={{
                  width: "100%",
                  height: "100%",
                  display: "block",
                }}
              />
            </div>

            {/* Empathy quote — italic, muted */}
            <p
              className="italic text-clara-text-secondary leading-relaxed"
              style={{ fontSize: "clamp(16px, 2vw, 20px)", maxWidth: "42ch" }}
            >
              &ldquo;{t.empathy}&rdquo;
            </p>

            {/* Thin orange divider accent */}
            <div
              className="h-[2px] w-12 rounded-full"
              style={{ background: "var(--color-clara-orange)" }}
              aria-hidden="true"
            />
          </div>

          {/* Right column — 2×2 stat ring grid */}
          <div className="md:w-1/2">
            <div className="grid grid-cols-2 gap-x-8 gap-y-10 place-items-center">
              {stats.map((stat, i) => (
                <StatRing
                  key={i}
                  value={stat.value}
                  label={stat.label}
                  fill={STAT_FILL[i] ?? 0.75}
                  visible={visible}
                  delay={300 + i * 120}
                />
              ))}
            </div>
          </div>
        </div>

        {/* ── Authority text — centered below the split ── */}
        <div
          className="mt-16 text-center"
          style={{
            opacity: visible ? 1 : 0,
            transform: visible ? "translateY(0)" : "translateY(20px)",
            transition:
              "opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.6s, transform 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.6s",
          }}
        >
          {/* Subtle top separator */}
          <div
            aria-hidden="true"
            className="mx-auto mb-8 h-px w-24 rounded-full"
            style={{ background: "rgba(var(--clara-blue-rgb),0.15)" }}
          />

          <p
            className="text-clara-text leading-relaxed mx-auto"
            style={{
              fontSize: "clamp(16px, 2vw, 20px)",
              maxWidth: "52ch",
              animation: visible
                ? "fadeInUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.6s both"
                : "none",
            }}
          >
            {t.authority}
          </p>
        </div>
      </div>
    </section>
  );
}
