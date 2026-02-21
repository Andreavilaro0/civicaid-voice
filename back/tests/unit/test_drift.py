"""Unit tests for src/core/rag/drift.py — DriftDetector."""

import json
import os
import tempfile
from datetime import datetime, timedelta, timezone

import pytest
from unittest.mock import MagicMock, patch

from src.core.rag.drift import DriftDetector, DriftResult


@pytest.fixture
def mock_store():
    store = MagicMock()
    store.get_procedure.return_value = None
    store.list_procedure_ids.return_value = []
    return store


@pytest.fixture
def detector(mock_store):
    return DriftDetector(mock_store)


class TestDriftResultDataclass:
    def test_default_fields(self):
        r = DriftResult(procedure_id="test", status="current")
        assert r.procedure_id == "test"
        assert r.staleness_days == 0
        assert r.staleness_score == 0.0
        assert r.content_hash_match is True
        assert r.detail == ""


class TestDriftDetectorInit:
    def test_creates_with_store(self, mock_store):
        d = DriftDetector(mock_store)
        assert d.store is mock_store


class TestCheckProcedure:
    @patch("src.core.rag.drift.config")
    def test_missing_procedure(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        mock_store.get_procedure.return_value = None
        result = detector.check_procedure("nonexistent")
        assert result.status == "missing"

    @patch("src.core.rag.drift.config")
    def test_current_procedure(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        now = datetime.now(timezone.utc)
        mock_store.get_procedure.return_value = {
            "content_hash": "abc",
            "last_fetched_at": now.isoformat(),
        }
        with patch.object(detector, "_find_source_json", return_value=None):
            result = detector.check_procedure("proc-1")
        assert result.status == "current"
        assert result.staleness_score < 0.5

    @patch("src.core.rag.drift.config")
    def test_stale_procedure(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 30
        old_date = datetime.now(timezone.utc) - timedelta(days=60)
        mock_store.get_procedure.return_value = {
            "content_hash": "abc",
            "last_fetched_at": old_date.isoformat(),
        }
        with patch.object(detector, "_find_source_json", return_value=None):
            result = detector.check_procedure("proc-1")
        assert result.status == "stale"
        assert result.staleness_score >= 1.0

    @patch("src.core.rag.drift.config")
    def test_drifted_procedure_hash_mismatch(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        now = datetime.now(timezone.utc)
        mock_store.get_procedure.return_value = {
            "content_hash": "old_hash",
            "last_fetched_at": now.isoformat(),
        }
        # Create a temp JSON file so hash comparison happens
        data = {"nombre": "Test", "organismo": "Test", "descripcion": "d"}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            path = f.name
        try:
            with patch.object(detector, "_find_source_json", return_value=path):
                result = detector.check_procedure("proc-1")
            assert result.status == "drifted"
            assert result.content_hash_match is False
        finally:
            os.unlink(path)

    @patch("src.core.rag.drift.config")
    def test_no_fetch_timestamp_is_stale(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        mock_store.get_procedure.return_value = {
            "content_hash": "abc",
        }
        with patch.object(detector, "_find_source_json", return_value=None):
            result = detector.check_procedure("proc-1")
        assert result.staleness_score == 1.0


class TestStalenessScore:
    @patch("src.core.rag.drift.config")
    def test_staleness_score_half(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 100
        half_date = datetime.now(timezone.utc) - timedelta(days=50)
        mock_store.get_procedure.return_value = {
            "content_hash": "abc",
            "last_fetched_at": half_date.isoformat(),
        }
        with patch.object(detector, "_find_source_json", return_value=None):
            result = detector.check_procedure("proc-1")
        assert 0.4 <= result.staleness_score <= 0.6

    @patch("src.core.rag.drift.config")
    def test_staleness_capped_at_one(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 10
        old = datetime.now(timezone.utc) - timedelta(days=100)
        mock_store.get_procedure.return_value = {
            "content_hash": "abc",
            "last_fetched_at": old.isoformat(),
        }
        with patch.object(detector, "_find_source_json", return_value=None):
            result = detector.check_procedure("proc-1")
        assert result.staleness_score == 1.0


class TestCheckAll:
    @patch("src.core.rag.drift.config")
    def test_returns_results_for_all_procedures(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        mock_store.list_procedure_ids.return_value = ["p1", "p2"]
        mock_store.get_procedure.return_value = None
        results = detector.check_all()
        assert len(results) == 2
        assert all(r.status == "missing" for r in results)

    @patch("src.core.rag.drift.config")
    def test_empty_when_no_procedures(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        mock_store.list_procedure_ids.return_value = []
        with patch.object(detector, "_get_all_procedure_ids", return_value=[]):
            results = detector.check_all()
        assert results == []


class TestGetStaleProcedures:
    @patch("src.core.rag.drift.config")
    def test_filters_stale_and_drifted(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        mock_store.list_procedure_ids.return_value = ["p1", "p2", "p3"]
        now = datetime.now(timezone.utc)

        def side_effect(pid):
            if pid == "p1":
                return {"content_hash": "h", "last_fetched_at": now.isoformat()}
            return None

        mock_store.get_procedure.side_effect = side_effect
        with patch.object(detector, "_find_source_json", return_value=None):
            results = detector.get_stale_procedures()
        # p2 and p3 are missing (which counts as stale/drifted/missing)
        stale_ids = [r.procedure_id for r in results]
        assert "p2" in stale_ids
        assert "p3" in stale_ids


class TestFindSourceJson:
    def test_finds_matching_file(self, detector):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "imv.json")
            with open(path, "w") as f:
                f.write("{}")
            with patch("src.core.rag.drift._TRAMITES_DIR", tmpdir):
                result = detector._find_source_json("age-segsocial-imv")
            assert result is not None
            assert result.endswith("imv.json")

    def test_returns_none_for_no_match(self, detector):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.core.rag.drift._TRAMITES_DIR", tmpdir):
                result = detector._find_source_json("nonexistent-proc")
            assert result is None
