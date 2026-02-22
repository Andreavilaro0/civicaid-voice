import { createContext, useState, type ReactNode } from "react";

export type MascotState = "idle" | "greeting" | "thinking" | "talking";

export interface MascotContextType {
  state: MascotState;
  setState: (s: MascotState) => void;
}

export const MascotContext = createContext<MascotContextType | null>(null);

export function MascotProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<MascotState>("idle");
  return (
    <MascotContext.Provider value={{ state, setState }}>
      {children}
    </MascotContext.Provider>
  );
}
