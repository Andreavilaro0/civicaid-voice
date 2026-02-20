"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import LanguageSelector from "@/components/ui/LanguageSelector";

/* ------------------------------------------------------------------ */
/*  Content bilingue                                                   */
/* ------------------------------------------------------------------ */
type Lang = "es" | "fr";

interface TopicItem {
  icon: string;
  label: string;
  speech: string;
}

const content: Record<
  Lang,
  {
    greeting: string;
    tagline: [string, string];
    description: string;
    mic_label: string;
    topics_hint: string;
    topics: TopicItem[];
    cta_text: string;
    welcome_speech: string;
    footer: string;
  }
> = {
  es: {
    greeting: "Hola, soy Clara",
    tagline: ["Tu voz", "tiene poder"],
    description:
      "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
    mic_label: "Pulsa para hablar",
    topics_hint: "O elige un tema:",
    topics: [
      { icon: "coin", label: "Ayuda\necon.", speech: "Ayuda economica" },
      { icon: "house", label: "Empadr.", speech: "Empadronamiento" },
      { icon: "health", label: "Salud", speech: "Tarjeta sanitaria" },
      { icon: "doc", label: "NIE/TIE", speech: "NIE o TIE" },
    ],
    cta_text: "Prefiero escribir",
    welcome_speech:
      "Hola, soy Clara. Pulsa el boton grande para hablarme.",
    footer: "Gratis · Confidencial · En tu idioma",
  },
  fr: {
    greeting: "Salut, je suis Clara",
    tagline: ["Ta voix", "a du pouvoir"],
    description:
      "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
    mic_label: "Appuie pour parler",
    topics_hint: "Ou choisis un sujet :",
    topics: [
      { icon: "coin", label: "Aide\necon.", speech: "Aide economique" },
      { icon: "house", label: "Empadr.", speech: "Empadronamiento" },
      { icon: "health", label: "Sante", speech: "Carte sanitaire" },
      { icon: "doc", label: "NIE/TIE", speech: "NIE ou TIE" },
    ],
    cta_text: "Je prefere ecrire",
    welcome_speech:
      "Salut, je suis Clara. Appuie sur le gros bouton pour me parler.",
    footer: "Gratuit · Confidentiel · Dans ta langue",
  },
};

/* ------------------------------------------------------------------ */
/*  Topic icons (inline SVG — small, 24px)                             */
/* ------------------------------------------------------------------ */
const topicIcons: Record<string, React.ReactNode> = {
  coin: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.66 0-3 1-3 2.25S10.34 12.5 12 12.5s3 1 3 2.25S13.66 16 12 16c-1 0-2-.5-2.5-1.5" />
      <path d="M12 6v2m0 8v2" />
    </svg>
  ),
  house: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1" />
    </svg>
  ),
  health: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4.8 2.3A6 6 0 0112 5a6 6 0 017.2-2.7C22.4 4.1 23 8.3 20 12c-2 2.5-5.3 5.3-8 7.5-2.7-2.2-6-5-8-7.5-3-3.7-2.4-7.9.8-9.7z" />
    </svg>
  ),
  doc: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <path d="M14 2v6h6" />
      <path d="M16 13H8m8 4H8m2-8H8" />
    </svg>
  ),
};

/* ------------------------------------------------------------------ */
/*  Speak helper — Web Speech API, fails silently                      */
/* ------------------------------------------------------------------ */
function speak(text: string, lang: Lang) {
  try {
    const synth = window.speechSynthesis;
    if (!synth) return;
    synth.cancel();
    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = lang === "es" ? "es-ES" : "fr-FR";
    msg.rate = 0.9;
    synth.speak(msg);
  } catch {
    /* browser blocked or unsupported */
  }
}

