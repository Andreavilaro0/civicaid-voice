"use client";

import { useState, useCallback, useRef } from "react";
import {
  sendMessage,
  generateSessionId,
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
  es: "Hola, soy Clara.\n\nLos tramites no deberian ser tan complicados. Estoy aqui para ayudarte a entenderlos, paso a paso, en tu idioma.\n\nPreguntame sobre el Ingreso Minimo Vital, el empadronamiento, la tarjeta sanitaria, o lo que necesites.",
  fr: "Bonjour, je suis Clara.\n\nLes demarches ne devraient pas etre si compliquees. Je suis la pour t'aider a les comprendre, etape par etape, dans ta langue.\n\nDemande-moi sur le Revenu Minimum Vital, l'inscription municipale, la carte sanitaire, ou ce dont tu as besoin.",
  ar: '\u0645\u0631\u062D\u0628\u0627\u060C \u0623\u0646\u0627 \u0643\u0644\u0627\u0631\u0627. \u0623\u0646\u0627 \u0647\u0646\u0627 \u0644\u0645\u0633\u0627\u0639\u062F\u062A\u0643 \u0641\u064A \u0627\u0644\u0625\u062C\u0631\u0627\u0621\u0627\u062A \u0627\u0644\u062D\u0643\u0648\u0645\u064A\u0629 \u0641\u064A \u0625\u0633\u0628\u0627\u0646\u064A\u0627.\n\n\u064A\u0645\u0643\u0646\u0646\u064A \u0645\u0633\u0627\u0639\u062F\u062A\u0643 \u0641\u064A:\n\u2014 \u0627\u0644\u062D\u062F \u0627\u0644\u0623\u062F\u0646\u0649 \u0644\u0644\u062F\u062E\u0644 (\u0645\u0633\u0627\u0639\u062F\u0629 \u0645\u0627\u0644\u064A\u0629)\n\u2014 \u0627\u0644\u062A\u0633\u062C\u064A\u0644 \u0627\u0644\u0628\u0644\u062F\u064A\n\u2014 \u0627\u0644\u0628\u0637\u0627\u0642\u0629 \u0627\u0644\u0635\u062D\u064A\u0629\n\n\u0645\u0627\u0630\u0627 \u062A\u062D\u062A\u0627\u062C\u061F',
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
  fr: {
    listening: "Clara ecoute ton message...",
    thinking: "Clara cherche des informations...",
    reading: "Clara lit ton document...",
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
    setMessages([
      {
        id: createId(),
        sender: "clara",
        text: welcomeMessages[initialLangRef.current],
        timestamp: new Date(),
      },
    ]);
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
          errorText =
            language === "fr"
              ? "Desolee, quelque chose s'est mal passe."
              : language === "ar"
              ? "\u0639\u0630\u0631\u0627\u064B\u060C \u062D\u062F\u062B \u062E\u0637\u0623 \u0645\u0627. \u0623\u0646\u0627 \u0644\u0627 \u0632\u0644\u062A \u0647\u0646\u0627 \u0645\u0639\u0643."
              : "Perdona, algo no ha ido bien. Sigo aqui contigo.";
          actionLabel = language === "fr" ? "Reessayer" : language === "ar" ? "\u0625\u0639\u0627\u062F\u0629 \u0627\u0644\u0645\u062D\u0627\u0648\u0644\u0629" : "Reintentar";
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
      send(text, audioBase64, imageBase64);
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
