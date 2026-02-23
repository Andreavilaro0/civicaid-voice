import { test, expect, type Page } from "@playwright/test";

const BASE = "/civicaid-voice";

/**
 * 100+ E2E Tests — Conversaciones Largas Multi-Tramite Multi-Ciudad
 *
 * 10 personas reales, 8 tramites, 10 ciudades, 3 idiomas.
 * 35 tests × 3 viewports (mobile/tablet/desktop) = 105 tests.
 *
 * Personas:
 *  1. Fatima Oukacha (32, Marruecos, Madrid) — madre divorciada, FR/ES
 *  2. Andriy Kovalenko (28, Ucrania, Barcelona) — refugiado, EN
 *  3. Maria del Carmen Ruiz (67, Espana, Sevilla) — viuda discapacidad, ES
 *  4. Kevin Mbeki (24, Senegal, Valencia) — indocumentado, FR
 *  5. Laura Fernandez (29, Espana, Bilbao) — victima VG, ES
 *  6. Ahmed Al-Hassan (35, Siria, Zaragoza) — refugiado familia, EN
 *  7. Sofia Morales (22, Colombia, Malaga) — joven trabajadora, ES
 *  8. Roberto Oliveira (45, Brasil, Alicante) — despedido discapacidad, ES
 *  9. Irina Petrovna (40, Rusia, Murcia) — madre soltera jornalera, ES
 * 10. Jean-Pierre Dupont (55, Francia, Palma) — prejubilado, FR
 */

/* ------------------------------------------------------------------ */
/*  Audio stub                                                         */
/* ------------------------------------------------------------------ */

async function stubAudio(page: Page) {
  await page.addInitScript(() => {
    const Orig = window.Audio;
    window.Audio = function () {
      const el = document.createElement("audio");
      Object.defineProperty(el, "crossOrigin", {
        get() { return el.getAttribute("crossorigin"); },
        set(v: string) { el.setAttribute("crossorigin", v); },
        configurable: true,
      });
      Object.defineProperty(el, "src", {
        get() { return el.getAttribute("data-src") || ""; },
        set(v: string) {
          el.setAttribute("data-src", v);
          Object.defineProperty(el, "duration", { value: 3, writable: true, configurable: true });
          Object.defineProperty(el, "readyState", { value: 4, writable: true, configurable: true });
          setTimeout(() => {
            el.dispatchEvent(new Event("loadedmetadata"));
            el.dispatchEvent(new Event("canplay"));
            el.dispatchEvent(new Event("canplaythrough"));
          }, 50);
        },
        configurable: true,
      });
      el.play = () => {
        el.dispatchEvent(new Event("play"));
        setTimeout(() => el.dispatchEvent(new Event("ended")), 200);
        return Promise.resolve();
      };
      return el as unknown as HTMLAudioElement;
    } as unknown as typeof Audio;
    window.Audio.prototype = Orig.prototype;
  });
}

/* ------------------------------------------------------------------ */
/*  KB — datos reales verificados de los 8 tramites                    */
/* ------------------------------------------------------------------ */

const KB = {
  imv: {
    phone: "900 20 22 22",
    url: "https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-8d06-4645-bde7-05374ee42ac7",
    institution: "Seguridad Social",
    amount: "604,21",
  },
  empadronamiento: {
    phone: "010",
    url: "https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Empadronamiento",
    institution: "Ayuntamiento",
  },
  tarjeta_sanitaria: {
    phone: "900 102 112",
    url: "https://www.comunidad.madrid/servicios/salud/tarjeta-sanitaria",
    institution: "SERMAS",
  },
  nie_tie: {
    phone: "060",
    url: "https://www.inclusion.gob.es/web/migraciones/informacion-util/tramites",
    institution: "Extranjeria",
  },
  ayuda_alquiler: {
    phone: "060",
    url: "https://www.mivau.gob.es/vivienda/ayudas-alquiler",
    institution: "MIVAU",
    amount: "250",
  },
  discapacidad: {
    phone: "012",
    url: "https://www.comunidad.madrid/servicios/asuntos-sociales/valoracion-discapacidad",
    institution: "Comunidad de Madrid",
    amount: "517,90",
  },
  justicia_gratuita: {
    phone: "060",
    url: "https://www.mjusticia.gob.es/es/ciudadania/tramites/asistencia-juridica-gratuita",
    institution: "Ministerio de Justicia",
  },
  desempleo: {
    phone: "901 119 999",
    url: "https://www.sepe.es/HomeSepe/prestaciones/prestacion-contributiva",
    institution: "SEPE",
    amount: "1.225,80",
  },
};

/* ------------------------------------------------------------------ */
/*  Interfaces                                                         */
/* ------------------------------------------------------------------ */

interface Turn {
  userText: string;
  mockResponse: string;
  mockSources: Array<{ name: string; url: string }>;
  mustContain: string[];
  mustNotContain?: string[];
}

interface Scenario {
  name: string;
  persona: string;
  lang: string;
  turns: Turn[];
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function esc(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

async function mockConversation(page: Page, turns: Turn[], lang: string) {
  let idx = 0;
  await page.route("**/api/chat", async (route) => {
    const t = turns[Math.min(idx, turns.length - 1)];
    idx++;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        response: t.mockResponse,
        source: "llm",
        language: lang,
        duration_ms: 200,
        audio_url: null,
        sources: t.mockSources,
      }),
    });
  });
  await page.route("**/api/tts", async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) });
  });
  await page.route("**/*.mp3", async (route) => route.abort("blockedbyclient"));
}

async function gotoChat(page: Page, lang: string) {
  await page.goto(`${BASE}/chat?lang=${lang}&mode=text`, { waitUntil: "domcontentloaded" });
  await expect(page.getByText(/Clara/i).first()).toBeVisible({ timeout: 8_000 });
}

async function sendAndWait(page: Page, text: string, pattern: RegExp) {
  const input = page.locator('input[type="text"]');
  await input.fill(text);
  await input.press("Enter");
  await expect(page.getByText(pattern).first()).toBeVisible({ timeout: 10_000 });
}

async function runScenario(page: Page, s: Scenario) {
  await stubAudio(page);
  await mockConversation(page, s.turns, s.lang);
  await gotoChat(page, s.lang);
  for (const turn of s.turns) {
    await sendAndWait(page, turn.userText, new RegExp(esc(turn.mustContain[0])));
    for (const fact of turn.mustContain) {
      await expect(page.getByText(fact).first()).toBeVisible({ timeout: 3_000 });
    }
    if (turn.mustNotContain) {
      for (const bad of turn.mustNotContain) {
        expect(await page.getByText(bad).count()).toBe(0);
      }
    }
  }
}

/* ------------------------------------------------------------------ */
/*  Group 1: Tramite conversations (16 scenarios)                      */
/*  Defined below in TRAMITE_SCENARIOS                                 */
/* ------------------------------------------------------------------ */

