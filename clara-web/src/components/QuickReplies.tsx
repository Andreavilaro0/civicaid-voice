"use client";

import type { Language } from "@/lib/types";

interface QuickRepliesProps {
  language: Language;
  onSelect: (text: string) => void;
  visible: boolean;
}

const QUICK_REPLIES: Record<Language, string[]> = {
  es: ["Ayuda de dinero", "Registrarme en mi ciudad", "Ir al medico"],
  fr: ["Aide financiere", "M'inscrire dans ma ville", "Aller chez le medecin"],
  ar: ["مساعدة مالية", "التسجيل في مدينتي", "الذهاب للطبيب"],
  en: ["Financial help", "Register in my city", "See a doctor"],
  pt: ["Ajuda financeira", "Registar na minha cidade", "Ir ao medico"],
  ro: ["Ajutor financiar", "Inregistrare in orasul meu", "Mersul la medic"],
  ca: ["Ajuda economica", "Registrar-me a la meva ciutat", "Anar al metge"],
  zh: ["经济援助", "在我的城市注册", "看医生"],
};

const ariaLabels: Record<Language, string> = {
  es: "Sugerencias rapidas",
  fr: "Suggestions rapides",
  ar: "اقتراحات سريعة",
  en: "Quick suggestions",
  pt: "Sugestoes rapidas",
  ro: "Sugestii rapide",
  ca: "Suggeriments rapids",
  zh: "快速建议",
};

export default function QuickReplies({ language, onSelect, visible }: QuickRepliesProps) {
  if (!visible) return null;

  const chips = QUICK_REPLIES[language];

  return (
    <nav aria-label={ariaLabels[language]}>
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
