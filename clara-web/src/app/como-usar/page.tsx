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
  en: [
    { icon: "1", title: "Open Clara", desc: "Access it from your phone or computer. No download needed." },
    { icon: "2", title: "Choose your language", desc: "Clara speaks Spanish, French and Arabic. Select yours at the top." },
    { icon: "3", title: "Speak or type", desc: "Press the microphone to speak, or type your question in the bar." },
    { icon: "4", title: "Get your answer", desc: "Clara explains step by step, with official links and in your language." },
  ],
  pt: [
    { icon: "1", title: "Abre a Clara", desc: "Acede a partir do teu telemovel ou computador. Nao precisas de descarregar nada." },
    { icon: "2", title: "Escolhe o teu idioma", desc: "A Clara fala espanhol, frances e arabe. Seleciona o teu no topo." },
    { icon: "3", title: "Fala ou escreve", desc: "Carrega no microfone para falar, ou escreve a tua pergunta na barra." },
    { icon: "4", title: "Recebe a tua resposta", desc: "A Clara explica-te passo a passo, com links oficiais e no teu idioma." },
  ],
  ro: [
    { icon: "1", title: "Deschide Clara", desc: "Acceseaza de pe telefonul sau calculatorul tau. Nu trebuie sa descarci nimic." },
    { icon: "2", title: "Alege limba ta", desc: "Clara vorbeste spaniola, franceza si araba. Selecteaza limba ta sus." },
    { icon: "3", title: "Vorbeste sau scrie", desc: "Apasa pe microfon pentru a vorbi, sau scrie intrebarea ta in bara." },
    { icon: "4", title: "Primeste raspunsul tau", desc: "Clara iti explica pas cu pas, cu linkuri oficiale si in limba ta." },
  ],
  ca: [
    { icon: "1", title: "Obre Clara", desc: "Entra des del teu mobil o ordinador. No cal descarregar res." },
    { icon: "2", title: "Tria el teu idioma", desc: "Clara parla castella, frances i arab. Selecciona el teu a dalt." },
    { icon: "3", title: "Parla o escriu", desc: "Prem el microfon per parlar, o escriu la teva pregunta a la barra." },
    { icon: "4", title: "Rep la teva resposta", desc: "Clara t'explica pas a pas, amb enllacos oficials i en el teu idioma." },
  ],
  zh: [
    { icon: "1", title: "打开Clara", desc: "从手机或电脑访问，无需下载任何内容。" },
    { icon: "2", title: "选择你的语言", desc: "Clara支持西班牙语、法语和阿拉伯语。在顶部选择你的语言。" },
    { icon: "3", title: "说话或输入", desc: "按下麦克风说话，或在栏中输入你的问题。" },
    { icon: "4", title: "获取你的回答", desc: "Clara会一步步为你解释，提供官方链接，并使用你的语言。" },
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
      en: "Step 1: open Clara from your device",
      pt: "Passo 1: abre a Clara a partir do teu dispositivo",
      ro: "Pasul 1: deschide Clara de pe dispozitivul tau",
      ca: "Pas 1: obre Clara des del teu dispositiu",
      zh: "第1步：从你的设备打开Clara",
    },
  },
  {
    src: "/media/steps/step-2-language.png",
    alt: {
      es: "Paso 2: elige tu idioma preferido",
      fr: "Étape 2 : choisis ta langue préférée",
      ar: "الخطوة 2: اختر لغتك المفضلة",
      en: "Step 2: choose your preferred language",
      pt: "Passo 2: escolhe o teu idioma preferido",
      ro: "Pasul 2: alege limba ta preferata",
      ca: "Pas 2: tria el teu idioma preferit",
      zh: "第2步：选择你的首选语言",
    },
  },
  {
    src: "/media/steps/step-3-speak.png",
    alt: {
      es: "Paso 3: habla o escribe tu pregunta",
      fr: "Étape 3 : parle ou écris ta question",
      ar: "الخطوة 3: تحدث أو اكتب سؤالك",
      en: "Step 3: speak or type your question",
      pt: "Passo 3: fala ou escreve a tua pergunta",
      ro: "Pasul 3: vorbeste sau scrie intrebarea ta",
      ca: "Pas 3: parla o escriu la teva pregunta",
      zh: "第3步：说出或输入你的问题",
    },
  },
  {
    src: "/media/steps/step-4-response.png",
    alt: {
      es: "Paso 4: recibe tu respuesta con links oficiales",
      fr: "Étape 4 : reçois ta réponse avec des liens officiels",
      ar: "الخطوة 4: احصل على إجابتك مع روابط رسمية",
      en: "Step 4: get your answer with official links",
      pt: "Passo 4: recebe a tua resposta com links oficiais",
      ro: "Pasul 4: primeste raspunsul tau cu linkuri oficiale",
      ca: "Pas 4: rep la teva resposta amb enllacos oficials",
      zh: "第4步：获取带有官方链接的回答",
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
                  : lang === "ar"
                  ? "فيديو تعليمي: كيفية استخدام كلارا"
                  : lang === "en"
                  ? "Video tutorial: how to use Clara"
                  : lang === "pt"
                  ? "Video tutorial: como usar a Clara"
                  : lang === "ro"
                  ? "Tutorial video: cum sa folosesti Clara"
                  : lang === "ca"
                  ? "Video tutorial: com fer servir Clara"
                  : "视频教程：如何使用Clara"
              }
            >
              <source src="/media/video/como-usar-clara.mp4" type="video/mp4" />
              <p className="p-4 text-center text-clara-text-secondary">
                {lang === "es"
                  ? "Tu navegador no soporta video. "
                  : lang === "fr"
                  ? "Votre navigateur ne supporte pas la vidéo. "
                  : lang === "ar"
                  ? "متصفحك لا يدعم الفيديو. "
                  : lang === "en"
                  ? "Your browser does not support video. "
                  : lang === "pt"
                  ? "O teu navegador nao suporta video. "
                  : lang === "ro"
                  ? "Browserul tau nu suporta video. "
                  : lang === "ca"
                  ? "El teu navegador no suporta video. "
                  : "你的浏览器不支持视频。"}
                <a
                  href="/media/video/como-usar-clara.mp4"
                  className="text-clara-blue underline"
                >
                  {lang === "es"
                    ? "Descargar video"
                    : lang === "fr"
                    ? "Télécharger la vidéo"
                    : lang === "ar"
                    ? "تحميل الفيديو"
                    : lang === "en"
                    ? "Download video"
                    : lang === "pt"
                    ? "Descarregar video"
                    : lang === "ro"
                    ? "Descarca videoul"
                    : lang === "ca"
                    ? "Descarrega el video"
                    : "下载视频"}
                </a>
              </p>
            </video>
          </div>
        </div>
      )}
    </SubPageLayout>
  );
}
