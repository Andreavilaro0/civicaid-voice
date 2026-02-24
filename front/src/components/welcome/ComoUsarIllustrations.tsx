import React from "react";

/* Step 1: Phone with Clara voice arcs */
export function IllustrationPhone() {
  return (
    <svg width="160" height="160" viewBox="0 0 160 160" fill="none" aria-hidden="true">
      {/* Phone body */}
      <rect x="48" y="20" width="64" height="120" rx="12" fill="#1B5E7B" opacity="0.12" stroke="#1B5E7B" strokeWidth="2" />
      <rect x="54" y="32" width="52" height="88" rx="4" fill="white" opacity="0.8" />
      {/* Screen glow */}
      <rect x="54" y="32" width="52" height="88" rx="4" fill="#1B5E7B" opacity="0.04" />
      {/* Clara arcs on screen */}
      <path d="M 68 76 A 12 12 0 0 1 92 76" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.6" />
      <path d="M 72 76 A 8 8 0 0 1 88 76" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.8" />
      <circle cx="80" cy="78" r="3" fill="#D46A1E" />
      {/* Home button */}
      <circle cx="80" cy="130" r="4" stroke="#1B5E7B" strokeWidth="1.5" opacity="0.3" />
      {/* Radiating connection lines */}
      <circle cx="80" cy="76" r="24" stroke="#1B5E7B" strokeWidth="1" opacity="0.1" strokeDasharray="4 4" />
      <circle cx="80" cy="76" r="36" stroke="#1B5E7B" strokeWidth="0.8" opacity="0.06" strokeDasharray="4 4" />
    </svg>
  );
}

/* Step 2: Globe with language bubbles */
export function IllustrationGlobe() {
  return (
    <svg width="160" height="160" viewBox="0 0 160 160" fill="none" aria-hidden="true">
      {/* Globe */}
      <circle cx="80" cy="80" r="36" fill="#1B5E7B" opacity="0.08" stroke="#1B5E7B" strokeWidth="1.5" />
      <ellipse cx="80" cy="80" rx="18" ry="36" stroke="#1B5E7B" strokeWidth="1" opacity="0.2" />
      <line x1="44" y1="80" x2="116" y2="80" stroke="#1B5E7B" strokeWidth="1" opacity="0.15" />
      <ellipse cx="80" cy="68" rx="32" ry="8" stroke="#1B5E7B" strokeWidth="0.8" opacity="0.12" />
      <ellipse cx="80" cy="92" rx="32" ry="8" stroke="#1B5E7B" strokeWidth="0.8" opacity="0.12" />
      {/* ES bubble — blue */}
      <rect x="14" y="36" width="36" height="24" rx="12" fill="#1B5E7B" opacity="0.15" />
      <text x="32" y="52" textAnchor="middle" fontSize="11" fontWeight="700" fill="#1B5E7B">ES</text>
      {/* FR bubble — orange */}
      <rect x="110" y="36" width="36" height="24" rx="12" fill="#D46A1E" opacity="0.15" />
      <text x="128" y="52" textAnchor="middle" fontSize="11" fontWeight="700" fill="#D46A1E">FR</text>
      {/* AR bubble — green */}
      <rect x="62" y="126" width="36" height="24" rx="12" fill="#2E7D4F" opacity="0.15" />
      <text x="80" y="142" textAnchor="middle" fontSize="11" fontWeight="700" fill="#2E7D4F" direction="rtl">عربي</text>
    </svg>
  );
}

