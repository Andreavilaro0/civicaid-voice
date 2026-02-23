import { test, expect, type Page, type Route } from "@playwright/test";
import { ChatPage } from "./pages/chat.page";
import { COMPREHENSIVE_SCENARIOS } from "./fixtures/scenarios-comprehensive";
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
/*  All scenarios combined                                           */
/* ──────────────────────────────────────────────────────────────── */

const ALL: ConversationScenario[] = [
  ...COMPREHENSIVE_SCENARIOS,
  imvDeepDiveES,
  empadronamientoFR,
  healthCardEN,
  rtlArabic,
  registrationZH,
];

/* ──────────────────────────────────────────────────────────────── */
/*  Shared helpers                                                   */
/* ──────────────────────────────────────────────────────────────── */

async function mockConversation(page: Page, scenario: ConversationScenario) {
  let turnIndex = 0;

  await page.route("**/api/tts", (route: Route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
  );

  await page.route("**/api/chat", async (route: Route) => {
    const turn: MockTurn | undefined = scenario.turns[turnIndex];
    if (!turn) {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ response: "Fin.", audio_url: null, source: "fallback", language: scenario.language, duration_ms: 100, sources: [] }),
      });
      return;
    }
    await new Promise((r) => setTimeout(r, Math.min(turn.delayMs, 500))); // cap delay for test speed
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

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 1: Full conversation flow (21 tests)                      */
/*  Verify each scenario runs to completion without errors           */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Full Conversation Flow", () => {
  for (const scenario of ALL) {
    test(`${scenario.name}: ${scenario.turns.length}-turn conversation completes`, async ({ page }) => {
      const chat = new ChatPage(page);
      await mockConversation(page, scenario);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      const metrics: number[] = [];
      for (let i = 0; i < scenario.turns.length; i++) {
        const { responseMs } = await chat.sendAndWait(scenario.turns[i].userMessage, 20_000);
        metrics.push(responseMs);
      }

      // Verify all messages rendered: welcome + (user + clara) * turns
      const totalExpected = 1 + scenario.turns.length * 2;
      const actual = await chat.countMessages();
      expect(actual).toBeGreaterThanOrEqual(totalExpected);

      // Log summary
      const avg = metrics.reduce((a, b) => a + b, 0) / metrics.length;
      console.log(`  ${scenario.name}: ${scenario.turns.length} turns, avg ${avg.toFixed(0)}ms/turn`);
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 2: Factual accuracy per turn (21 tests)                   */
/*  Verify mustContain/mustNotContain keywords                       */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Factual Accuracy", () => {
  for (const scenario of ALL) {
    const hasChecks = scenario.turns.some((t) => (t.mustContain && t.mustContain.length > 0) || (t.mustNotContain && t.mustNotContain.length > 0));
    if (!hasChecks) continue;

    test(`${scenario.name}: responses contain correct factual information`, async ({ page }) => {
      const chat = new ChatPage(page);
      await mockConversation(page, scenario);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      for (let i = 0; i < scenario.turns.length; i++) {
        const turn = scenario.turns[i];
        const { responseText } = await chat.sendAndWait(turn.userMessage, 20_000);

        if (turn.mustContain) {
          for (const kw of turn.mustContain) {
            expect.soft(responseText.toLowerCase(), `[${scenario.name}] Turn ${i + 1}: must contain "${kw}"`).toContain(kw.toLowerCase());
          }
        }
        if (turn.mustNotContain) {
          for (const kw of turn.mustNotContain) {
            expect.soft(responseText.toLowerCase(), `[${scenario.name}] Turn ${i + 1}: must NOT contain "${kw}"`).not.toContain(kw.toLowerCase());
          }
        }
      }
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 3: Language consistency (21 tests)                         */
/*  API always receives the correct language parameter                */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Language Consistency", () => {
  for (const scenario of ALL) {
    test(`${scenario.name}: API receives lang=${scenario.language} on every turn`, async ({ page }) => {
      const receivedLangs: string[] = [];
      let turnIdx = 0;

      await page.route("**/api/tts", (route) =>
        route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ audio_url: null }) }),
      );

      await page.route("**/api/chat", async (route) => {
        const body = JSON.parse(route.request().postData() ?? "{}");
        receivedLangs.push(body.language);
        const turn = scenario.turns[turnIdx];
        await new Promise((r) => setTimeout(r, 200));
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            response: turn?.claraResponse ?? "OK",
            audio_url: null,
            source: "llm",
            language: scenario.language,
            duration_ms: 200,
            sources: [],
          }),
        });
        turnIdx++;
      });

      const chat = new ChatPage(page);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      // Send first 3 turns (enough to verify consistency)
      const turnsToSend = Math.min(3, scenario.turns.length);
      for (let i = 0; i < turnsToSend; i++) {
        await chat.sendAndWait(scenario.turns[i].userMessage, 10_000);
      }

      expect(receivedLangs.length).toBe(turnsToSend);
      for (const lang of receivedLangs) {
        expect(lang).toBe(scenario.language);
      }
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 4: Performance per scenario (21 tests)                     */
/*  Measure and report response times                                */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Performance Metrics", () => {
  for (const scenario of ALL) {
    test(`${scenario.name}: all turns under 15s, no progressive slowdown`, async ({ page }) => {
      const chat = new ChatPage(page);
      await mockConversation(page, scenario);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      const times: number[] = [];
      for (let i = 0; i < scenario.turns.length; i++) {
        const { responseMs } = await chat.sendAndWait(scenario.turns[i].userMessage, 20_000);
        times.push(responseMs);
        expect(responseMs, `Turn ${i + 1} too slow`).toBeLessThan(15_000);
      }

      // Check no severe degradation
      if (times.length >= 4) {
        const firstHalf = times.slice(0, Math.floor(times.length / 2));
        const secondHalf = times.slice(Math.floor(times.length / 2));
        const avgFirst = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
        const avgSecond = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;
        const ratio = avgSecond / avgFirst;
        expect(ratio, "Performance degradation > 4x").toBeLessThan(4);
      }
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 5: URL & contact verification (specific scenarios)         */
/*  Verify real URLs, phones, and addresses appear correctly          */
/* ──────────────────────────────────────────────────────────────── */

test.describe("URLs, Phones & Addresses", () => {
  const urlScenarios = [
    {
      scenario: COMPREHENSIVE_SCENARIOS[0], // NIE/TIE
      checks: [
        { turn: 1, keywords: ["sede.administracionespublicas.gob.es", "Garcia de Paredes"] },
        { turn: 3, keywords: ["790", "012", "12"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[1], // Asilo
      checks: [
        { turn: 0, keywords: ["Pradillo, 40", "OAR"] },
        { turn: 2, keywords: ["91 441 55 00", "91 532 74 78", "900 22 22 92"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[2], // Asistencia juridica
      checks: [
        { turn: 2, keywords: ["Serrano, 9", "91 788 93 80"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[4], // SEPE
      checks: [
        { turn: 0, keywords: ["sepe.es", "901 119 999"] },
        { turn: 3, keywords: ["Sepulveda"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[5], // Discapacidad
      checks: [
        { turn: 0, keywords: ["Maudes, 26", "91 580 37 38"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[6], // Violencia genero
      checks: [
        { turn: 0, keywords: ["016", "112", "600 000 016", "016-online@igualdad.gob.es"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[12], // Salud mental
      checks: [
        { turn: 0, keywords: ["717 003 717", "024"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[13], // Permiso conducir
      checks: [
        { turn: 0, keywords: ["sede.dgt.gob.es"] },
        { turn: 1, keywords: ["28,30"] },
      ],
    },
    {
      scenario: COMPREHENSIVE_SCENARIOS[8], // Nacionalidad
      checks: [
        { turn: 1, keywords: ["CCSE", "DELE A2", "examenes.cervantes.es"] },
        { turn: 2, keywords: ["85 EUR", "25 preguntas"] },
        { turn: 6, keywords: ["790-026", "104 EUR"] },
      ],
    },
  ];

  for (const { scenario, checks } of urlScenarios) {
    test(`${scenario.name}: URLs/phones/addresses render correctly`, async ({ page }) => {
      const chat = new ChatPage(page);
      await mockConversation(page, scenario);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      // Only send up to the max turn we need to check
      const maxTurn = Math.max(...checks.map((c) => c.turn));
      for (let i = 0; i <= maxTurn; i++) {
        const { responseText } = await chat.sendAndWait(scenario.turns[i].userMessage, 20_000);

        const check = checks.find((c) => c.turn === i);
        if (check) {
          for (const kw of check.keywords) {
            expect.soft(responseText, `${scenario.name} turn ${i}: "${kw}"`).toContain(kw);
          }
        }
      }
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 6: Auto-scroll in long conversations (5 tests)             */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Auto-scroll Long Conversations", () => {
  const longScenarios = ALL.filter((s) => s.turns.length >= 8).slice(0, 5);

  for (const scenario of longScenarios) {
    test(`${scenario.name}: last message stays in viewport`, async ({ page }) => {
      const chat = new ChatPage(page);
      await mockConversation(page, scenario);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      for (let i = 0; i < scenario.turns.length; i++) {
        await chat.sendAndWait(scenario.turns[i].userMessage, 20_000);
      }

      // Last message should be visible
      const lastMsg = chat.allMessages.last();
      await expect(lastMsg).toBeInViewport();
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 7: Message ordering (5 tests)                              */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Message Order Integrity", () => {
  const orderScenarios = ALL.filter((s) => s.turns.length >= 6).slice(0, 5);

  for (const scenario of orderScenarios) {
    test(`${scenario.name}: messages alternate correctly`, async ({ page }) => {
      const chat = new ChatPage(page);
      await mockConversation(page, scenario);
      await chat.goto(scenario.language);
      await chat.expectWelcomeMessage();

      // Send first 4 turns
      for (let i = 0; i < 4; i++) {
        await chat.sendAndWait(scenario.turns[i].userMessage, 20_000);
      }

      // Verify order: welcome(clara), user, clara, user, clara, ...
      const articles = chat.allMessages;
      const count = await articles.count();
      expect(count).toBeGreaterThanOrEqual(9); // 1 welcome + 4*2

      // First is always Clara (welcome)
      const firstLabel = await articles.first().getAttribute("aria-label");
      expect(firstLabel).toMatch(/clara/i);

      // Subsequent alternate: user, clara, user, clara
      for (let i = 1; i < Math.min(count, 9); i++) {
        const label = await articles.nth(i).getAttribute("aria-label");
        const expected = i % 2 === 1 ? /your|tu/i : /clara/i;
        expect.soft(label, `Message ${i} sender`).toMatch(expected);
      }
    });
  }
});

/* ──────────────────────────────────────────────────────────────── */
/*  SUITE 8: Stress test (1 test — 15-turn rapid fire)               */
/* ──────────────────────────────────────────────────────────────── */

test.describe("Stress Test", () => {
  test("15-turn rapid conversation: no crashes, all messages render", async ({ page }) => {
    const chat = new ChatPage(page);
    await mockConversation(page, stressTestES);
    await chat.goto("es");
    await chat.expectWelcomeMessage();

    for (let i = 0; i < stressTestES.turns.length; i++) {
      await chat.sendAndWait(stressTestES.turns[i].userMessage, 20_000);
    }

    const total = await chat.countMessages();
    expect(total).toBeGreaterThanOrEqual(31); // 1 + 15*2

    const lastMsg = chat.allMessages.last();
    await expect(lastMsg).toBeInViewport();
  });
});
