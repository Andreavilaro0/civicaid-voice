# Dark Mode Visual Polish — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Elevate the dark mode from "functional" to "museum-quality" — fix all remaining visual issues (invisible elements, broken gradients, typography halation) and apply research-backed polish for the elderly/immigrant target audience.

**Architecture:** Pure CSS-first approach. All fixes use CSS custom properties that auto-switch via the existing `.dark` class system. No React state changes needed. Typography gets dark-mode-specific weight/spacing/line-height tuning. Decorative elements get theme-aware opacity and color overrides.

**Tech Stack:** CSS custom properties, Tailwind v4.2 `@custom-variant dark`, React inline styles with `var()` references, `useTheme()` hook for edge cases.

---

## Context & Research Summary

### Current State
The dark mode implementation (from `2026-02-23-dark-mode-fix.md`) established:
- Class-based `.dark` on `<html>` via ThemeProvider
- CSS variables for all brand colors with dark variants
- SVG stroke override rule: `.dark svg [stroke="#1B5E7B"] { stroke: #6BBFE0; }`
- Hover tokens: `--color-clara-blue-hover`, etc.

### Remaining Issues Found (Audit)
| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 3 | White gradient in PersonasSection, glass card in ProblemSection, Header data-URL SVG color |
| HIGH | 4 | Radial gradients invisible, floating arc RGBA colors, decorative elements lost |
| MEDIUM | 3 | Hardcoded Tailwind hex colors, border accent colors |
| LOW | 4 | Typography weight, letter-spacing, line-height, placeholder opacity |

### Research-Backed Improvements
From Apple HIG, Material Design 3, WCAG AAA, and accessibility research:

1. **Typography anti-halation:** Bump font-weight +50 in dark mode (400→450 body, 600→650 heading). Increase letter-spacing to `0.015em`. Increase line-height by +0.05.
2. **Surface elevation:** Add thin `1px solid rgba(255,255,255,0.06)` borders to cards for depth perception. Use inner top-edge highlight `inset 0 1px 0 0 rgba(255,255,255,0.05)`.
3. **Text color:** Current `#EBEBEB` is good. Consider `#E0E0E0` for body text (15.3:1 ratio, less halation) while keeping `#EBEBEB` for headings.
4. **Decorative elements:** Increase opacity 2-3x in dark mode (from 0.04→0.08-0.12). Use dark-palette colors, not light-mode colors.

### Design Philosophy Alignment
- **Civic Meridians:** "Deep atmospheric darkness... luminous lines trace pathways." Dark mode should feel like a night sky holding structure — not just inverted light mode.
- **Civic Tenderness:** "Screens held in trembling hands." Every element must be clearly visible, touchable, and warm.
- **Palette guidance:** Teal for digital pathways, amber for human moments, cool white for typographic clarity.

---

## Refined Dark Palette (v2)

| Token | Light | Dark v1 (current) | Dark v2 (this plan) | Rationale |
|-------|-------|-------------------|---------------------|-----------|
| `--color-clara-text` | `#1A1A2E` | `#EBEBEB` | `#E2E2E2` | Reduce halation: 15.6:1 still AAA, less blooming |
| `--color-clara-text-secondary` | `#4A4A5A` | `#B3B3B3` | `#A8A8B8` | Slightly cooler, matches blue-purple bg undertone |
| `--color-clara-card` | `#F5F5F5` | `#252542` | `#262648` | Slightly more blue tint for warmth (Civic Meridians depth) |
| `--color-clara-border` | `#E0E0E0` | `#3A3A60` | `#3A3A60` | Keep — works well |
| `--color-clara-info` | `#E3F2FD` | `#1E2A45` | `#1C2840` | Slightly deeper for Clara's bubbles |

---

## Tasks

### Task 1: Typography Dark Mode Refinements

**Files:**
- Modify: `front/src/globals.css` (dark mode section, ~lines 217-250)

**Step 1: Update dark text colors and add typography tokens**

In `front/src/globals.css`, update the `.dark` block:

```css
/* In .dark { ... } block, update these values: */
--color-clara-text: #E2E2E2;
--color-clara-text-secondary: #A8A8B8;
--color-clara-card: #262648;
--color-clara-info: #1C2840;
```

