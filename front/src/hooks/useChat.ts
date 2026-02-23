"use client";

import { useState, useCallback, useRef } from "react";
import {
  sendMessage,
  generateSessionId,
  generateTTS,
  resolveAudioUrl,
  getErrorMessage,
  ApiError,
} from "@/lib/api";
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

const welcomeMessages: Record<Language, string> = {
  es: "Hola, soy Clara. Soy una inteligencia artificial, no una persona.\n\nEstoy aqui para ayudarte con tramites del gobierno en Espana, paso a paso, en tu idioma. Mi informacion es orientativa.\n\nNo guardo tus datos personales. Cada conversacion empieza de cero.\n\nPreguntame sobre el Ingreso Minimo Vital, el empadronamiento, la tarjeta sanitaria, el NIE, o lo que necesites.",
  en: "Hi, I'm Clara. I'm an artificial intelligence, not a person.\n\nI'm here to help you with government procedures in Spain, step by step, in your language. My information is for guidance only.\n\nI don't store your personal data. Each conversation starts from scratch.\n\nAsk me about the Minimum Vital Income, municipal registration, the health card, NIE, or whatever you need.",
  fr: "Bonjour, je suis Clara. Je suis une intelligence artificielle, pas une personne.\n\nJe suis la pour t'aider avec les demarches administratives en Espagne, etape par etape, dans ta langue. Mes informations sont indicatives.\n\nJe ne conserve pas tes donnees personnelles. Chaque conversation repart de zero.\n\nDemande-moi sur le Revenu Minimum Vital, l'inscription municipale, la carte sanitaire, ou ce dont tu as besoin.",
  pt: "Olá, sou a Clara. Sou uma inteligência artificial, não uma pessoa.\n\nEstou aqui para te ajudar com trâmites do governo em Espanha, passo a passo, no teu idioma. A minha informação é orientativa.\n\nNão guardo os teus dados pessoais. Cada conversa começa do zero.\n\nPergunta-me sobre o Rendimento Mínimo Vital, o empadronamento, o cartão de saúde, ou o que precisares.",
  ro: "Bună, sunt Clara. Sunt o inteligență artificială, nu o persoană.\n\nSunt aici să te ajut cu procedurile guvernamentale din Spania, pas cu pas, în limba ta. Informațiile mele sunt orientative.\n\nNu păstrez datele tale personale. Fiecare conversație începe de la zero.\n\nÎntreabă-mă despre Venitul Minim Vital, înregistrarea municipală, cardul de sănătate, sau orice ai nevoie.",
  ca: "Hola, soc Clara. Soc una intel·ligència artificial, no una persona.\n\nSoc aquí per ajudar-te amb tràmits del govern a Espanya, pas a pas, en el teu idioma. La meva informació és orientativa.\n\nNo guardo les teves dades personals. Cada conversa comença de zero.\n\nPregunta'm sobre l'Ingrés Mínim Vital, l'empadronament, la targeta sanitària, o el que necessitis.",
  zh: "你好，我是Clara。我是人工智能，不是真人。\n\n我在这里帮你了解西班牙的政府手续，一步一步来，用你的语言。我的信息仅供参考。\n\n我不保存你的个人数据。每次对话都从零开始。\n\n你可以问我关于最低生活保障、市政登记、健康卡、NIE，或其他任何需要的问题。",
  ar: "\u0645\u0631\u062D\u0628\u0627\u060C \u0623\u0646\u0627 \u0643\u0644\u0627\u0631\u0627. \u0623\u0646\u0627 \u0630\u0643\u0627\u0621 \u0627\u0635\u0637\u0646\u0627\u0639\u064A\u060C \u0644\u0633\u062A \u0634\u062E\u0635\u0627\u064B \u062D\u0642\u064A\u0642\u064A\u0627\u064B.\n\n\u0623\u0646\u0627 \u0647\u0646\u0627 \u0644\u0645\u0633\u0627\u0639\u062F\u062A\u0643 \u0641\u064A \u0627\u0644\u0625\u062C\u0631\u0627\u0621\u0627\u062A \u0627\u0644\u062D\u0643\u0648\u0645\u064A\u0629 \u0641\u064A \u0625\u0633\u0628\u0627\u0646\u064A\u0627. \u0645\u0639\u0644\u0648\u0645\u0627\u062A\u064A \u0625\u0631\u0634\u0627\u062F\u064A\u0629.\n\n\u0644\u0627 \u0623\u062D\u0641\u0638 \u0628\u064A\u0627\u0646\u0627\u062A\u0643 \u0627\u0644\u0634\u062E\u0635\u064A\u0629. \u0643\u0644 \u0645\u062D\u0627\u062F\u062B\u0629 \u062A\u0628\u062F\u0623 \u0645\u0646 \u0627\u0644\u0635\u0641\u0631.\n\n\u064A\u0645\u0643\u0646\u0646\u064A \u0645\u0633\u0627\u0639\u062F\u062A\u0643 \u0641\u064A \u0627\u0644\u062D\u062F \u0627\u0644\u0623\u062F\u0646\u0649 \u0644\u0644\u062F\u062E\u0644\u060C \u0627\u0644\u062A\u0633\u062C\u064A\u0644 \u0627\u0644\u0628\u0644\u062F\u064A\u060C \u0627\u0644\u0628\u0637\u0627\u0642\u0629 \u0627\u0644\u0635\u062D\u064A\u0629\u060C \u0623\u0648 \u0645\u0627 \u062A\u062D\u062A\u0627\u062C.",
};

