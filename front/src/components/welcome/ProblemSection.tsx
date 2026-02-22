import { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { PROBLEM_SECTION, IMPACT, BEFORE_AFTER } from "@/lib/i18n";

// ─── Props ────────────────────────────────────────────────────────────────────

interface ProblemSectionProps {
  lang: Language;
}

// ─── AnimatedCounter ──────────────────────────────────────────────────────────
//
// Usage: <AnimatedCounter target="4.5M" label="..." visible={visible} />
//
// Counts from 0 to 4.5 in ~1.4 s using setInterval.
// Triggers only once when `visible` flips to true.
// The counter value renders in the `counter-glow` class (warm orange glow,
// defined in globals.css FASE 1 block) with font-family from CSS variable
// --font-display (Atkinson Hyperlegible).
// Wraps in a relative container so the orange radial glow and voice arcs
// sit behind the number without affecting layout.

function AnimatedCounter({
  target,
  label,
  visible,
}: {
  target: string;
  label: string;
  visible: boolean;
}) {
  const [count, setCount] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!visible) return;
    const end = 4.5;
    const duration = 1400;
    const steps = 35;
    const increment = end / steps;
    let current = 0;
    const timer = setInterval(() => {
      current += increment;
      if (current >= end) {
        setCount(end);
        setDone(true);
        clearInterval(timer);
        return;
      }
      setCount(Math.round(current * 10) / 10);
    }, duration / steps);
    return () => clearInterval(timer);
  }, [visible]);

  return (
    <div className="relative flex flex-col items-center">
      {/* Orange radial glow behind the number */}
      <div
        className="absolute pointer-events-none"
        style={{
          width: 400,
          height: 400,
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          background:
            "radial-gradient(ellipse at center, rgba(212,106,30,0.22) 0%, rgba(212,106,30,0.06) 45%, transparent 70%)",
          borderRadius: "50%",
        }}
        aria-hidden="true"
      />

      {/* Decorative voice arcs — concentric rings propagating outward */}
      <div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
        aria-hidden="true"
      >
        <div
          className="voice-arc voice-arc--animated"
          style={{
            width: 200,
            height: 200,
            border: "1.5px solid rgba(212,106,30,0.18)",
          }}
        />
        <div
          className="voice-arc"
          style={{
            width: 280,
            height: 280,
            border: "1.5px solid rgba(212,106,30,0.10)",
            animationDelay: "1s",
          }}
        />
        <div
          className="voice-arc voice-arc--animated"
          style={{
            width: 360,
            height: 360,
            border: "1px solid rgba(212,106,30,0.06)",
            animationDelay: "2s",
          }}
        />
      </div>

      {/* The counter number itself */}
      <span
        className="counter-glow relative"
        style={{
          fontFamily: "var(--font-display)",
          zIndex: 1,
          animation: done
            ? "counterPop 0.3s ease-out, counterGlowPulse 3s ease-in-out infinite"
            : "counterGlowPulse 3s ease-in-out infinite",
        }}
        aria-label={target}
        aria-live="polite"
        aria-atomic="true"
      >
        {visible ? `${count}M` : "0M"}
      </span>

      {/* Counter label — white on dark background */}
      <p
        className="relative mt-4 max-w-xs mx-auto leading-relaxed text-center"
        style={{
          fontFamily: "var(--font-body)",
          fontSize: "var(--font-size-body-sm)",
          color: "rgba(255,255,255,0.65)",
          zIndex: 1,
        }}
      >
        {label}
      </p>
    </div>
  );
}

// ─── TickerStrip ──────────────────────────────────────────────────────────────
//
// Horizontal auto-scrolling marquee of before/after cards.
//
// Architecture:
//   - Outer wrapper: `overflow-hidden` clip container with `role="marquee"`
//     and `aria-label` describing the content purpose.
//   - Inner `.ticker-strip`: the scrolling row (CSS keyframe `tickerScroll`
//     from globals.css, 30s linear infinite). Pauses on hover via CSS.
//   - Items are duplicated once (original + aria-hidden clone) so the loop
//     is visually seamless without a JS-based loop reset.
//
// Card layout: each item is a two-column grid inside a `glass-card` wrapper.
//   - "Before" cell: orange left border (#D46A1E), bg rgba(212,106,30,0.12)
//   - "After" cell: green left border (#2E7D4F), bg rgba(46,125,79,0.12)
//
// RTL: `.ticker-strip` gets `animation-direction: reverse` via CSS selector
//       `[dir="rtl"] .ticker-strip` already defined in globals.css.
// RTL borders: inline styles swap left/right conditionally via `isRTL`.

