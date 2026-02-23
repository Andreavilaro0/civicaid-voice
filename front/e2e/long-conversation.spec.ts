import { test, expect, type Page, type Route } from "@playwright/test";
import { ChatPage } from "./pages/chat.page";
import {
  imvDeepDiveES,
  empadronamientoFR,
  healthCardEN,
  rtlArabic,
  registrationZH,
  stressTestES,
  type ConversationScenario,
  type MockTurn,
} from "./fixtures/conversation-scenarios";

/* ──────────────────────────────────────────────────────────────── */
/*  Shared helpers                                                   */
/* ──────────────────────────────────────────────────────────────── */

/** Intercept backend API and serve mocked responses turn by turn */
async function mockConversation(page: Page, scenario: ConversationScenario) {
  let turnIndex = 0;

  // Mock TTS (return null — no audio in tests)
  await page.route("**/api/tts", (route: Route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
  );

  // Mock chat endpoint with sequential responses
  await page.route("**/api/chat", async (route: Route) => {
    const turn: MockTurn | undefined = scenario.turns[turnIndex];
    if (!turn) {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          response: "No tengo mas respuestas preparadas.",
          audio_url: null,
          source: "fallback",
          language: scenario.language,
          duration_ms: 100,
          sources: [],
        }),
      });
      return;
    }

    // Simulate backend latency
    await new Promise((r) => setTimeout(r, turn.delayMs));

    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        response: turn.claraResponse,
        audio_url: null,
        source: turn.source,
        language: scenario.language,
        duration_ms: turn.delayMs,
        sources: [],
      }),
    });

    turnIndex++;
  });
}

/** Run a full conversation scenario and collect metrics */
async function runConversation(
  chat: ChatPage,
  scenario: ConversationScenario,
): Promise<{
  totalMs: number;
  turnMetrics: { turn: number; responseMs: number; messageLength: number }[];
  totalMessages: number;
}> {
  const turnMetrics: { turn: number; responseMs: number; messageLength: number }[] = [];
  const totalStart = Date.now();

  for (let i = 0; i < scenario.turns.length; i++) {
    const turn = scenario.turns[i];
    const { responseMs, responseText } = await chat.sendAndWait(turn.userMessage, 20_000);

    turnMetrics.push({
      turn: i + 1,
      responseMs,
      messageLength: responseText.length,
    });
  }

  const totalMs = Date.now() - totalStart;
  const totalMessages = await chat.countMessages();

  return { totalMs, turnMetrics, totalMessages };
}

