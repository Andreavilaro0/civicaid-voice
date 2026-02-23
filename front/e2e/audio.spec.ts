import { test, expect, type Page } from "@playwright/test";

const BASE = "/civicaid-voice";

/** Mock audio URL the "backend" returns */
const MOCK_AUDIO_URL =
  "https://civicaid-voice.onrender.com/static/cache/test.mp3";

/* ------------------------------------------------------------------ */
/*  Audio element stub                                                 */
/*                                                                     */
/*  Real Audio loading is unreliable in headless browsers. We stub     */
/*  the Audio constructor to fire the right events and track calls     */
/*  so we can verify crossOrigin and src behavior.                     */
/* ------------------------------------------------------------------ */

/**
 * Injects an Audio constructor stub BEFORE the app loads.
 * The stub:
 * - Records property assignments (crossOrigin, src, preload)
 * - Fires loadedmetadata + canplaythrough after src is set
 * - Exposes tracking data on window.__audioStub
 */
async function stubAudio(page: Page) {
  await page.addInitScript(() => {
    const instances: Array<{
      src: string;
      crossOrigin: string | null;
      assignments: string[];
    }> = [];

    const OrigAudio = window.Audio;

    window.Audio = function () {
      const el = document.createElement("audio");
      const record: (typeof instances)[0] = {
        src: "",
        crossOrigin: null,
        assignments: [],
      };
      instances.push(record);

      // Override property setters to track assignments
      Object.defineProperty(el, "crossOrigin", {
        get() {
          return record.crossOrigin;
        },
        set(v: string) {
          record.crossOrigin = v;
          record.assignments.push("crossOrigin");
          el.setAttribute("crossorigin", v);
        },
        configurable: true,
      });

      const origSrcDesc = Object.getOwnPropertyDescriptor(
        HTMLMediaElement.prototype,
        "src",
      );
      Object.defineProperty(el, "src", {
        get() {
          return record.src;
        },
        set(v: string) {
          record.src = v;
          record.assignments.push("src");
          // Don't actually load the URL — fire synthetic events instead
          Object.defineProperty(el, "duration", {
            value: 3.5,
            writable: true,
            configurable: true,
          });
          Object.defineProperty(el, "readyState", {
            value: 4,
            writable: true,
            configurable: true,
          });
          // Fire events async (matches real browser behavior)
          setTimeout(() => {
            el.dispatchEvent(new Event("loadedmetadata"));
            el.dispatchEvent(new Event("canplay"));
            el.dispatchEvent(new Event("canplaythrough"));
          }, 50);
        },
        configurable: true,
      });

      // Stub play() to fire the play event
      el.play = () => {
        el.dispatchEvent(new Event("play"));
        // Simulate ending after a short time
        setTimeout(() => {
          el.dispatchEvent(new Event("ended"));
        }, 200);
        return Promise.resolve();
      };

      return el as unknown as HTMLAudioElement;
    } as unknown as typeof Audio;
    window.Audio.prototype = OrigAudio.prototype;

    (window as any).__audioStub = { instances };
  });
}

/* ------------------------------------------------------------------ */
/*  API route mocking                                                  */
/* ------------------------------------------------------------------ */

async function mockAPIs(page: Page, options?: { ttsReturnsNull?: boolean; chatAudioNull?: boolean }) {
  await page.route("**/api/tts", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        audio_url: options?.ttsReturnsNull ? null : MOCK_AUDIO_URL,
      }),
    });
  });

  await page.route("**/api/chat", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        response: "El IMV es una prestacion de la Seguridad Social.",
        source: "llm",
        language: "es",
        duration_ms: 150,
        audio_url: options?.chatAudioNull ? null : MOCK_AUDIO_URL,
        sources: [],
      }),
    });
  });

  // Block any real audio file requests (shouldn't happen with stub, but safety net)
  await page.route("**/*.mp3", async (route) => {
    await route.abort("blockedbyclient");
  });
}

/** Navigate to chat and wait for welcome text */
async function gotoChat(page: Page) {
  await page.goto(`${BASE}/chat?lang=es&mode=text`, {
    waitUntil: "domcontentloaded",
  });
  await expect(page.getByText(/Hola, soy Clara/i)).toBeVisible({
    timeout: 8_000,
  });
}

