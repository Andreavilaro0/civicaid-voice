import { test, expect } from "@playwright/test";

const BASE = "/civicaid-voice";

test.describe("Accessibility — ARIA", () => {
  test("language bar has radiogroup role", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const langBar = page.locator('[role="radiogroup"]');
    await expect(langBar).toBeVisible();
    await expect(langBar).toHaveAttribute("aria-label", "Seleccionar idioma");
  });

  test("language buttons have radio role and aria-checked", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const buttons = page.locator('[role="radio"]');
    const count = await buttons.count();
    expect(count).toBe(8);
    const esBtn = buttons.filter({ hasText: "ES" });
    await expect(esBtn).toHaveAttribute("aria-checked", "true");
    const enBtn = buttons.filter({ hasText: "EN" });
    await expect(enBtn).toHaveAttribute("aria-checked", "false");
  });

  test("hamburger menu has dialog role and aria-modal", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.getByLabel("Abrir menu").click();
    const dialog = page.locator('[role="dialog"]');
    await expect(dialog).toBeVisible();
    await expect(dialog).toHaveAttribute("aria-modal", "true");
  });

  test("chat input has proper aria-label", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    const input = page.locator('input[type="text"]');
    const label = await input.getAttribute("aria-label");
    expect(label).toBeTruthy();
    expect(label).toContain("pregunta");
  });

  test("send button has proper aria-label", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    const input = page.locator('input[type="text"]');
    await input.fill("test");
    const sendBtn = page.locator('button[type="submit"]');
    await expect(sendBtn).toHaveAttribute("aria-label", "Enviar");
  });

  test("voice button has proper aria-label", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    const voiceBtn = page.locator('.chat-form button[type="button"]').filter({ has: page.locator('svg path[d*="M12 14c1.66"]') });
    await expect(voiceBtn).toHaveAttribute("aria-label", "Grabar voz");
  });

  test("camera button has proper aria-label", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    const cameraBtn = page.locator('.chat-form button[type="button"]').filter({ has: page.locator('svg path[d*="M9 2L7.17"]') });
    await expect(cameraBtn).toHaveAttribute("aria-label", "Subir foto");
  });
});

test.describe("Accessibility — Keyboard Navigation", () => {
  test("Tab key navigates through homepage interactive elements", async ({ page }) => {
    await page.goto(`${BASE}/`);
    for (let i = 0; i < 10; i++) {
      await page.keyboard.press("Tab");
    }
    const focusedTag = await page.evaluate(() => document.activeElement?.tagName);
    expect(focusedTag).toBeTruthy();
  });

  test("Enter key activates language button", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const enBtn = page.locator('[role="radio"]').filter({ hasText: "EN" });
    await enBtn.focus();
    await page.keyboard.press("Enter");
    await expect(enBtn).toHaveAttribute("aria-checked", "true");
  });

  test("focus trap works in hamburger menu", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.getByLabel("Abrir menu").click();
    await page.waitForTimeout(200);
    for (let i = 0; i < 15; i++) {
      await page.keyboard.press("Tab");
    }
    const focusedInDialog = await page.evaluate(() => {
      const dialog = document.querySelector('[role="dialog"]');
      return dialog?.contains(document.activeElement);
    });
    expect(focusedInDialog).toBe(true);
  });

  test("chat input Enter submits message", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es`);
    const input = page.getByPlaceholder("Escribe tu pregunta...");
    await expect(input).toBeVisible({ timeout: 5_000 });
    await input.fill("Hola test");
    await input.press("Enter");
    await expect(input).toHaveValue("");
    await expect(page.getByText("Hola test")).toBeVisible({ timeout: 5_000 });
  });
});

test.describe("Accessibility — RTL Support", () => {
  test("Arabic homepage has RTL layout", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.evaluate(() => {
      const arBtn = document.querySelector('[role="radio"][aria-label="عربي"]');
      if (arBtn) { arBtn.scrollIntoView(); (arBtn as HTMLElement).click(); }
    });
    await page.waitForTimeout(300);
    const dir = await page.locator("html").getAttribute("dir");
    expect(dir).toBe("rtl");
    const lang = await page.locator("html").getAttribute("lang");
    expect(lang).toBe("ar");
  });

  test("Arabic chat input is RTL", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=ar`);
    const input = page.locator('input[type="text"]');
    await expect(input).toHaveAttribute("dir", "rtl");
    await expect(input).toHaveAttribute("placeholder", "اكتب سؤالك...");
  });

  test("Arabic description text is visible", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.evaluate(() => {
      const arBtn = document.querySelector('[role="radio"][aria-label="عربي"]');
      if (arBtn) { arBtn.scrollIntoView(); (arBtn as HTMLElement).click(); }
    });
    await expect(page.getByText("أساعدك في الإجراءات الاجتماعية")).toBeVisible({ timeout: 3_000 });
  });
});
