interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({
  message = "Clara esta buscando informacion...",
}: LoadingStateProps) {
  return (
    <div
      className="flex items-end gap-2"
      style={{ animation: "fadeInUp 0.3s ease-out both" }}
    >
      {/* Clara avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-clara-blue to-[#2980B9]
                      flex items-center justify-center shrink-0 shadow-sm mb-1">
        <svg width="16" height="16" viewBox="0 0 80 80" fill="none" aria-hidden="true">
          <path d="M 28 28 A 14 14 0 0 1 28 52" stroke="white" strokeWidth="5"
                strokeLinecap="round" fill="none" opacity="0.8" />
          <circle cx="28" cy="40" r="4.5" fill="#D46A1E" />
        </svg>
      </div>

      <div
        role="status"
        aria-live="polite"
        className="bg-white border border-clara-border/60 rounded-2xl rounded-bl-md
                   shadow-sm px-4 py-3 max-w-[78%]"
      >
        <div className="flex items-center gap-2.5">
          <div className="flex gap-1" aria-hidden="true">
            <span className="w-2 h-2 bg-clara-blue/50 rounded-full animate-bounce [animation-delay:0ms]" />
            <span className="w-2 h-2 bg-clara-blue/50 rounded-full animate-bounce [animation-delay:150ms]" />
            <span className="w-2 h-2 bg-clara-blue/50 rounded-full animate-bounce [animation-delay:300ms]" />
          </div>
          <p className="text-[14px] text-clara-text-secondary">{message}</p>
        </div>
      </div>
    </div>
  );
}