/* Step 3: Microphone with sound waves */
export function IllustrationMic() {
  return (
    <svg width="160" height="160" viewBox="0 0 160 160" fill="none" aria-hidden="true">
      {/* Mic body */}
      <rect x="68" y="32" width="24" height="52" rx="12" fill="#D46A1E" opacity="0.15" stroke="#D46A1E" strokeWidth="2" />
      {/* Mic grille lines */}
      <line x1="72" y1="44" x2="88" y2="44" stroke="#D46A1E" strokeWidth="1" opacity="0.3" />
      <line x1="72" y1="52" x2="88" y2="52" stroke="#D46A1E" strokeWidth="1" opacity="0.3" />
      <line x1="72" y1="60" x2="88" y2="60" stroke="#D46A1E" strokeWidth="1" opacity="0.3" />
      {/* Mic stand */}
      <path d="M 56 78 A 24 24 0 0 0 104 78" stroke="#D46A1E" strokeWidth="2" strokeLinecap="round" opacity="0.5" fill="none" />
      <line x1="80" y1="102" x2="80" y2="112" stroke="#D46A1E" strokeWidth="2" opacity="0.5" />
      <line x1="68" y1="112" x2="92" y2="112" stroke="#D46A1E" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
      {/* Sound waves — left */}
      <path d="M 54 48 A 16 16 0 0 0 54 72" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <path d="M 44 40 A 24 24 0 0 0 44 80" stroke="#1B5E7B" strokeWidth="1.2" strokeLinecap="round" opacity="0.15" />
      {/* Sound waves — right */}
      <path d="M 106 48 A 16 16 0 0 1 106 72" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <path d="M 116 40 A 24 24 0 0 1 116 80" stroke="#1B5E7B" strokeWidth="1.2" strokeLinecap="round" opacity="0.15" />
      {/* Keyboard hint below */}
      <rect x="52" y="124" width="56" height="16" rx="4" fill="#1B5E7B" opacity="0.08" stroke="#1B5E7B" strokeWidth="1" />
      <rect x="56" y="128" width="8" height="8" rx="1.5" fill="#1B5E7B" opacity="0.12" />
      <rect x="67" y="128" width="8" height="8" rx="1.5" fill="#1B5E7B" opacity="0.12" />
      <rect x="78" y="128" width="8" height="8" rx="1.5" fill="#1B5E7B" opacity="0.12" />
      <rect x="89" y="128" width="8" height="8" rx="1.5" fill="#1B5E7B" opacity="0.12" />
    </svg>
  );
}

/* Step 4: Document with checkmark */
export function IllustrationDocument() {
  return (
    <svg width="160" height="160" viewBox="0 0 160 160" fill="none" aria-hidden="true">
      {/* Document */}
      <rect x="44" y="20" width="72" height="100" rx="8" fill="#2E7D4F" opacity="0.08" stroke="#2E7D4F" strokeWidth="1.5" />
      {/* Text lines */}
      <line x1="56" y1="44" x2="104" y2="44" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.2" />
      <line x1="56" y1="56" x2="96" y2="56" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.15" />
      <line x1="56" y1="68" x2="100" y2="68" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.15" />
      <line x1="56" y1="80" x2="88" y2="80" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.1" />
      {/* Green checkmark circle */}
      <circle cx="100" cy="100" r="20" fill="#2E7D4F" opacity="0.15" />
      <circle cx="100" cy="100" r="20" stroke="#2E7D4F" strokeWidth="2" />
      <polyline points="90,100 97,108 112,92" stroke="#2E7D4F" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      {/* Link chain icon */}
      <path d="M 56 100 L 56 96 A 4 4 0 0 1 60 92 L 68 92" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <circle cx="56" cy="104" r="3" fill="#1B5E7B" opacity="0.2" />
      {/* Arrow to user */}
      <path d="M 80 128 L 80 144" stroke="#2E7D4F" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <path d="M 74 140 L 80 148 L 86 140" stroke="#2E7D4F" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.3" />
    </svg>
  );
}

/* Topic icons for example questions */
export function IconHouse() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1B5E7B" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}

export function IconCoins() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#D46A1E" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <path d="M16 8h-6a2 2 0 100 4h4a2 2 0 010 4H8" />
      <path d="M12 18V6" />
    </svg>
  );
}

export function IconMedical() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2E7D4F" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  );
}

export function IconIdCard() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1B5E7B" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="20" height="14" rx="2" />
      <line x1="2" y1="10" x2="22" y2="10" />
      <circle cx="8" cy="15" r="2" />
      <line x1="14" y1="14" x2="20" y2="14" />
      <line x1="14" y1="17" x2="18" y2="17" />
    </svg>
  );
}

/* Guarantee icons — larger versions */
export const LARGE_GUARANTEE_ICONS: Record<string, React.ReactNode> = {
  free: (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#2E7D4F" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <path d="M16 8h-6a2 2 0 100 4h4a2 2 0 010 4H8" />
      <path d="M12 18V6" />
    </svg>
  ),
  lock: (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0110 0v4" />
    </svg>
  ),
  "no-register": (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#D46A1E" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
      <circle cx="12" cy="7" r="4" />
      <line x1="2" y1="2" x2="22" y2="22" />
    </svg>
  ),
  clock: (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  ),
};

