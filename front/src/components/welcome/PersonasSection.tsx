import { useEffect, useRef, useState } from "react";
import type { Language } from "@/lib/types";
import { PERSONAS } from "@/lib/i18n";

interface PersonasSectionProps {
  lang: Language;
}

export default function PersonasSection({ lang }: PersonasSectionProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.disconnect(); } },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const colors: Record<string, string> = {
    maria: "border-l-clara-orange",
    ahmed: "border-l-clara-blue",
    fatima: "border-l-clara-green",
  };

  return (
    <section
      ref={sectionRef}
      className="w-full py-12 px-6 bg-[#FAFAFA] dark:bg-[#0f1419]"
      aria-label={
        lang === "ar" ? "قصص حقيقية" : lang === "fr" ? "Histoires réelles" : "Historias reales"
      }
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: "opacity 0.6s ease-out, transform 0.6s ease-out",
      }}
    >
      <div className="max-w-3xl mx-auto flex flex-col gap-4">
        {PERSONAS.map((persona, i) => (
          <div
            key={persona.id}
            className={`persona-chip border-l-4 ${colors[persona.id] ?? "border-l-clara-blue"}`}
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? "translateY(0)" : "translateY(16px)",
              transition: `opacity 0.5s ease-out ${i * 0.15}s, transform 0.5s ease-out ${i * 0.15}s`,
            }}
          >
            <img
              src={`/media/personas/${persona.id}.png`}
              alt={persona.name}
              width={64}
              height={64}
              className="w-16 h-16 rounded-full object-cover flex-shrink-0"
              loading="lazy"
            />
            <div className="flex-1 min-w-0">
              <p className="font-display font-bold text-body-sm text-clara-text dark:text-[#e8e8ee]">
                {persona.name}
              </p>
              <p className="text-label text-clara-text-secondary italic leading-snug">
                {persona.quote[lang]}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
