# Source Registry

Machine-readable catalog of official Spanish government sources for Clara's RAG system.

## Files

| File | Description |
|------|-------------|
| `registry.yaml` | All AGE + CCAA sources (25 AGE + 19 CCAA = 44 entries) |
| `local_seed.yaml` | Top 20 municipal sedes + Tier 2-4 strategy metadata |

## How to Add a Source

1. Add a new entry under the appropriate `jurisdiction` section in `registry.yaml`
2. Required fields: `id`, `name`, `jurisdiction`, `tier`, `portal_url`, `priority`, `access_method`
3. Run validation: `python3 scripts/validate_source_registry.py`
4. If the source has a new domain, also add it to `data/policy/allowlist.yaml`

## Schema

See `schemas/SourceRegistry.v1.schema.json` for the full validation schema.