**Step 2: Enhance the anti-halation typography rules**

Replace the existing `.dark body` and `.dark p, .dark li, .dark dd` rules with:

```css
.dark body {
  background: var(--color-clara-bg);
  color: var(--color-clara-text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Anti-halation: slightly heavier weight + wider spacing in dark */
.dark p, .dark li, .dark dd, .dark span, .dark td {
  letter-spacing: 0.015em;
  font-weight: 450;
}

/* Headings: bump weight for dark mode readability */
.dark h1, .dark h2, .dark h3 {
  font-weight: 750;
  letter-spacing: -0.005em;
}

/* Line-height bump in dark mode for body text separation */
.dark p, .dark li {
  line-height: 1.65;
}
```

**Step 3: Verify in browser**

Open `http://localhost:5176/civicaid-voice/`, toggle to dark mode. Check that:
- Body text looks slightly heavier but not bold
- Headings are crisp without blooming
- Text doesn't "vibrate" against dark background
- Secondary text is readable but clearly secondary

**Step 4: Commit**

```bash
git add front/src/globals.css
git commit -m "style(dark): refine typography — anti-halation weight/spacing/line-height"
```

---

### Task 2: Card & Surface Elevation Polish

**Files:**
- Modify: `front/src/globals.css` (dark mode adaptations section, ~lines 1118-1230)

**Step 1: Add card elevation styles for dark mode**

Add after the existing `.dark .shadow-warm` rules:

```css
/* Card elevation — thin border + inner highlight for depth perception */
.dark .bg-clara-card,
.dark .persona-chip,
.dark [class*="bg-clara-card"] {
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.04),
    0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Surface-1 areas — subtle distinction */
.dark .bg-clara-surface-1 {
  border: 1px solid rgba(255, 255, 255, 0.03);
}

/* Persona chip — warm shadows in dark */
.dark .persona-chip {
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.05),
    0 2px 16px rgba(0, 0, 0, 0.35);
}
.dark .persona-chip:hover {
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.08),
    0 8px 24px rgba(0, 0, 0, 0.4);
}

/* Footer link pills — glow in dark */
.dark .footer-link-pill {
  border: 1px solid rgba(107, 191, 224, 0.08);
}
.dark .footer-link-pill:hover {
  border-color: rgba(107, 191, 224, 0.15);
  box-shadow: 0 0 12px rgba(107, 191, 224, 0.08);
}
```

**Step 2: Verify in browser**

Check cards on all pages. Cards should:
- Have a thin bright top-edge highlight (like light hitting from above)
- Have visible but subtle borders separating them from the background
- Persona chips should float with warm depth
- Footer pills should have a subtle blue glow on hover

**Step 3: Commit**

```bash
git add front/src/globals.css
git commit -m "style(dark): add card elevation — thin borders, inner highlights, warm shadows"
```

---

### Task 3: Fix PersonasSection White Gradient (CRITICAL)

**Files:**
- Modify: `front/src/components/welcome/PersonasSection.tsx` (~line 358)

**Step 1: Read the file and find the white gradient**

The issue is a hardcoded `white` in a linear-gradient inside persona card avatars:

```tsx
style={{ background: `linear-gradient(135deg, white 0%, ${colors.glow} 100%)` }}
```

**Step 2: Replace with CSS variable**

Change to:
```tsx
style={{ background: `linear-gradient(135deg, var(--color-clara-card) 0%, ${colors.glow} 100%)` }}
```

This uses `--color-clara-card` which is `#F5F5F5` in light mode and `#262648` in dark — creating an appropriate gradient base for both themes.

**Step 3: Also check the floating arc SVGs** (~lines 177-179, 212-220)

These use hardcoded `rgba(27,94,123,...)` and `rgba(212,106,30,...)`. The CSS global rule `.dark svg [stroke="#1B5E7B"]` won't catch rgba values.

Add to `globals.css`:
```css
/* PersonasSection decorative arcs — more visible in dark */
.dark .persona-arc-blue circle { stroke: rgba(107, 191, 224, 0.18); }
.dark .persona-arc-orange circle { stroke: rgba(232, 147, 78, 0.14); }
```

