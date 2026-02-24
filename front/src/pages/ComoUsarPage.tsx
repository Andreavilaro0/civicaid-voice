import SubPageLayout from "@/components/welcome/SubPageLayout";
import HeroSection from "@/components/como-usar/HeroSection";
import BentoGrid from "@/components/como-usar/BentoGrid";
import QuickHelpSection from "@/components/como-usar/QuickHelpSection";
import TrustCTASection from "@/components/como-usar/TrustCTASection";
import FloatingDock from "@/components/como-usar/FloatingDock";

export default function ComoUsarPage() {
  return (
    <SubPageLayout slug="como-usar" fullBleed>
      {(lang, setLang) => (
        <>
          <HeroSection lang={lang} />
          <BentoGrid lang={lang} />
          <QuickHelpSection lang={lang} />
          <TrustCTASection lang={lang} />
          <FloatingDock lang={lang} setLang={setLang} />
        </>
      )}
    </SubPageLayout>
  );
}
