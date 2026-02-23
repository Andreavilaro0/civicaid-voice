/**
 * Comprehensive conversation scenarios for 100+ E2E tests.
 *
 * Covers uncommon tramites, real addresses, phone numbers, URLs,
 * factual accuracy, and multi-language long conversations.
 */

import type { ConversationScenario } from "./conversation-scenarios";

/* ══════════════════════════════════════════════════════════════════
 *  1. NIE / TIE — Deep procedural flow (ES, 10 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const nieTieES: ConversationScenario = {
  name: "NIE/TIE procedures (ES)",
  language: "es",
  turns: [
    {
      userMessage: "¿Qué diferencia hay entre el NIE y el TIE?",
      claraResponse:
        "El NIE (Numero de Identidad de Extranjero) es un numero unico que te identifica como extranjero en Espana. Todos los extranjeros que hacen tramites en Espana lo necesitan.\n\nEl TIE (Tarjeta de Identidad de Extranjero) es la tarjeta fisica que acredita tu permiso de residencia o estancia. Contiene tu NIE, foto y tipo de permiso.\n\nResumen: el NIE es el numero, el TIE es la tarjeta.",
      source: "llm",
      delayMs: 800,
      mustContain: ["Numero de Identidad de Extranjero", "Tarjeta de Identidad de Extranjero"],
      mustNotContain: ["pasaporte"],
    },
    {
      userMessage: "¿Dónde pido cita para el NIE en Madrid?",
      claraResponse:
        "Para pedir cita para el NIE en Madrid, ve a la sede electronica:\n\nhttps://sede.administracionespublicas.gob.es\n\nSelecciona 'Madrid' como provincia y elige 'Policia - Certificados y asignacion de NIE'.\n\nLas oficinas principales en Madrid son:\n- Oficina de Extranjeria: C/ Garcia de Paredes, 65 (metro Iglesia)\n- Comisaria de Aluche: C/ Jose Caballero, 3\n- Comisaria de la Policia Nacional en Tres Cantos\n\nLas citas se agotan rapido. Intenta a las 8:00 de la manana cuando se liberan nuevas.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["sede.administracionespublicas.gob.es", "Garcia de Paredes"],
    },
    {
      userMessage: "¿Qué documentos necesito para el NIE?",
      claraResponse:
        "Para solicitar el NIE necesitas:\n\n1. Formulario EX-15 (rellenado y firmado)\n2. Pasaporte original y copia\n3. Justificacion del motivo: contrato de trabajo, matricula universitaria, compraventa de vivienda, etc.\n4. Tasa 790 codigo 012 pagada (aproximadamente 12 EUR)\n5. Foto tamano carnet\n\nPuedes descargar el formulario EX-15 en:\nhttps://sede.administracionespublicas.gob.es/pagina/index/directorio/icpplus",
      source: "llm",
      delayMs: 900,
      mustContain: ["EX-15", "790", "012"],
    },
    {
      userMessage: "¿Cuánto cuesta la tasa?",
      claraResponse:
        "La tasa para el NIE es la Tasa 790, codigo 012. El importe actual es de 12,00 EUR.\n\nPuedes pagarla en cualquier banco con el modelo rellenado, o descargarlo desde:\nhttps://sede.policia.gob.es/Tasa790_012/\n\nImportante: debes pagar ANTES de la cita. Sin el justificante de pago no te atienden.",
      source: "llm",
      delayMs: 700,
      mustContain: ["12", "790", "012"],
      mustNotContain: ["50 EUR", "100 EUR"],
    },
    {
      userMessage: "¿Y para el TIE qué necesito?",
      claraResponse:
        "Para solicitar el TIE necesitas:\n\n1. Formulario EX-17\n2. Pasaporte original y copia\n3. 3 fotos tamano carnet fondo blanco\n4. Resolucion favorable de tu permiso de residencia\n5. Tasa 790 codigo 012 (12 EUR por el NIE si no lo tienes) + Tasa 790 codigo 062 (por la tarjeta, aprox 7,50 EUR)\n6. Certificado de empadronamiento\n7. Seguro medico o alta en Seguridad Social\n\nPlazo: 1 mes desde la resolucion favorable.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["EX-17", "062"],
    },
    {
      userMessage: "¿Qué es la tasa 062?",
      claraResponse:
        "La Tasa 790 codigo 062 es la tasa por expedicion de la tarjeta TIE. Su importe actual es de aproximadamente 7,50 EUR.\n\nEs diferente de la tasa 012 (asignacion de NIE). Si solicitas el TIE por primera vez, normalmente pagas las dos:\n- 012: asignacion NIE (12 EUR)\n- 062: expedicion tarjeta (7,50 EUR)\n\nTotal: unos 19,50 EUR.\n\nDescarga el modelo en: https://sede.policia.gob.es/Tasa790_062/",
      source: "llm",
      delayMs: 800,
      mustContain: ["7,50", "062"],
    },
    {
      userMessage: "¿Cuánto tarda en llegar el TIE?",
      claraResponse:
        "Tras la cita de huella dactilar, el TIE tarda normalmente entre 30 y 45 dias en estar listo.\n\nMientras tanto, te dan un resguardo que sirve como documento provisional.\n\nPuedes consultar el estado en:\nhttps://sede.administracionespublicas.gob.es/infoext2/jsp/indexie.jsp\n\nCuando este listo, recibes un SMS o puedes consultar online. Luego vas a recogerlo con tu pasaporte a la misma oficina.",
      source: "llm",
      delayMs: 800,
      mustContain: ["30", "45", "huella"],
    },
    {
      userMessage: "¿Puedo trabajar mientras espero el TIE?",
      claraResponse:
        "Si, si tu resolucion de autorizacion de residencia y trabajo es favorable, puedes trabajar desde el momento en que la recibes, sin necesidad de esperar al TIE fisico.\n\nEl resguardo de solicitud del TIE, junto con la resolucion favorable, te acreditan legalmente.\n\nTu empleador puede darte de alta en la Seguridad Social con el NIE y la resolucion.",
      source: "llm",
      delayMs: 700,
      mustContain: ["resolucion", "resguardo"],
    },
    {
      userMessage: "¿Y si me caduca el TIE?",
      claraResponse:
        "Si se te caduca el TIE, debes renovarlo:\n\n1. Solicita la renovacion en los 60 dias previos al vencimiento o hasta 90 dias despues\n2. Pide cita en https://sede.administracionespublicas.gob.es\n3. Necesitas: formulario EX-17, pasaporte, TIE caducado, foto, tasa 012, empadronamiento\n4. Justifica que sigues cumpliendo requisitos (contrato vigente, etc.)\n\nImportante: mientras tramitas la renovacion, tu estancia sigue siendo legal aunque el TIE este caducado, siempre que hayas solicitado dentro de plazo.",
      source: "llm",
      delayMs: 900,
      mustContain: ["60 dias", "90 dias", "renovacion"],
    },
    {
      userMessage: "Gracias Clara, muy completo",
      claraResponse:
        "De nada! Los tramites de extranjeria pueden ser complicados pero paso a paso se consiguen. Recuerda que las oficinas de extranjeria y los servicios sociales de tu ayuntamiento pueden orientarte si tienes dudas.\n\nMucho animo!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  2. Asilo y refugio (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const asiloES: ConversationScenario = {
  name: "Asilo y proteccion internacional (ES)",
  language: "es",
  turns: [
    {
      userMessage: "Acabo de llegar a España y quiero pedir asilo",
      claraResponse:
        "Tienes derecho a solicitar proteccion internacional (asilo) en Espana. Puedes hacerlo:\n\n1. En la frontera (puesto fronterizo, aeropuerto)\n2. En una Oficina de Asilo y Refugio (OAR)\n3. En cualquier Oficina de Extranjeria\n4. En un Centro de Internamiento de Extranjeros (CIE)\n\nEl plazo es de 1 mes desde tu llegada a Espana.\n\nLa Oficina de Asilo y Refugio (OAR) esta en Madrid: C/ Pradillo, 40.",
      source: "llm",
      delayMs: 900,
      mustContain: ["proteccion internacional", "OAR", "Pradillo, 40", "1 mes"],
    },
    {
      userMessage: "¿Qué pasa después de pedirlo?",
      claraResponse:
        "Despues de solicitar asilo:\n\n1. Te hacen una entrevista personal\n2. Recibes un documento provisional (tarjeta roja) que te identifica\n3. La tarjeta roja se renueva cada 6 meses\n4. A los 6 meses de la solicitud, puedes obtener autorizacion para trabajar\n5. La resolucion puede tardar entre 6 meses y 2 anos\n\nMientras tanto, tienes derecho a:\n- Asistencia sanitaria\n- Alojamiento (si no tienes recursos)\n- Asistencia juridica gratuita\n- Educacion para menores",
      source: "llm",
      delayMs: 1000,
      mustContain: ["tarjeta roja", "6 meses", "trabajar"],
    },
    {
      userMessage: "¿Dónde me dan alojamiento?",
      claraResponse:
        "El sistema de acogida para solicitantes de asilo en Espana tiene varias fases:\n\n1. Fase de acogida temporal: Centros del Ministerio (CREADE) o gestionados por ONGs como CEAR, ACCEM, Cruz Roja\n2. Fase de autonomia: ayuda economica para alquilar vivienda\n\nOrganizaciones que te ayudan:\n- CEAR: 91 441 55 00 / www.cear.es\n- ACCEM: 91 532 74 78 / www.accem.es\n- Cruz Roja: 900 22 22 92\n- ACNUR (informacion): www.acnur.org\n\nContacta con cualquiera de estas organizaciones, te orientaran.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["CEAR", "ACCEM", "Cruz Roja"],
    },
    {
      userMessage: "¿Puedo trabajar con la tarjeta roja?",
      claraResponse:
        "Con la tarjeta roja (documento de solicitante de proteccion internacional):\n\n- Primeros 6 meses: NO puedes trabajar legalmente\n- A partir de los 6 meses: SI, automaticamente obtienes autorizacion de trabajo si no has recibido resolucion\n\nNo necesitas un permiso de trabajo adicional. La propia tarjeta roja con mas de 6 meses te habilita.\n\nTu empleador puede verificarlo con el numero de tu tarjeta.",
      source: "llm",
      delayMs: 800,
      mustContain: ["6 meses", "tarjeta roja"],
    },
    {
      userMessage: "¿Me pueden deportar mientras tramitan mi asilo?",
      claraResponse:
        "No. Mientras tu solicitud de asilo esta en tramite, tienes el principio de no devolucion (non-refoulement). Esto significa que:\n\n1. No pueden expulsarte ni deportarte al pais de origen\n2. No pueden devolverte en frontera\n3. Tienes derecho a permanecer en Espana hasta que haya resolucion\n\nEste derecho esta protegido por la Convencion de Ginebra de 1951, la ley espanola 12/2009 y el derecho europeo.\n\nSi recibes alguna orden de expulsion, contacta inmediatamente con un abogado o con CEAR.",
      source: "llm",
      delayMs: 900,
      mustContain: ["no devolucion", "Convencion de Ginebra", "12/2009"],
    },
    {
      userMessage: "¿Y si me deniegan el asilo?",
      claraResponse:
        "Si te deniegan la solicitud de asilo:\n\n1. Recurso de reposicion: 1 mes ante la misma Oficina\n2. Recurso contencioso-administrativo: 2 meses ante la Audiencia Nacional\n3. Tienes derecho a asistencia juridica gratuita para recurrir\n\nMientras recurres, normalmente puedes seguir en Espana.\n\nAdemás, puedes solicitar proteccion subsidiaria (un nivel menor de proteccion) o autorizacion de residencia por razones humanitarias, por arraigo social (3 anos en Espana) u otras vias.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Audiencia Nacional", "recurso", "arraigo"],
    },
    {
      userMessage: "¿Qué es el arraigo social?",
      claraResponse:
        "El arraigo social es una autorizacion de residencia temporal para personas en situacion irregular que llevan al menos 3 anos en Espana de forma continuada. Requisitos:\n\n1. 3 anos de permanencia continuada en Espana (documentable)\n2. Sin antecedentes penales\n3. Contrato de trabajo de al menos 1 ano, O informe de insercion social del ayuntamiento\n4. Vinculacion con Espana (empadronamiento, cursos, asociaciones)\n\nDuracion: 1 ano renovable. Se solicita en la Oficina de Extranjeria de tu provincia.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["3 anos", "antecedentes penales", "contrato de trabajo"],
    },
    {
      userMessage: "Muchas gracias, me has tranquilizado mucho",
      claraResponse:
        "Me alegro mucho. Recuerda que no estas solo/a en este proceso. Las organizaciones como CEAR, ACCEM y Cruz Roja tienen equipos especializados que te acompanan en todo el tramite.\n\nSi necesitas algo mas, aqui estoy. Mucho animo y fuerza.",
      source: "llm",
      delayMs: 500,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  3. Asistencia juridica gratuita (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const asistenciaJuridicaES: ConversationScenario = {
  name: "Asistencia juridica gratuita (ES)",
  language: "es",
  turns: [
    {
      userMessage: "¿Puedo tener un abogado gratis?",
      claraResponse:
        "Si! En Espana existe el derecho a la asistencia juridica gratuita. Incluye:\n\n1. Abogado de oficio gratuito\n2. Procurador gratuito\n3. Exencion de tasas judiciales\n4. Peritos gratuitos\n\nLo regulan la Ley 1/1996 de Asistencia Juridica Gratuita y modificaciones posteriores.",
      source: "llm",
      delayMs: 800,
      mustContain: ["abogado de oficio", "Ley 1/1996"],
    },
    {
      userMessage: "¿Quién tiene derecho?",
      claraResponse:
        "Tienen derecho a asistencia juridica gratuita:\n\n1. Personas con ingresos brutos inferiores a 2 veces el IPREM (aprox. 1.200 EUR/mes en 2025)\n2. Victimas de violencia de genero (independientemente de ingresos)\n3. Victimas de terrorismo\n4. Menores de edad\n5. Personas con discapacidad (33% o mas)\n6. Victimas de trata\n7. Solicitantes de asilo\n\nSi eres extranjero en situacion irregular, tambien tienes derecho en procedimientos penales, de asilo y de extranjeria.",
      source: "llm",
      delayMs: 900,
      mustContain: ["IPREM", "violencia de genero", "discapacidad"],
    },
    {
      userMessage: "¿Dónde lo solicito?",
      claraResponse:
        "Solicita la asistencia juridica gratuita en el Colegio de Abogados de tu provincia:\n\n- Madrid: Colegio de Abogados de Madrid (ICAM), C/ Serrano, 9 — Tel: 91 788 93 80\n- Barcelona: ICAB, C/ Mallorca, 283 — Tel: 93 496 18 80\n- Valencia: ICAV, Plaza Tetuan, 16 — Tel: 96 394 12 90\n\nTambien puedes solicitarlo en el Juzgado donde se tramite tu caso.\n\nOnline: https://www.justiciagratuita.es (en algunas comunidades)",
      source: "llm",
      delayMs: 1000,
      mustContain: ["Colegio de Abogados", "Serrano, 9"],
    },
    {
      userMessage: "¿Cuánto tardan en asignarme abogado?",
      claraResponse:
        "El plazo legal es de 15 dias habiles desde que presentas la solicitud.\n\nEn la practica:\n- Casos urgentes (detencion, violencia de genero): se asigna en 24 horas\n- Casos normales: 1-3 semanas\n- En grandes ciudades con mucha demanda puede ser algo mas\n\nSi no recibes respuesta en 15 dias, se entiende concedida por silencio positivo.",
      source: "llm",
      delayMs: 800,
      mustContain: ["15 dias"],
    },
    {
      userMessage: "¿Puedo elegir al abogado?",
      claraResponse:
        "Normalmente no eliges: se asigna por turno de oficio del Colegio de Abogados.\n\nPero hay excepciones:\n1. Si ya tenias un abogado de oficio en un caso relacionado, puedes pedir que sea el mismo\n2. Puedes rechazar al abogado asignado (maximo 3 veces) con justificacion\n3. Si encuentras un abogado particular dispuesto a actuar gratis, puedes designarlo\n\nSi no estas conforme con tu abogado, puedes presentar queja ante el Colegio de Abogados.",
      source: "llm",
      delayMs: 800,
      mustContain: ["turno de oficio", "Colegio de Abogados"],
    },
    {
      userMessage: "¿Qué pasa si gano dinero después?",
      claraResponse:
        "Si tu situacion economica mejora en los 3 anos siguientes a recibir la asistencia juridica gratuita y superas el limite de ingresos (2x IPREM), podrias tener que devolver los costes.\n\nPero solo si:\n- Tus ingresos superan el limite durante 3 anos seguidos\n- La Comision de Asistencia Juridica Gratuita te lo reclama\n\nEn la practica es poco frecuente. No te preocupes por esto si ahora lo necesitas.",
      source: "llm",
      delayMs: 700,
      mustContain: ["3 anos", "IPREM"],
    },
    {
      userMessage: "¿Sirve para temas de extranjeria?",
      claraResponse:
        "Si! La asistencia juridica gratuita cubre especificamente:\n\n1. Procedimientos de asilo (obligatorio tener abogado)\n2. Denegacion de entrada en frontera\n3. Ordenes de expulsion\n4. Recursos contra denegacion de permisos\n5. Procedimientos de arraigo\n\nPara temas de extranjeria, el abogado de oficio es fundamental. Muchas denegaciones se revierten con un buen recurso.\n\nContacta con el turno de extranjeria de tu Colegio de Abogados.",
      source: "llm",
      delayMs: 900,
      mustContain: ["asilo", "expulsion", "arraigo"],
    },
    {
      userMessage: "Perfecto, gracias Clara",
      claraResponse:
        "De nada! La asistencia juridica gratuita es un derecho muy importante que mucha gente no conoce. No dudes en usarlo si lo necesitas.\n\nEstoy aqui para cualquier otra consulta. Animo!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  4. Ayudas de vivienda y bono alquiler (ES, 10 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const viviendaES: ConversationScenario = {
  name: "Ayudas vivienda y bono alquiler (ES)",
  language: "es",
  turns: [
    {
      userMessage: "No puedo pagar el alquiler, ¿hay ayudas?",
      claraResponse:
        "Si, hay varias ayudas para el alquiler en Espana:\n\n1. Bono Alquiler Joven: para menores de 35 anos, 250 EUR/mes durante 2 anos\n2. Ayudas al alquiler del Plan Estatal de Vivienda: hasta el 50% del alquiler\n3. Ayudas de emergencia de tu comunidad autonoma\n4. Prestaciones de urgencia social del ayuntamiento\n\nLo primero es acudir a los servicios sociales de tu ayuntamiento para valorar tu situacion.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Bono Alquiler Joven", "250", "servicios sociales"],
    },
    {
      userMessage: "Tengo 28 años, ¿puedo pedir el bono joven?",
      claraResponse:
        "Si! Con 28 anos cumples el requisito de edad (hasta 35 anos). Los requisitos del Bono Alquiler Joven son:\n\n1. Tener entre 18 y 35 anos\n2. Ingresos anuales inferiores a 3 veces el IPREM (aprox. 24.300 EUR brutos/ano)\n3. Ser titular de un contrato de alquiler\n4. Alquiler maximo de 600 EUR/mes (900 EUR en zonas tensionadas)\n5. Estar empadronado en la vivienda\n\nLa ayuda es de 250 EUR/mes durante 2 anos.",
      source: "llm",
      delayMs: 800,
      mustContain: ["35 anos", "IPREM", "250", "2 anos"],
    },
    {
      userMessage: "¿Dónde lo solicito?",
      claraResponse:
        "El Bono Alquiler Joven se solicita en tu comunidad autonoma:\n\n- Madrid: Direccion General de Vivienda, www.comunidad.madrid/servicios/vivienda\n- Cataluna: Agencia de l'Habitatge, www.habitatge.gencat.cat\n- Andalucia: Consejeria de Fomento, www.juntadeandalucia.es/organismos/fomento\n- Comunidad Valenciana: www.gva.es/es/inicio/area_de_prensa/noticias\n\nGeneralmente se hace por via telematica con certificado digital o Cl@ve.\n\nLas convocatorias suelen abrirse entre enero y marzo.",
      source: "llm",
      delayMs: 900,
      mustContain: ["comunidad autonoma"],
    },
    {
      userMessage: "No tengo certificado digital",
      claraResponse:
        "Sin certificado digital, tienes opciones:\n\n1. Cl@ve: Puedes registrarte por videollamada o presencialmente en oficinas de la Seguridad Social, Hacienda, o ayuntamientos. Es rapido y te sirve para muchos tramites.\n\n2. Presencial: Muchas comunidades permiten solicitar la ayuda presencialmente en las oficinas de vivienda.\n\n3. Servicios sociales: Pueden ayudarte a tramitarlo.\n\nPara obtener Cl@ve rapido:\n- Online con videollamada: https://clave.gob.es\n- Presencial: en oficinas de la AEAT, TGSS o correos.",
      source: "llm",
      delayMs: 800,
      mustContain: ["Cl@ve", "clave.gob.es"],
    },
    {
      userMessage: "¿Y si no cumplo para el bono joven?",
      claraResponse:
        "Si no cumples para el Bono Joven, hay otras ayudas:\n\n1. Ayudas al alquiler del Plan Estatal de Vivienda: hasta el 50% del alquiler, sin limite de edad\n2. Ayuda de emergencia social: tu ayuntamiento puede darte ayuda puntual para alquileres atrasados\n3. Renta minima de tu comunidad (RMI, REMI, etc.) que incluye ayuda para vivienda\n4. IMV (Ingreso Minimo Vital): complemento de vivienda si tienes alquiler\n\nVe a servicios sociales y explica tu situacion. Ellos valoran que ayudas te corresponden.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Plan Estatal", "IMV"],
    },
    {
      userMessage: "¿Me pueden echar si no pago?",
      claraResponse:
        "El proceso de desahucio por impago tiene plazos y protecciones:\n\n1. El propietario debe reclamarte judicialmente (no puede echarte por las buenas)\n2. Tienes derecho a enervar (pagar lo debido) y parar el desahucio la primera vez\n3. Los servicios sociales deben valorar tu vulnerabilidad\n4. Si hay menores, mayores o personas con discapacidad, el juez puede suspender el desahucio\n\nImportante: si recibes un requerimiento de pago, contacta inmediatamente con servicios sociales o con un abogado de oficio (gratuito).",
      source: "llm",
      delayMs: 1000,
      mustContain: ["desahucio", "enervar", "vulnerabilidad"],
    },
    {
      userMessage: "¿Hay vivienda social?",
      claraResponse:
        "Si, la Vivienda de Proteccion Oficial (VPO) y la vivienda social existen pero hay mucha demanda:\n\n1. Viviendas publicas en alquiler social: gestionadas por el IVIMA (Madrid), INCASOL (Cataluna), etc.\n2. Registro de demandantes de VPO: inscribete en tu comunidad autonoma\n3. Alquiler social de los bancos: mediante el Fondo Social de Vivienda (pisos de bancos a bajo precio)\n\nPara inscribirte como demandante de vivienda, ve a la oficina de vivienda de tu comunidad.\n\nListas de espera: pueden ser de varios anos, pero vale la pena apuntarse.",
      source: "llm",
      delayMs: 900,
      mustContain: ["VPO", "Fondo Social"],
    },
    {
      userMessage: "¿Qué es el Fondo Social de Vivienda?",
      claraResponse:
        "El Fondo Social de Vivienda es un convenio entre el Gobierno y los principales bancos para ofrecer viviendas en alquiler a precios muy bajos (entre 150 y 400 EUR/mes) a personas en situacion de especial vulnerabilidad:\n\n- Familias desahuciadas\n- Familias con todos los miembros en paro\n- Familias monoparentales con hijos\n- Victimas de violencia de genero\n\nInforma en tu ayuntamiento o en los servicios sociales. Tambien puedes consultar la web de tu banco.",
      source: "llm",
      delayMs: 800,
      mustContain: ["150", "400", "vulnerabilidad"],
    },
    {
      userMessage: "¿Los servicios sociales me ayudan con todo esto?",
      claraResponse:
        "Si, los servicios sociales de tu ayuntamiento son tu mejor punto de partida. Alli:\n\n1. Valoran tu situacion integral\n2. Te orientan sobre todas las ayudas disponibles\n3. Emiten informes sociales necesarios para muchos tramites\n4. Pueden gestionar ayudas de emergencia directamente\n5. Te derivan a recursos especializados (alojamiento, empleo, legal)\n\nPide cita en los servicios sociales de tu barrio. La atencion es gratuita y confidencial.",
      source: "llm",
      delayMs: 800,
      mustContain: ["servicios sociales", "informes sociales", "gratuita"],
    },
    {
      userMessage: "Gracias Clara, me siento mejor",
      claraResponse:
        "Me alegro! Se que la situacion puede agobiar, pero hay recursos disponibles. Lo mas importante es que des el primer paso: pide cita en servicios sociales.\n\nRecuerda que estoy aqui siempre que necesites informacion. Un abrazo y mucho animo!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  5. SEPE y prestaciones por desempleo (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const desempleoES: ConversationScenario = {
  name: "Prestaciones desempleo SEPE (ES)",
  language: "es",
  turns: [
    {
      userMessage: "Me han despedido, ¿qué hago?",
      claraResponse:
        "Lo primero, tranquilo/a. Tienes derechos. Los pasos inmediatos son:\n\n1. Firma la carta de despido (puedes poner 'no conforme')\n2. Tienes 15 dias habiles para solicitar la prestacion por desempleo en el SEPE\n3. Inscribete como demandante de empleo\n4. Si no estas de acuerdo con el despido, tienes 20 dias habiles para demandar\n\nWeb del SEPE: https://www.sepe.es\nTelefono: 901 119 999 (o 91 273 83 83)\nCita previa: https://sede.sepe.gob.es/citaprevia",
      source: "llm",
      delayMs: 1000,
      mustContain: ["15 dias", "SEPE", "sepe.es"],
    },
    {
      userMessage: "¿Cuánto me toca de paro?",
      claraResponse:
        "La prestacion por desempleo se calcula asi:\n\n- Primeros 180 dias: 70% de tu base reguladora\n- Resto del periodo: 50% de tu base reguladora\n\nLa base reguladora es la media de tus bases de cotizacion de los ultimos 180 dias.\n\nTopes 2025:\n- Maximo sin hijos: ~1.480 EUR/mes\n- Maximo con 2+ hijos: ~1.690 EUR/mes\n- Minimo sin hijos: ~560 EUR/mes\n- Minimo con hijos: ~750 EUR/mes\n\nDuracion: depende de los dias cotizados (minimo 360 dias cotizados = 4 meses de prestacion).",
      source: "llm",
      delayMs: 1000,
      mustContain: ["70%", "50%", "base reguladora", "180 dias"],
    },
    {
      userMessage: "Solo llevo 8 meses trabajando",
      claraResponse:
        "Con 8 meses (aprox. 240 dias cotizados), no llegas al minimo de 360 dias para la prestacion contributiva.\n\nPero puedes solicitar el subsidio por desempleo si:\n1. Has cotizado al menos 3 meses y tienes cargas familiares\n2. Has cotizado al menos 6 meses sin cargas familiares\n\nCon 8 meses SIN cargas familiares -> Si, tienes derecho al subsidio.\n\nEl subsidio es de 480 EUR/mes (80% del IPREM). Duracion: 6 meses.\n\nSolicitalo en el SEPE dentro de los 15 dias habiles.",
      source: "llm",
      delayMs: 900,
      mustContain: ["360 dias", "subsidio", "480", "IPREM"],
    },
    {
      userMessage: "¿Dónde está la oficina del SEPE más cercana en Barcelona?",
      claraResponse:
        "Las principales oficinas del SEPE en Barcelona son:\n\n1. SEPE Barcelona - Sepulveda: C/ Sepulveda, 148-150 (metro Universitat)\n2. SEPE Barcelona - Gran Via: Gran Via de les Corts Catalanes, 680\n3. SEPE Barcelona - Entenza: C/ Entenza, 326\n4. SOC Oficina de Treball (servicio autonomico): C/ Llull, 297\n\nPide cita previa en: https://sede.sepe.gob.es/citaprevia\nO llama al 901 119 999\n\nRecuerda que en Cataluna tambien puedes ir al SOC (Servei d'Ocupacio de Catalunya) para temas de empleo.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Sepulveda", "cita previa", "SOC"],
    },
    {
      userMessage: "¿Puedo trabajar mientras cobro el paro?",
      claraResponse:
        "Si, pero con condiciones:\n\n1. Trabajo a tiempo parcial: Puedes compatibilizar paro + trabajo parcial. Cobras la parte proporcional del paro.\n2. Trabajo por cuenta propia: Puedes capitalizar el paro (cobrar todo de golpe) para montar un negocio.\n3. Trabajos ocasionales: Si trabajas menos de 12 meses, puedes suspender la prestacion y reanudarla despues.\n\nImportante: SIEMPRE comunica al SEPE cualquier cambio. Si no lo haces, te pueden reclamar todo lo cobrado + sancion.",
      source: "llm",
      delayMs: 800,
      mustContain: ["tiempo parcial", "capitalizar"],
    },
    {
      userMessage: "¿Qué es el subsidio extraordinario?",
      claraResponse:
        "El subsidio extraordinario por desempleo (SED) esta pensado para personas que han agotado todas las prestaciones y siguen sin empleo. Requisitos:\n\n1. Haber agotado la prestacion contributiva y/o subsidios\n2. Llevar al menos 1 mes como demandante de empleo\n3. No superar el 75% del SMI en ingresos\n4. Responsabilidades familiares o tener 45+ anos\n\nCuantia: 480 EUR/mes (80% IPREM)\nDuracion: 6 meses\n\nSe solicita en el SEPE. Consulta tambien la Renta Activa de Insercion (RAI) como alternativa.",
      source: "llm",
      delayMs: 900,
      mustContain: ["SED", "480", "RAI"],
    },
    {
      userMessage: "¿Qué es la RAI?",
      claraResponse:
        "La Renta Activa de Insercion (RAI) es una ayuda para personas con especial dificultad de empleo:\n\n1. Desempleados mayores de 45 anos\n2. Victimas de violencia de genero o domestica\n3. Personas con discapacidad igual o superior al 33%\n4. Emigrantes retornados\n\nCuantia: 480 EUR/mes (80% IPREM)\nDuracion: 11 meses, renovable hasta 3 veces (maximo 33 meses)\n\nRequisitos: estar inscrito como demandante 12 meses en los ultimos 18, no superar 75% SMI, no haber cobrado RAI 3 veces.\n\nSolicitud en el SEPE.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Renta Activa de Insercion", "480", "33%", "11 meses"],
    },
    {
      userMessage: "Gracias, me quedo más tranquilo",
      claraResponse:
        "Me alegro! Perder el trabajo es estresante pero tienes proteccion. Lo mas urgente: solicita la prestacion en el SEPE antes de que pasen los 15 dias habiles.\n\nSi necesitas mas ayuda, aqui estoy. Mucho animo!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  6. Discapacidad y dependencia (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const discapacidadES: ConversationScenario = {
  name: "Discapacidad y dependencia (ES)",
  language: "es",
  turns: [
    {
      userMessage: "¿Cómo pido el certificado de discapacidad?",
      claraResponse:
        "El certificado de discapacidad se solicita en tu comunidad autonoma, en los Centros de Valoracion y Orientacion (CVO) o equivalentes:\n\n- Madrid: Centro Base, C/ Maudes, 26 (metro Cuatro Caminos) — Tel: 91 580 37 38\n- Cataluna: CAD (Centre d'Atenció a la Discapacitat)\n- Andalucia: Centro de Valoracion y Orientacion\n\nNecesitas: DNI/NIE, informes medicos actualizados, formulario de solicitud.\n\nLa valoracion determina un porcentaje de discapacidad. A partir del 33% accedes a beneficios.",
      source: "llm",
      delayMs: 900,
      mustContain: ["33%", "Maudes, 26", "Centro Base"],
    },
    {
      userMessage: "¿Qué beneficios da el 33%?",
      claraResponse:
        "Con el 33% de discapacidad reconocida accedes a:\n\n1. Reserva de empleo: empresas de 50+ trabajadores deben tener 2% de personas con discapacidad\n2. Bonificaciones en la contratacion para tu empleador\n3. Deducciones fiscales en el IRPF\n4. Descuentos en transporte publico (abono reducido)\n5. Exencion del impuesto de matriculacion de vehiculos\n6. Acceso a plazas de aparcamiento reservadas\n7. Prestaciones economicas especificas\n8. Acceso a la RAI si estas en desempleo\n\nCon el 65% o mas, las prestaciones son significativamente mayores.",
      source: "llm",
      delayMs: 900,
      mustContain: ["33%", "IRPF", "65%"],
    },
    {
      userMessage: "Mi madre es mayor y necesita ayuda en casa",
      claraResponse:
        "Tu madre puede solicitar la valoracion de dependencia. La Ley 39/2006 de Dependencia establece tres grados:\n\n- Grado I: Dependencia moderada\n- Grado II: Dependencia severa\n- Grado III: Gran dependencia\n\nSegun el grado, puede recibir:\n- Servicio de ayuda a domicilio (horas semanales de cuidador)\n- Tele-asistencia\n- Centro de dia\n- Residencia\n- Prestacion economica para cuidador familiar\n\nSolicitud: en los servicios sociales de tu ayuntamiento o en la comunidad autonoma.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["Ley 39/2006", "Grado I", "Grado II", "Grado III"],
    },
    {
      userMessage: "¿Cuánto tardan en valorarla?",
      claraResponse:
        "El plazo legal es de 6 meses desde la solicitud hasta la resolucion. En la practica, lamentablemente, suele tardar mas:\n\n- Valoracion: 2-4 meses para la visita del equipo\n- Resolucion: 2-6 meses mas\n- Total real: 6-12 meses en muchas comunidades\n\nSi pasan 6 meses sin respuesta, se aplica silencio administrativo positivo (se entiende reconocido el Grado I minimo).\n\nPuedes reclamar por via administrativa si hay retrasos excesivos.",
      source: "llm",
      delayMs: 800,
      mustContain: ["6 meses", "silencio administrativo"],
    },
    {
      userMessage: "¿Le dan dinero por ser dependiente?",
      claraResponse:
        "Si, existen prestaciones economicas vinculadas a la dependencia:\n\n1. Prestacion para cuidador familiar: si un familiar le cuida en casa\n   - Grado II: ~300-400 EUR/mes\n   - Grado III: ~400-700 EUR/mes\n\n2. Prestacion vinculada a servicio: si contrata un servicio privado acreditado\n\n3. Asistente personal: para fomentar la autonomia\n\nLa cuantia exacta depende del grado y la capacidad economica del beneficiario. Se actualiza anualmente.\n\nImportante: el cuidador familiar debe darse de alta en la Seguridad Social.",
      source: "llm",
      delayMs: 900,
      mustContain: ["cuidador familiar", "Seguridad Social"],
    },
    {
      userMessage: "¿Hay ayuda para adaptar la casa?",
      claraResponse:
        "Si! Existen ayudas para adaptar la vivienda:\n\n1. Plan Estatal de Vivienda: subvenciones para accesibilidad (rampas, ascensores, banos adaptados)\n2. Ayudas de la comunidad autonoma para rehabilitacion\n3. Ayudas del ayuntamiento para reformas de accesibilidad\n4. IMSERSO: programas especificos de adaptacion\n\nPueden cubrir hasta el 50-80% del coste de las obras.\n\nConsulta en:\n- Servicios sociales de tu ayuntamiento\n- Oficina de vivienda de tu comunidad autonoma\n- COCEMFE (Confederacion de personas con discapacidad): www.cocemfe.es",
      source: "llm",
      delayMs: 900,
      mustContain: ["accesibilidad", "COCEMFE"],
    },
    {
      userMessage: "¿Y la teleasistencia?",
      claraResponse:
        "La teleasistencia es un servicio que conecta a la persona mayor o dependiente con un centro de atencion 24 horas mediante un dispositivo (pulsera o colgante).\n\n- Coste: gratuito o copago muy bajo (0-10 EUR/mes segun ingresos)\n- Quien lo ofrece: ayuntamientos, Cruz Roja, empresas como Atenzia\n- Que incluye: boton de emergencia, llamadas periodicas de seguimiento, localizacion\n\nPara solicitarla, acude a los servicios sociales de tu ayuntamiento.\n\nEn Madrid: llama al 010 o al 91 480 42 82.",
      source: "llm",
      delayMs: 800,
      mustContain: ["teleasistencia", "24 horas", "Cruz Roja"],
    },
    {
      userMessage: "Muchas gracias Clara, esto me ayuda con mi madre",
      claraResponse:
        "Me alegro mucho de poder ayudarte. Cuidar de nuestros mayores es importante y mereces apoyo para hacerlo.\n\nRecuerda: servicios sociales del ayuntamiento es siempre el primer paso. Ellos te guian por todo el proceso.\n\nMucho animo con tu madre!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  7. Violencia de genero — recursos (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const violenciaGeneroES: ConversationScenario = {
  name: "Violencia de genero recursos (ES)",
  language: "es",
  turns: [
    {
      userMessage: "Necesito ayuda, mi pareja me trata mal",
      claraResponse:
        "Lo primero: no estas sola. Lo que vives tiene nombre y hay muchos recursos para ayudarte.\n\nLineas de atencion inmediata:\n- 016: Telefono de atencion a victimas de violencia de genero (24h, gratuito, no deja rastro en factura)\n- 112: Emergencias si estas en peligro inmediato\n- WhatsApp 016: 600 000 016\n- Email: 016-online@igualdad.gob.es\n\nPuedes llamar aunque no estes segura de querer denunciar. Te escuchan y orientan.",
      source: "llm",
      delayMs: 800,
      mustContain: ["016", "112", "600 000 016"],
    },
    {
      userMessage: "Tengo miedo de denunciar",
      claraResponse:
        "Es completamente normal tener miedo. Quiero que sepas que:\n\n1. La denuncia NO es obligatoria para recibir ayuda\n2. Puedes pedir una orden de proteccion sin denunciar penalmente\n3. Puedes ir a servicios sociales o al 016 sin denunciar\n4. Si decides denunciar, se activan protecciones inmediatas\n\nSi decides denunciar:\n- Puedes ir a cualquier comisaria de Policia o cuartel de Guardia Civil\n- En el juzgado de guardia\n- Tendras abogado/a de oficio gratuito/a inmediatamente\n\nNo tienes que decidir todo hoy. El primer paso es hablar con alguien de confianza.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["orden de proteccion", "abogado"],
    },
    {
      userMessage: "¿Qué es la orden de protección?",
      claraResponse:
        "La orden de proteccion es una medida judicial urgente que incluye:\n\n1. Prohibicion de acercamiento del agresor\n2. Salida del agresor del domicilio\n3. Uso de la vivienda para ti y tus hijos\n4. Custodia provisional de menores\n5. Pension alimenticia provisional\n\nSe tramita en 72 horas maximo por el Juzgado de Violencia sobre la Mujer.\n\nCon la orden de proteccion accedes automaticamente a:\n- RAI (480 EUR/mes)\n- Asistencia juridica gratuita\n- Prioridad en vivienda social\n- Ayuda economica del articulo 27 de la Ley 1/2004",
      source: "llm",
      delayMs: 1000,
      mustContain: ["72 horas", "Ley 1/2004", "RAI"],
    },
    {
      userMessage: "¿Hay casas de acogida?",
      claraResponse:
        "Si, existen centros de acogida (casas de emergencia y pisos tutelados):\n\n1. Centros de emergencia: acogida inmediata (24-72 horas)\n2. Casas de acogida: estancia media (3-12 meses)\n3. Pisos tutelados: estancia larga con apoyo para la autonomia\n\nPara acceder:\n- Llama al 016\n- Acude a servicios sociales de tu ayuntamiento\n- Policia puede derivarte directamente en situacion de emergencia\n\nLa ubicacion es confidencial por seguridad.\n\nTambien: la Delegacion del Gobierno contra la Violencia de Genero coordina recursos en toda Espana.",
      source: "llm",
      delayMs: 900,
      mustContain: ["casas de acogida", "confidencial", "016"],
    },
    {
      userMessage: "Soy extranjera sin papeles, ¿puedo pedir ayuda?",
      claraResponse:
        "Si, rotundamente si. La ley espanola protege a TODAS las victimas de violencia de genero, independientemente de tu situacion administrativa:\n\n1. Puedes denunciar sin miedo a ser expulsada\n2. Si denuncias, se suspende cualquier expediente de expulsion\n3. Puedes obtener autorizacion de residencia y trabajo por circunstancias excepcionales\n4. Tienes derecho a asistencia juridica gratuita\n5. Acceso a centros de acogida, ayudas economicas y sanitarias\n\nEsto esta protegido por el articulo 31 bis de la Ley de Extranjeria.\n\nNo dejes que tu situacion migratoria te impida pedir ayuda.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["31 bis", "residencia y trabajo", "expulsion"],
    },
    {
      userMessage: "¿Mis hijos también reciben protección?",
      claraResponse:
        "Si. Desde la Ley 8/2015, los menores expuestos a violencia de genero son reconocidos como victimas directas. Tienen derecho a:\n\n1. Asistencia psicologica gratuita\n2. Inclusion en la orden de proteccion\n3. Modificacion de la custodia y regimen de visitas\n4. Atencion educativa prioritaria\n5. Becas y ayudas especificas\n\nEl agresor puede perder la patria potestad si hay riesgo para los menores.\n\nLos Puntos de Encuentro Familiar son espacios seguros para los intercambios de menores si hay regimen de visitas.",
      source: "llm",
      delayMs: 900,
      mustContain: ["victimas directas", "Ley 8/2015", "patria potestad"],
    },
    {
      userMessage: "¿Hay ayudas económicas?",
      claraResponse:
        "Si, hay varias ayudas economicas para victimas de violencia de genero:\n\n1. RAI (Renta Activa de Insercion): 480 EUR/mes, 11 meses\n2. Ayuda economica art. 27 Ley 1/2004: pago unico equivalente a 6-18 meses de subsidio\n3. IMV: acceso preferente, sin periodo minimo de residencia\n4. Ayudas de emergencia social del ayuntamiento\n5. Bonificaciones en alquiler y vivienda social prioritaria\n6. Exencion de tasas (DNI, permisos, etc.)\n\nNinguna de estas ayudas requiere denuncia penal. La acreditacion puede ser por orden de proteccion, informe del Ministerio Fiscal, o informe de servicios sociales.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["RAI", "480", "art. 27", "IMV"],
    },
    {
      userMessage: "Gracias Clara, voy a llamar al 016",
      claraResponse:
        "Eso es un paso muy valiente e importante. Recuerda: el 016 es gratuito, confidencial, disponible 24 horas y no deja rastro en la factura del telefono.\n\nTambien puedes escribir al WhatsApp 600 000 016 si prefieres no llamar.\n\nNo estas sola. Hay mucha gente preparada para ayudarte. Mucha fuerza y cuidate.",
      source: "llm",
      delayMs: 500,
      mustContain: ["016", "600 000 016"],
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  8. Reagrupacion familiar (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const reagrupacionES: ConversationScenario = {
  name: "Reagrupacion familiar (ES)",
  language: "es",
  turns: [
    {
      userMessage: "Quiero traer a mi familia a España",
      claraResponse:
        "Para traer a tu familia a Espana puedes solicitar la reagrupacion familiar. Requisitos principales:\n\n1. Tener residencia legal en Espana (al menos 1 ano y renovada para otro ano mas)\n2. Medios economicos suficientes\n3. Vivienda adecuada (informe de adecuacion del ayuntamiento)\n\nPuedes reagrupar a:\n- Conyuge o pareja de hecho\n- Hijos menores de 18 anos\n- Ascendientes (padres) mayores de 65 anos en ciertos casos",
      source: "llm",
      delayMs: 900,
      mustContain: ["residencia legal", "1 ano", "vivienda adecuada"],
    },
    {
      userMessage: "¿Qué medios económicos necesito?",
      claraResponse:
        "Los medios economicos requeridos se calculan en base al IPREM:\n\n- Para reagrupar 1 familiar: 150% del IPREM (aprox. 900 EUR/mes)\n- Para cada familiar adicional: +50% del IPREM (aprox. 300 EUR/mes mas)\n\nSe acredita con:\n- Nominas de los ultimos 6 meses\n- Contrato de trabajo vigente\n- Declaracion de la renta\n- Extractos bancarios\n\nNo se exige un importe fijo total, sino que demuestres ingresos estables y suficientes.",
      source: "llm",
      delayMs: 800,
      mustContain: ["IPREM", "150%"],
    },
    {
      userMessage: "¿Cómo consigo el informe de vivienda?",
      claraResponse:
        "El informe de adecuacion de vivienda lo emite tu ayuntamiento. Demuestra que tu casa tiene condiciones minimas para la familia:\n\n1. Superficie minima por persona (varia segun municipio, generalmente 10-15 m2/persona)\n2. Condiciones de habitabilidad (luz, agua, calefaccion)\n3. No hacinamiento\n\nSolicitalo en los servicios sociales o en la oficina de vivienda de tu ayuntamiento.\n\nPlazo: suele tardar 1-3 meses.\n\nCoste: gratuito o tasa minima segun el ayuntamiento.\n\nSi alquilas, necesitas contrato a tu nombre.",
      source: "llm",
      delayMs: 800,
      mustContain: ["adecuacion", "habitabilidad", "ayuntamiento"],
    },
    {
      userMessage: "¿Dónde presento la solicitud?",
      claraResponse:
        "La solicitud de reagrupacion familiar se presenta en:\n\n1. Oficina de Extranjeria de tu provincia\n2. Online: https://sede.administracionespublicas.gob.es (con certificado digital)\n\nFormulario: EX-02 (Solicitud de autorizacion de residencia por reagrupacion familiar)\n\nDocumentos:\n- Formulario EX-02 rellenado\n- Pasaporte del reagrupante y del familiar\n- Tu TIE (vigente y renovado)\n- Acreditacion de medios economicos\n- Informe de vivienda\n- Certificado de parentesco (libro familia, acta matrimonio)\n- Tasa 790 codigo 052",
      source: "llm",
      delayMs: 1000,
      mustContain: ["EX-02", "052", "Oficina de Extranjeria"],
    },
    {
      userMessage: "¿Cuánto tarda el proceso?",
      claraResponse:
        "El proceso completo tiene varias fases:\n\n1. Resolucion de la autorizacion: plazo legal 3 meses (silencio positivo)\n2. Tu familiar solicita el visado en el consulado espanol de su pais: 1-2 meses\n3. Entrada en Espana y solicitud del TIE: 1 mes\n\nTotal estimado: 5-8 meses\n\nEn la practica, puede alargarse si faltan documentos o si el consulado tiene mucha demanda.\n\nConsejo: prepara todo bien desde el principio para evitar retrasos.",
      source: "llm",
      delayMs: 800,
      mustContain: ["3 meses", "visado", "consulado"],
    },
    {
      userMessage: "Mi mujer puede trabajar cuando llegue?",
      claraResponse:
        "Si! La autorizacion de residencia por reagrupacion familiar permite trabajar.\n\nDesde la reforma del Reglamento de Extranjeria, el familiar reagrupado obtiene autorizacion de residencia Y trabajo simultaneamente.\n\nNo necesita una autorizacion de trabajo separada. Puede buscar empleo y ser contratado/a desde el momento en que tenga el TIE.\n\nEsto aplica para conyuge e hijos en edad laboral.",
      source: "llm",
      delayMs: 700,
      mustContain: ["residencia Y trabajo", "TIE"],
    },
    {
      userMessage: "¿Y mis padres?",
      claraResponse:
        "Reagrupar a los padres (ascendientes) tiene condiciones mas estrictas:\n\n1. Solo si tienes residencia de larga duracion (5 anos o ciudadania UE)\n2. Padres deben ser mayores de 65 anos (excepciones por razones humanitarias)\n3. Debes demostrar que dependen economicamente de ti\n4. Necesidad de que residan contigo justificada\n\nSi no cumples estos requisitos, tus padres podrian solicitar:\n- Visado de visita (90 dias)\n- Arraigo familiar (si tienen nietos espanoles)\n- Residencia no lucrativa (si tienen medios propios)",
      source: "llm",
      delayMs: 900,
      mustContain: ["larga duracion", "65 anos"],
    },
    {
      userMessage: "Entendido, gracias Clara",
      claraResponse:
        "De nada! La reagrupacion familiar es un derecho importante. Te recomiendo preparar toda la documentacion con calma y pedir cita en la Oficina de Extranjeria con tiempo.\n\nSi necesitas ayuda con algun documento especifico, aqui estoy. Mucho animo para reunirte con tu familia!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  9. Nacionalidad espanola (ES, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const nacionalidadES: ConversationScenario = {
  name: "Nacionalidad espanola (ES)",
  language: "es",
  turns: [
    {
      userMessage: "¿Cómo puedo hacerme español?",
      claraResponse:
        "Puedes obtener la nacionalidad espanola por varias vias:\n\n1. Residencia: la mas comun. Requiere residencia legal continuada:\n   - 10 anos (regla general)\n   - 5 anos (refugiados)\n   - 2 anos (nacionales de paises iberoamericanos, Andorra, Filipinas, Guinea Ecuatorial, Portugal, sefardies)\n   - 1 ano (nacidos en Espana, casados con espanol/a, viudos de espanol/a)\n\n2. Carta de naturaleza: por circunstancias excepcionales (concedida por Real Decreto)\n\n3. Por opcion: hijos de espanoles nacidos en el extranjero",
      source: "llm",
      delayMs: 1000,
      mustContain: ["10 anos", "2 anos", "iberoamericanos"],
    },
    {
      userMessage: "Soy colombiano y llevo 3 años en España",
      claraResponse:
        "Como colombiano, te aplica el plazo reducido de 2 anos de residencia legal. Con 3 anos ya cumples el tiempo!\n\nRequisitos adicionales:\n1. Residencia legal y continuada (2 anos minimo)\n2. Buena conducta civica (sin antecedentes penales)\n3. Suficiente grado de integracion: superar el examen CCSE (conocimientos socioculturales) y el DELE A2 (espanol)\n4. No tener antecedentes penales en Espana ni en Colombia\n\nSolicitud: https://sede.mjusticia.gob.es\n\nEl examen CCSE lo organiza el Instituto Cervantes: https://examenes.cervantes.es",
      source: "llm",
      delayMs: 900,
      mustContain: ["2 anos", "CCSE", "DELE A2", "Cervantes"],
    },
    {
      userMessage: "¿Qué es el examen CCSE?",
      claraResponse:
        "El CCSE (Conocimientos Constitucionales y Socioculturales de Espana) es un examen obligatorio para la nacionalidad. Contenido:\n\n- 25 preguntas tipo test\n- 45 minutos\n- Necesitas 15 correctas para aprobar (60%)\n- Temas: Constitucion, organizacion del Estado, cultura, sociedad\n\nCoste: 85 EUR\nDonde: centros del Instituto Cervantes (hay en toda Espana)\n\nMaterial de estudio gratuito en: https://examenes.cervantes.es/es/ccse/preparar\n\nConvocatorias: varias al ano. Consulta fechas en la web del Cervantes.",
      source: "llm",
      delayMs: 800,
      mustContain: ["25 preguntas", "60%", "85 EUR"],
    },
    {
      userMessage: "¿Y si ya hablo español, necesito el DELE?",
      claraResponse:
        "Como colombiano (hispanohablante nativo), estas exento del DELE A2. Solo necesitas el CCSE.\n\nLa exencion del DELE aplica a nacionales de paises donde el espanol es idioma oficial:\n- Todos los paises de Hispanoamerica\n- Guinea Ecuatorial\n\nSi fueras de un pais no hispanohablante, entonces si necesitarias el DELE A2 (coste: ~130 EUR).\n\nAsí que tu solo tienes que aprobar el CCSE. Con estudio de 2-3 semanas normalmente es suficiente.",
      source: "llm",
      delayMs: 700,
      mustContain: ["exento", "DELE", "hispanohablante"],
    },
    {
      userMessage: "¿Cuánto tarda todo el proceso?",
      claraResponse:
        "El proceso de nacionalidad por residencia tarda bastante:\n\n1. Preparacion de documentos: 1-2 meses\n2. Presentacion de la solicitud online\n3. Resolucion: plazo legal 1 ano, pero en la practica tarda 2-3 anos\n4. Juramento/promesa ante el juez: 1-3 meses mas tras la resolucion\n5. Inscripcion en el Registro Civil\n\nTotal real: 2-4 anos desde la solicitud.\n\nPuedes consultar el estado en: https://sede.mjusticia.gob.es/es/tramites/nacionalidad-espanola\n\nTip: el expediente se agiliza si toda la documentacion esta completa desde el inicio.",
      source: "llm",
      delayMs: 900,
      mustContain: ["2-3 anos", "juramento"],
    },
    {
      userMessage: "¿Pierdo la nacionalidad colombiana?",
      claraResponse:
        "No! Colombia permite la doble nacionalidad con Espana. Hay un convenio bilateral.\n\nEspana tambien permite la doble nacionalidad con paises iberoamericanos.\n\nAsí que puedes ser espanol y colombiano al mismo tiempo. No tienes que renunciar a ninguna.\n\nEsto aplica a todos los paises iberoamericanos, Andorra, Filipinas, Guinea Ecuatorial y Portugal.\n\nSi fueras de otro pais (ej: Marruecos, China), tendrias que renunciar a la otra nacionalidad ante notario.",
      source: "llm",
      delayMs: 800,
      mustContain: ["doble nacionalidad", "convenio"],
    },
    {
      userMessage: "¿Cuánto cuesta todo?",
      claraResponse:
        "Los costes aproximados son:\n\n1. Examen CCSE: 85 EUR\n2. DELE A2 (si no eres hispanohablante): ~130 EUR\n3. Certificado de antecedentes penales espanoles: gratuito online\n4. Certificado de antecedentes del pais de origen: varia (Colombia: ~30 EUR en consulado)\n5. Certificado de nacimiento apostillado: varia\n6. Tasa de nacionalidad (Modelo 790-026): ~104 EUR\n\nTotal estimado: 220-350 EUR\n\nNo es un tramite caro. Los mayores costes son el tiempo y la paciencia.",
      source: "llm",
      delayMs: 800,
      mustContain: ["85 EUR", "104 EUR", "790-026"],
    },
    {
      userMessage: "Voy a empezar a preparar los papeles, gracias!",
      claraResponse:
        "Excelente decision! Te deseo mucho exito en el proceso. Recuerda empezar por el CCSE (estudia con el material gratuito del Cervantes) y reune los documentos con tiempo.\n\nSi necesitas ayuda con algun paso especifico, aqui me tienes. Mucha suerte!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  10. Homologacion de titulos (EN, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const homologacionEN: ConversationScenario = {
  name: "Degree recognition (EN)",
  language: "en",
  turns: [
    {
      userMessage: "I have a university degree from my country. Is it valid in Spain?",
      claraResponse:
        "Your foreign degree is not automatically valid in Spain. You need to go through a recognition process called 'homologacion'. There are two paths:\n\n1. Homologacion: Full recognition to the equivalent Spanish degree (for regulated professions like medicine, law, architecture)\n2. Equivalencia: Recognition of your academic level (for non-regulated professions)\n\nThe process is managed by the Ministry of Education:\nhttps://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/gestion-titulos/estudios-universitarios/titulos-extranjeros/homologacion-702.html",
      source: "llm",
      delayMs: 900,
      mustContain: ["homologacion", "Ministry of Education"],
    },
    {
      userMessage: "I'm a nurse. What do I need?",
      claraResponse:
        "Nursing is a regulated profession in Spain, so you need full homologacion. The process:\n\n1. Apply to the Ministry of Education (Ministerio de Educacion)\n2. Documents needed:\n   - Your nursing degree (apostilled and translated)\n   - Academic transcript (apostilled and translated)\n   - Passport/NIE\n   - Application form\n   - Fee: approximately 160 EUR (Tasa 079)\n\n3. The Ministry may require you to pass a specific exam or complete additional training (complementos formativos)\n\nTimeline: 6-12 months (sometimes longer)\n\nAfter homologacion, you also need to register with the Colegio de Enfermeria.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["apostilled", "Colegio de Enfermeria", "160"],
    },
    {
      userMessage: "Where do I get the apostille?",
      claraResponse:
        "The Apostille (Hague Apostille) must be obtained in the country that issued your degree:\n\n- It certifies your documents for international use\n- You get it from the designated authority in your home country (usually the Ministry of Foreign Affairs or equivalent)\n- Each document needs its own apostille\n\nFor countries NOT part of the Hague Convention, you need full legalization through the Spanish consulate in your country.\n\nDocuments that need apostille:\n1. Your degree/diploma\n2. Academic transcript\n3. Birth certificate (if needed)\n\nCost varies by country (usually $10-50 USD per document).",
      source: "llm",
      delayMs: 800,
      mustContain: ["Hague", "Ministry of Foreign Affairs"],
    },
    {
      userMessage: "Do I need to translate everything?",
      claraResponse:
        "Yes, all documents must be translated into Spanish by a sworn translator (traductor jurado).\n\nA sworn translator is officially authorized by the Spanish Ministry of Foreign Affairs. You can find the list at:\nhttps://www.exteriores.gob.es/es/ServiciosAlCiudadano/Paginas/Traductores-Interpretes-Jurados.aspx\n\nCost: approximately 30-80 EUR per page, depending on the translator and language.\n\nTip: If your documents are in Portuguese, you may not need translation (some offices accept Portuguese directly). For French, Italian, it varies.",
      source: "llm",
      delayMs: 800,
      mustContain: ["traductor jurado", "exteriores.gob.es"],
    },
    {
      userMessage: "How long until I can work as a nurse?",
      claraResponse:
        "The timeline for working as a nurse in Spain:\n\n1. Homologacion process: 6-18 months (Ministry of Education)\n2. If additional training required: 3-12 months more\n3. Register with Colegio de Enfermeria: 1-2 weeks\n4. Apply for jobs\n\nTotal: approximately 1-2 years\n\nWhile waiting, you can:\n- Work in non-regulated healthcare roles (auxiliar, cuidador/a)\n- Start the Colegio registration process early\n- Take Spanish language courses if needed\n- Prepare for any required exams\n\nSome hospitals hire nurses with homologacion 'in process' for auxiliary positions.",
      source: "llm",
      delayMs: 900,
      mustContain: ["6-18 months", "Colegio"],
    },
    {
      userMessage: "What if my degree is not recognized?",
      claraResponse:
        "If your homologacion is denied, you have options:\n\n1. Appeal (recurso de alzada): 1 month to file\n2. Complementos formativos: The Ministry may offer conditional recognition if you complete specific courses or exams\n3. Equivalencia de nivel: Even if full homologacion fails, you can get your academic level recognized\n4. Start a shorter Spanish program: Some universities offer 1-2 year bridging programs\n5. Work in non-regulated roles that value your experience\n\nMany denials are due to incomplete documentation, not incompatible qualifications. Check the denial letter carefully.",
      source: "llm",
      delayMs: 800,
      mustContain: ["recurso", "complementos formativos"],
    },
    {
      userMessage: "Is there help for refugees with degrees?",
      claraResponse:
        "Yes! Refugees and asylum seekers have special support:\n\n1. ENIC-NARIC Spain can provide 'credential evaluation' even without original documents\n2. UNESCO Qualifications Passport for Refugees\n3. Organizations like CEAR and ACCEM have specific programs for professional integration\n4. Some universities offer bridging programs specifically for refugees\n5. The European Qualifications Passport for Refugees (EQPR) is recognized in Spain\n\nContact:\n- CEAR: 91 441 55 00\n- Spanish ENIC-NARIC: https://www.educacionyfp.gob.es/educacion/mc/naric/",
      source: "llm",
      delayMs: 900,
      mustContain: ["ENIC-NARIC", "UNESCO", "CEAR"],
    },
    {
      userMessage: "Thank you Clara, this is very helpful!",
      claraResponse:
        "You're welcome! The homologacion process can be long but it's worth it. Start gathering your apostilled and translated documents as soon as possible.\n\nIf you need help with any specific step, I'm here! Good luck with your nursing career in Spain!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  11. Bancos y cuenta bancaria (FR, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const cuentaBancariaFR: ConversationScenario = {
  name: "Ouverture compte bancaire (FR)",
  language: "fr",
  turns: [
    {
      userMessage: "Comment ouvrir un compte en banque en Espagne?",
      claraResponse:
        "Pour ouvrir un compte bancaire en Espagne, tu as besoin de:\n\n1. Passeport ou carte d'identite\n2. NIE (Numero de Identidad de Extranjero)\n3. Certificat d'empadronamiento (pour certaines banques)\n4. Justificatif de revenus (pas toujours obligatoire)\n\nBanques principales:\n- CaixaBank: la plus grande, present partout\n- BBVA: bonne app mobile\n- Santander: reseau international\n- Sabadell, ING, Openbank (en ligne)\n\nSans NIE, certaines banques acceptent seulement le passeport pour un compte basique (cuenta para no residentes).",
      source: "llm",
      delayMs: 900,
      mustContain: ["NIE", "CaixaBank", "BBVA"],
    },
    {
      userMessage: "Je n'ai pas encore le NIE",
      claraResponse:
        "Sans NIE, tu peux quand meme ouvrir un compte de non-resident (cuenta para no residentes). Certaines banques qui l'acceptent:\n\n1. BBVA: accepte le passeport + justificatif de domicile du pays d'origine\n2. CaixaBank: possible avec passeport dans certaines agences\n3. Openbank (en ligne): peut fonctionner avec le passeport seul\n\nLe compte de non-resident a quelques limitations:\n- Pas de domiciliation de salaire parfois\n- Commissions plus elevees\n- Pas de credit\n\nJe te recommande de demander le NIE le plus vite possible pour avoir un compte normal. C'est gratuit et rapide.",
      source: "llm",
      delayMs: 800,
      mustContain: ["non-resident", "passeport"],
    },
    {
      userMessage: "Les comptes sont gratuits?",
      claraResponse:
        "Ca depend de la banque:\n\n- Comptes gratuits (sans conditions): ING, Openbank, EVO Banco, Revolut\n- Comptes gratuits avec conditions: CaixaBank (si domiciliation salaire ou 600 EUR/mois), BBVA (idem), Santander (idem)\n- Comptes avec frais: 3-10 EUR/mois si tu ne remplis pas les conditions\n\nPour eviter les frais, les options en ligne (ING, Openbank) sont les meilleures car elles sont 100% gratuites sans conditions.\n\nAttention aux frais caches: maintenance carte, virements, retraits hors reseau.",
      source: "llm",
      delayMs: 800,
      mustContain: ["ING", "Openbank", "gratuit"],
    },
    {
      userMessage: "Je peux envoyer de l'argent en France facilement?",
      claraResponse:
        "Oui! Les virements entre pays de la zone euro (Espagne-France) sont traites comme des virements nationaux:\n\n- Virements SEPA: gratuits ou tres bon marche (0-1 EUR)\n- Delai: 1 jour ouvrable\n- Tu as juste besoin de l'IBAN du destinataire\n\nPour les virements hors zone euro (Afrique, Asie, etc.):\n- Wise (ex-TransferWise): les meilleurs taux, 0,5-2% de commission\n- Western Union: rapide mais plus cher\n- Banque traditionnelle: souvent 15-30 EUR de frais\n\nJe recommande Wise pour les envois reguliers hors UE.",
      source: "llm",
      delayMs: 800,
      mustContain: ["SEPA", "IBAN"],
    },
    {
      userMessage: "C'est quoi le Bizum?",
      claraResponse:
        "Bizum est le systeme de paiement mobile le plus utilise en Espagne. C'est comme Lydia ou Paylib en France:\n\n- Tu envoies de l'argent instantanement avec juste le numero de telephone\n- Gratuit pour les particuliers\n- Limite: 1.000 EUR par operation, 2.000 EUR par jour\n- Integre dans l'app de ta banque (pas besoin d'app separee)\n\nPreque toutes les banques espagnoles le proposent: CaixaBank, BBVA, Santander, Sabadell, ING...\n\nC'est tres utilise au quotidien (partager addition, payer un ami, achats en ligne). Tout le monde connait Bizum en Espagne!",
      source: "llm",
      delayMs: 700,
      mustContain: ["Bizum", "1.000"],
    },
    {
      userMessage: "Comment je fais pour la declaration d'impots?",
      claraResponse:
        "En Espagne, la declaration d'impots (declaracion de la renta / IRPF) fonctionne ainsi:\n\n- Periode de declaration: avril a juin chaque annee\n- Obligatoire si tu gagnes plus de 22.000 EUR bruts/an (un seul employeur) ou 15.000 EUR (plusieurs employeurs)\n- Se fait en ligne sur: https://sede.agenciatributaria.gob.es\n- Tu as besoin de ton NIE et de Cl@ve ou certificat digital\n\nL'Agencia Tributaria prepare un brouillon (borrador) que tu peux verifier et valider.\n\nPour ta premiere annee, je te recommande d'aller a un gestoria (comptable) qui t'aidera pour 50-100 EUR.",
      source: "llm",
      delayMs: 900,
      mustContain: ["IRPF", "22.000", "agenciatributaria.gob.es"],
    },
    {
      userMessage: "Et si je travaille au noir?",
      claraResponse:
        "Je ne peux pas te conseiller de travailler au noir car c'est illegal et risque. Mais je comprends que parfois la situation est compliquee.\n\nRisques du travail au noir:\n- Amendes pour l'employeur (3.126-10.000 EUR)\n- Tu n'accumules pas de cotisations (pas de chomage, retraite, maladie)\n- Pas de couverture en cas d'accident de travail\n- Peut affecter tes futures demandes de residence\n\nSi tu es dans cette situation, sache que:\n- Tu peux denoncer ton employeur a l'Inspeccion de Trabajo (anonymement)\n- Apres 3 ans en Espagne, tu peux demander l'arraigo social\n- Les syndicats (CCOO, UGT) t'aident gratuitement meme sans papiers",
      source: "llm",
      delayMs: 1000,
      mustContain: ["Inspeccion de Trabajo", "arraigo", "CCOO", "UGT"],
    },
    {
      userMessage: "Merci Clara, c'est tres utile",
      claraResponse:
        "De rien! L'argent et la banque c'est complique quand on arrive dans un nouveau pays. N'hesite pas a me poser d'autres questions.\n\nBon courage pour ton installation en Espagne!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  12. Educacion: escolarizacion de hijos (PT, 8 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const educacionPT: ConversationScenario = {
  name: "Escolarizacao dos filhos (PT)",
  language: "pt",
  turns: [
    {
      userMessage: "Como matriculo os meus filhos na escola em Espanha?",
      claraResponse:
        "Para matricular os teus filhos numa escola em Espanha, precisas de:\n\n1. Certificado de empadronamento (registo municipal)\n2. Passaporte ou documento de identidade da crianca\n3. Cartao de vacinacao\n4. Notas do pais de origem (traduzidas se necessario)\n5. Foto tipo passe\n\nA educacao e obrigatoria dos 6 aos 16 anos e GRATUITA na escola publica.\n\nO periodo de matricula e geralmente em marco-abril. Fora desse periodo, vai diretamente a escola ou ao departamento de educacao do teu municipio.",
      source: "llm",
      delayMs: 900,
      mustContain: ["empadronamento", "6 aos 16", "GRATUITA"],
    },
    {
      userMessage: "E se nao tenho papeis?",
      claraResponse:
        "Mesmo sem documentacao regular, os teus filhos TEM DIREITO a educacao em Espanha. Isto esta garantido pela Constituicao e pela LO 2/2006 (Lei de Educacao).\n\nNao importa a situacao administrativa dos pais:\n- Todas as criancas entre 6-16 anos devem ser escolarizadas\n- A escola NAO pode pedir NIE nem permiso de residencia\n- O empadronamento e suficiente\n- Se nao tens empadronamento, os servicos sociais ajudam\n\nNenhum funcionario da escola pode denunciar a tua situacao migratoria. E confidencial.",
      source: "llm",
      delayMs: 900,
      mustContain: ["Constituicao", "LO 2/2006", "confidencial"],
    },
    {
      userMessage: "Ha ajudas para material escolar?",
      claraResponse:
        "Sim! Ha varias ajudas para familias com poucos recursos:\n\n1. Bolsas de livros e material: cada comunidade autonoma tem as suas\n2. Bolsa de cantina (comedor escolar): alimentacao gratuita ou a preco reduzido\n3. Bolsa de transporte escolar: se a escola e longe\n4. Programa de reutilizacao de livros: livros gratuitos emprestados pela escola\n5. Ajudas de emergencia dos servicos sociais\n\nPede informacao na secretaria da escola ou nos servicos sociais do teu municipio.\n\nPrazo: geralmente junho-setembro para o ano seguinte.",
      source: "llm",
      delayMs: 800,
      mustContain: ["bolsa", "cantina", "servicos sociais"],
    },
    {
      userMessage: "O meu filho nao fala espanhol",
      claraResponse:
        "Nao te preocupes! As escolas espanholas tem programas especificos para alunos que nao falam espanhol:\n\n1. Aulas de acogida / Aulas de enlace: classes intensivas de espanhol (3-9 meses)\n2. Apoio linguistico dentro da aula regular\n3. Adaptacoes curriculares temporarias\n4. Mediadores interculturais em muitas escolas\n\nO portugues e o espanhol sao linguas proximas, por isso a adaptacao e geralmente rapida (3-6 meses).\n\nAs criancas aprendem muito mais rapido do que os adultos. Em poucos meses, o teu filho vai estar a falar espanhol com os colegas.",
      source: "llm",
      delayMs: 800,
      mustContain: ["aulas de acogida", "linguistico"],
    },
    {
      userMessage: "Posso escolher a escola?",
      claraResponse:
        "Sim, podes indicar preferencias, mas a atribuicao depende de criterios:\n\n1. Proximidade do domicilio (maior pontuacao)\n2. Irmaos ja matriculados na escola\n3. Renda familiar baixa\n4. Familia numerosa\n5. Deficiencia de algum membro da familia\n\nSe nao consegues vaga na escola preferida, atribuem uma escola com vagas disponiveis.\n\nTipos de escola:\n- Publica (colegio publico): gratuita\n- Concertada (privada subvencionada): parcialmente gratuita\n- Privada: paga (400-1000 EUR/mes)\n\nRecomendo a escola publica, especialmente ao inicio.",
      source: "llm",
      delayMs: 800,
      mustContain: ["proximidade", "concertada"],
    },
    {
      userMessage: "E a universidade? Ha bolsas?",
      claraResponse:
        "Sim! Para a universidade em Espanha:\n\n1. Bolsas do Ministerio de Educacao (becas MEC): cobrem matricula + ajuda de manutencao\n   - Requisitos: renda familiar baixa, boas notas\n   - Solicitar em: https://www.becaseducacion.gob.es\n\n2. Bolsas da comunidade autonoma\n3. Bolsas da propria universidade\n4. Erasmus Mundus (para programas internacionais)\n\nAs matriculas na universidade publica custam 800-1.500 EUR/ano (muito mais barato que noutros paises).\n\nCom beca MEC, pode ser quase gratuito.",
      source: "llm",
      delayMs: 900,
      mustContain: ["becas MEC", "becaseducacion.gob.es"],
    },
    {
      userMessage: "Preciso de homologar os estudos do meu filho?",
      claraResponse:
        "Depende do nivel:\n\n- Educacao basica (ate 4o ESO / 16 anos): NAO precisa homologacao. Basta apresentar as notas traduzidas e a escola faz a equivalencia.\n- Bachillerato (16-18 anos): pode precisar de homologacao pelo Ministerio de Educacao\n- Universidade: precisa de homologacao ou credencial de acesso\n\nPara estudos portugueses, o processo e mais simples gracas aos acordos UE.\n\nSolicita a homologacao em: https://www.educacionyfp.gob.es\n\nDica: comecar o processo ANTES de chegar a Espanha para evitar atrasos.",
      source: "llm",
      delayMs: 800,
      mustContain: ["ESO", "Bachillerato"],
    },
    {
      userMessage: "Obrigado Clara!",
      claraResponse:
        "De nada! A educacao dos teus filhos e uma prioridade e Espanha garante esse direito para todas as criancas. Nao hesites em pedir ajuda na escola ou nos servicos sociais.\n\nBoa sorte para a familia! Estou aqui se precisares de mais alguma coisa.",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  13. Tramites de salud mental (ES, 6 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const saludMentalES: ConversationScenario = {
  name: "Salud mental recursos (ES)",
  language: "es",
  turns: [
    {
      userMessage: "No me encuentro bien emocionalmente, ¿hay ayuda psicológica gratis?",
      claraResponse:
        "Si, en Espana la atencion psicologica esta incluida en la sanidad publica. Para acceder:\n\n1. Ve a tu medico de cabecera (centro de salud)\n2. El medico te puede derivar a Salud Mental (psicologo/psiquiatra)\n3. La atencion es gratuita con tarjeta sanitaria\n\nAdemas, existen recursos de atencion inmediata:\n- Telefono de la Esperanza: 717 003 717 (24h)\n- Linea de Atencion a la Conducta Suicida: 024 (24h)\n- Crisis: llama al 112\n\nNo estas solo/a. Pedir ayuda es un acto de valentia.",
      source: "llm",
      delayMs: 900,
      mustContain: ["717 003 717", "024", "medico de cabecera"],
    },
    {
      userMessage: "Pero las listas de espera son muy largas",
      claraResponse:
        "Tienes razon, las listas de espera en salud mental publica pueden ser largas (2-6 meses en muchas zonas). Alternativas mientras esperas:\n\n1. ONGs con atencion psicologica gratuita:\n   - Telefono de la Esperanza: tambien ofrecen consultas presenciales\n   - Cruz Roja: programas de apoyo emocional\n   - Caritas: servicio de escucha y orientacion\n\n2. Universidades: clinicas universitarias con precios reducidos (15-30 EUR/sesion)\n\n3. Colegios de Psicologos: algunos tienen servicio de bajo coste\n\n4. Apps: Serenmind (del SNS), ejercicios guiados gratuitos\n\nSi es urgente (ideas suicidas, crisis), ve a urgencias directamente. Alli te atienden inmediatamente.",
      source: "llm",
      delayMs: 1000,
      mustContain: ["Telefono de la Esperanza", "Cruz Roja", "urgencias"],
    },
    {
      userMessage: "Soy inmigrante sin papeles, ¿me atienden?",
      claraResponse:
        "Si! La atencion en salud mental es un derecho para todas las personas en Espana, independientemente de tu situacion administrativa:\n\n1. Con tarjeta sanitaria: acceso completo\n2. Sin tarjeta: tienes derecho a urgencias y atencion basica\n3. Muchas comunidades dan tarjeta sanitaria a todos los empadronados, con o sin papeles\n\nAdemas:\n- Las lineas telefonicas (024, 717) son anonimas, no piden papeles\n- Las ONGs atienden sin preguntar documentacion\n- Los servicios sociales pueden derivarte a recursos especializados\n\nTu salud mental es prioritaria. No dejes de pedir ayuda por miedo a tu situacion.",
      source: "llm",
      delayMs: 900,
      mustContain: ["024", "anonimas", "empadronados"],
    },
    {
      userMessage: "¿Hay psicólogos que hablen mi idioma?",
      claraResponse:
        "Depende de tu idioma y tu ciudad, pero hay opciones:\n\n1. Servicios de mediacion intercultural: los ayuntamientos grandes tienen mediadores que acompanan en consultas medicas\n2. ONGs con equipos multilingues: CEAR, ACCEM, Cruz Roja (especialmente para refugiados)\n3. Psicologos privados bilingues: busca en el Colegio de Psicologos de tu provincia\n4. Atencion online: plataformas como Psicologos sin Fronteras\n\nEn Madrid y Barcelona hay mas opciones multilingues. En ciudades pequeñas, la mediacion intercultural es clave.\n\nPregunta en los servicios sociales de tu ayuntamiento, ellos conocen los recursos locales.",
      source: "llm",
      delayMs: 900,
      mustContain: ["mediacion intercultural", "CEAR"],
    },
    {
      userMessage: "Me da vergüenza ir al psicólogo",
      claraResponse:
        "Es completamente normal sentir eso. Muchas personas sienten verguenza al principio, especialmente si en tu cultura no se habla de salud mental abiertamente.\n\nAlgunas cosas que ayudan:\n\n1. Todo lo que digas es confidencial. El psicologo tiene secreto profesional\n2. No te van a juzgar. Estan formados para escuchar sin juicio\n3. Puedes empezar por telefono: llama al 717 003 717, es anonimo\n4. No tienes que contarlo todo en la primera cita\n5. Cuidar tu salud mental es tan importante como cuidar un dolor de espalda\n\nDar el primer paso es lo mas dificil. Despues cada vez es mas facil.",
      source: "llm",
      delayMs: 800,
      mustContain: ["confidencial", "secreto profesional", "717 003 717"],
    },
    {
      userMessage: "Gracias Clara, creo que voy a llamar",
      claraResponse:
        "Me alegra muchisimo oir eso. Es un paso muy importante y valiente.\n\nRecuerda: 717 003 717 (Telefono de la Esperanza, 24h) o 024 (Linea de Atencion a la Conducta Suicida, 24h).\n\nEstoy aqui siempre que me necesites. Cuidate mucho.",
      source: "llm",
      delayMs: 400,
      mustContain: ["717 003 717", "024"],
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  14. Permiso de conducir extranjero (ES, 6 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const permisoConducirES: ConversationScenario = {
  name: "Canje permiso conducir (ES)",
  language: "es",
  turns: [
    {
      userMessage: "¿Puedo conducir en España con mi carnet de mi país?",
      claraResponse:
        "Depende de tu situacion:\n\n1. Turista (menos de 6 meses): puedes conducir con tu permiso extranjero + Permiso Internacional de Conducir\n2. Residente: tienes 6 meses desde que obtienes la residencia para canjear tu permiso\n\nPaises con convenio de canje (no necesitan examen): la mayoria de paises de la UE, Suiza, algunos paises de Latinoamerica, Marruecos, Turquia, etc.\n\nPaises sin convenio: necesitas sacarte el carnet espanol desde cero (examen teorico + practico).\n\nConsulta la lista en: https://sede.dgt.gob.es/es/permisos-de-conducir/canje-permisos/",
      source: "llm",
      delayMs: 900,
      mustContain: ["6 meses", "canje", "sede.dgt.gob.es"],
    },
    {
      userMessage: "Soy de Colombia, ¿puedo canjear?",
      claraResponse:
        "Si! Colombia tiene convenio de canje con Espana. Puedes canjear tu licencia colombiana sin hacer examenes.\n\nProceso:\n1. Pide cita en la DGT: https://sede.dgt.gob.es/es/permisos-de-conducir/canje-permisos/\n2. Documentos:\n   - Tu licencia colombiana original y vigente\n   - Pasaporte y NIE\n   - Foto 32x26mm\n   - Tasa de canje: aprox. 28,30 EUR\n   - Reconocimiento medico (psicotecnico): 20-35 EUR en un centro autorizado\n\nPlazo: unas 2-4 semanas tras la cita.\n\nImportante: la licencia colombiana te la retiran y la envian al consulado colombiano.",
      source: "llm",
      delayMs: 800,
      mustContain: ["convenio", "28,30", "psicotecnico"],
    },
    {
      userMessage: "¿Dónde hago el reconocimiento médico?",
      claraResponse:
        "El reconocimiento medico (psicotecnico) para conducir se hace en Centros de Reconocimiento de Conductores autorizados por la DGT:\n\n- Hay en todas las ciudades, son clinicas privadas\n- Coste: 20-35 EUR (dependiendo del centro)\n- Duracion: 15-20 minutos\n- Incluye: vista, oido, reflejos, coordinacion, test psicologico basico\n\nPuedes buscar centros cercanos en:\nhttps://sede.dgt.gob.es/es/otros-tramites/centros-reconocimiento/\n\nNo necesitas cita previa en la mayoria. Lleva tu pasaporte/NIE.",
      source: "llm",
      delayMs: 700,
      mustContain: ["Centros de Reconocimiento", "20-35"],
    },
    {
      userMessage: "¿Y si mi permiso está caducado?",
      claraResponse:
        "Si tu permiso colombiano esta caducado, el canje es mas complicado:\n\n1. Si caduco hace menos de 5 anos: algunas jefaturas de la DGT aceptan el canje si presentas documentacion adicional (certificado de la autoridad colombiana)\n2. Si caduco hace mas de 5 anos: generalmente no aceptan el canje\n\nEn caso de que no acepten:\n- Tendras que sacarte el permiso espanol desde cero\n- Examen teorico: 30 preguntas test (maximo 3 errores)\n- Examen practico: conduccion en ciudad\n- Coste total: 200-600 EUR (autoescuela + tasas)\n\nConsulta tu caso especifico en la Jefatura Provincial de Trafico de tu provincia.",
      source: "llm",
      delayMs: 900,
      mustContain: ["5 anos", "30 preguntas", "autoescuela"],
    },
    {
      userMessage: "¿Hay autoescuelas baratas?",
      claraResponse:
        "Los precios de autoescuelas varian mucho:\n\n- Pack basico (teorico + practicas minimas): 300-500 EUR\n- Clases practicas sueltas: 25-40 EUR/hora\n- Solo examen teorico (si estudias por tu cuenta): tasa DGT ~94 EUR\n\nConsejos para ahorrar:\n1. Estudia la teoria por tu cuenta con apps gratuitas (DGT, Todotest, Practicatest)\n2. Compara precios entre autoescuelas\n3. Algunas autoescuelas online son mas baratas (Onroad, Drivesmart)\n4. Pregunta en servicios sociales: algunas comunidades subvencionan el permiso para desempleados\n\nEl permiso de conducir puede ser clave para encontrar trabajo, asi que vale la inversion.",
      source: "llm",
      delayMs: 800,
      mustContain: ["94 EUR", "DGT"],
    },
    {
      userMessage: "Gracias Clara!",
      claraResponse:
        "De nada! El permiso de conducir es un tramite importante para la vida diaria en Espana. Si eres colombiano, el canje es la via mas facil y rapida.\n\nPide tu cita en la DGT cuanto antes. Estoy aqui si necesitas mas ayuda!",
      source: "llm",
      delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  15. Cross-topic conversation: mixed queries (ES, 10 turns)
 * ══════════════════════════════════════════════════════════════════ */
