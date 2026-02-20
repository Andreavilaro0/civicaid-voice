# Link Health Checker Specification

> **Scope:** Automated monitoring of all URLs in Clara's source registry to ensure links remain accessible, valid, and content-stable.
> **Owner:** Link Governance team
> **Last updated:** 2026-02-18
> **Depends on:** `allowlist.md`, `canonicalization.md`

---

## Purpose

Clara serves vulnerable populations who depend on accurate government links. A broken or stale link erodes trust and can block a user from completing a critical procedure. The Link Health Checker continuously validates every URL in the source registry and triggers alerts before broken links reach users.

Goals:
1. Detect dead, moved, or degraded government URLs before they affect users.
2. Track content drift (page content changes silently without URL change).
3. Maintain uptime metrics per domain to inform crawl priority decisions.
4. Auto-flag failing domains for allowlist review.

---

## Check Types

### 1. HTTP HEAD Request (Availability)

Lightweight check to verify the URL is reachable and returns a valid status code.

| Parameter | Value |
|-----------|-------|
| Method | `HEAD` (fall back to `GET` if HEAD returns 405) |
| Connect timeout | 30 seconds |
| Read timeout | 30 seconds |
| Follow redirects | Yes, up to 5 hops |
| User-Agent | `ClaraLinkChecker/1.0 (+https://github.com/civicaid-voice)` |
| Expected success | HTTP 200, 301, 302 |

### 2. SSL Certificate Validation

Verify the TLS certificate is valid and not near expiry.

| Check | Threshold |
|-------|-----------|
| Certificate valid | Must not be expired or self-signed |
| Expiry warning | Alert if certificate expires within 14 days |
| Chain completeness | Full chain must validate against system CA store |
| Protocol minimum | TLS 1.2 |

### 3. Content Hash Comparison (Drift Detection)

Detect silent content changes by comparing a hash of the page body across checks.

| Parameter | Value |
|-----------|-------|
| Hash algorithm | SHA-256 |
| Scope | Main content body only (after boilerplate removal via trafilatura) |
| Comparison | Current hash vs. last stored hash |
| Drift threshold | Any hash change = flag for review |
| Storage | `content_hash` field in the source registry entry |

Content drift does not automatically trigger removal. It flags the URL for human review because the content may have been legitimately updated (e.g., new fiscal year amounts).

---

## Scheduling

Check frequency is determined by the URL's crawl priority tier (defined in `allowlist.md`).

| Priority | Tier | Check frequency | Examples |
|----------|------|-----------------|----------|
| **P0** | Tier 1 core (AGE portals) | **Daily** | `sepe.es`, `seg-social.es`, `boe.es` |
| **P1** | Tier 1 secondary + Tier 2 (CCAA) | **Weekly** | `comunidad.madrid`, `juntadeandalucia.es` |
| **P2** | Tier 3 (Municipal) | **Monthly** | `sede.madrid.es`, `sede.sevilla.org` |

### Scheduling Rules

- Checks run during off-peak hours (02:00-06:00 CET) to minimize load on government servers.
- Randomize check order within each priority band to avoid hammering a single domain.
- Rate limit: maximum 1 request per second per domain (same as fetch policy in `ingestion-playbook.md`).
- If a check fails, schedule an immediate retry after 1 hour (regardless of normal frequency).

---

## Alert Thresholds

| Condition | Action |
|-----------|--------|
| 1 failure | Log. No alert. Schedule retry in 1 hour. |
| 2 consecutive failures | Log with WARNING level. |
| **3 consecutive failures** | **ALERT.** Notify team via configured channel. Flag URL in registry as `degraded`. |
| 5 consecutive failures | Escalate. Consider temporarily hiding link from user-facing output. |
| **7 calendar days continuously down** | **Remove from active index.** URL still stored in registry as `inactive`. Requires manual re-activation. |
| SSL expiry < 14 days | ALERT. Informational only (government IT will handle renewal). |
| Content hash changed | Flag for review. Not an alert -- content updates are expected. |
| Redirect chain changed | ALERT. The canonical URL may need updating (see `canonicalization.md` Rule 7). |

### Alert Channels

- Primary: log entry with severity `ALERT` (picked up by observability stack per `OBSERVABILITY.md`).
- Secondary: weekly summary report (see Report Format below).
- Future (Q2+): Slack/email integration.

---

## Response Handling

How the checker interprets each HTTP status code.

