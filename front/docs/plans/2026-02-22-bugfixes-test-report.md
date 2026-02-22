# Bug Fixes from Test Report — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all High and Critical bugs found in the QA test report, plus quick Medium fixes.

**Architecture:** Targeted edits to 8 files — no new dependencies, no refactors. Each task is one file, one concern.

**Tech Stack:** React 19, TypeScript 5.9, React Router 7, Vite 7

---

## Task 1: Add 404 Catch-All Route

**Files:**
- Modify: `front/src/App.tsx:24-30`

**Step 1: Add catch-all route**

In `App.tsx`, add a `Navigate` import and a wildcard route that redirects to `/`:

```tsx
// Add to imports (line 1):
import { Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";

// Add inside <Routes> after the last <Route> (after line 29):
<Route path="*" element={<Navigate to="/" replace />} />
```

**Step 2: Verify**

Run: `npx tsc -b`
Expected: No errors.

Open `http://localhost:5190/nonexistent` — should redirect to `/`.

**Step 3: Commit**

```bash
git add front/src/App.tsx
git commit -m "fix: add 404 catch-all route to redirect to home"
```

---

## Task 2: Fix useEffect Dependency Arrays in ChatContent

**Files:**
- Modify: `front/src/pages/ChatContent.tsx:23,39`

**Step 1: Fix addWelcome effect (line 23)**

Change:
```tsx
useEffect(() => { addWelcome(); }, []);
```
To:
```tsx
useEffect(() => { addWelcome(); }, [addWelcome]);
```

`addWelcome` is wrapped in `useCallback([], [])` in `useChat.ts:125-136` so it is referentially stable. Adding it to deps is safe and silences the lint warning.

**Step 2: Fix mascot state effect (line 39)**

Change:
```tsx
}, [isLoading, messages.length]);
```
To:
```tsx
}, [isLoading, messages.length, setMascotState]);
```

`setMascotState` comes from `useState` in `MascotContext.tsx:13` so it is referentially stable.

**Step 3: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 4: Commit**

```bash
git add front/src/pages/ChatContent.tsx
git commit -m "fix: add missing deps to useEffect arrays in ChatContent"
```

---

## Task 3: Fix Side Effect Inside useMemo in MessageList

**Files:**
- Modify: `front/src/components/MessageList.tsx:40-50`

**Step 1: Replace useMemo with useEffect + useState**

The current code mutates a ref inside `useMemo` (line 45). Replace the `useMemo` block (lines 40-50) with:

```tsx
const [autoPlayId, setAutoPlayId] = useState<string | null>(null);
const autoPlayedIdsRef = useRef(new Set<string>());

useEffect(() => {
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (m.sender === "clara" && m.audio?.url && !m.loading && !autoPlayedIdsRef.current.has(m.id)) {
      autoPlayedIdsRef.current.add(m.id);
      setAutoPlayId(m.id);
      return;
    }
  }
  setAutoPlayId(null);
}, [messages]);
```

Also update imports (line 3) — add `useState`, remove `useMemo`:
```tsx
import { useEffect, useRef, useCallback, useState } from "react";
```

And remove the existing `autoPlayedIdsRef` declaration at line 38 (since it moves into the new block).

**Step 2: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 3: Commit**

```bash
git add front/src/components/MessageList.tsx
git commit -m "fix: move side effect from useMemo to useEffect in MessageList"
```

---

## Task 4: Validate Language URL Parameter

**Files:**
- Modify: `front/src/pages/ChatContent.tsx:15`

**Step 1: Add runtime validation**

Change line 15 from:
```tsx
const initialLang = (searchParams.get("lang") as Language) || "es";
```
To:
```tsx
const VALID_LANGS: Language[] = ["es", "en", "fr", "pt", "ro", "ca", "zh", "ar"];
const rawLang = searchParams.get("lang");
const initialLang: Language = VALID_LANGS.includes(rawLang as Language) ? (rawLang as Language) : "es";
```

**Step 2: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 3: Commit**

```bash
git add front/src/pages/ChatContent.tsx
git commit -m "fix: validate lang URL parameter instead of unsafe type cast"
```

---

## Task 5: Fix AudioContext Leak

**Files:**
- Modify: `front/src/hooks/useAudioPlayer.ts:35-50`
- Modify: `front/src/components/DocumentUpload.tsx:139-156`

**Step 1: Fix playClickFeedback in useAudioPlayer.ts**

Replace lines 35-50:
```tsx
function playClickFeedback(): void {
  if (typeof AudioContext === "undefined") return;
  if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "triangle";
    osc.frequency.value = 800;
    gain.gain.value = 0.05;
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
    osc.onended = () => ctx.close();
  } catch { /* silent fail — no audio context available */ }
}
```

The only change is adding `osc.onended = () => ctx.close();` after `osc.stop()`.

**Step 2: Fix playShutterFeedback in DocumentUpload.tsx**

Replace lines 139-156:
```tsx
function playShutterFeedback() {
  if (typeof AudioContext === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = 1200;
    gain.gain.setValueAtTime(0.06, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
    osc.onended = () => ctx.close();
  } catch {
    /* silent fail */
  }
}
```

