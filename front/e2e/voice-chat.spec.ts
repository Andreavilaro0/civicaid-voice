import { test, expect, type Page } from "@playwright/test";

const BASE = "/civicaid-voice";

/**
 * Voice Chat E2E Tests
 *
 * Tests the full voice recording flow across languages, error scenarios,
 * and edge cases. We stub MediaRecorder + getUserMedia + Audio to simulate
 * recording, and mock the backend for language-appropriate responses.
 */

/* ------------------------------------------------------------------ */
/*  Stubs: MediaRecorder + getUserMedia + Audio                        */
/* ------------------------------------------------------------------ */

async function stubBrowserAPIs(page: Page) {
  await page.addInitScript(() => {
    const tracker = {
      getUserMediaCalls: 0,
      recorderStartCalls: 0,
      recorderStopCalls: 0,
      lastMimeType: "",
    };
    (window as any).__voiceStub = tracker;

    /* Fake MediaStream */
    const fakeTrack = {
      kind: "audio", enabled: true, readyState: "live",
      stop() { this.readyState = "ended"; },
      getSettings: () => ({ sampleRate: 44100, channelCount: 1 }),
      addEventListener() {}, removeEventListener() {},
    };
    const fakeStream = {
      getTracks: () => [fakeTrack], getAudioTracks: () => [fakeTrack],
      getVideoTracks: () => [], active: true,
    };

    /* Stub getUserMedia */
    if (!navigator.mediaDevices) (navigator as any).mediaDevices = {};
    navigator.mediaDevices.getUserMedia = async () => {
      tracker.getUserMediaCalls++;
      return fakeStream as unknown as MediaStream;
    };

    /* Stub MediaRecorder */
    class FakeMediaRecorder extends EventTarget {
      state = "inactive";
      mimeType: string;
      ondataavailable: ((e: any) => void) | null = null;
      onstop: (() => void) | null = null;
      onerror: ((e: any) => void) | null = null;
      private _interval: any;

      stream: any;

      constructor(stream: any, options?: any) {
        super();
        this.stream = stream; // onstop handler calls recorder.stream.getTracks()
        this.mimeType = options?.mimeType || "audio/webm";
        tracker.lastMimeType = this.mimeType;
      }

      start(_timeslice?: number) {
        this.state = "recording";
        tracker.recorderStartCalls++;
        this._interval = setInterval(() => {
          if (this.state !== "recording") { clearInterval(this._interval); return; }
          const data = new Blob([new Uint8Array(256).fill(0)], { type: this.mimeType });
          const evt = new Event("dataavailable") as any;
          evt.data = data;
          this.ondataavailable?.(evt);
          this.dispatchEvent(evt);
        }, 100);
      }

      stop() {
        this.state = "inactive";
        tracker.recorderStopCalls++;
        clearInterval(this._interval);
        setTimeout(() => {
          const data = new Blob([new Uint8Array(512).fill(0)], { type: this.mimeType });
          const evt = new Event("dataavailable") as any;
          evt.data = data;
          this.ondataavailable?.(evt);
          this.dispatchEvent(evt);
          this.onstop?.();
          this.dispatchEvent(new Event("stop"));
        }, 50);
      }

      pause() { this.state = "paused"; }
      resume() { this.state = "recording"; }

      static isTypeSupported(mimeType: string) {
        return ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg;codecs=opus"].includes(mimeType);
      }
    }
    window.MediaRecorder = FakeMediaRecorder as any;

    /* Stub Audio (no real loading) */
    const OrigAudio = window.Audio;
    window.Audio = function () {
      const el = document.createElement("audio");
      Object.defineProperty(el, "crossOrigin", {
        get() { return el.getAttribute("crossorigin"); },
        set(v: string) { el.setAttribute("crossorigin", v); },
        configurable: true,
      });
      Object.defineProperty(el, "src", {
        get() { return el.getAttribute("data-src") || ""; },
        set(v: string) {
          el.setAttribute("data-src", v);
          Object.defineProperty(el, "duration", { value: 3, writable: true, configurable: true });
          Object.defineProperty(el, "readyState", { value: 4, writable: true, configurable: true });
          setTimeout(() => {
            el.dispatchEvent(new Event("loadedmetadata"));
            el.dispatchEvent(new Event("canplay"));
            el.dispatchEvent(new Event("canplaythrough"));
          }, 50);
        },
        configurable: true,
      });
      el.play = () => {
        el.dispatchEvent(new Event("play"));
        setTimeout(() => el.dispatchEvent(new Event("ended")), 200);
        return Promise.resolve();
      };
      return el as unknown as HTMLAudioElement;
    } as unknown as typeof Audio;
    window.Audio.prototype = OrigAudio.prototype;

    /* Stub AudioContext (silence beeps) */
    const OrigCtx = window.AudioContext;
    window.AudioContext = class extends OrigCtx {
      createOscillator() {
        const osc = super.createOscillator();
        osc.connect = () => osc as any;
        osc.start = () => {};
        osc.stop = () => {};
        return osc;
      }
    } as any;

    navigator.vibrate = () => true;
  });
}

