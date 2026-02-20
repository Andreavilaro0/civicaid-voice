# Red Team Report -- Q1 Final

**Project:** CivicAid/Clara -- Biblioteca Oficial v0 (RAG Espana)
**Date:** 2026-02-19
**Branch:** fix/fase3-full-pass
**Commit:** deb42a9688cec73c820fbe4265845a370bc72600
**Auditor:** A5 Red Team Skeptic (Claude Opus 4.6)

---

## Vector 1: Misleading Denominators

**Investigation:** Searched all `.md` files under `q1-sources/` for patterns like `N/N` to find cherry-picked denominators that might hide failures. Examined Q1-REPORT.md, Q1.1-REPORT.md, gates.md, FULLPASS-CLOSING-REPORT.md, AH-AUDIT-REPORT-v6.md, and FORENSIC-AUDIT-REPORT.md.

**Finding:**

Three different gate count schemes exist across documents:
- Q1 (original): 6/6 gates (G1-G6) in `gates.md:88`
- FULLPASS: 8/8 gates (G1-G7 + G2-post) in `FULLPASS-CLOSING-REPORT.md:88`
- v6/final: 7/7 gates (G1-G7) in `AH-AUDIT-REPORT-v6.md:94`, `GATES-RESULTS.final.md:22`

This is not cherry-picking -- each represents a different scope at a different point in time, and the context makes the denominator clear. The Q1 original had 6 conceptual gates; FULLPASS added G7 (link checker dry-run) plus a post-fix rerun of G2; v6/final settled on 7 canonical gates.

The `3/3 URLs OK` claim in Q1.1-REPORT.md line 20 and line 93 accurately describes the link checker smoke test denominator. The forensic audit (line 103) correctly flagged this as "PARTIAL" because the full live test crashed at URL 12/18. The caveat is now present.

`5/5 PASS` for tests is accurate and verified in `COMMANDS-AND-OUTPUTS.log` (exit code 0).

`19/19 CCAA` is accurate -- 17 autonomous communities + 2 autonomous cities = 19.

No cherry-picked or misleading denominators found.

**Verdict:** PASS

---

## Vector 2: Scope Ambiguity in URL Coverage

**Investigation:** Read the v6 audit report (`AH-AUDIT-REPORT-v6.md`) and FULLPASS-CLOSING-REPORT.md. Checked whether the two URL coverage scopes (enforcement vs. docs+data) are clearly defined and distinguished.

**Finding:**

The v6 audit explicitly defines two formal scopes (lines 28-32):
1. **Enforcement scope** -- data files only (`data/sources/`, `data/policy/`): 125 URLs, 100% covered
2. **Docs+Data scope** -- all markdown + data files: 261 URLs, 7 non-gov NOT_COVERED

The FULLPASS-CLOSING-REPORT.md at line 69 includes a v6 note clarifying the historical scope confusion: "The coverage numbers above (268/11) were computed with an informal scope mixing data files and some markdown references."

However, a residual ambiguity remains: the Q1-REPORT.md at lines 72-76 describes the allowlist as "Tier 1 (AGE): `*.gob.es` auto-allowed + 22 explicit domains; Tier 2 (CCAA): 19 community domain patterns; Tier 3 (Municipal): 20 municipal domains" -- this reports only primary domains, not total matchable domains (which is 109 including aliases). This is technically accurate (22 entries, not 22 total matchable) but a reader could be confused.

**Verdict:** PASS (scopes are clearly defined in v6; minor ambiguity in primary-vs-total domain counts is a documentation quality issue, not a correctness issue)

---

## Vector 3: Allowlist Counting Confusion

**Investigation:** Programmatically counted allowlist.yaml domains and aliases. Cross-referenced against every doc that mentions allowlist counts.

**Finding:**

Actual allowlist counts (verified programmatically):
- tier_1_age: 22 primary domains + 10 aliases = 32 matchable
- tier_2_ccaa: 19 primary domains + 25 aliases = 44 matchable
- tier_3_municipal: 20 primary domains + 13 aliases = 33 matchable
- Grand total: 61 primary + 48 aliases = 109 matchable
- Auto-allow rules: 5
- File lines: 362