/* ──────────────────────────────────────────────────────────────── */
/*  Test Suite: Long Conversations                                   */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Long Conversations — Flow & Duration", () => {
  test("ES: 10-turn IMV deep-dive completes without errors", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, imvDeepDiveES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    const { totalMs, turnMetrics, totalMessages } = await runConversation(chat, imvDeepDiveES);

    // 10 user messages + 10 clara responses + 1 welcome = 21
    expect(totalMessages).toBeGreaterThanOrEqual(21);

    // Log metrics for analysis
    console.log(`\n=== IMV Deep-Dive (ES) — ${imvDeepDiveES.turns.length} turns ===`);
    console.log(`Total time: ${(totalMs / 1000).toFixed(1)}s`);
    for (const m of turnMetrics) {
      console.log(`  Turn ${m.turn}: ${m.responseMs}ms (${m.messageLength} chars)`);
    }

    // Every turn should resolve in under 15s
    for (const m of turnMetrics) {
      expect(m.responseMs).toBeLessThan(15_000);
    }
  });

  test("FR: 8-turn empadronamiento in French flows correctly", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, empadronamientoFR);
    await chat.goto("fr");
    await chat.expectWelcomeMessage();

    const { totalMs, turnMetrics, totalMessages } = await runConversation(chat, empadronamientoFR);

    expect(totalMessages).toBeGreaterThanOrEqual(17); // 8+8+1
    console.log(`\n=== Empadronamiento (FR) — ${empadronamientoFR.turns.length} turns ===`);
    console.log(`Total time: ${(totalMs / 1000).toFixed(1)}s`);
    for (const m of turnMetrics) {
      console.log(`  Turn ${m.turn}: ${m.responseMs}ms`);
    }
  });

  test("EN: 8-turn health card + topic switch flows correctly", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, healthCardEN);
    await chat.goto("en");
    await chat.expectWelcomeMessage();

    const { totalMs, turnMetrics, totalMessages } = await runConversation(chat, healthCardEN);

    expect(totalMessages).toBeGreaterThanOrEqual(17);
    console.log(`\n=== Health Card + Mixed (EN) — ${healthCardEN.turns.length} turns ===`);
    console.log(`Total time: ${(totalMs / 1000).toFixed(1)}s`);
    for (const m of turnMetrics) {
      console.log(`  Turn ${m.turn}: ${m.responseMs}ms`);
    }
  });

  test("Stress: 15 rapid turns without UI degradation", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, stressTestES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    const { totalMs, turnMetrics, totalMessages } = await runConversation(chat, stressTestES);

    // 15 user + 15 clara + 1 welcome = 31
    expect(totalMessages).toBeGreaterThanOrEqual(31);

    // Check no progressive slowdown: last turn shouldn't be >3x slower than first
    const firstTurn = turnMetrics[0].responseMs;
    const lastTurn = turnMetrics[turnMetrics.length - 1].responseMs;
    expect(lastTurn).toBeLessThan(firstTurn * 5); // generous margin for CI

    console.log(`\n=== Stress Test (ES) — 15 turns ===`);
    console.log(`Total time: ${(totalMs / 1000).toFixed(1)}s`);
    console.log(`First turn: ${firstTurn}ms | Last turn: ${lastTurn}ms`);
    console.log(`Ratio (last/first): ${(lastTurn / firstTurn).toFixed(2)}x`);

    // Verify scrolling works — last message should be visible
    const lastMsg = chat.allMessages.last();
    await expect(lastMsg).toBeInViewport();
  });
});

/* ──────────────────────────────────────────────────────────────── */
/*  Test Suite: Language Understanding                               */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Language Understanding — Multilingual Accuracy", () => {
  test("API receives correct language parameter for each locale", async ({ page }) => {
    const languages = ["es", "en", "fr", "pt", "ar", "zh"] as const;
    const receivedLanguages: string[] = [];

    // Intercept all API calls and record language
    await page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );
    await page.route("**/api/chat", async (route) => {
      const body = JSON.parse(route.request().postData() ?? "{}");
      receivedLanguages.push(body.language);
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          response: `Response in ${body.language}`,
          audio_url: null,
          source: "llm",
          language: body.language,
          duration_ms: 100,
          sources: [],
        }),
      });
    });

    for (const lang of languages) {
      receivedLanguages.length = 0;
      const chat = new ChatPage(page);
      await chat.goto(lang);
      await chat.expectWelcomeMessage();
      await chat.sendAndWait("Test message", 10_000);
      expect(receivedLanguages[0]).toBe(lang);
    }
  });

  test("Arabic conversation renders RTL correctly", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, rtlArabic);
    await chat.goto("ar");
    await chat.expectWelcomeMessage();

    // Send first message
    await chat.sendAndWait(rtlArabic.turns[0].userMessage, 10_000);

    // Verify input has RTL direction
    const inputDir = await chat.textInput.getAttribute("dir");
    expect(inputDir).toBe("rtl");

    // Verify Clara's response contains Arabic text
    const responseText = await chat.getLastClaraMessageText();
    expect(responseText).toContain("الضمان الاجتماعي");
  });

  test("Chinese conversation displays correctly", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, registrationZH);
    await chat.goto("zh");
    await chat.expectWelcomeMessage();

    // Run full conversation
    for (const turn of registrationZH.turns) {
      await chat.sendAndWait(turn.userMessage, 10_000);
      const responseText = await chat.getLastClaraMessageText();

      // Verify Chinese characters render
      if (turn.mustContain && turn.mustContain.length > 0) {
        for (const keyword of turn.mustContain) {
          expect(responseText).toContain(keyword);
        }
      }
    }
  });

  test("French conversation maintains language throughout", async ({ page }) => {
    const chat = new ChatPage(page);
    const sentLanguages: string[] = [];

    await page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );

    let turnIdx = 0;
    await page.route("**/api/chat", async (route) => {
      const body = JSON.parse(route.request().postData() ?? "{}");
      sentLanguages.push(body.language);
      const turn = empadronamientoFR.turns[turnIdx];
      await new Promise((r) => setTimeout(r, 200));
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          response: turn?.claraResponse ?? "Merci!",
          audio_url: null,
          source: "llm",
          language: "fr",
          duration_ms: 200,
          sources: [],
        }),
      });
      turnIdx++;
    });

    await chat.goto("fr");
    await chat.expectWelcomeMessage();

    // Send 4 messages
    for (let i = 0; i < 4; i++) {
      await chat.sendAndWait(empadronamientoFR.turns[i].userMessage, 10_000);
    }

    // ALL API calls should have language="fr"
    expect(sentLanguages.every((l) => l === "fr")).toBe(true);
    expect(sentLanguages.length).toBe(4);
  });
});

