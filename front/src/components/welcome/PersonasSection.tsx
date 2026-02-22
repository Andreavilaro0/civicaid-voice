import { useEffect, useRef, useState, useCallback } from "react";
import type { Language } from "@/lib/types";
import { PERSONAS } from "@/lib/i18n";
import { cdn } from "@/lib/constants";

interface PersonasSectionProps {
  lang: Language;
}

/* ------------------------------------------------------------------ */
/*  useTypewriter — animates a string character by character           */
/*  Instantly completes if prefers-reduced-motion is active            */
/* ------------------------------------------------------------------ */
function useTypewriter(text: string, active: boolean, intervalMs = 40) {
  const [displayed, setDisplayed] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!active) return;

    // Respect reduced-motion preference: show full text immediately
    const reducedMotion =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reducedMotion) {
      setDisplayed(text.length);
      setDone(true);
      return;
    }

    // Reset state when text or active changes
    setDisplayed(0);
    setDone(false);

    const id = setInterval(() => {
      setDisplayed((prev) => {
        const next = prev + 1;
        if (next >= text.length) {
          clearInterval(id);
          setDone(true);
          return text.length;
        }
        return next;
      });
    }, intervalMs);

    return () => clearInterval(id);
  }, [text, active, intervalMs]);

  return { displayed, done };
}

/* ------------------------------------------------------------------ */
/*  TypewriterQuote — renders quote text with typewriter animation     */
/* ------------------------------------------------------------------ */
function TypewriterQuote({
  text,
  active,
}: {
  text: string;
  active: boolean;
}) {
  const { displayed, done } = useTypewriter(text, active, 40);
  const visibleText = text.slice(0, displayed);

  return (
    <p
      className="italic leading-snug text-clara-text-secondary dark:text-[#a0a0b0] text-[20px] md:text-[24px]"
      aria-label={text}
      style={{ fontSize: "clamp(20px, 2.5vw, 28px)", lineHeight: 1.5 }}
    >
      {visibleText}
      {!done && (
        <span className="typewriter-cursor" aria-hidden="true" />
      )}
    </p>
  );
}

/* ------------------------------------------------------------------ */
/*  TiltCard — 3D hover tilt, 12° range, persona-card-reveal entrance */
/* ------------------------------------------------------------------ */
function TiltCard({
  children,
  className = "",
  revealDelay = 0,
  visible = false,
}: {
  children: React.ReactNode;
  className?: string;
  revealDelay?: number;
  visible?: boolean;
}) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [hovering, setHovering] = useState(false);

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      const card = cardRef.current;
      if (!card) return;
      const rect = card.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const rotateX = ((e.clientY - centerY) / (rect.height / 2)) * -12;
      const rotateY = ((e.clientX - centerX) / (rect.width / 2)) * 12;
      setTilt({ x: rotateX, y: rotateY });
    },
    []
  );

  const handleMouseLeave = useCallback(() => {
    setTilt({ x: 0, y: 0 });
    setHovering(false);
  }, []);

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setHovering(true)}
      onMouseLeave={handleMouseLeave}
      // persona-card-reveal drives the CSS entrance animation
      className={`persona-card-reveal ${className}`}
      style={{
        perspective: "800px",
        // Only play the entrance animation once the section is visible
        animationPlayState: visible ? "running" : "paused",
        animationDelay: `${revealDelay}s`,
      }}
    >
      <div
        style={{
          transform: `rotateX(${tilt.x}deg) rotateY(${tilt.y}deg) scale(${
            hovering ? 1.02 : 1
          })`,
          transition: hovering
            ? "transform 0.1s ease-out"
            : "transform 0.4s ease-out",
          transformStyle: "preserve-3d",
          boxShadow: hovering
            ? `${tilt.y * -1.5}px ${tilt.x * 1.5}px 40px rgba(27,94,123,0.18), 0 0 24px rgba(27,94,123,0.10)`
            : "0 4px 24px rgba(27,94,123,0.06)",
          borderRadius: "20px",
        }}
      >
        {children}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  FloatingArcs — 3 decorative SVG voice arcs with arcDrift CSS anim */
