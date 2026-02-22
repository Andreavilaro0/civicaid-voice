import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import Header from "@/components/Header";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import VoiceRecorder from "@/components/VoiceRecorder";
import DocumentUpload from "@/components/DocumentUpload";
import QuickReplies from "@/components/QuickReplies";
import { useChat } from "@/hooks/useChat";
import { useMascotState } from "@/hooks/useMascotState.ts";
import type { Language } from "@/lib/types";

export default function ChatContent() {
  const [searchParams] = useSearchParams();
  const VALID_LANGS: Language[] = ["es", "en", "fr", "pt", "ro", "ca", "zh", "ar"];
  const rawLang = searchParams.get("lang");
  const initialLang: Language = VALID_LANGS.includes(rawLang as Language) ? (rawLang as Language) : "es";
  const [voiceActive, setVoiceActive] = useState(false);
  const [documentActive, setDocumentActive] = useState(false);
  const [showQuickReplies, setShowQuickReplies] = useState(true);
  const { messages, isLoading, language, setLanguage, send, addWelcome, retryLast, getLoadingMessage } = useChat(initialLang);
  const { setState: setMascotState } = useMascotState();
  const prevMsgCountRef = useRef(messages.length);

  useEffect(() => { addWelcome(); }, [addWelcome]);

  // Sync mascot state with chat loading
  useEffect(() => {
    if (isLoading) {
      setMascotState("thinking");
    } else if (messages.length > prevMsgCountRef.current) {
      // New message arrived — show talking, then idle
      setMascotState("talking");
      const timer = setTimeout(() => setMascotState("idle"), 2000);
      prevMsgCountRef.current = messages.length;
      return () => clearTimeout(timer);
    } else {
      setMascotState("idle");
    }
    prevMsgCountRef.current = messages.length;
  }, [isLoading, messages.length, setMascotState]);

  return (
    <div className="flex flex-col h-screen bg-clara-bg">
      <Header language={language} onLanguageChange={setLanguage} />
      <MessageList messages={messages} language={language} getLoadingMessage={getLoadingMessage} onRetry={retryLast} />
      <QuickReplies language={language} visible={showQuickReplies && messages.length <= 2}
        onSelect={(text) => { setShowQuickReplies(false); send(text); }} />
      <ChatInput onSendText={(text) => { setShowQuickReplies(false); send(text); }}
        onStartVoice={() => setVoiceActive(true)} onOpenCamera={() => setDocumentActive(true)}
        disabled={isLoading} language={language} activeMode={voiceActive ? "voice" : "text"} />
      <VoiceRecorder visible={voiceActive} language={language}
        onRecordingComplete={(audioBase64) => { setVoiceActive(false); send("", audioBase64); }}
        onCancel={() => setVoiceActive(false)} />
      <DocumentUpload visible={documentActive} language={language}
        onUpload={(imageBase64) => { setDocumentActive(false); send("", undefined, imageBase64); }}
        onCancel={() => setDocumentActive(false)} />
    </div>
  );
}
