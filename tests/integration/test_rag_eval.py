"""Integration tests for RAG evaluation framework."""
import json
import os
import pytest


class TestEvalSetStructure:
    """Validate the eval set JSON structure."""

    @pytest.fixture
    def eval_set(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "evals", "rag_eval_set.json"
        )
        with open(path) as f:
            return json.load(f)

    def test_has_queries(self, eval_set):
        assert "queries" in eval_set
        assert len(eval_set["queries"]) >= 50

    def test_query_has_required_fields(self, eval_set):
        required = {"id", "query", "expected_procedure", "category"}
        for q in eval_set["queries"]:
            missing = required - set(q.keys())
            assert not missing, f"Query {q.get('id', '?')} missing: {missing}"

    def test_has_negative_queries(self, eval_set):
        negatives = [q for q in eval_set["queries"] if q["category"] == "negative"]
        assert len(negatives) >= 3

    def test_has_acronym_queries(self, eval_set):
        acronyms = [q for q in eval_set["queries"] if q["category"] == "acronyms"]
        assert len(acronyms) >= 3

    def test_has_territorial_queries(self, eval_set):
        territorial = [q for q in eval_set["queries"] if q["category"] == "territorial"]
        assert len(territorial) >= 3

    def test_has_colloquial_queries(self, eval_set):
        colloquial = [q for q in eval_set["queries"] if q["category"] == "colloquial"]
        assert len(colloquial) >= 3

    def test_unique_ids(self, eval_set):
        ids = [q["id"] for q in eval_set["queries"]]
        assert len(ids) == len(set(ids)), "Duplicate query IDs found"


class TestEvalFramework:
    """Test the evaluation framework module."""

    def test_import_eval_module(self):
        from src.utils.rag_eval import compute_metrics
        assert callable(compute_metrics)

    def test_compute_metrics_perfect_score(self):
        from src.utils.rag_eval import compute_metrics
        results = [
            {"query_id": "q1", "expected_procedure": "imv",
             "retrieved_procedures": ["imv", "empadronamiento", "tsi"],
             "top_procedure": "imv"},
            {"query_id": "q2", "expected_procedure": "empadronamiento",
             "retrieved_procedures": ["empadronamiento", "imv"],
             "top_procedure": "empadronamiento"},
        ]
        metrics = compute_metrics(results)
        assert metrics["precision_at_1"] == 1.0
        assert metrics["precision_at_3"] == 1.0
        assert metrics["mrr"] == 1.0

    def test_compute_metrics_partial_score(self):
        from src.utils.rag_eval import compute_metrics
        results = [
            {"query_id": "q1", "expected_procedure": "imv",
             "retrieved_procedures": ["empadronamiento", "imv", "tsi"],
             "top_procedure": "empadronamiento"},
            {"query_id": "q2", "expected_procedure": "tsi",
             "retrieved_procedures": ["tsi"],
             "top_procedure": "tsi"},
        ]
        metrics = compute_metrics(results)
        assert metrics["precision_at_1"] == 0.5  # 1/2 correct at position 1
        assert metrics["precision_at_3"] == 1.0  # Both found in top 3
        assert 0.5 < metrics["mrr"] < 1.0

    def test_compute_metrics_handles_negatives(self):
        from src.utils.rag_eval import compute_metrics
        results = [
            {"query_id": "q1", "expected_procedure": None,
             "retrieved_procedures": [],
             "top_procedure": None},
        ]
        metrics = compute_metrics(results)
        # Negative queries (expected=None) with no results = correct
        assert metrics["precision_at_1"] == 1.0
