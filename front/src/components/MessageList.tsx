"use client";

import { useEffect, useRef, useCallback, useState } from "react";
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

/** Labels bilingues para la lista */
const labels: Record<Language, { conversation: string; source: string; listen: string }> = {
  es: { conversation: "Conversacion con Clara", source: "Fuente", listen: "Escuchar respuesta" },
  en: { conversation: "Conversation with Clara", source: "Source", listen: "Listen to response" },
  fr: { conversation: "Conversation avec Clara", source: "Source", listen: "Ecouter la reponse" },
  pt: { conversation: "Conversa com Clara", source: "Fonte", listen: "Ouvir resposta" },
  ro: { conversation: "Conversație cu Clara", source: "Sursă", listen: "Ascultă răspunsul" },
  ca: { conversation: "Conversa amb Clara", source: "Font", listen: "Escoltar resposta" },
  zh: { conversation: "与Clara的对话", source: "来源", listen: "收听回复" },
  ar: { conversation: "محادثة مع كلارا", source: "المصدر", listen: "استمع للرد" },
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
  const [autoPlayId, setAutoPlayId] = useState<string | null>(null);
  const autoPlayedIdsRef = useRef(new Set<string>());

  useEffect(() => {
    for (let i = messages.length - 1; i >= 0; i--) {
      const m = messages[i];
      if (m.sender === "clara" && m.audio?.url && !m.loading && !autoPlayedIdsRef.current.has(m.id)) {
        autoPlayedIdsRef.current.add(m.id);
        setAutoPlayId(m.id);
        return;
      }
    }
    setAutoPlayId(null);
  }, [messages]);

  // Detectar si el usuario scrolleo hacia arriba manualmente
  const handleScroll = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    userScrolledRef.current = distanceFromBottom > 100;
  }, []);

  // Auto-scroll al fondo si el usuario no ha scrolleado manualmente
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
      className="flex-1 overflow-y-auto px-4 py-6 space-y-2"
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
            {/* Texto del mensaje — leading-relaxed para legibilidad, balance en Clara */}
            <p className="whitespace-pre-wrap leading-relaxed">
              {msg.text}
            </p>

            {/* Boton de accion en errores — REAL button, no texto plano */}
            {msg.error && (
              <button
                onClick={onRetry}
                className="mt-3 px-4 py-2 bg-clara-blue text-white rounded-lg
                           text-label font-medium min-h-touch-sm
                           hover:bg-[var(--color-clara-blue-hover)] transition-colors duration-150
                           focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2"
              >
                {msg.error.actionLabel}
              </button>
            )}

            {/* Audio player — reproduccion de respuesta de Clara */}
            {msg.audio && msg.audio.url && (
              <AudioPlayer
                src={resolveAudioUrl(msg.audio.url) || msg.audio.url}
                language={language}
                autoPlay={msg.id === autoPlayId}
              />
            )}

            {/* Fuentes citadas */}
            {msg.sources && msg.sources.length > 0 && (
              <p className="text-label mt-2 text-clara-text-secondary">
                {l.source}:{" "}
                {msg.sources.map((s, i) => (
                  <span key={i}>
                    {i > 0 && ", "}
                    <a
                      href={s.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline hover:opacity-100"
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
