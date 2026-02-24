import { test, devices, type BrowserContext, type Page } from "@playwright/test";

const BASE = "http://localhost:5176/civicaid-voice/como-usar";
const SS = "e2e/screenshots";

const MOBILE_DEVICES = [
  { name: "iPhone-SE", config: devices["iPhone SE"] },
  { name: "iPhone-14", config: devices["iPhone 14"] },
  { name: "iPhone-14-Pro-Max", config: devices["iPhone 14 Pro Max"] },
  { name: "Pixel-5", config: devices["Pixel 5"] },
  { name: "Galaxy-S9", config: devices["Galaxy S9+"] },
];

for (const device of MOBILE_DEVICES) {
  test.describe(`Mobile Audit — ${device.name}`, () => {
    let context: BrowserContext;
    let page: Page;

    test.beforeEach(async ({ browser }) => {
      context = await browser.newContext({
        ...device.config,
        // Override browser type concerns by only using viewport + userAgent
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

    test(`full page screenshot — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(2000);
      await page.screenshot({
        path: `${SS}/${device.name}-full-page.png`,
        fullPage: true,
      });
    });

    test(`hero section — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1500);
      await page.screenshot({
        path: `${SS}/${device.name}-hero-viewport.png`,
      });
    });

    test(`bento grid scroll — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1000);

      const bento = page.locator("#bento-grid");
      if (await bento.count()) {
        await bento.scrollIntoViewIfNeeded();
        await page.waitForTimeout(1500);
        await page.screenshot({
          path: `${SS}/${device.name}-bento-grid.png`,
        });

        await page.evaluate(() => window.scrollBy(0, 400));
        await page.waitForTimeout(800);
        await page.screenshot({
          path: `${SS}/${device.name}-bento-grid-2.png`,
        });

        await page.evaluate(() => window.scrollBy(0, 400));
        await page.waitForTimeout(800);
        await page.screenshot({
          path: `${SS}/${device.name}-bento-grid-3.png`,
        });
      }
    });

    test(`chips and practice card — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1000);

      const chips = page.locator(".chip-tap").first();
      if (await chips.count()) {
        await chips.scrollIntoViewIfNeeded();
        await page.waitForTimeout(1200);
        await page.screenshot({
          path: `${SS}/${device.name}-chips.png`,
        });
      }
    });

    test(`quick help section — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1000);

      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.6));
      await page.waitForTimeout(1500);
      await page.screenshot({
        path: `${SS}/${device.name}-quick-help.png`,
      });
    });

    test(`trust CTA + floating dock — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1000);

      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.8));
      await page.waitForTimeout(1500);
      await page.screenshot({
        path: `${SS}/${device.name}-trust-cta.png`,
      });

      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.5));
      await page.waitForTimeout(800);
      await page.screenshot({
        path: `${SS}/${device.name}-floating-dock.png`,
      });
    });

    test(`floating dock language dropdown — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1000);

      await page.evaluate(() => window.scrollTo(0, window.innerHeight));
      await page.waitForTimeout(1500);

      const dockNav = page.locator(".como-usar-dock");
      if (await dockNav.count()) {
        const langBtn = dockNav.locator("button").last();
        if (await langBtn.isVisible()) {
          await langBtn.click();
          await page.waitForTimeout(500);
          await page.screenshot({
            path: `${SS}/${device.name}-dock-lang-dropdown.png`,
          });
        }
      }
    });

    test(`dark mode — ${device.name}`, async () => {
      await page.emulateMedia({ colorScheme: "dark" });
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1500);

      // emulateMedia already activates dark mode via "system" preference.
      // Do NOT click the toggle — that would switch it back to light.

      await page.screenshot({
        path: `${SS}/${device.name}-dark-hero.png`,
      });

      await page.evaluate(() => window.scrollTo(0, window.innerHeight * 1.2));
      await page.waitForTimeout(1200);
      await page.screenshot({
        path: `${SS}/${device.name}-dark-bento.png`,
      });

      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(1200);
      await page.screenshot({
        path: `${SS}/${device.name}-dark-bottom.png`,
      });
    });

    test(`touch targets and overflow check — ${device.name}`, async () => {
      await page.goto(BASE, { waitUntil: "networkidle" });
      await page.waitForTimeout(1500);

      // Scroll full page to trigger all IntersectionObserver reveals
      await page.evaluate(async () => {
        const totalHeight = document.body.scrollHeight;
        for (let y = 0; y < totalHeight; y += 300) {
          window.scrollTo(0, y);
          await new Promise((r) => setTimeout(r, 200));
        }
        window.scrollTo(0, 0);
        await new Promise((r) => setTimeout(r, 500));
      });

      const hasHorizontalOverflow = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });

      const smallButtons = await page.evaluate(() => {
        const buttons = document.querySelectorAll("button, a, [role='button'], [role='option']");
        const issues: string[] = [];
        buttons.forEach((btn) => {
          const rect = btn.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            if (rect.width < 44 || rect.height < 44) {
              const text = (btn as HTMLElement).innerText?.slice(0, 30) || btn.tagName;
              issues.push(
                `"${text}" — ${Math.round(rect.width)}x${Math.round(rect.height)}px (need 44x44)`
              );
            }
          }
        });
        return issues;
      });

      const smallText = await page.evaluate(() => {
        const all = document.querySelectorAll("*");
        const issues: string[] = [];
        const seen = new Set<string>();
        all.forEach((el) => {
          const style = window.getComputedStyle(el);
          const fontSize = parseFloat(style.fontSize);
          if (fontSize > 0 && fontSize < 12 && el.textContent?.trim()) {
            const text = el.textContent.trim().slice(0, 40);
            const key = `${fontSize}-${text}`;
            if (!seen.has(key)) {
              seen.add(key);
              issues.push(`${fontSize}px: "${text}"`);
            }
          }
        });
        return issues;
      });

      const overflowIssues = await page.evaluate(() => {
        const issues: string[] = [];
        const all = document.querySelectorAll("*");
        all.forEach((el) => {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.right > window.innerWidth + 2) {
            const tag = el.tagName.toLowerCase();
            const cls = el.className?.toString().slice(0, 40) || "";
            issues.push(`${tag}.${cls} overflows right by ${Math.round(rect.right - window.innerWidth)}px`);
          }
        });
        return [...new Set(issues)].slice(0, 20);
      });

      const spacingIssues = await page.evaluate(() => {
        const issues: string[] = [];
        const textElements = document.querySelectorAll("h1, h2, h3, h4, p, span");
        textElements.forEach((el) => {
          const rect = el.getBoundingClientRect();
          const text = el.textContent?.trim().slice(0, 30) || "";
          if (rect.width > 0 && text) {
            if (rect.left < 8) {
              issues.push(`Text touching left edge (${Math.round(rect.left)}px): "${text}"`);
            }
            if (rect.right > window.innerWidth - 8) {
              issues.push(`Text touching right edge (${Math.round(window.innerWidth - rect.right)}px gap): "${text}"`);
            }
          }
        });
        return [...new Set(issues)].slice(0, 15);
      });

      const dockOverlap = await page.evaluate(() => {
        const dock = document.querySelector(".como-usar-dock");
        if (!dock) return [];
        const dockRect = dock.getBoundingClientRect();
        const issues: string[] = [];
        const interactives = document.querySelectorAll("button, a, [role='button']");
        interactives.forEach((el) => {
          if (dock.contains(el)) return;
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.bottom > dockRect.top && rect.top < dockRect.bottom) {
            const text = (el as HTMLElement).innerText?.slice(0, 30) || el.tagName;
            issues.push(`"${text}" may be hidden behind floating dock`);
          }
        });
        return issues;
      });

      const vw = device.config.viewport?.width;
      const vh = device.config.viewport?.height;
      const report = [
        `\n=== MOBILE AUDIT: ${device.name} (${vw}x${vh}) ===`,
        ``,
        `## Horizontal Overflow: ${hasHorizontalOverflow ? "!! YES — PAGE SCROLLS HORIZONTALLY !!" : "No (OK)"}`,
        ``,
        `## Small Touch Targets (below 44x44 — WCAG):`,
        ...(smallButtons.length ? smallButtons.map((b) => `  - ${b}`) : ["  None found (OK)"]),
        ``,
        `## Text Below 12px (readability risk):`,
        ...(smallText.length ? smallText.map((t) => `  - ${t}`) : ["  None found (OK)"]),
        ``,
        `## Elements Overflowing Right Edge:`,
        ...(overflowIssues.length ? overflowIssues.map((o) => `  - ${o}`) : ["  None found (OK)"]),
        ``,
        `## Spacing Issues (text touching screen edges):`,
        ...(spacingIssues.length ? spacingIssues.map((s) => `  - ${s}`) : ["  None found (OK)"]),
        ``,
        `## Dock Overlap (interactive elements behind dock):`,
        ...(dockOverlap.length ? dockOverlap.map((d) => `  - ${d}`) : ["  None found (OK)"]),
      ].join("\n");

      const fs = await import("fs");
      fs.mkdirSync(`${SS}`, { recursive: true });
      fs.appendFileSync(`${SS}/audit-report.txt`, report + "\n\n");
    });
  });
}