export const EXAMPLE_ICONS: React.ReactNode[] = [
  <IconHouse key="h" />,
  <IconCoins key="c" />,
  <IconMedical key="m" />,
  <IconIdCard key="i" />,
];

export const STEP_ILLUSTRATIONS: React.ReactNode[] = [
  <IllustrationPhone key="p" />,
  <IllustrationGlobe key="g" />,
  <IllustrationMic key="mic" />,
  <IllustrationDocument key="d" />,
];

/* ── Large mic illustration (240x240) for bento Paso 3 ── */
export function IllustrationMicLarge() {
  return (
    <svg width="240" height="240" viewBox="0 0 240 240" fill="none" aria-hidden="true">
      {/* Mic body */}
      <rect x="96" y="40" width="48" height="80" rx="24" fill="#D46A1E" opacity="0.12" stroke="#D46A1E" strokeWidth="2.5" />
      {/* Mic grille lines */}
      <line x1="108" y1="60" x2="132" y2="60" stroke="#D46A1E" strokeWidth="1.5" opacity="0.25" />
      <line x1="108" y1="72" x2="132" y2="72" stroke="#D46A1E" strokeWidth="1.5" opacity="0.25" />
      <line x1="108" y1="84" x2="132" y2="84" stroke="#D46A1E" strokeWidth="1.5" opacity="0.25" />
      <line x1="108" y1="96" x2="132" y2="96" stroke="#D46A1E" strokeWidth="1.5" opacity="0.25" />
      {/* Mic stand */}
      <path d="M 76 116 A 44 44 0 0 0 164 116" stroke="#D46A1E" strokeWidth="2.5" strokeLinecap="round" opacity="0.4" fill="none" />
      <line x1="120" y1="160" x2="120" y2="180" stroke="#D46A1E" strokeWidth="2.5" opacity="0.4" />
      <line x1="100" y1="180" x2="140" y2="180" stroke="#D46A1E" strokeWidth="2.5" strokeLinecap="round" opacity="0.4" />
      {/* Sound waves — left */}
      <path d="M 72 64 A 28 28 0 0 0 72 108" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.2" />
      <path d="M 56 52 A 40 40 0 0 0 56 120" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.12" />
      <path d="M 40 40 A 52 52 0 0 0 40 132" stroke="#1B5E7B" strokeWidth="1" strokeLinecap="round" opacity="0.06" />
      {/* Sound waves — right */}
      <path d="M 168 64 A 28 28 0 0 1 168 108" stroke="#1B5E7B" strokeWidth="2" strokeLinecap="round" opacity="0.2" />
      <path d="M 184 52 A 40 40 0 0 1 184 120" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" opacity="0.12" />
      <path d="M 200 40 A 52 52 0 0 1 200 132" stroke="#1B5E7B" strokeWidth="1" strokeLinecap="round" opacity="0.06" />
      {/* Decorative dot */}
      <circle cx="120" cy="80" r="4" fill="#D46A1E" opacity="0.6" />
    </svg>
  );
}

/* ── Quick help icons (40x40) ── */
export function IconMicrophone() {
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#D46A1E" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="9" y="2" width="6" height="11" rx="3" />
      <path d="M5 10a7 7 0 0014 0" />
      <line x1="12" y1="17" x2="12" y2="21" />
      <line x1="8" y1="21" x2="16" y2="21" />
    </svg>
  );
}

export function IconVolume() {
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#1B5E7B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
      <path d="M19.07 4.93a10 10 0 010 14.14" />
      <path d="M15.54 8.46a5 5 0 010 7.07" />
    </svg>
  );
}

export function IconShare() {
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#2E7D4F" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="18" cy="5" r="3" />
      <circle cx="6" cy="12" r="3" />
      <circle cx="18" cy="19" r="3" />
      <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
      <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
    </svg>
  );
}

export function IconList() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="8" y1="6" x2="21" y2="6" />
      <line x1="8" y1="12" x2="21" y2="12" />
      <line x1="8" y1="18" x2="21" y2="18" />
      <line x1="3" y1="6" x2="3.01" y2="6" />
      <line x1="3" y1="12" x2="3.01" y2="12" />
      <line x1="3" y1="18" x2="3.01" y2="18" />
    </svg>
  );
}
