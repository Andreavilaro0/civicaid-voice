"use client";

import SubPageLayout from "@/components/welcome/SubPageLayout";
import type { Language } from "@/lib/types";

const roadmap: Record<Language, { icon: string; title: string; desc: string; status: string }[]> = {
  es: [
    { icon: "🗣", title: "Mas idiomas", desc: "Rumano, ucraniano, chino y mas. Clara quiere hablar todos los idiomas de la migracion en Espana.", status: "Proximo" },
    { icon: "📋", title: "Mas tramites", desc: "Asilo, homologacion de titulos, reagrupacion familiar y otros tramites que la comunidad mas necesita.", status: "En desarrollo" },
    { icon: "🤝", title: "Alianzas", desc: "Colaboracion con ayuntamientos, ONGs y servicios sociales para que Clara llegue a mas personas.", status: "Explorando" },
    { icon: "📱", title: "App movil", desc: "Una aplicacion nativa con acceso offline para zonas con mala conexion.", status: "Futuro" },
  ],
  fr: [
    { icon: "🗣", title: "Plus de langues", desc: "Roumain, ukrainien, chinois et plus. Clara veut parler toutes les langues de la migration en Espagne.", status: "Prochain" },
    { icon: "📋", title: "Plus de demarches", desc: "Asile, reconnaissance de diplomes, regroupement familial et d'autres demarches necessaires.", status: "En cours" },
    { icon: "🤝", title: "Partenariats", desc: "Collaboration avec les mairies, ONGs et services sociaux pour que Clara atteigne plus de personnes.", status: "Exploration" },
    { icon: "📱", title: "Application mobile", desc: "Une application native avec acces hors ligne pour les zones avec mauvaise connexion.", status: "Futur" },
  ],
  ar: [
    { icon: "🗣", title: "المزيد من اللغات", desc: "الرومانية والأوكرانية والصينية وغيرها. كلارا تريد التحدث بجميع لغات الهجرة في إسبانيا.", status: "قريبا" },
    { icon: "📋", title: "المزيد من الإجراءات", desc: "اللجوء ومعادلة الشهادات ولم الشمل العائلي وإجراءات أخرى يحتاجها المجتمع.", status: "قيد التطوير" },
    { icon: "🤝", title: "شراكات", desc: "تعاون مع البلديات والمنظمات غير الحكومية والخدمات الاجتماعية لتصل كلارا لمزيد من الأشخاص.", status: "استكشاف" },
    { icon: "📱", title: "تطبيق موبايل", desc: "تطبيق أصلي مع وصول دون اتصال للمناطق ذات الاتصال الضعيف.", status: "المستقبل" },
  ],
  en: [
    { icon: "🗣", title: "More languages", desc: "Romanian, Ukrainian, Chinese and more. Clara wants to speak every migration language in Spain.", status: "Next" },
    { icon: "📋", title: "More procedures", desc: "Asylum, degree recognition, family reunification and other procedures the community needs most.", status: "In development" },
    { icon: "🤝", title: "Partnerships", desc: "Collaboration with city councils, NGOs and social services so Clara reaches more people.", status: "Exploring" },
    { icon: "📱", title: "Mobile app", desc: "A native app with offline access for areas with poor connectivity.", status: "Future" },
  ],
  pt: [
    { icon: "🗣", title: "Mais idiomas", desc: "Romeno, ucraniano, chinês e mais. Clara quer falar todos os idiomas da migração em Espanha.", status: "Próximo" },
    { icon: "📋", title: "Mais procedimentos", desc: "Asilo, reconhecimento de diplomas, reagrupamento familiar e outros procedimentos que a comunidade mais precisa.", status: "Em desenvolvimento" },
    { icon: "🤝", title: "Parcerias", desc: "Colaboração com câmaras municipais, ONGs e serviços sociais para que Clara chegue a mais pessoas.", status: "Explorando" },
    { icon: "📱", title: "App móvel", desc: "Uma aplicação nativa com acesso offline para zonas com má conexão.", status: "Futuro" },
  ],
  ro: [
    { icon: "🗣", title: "Mai multe limbi", desc: "Ucraineană, chineză și altele. Clara vrea să vorbească toate limbile migrației în Spania.", status: "Următor" },
    { icon: "📋", title: "Mai multe proceduri", desc: "Azil, recunoașterea diplomelor, reîntregirea familiei și alte proceduri de care comunitatea are nevoie.", status: "În dezvoltare" },
    { icon: "🤝", title: "Parteneriate", desc: "Colaborare cu primării, ONG-uri și servicii sociale pentru ca Clara să ajungă la mai multe persoane.", status: "Explorare" },
    { icon: "📱", title: "Aplicație mobilă", desc: "O aplicație nativă cu acces offline pentru zonele cu conexiune slabă.", status: "Viitor" },
  ],
  ca: [
    { icon: "🗣", title: "Més idiomes", desc: "Romanès, ucraïnès, xinès i més. Clara vol parlar tots els idiomes de la migració a Espanya.", status: "Proper" },
    { icon: "📋", title: "Més tràmits", desc: "Asil, homologació de títols, reagrupament familiar i altres tràmits que la comunitat més necessita.", status: "En desenvolupament" },
    { icon: "🤝", title: "Aliances", desc: "Col·laboració amb ajuntaments, ONGs i serveis socials perquè Clara arribi a més persones.", status: "Explorant" },
    { icon: "📱", title: "App mòbil", desc: "Una aplicació nativa amb accés offline per a zones amb mala connexió.", status: "Futur" },
  ],
  zh: [
    { icon: "🗣", title: "更多语言", desc: "罗马尼亚语、乌克兰语、中文等。Clara希望能说西班牙移民使用的所有语言。", status: "即将推出" },
    { icon: "📋", title: "更多手续", desc: "庇护、学历认证、家庭团聚及社区最需要的其他手续。", status: "开发中" },
    { icon: "🤝", title: "合作伙伴", desc: "与市政厅、非政府组织和社会服务机构合作，让Clara帮助更多人。", status: "探索中" },
    { icon: "📱", title: "移动应用", desc: "一款支持离线访问的原生应用，适用于网络连接不佳的地区。", status: "未来" },
  ],
};

