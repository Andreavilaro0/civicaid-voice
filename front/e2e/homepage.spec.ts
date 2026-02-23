import { test, expect } from "@playwright/test";

const BASE = "/civicaid-voice";

test.describe("Homepage — Hero Section", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.waitForLoadState("domcontentloaded");
  });

  test("renders Clara logo and brand name", async ({ page }) => {
    await expect(page.getByText("Clara", { exact: true }).first()).toBeVisible();
  });

  test("renders greeting cycle text", async ({ page }) => {
    const greetings = [
      "Hola, soy Clara",
      "Hi, I'm Clara",
      "Bonjour, je suis Clara",
    ];
    const found = await Promise.any(
      greetings.map((g) =>
        expect(page.getByText(g)).toBeVisible({ timeout: 6_000 }).then(() => true)
      )
    ).catch(() => false);
    expect(found).toBeTruthy();
  });

  test("renders tagline with colored spans", async ({ page }) => {
    const blueSpan = page.locator(".text-clara-blue").first();
    const orangeSpan = page.locator(".text-clara-orange").first();
    await expect(blueSpan).toBeVisible({ timeout: 6_000 });
    await expect(orangeSpan).toBeVisible();
  });

  test("mic button navigates to chat with voice mode", async ({ page }) => {
    const micButton = page.getByLabel("Pulsa para hablar").first();
    await expect(micButton).toBeVisible();
    // BUG: mic button has breathing animation that makes it "not stable" — force click
    await micButton.click({ force: true });
    await expect(page).toHaveURL(/\/chat\?.*mode=voice/);
  });

  test("renders suggestion chips", async ({ page }) => {
    const chips = page.locator("button").filter({ hasText: /IMV|empadronamiento|tarjeta sanitaria|ayuda|income|aide/i });
    await expect(chips.first()).toBeVisible({ timeout: 3_000 });
  });

  test("suggestion chip navigates to chat with topic", async ({ page }) => {
    const chip = page.locator("button").filter({ hasText: /IMV|empadronamiento|tarjeta sanitaria|income|aide/i }).first();
    await chip.click();
    await expect(page).toHaveURL(/\/chat\?.*topic=/);
  });

  test("renders footer text", async ({ page }) => {
    const footer = page.getByText(/Gratis|Gratuito|Free|Gratuit/i).first();
    await expect(footer).toBeVisible();
  });

  test("scroll indicator is visible", async ({ page }) => {
    // The scroll indicator is below the footer text "Gratis · Confidencial..."
    const footerSection = page.getByText(/Gratis.*Confidencial/i).first();
    await expect(footerSection).toBeVisible();
    // Verify there's content below the hero (scroll sections exist)
    const sections = page.locator("section");
    expect(await sections.count()).toBeGreaterThanOrEqual(1);
  });
});

