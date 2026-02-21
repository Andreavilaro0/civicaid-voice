#!/usr/bin/env python3
"""CLI runner for the RAG ingestion pipeline.

Usage:
    python scripts/run_ingestion.py --all
    python scripts/run_ingestion.py --all --dry-run
    python scripts/run_ingestion.py --source imv --dry-run
    python scripts/run_ingestion.py --registry --force
"""

import argparse
import json
import logging
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Set RAG_DB_URL before any project imports
if not os.environ.get("RAG_DB_URL"):
    os.environ["RAG_DB_URL"] = "postgresql://clara:clara_dev@localhost:5432/clara_rag"

# Enable ingestion for CLI usage
os.environ.setdefault("RAG_INGESTION_ENABLED", "true")

from src.core.rag.ingestion import IngestionPipeline  # noqa: E402
from src.core.rag.store import PGVectorStore  # noqa: E402

logger = logging.getLogger("run_ingestion")

_TRAMITES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "tramites"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Clara RAG ingestion pipeline.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Re-ingest all tramites from data/tramites/",
    )
    group.add_argument(
        "--source",
        type=str,
        metavar="ID",
        help="Ingest a specific tramite by filename (without .json)",
    )
    group.add_argument(
        "--registry",
        action="store_true",
        help="Ingest from data/sources/registry.yaml (tier-based)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without writing to DB",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore content hash (re-process even if unchanged)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    store = PGVectorStore()
    pipeline = IngestionPipeline(store)

    start = time.monotonic()
    results = []

    if args.all:
        logger.info("Ingesting all tramites (dry_run=%s, force=%s)", args.dry_run, args.force)
        results = pipeline.ingest_all(dry_run=args.dry_run)
    elif args.source:
        source_path = os.path.normpath(
            os.path.join(_TRAMITES_DIR, f"{args.source}.json")
        )
        if not os.path.isfile(source_path):
            logger.error("Source file not found: %s", source_path)
            sys.exit(1)
        logger.info("Ingesting source: %s (dry_run=%s)", args.source, args.dry_run)
        result = pipeline.ingest_source(source_path, dry_run=args.dry_run)
        results = [result]
    elif args.registry:
        logger.info("Ingesting from registry (dry_run=%s)", args.dry_run)
        results = pipeline.ingest_from_registry(dry_run=args.dry_run)

    elapsed_s = round(time.monotonic() - start, 2)

    # Build report
    report = {
        "processed": len(results),
        "fetched": sum(1 for r in results if r.status == "fetched"),
        "updated": sum(1 for r in results if r.status == "updated"),
        "unchanged": sum(1 for r in results if r.status == "no_change"),
        "errors": sum(1 for r in results if r.status == "error"),
        "duration_s": elapsed_s,
        "dry_run": args.dry_run,
        "details": [
            {
                "source_id": r.source_id,
                "status": r.status,
                "chunks_created": r.chunks_created,
                "content_hash": r.content_hash[:12] + "..." if r.content_hash else "",
                "error": r.error,
                "duration_ms": r.duration_ms,
            }
            for r in results
        ],
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))

    if report["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