function TickerStrip({
  items,
  beforeLabel,
  afterLabel,
  isRTL,
}: {
  items: { before: string; after: string }[];
  beforeLabel: string;
  afterLabel: string;
  isRTL: boolean;
}) {
  // Render one set of cards, duplicated for the seamless loop.
  function Cards({ ariaHidden }: { ariaHidden?: boolean }) {
    return (
      <>
        {items.map((row, i) => (
          <div
            key={i}
            className="glass-card"
            style={{
              // Dark-adapted glass card: semi-transparent on dark blue bg
              background: "rgba(255,255,255,0.07)",
              border: "1px solid rgba(255,255,255,0.12)",
              boxShadow: "0 4px 24px rgba(0,0,0,0.25)",
              borderRadius: 20,
              minWidth: 480,
              maxWidth: 560,
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 0,
              overflow: "hidden",
              flexShrink: 0,
            }}
            aria-hidden={ariaHidden || undefined}
          >
            {/* Before cell */}
            <div
              style={{
                padding: "20px 24px",
                background: "rgba(212,106,30,0.10)",
                borderLeft: isRTL ? "none" : "3px solid #D46A1E",
                borderRight: isRTL ? "3px solid #D46A1E" : "none",
                fontSize: 15,
                lineHeight: 1.55,
                color: "rgba(255,255,255,0.82)",
                position: "relative",
              }}
            >
              {/* Micro label */}
              <span
                style={{
                  display: "block",
                  fontSize: 11,
                  fontFamily: "var(--font-display)",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                  color: "#D46A1E",
                  marginBottom: 8,
                  opacity: 0.9,
                }}
              >
                {beforeLabel}
              </span>
              {row.before}
            </div>

            {/* After cell */}
            <div
              style={{
                padding: "20px 24px",
                background: "rgba(46,125,79,0.12)",
                borderLeft: isRTL ? "none" : "3px solid #2E7D4F",
                borderRight: isRTL ? "3px solid #2E7D4F" : "none",
                fontSize: 15,
                lineHeight: 1.55,
                color: "rgba(255,255,255,0.82)",
              }}
            >
              {/* Micro label */}
              <span
                style={{
                  display: "block",
                  fontSize: 11,
                  fontFamily: "var(--font-display)",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                  color: "#4caf7d",
                  marginBottom: 8,
                  opacity: 0.9,
                }}
              >
                {afterLabel}
              </span>
              {row.after}
            </div>
          </div>
        ))}
      </>
    );
  }

  return (
    // Outer overflow clip — full bleed, no side padding
    <div
      style={{ width: "100%", overflow: "hidden" }}
      role="marquee"
      aria-label={`${beforeLabel} / ${afterLabel}`}
    >
      {/* Edge fade masks so cards fade in/out at the viewport edges */}
      <div style={{ position: "relative" }}>
        <div
          aria-hidden="true"
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: 80,
            height: "100%",
            background:
              "linear-gradient(to right, var(--color-clara-blue, #1B5E7B), transparent)",
            zIndex: 2,
            pointerEvents: "none",
          }}
        />
        <div
          aria-hidden="true"
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: 80,
            height: "100%",
            background:
              "linear-gradient(to left, var(--color-clara-blue, #1B5E7B), transparent)",
            zIndex: 2,
            pointerEvents: "none",
          }}
        />

        {/* The scrolling strip */}
        <div className="ticker-strip" style={{ gap: 16, padding: "4px 0" }}>
          {/* Original set — visible and readable */}
          <Cards />
          {/* Duplicate set — hidden from AT, creates the seamless loop */}
          <Cards ariaHidden />
        </div>
      </div>
    </div>
  );
}

