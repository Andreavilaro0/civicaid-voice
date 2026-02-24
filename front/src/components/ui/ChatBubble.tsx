/**
 * ChatBubble — Clara / User message bubble
 *
 * Redesigned to match teal-themed reference with mascot avatar,
 * cleaner spacing, and refined bubble shapes.
 */

interface ChatBubbleProps {
  sender: "clara" | "user";
  children: React.ReactNode;
  timestamp?: string;
}

/** Teal rounded-square Clara mascot avatar — matches Header */
function ClaraAvatar() {
  return (
    <div
      className="flex-shrink-0 w-9 h-9 rounded-xl bg-clara-blue flex items-center justify-center"
      aria-hidden="true"
    >
      <svg width="20" height="20" viewBox="0 0 32 32" fill="none">
        <rect x="6" y="4" width="20" height="18" rx="6" stroke="white" strokeWidth="1.8" fill="none" />
        <circle cx="12" cy="13" r="2" fill="white" />
        <circle cx="20" cy="13" r="2" fill="white" />
        <path d="M11 18 Q16 22 21 18" stroke="white" strokeWidth="1.6" strokeLinecap="round" fill="none" />
        <line x1="16" y1="4" x2="16" y2="1" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="16" cy="0.5" r="1.2" fill="white" />
        <rect x="2" y="10" width="4" height="6" rx="2" fill="white" opacity="0.7" />
        <rect x="26" y="10" width="4" height="6" rx="2" fill="white" opacity="0.7" />
      </svg>
    </div>
  );
}

export default function ChatBubble({ sender, children, timestamp }: ChatBubbleProps) {
  const isClara = sender === "clara";

  if (isClara) {
    return (
      <div className="flex items-start gap-3 justify-start mb-4">
        <ClaraAvatar />

        <div className="flex flex-col items-start max-w-[82%] md:max-w-[70%] min-w-0">
          <span className="text-clara-blue font-display font-semibold text-[13px] mb-1.5 ml-1 tracking-wide uppercase">
            Clara
          </span>

          <div
            className="
              clara-bubble bg-white dark:bg-[#2a2a4a] border border-clara-border/50
              shadow-[0_1px_3px_rgba(0,0,0,0.06)]
              rounded-2xl rounded-tl-md
              px-4 py-3.5
              overflow-hidden break-words
            "
            role="article"
            aria-label="Clara message"
          >
            <div className="text-clara-text text-[16px] leading-relaxed space-y-2">
              {children}
            </div>

            {timestamp && (
              <p className="text-[12px] text-clara-text-secondary/70 mt-2.5 text-right select-none tabular-nums">
                {timestamp}
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  /* ── User bubble — teal with white text ─────────────────── */
  return (
    <div className="flex justify-end mb-4">
      <div
        className="
          bg-clara-blue text-white
          rounded-2xl rounded-tr-md
          px-4 py-3.5
          max-w-[82%] md:max-w-[70%]
          shadow-[0_1px_3px_rgba(0,0,0,0.1)]
        "
        role="article"
        aria-label="Your message"
      >
        <div className="text-[16px] leading-relaxed space-y-2">{children}</div>

        {timestamp && (
          <p className="text-[12px] text-white/50 mt-2.5 text-right select-none tabular-nums">
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
}
