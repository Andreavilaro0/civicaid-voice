"use client";

import { useEffect, useRef, useCallback } from "react";
import ChatBubble from "@/components/ui/ChatBubble";
import LoadingState from "@/components/ui/LoadingState";
import AudioPlayer from "@/components/ui/AudioPlayer";
import { resolveAudioUrl } from "@/lib/api";
import type { Message, Language, LoadingContext } from "@/lib/types";

interface MessageListProps {
  messages: Message[];
  language: Language;
  getLoadingMessage: (context: LoadingContext) => string;
  onRetry: () => void;
}

const labels: Record<Language, { conversation: string; source: string; listen: string }> = {
  es: { conversation: "Conversacion con Clara", source: "Fuente", listen: "Escuchar respuesta" },
  fr: { conversation: "Conversation avec Clara", source: "Source", listen: "Ecouter la reponse" },
  ar: { conversation: "محادثة مع كلارا", source: "المصدر", listen: "استمع للرد" },
  en: { conversation: "Conversation with Clara", source: "Source", listen: "Listen to response" },
  pt: { conversation: "Conversa com a Clara", source: "Fonte", listen: "Ouvir resposta" },
  ro: { conversation: "Conversatie cu Clara", source: "Sursa", listen: "Asculta raspunsul" },
  ca: { conversation: "Conversa amb Clara", source: "Font", listen: "Escoltar resposta" },
  zh: { conversation: "与Clara的对话", source: "来源", listen: "收听回复" },
};

export default function MessageList({
  messages,
  language,
  getLoadingMessage,
  onRetry,
}: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const userScrolledRef = useRef(false);

  const handleScroll = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    userScrolledRef.current = distanceFromBottom > 100;
  }, []);

  useEffect(() => {
    if (!userScrolledRef.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const l = labels[language];

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto px-4 py-6 space-y-4"
      role="log"
      aria-label={l.conversation}
      aria-live="polite"
    >
      {messages.map((msg) =>
        msg.loading ? (
          <LoadingState
            key={msg.id}
            message={getLoadingMessage(msg.loading)}
          />
        ) : (
          <ChatBubble
            key={msg.id}
            sender={msg.sender}
            timestamp={msg.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          >
            <p
              className="whitespace-pre-wrap leading-relaxed"
              style={msg.sender === "clara" ? { textWrap: "balance" } : undefined}
            >
              {msg.text}
            </p>

            {msg.error && (
              <button
                onClick={onRetry}
                className="mt-3 px-4 py-2 bg-clara-blue text-white rounded-full
                           text-label font-medium min-h-touch-sm
                           hover:bg-[#164d66] transition-colors duration-150
                           focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2"
              >
                {msg.error.actionLabel}
              </button>
            )}

            {msg.audio && msg.audio.url && (
              <AudioPlayer
                src={resolveAudioUrl(msg.audio.url) || msg.audio.url}
                language={language}
              />
            )}

            {msg.sources && msg.sources.length > 0 && (
              <p className="text-[13px] mt-2 text-clara-text-secondary">
                {l.source}:{" "}
                {msg.sources.map((s, i) => (
                  <span key={i}>
                    {i > 0 && ", "}
                    <a
                      href={s.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline hover:text-clara-blue transition-colors"
                    >
                      {s.name}
                    </a>
                  </span>
                ))}
              </p>
            )}
          </ChatBubble>
        ),
      )}
      <div ref={bottomRef} />
    </div>
  );
}