/* ------------------------------------------------------------------ */
/*  Backend mock factory                                               */
/* ------------------------------------------------------------------ */

const MOCK_AUDIO_URL = "https://civicaid-voice.onrender.com/static/cache/resp.mp3";

interface MockOpts {
  responseLang?: string;
  responseText?: string;
  transcriptionFails?: boolean;
  networkError?: boolean;
  audioUrl?: string | null;
}

async function mockBackend(page: Page, opts: MockOpts = {}) {
  const {
    responseLang = "es",
    responseText = "El Ingreso Minimo Vital es una prestacion economica.",
    transcriptionFails = false,
    networkError = false,
    audioUrl = MOCK_AUDIO_URL,
  } = opts;

  await page.route("**/api/chat", async (route) => {
    if (networkError) { await route.abort("connectionfailed"); return; }
    if (transcriptionFails) {
      await route.fulfill({ status: 422, contentType: "application/json", body: JSON.stringify({ error: "audio_transcription_failed" }) });
      return;
    }
    await route.fulfill({
      status: 200, contentType: "application/json",
      body: JSON.stringify({ response: responseText, source: "llm", language: responseLang, duration_ms: 200, audio_url: audioUrl, sources: [] }),
    });
  });

  await page.route("**/api/tts", async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: audioUrl }) });
  });

  await page.route("**/*.mp3", async (route) => route.abort("blockedbyclient"));
}

/* ------------------------------------------------------------------ */
/*  Navigation — always use mode=text to avoid auto-opening overlay    */
/* ------------------------------------------------------------------ */

async function gotoChat(page: Page, lang = "es") {
  await page.goto(`${BASE}/chat?lang=${lang}&mode=text`, {
    waitUntil: "domcontentloaded",
  });
  await expect(page.getByText(/Clara/i).first()).toBeVisible({ timeout: 8_000 });
}

/* ------------------------------------------------------------------ */
/*  Helper: full voice recording cycle                                 */
/*  Uses the ChatInput mic button (inside .chat-form)                  */
/* ------------------------------------------------------------------ */

async function recordAndSend(page: Page, durationMs = 1500) {
  // The ChatInput mic button is inside the form at the bottom
  const chatForm = page.locator("form");
  const micBtn = chatForm.locator('button[type="button"]').filter({
    has: page.locator('svg'),
  }).last(); // mic is the last non-submit button in the form
  await expect(micBtn).toBeVisible({ timeout: 5_000 });
  await expect(micBtn).toBeEnabled();
  await micBtn.click();

  // Voice overlay should appear
  const overlay = page.locator('[role="dialog"]');
  await expect(overlay).toBeVisible({ timeout: 3_000 });

  // Tap the large (96x96) recording button inside the overlay to start
  // Use force:true because the button has a pulsing CSS animation
  const bigBtn = overlay.locator("button.w-touch-lg");
  await expect(bigBtn).toBeVisible();
  await bigBtn.click({ force: true });

  // Wait for recording to register (>1s guard)
  await page.waitForTimeout(durationMs);

  // Tap big button again to stop and send (also animated while recording)
  await bigBtn.click({ force: true });

  // Overlay should close after send
  await expect(overlay).not.toBeVisible({ timeout: 5_000 });
}

/* ================================================================== */
/*  Test Suite 1: Voice in Different Languages                         */
/* ================================================================== */

