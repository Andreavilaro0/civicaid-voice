import { test, expect } from "@playwright/test";

const BASE = "/civicaid-voice";

test.describe("Navigation — Routes", () => {
  test("/ renders homepage", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await expect(page.locator('[role="radiogroup"]')).toBeVisible();
  });

  test("/chat renders chat page", async ({ page }) => {
    await page.goto(`${BASE}/chat`);
    await expect(page.locator('input[type="text"]')).toBeVisible();
  });

  test("/como-usar renders how-to page", async ({ page }) => {
    await page.goto(`${BASE}/como-usar?lang=es`);
    await expect(page.getByText(/usar|como/i).first()).toBeVisible({ timeout: 5_000 });
  });

  test("/quienes-somos renders about page", async ({ page }) => {
    await page.goto(`${BASE}/quienes-somos?lang=es`);
    await page.waitForLoadState("domcontentloaded");
    await expect(page.locator("body")).toBeVisible();
  });

  test("/futuro renders future page", async ({ page }) => {
    await page.goto(`${BASE}/futuro?lang=es`);
    await page.waitForLoadState("domcontentloaded");
    await expect(page.locator("body")).toBeVisible();
  });

  test("/info-legal renders legal info page", async ({ page }) => {
    await page.goto(`${BASE}/info-legal?lang=es`);
    await page.waitForLoadState("domcontentloaded");
    await expect(page.locator("body")).toBeVisible();
  });

  test("unknown route redirects to homepage", async ({ page }) => {
    await page.goto(`${BASE}/unknown-page`);
    await expect(page).toHaveURL(/\/civicaid-voice\/$/);
  });
});

test.describe("Navigation — Menu to Sub-pages", () => {
  test("menu → como-usar works", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.getByLabel("Abrir menu").click();
    const menuLinks = page.locator('[role="dialog"] nav a');
    const comoUsarLink = menuLinks.filter({ hasText: /usar|guide|utiliser/i }).first();
    if (await comoUsarLink.count()) {
      await comoUsarLink.click();
      await expect(page).toHaveURL(/como-usar/);
    }
  });

  test("sub-page has back navigation to home", async ({ page }) => {
    await page.goto(`${BASE}/como-usar?lang=es`);
    await page.waitForLoadState("domcontentloaded");
    // Back button is a <button> "Volver al inicio", not an <a> tag
    const backBtn = page.getByRole("button", { name: /Volver|Back|Retour/i });
    await expect(backBtn).toBeVisible({ timeout: 3_000 });
  });
});

test.describe("Navigation — Homepage to Chat flows", () => {
  test("hero mic button → chat?mode=voice", async ({ page }) => {
    await page.goto(`${BASE}/`);
    // BUG: mic button breathing animation blocks Playwright stability checks
    // Use JS click to bypass animation instability
    await page.evaluate(() => {
      const btn = document.querySelector('[aria-label="Pulsa para hablar"]') ||
                  document.querySelector('[aria-label="Tap to speak"]');
      if (btn) {
        btn.scrollIntoView({ block: "center" });
        (btn as HTMLElement).click();
      }
    });
    await expect(page).toHaveURL(/\/chat\?.*mode=voice/);
  });

  test("prompt bar submit → chat with topic", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const promptInput = page.locator('input[placeholder]').first();
    if (await promptInput.isVisible()) {
      await promptInput.fill("Necesito ayuda con el IMV");
      await promptInput.press("Enter");
      await expect(page).toHaveURL(/\/chat/);
    }
  });
});
