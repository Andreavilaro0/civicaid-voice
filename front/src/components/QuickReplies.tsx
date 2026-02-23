"use client";

/**
 * QuickReplies — suggested prompt chips shown below the chat input.
 *
 * Renders a horizontal wrapping strip of tappable chip buttons. Tapping a chip
 * calls `onSelect` with the chip text so the parent can inject it into the chat
 * input or submit it directly as a user message.
 *
 * The component returns null when `visible` is false, so the caller controls
 * visibility (e.g. hide after the first user message, or after a topic is
 * chosen in voice mode).
 *
 * Usage:
 *   import QuickReplies from "@/components/QuickReplies";
 *
 *   <QuickReplies
 *     language="es"
 *     visible={!hasMessages}
 *     onSelect={(text) => submitMessage(text)}
 *   />
 */

import type { Language } from "@/lib/types";

interface QuickRepliesProps {
  /** Current UI language — determines which chip labels to display */
  language: Language;
  /** Called with the chip's text when the user taps a suggestion */
  onSelect: (text: string) => void;
  /** When false the component renders nothing (no DOM node at all) */
  visible: boolean;
}

/* ------------------------------------------------------------------ */
/*  Localised chip labels                                              */
/* ------------------------------------------------------------------ */

const QUICK_REPLIES: Record<Language, string[]> = {
  es: ["¿Qué es el IMV?", "Empadronamiento", "Tarjeta sanitaria"],
  en: ["What is the IMV?", "Registration", "Health card"],
  fr: ["Qu'est-ce que le RMV?", "Inscription", "Carte sanitaire"],
  pt: ["O que é o IMV?", "Inscrição", "Cartão de saúde"],
  ro: ["Ce este IMV?", "Înregistrare", "Card de sănătate"],
  ca: ["Què és l'IMV?", "Empadronament", "Targeta sanitària"],
  zh: ["什么是IMV？", "居民登记", "医疗卡"],
  ar: ["ما هو الحد الأدنى؟", "التسجيل البلدي", "البطاقة الصحية"],
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function QuickReplies({
  language,
  onSelect,
  visible,
}: QuickRepliesProps) {
  if (!visible) return null;

  const chips = QUICK_REPLIES[language];

  const navLabels: Record<Language, string> = {
    es: "Sugerencias rápidas",
    en: "Quick suggestions",
    fr: "Suggestions rapides",
    pt: "Sugestões rápidas",
    ro: "Sugestii rapide",
    ca: "Suggeriments ràpids",
    zh: "快速建议",
    ar: "اقتراحات سريعة",
  };

  return (
    <nav aria-label={navLabels[language]}>
      <div
        className="flex flex-wrap gap-2 px-4 py-2 justify-center"
        style={{ animation: "fadeInUp 0.4s ease-out both" }}
      >
        {chips.map((text) => (
          <button
            key={text}
            onClick={() => onSelect(text)}
            className="quick-chip"
            aria-label={text}
            type="button"
          >
            {text}
          </button>
        ))}
      </div>
    </nav>
  );
}
