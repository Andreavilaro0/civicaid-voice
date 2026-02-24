import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { COMO_USAR_PAGE, COMO_USAR_EXTRA } from "@/lib/i18n";
import { useInView } from "@/hooks/useInView";
import { useTilt } from "@/hooks/useTilt";
import {
  STEP_ILLUSTRATIONS,
  IllustrationMicLarge,
} from "@/components/welcome/ComoUsarIllustrations";

interface BentoGridProps {
  lang: Language;
}

/* ── Tiltable bento card wrapper ── */
function BentoCard({
  children,
  className = "",
  delay = 0,
  visible = false,
  span2 = false,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  visible?: boolean;
  span2?: boolean;
}) {
  const { ref, style: tiltStyle, handlers } = useTilt(8);

  return (
    <div
      ref={ref}
      {...handlers}
      className={`glass-card bento-card-glow p-5 ${span2 ? "sm:col-span-2" : ""} ${className}`}
      style={{
        perspective: "800px",
        borderRadius: 20,
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0) scale(1)" : "translateY(24px) scale(0.95)",
        transition: `opacity 0.6s ease-out ${delay}ms, transform 0.6s cubic-bezier(0.22,1,0.36,1) ${delay}ms`,
      }}
    >
      <div style={tiltStyle}>
        {children}
      </div>
    </div>
  );
}

/* ── Step number badge ── */
function StepBadge({ n }: { n: number }) {
  return (
    <div
      className="brand-gradient"
      style={{
        width: 32,
        height: 32,
        borderRadius: "50%",
        color: "white",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "var(--font-display)",
        fontWeight: 700,
        fontSize: 15,
        flexShrink: 0,
      }}
      aria-hidden="true"
    >
      {n}
    </div>
  );
}

