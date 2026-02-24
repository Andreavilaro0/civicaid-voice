"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import {
  sendMessage,
  generateSessionId,
  generateTTS,
  resolveAudioUrl,
  getErrorMessage,
  ApiError,
} from "@/lib/api";
import { API_BASE_URL } from "@/lib/constants";
import type {
  Message,
  Language,
  ChatResponse,
  LoadingContext,
  ApiInputType,
  AudioPlayback,
  ErrorAction,
} from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Helpers internos                                                   */
/* ------------------------------------------------------------------ */

function createId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

/* ------------------------------------------------------------------ */
/*  Mensajes de bienvenida                                            */
/* ------------------------------------------------------------------ */

const LEGAL_PAGE = "https://andreavilaro0.github.io/civicaid-voice/info-legal";

const welcomeMessages: Record<Language, string> = {
  es: `Hola, soy Clara!\n\nSoy una inteligencia artificial, no una persona. Mi información es orientativa y no sustituye asesoramiento profesional.\n\nTe ayudo con más de 20 trámites sociales en España: IMV, empadronamiento, tarjeta sanitaria, NIE, pensiones, bono social eléctrico, reagrupación familiar, arraigo, becas, prestaciones por nacimiento y más.\n\nPuedes hablarme con audio o escribir tu pregunta.\nHablo español, francés, inglés, portugués, rumano, catalán, chino y árabe.\nGratis y confidencial.\n\nInfo legal: ${LEGAL_PAGE}?lang=es`,
  en: `Hi, I'm Clara!\n\nI am an artificial intelligence, not a person. My information is for guidance only and does not replace professional advice.\n\nI help you with over 20 social services in Spain: minimum income, registration, health card, NIE, pensions, electricity social bonus, family reunification, residency, scholarships, parental leave and more.\n\nYou can send me a voice message or type your question.\nI speak Spanish, French, English, Portuguese, Romanian, Catalan, Chinese and Arabic.\nFree and confidential.\n\nLegal info: ${LEGAL_PAGE}?lang=en`,
  fr: `Salut, je suis Clara!\n\nJe suis une intelligence artificielle, pas une personne. Mes informations sont indicatives et ne remplacent pas un conseil professionnel.\n\nJe t'aide avec plus de 20 démarches sociales en Espagne: RMV, inscription, carte sanitaire, NIE, pensions, bon social électrique, regroupement familial, enracinement, bourses, congé parental et plus.\n\nTu peux m'envoyer un audio ou écrire ta question.\nJe parle espagnol, français, anglais, portugais, roumain, catalan, chinois et arabe.\nGratuit et confidentiel.\n\nInfos légales: ${LEGAL_PAGE}?lang=fr`,
  pt: `Olá, sou a Clara!\n\nSou uma inteligência artificial, não uma pessoa. A minha informação é orientativa e não substitui aconselhamento profissional.\n\nAjudo-te com mais de 20 trâmites sociais em Espanha: rendimento mínimo, inscrição, cartão de saúde, NIE, pensões, bónus social elétrico, reagrupamento familiar, arraigo, bolsas, licença parental e mais.\n\nPodes enviar-me um áudio ou escrever a tua pergunta.\nFalo espanhol, francês, inglês, português, romeno, catalão, chinês e árabe.\nGratuito e confidencial.\n\nInfo legal: ${LEGAL_PAGE}?lang=pt`,
  ro: `Bună, sunt Clara!\n\nSunt o inteligență artificială, nu o persoană. Informațiile mele sunt orientative și nu înlocuiesc consilierea profesională.\n\nTe ajut cu peste 20 de proceduri sociale din Spania: venitul minim, înregistrarea, cardul de sănătate, NIE, pensii, bonusul social electric, reîntregirea familiei, arraigo, burse, concediu parental și altele.\n\nPoți să trimiți un mesaj vocal sau să scrii întrebarea ta.\nVorbesc spaniolă, franceză, engleză, portugheză, română, catalană, chineză și arabă.\nGratuit și confidențial.\n\nInfo legale: ${LEGAL_PAGE}?lang=ro`,
  ca: `Hola, soc la Clara!\n\nSoc una intel·ligència artificial, no una persona. La meva informació és orientativa i no substitueix l'assessorament professional.\n\nT'ajudo amb més de 20 tràmits socials a Espanya: IMV, empadronament, targeta sanitària, NIE, pensions, bo social elèctric, reagrupament familiar, arrelament, beques, baixa per naixement i més.\n\nPots enviar-me un àudio o escriure la teva pregunta.\nParlo castellà, francès, anglès, portuguès, romanès, català, xinès i àrab.\nGratuït i confidencial.\n\nInfo legal: ${LEGAL_PAGE}?lang=ca`,
  zh: `你好，我是Clara!\n\n我是人工智能，不是真人。我提供的信息仅供参考，不能替代专业建议。\n\n我帮助你办理西班牙20多项社会事务：最低收入、登记注册、医疗卡、NIE、养老金、电力社会补贴、家庭团聚、扎根居留、奖学金、产假等。\n\n你可以发送语音或输入文字提问。\n我会说西班牙语、法语、英语、葡萄牙语、罗马尼亚语、加泰罗尼亚语、中文和阿拉伯语。\n免费且保密。\n\n法律信息: ${LEGAL_PAGE}?lang=zh`,
  ar: `مرحبا، أنا كلارا!\n\nأنا ذكاء اصطناعي، لست شخصاً حقيقياً. معلوماتي إرشادية ولا تحل محل الاستشارة المهنية.\n\nأساعدك في أكثر من 20 إجراء اجتماعي في إسبانيا: الحد الأدنى للدخل، التسجيل البلدي، البطاقة الصحية، NIE، المعاشات، المكافأة الاجتماعية للكهرباء، لم شمل الأسرة، الإقامة، المنح، إجازة الولادة والمزيد.\n\nيمكنك إرسال صوت أو كتابة سؤالك.\nأتحدث الإسبانية والفرنسية والإنجليزية والبرتغالية والرومانية والكتالونية والصينية والعربية.\nمجاني وسري.\n\nالمعلومات القانونية: ${LEGAL_PAGE}?lang=ar`,
};