test.describe("Voice Chat — Multi-language", () => {
  const scenarios = [
    {
      lang: "es",
      responseText: "El IMV es una ayuda economica para personas vulnerables.",
      expectInChat: /IMV es una ayuda/i,
    },
    {
      lang: "en",
      responseText: "The Minimum Vital Income is a financial benefit for vulnerable people in Spain.",
      expectInChat: /Minimum Vital Income/i,
    },
    {
      lang: "fr",
      responseText: "Le Revenu Minimum Vital est une aide economique pour les personnes vulnerables.",
      expectInChat: /Revenu Minimum Vital/i,
    },
    {
      lang: "ar",
      responseText: "الحد الأدنى للدخل الحيوي هو مساعدة اقتصادية للأشخاص الضعفاء في إسبانيا.",
      expectInChat: /الحد الأدنى/,
    },
    {
      lang: "zh",
      responseText: "最低生活保障是西班牙为弱势群体提供的经济援助。",
      expectInChat: /最低生活保障/,
    },
  ];

  for (const s of scenarios) {
    test(`voice recording in ${s.lang.toUpperCase()} returns ${s.lang.toUpperCase()} response`, async ({ page }) => {
      await stubBrowserAPIs(page);
      await mockBackend(page, { responseLang: s.lang, responseText: s.responseText });
      await gotoChat(page, s.lang);

      await recordAndSend(page);

      await expect(page.getByText(s.expectInChat).first()).toBeVisible({ timeout: 10_000 });
    });
  }
});

/* ================================================================== */
/*  Test Suite 2: Backend receives correct language (our fix)          */
/* ================================================================== */

test.describe("Voice Chat — Language Respect", () => {
  test("API receives language=en when user selects English", async ({ page }) => {
    let capturedReq: any = null;

    await stubBrowserAPIs(page);
    await page.route("**/api/chat", async (route) => {
      capturedReq = route.request().postDataJSON();
      await route.fulfill({
        status: 200, contentType: "application/json",
        body: JSON.stringify({ response: "The IMV is a benefit.", source: "llm", language: "en", duration_ms: 150, audio_url: null, sources: [] }),
      });
    });
    await page.route("**/api/tts", async (route) => {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) });
    });

    await gotoChat(page, "en");
    await recordAndSend(page);

    await expect(page.getByText(/IMV is a benefit/i)).toBeVisible({ timeout: 10_000 });

    expect(capturedReq).not.toBeNull();
    expect(capturedReq.language).toBe("en");
    expect(capturedReq.input_type).toBe("audio");
    expect(capturedReq.audio_base64).toBeTruthy();
  });

  test("API receives language=fr when user selects French", async ({ page }) => {
    let capturedLang: string | null = null;

    await stubBrowserAPIs(page);
    await page.route("**/api/chat", async (route) => {
      capturedLang = route.request().postDataJSON().language;
      await route.fulfill({
        status: 200, contentType: "application/json",
        body: JSON.stringify({ response: "Le RMV est une aide.", source: "llm", language: "fr", duration_ms: 150, audio_url: null, sources: [] }),
      });
    });
    await page.route("**/api/tts", async (route) => {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) });
    });

    await gotoChat(page, "fr");
    await recordAndSend(page);

    await expect(page.getByText(/RMV est une aide/i)).toBeVisible({ timeout: 10_000 });
    expect(capturedLang).toBe("fr");
  });
});

/* ================================================================== */
/*  Test Suite 3: Transcription Errors (noise, silence, garbled)       */
/* ================================================================== */

test.describe("Voice Chat — Transcription Errors", () => {
  test("background noise: shows error when transcription fails (422)", async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page, { transcriptionFails: true });
    await gotoChat(page, "es");

    await recordAndSend(page);

    // 422 → audio category error → "No he podido entender el audio"
    await expect(
      page.getByText(/entender|audio|repetir|escribir/i).first(),
    ).toBeVisible({ timeout: 10_000 });
  });

  test("transcription failure offers action button", async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page, { transcriptionFails: true });
    await gotoChat(page, "es");

    await recordAndSend(page);

    // Error action button (Escribir)
    await expect(
      page.getByRole("button", { name: /Escribir/i }),
    ).toBeVisible({ timeout: 10_000 });
  });

  test("transcription failure in English shows English error message", async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page, { transcriptionFails: true });
    await gotoChat(page, "en");

    await recordAndSend(page);

    await expect(
      page.getByText(/understand|audio|repeat|type/i).first(),
    ).toBeVisible({ timeout: 10_000 });
  });

  test("network error during voice send shows connection error", async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page, { networkError: true });
    await gotoChat(page, "es");

    await recordAndSend(page);

    await expect(
      page.getByText(/conexion|wifi|datos/i).first(),
    ).toBeVisible({ timeout: 10_000 });
  });
});

/* ================================================================== */
/*  Test Suite 4: Recording UI States                                  */
/* ================================================================== */