Documents consistently report "22 AGE domains", "19 CCAA domains", "20 municipal domains". The v6 ground truth (`AH-AUDIT-REPORT-v6.md:62-65`) clearly distinguishes: "tier_1_age: 22 domains (32 with aliases)". The GROUND-TRUTH.final.txt also makes this distinction: "T1: 22 domains + 10 aliases = 32".

The Q1.1-REPORT.md line 17 says "allowlist (22 AGE + 19 CCAA + 20 municipal domains)" -- this counts primary entries, which is consistent usage throughout. The `(32 with aliases)` qualifier appears in the ground truth and v6 audit where precision matters.

No conflation of lines/domains/aliases found.

**Verdict:** PASS

---

## Vector 4: Stale Historical Claims

**Investigation:** Read FORENSIC-AUDIT-REPORT.md for any claims that were accurate at writing time but are now stale. Checked for "3/3 PASS" test references and other time-sensitive numbers.

**Finding:**

The FORENSIC-AUDIT-REPORT.md contains two stale references:
1. Line 106: `Unit tests | 3/3 PASS | **3/3 PASS** | VERIFIED` -- This was accurate at the time of the original forensic audit (before AUDIT-04 added 2 negative tests). The "Fixes Applied" section (line 163+) documents that tests grew to 5/5 PASS.
2. Line 213: `pytest tests/unit/test_validators.py -v   # 3/3 PASS` -- Same issue; reflects pre-fix state.

These stale numbers are within a forensic audit document that is inherently point-in-time. The document title says "Date: 2026-02-18" and the "Fixes Applied" section (added at the bottom) updates to 5/5. The structure is: original findings at top, fixes at bottom. This is a reasonable forensic audit structure.

However, a reader scanning the Claims Ledger at line 106 might take "3/3 PASS" as the current state without reading the fixes section.

**Verdict:** NOTE -- The stale "3/3" references in the forensic audit are in a point-in-time document that documents its own fixes. Not misleading in context, but could confuse a hasty reader. Recommend adding a header note: "Numbers in the original claims ledger reflect pre-fix state; see Fixes Applied section for current values."

---

## Vector 5: "No Code Touched" Claim

**Investigation:** Ran `git log --oneline --name-only -- src/` and `git diff main..fix/fase3-full-pass --name-only -- src/` to verify no src/ files were modified by Q1 work. Also checked working tree and staged changes.

**Finding:**

`git diff main..fix/fase3-full-pass --name-only -- src/` returns empty -- zero src/ files changed between main and the fix branch. The working tree diff (`git diff HEAD -- src/`) is also empty.

The most recent commit touching `src/` is `deb42a9` ("Fase 1 polish + Fase 2 memory system") which is the HEAD commit on main and is the base for the Q1 branch -- not a Q1 change.

Q1.1-REPORT.md line 23 states: "No `src/` files touched -- all changes in `data/`, `schemas/`, `scripts/`, `tests/`, `docs/`". This is verified.

**Verdict:** PASS

---

## Vector 6: Invented URLs

**Investigation:** Extracted all unique domains from `registry.yaml` (64 domains) and `local_seed.yaml` (24 domains). Spot-checked 5 domains for plausibility as real Spanish government sites.

**Finding:**

All domains follow legitimate Spanish government naming patterns:
- AGE: `*.gob.es` (standard for central government), `boe.es`, `sepe.es`, `seg-social.es`
- CCAA: Regional TLDs (`.cat`, `.eus`, `.gal`) or `.es` variants (e.g., `www.juntadeandalucia.es`, `www.euskadi.eus`, `web.gencat.cat`)
- Local: Municipal patterns (`sede.madrid.es`, `sede.sevilla.org`, `seuelectronica.ajuntament.barcelona.cat`)
- Specialized: `sede.malaga.eu` (.eu for Malaga), `www.bilbao.eus` (Basque TLD), `sede.coruna.gal` (Galician TLD)

