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
};

const modeLabels: Record<Language, { write: string; voice: string; photo: string; send: string }> = {
  es: { write: "Escribir", voice: "Voz", photo: "Foto", send: "Enviar" },
  fr: { write: "Ecrire", voice: "Voix", photo: "Photo", send: "Envoyer" },
  ar: { write: "كتابة", voice: "صوت", photo: "صورة", send: "إرسال" },
};

export default function ChatInput({
  onSendText,
  onStartVoice,
  onOpenCamera,
  disabled,
  language,
  activeMode = "text",
}: ChatInputProps) {
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const l = modeLabels[language];

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;
    onSendText(trimmed);
    setText("");
    inputRef.current?.focus();
  }

  return (
    <div className="sticky bottom-0 bg-white border-t border-clara-border px-4 py-3 space-y-3">
      {/* Linea 1: Input + Enviar */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={placeholders[language]}
          disabled={disabled}
          aria-label={placeholders[language]}
          className="flex-1 h-[56px] px-4 border-2 border-clara-border rounded-xl
                     text-body-sm font-body bg-white
                     focus:border-clara-blue focus:outline-none
                     disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={disabled || !text.trim()}
          aria-label={l.send}
          className="min-w-touch min-h-touch bg-clara-blue text-white rounded-xl
                     flex items-center justify-center
                     hover:bg-[#164d66] transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </form>

      {/* Linea 2: 3 botones de modo */}
      <div className="flex gap-3 justify-center">
        {/* Escribir — focus al input, muestra estado activo */}
        <button
          type="button"
          onClick={() => inputRef.current?.focus()}
          disabled={disabled}
          aria-label={l.write}
          aria-pressed={activeMode === "text"}
          className={`flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed
                     ${activeMode === "text"
                       ? "border-clara-blue text-clara-blue bg-clara-blue/5 font-medium"
                       : "border-clara-border text-clara-text-secondary hover:border-clara-blue hover:text-clara-blue"
                     }`}
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M20 5H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z" />
          </svg>
          <span className="text-label mt-1">{l.write}</span>
        </button>

        {/* Voz — stub para Q7 */}
        <button
          type="button"
          onClick={onStartVoice}
          disabled={disabled}
          aria-label={l.voice}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-orange text-clara-orange
                     hover:bg-clara-orange hover:text-white
                     transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
          </svg>
          <span className="text-label mt-1">{l.voice}</span>
        </button>

        {/* Foto — stub para Q9 */}
        <button
          type="button"
          onClick={onOpenCamera}
          disabled={disabled}
          aria-label={l.photo}
          className="flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 border-clara-border text-clara-text-secondary
                     hover:border-clara-blue hover:text-clara-blue
                     transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
          </svg>
          <span className="text-label mt-1">{l.photo}</span>
        </button>
      </div>
    </div>
  );
}