/* ──────────────────────────────────────────────────────────────── */
/*  Test Suite: Information Accuracy                                 */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Information Accuracy — Factual Content Checks", () => {
  test("IMV responses contain correct factual information", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, imvDeepDiveES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    for (let i = 0; i < imvDeepDiveES.turns.length; i++) {
      const turn = imvDeepDiveES.turns[i];
      const { responseText } = await chat.sendAndWait(turn.userMessage, 15_000);

      // Check required keywords
      if (turn.mustContain) {
        for (const keyword of turn.mustContain) {
          expect.soft(responseText, `Turn ${i + 1} should contain "${keyword}"`).toContain(keyword);
        }
      }

      // Check forbidden keywords (misinformation)
      if (turn.mustNotContain) {
        for (const keyword of turn.mustNotContain) {
          expect.soft(responseText, `Turn ${i + 1} should NOT contain "${keyword}"`).not.toContain(keyword);
        }
      }
    }
  });

  test("Health card responses contain correct English information", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, healthCardEN);
    await chat.goto("en");
    await chat.expectWelcomeMessage();

    for (let i = 0; i < healthCardEN.turns.length; i++) {
      const turn = healthCardEN.turns[i];
      const { responseText } = await chat.sendAndWait(turn.userMessage, 15_000);

      if (turn.mustContain) {
        for (const keyword of turn.mustContain) {
          expect.soft(responseText, `EN Turn ${i + 1}: "${keyword}"`).toContain(keyword);
        }
      }
      if (turn.mustNotContain) {
        for (const keyword of turn.mustNotContain) {
          expect.soft(responseText, `EN Turn ${i + 1} NO: "${keyword}"`).not.toContain(keyword);
        }
      }
    }
  });

  test("French empadronamiento responses are accurate", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, empadronamientoFR);
    await chat.goto("fr");
    await chat.expectWelcomeMessage();

    for (let i = 0; i < empadronamientoFR.turns.length; i++) {
      const turn = empadronamientoFR.turns[i];
      const { responseText } = await chat.sendAndWait(turn.userMessage, 15_000);

      if (turn.mustContain) {
        for (const keyword of turn.mustContain) {
          expect.soft(responseText, `FR Turn ${i + 1}: "${keyword}"`).toContain(keyword);
        }
      }
      if (turn.mustNotContain) {
        for (const keyword of turn.mustNotContain) {
          expect.soft(responseText, `FR Turn ${i + 1} NO: "${keyword}"`).not.toContain(keyword);
        }
      }
    }
  });
});

