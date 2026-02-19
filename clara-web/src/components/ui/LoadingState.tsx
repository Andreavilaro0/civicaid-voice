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
      className="flex items-center gap-3 px-4 py-3 bg-clara-info rounded-bubble max-w-[85%]"
    >
      <div className="flex gap-1" aria-hidden="true">
        <span className="w-2 h-2 bg-clara-blue rounded-full animate-bounce [animation-delay:0ms]" />
        <span className="w-2 h-2 bg-clara-blue rounded-full animate-bounce [animation-delay:150ms]" />
        <span className="w-2 h-2 bg-clara-blue rounded-full animate-bounce [animation-delay:300ms]" />
      </div>
      <p className="text-body-sm text-clara-text-secondary">{message}</p>
    </div>
  );
}
