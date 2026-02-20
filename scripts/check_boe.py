#!/usr/bin/env python3
"""CLI runner for BOE (Boletin Oficial del Estado) monitoring.

Usage:
    python scripts/check_boe.py --check
    python scripts/check_boe.py --check --json
    python scripts/check_boe.py --check --keywords "imv,nie,desempleo" --min-score 0.3
    python scripts/check_boe.py --check --days 14
"""

import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Enable BOE monitor for CLI usage
os.environ.setdefault("RAG_BOE_MONITOR_ENABLED", "true")

from src.core.rag.boe_monitor import BOEMonitor  # noqa: E402

logger = logging.getLogger("check_boe")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor BOE RSS feed for relevant legal updates.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        required=True,
        help="Fetch RSS + match keywords + report alerts",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        default=None,
        metavar="KW",
        help='Comma-separated keywords to override defaults (e.g. "imv,nie,desempleo")',
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        metavar="SCORE",
        help="Minimum relevance threshold (0.0-1.0, default: 0.0)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        metavar="N",
        help="Days to look back (default: 7)",
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

    keywords = None
    if args.keywords:
        keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]

    monitor = BOEMonitor(keywords=keywords)
    alerts = monitor.check_updates(days_back=args.days)

    # Filter by min-score
    if args.min_score > 0:
        alerts = [a for a in alerts if a.relevance_score >= args.min_score]

    if args.json_output:
        output = {
            "total_alerts": len(alerts),
            "days_back": args.days,
            "min_score": args.min_score,
            "keywords_used": keywords or BOEMonitor.KEYWORDS,
            "alerts": [
                {
                    "title": a.title,
                    "url": a.url,
                    "published_date": a.published_date,
                    "keywords_matched": a.keywords_matched,
                    "relevance_score": a.relevance_score,
                }
                for a in alerts
            ],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if not alerts:
            print("No BOE alerts found for the given criteria.")
        else:
            print(f"Found {len(alerts)} BOE alerts (last {args.days} days):\n")
            for a in alerts:
                print(f"  [{a.relevance_score:.2f}] {a.title}")
                print(f"         Keywords: {', '.join(a.keywords_matched)}")
                print(f"         Date: {a.published_date}")
                print(f"         URL: {a.url}")
                print()


if __name__ == "__main__":
    main()
