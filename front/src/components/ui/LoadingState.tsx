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
      className="flex items-start gap-3 justify-start mb-4"
    >
      {/* Clara avatar — matches ChatBubble's mascot avatar */}
      <div
        aria-hidden="true"
        className="flex-shrink-0 w-9 h-9 rounded-xl bg-clara-blue flex items-center justify-center"
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

      {/* Bubble */}
      <div
        className="
          max-w-[82%]
          px-4 py-3.5
          bg-white dark:bg-[#2a2a4a] border border-clara-border/50
          shadow-[0_1px_3px_rgba(0,0,0,0.06)]
          rounded-2xl rounded-tl-md
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
