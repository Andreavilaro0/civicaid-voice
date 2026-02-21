# JSON Schemas

Validation schemas for Clara's data artifacts.

## Files

| File | Description |
|------|-------------|
| `SourceRegistry.v1.schema.json` | Schema for `data/sources/registry.yaml` and `local_seed.yaml` |
| `ProcedureDoc.v1.schema.json` | Schema for normalized procedure documents (future `data/ingested/`) |

## Usage

```bash
python3 scripts/validate_source_registry.py
python3 scripts/validate_proceduredoc_schema.py data/tramites/imv.json
python3 scripts/validate_policy.py
```
