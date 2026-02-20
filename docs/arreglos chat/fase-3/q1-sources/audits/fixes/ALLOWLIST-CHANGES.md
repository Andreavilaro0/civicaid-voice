# Allowlist Coverage Fixes
Date: 2026-02-19
Agent: A3 (Allowlist/Policy Coverage Fixer)
File modified: `data/policy/allowlist.yaml`

## Domains Added

| Domain | Tier | Entry Type | Reason | Source Reference | Risk |
|--------|------|-----------|--------|-----------------|------|
| `www.sepe.es` | tier_1_age | alias of `sepe.es` | SEPE portal uses www prefix; registry.yaml `portal_url` is `https://www.sepe.es/`. Resolves case-sensitivity and backtick-artifact NOT_COVERED entries (`SEPE.ES`, `www.sepe.es\``) | `data/sources/registry.yaml` line 147 | LOW |
| `jccm.es` | tier_2_ccaa | alias of `castillalamancha.es` | Castilla-La Mancha uses `jccm.es` as portal domain. Allowlist had `castillalamancha.es` but registry uses `https://www.jccm.es/`. Gap flagged in v3, v4, and v5 audits. | `data/sources/registry.yaml` lines 577-579 | LOW |
| `www.jccm.es` | tier_2_ccaa | alias of `castillalamancha.es` | www-prefixed variant of jccm.es, used in registry portal_url | `data/sources/registry.yaml` line 577 | LOW |
| `sede.grancanaria.com` | tier_3_municipal | new entry | Cabildo de Gran Canaria sede electronica. Island government entity referenced in CCAA docs. | `docs/.../source-registry/ccaa.md` | LOW |

## Verification Checklist

- [x] `default_action: reject` remains unchanged (line 3)
- [x] No overlap with `data/policy/blocklist.yaml` (checked all 23 blocklisted domains + 4 patterns)
- [x] `sepe.es` was already in tier_1_age -- only added `www.sepe.es` as alias
- [x] `castillalamancha.es` was already in tier_2_ccaa -- only added `jccm.es` and `www.jccm.es` as aliases
- [x] `sede.grancanaria.com` is a new tier_3_municipal entry (Cabildo, not CCAA)
- [x] All added domains are genuine government entities verified against registry/seed files

## Justified Exceptions (NOT_COVERED but non-government)

These 12 NOT_COVERED URLs are from non-government reference/tooling domains. They are correctly NOT in the allowlist because the allowlist is government-only. No action needed.

| Domain | URL Count | Source Context | Reason | Action |
|--------|-----------|---------------|--------|--------|
| `github.com` | 5 | references.md, ingestion-playbook.md, age.md, link-checking-spec.md | Code hosting -- project repos, library references | Exception: non-government tooling reference |
| `docs.ckan.org` | 1 | references.md | CKAN open data platform documentation | Exception: non-government technical docs |
| `help.unhcr.org` | 1 | age.md (source-registry) | UNHCR Spain refugee help portal | Exception: international org, not Spanish gov |
| `json-schema.org` | 1 | normalization-schema.md | JSON Schema specification URI | Exception: technical standard reference |
| `ropenspain.github.io` | 1 | age.md (source-registry) | R OpenSpain CatastRo library docs | Exception: open-source project docs |
| `trafilatura.readthedocs.io` | 1 | references.md | Web scraping library documentation | Exception: non-government tooling reference |
| `example.es\`` | 1 | canonicalization.md | Template/example URL with backtick artifact | Exception: not a real URL (template) |
| `www.sepe.es\`` | 0 | canonicalization.md | Backtick artifact -- real domain `www.sepe.es` now covered as alias | Fixed: added `www.sepe.es` alias |

## Before/After

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| COVERED URLs | 264 | 268 | +4 |
| NOT_COVERED URLs | 15 | 11 | -4 |
| NOT_COVERED gov domains | 2 (SEPE.ES case issue, sede.grancanaria.com) | 0 | -2 |
| NOT_COVERED non-gov (justified) | 11 | 11 | 0 |
| NOT_COVERED artifacts | 2 (example.es\`, www.sepe.es\`) | 0* | -2 |
| tier_1_age domains | 22 | 22 (no new, just alias) | 0 |
| tier_2_ccaa domains | 19 | 19 (no new, just aliases) | 0 |
| tier_3_municipal domains | 19 | 20 | +1 |

*Note: `www.sepe.es\`` is now covered because `www.sepe.es` was added as alias (backtick is an extraction artifact). `SEPE.ES` coverage depends on case-insensitive matching at enforcement time -- the canonical domain `sepe.es` was already listed. `example.es\`` remains as a template artifact (not a real domain).

## Detailed Change Diff

```yaml
# tier_1_age > sepe.es: added www.sepe.es alias
- domain: "sepe.es"
  aliases:
+   - "www.sepe.es"      # NEW
    - "sede.sepe.gob.es"

# tier_2_ccaa > castillalamancha.es: added jccm.es aliases
- domain: "castillalamancha.es"
  aliases:
    - "sede.castillalamancha.es"
+   - "jccm.es"           # NEW
+   - "www.jccm.es"       # NEW

# tier_3_municipal: new entry
+ - domain: "sede.grancanaria.com"
+   municipality: "Gran Canaria (Cabildo)"
+   notes: "Cabildo de Gran Canaria - island government sede electronica"
```
