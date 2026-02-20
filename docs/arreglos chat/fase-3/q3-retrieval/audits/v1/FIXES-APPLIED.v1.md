# Q3 Fixes Applied — v1

**Date:** 2026-02-19
**Auditor:** Claude Code (prompt-engineer mode)

## Summary

| Priority | Count | Types |
|----------|-------|-------|
| P0 (security) | 2 | CODE-FIX, PROMPT-FIX |
| P1 (drift) | 9 | DOC-FIX |
| **Total** | **11** | |

## Fixes

| # | Priority | Hallazgo | Tipo | Archivo(s) | Cambio | Status |
|---|----------|----------|------|-----------|--------|--------|
| 1 | P0 | RT-14a: chunks_block no en rule 11 | PROMPT-FIX | system_prompt.py:22 | Agregado "CHUNKS RECUPERADOS" a rule 11 data-only blocks | DONE |
| 2 | P0 | RT-14b/c: chunk content sin sanitizar, [Cn] spoofable | CODE-FIX | llm_generate.py:38-44 | Agregado escape de `[C` en content_preview y brackets en section_name | DONE |
| 3 | P1 | "83 tests nuevos" → 86 def test_ | DOC-FIX | Q3-CLOSING-REPORT.md:18 | Corregido a "86 tests nuevos (83 passed + 3 skipped)" | DONE |
| 4 | P1 | Tabla header "83 tests" | DOC-FIX | Q3-CLOSING-REPORT.md:42 | Corregido a "86 def test_ — 83 passed, 3 skipped" | DONE |
| 5 | P1 | Metricas "Tests nuevos Q3: 83" | DOC-FIX | Q3-CLOSING-REPORT.md:103 | Corregido a "86 (83 passed + 3 skipped)" | DONE |
| 6 | P1 | G11 "PASS (83)" | DOC-FIX | Q3-CLOSING-REPORT.md:81 | Corregido a "PASS (86 def test_, 83 passed)" | DONE |
| 7 | P1 | synonyms.py LOC 73 → 72 | DOC-FIX | Q3-CLOSING-REPORT.md:26 | Corregido a 72 | DONE |
| 8 | P1 | reranker.py LOC 197 → 196 | DOC-FIX | Q3-CLOSING-REPORT.md:27 | Corregido a 196 | DONE |
| 9 | P1 | Design D2 "gemini (default)" | DOC-FIX | Q3-DESIGN.md:29-30 | Corregido a "gemini (alta precision)" y "heuristic (default)" | DONE |
| 10 | P1 | Design LOC 73/197/~228/~115 | DOC-FIX | Q3-DESIGN.md:91-94 | Corregido a 72/196/226/116 (wc -l) | DONE |
| 11 | P1 | Design "65 unit + 18 integration" | DOC-FIX | Q3-DESIGN.md:116 | Corregido a "65 unit + 21 integration/eval; 83 passed + 3 skipped" | DONE |

## Post-Fix Verification

```
$ PYTHONPATH=. pytest tests/ --tb=short -q
347 passed, 11 skipped, 5 xpassed, 1 warning in 3.21s

$ ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
All checks passed!
```

0 regresiones. Todos los fixes verificados.

---

## Round 1 — P0 Security Fixes (RT-13, RT-14a, G-S1/RT-14b)

**Date:** 2026-02-19
**Applied by:** fixer agent

| # | Priority | Finding | Type | File | Change | Status |
|---|----------|---------|------|------|--------|--------|
| 12 | P0 | RT-13: user_text raw injection | PROMPT-FIX | llm_generate.py:120 | Added escape_xml_tags(user_text) before prompt assembly | FIXED |
| 13 | P0 | RT-14a: source_url unsanitized | PROMPT-FIX | llm_generate.py:50-51 | Added escape_xml_tags + zero-width space defense to source_url | FIXED |
| 14 | P0 | G-S1/RT-14b: content_preview incomplete | PROMPT-FIX | llm_generate.py:42 | Added escape_xml_tags() to content_preview before zero-width space defense | FIXED |

### Details

**P0-1 (RT-13): user_text**
- Before: `user_text` injected raw into `<user_query>` tags
- After: `escape_xml_tags(user_text)` applied; sanitized value used in prompt
- Attack prevented: User sending `</user_query>` to break out of data block

**P0-2 (RT-14a): source_url**
- Before: `chunk['source_url']` injected raw into prompt
- After: `escape_xml_tags()` + zero-width space `[C` defense applied
- Attack prevented: Compromised KB entry injecting prompt instructions via URL field

**P0-3 (G-S1/RT-14b): content_preview**
- Before: Only zero-width space defense for `[C` patterns; no XML tag escaping
- After: `escape_xml_tags(content)` applied BEFORE the existing zero-width space defense
- Attack prevented: XML tag injection via content_preview field

### Round 1 Post-Fix Verification
- Tests: 347 passed, 11 skipped, 5 xpassed, 0 failed
- Lint: All checks passed (ruff E,F,W)
- Security gates: G-S1 PASS, G-S3 PASS, G-S4 PASS
- Evidence: `docs/arreglos chat/fase-3/q3-retrieval/evidence/GATES-POSTFIX.v1.log`

---

## Round 2 — Audit Protocol Fixes (G-U2 lint, Drift snapshot, RT-13 defense-in-depth)

**Date:** 2026-02-20
**Applied by:** fixer agent (T9-T11)

| # | Priority | Finding | Type | File | Change | Status |
|---|----------|---------|------|------|--------|--------|
| FIX-1a | P0 | G-U2 lint F401 | TEST-FIX | test_fallback_chain.py:9 | Remove unused `import pytest` | DONE |
| FIX-1b | P0 | G-U2 lint F401 | TEST-FIX | test_boe_monitor.py:6 | Remove unused `MagicMock` from import | DONE |
| FIX-1c | P0 | G-U2 lint F401 | TEST-FIX | test_directory.py:3 | Remove unused `import pytest` | DONE |
| FIX-1d | P0 | G-U2 lint F401 | TEST-FIX | test_fallback_retriever.py:6 | Remove unused `import pytest` | DONE |
| FIX-1e | P0 | G-U2 lint F841 | TEST-FIX | test_ingestion.py:135 | Remove unused `doc_data` assignment | DONE |
| FIX-1f | P0 | G-U2 lint F401 | TEST-FIX | test_response_cache.py:4 | Remove unused `patch` from import | DONE |
| FIX-1g | P0 | G-U2 lint F401 | TEST-FIX | test_response_cache.py:6 | Remove unused `import pytest` | DONE |
| FIX-2a | P1 | Drift D1-D10 | DOC-FIX | Q3-CLOSING-REPORT.md | Add Snapshot header declaring Q3 closing state | DONE |
| FIX-2b | P1 | Drift D1-D10 | DOC-FIX | Q3-DESIGN.md | Add Snapshot header declaring Q3 closing state | DONE |
| FIX-2c | P1 | Drift D1-D10 | DOC-FIX | evidence/gates.md | Add Snapshot header declaring Q3 closing state | DONE |
| FIX-3 | P2 | RT-13 kb_context | CODE-FIX | llm_generate.py:78 | Apply escape_xml_tags() to _build_kb_context JSON output | DONE |

### Round 2 Post-Fix Verification

```
$ PYTHONPATH=. pytest tests/ -q --tb=no
493 passed, 19 skipped, 5 xpassed in 4.25s

$ ruff check src/ tests/ scripts/ --select E,F,W --ignore E501
All checks passed!

$ PYTHONPATH=. python3 -c "import src.app; print('OK')"
OK
```

0 regressions. All 3 gates PASS. All Round 2 fixes verified.
