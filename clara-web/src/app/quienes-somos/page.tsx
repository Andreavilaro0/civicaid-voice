"use client";

import Image from "next/image";
import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";
import { IMPACT, PERSONAS, BEFORE_AFTER } from "@/lib/i18n";
import SvgDefs from "@/components/SvgDefs";

const brandStory: Record<Language, { title: string; body: string }> = {
  es: {
    title: "La historia de Clara",
    body: "Clara nacio en un hackathon de OdiseIA4Good con una mision: que nadie se quede sin acceder a una ayuda social por no entender el idioma o la burocracia. Somos un equipo de 5 personas que creen que la tecnologia debe servir a quien mas la necesita.",
  },
  fr: {
    title: "L'histoire de Clara",
    body: "Clara est nee lors d'un hackathon OdiseIA4Good avec une mission: que personne ne soit prive d'aide sociale parce qu'il ne comprend pas la langue ou la bureaucratie. Nous sommes une equipe de 5 personnes qui croient que la technologie doit servir ceux qui en ont le plus besoin.",
  },
  ar: {
    title: "قصة كلارا",
    body: "وُلدت كلارا في هاكاثون OdiseIA4Good بمهمة واحدة: ألا يُحرم أي شخص من المساعدات الاجتماعية لأنه لا يفهم اللغة أو البيروقراطية. نحن فريق من 5 أشخاص يؤمنون بأن التكنولوجيا يجب أن تخدم من يحتاجها أكثر.",
  },
  en: {
    title: "The story of Clara",
    body: "Clara was born at an OdiseIA4Good hackathon with one mission: that no one should miss out on social aid because they don't understand the language or the bureaucracy. We are a team of 5 people who believe technology should serve those who need it most.",
  },
  pt: {
    title: "A história de Clara",
    body: "Clara nasceu num hackathon OdiseIA4Good com uma missão: que ninguém fique sem aceder a uma ajuda social por não entender o idioma ou a burocracia. Somos uma equipa de 5 pessoas que acreditam que a tecnologia deve servir quem mais precisa.",
  },
  ro: {
    title: "Povestea Clarei",
    body: "Clara s-a născut la un hackathon OdiseIA4Good cu o misiune: nimeni să nu fie privat de ajutor social pentru că nu înțelege limba sau birocrația. Suntem o echipă de 5 persoane care cred că tehnologia trebuie să îi servească pe cei care au cea mai mare nevoie.",
  },
  ca: {
    title: "La història de Clara",
    body: "Clara va néixer en un hackathon d'OdiseIA4Good amb una missió: que ningú es quedi sense accedir a una ajuda social per no entendre l'idioma o la burocràcia. Som un equip de 5 persones que creuen que la tecnologia ha de servir a qui més la necessita.",
  },
  zh: {
    title: "Clara的故事",
    body: "Clara诞生于OdiseIA4Good黑客马拉松，带着一个使命：不让任何人因为语言障碍或繁琐的行政流程而错失社会援助。我们是一个5人团队，坚信技术应当服务于最需要它的人。",
  },
};

export default function QuienesSomosPage() {
  return (
    <SubPageLayout slug="quienes-somos">
      {(lang) => (
        <div className="flex flex-col gap-8">
          <SvgDefs />

          {/* Impact counter */}
          <div className="text-center p-6 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm">
            <div className="impact-counter mb-2">4.5M</div>
            <p className="text-body text-clara-text-secondary leading-relaxed max-w-md mx-auto">
              {IMPACT[lang].counter_label}
            </p>
          </div>

          {/* Personas */}
          <div className="flex flex-col gap-3">
            {PERSONAS.map((persona) => {
              const colors: Record<string, string> = {
                maria: "border-l-clara-orange",
                ahmed: "border-l-clara-blue",
                fatima: "border-l-clara-green",
              };
              return (
                <div
                  key={persona.id}
                  className={`persona-chip border-l-4 ${colors[persona.id] ?? "border-l-clara-blue"}`}
                >
                  <Image
                    src={`/media/personas/${persona.id}.png`}
                    alt={persona.name}
                    width={64}
                    height={64}
                    className="w-16 h-16 rounded-full object-cover flex-shrink-0"
                    loading="lazy"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-display font-bold text-body-sm text-clara-text dark:text-[#e8e8ee]">
                      {persona.name}
                    </p>
                    <p className="text-label text-clara-text-secondary italic leading-snug">
                      {persona.quote[lang]}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Before / After */}
          <div>
            <div className="flex gap-4 mb-3">
              <span className="flex-1 text-center font-display font-bold text-body-sm text-clara-orange">
                {IMPACT[lang].before_label}
              </span>
              <span className="flex-1 text-center font-display font-bold text-body-sm text-clara-green">
                {IMPACT[lang].after_label}
              </span>
            </div>
            <div className="before-after-grid">
              {BEFORE_AFTER[lang].slice(0, 2).map((row, i) => (
                <div key={i} className="contents">
                  <div className="before-cell">{row.before}</div>
                  <div className="after-cell">{row.after}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Brand story */}
          <div className="p-6 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm">
            <h2 className="font-display font-bold text-h2 text-clara-blue mb-3">
              {brandStory[lang].title}
            </h2>
            <p className="text-body text-clara-text-secondary leading-relaxed">
              {brandStory[lang].body}
            </p>
          </div>
        </div>
      )}
    </SubPageLayout>
  );
}
