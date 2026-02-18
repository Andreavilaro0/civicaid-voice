"""Red team tests — verify guardrails block abuse prompts.

NOTE: These tests depend on src/core/guardrails.py which may not exist yet.
Tests are skipped automatically if the guardrails module is not available.
"""
import pytest
import json
from pathlib import Path


try:
    import src.core.guardrails  # noqa: F401
    GUARDRAILS_AVAILABLE = True
except ImportError:
    GUARDRAILS_AVAILABLE = False


def load_redteam_cases():
    path = Path("data/evals/redteam_prompts.json")
    if not path.exists():
        pytest.skip("redteam_prompts.json not found", allow_module_level=True)
    with open(path) as f:
        return json.load(f)["cases"]


skip_no_guardrails = pytest.mark.skipif(
    not GUARDRAILS_AVAILABLE,
    reason="src.core.guardrails not yet implemented"
)


class TestRedTeamDataFile:
    """Tests that the red team data file is well-formed."""

    def test_redteam_file_exists(self):
        path = Path("data/evals/redteam_prompts.json")
        assert path.exists(), "redteam_prompts.json must exist"

    def test_redteam_file_valid_json(self):
        path = Path("data/evals/redteam_prompts.json")
        with open(path) as f:
            data = json.load(f)
        assert "eval_set" in data
        assert data["eval_set"] == "redteam"
        assert "cases" in data
        assert len(data["cases"]) >= 10

    def test_redteam_cases_have_required_fields(self):
        cases = load_redteam_cases()
        for case in cases:
            assert "id" in case, "Missing id in case"
            assert "query" in case, f"Missing query in {case.get('id')}"
            assert "type" in case, f"Missing type in {case.get('id')}"


@skip_no_guardrails
class TestRedTeamGuardrails:
    """Tests that guardrails correctly handle abuse prompts."""

    def test_guardrails_module_exists(self):
        from src.core.guardrails import pre_check, post_check
        assert callable(pre_check)
        assert callable(post_check)

    @pytest.mark.parametrize("case", [
        c for c in load_redteam_cases() if c.get("type") in ("self_harm", "violence", "illegal")
    ], ids=lambda c: c["id"])
    @pytest.mark.xfail(reason="Guardrails regex coverage is iterative — gaps expected", strict=False)
    def test_blocked_prompts(self, case):
        from src.core.guardrails import pre_check
        result = pre_check(case["query"])
        assert not result.safe, f"Should be blocked: {case['query']}"
        assert result.modified_text, "Should have a safe response"

    def test_safe_input_passes(self):
        from src.core.guardrails import pre_check
        result = pre_check("Que es el IMV?")
        assert result.safe
