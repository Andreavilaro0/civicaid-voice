"use client";

import { useEffect, useRef, useCallback } from "react";
import ChatBubble from "@/components/ui/ChatBubble";
import LoadingState from "@/components/ui/LoadingState";
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
  fr: { conversation: "Conversation avec Clara", source: "Source", listen: "Ecouter la reponse" },
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
            <p
              className="whitespace-pre-wrap leading-relaxed"
              style={msg.sender === "clara" ? { textWrap: "balance" } : undefined}
            >
              {msg.text}
            </p>

            {/* Boton de accion en errores — REAL button, no texto plano */}
            {msg.error && (
              <button
                onClick={onRetry}
                className="mt-3 px-4 py-2 bg-clara-blue text-white rounded-lg
                           text-label font-medium min-h-touch-sm
                           hover:bg-[#164d66] transition-colors duration-150
                           focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2"
              >
                {msg.error.actionLabel}
              </button>
            )}

            {/* Audio stub — Q8 reemplazara con AudioPlayer */}
            {msg.audio && (
              <button
                className="flex items-center gap-2 mt-2 px-3 py-2
                           bg-white/60 rounded-lg text-clara-blue
                           min-h-touch-sm hover:bg-white/80 transition-colors duration-150"
                aria-label={l.listen}
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
                <span className="text-[16px] font-medium">{l.listen}</span>
              </button>
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
