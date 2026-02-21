#!/usr/bin/env python3
"""Validate a ProcedureDoc JSON against ProcedureDoc.v1.schema.json."""
import json
import sys
from pathlib import Path

import jsonschema

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "schemas" / "ProcedureDoc.v1.schema.json"


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path-to-proceduredoc.json>")
        return 1
    doc_path = Path(sys.argv[1])
    if not doc_path.is_absolute():
        doc_path = Path.cwd() / doc_path
    if not doc_path.exists():
        print(f"ERROR: File not found: {doc_path}")
        return 1
    with open(SCHEMA) as f:
        schema = json.load(f)
    with open(doc_path) as f:
        doc = json.load(f)
    try:
        jsonschema.validate(instance=doc, schema=schema)
        print(f"PASS: {doc_path.name} valid against ProcedureDoc v1")
        print(f"  id: {doc.get('id')}")
        print(f"  nombre: {doc.get('nombre')}")
        print(f"  completeness: {doc.get('completeness_score')}")
        return 0
    except jsonschema.ValidationError as e:
        print(f"FAIL: {doc_path.name}")
        print(f"  Error: {e.message}")
        path = ".".join(str(p) for p in e.absolute_path)
        if path:
            print(f"  Path: {path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
