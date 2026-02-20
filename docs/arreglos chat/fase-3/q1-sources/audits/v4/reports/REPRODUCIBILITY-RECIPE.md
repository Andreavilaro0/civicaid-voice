# Reproducibility Recipe -- Audit v4

**Date:** 2026-02-18
**Purpose:** Commands to independently reproduce all evidence used in Anti-Hallucination Audit v4.
**Prerequisites:** Python 3.11+, venv with `pyyaml` and `jsonschema` installed.

---

## Setup

```bash
# Navigate to project root
cd /Users/andreaavila/Documents/hakaton/civicaid-voice

# Activate virtual environment
source .venv/bin/activate

# Verify dependencies
python3 -c "import yaml; print(f'pyyaml: {yaml.__version__}')"
python3 -c "import jsonschema; print(f'jsonschema: {jsonschema.__version__}')"  # 4.26.0
```

---

## G1: Source Registry Validation

```bash
python3 scripts/validate_source_registry.py
```

**Expected output:**
```
=== Source Registry Validation ===

  registry.yaml: PASS (44 sources — AGE: 25, CCAA: 19, Local: 0)
  local_seed.yaml: PASS (20 sources — AGE: 0, CCAA: 0, Local: 20)

PASS: All source registry files valid.
```

**Exit code:** 0

---

## G2: Policy Validation

```bash
python3 scripts/validate_policy.py
```

**Expected output:**
```
=== Policy Validation ===

  allowlist.yaml: PASS
  blocklist.yaml: PASS
  canonical_rules.yaml: PASS

PASS: All policy files valid.
```

**Exit code:** 0

---

## G3: ProcedureDoc Schema Validation

```bash
python3 scripts/validate_proceduredoc_schema.py \
  "docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"
```

**Expected output:**
```
PASS: proceduredoc.sample.json valid against ProcedureDoc v1
  id: age-inss-ingreso-minimo-vital
  nombre: Ingreso Minimo Vital
  completeness: 0.86
```

**Exit code:** 0

---

## Unit Tests (pytest)

```bash
pytest tests/unit/test_validators.py -v
```

**Expected output:**
```
tests/unit/test_validators.py::TestValidateSourceRegistry::test_validates PASSED
tests/unit/test_validators.py::TestValidatePolicy::test_validates PASSED
tests/unit/test_validators.py::TestValidateProcedureDoc::test_sample_validates PASSED
tests/unit/test_validators.py::TestValidateProcedureDoc::test_invalid_proceduredoc_rejected PASSED
tests/unit/test_validators.py::TestValidateProcedureDoc::test_missing_file_rejected PASSED

5 passed in 0.60s
```

**Exit code:** 0

---

## Test Collection (pytest --collect-only)

```bash
pytest tests/unit/test_validators.py --collect-only
```

**Expected output:**
```
5 tests collected

<Class TestValidateSourceRegistry>
  <Function test_validates>
<Class TestValidatePolicy>
  <Function test_validates>
<Class TestValidateProcedureDoc>
  <Function test_sample_validates>
  <Function test_invalid_proceduredoc_rejected>
  <Function test_missing_file_rejected>
```

---

## Lint (ruff)

```bash
ruff check scripts/ tests/unit/test_validators.py
```

**Expected output:**
```
All checks passed!
```

**Exit code:** 0

---

## Registry Ground Truth Counts

```bash
python3 -c "
import yaml, collections, pathlib

# Registry sources
reg = yaml.safe_load(pathlib.Path('data/sources/registry.yaml').read_text())
sources = reg.get('sources', [])
print(f'registry.yaml total sources: {len(sources)}')

# By jurisdiction
by_j = collections.Counter(s.get('jurisdiction') for s in sources)
print(f'by_jurisdiction: {dict(by_j)}')

# AGE by priority
by_jp = collections.Counter(
    f\"{s.get('jurisdiction')}-P{s.get('priority')}\"
    for s in sources
)
print(f'by_jurisdiction_priority: {dict(by_jp)}')

# Local seed
seed = yaml.safe_load(pathlib.Path('data/sources/local_seed.yaml').read_text())
print(f'local_seed.yaml sources: {len(seed.get(\"sources\", []))}')

# Line counts
print(f'registry.yaml lines: {len(pathlib.Path(\"data/sources/registry.yaml\").read_text().splitlines())}')
print(f'local_seed.yaml lines: {len(pathlib.Path(\"data/sources/local_seed.yaml\").read_text().splitlines())}')
"
```

**Expected output:**
```
registry.yaml total sources: 44
by_jurisdiction: {"age": 25, "ccaa": 19}
by_jurisdiction_priority: {"age-P0": 10, "age-P1": 11, "age-P2": 4, "ccaa-P0": 5, "ccaa-P1": 8, "ccaa-P2": 6}
local_seed.yaml sources: 20
registry.yaml lines: 799
local_seed.yaml lines: 413
```

---

