#!/usr/bin/env python3
"""Validate source registry YAML files against JSON Schema."""
import json
import sys
from pathlib import Path

import yaml
import jsonschema

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "schemas" / "SourceRegistry.v1.schema.json"
REGISTRY = REPO / "data" / "sources" / "registry.yaml"
LOCAL = REPO / "data" / "sources" / "local_seed.yaml"


def load_yaml(p):
    with open(p) as f:
        return yaml.safe_load(f)


def load_json(p):
    with open(p) as f:
        return json.load(f)


def validate(data, schema, name):
    try:
        jsonschema.validate(instance=data, schema=schema)
        sources = data.get("sources", [])
        age = sum(1 for s in sources if s.get("jurisdiction") == "age")
        ccaa = sum(1 for s in sources if s.get("jurisdiction") == "ccaa")
        local = sum(1 for s in sources if s.get("jurisdiction") == "local")
        print(f"  {name}: PASS ({len(sources)} sources — AGE: {age}, CCAA: {ccaa}, Local: {local})")
        return True
    except jsonschema.ValidationError as e:
        print(f"  {name}: FAIL — {e.message}")
        path = ".".join(str(p) for p in e.absolute_path)
        if path:
            print(f"    Path: {path}")
        return False


def main():
    print("=== Source Registry Validation ===\n")
    schema = load_json(SCHEMA)
    ok = True
    for path in [REGISTRY, LOCAL]:
        if path.exists():
            if not validate(load_yaml(path), schema, path.name):
                ok = False
        else:
            print(f"  {path.name}: MISSING")
            ok = False
    print()
    print("PASS: All source registry files valid." if ok else "FAIL: Validation errors found.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