Spot-check of 5 domains:
1. `administracion.gob.es` -- Known Spanish government portal (PAG)
2. `www.boe.es` -- Boletin Oficial del Estado, real and well-known
3. `sede.comunidad.madrid` -- Uses `.madrid` TLD, real Community of Madrid sede
4. `sede.sevilla.org` -- Plausible municipal sede
5. `seuelectronica.ajuntament.barcelona.cat` -- Catalan naming ("seu electronica" = sede electronica in Catalan), `.cat` TLD

No obviously fabricated URLs detected. Domain patterns, TLDs, and naming conventions are all consistent with real Spanish government infrastructure. The BOE API URLs have been annotated as base paths requiring runtime parameters (per AUDIT-06 fix), which is accurate.

Note: HTTP validation is explicitly deferred to Q2. This vector only checks domain plausibility, not reachability.

**Verdict:** PASS

---

## Vector 7: Phantom Files

**Investigation:** Checked that every file path referenced in Q1.1-BIBLIOTECA-OFICIAL-v0-REPORT.md and FULLPASS-CLOSING-REPORT.md actually exists on disk.

**Finding:**

Q1.1 report references (18 paths checked):
- All 7 data files (registry.yaml, local_seed.yaml, READMEs, policy files): **ALL EXIST**
- All 3 schema files: **ALL EXIST**
- All 4 scripts: **ALL EXIST**
- Test file: **EXISTS**
- All 3 evidence samples: **ALL EXIST**

FULLPASS evidence pack (audit/fixes/):
- 4 markdown files (FULLPASS, DOCFIX, ALLOWLIST, GATES): **ALL EXIST**
- `evidence/` subdirectory with 10 evidence files: **ALL EXIST**
- `evidence/baseline/` with 5 pre-fix snapshots: **ALL EXIST**

v6 evidence pack:
- 16 evidence files listed in AH-AUDIT-REPORT-v6.md: **ALL 16 EXIST**
- 3 report files in `reports/`: **ALL EXIST** (00-recon.md, GATES-RESULTS.v6.md, A2-DOC-CONSISTENCY.v6.md)

One minor note: The FULLPASS report tree diagram mentions `SEMANTIC-CHANGES.md` but annotates it as "(integrated into DOCFIX)". This file does not exist standalone, but the annotation explains why. Not a phantom.

Zero phantom files detected.

**Verdict:** PASS

---

## Vector 8: Gates Claims vs Evidence

**Investigation:** Read `COMMANDS-AND-OUTPUTS.log` in the q1-final directory. Verified that every gate claimed as PASS has exit code 0 in the log.

**Finding:**

The log file contains verbatim output for 7 gates:

| Gate | Claimed | Exit Code in Log | Output Consistent |
|------|---------|-----------------|-------------------|
| G1 Registry | PASS (44+20) | `EXIT: 0` | Yes -- "PASS (44 sources -- AGE: 25, CCAA: 19, Local: 0)" + "PASS (20 sources)" |
| G2 Policy | PASS | `EXIT: 0` | Yes -- "allowlist.yaml: PASS, blocklist.yaml: PASS, canonical_rules.yaml: PASS" |
| G3 ProcedureDoc | PASS (0.86) | `EXIT: 0` | Yes -- "completeness: 0.86" |
| G4 collect-only | PASS (5 tests) | `EXIT: 0` | Yes -- "collected 5 items" |
| G5 pytest -v | PASS (5/5) | `EXIT: 0` | Yes -- "5 passed in 0.60s" |
| G6 ruff | PASS (0 errors) | `EXIT: 0` | Yes -- "All checks passed!" |
| G7 link_check dry-run | PASS (8 URLs) | `EXIT: 0` | Yes -- "Dry run complete. 8 URLs would be checked." |

All 7 gates have `EXIT: 0` and matching output. The log also includes timestamp (`2026-02-19 11:57:13 UTC`), branch (`fix/fase3-full-pass`), commit (`deb42a9`), and Python version (`3.11.8`).

No discrepancy between claimed results and evidence.

**Verdict:** PASS

---

## Vector 9: Schema Version Mismatch

**Investigation:** Read both JSON Schema files and checked their `$schema` and `$id` fields. Verified Draft 2020-12 compliance and consistency.

