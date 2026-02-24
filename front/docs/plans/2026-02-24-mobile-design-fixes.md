# Mobile Design Fixes — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix 9 design bugs found during Playwright mobile audit so the `/como-usar` page works flawlessly on phones (320px-430px).

**Architecture:** All fixes are CSS and component-level changes. No new dependencies. Parallel-safe: Tasks 1-5 touch different files and can run simultaneously. Tasks 6-7 depend on earlier tasks.

**Tech Stack:** React 19, Tailwind/CSS custom properties, Playwright for verification

---

## Task 1: Fix invisible content — `useInView` never triggers below fold

**Agent:** `agent-useInView` (general-purpose)

**Problem:** All sections below the hero start at `opacity: 0` via `useInView`. IntersectionObserver never fires because the elements are never scrolled into view during SSR/initial paint. Full-page screenshots show a 9000px blank page.

**Files:**
- Modify: `src/hooks/useInView.ts`

**Step 1: Read current file**

Read `src/hooks/useInView.ts` to understand the hook.

**Step 2: Fix the hook — check if element is already in viewport on mount**

Replace the entire file with:

```typescript
import { useEffect, useRef, useState } from "react";

/**
 * useInView — triggers once when element enters viewport.
 * Fixed: checks initial visibility on mount (covers elements already in view).
 */
export function useInView(threshold = 0.1) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Check if already in viewport (fixes below-fold content that
    // gets layout but observer hasn't fired yet)
    const rect = el.getBoundingClientRect();
    if (
      rect.top < window.innerHeight &&
      rect.bottom > 0
    ) {
      setVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold, rootMargin: "100px 0px" }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold]);

  return { ref, visible };
}
```

Key changes:
- Added `getBoundingClientRect()` check on mount — if the element is already visible, set `visible = true` immediately
- Added `rootMargin: "100px 0px"` — triggers 100px before element enters viewport, so content appears before user reaches it (eliminates "blank section" flash)

**Step 3: Verify**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 4: Commit**

```bash
git add src/hooks/useInView.ts
git commit -m "fix: useInView checks initial visibility + adds rootMargin for early trigger"
```

---

## Task 2: Fix touch targets — all buttons to 44px minimum height

**Agent:** `agent-touch-targets` (general-purpose)

**Problem:** 8 buttons have `minHeight: 40` (chips, "Intentar", "Habla con Clara"). WCAG 2.1 AA requires 44x44px minimum on mobile.

**Files:**
- Modify: `src/components/como-usar/BentoGrid.tsx` (lines 162, 190, 255)
- Modify: `src/components/como-usar/QuickHelpSection.tsx` (line with "Habla con Clara")

**Step 1: In `BentoGrid.tsx`, find all `minHeight: 40` and change to `minHeight: 44`**

There are 3 occurrences:
- Line 162: "Intentar" practice button — change `minHeight: 40` to `minHeight: 44`
- Line 190: chip buttons — change `minHeight: 40` to `minHeight: 44`
- Line 255: "Habla con Clara" card CTA — change `minHeight: 40` to `minHeight: 44`

Also bump padding from `8px 24px` / `8px 18px` to `10px 24px` / `10px 18px` to visually match the taller hit area.

**Step 2: In `QuickHelpSection.tsx`, check for any `minHeight: 40` or small button sizes**

The "Habla con Clara" button inside QuickHelpSection card has no explicit minHeight but relies on padding. No change needed if it renders > 44px.

**Step 3: Verify**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 4: Commit**

```bash
git add src/components/como-usar/BentoGrid.tsx
git commit -m "fix: increase touch targets to 44px minimum (WCAG 2.1 AA)"
```

---

## Task 3: Fix language bar overflow in SubPageLayout header

**Agent:** `agent-lang-bar` (general-purpose)

**Problem:** The `LanguageBar` in the SubPageLayout header overflows 200-452px right on mobile. The lang pills for PT, RO, CA, ZH, AR are completely off-screen. The header tries to fit: back button + title + theme toggle + 8 language pills in one row on 320px.

**Files:**
- Modify: `src/components/welcome/SubPageLayout.tsx` (header section, lines 28-53)

**Step 1: Read SubPageLayout.tsx**

Read the file to confirm current structure.

**Step 2: Fix the header — constrain language bar with `overflow-hidden` and `max-w`**

