import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { COMO_USAR_PAGE, COMO_USAR_EXTRA } from "@/lib/i18n";
import { useInView } from "@/hooks/useInView";
import { LARGE_GUARANTEE_ICONS } from "@/components/welcome/ComoUsarIllustrations";

interface TrustCTASectionProps {
  lang: Language;
}

export default function TrustCTASection({ lang }: TrustCTASectionProps) {
  const navigate = useNavigate();
  const t = COMO_USAR_PAGE[lang];
  const tx = COMO_USAR_EXTRA[lang];
  const badges = useInView(0.1);
  const cta = useInView(0.2);

  const trustItems = [
    { icon: "free", label: tx.trust_free },
    { icon: "lock", label: tx.trust_private },
    { icon: "clock", label: tx.trust_247 },
  ];

  return (
    <section className="max-w-3xl mx-auto px-6 py-12">
      {/* Guarantee badges */}
      <div ref={badges.ref} className="flex flex-wrap items-center justify-center gap-4 mb-10">
        {trustItems.map((item, i) => (
          <div
            key={item.icon}
            className="guarantee-badge"
            style={{
              opacity: badges.visible ? 1 : 0,
              transform: badges.visible ? "translateY(0)" : "translateY(12px)",
              transition: `opacity 0.45s ease-out ${150 + i * 100}ms, transform 0.45s ease-out ${150 + i * 100}ms`,
            }}
          >
            {LARGE_GUARANTEE_ICONS[item.icon]}
            <span className="font-display font-bold text-clara-text" style={{ fontSize: 15 }}>
              {item.label}
            </span>
          </div>
        ))}
      </div>

      {/* CTA */}
      <div ref={cta.ref} className="flex flex-col items-center gap-4 text-center py-6">
        <h3
          className="font-display font-bold text-clara-text"
          style={{
            fontSize: "clamp(22px, 5vw, 30px)",
            opacity: cta.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out",
          }}
        >
          {t.cta_headline}
        </h3>
        <p
          className="text-clara-text-secondary"
          style={{
            fontSize: "clamp(15px, 2vw, 18px)",
            opacity: cta.visible ? 1 : 0,
            transition: "opacity 0.6s ease-out 0.1s",
          }}
        >
          {t.cta_sub}
        </p>
        <button
          onClick={() => navigate(`/chat?lang=${lang}`)}
          className="brand-gradient btn-magnetic font-display font-bold text-white rounded-full
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          style={{
            padding: "14px 36px",
            fontSize: 18,
            boxShadow: "0 4px 20px rgba(var(--clara-blue-rgb),0.3)",
            opacity: cta.visible ? 1 : 0,
            transform: cta.visible ? "scale(1)" : "scale(0.9)",
            transition: "opacity 0.5s ease-out 0.2s, transform 0.5s cubic-bezier(0.22,1,0.36,1) 0.2s",
            minHeight: 52,
          }}
        >
          {t.cta_button}
        </button>
      </div>
    </section>
  );
}
