# Contradictions Fixed — Phase 3 Anti-Humo

> Generated: 2026-02-13
> Agent: claims-librarian
> Total contradictions detected: 6
> Scope: Documentation-only audit (no code edits per file ownership rules)

## Contradictions Found

| # | File | Before (Incorrect) | After (Correct Value) | CLM ref | Fix Status |
|---|------|--------------------|-----------------------|---------|------------|
| 1 | docs/00-EXECUTIVE-SUMMARY.md:57 | "Skills en pipeline: **10**" | Should be "Skills en pipeline: **11**" (11 .py files in src/core/skills/ excl __init__.py) | CLM-032 | DETECTED — fix outside my file ownership |
| 2 | docs/00-EXECUTIVE-SUMMARY.md:58 | "Feature flags: **10**" | Should be "Feature flags: **9**" (9 flags listed in CLAUDE.md and verified in config.py) | CLM-033 | DETECTED — fix outside my file ownership |
| 3 | docs/00-EXECUTIVE-SUMMARY.md:118 | "Fase 3 -- Demo en Vivo \| EN CURSO" | Should be "Fase 3 -- Demo en Vivo \| COMPLETADA" (Phase 3 closed per CLAUDE.md + PHASE-STATUS.md) | CLM-034 | DETECTED — fix outside my file ownership |
| 4 | docs/06-integrations/NOTION-OS.md:3 | Header: "75 entradas" | Should be "81 entradas" to match line 41 data (43 Backlog + 12 KB + 26 Testing = 81). 75 was Phase 2 count. | CLM-035 | DETECTED — fix outside my file ownership |
| 5 | docs/07-evidence/PHASE-1-EVIDENCE.md:62 | Cache count command: `json.load(...)['entries']` | JSON is a plain array, not `{"entries": [...]}`. Command should be `len(json.load(open('data/cache/demo_cache.json')))`. Result (8) is still correct. | CLM-037 | DETECTED — fix outside my file ownership |
| 6 | docs/07-evidence/PHASE-2-EVIDENCE.md:223 | "test_guardrails.py \| 18 \| ..." | Actual count is 19 `def test_` functions. TEST-PLAN.md also says 19. | CLM-036 | DETECTED — fix outside my file ownership |

## Notes

- **File ownership constraint**: This agent (claims-librarian) is only authorized to write to `docs/07-evidence/artifacts/phase3/2026-02-13_0030/`. The contradictions above exist in files owned by other agents (Docs/Architecture, Release/PM). The fixes are documented here for the responsible agents to apply.
- **Severity**: All contradictions are cosmetic/documentation-level. No code bugs found. The codebase behavior is correct.
- **Historical accuracy**: Some "contradictions" (like PHASE-STATUS.md showing 75 Notion entries for Phase 2) are historically correct for the phase they document. Only cross-phase references that show stale data are flagged.

## Previously Fixed Contradictions (Phase 1 Hardening)

Per CLAUDE.md "Fixes Aplicados" section, 9 fixes were applied in Phase 1:

1. DEMO_MODE implemented in pipeline.py (was dead code) -- **Verified fixed** (CLM-012)
2. WHISPER_ON short-circuit for audio -- **Partially superseded** by Gemini refactor (CLM-018)
3. Twilio REST timeout (10s) in send_response.py -- **Verified fixed** (CLM-013)
4. NumMedia safe parsing (try/except) in webhook.py -- **Verified fixed** (CLM-014)
5. Silent thread death protection in pipeline.py -- **Verified fixed** (CLM-015)
6. Twilio webhook signature validation (RequestValidator) -- **Verified fixed** (CLM-009)
7. Docker build fix (setuptools<75 + --no-build-isolation) -- **Superseded** by Whisper removal (CLM-041)
8. .dockerignore creado -- **Verified fixed** (CLM-016)
9. Unused import time removed from logger.py -- **Verified fixed** (CLM-042)

## Recommended Actions

1. **EXEC-SUMMARY owner** should update lines 57, 58, and 118 to match verified values (11 skills, 9 flags, Phase 3 COMPLETADA).
2. **NOTION-OS.md owner** should update the header summary from "75 entradas" to "81 entradas".
3. **PHASE-1-EVIDENCE owner** should fix the cache count command syntax (remove `['entries']`).
4. **PHASE-2-EVIDENCE owner** should update test_guardrails count from 18 to 19.
