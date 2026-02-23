import { useState, useRef } from "react";
import type { Language } from "@/lib/types";

// Usage:
// <ChatInput
//   onSendText={(text) => console.log(text)}
//   onStartVoice={() => console.log("voice")}
//   onOpenCamera={() => console.log("camera")}
//   disabled={false}
//   language="es"
// />

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
  activeMode = "text",
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
      className={[
        "px-3 py-3",
        "bg-clara-bg/80",
        "backdrop-blur-lg",
        "border-t border-clara-border/50",
      ].join(" ")}
      style={{ paddingBottom: "max(12px, env(safe-area-inset-bottom))" }}
    >
      <form
        onSubmit={handleSubmit}
        className={[
          "chat-form flex items-center",
          "border-2 border-clara-border",
          "rounded-2xl",
          "transition-[border-color,box-shadow] duration-150",
          "focus-within:border-clara-blue focus-within:shadow-[0_0_0_3px_rgba(var(--clara-blue-rgb),0.1)]",
          disabled ? "opacity-50" : "",
        ].join(" ")}
      >
        {/* Camera button — left */}
        <button
          type="button"
          onClick={onOpenCamera}
          disabled={disabled}
          aria-label={labels.photo}
          className={[
            "flex-none flex items-center justify-center",
            "w-12 h-12 ml-1",
            "rounded-xl",
            "text-clara-text-secondary hover:text-clara-blue",
            "transition-colors duration-150",
            "disabled:cursor-not-allowed",
          ].join(" ")}
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
          </svg>
        </button>

        {/* Text input — middle */}
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
            "flex-1 h-12 px-3",
            "bg-transparent border-none outline-none",
            "text-body-sm font-body",
            "text-clara-text placeholder:text-clara-text-secondary",
            "disabled:cursor-not-allowed",
          ].join(" ")}
        />

        {/* Voice or Send button — right */}
        {hasText ? (
          <button
            type="submit"
            disabled={disabled}
            aria-label={labels.send}
            className={[
              "flex-none flex items-center justify-center",
              "w-12 h-12 mr-1",
              "rounded-xl",
              "bg-clara-blue text-white",
              "hover:bg-[var(--color-clara-blue-hover)]",
              "transition-colors duration-150",
              "disabled:cursor-not-allowed disabled:opacity-50",
            ].join(" ")}
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
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
              "w-12 h-12 mr-1",
              "rounded-xl",
              "text-clara-text-secondary hover:text-clara-blue",
              "transition-colors duration-150",
              "disabled:cursor-not-allowed",
            ].join(" ")}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
            </svg>
          </button>
        )}
      </form>
    </div>
  );
}
