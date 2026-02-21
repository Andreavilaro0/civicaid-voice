"""Tests for eval runner framework."""

import os
from src.utils.eval_runner import (
    load_eval_cases,
    run_eval_case,
    run_eval_set,
    generate_report_markdown,
    EvalResult,
    EvalReport,
)


PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVAL_DIR = os.path.join(PROJ_ROOT, "data", "evals")


def test_load_eval_cases():
    """Eval cases load from data/evals/ with at least 4 sets and 16 cases."""
    cases = load_eval_cases(EVAL_DIR)
    assert len(cases) >= 4, f"Expected >=4 eval sets, got {len(cases)}"
    total = sum(len(c) for c in cases.values())
    assert total >= 16, f"Expected >=16 total cases, got {total}"


def test_load_eval_cases_missing_dir():
    """load_eval_cases returns empty dict for nonexistent directory."""
    cases = load_eval_cases("/tmp/nonexistent_eval_dir_xyz")
    assert cases == {}


def test_run_eval_case_pass():
    """run_eval_case passes when response contains expected text."""
    case = {
        "id": "test_01",
        "query": "test query",
        "expected_contains": ["hello", "world"],
        "expected_not_contains": ["goodbye"],
    }
    result = run_eval_case(case, "Hello World, nice to meet you")
    assert result.passed is True
    assert result.score == 1.0
    assert result.checks_passed == 3
    assert result.checks_total == 3
    assert result.failures == []


def test_run_eval_case_fail_missing():
    """run_eval_case fails when expected text is missing."""
    case = {
        "id": "test_02",
        "query": "test query",
        "expected_contains": ["hello", "missing_word"],
    }
    result = run_eval_case(case, "Hello there")
    assert result.passed is False
    assert result.checks_passed == 1
    assert result.checks_total == 2
    assert len(result.failures) == 1
    assert "missing_word" in result.failures[0]


def test_run_eval_case_fail_unexpected():
    """run_eval_case fails when unexpected text is present."""
    case = {
        "id": "test_03",
        "query": "test query",
        "expected_not_contains": ["bad_word"],
    }
    result = run_eval_case(case, "This has bad_word in it")
    assert result.passed is False
    assert result.checks_passed == 0
    assert result.checks_total == 1


def test_run_eval_case_no_checks():
    """run_eval_case with no expected fields passes vacuously."""
    case = {"id": "test_04", "query": "test query"}
    result = run_eval_case(case, "anything")
    assert result.passed is True
    assert result.score == 0.0  # 0/0 -> 0/max(0,1) = 0.0


def test_run_eval_set():
    """run_eval_set aggregates results correctly."""
    cases = [
        {"id": "s_01", "query": "q1", "expected_contains": ["yes"]},
        {"id": "s_02", "query": "q2", "expected_contains": ["no"]},
    ]

    def mock_response(query: str, lang: str) -> str:
        return "yes this is a response"

    report = run_eval_set("test_set", cases, mock_response)
    assert report.eval_set == "test_set"
    assert report.total_cases == 2
    assert report.passed == 1  # "yes" found, "no" not found
    assert report.failed == 1


def test_eval_report_generation():
    """generate_report_markdown produces valid markdown."""
    reports = [
        EvalReport(
            eval_set="test",
            total_cases=2,
            passed=1,
            failed=1,
            avg_score=0.5,
            results=[
                EvalResult(
                    case_id="t_01",
                    query="q1",
                    passed=True,
                    score=1.0,
                    checks_passed=1,
                    checks_total=1,
                ),
                EvalResult(
                    case_id="t_02",
                    query="q2",
                    passed=False,
                    score=0.0,
                    checks_passed=0,
                    checks_total=1,
                    failures=["MISSING: 'x' not found"],
                ),
            ],
        )
    ]
    md = generate_report_markdown(reports)
    assert "# Eval Report" in md
    assert "1/2 passed" in md
    assert "[PASS] t_01" in md
    assert "[FAIL] t_02" in md
    assert "MISSING" in md


def test_eval_runner_with_cache():
    """Run eval cases against actual cache.match to verify integration."""
    from src.core import cache
    from src.core.models import InputType

    cache.load_cache()

    def get_response(query: str, lang: str) -> str:
        result = cache.match(query, lang, InputType.TEXT)
        if result.hit and result.entry:
            return result.entry.respuesta
        return ""

    cases = load_eval_cases(EVAL_DIR)
    # IMV eval set should exist and cache should match basic IMV query
    assert "imv" in cases
    imv_cases = cases["imv"]
    report = run_eval_set("imv", imv_cases, get_response)
    # At least the first case ("Que es el IMV?") should pass via cache
    first_result = report.results[0]
    assert first_result.case_id == "imv_01"
    assert first_result.passed is True, f"imv_01 failed: {first_result.failures}"
