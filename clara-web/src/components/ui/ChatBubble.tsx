interface ChatBubbleProps {
  sender: "clara" | "user";
  children: React.ReactNode;
  timestamp?: string;
}

export default function ChatBubble({ sender, children, timestamp }: ChatBubbleProps) {
  const isClara = sender === "clara";

  return (
    <div
      className={`flex items-end gap-2 ${isClara ? "justify-start" : "justify-end"}`}
      style={{ animation: "fadeInUp 0.3s ease-out both" }}
    >
      {/* Clara avatar */}
      {isClara && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-clara-blue to-[#2980B9]
                        flex items-center justify-center shrink-0 shadow-sm mb-1">
          <svg width="16" height="16" viewBox="0 0 80 80" fill="none" aria-hidden="true">
            <path d="M 28 28 A 14 14 0 0 1 28 52" stroke="white" strokeWidth="5"
                  strokeLinecap="round" fill="none" opacity="0.8" />
            <circle cx="28" cy="40" r="4.5" fill="#D46A1E" />
          </svg>
        </div>
      )}

      <div
        className={`
          max-w-[78%] px-4 py-3 text-body-sm
          ${isClara
            ? "bg-white border border-clara-border/60 text-clara-text rounded-2xl rounded-bl-md shadow-sm"
            : "bg-clara-blue text-white rounded-2xl rounded-br-md shadow-sm"
          }
        `}
      >
        <div className="space-y-2">{children}</div>
        {timestamp && (
          <p className={`text-[12px] mt-1.5 text-right ${isClara ? "text-clara-text-secondary/60" : "text-white/60"}`}>
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
}
