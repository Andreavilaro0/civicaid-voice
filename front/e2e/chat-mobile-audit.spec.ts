import { test, devices, type BrowserContext, type Page } from "@playwright/test";
import * as fs from "fs";

const BASE = "http://localhost:5176/civicaid-voice/chat?lang=es";
const SS = "e2e/screenshots";
const REPORT_PATH = `${SS}/chat-audit-report.txt`;

const MOBILE_DEVICES = [
  { name: "iPhone-SE", config: devices["iPhone SE"], width: 320, height: 568 },
  { name: "iPhone-14", config: devices["iPhone 14"], width: 390, height: 844 },
  { name: "Pixel-5", config: devices["Pixel 5"], width: 393, height: 851 },
];

/* ── Helper: append lines to the shared report file ── */
function appendReport(lines: string[]) {
  fs.mkdirSync(SS, { recursive: true });
  fs.appendFileSync(REPORT_PATH, lines.join("\n") + "\n", "utf-8");
}

/* ── Clear previous report at startup ── */
test.beforeAll(async () => {
  fs.mkdirSync(SS, { recursive: true });
  fs.writeFileSync(
    REPORT_PATH,
    `CHAT PAGE MOBILE AUDIT\nGenerated: ${new Date().toISOString()}\nURL: ${BASE}\n`,
    "utf-8"
  );
});

/* ── Configure serial execution so report doesn't interleave ── */
test.describe.configure({ mode: "serial" });

