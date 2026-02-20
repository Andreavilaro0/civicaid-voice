#!/usr/bin/env python3
"""
Link health checker for CivicAid source registry.

Usage:
    python3 scripts/link_check.py [--smoke] [--limit N] [--output PATH] [--dry-run]
"""
import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "data" / "sources" / "registry.yaml"
LOCAL = REPO / "data" / "sources" / "local_seed.yaml"
UA = "ClaraBot/1.0 (CivicAid; link-checker)"


def load_urls(smoke=False):
    urls = []
    for path in [REGISTRY, LOCAL]:
        if not path.exists():
            print(f"WARNING: {path.name} not found", file=sys.stderr)
            continue
        with open(path) as f:
            data = yaml.safe_load(f)
        for src in data.get("sources", []):
            if smoke and src.get("priority") != "P0":
                continue
            sid = src.get("id", "unknown")
            tier = src.get("tier", 0)
            rate = src.get("rate_limit_rps", 1.0)
            for field in ["portal_url", "sede_url", "catalogo_url", "api_url"]:
                url = src.get(field)
                if url:
                    urls.append({"url": url, "source_id": sid, "url_field": field, "tier": tier, "rate": rate})
    return urls


def check(url, timeout=30):
    result = {
        "url": url, "final_url": url, "status_code": None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "redirect_chain": [], "response_time_ms": None, "failure_reason": None,
    }
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        t0 = time.monotonic()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ms = (time.monotonic() - t0) * 1000
            result.update(status_code=resp.status, final_url=resp.url, response_time_ms=round(ms, 1))
    except urllib.error.HTTPError as e:
        result.update(status_code=e.code, failure_reason=str(e.reason))
    except urllib.error.URLError as e:
        result["failure_reason"] = str(e.reason)
    except Exception as e:
        result["failure_reason"] = f"{type(e).__name__}: {e}"
    return result


def main():
    ap = argparse.ArgumentParser(description="Link health checker")
    ap.add_argument("--smoke", action="store_true", help="P0 only")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--output", type=str, help="JSONL output path")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    urls = load_urls(smoke=args.smoke)[:args.limit]
    # Deduplicate by URL
    seen = set()
    deduped = []
    for u in urls:
        if u["url"] not in seen:
            seen.add(u["url"])
            deduped.append(u)
    urls = deduped

    print(f"Link checker: {len(urls)} URLs (smoke={args.smoke}, limit={args.limit})", file=sys.stderr)

    if args.dry_run:
        for e in urls:
            print(f"  [{e['source_id']}] {e['url']}", file=sys.stderr)
        print(f"\nDry run complete. {len(urls)} URLs would be checked.", file=sys.stderr)
        return 0

    out = open(args.output, "w") if args.output else sys.stdout
    ok = fail = 0
    last_domain = None

    for i, entry in enumerate(urls):
        domain = urlparse(entry["url"]).netloc
        if domain == last_domain:
            time.sleep(1.0 / entry.get("rate", 1.0))
        last_domain = domain

        r = check(entry["url"])
        r["source_id"] = entry["source_id"]
        r["url_field"] = entry["url_field"]
        r["tier"] = entry["tier"]

        s = r["status_code"]
        is_ok = s is not None and 200 <= s < 400
        ok += 1 if is_ok else 0
        fail += 0 if is_ok else 1
        icon = "OK" if is_ok else "FAIL"
        print(f"  [{i+1}/{len(urls)}] {icon} {s or 'ERR'} {entry['url'][:80]}", file=sys.stderr)
        out.write(json.dumps(r, ensure_ascii=False) + "\n")

    if args.output:
        out.close()
    print(f"\nResults: {ok} OK, {fail} FAIL, {len(urls)} total", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
