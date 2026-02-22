import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
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
        className="fixed bottom-4 right-4 z-40 pointer-events-auto cursor-pointer hover:scale-105 transition-transform duration-300"
        onClick={() => { if (!isChat) navigate("/chat"); }}
        role={isChat ? undefined : "link"}
        aria-label={isChat ? undefined : "Abrir chat con Clara"}
      >
        <ClaraMascot />
      </div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/como-usar" element={<ComoUsarPage />} />
        <Route path="/quienes-somos" element={<QuienesSomosPage />} />
        <Route path="/futuro" element={<FuturoPage />} />
      </Routes>
    </>
  );
}
