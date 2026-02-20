"""BOE (Boletin Oficial del Estado) monitoring — MVP keyword alerts."""

import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError

from src.core.config import config

logger = logging.getLogger(__name__)


@dataclass
class BOEAlert:
    """A BOE entry that matched monitoring keywords."""

    title: str
    url: str
    published_date: str
    keywords_matched: list[str] = field(default_factory=list)
    relevance_score: float = 0.0


class BOEMonitor:
    """Monitor BOE RSS feed for relevant updates.

    MVP implementation: fetch RSS, match against keywords, score relevance.
    Uses only stdlib (xml.etree, urllib) — no external dependencies.
    """

    BOE_RSS_URL = "https://www.boe.es/rss/boe.php?s=1"  # Seccion I

    KEYWORDS = [
        "prestacion",
        "ayuda",
        "ingreso minimo",
        "extranjeria",
        "empadronamiento",
        "discapacidad",
        "desempleo",
        "alquiler",
        "subsidio",
        "pension",
        "tarjeta sanitaria",
        "residencia",
        "asilo",
    ]

    def __init__(self, rss_url: str = None, keywords: list[str] = None):
        self.rss_url = rss_url or self.BOE_RSS_URL
        self.keywords = keywords or self.KEYWORDS

    def check_updates(self, days_back: int = 7) -> list[BOEAlert]:
        """Check BOE RSS for relevant updates within days_back window.

        Returns a list of BOEAlert for entries matching keywords.
        Returns empty list on network errors (fail gracefully).
        """
        if not config.RAG_BOE_MONITOR_ENABLED:
            logger.debug("BOE monitor disabled (RAG_BOE_MONITOR_ENABLED=false)")
            return []

        try:
            content = self._fetch_rss()
        except Exception as exc:
            logger.warning("Failed to fetch BOE RSS: %s", exc)
            return []

        if not content:
            return []

        entries = self._parse_rss(content)
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)

        alerts: list[BOEAlert] = []
        for entry in entries:
            # Filter by date if available
            pub_date_str = entry.get("published_date", "")
            if pub_date_str:
                try:
                    pub_date = self._parse_date(pub_date_str)
                    if pub_date and pub_date < cutoff:
                        continue
                except Exception:
                    pass  # Include entries with unparseable dates

            title = entry.get("title", "")
            summary = entry.get("summary", "")
            matched, score = self._match_keywords(title, summary)

            if matched:
                alerts.append(BOEAlert(
                    title=title,
                    url=entry.get("url", ""),
                    published_date=pub_date_str,
                    keywords_matched=matched,
                    relevance_score=score,
                ))

        # Sort by relevance descending
        alerts.sort(key=lambda a: a.relevance_score, reverse=True)

        logger.info(
            "BOE check: %d entries parsed, %d alerts matched",
            len(entries), len(alerts),
        )
        return alerts

    def _fetch_rss(self) -> str:
        """Fetch RSS content from BOE URL."""
        req = Request(
            self.rss_url,
            headers={"User-Agent": "CivicAid-Clara/1.0 (BOE monitor)"},
        )
        try:
            with urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except URLError as exc:
            logger.warning("BOE RSS fetch error: %s", exc)
            return ""

    def _parse_rss(self, content: str) -> list[dict]:
        """Parse RSS XML into a list of entry dicts."""
        entries: list[dict] = []

        try:
            root = ET.fromstring(content)
        except ET.ParseError as exc:
            logger.warning("Failed to parse BOE RSS XML: %s", exc)
            return entries

        # Handle both RSS 2.0 (<channel><item>) and Atom (<entry>)
        # BOE uses RSS 2.0
        for item in root.iter("item"):
            entry = {
                "title": self._get_text(item, "title"),
                "url": self._get_text(item, "link"),
                "summary": self._get_text(item, "description"),
                "published_date": self._get_text(item, "pubDate"),
            }
            if entry["title"]:
                entries.append(entry)

        return entries

    def _match_keywords(
        self, title: str, summary: str,
    ) -> tuple[list[str], float]:
        """Match title and summary against keywords.

        Returns (matched_keywords, relevance_score).
        Score = matched_count / total_keywords, boosted by title matches.
        """
        text = f"{title} {summary}".lower()
        matched = []

        for kw in self.keywords:
            if kw.lower() in text:
                matched.append(kw)

        if not matched:
            return [], 0.0

        # Base score: fraction of keywords matched
        base_score = len(matched) / len(self.keywords)

        # Boost for title matches (title matches are more relevant)
        title_lower = title.lower()
        title_matches = sum(1 for kw in matched if kw.lower() in title_lower)
        title_boost = 0.2 * (title_matches / max(len(matched), 1))

        score = min(1.0, base_score + title_boost)
        return matched, round(score, 3)

    @staticmethod
    def _get_text(element: ET.Element, tag: str) -> str:
        """Safely extract text from an XML child element."""
        child = element.find(tag)
        if child is not None and child.text:
            return child.text.strip()
        return ""

    @staticmethod
    def _parse_date(date_str: str) -> datetime | None:
        """Parse RSS date formats (RFC 822 variant)."""
        # BOE uses format like "Mon, 17 Feb 2025 00:00:00 +0100"
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
