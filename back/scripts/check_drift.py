#!/usr/bin/env python3
"""CLI runner for drift detection on RAG procedures.

Usage:
    python scripts/check_drift.py --all
    python scripts/check_drift.py --stale --json
    python scripts/check_drift.py --all --threshold 30 --webhook
"""

import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Set RAG_DB_URL before any project imports
if not os.environ.get("RAG_DB_URL"):
    os.environ["RAG_DB_URL"] = "postgresql://clara:clara_dev@localhost:5432/clara_rag"

from src.core.rag.drift import DriftDetector  # noqa: E402
from src.core.rag.store import PGVectorStore  # noqa: E402

logger = logging.getLogger("check_drift")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect content drift and staleness in RAG procedures.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Check all procedures in DB vs JSON source",
    )
    group.add_argument(
        "--stale",
        action="store_true",
        help="List only procedures with staleness > threshold",
    )
    parser.add_argument(
        "--webhook",
        action="store_true",
        help="Send alert to RAG_DRIFT_WEBHOOK_URL if drift detected",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=None,
        metavar="DAYS",
        help="Override RAG_STALENESS_THRESHOLD_DAYS (default: from config)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


def _send_webhook(results: list, webhook_url: str) -> bool:
    """Send drift alert to webhook URL. Returns True on success."""
    from urllib.request import Request, urlopen
    from urllib.error import URLError

    payload = json.dumps({
        "text": f"Drift alert: {len(results)} procedures need attention",
        "procedures": [
            {
                "id": r.procedure_id,
                "status": r.status,
                "staleness_days": r.staleness_days,
                "detail": r.detail,
            }
            for r in results
        ],
    }).encode("utf-8")

    req = Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=10) as resp:
            logger.info("Webhook sent: %d", resp.status)
            return True
    except URLError as exc:
        logger.error("Webhook failed: %s", exc)
        return False


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    store = PGVectorStore()
    detector = DriftDetector(store)

    if args.all:
        results = detector.check_all(threshold_days=args.threshold)
    else:  # --stale
        results = detector.get_stale_procedures(threshold_days=args.threshold)

    # Output
    if args.json_output:
        output = {
            "total": len(results),
            "current": sum(1 for r in results if r.status == "current"),
            "stale": sum(1 for r in results if r.status == "stale"),
            "drifted": sum(1 for r in results if r.status == "drifted"),
            "missing": sum(1 for r in results if r.status == "missing"),
            "procedures": [
                {
                    "id": r.procedure_id,
                    "status": r.status,
                    "staleness_days": r.staleness_days,
                    "staleness_score": r.staleness_score,
                    "content_hash_match": r.content_hash_match,
                    "detail": r.detail,
                }
                for r in results
            ],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        for r in results:
            icon = {"current": "OK", "stale": "STALE", "drifted": "DRIFT", "missing": "MISS"}.get(r.status, "?")
            print(f"  [{icon:5s}] {r.procedure_id} — {r.detail}")
        print()
        current = sum(1 for r in results if r.status == "current")
        stale = sum(1 for r in results if r.status == "stale")
        drifted = sum(1 for r in results if r.status == "drifted")
        missing = sum(1 for r in results if r.status == "missing")
        print(f"Summary: {current} current, {stale} stale, {drifted} drifted, {missing} missing")

    # Webhook
    if args.webhook:
        webhook_url = os.environ.get("RAG_DRIFT_WEBHOOK_URL", "")
        if not webhook_url:
            logger.warning("--webhook requested but RAG_DRIFT_WEBHOOK_URL is not set")
        else:
            alertable = [r for r in results if r.status in ("stale", "drifted", "missing")]
            if alertable:
                _send_webhook(alertable, webhook_url)
            else:
                logger.info("No drift detected — skipping webhook")


if __name__ == "__main__":
    main()
