"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { SUGGESTIONS, PROMPT_PLACEHOLDER, MENU_ITEMS } from "@/lib/i18n";
import PromptBar from "@/components/welcome/PromptBar";
import SuggestionChips from "@/components/welcome/SuggestionChips";
import LanguageBar from "@/components/welcome/LanguageBar";
import HamburgerMenu from "@/components/welcome/HamburgerMenu";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */
type Lang = "es" | "fr" | "ar";

/* ------------------------------------------------------------------ */
/*  Speak helper — ElevenLabs static → Web Speech API                  */
/* ------------------------------------------------------------------ */
let _currentAudio: HTMLAudioElement | null = null;

/* Pre-generated ElevenLabs audio (Charlotte, Multilingual v2) */
const ELEVENLABS_WELCOME: Record<Lang, string> = {
  es: "/audio/welcome-es.mp3",
  fr: "/audio/welcome-fr.mp3",
  ar: "/audio/welcome-ar.mp3",
};

async function speak(text: string, lang: Lang, useWelcome = false) {
  if (_currentAudio) {
    _currentAudio.pause();
    _currentAudio = null;
  }
  try { window.speechSynthesis?.cancel(); } catch { /* noop */ }

  /* 1. ElevenLabs pre-generated welcome audio (instant, best quality) */
  if (useWelcome && ELEVENLABS_WELCOME[lang]) {
    try {
      const audio = new Audio(ELEVENLABS_WELCOME[lang]);
      audio.preload = "auto";
      _currentAudio = audio;
      await new Promise<void>((resolve, reject) => {
        audio.oncanplaythrough = () => { audio.play().then(resolve).catch(reject); };
        audio.onerror = reject;
      });
      return;
    } catch {
      /* autoplay blocked or file missing — fall through silently */
    }
  }

  /* 2. Browser Web Speech API (fallback) */
  _speakBrowser(text, lang);
}

const LANG_MAP: Record<Lang, string> = { es: "es-ES", fr: "fr-FR", ar: "ar-SA" };
const PREFERRED_VOICES: Record<string, string[]> = {
  "es-ES": ["Mónica", "Monica", "Paulina", "Google español"],
  "fr-FR": ["Amélie", "Amelie", "Audrey", "Google français"],
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
  } catch {
    /* browser blocked or unsupported */
  }
}

/* ------------------------------------------------------------------ */
/*  Content & cycling data                                             */
/* ------------------------------------------------------------------ */
const content: Record<Lang, {
  description: string;
  welcome_speech: string;
  footer: string;
}> = {
  es: {
    description: "Te ayudo con trámites sociales en España. Habla o escribe en tu idioma.",
    welcome_speech: "Hola, soy Clara. Estoy aquí para ayudarte con cualquier trámite. Habla o escribe, en tu idioma.",
    footer: "Gratis · Confidencial · En tu idioma",
  },
  fr: {
    description: "Je t'aide avec les démarches sociales en Espagne. Parle ou écris dans ta langue.",
    welcome_speech: "Bonjour, je suis Clara. Je suis là pour t'aider. Parle ou écris dans ta langue.",
    footer: "Gratuit · Confidentiel · Dans ta langue",
  },
  ar: {
    description: "أساعدك في الإجراءات الاجتماعية في إسبانيا. تحدث أو اكتب بلغتك.",
    welcome_speech: "مرحبا، أنا كلارا. أنا هنا لمساعدتك. تحدث أو اكتب بلغتك.",
    footer: "مجاني · سري · بلغتك",
  },
};

const CYCLE_GREETINGS: { text: string; tagline: [string, string]; mic: string; lang: Lang }[] = [
  { text: "Hola, soy Clara", tagline: ["Tu voz", "tiene poder"], mic: "Pulsa para hablar", lang: "es" },
  { text: "Bonjour, je suis Clara", tagline: ["Ta voix", "a du pouvoir"], mic: "Appuie pour parler", lang: "fr" },
  { text: "مرحبا، أنا كلارا", tagline: ["صوتك", "له قوة"], mic: "اضغط للتحدث", lang: "ar" },
];

const CYCLE_INTERVAL = 5000;
const PAUSE_DURATION = 15000;