## Policy Ground Truth Counts

```bash
python3 -c "
import yaml, pathlib

# Allowlist
a = yaml.safe_load(pathlib.Path('data/policy/allowlist.yaml').read_text())
print(f'allowlist default_action: {a.get(\"default_action\")}')
for tier in ['tier_1_age', 'tier_2_ccaa', 'tier_3_municipal']:
    domains = a.get(tier, {}).get('domains', [])
    print(f'{tier}: {len(domains)} domains')
lines = len(pathlib.Path('data/policy/allowlist.yaml').read_text().splitlines())
print(f'allowlist.yaml lines: {lines}')

print()

# Blocklist
b = yaml.safe_load(pathlib.Path('data/policy/blocklist.yaml').read_text())
cats = b.get('categories', [])
print(f'blocklist categories: {len(cats)}')
total_domains = sum(len(c.get('domains', [])) for c in cats)
print(f'blocklist domains_in_cats: {total_domains}')
patterns = b.get('top_level_patterns', [])
print(f'blocklist top_level_patterns: {len(patterns)}')
lines = len(pathlib.Path('data/policy/blocklist.yaml').read_text().splitlines())
print(f'blocklist.yaml lines: {lines}')

print()

# Canonical rules
c = yaml.safe_load(pathlib.Path('data/policy/canonical_rules.yaml').read_text())
print(f'canonical rules: {len(c.get(\"rules\", []))}')
print(f'canonical pipeline_order: {len(c.get(\"pipeline_order\", []))}')
print(f'canonical tracking_params: {len(c.get(\"tracking_params\", []))}')
print(f'canonical session_params: {len(c.get(\"session_params\", []))}')
lines = len(pathlib.Path('data/policy/canonical_rules.yaml').read_text().splitlines())
print(f'canonical_rules.yaml lines: {lines}')
"
```

**Expected output:**
```
allowlist default_action: reject
tier_1_age: 22 domains
tier_2_ccaa: 19 domains
tier_3_municipal: 19 domains
allowlist.yaml lines: 355

blocklist categories: 9
blocklist domains_in_cats: 23
blocklist top_level_patterns: 4
blocklist.yaml lines: 72

canonical rules: 10
canonical pipeline_order: 12
canonical tracking_params: 17
canonical session_params: 7
canonical_rules.yaml lines: 233
```

---

## Phantom Path Check

```bash
python3 -c "
import os

paths = [
    'data/ingested/procedures/',
    'data/ingested/raw/',
    'data/tramites/',
    'data/policy/allowlist.yaml',
    'data/sources/registry.yaml',
    'schemas/ProcedureDoc.v1.schema.json',
    'schemas/SourceRegistry.v1.schema.json',
    'scripts/validate_source_registry.py',
    'scripts/validate_policy.py',
    'scripts/validate_proceduredoc_schema.py',
    'scripts/link_check.py',
    'tests/unit/test_validators.py',
]
for p in paths:
    status = 'EXISTS' if os.path.exists(p) else 'PHANTOM'
    print(f'{p}: {status}')
"
```

**Expected output:**
```
data/ingested/procedures/: PHANTOM
data/ingested/raw/: PHANTOM
data/tramites/: EXISTS
data/policy/allowlist.yaml: EXISTS
data/sources/registry.yaml: EXISTS
schemas/ProcedureDoc.v1.schema.json: EXISTS
schemas/SourceRegistry.v1.schema.json: EXISTS
scripts/validate_source_registry.py: EXISTS
scripts/validate_policy.py: EXISTS
scripts/validate_proceduredoc_schema.py: EXISTS
scripts/link_check.py: EXISTS
tests/unit/test_validators.py: EXISTS
```

Note: `data/ingested/procedures/` and `data/ingested/raw/` are Q2 planned artifacts and are expected to be PHANTOM in Q1.1.

---

## URL Extraction and Allowlist Coverage Check

```bash
python3 -c "
import yaml, pathlib, re
from urllib.parse import urlparse

# Load allowlist
a = yaml.safe_load(pathlib.Path('data/policy/allowlist.yaml').read_text())

# Extract all explicit domains + patterns
allowed_domains = set()
patterns = []
for tier in ['tier_1_age', 'tier_2_ccaa', 'tier_3_municipal']:
    for entry in a.get(tier, {}).get('domains', []):
        d = entry.get('domain', '')
        allowed_domains.add(d)
        for alias in entry.get('aliases', []):
            allowed_domains.add(alias)
for p in a.get('auto_allow_patterns', []):
    patterns.append(p)

# Extract URLs from YAML files
urls = []
for f in ['data/sources/registry.yaml', 'data/sources/local_seed.yaml']:
    content = pathlib.Path(f).read_text()
    found = re.findall(r'https?://[^\s\"\'<>]+', content)
    for u in found:
        u = u.rstrip(',')
        urls.append((u, f))

# Check coverage
covered = 0
not_covered = 0
for url, src in urls:
    domain = urlparse(url).netloc
    is_covered = domain in allowed_domains
    if not is_covered:
        # Check subdomain_of
        for d in allowed_domains:
            if domain.endswith('.' + d):
                is_covered = True
                break
    if not is_covered:
        # Check patterns like *.gob.es
        for p in patterns:
            if p.startswith('*.'):
                suffix = p[1:]  # .gob.es
                if domain.endswith(suffix):
                    is_covered = True
                    break
    if is_covered:
        covered += 1
    else:
        not_covered += 1
        # Uncomment to see NOT_COVERED: print(f'  NOT_COVERED: {domain} <- {url}')

print(f'Total URLs: {len(urls)}')
print(f'COVERED: {covered}')
print(f'NOT_COVERED: {not_covered}')
print(f'Coverage: {covered/len(urls)*100:.1f}%')
"
```

