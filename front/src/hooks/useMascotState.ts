import { useContext } from "react";
import { MascotContext } from "@/contexts/MascotContext.tsx";
import type { MascotContextType } from "@/contexts/MascotContext.tsx";

export function useMascotState(): MascotContextType {
  const ctx = useContext(MascotContext);
  if (!ctx) throw new Error("useMascotState must be used within MascotProvider");
  return ctx;
}