| Status | Interpretation | Action |
|--------|---------------|--------|
| **200** | Healthy | Record success. Compare content hash. |
| **301** | Permanent redirect | Follow. If final destination differs from stored canonical URL, flag for canonicalization update. |
| **302/307** | Temporary redirect | Follow. If this is new behavior (previously returned 200), log the change. |
| **304** | Not modified | Healthy (when using conditional requests with `If-None-Match`/`If-Modified-Since`). No content hash update needed. |
| **403** | Forbidden | May indicate IP block or auth requirement. Log. Count as failure for alert threshold. |
| **404** | Not found | Page removed or URL changed. Count as failure. |
| **410** | Gone | Page explicitly removed. Immediately mark as `inactive` in registry. |
| **429** | Rate limited | Do NOT count as failure. Back off per `Retry-After` header. Reschedule. |
| **5xx** | Server error | Count as failure. Retry with exponential backoff (2s, 4s, 8s, max 3 retries). |
| **Timeout** | No response within 60s | Count as failure. Retry once with doubled timeout. |
| **DNS error** | Domain does not resolve | Count as failure. Critical -- domain may be completely gone. |
| **SSL error** | Certificate invalid/expired | Count as failure. Log certificate details for review. |

---

## Metrics to Track

### Per-URL Metrics

| Metric | Description | Type |
|--------|-------------|------|
| `uptime_pct` | Percentage of successful checks over rolling 30-day window | Float 0.0-100.0 |
| `avg_response_time_ms` | Average HEAD request response time (rolling 30 days) | Integer, milliseconds |
| `last_check_at` | Timestamp of most recent check | ISO 8601 |
| `last_success_at` | Timestamp of most recent successful check | ISO 8601 |
| `last_status_code` | HTTP status from most recent check | Integer |
| `consecutive_failures` | Count of consecutive failed checks (resets on success) | Integer |
| `content_hash` | SHA-256 of last successfully fetched content body | Hex string |
| `content_hash_changed_at` | Timestamp of last content hash change | ISO 8601 |
| `redirect_chain` | Ordered list of URLs in current redirect chain | Array of strings |
| `ssl_expiry` | TLS certificate expiration date | ISO 8601 date |

### Per-Domain Aggregate Metrics

| Metric | Description |
|--------|-------------|
| `domain_uptime_pct` | Average uptime across all URLs on the domain |
| `domain_avg_response_ms` | Average response time across all URLs on the domain |
| `total_urls` | Count of registered URLs on the domain |
| `failing_urls` | Count of URLs currently in failure state |
| `last_full_check` | Timestamp of last complete check cycle for this domain |

---

## Report Format

A weekly markdown report is generated summarizing the health of all monitored URLs.

### Summary Section

```markdown
## Link Health Report -- Week of 2026-02-16

**Total URLs monitored:** 142
**Healthy:** 135 (95.1%)
**Degraded:** 4 (2.8%)
**Down:** 2 (1.4%)
**New issues this week:** 3
**Resolved this week:** 1
```

### Detail Table

| Domain | URL (path) | Last Check | Status | Response (ms) | Uptime 30d | Issues |
|--------|------------|------------|--------|---------------|------------|--------|
| sepe.es | `/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html` | 2026-02-18T03:14Z | 200 | 342 | 99.8% | -- |
| seg-social.es | `/wps/portal/wss/internet/Trabajadores/...` | 2026-02-18T03:15Z | 200 | 1205 | 98.2% | Slow (>1s) |
| sede.madrid.es | `/portal/site/tramites` | 2026-02-17T03:22Z | 404 | -- | 87.3% | Down 3 days, ALERT |
| comunidad.madrid | `/servicios/salud/tarjeta-sanitaria` | 2026-02-18T03:18Z | 301 | 289 | 100% | Redirect changed |

### Issues Summary

```markdown
### Active Issues

1. **sede.madrid.es/portal/site/tramites** -- 404 since 2026-02-15. 3 consecutive failures. ALERT sent.
2. **juntadeandalucia.es/tramites/...** -- SSL certificate expires 2026-03-01. Warning.
3. **sede.seg-social.gob.es/wps/...** -- Content hash changed 2026-02-17. Review pending.
```

---

## Pseudocode: Health Checker

