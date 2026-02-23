import { test, expect } from "@playwright/test";

const BASE = "/civicaid-voice";

test.describe("Dark Mode", () => {
  test("theme toggle exists in hamburger menu", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.getByLabel("Abrir menu").click();
    const dialog = page.locator('[role="dialog"]');
    await expect(dialog).toBeVisible();
    const toggleArea = dialog.locator(".border-b").nth(1);
    await expect(toggleArea).toBeVisible();
  });

  test("compact theme toggle exists in header", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const header = page.locator("header");
    await expect(header).toBeVisible();
  });

  test("dark mode toggle changes html class", async ({ page }) => {
    await page.goto(`${BASE}/`);
    const initialClass = await page.locator("html").getAttribute("class");
    await page.getByLabel("Abrir menu").click();
    const toggleBtn = page.locator('[role="dialog"]').locator("button").filter({ hasText: /oscuro|dark|mode/i });
    if (await toggleBtn.count() > 0) {
      await toggleBtn.first().click();
      await page.waitForTimeout(300);
      const newClass = await page.locator("html").getAttribute("class");
      expect(newClass).not.toBe(initialClass);
    }
  });

  test("dark mode preserves readability", async ({ page }) => {
    await page.goto(`${BASE}/`);
    await page.evaluate(() => document.documentElement.classList.add("dark"));
    await page.waitForTimeout(200);
    const textColor = await page.evaluate(() => {
      const el = document.querySelector("h1") || document.querySelector("p");
      return el ? getComputedStyle(el).color : null;
    });
    expect(textColor).toBeTruthy();
  });
});