**Expected output:**
```
Total URLs: 157
COVERED: 137
NOT_COVERED: 20
Coverage: 87.3%
```

---

## Claims File Integrity Check

```bash
python3 -c "
import json

total = 0
statuses = {}
ids = []
valid_json = True

with open('docs/arreglos chat/fase-3/audits-v4/claims/claims.v4.jsonl') as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            print(f'INVALID JSON at line {i}')
            valid_json = False
            continue
        total += 1
        s = obj.get('status', 'UNKNOWN')
        statuses[s] = statuses.get(s, 0) + 1
        ids.append(obj.get('claim_id'))

print(f'Total claims: {total}')
print(f'All valid JSON: {valid_json}')
print(f'Statuses: {statuses}')
print(f'Sum: {sum(statuses.values())}')
print(f'IDs unique: {len(set(ids)) == len(ids)}')
print(f'IDs sequential: {ids == [f\"C-{i:03d}\" for i in range(1, total+1)]}')
"
```

**Expected output:**
```
Total claims: 240
All valid JSON: True
Statuses: {'CONTRADICTED': 21, 'VERIFIED': 192, 'SEMANTIC_FLAG': 27}
Sum: 240
IDs unique: True
IDs sequential: True
```

---

## Full Evidence Regeneration

To regenerate all evidence files from scratch:

```bash
# From project root, with venv activated
AUDIT_DIR="docs/arreglos chat/fase-3/audits-v4"

# 1. Preflight
python3 -c "
import subprocess, sys, datetime
print(f'=== PREFLIGHT v4 ===')
print(f'Date: {datetime.datetime.utcnow().isoformat()}Z')
subprocess.run(['git', 'rev-parse', '--show-toplevel'])
subprocess.run(['git', 'status', '--short'])
" > "$AUDIT_DIR/evidence/preflight.txt" 2>&1

# 2. Registry counts
python3 -c "<registry counting script above>" > "$AUDIT_DIR/evidence/registry-counts.txt"

# 3. Policy counts
python3 -c "<policy counting script above>" > "$AUDIT_DIR/evidence/policy-counts.txt"

# 4. Schema validation (G1 + G2 + G3)
{
  echo "=== G1: Registry Validation ==="
  python3 scripts/validate_source_registry.py
  echo "exit_code: $?"
  echo ""
  echo "=== G2: Policy Validation ==="
  python3 scripts/validate_policy.py
  echo "exit_code: $?"
  echo ""
  echo "=== G3: ProcedureDoc Validation ==="
  python3 scripts/validate_proceduredoc_schema.py \
    "docs/arreglos chat/fase-3/q1-sources/evidence/samples/proceduredoc.sample.json"
  echo "exit_code: $?"
} > "$AUDIT_DIR/evidence/schema-validate.txt" 2>&1

# 5. Pytest
{
  echo "=== pytest -v ==="
  pytest tests/unit/test_validators.py -v
  echo "exit_code: $?"
} > "$AUDIT_DIR/evidence/pytest-run.txt" 2>&1

# 6. Pytest collect-only
{
  echo "=== pytest --collect-only ==="
  pytest tests/unit/test_validators.py --collect-only
  echo "exit_code: $?"
} > "$AUDIT_DIR/evidence/pytest-collect-only.txt" 2>&1

# 7. Ruff
{
  echo "=== ruff check ==="
  ruff check scripts/ tests/unit/test_validators.py
  echo "exit_code: $?"
} > "$AUDIT_DIR/evidence/ruff.txt" 2>&1
```

---

## Notes

- All commands assume working directory is `/Users/andreaavila/Documents/hakaton/civicaid-voice`
- Virtual environment must be activated: `source .venv/bin/activate`
- Python version at time of audit: 3.14.3 (preflight) / 3.11.8 (pytest)
- All expected outputs match the evidence files stored in `audits-v4/evidence/`
- If any command produces different output, the evidence has drifted and the audit should be re-run

---

*Generated by A6v4 (Report Generator & Meta-Consistency Checker), Anti-Hallucination Audit v4, 2026-02-18*
