import { Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import ComoUsarPage from "./pages/ComoUsarPage";
import QuienesSomosPage from "./pages/QuienesSomosPage";
import FuturoPage from "./pages/FuturoPage";
import ClaraMascot from "./components/ClaraMascot.tsx";

export default function App() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const isChat = pathname === "/chat";

  return (
    <>
      <div
        className={`fixed right-4 z-40 pointer-events-auto cursor-pointer hover:scale-105 transition-all duration-300 ${isChat ? "bottom-24" : "bottom-4"}`}
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
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