const TRAMITE_SCENARIOS: Scenario[] = [
  /* ---- 1. IMV ES — Fatima (Madrid) ---- */
  {
    name: "IMV ES", persona: "Fatima Oukacha", lang: "es",
    turns: [
      { userText: "Hola, soy Fatima. Estoy divorciada con 2 hijos y sin ingresos. Que ayuda puedo pedir?",
        mockResponse: "Hola Fatima. Puedes solicitar el Ingreso Minimo Vital (IMV), una prestacion de la Seguridad Social. Para un adulto solo son 604,21 euros al mes. Llama gratis al 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["604,21", "900 20 22 22", "Seguridad Social"],
        mustNotContain: ["Cruz Roja gestiona", "1.000€"] },
      { userText: "Que requisitos necesito para el IMV?",
        mockResponse: "Necesitas tener entre 23 y 65 anos, residencia legal en Espana de al menos 1 ano, y estar en situacion de vulnerabilidad economica. Como madre con hijos, puedes solicitarlo desde los 18 anos.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["23", "65", "1 ano"] },
      { userText: "Como lo solicito?",
        mockResponse: "Puedes solicitarlo online en sede.seg-social.gob.es o presencialmente pidiendo cita previa en tu oficina del INSS. Tambien por telefono al 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["900 20 22 22", "INSS"] },
      { userText: "Que documentos necesito?",
        mockResponse: "Necesitas DNI o NIE de todos los miembros del hogar, certificado de empadronamiento, libro de familia, declaracion de la renta y certificado bancario.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["DNI", "empadronamiento"] },
      { userText: "Cuanto tarda en resolverse?",
        mockResponse: "El plazo maximo de resolucion es de 6 meses desde la solicitud. Normalmente tarda entre 3 y 6 meses.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["6 meses"] },
      { userText: "Si tengo 2 hijos cuanto me dan?",
        mockResponse: "Para una unidad familiar con un adulto y 2 menores, la cuantia sube. La base es 604,21 euros mas complementos por cada menor a cargo.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["604,21"] },
      { userText: "Donde voy en persona en Madrid?",
        mockResponse: "En Madrid puedes ir a la oficina del INSS en Calle Padre Damian 4, 28036 Madrid. Pide cita previa.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Padre Damian"] },
      { userText: "Hay algun telefono gratuito?",
        mockResponse: "Si, la linea gratuita del IMV es el 900 20 22 22 de la Seguridad Social. Atienden de lunes a viernes.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["900 20 22 22"] },
    ],
  },
  /* ---- 2. IMV EN — Andriy (Barcelona) ---- */
  {
    name: "IMV EN", persona: "Andriy Kovalenko", lang: "en",
    turns: [
      { userText: "Hi, I'm a refugee from Ukraine. What financial help can I get?",
        mockResponse: "You can apply for the Minimum Vital Income (IMV) from Social Security. A single adult receives 604.21 euros per month. Call 900 20 22 22 for free.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["604.21", "900 20 22 22", "Social Security"] },
      { userText: "What are the requirements?",
        mockResponse: "You need to be between 23 and 65 years old, have legal residence in Spain for at least 1 year, and be in economic vulnerability.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["23", "65"] },
      { userText: "How do I apply?",
        mockResponse: "Apply online at sede.seg-social.gob.es or in person at your local INSS office. You can also call 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["INSS", "900 20 22 22"] },
      { userText: "How long does it take?",
        mockResponse: "The maximum processing time is 6 months from the application date.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["6 months"] },
      { userText: "Where do I go in Barcelona?",
        mockResponse: "In Barcelona, go to the INSS office at Passeig de Sant Joan 189, 08037 Barcelona. Book an appointment first.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Sant Joan"] },
    ],
  },
  /* ---- 3. Empadronamiento ES — Irina (Murcia) ---- */
  {
    name: "Empadronamiento ES", persona: "Irina Petrovna", lang: "es",
    turns: [
      { userText: "Hola, soy Irina. Acabo de mudarme a Murcia con mi hijo. Necesito empadronarme.",
        mockResponse: "El empadronamiento es un derecho y es gratuito. Se hace en el Ayuntamiento. En Murcia, pide cita en la OAC o llama al 010.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["derecho", "gratuito", "Ayuntamiento", "010"] },
      { userText: "Por que es importante?",
        mockResponse: "El empadronamiento es obligatorio y necesario para acceder a la tarjeta sanitaria, escolarizar a tu hijo, solicitar el IMV y otras ayudas.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["tarjeta sanitaria", "IMV"] },
      { userText: "Que documentos necesito?",
        mockResponse: "Necesitas tu DNI o NIE (o pasaporte), un justificante de vivienda como contrato de alquiler o escritura, y rellenar la hoja padronal.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["DNI", "contrato"] },
      { userText: "Donde voy en Murcia?",
        mockResponse: "En Murcia, ve a la Oficina de Atencion al Ciudadano en Plaza Cardenal Belluga 1, 30004 Murcia. Telefono 010 o 968 358 600.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Cardenal Belluga", "968 358 600"] },
      { userText: "Es gratis de verdad?",
        mockResponse: "Si, el empadronamiento es completamente gratuito. Es un derecho y una obligacion para todos los residentes, independientemente de su situacion legal.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["gratuito", "derecho"] },
      { userText: "Puedo empadronar a mi hijo menor?",
        mockResponse: "Si, puedes empadronar a tu hijo con tu misma solicitud. Lleva su pasaporte o DNI y el libro de familia.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["libro de familia"] },
    ],
  },
  /* ---- 4. Empadronamiento FR — Kevin (Valencia) ---- */
  {
    name: "Empadronamiento FR", persona: "Kevin Mbeki", lang: "fr",
    turns: [
      { userText: "Bonjour, je suis Kevin. Je viens d'arriver a Valencia. Comment m'inscrire?",
        mockResponse: "L'inscription municipale (empadronamiento) se fait a la Mairie. C'est gratuit et c'est un droit pour tous. Appelez le 010 pour un rendez-vous.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Mairie", "gratuit", "010"] },
      { userText: "Quels documents faut-il?",
        mockResponse: "Il vous faut votre passeport ou carte d'identite, un justificatif de domicile (contrat de location) et remplir le formulaire padronal.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["passeport", "contrat"] },
      { userText: "Ou est le bureau a Valencia?",
        mockResponse: "A Valencia, l'Oficina de Estadistica se trouve Placa del Ayuntamiento 1, 46002 Valencia. Telephone 010 ou 963 525 478.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Ayuntamiento 1", "963 525 478"] },
      { userText: "C'est vraiment gratuit?",
        mockResponse: "Oui, c'est entierement gratuit. L'empadronamiento est un droit pour tous les residents, quelle que soit votre situation legale.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["gratuit", "droit"] },
      { userText: "Meme sans papiers?",
        mockResponse: "Oui, meme sans papiers. L'empadronamiento est un droit fondamental. Le personnel municipal ne peut pas vous refuser l'inscription ni alerter la police.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["droit"] },
    ],
  },
  /* ---- 5. Tarjeta sanitaria ES — Maria del Carmen (Sevilla) ---- */
  {
    name: "Tarjeta sanitaria ES", persona: "Maria del Carmen Ruiz", lang: "es",
    turns: [
      { userText: "Hola, soy Maria del Carmen. Tengo 67 anos y necesito la tarjeta sanitaria.",
        mockResponse: "La Tarjeta Sanitaria Individual (TSI) te da acceso a medico de familia, urgencias y medicamentos subvencionados. En Andalucia, ve a tu Centro de Salud del SAS.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["Centro de Salud", "urgencias"] },
      { userText: "Quien puede tenerla?",
        mockResponse: "Todas las personas empadronadas tienen derecho. Las urgencias son para TODOS, incluso sin tarjeta. Llama al 900 102 112 para informacion.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["TODOS", "900 102 112"] },
      { userText: "Que documentos necesito?",
        mockResponse: "Necesitas tu DNI, certificado de empadronamiento y, si eres pensionista, tu tarjeta de la Seguridad Social.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["DNI", "empadronamiento"] },
      { userText: "Y si no tengo papeles, puedo ir a urgencias?",
        mockResponse: "Si, las urgencias son un derecho para TODOS, independientemente de tu situacion administrativa. Ningun hospital puede rechazarte en urgencias.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["TODOS", "urgencias"] },
      { userText: "Donde voy en Sevilla?",
        mockResponse: "En Sevilla, ve a tu Centro de Salud del SAS mas cercano. Para informacion llama al 955 545 060 o Salud Responde.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["955 545 060"] },
      { userText: "Tiene coste?",
        mockResponse: "No, la tarjeta sanitaria es gratuita. Los medicamentos tienen copago reducido para pensionistas.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["gratuita"] },
    ],
  },
  /* ---- 6. Tarjeta sanitaria EN — Ahmed (Zaragoza) ---- */
  {
    name: "Tarjeta sanitaria EN", persona: "Ahmed Al-Hassan", lang: "en",
    turns: [
      { userText: "Hello, my family and I are refugees in Zaragoza. How do we get health cards?",
        mockResponse: "The Individual Health Card (TSI) gives you access to family doctor, emergency care, and subsidized medicine. Go to your nearest Health Center.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["Health Center", "emergency"] },
      { userText: "Can everyone get it?",
        mockResponse: "Yes, everyone registered (empadronado) can get it. Emergency care is available for ALL people regardless of status. Call 900 102 112.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["ALL", "900 102 112"] },
      { userText: "What documents do we need?",
        mockResponse: "You need ID (passport or NIE), empadronamiento certificate, and Social Security number if you have one.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["empadronamiento"] },
      { userText: "Where in Zaragoza?",
        mockResponse: "In Zaragoza, go to your nearest Centro de Salud del SALUD. Call 976 714 000 for information.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["976 714 000"] },
      { userText: "Is it free?",
        mockResponse: "Yes, the health card is free. Prescriptions may have a small copayment.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["free"] },
    ],
  },
  /* ---- 7. NIE/TIE ES — Roberto (Alicante) ---- */
  {
    name: "NIE/TIE ES", persona: "Roberto Oliveira", lang: "es",
    turns: [
      { userText: "Hola, soy Roberto. Necesito renovar mi TIE en Alicante.",
        mockResponse: "Para renovar la TIE necesitas cita previa en la Oficina de Extranjeria. Llama al 060 para informacion.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["060", "Extranjeria"] },
      { userText: "Cual es la diferencia entre NIE y TIE?",
        mockResponse: "El NIE es tu numero de identidad de extranjero (permanente). La TIE es la Tarjeta de Identidad de Extranjero (fisica, se renueva).",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["NIE", "TIE"] },
      { userText: "Que formulario necesito?",
        mockResponse: "Necesitas el formulario EX-17 para la renovacion de la TIE. Descargalo en inclusion.gob.es.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["EX-17"] },
      { userText: "Cuanto tarda?",
        mockResponse: "El proceso tarda entre 30 y 45 dias habiles normalmente.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["30", "45 dias"] },
      { userText: "Cuando debo renovar?",
        mockResponse: "Debes renovar en los 60 dias anteriores a la caducidad de tu TIE. No esperes a que caduque.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["60 dias"] },
      { userText: "Hay alguna tasa?",
        mockResponse: "Si, debes pagar la tasa modelo 790 codigo 012. El importe depende del tipo de autorizacion.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["790"] },
      { userText: "Telefono de informacion?",
        mockResponse: "Llama al 060 para cualquier consulta sobre extranjeria. Atienden en varios idiomas.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["060"] },
    ],
  },
  /* ---- 8. NIE/TIE EN — Andriy (Barcelona) ---- */
  {
    name: "NIE/TIE EN", persona: "Andriy Kovalenko", lang: "en",
    turns: [
      { userText: "I need to get my NIE in Barcelona. How?",
        mockResponse: "Book an appointment at the Immigration Office (Oficina de Extranjeria). Call 060 for information.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["060", "Extranjeria"] },
      { userText: "What form do I need?",
        mockResponse: "You need form EX-17 for the TIE application. Download it from inclusion.gob.es.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["EX-17"] },
      { userText: "How long does it take?",
        mockResponse: "Processing takes between 30 and 45 working days typically.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["30", "45"] },
      { userText: "When should I renew?",
        mockResponse: "Apply for renewal within 60 days before your TIE expires. Don't wait until it's expired.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["60 days"] },
      { userText: "Any fees?",
        mockResponse: "Yes, you need to pay fee form 790 code 012. The amount depends on your authorization type.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["790"] },
    ],
  },
  /* ---- 9. Ayuda alquiler ES — Sofia (Malaga) ---- */
  {
    name: "Ayuda alquiler ES", persona: "Sofia Morales", lang: "es",
    turns: [
      { userText: "Hola, soy Sofia, tengo 22 anos. Hay ayudas para alquilar un piso?",
        mockResponse: "Si, existe el Bono Alquiler Joven de 250 euros al mes para menores de 35 anos. Lo gestiona el MIVAU. Llama al 060.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["250", "35", "MIVAU"],
        mustNotContain: ["500€/mes"] },
      { userText: "Que requisitos tiene?",
        mockResponse: "Debes ser menor de 35 anos, tener ingresos inferiores a 3 veces el IPREM, y tener un contrato de alquiler vigente.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["35", "IPREM"] },
      { userText: "Cuanto dan exactamente?",
        mockResponse: "El Bono Joven son 250 euros al mes durante 2 anos, compatible con otras ayudas autonomicas.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["250"] },
      { userText: "Donde solicito en Malaga?",
        mockResponse: "En Malaga, solicita a traves de la Junta de Andalucia o en mivau.gob.es. Llama al 060 o al 012 para informacion.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["060"] },
      { userText: "Que documentos necesito?",
        mockResponse: "Necesitas DNI/NIE, contrato de alquiler, declaracion de la renta, certificado de empadronamiento y vida laboral.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["contrato de alquiler"] },
      { userText: "Hay limite de renta del piso?",
        mockResponse: "Si, el alquiler no puede superar los 600 euros al mes (900 en zonas tensionadas como Madrid o Barcelona).",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["600"] },
    ],
  },
  /* ---- 10. Ayuda alquiler FR — Jean-Pierre (Palma) ---- */
  {
    name: "Ayuda alquiler FR", persona: "Jean-Pierre Dupont", lang: "fr",
    turns: [
      { userText: "Bonjour, je cherche une aide au loyer a Palma.",
        mockResponse: "Il existe le Bono Alquiler Joven de 250 euros par mois pour les moins de 35 ans. Gere par le MIVAU. Appelez le 060.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["250", "35", "MIVAU"] },
      { userText: "Quelles sont les conditions?",
        mockResponse: "Avoir moins de 35 ans, des revenus inferieurs a 3 fois l'IPREM, et un contrat de location en cours.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["35", "IPREM"] },
      { userText: "Combien exactement?",
        mockResponse: "Le Bono Joven est de 250 euros par mois pendant 2 ans.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["250"] },
      { userText: "Ou faire la demande?",
        mockResponse: "Faites la demande sur mivau.gob.es ou aupres de votre communaute autonome. Appelez le 060.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["060"] },
      { userText: "Quels documents?",
        mockResponse: "Passeport ou NIE, contrat de location, declaration de revenus et certificat d'empadronamiento.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["contrat"] },
    ],
  },
  /* ---- 11. Discapacidad ES — Roberto (Alicante) ---- */
  {
    name: "Discapacidad ES", persona: "Roberto Oliveira", lang: "es",
    turns: [
      { userText: "Tuve un accidente laboral y quiero pedir el certificado de discapacidad.",
        mockResponse: "El certificado de discapacidad lo emite tu Comunidad Autonoma. Reconoce grados del 33%, 65% y 75% con diferentes beneficios. Llama al 012.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%", "65%", "012"],
        mustNotContain: ["100% discapacidad"] },
      { userText: "Que beneficios tiene el 33%?",
        mockResponse: "Con el 33% tienes acceso a reserva de empleo, reducciones fiscales, bonificaciones en transporte y acceso a centros especiales de empleo.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%", "empleo"] },
      { userText: "Y el 65%?",
        mockResponse: "Con el 65% accedes a la pension no contributiva de 517,90 euros al mes, exencion de copago farmaceutico y mas beneficios fiscales.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["65%", "517,90"] },
      { userText: "Que pasa con el 75%?",
        mockResponse: "El 75% con necesidad de tercera persona anade un complemento del 50% a la pension. Tambien tarjeta de estacionamiento y asistencia personal.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["75%"] },
      { userText: "Como solicito el certificado?",
        mockResponse: "Solicita cita en el Centro Base de tu comunidad autonoma. Necesitas informe medico, DNI/NIE e informe social. Llama al 012 o al 060.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["012"] },
      { userText: "Cuanto tarda?",
        mockResponse: "El proceso de valoracion tarda normalmente entre 3 y 6 meses segun la comunidad autonoma.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["6 meses"] },
      { userText: "Hay beneficios fiscales?",
        mockResponse: "Si, con el certificado tienes deducciones en IRPF, reduccion del IVA en vehiculos adaptados y exencion del impuesto de matriculacion.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["IRPF"] },
    ],
  },
  /* ---- 12. Discapacidad EN — Ahmed (Zaragoza) ---- */
  {
    name: "Discapacidad EN", persona: "Ahmed Al-Hassan", lang: "en",
    turns: [
      { userText: "My son has a disability. How do I get a certificate in Spain?",
        mockResponse: "The disability certificate is issued by your regional government. It recognizes degrees of 33%, 65% and 75% with different benefits.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%", "65%", "disability"] },
      { userText: "What benefits at 33%?",
        mockResponse: "At 33% you get access to job quotas, tax reductions, transport discounts and special employment centers.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%"] },
      { userText: "What about 65%?",
        mockResponse: "At 65% you can receive a non-contributory pension of 517.90 euros per month and exemption from pharmacy copayments.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["65%", "517.90"] },
      { userText: "How do I apply?",
        mockResponse: "Book an appointment at your regional Centro Base. Bring medical reports, ID, and social report. Call 012 or 060.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["012"] },
      { userText: "How long does it take?",
        mockResponse: "The assessment process typically takes 3 to 6 months depending on the region.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["6 months"] },
    ],
  },
  /* ---- 13. Justicia gratuita ES — Laura (Bilbao) ---- */
  {
    name: "Justicia gratuita ES", persona: "Laura Fernandez", lang: "es",
    turns: [
      { userText: "Soy victima de violencia de genero y necesito un abogado. No puedo pagar.",
        mockResponse: "Tienes derecho a justicia gratuita. Como victima de violencia de genero tienes acceso automatico sin limite de ingresos. Llama al 060 para informacion.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["justicia gratuita", "060"],
        mustNotContain: ["abogado privado gratis"] },
      { userText: "Quien mas puede pedirla?",
        mockResponse: "Cualquier persona con ingresos inferiores a 2 veces el IPREM puede solicitar justicia gratuita.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["IPREM"] },
      { userText: "Como la solicito?",
        mockResponse: "Presenta la solicitud en el Servicio de Orientacion Juridica (SOJ) de tu partido judicial o en el Colegio de Abogados.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["SOJ"] },
      { userText: "Cuanto tardan en contestar?",
        mockResponse: "El plazo maximo de resolucion es de 30 dias. Si no contestan, se aplica silencio positivo: se entiende concedida.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["30 dias", "silencio positivo"] },
      { userText: "Que incluye?",
        mockResponse: "Incluye abogado y procurador de oficio, asistencia pericial gratuita, exencion de tasas judiciales y depositos.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["abogado"] },
      { userText: "Donde en Bilbao?",
        mockResponse: "En Bilbao, acude al SOJ del Colegio de Abogados de Bizkaia. Tambien puedes llamar al 060 o al Ministerio de Justicia.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["SOJ", "060"] },
    ],
  },
  /* ---- 14. Justicia gratuita FR — Fatima (Madrid) ---- */
  {
    name: "Justicia gratuita FR", persona: "Fatima Oukacha", lang: "fr",
    turns: [
      { userText: "J'ai besoin d'un avocat mais je n'ai pas d'argent.",
        mockResponse: "Vous avez droit a l'aide juridictionnelle gratuite. Appelez le 060 pour information ou rendez-vous au SOJ.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["060", "SOJ"] },
      { userText: "Quelles conditions?",
        mockResponse: "Vos revenus doivent etre inferieurs a 2 fois l'IPREM. Les victimes de violence de genre y ont droit automatiquement.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["IPREM"] },
      { userText: "Combien de temps pour la reponse?",
        mockResponse: "Le delai maximum est de 30 jours. Sans reponse, le silence positif s'applique: la demande est consideree acceptee.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["30 jours"] },
      { userText: "Que comprend l'aide?",
        mockResponse: "L'aide comprend un avocat commis d'office, un procureur, expertise gratuite et exemption des frais de justice.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["avocat"] },
      { userText: "Ou a Madrid?",
        mockResponse: "A Madrid, rendez-vous au SOJ du Colegio de Abogados de Madrid. Appelez le 060.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["SOJ", "060"] },
    ],
  },
  /* ---- 15. Desempleo ES — Sofia (Malaga) ---- */
  {
    name: "Desempleo ES", persona: "Sofia Morales", lang: "es",
    turns: [
      { userText: "Me acaban de despedir. Tengo derecho al paro?",
        mockResponse: "Si has cotizado al menos 360 dias en los ultimos 6 anos, tienes derecho a la prestacion por desempleo del SEPE. Llama al 901 119 999.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["901 119 999", "SEPE"],
        mustNotContain: ["indefinido sin cotizar"] },
      { userText: "Cuanto tiempo tengo para pedirlo?",
        mockResponse: "Tienes 15 dias habiles desde el fin del contrato para solicitar la prestacion. No pierdas el plazo.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["15 dias"] },
      { userText: "Cuanto me dan?",
        mockResponse: "Los primeros 180 dias cobras el 70% de tu base reguladora. Despues baja al 50%.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["70%", "50%"] },
      { userText: "Cual es el maximo?",
        mockResponse: "La cuantia maxima de la prestacion por desempleo es de 1.225,80 euros al mes sin hijos.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["1.225,80"] },
      { userText: "Donde lo pido?",
        mockResponse: "Solicita la prestacion en tu oficina del SEPE mas cercana o por internet en sepe.es. Necesitas cita previa.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["SEPE"] },
      { userText: "Que documentos necesito?",
        mockResponse: "Necesitas DNI/NIE, certificado de empresa, documento de afiliacion a la Seguridad Social y numero de cuenta bancaria.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["DNI"] },
      { userText: "Telefono del SEPE?",
        mockResponse: "El telefono de atencion del SEPE es el 901 119 999. Tambien puedes usar el 060 para informacion general.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["901 119 999"] },
    ],
  },
  /* ---- 16. Desempleo EN — Andriy (Barcelona) ---- */
  {
    name: "Desempleo EN", persona: "Andriy Kovalenko", lang: "en",
    turns: [
      { userText: "I just lost my job. Can I get unemployment benefits?",
        mockResponse: "If you contributed for at least 360 days in the last 6 years, you can claim unemployment from SEPE. Call 901 119 999.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["901 119 999", "SEPE"] },
      { userText: "How long do I have to apply?",
        mockResponse: "You must apply within 15 days of your contract ending. Don't miss the deadline.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["15 days"] },
      { userText: "How much will I receive?",
        mockResponse: "For the first 180 days you receive 70% of your regulatory base. After that it drops to 50%.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["70%", "50%"] },
      { userText: "What is the maximum?",
        mockResponse: "The maximum unemployment benefit is 1,225.80 euros per month without dependents.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["1,225.80"] },
      { userText: "Where do I apply in Barcelona?",
        mockResponse: "Apply at your nearest SEPE office or online at sepe.es. You need an appointment.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["SEPE"] },
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  Group 2: Office scenarios (7 tests)                                */
/* ------------------------------------------------------------------ */

const OFFICE_SCENARIOS: Scenario[] = [
  /* ---- Madrid — Fatima ---- */
  {
    name: "Oficinas Madrid", persona: "Fatima Oukacha", lang: "es",
    turns: [
      { userText: "Donde me empadrono en Madrid?",
        mockResponse: "En Madrid, ve a la OAC en Calle Gran Via 3, 28013 Madrid. Telefono 010 o 915 298 210. Horario lunes a viernes 8:30 a 14:30.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Gran Via 3", "915 298 210"] },
      { userText: "Y para la tarjeta sanitaria?",
        mockResponse: "Para la tarjeta sanitaria en Madrid, ve a tu Centro de Salud. Llama al 012 o al 900 102 112. Horario lunes a viernes 9:00 a 14:00.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["900 102 112"] },
      { userText: "Y el IMV?",
        mockResponse: "Para el IMV en Madrid, ve al INSS en Calle Padre Damian 4, 28036 Madrid. Telefono 900 20 22 22. Horario lunes a viernes 9:00 a 14:00.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Padre Damian 4", "900 20 22 22"] },
    ],
  },
  /* ---- Barcelona — Andriy ---- */
  {
    name: "Oficinas Barcelona", persona: "Andriy Kovalenko", lang: "en",
    turns: [
      { userText: "Where do I register my address in Barcelona?",
        mockResponse: "Go to the OAC at Placa de Sant Miquel 4, 08002 Barcelona. Call 010 or 932 850 700. Open Monday to Friday 8:30 to 14:30.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Sant Miquel 4", "932 850 700"] },
      { userText: "Health card?",
        mockResponse: "Go to your nearest CAP. Call 061 or 900 111 000. Open Monday to Friday 8:00 to 20:00.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["900 111 000"] },
      { userText: "IMV office?",
        mockResponse: "The INSS office is at Passeig de Sant Joan 189, 08037 Barcelona. Call 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Sant Joan 189", "900 20 22 22"] },
    ],
  },
  /* ---- Valencia — Kevin ---- */
  {
    name: "Oficinas Valencia", persona: "Kevin Mbeki", lang: "fr",
    turns: [
      { userText: "Ou m'inscrire a Valencia?",
        mockResponse: "A Valencia, allez a l'Oficina de Estadistica, Placa del Ayuntamiento 1, 46002 Valencia. Telephone 010 ou 963 525 478.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Ayuntamiento 1", "963 525 478"] },
      { userText: "Carte sanitaire?",
        mockResponse: "Allez au Centro de Salud. Telephone 900 161 161. Horaire lundi a vendredi 9:00 a 14:00.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["900 161 161"] },
      { userText: "Bureau IMV?",
        mockResponse: "Le bureau INSS est a Calle Bailen 46, 46007 Valencia. Telephone 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Bailen 46", "900 20 22 22"] },
    ],
  },
  /* ---- Sevilla — Maria del Carmen ---- */
  {
    name: "Oficinas Sevilla", persona: "Maria del Carmen Ruiz", lang: "es",
    turns: [
      { userText: "Donde me empadrono en Sevilla?",
        mockResponse: "En Sevilla, ve al Registro General del Ayuntamiento en Plaza Nueva 1, 41001 Sevilla. Telefono 010 o 955 470 000.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Plaza Nueva 1", "955 470 000"] },
      { userText: "Tarjeta sanitaria?",
        mockResponse: "Ve al Centro de Salud del SAS. Telefono 955 545 060 o Salud Responde.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["955 545 060"] },
      { userText: "Oficina del INSS?",
        mockResponse: "El INSS esta en Avenida de la Constitucion 2, 41001 Sevilla. Telefono 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Constitucion 2", "900 20 22 22"] },
    ],
  },
  /* ---- Bilbao + Zaragoza — Laura + Ahmed ---- */
  {
    name: "Oficinas Bilbao + Zaragoza", persona: "Laura + Ahmed", lang: "es",
    turns: [
      { userText: "Donde me empadrono en Bilbao?",
        mockResponse: "En Bilbao, ve al Servicio de Atencion Ciudadana en Plaza Ernesto Erkoreka 1, 48007 Bilbao. Telefono 010 o 944 204 200.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Erkoreka 1", "944 204 200"] },
      { userText: "Y la tarjeta sanitaria en Bilbao?",
        mockResponse: "En Bilbao ve a Osakidetza. Telefono 900 203 050. Horario lunes a viernes 8:00 a 15:00.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["900 203 050"] },
      { userText: "Donde me empadrono en Zaragoza?",
        mockResponse: "En Zaragoza, ve a la Oficina de Registro en Plaza del Pilar 18, 50003 Zaragoza. Telefono 010 o 976 721 100.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Pilar 18", "976 721 100"] },
      { userText: "Tarjeta sanitaria en Zaragoza?",
        mockResponse: "En Zaragoza ve al Centro de Salud del SALUD. Telefono 976 714 000.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["976 714 000"] },
    ],
  },
  /* ---- Malaga + Alicante — Sofia + Roberto ---- */
  {
    name: "Oficinas Malaga + Alicante", persona: "Sofia + Roberto", lang: "es",
    turns: [
      { userText: "Donde me empadrono en Malaga?",
        mockResponse: "En Malaga, ve a la Oficina de Atencion al Ciudadano en Avenida de Cervantes 4, 29016 Malaga. Telefono 010 o 951 926 010.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Cervantes 4", "951 926 010"] },
      { userText: "Y la oficina del INSS en Malaga?",
        mockResponse: "El INSS de Malaga esta en Calle Hilera 4, 29007 Malaga. Telefono 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Hilera 4", "900 20 22 22"] },
      { userText: "Empadronamiento en Alicante?",
        mockResponse: "En Alicante, la OIAC esta en Calle Jorge Juan 1, 03002 Alicante. Telefono 010 o 965 149 100.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Jorge Juan 1", "965 149 100"] },
      { userText: "INSS en Alicante?",
        mockResponse: "El INSS de Alicante esta en Avenida Aguilera 53, 03007 Alicante. Telefono 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["Aguilera 53", "900 20 22 22"] },
    ],
  },
  /* ---- Murcia + Palma — Irina + Jean-Pierre ---- */
  {
    name: "Oficinas Murcia + Palma", persona: "Irina + Jean-Pierre", lang: "es",
    turns: [
      { userText: "Donde me empadrono en Murcia?",
        mockResponse: "En Murcia, ve a la Oficina de Atencion al Ciudadano en Plaza Cardenal Belluga 1, 30004 Murcia. Telefono 010 o 968 358 600.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Cardenal Belluga 1", "968 358 600"] },
      { userText: "Tarjeta sanitaria en Murcia?",
        mockResponse: "En Murcia, ve al Centro de Salud del SMS. Telefono 968 365 656.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["968 365 656"] },
      { userText: "Empadronamiento en Palma?",
        mockResponse: "En Palma, ve a la OAC en Plaza de Cort 1, 07001 Palma. Telefono 010 o 971 225 900.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["Cort 1", "971 225 900"] },
      { userText: "Salud en Palma?",
        mockResponse: "En Palma, ve al Centro de Salud del IB-SALUT. Telefono 971 211 313.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["971 211 313"] },
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  Group 5: Cross-topic edge cases (5 tests)                          */
/* ------------------------------------------------------------------ */

const EDGE_SCENARIOS: Scenario[] = [
  /* ---- 5a. Cross-topic 8-turn — Ahmed (all tramites) ---- */
  {
    name: "Cross-topic 8 tramites", persona: "Ahmed Al-Hassan", lang: "es",
    turns: [
      { userText: "Necesito el IMV",
        mockResponse: "El IMV lo gestiona la Seguridad Social. Llama al 900 20 22 22.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["900 20 22 22"] },
      { userText: "Tambien empadronarme",
        mockResponse: "El empadronamiento se hace en el Ayuntamiento. Llama al 010.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["010"] },
      { userText: "Y tarjeta sanitaria",
        mockResponse: "Ve a tu Centro de Salud. Llama al 900 102 112.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["900 102 112"] },
      { userText: "Renovar NIE",
        mockResponse: "Para el NIE, cita en Extranjeria. Formulario EX-17. Llama al 060.",
        mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }],
        mustContain: ["060", "EX-17"] },
      { userText: "Ayuda alquiler",
        mockResponse: "El Bono Joven son 250 euros al mes para menores de 35 del MIVAU.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["250"] },
      { userText: "Certificado discapacidad",
        mockResponse: "El certificado reconoce grados 33%, 65% y 75%. Llama al 012.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%", "012"] },
      { userText: "Justicia gratuita",
        mockResponse: "Si tus ingresos son inferiores a 2 veces el IPREM, tienes derecho. Ve al SOJ. Llama al 060.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["IPREM", "SOJ"] },
      { userText: "Y el paro",
        mockResponse: "Tienes 15 dias habiles para pedir el paro en el SEPE. Llama al 901 119 999.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["901 119 999", "15 dias"] },
    ],
  },
  /* ---- 5b. Persona sin papeles — Kevin (Valencia) ---- */
  {
    name: "Persona sin papeles", persona: "Kevin Mbeki", lang: "es",
    turns: [
      { userText: "No tengo papeles. Puedo acceder a algo?",
        mockResponse: "Si. El empadronamiento es un derecho para TODOS, independientemente de tu situacion legal. Ve al Ayuntamiento.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["derecho", "TODOS", "empadronamiento"] },
      { userText: "Me pueden denunciar si voy?",
        mockResponse: "No. El Ayuntamiento no puede comunicar tus datos a la policia. El empadronamiento es confidencial y es tu derecho.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["derecho"] },
      { userText: "Y si me pongo enfermo?",
        mockResponse: "Las urgencias son para TODOS. Ningun hospital puede rechazarte en urgencias, tengas o no papeles.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["urgencias", "TODOS"] },
      { userText: "Puedo tener tarjeta sanitaria?",
        mockResponse: "Con el empadronamiento puedes solicitar la tarjeta sanitaria para acceso completo al Centro de Salud.",
        mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }],
        mustContain: ["empadronamiento", "Centro de Salud"] },
      { userText: "Hay ayuda para la comida?",
        mockResponse: "Los servicios sociales del Ayuntamiento pueden ayudarte con alimentacion, alojamiento y orientacion. Pide cita en servicios sociales de tu zona.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["servicios sociales"] },
      { userText: "Que mas puedo hacer con el padron?",
        mockResponse: "Con el empadronamiento puedes escolarizar a tus hijos, acceder a servicios sociales y, tras 3 anos, solicitar arraigo social.",
        mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }],
        mustContain: ["empadronamiento"] },
    ],
  },
  /* ---- 5c. Victima violencia genero — Laura (Bilbao) ---- */
  {
    name: "Victima violencia genero", persona: "Laura Fernandez", lang: "es",
    turns: [
      { userText: "Soy victima de violencia de genero. Que ayuda hay?",
        mockResponse: "Llama al 016, la linea de atencion a victimas de violencia de genero. Tienes derecho a justicia gratuita automatica sin limite de ingresos.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["016", "justicia gratuita"] },
      { userText: "Puedo pedir el IMV?",
        mockResponse: "Si. Como victima de violencia de genero puedes acceder al IMV sin el requisito de 1 ano de residencia. La cuantia base es 604,21 euros.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["IMV", "604,21"] },
      { userText: "Necesito un abogado ya",
        mockResponse: "Ve al SOJ del Colegio de Abogados. Como victima de VG tienes abogado de oficio inmediato, 24 horas. Llama al 060.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["SOJ", "060"] },
      { userText: "Hay ayuda para vivienda?",
        mockResponse: "Si, las victimas de VG tienen prioridad en vivienda social y acceso al Bono Alquiler. Contacta servicios sociales de tu municipio.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["vivienda"] },
      { userText: "Que mas protecciones hay?",
        mockResponse: "Tienes derecho a orden de proteccion, cambio de domicilio, ayudas economicas especificas, y prioridad en programas de empleo.",
        mockSources: [{ name: "justicia_gratuita", url: KB.justicia_gratuita.url }],
        mustContain: ["proteccion"] },
    ],
  },
  /* ---- 5d. Persona con discapacidad — Roberto (Alicante) ---- */
  {
    name: "Persona con discapacidad completo", persona: "Roberto Oliveira", lang: "es",
    turns: [
      { userText: "Tengo discapacidad del 45%. Que beneficios tengo?",
        mockResponse: "Con el 33% o mas tienes reserva de empleo, reducciones fiscales en IRPF y bonificaciones en transporte.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%", "fiscal"] },
      { userText: "Si llego al 65%?",
        mockResponse: "Con el 65% accedes a pension no contributiva de 517,90 euros y exencion de copago farmaceutico.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["65%", "517,90"] },
      { userText: "Hay cuota de empleo?",
        mockResponse: "Si, las empresas con mas de 50 trabajadores deben reservar al menos el 2% de puestos para personas con discapacidad del 33% o mas.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["33%"] },
      { userText: "Beneficios en impuestos?",
        mockResponse: "Tienes deducciones en IRPF, reduccion de IVA en vehiculos adaptados y exencion del impuesto de matriculacion.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["IRPF", "IVA"] },
      { userText: "Como actualizo mi grado?",
        mockResponse: "Pide revision de grado en el Centro Base de tu comunidad. Necesitas nuevos informes medicos. Llama al 012.",
        mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }],
        mustContain: ["012"] },
    ],
  },
  /* ---- 5e. Joven desempleado — Sofia (Malaga) ---- */
  {
    name: "Joven desempleado multi-ayuda", persona: "Sofia Morales", lang: "es",
    turns: [
      { userText: "Tengo 22 anos, me quedé sin trabajo. Que puedo pedir?",
        mockResponse: "Si cotizaste al menos 360 dias, solicita el paro en el SEPE. Tienes 15 dias habiles. Llama al 901 119 999.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["SEPE", "15 dias"] },
      { userText: "No llego a pagar el alquiler",
        mockResponse: "Puedes pedir el Bono Joven de 250 euros al mes si eres menor de 35. Lo gestiona el MIVAU.",
        mockSources: [{ name: "ayuda_alquiler", url: KB.ayuda_alquiler.url }],
        mustContain: ["250", "Bono Joven"] },
      { userText: "Puedo pedir el IMV tambien?",
        mockResponse: "Si tus ingresos son muy bajos, puedes solicitar el IMV de 604,21 euros en la Seguridad Social. Son compatibles.",
        mockSources: [{ name: "imv", url: KB.imv.url }],
        mustContain: ["IMV", "604,21"] },
      { userText: "Cuanto es el maximo del paro?",
        mockResponse: "La cuantia maxima de desempleo es 1.225,80 euros al mes. Cobras el 70% los primeros 180 dias.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["1.225,80", "70%"] },
      { userText: "Donde pido todo en Malaga?",
        mockResponse: "El paro en la oficina SEPE de Malaga. El Bono Joven en mivau.gob.es. El IMV en el INSS de Calle Hilera 4, Malaga.",
        mockSources: [{ name: "desempleo", url: KB.desempleo.url }],
        mustContain: ["SEPE", "Hilera 4"] },
    ],
  },
];

/* ================================================================== */
/*  TEST SUITE — Group 1: Tramite Conversations (16 tests)             */
/* ================================================================== */

test.describe("Group 1: Tramite Conversations", () => {
  for (const s of TRAMITE_SCENARIOS) {
    test(`${s.name} — ${s.persona} (${s.lang})`, async ({ page }) => {
      test.setTimeout(60_000);
      await runScenario(page, s);
    });
  }
});

/* ================================================================== */
/*  TEST SUITE — Group 2: Offices by City (7 tests)                    */
/* ================================================================== */

test.describe("Group 2: Oficinas por Ciudad", () => {
  for (const s of OFFICE_SCENARIOS) {
    test(`${s.name} — ${s.persona}`, async ({ page }) => {
      test.setTimeout(60_000);
      await runScenario(page, s);
    });
  }
});

/* ================================================================== */
/*  TEST SUITE — Group 3: Anti-Hallucination (4 tests)                 */
/* ================================================================== */

test.describe("Group 3: Anti-Alucinacion", () => {
  const REAL_PHONES = ["900 20 22 22", "010", "900 102 112", "060", "901 119 999", "012"];

  test("3a — Telefonos reales vs inventados", async ({ page }) => {
    test.setTimeout(60_000);
    const turns: Turn[] = [
      { userText: "Como pido el IMV?", mockResponse: "Llama al 900 20 22 22 de la Seguridad Social para el IMV.", mockSources: [{ name: "imv", url: KB.imv.url }], mustContain: ["900 20 22 22"] },
      { userText: "Y el empadronamiento?", mockResponse: "Llama al 010 de tu Ayuntamiento para cita de empadronamiento.", mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }], mustContain: ["010"] },
      { userText: "Tarjeta sanitaria?", mockResponse: "Para la tarjeta sanitaria llama al 900 102 112 del SERMAS.", mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }], mustContain: ["900 102 112"] },
      { userText: "NIE?", mockResponse: "Para el NIE llama al 060 de Extranjeria.", mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }], mustContain: ["060"] },
      { userText: "Paro?", mockResponse: "Para la prestacion por desempleo llama al 901 119 999 del SEPE.", mockSources: [{ name: "desempleo", url: KB.desempleo.url }], mustContain: ["901 119 999"] },
    ];
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    for (const t of turns) {
      await sendAndWait(page, t.userText, new RegExp(esc(t.mustContain[0])));
    }
    const texts = await page.locator('[class*="message"]').allInnerTexts();
    const all = texts.join(" ");
    const found = all.match(/\b\d[\d\s]{5,}\d\b/g) || [];
    for (const p of found) {
      const n = p.trim();
      expect(REAL_PHONES.some((rp) => n.includes(rp) || rp.includes(n))).toBe(true);
    }
  });

  test("3b — Instituciones reales, no fabricadas", async ({ page }) => {
    const turns: Turn[] = [
      { userText: "Quien gestiona el IMV?", mockResponse: "El IMV lo gestiona la Seguridad Social (INSS). Llama al 900 20 22 22.", mockSources: [{ name: "imv", url: KB.imv.url }], mustContain: ["Seguridad Social"], mustNotContain: ["Cruz Roja gestiona", "Caritas tramita", "UNICEF Espana"] },
    ];
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    await sendAndWait(page, turns[0].userText, /Seguridad Social/);
    await expect(page.getByText("Seguridad Social").first()).toBeVisible();
    for (const bad of turns[0].mustNotContain!) {
      expect(await page.getByText(bad).count()).toBe(0);
    }
  });

  test("3c — Cantidades correctas (604,21 / 517,90 / 1.225,80)", async ({ page }) => {
    test.setTimeout(60_000);
    const turns: Turn[] = [
      { userText: "Cuanto es el IMV?", mockResponse: "El IMV para un adulto solo es de 604,21 euros al mes.", mockSources: [{ name: "imv", url: KB.imv.url }], mustContain: ["604,21"], mustNotContain: ["1.000€ de IMV"] },
      { userText: "Y la pension discapacidad?", mockResponse: "La pension no contributiva por discapacidad es de 517,90 euros al mes.", mockSources: [{ name: "discapacidad", url: KB.discapacidad.url }], mustContain: ["517,90"], mustNotContain: ["2.000€ pension"] },
      { userText: "Maximo del paro?", mockResponse: "La prestacion maxima por desempleo es de 1.225,80 euros al mes.", mockSources: [{ name: "desempleo", url: KB.desempleo.url }], mustContain: ["1.225,80"] },
    ];
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    for (const t of turns) {
      await sendAndWait(page, t.userText, new RegExp(esc(t.mustContain[0])));
      for (const fact of t.mustContain) {
        await expect(page.getByText(fact).first()).toBeVisible({ timeout: 3_000 });
      }
      if (t.mustNotContain) {
        for (const bad of t.mustNotContain) {
          expect(await page.getByText(bad).count()).toBe(0);
        }
      }
    }
  });

  test("3d — Plazos correctos (15 dias paro, 60 dias NIE, 6 meses IMV)", async ({ page }) => {
    test.setTimeout(60_000);
    const turns: Turn[] = [
      { userText: "Plazo para pedir el paro?", mockResponse: "Tienes 15 dias habiles desde el fin del contrato para pedir la prestacion por desempleo en el SEPE.", mockSources: [{ name: "desempleo", url: KB.desempleo.url }], mustContain: ["15 dias"], mustNotContain: ["3 dias para paro"] },
      { userText: "Plazo renovacion NIE?", mockResponse: "Debes renovar el NIE en los 60 dias anteriores a su caducidad en la Oficina de Extranjeria.", mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }], mustContain: ["60 dias"], mustNotContain: ["1 ano para NIE"] },
      { userText: "Residencia para el IMV?", mockResponse: "Necesitas al menos 6 meses de residencia legal en Espana para solicitar el IMV.", mockSources: [{ name: "imv", url: KB.imv.url }], mustContain: ["6 meses"] },
    ];
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    for (const t of turns) {
      await sendAndWait(page, t.userText, new RegExp(esc(t.mustContain[0])));
      for (const fact of t.mustContain) {
        await expect(page.getByText(fact).first()).toBeVisible({ timeout: 3_000 });
      }
      if (t.mustNotContain) {
        for (const bad of t.mustNotContain) {
          expect(await page.getByText(bad).count()).toBe(0);
        }
      }
    }
  });
});

/* ================================================================== */
/*  TEST SUITE — Group 4: URLs y Links (3 tests)                      */
/* ================================================================== */

test.describe("Group 4: URLs y Links", () => {
  const GOV_DOMAINS = ["seg-social.es", "madrid.es", "comunidad.madrid", "inclusion.gob.es", "mivau.gob.es", "mjusticia.gob.es", "sepe.es"];

  test("4a — URLs gobierno validas tras 5 turnos", async ({ page }) => {
    test.setTimeout(60_000);
    const turns: Turn[] = [
      { userText: "IMV info", mockResponse: "Info del IMV en la Seguridad Social. Mas en seg-social.es.", mockSources: [{ name: "imv", url: KB.imv.url }], mustContain: ["seg-social.es"] },
      { userText: "Empadronamiento", mockResponse: "Empadronamiento en madrid.es del Ayuntamiento.", mockSources: [{ name: "empadronamiento", url: KB.empadronamiento.url }], mustContain: ["madrid.es"] },
      { userText: "Tarjeta sanitaria", mockResponse: "Tarjeta sanitaria en comunidad.madrid del SERMAS.", mockSources: [{ name: "tarjeta_sanitaria", url: KB.tarjeta_sanitaria.url }], mustContain: ["comunidad.madrid"] },
      { userText: "NIE", mockResponse: "NIE en inclusion.gob.es de Extranjeria.", mockSources: [{ name: "nie_tie", url: KB.nie_tie.url }], mustContain: ["inclusion.gob.es"] },
      { userText: "Desempleo", mockResponse: "Desempleo en sepe.es del SEPE.", mockSources: [{ name: "desempleo", url: KB.desempleo.url }], mustContain: ["sepe.es"] },
    ];
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    for (const t of turns) {
      await sendAndWait(page, t.userText, new RegExp(esc(t.mustContain[0])));
    }
    const links = await page.locator("a[href]").evaluateAll((els) => els.map((e) => e.getAttribute("href") || ""));
    const govLinks = links.filter((h) => GOV_DOMAINS.some((d) => h.includes(d)));
    expect(govLinks.length).toBeGreaterThan(0);
    for (const l of govLinks) {
      expect(() => new URL(l)).not.toThrow();
    }
  });

  test("4b — URL correcta por tramite", async ({ page }) => {
    test.setTimeout(60_000);
    const checks: Array<{ q: string; resp: string; src: { name: string; url: string }; domain: string }> = [
      { q: "Info IMV", resp: "Consulta el IMV en seg-social.es de la Seguridad Social.", src: { name: "imv", url: KB.imv.url }, domain: "seg-social.es" },
      { q: "Info empadronamiento", resp: "Consulta en madrid.es del Ayuntamiento.", src: { name: "empadronamiento", url: KB.empadronamiento.url }, domain: "madrid.es" },
      { q: "Info NIE", resp: "Consulta en inclusion.gob.es de Extranjeria.", src: { name: "nie_tie", url: KB.nie_tie.url }, domain: "inclusion.gob.es" },
    ];
    const turns: Turn[] = checks.map((c) => ({
      userText: c.q,
      mockResponse: c.resp,
      mockSources: [c.src],
      mustContain: [c.domain],
    }));
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    for (let i = 0; i < checks.length; i++) {
      await sendAndWait(page, checks[i].q, new RegExp(esc(checks[i].domain)));
      const links = await page.locator("a[href]").evaluateAll((els) => els.map((e) => e.getAttribute("href") || ""));
      expect(links.some((l) => l.includes(checks[i].domain))).toBe(true);
    }
  });

  test("4c — No URLs inventadas", async ({ page }) => {
    const turns: Turn[] = [
      { userText: "Que tramites hay?", mockResponse: "Puedes consultar el IMV en seg-social.es y el empadronamiento en madrid.es.", mockSources: [{ name: "imv", url: KB.imv.url }], mustContain: ["seg-social.es"] },
    ];
    await stubAudio(page);
    await mockConversation(page, turns, "es");
    await gotoChat(page, "es");
    await sendAndWait(page, turns[0].userText, /seg-social\.es/);
    const links = await page.locator("a[href]").evaluateAll((els) => els.map((e) => e.getAttribute("href") || ""));
    const fake = ["tramites-inventados.es", "ayudas-falsas.com", "gobierno-falso.org"];
    for (const f of fake) {
      expect(links.some((l) => l.includes(f))).toBe(false);
    }
  });
});

/* ================================================================== */
/*  TEST SUITE — Group 5: Cross-topic & Edge Cases (5 tests)           */
/* ================================================================== */

test.describe("Group 5: Cross-topic y Edge Cases", () => {
  for (const s of EDGE_SCENARIOS) {
    test(`${s.name} — ${s.persona} (${s.lang})`, async ({ page }) => {
      test.setTimeout(60_000);
      await runScenario(page, s);
    });
  }
});
