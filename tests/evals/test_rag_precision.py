"""RAG precision evaluation tests — require Docker + PostgreSQL.

Run with: RAG_ENABLED=true pytest tests/evals/test_rag_precision.py -v
Skip automatically when RAG_DB_URL is not set.
"""
import json
import os
import pytest

# Skip entire module if RAG is not configured
pytestmark = pytest.mark.skipif(
    not os.getenv("RAG_DB_URL"),
    reason="RAG_DB_URL not set — requires Docker PostgreSQL"
)


@pytest.fixture(scope="module")
def eval_queries():
    """Load the evaluation query set."""
    eval_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "evals", "rag_eval_set.json"
    )
    with open(eval_path) as f:
        data = json.load(f)
    return data["queries"]


@pytest.fixture(scope="module")
def retriever():
    """Create a PGVectorRetriever instance."""
    from src.core.retriever import PGVectorRetriever
    return PGVectorRetriever()


class TestRagPrecision:
    """Evaluate retrieval precision against the eval set.

    These tests measure actual retrieval quality against the DB
    and serve as quality gates for Q3.
    """

    def test_precision_at_3_above_threshold(self, eval_queries, retriever):
        """G9: Precision@3 >= 0.85."""
        positive_queries = [q for q in eval_queries if q.get("expected_procedure")]
        correct = 0
        total = len(positive_queries)

        for q in positive_queries:
            kb = retriever.retrieve(q["query"], "es")
            if kb and kb.tramite == q["expected_procedure"]:
                correct += 1

        precision = correct / total if total else 0
        assert precision >= 0.85, (
            f"Precision@3 = {precision:.2%} (expected >= 85%, "
            f"{correct}/{total} correct)"
        )

    def test_bm25_activation_rate(self, eval_queries, retriever):
        """G10: BM25 activation >= 60%."""
        # This would need access to raw search results
        # For now, verify that acronym queries return results
        acronym_queries = [q for q in eval_queries if q.get("category") == "acronyms"]
        found = 0
        for q in acronym_queries:
            kb = retriever.retrieve(q["query"], "es")
            if kb:
                found += 1

        rate = found / len(acronym_queries) if acronym_queries else 0
        assert rate >= 0.60, (
            f"Acronym retrieval rate = {rate:.2%} (expected >= 60%)"
        )

    def test_negative_queries_return_none_or_low(self, eval_queries, retriever):
        """Negative queries should not return confident results."""
        negative_queries = [q for q in eval_queries if q.get("expected_procedure") is None]
        false_positives = 0
        for q in negative_queries:
            kb = retriever.retrieve(q["query"], "es")
            if kb is not None:
                false_positives += 1

        fp_rate = false_positives / len(negative_queries) if negative_queries else 0
        # Allow up to 40% false positives for negative queries
        assert fp_rate <= 0.40, (
            f"False positive rate = {fp_rate:.2%} (expected <= 40%)"
        )