Same pattern — add `osc.onended = () => ctx.close();`.

**Step 3: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 4: Commit**

```bash
git add front/src/hooks/useAudioPlayer.ts front/src/components/DocumentUpload.tsx
git commit -m "fix: close AudioContext after feedback sound to prevent resource leak"
```

---

## Task 6: Fix Unhandled Promises

**Files:**
- Modify: `front/src/hooks/useChat.ts:267`
- Modify: `front/src/components/VoiceRecorder.tsx:358`

**Step 1: Fix retryLast in useChat.ts**

Change line 267 from:
```tsx
send(text, audioBase64, imageBase64);
```
To:
```tsx
void send(text, audioBase64, imageBase64);
```

The `void` operator explicitly marks the promise as intentionally unhandled. `send()` already has its own internal try/catch that handles all errors and updates the UI.

**Step 2: Fix VoiceRecorder start() call**

Change line 358 from:
```tsx
onClick={() => start()}
```
To:
```tsx
onClick={() => void start()}
```

**Step 3: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 4: Commit**

```bash
git add front/src/hooks/useChat.ts front/src/components/VoiceRecorder.tsx
git commit -m "fix: mark intentionally fire-and-forget promises with void operator"
```

---

## Task 7: Fix ClaraMascot Reactivity Bugs

**Files:**
- Modify: `front/src/components/ClaraMascot.tsx:16-36,53`

**Step 1: Fix useWidgetSize hook (lines 16-36)**

Replace the entire `useWidgetSize` function with a version that uses `useCallback` for `getSize` and derives `isMobile` reactively:

```tsx
function useWidgetSize(isChat: boolean) {
  const getSize = useCallback((w: number) => {
    if (isChat) return w < 1024 ? 100 : 130;
    return w < 640 ? 120 : w < 1024 ? 160 : 200;
  }, [isChat]);

  const [size, setSize] = useState(() => getSize(window.innerWidth));

  useEffect(() => {
    setSize(getSize(window.innerWidth));
    const onResize = () => setSize(getSize(window.innerWidth));
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [getSize]);

  return size;
}
```

This eliminates the duplicate effect and properly lists `getSize` in deps.

Also add `useCallback` to the import on line 1:
```tsx
import { useEffect, useState, useRef, useCallback } from "react";
```

**Step 2: Fix isMobile to be reactive (line 53)**

Replace:
```tsx
const isMobile = window.innerWidth < 640;
```
With:
```tsx
const isMobile = widgetSize <= 120;
```

Since `widgetSize` is already reactive (from `useWidgetSize`) and the mobile size is 120px, we can derive `isMobile` from it instead of reading `window.innerWidth` directly during render. This avoids the non-reactive read and uses the already-updated state.

**Step 3: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 4: Commit**

```bash
git add front/src/components/ClaraMascot.tsx
git commit -m "fix: make ClaraMascot widget size and isMobile reactive to resize"
```

---

## Task 8: Make Mascot Keyboard Accessible

**Files:**
- Modify: `front/src/App.tsx:16-23`

**Step 1: Add tabIndex and keyboard handler**

Replace lines 16-23:
```tsx
      <div
        className={`fixed right-4 z-40 pointer-events-auto cursor-pointer hover:scale-105 transition-all duration-300 ${isChat ? "bottom-24" : "bottom-4"}`}
        onClick={() => { if (!isChat) navigate("/chat"); }}
        role={isChat ? undefined : "link"}
        aria-label={isChat ? undefined : "Abrir chat con Clara"}
        tabIndex={isChat ? undefined : 0}
        onKeyDown={(e) => { if (!isChat && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); navigate("/chat"); } }}
      >
```

**Step 2: Verify**

Run: `npx tsc -b`
Expected: No errors.

**Step 3: Commit**

```bash
git add front/src/App.tsx
git commit -m "fix: make mascot keyboard-focusable with Enter/Space navigation"
```

---

## Verification

After all tasks, run the full build:

```bash
cd front && npm run build
```

Expected: Clean build, no TypeScript errors, no Vite errors.

Then test manually:
1. `/nonexistent` redirects to `/`
2. Clara mascot is Tab-focusable on non-chat pages
3. Chat page loads without console errors (except CORS on TTS which is a backend issue)
4. Audio click feedback sounds play and don't leak contexts
5. Resize window — mascot size changes, mobile chat hides mascot

---

## Summary

| Task | Severity | Files | What |
|------|----------|-------|------|
| 1 | High | App.tsx | 404 catch-all route |
| 2 | High | ChatContent.tsx | useEffect deps (addWelcome, setMascotState) |
| 3 | High | MessageList.tsx | Side effect out of useMemo |
| 4 | Medium | ChatContent.tsx | Validate lang URL param |
| 5 | Medium | useAudioPlayer.ts, DocumentUpload.tsx | AudioContext leak |
| 6 | Medium | useChat.ts, VoiceRecorder.tsx | Unhandled promises |
| 7 | Medium | ClaraMascot.tsx | Reactive widget size + isMobile |
| 8 | Low | App.tsx | Keyboard accessibility for mascot |
