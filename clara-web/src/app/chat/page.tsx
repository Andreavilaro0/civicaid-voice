"use client";

import { useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Header from "@/components/Header";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import { useChat } from "@/hooks/useChat";
import type { Language } from "@/lib/types";

const comingSoon: Record<Language, string> = {
  es: "Esta funcion estara disponible pronto",
  fr: "Cette fonction sera bientot disponible",
};

function ChatContent() {
  const searchParams = useSearchParams();
  const initialLang = (searchParams.get("lang") as Language) || "es";
  const {
    messages,
    isLoading,
    language,
    setLanguage,
    send,
    addWelcome,
    retryLast,
    getLoadingMessage,
  } = useChat(initialLang);

  // Clara saluda al entrar — solo una vez (addWelcome tiene guard interno)
  useEffect(() => {
    addWelcome();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col h-screen bg-clara-bg">
      <Header language={language} onLanguageChange={setLanguage} />

      <MessageList
        messages={messages}
        language={language}
        getLoadingMessage={getLoadingMessage}
        onRetry={retryLast}
      />

      <ChatInput
        onSendText={(text) => send(text)}
        onStartVoice={() => {
          // Q7 reemplazara con VoiceRecorder
          alert(comingSoon[language]);
        }}
        onOpenCamera={() => {
          // Q9 reemplazara con DocumentUpload
          alert(comingSoon[language]);
        }}
        disabled={isLoading}
        language={language}
      />
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense>
      <ChatContent />
    </Suspense>
  );
}
