import { useEffect, useRef, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { SUGGESTIONS, PROMPT_PLACEHOLDER, MENU_ITEMS, SECOND_CTA } from "@/lib/i18n";
import { cdn } from "@/lib/constants";
import PromptBar from "@/components/welcome/PromptBar";
import SuggestionChips from "@/components/welcome/SuggestionChips";
import LanguageBar from "@/components/welcome/LanguageBar";
import HamburgerMenu from "@/components/welcome/HamburgerMenu";
import ProblemSection from "@/components/welcome/ProblemSection";
import PersonasSection from "@/components/welcome/PersonasSection";
import GuideSection from "@/components/welcome/GuideSection";
import PlanSection from "@/components/welcome/PlanSection";
import SuccessSection from "@/components/welcome/SuccessSection";
import FooterSection from "@/components/welcome/FooterSection";
import { useMascotState } from "@/hooks/useMascotState.ts";

type Lang = Language;

let _currentAudio: HTMLAudioElement | null = null;

/** CDN-hosted per-language welcome audio (ElevenLabs Sara Martin / Charlotte) */
const ELEVENLABS_WELCOME: Partial<Record<Lang, string>> = {
  es: cdn("/audio/welcome-es.mp3"),
  fr: cdn("/audio/welcome-fr.mp3"),
  ar: cdn("/audio/welcome-ar.mp3"),
};

/** Local fallback — multilingual welcome in public/audio/ */
const WELCOME_AUDIO_LOCAL = `${import.meta.env.BASE_URL}audio/welcome-multilingual.mp3`;

async function speak(text: string, lang: Lang, useWelcome = false) {
  if (_currentAudio) { _currentAudio.pause(); _currentAudio = null; }
  try { window.speechSynthesis?.cancel(); } catch { /* noop */ }

  // 1. Pre-recorded CDN audio per language (fastest, no backend needed)
  if (useWelcome) {
    const cdnUrl = ELEVENLABS_WELCOME[lang];
    if (cdnUrl) {
      try {
        const audio = new Audio(cdnUrl);
        audio.preload = "auto";
        _currentAudio = audio;
        await new Promise<void>((resolve, reject) => {
          audio.oncanplaythrough = () => { audio.play().then(resolve).catch(reject); };
          audio.onerror = reject;
        });
        return;
      } catch { /* fall through */ }
    }
  }

  // 2. Backend TTS (ElevenLabs Sara Martin — misma voz calida que WhatsApp)
  try {
    const { generateTTS } = await import("@/lib/api");
    const audioUrl = await generateTTS(text, lang);
    if (audioUrl) {
      const audio = new Audio(audioUrl);
      audio.preload = "auto";
      _currentAudio = audio;
      await new Promise<void>((resolve, reject) => {
        audio.oncanplaythrough = () => { audio.play().then(resolve).catch(reject); };
        audio.onerror = reject;
      });
      return;
    }
  } catch { /* fall through to local file */ }

  // 3. Fallback: local multilingual welcome MP3
  if (useWelcome) {
    try {
      const audio = new Audio(WELCOME_AUDIO_LOCAL);
      audio.preload = "auto";
      _currentAudio = audio;
      await new Promise<void>((resolve, reject) => {
        audio.oncanplaythrough = () => { audio.play().then(resolve).catch(reject); };
        audio.onerror = reject;
      });
      return;
    } catch { /* fall through */ }
  }

  // 4. Last resort: browser Speech API
  _speakBrowser(text, lang);
}

const LANG_MAP: Record<Lang, string> = {
  es: "es-ES", en: "en-US", fr: "fr-FR", pt: "pt-PT",
  ro: "ro-RO", ca: "ca-ES", zh: "zh-CN", ar: "ar-SA",
};
const PREFERRED_VOICES: Record<string, string[]> = {
  "es-ES": ["Monica", "Paulina", "Google español"],
  "en-US": ["Samantha", "Alex", "Google US English"],
  "fr-FR": ["Amelie", "Audrey", "Google français"],
  "pt-PT": ["Joana", "Google português"],
  "ro-RO": ["Ioana", "Google română"],
  "ca-ES": ["Montse", "Google català"],
  "zh-CN": ["Ting-Ting", "Google 中文"],
  "ar-SA": ["Maged", "Lana", "Google العربية"],
};

function _speakBrowser(text: string, lang: Lang) {
  try {
    const synth = window.speechSynthesis;
    if (!synth) return;
    const langCode = LANG_MAP[lang];
    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = langCode;
    msg.rate = 0.88;
    msg.pitch = 1.05;
    const voices = synth.getVoices();
    const preferred = PREFERRED_VOICES[langCode] ?? [];
    for (const name of preferred) {
      const match = voices.find((v) => v.name.includes(name));
      if (match) { msg.voice = match; break; }
    }
    if (!msg.voice) {
      const fallback = voices.find((v) => v.lang.startsWith(langCode.slice(0, 2)));
      if (fallback) msg.voice = fallback;
    }
    synth.speak(msg);
  } catch { /* noop */ }
}

const content: Record<Lang, { description: string; welcome_speech: string; footer: string }> = {
  es: {
    description: "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
    welcome_speech: "Hola, soy Clara. Estoy aqui para ayudarte con cualquier tramite. Habla o escribe, en tu idioma.",
    footer: "Gratis · Confidencial · En tu idioma",
  },
  en: {
    description: "I help you with social procedures in Spain. Speak or write in your language.",
    welcome_speech: "Hi, I'm Clara. I'm here to help you with any procedure. Speak or write, in your language.",
    footer: "Free · Confidential · In your language",
  },
  fr: {
    description: "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
    welcome_speech: "Bonjour, je suis Clara. Je suis la pour t'aider. Parle ou ecris dans ta langue.",
    footer: "Gratuit · Confidentiel · Dans ta langue",
  },
  pt: {
    description: "Ajudo-te com trâmites sociais em Espanha. Fala ou escreve no teu idioma.",
    welcome_speech: "Olá, sou Clara. Estou aqui para te ajudar com qualquer trâmite. Fala ou escreve, no teu idioma.",
    footer: "Gratuito · Confidencial · No teu idioma",
  },
  ro: {
    description: "Te ajut cu proceduri sociale în Spania. Vorbește sau scrie în limba ta.",
    welcome_speech: "Bună, sunt Clara. Sunt aici să te ajut cu orice procedură. Vorbește sau scrie, în limba ta.",
    footer: "Gratuit · Confidențial · În limba ta",
  },
  ca: {
    description: "T'ajudo amb tràmits socials a Espanya. Parla o escriu en el teu idioma.",
    welcome_speech: "Hola, soc Clara. Soc aquí per ajudar-te amb qualsevol tràmit. Parla o escriu, en el teu idioma.",
    footer: "Gratuït · Confidencial · En el teu idioma",
  },
  zh: {
    description: "我帮你处理西班牙的社会事务。用你的语言说话或写字。",
    welcome_speech: "你好，我是Clara。我在这里帮你处理任何手续。用你的语言说话或写字。",
    footer: "免费 · 保密 · 用你的语言",
  },
  ar: {
    description: "أساعدك في الإجراءات الاجتماعية في إسبانيا. تحدث أو اكتب بلغتك.",
    welcome_speech: "مرحبا، أنا كلارا. أنا هنا لمساعدتك. تحدث أو اكتب بلغتك.",
    footer: "مجاني · سري · بلغتك",
  },
};

const CYCLE_GREETINGS: { text: string; tagline: [string, string]; mic: string; lang: Lang }[] = [
  { text: "Hola, soy Clara", tagline: ["Tu voz", "tiene poder"], mic: "Pulsa para hablar", lang: "es" },
  { text: "Hi, I'm Clara", tagline: ["Your voice", "has power"] as [string, string], mic: "Tap to speak", lang: "en" as Lang },
  { text: "Bonjour, je suis Clara", tagline: ["Ta voix", "a du pouvoir"], mic: "Appuie pour parler", lang: "fr" },
  { text: "Olá, sou Clara", tagline: ["A tua voz", "tem poder"] as [string, string], mic: "Toca para falar", lang: "pt" as Lang },
  { text: "Bună, sunt Clara", tagline: ["Vocea ta", "are putere"] as [string, string], mic: "Apasă pentru a vorbi", lang: "ro" as Lang },
  { text: "Hola, soc Clara", tagline: ["La teva veu", "té poder"] as [string, string], mic: "Toca per parlar", lang: "ca" as Lang },
  { text: "你好，我是Clara", tagline: ["你的声音", "有力量"] as [string, string], mic: "点击说话", lang: "zh" as Lang },
  { text: "مرحبا، أنا كلارا", tagline: ["صوتك", "له قوة"], mic: "اضغط للتحدث", lang: "ar" },
];

const CYCLE_INTERVAL = 5000;
const PAUSE_DURATION = 15000;

export default function HomePage() {
  const navigate = useNavigate();
  const [lang, setLang] = useState<Lang>("es");
  const hasSpokenRef = useRef(false);
  const { setState: setMascotState } = useMascotState();

  // Greeting animation on mount
  useEffect(() => {
    setMascotState("greeting");
    const timer = setTimeout(() => setMascotState("idle"), 2000);
    return () => clearTimeout(timer);
  }, []);
  const [cycleIdx, setCycleIdx] = useState(0);
  const [cycleFade, setCycleFade] = useState(true);
  const cycleTimerRef = useRef<ReturnType<typeof setInterval>>(undefined);
  const pauseTimerRef = useRef<ReturnType<typeof setTimeout>>(undefined);
  const [cyclingPaused, setCyclingPaused] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const t = content[lang];
  const cycled = CYCLE_GREETINGS[cycleIdx];

  const handleLangChange = useCallback((newLang: Lang) => {
    setLang(newLang);
    setCyclingPaused(true);
    const matchIdx = CYCLE_GREETINGS.findIndex((g) => g.lang === newLang);
    if (matchIdx >= 0) {
      setCycleFade(false);
      setTimeout(() => { setCycleIdx(matchIdx); setCycleFade(true); }, 300);
    }
    clearTimeout(pauseTimerRef.current);
    pauseTimerRef.current = setTimeout(() => setCyclingPaused(false), PAUSE_DURATION);
  }, []);

  useEffect(() => {
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.documentElement.lang = lang;
  }, [lang]);

  useEffect(() => {
    window.speechSynthesis?.getVoices();
    const handleVoices = () => window.speechSynthesis?.getVoices();
    window.speechSynthesis?.addEventListener?.("voiceschanged", handleVoices);
    return () => window.speechSynthesis?.removeEventListener?.("voiceschanged", handleVoices);
  }, []);

  useEffect(() => {
    if (hasSpokenRef.current) return;
    const playWelcome = () => {
      if (hasSpokenRef.current) return;
      hasSpokenRef.current = true;
      speak(content[lang].welcome_speech, lang, true);
      document.removeEventListener("click", playWelcome);
      document.removeEventListener("touchstart", playWelcome);
      document.removeEventListener("keydown", playWelcome);
    };
    // Try autoplay first (works if browser allows it)
    const timer = setTimeout(() => {
      const testUrl = ELEVENLABS_WELCOME[lang] || WELCOME_AUDIO_LOCAL;
      const audio = new Audio(testUrl);
      audio.play().then(() => {
        audio.pause();
        audio.currentTime = 0;
        playWelcome();
      }).catch(() => {
        // Autoplay blocked — wait for first user interaction
        document.addEventListener("click", playWelcome, { once: false });
        document.addEventListener("touchstart", playWelcome, { once: false });
        document.addEventListener("keydown", playWelcome, { once: false });
      });
    }, 600);
    return () => {
      clearTimeout(timer);
      hasSpokenRef.current = false;
      document.removeEventListener("click", playWelcome);
      document.removeEventListener("touchstart", playWelcome);
      document.removeEventListener("keydown", playWelcome);
    };
  }, []);

  useEffect(() => {
    if (cyclingPaused) { clearInterval(cycleTimerRef.current); return; }
    cycleTimerRef.current = setInterval(() => {
      setCycleFade(false);
      setTimeout(() => { setCycleIdx((prev) => (prev + 1) % CYCLE_GREETINGS.length); setCycleFade(true); }, 400);
    }, CYCLE_INTERVAL);
    return () => clearInterval(cycleTimerRef.current);
  }, [cyclingPaused]);

  function goToChat(mode: "voice" | "text", topic?: string) {
    if (_currentAudio) { _currentAudio.pause(); _currentAudio = null; }
    try { window.speechSynthesis?.cancel(); } catch { /* noop */ }
    const params = new URLSearchParams({ lang, mode });
    if (topic) params.set("topic", topic);
    navigate(`/chat?${params.toString()}`);
  }

  const secondCta = SECOND_CTA[lang];

  return (
    <div className="flex flex-col min-h-screen overflow-x-hidden w-full max-w-[100vw]">
      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 1: HERO (above the fold) — mantener actual            */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-6 py-4
                          bg-gradient-to-b from-clara-bg via-[#F0F7FA] to-[#E8F1F5] overflow-hidden">
        {/* Atmospheric decorative circles */}
        <div className="absolute top-[20%] -left-[100px] w-[300px] h-[300px] rounded-full pointer-events-none"
             style={{ background: "radial-gradient(circle, rgba(27,94,123,0.04) 0%, transparent 70%)" }} aria-hidden="true" />
        <div className="absolute bottom-[15%] -right-[80px] w-[250px] h-[250px] rounded-full pointer-events-none"
             style={{ background: "radial-gradient(circle, rgba(212,106,30,0.03) 0%, transparent 70%)" }} aria-hidden="true" />

        <div className="absolute top-0 left-0 right-0 w-full max-w-3xl mx-auto flex items-center justify-between px-6 pt-4 pb-2 z-10">
          <button onClick={() => setMenuOpen(true)} aria-label="Abrir menu"
            className="w-touch-sm h-touch-sm flex items-center justify-center rounded-xl
                       hover:bg-white/60 dark:hover:bg-[#2a2f36] transition-colors">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M3 12h18" /><path d="M3 6h18" /><path d="M3 18h18" />
            </svg>
          </button>
          <LanguageBar lang={lang} onChangeLang={handleLangChange} />
        </div>

        <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} items={MENU_ITEMS[lang]} lang={lang} />

        <div className="relative w-[64px] h-[64px] md:w-[96px] md:h-[96px] flex items-center justify-center mb-2"
             role="img" aria-label="Logo de Clara" style={{ animation: "fadeInUp 0.6s ease-out both" }}>
          <div className="absolute inset-0 rounded-full border-2 border-clara-blue/10" style={{ animation: "logoRipple 3s ease-out infinite" }} />
          <div className="absolute inset-[-12px] rounded-full border border-clara-blue/5" style={{ animation: "logoRipple 3s ease-out 1s infinite" }} />
          <svg className="w-[48px] h-[48px] md:w-[72px] md:h-[72px]" viewBox="0 0 80 80" fill="none" aria-hidden="true">
            <path d="M 28 14 A 30 30 0 0 1 28 66" stroke="#1B5E7B" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.35" />
            <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="#1B5E7B" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.65" />
            <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="#1B5E7B" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="1" />
            <circle cx="28" cy="40" r="5.5" fill="#D46A1E" />
          </svg>
        </div>

        <p className="text-body-sm text-clara-text-secondary font-medium mb-1 transition-opacity duration-400"
           style={{ opacity: cycleFade ? 1 : 0, direction: cycled.lang === "ar" ? "rtl" : "ltr", animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.1s" }}
           aria-live="polite" aria-atomic="true">
          {cycled.text}
        </p>

        <h1 className="font-display font-bold text-[32px] md:text-[44px] lg:text-[56px] leading-[1.08] text-clara-text text-center mb-1 transition-opacity duration-400"
            style={{ opacity: cycleFade ? 1 : 0, direction: cycled.lang === "ar" ? "rtl" : "ltr", animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.15s" }}>
          <span className="text-clara-blue">{cycled.tagline[0]}</span><br />
          <span className="text-clara-orange">{cycled.tagline[1]}</span>
        </h1>

        <p className="text-body-sm md:text-body text-clara-text-secondary text-center max-w-[300px] lg:max-w-[480px] mb-3 leading-relaxed"
           style={{ animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.2s" }}>
          {t.description}
        </p>

        <button onClick={() => goToChat("voice")} aria-label={cycled.mic}
          className="w-[80px] h-[80px] md:w-[120px] md:h-[120px] bg-gradient-to-br from-clara-blue to-[#134a5f]
                     rounded-full flex items-center justify-center shadow-xl shadow-clara-blue/30
                     hover:shadow-2xl hover:shadow-clara-blue/40 active:scale-95 transition-all duration-200 mb-2"
          style={{ animation: "scaleIn 0.4s ease-out 0.3s both, gentlePulse 3s ease-in-out 0.7s infinite" }}>
          <svg className="w-[44px] h-[44px] md:w-[52px] md:h-[52px]" viewBox="0 0 24 24" fill="white" aria-hidden="true">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
          </svg>
        </button>

        <p className="text-body-sm text-clara-text-secondary font-medium mb-4 transition-opacity duration-400"
           style={{ opacity: cycleFade ? 1 : 0, direction: cycled.lang === "ar" ? "rtl" : "ltr", animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.35s" }}>
          {cycled.mic}
        </p>

        <div className="w-full flex justify-center mb-3" style={{ animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.4s" }}>
          <SuggestionChips suggestions={SUGGESTIONS[CYCLE_GREETINGS[cycleIdx].lang] ?? SUGGESTIONS.es} cycleFade={cycleFade} onChipTap={(text) => goToChat("text", text)} />
        </div>

        <div className="w-full flex justify-center mb-4" style={{ animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.5s" }}>
          <PromptBar placeholders={[PROMPT_PLACEHOLDER.es, PROMPT_PLACEHOLDER.en, PROMPT_PLACEHOLDER.fr, PROMPT_PLACEHOLDER.pt, PROMPT_PLACEHOLDER.ro, PROMPT_PLACEHOLDER.ca, PROMPT_PLACEHOLDER.zh, PROMPT_PLACEHOLDER.ar]} cycleIdx={cycleIdx} cycleFade={cycleFade} onSubmitText={(text) => goToChat("text", text)} onMicTap={() => goToChat("voice")} />
        </div>

        <p className="text-label text-clara-text-secondary/80 text-center tracking-wider"
           style={{ animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.6s" }}>
          {t.footer}
        </p>

        {/* Scroll indicator */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2" style={{ animation: "float 2s ease-in-out infinite" }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
               className="text-clara-text-secondary/40" aria-hidden="true">
            <path d="M12 5v14" />
            <path d="M19 12l-7 7-7-7" />
          </svg>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 2: PROBLEMA (SB7 §2)                                  */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <ProblemSection lang={lang} />

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 3: PERSONAS — empathy (SB7 §3)                        */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <PersonasSection lang={lang} />

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 4: GUIA — Clara as solution (SB7 §3–4)                */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <GuideSection lang={lang} />

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 5: PLAN — 3 steps (SB7 §4)                           */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <PlanSection lang={lang} />

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 6: EXITO — transformation (SB7 §7)                    */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <SuccessSection lang={lang} />

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 7: SEGUNDO CTA                                        */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <section className="section-viewport section-dark section-grain relative w-full flex flex-col items-center justify-center px-6
                          bg-gradient-to-b from-[#0f1419] via-[#1B5E7B]/20 to-[#0f1419] overflow-hidden">
        {/* Radar arcs — decorative concentric circles */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none" aria-hidden="true">
          {[
            { size: 200, opacity: 0.12, delay: "0s" },
            { size: 300, opacity: 0.09, delay: "0.4s" },
            { size: 400, opacity: 0.07, delay: "0.8s" },
            { size: 500, opacity: 0.05, delay: "1.2s" },
            { size: 600, opacity: 0.04, delay: "1.6s" },
          ].map(({ size, opacity, delay }) => (
            <div
              key={size}
              className="radar-arc"
              style={{
                width: size,
                height: size,
                opacity,
                animationDelay: delay,
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
              }}
            />
          ))}
        </div>

        <div className="relative max-w-3xl mx-auto flex flex-col items-center gap-6 py-16">
          <h2 className="cta-headline-glow font-display font-bold text-[32px] md:text-[44px] text-white text-center">
            {secondCta.headline}
          </h2>

          {/* Mic button with ripple rings */}
          <div
            className="relative flex items-center justify-center"
            style={{ animation: "ctaMicEntrance 0.7s cubic-bezier(0.22,1,0.36,1) both" }}
          >
            {/* Triple ripple rings */}
            <div className="cta-ripple-ring" aria-hidden="true" />
            <div className="cta-ripple-ring" aria-hidden="true" style={{ animationDelay: "0.6s" }} />
            <div className="cta-ripple-ring" aria-hidden="true" style={{ animationDelay: "1.2s" }} />

            <button
              onClick={() => goToChat("voice")}
              aria-label={secondCta.mic_label}
              className="relative z-10 w-[120px] h-[120px] md:w-[160px] md:h-[160px]
                         bg-gradient-to-br from-clara-blue to-[#134a5f]
                         rounded-full flex items-center justify-center
                         shadow-xl shadow-clara-blue/30
                         hover:shadow-2xl hover:shadow-clara-blue/40
                         active:scale-95 transition-all duration-200"
              style={{ animation: "gentlePulse 3s ease-in-out infinite" }}
            >
              <svg
                className="w-[56px] h-[56px] md:w-[72px] md:h-[72px]"
                viewBox="0 0 24 24"
                fill="white"
                aria-hidden="true"
              >
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
            </button>
          </div>

          <p className="text-body-sm text-white font-medium">
            {secondCta.mic_label}
          </p>

          <div className="w-full flex justify-center">
            <SuggestionChips suggestions={SUGGESTIONS[lang]} cycleFade={true} onChipTap={(text) => goToChat("text", text)} />
          </div>

          <div className="w-full flex justify-center">
            <PromptBar
              placeholders={[PROMPT_PLACEHOLDER[lang]]}
              cycleIdx={0}
              cycleFade={true}
              onSubmitText={(text) => goToChat("text", text)}
              onMicTap={() => goToChat("voice")}
            />
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 8: FOOTER                                             */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <FooterSection lang={lang} />
    </div>
  );
}
