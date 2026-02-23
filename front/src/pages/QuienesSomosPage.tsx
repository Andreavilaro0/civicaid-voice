import { useEffect, useRef, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";
import { QUIENES_SOMOS_STORY, STATS } from "@/lib/i18n";

/* ─── Scroll-reveal hooks ─── */

/** Generic reveal — triggers class swap on intersection */
function useRevealClass() {
  const ref = useRef<HTMLDivElement>(null);
  const [revealed, setRevealed] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) { setRevealed(true); obs.disconnect(); } },
      { threshold: 0.15 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  return { ref, revealed };
}

/** Classic translateY reveal with configurable delay */
function useReveal(delay = 0) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) { setVisible(true); obs.disconnect(); } },
      { threshold: 0.15 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  const style: React.CSSProperties = {
    opacity: visible ? 1 : 0,
    transform: visible ? "translateY(0)" : "translateY(28px)",
    transition: `opacity 0.8s cubic-bezier(0.22,1,0.36,1) ${delay}s, transform 0.8s cubic-bezier(0.22,1,0.36,1) ${delay}s`,
  };
  return { ref, style, visible };
}

/* ─── Reveal wrapper variants ─── */

function RevealUp({ children, className = "", delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  const { ref, style } = useReveal(delay);
  return <div ref={ref} style={style} className={className}>{children}</div>;
}

/** CSS-class based reveal for slide/scale variants */
function RevealCSS({ variant, children, className = "", delay = 0 }: {
  variant: "slide-left" | "slide-right" | "scale" | "up";
  children: React.ReactNode;
  className?: string;
  delay?: number;
}) {
  const { ref, revealed } = useRevealClass();
  return (
    <div
      ref={ref}
      className={`reveal-${variant} ${revealed ? "revealed" : ""} ${className}`}
      style={{ transitionDelay: `${delay}s` }}
    >
      {children}
    </div>
  );
}

/** Word-by-word stagger reveal for headlines */
function WordStagger({ text, className = "" }: { text: string; className?: string }) {
  const { ref, revealed } = useRevealClass();
  const words = text.split(" ");
  return (
    <span ref={ref} className={`word-stagger ${revealed ? "revealed" : ""} ${className}`}>
      {words.map((word, i) => (
        <span key={i} style={{ transitionDelay: `${i * 0.08}s` }}>
          {word}{i < words.length - 1 ? "\u00A0" : ""}
        </span>
      ))}
    </span>
  );
}

/** Typewriter — reveals text letter by letter on scroll with blinking cursor */
function Typewriter({ text, className = "", speed = 45 }: { text: string; className?: string; speed?: number }) {
  const { ref, revealed } = useRevealClass();
  const [displayed, setDisplayed] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!revealed) return;
    setDisplayed("");
    setDone(false);
    let i = 0;
    const iv = setInterval(() => {
      i++;
      setDisplayed(text.slice(0, i));
      if (i >= text.length) {
        clearInterval(iv);
        setDone(true);
      }
    }, speed);
    return () => clearInterval(iv);
  }, [revealed, text, speed]);

  return (
    <span ref={ref} className={className}>
      {revealed ? displayed : "\u00A0"}
      <span
        className={`typewriter-cursor ${done ? "typewriter-cursor--hidden" : ""}`}
        aria-hidden="true"
      />
    </span>
  );
}

