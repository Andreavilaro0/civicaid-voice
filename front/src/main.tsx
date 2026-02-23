import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { MascotProvider } from "./contexts/MascotContext.tsx";
import { ThemeProvider } from "./contexts/ThemeContext.tsx";
import App from "./App";
import "./globals.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <ThemeProvider>
        <MascotProvider>
          <App />
        </MascotProvider>
      </ThemeProvider>
    </BrowserRouter>
  </StrictMode>
);