In SubPageLayout.tsx, change the header's right-side `div` to constrain the LanguageBar:

Replace:
```tsx
          <div className="flex items-center gap-1">
            <ThemeToggleCompact />
            <LanguageBar lang={lang} onChangeLang={setLang} />
          </div>
```

With:
```tsx
          <div className="flex items-center gap-1 min-w-0">
            <ThemeToggleCompact />
            <div className="overflow-hidden min-w-0 max-w-[180px] sm:max-w-[260px]">
              <LanguageBar lang={lang} onChangeLang={setLang} compact />
            </div>
          </div>
```

Key changes:
- Added `min-w-0` on parent to allow flex item to shrink
- Wrapped LanguageBar in a constrained `div` with `overflow-hidden` and `max-w`
- Added `compact` prop (already supported by LanguageBar — uses smaller pills)
- The language bar already has horizontal scroll via `overflow-x-auto`, so user can still scroll to see all languages — they just don't overflow the page

**Step 3: Also fix the page title wrapping — make it smaller on mobile**

Replace the `h1` element:

From:
```tsx
          <h1 className="font-display font-bold text-h2 text-clara-text text-center flex-1">
            {title}
          </h1>
```

To:
```tsx
          <h1 className="font-display font-bold text-clara-text text-center flex-1 truncate" style={{ fontSize: "clamp(16px, 4vw, 28px)" }}>
            {title}
          </h1>
```

Key changes:
- `text-h2` (28px fixed) replaced with `clamp(16px, 4vw, 28px)` — scales down on narrow screens
- Added `truncate` so it clips instead of wrapping to 3 lines

**Step 4: Verify**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 5: Commit**

```bash
git add src/components/welcome/SubPageLayout.tsx
git commit -m "fix: constrain language bar overflow + responsive header title"
```

---

## Task 4: Fix spline-viewer overflow

**Agent:** `agent-spline` (general-purpose)

**Problem:** The `spline-viewer` in `ClaraMascot.tsx` overflows right by 279px on all mobile devices. The parent container isn't clipping it.

**Files:**
- Modify: `src/components/ClaraMascot.tsx` (the outer wrapper div)

**Step 1: Read ClaraMascot.tsx**

Read the full file to understand the wrapper structure.

**Step 2: Add `overflow: hidden` to the outermost container**

Find the outermost wrapper `div` of ClaraMascot and add `overflow: "hidden"` to its style. The parent already has `pointerEvents: "none"`, so the overflow is purely visual.

Also ensure the wrapper has `maxWidth: "100%"` or `width: "100%"` to prevent it from expanding beyond the viewport.

**Step 3: Verify**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 4: Commit**

```bash
git add src/components/ClaraMascot.tsx
git commit -m "fix: clip spline-viewer overflow on mobile"
```

---

## Task 5: Fix floating dock overlapping hero buttons

**Agent:** `agent-dock` (general-purpose)

**Problem:** On iPhone SE / iPhone 14, the floating dock at the bottom of the screen covers the hero "Hablar con Clara" / "Ver la guia" buttons when the dock becomes visible (after 60vh scroll).

**Files:**
- Modify: `src/components/como-usar/FloatingDock.tsx` (scroll threshold)
- Modify: `src/globals.css` (dock bottom position on small screens)

**Step 1: Increase the scroll threshold from 60vh to 100vh**

In `FloatingDock.tsx`, change line 33:

From:
```typescript
      const threshold = window.innerHeight * 0.6;
```

To:
```typescript
      const threshold = window.innerHeight * 1.0;
```

This ensures the dock only appears after the user has scrolled past the entire hero viewport (where the CTA buttons live).

**Step 2: Add safe area padding for mobile notch/gesture bar**

In `src/globals.css`, update `.como-usar-dock`:

Add after `bottom: 24px;`:
```css
  bottom: max(24px, env(safe-area-inset-bottom, 0px) + 12px);
```

This prevents the dock from being hidden by iPhone gesture bars.

**Step 3: Verify**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 4: Commit**

```bash
git add src/components/como-usar/FloatingDock.tsx src/globals.css
git commit -m "fix: dock appears after full hero scroll + safe-area bottom"
```

---

## Task 6: Fix dark mode not respecting system preference

**Agent:** `agent-darkmode` (general-purpose)