export default function BentoGrid({ lang }: BentoGridProps) {
  const navigate = useNavigate();
  const t = COMO_USAR_PAGE[lang];
  const tx = COMO_USAR_EXTRA[lang];
  const view = useInView(0.05);

  // Map chip labels to chat queries
  const chipQueries: Record<string, Record<Language, string>> = {
    Padron: { es: "¿Qué necesito para el empadronamiento?", en: "What do I need for municipal registration?", fr: "De quoi ai-je besoin pour l'inscription municipale ?", pt: "O que preciso para o empadronamento?", ro: "Ce am nevoie pentru înregistrarea municipală?", ca: "Què necessito per a l'empadronament?", zh: "市政登记需要什么？", ar: "ما الذي أحتاجه للتسجيل البلدي؟" },
    IMV: { es: "¿Cómo solicito el Ingreso Mínimo Vital?", en: "How do I apply for the Minimum Vital Income?", fr: "Comment demander le Revenu Minimum Vital ?", pt: "Como peço o Rendimento Mínimo Vital?", ro: "Cum aplic pentru Venitul Minim Vital?", ca: "Com sol·licito l'Ingrés Mínim Vital?", zh: "如何申请最低生活保障？", ar: "كيف أتقدم بطلب للحد الأدنى من الدخل؟" },
    Salud: { es: "¿Qué documentos piden para la tarjeta sanitaria?", en: "What documents are needed for the health card?", fr: "Quels documents pour la carte sanitaire ?", pt: "Que documentos pedem para o cartão de saúde?", ro: "Ce documente sunt necesare pentru cardul de sănătate?", ca: "Quins documents demanen per a la targeta sanitària?", zh: "健康卡需要哪些文件？", ar: "ما المستندات المطلوبة للبطاقة الصحية؟" },
    NIE: { es: "¿Cómo renuevo mi NIE?", en: "How do I renew my NIE?", fr: "Comment renouveler mon NIE ?", pt: "Como renovo o meu NIE?", ro: "Cum îmi reînnoiesc NIE-ul?", ca: "Com renovo el meu NIE?", zh: "如何续签NIE？", ar: "كيف أجدد NIE الخاص بي؟" },
  };

  // Find the right query for a chip label
  function getChipQuery(chipIndex: number): string {
    const keys = ["Padron", "IMV", "Salud", "NIE"];
    const key = keys[chipIndex];
    return chipQueries[key]?.[lang] ?? t.examples[chipIndex] ?? "";
  }

  return (
    <section ref={view.ref} id="bento-grid" className="max-w-3xl mx-auto px-6 py-12">
      {/* Section title */}
      <h3
        className="font-display font-bold text-clara-text text-center mb-8"
        style={{
          fontSize: "clamp(22px, 4vw, 30px)",
          opacity: view.visible ? 1 : 0,
          transition: "opacity 0.6s ease-out",
        }}
      >
        {t.steps_title}
      </h3>

      <div className="bento-grid">
        {/* Card 1 — Paso 1: Abrir */}
        <BentoCard delay={100} visible={view.visible}>
          <div className="flex flex-col items-center text-center gap-3">
            <div style={{ animation: view.visible ? "float 6s ease-in-out infinite" : "none" }}>
              {STEP_ILLUSTRATIONS[0]}
            </div>
            <StepBadge n={1} />
            <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
              {t.steps[0].title}
            </p>
            <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
              {t.steps[0].desc}
            </p>
          </div>
        </BentoCard>

        {/* Card 2 — Practicar */}
        <BentoCard delay={220} visible={view.visible}>
          <div className="flex flex-col items-center text-center gap-3">
            <div className="flex gap-2 mb-1" aria-hidden="true">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="dot-pulse"
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: "rgba(var(--clara-blue-rgb),0.35)",
                    animationDelay: `${i * 0.4}s`,
                  }}
                />
              ))}
            </div>
            <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
              {tx.practice_title}
            </p>
            <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
              {tx.practice_desc}
            </p>
            <button
              onClick={() => navigate(`/chat?lang=${lang}`)}
              className="chip-tap rounded-full font-display font-bold text-clara-blue mt-1
                         focus-visible:outline focus-visible:outline-[3px]
                         focus-visible:outline-clara-blue focus-visible:outline-offset-2"
              style={{
                padding: "10px 24px",
                fontSize: 14,
                border: "1.5px solid rgba(var(--clara-blue-rgb),0.2)",
                background: "rgba(var(--clara-blue-rgb),0.04)",
                minHeight: 44,
              }}
            >
              {tx.practice_cta}
            </button>
          </div>
        </BentoCard>

        {/* Card 3 — Ejemplos locales (span 2 on desktop) */}
        <BentoCard delay={340} visible={view.visible} span2>
          <div className="flex flex-col items-center text-center gap-3">
            <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
              {tx.local_examples_title}
            </p>
            <div className="flex flex-wrap items-center justify-center gap-2">
              {tx.chips.map((chip, i) => (
                <button
                  key={chip}
                  onClick={() => navigate(`/chat?lang=${lang}&q=${encodeURIComponent(getChipQuery(i))}`)}
                  className="chip-tap rounded-full font-display text-clara-text
                             focus-visible:outline focus-visible:outline-[3px]
                             focus-visible:outline-clara-blue focus-visible:outline-offset-2"
                  style={{
                    padding: "10px 18px",
                    fontSize: 14,
                    fontWeight: 600,
                    border: "1.5px solid rgba(var(--clara-blue-rgb),0.15)",
                    background: "rgba(var(--clara-blue-rgb),0.04)",
                    minHeight: 44,
                  }}
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>
        </BentoCard>

        {/* Card 4 — Paso 2: Idioma */}
        <BentoCard delay={460} visible={view.visible}>
          <div className="flex flex-col items-center text-center gap-3">
            <div style={{ animation: view.visible ? "float 6s ease-in-out 0.5s infinite" : "none" }}>
              {STEP_ILLUSTRATIONS[1]}
            </div>
            <StepBadge n={2} />
            <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
              {t.steps[1].title}
            </p>
            <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
              {t.steps[1].desc}
            </p>
          </div>
        </BentoCard>

        {/* Card 5 — Paso 3: Hablar (large mic) */}
        <BentoCard delay={580} visible={view.visible}>
          <div className="flex flex-col items-center text-center gap-3">
            <div style={{ animation: view.visible ? "float 6s ease-in-out 1s infinite" : "none" }}>
              <IllustrationMicLarge />
            </div>
            <StepBadge n={3} />
            <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
              {t.steps[2].title}
            </p>
            <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
              {t.steps[2].desc}
            </p>
          </div>
        </BentoCard>

        {/* Card 6 — Paso 4: Escuchar */}
        <BentoCard delay={700} visible={view.visible} span2>
          <div className="flex flex-col items-center text-center gap-3">
            <div style={{ animation: view.visible ? "float 6s ease-in-out 1.5s infinite" : "none" }}>
              {STEP_ILLUSTRATIONS[3]}
            </div>
            <StepBadge n={4} />
            <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
              {t.steps[3].title}
            </p>
            <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
              {t.steps[3].desc}
            </p>
            <button
              onClick={() => navigate(`/chat?lang=${lang}`)}
              className="chip-tap rounded-full font-display font-bold text-clara-blue mt-1
                         focus-visible:outline focus-visible:outline-[3px]
                         focus-visible:outline-clara-blue focus-visible:outline-offset-2"
              style={{
                padding: "10px 24px",
                fontSize: 14,
                border: "1.5px solid rgba(var(--clara-blue-rgb),0.2)",
                background: "rgba(var(--clara-blue-rgb),0.04)",
                minHeight: 44,
              }}
            >
              {t.cta_button}
            </button>
          </div>
        </BentoCard>
      </div>
    </section>
  );
}
