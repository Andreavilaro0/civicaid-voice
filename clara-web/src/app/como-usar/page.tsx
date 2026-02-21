"use client";

import Image from "next/image";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";

const steps: Record<Language, { icon: string; title: string; desc: string }[]> = {
  es: [
    { icon: "1", title: "Abre Clara", desc: "Entra desde tu movil o computadora. No necesitas descargar nada." },
    { icon: "2", title: "Elige tu idioma", desc: "Clara habla espanol, frances y arabe. Selecciona el tuyo arriba." },
    { icon: "3", title: "Habla o escribe", desc: "Pulsa el microfono para hablar, o escribe tu pregunta en la barra." },
    { icon: "4", title: "Recibe tu respuesta", desc: "Clara te explica paso a paso, con links oficiales y en tu idioma." },
  ],
  fr: [
    { icon: "1", title: "Ouvre Clara", desc: "Entre depuis ton portable ou ordinateur. Pas besoin de telecharger." },
    { icon: "2", title: "Choisis ta langue", desc: "Clara parle espagnol, francais et arabe. Selectionne la tienne." },
    { icon: "3", title: "Parle ou ecris", desc: "Appuie sur le micro pour parler, ou ecris ta question dans la barre." },
    { icon: "4", title: "Recois ta reponse", desc: "Clara t'explique etape par etape, avec des liens officiels et dans ta langue." },
  ],
  ar: [
    { icon: "1", title: "افتح كلارا", desc: "ادخل من هاتفك أو حاسوبك. لا تحتاج تحميل أي شيء." },
    { icon: "2", title: "اختر لغتك", desc: "كلارا تتحدث الإسبانية والفرنسية والعربية. اختر لغتك في الأعلى." },
    { icon: "3", title: "تحدث أو اكتب", desc: "اضغط على الميكروفون للتحدث، أو اكتب سؤالك في الشريط." },
    { icon: "4", title: "احصل على إجابتك", desc: "كلارا تشرح لك خطوة بخطوة، مع روابط رسمية وبلغتك." },
  ],
};

// Step image filenames and per-language alt text
const stepImages: {
  src: string;
  alt: Record<Language, string>;
}[] = [
  {
    src: "/media/steps/step-1-open.png",
    alt: {
      es: "Paso 1: abre Clara desde tu dispositivo",
      fr: "Étape 1 : ouvre Clara depuis ton appareil",
      ar: "الخطوة 1: افتح كلارا من جهازك",
    },
  },
  {
    src: "/media/steps/step-2-language.png",
    alt: {
      es: "Paso 2: elige tu idioma preferido",
      fr: "Étape 2 : choisis ta langue préférée",
      ar: "الخطوة 2: اختر لغتك المفضلة",
    },
  },
  {
    src: "/media/steps/step-3-speak.png",
    alt: {
      es: "Paso 3: habla o escribe tu pregunta",
      fr: "Étape 3 : parle ou écris ta question",
      ar: "الخطوة 3: تحدث أو اكتب سؤالك",
    },
  },
  {
    src: "/media/steps/step-4-response.png",
    alt: {
      es: "Paso 4: recibe tu respuesta con links oficiales",
      fr: "Étape 4 : reçois ta réponse avec des liens officiels",
      ar: "الخطوة 4: احصل على إجابتك مع روابط رسمية",
    },
  },
];

export default function ComoUsarPage() {
  return (
    <SubPageLayout slug="como-usar">
      {(lang) => (
        <div className="flex flex-col gap-8">
          {/* Steps */}
          <div className="flex flex-col gap-4">
            {steps[lang].map((step, index) => {
              const image = stepImages[index];
              return (
                <div
                  key={step.icon}
                  className="bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm overflow-hidden"
                >
                  <Image
                    src={image.src}
                    alt={image.alt[lang]}
                    width={800}
                    height={533}
                    className="w-full h-48 object-cover"
                    loading="lazy"
                  />
                  <div className="flex items-start gap-4 p-5">
                    <div className="flex-shrink-0 w-12 h-12 bg-clara-blue text-white rounded-full
                                   flex items-center justify-center font-display font-bold text-h2">
                      {step.icon}
                    </div>
                    <div className="flex-1">
                      <h2 className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee] mb-1">
                        {step.title}
                      </h2>
                      <p className="text-body-sm text-clara-text-secondary leading-relaxed">
                        {step.desc}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Video tutorial */}
          <div className="rounded-2xl overflow-hidden shadow-warm bg-white">
            <video
              controls
              preload="metadata"
              poster="/media/steps/step-1-open.png"
              className="w-full aspect-video"
              aria-label={
                lang === "es"
                  ? "Video tutorial: cómo usar Clara"
                  : lang === "fr"
                  ? "Vidéo tutoriel: comment utiliser Clara"
                  : "فيديو تعليمي: كيفية استخدام كلارا"
              }
            >
              <source src="/media/video/como-usar-clara.mp4" type="video/mp4" />
              <p className="p-4 text-center text-clara-text-secondary">
                {lang === "es"
                  ? "Tu navegador no soporta video. "
                  : lang === "fr"
                  ? "Votre navigateur ne supporte pas la vidéo. "
                  : "متصفحك لا يدعم الفيديو. "}
                <a
                  href="/media/video/como-usar-clara.mp4"
                  className="text-clara-blue underline"
                >
                  {lang === "es"
                    ? "Descargar video"
                    : lang === "fr"
                    ? "Télécharger la vidéo"
                    : "تحميل الفيديو"}
                </a>
              </p>
            </video>
          </div>
        </div>
      )}
    </SubPageLayout>
  );
}