export const mixedTopicsES: ConversationScenario = {
  name: "Mixed topics conversation (ES)",
  language: "es",
  turns: [
    {
      userMessage: "Acabo de llegar a España, ¿por dónde empiezo?",
      claraResponse: "Lo primero al llegar a Espana es el empadronamiento (registrarte en tu ayuntamiento). Es gratis, rapido, y es la llave que abre todas las demas puertas: tarjeta sanitaria, escuela para tus hijos, ayudas sociales.\n\nLleva tu pasaporte y un justificante de tu direccion (contrato de alquiler o declaracion del propietario) al ayuntamiento de tu ciudad.",
      source: "llm", delayMs: 700,
      mustContain: ["empadronamiento", "ayuntamiento"],
    },
    {
      userMessage: "Ya me empadroné, ¿ahora qué?",
      claraResponse: "Muy bien! Ahora los siguientes pasos son:\n\n1. Tarjeta sanitaria: ve a tu centro de salud con el empadronamiento y pasaporte\n2. NIE: si aun no lo tienes, pidelo cuanto antes\n3. Si tienes hijos: inscribirlos en la escuela\n4. Cuenta bancaria: necesitaras un IBAN para cobrar y hacer tramites\n5. Si necesitas ayuda economica: pide cita en servicios sociales\n\nCada paso depende del anterior, asi que ve en este orden.",
      source: "llm", delayMs: 800,
      mustContain: ["tarjeta sanitaria", "NIE"],
    },
    {
      userMessage: "¿Puedo ir al médico ya?",
      claraResponse: "Si! Con tu certificado de empadronamiento, puedes ir al centro de salud mas cercano y pedir que te asignen un medico de cabecera. Te daran la tarjeta sanitaria provisional en el acto.\n\nSi es urgente, puedes ir directamente a urgencias del hospital sin tarjeta. Te atenderan igualmente.",
      source: "llm", delayMs: 600,
      mustContain: ["centro de salud", "urgencias"],
    },
    {
      userMessage: "Necesito trabajar urgente",
      claraResponse: "Para trabajar legalmente en Espana necesitas:\n\n1. NIE con autorizacion de trabajo\n2. Numero de afiliacion a la Seguridad Social (tu empleador lo tramita)\n\nMientras tanto, puedes:\n- Inscribirte en el SEPE como demandante de empleo: https://sede.sepe.gob.es\n- Ir a los servicios de empleo de tu comunidad (SOC, SAE, Lanbide, etc.)\n- ONGs que ayudan con empleo: Cruz Roja, ACCEM, CEAR\n\nSi no tienes permiso de trabajo, los servicios sociales pueden orientarte sobre tus opciones.",
      source: "llm", delayMs: 800,
      mustContain: ["SEPE", "Seguridad Social"],
    },
    {
      userMessage: "No tengo dinero para comer",
      claraResponse: "Si necesitas ayuda alimentaria urgente, hay recursos:\n\n1. Bancos de alimentos: reparten comida gratuitamente\n2. Cruz Roja: programa de distribucion de alimentos\n3. Caritas: comedores sociales y cestas de alimentos\n4. Servicios sociales del ayuntamiento: tarjetas de ayuda para supermercados\n\nContacta con servicios sociales de tu ayuntamiento para que valoren tu situacion y te deriven al recurso mas adecuado.\n\nTambien: muchas parroquias y mezquitas reparten alimentos sin requisitos.",
      source: "llm", delayMs: 800,
      mustContain: ["Bancos de alimentos", "Cruz Roja", "Caritas"],
    },
    {
      userMessage: "¿Hay wifi gratis? No tengo internet",
      claraResponse: "Si! Puedes acceder a internet gratis en:\n\n1. Bibliotecas publicas: wifi gratis + ordenadores. Busca la mas cercana en la web de tu ayuntamiento\n2. Centros civicos y culturales: muchos tienen wifi abierto\n3. Zonas wifi municipales: muchas plazas y parques tienen wifi del ayuntamiento\n4. Centros de Cruz Roja y Caritas: wifi disponible\n5. Cafeterias y centros comerciales\n\nPara contratar internet barato en casa: Digi, Lowi, O2 ofrecen planes desde 5-10 EUR/mes para movil.",
      source: "llm", delayMs: 700,
      mustContain: ["Bibliotecas", "wifi"],
    },
    {
      userMessage: "Necesito aprender español",
      claraResponse: "Hay muchas opciones gratuitas para aprender espanol:\n\n1. Escuelas Oficiales de Idiomas (EOI): cursos gratuitos o muy baratos, con certificacion oficial\n2. CEPI (Centro de Participacion e Integracion): cursos gratuitos para inmigrantes\n3. Cruz Roja: clases de espanol gratuitas\n4. Caritas: talleres de idioma\n5. Asociaciones de vecinos y ONGs locales\n6. Online gratuito: SpanishPod101, Duolingo, Busuu\n\nLa EOI es la mejor opcion porque el titulo tiene valor oficial.\n\nPregunta en tu ayuntamiento por cursos de espanol para inmigrantes.",
      source: "llm", delayMs: 800,
      mustContain: ["Escuelas Oficiales de Idiomas", "CEPI"],
    },
    {
      userMessage: "¿Me pueden deportar?",
      claraResponse: "Depende de tu situacion:\n\n1. Si tienes residencia legal: NO, a menos que cometas un delito grave\n2. Si eres solicitante de asilo: NO, proteccion de no devolucion\n3. Si estas en situacion irregular: existe el riesgo, pero en la practica:\n   - La policia no busca activamente a irregulares\n   - Si te identifican, pueden iniciar expediente de expulsion\n   - Tienes derecho a abogado y a recurrir\n   - Con arraigo (3 anos) puedes regularizarte\n\nSi tienes miedo, contacta con un abogado (turno de oficio gratuito) o con CEAR/ACCEM.",
      source: "llm", delayMs: 1000,
      mustContain: ["arraigo", "abogado"],
    },
    {
      userMessage: "¿Cómo consigo el arraigo?",
      claraResponse: "Hay varios tipos de arraigo:\n\n1. Arraigo social (el mas comun):\n   - 3 anos de permanencia continuada en Espana\n   - Sin antecedentes penales\n   - Contrato de trabajo de 1 ano O informe de integracion social\n\n2. Arraigo laboral:\n   - 2 anos en Espana + relacion laboral de al menos 6 meses (aunque sea sin contrato)\n\n3. Arraigo familiar:\n   - Padre/madre de menor espanol\n   - Hijo de padre/madre espanol\n\nSolicitud: Oficina de Extranjeria de tu provincia.\nCoste: tasa 790 codigo 052 (aprox. 38 EUR).",
      source: "llm", delayMs: 1000,
      mustContain: ["3 anos", "arraigo social", "arraigo laboral", "arraigo familiar"],
    },
    {
      userMessage: "Muchísimas gracias Clara, me siento mucho mejor",
      claraResponse: "Me alegro mucho! Llegar a un pais nuevo puede ser abrumador, pero hay muchos recursos disponibles. El primer paso siempre es servicios sociales del ayuntamiento.\n\nRecuerda que estoy aqui las 24 horas para lo que necesites. Un gran abrazo y mucho animo!",
      source: "llm", delayMs: 400,
    },
  ],
};

/* ══════════════════════════════════════════════════════════════════
 *  Export everything
 * ══════════════════════════════════════════════════════════════════ */
export const COMPREHENSIVE_SCENARIOS: ConversationScenario[] = [
  nieTieES,
  asiloES,
  asistenciaJuridicaES,
  viviendaES,
  desempleoES,
  discapacidadES,
  violenciaGeneroES,
  reagrupacionES,
  nacionalidadES,
  homologacionEN,
  cuentaBancariaFR,
  educacionPT,
  saludMentalES,
  permisoConducirES,
  mixedTopicsES,
];