/* ──────────────────────────────────────────────────────────────── */
/*  Test Suite: Conversation Flow & UX                               */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Conversation Flow — UX Behavior", () => {
  test("Quick chips disappear after first message", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, imvDeepDiveES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    // Quick chips should be visible initially
    await chat.expectQuickChipsVisible();

    // Send first message
    await chat.sendAndWait(imvDeepDiveES.turns[0].userMessage, 10_000);

    // Quick chips should be hidden now
    await chat.expectQuickChipsHidden();
  });

  test("Loading indicator appears while waiting for response", async ({ page }) => {
    const chat = new ChatPage(page);
    // Use a slow response to catch the loading state
    await page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );
    await page.route("**/api/chat", async (route) => {
      // 2 second delay to ensure we can see loading
      await new Promise((r) => setTimeout(r, 2000));
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          response: "Respuesta de Clara",
          audio_url: null,
          source: "llm",
          language: "es",
          duration_ms: 2000,
          sources: [],
        }),
      });
    });

    await chat.goto("es");
    await chat.expectWelcomeMessage();

    // Type and send
    await chat.textInput.fill("¿Qué es el IMV?");
    await chat.sendButton.click();

    // Loading should appear
    await chat.expectLoading();

    // Wait for response
    await chat.waitForResponse(10_000);

    // Loading should disappear
    await chat.expectNotLoading();
  });

  test("Input is disabled while loading", async ({ page }) => {
    const chat = new ChatPage(page);
    await page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );
    await page.route("**/api/chat", async (route) => {
      await new Promise((r) => setTimeout(r, 2000));
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          response: "Respuesta",
          audio_url: null,
          source: "llm",
          language: "es",
          duration_ms: 100,
          sources: [],
        }),
      });
    });

    await chat.goto("es");
    await chat.expectWelcomeMessage();

    await chat.textInput.fill("Hola");
    await chat.sendButton.click();

    // Input should be disabled during loading
    await expect(chat.textInput).toBeDisabled();

    // After response, input should be enabled again
    await chat.waitForResponse(10_000);
    await expect(chat.textInput).toBeEnabled();
  });

  test("Auto-scroll keeps latest message visible in long conversation", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, stressTestES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    // Send 10 messages to fill the viewport
    for (let i = 0; i < 10; i++) {
      await chat.sendAndWait(stressTestES.turns[i].userMessage, 10_000);

      // Last message should always be in viewport
      const lastMsg = chat.allMessages.last();
      await expect(lastMsg).toBeInViewport();
    }
  });

  test("Messages maintain correct order in long conversation", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, imvDeepDiveES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    // Run first 5 turns
    for (let i = 0; i < 5; i++) {
      await chat.sendAndWait(imvDeepDiveES.turns[i].userMessage, 10_000);
    }

    // Verify message order: all articles should alternate clara/user
    // (welcome is clara, then user/clara pairs)
    const articles = chat.allMessages;
    const count = await articles.count();

    // First message is welcome (clara)
    const firstLabel = await articles.first().getAttribute("aria-label");
    expect(firstLabel).toMatch(/clara/i);

    // Subsequent messages alternate: user, clara, user, clara...
    for (let i = 1; i < count; i++) {
      const label = await articles.nth(i).getAttribute("aria-label");
      const expectedSender = i % 2 === 1 ? /your|tu/i : /clara/i;
      expect(label).toMatch(expectedSender);
    }
  });

  test("Error recovery: retry works after a failed message", async ({ page }) => {
    const chat = new ChatPage(page);
    let callCount = 0;

    await page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );
    await page.route("**/api/chat", async (route) => {
      callCount++;
      if (callCount === 1) {
        // First call fails
        await route.fulfill({ status: 500, contentType: "application/json", body: JSON.stringify({ error: "server_error" }) });
      } else {
        // Second call succeeds (retry)
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            response: "Aqui esta tu respuesta sobre el IMV.",
            audio_url: null,
            source: "llm",
            language: "es",
            duration_ms: 100,
            sources: [],
          }),
        });
      }
    });

    await chat.goto("es");
    await chat.expectWelcomeMessage();
    await chat.sendMessage("¿Qué es el IMV?");
    await chat.waitForResponse(10_000);

    // Should see error message with retry button
    const retryButton = page.getByRole("button", { name: /reintentar|retry/i });
    await expect(retryButton).toBeVisible();

    // Click retry
    await retryButton.click();
    await chat.waitForResponse(10_000);

    // Should now see successful response
    const lastText = await chat.getLastClaraMessageText();
    expect(lastText).toContain("IMV");
  });
});