// ─── ProblemSection ───────────────────────────────────────────────────────────
//
// FASE 1 — "El Muro": full-viewport dark cinematic section.
//
// Layout (top to bottom):
//   1. Section marker "02" watermark (absolute, top-left)
//   2. Large decorative voice arcs (absolute, centered behind counter)
//   3. Headline: wall-headline class with word-stagger animation
//      (spans only animate once IntersectionObserver fires)
//   4. Subtitle paragraph (white/muted, revealed with fade)
//   5. AnimatedCounter (the "4.5M" number with orange glow)
//   6. Column labels for the ticker (Antes / Con Clara)
//   7. TickerStrip — horizontal auto-scroll of before/after cards
//
// Intersection observer:
//   - threshold: 0.1 — fires when 10% of section enters viewport
//   - Disconnects after first intersection (one-shot reveal)
//   - `visible` state gates all CSS class additions and the counter

export default function ProblemSection({ lang }: ProblemSectionProps) {
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

  const t = PROBLEM_SECTION[lang];
  const impact = IMPACT[lang];
  const beforeAfter = BEFORE_AFTER[lang]; // 3 items
  const isRTL = lang === "ar";

  // Split title into individual word spans for staggered animation.
  // The `.wall-headline` CSS rule targets `> span` children and staggers
  // animation-delay for the first 3 words. We add `word-stagger` so the
  // base state is opacity:0 / translateY(20px), only revealed via the
  // `revealed` class which triggers the CSS transitions.
  const titleWords = t.title.split(" ");

  return (
    <section
      ref={sectionRef}
      className="section-viewport section-dark section-grain"
      aria-labelledby="problem-title"
    >
      {/* ── Section marker watermark "02" ──────────────────────────── */}
      <div
        className="section-marker"
        aria-hidden="true"
        style={{ color: "rgba(255,255,255,0.08)" }}
      >
        02
      </div>

      {/* ── Large background voice arcs (decorative, centered) ───────
          These sit behind everything else and add cinematic depth.
          Sizes chosen so they're visible even on the narrowest mobile.  */}
      <div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
        aria-hidden="true"
        style={{ zIndex: 0 }}
      >
        <div
          className="voice-arc voice-arc--animated"
          style={{
            width: "min(500px, 90vw)",
            height: "min(500px, 90vw)",
            border: "1px solid rgba(212,106,30,0.07)",
            position: "absolute",
          }}
        />
        <div
          className="voice-arc"
          style={{
            width: "min(700px, 120vw)",
            height: "min(700px, 120vw)",
            border: "1px solid rgba(212,106,30,0.04)",
            animationDelay: "1.5s",
            position: "absolute",
          }}
        />
        <div
          className="voice-arc voice-arc--animated"
          style={{
            width: "min(900px, 150vw)",
            height: "min(900px, 150vw)",
            border: "1px solid rgba(212,106,30,0.025)",
            animationDelay: "3s",
            position: "absolute",
          }}
        />
      </div>

      {/* ── Main content container ─────────────────────────────────── */}
      <div
        className="relative flex flex-col items-center gap-12 w-full max-w-4xl mx-auto"
        style={{ zIndex: 1 }}
      >
        {/* ── Headline block ─────────────────────────────────────── */}
        <div className="text-center px-6">
          {/*
            `wall-headline` defines font size (clamp 48px–96px), weight,
            line-height, color (#fff), and the wallReveal keyframe on
            each `> span`. We conditionally add `word-stagger` to keep
            spans at opacity:0 until `visible` triggers `revealed`.
            The wall-headline CSS already adds animation directly on spans,
            so we only need to gate the class presence.
          */}
          <h2
            id="problem-title"
            className={`wall-headline word-stagger${visible ? " revealed" : ""}`}
            style={{
              // Ensure words don't split in the middle on narrow screens
              wordBreak: "keep-all",
              overflowWrap: "break-word",
            }}
          >
            {titleWords.map((word, i) => (
              <span
                key={i}
                style={{
                  // Add a hair space between words since display:inline-block
                  // collapses whitespace between sibling spans
                  marginRight: i < titleWords.length - 1 ? "0.35em" : 0,
                  // Stagger beyond nth-child(3) handled by explicit delay
                  animationDelay: visible ? `${i * 0.15}s` : "0s",
                }}
              >
                {word}
              </span>
            ))}
          </h2>

          {/* Subtitle */}
          <p
            style={{
              fontFamily: "var(--font-body)",
              fontSize: "var(--font-size-body-sm)",
              lineHeight: "var(--font-size-body-sm--line-height)",
              color: "rgba(255,255,255,0.60)",
              maxWidth: "52ch",
              margin: "20px auto 0",
              opacity: visible ? 1 : 0,
              transform: visible ? "translateY(0)" : "translateY(16px)",
              transition: "opacity 0.7s ease-out 0.5s, transform 0.7s ease-out 0.5s",
            }}
          >
            {t.subtitle}
          </p>
        </div>

        {/* ── Divider rule — brand orange, 64px ────────────────────── */}
        <hr
          className="divider-line"
          aria-hidden="true"
          style={{
            opacity: visible ? 1 : 0,
            transform: visible ? "scaleX(1)" : "scaleX(0)",
            transition: "opacity 0.5s ease-out 0.6s, transform 0.6s cubic-bezier(0.22,1,0.36,1) 0.6s",
            transformOrigin: "center",
            margin: 0,
          }}
        />

        {/* ── Counter block ─────────────────────────────────────────
            Wrapped in a reveal container so it scales in after the
            headline has settled (delay 0.4s).                         */}
        <div
          style={{
            opacity: visible ? 1 : 0,
            transform: visible ? "scale(1)" : "scale(0.88)",
            transition:
              "opacity 0.7s ease-out 0.4s, transform 0.7s cubic-bezier(0.22,1,0.36,1) 0.4s",
          }}
        >
          <AnimatedCounter
            target="4.5M"
            label={impact.counter_label}
            visible={visible}
          />
        </div>

        {/* ── Ticker section ────────────────────────────────────────
            Column labels appear above the ticker strip.
            The strip itself is full-bleed (negative horizontal margin
            so it ignores the parent's max-width padding).               */}
        <div
          className="w-full"
          style={{
            opacity: visible ? 1 : 0,
            transform: visible ? "translateY(0)" : "translateY(24px)",
            transition:
              "opacity 0.7s ease-out 0.7s, transform 0.7s ease-out 0.7s",
          }}
        >
          {/* Column label row */}
          <div
            className="flex px-6 mb-5"
            style={{ gap: 16, justifyContent: "center" }}
          >
            <span
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                fontFamily: "var(--font-display)",
                fontWeight: 700,
                fontSize: 14,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                color: "#D46A1E",
              }}
            >
              {/* Orange dot */}
              <span
                aria-hidden="true"
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#D46A1E",
                  boxShadow: "0 0 8px rgba(212,106,30,0.6)",
                  flexShrink: 0,
                  display: "inline-block",
                }}
              />
              {impact.before_label}
            </span>

            <span
              style={{
                width: 1,
                height: 20,
                background: "rgba(255,255,255,0.15)",
                alignSelf: "center",
                flexShrink: 0,
              }}
              aria-hidden="true"
            />

            <span
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                fontFamily: "var(--font-display)",
                fontWeight: 700,
                fontSize: 14,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                color: "#4caf7d",
              }}
            >
              {/* Green dot */}
              <span
                aria-hidden="true"
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#2E7D4F",
                  boxShadow: "0 0 8px rgba(46,125,79,0.6)",
                  flexShrink: 0,
                  display: "inline-block",
                }}
              />
              {impact.after_label}
            </span>
          </div>

          {/* Full-bleed ticker — negative margin escapes the max-w container */}
          <div style={{ marginLeft: "calc(-50vw + 50%)", marginRight: "calc(-50vw + 50%)" }}>
            <TickerStrip
              items={beforeAfter}
              beforeLabel={impact.before_label}
              afterLabel={impact.after_label}
              isRTL={isRTL}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
