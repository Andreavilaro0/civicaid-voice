# Dark Mode Fix — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix dark mode to be accessible, beautiful, and usable for Clara's vulnerable audience (elderly 65+, immigrants, low-literacy users, visually impaired) while honoring the Civic Tenderness and Civic Meridians design philosophies.

**Architecture:** Replace the fragile CSS-only dark mode (scattered hardcoded hex values across 40+ locations) with a systematic, CSS-variable-driven dark theme controlled by a ThemeProvider. Add a manual toggle (elderly users often don't know about system dark mode settings). Adjust all brand colors for dark backgrounds to meet WCAG AAA. Apply anti-halation typography measures.

**Tech Stack:** React 19, Tailwind CSS v4.2 (@tailwindcss/vite), CSS custom properties, localStorage for persistence.

---

## Audit: Current Problems

| # | Problem | Impact | Files |
|---|---------|--------|-------|
| 1 | **No manual toggle** — relies solely on `prefers-color-scheme` media query | Elderly users can't control theme; shared devices force one preference | All — system-wide |
| 2 | **Brand colors FAIL on dark bg** — Clara Blue `#1B5E7B` has 2.38:1 contrast on `#0f1419` | Text using brand blue is invisible in dark mode | `globals.css`, all components using `text-clara-blue` |
| 3 | **40+ hardcoded hex values** — `dark:bg-[#0f1419]`, `dark:text-[#e8e8ee]` scattered across components | Impossible to maintain; inconsistent dark mode | Every component with `dark:` classes |
| 4 | **No anti-halation** — missing font-smoothing, no letter-spacing adjustment | White text bleeds/glows for users with astigmatism or aging eyes | `globals.css` |
| 5 | **Hero gradient hardcoded** — `from-clara-bg via-[#F0F7FA] to-[#E8F1F5]` | Hero section stays light-colored in dark mode | `HomePage.tsx:246` |
| 6 | **No surface elevation** — all cards use flat `#1a1f26` | No depth hierarchy; cards merge with background | `globals.css`, card components |
| 7 | **Stat numbers/counters hardcoded** — `.impact-counter { color: #1B5E7B }` | Invisible in dark mode (2.38:1 contrast) | `globals.css:271-273`, `globals.css:353-361` |
| 8 | **Before/after cells hardcoded** — rgba light-mode backgrounds | Barely visible cells in dark mode | `globals.css:248-264`, `globals.css:450-485` |
| 9 | **Decorative elements unchanged** — shadows use `rgba(27,94,123,0.06)` which is invisible on dark bg | Shadow/glow effects disappear | `globals.css:184-193` |
| 10 | **Footer link pills** — `color: #1B5E7B` fails contrast | Footer links unreadable | `globals.css:696-722` |

---

## Dark Mode Palette

### Design Philosophy Alignment

From **Civic Tenderness**: "Space is not empty — it breathes. Vast fields of soft ground establish a canvas of calm." In dark mode, the background must still breathe — never pure black (#000000), but a warm-cool dark that holds depth.

From **Civic Meridians**: "Deep, atmospheric darkness: not the darkness of absence, but of depth, the way a night sky holds infinite structure within apparent void." The dark background uses a blue-purple undertone (`#1A1A2E`) that evokes the night sky and institutional trust.

### Background & Surface Palette

| Token | Light | Dark | Purpose |
|-------|-------|------|---------|
| `--color-clara-bg` | `#FAFAFA` | `#1A1A2E` | Base background (warm-cool, institutional trust) |
| `--color-clara-surface-1` | `#F5F5F5` | `#20203A` | Navigation, sidebar |
| `--color-clara-card` | `#F5F5F5` | `#252542` | Cards, panels (2dp elevation) |
| `--color-clara-surface-3` | `#EEEEEE` | `#2C2C4D` | Dialogs, modals (3dp) |
| `--color-clara-border` | `#E0E0E0` | `#3A3A60` | Borders, separators |
| `--color-clara-info` | `#E3F2FD` | `#1E2A45` | Clara messages, info blocks |
| `--color-clara-hover` | `#F0F0F0` | `#3A3A60` | Hover/active states |

### Text Palette (Anti-Halation)

| Token | Light | Dark | Contrast on `#1A1A2E` | Notes |
|-------|-------|------|-----------------------|-------|
| `--color-clara-text` | `#1A1A2E` | `#EBEBEB` | 14.31:1 (AAA) | Off-white, NOT pure white (reduces halation) |
| `--color-clara-text-secondary` | `#4A4A5A` | `#B3B3B3` | 8.14:1 (AAA) | Labels, captions |
| Disabled | `#9E9E9E` | `#757575` | 3.70:1 | AA Large only |

### Brand Colors (Adjusted for Dark Mode)

Original brand colors FAIL accessibility on dark backgrounds. These adjusted variants maintain brand identity while meeting WCAG AAA (7:1+):

| Token | Light | Dark | Contrast on `#1A1A2E` | WCAG |
|-------|-------|------|-----------------------|------|
| `--color-clara-blue` | `#1B5E7B` | `#6BBFE0` | 8.25:1 | AAA |
| `--color-clara-orange` | `#D46A1E` | `#E8934E` | 7.08:1 | AAA |
| `--color-clara-green` | `#2E7D4F` | `#6EC08D` | 7.79:1 | AAA |
| `--color-clara-error` | `#C62828` | `#EF8A8A` | 7.04:1 | AAA |
| `--color-clara-warning` | `#F9A825` | `#F0C066` | 10.10:1 | AAA |

### Links

| State | Dark Color | Contrast | Treatment |
|-------|-----------|----------|-----------|
| Default | `#6CB4EE` | 7.64:1 (AAA) | Always underlined |
| Hover | `#7CC4F5` | 8.99:1 (AAA) | Underline thickens |
| Visited | `#9B8EC2` | 5.5:1 (AA) | Underlined, muted purple |

### Gradient Equivalents

| Context | Light | Dark |
|---------|-------|------|
| Hero section | `from-clara-bg via-[#F0F7FA] to-[#E8F1F5]` | `from-[#1A1A2E] via-[#1E2240] to-[#1A2545]` |
| Dark section | `from-[#0f1419] via-[#1B5E7B]/20 to-[#0f1419]` | `from-[#12122A] via-[#1B5E7B]/15 to-[#12122A]` |
| Step number | `from-[#1B5E7B] to-[#134a5f]` | `from-[#6BBFE0] to-[#5BB0D4]` (lighter in dark) |

---

## Implementation Tasks

### Task 1: Create ThemeProvider Context

**Files:**
- Create: `front/src/contexts/ThemeContext.tsx`
- Modify: `front/src/main.tsx`

**Step 1: Write the ThemeProvider**

```tsx
// front/src/contexts/ThemeContext.tsx
import { createContext, useContext, useEffect, useState, useCallback } from "react";

type Theme = "light" | "dark" | "system";

interface ThemeContextValue {
  theme: Theme;
  resolved: "light" | "dark";
  setTheme: (t: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: "system",
  resolved: "light",
  setTheme: () => {},
});

export function useTheme() {
  return useContext(ThemeContext);
}

function getSystemPreference(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    try {
      const stored = localStorage.getItem("clara-theme");
      if (stored === "light" || stored === "dark" || stored === "system") return stored;
    } catch { /* noop */ }
    return "system";
  });

  const [systemPref, setSystemPref] = useState<"light" | "dark">(getSystemPreference);
  const resolved = theme === "system" ? systemPref : theme;

  const setTheme = useCallback((t: Theme) => {
    setThemeState(t);
    try { localStorage.setItem("clara-theme", t); } catch { /* noop */ }
  }, []);

  // Listen to system preference changes
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => setSystemPref(e.matches ? "dark" : "light");
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  // Apply class to <html>
  useEffect(() => {
    const root = document.documentElement;
    if (resolved === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }, [resolved]);

  return (
    <ThemeContext.Provider value={{ theme, resolved, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

**Step 2: Wrap app in ThemeProvider**

In `front/src/main.tsx`, import and wrap:

```tsx
import { ThemeProvider } from "@/contexts/ThemeContext";

// Wrap <App /> with <ThemeProvider>
<ThemeProvider>
  <App />
</ThemeProvider>
```

**Step 3: Run dev server to verify no errors**

Run: `cd civicaid-voice/front && npm run dev`
Expected: App loads without errors, no visible change yet.

**Step 4: Commit**

```bash
git add front/src/contexts/ThemeContext.tsx front/src/main.tsx
git commit -m "feat: add ThemeProvider with system detection + localStorage persistence"
```

---

### Task 2: Rewrite CSS Variables for Dark Mode

**Files:**
- Modify: `front/src/globals.css` (lines 1-220, the theme and dark mode block)

Replace the current `@media (prefers-color-scheme: dark)` approach with class-based `.dark` selector, and add the new palette.

**Step 1: Update the `@theme inline` block and dark mode variables**

Replace the entire dark mode section in `globals.css` (lines 206-220):

```css
/* OLD: @media (prefers-color-scheme: dark) { ... } */
/* NEW: class-based dark mode */

/* ── Dark Mode (class-based: html.dark) ── */
.dark {
  --color-clara-bg: #1A1A2E;
  --color-clara-text: #EBEBEB;
  --color-clara-text-secondary: #B3B3B3;
  --color-clara-card: #252542;
  --color-clara-border: #3A3A60;
  --color-clara-info: #1E2A45;
  --color-clara-error: #EF8A8A;
  --color-clara-warning: #F0C066;
  --color-clara-blue: #6BBFE0;
  --color-clara-orange: #E8934E;
  --color-clara-green: #6EC08D;
  --color-clara-surface-1: #20203A;
  --color-clara-hover: #3A3A60;
  color-scheme: dark;
}
.dark body {
  background: var(--color-clara-bg);
  color: var(--color-clara-text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
/* Anti-halation: slightly increase letter-spacing in dark mode body text */
.dark p, .dark li, .dark dd {
  letter-spacing: 0.01em;
}
```

Add the new surface-1, hover tokens to the `@theme inline` block (light defaults):

```css
/* Inside @theme inline, add: */
--color-clara-surface-1: #F5F5F5;
--color-clara-hover: #F0F0F0;
```

**Step 2: Update all `@media (prefers-color-scheme: dark)` blocks to `.dark` selectors**

Search and replace throughout `globals.css`:
- `@media (prefers-color-scheme: dark) {` blocks for `.persona-chip`, `.quick-chip`, `.glass-card`, `.stat-card`, `.section-dark`, `.guarantee-badge`, `.footer-link-pill`, `.section-bleed-*` — change all to `.dark` class selectors.

For each block, the pattern is:
```css
/* OLD */
@media (prefers-color-scheme: dark) {
  .persona-chip { background: #1a1f26; }
}
/* NEW */
.dark .persona-chip { background: var(--color-clara-card); }
```

**Step 3: Add dark-mode-aware utility classes for hardcoded colors**

Replace hardcoded color values in CSS classes with CSS variables:

```css
/* stat numbers — use brand blue variable */
.impact-counter { color: var(--color-clara-blue); }
.impact-counter-lg { color: var(--color-clara-blue); }
.stat-number { color: var(--color-clara-blue); }

/* before/after cells */
.before-cell { background: rgba(from var(--color-clara-orange) r g b / 0.06); }
.after-cell { background: rgba(from var(--color-clara-green) r g b / 0.06); }
.before-cell strong { color: var(--color-clara-orange); }
.after-cell strong { color: var(--color-clara-green); }

/* footer link pills */
.footer-link-pill { color: var(--color-clara-blue); }

/* warm shadows — adapt for dark mode */
.dark .shadow-warm {
  box-shadow: 0 2px 20px rgba(0,0,0,0.3), 0 0 0 1px var(--color-clara-border);
}
.dark .shadow-warm-hover:hover {
  box-shadow: 0 8px 30px rgba(0,0,0,0.4), 0 0 0 1px var(--color-clara-border);
}
```

**Step 4: Run dev server, toggle dark class manually via DevTools**

Run: `cd civicaid-voice/front && npm run dev`
In DevTools: `document.documentElement.classList.add('dark')`
Expected: Background changes to `#1A1A2E`, text to `#EBEBEB`, brand colors lightened.

**Step 5: Commit**

```bash
git add front/src/globals.css
git commit -m "feat: rewrite dark mode from media-query to class-based with new accessible palette"
```

---

### Task 3: Remove Hardcoded `dark:` Classes from Components

**Files to modify (ALL `dark:` references must be removed/replaced):**

| File | dark: occurrences |
|------|-------------------|
| `front/src/pages/HomePage.tsx` | 4 |
| `front/src/pages/ComoUsarPage.tsx` | 12 |
| `front/src/pages/FuturoPage.tsx` | 10 |
| `front/src/pages/QuienesSomosPage.tsx` | 7 |
| `front/src/components/Header.tsx` | 7 |
| `front/src/components/ChatInput.tsx` | 3 |
| `front/src/components/ui/ChatBubble.tsx` | 3 |
| `front/src/components/ui/LoadingState.tsx` | 1 |
| `front/src/components/welcome/PlanSection.tsx` | 4 |
| `front/src/components/welcome/PromptBar.tsx` | 2 |
| `front/src/components/welcome/HamburgerMenu.tsx` | 6 |
| `front/src/components/welcome/SubPageLayout.tsx` | 3 |
| `front/src/components/welcome/GuideSection.tsx` | 5 |
| `front/src/components/welcome/PersonasSection.tsx` | 3 |
| `front/src/components/welcome/LanguageBar.tsx` | 2 |
| `front/src/components/welcome/FooterSection.tsx` | 2 |
| `front/src/components/welcome/SuggestionChips.tsx` | 3 |

**Strategy:** Since the CSS variables now automatically switch values in `.dark`, replace hardcoded `dark:` overrides with the semantic Tailwind classes that reference the CSS variables:

| Old Pattern | New Pattern |
|-------------|-------------|
| `bg-white dark:bg-[#0f1419]` | `bg-clara-bg` |
| `bg-white dark:bg-[#1a1f26]` | `bg-clara-card` |
| `dark:bg-[#0f1419]/80` | `bg-clara-bg/80` |
| `dark:bg-[#1a1f26]` | `bg-clara-card` |
| `dark:bg-[#141a20]` | `bg-clara-surface-1` |
| `dark:bg-[#2a2f36]` | `bg-clara-hover` |
| `text-clara-text dark:text-[#e8e8ee]` | `text-clara-text` (variable handles both) |
| `text-clara-text-secondary dark:text-[#a0a0b0]` | `text-clara-text-secondary` (variable handles both) |
| `border-clara-border dark:border-[#2a2f36]` | `border-clara-border` (variable handles both) |
| `dark:text-white/90` | `text-clara-text` |
| `dark:text-white/40` | `text-clara-text-secondary` |
| `dark:text-[#a0c4d4]` | `text-clara-blue` |

**Step 1: Process each file one at a time**

For each file listed above, remove all `dark:*` classes and replace the light-mode class with the semantic token class. Example for `Header.tsx`:

```tsx
// OLD:
className="sticky top-0 z-10 bg-white/80 dark:bg-[#0f1419]/80 backdrop-blur-lg border-b border-clara-border/50 dark:border-[#2a2f36]/50"

// NEW:
className="sticky top-0 z-10 bg-clara-bg/80 backdrop-blur-lg border-b border-clara-border/50"
```

**Step 2: Handle the Hero gradient in HomePage.tsx:246**

```tsx
// OLD:
className="... bg-gradient-to-b from-clara-bg via-[#F0F7FA] to-[#E8F1F5] ..."

// NEW — use a custom gradient class:
className="... bg-clara-bg hero-gradient ..."
```

Add to `globals.css`:
```css
.hero-gradient {
  background: linear-gradient(to bottom, var(--color-clara-bg), #F0F7FA, #E8F1F5);
}
.dark .hero-gradient {
  background: linear-gradient(to bottom, var(--color-clara-bg), #1E2240, #1A2545);
}
```

**Step 3: Handle the "section-dark" CTA in HomePage.tsx:376-377**

```tsx
// OLD:
className="section-viewport section-dark section-grain ... bg-gradient-to-b from-[#0f1419] via-[#1B5E7B]/20 to-[#0f1419] ..."

// NEW:
className="section-viewport section-dark section-grain ... bg-gradient-to-b from-[#0f1419] via-[#1B5E7B]/20 to-[#0f1419] ..."
// (this section is intentionally dark in both modes — keep as-is, it's designed to be dark)
```

**Step 4: Test each page in both modes**

Run: `cd civicaid-voice/front && npm run dev`
Visit each page: `/`, `/chat`, `/como-usar`, `/quienes-somos`, `/futuro`
Toggle: DevTools `document.documentElement.classList.toggle('dark')`
Expected: All text readable, no hardcoded colors remaining, all backgrounds adapt.

**Step 5: Commit**

```bash
git add -A front/src/
git commit -m "refactor: replace 40+ hardcoded dark: classes with semantic CSS variable tokens"
```

---

### Task 4: Build the Theme Toggle Component

**Files:**
- Create: `front/src/components/ui/ThemeToggle.tsx`
- Modify: `front/src/pages/HomePage.tsx` (header)
- Modify: `front/src/components/Header.tsx` (chat header)
- Modify: `front/src/components/welcome/HamburgerMenu.tsx`

**Step 1: Write the ThemeToggle component**

```tsx
// front/src/components/ui/ThemeToggle.tsx
import { useTheme } from "@/contexts/ThemeContext";

/**
 * Accessible theme toggle for elderly/low-literacy users.
 * Large touch target (48px), text label, visual preview swatches.
 */
export default function ThemeToggle() {
  const { theme, setTheme, resolved } = useTheme();

  const options: { value: "light" | "dark" | "system"; icon: string; label: string }[] = [
    { value: "light", icon: "\u2600", label: "Claro" },     // Sun
    { value: "dark", icon: "\u263E", label: "Oscuro" },      // Moon
    { value: "system", icon: "\u2699", label: "Auto" },      // Gear
  ];

  return (
    <div className="flex items-center gap-1 p-1 rounded-xl bg-clara-card border border-clara-border" role="radiogroup" aria-label="Tema visual">
      {options.map((opt) => (
        <button
          key={opt.value}
          role="radio"
          aria-checked={theme === opt.value}
          onClick={() => setTheme(opt.value)}
          className={`flex items-center gap-1 px-3 py-2 rounded-lg text-label font-medium transition-colors min-h-[44px]
            ${theme === opt.value
              ? "bg-clara-blue text-white"
              : "text-clara-text-secondary hover:bg-clara-hover"
            }`}
        >
          <span aria-hidden="true">{opt.icon}</span>
          <span>{opt.label}</span>
        </button>
      ))}
    </div>
  );
}
```

**Step 2: Add ThemeToggle to HamburgerMenu**

In `front/src/components/welcome/HamburgerMenu.tsx`, import and add above the nav links:

```tsx
import ThemeToggle from "@/components/ui/ThemeToggle";

// Inside the menu panel, before the nav links:
<div className="px-4 py-3 border-b border-clara-border">
  <ThemeToggle />
</div>
```

**Step 3: Add compact toggle to headers (optional: icon-only)**

In `Header.tsx` and `HomePage.tsx` header, add a small sun/moon button:

```tsx
import { useTheme } from "@/contexts/ThemeContext";

// Inside header:
const { resolved, setTheme } = useTheme();

<button
  onClick={() => setTheme(resolved === "dark" ? "light" : "dark")}
  aria-label={resolved === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
  className="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-clara-hover transition-colors"
>
  {resolved === "dark" ? "\u2600\uFE0F" : "\u263E"}
</button>
```

**Step 4: Test the toggle**

Run: `cd civicaid-voice/front && npm run dev`
Expected: Clicking toggles theme, persists on refresh, respects system preference when set to "Auto".

**Step 5: Commit**

```bash
git add front/src/components/ui/ThemeToggle.tsx front/src/components/welcome/HamburgerMenu.tsx front/src/components/Header.tsx front/src/pages/HomePage.tsx
git commit -m "feat: add accessible theme toggle (light/dark/auto) with 44px touch targets"
```

---

### Task 5: Fix Dark Mode Shadows, Glows, and Decorative Elements

**Files:**
- Modify: `front/src/globals.css`

**Step 1: Update shadow utilities for dark mode**

```css
/* Warm shadows — dark mode adaptations */
.dark .shadow-warm {
  box-shadow: 0 2px 20px rgba(0,0,0,0.3), 0 0 0 1px rgba(58,58,96,0.5);
}
.dark .shadow-warm-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.4), 0 0 0 1px rgba(58,58,96,0.5);
}

/* Glass card — dark mode */
.dark .glass-card {
  background: rgba(37,37,66,0.7);
  border: 1px solid rgba(58,58,96,0.5);
  box-shadow: 0 4px 24px rgba(0,0,0,0.3), 0 1px 0 rgba(58,58,96,0.3) inset;
}

/* Stat card — dark mode */
.dark .stat-card {
  background: rgba(37,37,66,0.6);
  border: 1px solid rgba(58,58,96,0.5);
}

/* Persona chip — dark mode */
.dark .persona-chip { background: var(--color-clara-card); }

/* Quick chip — dark mode */
.dark .quick-chip {
  background: var(--color-clara-card);
  border-color: var(--color-clara-border);
  color: var(--color-clara-blue);
}

/* Voice arcs — slightly more visible in dark mode */
.dark .voice-arc {
  border-color: rgba(107,191,224,0.12);
}

/* Guarantee badge — dark mode */
.dark .guarantee-badge {
  background: rgba(37,37,66,0.7);
  border: 1px solid rgba(58,58,96,0.5);
}

/* Glow dot — slightly brighter in dark */
.dark .glow-dot {
  background: var(--color-clara-orange);
  box-shadow: 0 0 16px rgba(232,147,78,0.5), 0 0 6px rgba(232,147,78,0.7);
}

/* Counter glow — use adjusted orange */
.dark .counter-glow {
  color: var(--color-clara-orange);
  text-shadow: 0 0 20px rgba(232,147,78,0.4), 0 0 60px rgba(232,147,78,0.15);
}

/* CTA headline glow — adjusted for dark */
.dark .cta-headline-glow {
  text-shadow: 0 0 10px rgba(107,191,224,0.5), 0 0 30px rgba(107,191,224,0.2);
}

/* Radar arcs — use adjusted blue */
.dark .radar-arc {
  border-color: rgba(107,191,224,0.12);
}

/* Step number mega — adjusted gradient */
.dark .step-number-mega {
  background: linear-gradient(135deg, var(--color-clara-blue), #5BB0D4);
  box-shadow: 0 4px 20px rgba(107,191,224,0.3), 0 0 40px rgba(107,191,224,0.1);
}

/* Section dark — adjusted for dark mode base */
.dark .section-dark { background: #1E2240; }

/* Section bleed gradients — dark mode */
.dark .section-bleed-dark-to-light::before {
  background: linear-gradient(to bottom, #1E2240, transparent);
}
.dark .section-bleed-light-to-dark::before {
  background: linear-gradient(to bottom, var(--color-clara-bg), transparent);
}

/* Footer link pills — dark mode */
.dark .footer-link-pill {
  background: rgba(107,191,224,0.1);
  color: var(--color-clara-blue);
}
.dark .footer-link-pill:hover {
  background: rgba(107,191,224,0.18);
}

/* Prompt bar focus — dark mode */
.dark .prompt-bar:focus-within {
  border-color: var(--color-clara-blue);
  box-shadow: 0 0 0 3px rgba(107,191,224,0.2), 0 2px 20px rgba(107,191,224,0.15);
}

/* Body grain overlay — reduce in dark mode */
.dark body::after { opacity: 0.015; }

/* Text gradient warm — dark mode */
.dark .text-gradient-warm {
  background: linear-gradient(135deg, var(--color-clara-blue) 0%, var(--color-clara-green) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**Step 2: Update before/after cells**

```css
/* Before/after cells — dark mode */
.dark .before-cell { background: rgba(232,147,78,0.08); }
.dark .after-cell { background: rgba(110,192,141,0.08); }
.dark .before-cell-enhanced { background: rgba(232,147,78,0.06); }
.dark .after-cell-enhanced { background: rgba(110,192,141,0.06); }
```

**Step 3: Test all sections in dark mode**

Run: `cd civicaid-voice/front && npm run dev`
Check: Shadows visible on dark bg, glow effects adapted, decorative elements subtle but present.

**Step 4: Commit**

```bash
git add front/src/globals.css
git commit -m "feat: adapt shadows, glows, and decorative elements for dark mode"
```

---

### Task 6: Fix Specific Page Dark Mode Issues

**Files:**
- Modify: `front/src/pages/HomePage.tsx`
- Modify: `front/src/components/welcome/ProblemSection.tsx`
- Modify: `front/src/components/welcome/GuideSection.tsx`
- Modify: `front/src/components/welcome/SuccessSection.tsx`
- Modify: `front/src/components/welcome/FooterSection.tsx`

**Step 1: Fix HomePage Hero gradient**

In `HomePage.tsx`, the hero section (line ~246) uses hardcoded gradient colors. Replace:

```tsx
// OLD:
className="... bg-gradient-to-b from-clara-bg via-[#F0F7FA] to-[#E8F1F5] ..."

// NEW:
className="... hero-gradient ..."
```

And the atmospheric decorative circles need dark mode adaptation:

```tsx
// OLD:
style={{ background: "radial-gradient(circle, rgba(27,94,123,0.04) 0%, transparent 70%)" }}

// NEW (both circles): Keep as-is — these are subtle enough at 3-4% opacity to work in both modes.
```

**Step 2: Fix FooterSection wave SVG fill**

In `FooterSection.tsx`, the wave SVG uses `text-white dark:text-[#1a1f26]`. Replace with:

```tsx
// OLD:
className="text-white dark:text-[#1a1f26]"

// NEW:
className="text-clara-card"
```

(Since `--color-clara-card` maps to `#F5F5F5` in light / `#252542` in dark, and the footer background is `bg-clara-card`, the wave should match.)

**Step 3: Fix GuideSection section background**

In `GuideSection.tsx:134`:
```tsx
// OLD:
className="... bg-[#F0F7FA] dark:bg-[#141a20] ..."

// NEW:
className="... bg-clara-surface-1 ..."
```

Add to `globals.css` `@theme inline`:
```css
--color-clara-surface-1: #F0F7FA;
```
And in `.dark`:
```css
--color-clara-surface-1: #20203A;
```

(NOTE: Reuse the same token — light value is `#F0F7FA` for these tinted sections, not `#F5F5F5`. Adjust the token or create a `--color-clara-surface-tinted`.)

Actually, a simpler approach: create a specific token:
```css
/* @theme inline */
--color-clara-bg-tinted: #F0F7FA;
/* .dark */
--color-clara-bg-tinted: #20203A;
```

Then use `bg-clara-bg-tinted` in GuideSection, PersonasSection's `bg-[#FAFAFA]`, and QuienesSomosPage's `bg-[#F0F7FA]`.

**Step 4: Test all pages end-to-end**

Visit each page in both light and dark mode:
- `/` — hero, problem, personas, guide, plan, success, CTA, footer
- `/chat` — header, messages, input
- `/como-usar` — all step cards
- `/quienes-somos` — team section, E-V-I section
- `/futuro` — roadmap cards

Expected: No hardcoded colors visible, all text readable, all backgrounds appropriate.

**Step 5: Commit**

```bash
git add -A front/src/
git commit -m "fix: page-specific dark mode issues (hero gradient, footer wave, section backgrounds)"
```

---

### Task 7: Add Tailwind `dark:` Variant Support via Class Strategy

**Files:**
- Modify: `front/src/globals.css` (Tailwind config)

Since this project uses Tailwind CSS v4.2 with `@tailwindcss/vite`, the dark mode strategy is configured via CSS, not a config file.

**Step 1: Add dark mode class strategy**

At the top of `globals.css`, after `@import "tailwindcss";`:

```css
@import "tailwindcss";

/* Enable class-based dark mode for Tailwind's dark: variant */
@custom-variant dark (&:where(.dark, .dark *));
```

This makes Tailwind's built-in `dark:` variant work with the `.dark` class on `<html>` instead of the media query.

**Step 2: Verify Tailwind dark: classes work**

Run: `cd civicaid-voice/front && npm run dev`
Add a test element: `<div className="bg-white dark:bg-red-500">Test</div>`
Toggle dark mode — should turn red.

**Step 3: Commit**

```bash
git add front/src/globals.css
git commit -m "feat: configure Tailwind v4.2 dark variant to use class strategy"
```

> **NOTE:** This task should be done BEFORE Task 3, since Task 3 may need some remaining `dark:` Tailwind classes for edge cases where CSS variables alone aren't sufficient (e.g., opacity modifiers). Reorder execution accordingly: **Task 7 -> Task 2 -> Task 3**.

---

### Task 8: Accessibility & Anti-Halation Typography in Dark Mode

**Files:**
- Modify: `front/src/globals.css`

**Step 1: Add font-smoothing for dark mode**

```css
.dark body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

(Already included in Task 2, verify it's present.)

**Step 2: Increase letter-spacing subtly in dark mode**

```css
.dark p, .dark li, .dark dd {
  letter-spacing: 0.01em;
}
```

(Already included in Task 2, verify it's present.)

**Step 3: Ensure font-weight >= 400 in dark mode**

Verify no component uses `font-light` or `font-thin` (weight 300/100). Search:

Run: `grep -r "font-light\|font-thin\|font-extralight" front/src/`
Expected: No matches. If any found, replace with `font-normal` (400) minimum.

**Step 4: Verify focus ring visibility in dark mode**

```css
.dark *:focus-visible {
  outline: 3px solid var(--color-clara-blue);
  outline-offset: 2px;
}
```

Since `--color-clara-blue` becomes `#6BBFE0` in dark mode (8.25:1 contrast on `#1A1A2E`), focus rings are highly visible.

**Step 5: Test with browser accessibility tools**

- Chrome DevTools > Rendering > Emulate vision deficiency > Blurred vision
- Chrome DevTools > Rendering > Emulate vision deficiency > Protanopia
- Chrome DevTools > Rendering > Emulate vision deficiency > Deuteranopia

Expected: All text readable, focus rings visible, no information conveyed by color alone.

**Step 6: Commit**

```bash
git add front/src/globals.css
git commit -m "feat: anti-halation typography and accessibility improvements for dark mode"
```

---

### Task 9: Final QA and Edge Cases

**Files:**
- Possibly modify: any file with remaining issues

**Step 1: Full visual audit in dark mode**

Open each page and check:
- [ ] Background transitions between sections are smooth (no jarring color jumps)
- [ ] All text meets 7:1 AAA contrast minimum
- [ ] Brand colors (blue, orange, green) are the lightened dark-mode variants
- [ ] Cards have visible borders/elevation
- [ ] Shadows are visible (adapted for dark backgrounds)
- [ ] Glow effects (counter, CTA, dots) are visible but not overwhelming
- [ ] SVG logo/icons are visible (strokes use brand colors that adapt)
- [ ] Form inputs (PromptBar, ChatInput) have visible borders
- [ ] Focus rings (Tab navigation) are bright and clear
- [ ] Animations still work (reduced-motion respected)
- [ ] RTL (Arabic) layout still correct in dark mode
- [ ] Footer wave seamlessly matches footer background

**Step 2: Test localStorage persistence**

1. Set theme to "dark", refresh page — should stay dark
2. Set theme to "light", refresh — should stay light
3. Set theme to "auto", change system preference — should follow system
4. Clear localStorage, refresh — should default to system preference

**Step 3: Test on mobile viewport**

Chrome DevTools > Device toolbar > iPhone 14 Pro / Galaxy S21
- Theme toggle accessible from hamburger menu
- Touch targets >= 44px for toggle buttons
- No horizontal scroll introduced

**Step 4: Fix any issues found**

Address any visual bugs discovered during QA.

**Step 5: Commit**

```bash
git add -A front/src/
git commit -m "fix: dark mode QA — edge cases and final polish"
```

---

## Recommended Execution Order

Due to dependencies, execute in this order:

1. **Task 1** — ThemeProvider (foundation)
2. **Task 7** — Tailwind dark variant config (needed before CSS/component changes)
3. **Task 2** — CSS variables rewrite (core palette)
4. **Task 5** — Dark shadows/glows/decorative (CSS completeness)
5. **Task 8** — Anti-halation typography (CSS completeness)
6. **Task 3** — Remove hardcoded `dark:` from components (biggest task)
7. **Task 6** — Page-specific fixes (gradients, waves, tinted sections)
8. **Task 4** — Theme toggle UI (user-facing)
9. **Task 9** — Final QA

---

## Color Reference Card

### Light Mode (unchanged)

```
Background:     #FAFAFA     Cards:     #F5F5F5     Borders:    #E0E0E0
Text:           #1A1A2E     Text 2:    #4A4A5A
Blue:           #1B5E7B     Orange:    #D46A1E     Green:      #2E7D4F
Error:          #C62828     Warning:   #F9A825     Info bg:    #E3F2FD
```

### Dark Mode (new)

```
Background:     #1A1A2E     Cards:     #252542     Borders:    #3A3A60
Text:           #EBEBEB     Text 2:    #B3B3B3
Blue:           #6BBFE0     Orange:    #E8934E     Green:      #6EC08D
Error:          #EF8A8A     Warning:   #F0C066     Info bg:    #1E2A45
Surface-1:      #20203A     Hover:     #3A3A60
```

### Contrast Ratios (Dark Mode, all on `#1A1A2E`)

| Element | Color | Ratio | WCAG |
|---------|-------|-------|------|
| Primary text | `#EBEBEB` | 14.31:1 | AAA |
| Secondary text | `#B3B3B3` | 8.14:1 | AAA |
| Clara Blue | `#6BBFE0` | 8.25:1 | AAA |
| Clara Orange | `#E8934E` | 7.08:1 | AAA |
| Clara Green | `#6EC08D` | 7.79:1 | AAA |
| Error | `#EF8A8A` | 7.04:1 | AAA |
| Warning | `#F0C066` | 10.10:1 | AAA |
| Links | `#6CB4EE` | 7.64:1 | AAA |

---

## Research Sources

- Smashing Magazine 2025: "Inclusive Dark Mode: Designing Accessible Dark Themes"
- Nielsen Norman Group: "Dark Mode vs Light Mode"
- IEEE VIS 2024: "Contrast Polarity and Age Groups"
- Material Design: "Dark Theme" (surface elevation system)
- UX Movement: "Why You Should Never Use Pure Black for Text or Backgrounds"
- BOIA: "Dark Mode Can Improve Text Readability — But Not for Everyone"
- Civic Tenderness Philosophy (internal): institutional warmth for vulnerable populations
- Civic Meridians Philosophy (internal): atmospheric darkness with luminous pathways