Then add `className="persona-arc-blue"` and `className="persona-arc-orange"` to the respective SVG wrappers in PersonasSection.tsx.

**Step 4: Verify**

Check PersonasSection in dark mode. Avatar gradient backgrounds should blend with the card. Decorative arcs should be subtly visible.

**Step 5: Commit**

```bash
git add front/src/components/welcome/PersonasSection.tsx front/src/globals.css
git commit -m "fix(dark): PersonasSection — theme-aware gradient + decorative arcs"
```

---

### Task 4: Fix ProblemSection Glass Cards (CRITICAL)

**Files:**
- Modify: `front/src/components/welcome/ProblemSection.tsx` (~lines 177-182, 198-199, 231)

**Step 1: Read the file and identify all hardcoded colors**

Key issues:
1. Glass card background: `rgba(255,255,255,0.07)` — designed for dark section only, but should use theme-aware values
2. Glass card border: `rgba(255,255,255,0.12)` — same issue
3. Accent borders: `3px solid #D46A1E` and `3px solid #2E7D4F` — should use CSS variables
4. Voice arc SVG borders: `rgba(212,106,30,...)` colors

**Step 2: Fix accent border colors**

Replace:
```tsx
borderLeft: isRTL ? "none" : "3px solid #D46A1E"
```
With:
```tsx
borderLeft: isRTL ? "none" : "3px solid var(--color-clara-orange)"
```

And:
```tsx
borderLeft: isRTL ? "none" : "3px solid #2E7D4F"
```
With:
```tsx
borderLeft: isRTL ? "none" : "3px solid var(--color-clara-green)"
```

**Step 3: Fix the radial gradient background** (~line 66)

Replace:
```tsx
background: "radial-gradient(circle, rgba(212,106,30,0.03) 0%, transparent 70%)"
```
With:
```tsx
background: "radial-gradient(circle, rgba(var(--clara-orange-rgb, 212,106,30), 0.06) 0%, transparent 70%)"
```

Note: Since CSS `rgba()` with custom properties needs the raw RGB values, add these to `globals.css`:
```css
:root {
  --clara-blue-rgb: 27, 94, 123;
  --clara-orange-rgb: 212, 106, 30;
  --clara-green-rgb: 46, 125, 79;
}
.dark {
  --clara-blue-rgb: 107, 191, 224;
  --clara-orange-rgb: 232, 147, 78;
  --clara-green-rgb: 110, 192, 141;
}
```

**Step 4: Verify in browser**

ProblemSection should show:
- Accent borders using theme-appropriate brand colors
- Radial background gradient subtly visible in both modes
- Glass cards properly styled

**Step 5: Commit**

```bash
git add front/src/components/welcome/ProblemSection.tsx front/src/globals.css
git commit -m "fix(dark): ProblemSection — theme-aware borders, gradients, glass cards"
```

---

### Task 5: Fix Header Data-URL SVG Color (CRITICAL)

**Files:**
- Modify: `front/src/components/Header.tsx` (~line 56)

**Step 1: Read the file and find the data URL**

The issue is an SVG chevron in a `<select>` element with hardcoded `%234A4A5A` (which is `#4A4A5A` — the light mode secondary text color). In dark mode, this is invisible.

**Step 2: Replace with a React component approach**

Instead of a data URL, wrap the `<select>` in a container with a visible SVG chevron that uses `currentColor`:

```tsx
<div className="relative">
  <select
    /* ... existing props ... */
    style={{
      /* remove the backgroundImage property */
      appearance: "none",
      /* keep other styles */
    }}
  >
    {/* ... options ... */}
  </select>
  <svg
    className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-clara-text-secondary"
    width="16" height="16" viewBox="0 0 24 24"
    fill="none" stroke="currentColor" strokeWidth="2.5"
    strokeLinecap="round" strokeLinejoin="round"
    aria-hidden="true"
  >
    <polyline points="6 9 12 15 18 9" />
  </svg>
</div>
```

By using `currentColor` and `text-clara-text-secondary`, the chevron automatically adapts to dark mode via the CSS variable system.

