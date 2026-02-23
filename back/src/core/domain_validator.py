"""Domain validator — enforces allowlist/blocklist policy on URLs.
Singleton that loads data/policy/allowlist.yaml and blocklist.yaml once,
then exposes is_domain_approved(url) -> bool.

Validation order:
  1. Blocklist explicit domain -> reject
  2. Blocklist wildcard patterns (*.wordpress.com) -> reject
  3. Auto-allow *.gob.es -> approve
  4. Allowlist explicit (Tier 1 AGE, Tier 2 CCAA, Tier 3 Municipal) -> approve
  5. Default -> reject + log warning
"""

import logging
import os
import re
from typing import Optional
from urllib.parse import urlparse

import yaml

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, "data", "policy"
)


def _load_yaml(filename: str) -> dict:
    path = os.path.normpath(os.path.join(_BASE_DIR, filename))
    if not os.path.exists(path):
        logger.warning("Policy file not found: %s", path)
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _extract_domain(url: str) -> Optional[str]:
    """Extract the hostname from a URL, stripping www. prefix."""
    if not url:
        return None
    # Add scheme if missing so urlparse works
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        host = urlparse(url).hostname
        if host:
            host = host.lower()
            if host.startswith("www."):
                host = host[4:]
            return host
    except Exception:
        pass
    return None


class DomainValidator:
    """Validates URLs against government allowlist/blocklist policy."""

    def __init__(self) -> None:
        self._blocked_domains: set[str] = set()
        self._blocked_patterns: list[re.Pattern] = []
        self._allowed_domains: set[str] = set()
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._load_blocklist()
        self._load_allowlist()
        self._loaded = True
        logger.info(
            "DomainValidator loaded: %d blocked domains, %d blocked patterns, %d allowed domains",
            len(self._blocked_domains),
            len(self._blocked_patterns),
            len(self._allowed_domains),
        )

    def _load_blocklist(self) -> None:
        data = _load_yaml("blocklist.yaml")
        for cat in data.get("categories", []):
            for d in cat.get("domains", []):
                self._blocked_domains.add(d.lower())
        for pat in data.get("patterns", []):
            # Convert glob *.example.com to regex
            regex = re.escape(pat).replace(r"\*", r"[^.]+")
            self._blocked_patterns.append(re.compile(f"^{regex}$", re.IGNORECASE))

    def _load_allowlist(self) -> None:
        data = _load_yaml("allowlist.yaml")
        # Tier 1 AGE
        for entry in data.get("tier_1_age", {}).get("domains", []):
            self._add_domain(entry)
        # Tier 2 CCAA
        for entry in data.get("tier_2_ccaa", {}).get("domains", []):
            self._add_domain(entry)
        # Tier 3 Municipal
        for entry in data.get("tier_3_municipal", {}).get("domains", []):
            self._add_domain(entry)

    def _add_domain(self, entry: dict) -> None:
        domain = entry.get("domain", "").lower()
        if domain:
            self._allowed_domains.add(domain)
        for alias in entry.get("aliases", []):
            alias_clean = alias.lower()
            # Strip www. from aliases too
            if alias_clean.startswith("www."):
                alias_clean = alias_clean[4:]
            self._allowed_domains.add(alias_clean)

    def is_domain_approved(self, url: str) -> bool:
        """Check if a URL's domain is approved per policy.

        Returns True if approved, False if blocked or unknown.
        """
        self._ensure_loaded()
        domain = _extract_domain(url)
        if not domain:
            return False

        # 1. Blocklist explicit
        if domain in self._blocked_domains:
            logger.warning("Domain blocked (explicit blocklist): %s", domain)
            return False

        # 2. Blocklist wildcard patterns
        for pattern in self._blocked_patterns:
            if pattern.match(domain):
                logger.warning("Domain blocked (pattern %s): %s", pattern.pattern, domain)
                return False

        # 3. Auto-allow *.gob.es
        if domain.endswith(".gob.es") or domain == "gob.es":
            return True

        # 4. Allowlist explicit — check domain and parent domains
        if domain in self._allowed_domains:
            return True
        # Check if it's a subdomain of an allowed domain
        parts = domain.split(".")
        for i in range(1, len(parts)):
            parent = ".".join(parts[i:])
            if parent in self._allowed_domains:
                return True

        # 5. Default reject
        logger.warning("Domain rejected (not in allowlist): %s (from %s)", domain, url)
        return False

    def reload(self) -> None:
        """Force reload of policy files (for testing)."""
        self._blocked_domains.clear()
        self._blocked_patterns.clear()
        self._allowed_domains.clear()
        self._loaded = False
        self._ensure_loaded()


# Singleton
_validator: Optional[DomainValidator] = None


def get_validator() -> DomainValidator:
    global _validator
    if _validator is None:
        _validator = DomainValidator()
    return _validator


def is_domain_approved(url: str) -> bool:
    """Convenience function — calls singleton validator."""
    return get_validator().is_domain_approved(url)


def extract_urls(text: str) -> list[str]:
    """Extract all URLs from a text string."""
    url_pattern = re.compile(
        r'https?://[^\s<>"\'\])\},;]+',
        re.IGNORECASE,
    )
    return url_pattern.findall(text)


def reset_validator() -> None:
    """Reset singleton (for testing)."""
    global _validator
    _validator = None
