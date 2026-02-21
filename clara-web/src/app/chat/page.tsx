"use client";

import dynamic from "next/dynamic";

// ChatContent uses browser-only APIs (MediaRecorder, FileReader, etc.)
// Load it client-only to prevent SSR prerender failures.
const ChatContent = dynamic(() => import("./ChatContent"), { ssr: false });

export default function ChatPage() {
  return <ChatContent />;
}