**Finding:**

ProcedureDoc.v1.schema.json (line 2):
- `$schema`: `https://json-schema.org/draft/2020-12/schema`
- `$id`: `https://civicaid-voice.local/schemas/ProcedureDoc.v1.schema.json`
- Properties: 29 (verified by counting `properties` keys)
- Required: 13 fields (verified by counting `required` array)

SourceRegistry.v1.schema.json (line 2):
- `$schema`: `https://json-schema.org/draft/2020-12/schema`
- `$id`: `https://civicaid-voice.local/schemas/SourceRegistry.v1.schema.json`
- Required per SourceEntry: 7 fields (id, name, jurisdiction, tier, priority, portal_url, access_method)
- Conditional requires: ccaa_code when jurisdiction=ccaa, municipality when jurisdiction=local

Both schemas:
- Reference Draft 2020-12 (consistent)
- Use `.local` domain for `$id` (appropriate for non-published schemas)
- Are validated by `validate_source_registry.py` and `validate_proceduredoc_schema.py` via `jsonschema.validate()`
- The validators successfully validate against their respective data files (verified in COMMANDS-AND-OUTPUTS.log)

No version mismatch detected.

**Verdict:** PASS

---

## Vector 10: Undeclared Internet Dependency

**Investigation:** Read all 4 validation scripts and the test file to check for any HTTP/network calls that would require internet access to pass.

**Finding:**

Scripts analyzed:
1. `scripts/validate_source_registry.py` -- Reads local YAML + JSON files only. Imports: yaml, jsonschema, json, sys, pathlib. **No network calls.**
2. `scripts/validate_policy.py` -- Reads local YAML files only. Imports: yaml, sys, pathlib. **No network calls.**
3. `scripts/validate_proceduredoc_schema.py` -- Reads local JSON files only. Imports: jsonschema, json, sys, pathlib. **No network calls.**
4. `scripts/link_check.py` -- DOES use `urllib.request` for HTTP calls, BUT gates only run it in `--dry-run` mode (as confirmed in COMMANDS-AND-OUTPUTS.log: "Dry run complete. 8 URLs would be checked."). Dry-run mode does NOT make HTTP calls; it only lists URLs. **No network dependency in gate execution.**
5. `tests/unit/test_validators.py` -- Runs the 3 validator scripts via subprocess. Tests use `_run()` helper that calls `subprocess.run()` on local scripts. **No network calls.**

The `jsonschema` library performs local-only validation (it does NOT fetch `$schema` URLs). The `$id` and `$schema` fields are metadata; the library validates against the schema object passed in-memory.

No undeclared internet dependency.

**Verdict:** PASS

---

## Overall Verdict: PASS

All 10 attack vectors investigated. Results:

| Vector | Name | Verdict |
|--------|------|---------|
| 1 | Misleading denominators | PASS |
| 2 | Scope ambiguity in URL coverage | PASS |
| 3 | Allowlist counting confusion | PASS |
| 4 | Stale historical claims | NOTE |
| 5 | "No code touched" claim | PASS |
| 6 | Invented URLs | PASS |
| 7 | Phantom files | PASS |
| 8 | Gates claims vs evidence | PASS |
| 9 | Schema version mismatch | PASS |
| 10 | Undeclared internet dependency | PASS |

**9 PASS, 1 NOTE, 0 FAIL**

The single NOTE (Vector 4) is a cosmetic concern: the forensic audit report contains pre-fix test counts ("3/3 PASS") in its claims ledger that could confuse a reader who doesn't read the "Fixes Applied" section at the bottom. This is inherent to point-in-time documents and does not constitute a factual error in the current state of the project.

**Conclusion:** The Q1 Biblioteca Oficial v0 artifacts pass red team scrutiny. Documentation is internally consistent with data files. All gates produce exit code 0 with matching output. No fabricated URLs, phantom files, misleading denominators, internet dependencies, or schema mismatches found.

---

*Generated 2026-02-19 by A5 Red Team Skeptic*
*Auditor: Claude Code (Opus 4.6)*
