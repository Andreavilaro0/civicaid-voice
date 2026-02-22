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
  es: ["Ayuda de dinero", "Registrarme en mi ciudad", "Ir al médico"],
  en: ["Financial help", "Register in my city", "See a doctor"],
  fr: ["Aide financière", "M'inscrire dans ma ville", "Aller chez le médecin"],
  pt: ["Ajuda financeira", "Registar-me na minha cidade", "Ir ao médico"],
  ro: ["Ajutor financiar", "Înregistrare în orașul meu", "Mergi la doctor"],
  ca: ["Ajuda econòmica", "Registrar-me a la meva ciutat", "Anar al metge"],
  zh: ["经济援助", "在我的城市注册", "看医生"],
  ar: ["مساعدة مالية", "التسجيل في مدينتي", "الذهاب للطبيب"],
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