**Step 3: Verify**

The language selector dropdown in the header should show a visible chevron in both light and dark mode.

**Step 4: Commit**

```bash
git add front/src/components/Header.tsx
git commit -m "fix(dark): Header dropdown chevron — use currentColor instead of data-URL hex"
```

---

### Task 6: Fix Decorative Radial Gradients (HIGH)

**Files:**
- Modify: `front/src/pages/HomePage.tsx` (~lines 250, 252)
- Modify: `front/src/globals.css`

**Step 1: Add RGB token variables to globals.css**

(If not already done in Task 4, add the `--clara-blue-rgb` / `--clara-orange-rgb` tokens to `:root` and `.dark` blocks.)

**Step 2: Fix HomePage radial gradients**

Replace:
```tsx
style={{ background: "radial-gradient(circle, rgba(27,94,123,0.04) 0%, transparent 70%)" }}
```
With:
```tsx
style={{ background: "radial-gradient(circle, rgba(var(--clara-blue-rgb), 0.06) 0%, transparent 70%)" }}
```

And:
```tsx
style={{ background: "radial-gradient(circle, rgba(212,106,30,0.03) 0%, transparent 70%)" }}
```
With:
```tsx
style={{ background: "radial-gradient(circle, rgba(var(--clara-orange-rgb), 0.05) 0%, transparent 70%)" }}
```

Note: Slightly higher opacity (0.04→0.06, 0.03→0.05) because dark mode radial gradients need more intensity to be visible.

**Step 3: Verify**

In dark mode, the decorative background blobs on the home page hero section should be subtly visible — teal and amber halos consistent with Civic Meridians philosophy.

**Step 4: Commit**

```bash
git add front/src/pages/HomePage.tsx front/src/globals.css
git commit -m "fix(dark): decorative radial gradients — theme-aware RGB tokens"
```

---

### Task 7: Fix PersonasSection Floating Arc RGBA Colors (HIGH)

**Files:**
- Modify: `front/src/components/welcome/PersonasSection.tsx` (~lines 177-179, 212-220)

**Step 1: Replace hardcoded RGBA with variable-based RGBA**

For the blue arc SVG (~line 177-179), change:
```tsx
stroke="rgba(27,94,123,0.18)"
```
To:
```tsx
stroke={`rgba(var(--clara-blue-rgb), 0.18)`}
```

Wait — SVG attributes don't resolve CSS `var()`. Instead, use inline `style`:

```tsx
<circle cx="40" cy="40" r="35" fill="none" strokeWidth="1"
  style={{ stroke: `rgba(var(--clara-blue-rgb), 0.18)` }} />
```

Actually, SVG inline styles DO resolve CSS custom properties. So change from `stroke=` attribute to `style={{ stroke: }}` for all decorative arcs.

For the orange arc SVG (~lines 212-220), change similarly:
```tsx
style={{ stroke: `rgba(var(--clara-orange-rgb), 0.14)` }}
```

**Step 2: Verify**

The floating decorative arcs in PersonasSection should be subtly visible in both light and dark modes, using the appropriate palette colors.

**Step 3: Commit**

```bash
git add front/src/components/welcome/PersonasSection.tsx
git commit -m "fix(dark): PersonasSection floating arcs — CSS variable RGBA strokes"
```

---

### Task 8: Fix Remaining Hardcoded Colors (MEDIUM)

**Files:**
- Modify: `front/src/components/welcome/GuideSection.tsx` (~line 27, 49)
- Modify: `front/src/components/welcome/SuccessSection.tsx` (SVG strokes)

**Step 1: Fix GuideSection strokeColor logic**

Line 27:
```tsx
const strokeColor = fill >= 0.85 ? "#2E7D4F" : "#1B5E7B";
```

Replace with:
```tsx
const strokeColor = fill >= 0.85
  ? "var(--color-clara-green)"
  : "var(--color-clara-blue)";
```

Line 49:
```tsx
className="text-[#1B5E7B]/10"
```

Replace with:
```tsx
className="text-clara-blue/10"
```

**Step 2: Fix SuccessSection SVG strokes**

