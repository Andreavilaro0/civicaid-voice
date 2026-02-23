/**
 * ChatBubble — Clara / User message bubble
 *
 * Usage:
 *   <ChatBubble sender="clara" timestamp="10:42">
 *     Hola, soy Clara. ¿En qué te puedo ayudar hoy?
 *   </ChatBubble>
 *
 *   <ChatBubble sender="user" timestamp="10:43">
 *     Necesito información sobre el IMV.
 *   </ChatBubble>
 */

interface ChatBubbleProps {
  sender: "clara" | "user";
  children: React.ReactNode;
  timestamp?: string;
}

/** 32 × 32 circular Clara avatar with a white voice-arc SVG */
function ClaraAvatar() {
  return (
    <div
      className="flex-shrink-0 w-8 h-8 rounded-full bg-clara-blue flex items-center justify-center"
      aria-hidden="true"
    >
      {/* Voice arc — three concentric arcs growing outward from a mic dot */}
      <svg
        width="18"
        height="18"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Center dot */}
        <circle cx="8" cy="8" r="1.5" fill="white" />
        {/* Inner arc */}
        <path
          d="M5.5 8 A2.5 2.5 0 0 1 10.5 8"
          stroke="white"
          strokeWidth="1.2"
          strokeLinecap="round"
          fill="none"
        />
        {/* Outer arc */}
        <path
          d="M3.5 8 A4.5 4.5 0 0 1 12.5 8"
          stroke="white"
          strokeWidth="1.2"
          strokeLinecap="round"
          fill="none"
          opacity="0.65"
        />
      </svg>
    </div>
  );
}

export default function ChatBubble({ sender, children, timestamp }: ChatBubbleProps) {
  const isClara = sender === "clara";

  if (isClara) {
    return (
      <div className="flex items-start gap-2.5 justify-start mb-3">
        {/* Avatar sits at the top-left, aligned with the bubble top */}
        <ClaraAvatar />

        <div className="flex flex-col items-start max-w-[82%] md:max-w-[70%]">
          {/* Sender label */}
          <span className="text-clara-blue font-display font-bold text-[14px] mb-1 ml-1">
            Clara
          </span>

          {/* Bubble */}
          <div
            className="
              clara-bubble bg-clara-card border border-clara-border/60 shadow-sm
              rounded-2xl rounded-tl-sm
              px-4 py-3
            "
            role="article"
            aria-label="Clara message"
          >
            <div className="text-clara-text text-[16px] leading-relaxed space-y-2">
              {children}
            </div>

            {timestamp && (
              <p className="text-[12px] text-clara-text-secondary mt-2 text-right select-none">
                {timestamp}
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  /* ── User bubble ─────────────────────────────────────────── */
  return (
    <div className="flex justify-end mb-3">
      <div
        className="
          bg-clara-blue text-white
          rounded-2xl rounded-tr-sm
          px-4 py-3
          max-w-[82%] md:max-w-[70%]
        "
        role="article"
        aria-label="Your message"
      >
        <div className="text-[16px] leading-relaxed space-y-2">{children}</div>

        {timestamp && (
          <p className="text-[12px] text-white/60 mt-2 text-right select-none">
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
}