```python
import hashlib
import ssl
import socket
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

import requests
from trafilatura import extract as trafilatura_extract


# ============================================================
# Data structures
# ============================================================

@dataclass
class CheckResult:
    url: str
    checked_at: str                    # ISO 8601
    status_code: Optional[int]         # None if connection failed entirely
    response_time_ms: Optional[int]
    redirect_chain: list[str]
    content_hash: Optional[str]        # SHA-256 of extracted body
    ssl_expiry: Optional[str]          # ISO 8601 date
    ssl_valid: bool
    error: Optional[str]               # Human-readable error if failed

@dataclass
class URLRecord:
    url: str
    domain: str
    priority: str                      # "P0", "P1", "P2"
    tier: int                          # 1, 2, 3
    last_check: Optional[CheckResult] = None
    consecutive_failures: int = 0
    uptime_checks_30d: list[bool] = field(default_factory=list)
    content_hash: Optional[str] = None
    status: str = "active"             # "active" | "degraded" | "inactive"


# ============================================================
# Configuration
# ============================================================

SCHEDULE = {
    "P0": timedelta(days=1),
    "P1": timedelta(weeks=1),
    "P2": timedelta(days=30),
}

ALERT_THRESHOLD = 3            # consecutive failures before alert
DEGRADED_THRESHOLD = 5         # consecutive failures before degraded
REMOVAL_THRESHOLD_DAYS = 7     # calendar days down before removal from active index
REQUEST_TIMEOUT = (30, 30)     # (connect, read) in seconds
MAX_REDIRECTS = 5
USER_AGENT = "ClaraLinkChecker/1.0 (+https://github.com/civicaid-voice)"
SSL_EXPIRY_WARNING_DAYS = 14


# ============================================================
# Core check functions
# ============================================================

def check_http(url: str) -> CheckResult:
    """Perform HTTP HEAD check with GET fallback."""
    checked_at = datetime.utcnow().isoformat() + "Z"
    redirect_chain = []

    try:
        resp = requests.head(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )

        # Some government servers reject HEAD -- fall back to GET
        if resp.status_code == 405:
            resp = requests.get(
                url,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                headers={"User-Agent": USER_AGENT},
            )

        redirect_chain = [r.url for r in resp.history] + [resp.url]

        # Compute content hash when body is available (GET responses)
        content_hash = None
        if resp.text:
            main_content = trafilatura_extract(resp.text) or resp.text
            content_hash = hashlib.sha256(
                main_content.encode("utf-8")
            ).hexdigest()

        response_time_ms = int(resp.elapsed.total_seconds() * 1000)

        return CheckResult(
            url=url,
            checked_at=checked_at,
            status_code=resp.status_code,
            response_time_ms=response_time_ms,
            redirect_chain=redirect_chain,
            content_hash=content_hash,
            ssl_expiry=None,
            ssl_valid=True,
            error=None,
        )

    except requests.exceptions.Timeout:
        return CheckResult(
            url=url, checked_at=checked_at,
            status_code=None, response_time_ms=None,
            redirect_chain=[], content_hash=None,
            ssl_expiry=None, ssl_valid=False,
            error="Timeout after 60s",
        )
    except requests.exceptions.ConnectionError as e:
        return CheckResult(
            url=url, checked_at=checked_at,
            status_code=None, response_time_ms=None,
            redirect_chain=[], content_hash=None,
            ssl_expiry=None, ssl_valid=False,
            error=f"Connection error: {e}",
        )


def check_ssl(url: str) -> tuple[bool, Optional[str]]:
    """Validate SSL certificate and return (is_valid, expiry_date_str)."""
    hostname = urlparse(url).hostname
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.socket(), server_hostname=hostname
        ) as sock:
            sock.settimeout(10)
            sock.connect((hostname, 443))
            cert = sock.getpeercert()
            expiry_str = cert.get("notAfter", "")
            expiry_date = datetime.strptime(
                expiry_str, "%b %d %H:%M:%S %Y %Z"
            )
            is_valid = expiry_date > datetime.utcnow()
            return is_valid, expiry_date.strftime("%Y-%m-%d")
    except Exception:
        return False, None


# ============================================================
# Orchestrator
# ============================================================

def run_health_checks(registry: list[URLRecord]) -> list[CheckResult]:
    """Run scheduled health checks on all due URLs."""
    now = datetime.utcnow()
    results = []

    for record in registry:
        # Skip inactive URLs
        if record.status == "inactive":
            continue

        # Check if this URL is due for a check
        if record.last_check:
            last = datetime.fromisoformat(
                record.last_check.checked_at.rstrip("Z")
            )
            interval = SCHEDULE[record.priority]
            if now - last < interval:
                continue

        # --- Phase 1: HTTP check ---
        result = check_http(record.url)

        # --- Phase 2: SSL check ---
        ssl_valid, ssl_expiry = check_ssl(record.url)
        result.ssl_valid = ssl_valid
        result.ssl_expiry = ssl_expiry

        # --- Evaluate result ---
        is_success = result.status_code in (200, 301, 302, 304)

        if is_success:
            record.consecutive_failures = 0
            if record.status == "degraded":
                record.status = "active"
                log_event(record.url, "recovered")

            # Content drift detection
            if (
                result.content_hash
                and record.content_hash
                and result.content_hash != record.content_hash
            ):
                flag_content_drift(record, result)

            record.content_hash = result.content_hash or record.content_hash

            # Redirect chain change detection
            if (
                record.last_check
                and record.last_check.redirect_chain
                and record.last_check.redirect_chain != result.redirect_chain
            ):
                flag_redirect_change(record, result)
        else:
            record.consecutive_failures += 1

        # Update rolling uptime window (keep last 30 entries)
        record.uptime_checks_30d.append(is_success)
        if len(record.uptime_checks_30d) > 30:
            record.uptime_checks_30d = record.uptime_checks_30d[-30:]

        # --- Alert logic ---
        if record.consecutive_failures == ALERT_THRESHOLD:
            send_alert(record, result)

        if record.consecutive_failures >= DEGRADED_THRESHOLD:
            record.status = "degraded"

        # --- Removal logic (7 days down) ---
        if record.consecutive_failures > 0 and record.last_check:
            last_success = find_last_success(record)
            if last_success and (now - last_success).days >= REMOVAL_THRESHOLD_DAYS:
                deactivate_url(record)

        # --- SSL expiry warning ---
        if ssl_expiry:
            expiry_dt = datetime.strptime(ssl_expiry, "%Y-%m-%d")
            if (expiry_dt - now).days < SSL_EXPIRY_WARNING_DAYS:
                send_ssl_warning(record, ssl_expiry)

        # --- HTTP 410 Gone: immediate deactivation ---
        if result.status_code == 410:
            deactivate_url(record)

        record.last_check = result
        results.append(result)

    return results


# ============================================================
# Integration hooks (stubs -- implement per observability stack)
# ============================================================

def flag_content_drift(record, result):
    log_review(record.url, "content_drift",
               old_hash=record.content_hash,
               new_hash=result.content_hash)

def flag_redirect_change(record, result):
    log_review(record.url, "redirect_change",
               old_chain=record.last_check.redirect_chain,
               new_chain=result.redirect_chain)

def deactivate_url(record):
    record.status = "inactive"
    log_review(record.url, "deactivated",
               detail=f"{record.consecutive_failures} consecutive failures")

def send_alert(record, result):
    log_event(record.url, f"ALERT: {record.consecutive_failures} consecutive failures, "
              f"last status: {result.status_code or result.error}")

def send_ssl_warning(record, expiry):
    log_event(record.url, f"SSL WARNING: certificate expires {expiry}")

def find_last_success(record) -> Optional[datetime]:
    """Find timestamp of last successful check from history."""
    pass  # Implementation depends on check history storage

def log_review(url, reason, **kwargs):
    """Add entry to the human review queue."""
    pass

def log_event(url, message):
    """Append to audit log."""
    pass
```