/* ------------------------------------------------------------------ */
/*  WelcomePage                                                        */
/* ------------------------------------------------------------------ */
export default function WelcomePage() {
  const router = useRouter();
  const [lang, setLang] = useState<Lang>("es");
  const hasSpokenRef = useRef(false);

  const t = content[lang];

  /* Auto-play welcome audio on mount — progressive enhancement */
  useEffect(() => {
    if (hasSpokenRef.current) return;
    hasSpokenRef.current = true;

    const timer = setTimeout(() => {
      speak(content[lang].welcome_speech, lang);
    }, 600);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function goToChat(mode: "voice" | "text", topic?: string) {
    try { window.speechSynthesis?.cancel(); } catch {}
    const params = new URLSearchParams({ lang, mode });
    if (topic) params.set("topic", topic);
    router.push(`/chat?${params.toString()}`);
  }

  function handleTopicTap(topic: TopicItem) {
    speak(topic.speech, lang);
    goToChat("voice", topic.speech);
  }

  return (
    <div
      className="relative flex flex-col items-center justify-center min-h-screen px-6
                 bg-gradient-to-b from-[#FFFAF5] via-[#FFF5EC] to-[#FFEDE0]
                 overflow-x-hidden"
    >
      {/* ── Language selector — top right ── */}
      <div className="fixed top-5 right-5 z-10">
        <LanguageSelector defaultLang={lang} onChange={setLang} />
      </div>

      {/* ── Logo ── */}
      <div
        className="w-[72px] h-[72px] bg-gradient-to-br from-clara-orange to-[#B85A18]
                   rounded-[18px] flex items-center justify-center
                   shadow-lg shadow-clara-orange/25 mb-4"
        role="img"
        aria-label="Logo de Clara"
      >
        <span className="text-white font-display font-bold text-[34px] leading-none select-none">
          C
        </span>
      </div>

      {/* ── Greeting + Tagline ── */}
      <p className="text-body-sm text-clara-text-secondary font-medium mb-2">
        {t.greeting} 👋
      </p>

      <h1 className="font-display font-bold text-[44px] leading-[1.08] text-clara-text text-center mb-3">
        {t.tagline[0]}
        <br />
        {t.tagline[1]}
      </h1>

      <p className="text-body text-clara-text-secondary text-center max-w-[300px] mb-8 leading-relaxed">
        {t.description}
      </p>

      {/* ══════════════════════════════════════════════════════════ */}
      {/*  HUGE MIC BUTTON — the hero, impossible to miss           */}
      {/* ══════════════════════════════════════════════════════════ */}
      <button
        onClick={() => goToChat("voice")}
        aria-label={t.mic_label}
        className="w-[120px] h-[120px] bg-gradient-to-br from-clara-blue to-[#134a5f]
                   rounded-full flex items-center justify-center
                   shadow-xl shadow-clara-blue/30
                   hover:shadow-2xl hover:shadow-clara-blue/40
                   active:scale-95 transition-all duration-200
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-4
                   mb-3"
        style={{ animation: "gentlePulse 3s ease-in-out infinite" }}
      >
        <svg width="52" height="52" viewBox="0 0 24 24" fill="white" aria-hidden="true">
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
          <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
        </svg>
      </button>

      <p className="text-body-sm text-clara-text-secondary font-medium mb-6">
        {t.mic_label}
      </p>

      {/* ══════════════════════════════════════════════════════════ */}
      {/*  TOPIC ICONS — tap to speak + navigate                    */}
      {/* ══════════════════════════════════════════════════════════ */}
      <p className="text-label text-clara-text-secondary/60 mb-3">
        {t.topics_hint}
      </p>

      <div className="flex gap-4 mb-8">
        {t.topics.map((topic) => (
          <button
            key={topic.icon}
            onClick={() => handleTopicTap(topic)}
            aria-label={topic.speech}
            className="flex flex-col items-center gap-1.5 group"
          >
            <div
              className="w-[56px] h-[56px] bg-white rounded-2xl border-2 border-clara-border/60
                         flex items-center justify-center
                         group-hover:border-clara-orange/50 group-hover:shadow-md
                         group-active:scale-95 transition-all duration-150
                         group-focus-visible:outline group-focus-visible:outline-[3px]
                         group-focus-visible:outline-clara-blue group-focus-visible:outline-offset-2"
            >
              <span className="text-clara-orange">{topicIcons[topic.icon]}</span>
            </div>
            <span className="text-[13px] text-clara-text-secondary leading-tight text-center max-w-[64px] whitespace-pre-line">
              {topic.label}
            </span>
          </button>
        ))}
      </div>

      {/* ══════════════════════════════════════════════════════════ */}
      {/*  SECONDARY — for users who prefer to type                 */}
      {/* ══════════════════════════════════════════════════════════ */}
      <button
        onClick={() => goToChat("text")}
        aria-label={t.cta_text}
        className="text-body-sm text-clara-blue font-medium underline underline-offset-4
                   min-h-touch-sm flex items-center gap-2
                   hover:text-[#134a5f] transition-colors duration-150
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-2
                   mb-6"
      >
        <svg
          width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"
        >
          <path d="M4 7h16M4 12h10M4 17h12" />
        </svg>
        {t.cta_text}
      </button>

      {/* ── Footer ── */}
      <p className="text-label text-clara-text-secondary/50 text-center tracking-wider">
        {t.footer}
      </p>
    </div>
  );
}