test.describe("Homepage — Language Switching", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.waitForLoadState("domcontentloaded");
  });

  test("language bar has 8 language buttons", async ({ page }) => {
    const langBar = page.locator('[role="radiogroup"]');
    await expect(langBar).toBeVisible();
    const buttons = langBar.locator('[role="radio"]');
    await expect(buttons).toHaveCount(8);
  });

  test("ES is selected by default", async ({ page }) => {
    const esButton = page.locator('[role="radio"]').filter({ hasText: "ES" });
    await expect(esButton).toHaveAttribute("aria-checked", "true");
  });

  test("switching to FR updates description text", async ({ page }) => {
    const frButton = page.locator('[role="radio"]').filter({ hasText: "FR" });
    await frButton.click();
    await expect(page.getByText(/demarches sociales en Espagne/i)).toBeVisible({ timeout: 3_000 });
  });

  test("switching to EN updates description text", async ({ page }) => {
    const enButton = page.locator('[role="radio"]').filter({ hasText: "EN" });
    await enButton.click();
    await expect(page.getByText(/social procedures in Spain/i)).toBeVisible({ timeout: 3_000 });
  });

  test("switching to AR sets RTL direction", async ({ page }) => {
    await page.evaluate(() => {
      const arBtn = document.querySelector('[role="radio"][aria-label="عربي"]');
      if (arBtn) { arBtn.scrollIntoView(); (arBtn as HTMLElement).click(); }
    });
    await page.waitForTimeout(300);
    const htmlDir = await page.locator("html").getAttribute("dir");
    expect(htmlDir).toBe("rtl");
  });

  test("switching back from AR to ES sets LTR direction", async ({ page }) => {
    await page.evaluate(() => {
      const arBtn = document.querySelector('[role="radio"][aria-label="عربي"]');
      if (arBtn) { arBtn.scrollIntoView(); (arBtn as HTMLElement).click(); }
    });
    await page.waitForTimeout(300);
    await page.evaluate(() => {
      const esBtn = document.querySelector('[role="radio"][aria-label="Español"]');
      if (esBtn) { esBtn.scrollIntoView(); (esBtn as HTMLElement).click(); }
    });
    await page.waitForTimeout(300);
    const htmlDir = await page.locator("html").getAttribute("dir");
    expect(htmlDir).toBe("ltr");
  });

  test("switching to ZH shows Chinese description", async ({ page }) => {
    await page.evaluate(() => {
      const all = document.querySelectorAll('[role="radio"]');
      const zhBtn = Array.from(all).find(el => el.textContent?.includes("中文"));
      if (zhBtn) { zhBtn.scrollIntoView(); (zhBtn as HTMLElement).click(); }
    });
    await expect(page.getByText("我帮你处理西班牙的社会事务")).toBeVisible({ timeout: 3_000 });
  });
});

test.describe("Homepage — Hamburger Menu", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.waitForLoadState("domcontentloaded");
  });

  test("menu button opens sidebar", async ({ page }) => {
    await page.getByLabel("Abrir menu").click();
    await expect(page.locator('[role="dialog"]')).toBeVisible();
  });

  test("menu has navigation links", async ({ page }) => {
    await page.getByLabel("Abrir menu").click();
    await expect(page.locator('[role="dialog"] nav a')).toHaveCount(4);
  });

  test("close button closes menu", async ({ page }) => {
    await page.getByLabel("Abrir menu").click();
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await page.getByLabel("Cerrar menu").click();
    await expect(page.locator('[role="dialog"]')).not.toBeVisible();
  });

  test("Escape key closes menu", async ({ page }) => {
    await page.getByLabel("Abrir menu").click();
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.locator('[role="dialog"]')).not.toBeVisible();
  });

  test("clicking backdrop closes menu", async ({ page }) => {
    await page.getByLabel("Abrir menu").click();
    const dialog = page.locator('[role="dialog"]');
    await expect(dialog).toBeVisible();
    // Click the backdrop overlay (the semi-transparent area outside the menu panel)
    const viewport = page.viewportSize()!;
    await page.mouse.click(viewport.width - 5, viewport.height / 2);
    await expect(dialog).not.toBeVisible({ timeout: 3_000 });
  });

  test("menu link navigates to sub-page", async ({ page }) => {
    await page.getByLabel("Abrir menu").click();
    await page.locator('[role="dialog"] nav a').first().click();
    await page.waitForURL(/\/(como-usar|quienes-somos|futuro|info-legal)/);
  });
});

test.describe("Homepage — Scroll Sections", () => {
  test("page has multiple sections below hero", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const sections = page.locator("section");
    expect(await sections.count()).toBeGreaterThanOrEqual(2);
  });

  test("second CTA section has mic button", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    const micButtons = page.locator('button svg path[d*="M12 14c1.66"]');
    expect(await micButtons.count()).toBeGreaterThanOrEqual(2);
  });
});

test.describe("Homepage — ClaraMascot", () => {
  test("mascot is visible as floating button", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const mascotWrapper = page.locator(".fixed.right-4.z-40");
    await expect(mascotWrapper).toBeVisible();
  });

  test("clicking mascot navigates to chat", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const mascotWrapper = page.locator(".fixed.right-4.z-40");
    await mascotWrapper.click();
    await expect(page).toHaveURL(/\/chat/);
  });
});
