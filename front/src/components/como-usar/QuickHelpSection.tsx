import type { Language } from "@/lib/types";
import { COMO_USAR_EXTRA } from "@/lib/i18n";
import { useInView } from "@/hooks/useInView";
import { useTilt } from "@/hooks/useTilt";
import {
  IconMicrophone,
  IconVolume,
  IconShare,
} from "@/components/welcome/ComoUsarIllustrations";

interface QuickHelpSectionProps {
  lang: Language;
}

function HelpCard({
  icon,
  title,
  desc,
  delay,
  visible,
  onAction,
}: {
  icon: React.ReactNode;
  title: string;
  desc: string;
  delay: number;
  visible: boolean;
  onAction?: () => void;
}) {
  const { ref, style: tiltStyle, handlers } = useTilt(6);

  return (
    <div
      ref={ref}
      {...handlers}
      className="glass-card bento-card-glow p-5 flex flex-col items-center text-center gap-3 flex-1 min-w-[140px]"
      style={{
        perspective: "800px",
        borderRadius: 20,
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(20px)",
        transition: `opacity 0.5s ease-out ${delay}ms, transform 0.5s ease-out ${delay}ms`,
        cursor: onAction ? "pointer" : "default",
      }}
      onClick={onAction}
      role={onAction ? "button" : undefined}
      tabIndex={onAction ? 0 : undefined}
      onKeyDown={onAction ? (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onAction(); } } : undefined}
    >
      <div style={tiltStyle}>
        <div className="flex flex-col items-center gap-3">
          <div style={{ opacity: 0.8 }}>{icon}</div>
          <p className="font-display font-bold text-clara-text" style={{ fontSize: 16 }}>
            {title}
          </p>
          <p className="text-clara-text-secondary leading-snug" style={{ fontSize: 14 }}>
            {desc}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function QuickHelpSection({ lang }: QuickHelpSectionProps) {
  const tx = COMO_USAR_EXTRA[lang];
  const view = useInView(0.1);

  async function handleShare() {
    const shareData = {
      title: "Clara — Tu voz tiene poder",
      text: tx.quick_help_share_desc,
      url: window.location.origin,
    };
    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        await navigator.clipboard.writeText(window.location.origin);
      }
    } catch {
      // User cancelled share — ignore
    }
  }

  return (
    <section ref={view.ref} className="max-w-3xl mx-auto px-6 py-12">
      <h3
        className="font-display font-bold text-clara-text text-center mb-8"
        style={{
          fontSize: "clamp(20px, 4vw, 26px)",
          opacity: view.visible ? 1 : 0,
          transition: "opacity 0.6s ease-out",
        }}
      >
        {tx.quick_help_title}
      </h3>

      <div className="flex flex-col sm:flex-row gap-4">
        <HelpCard
          icon={<IconMicrophone />}
          title={tx.quick_help_mic}
          desc={tx.quick_help_mic_desc}
          delay={100}
          visible={view.visible}
        />
        <HelpCard
          icon={<IconVolume />}
          title={tx.quick_help_volume}
          desc={tx.quick_help_volume_desc}
          delay={220}
          visible={view.visible}
        />
        <HelpCard
          icon={<IconShare />}
          title={tx.quick_help_share}
          desc={tx.quick_help_share_desc}
          delay={340}
          visible={view.visible}
          onAction={handleShare}
        />
      </div>
    </section>
  );
}
