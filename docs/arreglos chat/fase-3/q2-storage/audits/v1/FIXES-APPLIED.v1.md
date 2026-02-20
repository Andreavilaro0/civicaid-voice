# Q2 Audit v1 — Fixes Applied (Round 2)

**Date:** 2026-02-19
**Auditor:** team-lead (manual)
**Input:** DRIFT-CHECK.v1.md (10 DRIFTs), RED-TEAM-REPORT.v1.md (2 FAILs)

---

## Fixes Applied

| # | Priority | DRIFT/FAIL | Fix | File(s) |
|---|----------|-----------|-----|---------|
| 1 | **P0** | Q2-DESIGN.md Feature Flags table: `models/text-embedding-004` | Changed to `models/gemini-embedding-001` | Q2-DESIGN.md line 85 |
| 2 | **P1** | "72 new tests" across all docs | Changed to "80 new RAG tests" (9+16+6+11+30+4+4) with note that G9 runs 72 unit only | Q2-CLOSING-REPORT.md (lines 12, 64, 92, 106), gates.md (lines 21, 111, 118), README.md (line 119) |
| 3 | **P1** | "test_migrator.py (20)" | Changed to "(30)" | Q2-CLOSING-REPORT.md line 69 |
| 4 | **P1** | Missing test counts for test_rag_models.py and test_store.py | Added "(9)" and "(11)" respectively | Q2-CLOSING-REPORT.md E9 section |
| 5 | **P1** | "197 existing tests" / "269 total" inconsistent with def test_ counts | Added clarifying breakdown: 80 RAG + 193 non-RAG = 273 def test_, 277 collected by pytest (includes parametrized). Verbatim gate outputs preserved. | gates.md line 118 |
| 6 | **P1** | G10 description "269 total (264+5 xpassed)" | Updated to "277 collected: 264 passed, 8 skipped, 5 xpassed" | Q2-CLOSING-REPORT.md, gates.md |
| 7 | **P1** | Main README Q2 row says "Pendiente" | Changed to "CERRADA" with description, added Q2 section to index | docs/arreglos chat/README.md |

## Counting Methodology Note

The test count discrepancy stems from three different counting methods:

1. **`def test_` count** (source-level): 273 total (80 RAG + 193 non-RAG)
2. **`pytest --collect-only`** (collected): 277 total (includes parametrized/generated tests)
3. **G9 gate** (unit RAG only): 72 passed (excludes 8 integration tests requiring Docker)
4. **G10 gate** (full run): 277 collected, 264 passed + 8 skipped + 5 xpassed

All verbatim gate outputs are preserved as-is (they are real pytest output). Summary claims now use the `def test_` count (80 new) with notes explaining the G9/G10 methodology difference.

## Fixes NOT Applied (NOTE items)

The following DRIFT-CHECK items are NOTEs (not fixable from code alone):

- Chunk/word counts (20 chunks, 3,879 words) — DB-dependent, internally consistent
- pgvector version 0.8.1 — Docker-dependent, verbatim evidence provided
- Ruff "0 errors" — requires running ruff, gate evidence says "All checks passed!"
- G6 score=0.7666 — DB-dependent, from live query

## RED-TEAM Fixes

| Vector | Original Status | Fix |
|--------|----------------|-----|
| RT-09: Test count denominator | FAIL | Fixed: clarified 80 total RAG tests, explained G9 = 72 unit subset |
| RT-10: Counting confusion | FAIL | Fixed: added counting methodology note, reconciled all 3 methods |

---

*Generated 2026-02-19 by Q2 audit v1 Round 2*
