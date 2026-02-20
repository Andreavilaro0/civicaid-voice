#!/usr/bin/env python3
"""Run RAG evaluation against the eval set.

Usage:
    python scripts/run_rag_eval.py                    # Full eval (requires Docker + DB)
    python scripts/run_rag_eval.py --dry-run           # Validate eval set structure only
    python scripts/run_rag_eval.py --output report.json # Save results to file
    python scripts/run_rag_eval.py --quick              # Run only first 20 queries
    python scripts/run_rag_eval.py --category basic_info  # Run only one category
    python scripts/run_rag_eval.py --compare prev.json  # Compare against previous run
"""

import argparse
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.rag_eval import load_eval_set, compute_metrics, format_report


def _compare_runs(current: dict, previous_path: str) -> str:
    """Compare current metrics against a previous run file."""
    with open(previous_path) as f:
        prev = json.load(f)
    prev_m = prev["metrics"]
    cur_m = current

    lines = [
        "",
        "=" * 50,
        "Comparison with previous run",
        "=" * 50,
    ]
    for key in ("precision_at_1", "precision_at_3", "mrr", "bm25_activation_rate"):
        old_val = prev_m.get(key, 0.0)
        new_val = cur_m.get(key, 0.0)
        delta = new_val - old_val
        arrow = "+" if delta >= 0 else ""
        lines.append(f"  {key:25s}: {old_val:.2%} -> {new_val:.2%} ({arrow}{delta:.2%})")
    lines.append(f"  {'total_queries':25s}: {prev_m.get('total_queries', 0)} -> {cur_m.get('total_queries', 0)}")
    lines.append("=" * 50)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run RAG evaluation")
    parser.add_argument("--eval-set", default="data/evals/rag_eval_set.json",
                        help="Path to eval set JSON")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only validate eval set structure")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--quick", action="store_true",
                        help="Run only first 20 queries (for fast iteration)")
    parser.add_argument("--category",
                        help="Run only queries from a specific category")
    parser.add_argument("--compare",
                        help="Compare results against a previous run JSON file")
    args = parser.parse_args()

    # Load eval set
    eval_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        args.eval_set,
    )
    queries = load_eval_set(eval_path)
    print(f"Loaded {len(queries)} queries from {args.eval_set}")

    # Filter by category if specified
    if args.category:
        queries = [q for q in queries if q.get("category") == args.category]
        print(f"Filtered to {len(queries)} queries in category '{args.category}'")

    # Quick mode — first 20 queries only
    if args.quick:
        queries = queries[:20]
        print(f"Quick mode: running {len(queries)} queries")

    if args.dry_run:
        # Validate structure
        categories = {}
        for q in queries:
            cat = q.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        print(f"\nCategories: {json.dumps(categories, indent=2)}")
        print(f"\nTotal: {len(queries)} queries")
        print("Eval set structure: OK")
        return

    # Full evaluation requires DB connection
    try:
        from src.core.config import config
        if not config.RAG_ENABLED or not config.RAG_DB_URL:
            print("ERROR: RAG_ENABLED=true and RAG_DB_URL required for full eval")
            print("Use --dry-run to validate eval set without DB")
            sys.exit(1)

        from src.core.rag.store import PGVectorStore
        from src.core.rag.embedder import embed_text
        from src.core.rag.reranker import rerank
        from src.core.rag.territory import detect_territory
        store = PGVectorStore()
    except Exception as e:
        print(f"ERROR: Cannot initialize store: {e}")
        print("Use --dry-run to validate eval set without DB")
        sys.exit(1)

    # Run evaluation — use store.search_hybrid directly for top-k procedure IDs and BM25 scores
    results = []
    for i, q in enumerate(queries):
        print(f"  [{i+1}/{len(queries)}] {q['id']}: {q['query'][:60]}...", flush=True)
        try:
            territory = detect_territory(q["query"])
            query_embedding = embed_text(q["query"])
            raw_results = store.search_hybrid(
                query_text=q["query"],
                query_embedding=query_embedding,
                top_k=config.RAG_TOP_K,
                weight=config.RAG_HYBRID_WEIGHT,
                territory_filter=territory,
            )
            raw_results = rerank(
                q["query"], raw_results,
                strategy=config.RAG_RERANK_STRATEGY,
            )

            # Deduplicate procedure IDs preserving order
            seen = set()
            procedure_ids = []
            max_bm25 = 0.0
            for r in raw_results:
                pid = r["procedure_id"]
                if pid not in seen:
                    seen.add(pid)
                    procedure_ids.append(pid)
                bm25 = r.get("bm25_score", 0.0)
                if bm25 > max_bm25:
                    max_bm25 = bm25

            result = {
                "query_id": q["id"],
                "query": q["query"],
                "category": q.get("category", "unknown"),
                "expected_procedure": q.get("expected_procedure"),
                "top_procedure": procedure_ids[0] if procedure_ids else None,
                "retrieved_procedures": procedure_ids[:3],
                "bm25_score": max_bm25,
            }
        except Exception as e:
            result = {
                "query_id": q["id"],
                "query": q["query"],
                "category": q.get("category", "unknown"),
                "expected_procedure": q.get("expected_procedure"),
                "top_procedure": None,
                "retrieved_procedures": [],
                "bm25_score": 0,
                "error": str(e),
            }
        results.append(result)

    # Compute metrics
    metrics = compute_metrics(results)
    print(format_report(metrics))

    # Compare if requested
    if args.compare:
        compare_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            args.compare,
        )
        if os.path.exists(compare_path):
            print(_compare_runs(metrics, compare_path))
        else:
            print(f"\nWARNING: Comparison file not found: {args.compare}")

    # Save if requested
    if args.output:
        output_data = {"metrics": metrics, "results": results}
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
