"use client";

/**
 * SvgDefs — hidden SVG symbol definitions for the Clara design system.
 *
 * Render this component once near the top of the component tree (e.g. in the
 * root layout). Other components can then reference any symbol with:
 *
 *   <svg width="48" height="48">
 *     <use href="#icon-blue" />
 *   </svg>
 *
 * Symbols defined here:
 *   #icon-blue     — Clara logo (3 blue arcs + orange dot)
 *   #icon-white    — Clara logo, white variant (for dark/coloured backgrounds)
 *   #persona-maria — Illustrated portrait: orange background, hijab
 *   #persona-ahmed — Illustrated portrait: blue background
 *   #persona-fatima — Illustrated portrait: green background, hijab
 */
export default function SvgDefs() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      style={{ display: "none" }}
      aria-hidden="true"
    >
      {/* ── Clara logo — 3 concentric arcs (voice waves) + orange origin dot ── */}
      <symbol id="icon-blue" viewBox="0 0 80 80" fill="none">
        <path
          d="M 28 14 A 30 30 0 0 1 28 66"
          stroke="#1B5E7B"
          strokeWidth="4.5"
          strokeLinecap="round"
          fill="none"
          opacity="0.35"
        />
        <path
          d="M 28 23 A 20 20 0 0 1 28 57"
          stroke="#1B5E7B"
          strokeWidth="4.5"
          strokeLinecap="round"
          fill="none"
          opacity="0.65"
        />
        <path
          d="M 28 32 A 10 10 0 0 1 28 48"
          stroke="#1B5E7B"
          strokeWidth="4.5"
          strokeLinecap="round"
          fill="none"
          opacity="1"
        />
        <circle cx="28" cy="40" r="5.5" fill="#D46A1E" />
      </symbol>

      {/* ── Clara logo — white variant for dark/coloured backgrounds ── */}
      <symbol id="icon-white" viewBox="0 0 80 80" fill="none">
        <path
          d="M 28 14 A 30 30 0 0 1 28 66"
          stroke="#FFFFFF"
          strokeWidth="4.5"
          strokeLinecap="round"
          fill="none"
          opacity="0.35"
        />
        <path
          d="M 28 23 A 20 20 0 0 1 28 57"
          stroke="#FFFFFF"
          strokeWidth="4.5"
          strokeLinecap="round"
          fill="none"
          opacity="0.65"
        />
        <path
          d="M 28 32 A 10 10 0 0 1 28 48"
          stroke="#FFFFFF"
          strokeWidth="4.5"
          strokeLinecap="round"
          fill="none"
          opacity="1"
        />
        <circle cx="28" cy="40" r="5.5" fill="#D46A1E" />
      </symbol>

      {/* ── Persona: María — orange background, hijab, warm cheeks ── */}
      <symbol id="persona-maria" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="32" fill="#D46A1E" />
        <circle cx="32" cy="32" r="30" fill="#E8884A" />
        {/* hijab */}
        <ellipse cx="32" cy="26" rx="18" ry="16" fill="#C45A10" />
        <ellipse cx="32" cy="30" rx="16" ry="14" fill="#D46A1E" />
        {/* face */}
        <ellipse cx="32" cy="30" rx="11" ry="12" fill="#DEB28A" />
        {/* eyes */}
        <ellipse cx="28" cy="28" rx="1.8" ry="1.2" fill="#3D2B1F" />
        <ellipse cx="36" cy="28" rx="1.8" ry="1.2" fill="#3D2B1F" />
        {/* gentle smile */}
        <path
          d="M28 33 Q32 37 36 33"
          stroke="#3D2B1F"
          strokeWidth="1.2"
          fill="none"
          strokeLinecap="round"
        />
        {/* warmth on cheeks */}
        <circle cx="26" cy="32" r="2" fill="#E8A080" opacity="0.5" />
        <circle cx="38" cy="32" r="2" fill="#E8A080" opacity="0.5" />
      </symbol>

      {/* ── Persona: Ahmed — blue background, short hair, confident smile ── */}
      <symbol id="persona-ahmed" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="32" fill="#1B5E7B" />
        <circle cx="32" cy="32" r="30" fill="#2A7A9A" />
        {/* hair */}
        <ellipse cx="32" cy="22" rx="12" ry="10" fill="#2C1810" />
        {/* face */}
        <ellipse cx="32" cy="28" rx="11" ry="12" fill="#8B6F47" />
        {/* eyes */}
        <ellipse cx="28" cy="26" rx="1.8" ry="1.3" fill="#1A1A2E" />
        <ellipse cx="36" cy="26" rx="1.8" ry="1.3" fill="#1A1A2E" />
        {/* confident smile */}
        <path
          d="M28 31 Q32 35 36 31"
          stroke="#1A1A2E"
          strokeWidth="1.2"
          fill="none"
          strokeLinecap="round"
        />
        {/* shirt collar */}
        <path
          d="M22 42 Q27 38 32 42 Q37 38 42 42"
          stroke="#ffffff"
          strokeWidth="1.5"
          fill="none"
          opacity="0.6"
        />
      </symbol>

      {/* ── Persona: Fátima — green background, hijab, caring warm smile ── */}
      <symbol id="persona-fatima" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="32" fill="#2E7D4F" />
        <circle cx="32" cy="32" r="30" fill="#3D9A66" />
        {/* hijab */}
        <ellipse cx="32" cy="26" rx="17" ry="15" fill="#267A45" />
        <ellipse cx="32" cy="30" rx="15" ry="13" fill="#2E7D4F" />
        {/* face */}
        <ellipse cx="32" cy="29" rx="10.5" ry="11.5" fill="#D4A574" />
        {/* caring eyes */}
        <ellipse cx="28.5" cy="27" rx="1.6" ry="1.2" fill="#2C1810" />
        <ellipse cx="35.5" cy="27" rx="1.6" ry="1.2" fill="#2C1810" />
        {/* warm smile */}
        <path
          d="M28.5 32 Q32 35.5 35.5 32"
          stroke="#2C1810"
          strokeWidth="1.1"
          fill="none"
          strokeLinecap="round"
        />
        {/* warmth on cheeks */}
        <circle cx="26.5" cy="31" r="1.8" fill="#D49A7A" opacity="0.4" />
        <circle cx="37.5" cy="31" r="1.8" fill="#D49A7A" opacity="0.4" />
      </symbol>
    </svg>
  );
}