/* ================================================================== */
/*  Fix #1 — crossOrigin = "anonymous"                                 */
/* ================================================================== */

test.describe("Audio — crossOrigin attribute", () => {
  test("useAudioPlayer sets crossOrigin=anonymous before setting src", async ({
    page,
  }) => {
    await stubAudio(page);
    await mockAPIs(page);
    await gotoChat(page);

    // Wait for AudioPlayer to render (play button visible = Audio was created)
    await expect(
      page.getByLabel(/Escuchar respuesta/i).first(),
    ).toBeVisible({ timeout: 8_000 });

    // Check that crossOrigin was set BEFORE src on at least one Audio instance
    const stub = await page.evaluate(
      () => (window as any).__audioStub,
    );
    expect(stub.instances.length).toBeGreaterThan(0);

    const first = stub.instances[0];
    expect(first.crossOrigin).toBe("anonymous");

    const crossIdx = first.assignments.indexOf("crossOrigin");
    const srcIdx = first.assignments.indexOf("src");
    expect(crossIdx).toBeGreaterThanOrEqual(0);
    expect(srcIdx).toBeGreaterThan(crossIdx); // crossOrigin set before src
  });
});

/* ================================================================== */
/*  Fixes #2 + #3 — Welcome TTS truncation                            */
/* ================================================================== */

test.describe("Audio — Welcome Message", () => {
  test("welcome message shows AudioPlayer when TTS returns audio URL", async ({
    page,
  }) => {
    await stubAudio(page);
    await mockAPIs(page);
    await gotoChat(page);

    const playBtn = page.getByLabel(/Escuchar respuesta/i).first();
    await expect(playBtn).toBeVisible({ timeout: 8_000 });
  });

  test("TTS request contains only first paragraph of welcome text", async ({
    page,
  }) => {
    let ttsBody: { text: string; language: string } | null = null;

    await stubAudio(page);

    // Custom TTS mock that captures the request body
    await page.route("**/api/tts", async (route) => {
      ttsBody = route.request().postDataJSON();
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ audio_url: MOCK_AUDIO_URL }),
      });
    });
    await page.route("**/*.mp3", async (route) => route.abort("blockedbyclient"));

    await gotoChat(page);

    // Wait for AudioPlayer to confirm TTS was called
    await expect(
      page.getByLabel(/Escuchar respuesta/i).first(),
    ).toBeVisible({ timeout: 8_000 });

    expect(ttsBody).not.toBeNull();
    // First paragraph only — no double newlines, no "tramites"
    expect(ttsBody!.text).toContain("Clara");
    expect(ttsBody!.text).not.toContain("\n\n");
    expect(ttsBody!.text).not.toContain("tramites del gobierno");
    expect(ttsBody!.text.length).toBeLessThan(200);
  });
});

/* ================================================================== */
/*  Fix #4 — No double resolveAudioUrl + Chat Response                 */
/* ================================================================== */

test.describe("Audio — Chat Response", () => {
  test("Clara response renders AudioPlayer after sending a message", async ({
    page,
  }) => {
    await stubAudio(page);
    await mockAPIs(page);
    await gotoChat(page);

    // Wait for welcome AudioPlayer
    await expect(
      page.getByLabel(/Escuchar respuesta/i).first(),
    ).toBeVisible({ timeout: 8_000 });

    // Send a message
    const input = page.locator('input[type="text"]');
    await input.fill("Que es el IMV?");
    await input.press("Enter");

    // Wait for Clara's response text
    await expect(
      page.getByText("El IMV es una prestacion de la Seguridad Social."),
    ).toBeVisible({ timeout: 10_000 });

    // Should now have 2 AudioPlayers (welcome + response)
    const players = page.getByLabel(/Escuchar respuesta|Pausar audio|Continuar audio/i);
    await expect(players.nth(1)).toBeVisible({ timeout: 5_000 });
  });

  test("audio src matches the URL from API (no double-resolve prefix)", async ({
    page,
  }) => {
    await stubAudio(page);
    await mockAPIs(page);
    await gotoChat(page);

    const input = page.locator('input[type="text"]');
    await input.fill("Que es el IMV?");
    await input.press("Enter");

    await expect(
      page.getByText("El IMV es una prestacion de la Seguridad Social."),
    ).toBeVisible({ timeout: 10_000 });

    // Check Audio stubs: all non-empty src values should be MOCK_AUDIO_URL exactly
    // (useAudioPlayer sets src="" on cleanup, which we filter out)
    const stub = await page.evaluate(
      () => (window as any).__audioStub,
    );
    const srcs = stub.instances
      .map((i: any) => i.src)
      .filter((s: string) => s !== "");
    expect(srcs.length).toBeGreaterThan(0);
    for (const src of srcs) {
      // Should be the exact URL, not double-prefixed
      expect(src).toBe(MOCK_AUDIO_URL);
    }
  });
});