/* ------------------------------------------------------------------ */
/*  Loading messages por contexto                                      */
/* ------------------------------------------------------------------ */

const loadingMessages: Record<Language, Record<LoadingContext, string>> = {
  es: {
    listening: "Clara esta escuchando tu mensaje...",
    thinking: "Clara esta buscando informacion...",
    reading: "Clara esta leyendo tu documento...",
  },
  en: {
    listening: "Clara is listening...",
    thinking: "Clara is looking for information...",
    reading: "Clara is reading your document...",
  },
  fr: {
    listening: "Clara ecoute ton message...",
    thinking: "Clara cherche des informations...",
    reading: "Clara lit ton document...",
  },
  pt: {
    listening: "Clara está a ouvir...",
    thinking: "Clara está a procurar informação...",
    reading: "Clara está a ler o teu documento...",
  },
  ro: {
    listening: "Clara ascultă...",
    thinking: "Clara caută informații...",
    reading: "Clara citește documentul tău...",
  },
  ca: {
    listening: "Clara està escoltant...",
    thinking: "Clara està buscant informació...",
    reading: "Clara està llegint el teu document...",
  },
  zh: {
    listening: "Clara正在听...",
    thinking: "Clara正在查找信息...",
    reading: "Clara正在阅读你的文件...",
  },
  ar: {
    listening: "\u0643\u0644\u0627\u0631\u0627 \u062A\u0633\u062A\u0645\u0639 \u0625\u0644\u0649 \u0631\u0633\u0627\u0644\u062A\u0643...",
    thinking: "\u0643\u0644\u0627\u0631\u0627 \u062A\u0628\u062D\u062B \u0639\u0646 \u0645\u0639\u0644\u0648\u0645\u0627\u062A...",
    reading: "\u0643\u0644\u0627\u0631\u0627 \u062A\u0642\u0631\u0623 \u0645\u0633\u062A\u0646\u062F\u0643...",
  },
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

  const getLoadingMessage = useCallback(
    (context: LoadingContext) => loadingMessages[language][context],
    [language],
  );

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
    generateTTS(welcomeText, lang).then((audioUrl) => {
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
            es: "Perdona, algo no ha ido bien. Sigo aqui contigo.",
            en: "Sorry, something went wrong. I'm still here with you.",
            fr: "Desolee, quelque chose s'est mal passe.",
            pt: "Desculpa, algo correu mal. Continuo aqui contigo.",
            ro: "Scuze, ceva nu a mers bine. Sunt încă aici cu tine.",
            ca: "Perdona, alguna cosa no ha anat bé. Segueixo aquí amb tu.",
            zh: "抱歉，出了点问题。我还在这里陪你。",
            ar: "\u0639\u0630\u0631\u0627\u064B\u060C \u062D\u062F\u062B \u062E\u0637\u0623 \u0645\u0627. \u0623\u0646\u0627 \u0644\u0627 \u0632\u0644\u062A \u0647\u0646\u0627 \u0645\u0639\u0643.",
          };
          const fallbackLabel: Record<Language, string> = {
            es: "Reintentar",
            en: "Retry",
            fr: "Reessayer",
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
      }
    },
    [language],
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