Lines 54-55 and 73-74 have hardcoded `stroke="#1B5E7B"` and `stroke="#2E7D4F"` in decorative SVGs. These SHOULD already be caught by the global CSS rule `.dark svg [stroke="#1B5E7B"] { stroke: #6BBFE0; }` — but verify this works. If the SVGs use inline `stroke` attributes, the CSS attribute selector should match them.

Also fix the `stroke="#D46A1E"` instances in lines 73-74.

**Step 3: Verify**

Check GuideSection stat rings and SuccessSection decorative circles in dark mode. All should use the dark palette blues/greens.

**Step 4: Commit**

```bash
git add front/src/components/welcome/GuideSection.tsx front/src/components/welcome/SuccessSection.tsx
git commit -m "fix(dark): GuideSection + SuccessSection — CSS variable colors"
```

---

### Task 9: Final Visual Polish & QA

**Files:**
- Modify: `front/src/globals.css` (various small tweaks)

**Step 1: Improve placeholder text visibility**

```css
/* Placeholder text — slightly more visible in dark mode */
.dark ::placeholder {
  color: var(--color-clara-text-secondary);
  opacity: 0.55;
}
```

**Step 2: Improve section transitions**

The existing `.section-bleed-light-to-dark::before` and `.section-bleed-dark-to-light::before` gradients use hardcoded colors. Update:

```css
.section-bleed-light-to-dark::before {
  background: linear-gradient(to bottom, var(--color-clara-bg), transparent);
}
/* Remove the separate .dark override — the var() handles it automatically */
```

**Step 3: Add subtle body background texture for dark mode**

Civic Meridians describes "depth, the way a night sky holds infinite structure." Add a very subtle radial gradient to the body:

```css
.dark body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(107, 191, 224, 0.03) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(232, 147, 78, 0.02) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}
```

This adds an almost-imperceptible teal and amber atmospheric glow — the "luminous pathways" of Civic Meridians.

**Step 4: Run full build verification**

```bash
cd front && npx tsc --noEmit && npx vite build
```

Expected: 0 TypeScript errors, clean Vite build.

**Step 5: Visual QA checklist**

Open every page in both light and dark mode and verify:
- [ ] **HomePage hero**: gradient, mic button, typography all correct
- [ ] **PersonasSection**: cards, avatars, floating arcs visible
- [ ] **GuideSection**: stat rings, progress bars, decorative elements
- [ ] **ProblemSection**: glass cards, accent borders, voice arcs
- [ ] **SuccessSection**: before/after cards, quote, decorative circles
- [ ] **PlanSection**: decorative arcs visible
- [ ] **FooterSection**: wave SVG, link pills, logo
- [ ] **ComoUsarPage**: illustrations, step badges, gradients
- [ ] **FuturoPage**: status badges, CTA
- [ ] **QuienesSomosPage**: team cards, ClaraArcs
- [ ] **Header**: language selector dropdown chevron visible
- [ ] **HamburgerMenu**: theme toggle (Light/Dark/Auto), link colors
- [ ] **ChatInput**: border, send button, placeholder
- [ ] **ChatBubble**: Clara vs user bubbles distinguishable
- [ ] **VoiceRecorder**: mic button, timer, wave animation, cancel/send buttons
- [ ] **ThemeToggle**: sun/moon icon transitions correctly

**Step 6: Commit**

```bash
git add front/src/globals.css
git commit -m "style(dark): final polish — placeholders, section transitions, atmospheric depth"
```

---

## Execution Order & Dependencies

```
Task 1 (Typography)         ─┐
Task 2 (Card Elevation)      ├─ Independent, do in parallel
Task 5 (Header Chevron)     ─┘
        │
Task 4 (ProblemSection)     ─┐ Depends on Task 4 for RGB tokens
Task 3 (PersonasSection)     ├─ in globals.css
Task 6 (Radial Gradients)    │
Task 7 (PersonasSection Arcs)┘
        │
Task 8 (Remaining Colors)   ─── Cleanup
        │
Task 9 (Final Polish + QA)  ─── Must be last
```

**Estimated total time:** 3-4 hours with subagent-driven approach.
