# Fase 2 — Backlog (remaining for Fase 3+)

## Completed (Fase 2)
- [x] MEM-01: Memory config flags
- [x] MEM-02: MemoryState schema + user hash
- [x] MEM-03: MemoryStore abstraction + dev backend
- [x] MEM-04: Redis backend
- [x] MEM-05: Tag sanitization
- [x] MEM-06: Memory-aware system prompt
- [x] MEM-07: Opt-in/forget command detection + templates
- [x] MEM-08: Pipeline integration
- [x] MEM-09: /forget admin endpoint
- [x] MEM-10: Memory observability logging
- [x] MEM-11: Health endpoint memory status
- [x] MEM-12: Multi-turn eval cases (25)
- [x] MEM-13: User isolation tests
- [x] MEM-14: Deploy config (render.yaml + conftest)
- [x] MEM-15: Final documentation + closing report

## Pending (Fase 3 candidates)

| ID | Title | Priority | Notes |
|----|-------|----------|-------|
| FASE3-MEMORY-01 | LLM-based conversation summary | Medium | Replace heuristic summary with LLM-generated summaries |
| FASE3-MEMORY-02 | Postgres backend option | Low | Add PostgreSQL as alternative to Redis |
| FASE3-OBS-01 | Memory size monitoring/alerts | Medium | Track memory usage, alert on growth |
| FASE3-SEC-01 | Rate limiting on /forget | Low | Prevent abuse of delete endpoint |
| FASE3-EVAL-01 | Summary quality evaluation | Medium | Eval how well summaries capture conversation |
| FASE3-MEMORY-03 | last_turns array (k<=12) | Low | Store last k turns for richer context |
| FASE3-MEMORY-04 | Slot extraction (ciudad, situacion) | Medium | Parse user info into structured slots |
| FASE3-MEMORY-05 | Memory compression for large states | Low | Compress old summaries to save Redis space |
| FASE3-RAG-01 | Vector RAG integration | High | Phase 3 core: vector search for KB |
| FASE3-TTS-01 | Premium TTS (ElevenLabs) | Low | Phase 4: better voice quality |
