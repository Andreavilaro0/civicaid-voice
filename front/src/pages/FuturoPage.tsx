import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";

const roadmap: Record<Language, { icon: string; title: string; desc: string; status: string }[]> = {
  es: [
    { icon: "\u{1F5E3}", title: "Mas idiomas", desc: "Rumano, ucraniano, chino y mas. Clara quiere hablar todos los idiomas de la migracion en Espana.", status: "Proximo" },
    { icon: "\u{1F4CB}", title: "Mas tramites", desc: "Asilo, homologacion de titulos, reagrupacion familiar y otros tramites que la comunidad mas necesita.", status: "En desarrollo" },
    { icon: "\u{1F91D}", title: "Alianzas", desc: "Colaboracion con ayuntamientos, ONGs y servicios sociales para que Clara llegue a mas personas.", status: "Explorando" },
    { icon: "\u{1F4F1}", title: "App movil", desc: "Una aplicacion nativa con acceso offline para zonas con mala conexion.", status: "Futuro" },
  ],
  fr: [
    { icon: "\u{1F5E3}", title: "Plus de langues", desc: "Roumain, ukrainien, chinois et plus. Clara veut parler toutes les langues de la migration en Espagne.", status: "Prochain" },
    { icon: "\u{1F4CB}", title: "Plus de demarches", desc: "Asile, reconnaissance de diplomes, regroupement familial et d'autres demarches necessaires.", status: "En cours" },
    { icon: "\u{1F91D}", title: "Partenariats", desc: "Collaboration avec les mairies, ONGs et services sociaux pour que Clara atteigne plus de personnes.", status: "Exploration" },
    { icon: "\u{1F4F1}", title: "Application mobile", desc: "Une application native avec acces hors ligne pour les zones avec mauvaise connexion.", status: "Futur" },
  ],
  ar: [
    { icon: "\u{1F5E3}", title: "المزيد من اللغات", desc: "الرومانية والأوكرانية والصينية وغيرها. كلارا تريد التحدث بجميع لغات الهجرة في إسبانيا.", status: "قريبا" },
    { icon: "\u{1F4CB}", title: "المزيد من الإجراءات", desc: "اللجوء ومعادلة الشهادات ولم الشمل العائلي وإجراءات أخرى يحتاجها المجتمع.", status: "قيد التطوير" },
    { icon: "\u{1F91D}", title: "شراكات", desc: "تعاون مع البلديات والمنظمات غير الحكومية والخدمات الاجتماعية لتصل كلارا لمزيد من الأشخاص.", status: "استكشاف" },
    { icon: "\u{1F4F1}", title: "تطبيق موبايل", desc: "تطبيق أصلي مع وصول دون اتصال للمناطق ذات الاتصال الضعيف.", status: "المستقبل" },
  ],
};

const statusColors: Record<string, string> = {
  Proximo: "bg-clara-green/10 text-clara-green", "En desarrollo": "bg-clara-blue/10 text-clara-blue",
  Explorando: "bg-clara-orange/10 text-clara-orange", Futuro: "bg-clara-text-secondary/10 text-clara-text-secondary",
  Prochain: "bg-clara-green/10 text-clara-green", "En cours": "bg-clara-blue/10 text-clara-blue",
  Exploration: "bg-clara-orange/10 text-clara-orange", Futur: "bg-clara-text-secondary/10 text-clara-text-secondary",
  "قريبا": "bg-clara-green/10 text-clara-green", "قيد التطوير": "bg-clara-blue/10 text-clara-blue",
  "استكشاف": "bg-clara-orange/10 text-clara-orange", "المستقبل": "bg-clara-text-secondary/10 text-clara-text-secondary",
};

export default function FuturoPage() {
  return (
    <SubPageLayout slug="futuro">
      {(lang) => (
        <div className="flex flex-col gap-4">
          {roadmap[lang].map((item) => (
            <div key={item.title} className="flex items-start gap-4 p-5 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm">
              <span className="text-[32px] flex-shrink-0" aria-hidden="true">{item.icon}</span>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <h2 className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee]">{item.title}</h2>
                  <span className={`text-label px-2 py-0.5 rounded-full font-medium ${statusColors[item.status] ?? ""}`}>{item.status}</span>
                </div>
                <p className="text-body-sm text-clara-text-secondary leading-relaxed">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </SubPageLayout>
  );
}
