interface ChatBubbleProps {
  sender: "clara" | "user";
  children: React.ReactNode;
  timestamp?: string;
}

export default function ChatBubble({ sender, children, timestamp }: ChatBubbleProps) {
  const isClara = sender === "clara";

  return (
    <div className={`flex ${isClara ? "justify-start" : "justify-end"} mb-4`}>
      <div
        className={`
          max-w-[85%] px-4 py-3 rounded-bubble text-body-sm
          ${isClara
            ? "bg-clara-info text-clara-text rounded-bl-sm"
            : "bg-clara-blue text-white rounded-br-sm"
          }
        `}
      >
        {isClara && (
          <p className="font-display font-bold text-label text-clara-blue mb-1">
            Clara
          </p>
        )}
        <div className="space-y-2">{children}</div>
        {timestamp && (
          <p className="text-[14px] text-clara-text-secondary mt-2 text-right">
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
}