/* ------------------------------------------------------------------ */
function FloatingArcs() {
  return (
    <>
      {/* Arc 1 — upper-left, large, blue tones */}
      <svg
        className="floating-arc"
        style={{
          top: "5%",
          left: "-60px",
          width: 220,
          height: 220,
          animationDelay: "0s",
          animationDuration: "9s",
        }}
        viewBox="0 0 220 220"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M 20 110 A 90 90 0 0 1 200 110"
          stroke="rgba(27,94,123,0.18)"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M 40 110 A 70 70 0 0 1 180 110"
          stroke="rgba(27,94,123,0.12)"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
        <path
          d="M 60 110 A 50 50 0 0 1 160 110"
          stroke="rgba(27,94,123,0.08)"
          strokeWidth="1"
          strokeLinecap="round"
        />
      </svg>

      {/* Arc 2 — lower-right, medium, orange tones */}
      <svg
        className="floating-arc"
        style={{
          bottom: "8%",
          right: "-40px",
          width: 180,
          height: 180,
          animationDelay: "3s",
          animationDuration: "11s",
        }}
        viewBox="0 0 180 180"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M 90 160 A 75 75 0 0 0 90 20"
          stroke="rgba(212,106,30,0.14)"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M 90 140 A 55 55 0 0 0 90 40"
          stroke="rgba(212,106,30,0.09)"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      </svg>

      {/* Arc 3 — mid-right, small, green accent */}
      <svg
        className="floating-arc"
        style={{
          top: "40%",
          right: "4%",
          width: 120,
          height: 120,
          animationDelay: "6s",
          animationDuration: "7s",
        }}
        viewBox="0 0 120 120"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M 10 60 A 50 50 0 0 1 110 60"
          stroke="rgba(46,125,79,0.15)"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M 24 60 A 36 36 0 0 1 96 60"
          stroke="rgba(46,125,79,0.09)"
          strokeWidth="1"
          strokeLinecap="round"
        />
      </svg>
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  Accent color tokens per persona                                    */
/* ------------------------------------------------------------------ */
const accentColors: Record<
  string,
  { border: string; glow: string; ring: string; quoteColor: string }
> = {
  maria: {
    border: "border-l-clara-orange",
    glow: "rgba(212,106,30,0.10)",
    ring: "rgba(212,106,30,0.2)",
    quoteColor: "rgba(212,106,30,0.15)",
  },
  ahmed: {
    border: "border-l-clara-blue",
    glow: "rgba(27,94,123,0.10)",
    ring: "rgba(27,94,123,0.2)",
    quoteColor: "rgba(27,94,123,0.15)",
  },
  fatima: {
    border: "border-l-clara-green",
    glow: "rgba(46,125,79,0.10)",
    ring: "rgba(46,125,79,0.2)",
    quoteColor: "rgba(46,125,79,0.15)",
  },
};

/* ------------------------------------------------------------------ */
/*  Section title strings                                              */
/* ------------------------------------------------------------------ */
const SECTION_TITLES: Record<Language, string> = {
  es: "Historias reales",
  en: "Real stories",
  fr: "Histoires reelles",
  pt: "Histórias reais",
  ro: "Povești reale",
  ca: "Històries reals",
  zh: "真实故事",
  ar: "قصص حقيقية",
};

/* ------------------------------------------------------------------ */
/*  PersonasSection — FASE 2 "Las Voces" cinematic cards              */
/* ------------------------------------------------------------------ */
export default function PersonasSection({ lang }: PersonasSectionProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  // Trigger reveal once section enters viewport
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

  return (
    <section
      ref={sectionRef}
      className="relative w-full py-20 px-6 bg-[#FAFAFA] dark:bg-[#0f1419] overflow-hidden section-bleed-dark-to-light"
      aria-label={SECTION_TITLES[lang]}
    >
      {/* Floating decorative voice arcs */}
      <FloatingArcs />

      <div className="max-w-3xl mx-auto flex flex-col gap-8 relative z-10">
        {/* Section label */}
        <p
          className="text-center text-body-sm text-clara-text-secondary font-display font-medium uppercase tracking-widest mb-2"
          style={{
            opacity: visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
            letterSpacing: "0.15em",
          }}
        >
          {SECTION_TITLES[lang]}
        </p>

        {PERSONAS.map((persona, i) => {
          const colors = accentColors[persona.id] ?? accentColors.ahmed;
          const quoteText = persona.quote[lang];
          // 0.1s stagger between cards
          const revealDelay = 0.1 + i * 0.1;

          return (
            <TiltCard
              key={persona.id}
              revealDelay={revealDelay}
              visible={visible}
            >
              <div
                className={`persona-chip border-l-4 ${colors.border}`}
                style={{
                  background: `linear-gradient(135deg, white 0%, ${colors.glow} 100%)`,
                  padding: "24px 28px",
                  borderRadius: "20px",
                  position: "relative",
                  overflow: "hidden",
                  alignItems: "flex-start",
                }}
              >
                {/* Oversized decorative quote mark — sits behind content */}
                <span
                  className="oversized-quote"
                  aria-hidden="true"
                  style={{
                    color: colors.quoteColor,
                    // Override the global .oversized-quote opacity:0.08
                    // to use the per-persona 15% opacity color directly
                    opacity: 1,
                    fontSize: "120px",
                    top: "-12px",
                    zIndex: 0,
                  }}
                >
                  &ldquo;
                </span>

                {/* Avatar with ambient glow ring */}
                <div
                  className="relative flex-shrink-0"
                  style={{ transform: "translateZ(20px)", zIndex: 1 }}
                >
                  <div
                    className="absolute -inset-1 rounded-2xl"
                    style={{ background: colors.ring, filter: "blur(6px)" }}
                    aria-hidden="true"
                  />
                  <img
                    src={cdn(`/media/personas/${persona.id}.png`)}
                    alt={persona.name}
                    width={96}
                    height={96}
                    className="relative w-[96px] h-[96px] rounded-2xl object-cover shadow-lg"
                    loading="lazy"
                  />
                </div>

                {/* Name + animated quote */}
                <div
                  className="flex-1 min-w-0"
                  style={{ transform: "translateZ(10px)", zIndex: 1 }}
                >
                  <p className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee] mb-2">
                    {persona.name}
                  </p>
                  <TypewriterQuote text={quoteText} active={visible} />
                </div>
              </div>
            </TiltCard>
          );
        })}
      </div>
    </section>
  );
}
