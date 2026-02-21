/* ================================================================== */
/*  constants.ts — Configuracion centralizada para Clara Web          */
/* ================================================================== */

import type { AudioFeedbackParams } from "./types";

/* ------------------------------------------------------------------ */
/*  API                                                               */
/* ------------------------------------------------------------------ */

/**
 * URL base del backend Flask.
 * Dev: http://localhost:5000 | Prod: VITE_API_URL en Render/Vercel
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5000";

/** Timeout para requests al backend (ms). Generoso para conexiones lentas */
export const API_TIMEOUT_MS = 30_000;

/* ------------------------------------------------------------------ */
/*  Colores — nombres semanticos, no genericos                       */
/*  "Civic Tenderness: el color conversa, no grita"                  */
/* ------------------------------------------------------------------ */

/**
 * Paleta Clara para uso fuera de Tailwind (canvas, SVG dinamico, Web Audio viz).
 * Para CSS: usar tokens Tailwind (bg-clara-blue, text-clara-orange, etc.)
 */
export const COLORS = {
  trust: "#1B5E7B",      // Azul — confianza, headers, primary
  warmth: "#D46A1E",     // Naranja — calidez, CTAs, active
  hope: "#2E7D4F",       // Verde — esperanza, success
  alert: "#C62828",      // Error — honesto, no alarmante
  caution: "#F9A825",    // Warning — atencion necesaria
} as const;

/* ------------------------------------------------------------------ */
/*  Motion — lenguaje de animacion consistente                       */
/*  "Civic Tenderness: calido, sin prisa, nunca abrupto"             */
/* ------------------------------------------------------------------ */

/** Easing curves — expo out se siente calido y fisico */
export const EASING = {
  /** Elementos que entran (burbujas, cards, modals) */
  out: "cubic-bezier(0.16, 1, 0.3, 1)",
  /** Elementos que salen (dismiss, close) */
  in: "cubic-bezier(0.55, 0, 1, 0.45)",
  /** Elementos que se transforman (hover, pressed) */
  inOut: "cubic-bezier(0.65, 0, 0.35, 1)",
} as const;

/** Duraciones en ms — generosas para usuarios mayores */
export const DURATION = {
  /** Feedback inmediato (pressed, hover) */
  instant: 150,
  /** Transiciones normales (color, border) */
  normal: 300,
  /** Entradas de elementos (bubble appear, card slide) */
  enter: 500,
  /** Stagger entre elementos secuenciales (burbujas de chat) */
  stagger: 80,
} as const;

/* ------------------------------------------------------------------ */
/*  Audio feedback — DNA sonora de Clara                             */
/*  Patron Mastercard: misma identidad en todos los touchpoints      */
/* ------------------------------------------------------------------ */

/** Frecuencias para feedback auditivo via Web Audio API */
export const AUDIO_FEEDBACK: Record<string, AudioFeedbackParams> = {
  /** Beep al iniciar — A4 ascendente, triangulo calido, 200ms */
  recordStart: { frequency: 440, duration: 200, type: "triangle" },
  /** Beep al parar — F4 descendente, triangulo calido, 200ms */
  recordStop: { frequency: 349, duration: 200, type: "triangle" },
  /** Beep de aviso a 50s — doble pulso A4, urgencia suave */
  recordWarning: { frequency: 440, duration: 120, type: "triangle" },
  /** Sonido sutil de mensaje enviado — C5 */
  messageSent: { frequency: 523, duration: 100, type: "triangle" },
};

/* ------------------------------------------------------------------ */
/*  Limites funcionales                                              */
/* ------------------------------------------------------------------ */

/** Limites de grabacion de voz — spec design/02-FRONTEND-ACCESIBLE.md */
export const MAX_RECORDING_SECONDS = 60;
export const RECORDING_WARNING_SECONDS = 50;
