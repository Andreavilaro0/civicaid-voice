"""Eval tests for Q4 — verify expanded eval set structure and completeness."""

import json
import os

import pytest

EVAL_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, "data", "evals", "rag_eval_set.json"
)

pytestmark = pytest.mark.skipif(
    not os.path.exists(EVAL_PATH),
    reason="rag_eval_set.json not found",
)


@pytest.fixture(scope="module")
def eval_data():
    with open(EVAL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def queries(eval_data):
    return eval_data["queries"]


class TestEvalSetStructure:
    def test_has_200_plus_queries(self, queries):
        assert len(queries) >= 200, f"Expected 200+, got {len(queries)}"

    def test_all_queries_have_required_fields(self, queries):
        required = {"id", "query", "expected_procedure", "category"}
        for q in queries:
            missing = required - set(q.keys())
            assert not missing, f"Query {q.get('id')} missing fields: {missing}"

    def test_no_duplicate_ids(self, queries):
        ids = [q["id"] for q in queries]
        dupes = [i for i in ids if ids.count(i) > 1]
        assert len(set(dupes)) == 0, f"Duplicate IDs: {set(dupes)}"


class TestEvalSetCategories:
    EXPECTED_CATEGORIES = {
        "basic_info",
        "acronyms",
        "colloquial",
        "territorial",
        "negative",
        "multi_tramite",
        "edge_case",
    }

    def test_all_categories_present(self, queries):
        found = {q["category"] for q in queries}
        missing = self.EXPECTED_CATEGORIES - found
        assert not missing, f"Missing categories: {missing}"

    def test_negatives_have_null_procedure(self, queries):
        negatives = [q for q in queries if q["category"] == "negative"]
        for q in negatives:
            assert q["expected_procedure"] is None, (
                f"Negative query {q['id']} has non-null procedure"
            )

    def test_territorial_have_territory(self, queries):
        territorial = [q for q in queries if q["category"] == "territorial"]
        for q in territorial:
            assert q.get("territory") is not None, (
                f"Territorial query {q['id']} has no territory"
            )
