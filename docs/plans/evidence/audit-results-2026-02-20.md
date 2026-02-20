# File System Audit Results — 2026-02-20

## T1: Empty Files
No empty .py/.md/.json files found.

## T2: Duplicate File Names
Most duplicates are expected (gates.md exists per quarter, README.md exists per directory, etc.).
Actionable duplicates checked in T13.

## T3: Large Files (>100KB)
- `design/assets/civic-tenderness-canvas.png` — design asset, keep
- `eval_report_q4_fix*.json` — root-level eval reports (to be moved)
- `docs/09-academic/Sprint3_*.pdf` — academic deliverables, keep
- `clara-web/.next/` — build cache, should be in .gitignore

## T4: Test Count
493 passed, 19 skipped, 5 xpassed (517 collected)

## T5: TODO/FIXME
Only 1 false positive found (test docstring containing "TODOS" the Spanish word).
No actual TODO/FIXME/HACK comments in source code.
