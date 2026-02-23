"use client";

import { useState, useRef, useEffect } from "react";

interface PromptBarProps {
  placeholders: string[];
  cycleIdx: number;
  cycleFade: boolean;
  onSubmitText: (text: string) => void;
  onMicTap: () => void;
}

export default function PromptBar({
  placeholders,
  cycleIdx,
  cycleFade,
  onSubmitText,
  onMicTap,
}: PromptBarProps) {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const [currentPlaceholder, setCurrentPlaceholder] = useState(placeholders[0] ?? "");

  useEffect(() => {
    setCurrentPlaceholder(placeholders[cycleIdx % placeholders.length] ?? "");
  }, [cycleIdx, placeholders]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    onSubmitText(trimmed);
    setValue("");
  }

  return (
    <form
      role="search"
      onSubmit={handleSubmit}
      className="prompt-bar w-full max-w-[560px] md:max-w-[640px]
                 flex items-center gap-2 px-4 py-3
                 bg-clara-card rounded-2xl
                 border-2 border-clara-border
                 shadow-warm transition-all duration-200"
    >
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={currentPlaceholder}
        aria-label={currentPlaceholder}
        className="flex-1 bg-transparent text-body-sm text-clara-text
                   placeholder:text-clara-text-secondary/50 outline-none min-w-0
                   transition-opacity duration-300"
        style={{
          direction: cycleFade && currentPlaceholder.charCodeAt(0) > 0x600 ? "rtl" : "ltr",
        }}
      />

      {value.trim() ? (
        <button
          type="submit"
          aria-label="Enviar"
          className="flex-shrink-0 w-touch-sm h-touch-sm flex items-center justify-center
                     rounded-full bg-clara-blue text-white
                     hover:bg-[var(--color-clara-blue-hover)] active:scale-95 transition-all duration-150
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M22 2L11 13" />
            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
          </svg>
        </button>
      ) : (
        <button
          type="button"
          onClick={onMicTap}
          aria-label="Hablar"
          className="flex-shrink-0 w-touch-sm h-touch-sm flex items-center justify-center
                     rounded-full bg-clara-orange/10 text-clara-orange
                     hover:bg-clara-orange/20 active:scale-95 transition-all duration-150
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-orange focus-visible:outline-offset-2"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
          </svg>
        </button>
      )}
    </form>
  );
}