/** Stat with pop animation */
function StatPop({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) {
  const { ref, revealed } = useRevealClass();
  return (
    <div ref={ref} className={`stat-pop ${revealed ? "revealed" : ""}`} style={{ animationDelay: `${delay}s` }}>
      {children}
    </div>
  );
}

/** Animated counter — counts from 0 to target on scroll with easeOutExpo */
function CountUp({ value, delay = 0 }: { value: string; delay?: number }) {
  const { ref, revealed } = useRevealClass();
  const [display, setDisplay] = useState(0);

  // Parse: prefix (e.g. "<", "+"), numeric part, suffix (e.g. "+", "s", "ث")
  const match = value.match(/^([^0-9]*)(\d+)(.*)$/);
  const prefix = match ? match[1] : "";
  const target = match ? parseInt(match[2], 10) : 0;
  const suffix = match ? match[3] : value;

  useEffect(() => {
    if (!revealed || target === 0) return;
    const duration = 1500;
    let start: number | null = null;
    let raf = 0;
    const timeout = setTimeout(() => {
      const step = (ts: number) => {
        if (!start) start = ts;
        const progress = Math.min((ts - start) / duration, 1);
        const eased = 1 - Math.pow(2, -10 * progress); // easeOutExpo
        setDisplay(Math.round(eased * target));
        if (progress < 1) raf = requestAnimationFrame(step);
      };
      raf = requestAnimationFrame(step);
    }, delay * 1000);
    return () => { clearTimeout(timeout); cancelAnimationFrame(raf); };
  }, [revealed, target, delay]);

  if (!match) return <>{value}</>;
  return (
    <span ref={ref as React.Ref<HTMLSpanElement>}>
      {prefix}{revealed ? display : 0}{suffix}
    </span>
  );
}

/* ─── Inline components ─── */

function SectionMarker({ n }: { n: string }) {
  return <span className="section-marker" aria-hidden="true">{n}</span>;
}

function Divider({ full }: { full?: boolean }) {
  const { ref, revealed } = useRevealClass();
  return (
    <hr
      ref={ref as React.Ref<HTMLHRElement>}
      className={`${full ? "divider-line--full" : "divider-line"} ${revealed ? "revealed" : ""}`}
    />
  );
}

/** Clara voice arcs — decorative SVG (white or blue) */
function ClaraArcs({ size = 120, white, className = "", pulse }: {
  size?: number;
  white?: boolean;
  className?: string;
  pulse?: boolean;
}) {
  const stroke = white ? "#ffffff" : "#1B5E7B";
  return (
    <svg
      className={`clara-arcs ${pulse ? "clara-arcs--pulse" : ""} ${className}`}
      width={size}
      height={size}
      viewBox="0 0 80 80"
      fill="none"
      aria-hidden="true"
    >
      <path className="arc-outer" d="M 28 14 A 30 30 0 0 1 28 66" stroke={stroke} strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.25" />
      <path className="arc-middle" d="M 28 23 A 20 20 0 0 1 28 57" stroke={stroke} strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.5" />
      <path className="arc-inner" d="M 28 32 A 10 10 0 0 1 28 48" stroke={stroke} strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.85" />
      <circle className="arc-dot" cx="28" cy="40" r="5.5" fill="#D46A1E" />
    </svg>
  );
}

export default function QuienesSomosPage() {
  const navigate = useNavigate();

  return (
    <SubPageLayout slug="quienes-somos" fullBleed>
      {(lang) => {
        const t = QUIENES_SOMOS_STORY[lang];

        function goToChat() {
          navigate(`/chat?lang=${lang}&mode=voice`);
        }

        return (
          <div className="flex flex-col">

            {/* ══════════ 01 EMPATIZAR — dark ══════════ */}
            <section className="section-viewport section-dark">
              <SectionMarker n="01" />

              {/* Decorative arcs — top right */}
              <div className="absolute top-16 opacity-15 pointer-events-none"
                   style={{ right: "5%", transform: "rotate(-15deg)" }}>
                <ClaraArcs size={180} white pulse className="clara-arcs--float" />
              </div>

              <div className="max-w-2xl mx-auto w-full text-center">
                <h2 className="font-display font-bold text-[48px] md:text-[72px] leading-[1.05] heading-tight mb-6">
                  <Typewriter text={t.empatizar.title} speed={40} />
                </h2>

                <RevealUp delay={0.3}>
                  <p className="text-[20px] md:text-[22px] leading-relaxed text-white/70 mb-8 max-w-xl mx-auto">
                    {t.empatizar.body}
                  </p>
                </RevealUp>

                <Divider />

                <RevealCSS variant="scale" delay={0.5}>
                  <p className="inline-block px-6 py-3 rounded-full bg-clara-orange/20 text-[18px] md:text-[20px] text-clara-orange font-bold mt-2">
                    {t.empatizar.stat}
                  </p>
                </RevealCSS>
              </div>
            </section>

            {/* ══════════ 02 VALIDAR — light ══════════ */}
            <section className="section-viewport bg-clara-card">
              <SectionMarker n="02" />

              <div className="max-w-2xl mx-auto w-full text-center">
                <RevealCSS variant="slide-left">
                  <h2 className="font-display font-bold text-[40px] md:text-[56px] leading-[1.08] heading-tight text-clara-text mb-5">
                    {t.validar.title}
                  </h2>
                </RevealCSS>

                <RevealUp delay={0.2}>
                  <p className="text-[20px] md:text-[22px] text-clara-text-secondary leading-relaxed mb-10 max-w-xl mx-auto">
                    {t.validar.body}
                  </p>
                </RevealUp>

                <Divider />

                {/* Dramatic closing — huge + orange + typewriter */}
                <p className="font-display font-bold text-[48px] md:text-[64px] leading-[1.05] heading-tight text-clara-orange mt-4">
                  <Typewriter text={t.validar.closing} speed={55} />
                </p>
              </div>
            </section>

            {/* ══════════ 03 EL MOMENTO — light alt ══════════ */}
            <section className="section-viewport bg-clara-surface-1">
              <SectionMarker n="03" />

              {/* Decorative arcs — bottom left */}
              <div className="absolute bottom-12 opacity-10 pointer-events-none"
                   style={{ left: "3%", transform: "rotate(20deg) scaleX(-1)" }}>
                <ClaraArcs size={140} className="clara-arcs--float" />
              </div>

              <div className="max-w-2xl mx-auto w-full">
                <RevealCSS variant="slide-right">
                  <h2 className="font-display font-bold text-[44px] md:text-[64px] leading-[1.05] heading-tight text-clara-blue mb-10 text-center">
                    {t.momento.title}
                  </h2>
                </RevealCSS>

                {t.momento.body.split("\n\n").map((paragraph, i) => {
                  const parts = t.momento.body.split("\n\n");
                  const isLast = i === parts.length - 1;
                  return (
                    <RevealCSS
                      key={i}
                      variant={i % 2 === 0 ? "slide-left" : "slide-right"}
                      delay={0.15 + i * 0.12}
                    >
                      <p
                        className={`text-[20px] md:text-[22px] leading-relaxed mb-6 last:mb-0 ${
                          isLast
                            ? "font-bold text-clara-orange text-center text-[24px] md:text-[28px]"
                            : "text-clara-text-secondary"
                        }`}
                      >
                        {paragraph}
                      </p>
                    </RevealCSS>
                  );
                })}
              </div>
            </section>

            {/* ══════════ STATS — full viewport, Mastercard-style counters ══════════ */}
            <section className="section-viewport section-dark">
              <div className="max-w-5xl mx-auto w-full grid grid-cols-2 md:grid-cols-4 gap-y-12 md:gap-y-0">
                {STATS[lang].map((stat, i) => (
                  <div key={i} className="relative flex flex-col items-center text-center px-4">
                    {/* Vertical separator — desktop only, not on first */}
                    {i > 0 && (
                      <div className="hidden md:block absolute left-0 top-1/2 -translate-y-1/2 w-px h-20 bg-white/10" />
                    )}
                    <div className="font-display font-bold text-[64px] md:text-[96px] lg:text-[120px] text-white leading-none heading-tight">
                      <CountUp value={stat.value} delay={i * 0.2} />
                    </div>
                    {/* Orange accent divider */}
                    <div className="w-8 h-0.5 bg-clara-orange/40 mt-4 mb-3" />
                    <div className="text-[12px] md:text-[14px] uppercase tracking-[0.15em] text-white/50">
                      {stat.label}
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* ══════════ 04 EQUIPO — light ══════════ */}
            <section className="section-viewport bg-clara-bg">
              <SectionMarker n="04" />

              <div className="max-w-2xl mx-auto w-full">
                <RevealUp>
                  <div className="flex justify-center mb-6">
                    <ClaraArcs size={64} pulse />
                  </div>
                </RevealUp>

                <RevealCSS variant="scale" delay={0.1}>
                  <h2 className="font-display font-bold text-[44px] md:text-[64px] leading-[1.05] heading-tight text-clara-text mb-4 text-center">
                    {t.equipo.title}
                  </h2>
                </RevealCSS>

                <RevealUp delay={0.2}>
                  <p className="text-[20px] md:text-[22px] text-clara-text-secondary leading-relaxed mb-10 text-center italic">
                    &ldquo;{t.equipo.intro}&rdquo;
                  </p>
                </RevealUp>

                <Divider full />

                {t.equipo.members.map((member, i) => (
                  <RevealCSS key={member.name} variant="slide-left" delay={0.25 + i * 0.12}>
                    <div className="py-8 flex items-center gap-5">
                      <span className="flex-shrink-0 w-16 h-16 flex items-center justify-center rounded-full bg-clara-blue text-white font-display font-bold text-[28px] shadow-lg shadow-clara-blue/20">
                        {member.name[0]}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="font-display font-bold text-[22px] text-clara-text">
                          {member.name}
                        </p>
                        <p className="text-[18px] text-clara-text-secondary">
                          {member.role}
                        </p>
                      </div>
                    </div>
                    <Divider full />
                  </RevealCSS>
                ))}
              </div>
            </section>

            {/* ══════════ 05 CTA — dark ══════════ */}
            <section className="section-viewport section-dark">
              <SectionMarker n="05" />

              {/* Large decorative arcs — centered behind CTA */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-10 pointer-events-none">
                <ClaraArcs size={320} white pulse />
              </div>

              <div className="relative max-w-2xl mx-auto w-full flex flex-col items-center text-center gap-6">
                <h2 className="font-display font-bold text-[52px] md:text-[80px] leading-[1.0] heading-tight">
                  <Typewriter text={t.cta.title} speed={50} />
                </h2>

                <RevealUp delay={0.2}>
                  <p className="text-[20px] md:text-[22px] text-white/65 leading-relaxed max-w-md">
                    {t.cta.body}
                  </p>
                </RevealUp>

                <Divider />

                <RevealCSS variant="up" delay={0.4}>
                  <button
                    onClick={goToChat}
                    className="group flex items-center gap-3 px-10 py-5 min-h-touch
                               bg-clara-orange text-white
                               rounded-full font-display font-bold text-[20px]
                               shadow-lg shadow-clara-orange/30
                               hover:shadow-xl hover:shadow-clara-orange/40
                               hover:scale-105
                               active:scale-95 transition-all duration-300
                               focus-visible:outline focus-visible:outline-[3px]
                               focus-visible:outline-white focus-visible:outline-offset-2"
                  >
                    <svg
                      width="28" height="28" viewBox="0 0 24 24" fill="white" aria-hidden="true"
                      className="group-hover:scale-110 transition-transform duration-300"
                    >
                      <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                      <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                    </svg>
                    {t.cta.button}
                  </button>
                </RevealCSS>
              </div>
            </section>

          </div>
        );
      }}
    </SubPageLayout>
  );
}