**Problem:** The page doesn't activate dark mode when the OS is set to dark. The theme system uses localStorage/class-based toggle, but doesn't check `prefers-color-scheme` as fallback.

**Files:**
- Modify: `src/contexts/ThemeContext.tsx`

**Step 1: Read ThemeContext.tsx**

Read the full file to understand how the theme is resolved.

**Step 2: Ensure `prefers-color-scheme: dark` is used as initial default**

In the theme context, the initial state should check:
1. `localStorage.getItem("theme")` first (user preference)
2. `window.matchMedia("(prefers-color-scheme: dark)").matches` second (OS preference)
3. "light" as final fallback

If this logic is already present, the dark mode screenshots may have failed because Playwright's `emulateMedia` doesn't trigger the `matchMedia` listener that was already evaluated. In that case, this is a test issue, not a code issue. Verify by reading the file first.

**Step 3: Verify and commit if changes needed**

```bash
git add src/contexts/ThemeContext.tsx
git commit -m "fix: respect OS dark mode preference as default"
```

---

## Task 7: Fix language bar text at 11px

**Agent:** `agent-text-size` (general-purpose)

**Problem:** Language labels "ES", "FR", "عربي" render at 11px on mobile — below the 12px readability minimum. This is especially problematic for Arabic script.

**Files:**
- Modify: `src/components/welcome/LanguageBar.tsx` (compact mode font size)

**Step 1: In LanguageBar.tsx, find the compact mode font size**

Line 59: `"px-2.5 py-1.5 text-[13px]"` — this is the compact mode. But the audit shows 11px, which means the default compact styling is being computed smaller than declared due to viewport scaling or the non-compact mode has a similar issue.

**Step 2: Bump the compact font size from 13px to 14px**

Change:
```tsx
? "px-2.5 py-1.5 text-[13px]"
```
To:
```tsx
? "px-2.5 py-1.5 text-[14px]"
```

And ensure the short label `<span>` has a minimum font size:

Change:
```tsx
<span>{l.short}</span>
```
To:
```tsx
<span style={{ fontSize: "max(12px, 1em)" }}>{l.short}</span>
```

This guarantees the text never drops below 12px regardless of viewport scaling.

**Step 3: Verify**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 4: Commit**

```bash
git add src/components/welcome/LanguageBar.tsx
git commit -m "fix: language labels min 12px for mobile readability"
```

---

## Task 8: Run Playwright mobile audit to verify all fixes

**Agent:** `agent-verify` (general-purpose)

**Depends on:** Tasks 1-7 all complete

**Files:**
- Run: `e2e/mobile-audit.spec.ts`

**Step 1: Start dev server if not running**

```bash
npm run dev -- --port 5176
```

**Step 2: Run the audit tests**

```bash
npx playwright test e2e/mobile-audit.spec.ts --project=mobile --reporter=line
```

**Step 3: Read the audit report**

```bash
cat e2e/screenshots/audit-report.txt
```

**Step 4: Verify expected improvements**

- [ ] No horizontal overflow on any device
- [ ] No touch targets below 44x44px (except "Ir al contenido principal" skip link — that's a hidden skip link, OK)
- [ ] No text below 12px
- [ ] No elements overflowing right edge (lang-bar and spline-viewer fixed)
- [ ] No dock overlap with hero buttons
- [ ] Content visible in full-page screenshots (no blank sections)

**Step 5: Final commit**

```bash
git add -A
git commit -m "verify: mobile audit passes on all 5 devices"
```

---

## Parallel Execution Map

```
Tasks that can run simultaneously (no file conflicts):

  [Task 1: useInView]          -- src/hooks/useInView.ts
  [Task 2: touch targets]      -- src/components/como-usar/BentoGrid.tsx
  [Task 3: lang bar overflow]  -- src/components/welcome/SubPageLayout.tsx
  [Task 4: spline overflow]    -- src/components/ClaraMascot.tsx
  [Task 5: dock threshold]     -- src/components/como-usar/FloatingDock.tsx + globals.css
  [Task 6: dark mode]          -- src/contexts/ThemeContext.tsx
  [Task 7: text 11px]          -- src/components/welcome/LanguageBar.tsx

  All 7 tasks touch DIFFERENT files — fully parallelizable.

  [Task 8: verify]             -- depends on all 7 tasks complete
```
