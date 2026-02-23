#!/usr/bin/env python3
"""Verify URLs in vivo — checks that fuente_url in tramites JSON and
source URLs in registry.yaml are still reachable.

Uses requests library with browser-like User-Agent.  Falls back from HEAD
to GET when a site returns 403/405 on HEAD (common with government servers).

Usage:
    cd civicaid-voice/back && python scripts/check_sources.py
"""

import json
import sys
import time
from pathlib import Path

import requests
import yaml

# Allow running from back/ or back/scripts/
BACK_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BACK_DIR / "data"
TRAMITES_DIR = DATA_DIR / "tramites"
REGISTRY_PATH = DATA_DIR / "sources" / "registry.yaml"

REQUEST_TIMEOUT = 20

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.5",
}


def _check_url(url: str) -> dict:
    """Check a URL with HEAD, falling back to GET on 403/405."""
    result = {"url": url, "status": None, "ok": False, "error": None, "latency_ms": 0, "method": "HEAD"}
    start = time.time()

    try:
        resp = requests.head(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        result["status"] = resp.status_code

        # Some gov sites block HEAD — retry with GET
        if resp.status_code in (403, 405, 406):
            result["method"] = "GET"
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True, stream=True)
            result["status"] = resp.status_code
            resp.close()

        result["ok"] = result["status"] < 400

        # madrid.es blocks ALL automated requests (even homepage) — mark as likely OK
        if result["status"] == 403 and "madrid.es" in url and "comunidad.madrid" not in url:
            result["ok"] = True
            result["error"] = "403 bot-blocked (works in browser)"

    except requests.exceptions.SSLError as e:
        # Retry without SSL verification for gov sites with cert issues
        try:
            result["method"] = "GET (no-verify)"
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True, verify=False, stream=True)
            result["status"] = resp.status_code
            result["ok"] = result["status"] < 400
            resp.close()
        except Exception as e2:
            result["error"] = f"SSL+retry failed: {e2}"

    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Connection error: {e}"
    except requests.exceptions.Timeout:
        result["error"] = "Timeout"
    except Exception as e:
        result["error"] = str(e)

    result["latency_ms"] = round((time.time() - start) * 1000)
    return result


def collect_tramites_urls() -> list[dict]:
    """Read each tramites JSON and extract fuente_url."""
    urls = []
    if not TRAMITES_DIR.exists():
        print(f"WARNING: {TRAMITES_DIR} not found")
        return urls
    for path in sorted(TRAMITES_DIR.glob("*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        fuente = data.get("fuente_url", "")
        if fuente:
            urls.append({
                "source": f"tramites/{path.name}",
                "tramite": data.get("tramite", path.stem),
                "url": fuente,
            })
    return urls


def collect_registry_urls() -> list[dict]:
    """Read registry.yaml and extract portal_url / sede_url from each source."""
    urls = []
    if not REGISTRY_PATH.exists():
        print(f"WARNING: {REGISTRY_PATH} not found")
        return urls
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    for section_key in ("tier_1_age", "tier_2_ccaa", "tier_3_other"):
        section = data.get(section_key, {})
        sources = section.get("sources", [])
        for src in sources:
            src_id = src.get("id", "unknown")
            for url_key in ("portal_url", "sede_url"):
                url = src.get(url_key, "")
                if url:
                    urls.append({
                        "source": f"registry/{src_id}",
                        "field": url_key,
                        "url": url,
                    })
    return urls


def main() -> int:
    # Suppress InsecureRequestWarning for SSL-retry checks
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("=" * 70)
    print("Clara Source URL Checker")
    print("=" * 70)

    # 1. Tramites URLs
    tramites = collect_tramites_urls()
    print(f"\n--- Tramites fuente_url ({len(tramites)} URLs) ---\n")

    broken_count = 0
    broken_list: list[dict] = []
    for entry in tramites:
        result = _check_url(entry["url"])
        status_str = str(result["status"] or "ERR")
        icon = "OK" if result["ok"] else "FAIL"
        method = f" [{result['method']}]" if result["method"] != "HEAD" else ""
        line = f"  [{icon}] {status_str:>4}  {entry['tramite']:<30} {entry['url']}{method}"
        if result["error"]:
            line += f"  ({result['error']})"
        print(line)
        if not result["ok"]:
            broken_count += 1
            broken_list.append({**entry, **result})

    # 2. Registry URLs
    registry = collect_registry_urls()
    print(f"\n--- Registry URLs ({len(registry)} URLs) ---\n")

    for entry in registry:
        result = _check_url(entry["url"])
        status_str = str(result["status"] or "ERR")
        icon = "OK" if result["ok"] else "FAIL"
        method = f" [{result['method']}]" if result["method"] != "HEAD" else ""
        line = f"  [{icon}] {status_str:>4}  {entry['source']:<40} {entry['url']}{method}"
        if result["error"]:
            line += f"  ({result['error']})"
        print(line)
        if not result["ok"]:
            broken_count += 1
            broken_list.append({**entry, **result})

    # Summary
    total = len(tramites) + len(registry)
    active = total - broken_count
    print(f"\n{'=' * 70}")
    print(f"SUMMARY: {active}/{total} URLs active, {broken_count} broken/unreachable")
    if broken_list:
        print(f"\nBroken URLs requiring attention:")
        for b in broken_list:
            tramite = b.get("tramite", b.get("source", "?"))
            print(f"  - {tramite}: {b['url']} (status={b.get('status')}, error={b.get('error')})")
    print(f"{'=' * 70}")

    return 1 if broken_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
