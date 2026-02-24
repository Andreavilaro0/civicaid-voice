import { useTheme } from "@/contexts/ThemeContext";

/** Compact sun/moon toggle for headers. 44px min touch target. */
export function ThemeToggleCompact() {
  const { resolved, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(resolved === "dark" ? "light" : "dark")}
      aria-label={resolved === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
      className="w-11 h-11 sm:w-touch-sm sm:h-touch-sm flex items-center justify-center rounded-xl
                 hover:bg-clara-hover transition-colors text-clara-text-secondary"
    >
      {resolved === "dark" ? (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
      ) : (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      )}
    </button>
  );
}

/** Full theme selector for menus: Light / Dark / Auto. */
export function ThemeToggleFull() {
  const { theme, setTheme } = useTheme();

  const options: { value: "light" | "dark" | "system"; label: string }[] = [
    { value: "light", label: "Claro" },
    { value: "dark", label: "Oscuro" },
    { value: "system", label: "Auto" },
  ];

  return (
    <div className="flex items-center gap-1 p-1 rounded-xl bg-clara-bg border border-clara-border" role="radiogroup" aria-label="Tema visual">
      {options.map((opt) => (
        <button
          key={opt.value}
          role="radio"
          aria-checked={theme === opt.value}
          onClick={() => setTheme(opt.value)}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-label font-medium transition-colors min-h-[44px]
            ${theme === opt.value
              ? "bg-clara-blue text-white"
              : "text-clara-text-secondary hover:bg-clara-hover"
            }`}
        >
          <span>{opt.label}</span>
        </button>
      ))}
    </div>
  );
}
