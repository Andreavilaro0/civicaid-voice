#!/usr/bin/env python3
"""Run eval suite against Clara's cache/KB."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import cache
from src.core.skills.kb_lookup import kb_lookup
from src.core.models import InputType
from src.utils.eval_runner import load_eval_cases, run_eval_set, generate_report_markdown

# Load cache
cache.load_cache()


def get_cache_response(query: str, language: str) -> str:
    """Get response from cache match, falling back to KB lookup."""
    result = cache.match(query, language, InputType.TEXT)
    if result.hit and result.entry:
        return result.entry.respuesta
    # Try KB lookup
    kb = kb_lookup(query, language)
    if kb:
        return json.dumps(kb.datos, ensure_ascii=False)
    return ""


eval_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "evals")
all_cases = load_eval_cases(eval_dir)
reports = []
for eval_set, cases in all_cases.items():
    report = run_eval_set(eval_set, cases, get_cache_response)
    reports.append(report)

md = generate_report_markdown(reports)
print(md)

# Write report
report_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "04-testing", "evals_report.md",
)
with open(report_path, "w") as f:
    f.write(md)
print(f"\nReport written to {report_path}")
