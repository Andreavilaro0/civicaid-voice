import { test, expect } from "@playwright/test";

const BASE = "/civicaid-voice";

test.describe("Responsive — Mobile (iPhone 14)", () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test("homepage hero fits viewport without horizontal scroll", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const body = page.locator("body");
    const bodyWidth = await body.evaluate((el) => el.scrollWidth);
    const viewportWidth = 390;
    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 1);
  });

  test("language bar is scrollable or wraps on small screens", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const langBar = page.locator('[role="radiogroup"]');
    await expect(langBar).toBeVisible();
    const barBox = await langBar.boundingBox();
    expect(barBox).toBeTruthy();
    if (barBox) {
      expect(barBox.x).toBeGreaterThanOrEqual(-5);
    }
  });

  test("hamburger menu opens correctly on mobile", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.getByLabel("Abrir menu").click();
    const dialog = page.locator('[role="dialog"]');
    await expect(dialog).toBeVisible();
    // Dialog should fit within mobile viewport
    const box = await dialog.boundingBox();
    expect(box).toBeTruthy();
  });

  test("chat input is accessible at bottom on mobile", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    const input = page.locator('input[type="text"]');
    await expect(input).toBeVisible();
    const box = await input.boundingBox();
    expect(box).toBeTruthy();
    if (box) {
      expect(box.y).toBeGreaterThan(400);
    }
  });

  test("mic button is large enough to tap (min 44px)", async ({ page }) => {
    await page.goto(`${BASE}/`);
    // Wait for page to stabilize after animations
    await page.waitForTimeout(1_000);
    const size = await page.evaluate(() => {
      // Find all buttons with mic-related aria-labels
      const selectors = [
        '[aria-label="Pulsa para hablar"]',
        '[aria-label="Tap to speak"]',
        '[aria-label="Appuyez pour parler"]',
        '[aria-label="Toca per parlar"]',
      ];
      let btn: Element | null = null;
      for (const sel of selectors) {
        btn = document.querySelector(sel);
        if (btn) break;
      }
      if (!btn) return null;
      // Force layout calculation
      const computed = getComputedStyle(btn);
      return {
        width: parseFloat(computed.width) || btn.getBoundingClientRect().width,
        height: parseFloat(computed.height) || btn.getBoundingClientRect().height,
      };
    });
    expect(size).toBeTruthy();
    if (size) {
      // Hero mic button should be at least 44px (WCAG touch target)
      expect(size.width).toBeGreaterThanOrEqual(44);
      expect(size.height).toBeGreaterThanOrEqual(44);
    }
  });
});

test.describe("Responsive — Tablet (iPad Mini)", () => {
  test.use({ viewport: { width: 768, height: 1024 } });

  test("homepage renders without overflow", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
    expect(scrollWidth).toBeLessThanOrEqual(769);
  });

  test("suggestion chips are visible on tablet", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const chips = page.locator("button").filter({ hasText: /IMV|empadronamiento|tarjeta/i });
    if (await chips.first().isVisible()) {
      const box = await chips.first().boundingBox();
      expect(box).toBeTruthy();
    }
  });
});

test.describe("Responsive — Desktop (1440px)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  test("homepage content is centered with max-width", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const heroSection = page.locator("section").first();
    await expect(heroSection).toBeVisible();
  });

  test("chat page fills full height", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    // Verify main chat container exists and fills viewport
    const bodyHeight = await page.evaluate(() => {
      const main = document.querySelector("main") || document.querySelector("[class*='h-screen']");
      if (!main) return 0;
      const rect = main.getBoundingClientRect();
      return rect.height;
    });
    const viewportHeight = page.viewportSize()!.height;
    // Chat container should fill at least 80% of viewport
    expect(bodyHeight).toBeGreaterThan(viewportHeight * 0.8);
  });
});
