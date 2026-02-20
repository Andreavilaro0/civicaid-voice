"""Integration tests for drift detection pipeline — mock store, skip if no Docker."""

import json
import os
import tempfile
from datetime import datetime, timedelta, timezone

import pytest
from unittest.mock import MagicMock, patch

from src.core.rag.drift import DriftDetector, DriftResult

pytestmark = pytest.mark.skipif(
    not os.getenv("RAG_DB_URL"),
    reason="RAG_DB_URL not set — Docker/PG not available",
)


@pytest.fixture
def mock_store():
    store = MagicMock()
    store.get_procedure.return_value = None
    store.list_procedure_ids.return_value = ["proc-1", "proc-2"]
    return store


@pytest.fixture
def detector(mock_store):
    return DriftDetector(mock_store)


@pytest.fixture
def tramite_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        data = {"nombre": "Test", "organismo": "Org", "descripcion": "d"}
        with open(os.path.join(tmpdir, "test.json"), "w") as f:
            json.dump(data, f)
        yield tmpdir


class TestDriftPipelineIntegration:
    @patch("src.core.rag.drift.config")
    def test_check_all_returns_results(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        results = detector.check_all()
        assert len(results) == 2
        assert all(isinstance(r, DriftResult) for r in results)

    @patch("src.core.rag.drift.config")
    def test_stale_detection_with_old_timestamp(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 30
        old = datetime.now(timezone.utc) - timedelta(days=100)
        mock_store.get_procedure.return_value = {
            "content_hash": "h",
            "last_fetched_at": old.isoformat(),
        }
        with patch.object(detector, "_find_source_json", return_value=None):
            results = detector.check_all()
        stale = [r for r in results if r.status == "stale"]
        assert len(stale) == 2

    @patch("src.core.rag.drift.config")
    def test_get_stale_filters_current(self, mock_config, detector, mock_store):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        now = datetime.now(timezone.utc)

        def side_effect(pid):
            if pid == "proc-1":
                return {"content_hash": "h", "last_fetched_at": now.isoformat()}
            return None

        mock_store.get_procedure.side_effect = side_effect
        with patch.object(detector, "_find_source_json", return_value=None):
            stale = detector.get_stale_procedures()
        ids = [r.procedure_id for r in stale]
        assert "proc-1" not in ids
        assert "proc-2" in ids

    @patch("src.core.rag.drift.config")
    def test_drift_detected_with_hash_mismatch(
        self, mock_config, detector, mock_store, tramite_dir,
    ):
        mock_config.RAG_STALENESS_THRESHOLD_DAYS = 90
        now = datetime.now(timezone.utc)
        mock_store.list_procedure_ids.return_value = ["test"]
        mock_store.get_procedure.return_value = {
            "content_hash": "wrong_hash",
            "last_fetched_at": now.isoformat(),
        }
        with patch("src.core.rag.drift._TRAMITES_DIR", tramite_dir):
            results = detector.check_all()
        drifted = [r for r in results if r.status == "drifted"]
        assert len(drifted) >= 1
