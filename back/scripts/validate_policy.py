#!/usr/bin/env python3
"""Validate policy YAML files for structural correctness."""
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
POLICY = REPO / "data" / "policy"


def load_yaml(p):
    with open(p) as f:
        return yaml.safe_load(f)


def check_allowlist(data):
    errors = []
    if data.get("default_action") != "reject":
        errors.append("default_action should be 'reject'")
    for section in ["tier_1_age", "tier_2_ccaa"]:
        section_data = data.get(section)
        if not section_data:
            errors.append(f"Missing or empty '{section}'")
            continue
        # Support both flat list and {description, domains} object
        if isinstance(section_data, dict):
            items = section_data.get("domains", [])
        elif isinstance(section_data, list):
            items = section_data
        else:
            errors.append(f"'{section}' has unexpected type {type(section_data).__name__}")
            continue
        if not items:
            errors.append(f"'{section}' has no domains")
        for entry in items:
            if isinstance(entry, dict) and "domain" not in entry:
                errors.append(f"Entry in {section} missing 'domain'")
        if section == "tier_1_age" and len(items) < 10:
            errors.append(f"tier_1_age has {len(items)} domains (need >= 10)")
        if section == "tier_2_ccaa" and len(items) < 15:
            errors.append(f"tier_2_ccaa has {len(items)} entries (need >= 15)")
    return errors


def check_blocklist(data):
    errors = []
    cats = data.get("categories", [])
    if not cats:
        errors.append("Missing 'categories'")
    for c in cats:
        if "category" not in c:
            errors.append("Category entry missing 'category' field")
        if not c.get("domains") and not c.get("reason"):
            errors.append(f"Category '{c.get('category','?')}' has no domains or reason")
    if "patterns" not in data:
        errors.append("Missing 'patterns'")
    return errors


def check_canonical(data):
    errors = []
    rules = data.get("rules", [])
    if len(rules) < 10:
        errors.append(f"Only {len(rules)} rules (need >= 10)")
    if "tracking_params_strip" not in data:
        errors.append("Missing 'tracking_params_strip'")
    if "session_params_strip" not in data:
        errors.append("Missing 'session_params_strip'")
    return errors


CHECKS = {
    "allowlist.yaml": check_allowlist,
    "blocklist.yaml": check_blocklist,
    "canonical_rules.yaml": check_canonical,
}


def main():
    print("=== Policy Validation ===\n")
    ok = True
    for fname, checker in CHECKS.items():
        path = POLICY / fname
        if not path.exists():
            print(f"  {fname}: MISSING")
            ok = False
            continue
        errors = checker(load_yaml(path))
        if errors:
            print(f"  {fname}: FAIL")
            for e in errors:
                print(f"    - {e}")
            ok = False
        else:
            print(f"  {fname}: PASS")
    print()
    print("PASS: All policy files valid." if ok else "FAIL: Policy validation errors found.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
