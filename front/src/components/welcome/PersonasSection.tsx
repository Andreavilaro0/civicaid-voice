import { useEffect, useRef, useState, useCallback } from "react";
import type { Language } from "@/lib/types";
import { PERSONAS } from "@/lib/i18n";

interface PersonasSectionProps {
  lang: Language;
}

/** 3D tilt card with parallax effect */
function TiltCard({
  children,
  className = "",
  delay = 0,
  visible = false,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  visible?: boolean;
}) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [hovering, setHovering] = useState(false);

  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const card = cardRef.current;
    if (!card) return;
    const rect = card.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const rotateX = ((e.clientY - centerY) / (rect.height / 2)) * -8;
    const rotateY = ((e.clientX - centerX) / (rect.width / 2)) * 8;
    setTilt({ x: rotateX, y: rotateY });
  }, []);

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
      className={className}
      style={{
        perspective: "800px",
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(16px)",
        transition: `opacity 0.5s ease-out ${delay}s, transform 0.5s ease-out ${delay}s`,
      }}
    >
      <div
        style={{
          transform: `rotateX(${tilt.x}deg) rotateY(${tilt.y}deg) scale(${hovering ? 1.02 : 1})`,
          transition: hovering ? "transform 0.1s ease-out" : "transform 0.4s ease-out",
          transformStyle: "preserve-3d",
          boxShadow: hovering
            ? `${tilt.y * -1.5}px ${tilt.x * 1.5}px 30px rgba(27,94,123,0.15), 0 0 20px rgba(27,94,123,0.08)`
            : "0 2px 20px rgba(27,94,123,0.06)",
          borderRadius: "16px",
        }}
      >
        {children}
      </div>
    </div>
  );
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

  const glowColors: Record<string, string> = {
    maria: "rgba(212,106,30,0.12)",
    ahmed: "rgba(27,94,123,0.12)",
    fatima: "rgba(46,125,79,0.12)",
  };

  return (
    <section
      ref={sectionRef}
      className="w-full py-12 px-6 bg-[#FAFAFA] dark:bg-[#0f1419]"
      aria-label={
        lang === "ar" ? "قصص حقيقية" : lang === "fr" ? "Histoires réelles" : "Historias reales"
      }
    >
      <div className="max-w-3xl mx-auto flex flex-col gap-5">
        {PERSONAS.map((persona, i) => (
          <TiltCard
            key={persona.id}
            delay={i * 0.15}
            visible={visible}
          >
            <div
              className={`persona-chip border-l-4 ${colors[persona.id] ?? "border-l-clara-blue"}`}
              style={{
                background: `linear-gradient(135deg, white 0%, ${glowColors[persona.id] ?? "rgba(27,94,123,0.05)"} 100%)`,
              }}
            >
              <div className="relative flex-shrink-0" style={{ transform: "translateZ(20px)" }}>
                <img
                  src={`/media/personas/${persona.id}.png`}
                  alt={persona.name}
                  width={72}
                  height={72}
                  className="w-[72px] h-[72px] rounded-2xl object-cover shadow-lg"
                  loading="lazy"
                />
              </div>
              <div className="flex-1 min-w-0" style={{ transform: "translateZ(10px)" }}>
                <p className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee]">
                  {persona.name}
                </p>
                <p className="text-body-sm text-clara-text-secondary italic leading-snug mt-1">
                  {persona.quote[lang]}
                </p>
              </div>
            </div>
          </TiltCard>
        ))}
      </div>
    </section>
  );
}
