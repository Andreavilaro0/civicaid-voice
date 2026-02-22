"use client";

import { useState, useRef } from "react";
import type { Language } from "@/lib/types";

interface ChatInputProps {
  onSendText: (text: string) => void;
  onStartVoice: () => void;
  onOpenCamera: () => void;
  disabled: boolean;
  language: Language;
  activeMode?: "text" | "voice" | "photo";
}

const placeholders: Record<Language, string> = {
  es: "Escribe tu pregunta...",
  fr: "Ecris ta question...",
  ar: "اكتب سؤالك...",
  en: "Type your question...",
  pt: "Escreve a tua pergunta...",
  ro: "Scrie intrebarea ta...",
  ca: "Escriu la teva pregunta...",
  zh: "输入你的问题...",
};

const sendLabels: Record<Language, string> = {
  es: "Enviar",
  fr: "Envoyer",
  ar: "إرسال",
  en: "Send",
  pt: "Enviar",
  ro: "Trimite",
  ca: "Enviar",
  zh: "发送",
};

const voiceLabels: Record<Language, string> = {
  es: "Grabar voz",
  fr: "Enregistrer la voix",
  ar: "تسجيل صوتي",
  en: "Record voice",
  pt: "Gravar voz",
  ro: "Inregistreaza vocea",
  ca: "Gravar veu",
  zh: "录制语音",
};

const photoLabels: Record<Language, string> = {
  es: "Enviar foto",
  fr: "Envoyer une photo",
  ar: "إرسال صورة",
  en: "Send photo",
  pt: "Enviar foto",
  ro: "Trimite fotografie",
  ca: "Enviar foto",
  zh: "发送照片",
};

export default function ChatInput({
  onSendText,
  onStartVoice,
  onOpenCamera,
  disabled,
  language,
}: ChatInputProps) {
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const hasText = text.trim().length > 0;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;
    onSendText(trimmed);
    setText("");
    inputRef.current?.focus();
  }

  return (
    <div className="sticky bottom-0 bg-white/80 backdrop-blur-lg border-t border-clara-border/50 px-3 py-3">
      <form onSubmit={handleSubmit} className="flex items-center gap-2 max-w-[640px] mx-auto">
        {/* Camera button */}
        <button
          type="button"
          onClick={onOpenCamera}
          disabled={disabled}
          aria-label={photoLabels[language]}
          className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full
                     text-clara-text-secondary hover:text-clara-blue hover:bg-clara-card
                     transition-colors duration-150
                     disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
            <circle cx="12" cy="13" r="4" />
          </svg>
        </button>

        {/* Text input */}
        <div className="flex-1 flex items-center bg-clara-card border border-clara-border/60
                        rounded-full px-4 min-h-[48px]
                        focus-within:border-clara-blue focus-within:shadow-[0_0_0_3px_rgba(27,94,123,0.1)]
                        transition-all duration-200">
          <input
            ref={inputRef}
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={placeholders[language]}
            disabled={disabled}
            aria-label={placeholders[language]}
            className="flex-1 bg-transparent text-[16px] font-body text-clara-text
                       placeholder:text-clara-text-secondary/50
                       focus:outline-none
                       disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>

        {/* Voice / Send button — toggles based on text content */}
        {hasText ? (
          <button
            type="submit"
            disabled={disabled}
            aria-label={sendLabels[language]}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full
                       bg-clara-blue text-white shadow-sm
                       hover:bg-[#164d66] active:scale-95
                       transition-all duration-150
                       disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          </button>
        ) : (
          <button
            type="button"
            onClick={onStartVoice}
            disabled={disabled}
            aria-label={voiceLabels[language]}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full
                       bg-clara-orange text-white shadow-sm
                       hover:bg-[#B85A18] active:scale-95
                       transition-all duration-150
                       disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
            </svg>
          </button>
        )}
      </form>
    </div>
  );
}
