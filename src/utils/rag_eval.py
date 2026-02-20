"""RAG evaluation framework for Clara — computes precision, MRR, BM25 activation."""

import json
import logging

logger = logging.getLogger(__name__)


def load_eval_set(path: str) -> list[dict]:
    """Load evaluation queries from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return data["queries"]


def compute_metrics(results: list[dict]) -> dict:
    """Compute retrieval quality metrics from evaluation results.

    Each result dict should have:
        query_id: str
        expected_procedure: str | None (None = negative query)
        retrieved_procedures: list[str] (top-k procedure IDs)
        top_procedure: str | None (first result)
        bm25_score: float (optional, for BM25 activation)

    Returns dict with:
        precision_at_1, precision_at_3, mrr, bm25_activation_rate,
        total_queries, positive_queries, negative_queries
    """
    if not results:
        return {
            "precision_at_1": 0.0, "precision_at_3": 0.0, "mrr": 0.0,
            "bm25_activation_rate": 0.0,
            "total_queries": 0, "positive_queries": 0, "negative_queries": 0,
        }

    correct_at_1 = 0
    correct_at_3 = 0
    reciprocal_ranks = []
    bm25_active = 0
    positive_count = 0
    negative_count = 0

    for r in results:
        expected = r.get("expected_procedure")
        retrieved = r.get("retrieved_procedures", [])
        top = r.get("top_procedure")

        if expected is None:
            # Negative query — correct if no results or no matching procedure
            negative_count += 1
            if not retrieved:
                correct_at_1 += 1
                correct_at_3 += 1
                reciprocal_ranks.append(1.0)
            else:
                correct_at_1 += 0
                correct_at_3 += 0
                reciprocal_ranks.append(0.0)
            continue

        positive_count += 1

        # Precision@1
        if top == expected:
            correct_at_1 += 1

        # Precision@3
        if expected in retrieved[:3]:
            correct_at_3 += 1

        # MRR
        try:
            rank = retrieved.index(expected) + 1
            reciprocal_ranks.append(1.0 / rank)
        except ValueError:
            reciprocal_ranks.append(0.0)

        # BM25 activation
        if r.get("bm25_score", 0) > 0:
            bm25_active += 1

    total = len(results)
    return {
        "precision_at_1": correct_at_1 / total if total else 0.0,
        "precision_at_3": correct_at_3 / total if total else 0.0,
        "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0,
        "bm25_activation_rate": bm25_active / positive_count if positive_count else 0.0,
        "total_queries": total,
        "positive_queries": positive_count,
        "negative_queries": negative_count,
    }


def format_report(metrics: dict) -> str:
    """Format metrics as a human-readable report."""
    lines = [
        "=" * 50,
        "RAG Evaluation Report",
        "=" * 50,
        f"Total queries:       {metrics['total_queries']}",
        f"  Positive:          {metrics['positive_queries']}",
        f"  Negative:          {metrics['negative_queries']}",
        "",
        f"Precision@1:         {metrics['precision_at_1']:.2%}",
        f"Precision@3:         {metrics['precision_at_3']:.2%}",
        f"MRR:                 {metrics['mrr']:.2%}",
        f"BM25 activation:     {metrics['bm25_activation_rate']:.2%}",
        "",
        "Thresholds:",
        f"  Precision@3 >= 85%: {'PASS' if metrics['precision_at_3'] >= 0.85 else 'FAIL'}",
        f"  Precision@1 >= 70%: {'PASS' if metrics['precision_at_1'] >= 0.70 else 'FAIL'}",
        f"  BM25 >= 60%:        {'PASS' if metrics['bm25_activation_rate'] >= 0.60 else 'FAIL'}",
        "=" * 50,
    ]
    return "\n".join(lines)
