import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import ComoUsarPage from "./pages/ComoUsarPage";
import QuienesSomosPage from "./pages/QuienesSomosPage";
import FuturoPage from "./pages/FuturoPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/chat" element={<ChatPage />} />
      <Route path="/como-usar" element={<ComoUsarPage />} />
      <Route path="/quienes-somos" element={<QuienesSomosPage />} />
      <Route path="/futuro" element={<FuturoPage />} />
    </Routes>
  );
}