---

## Integration with the Allowlist

The health checker feeds back into the allowlist (defined in `allowlist.md`) through the following rules.

### Auto-Flag for Review

| Condition | Action on Allowlist |
|-----------|---------------------|
| Domain has >50% URLs failing | Flag entire domain for allowlist review |
| Single URL down for 7+ days | Mark URL `inactive`; domain stays on allowlist |
| All URLs on a domain down for 14+ days | Flag domain for potential removal from allowlist |
| SSL certificate expired and not renewed within 7 days | Flag domain for review |
| Domain redirects to a non-allowlisted domain | Immediate flag -- possible domain takeover or migration |

### Feedback Loop

```
Health Checker --> Detects failure
                    |
                    +--> Updates URL status in source registry
                    |      (active -> degraded -> inactive)
                    |
                    +--> If domain-level issue:
                    |      Flag domain in allowlist for review
                    |      (per Domain Review Process in allowlist.md)
                    |
                    +--> If content drift:
                    |      Flag for re-extraction
                    |      (triggers ingestion pipeline re-run for that URL)
                    |
                    +--> Weekly report includes all flagged items
                           for human review
```

### Re-Activation

A URL marked `inactive` can be re-activated only through manual review:
1. Team member verifies the URL is back online and serving correct content.
2. URL passes all three check types (HTTP, SSL, content hash baseline).
3. Team member updates the registry entry status to `active`.
4. Normal check scheduling resumes.

---

## Storage

Health check results are stored alongside the source registry:

```
data/
  health/
    checks/
      <url_hash>.json          # Latest CheckResult per URL + rolling 30-check history
    reports/
      report-YYYY-WW.md       # Weekly markdown report
    metrics/
      domain-metrics.json      # Aggregated per-domain metrics
```

---

## Out of Scope (Q2+)

- Real-time alerting via Slack or email (Q2 -- depends on observability integration).
- Automated re-crawl trigger on content drift (Q2 -- requires ingestion pipeline automation).
- Visual diff of changed pages (Q3 -- useful but not critical).
- Monitoring of non-HTTP resources (FTP, SFTP) -- not applicable to current registry.
