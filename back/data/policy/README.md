# Link Governance Policy

Machine-readable rules for domain trust, URL canonicalization, and citation governance.

## Files

| File | Description |
|------|-------------|
| `allowlist.yaml` | Domains Clara may crawl/cite, organized by tier |
| `blocklist.yaml` | Domains always rejected (commercial, SEO, forums, etc.) |
| `canonical_rules.yaml` | URL normalization rules (10 rules) + params to strip |

## How the Policy is Applied

1. **Crawl time:** Before fetching any URL, check `allowlist.yaml`. Reject if not listed (or if in `blocklist.yaml`).
2. **Store time:** Canonicalize every URL using rules in `canonical_rules.yaml` before storing.
3. **Cite time:** Clara only cites URLs from Tier 1-3 allowed domains. Prefer informative links over homepages.

## Validation

Run: `python3 scripts/validate_policy.py`