/* ------------------------------------------------------------------ */
/*  Loading messages por contexto                                      */
/* ------------------------------------------------------------------ */

const loadingMessages: Record<Language, Record<LoadingContext, string>> = {
  es: {
    listening: "Te escucho. Dame un momento.",
    thinking: "Buena pregunta. Dame un momento que busco la información.",
    reading: "Voy a mirar tu documento. Dame un segundo.",
  },
  en: {
    listening: "I hear you. Give me a moment.",
    thinking: "Good question. Give me a moment to look into this.",
    reading: "Let me look at your document. One second.",
  },
  fr: {
    listening: "Je vous écoute. Un instant.",
    thinking: "Bonne question. Un instant, je cherche l'information.",
    reading: "Je regarde votre document. Un instant.",
  },
  pt: {
    listening: "Estou a ouvir-te. Dá-me um momento.",
    thinking: "Boa pergunta. Dá-me um momento que procuro a informação.",
    reading: "Vou ver o teu documento. Dá-me um segundo.",
  },
  ro: {
    listening: "Te aud. Dă-mi un moment.",
    thinking: "Întrebare bună. Dă-mi un moment să caut informația.",
    reading: "Mă uit la documentul tău. O secundă.",
  },
  ca: {
    listening: "T'escolto. Dona'm un moment.",
    thinking: "Bona pregunta. Dona'm un moment que busco la informació.",
    reading: "Vaig a mirar el teu document. Dona'm un segon.",
  },
  zh: {
    listening: "我听到了。请等一下。",
    thinking: "好问题。请等一下，我查找一下信息。",
    reading: "让我看看你的文件。请等一下。",
  },
  ar: {
    listening: "\u0623\u0633\u0645\u0639\u0643. \u0644\u062D\u0638\u0629 \u0645\u0646 \u0641\u0636\u0644\u0643.",
    thinking: "\u0633\u0624\u0627\u0644 \u062C\u064A\u062F. \u0644\u062D\u0638\u0629\u060C \u0623\u0628\u062D\u062B \u0639\u0646 \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062A.",
    reading: "\u0633\u0623\u0646\u0638\u0631 \u0641\u064A \u0648\u062B\u064A\u0642\u062A\u0643. \u0644\u062D\u0638\u0629 \u0645\u0646 \u0641\u0636\u0644\u0643.",
  },
};

