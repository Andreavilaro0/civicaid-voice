import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";
import { QUIENES_SOMOS_STORY, STATS } from "@/lib/i18n";

/** Scroll-reveal hook — fades in when element enters viewport */
function useReveal() {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.disconnect(); } },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  const style: React.CSSProperties = {
    opacity: visible ? 1 : 0,
    transform: visible ? "translateY(0)" : "translateY(20px)",
    transition: "opacity 0.6s ease-out, transform 0.6s ease-out",
  };
  return { ref, style };
}

function RevealSection({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const { ref, style } = useReveal();
  return <div ref={ref} style={style} className={className}>{children}</div>;
}

export default function QuienesSomosPage() {
  const navigate = useNavigate();

  return (
    <SubPageLayout slug="quienes-somos">
      {(lang) => {
        const t = QUIENES_SOMOS_STORY[lang];

        function goToChat() {
          navigate(`/chat?lang=${lang}&mode=voice`);
        }

        return (
          <div className="flex flex-col gap-0 -mx-6 -mt-8">

            {/* ── Section 1: EMPATIZAR ── */}
            <RevealSection className="px-6 py-10 bg-white dark:bg-[#1a1f26]">
              <div className="max-w-lg mx-auto text-center">
                <h2 className="font-display font-bold text-h1 text-clara-text dark:text-[#e8e8ee] mb-4">
                  {t.empatizar.title}
                </h2>
                <p className="text-body text-clara-text-secondary leading-relaxed mb-6">
                  {t.empatizar.body}
                </p>
                <p className="text-body-sm text-clara-blue font-medium">
                  {t.empatizar.stat}
                </p>
              </div>
            </RevealSection>

            {/* ── Section 2: VALIDAR ── */}
            <RevealSection className="px-6 py-10 bg-[#FAFAFA] dark:bg-[#0f1419]">
              <div className="max-w-lg mx-auto text-center">
                <h2 className="font-display font-bold text-h2 text-clara-text dark:text-[#e8e8ee] mb-4">
                  {t.validar.title}
                </h2>
                <p className="text-body text-clara-text-secondary leading-relaxed mb-4">
                  {t.validar.body}
                </p>
                <p className="font-display font-bold text-h2 text-clara-orange">
                  {t.validar.closing}
                </p>
              </div>
            </RevealSection>

            {/* ── Section 3: EL MOMENTO ── */}
            <RevealSection className="px-6 py-10 bg-[#F0F7FA] dark:bg-[#141a20]">
              <div className="max-w-lg mx-auto">
                <h2 className="font-display font-bold text-h2 text-clara-blue mb-4 text-center">
                  {t.momento.title}
                </h2>
                {t.momento.body.split("\n\n").map((paragraph, i) => (
                  <p key={i} className="text-body text-clara-text-secondary leading-relaxed mb-4 last:mb-0">
                    {paragraph}
                  </p>
                ))}
              </div>
            </RevealSection>

            {/* ── Stats strip ── */}
            <RevealSection className="px-6 py-8 bg-white dark:bg-[#1a1f26]">
              <div className="stats-strip">
                {STATS[lang].map((stat, i) => (
                  <div key={i} className="stat-item">
                    <div className="stat-number">{stat.value}</div>
                    <div className="stat-label">{stat.label}</div>
                  </div>
                ))}
              </div>
            </RevealSection>

            {/* ── Section 4: EQUIPO ── */}
            <RevealSection className="px-6 py-10 bg-[#FAFAFA] dark:bg-[#0f1419]">
              <div className="max-w-lg mx-auto">
                <h2 className="font-display font-bold text-h2 text-clara-text dark:text-[#e8e8ee] mb-3 text-center">
                  {t.equipo.title}
                </h2>
                <p className="text-body text-clara-text-secondary leading-relaxed mb-6 text-center">
                  {t.equipo.intro}
                </p>
                <div className="flex flex-col gap-3">
                  {t.equipo.members.map((member) => (
                    <div
                      key={member.name}
                      className="flex items-center gap-4 p-4 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm"
                    >
                      <span className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-clara-blue/10 text-clara-blue font-display font-bold text-h2">
                        {member.name[0]}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee]">
                          {member.name}
                        </p>
                        <p className="text-body-sm text-clara-text-secondary italic">
                          {member.role}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </RevealSection>

            {/* ── Section 5: CTA ── */}
            <RevealSection className="px-6 py-12 bg-gradient-to-b from-[#F0F7FA] to-[#E8F1F5] dark:from-[#141a20] dark:to-[#0f1419]">
              <div className="max-w-lg mx-auto flex flex-col items-center text-center gap-6">
                <h2 className="font-display font-bold text-[28px] md:text-h1 leading-tight">
                  <span className="text-clara-blue">{t.cta.title.split(" ").slice(0, 2).join(" ")} </span>
                  <span className="text-clara-orange">{t.cta.title.split(" ").slice(2).join(" ")}</span>
                </h2>
                <p className="text-body text-clara-text-secondary leading-relaxed">
                  {t.cta.body}
                </p>
                <button
                  onClick={goToChat}
                  className="flex items-center gap-3 px-8 py-4 min-h-touch
                             bg-gradient-to-br from-clara-blue to-[#134a5f] text-white
                             rounded-2xl font-display font-bold text-button
                             shadow-xl shadow-clara-blue/30
                             hover:shadow-2xl hover:shadow-clara-blue/40
                             active:scale-95 transition-all duration-200
                             focus-visible:outline focus-visible:outline-[3px]
                             focus-visible:outline-clara-blue focus-visible:outline-offset-2"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="white" aria-hidden="true">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                  </svg>
                  {t.cta.button}
                </button>
              </div>
            </RevealSection>
          </div>
        );
      }}
    </SubPageLayout>
  );
}