const statusColors: Record<string, string> = {
  Proximo: "bg-clara-green/10 text-clara-green",
  "En desarrollo": "bg-clara-blue/10 text-clara-blue",
  Explorando: "bg-clara-orange/10 text-clara-orange",
  Futuro: "bg-clara-text-secondary/10 text-clara-text-secondary",
  Prochain: "bg-clara-green/10 text-clara-green",
  "En cours": "bg-clara-blue/10 text-clara-blue",
  Exploration: "bg-clara-orange/10 text-clara-orange",
  Futur: "bg-clara-text-secondary/10 text-clara-text-secondary",
  "قريبا": "bg-clara-green/10 text-clara-green",
  "قيد التطوير": "bg-clara-blue/10 text-clara-blue",
  "استكشاف": "bg-clara-orange/10 text-clara-orange",
  "المستقبل": "bg-clara-text-secondary/10 text-clara-text-secondary",
  // en
  Next: "bg-clara-green/10 text-clara-green",
  "In development": "bg-clara-blue/10 text-clara-blue",
  Exploring: "bg-clara-orange/10 text-clara-orange",
  Future: "bg-clara-text-secondary/10 text-clara-text-secondary",
  // pt
  "Próximo": "bg-clara-green/10 text-clara-green",
  "Em desenvolvimento": "bg-clara-blue/10 text-clara-blue",
  // pt "Explorando" already matches es
  // pt "Futuro" already matches ca/fr
  // ro
  "Următor": "bg-clara-green/10 text-clara-green",
  "În dezvoltare": "bg-clara-blue/10 text-clara-blue",
  Explorare: "bg-clara-orange/10 text-clara-orange",
  Viitor: "bg-clara-text-secondary/10 text-clara-text-secondary",
  // ca
  Proper: "bg-clara-green/10 text-clara-green",
  "En desenvolupament": "bg-clara-blue/10 text-clara-blue",
  Explorant: "bg-clara-orange/10 text-clara-orange",
  // ca "Futur" already matches fr
  // zh
  "即将推出": "bg-clara-green/10 text-clara-green",
  "开发中": "bg-clara-blue/10 text-clara-blue",
  "探索中": "bg-clara-orange/10 text-clara-orange",
  "未来": "bg-clara-text-secondary/10 text-clara-text-secondary",
};

export default function FuturoPage() {
  return (
    <SubPageLayout slug="futuro">
      {(lang) => (
        <div className="flex flex-col gap-4">
          {roadmap[lang].map((item) => (
            <div
              key={item.title}
              className="flex items-start gap-4 p-5 bg-white dark:bg-[#1a1f26] rounded-2xl shadow-warm"
            >
              <span className="text-[32px] flex-shrink-0" aria-hidden="true">
                {item.icon}
              </span>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <h2 className="font-display font-bold text-body text-clara-text dark:text-[#e8e8ee]">
                    {item.title}
                  </h2>
                  <span className={`text-label px-2 py-0.5 rounded-full font-medium ${statusColors[item.status] ?? ""}`}>
                    {item.status}
                  </span>
                </div>
                <p className="text-body-sm text-clara-text-secondary leading-relaxed">
                  {item.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </SubPageLayout>
  );
}