/* ------------------------------------------------------------------ */
/*  Follow-up & goodbye messages                                       */
/* ------------------------------------------------------------------ */

const FOLLOWUP_DELAY_MS = 5 * 60 * 1000; // 5 minutes
const GOODBYE_DELAY_MS = 3 * 60 * 1000;  // 3 minutes after follow-up

const FOLLOWUP_MESSAGES: Record<Language, string> = {
  es: "¿Sigues ahí? Si necesitas algo más, estoy aquí para ayudarte.",
  en: "Are you still there? If you need anything else, I'm here to help.",
  fr: "Tu es encore là? Si tu as besoin d'autre chose, je suis là pour t'aider.",
  pt: "Ainda estás aí? Se precisas de mais alguma coisa, estou aqui para ajudar.",
  ro: "Mai ești acolo? Dacă ai nevoie de altceva, sunt aici să te ajut.",
  ca: "Encara hi ets? Si necessites alguna cosa més, soc aquí per ajudar-te.",
  zh: "你还在吗？如果还需要帮助，我在这里。",
  ar: "هل لا تزال هنا؟ إذا كنت بحاجة إلى شيء آخر، أنا هنا لمساعدتك.",
};

const FOLLOWUP_SPEECH: Record<Language, string> = {
  es: "¿Sigues ahí? Si necesitas algo más, estoy aquí para ayudarte.",
  en: "Are you still there? If you need anything else, I'm here to help.",
  fr: "Tu es encore là? Si tu as besoin d'autre chose, je suis là.",
  pt: "Ainda estás aí? Se precisas de mais alguma coisa, estou aqui.",
  ro: "Mai ești acolo? Dacă ai nevoie de altceva, sunt aici.",
  ca: "Encara hi ets? Si necessites alguna cosa més, soc aquí.",
  zh: "你还在吗？如果还需要帮助，我在这里。",
  ar: "هل لا تزال هنا؟ أنا هنا لمساعدتك.",
};

const GOODBYE_MESSAGES: Record<Language, string> = {
  es: `Parece que ya no estás. No guardamos ningún dato tuyo, tu privacidad es lo primero. Si vuelves a necesitar ayuda, aquí me tienes. ¡Cuídate mucho!\n\nInfo legal y privacidad: ${LEGAL_PAGE}?lang=es`,
  en: `It seems you've left. We don't store any of your data — your privacy comes first. If you need help again, I'll be here. Take care!\n\nLegal info & privacy: ${LEGAL_PAGE}?lang=en`,
  fr: `Il semble que tu sois parti. Nous ne conservons aucune de tes données, ta vie privée est notre priorité. Si tu as encore besoin d'aide, je suis là. Prends soin de toi!\n\nInfos légales et confidentialité: ${LEGAL_PAGE}?lang=fr`,
  pt: `Parece que já foste. Não guardamos nenhum dado teu, a tua privacidade é o mais importante. Se voltares a precisar de ajuda, estou aqui. Cuida-te!\n\nInfo legal e privacidade: ${LEGAL_PAGE}?lang=pt`,
  ro: `Se pare că ai plecat. Nu stocăm niciun fel de date ale tale, confidențialitatea ta este prioritară. Dacă ai nevoie de ajutor din nou, sunt aici. Ai grijă de tine!\n\nInfo legale și confidențialitate: ${LEGAL_PAGE}?lang=ro`,
  ca: `Sembla que ja no hi ets. No guardem cap dada teva, la teva privacitat és el primer. Si tornes a necessitar ajuda, aquí em tens. Cuida't molt!\n\nInfo legal i privacitat: ${LEGAL_PAGE}?lang=ca`,
  zh: `看起来你已经离开了。我们不保存你的任何数据，你的隐私是第一位的。如果你再次需要帮助，我在这里。保重！\n\n法律信息与隐私: ${LEGAL_PAGE}?lang=zh`,
  ar: `يبدو أنك غادرت. لا نحتفظ بأي من بياناتك، خصوصيتك هي الأولوية. إذا احتجت المساعدة مرة أخرى، أنا هنا. اعتنِ بنفسك!\n\nالمعلومات القانونية والخصوصية: ${LEGAL_PAGE}?lang=ar`,
};

