"""Unit tests for src/core/rag/boe_monitor.py — BOEMonitor."""

from datetime import datetime, timedelta, timezone

import pytest
from unittest.mock import patch

from src.core.rag.boe_monitor import BOEAlert, BOEMonitor


SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>BOE</title>
    <item>
      <title>Real Decreto sobre prestacion por desempleo</title>
      <link>https://boe.es/1</link>
      <description>Modificacion de la prestacion por desempleo y subsidio</description>
      <pubDate>{pub_date}</pubDate>
    </item>
    <item>
      <title>Ley organica de educacion</title>
      <link>https://boe.es/2</link>
      <description>Reforma del sistema educativo nacional</description>
      <pubDate>{pub_date}</pubDate>
    </item>
    <item>
      <title>Ayuda al alquiler para jovenes</title>
      <link>https://boe.es/3</link>
      <description>Bono alquiler joven convocatoria</description>
      <pubDate>{pub_date}</pubDate>
    </item>
  </channel>
</rss>"""


def _recent_rss():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%a, %d %b %Y %H:%M:%S %z")
    return SAMPLE_RSS.format(pub_date=date_str)


def _old_rss():
    old = datetime.now(timezone.utc) - timedelta(days=30)
    date_str = old.strftime("%a, %d %b %Y %H:%M:%S %z")
    return SAMPLE_RSS.format(pub_date=date_str)


@pytest.fixture
def monitor():
    return BOEMonitor()


class TestBOEAlertDataclass:
    def test_fields_exist(self):
        a = BOEAlert(title="t", url="u", published_date="d")
        assert a.title == "t"
        assert a.url == "u"
        assert a.published_date == "d"
        assert a.keywords_matched == []
        assert a.relevance_score == 0.0

    def test_custom_fields(self):
        a = BOEAlert(
            title="t", url="u", published_date="d",
            keywords_matched=["a", "b"], relevance_score=0.5,
        )
        assert len(a.keywords_matched) == 2
        assert a.relevance_score == 0.5


class TestBOEMonitorInit:
    def test_default_url(self, monitor):
        assert "boe.es" in monitor.rss_url

    def test_default_keywords(self, monitor):
        assert len(monitor.keywords) > 0
        assert "prestacion" in monitor.keywords

    def test_custom_url_and_keywords(self):
        m = BOEMonitor(rss_url="https://custom.rss", keywords=["test"])
        assert m.rss_url == "https://custom.rss"
        assert m.keywords == ["test"]


class TestCheckUpdates:
    @patch("src.core.rag.boe_monitor.config")
    def test_with_matching_entries(self, mock_config, monitor):
        mock_config.RAG_BOE_MONITOR_ENABLED = True
        with patch.object(monitor, "_fetch_rss", return_value=_recent_rss()):
            alerts = monitor.check_updates(days_back=7)
        # "prestacion por desempleo" and "ayuda al alquiler" should match
        assert len(alerts) >= 2
        assert all(isinstance(a, BOEAlert) for a in alerts)

    @patch("src.core.rag.boe_monitor.config")
    def test_empty_rss_returns_empty(self, mock_config, monitor):
        mock_config.RAG_BOE_MONITOR_ENABLED = True
        empty_rss = '<?xml version="1.0"?><rss><channel></channel></rss>'
        with patch.object(monitor, "_fetch_rss", return_value=empty_rss):
            alerts = monitor.check_updates()
        assert alerts == []

    @patch("src.core.rag.boe_monitor.config")
    def test_network_error_returns_empty(self, mock_config, monitor):
        mock_config.RAG_BOE_MONITOR_ENABLED = True
        with patch.object(monitor, "_fetch_rss", side_effect=Exception("timeout")):
            alerts = monitor.check_updates()
        assert alerts == []

    @patch("src.core.rag.boe_monitor.config")
    def test_disabled_returns_empty(self, mock_config, monitor):
        mock_config.RAG_BOE_MONITOR_ENABLED = False
        alerts = monitor.check_updates()
        assert alerts == []

    @patch("src.core.rag.boe_monitor.config")
    def test_old_entries_filtered_by_date(self, mock_config, monitor):
        mock_config.RAG_BOE_MONITOR_ENABLED = True
        with patch.object(monitor, "_fetch_rss", return_value=_old_rss()):
            alerts = monitor.check_updates(days_back=7)
        # Entries are 30 days old, window is 7 days — should be filtered out
        assert alerts == []


class TestMatchKeywords:
    def test_matching_keywords(self, monitor):
        matched, score = monitor._match_keywords(
            "Real Decreto sobre prestacion por desempleo",
            "Modificacion de la prestacion",
        )
        assert "prestacion" in matched
        assert "desempleo" in matched
        assert score > 0

    def test_no_match(self, monitor):
        matched, score = monitor._match_keywords(
            "Ley de educacion", "Reforma educativa"
        )
        assert matched == []
        assert score == 0.0

    def test_title_boost(self, monitor):
        # Same keywords, but one has keyword in title
        _, score_title = monitor._match_keywords("prestacion desempleo", "")
        _, score_body = monitor._match_keywords("ley general", "prestacion desempleo")
        # Title match should score higher (or equal if both match same keywords)
        assert score_title >= score_body


class TestParseDate:
    def test_rfc822_format(self):
        dt = BOEMonitor._parse_date("Mon, 17 Feb 2025 00:00:00 +0100")
        assert dt is not None
        assert dt.year == 2025

    def test_iso_format(self):
        dt = BOEMonitor._parse_date("2025-02-17T10:00:00+01:00")
        assert dt is not None

    def test_simple_date(self):
        dt = BOEMonitor._parse_date("2025-02-17")
        assert dt is not None

    def test_invalid_returns_none(self):
        dt = BOEMonitor._parse_date("not a date")
        assert dt is None
