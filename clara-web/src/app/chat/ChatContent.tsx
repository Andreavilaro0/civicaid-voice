"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Header from "@/components/Header";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import VoiceRecorder from "@/components/VoiceRecorder";
import DocumentUpload from "@/components/DocumentUpload";
import QuickReplies from "@/components/QuickReplies";
import { useChat } from "@/hooks/useChat";
import type { Language } from "@/lib/types";

export default function ChatContent() {
  const searchParams = useSearchParams();
  const initialLang = (searchParams.get("lang") as Language) || "es";
  const [voiceActive, setVoiceActive] = useState(false);
  const [documentActive, setDocumentActive] = useState(false);
  const [showQuickReplies, setShowQuickReplies] = useState(true);
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

      {/* Quick-reply chips — shown after welcome, hidden after first send */}
      <QuickReplies
        language={language}
        visible={showQuickReplies && messages.length <= 2}
        onSelect={(text) => {
          setShowQuickReplies(false);
          send(text);
        }}
      />

      <ChatInput
        onSendText={(text) => {
          setShowQuickReplies(false);
          send(text);
        }}
        onStartVoice={() => setVoiceActive(true)}
        onOpenCamera={() => setDocumentActive(true)}
        disabled={isLoading}
        language={language}
        activeMode={voiceActive ? "voice" : "text"}
      />

      {/* VoiceRecorder overlay — siempre montado, controlado por visible */}
      <VoiceRecorder
        visible={voiceActive}
        language={language}
        onRecordingComplete={(audioBase64) => {
          setVoiceActive(false);
          send("", audioBase64);
        }}
        onCancel={() => setVoiceActive(false)}
      />

      {/* DocumentUpload overlay — patron identico a VoiceRecorder */}
      <DocumentUpload
        visible={documentActive}
        language={language}
        onUpload={(imageBase64) => {
          setDocumentActive(false);
          send("", undefined, imageBase64);
        }}
        onCancel={() => setDocumentActive(false)}
      />
    </div>
  );
}
