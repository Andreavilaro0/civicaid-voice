"""Eval runner -- loads eval JSON cases, runs assertions, produces report."""

import json
import datetime
from dataclasses import dataclass, field
from typing import List, Callable
from pathlib import Path


@dataclass
class EvalResult:
    case_id: str
    query: str
    passed: bool
    score: float  # 0.0 to 1.0
    checks_passed: int
    checks_total: int
    failures: List[str] = field(default_factory=list)


@dataclass
class EvalReport:
    eval_set: str
    total_cases: int
    passed: int
    failed: int
    avg_score: float
    results: List[EvalResult] = field(default_factory=list)


def load_eval_cases(eval_dir: str = "data/evals") -> dict:
    """Load all eval JSON files from directory."""
    cases = {}
    eval_path = Path(eval_dir)
    if not eval_path.exists():
        return cases
    for f in sorted(eval_path.glob("*_evals.json")):
        with open(f) as fh:
            data = json.load(fh)
            cases[data["eval_set"]] = data["cases"]
    return cases


def run_eval_case(case: dict, response_text: str) -> EvalResult:
    """Run assertions on a single eval case against a response."""
    checks_passed = 0
    checks_total = 0
    failures = []

    # Check expected_contains
    for expected in case.get("expected_contains", []):
        checks_total += 1
        if expected.lower() in response_text.lower():
            checks_passed += 1
        else:
            failures.append(f"MISSING: '{expected}' not found in response")

    # Check expected_not_contains
    for unexpected in case.get("expected_not_contains", []):
        checks_total += 1
        if unexpected.lower() not in response_text.lower():
            checks_passed += 1
        else:
            failures.append(f"UNEXPECTED: '{unexpected}' found in response")

    score = checks_passed / max(checks_total, 1)
    return EvalResult(
        case_id=case["id"],
        query=case["query"],
        passed=len(failures) == 0,
        score=score,
        checks_passed=checks_passed,
        checks_total=checks_total,
        failures=failures,
    )


def run_eval_set(
    eval_set: str, cases: list, get_response: Callable[[str, str], str]
) -> EvalReport:
    """Run all cases in an eval set. get_response is callable(query, lang) -> str."""
    results = []
    for case in cases:
        response = get_response(case["query"], case.get("language", "es"))
        result = run_eval_case(case, response)
        results.append(result)

    passed = sum(1 for r in results if r.passed)
    avg_score = sum(r.score for r in results) / max(len(results), 1)

    return EvalReport(
        eval_set=eval_set,
        total_cases=len(cases),
        passed=passed,
        failed=len(cases) - passed,
        avg_score=avg_score,
        results=results,
    )


def generate_report_markdown(reports: List[EvalReport]) -> str:
    """Generate markdown report from eval results."""
    lines = [
        "# Eval Report",
        "",
        f"Generated: {datetime.datetime.now().isoformat()}",
        "",
    ]

    total_pass = sum(r.passed for r in reports)
    total_fail = sum(r.failed for r in reports)
    total = total_pass + total_fail

    lines.append(
        f"## Summary: {total_pass}/{total} passed"
        f" ({total_pass / max(total, 1) * 100:.0f}%)"
    )
    lines.append("")
    lines.append("| Eval Set | Cases | Passed | Failed | Avg Score |")
    lines.append("|----------|-------|--------|--------|-----------|")
    for r in reports:
        lines.append(
            f"| {r.eval_set} | {r.total_cases} | {r.passed} | {r.failed}"
            f" | {r.avg_score:.1%} |"
        )
    lines.append("")

    for r in reports:
        lines.append(f"## {r.eval_set}")
        lines.append("")
        for res in r.results:
            status = "PASS" if res.passed else "FAIL"
            lines.append(
                f"- [{status}] {res.case_id}: `{res.query}`"
                f" ({res.checks_passed}/{res.checks_total})"
            )
            for f in res.failures:
                lines.append(f"  - {f}")
        lines.append("")

    return "\n".join(lines)