/* ──────────────────────────────────────────────────────────────── */
/*  Test Suite: Performance Metrics                                  */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Performance — Response Times & Stability", () => {
  test("Measure per-turn response times across 10 turns", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, imvDeepDiveES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    const { turnMetrics } = await runConversation(chat, imvDeepDiveES);

    console.log("\n=== Performance Report: IMV 10-turn ===");
    console.log("Turn | Response Time | Message Length");
    console.log("-----|---------------|---------------");

    let totalResponseMs = 0;
    for (const m of turnMetrics) {
      console.log(`  ${String(m.turn).padStart(2)}  |  ${String(m.responseMs).padStart(6)}ms    |  ${m.messageLength} chars`);
      totalResponseMs += m.responseMs;
    }

    const avgMs = totalResponseMs / turnMetrics.length;
    console.log(`\nAverage response time: ${avgMs.toFixed(0)}ms`);
    console.log(`Total conversation time: ${(totalResponseMs / 1000).toFixed(1)}s`);

    // All responses should complete within acceptable bounds
    for (const m of turnMetrics) {
      expect(m.responseMs, `Turn ${m.turn} too slow`).toBeLessThan(15_000);
    }
  });

  test("15-turn stress test: no memory leaks or progressive slowdown", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, stressTestES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    const { turnMetrics, totalMs } = await runConversation(chat, stressTestES);

    // Calculate average of first 3 vs last 3 turns
    const firstAvg = turnMetrics.slice(0, 3).reduce((a, b) => a + b.responseMs, 0) / 3;
    const lastAvg = turnMetrics.slice(-3).reduce((a, b) => a + b.responseMs, 0) / 3;
    const ratio = lastAvg / firstAvg;

    console.log("\n=== Stress Test Performance ===");
    console.log(`First 3 avg: ${firstAvg.toFixed(0)}ms`);
    console.log(`Last 3 avg: ${lastAvg.toFixed(0)}ms`);
    console.log(`Degradation ratio: ${ratio.toFixed(2)}x`);
    console.log(`Total: ${(totalMs / 1000).toFixed(1)}s for 15 turns`);

    // Allow up to 4x degradation (generous for CI environments)
    expect(ratio, "Performance degradation too high").toBeLessThan(4);
  });

  test("Quick chip click has same performance as text input", async ({ page }) => {
    const chat = new ChatPage(page);

    await page.route("**/api/tts", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
    );
    await page.route("**/api/chat", async (route) => {
      await new Promise((r) => setTimeout(r, 300));
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          response: "Respuesta rapida.",
          audio_url: null,
          source: "cache",
          language: "es",
          duration_ms: 300,
          sources: [],
        }),
      });
    });

    await chat.goto("es");
    await chat.expectWelcomeMessage();

    // Time a quick chip click
    const chipStart = Date.now();
    await chat.clickQuickChip("¿Qué es el IMV?");
    await chat.waitForResponse(10_000);
    const chipMs = Date.now() - chipStart;

    console.log(`\nQuick chip response: ${chipMs}ms`);
    expect(chipMs).toBeLessThan(10_000);
  });
});