/* ================================================================== */
/*  AudioPlayer UI components                                          */
/* ================================================================== */

test.describe("Audio — Player UI", () => {
  test.beforeEach(async ({ page }) => {
    await stubAudio(page);
    await mockAPIs(page);
    await gotoChat(page);
  });

  test("AudioPlayer has play button, progress bar, and speed button", async ({
    page,
  }) => {
    const playBtn = page.getByLabel(/Escuchar respuesta/i).first();
    await expect(playBtn).toBeVisible({ timeout: 8_000 });

    const slider = page.getByLabel(/Progreso del audio/i).first();
    await expect(slider).toBeVisible();

    const speedBtn = page.getByLabel(/Velocidad/i).first();
    await expect(speedBtn).toBeVisible();
    await expect(speedBtn).toHaveText("1x");
  });

  test("speed button cycles through speeds on click", async ({ page }) => {
    const speedBtn = page.getByLabel(/Velocidad/i).first();
    await expect(speedBtn).toBeVisible({ timeout: 8_000 });

    await speedBtn.click();
    await expect(speedBtn).toHaveText("1.25x");
  });
});

/* ================================================================== */
/*  Error state (without Audio stub — real error)                      */
/* ================================================================== */

test.describe("Audio — Error State", () => {
  test("shows 'Audio no disponible' when audio file fails to load", async ({
    page,
  }) => {
    // NO stubAudio() — let real Audio try and fail
    await page.route("**/*.mp3", async (route) => {
      await route.abort("connectionfailed");
    });
    await page.route("**/api/tts", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ audio_url: MOCK_AUDIO_URL }),
      });
    });

    await page.goto(`${BASE}/chat?lang=es&mode=text`, {
      waitUntil: "domcontentloaded",
    });

    const errorAlert = page.locator('[role="alert"]');
    await expect(errorAlert).toBeVisible({ timeout: 10_000 });
    await expect(errorAlert).toContainText("Audio no disponible");
  });
});

/* ================================================================== */
/*  Graceful degradation — TTS returns null                            */
/* ================================================================== */

test.describe("Audio — Graceful Degradation", () => {
  test("no AudioPlayer when TTS returns null", async ({ page }) => {
    await stubAudio(page);
    await mockAPIs(page, { ttsReturnsNull: true });

    await gotoChat(page);

    // Give time for async TTS to resolve (returns null)
    await page.waitForTimeout(2_000);
    expect(await page.getByLabel(/Escuchar respuesta/i).count()).toBe(0);
    expect(await page.locator('[role="alert"]').count()).toBe(0);
  });

  test("chat response without audio_url shows no AudioPlayer", async ({
    page,
  }) => {
    await stubAudio(page);
    await mockAPIs(page, { ttsReturnsNull: true, chatAudioNull: true });

    await gotoChat(page);

    const input = page.locator('input[type="text"]');
    await input.fill("Que es el IMV?");
    await input.press("Enter");

    await expect(
      page.getByText("El IMV es una prestacion de la Seguridad Social."),
    ).toBeVisible({ timeout: 10_000 });

    // No AudioPlayer anywhere
    expect(await page.getByLabel(/Escuchar respuesta/i).count()).toBe(0);
  });
});
