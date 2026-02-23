/**
 * LoadingState — typing indicator styled as a Clara chat bubble.
 *
 * Usage:
 *   <LoadingState />
 *   <LoadingState message="Buscando informacion..." />
 */

interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({
  message = "Clara esta buscando informacion...",
}: LoadingStateProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-label={message}
      className="flex items-end gap-2.5 justify-start mb-3"
    >
      {/* Clara avatar — mirrors ChatBubble's clara-side avatar */}
      <div
        aria-hidden="true"
        className="
          flex-shrink-0
          w-8 h-8
          rounded-full
          bg-clara-blue
          flex items-center justify-center
          shadow-sm
        "
      >
        {/* Voice-arc SVG identical to the one used in ChatBubble for Clara */}
        <svg
          width="18"
          height="18"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          {/* Centre bar */}
          <rect x="7" y="4" width="2" height="8" rx="1" fill="white" />
          {/* Inner arcs */}
          <path
            d="M5 6 Q3.5 8 5 10"
            stroke="white"
            strokeWidth="1.4"
            strokeLinecap="round"
            fill="none"
          />
          <path
            d="M11 6 Q12.5 8 11 10"
            stroke="white"
            strokeWidth="1.4"
            strokeLinecap="round"
            fill="none"
          />
          {/* Outer arcs */}
          <path
            d="M3 4.5 Q0.5 8 3 11.5"
            stroke="white"
            strokeWidth="1.2"
            strokeLinecap="round"
            fill="none"
            opacity="0.6"
          />
          <path
            d="M13 4.5 Q15.5 8 13 11.5"
            stroke="white"
            strokeWidth="1.2"
            strokeLinecap="round"
            fill="none"
            opacity="0.6"
          />
        </svg>
      </div>

      {/* Bubble */}
      <div
        className="
          max-w-[85%]
          px-4 py-3
          bg-clara-card border border-clara-border/60 shadow-sm
          rounded-2xl rounded-tl-sm
          flex flex-col gap-2
        "
      >
        {/* Typing dots */}
        <div className="flex items-center gap-1.5" aria-hidden="true">
          <span
            className="
              w-2 h-2 bg-clara-blue/60 rounded-full
              animate-bounce [animation-delay:0ms]
            "
          />
          <span
            className="
              w-2 h-2 bg-clara-blue/60 rounded-full
              animate-bounce [animation-delay:150ms]
            "
          />
          <span
            className="
              w-2 h-2 bg-clara-blue/60 rounded-full
              animate-bounce [animation-delay:300ms]
            "
          />
        </div>

        {/* Message text */}
        <p className="text-body-sm text-clara-text-secondary">{message}</p>
      </div>
    </div>
  );
}
