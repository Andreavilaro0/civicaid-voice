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
  en: "Type your question...",
  fr: "Écris ta question...",
  pt: "Escreve a tua pergunta...",
  ro: "Scrie întrebarea ta...",
  ca: "Escriu la teva pregunta...",
  zh: "输入你的问题...",
  ar: "اكتب سؤالك...",
};

const ariaLabels: Record<Language, { send: string; voice: string; photo: string }> = {
  es: { send: "Enviar", voice: "Grabar voz", photo: "Subir foto" },
  en: { send: "Send", voice: "Record voice", photo: "Upload photo" },
  fr: { send: "Envoyer", voice: "Enregistrer", photo: "Photo" },
  pt: { send: "Enviar", voice: "Gravar voz", photo: "Foto" },
  ro: { send: "Trimite", voice: "Înregistrează", photo: "Foto" },
  ca: { send: "Enviar", voice: "Gravar veu", photo: "Foto" },
  zh: { send: "发送", voice: "录音", photo: "照片" },
  ar: { send: "إرسال", voice: "تسجيل صوتي", photo: "صورة" },
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
  const labels = ariaLabels[language];
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
    <div
      className="px-2 sm:px-3 py-2 bg-clara-bg/80 backdrop-blur-lg border-t border-clara-border/30 flex-shrink-0"
      style={{ paddingBottom: "max(8px, env(safe-area-inset-bottom))" }}
    >
      <form
        onSubmit={handleSubmit}
        className={[
          "chat-form flex items-center gap-1.5 sm:gap-2 overflow-hidden",
          "bg-white dark:bg-[#2a2a4a]",
          "border border-clara-border/60",
          "rounded-full",
          "shadow-[0_1px_4px_rgba(0,0,0,0.06)]",
          "pl-2 pr-1.5 py-1.5",
          "transition-[border-color,box-shadow] duration-150",
          "focus-within:border-clara-blue/50 focus-within:shadow-[0_0_0_3px_rgba(45,106,90,0.08)]",
          disabled ? "opacity-50" : "",
        ].join(" ")}
      >
        {/* Camera button — subtle, left side */}
        <button
          type="button"
          onClick={onOpenCamera}
          disabled={disabled}
          aria-label={labels.photo}
          className={[
            "flex-none flex items-center justify-center",
            "w-9 h-9 sm:w-11 sm:h-11",
            "rounded-full",
            "text-clara-text-secondary/60 hover:text-clara-blue hover:bg-clara-card",
            "transition-colors duration-150",
            "disabled:cursor-not-allowed",
          ].join(" ")}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
          </svg>
        </button>

        {/* Text input */}
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={placeholders[language]}
          disabled={disabled}
          aria-label={placeholders[language]}
          dir={language === "ar" ? "rtl" : "ltr"}
          className={[
            "flex-1 h-11 px-2",
            "bg-transparent border-none outline-none",
            "text-[16px] font-body",
            "text-clara-text placeholder:text-clara-text-secondary/50",
            "disabled:cursor-not-allowed",
          ].join(" ")}
        />

        {/* Voice or Send button — teal circle */}
        {hasText ? (
          <button
            type="submit"
            disabled={disabled}
            aria-label={labels.send}
            className={[
              "flex-none flex items-center justify-center",
              "w-11 h-11",
              "rounded-full",
              "bg-clara-blue text-white",
              "hover:bg-[var(--color-clara-blue-hover)]",
              "active:scale-95",
              "transition-[background-color,transform] duration-150",
              "disabled:cursor-not-allowed disabled:opacity-50",
            ].join(" ")}
          >
            {/* Arrow-up send icon */}
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <line x1="12" y1="19" x2="12" y2="5" />
              <polyline points="5 12 12 5 19 12" />
            </svg>
          </button>
        ) : (
          <button
            type="button"
            onClick={onStartVoice}
            disabled={disabled}
            aria-label={labels.voice}
            className={[
              "flex-none flex items-center justify-center",
              "w-11 h-11",
              "rounded-full",
              "bg-clara-blue text-white",
              "hover:opacity-90",
              "active:scale-95",
              "transition-[background-color,transform,opacity] duration-150",
              "disabled:cursor-not-allowed disabled:opacity-50",
            ].join(" ")}
            style={!disabled ? { animation: "micHintPulse 2.5s ease-in-out infinite" } : undefined}
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
            </svg>
          </button>
        )}
      </form>

      {/* Legal footer text */}
      <p className="text-center text-[12px] text-clara-text-secondary/40 mt-1.5 px-4 leading-tight">
        Clara es IA orientativa. Consulta siempre fuentes oficiales.
      </p>
    </div>
  );
}