const GOODBYE_SPEECH: Record<Language, string> = {
  es: "Parece que ya no estás. No guardamos ningún dato tuyo. Si vuelves a necesitar ayuda, aquí me tienes. Cuídate mucho.",
  en: "It seems you've left. We don't store any of your data. If you need help again, I'll be here. Take care.",
  fr: "Il semble que tu sois parti. Nous ne conservons aucune de tes données. Si tu as encore besoin d'aide, je suis là. Prends soin de toi.",
  pt: "Parece que já foste. Não guardamos nenhum dado teu. Se voltares a precisar de ajuda, estou aqui. Cuida-te.",
  ro: "Se pare că ai plecat. Nu stocăm niciun fel de date ale tale. Dacă ai nevoie de ajutor din nou, sunt aici. Ai grijă de tine.",
  ca: "Sembla que ja no hi ets. No guardem cap dada teva. Si tornes a necessitar ajuda, aquí em tens. Cuida't molt.",
  zh: "看起来你已经离开了。我们不保存你的任何数据。如果你再次需要帮助，我在这里。保重。",
  ar: "يبدو أنك غادرت. لا نحتفظ بأي من بياناتك. إذا احتجت المساعدة مرة أخرى، أنا هنا. اعتنِ بنفسك.",
};

/* ------------------------------------------------------------------ */
/*  Hook                                                              */
/* ------------------------------------------------------------------ */

export interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  language: Language;
  setLanguage: (lang: Language) => void;
  send: (text: string, audioBase64?: string, imageBase64?: string) => Promise<void>;
  addWelcome: () => void;
  retryLast: () => void;
  getLoadingMessage: (context: LoadingContext) => string;
}

