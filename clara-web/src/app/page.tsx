"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Button from "@/components/ui/Button";
import LanguageSelector from "@/components/ui/LanguageSelector";

/* ------------------------------------------------------------------ */
/*  Content map: cada idioma tiene su set de textos.                  */
/*  Estructura tipada para que TS avise si falta una key.             */
/* ------------------------------------------------------------------ */
type Lang = "es" | "fr";

interface WelcomeContent {
  tagline: string;
  description: string;
  cta_voice: string;
  cta_text: string;
}

const content: Record<Lang, WelcomeContent> = {
  es: {
    tagline: "Tu voz tiene poder",
    description:
      "Te ayudo con tramites sociales en Espana. Habla o escribe en tu idioma.",
    cta_voice: "Empezar a hablar",
    cta_text: "Prefiero escribir",
  },
  fr: {
    tagline: "Ta voix a du pouvoir",
    description:
      "Je t'aide avec les demarches sociales en Espagne. Parle ou ecris dans ta langue.",
    cta_voice: "Commencer a parler",
    cta_text: "Je prefere ecrire",
  },
};

/* ------------------------------------------------------------------ */
/*  WelcomePage — la primera pantalla que el usuario ve                */
/* ------------------------------------------------------------------ */
export default function WelcomePage() {
  const router = useRouter();
  const [lang, setLang] = useState<Lang>("es");

  const t = content[lang];

  function goToChat(mode: "voice" | "text") {
    router.push(`/chat?lang=${lang}&mode=${mode}`);
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
      {/* ---- ZONA DE IDENTIDAD ---- */}

      {/* Logo placeholder — circulo 120px con "C" */}
      <div
        className="w-[120px] h-[120px] bg-clara-blue rounded-full flex items-center justify-center mb-6"
        role="img"
        aria-label="Logo de Clara"
      >
        <span className="text-white font-display font-bold text-[48px] leading-none select-none">
          C
        </span>
      </div>

      {/* Tagline — lo primero que se lee */}
      <h1 className="font-display font-bold text-h1 text-clara-blue text-center mb-4">
        {t.tagline}
      </h1>

      {/* Descripcion — calida, directa, sin jerga */}
      <p className="text-body text-clara-text-secondary text-center max-w-md mb-8 leading-relaxed">
        {t.description}
      </p>

      {/* ---- ZONA DE CONFIGURACION ---- */}

      {/* Selector de idioma — visible sin scroll */}
      <div className="mb-10">
        <LanguageSelector defaultLang={lang} onChange={setLang} />
      </div>

      {/* ---- ZONA DE ACCION ---- */}

      <div className="w-full max-w-md space-y-4">
        {/* CTA primario — "Empezar a hablar" */}
        <Button
          variant="primary"
          fullWidth
          onPress={() => goToChat("voice")}
          aria-label={t.cta_voice}
          icon={
            <img src="/icons/mic.svg" alt="" width={28} height={28} aria-hidden="true" />
          }
          className="h-[72px] text-[22px]"
        >
          {t.cta_voice}
        </Button>

        {/* CTA secundario — "Prefiero escribir" */}
        <Button
          variant="secondary"
          fullWidth
          onPress={() => goToChat("text")}
          aria-label={t.cta_text}
          icon={
            <img src="/icons/keyboard.svg" alt="" width={28} height={28} aria-hidden="true" />
          }
          className="h-[56px]"
        >
          {t.cta_text}
        </Button>
      </div>
    </div>
  );
}