/* ------------------------------------------------------------------ */
/*  WelcomePage                                                        */
/* ------------------------------------------------------------------ */
export default function WelcomePage() {
  const router = useRouter();
  const [lang, setLang] = useState<Lang>("es");
  const hasSpokenRef = useRef(false);

  /* Cycling state */
  const [cycleIdx, setCycleIdx] = useState(0);
  const [cycleFade, setCycleFade] = useState(true);
  const cycleTimerRef = useRef<ReturnType<typeof setInterval>>(undefined);
  const pauseTimerRef = useRef<ReturnType<typeof setTimeout>>(undefined);
  const [cyclingPaused, setCyclingPaused] = useState(false);

  /* Menu state */
  const [menuOpen, setMenuOpen] = useState(false);

  const t = content[lang];
  const cycled = CYCLE_GREETINGS[cycleIdx];

  /* ── Pause cycling when user picks a language ── */
  const handleLangChange = useCallback((newLang: Lang) => {
    setLang(newLang);
    setCyclingPaused(true);
    const matchIdx = CYCLE_GREETINGS.findIndex((g) => g.lang === newLang);
    if (matchIdx >= 0) {
      setCycleFade(false);
      setTimeout(() => {
        setCycleIdx(matchIdx);
        setCycleFade(true);
      }, 300);
    }
    clearTimeout(pauseTimerRef.current);
    pauseTimerRef.current = setTimeout(() => setCyclingPaused(false), PAUSE_DURATION);
  }, []);

  /* RTL support */
  useEffect(() => {
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.documentElement.lang = lang;
  }, [lang]);

  /* Preload voices */
  useEffect(() => {
    window.speechSynthesis?.getVoices();
    const handleVoices = () => window.speechSynthesis?.getVoices();
    window.speechSynthesis?.addEventListener?.("voiceschanged", handleVoices);
    return () => window.speechSynthesis?.removeEventListener?.("voiceschanged", handleVoices);
  }, []);

  /* Auto-play welcome audio */
  useEffect(() => {
    if (hasSpokenRef.current) return;
    hasSpokenRef.current = true;
    const timer = setTimeout(() => {
      speak(content[lang].welcome_speech, lang, true);
    }, 600);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* Airport-style cycling */
  useEffect(() => {
    if (cyclingPaused) {
      clearInterval(cycleTimerRef.current);
      return;
    }
    cycleTimerRef.current = setInterval(() => {
      setCycleFade(false);
      setTimeout(() => {
        setCycleIdx((prev) => (prev + 1) % CYCLE_GREETINGS.length);
        setCycleFade(true);
      }, 400);
    }, CYCLE_INTERVAL);
    return () => clearInterval(cycleTimerRef.current);
  }, [cyclingPaused]);

  /* Navigation helpers */
  function goToChat(mode: "voice" | "text", topic?: string) {
    if (_currentAudio) { _currentAudio.pause(); _currentAudio = null; }
    try { window.speechSynthesis?.cancel(); } catch { /* noop */ }
    const params = new URLSearchParams({ lang, mode });
    if (topic) params.set("topic", topic);
    router.push(`/chat?${params.toString()}`);
  }

  return (
    <div
      className="relative flex flex-col items-center justify-center min-h-screen px-6 py-4
                 bg-gradient-to-b from-clara-bg via-[#F0F7FA] to-[#E8F1F5]
                 overflow-x-hidden"
    >
      {/* ── Top bar: hamburger + language ── */}
      <div className="absolute top-0 left-0 right-0 w-full max-w-3xl mx-auto flex items-center justify-between px-6 pt-4 pb-2 z-10">
        <button
          onClick={() => setMenuOpen(true)}
          aria-label="Abrir menu"
          className="w-touch-sm h-touch-sm flex items-center justify-center rounded-xl
                     hover:bg-white/60 dark:hover:bg-[#2a2f36] transition-colors
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M3 12h18" />
            <path d="M3 6h18" />
            <path d="M3 18h18" />
          </svg>
        </button>

        <LanguageBar lang={lang} onChangeLang={handleLangChange} />
      </div>

      {/* ── Hamburger menu ── */}
      <HamburgerMenu
        isOpen={menuOpen}
        onClose={() => setMenuOpen(false)}
        items={MENU_ITEMS[lang]}
        lang={lang}
      />

      {/* ── Logo ── */}
      <div
        className="relative w-[64px] h-[64px] md:w-[96px] md:h-[96px] flex items-center justify-center mb-2"
        role="img"
        aria-label="Logo de Clara"
        style={{ animation: "fadeInUp 0.6s ease-out both" }}
      >
        <div className="absolute inset-0 rounded-full border-2 border-clara-blue/10"
             style={{ animation: "logoRipple 3s ease-out infinite" }} />
        <div className="absolute inset-[-12px] rounded-full border border-clara-blue/5"
             style={{ animation: "logoRipple 3s ease-out 1s infinite" }} />
        <svg className="w-[48px] h-[48px] md:w-[72px] md:h-[72px]" viewBox="0 0 80 80" fill="none" aria-hidden="true">
          <path d="M 28 14 A 30 30 0 0 1 28 66" stroke="#1B5E7B" strokeWidth="4.5"
                strokeLinecap="round" fill="none" opacity="0.35" />
          <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="#1B5E7B" strokeWidth="4.5"
                strokeLinecap="round" fill="none" opacity="0.65" />
          <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="#1B5E7B" strokeWidth="4.5"
                strokeLinecap="round" fill="none" opacity="1" />
          <circle cx="28" cy="40" r="5.5" fill="#D46A1E" />
        </svg>
      </div>

      {/* ── Cycling Greeting ── */}
      <p
        className="text-body-sm text-clara-text-secondary font-medium mb-1 transition-opacity duration-400"
        style={{
          opacity: cycleFade ? 1 : 0,
          direction: cycled.lang === "ar" ? "rtl" : "ltr",
          animation: "fadeInUp 0.5s ease-out both",
          animationDelay: "0.1s",
        }}
        aria-live="polite"
        aria-atomic="true"
      >
        {cycled.text}
      </p>

      <h1
        className="font-display font-bold text-[32px] md:text-[44px] lg:text-[56px] leading-[1.08] text-clara-text text-center mb-1 transition-opacity duration-400"
        style={{
          opacity: cycleFade ? 1 : 0,
          direction: cycled.lang === "ar" ? "rtl" : "ltr",
          animation: "fadeInUp 0.5s ease-out both",
          animationDelay: "0.15s",
        }}
      >
        <span className="text-clara-blue">{cycled.tagline[0]}</span>
        <br />
        <span className="text-clara-orange">{cycled.tagline[1]}</span>
      </h1>

      <p
        className="text-body-sm md:text-body text-clara-text-secondary text-center max-w-[300px] lg:max-w-[480px] mb-3 leading-relaxed"
        style={{ animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.2s" }}
      >
        {t.description}
      </p>

      {/* ── Mic button ── */}
      <button
        onClick={() => goToChat("voice")}
        aria-label={cycled.mic}
        className="w-[80px] h-[80px] md:w-[120px] md:h-[120px] bg-gradient-to-br from-clara-blue to-[#134a5f]
                   rounded-full flex items-center justify-center
                   shadow-xl shadow-clara-blue/30
                   hover:shadow-2xl hover:shadow-clara-blue/40
                   active:scale-95 transition-all duration-200
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-4
                   mb-2"
        style={{ animation: "scaleIn 0.4s ease-out 0.3s both, gentlePulse 3s ease-in-out 0.7s infinite" }}
      >
        <svg className="w-[44px] h-[44px] md:w-[52px] md:h-[52px]" viewBox="0 0 24 24" fill="white" aria-hidden="true">
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
          <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
        </svg>
      </button>

      <p
        className="text-body-sm text-clara-text-secondary font-medium mb-4 transition-opacity duration-400"
        style={{
          opacity: cycleFade ? 1 : 0,
          direction: cycled.lang === "ar" ? "rtl" : "ltr",
          animation: "fadeInUp 0.4s ease-out both",
          animationDelay: "0.35s",
        }}
      >
        {cycled.mic}
      </p>

      {/* ── Suggestion chips ── */}
      <div
        className="w-full flex justify-center mb-3"
        style={{ animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.4s" }}
      >
        <SuggestionChips
          suggestions={SUGGESTIONS[CYCLE_GREETINGS[cycleIdx].lang] ?? SUGGESTIONS.es}
          cycleFade={cycleFade}
          onChipTap={(text) => goToChat("text", text)}
        />
      </div>

      {/* ── Prompt bar ── */}
      <div
        className="w-full flex justify-center mb-4"
        style={{ animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.5s" }}
      >
        <PromptBar
          placeholders={[PROMPT_PLACEHOLDER.es, PROMPT_PLACEHOLDER.fr, PROMPT_PLACEHOLDER.ar]}
          cycleIdx={cycleIdx}
          cycleFade={cycleFade}
          onSubmitText={(text) => goToChat("text", text)}
          onMicTap={() => goToChat("voice")}
        />
      </div>

      {/* ── Footer ── */}
      <p
        className="text-label text-clara-text-secondary/80 text-center tracking-wider"
        style={{ animation: "fadeInUp 0.4s ease-out both", animationDelay: "0.6s" }}
      >
        {t.footer}
      </p>
    </div>
  );
}