export function useChat(initialLang: Language = "es"): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState<Language>(initialLang);
  const sessionId = useRef(generateSessionId());
  const lastRequestRef = useRef<{
    text: string;
    audioBase64?: string;
    imageBase64?: string;
  } | null>(null);
  const isSendingRef = useRef(false);
  const initialLangRef = useRef<Language>(initialLang);
  const hasWelcomedRef = useRef(false);
  const followupTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const goodbyeTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const getLoadingMessage = useCallback(
    (context: LoadingContext) => loadingMessages[language][context],
    [language],
  );

  const clearInactivityTimers = useCallback(() => {
    if (followupTimerRef.current) {
      clearTimeout(followupTimerRef.current);
      followupTimerRef.current = null;
    }
    if (goodbyeTimerRef.current) {
      clearTimeout(goodbyeTimerRef.current);
      goodbyeTimerRef.current = null;
    }
  }, []);

  const startInactivityTimers = useCallback(
    (lang: Language) => {
      clearInactivityTimers();

      followupTimerRef.current = setTimeout(() => {
        // Add follow-up message from Clara
        const followupId = createId();
        const followupText = FOLLOWUP_MESSAGES[lang];
        setMessages((prev) => [
          ...prev,
          {
            id: followupId,
            sender: "clara" as const,
            text: followupText,
            timestamp: new Date(),
          },
        ]);

        // Generate TTS for follow-up (best-effort)
        generateTTS(FOLLOWUP_SPEECH[lang], lang).then((audioUrl) => {
          if (audioUrl) {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === followupId
                  ? { ...m, audio: { url: audioUrl, state: "idle" as const } }
                  : m,
              ),
            );
          }
        });

        // Start goodbye timer (3 min after follow-up)
        goodbyeTimerRef.current = setTimeout(() => {
          const goodbyeId = createId();
          const goodbyeText = GOODBYE_MESSAGES[lang];
          setMessages((prev) => [
            ...prev,
            {
              id: goodbyeId,
              sender: "clara" as const,
              text: goodbyeText,
              timestamp: new Date(),
            },
          ]);

          // Generate TTS for goodbye (best-effort)
          generateTTS(GOODBYE_SPEECH[lang], lang).then((audioUrl) => {
            if (audioUrl) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === goodbyeId
                    ? { ...m, audio: { url: audioUrl, state: "idle" as const } }
                    : m,
                ),
              );
            }
          });

          // Call session/end to clear backend history
          fetch(`${API_BASE_URL}/api/session/end`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId.current }),
          }).catch(() => {});
        }, GOODBYE_DELAY_MS);
      }, FOLLOWUP_DELAY_MS);
    },
    [clearInactivityTimers],
  );

  // Cleanup timers on unmount
  useEffect(() => {
    return () => {
      clearInactivityTimers();
    };
  }, [clearInactivityTimers]);

  const addWelcome = useCallback(() => {
    if (hasWelcomedRef.current) return;
    hasWelcomedRef.current = true;
    const lang = initialLangRef.current;
    const welcomeText = welcomeMessages[lang];
    const welcomeId = createId();
    setMessages([
      {
        id: welcomeId,
        sender: "clara",
        text: welcomeText,
        timestamp: new Date(),
      },
    ]);
    // Generate TTS for welcome message (best-effort, non-blocking)
    // TTS: usar solo primera oracion para no exceder limite del backend
    const ttsText = welcomeText.split("\n\n")[0];
    generateTTS(ttsText, lang).then((audioUrl) => {
      if (audioUrl) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === welcomeId
              ? { ...m, audio: { url: audioUrl, state: "idle" as const } }
              : m,
          ),
        );
      }
    });
  }, []); // sin dependencias — solo ejecuta una vez, usa ref para idioma

  // When language changes, update the welcome message text + regenerate TTS
  const welcomeIdRef = useRef<string | null>(null);
  useEffect(() => {
    if (!hasWelcomedRef.current) return; // Welcome not yet shown
    const newText = welcomeMessages[language];
    const newId = createId();
    welcomeIdRef.current = newId;

    // Replace the first message (welcome) with the new language version
    setMessages((prev) => {
      if (prev.length === 0) return prev;
      const first = prev[0];
      if (first.sender !== "clara") return prev;
      return [
        { ...first, id: newId, text: newText, audio: undefined },
        ...prev.slice(1),
      ];
    });

    // Regenerate TTS for the new language
    const ttsText = newText.split("\n\n")[0];
    generateTTS(ttsText, language).then((audioUrl) => {
      if (audioUrl && welcomeIdRef.current === newId) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === newId
              ? { ...m, audio: { url: audioUrl, state: "idle" as const } }
              : m,
          ),
        );
      }
    });
  }, [language]); // eslint-disable-line react-hooks/exhaustive-deps

  const send = useCallback(
    async (text: string, audioBase64?: string, imageBase64?: string) => {
      // Guard sincronico contra double-submit (Maria tiene temblor en las manos)
      if (isSendingRef.current) return;
      isSendingRef.current = true;

      // Guardar request para posible retry
      lastRequestRef.current = { text, audioBase64, imageBase64 };

      // Determinar tipo de input y contexto de carga
      let inputType: ApiInputType = "text";
      let loadingContext: LoadingContext = "thinking";

      if (audioBase64) {
        inputType = "audio";
        loadingContext = "listening";
      } else if (imageBase64) {
        inputType = "image";
        loadingContext = "reading";
      }

      // Agregar mensaje del usuario
      const userMsg: Message = {
        id: createId(),
        sender: "user",
        text: text || (audioBase64 ? "\u{1F3A4}" : "\u{1F4F7}"),
        timestamp: new Date(),
      };

      // Agregar loading placeholder de Clara
      const loadingMsgId = createId();
      const loadingMsg: Message = {
        id: loadingMsgId,
        sender: "clara",
        text: "",
        timestamp: new Date(),
        loading: loadingContext,
      };

      setMessages((prev) => [...prev, userMsg, loadingMsg]);
      setIsLoading(true);

      try {
        const response: ChatResponse = await sendMessage({
          text,
          language,
          input_type: inputType,
          audio_base64: audioBase64 || null,
          image_base64: imageBase64 || null,
          session_id: sessionId.current,
        });

        // Construir AudioPlayback si hay audio
        const resolvedUrl = resolveAudioUrl(response.audio_url);
        const audio: AudioPlayback | undefined = resolvedUrl
          ? { url: resolvedUrl, state: "idle" }
          : undefined;

        const claraMsg: Message = {
          id: createId(),
          sender: "clara",
          text: response.response,
          audio,
          sources: response.sources,
          timestamp: new Date(),
        };

        // Reemplazar loading con respuesta real
        setMessages((prev) =>
          prev.filter((m) => m.id !== loadingMsgId).concat(claraMsg),
        );
      } catch (err) {
        // Error → burbuja de Clara con mensaje humano + boton de accion REAL
        let errorText: string;
        let errorAction: ErrorAction = "retry";
        let actionLabel: string;

        if (err instanceof ApiError) {
          const errInfo = getErrorMessage(err, language);
          errorText = errInfo.message;
          errorAction = errInfo.action;
          actionLabel = errInfo.actionLabel;
        } else {
          const fallbackText: Record<Language, string> = {
            es: "Perdona, algo no ha ido bien. Sigo aquí contigo.",
            en: "Sorry, something went wrong. I'm still here with you.",
            fr: "Désolée, quelque chose s'est mal passé.",
            pt: "Desculpa, algo correu mal. Continuo aqui contigo.",
            ro: "Scuze, ceva nu a mers bine. Sunt încă aici cu tine.",
            ca: "Perdona, alguna cosa no ha anat bé. Segueixo aquí amb tu.",
            zh: "抱歉，出了点问题。我还在这里陪你。",
            ar: "\u0639\u0630\u0631\u0627\u064B\u060C \u062D\u062F\u062B \u062E\u0637\u0623 \u0645\u0627. \u0623\u0646\u0627 \u0644\u0627 \u0632\u0644\u062A \u0647\u0646\u0627 \u0645\u0639\u0643.",
          };
          const fallbackLabel: Record<Language, string> = {
            es: "Reintentar",
            en: "Retry",
            fr: "Réessayer",
            pt: "Tentar novamente",
            ro: "Reîncearcă",
            ca: "Reintentar",
            zh: "重试",
            ar: "\u0625\u0639\u0627\u062F\u0629 \u0627\u0644\u0645\u062D\u0627\u0648\u0644\u0629",
          };
          errorText = fallbackText[language];
          actionLabel = fallbackLabel[language];
        }

        const errorMsg: Message = {
          id: createId(),
          sender: "clara",
          text: errorText,
          timestamp: new Date(),
          error: { action: errorAction, actionLabel },
        };

        setMessages((prev) =>
          prev.filter((m) => m.id !== loadingMsgId).concat(errorMsg),
        );
      } finally {
        setIsLoading(false);
        isSendingRef.current = false;
        // Start inactivity timers after every message exchange
        startInactivityTimers(language);
      }
    },
    [language, startInactivityTimers],
  );

  const retryLast = useCallback(() => {
    if (lastRequestRef.current) {
      const { text, audioBase64, imageBase64 } = lastRequestRef.current;
      void send(text, audioBase64, imageBase64);
    }
  }, [send]);

  return {
    messages,
    isLoading,
    language,
    setLanguage,
    send,
    addWelcome,
    retryLast,
    getLoadingMessage,
  };
}