test.describe("Voice Chat — Recording UI", () => {
  test.beforeEach(async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page);
    await gotoChat(page, "es");
  });

  test("mic button opens voice recording overlay", async ({ page }) => {
    const chatForm = page.locator("form");
    const micBtn = chatForm.locator('button[type="button"]').filter({ has: page.locator("svg") }).last();
    await micBtn.click();

    const overlay = page.locator('[role="dialog"]');
    await expect(overlay).toBeVisible();
  });

  test("timer counts up while recording", async ({ page }) => {
    const chatForm = page.locator("form");
    const micBtn = chatForm.locator('button[type="button"]').filter({ has: page.locator("svg") }).last();
    await micBtn.click();

    const overlay = page.locator('[role="dialog"]');
    await expect(overlay).toBeVisible();

    const bigBtn = overlay.locator("button.w-touch-lg");
    await bigBtn.click({ force: true });

    // Timer should tick past 0:01
    await expect(overlay.getByText(/0:0[1-9]/)).toBeVisible({ timeout: 3_000 });
  });

  test("cancel button discards recording and closes overlay", async ({ page }) => {
    const chatForm = page.locator("form");
    const micBtn = chatForm.locator('button[type="button"]').filter({ has: page.locator("svg") }).last();
    await micBtn.click();

    const overlay = page.locator('[role="dialog"]');
    const bigBtn = overlay.locator("button.w-touch-lg");
    await bigBtn.click({ force: true });
    await page.waitForTimeout(1_500);

    // Cancel (button is inside the overlay)
    const cancelBtn = overlay.getByLabel(/Cancelar|Cancel/i);
    await cancelBtn.click({ force: true });

    await expect(overlay).not.toBeVisible({ timeout: 5_000 });
  });

  test("Escape key cancels recording overlay", async ({ page }) => {
    const chatForm = page.locator("form");
    const micBtn = chatForm.locator('button[type="button"]').filter({ has: page.locator("svg") }).last();
    await micBtn.click();

    const overlay = page.locator('[role="dialog"]');
    await expect(overlay).toBeVisible();

    await page.keyboard.press("Escape");
    await expect(overlay).not.toBeVisible({ timeout: 3_000 });
  });

  test("user message shows microphone emoji after voice send", async ({ page }) => {
    await recordAndSend(page);

    // Voice messages show a microphone emoji as the user message text
    await expect(page.getByText("\u{1F3A4}")).toBeVisible({ timeout: 10_000 });
  });
});

/* ================================================================== */
/*  Test Suite 5: Edge Cases                                           */
/* ================================================================== */

test.describe("Voice Chat — Edge Cases", () => {
  test("very short recording (<1s) is ignored (double-tap guard)", async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page);
    await gotoChat(page, "es");

    const chatForm = page.locator("form");
    const micBtn = chatForm.locator('button[type="button"]').filter({ has: page.locator("svg") }).last();
    await micBtn.click();

    const overlay = page.locator('[role="dialog"]');
    const bigBtn = overlay.locator("button.w-touch-lg");
    await bigBtn.click({ force: true }); // start

    // Try to stop immediately (<1s) — should be ignored
    await page.waitForTimeout(200);
    await bigBtn.click({ force: true });

    // Overlay should still be visible (recording continues)
    await expect(overlay).toBeVisible();
  });

  test("mic button is disabled while Clara is loading", async ({ page }) => {
    await stubBrowserAPIs(page);
    await page.route("**/api/chat", async (route) => {
      await new Promise((r) => setTimeout(r, 5_000));
      await route.fulfill({
        status: 200, contentType: "application/json",
        body: JSON.stringify({ response: "OK", source: "llm", language: "es", duration_ms: 100, audio_url: null, sources: [] }),
      });
    });
    await page.route("**/api/tts", async (route) => {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) });
    });

    await gotoChat(page, "es");

    // Send text to trigger loading
    const input = page.locator('input[type="text"]');
    await input.fill("Hola");
    await input.press("Enter");

    // Mic button should be disabled during loading
    const chatForm = page.locator("form");
    const micBtn = chatForm.locator('button[type="button"]').filter({ has: page.locator("svg") }).last();
    await expect(micBtn).toBeDisabled({ timeout: 3_000 });
  });
});

/* ================================================================== */
/*  Test Suite 6: Voice + Audio playback integration                   */
/* ================================================================== */

test.describe("Voice Chat — Response with Audio", () => {
  test("voice question gets response with AudioPlayer", async ({ page }) => {
    await stubBrowserAPIs(page);
    await mockBackend(page, { responseText: "Clara responde con audio.", audioUrl: MOCK_AUDIO_URL });
    await gotoChat(page, "es");

    await recordAndSend(page);

    await expect(page.getByText("Clara responde con audio.")).toBeVisible({ timeout: 10_000 });

    // AudioPlayer play button should be present
    const playBtns = page.getByLabel(/Escuchar respuesta/i);
    expect(await playBtns.count()).toBeGreaterThanOrEqual(1);
  });
});
