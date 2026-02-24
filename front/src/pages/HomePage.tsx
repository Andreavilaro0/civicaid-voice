import { useEffect, useRef, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import type { Language } from "@/lib/types";
import { SUGGESTIONS, PROMPT_PLACEHOLDER, MENU_ITEMS, SECOND_CTA } from "@/lib/i18n";

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
import { ThemeToggleCompact } from "@/components/ui/ThemeToggle";
import { useMascotState } from "@/hooks/useMascotState.ts";

type Lang = Language;

let _currentAudio: HTMLAudioElement | null = null;

/** Single multilingual welcome audio (ES + FR + AR in one clip) */
const WELCOME_AUDIO_URL = `${import.meta.env.BASE_URL}audio/welcome-multilingual.mp3`;

/** Play only the multilingual welcome MP3 — returns true if playback started */
async function playWelcomeAudio(): Promise<boolean> {
  if (_currentAudio) { _currentAudio.pause(); _currentAudio = null; }
  try {
    const audio = new Audio(WELCOME_AUDIO_URL);
    audio.preload = "auto";
    _currentAudio = audio;
    await new Promise<void>((resolve, reject) => {
      audio.oncanplaythrough = () => { audio.play().then(resolve).catch(reject); };
      audio.onerror = reject;
    });
    return true;
  } catch {
    return false; // autoplay blocked — will retry on user interaction
  }
}

const content: Record<Lang, { description: string; footer: string }> = {
  es: {
    description: "Te ayudo con trámites sociales en España. Habla o escribe en tu idioma.",
    footer: "Gratis · Confidencial · En tu idioma",
  },
  en: {
    description: "I help you with social procedures in Spain. Speak or write in your language.",
    footer: "Free · Confidential · In your language",
  },
  fr: {
    description: "Je t'aide avec les démarches sociales en Espagne. Parle ou écris dans ta langue.",
    footer: "Gratuit · Confidentiel · Dans ta langue",
  },
  pt: {
    description: "Ajudo-te com trâmites sociais em Espanha. Fala ou escreve no teu idioma.",
    footer: "Gratuito · Confidencial · No teu idioma",
  },
  ro: {
    description: "Te ajut cu proceduri sociale în Spania. Vorbește sau scrie în limba ta.",
    footer: "Gratuit · Confidențial · În limba ta",
  },
  ca: {
    description: "T'ajudo amb tràmits socials a Espanya. Parla o escriu en el teu idioma.",
    footer: "Gratuït · Confidencial · En el teu idioma",
  },
  zh: {
    description: "我帮你处理西班牙的社会事务。用你的语言说话或写字。",
    footer: "免费 · 保密 · 用你的语言",
  },
  ar: {
    description: "أساعدك في الإجراءات الاجتماعية في إسبانيا. تحدث أو اكتب بلغتك.",
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

/* ------------------------------------------------------------------ */
/*  Sección datos + WhatsApp                                           */
/* ------------------------------------------------------------------ */

const DATA_WA_CONTENT: Record<Lang, {
  title: string;
  stats: { value: string; label: string }[];
  whatsapp_title: string;
  whatsapp_body: string;
  whatsapp_badge: string;
}> = {
  es: {
    title: "La realidad en números",
    stats: [
      { value: "4.5M", label: "personas inmigrantes en España" },
      { value: "1/5", label: "residentes en España nacieron en otro país" },
      { value: "8", label: "idiomas que habla Clara" },
      { value: "20+", label: "trámites cubiertos" },
    ],
    whatsapp_title: "Próximamente en WhatsApp",
    whatsapp_body: "Clara fue construida con la API de Meta para WhatsApp. Nuestro plan es tener la línea activa para que cualquier persona pueda escribir o hablar con Clara directamente desde WhatsApp, sin descargar nada.",
    whatsapp_badge: "En desarrollo",
  },
  en: {
    title: "The reality in numbers",
    stats: [
      { value: "4.5M", label: "immigrants in Spain" },
      { value: "1/5", label: "residents in Spain were born abroad" },
      { value: "8", label: "languages Clara speaks" },
      { value: "20+", label: "procedures covered" },
    ],
    whatsapp_title: "Coming soon on WhatsApp",
    whatsapp_body: "Clara was built with Meta's WhatsApp API. Our plan is to have the line active so anyone can write or speak to Clara directly from WhatsApp, without downloading anything.",
    whatsapp_badge: "In development",
  },
  fr: {
    title: "La réalité en chiffres",
    stats: [
      { value: "4.5M", label: "immigrés en Espagne" },
      { value: "1/5", label: "résidents en Espagne sont nés à l'étranger" },
      { value: "8", label: "langues parlées par Clara" },
      { value: "20+", label: "démarches couvertes" },
    ],
    whatsapp_title: "Bientôt sur WhatsApp",
    whatsapp_body: "Clara a été construite avec l'API WhatsApp de Meta. Notre plan est d'avoir la ligne active pour que n'importe qui puisse écrire ou parler avec Clara directement depuis WhatsApp, sans rien télécharger.",
    whatsapp_badge: "En développement",
  },
  pt: {
    title: "A realidade em números",
    stats: [
      { value: "4.5M", label: "imigrantes em Espanha" },
      { value: "1/5", label: "residentes em Espanha nasceram noutro país" },
      { value: "8", label: "idiomas que Clara fala" },
      { value: "20+", label: "trâmites cobertos" },
    ],
    whatsapp_title: "Em breve no WhatsApp",
    whatsapp_body: "Clara foi construída com a API do WhatsApp da Meta. O nosso plano é ter a linha ativa para que qualquer pessoa possa escrever ou falar com Clara diretamente do WhatsApp, sem descarregar nada.",
    whatsapp_badge: "Em desenvolvimento",
  },
  ro: {
    title: "Realitatea în cifre",
    stats: [
      { value: "4.5M", label: "imigranți în Spania" },
      { value: "1/5", label: "rezidenți în Spania s-au născut în altă țară" },
      { value: "8", label: "limbi vorbite de Clara" },
      { value: "20+", label: "proceduri acoperite" },
    ],
    whatsapp_title: "În curând pe WhatsApp",
    whatsapp_body: "Clara a fost construită cu API-ul WhatsApp de la Meta. Planul nostru este să avem linia activă pentru ca oricine să poată scrie sau vorbi cu Clara direct din WhatsApp, fără să descarce nimic.",
    whatsapp_badge: "În dezvoltare",
  },
  ca: {
    title: "La realitat en xifres",
    stats: [
      { value: "4.5M", label: "immigrants a Espanya" },
      { value: "1/5", label: "residents a Espanya van néixer a un altre país" },
      { value: "8", label: "idiomes que parla Clara" },
      { value: "20+", label: "tràmits coberts" },
    ],
    whatsapp_title: "Properament a WhatsApp",
    whatsapp_body: "Clara va ser construïda amb l'API de WhatsApp de Meta. El nostre pla és tenir la línia activa perquè qualsevol persona pugui escriure o parlar amb Clara directament des de WhatsApp, sense descarregar res.",
    whatsapp_badge: "En desenvolupament",
  },
  zh: {
    title: "数据中的现实",
    stats: [
      { value: "4.5M", label: "西班牙的移民人口" },
      { value: "1/5", label: "西班牙居民出生在其他国家" },
      { value: "8", label: "Clara会说的语言" },
      { value: "20+", label: "覆盖的事务类型" },
    ],
    whatsapp_title: "即将登陆WhatsApp",
    whatsapp_body: "Clara使用Meta的WhatsApp API构建。我们的计划是开通WhatsApp热线，让任何人都可以直接通过WhatsApp与Clara交流，无需下载任何应用。",
    whatsapp_badge: "开发中",
  },
  ar: {
    title: "الواقع بالأرقام",
    stats: [
      { value: "4.5M", label: "مهاجر في إسبانيا" },
      { value: "1/5", label: "من سكان إسبانيا ولدوا في بلد آخر" },
      { value: "8", label: "لغات تتحدثها كلارا" },
      { value: "20+", label: "إجراء مغطى" },
    ],
    whatsapp_title: "قريباً على واتساب",
    whatsapp_body: "تم بناء كلارا باستخدام واجهة برمجة تطبيقات واتساب من ميتا. خطتنا هي تفعيل الخط حتى يتمكن أي شخص من الكتابة أو التحدث مع كلارا مباشرة من واتساب، دون تحميل أي شيء.",
    whatsapp_badge: "قيد التطوير",
  },
};

function DataWhatsAppSection({ lang }: { lang: Lang }) {
  const t = DATA_WA_CONTENT[lang];
  return (
    <section className="relative w-full bg-clara-bg px-6 py-16 overflow-hidden">
      <div className="max-w-3xl mx-auto flex flex-col items-center gap-12">
        {/* Stats grid */}
        <div className="text-center">
          <h2 className="font-display font-bold text-[28px] md:text-[36px] text-clara-text mb-8">
            {t.title}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {t.stats.map((stat) => (
              <div key={stat.value} className="flex flex-col items-center gap-2 p-4 rounded-2xl bg-clara-card border border-clara-border/50">
                <span className="font-display font-bold text-[32px] md:text-[40px] text-clara-orange leading-none">
                  {stat.value}
                </span>
                <span className="text-body-sm text-clara-text-secondary text-center leading-snug">
                  {stat.label}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* WhatsApp card */}
        <div className="w-full max-w-lg p-6 rounded-2xl bg-clara-card border border-clara-border/50 shadow-lg flex flex-col items-center gap-4 text-center">
          <div className="flex items-center gap-3">
            <svg className="w-10 h-10 text-[#25D366] flex-shrink-0" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
            </svg>
            <h3 className="font-display font-bold text-[22px] md:text-[26px] text-clara-text">
              {t.whatsapp_title}
            </h3>
          </div>
          <p className="text-body-sm text-clara-text-secondary leading-relaxed">
            {t.whatsapp_body}
          </p>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-clara-orange/10 text-clara-orange text-label font-medium">
            <span className="w-2 h-2 rounded-full bg-clara-orange animate-pulse" />
            {t.whatsapp_badge}
          </span>
        </div>
      </div>
    </section>
  );
}

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
    if (hasSpokenRef.current) return;
    const cleanup = () => {
      document.removeEventListener("click", onInteraction);
      document.removeEventListener("touchstart", onInteraction);
      document.removeEventListener("keydown", onInteraction);
    };
    const onInteraction = async () => {
      if (hasSpokenRef.current) return;
      hasSpokenRef.current = true;
      cleanup();
      await playWelcomeAudio();
    };
    // Try autoplay directly (works if user has interacted with site before)
    const timer = setTimeout(async () => {
      if (hasSpokenRef.current) return;
      const played = await playWelcomeAudio();
      if (played) {
        hasSpokenRef.current = true;
        cleanup();
      }
      // If autoplay failed, listeners below will handle it on first interaction
    }, 600);
    // Wait for first user interaction (click, tap, keypress)
    document.addEventListener("click", onInteraction, { once: false });
    document.addEventListener("touchstart", onInteraction, { once: false });
    document.addEventListener("keydown", onInteraction, { once: false });
    return () => {
      clearTimeout(timer);
      hasSpokenRef.current = false;
      cleanup();
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
      <section className="relative flex flex-col items-center justify-center min-h-screen px-6 pt-[64px] pb-4
                          hero-gradient overflow-hidden">
        {/* Atmospheric decorative circles */}
        <div className="absolute top-[20%] -left-[100px] w-[300px] h-[300px] rounded-full pointer-events-none"
             style={{ background: "radial-gradient(circle, rgba(var(--clara-blue-rgb),0.04) 0%, transparent 70%)" }} aria-hidden="true" />
        <div className="absolute bottom-[15%] -right-[80px] w-[250px] h-[250px] rounded-full pointer-events-none"
             style={{ background: "radial-gradient(circle, rgba(var(--clara-orange-rgb),0.03) 0%, transparent 70%)" }} aria-hidden="true" />

        <header className="fixed top-0 left-0 right-0 z-20 bg-clara-bg/70 backdrop-blur-md border-b border-clara-border/30">
          <div className="max-w-3xl mx-auto flex items-center justify-between px-4 h-[56px] sm:h-[60px]">
            <button onClick={() => setMenuOpen(true)} aria-label="Abrir menu"
              className="w-11 h-11 sm:w-touch-sm sm:h-touch-sm flex items-center justify-center rounded-xl
                         hover:bg-clara-hover transition-colors flex-shrink-0">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                   strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M3 12h18" /><path d="M3 6h18" /><path d="M3 18h18" />
              </svg>
            </button>

            <div className="flex-1 flex justify-center overflow-hidden mx-2 min-w-0 max-w-[50vw] sm:max-w-none">
              <LanguageBar lang={lang} onChangeLang={handleLangChange} compact />
            </div>

            <div className="flex items-center gap-1 flex-shrink-0">
              <ThemeToggleCompact />
              <div className="flex items-center gap-1.5">
                <svg className="w-5 h-5" viewBox="0 0 80 80" fill="none" aria-hidden="true">
                  <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="var(--color-clara-blue)" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.65" />
                  <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="var(--color-clara-blue)" strokeWidth="4.5" strokeLinecap="round" fill="none" />
                  <circle cx="28" cy="40" r="4" fill="var(--color-clara-orange)" />
                </svg>
                <span className="font-display font-bold text-[15px] text-clara-text hidden sm:inline">Clara</span>
              </div>
            </div>
          </div>
        </header>

        <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} items={MENU_ITEMS[lang]} lang={lang} />

        <div className="relative w-[64px] h-[64px] md:w-[96px] md:h-[96px] flex items-center justify-center mb-2"
             role="img" aria-label="Logo de Clara" style={{ animation: "fadeInUp 0.6s ease-out both" }}>
          <div className="absolute inset-0 rounded-full border-2 border-clara-blue/10" style={{ animation: "logoRipple 3s ease-out infinite" }} />
          <div className="absolute inset-[-12px] rounded-full border border-clara-blue/5" style={{ animation: "logoRipple 3s ease-out 1s infinite" }} />
          <svg className="w-[48px] h-[48px] md:w-[72px] md:h-[72px]" viewBox="0 0 80 80" fill="none" aria-hidden="true">
            <path d="M 28 14 A 30 30 0 0 1 28 66" stroke="var(--color-clara-blue)" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.35" />
            <path d="M 28 23 A 20 20 0 0 1 28 57" stroke="var(--color-clara-blue)" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="0.65" />
            <path d="M 28 32 A 10 10 0 0 1 28 48" stroke="var(--color-clara-blue)" strokeWidth="4.5" strokeLinecap="round" fill="none" opacity="1" />
            <circle cx="28" cy="40" r="5.5" fill="var(--color-clara-orange)" />
          </svg>
        </div>

        <p className="text-body-sm text-clara-text-secondary font-medium mb-1 transition-opacity duration-400"
           style={{ opacity: cycleFade ? 1 : 0, direction: cycled.lang === "ar" ? "rtl" : "ltr", animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.1s" }}
           aria-live="polite" aria-atomic="true">
          {cycled.text}
        </p>

        <h1 className="font-display font-bold leading-[1.08] text-clara-text text-center mb-1 transition-opacity duration-400"
            style={{ fontSize: "clamp(28px, 8vw, 36px)", opacity: cycleFade ? 1 : 0, direction: cycled.lang === "ar" ? "rtl" : "ltr", animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.15s" }}>
          <span className="text-clara-blue">{cycled.tagline[0]}</span><br />
          <span className="text-clara-orange">{cycled.tagline[1]}</span>
        </h1>

        <p className="text-body-sm md:text-body text-clara-text-secondary text-center max-w-[300px] lg:max-w-[480px] mb-3 leading-relaxed"
           style={{ animation: "fadeInUp 0.5s ease-out both", animationDelay: "0.2s" }}>
          {t.description}
        </p>

        <button onClick={() => goToChat("voice")} aria-label={cycled.mic}
          className="w-[80px] h-[80px] md:w-[120px] md:h-[120px] brand-gradient
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
      {/* SECTION 7: DATOS + WHATSAPP                                   */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <DataWhatsAppSection lang={lang} />

      {/* ═══════════════════════════════════════════════════════════════ */}
      {/* SECTION 8: SEGUNDO CTA                                        */}
      {/* ═══════════════════════════════════════════════════════════════ */}
      <section className="section-viewport section-dark section-grain relative w-full flex flex-col items-center justify-center px-6
                          cta-dark-gradient overflow-hidden">
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
                         brand-gradient
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
