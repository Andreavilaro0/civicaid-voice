import { Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import ComoUsarPage from "./pages/ComoUsarPage";
import QuienesSomosPage from "./pages/QuienesSomosPage";
import FuturoPage from "./pages/FuturoPage";
import InfoLegalPage from "./pages/InfoLegalPage";
import ClaraMascot from "./components/ClaraMascot.tsx";

export default function App() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const isChat = pathname === "/chat";
  const isHome = pathname === "/";

  const mascotPos = isChat
    ? "bottom-24"
    : isHome
      ? "bottom-[200px] sm:bottom-4"
      : "bottom-4";

  return (
    <>
      <div
        className={`fixed right-4 z-40 pointer-events-auto cursor-pointer hover:scale-105 transition-all duration-300 ${mascotPos}`}
        onClick={() => { if (!isChat) navigate("/chat"); }}
        role={isChat ? undefined : "link"}
        aria-label={isChat ? undefined : "Abrir chat con Clara"}
        tabIndex={isChat ? undefined : 0}
        onKeyDown={(e) => { if (!isChat && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); navigate("/chat"); } }}
      >
        <ClaraMascot />
      </div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/como-usar" element={<ComoUsarPage />} />
        <Route path="/quienes-somos" element={<QuienesSomosPage />} />
        <Route path="/futuro" element={<FuturoPage />} />
        <Route path="/info-legal" element={<InfoLegalPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
