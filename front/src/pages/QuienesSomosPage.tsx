import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";

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
};

const teamMembers: Record<Language, { name: string; role: string }[]> = {
  es: [
    { name: "Robert", role: "Backend lead, pipeline y presentacion" },
    { name: "Marcos", role: "Routes, Twilio, deploy y audio" },
    { name: "Lucas", role: "Investigacion KB, testing y demo" },
    { name: "Daniel", role: "Web y video" },
    { name: "Andrea", role: "Notion, slides y coordinacion" },
  ],
  fr: [
    { name: "Robert", role: "Backend lead, pipeline et présentation" },
    { name: "Marcos", role: "Routes, Twilio, déploiement et audio" },
    { name: "Lucas", role: "Recherche KB, tests et démo" },
    { name: "Daniel", role: "Web et vidéo" },
    { name: "Andrea", role: "Notion, slides et coordination" },
  ],
  ar: [
    { name: "Robert", role: "قيادة الخلفية، خط الأنابيب والعرض" },
    { name: "Marcos", role: "المسارات، Twilio، النشر والصوت" },
    { name: "Lucas", role: "بحث قاعدة المعرفة، الاختبار والعرض التجريبي" },
    { name: "Daniel", role: "الويب والفيديو" },
    { name: "Andrea", role: "Notion، العروض والتنسيق" },
  ],
};

const missionStatement: Record<Language, { title: string; body: string }> = {
  es: {
    title: "Nuestra misión",
    body: "Creemos que entender tus derechos no debería ser un privilegio. Clara existe para que 4.5 millones de personas vulnerables en España puedan acceder a las ayudas que les corresponden, sin importar el idioma que hablen.",
  },
  fr: {
    title: "Notre mission",
    body: "Nous croyons que comprendre tes droits ne devrait pas être un privilège. Clara existe pour que 4,5 millions de personnes vulnérables en Espagne puissent accéder aux aides auxquelles elles ont droit, quelle que soit leur langue.",
  },
  ar: {
    title: "مهمتنا",
    body: "نؤمن بأن فهم حقوقك لا ينبغي أن يكون امتيازاً. كلارا موجودة لكي يتمكن 4.5 مليون شخص ضعيف في إسبانيا من الحصول على المساعدات التي يستحقونها، بغض النظر عن اللغة التي يتحدثونها.",
  },
};

export default function QuienesSomosPage() {
  return (
    <SubPageLayout slug="quienes-somos">
      {(lang) => (
        <div className="flex flex-col gap-8">
          {/* Brand story */}
          <div className="p-6 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm">
            <h2 className="font-display font-bold text-h2 text-clara-blue mb-3">{brandStory[lang].title}</h2>
            <p className="text-body text-clara-text-secondary leading-relaxed">{brandStory[lang].body}</p>
          </div>

          {/* Mission */}
          <div className="p-6 bg-[#F0F7FA] dark:bg-[#141a20] rounded-2xl">
            <h2 className="font-display font-bold text-h2 text-clara-text dark:text-[#e8e8ee] mb-3">{missionStatement[lang].title}</h2>
            <p className="text-body text-clara-text-secondary leading-relaxed">{missionStatement[lang].body}</p>
          </div>

          {/* Team */}
          <div>
            <h2 className="font-display font-bold text-h2 text-clara-text dark:text-[#e8e8ee] mb-4 text-center">
              {lang === "ar" ? "الفريق" : lang === "fr" ? "L'équipe" : "El equipo"}
            </h2>
            <div className="flex flex-col gap-3">
              {teamMembers[lang].map((member) => (
                <div
                  key={member.name}
                  className="flex items-center gap-4 p-4 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm"
                >
                  <span className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-clara-blue/10 text-clara-blue font-display font-bold text-h2">
                    {member.name[0]}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee]">{member.name}</p>
                    <p className="text-body-sm text-clara-text-secondary">{member.role}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </SubPageLayout>
  );
}
