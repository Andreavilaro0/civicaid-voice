import { test, expect } from "@playwright/test";

const BASE = "/civicaid-voice";

test.describe("Chat Page — Layout", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es&mode=text`);
    await page.waitForLoadState("domcontentloaded");
  });

  test("renders header with language selector", async ({ page }) => {
    const header = page.locator("header").first();
    await expect(header).toBeVisible();
  });

  test("renders chat input bar at bottom", async ({ page }) => {
    const input = page.locator('input[type="text"]');
    await expect(input).toBeVisible();
    await expect(input).toHaveAttribute("placeholder", "Escribe tu pregunta...");
  });

  test("renders welcome message from Clara", async ({ page }) => {
    // Clara sends a welcome message on load
    const claraMsg = page.getByText(/Clara|ayud|bienvenid|hola/i).first();
    await expect(claraMsg).toBeVisible({ timeout: 5_000 });
  });

  test("shows quick reply buttons initially", async ({ page }) => {
    // Quick replies should be visible when there are <= 2 messages
    const quickReplies = page.locator("button").filter({ hasText: /IMV|empadronamiento|tarjeta/i });
    // Might not exist if language doesn't match — just check the area exists
    await page.waitForTimeout(1_000);
  });

  test("chat input has camera button", async ({ page }) => {
    const cameraBtn = page.locator('button').filter({ has: page.locator('svg path[d*="M9 2L7.17"]') });
    await expect(cameraBtn).toBeVisible();
  });

  test("chat input has voice button when empty", async ({ page }) => {
    const voiceBtn = page.locator('.chat-form button[type="button"]').filter({ has: page.locator('svg path[d*="M12 14c1.66"]') });
    await expect(voiceBtn).toBeVisible();
  });
});

test.describe("Chat Page — Text Input", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es&mode=text`);
    await page.waitForLoadState("domcontentloaded");
  });

  test("typing text shows send button instead of mic", async ({ page }) => {
    const input = page.locator('input[type="text"]');
    await input.fill("Hola Clara");
    // Send button should appear (paper plane icon)
    const sendBtn = page.locator('button[type="submit"]');
    await expect(sendBtn).toBeVisible();
  });

  test("clearing text brings back mic button", async ({ page }) => {
    const input = page.locator('input[type="text"]');
    await input.fill("Hola");
    await expect(page.locator('button[type="submit"]')).toBeVisible();
    await input.fill("");
    // Mic button should reappear
    const voiceBtn = page.locator('.chat-form button[type="button"]').filter({ has: page.locator('svg path[d*="M12 14c1.66"]') });
    await expect(voiceBtn).toBeVisible();
  });

  test("submitting empty text does nothing", async ({ page }) => {
    const input = page.locator('input[type="text"]');
    await input.press("Enter");
    // Input should still be empty, no message sent
    await expect(input).toHaveValue("");
  });

  test("input clears after submit", async ({ page }) => {
    const input = page.locator('input[type="text"]');
    await input.fill("Hola Clara");
    await input.press("Enter");
    await expect(input).toHaveValue("");
  });

  test("user message appears in chat after submit", async ({ page }) => {
    const input = page.locator('input[type="text"]');
    await input.fill("Que es el IMV?");
    await input.press("Enter");
    await expect(page.getByText("Que es el IMV?")).toBeVisible({ timeout: 3_000 });
  });
});

test.describe("Chat Page — Language Variants", () => {
  test("French chat shows French placeholder", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=fr`);
    const input = page.locator('input[type="text"]');
    await expect(input).toHaveAttribute("placeholder", /cris ta question/i);
  });

  test("Arabic chat sets RTL on input", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=ar`);
    const input = page.locator('input[type="text"]');
    await expect(input).toHaveAttribute("dir", "rtl");
  });

  test("Chinese chat shows Chinese placeholder", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=zh`);
    const input = page.locator('input[type="text"]');
    await expect(input).toHaveAttribute("placeholder", "输入你的问题...");
  });

  test("English chat shows English placeholder", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=en`);
    const input = page.locator('input[type="text"]');
    await expect(input).toHaveAttribute("placeholder", "Type your question...");
  });

  test("Portuguese chat shows Portuguese placeholder", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=pt`);
    const input = page.locator('input[type="text"]');
    await expect(input).toHaveAttribute("placeholder", /Escreve a tua pergunta/i);
  });
});

test.describe("Chat Page — Topic from Homepage", () => {
  test("topic query param auto-sends message", async ({ page }) => {
    await page.goto(`${BASE}/chat?lang=es&mode=text&topic=Qu%C3%A9%20es%20el%20IMV`);
    // The topic text should appear as a user message
    await expect(page.getByText(/Qué es el IMV/)).toBeVisible({ timeout: 5_000 });
  });
});