for (const device of MOBILE_DEVICES) {
  test.describe(`Chat Mobile Audit — ${device.name}`, () => {
    let context: BrowserContext;
    let page: Page;

    test.beforeEach(async ({ browser }) => {
      context = await browser.newContext({
        viewport: device.config.viewport,
        userAgent: device.config.userAgent,
        deviceScaleFactor: device.config.deviceScaleFactor,
        isMobile: device.config.isMobile,
        hasTouch: device.config.hasTouch,
      });
      page = await context.newPage();
    });

    test.afterEach(async () => {
      await page?.close();
      await context?.close();
    });

    /* ------------------------------------------------------------------ */
    /*  1. Hero viewport — initial chat page load                         */
    /* ------------------------------------------------------------------ */
    test(`initial load screenshot — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(2000);
      await page.screenshot({
        path: `${SS}/chat-${device.name}-initial-load.png`,
      });
    });

    /* ------------------------------------------------------------------ */
    /*  2. Chat input area                                                 */
    /* ------------------------------------------------------------------ */
    test(`chat input area screenshot — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1500);

      const chatInput = page.locator("input[type='text']").first();
      if (await chatInput.count()) {
        await chatInput.scrollIntoViewIfNeeded();
        await page.waitForTimeout(500);
      }

      await page.screenshot({
        path: `${SS}/chat-${device.name}-input-area.png`,
      });
    });

    /* ------------------------------------------------------------------ */
    /*  3. Type a message and capture the response area                    */
    /* ------------------------------------------------------------------ */
    test(`message and response area — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(2000);

      const chatInput = page.locator("input[type='text']").first();
      if (await chatInput.count()) {
        await chatInput.fill("Hola, necesito ayuda con el empadronamiento");
        await page.waitForTimeout(500);

        await page.screenshot({
          path: `${SS}/chat-${device.name}-typed-message.png`,
        });

        // Submit the message
        const sendBtn = page.locator("button[type='submit']");
        if (await sendBtn.count()) {
          await sendBtn.click();
        } else {
          await chatInput.press("Enter");
        }

        // Wait for response or loading state
        await page.waitForTimeout(4000);

        await page.screenshot({
          path: `${SS}/chat-${device.name}-response-area.png`,
        });
      }
    });

    /* ------------------------------------------------------------------ */
    /*  4. Dark mode version                                               */
    /* ------------------------------------------------------------------ */
    test(`dark mode screenshot — ${device.name}`, async () => {
      await page.emulateMedia({ colorScheme: "dark" });
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1500);

      // Toggle dark mode via theme button
      const themeToggle = page.locator(
        '[aria-label*="theme"], [aria-label*="modo"], [aria-label*="dark"], [aria-label*="oscuro"]'
      );
      if (await themeToggle.count()) {
        await themeToggle.first().click();
        await page.waitForTimeout(800);
      }

      await page.screenshot({
        path: `${SS}/chat-${device.name}-dark-mode.png`,
      });

      // Also capture input area in dark mode
      const chatInput = page.locator("input[type='text']").first();
      if (await chatInput.count()) {
        await chatInput.fill("Pregunta de prueba en modo oscuro");
        await page.waitForTimeout(500);
      }

      await page.screenshot({
        path: `${SS}/chat-${device.name}-dark-mode-input.png`,
      });
    });

    /* ------------------------------------------------------------------ */
    /*  5. Full automated audit: all checks + report                       */
    /* ------------------------------------------------------------------ */
    test(`automated audit checks — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(2500);

      const vw = device.config.viewport?.width ?? device.width;
      const vh = device.config.viewport?.height ?? device.height;
      const lines: string[] = [];

      lines.push(`\n${"=".repeat(70)}`);
      lines.push(`CHAT MOBILE AUDIT: ${device.name} (${vw}x${vh})`);
      lines.push(`${"=".repeat(70)}`);

      /* ── A. Horizontal overflow ── */
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
      const hasHorizontalOverflow = scrollWidth > clientWidth;
      lines.push(`\n## A. Horizontal Overflow`);
      lines.push(
        hasHorizontalOverflow
          ? `  !! FAIL — Page scrolls horizontally (scrollWidth: ${scrollWidth}px vs clientWidth: ${clientWidth}px)`
          : `  PASS — No horizontal overflow`
      );

      /* ── B. Touch targets below 44x44px ── */
      const smallButtons = await page.evaluate(() => {
        const els = document.querySelectorAll(
          "button, a, [role='button'], [role='option'], input, textarea"
        );
        const issues: string[] = [];
        els.forEach((el) => {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            if (rect.width < 44 || rect.height < 44) {
              const text =
                (el as HTMLElement).innerText?.trim().slice(0, 40) ||
                el.getAttribute("aria-label")?.slice(0, 40) ||
                el.tagName;
              issues.push(
                `"${text}" — ${Math.round(rect.width)}x${Math.round(rect.height)}px (minimum 44x44)`
              );
            }
          }
        });
        return issues;
      });
      lines.push(`\n## B. Touch Targets Below 44x44px (WCAG 2.5.8)`);
      if (smallButtons.length) {
        smallButtons.forEach((b) => lines.push(`  - ${b}`));
      } else {
        lines.push(`  PASS — All touch targets meet 44x44px minimum`);
      }

      /* ── C. Text below 12px ── */
      const smallText = await page.evaluate(() => {
        const all = document.querySelectorAll("*");
        const issues: string[] = [];
        const seen = new Set<string>();
        all.forEach((el) => {
          const style = window.getComputedStyle(el);
          const fontSize = parseFloat(style.fontSize);
          const text = el.textContent?.trim() || "";
          if (fontSize > 0 && fontSize < 12 && text.length > 0) {
            const sample = text.slice(0, 50);
            const key = `${fontSize}-${sample}`;
            if (!seen.has(key)) {
              seen.add(key);
              issues.push(
                `${fontSize}px: "${sample}" (element: ${el.tagName.toLowerCase()}.${el.className?.toString().slice(0, 30) || ""})`
              );
            }
          }
        });
        return issues;
      });
      lines.push(`\n## C. Text Below 12px (readability risk)`);
      if (smallText.length) {
        smallText.forEach((t) => lines.push(`  - ${t}`));
      } else {
        lines.push(`  PASS — No text below 12px found`);
      }

      /* ── D. Elements overflowing viewport edges ── */
      const overflowIssues = await page.evaluate(() => {
        const issues: string[] = [];
        const all = document.querySelectorAll("*");
        const vw = window.innerWidth;
        all.forEach((el) => {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0) {
            if (rect.right > vw + 2) {
              const tag = el.tagName.toLowerCase();
              const cls = el.className?.toString().slice(0, 50) || "";
              issues.push(
                `${tag}.${cls} overflows RIGHT by ${Math.round(rect.right - vw)}px`
              );
            }
            if (rect.left < -2) {
              const tag = el.tagName.toLowerCase();
              const cls = el.className?.toString().slice(0, 50) || "";
              issues.push(
                `${tag}.${cls} overflows LEFT by ${Math.round(Math.abs(rect.left))}px`
              );
            }
          }
        });
        return [...new Set(issues)].slice(0, 25);
      });
      lines.push(`\n## D. Elements Overflowing Viewport Edges`);
      if (overflowIssues.length) {
        overflowIssues.forEach((o) => lines.push(`  - ${o}`));
      } else {
        lines.push(`  PASS — No elements overflowing viewport`);
      }

      /* ── E. Input field usability ── */
      const inputUsability = await page.evaluate(() => {
        const input = document.querySelector("input[type='text']") as HTMLInputElement;
        if (!input) return { found: false, issues: ["No text input found on the page"], rect: null, fontSize: 0 };

        const rect = input.getBoundingClientRect();
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const issues: string[] = [];

        if (rect.height === 0 || rect.width === 0) {
          issues.push("Input has zero dimensions — not rendered");
        }
        if (rect.bottom > vh) {
          issues.push(
            `Input is below viewport fold by ${Math.round(rect.bottom - vh)}px — may be unreachable without scrolling`
          );
        }
        const keyboardZone = vh * 0.6;
        if (rect.top > keyboardZone) {
          issues.push(
            `Input is at ${Math.round(rect.top)}px from top — when keyboard opens (~${Math.round(vh * 0.4)}px high), it may be covered`
          );
        }
        if (rect.width < vw * 0.5) {
          issues.push(
            `Input width is only ${Math.round(rect.width)}px (${Math.round((rect.width / vw) * 100)}% of viewport) — may be cramped`
          );
        }

        const style = window.getComputedStyle(input);
        const fontSize = parseFloat(style.fontSize);
        if (fontSize < 16) {
          issues.push(
            `Input font-size is ${fontSize}px — iOS will auto-zoom on focus (must be >= 16px)`
          );
        }

        const paddingLeft = parseFloat(style.paddingLeft);
        const paddingRight = parseFloat(style.paddingRight);
        if (paddingLeft < 8 || paddingRight < 8) {
          issues.push(
            `Input padding too small (L: ${paddingLeft}px, R: ${paddingRight}px) — text may appear cramped`
          );
        }

        return {
          found: true,
          rect: {
            top: Math.round(rect.top),
            bottom: Math.round(rect.bottom),
            left: Math.round(rect.left),
            right: Math.round(rect.right),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          },
          fontSize,
          issues,
        };
      });
      lines.push(`\n## E. Input Field Usability`);
      if (!inputUsability.found) {
        lines.push(`  !! FAIL — No text input found`);
      } else {
        const r = inputUsability.rect!;
        lines.push(
          `  Position: top=${r.top}px, bottom=${r.bottom}px, width=${r.width}px, height=${r.height}px`
        );
        lines.push(`  Font size: ${inputUsability.fontSize}px`);
        if (inputUsability.issues.length) {
          inputUsability.issues.forEach((i) => lines.push(`  - !! ${i}`));
        } else {
          lines.push(`  PASS — Input is reachable and usable`);
        }
      }

      /* ── F. Chat bubble text readability ── */
      const bubbleReadability = await page.evaluate(() => {
        const bubbles = document.querySelectorAll('[role="article"]');
        const issues: string[] = [];
        const info: string[] = [];

        bubbles.forEach((bubble, idx) => {
          const rect = bubble.getBoundingClientRect();
          const style = window.getComputedStyle(bubble);
          const fontSize = parseFloat(style.fontSize);
          const lineHeight = parseFloat(style.lineHeight);
          const vw = window.innerWidth;

          info.push(
            `Bubble ${idx + 1}: width=${Math.round(rect.width)}px (${Math.round((rect.width / vw) * 100)}% of vw), fontSize=${fontSize}px, lineHeight=${lineHeight}px`
          );

          if (rect.width > vw * 0.92) {
            issues.push(
              `Bubble ${idx + 1} is too wide (${Math.round(rect.width)}px = ${Math.round((rect.width / vw) * 100)}% of viewport) — may feel cramped`
            );
          }

          const texts = bubble.querySelectorAll("p, span, div");
          texts.forEach((t) => {
            const tStyle = window.getComputedStyle(t);
            const tSize = parseFloat(tStyle.fontSize);
            if (tSize > 0 && tSize < 14 && t.textContent?.trim()) {
              issues.push(
                `Bubble ${idx + 1} has text at ${tSize}px: "${t.textContent.trim().slice(0, 30)}"`
              );
            }
          });

          if (lineHeight > 0 && fontSize > 0 && lineHeight / fontSize < 1.3) {
            issues.push(
              `Bubble ${idx + 1} line-height ratio is ${(lineHeight / fontSize).toFixed(2)} (recommended >= 1.4 for readability)`
            );
          }

          const paddingL = parseFloat(style.paddingLeft);
          const paddingR = parseFloat(style.paddingRight);
          if (paddingL < 10 || paddingR < 10) {
            issues.push(
              `Bubble ${idx + 1} has tight padding (L: ${paddingL}px, R: ${paddingR}px)`
            );
          }
        });

        return { info, issues, count: bubbles.length };
      });
      lines.push(`\n## F. Chat Bubble Text Readability`);
      lines.push(`  Found ${bubbleReadability.count} chat bubbles`);
      bubbleReadability.info.forEach((i) => lines.push(`  ${i}`));
      if (bubbleReadability.issues.length) {
        bubbleReadability.issues.forEach((i) => lines.push(`  - !! ${i}`));
      } else {
        lines.push(`  PASS — Chat bubbles appear readable`);
      }

      /* ── G. Quick reply chips check ── */
      const quickReplyCheck = await page.evaluate(() => {
        const chips = document.querySelectorAll(".quick-chip");
        const issues: string[] = [];
        const info: string[] = [];
        const vw = window.innerWidth;

        chips.forEach((chip, idx) => {
          const rect = chip.getBoundingClientRect();
          const style = window.getComputedStyle(chip);
          const fontSize = parseFloat(style.fontSize);
          const text = (chip as HTMLElement).innerText?.trim() || "";

          info.push(
            `Chip ${idx + 1}: "${text}" — ${Math.round(rect.width)}x${Math.round(rect.height)}px, font=${fontSize}px`
          );

          if (rect.height < 44) {
            issues.push(`Chip "${text}" height is ${Math.round(rect.height)}px (minimum 44px)`);
          }
          if (rect.right > vw) {
            issues.push(`Chip "${text}" overflows viewport by ${Math.round(rect.right - vw)}px`);
          }
          if (fontSize < 14) {
            issues.push(`Chip "${text}" font size is ${fontSize}px (minimum 14px recommended)`);
          }
        });

        return { info, issues, count: chips.length };
      });
      lines.push(`\n## G. Quick Reply Chips`);
      lines.push(`  Found ${quickReplyCheck.count} quick reply chips`);
      quickReplyCheck.info.forEach((i) => lines.push(`  ${i}`));
      if (quickReplyCheck.issues.length) {
        quickReplyCheck.issues.forEach((i) => lines.push(`  - !! ${i}`));
      } else if (quickReplyCheck.count > 0) {
        lines.push(`  PASS — Quick reply chips meet minimum size requirements`);
      } else {
        lines.push(`  INFO — No quick reply chips visible`);
      }

      /* ── H. Header layout check ── */
      const headerCheck = await page.evaluate(() => {
        const header = document.querySelector("header");
        if (!header) return { found: false, info: [] as string[], issues: ["No header element found"] };

        const rect = header.getBoundingClientRect();
        const vw = window.innerWidth;
        const issues: string[] = [];
        const info: string[] = [];

        info.push(`Header: ${Math.round(rect.width)}x${Math.round(rect.height)}px`);

        if (rect.height < 44) {
          issues.push(`Header too short: ${Math.round(rect.height)}px (minimum 44px for touch)`);
        }
        if (rect.width > vw) {
          issues.push(`Header overflows viewport: ${Math.round(rect.width)}px > ${vw}px`);
        }

        const buttons = header.querySelectorAll("button");
        buttons.forEach((btn) => {
          const bRect = btn.getBoundingClientRect();
          const label =
            btn.getAttribute("aria-label") || (btn as HTMLElement).innerText?.trim().slice(0, 20) || "unknown";
          if (bRect.width < 40 || bRect.height < 40) {
            issues.push(
              `Header button "${label}" is ${Math.round(bRect.width)}x${Math.round(bRect.height)}px (minimum 40x40)`
            );
          }
        });

        const h1 = header.querySelector("h1");
        if (h1) {
          const h1Rect = h1.getBoundingClientRect();
          if (h1Rect.right > vw - 8) {
            issues.push("Header title may be truncated or touching right edge");
          }
        }

        return { found: true, info, issues };
      });
      lines.push(`\n## H. Header Layout`);
      if (!headerCheck.found) {
        lines.push(`  !! No header found`);
      } else {
        headerCheck.info.forEach((i: string) => lines.push(`  ${i}`));
        if (headerCheck.issues.length) {
          headerCheck.issues.forEach((i) => lines.push(`  - !! ${i}`));
        } else {
          lines.push(`  PASS — Header layout looks correct`);
        }
      }

      /* ── I. Overall layout spacing ── */
      const layoutCheck = await page.evaluate(() => {
        const issues: string[] = [];
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        const msgList = document.querySelector('[role="log"]');
        if (msgList) {
          const rect = msgList.getBoundingClientRect();
          if (rect.height < vh * 0.3) {
            issues.push(
              `Message list area is only ${Math.round(rect.height)}px tall (${Math.round((rect.height / vh) * 100)}% of viewport) — may feel cramped`
            );
          }
        }

        const allText = document.querySelectorAll("p, h1, h2, span");
        let offScreenCount = 0;
        allText.forEach((el) => {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.left > vw) offScreenCount++;
        });
        if (offScreenCount > 0) {
          issues.push(`${offScreenCount} text element(s) are completely off-screen to the right`);
        }

        const bodyHeight = document.body.scrollHeight;
        if (bodyHeight > vh * 1.2) {
          issues.push(
            `Page body height (${bodyHeight}px) exceeds viewport (${vh}px) — chat page should NOT scroll vertically past 100dvh`
          );
        }

        return issues;
      });
      lines.push(`\n## I. Overall Layout`);
      if (layoutCheck.length) {
        layoutCheck.forEach((i) => lines.push(`  - !! ${i}`));
      } else {
        lines.push(`  PASS — Layout fills viewport correctly`);
      }

      /* ── Write this device's report ── */
      appendReport(lines);
    });
  });
}
