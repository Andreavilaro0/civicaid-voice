"use client";

interface SuggestionChipsProps {
  suggestions: string[];
  cycleFade: boolean;
  onChipTap: (text: string) => void;
}

export default function SuggestionChips({
  suggestions,
  cycleFade,
  onChipTap,
}: SuggestionChipsProps) {
  return (
    <div
      className="suggestion-chips-scroll w-full max-w-[calc(100vw-48px)] md:max-w-[640px]
                 flex gap-2 overflow-x-auto md:flex-wrap md:justify-center
                 px-1 pr-4 py-1 transition-opacity duration-400"
      style={{ opacity: cycleFade ? 1 : 0 }}
    >
      {suggestions.map((text) => (
        <button
          key={text}
          onClick={() => onChipTap(text)}
          className="flex-shrink-0 min-h-touch-sm px-4 py-2
                     rounded-full border-2 border-clara-border
                     bg-clara-card
                     text-body-sm text-clara-blue font-medium whitespace-nowrap
                     hover:border-clara-blue/50 hover:bg-clara-info
                     active:scale-95 transition-all duration-150
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          {text}
        </button>
      ))}
    </div>
  );
}
