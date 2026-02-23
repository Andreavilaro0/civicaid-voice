import { type Page, type Locator, expect } from "@playwright/test";

/**
 * ChatPage — Page Object Model for Clara's chat interface.
 *
 * Encapsulates all locators and actions needed for E2E testing.
 * Uses role-based and aria-label selectors for reliability.
 */
export class ChatPage {
  readonly page: Page;
  private static readonly BASE = "/civicaid-voice";

  /* ── Locators ── */
  readonly messageLog: Locator;
  readonly textInput: Locator;
  readonly sendButton: Locator;
  readonly voiceButton: Locator;
  readonly quickChips: Locator;
  readonly loadingIndicator: Locator;
  readonly header: Locator;

  constructor(page: Page) {
    this.page = page;
    this.messageLog = page.locator('[role="log"]');
    this.textInput = page.locator("input[type='text']");
    this.sendButton = page.locator('button[type="submit"]');
    this.voiceButton = page.locator('.chat-form button[type="button"]').last();
    this.quickChips = page.locator(".quick-chip");
    this.loadingIndicator = page.locator('[role="status"]');
    this.header = page.locator("header");
  }

  /* ── Navigation ── */

  async goto(lang = "es") {
    // Mock TTS to prevent network errors (no backend during tests)
    await this.page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );
    await this.page.goto(`${ChatPage.BASE}/chat?lang=${lang}&mode=text`);
    await this.page.waitForLoadState("domcontentloaded");
  }

  /* ── Messages ── */

  /** Get all visible message bubbles */
  get claraMessages(): Locator {
    return this.page.locator('[aria-label="Clara message"], [aria-label="Mensaje de Clara"]');
  }

  get userMessages(): Locator {
    return this.page.locator('[aria-label="Your message"], [aria-label="Tu mensaje"]');
  }

  get allMessages(): Locator {
    return this.page.locator('[role="article"]');
  }

  /** Get the text content of the last Clara message */
  async getLastClaraMessageText(): Promise<string> {
    const msgs = this.claraMessages;
    const count = await msgs.count();
    if (count === 0) return "";
    return (await msgs.nth(count - 1).textContent()) ?? "";
  }

  /** Get all Clara message texts as an array */
  async getAllClaraMessageTexts(): Promise<string[]> {
    const msgs = this.claraMessages;
    const count = await msgs.count();
    const texts: string[] = [];
    for (let i = 0; i < count; i++) {
      texts.push((await msgs.nth(i).textContent()) ?? "");
    }
    return texts;
  }

  /** Count total messages (Clara + User) */
  async countMessages(): Promise<number> {
    return await this.allMessages.count();
  }

  /* ── Input & Send ── */

  /** Type a message and send it */
  async sendMessage(text: string) {
    await this.textInput.fill(text);
    await this.sendButton.click();
  }

  /** Click a quick reply chip by its text */
  async clickQuickChip(text: string) {
    await this.page.getByRole("button", { name: text }).click();
  }

  /* ── Waiting ── */

  /** Wait for Clara's loading indicator to appear */
  async waitForLoading() {
    await this.loadingIndicator.first().waitFor({ state: "visible", timeout: 5_000 }).catch(() => {
      /* loading may be too fast to catch — that's OK */
    });
  }

  /** Wait for Clara's response (loading disappears + new Clara message appears) */
  async waitForResponse(timeout = 15_000) {
    // Wait for loading to disappear
    await this.loadingIndicator.first().waitFor({ state: "hidden", timeout }).catch(() => {});
    // Small buffer for DOM update
    await this.page.waitForTimeout(200);
  }

  /** Send a message and wait for Clara's response. Returns response time in ms. */
  async sendAndWait(text: string, timeout = 15_000): Promise<{ responseMs: number; responseText: string }> {
    const countBefore = await this.claraMessages.count();
    const start = Date.now();
    await this.sendMessage(text);
    // Wait until a new Clara message appears (beyond the loading state)
    await this.claraMessages.nth(countBefore).waitFor({ state: "visible", timeout });
    await this.waitForResponse(timeout);
    const responseMs = Date.now() - start;
    const responseText = await this.getLastClaraMessageText();
    return { responseMs, responseText };
  }

  /* ── Assertions ── */

  /** Assert welcome message is visible (uses text match for reliability) */
  async expectWelcomeMessage() {
    const welcome = this.page.getByText(/Clara|ayud|bienvenid|hola|Hi|Salut|Buna/i).first();
    await expect(welcome).toBeVisible({ timeout: 8_000 });
  }

  /** Assert quick chips are visible */
  async expectQuickChipsVisible() {
    await expect(this.quickChips.first()).toBeVisible();
  }

  /** Assert quick chips are hidden */
  async expectQuickChipsHidden() {
    await expect(this.quickChips.first()).not.toBeVisible();
  }

  /** Assert the loading indicator is showing */
  async expectLoading() {
    await expect(this.loadingIndicator.first()).toBeVisible();
  }

  /** Assert no loading indicator */
  async expectNotLoading() {
    await expect(this.loadingIndicator.first()).not.toBeVisible();
  }
}
