"""Unit tests for src/utils/rag_metrics.py — RAGMetrics collector."""

import pytest
from src.utils.rag_metrics import RAGMetrics


@pytest.fixture
def metrics():
    m = RAGMetrics()
    return m


class TestRAGMetricsInitialValues:
    def test_initial_retrieval_total_is_zero(self, metrics):
        assert metrics.retrieval_total == 0

    def test_initial_ingestion_total_is_zero(self, metrics):
        assert metrics.ingestion_total == 0

    def test_initial_drift_total_is_zero(self, metrics):
        assert metrics.drift_checks_total == 0

    def test_initial_satisfaction_total_is_zero(self, metrics):
        assert metrics.satisfaction_total == 0

    def test_initial_latency_avg_is_zero(self, metrics):
        assert metrics.retrieval_latency_avg_ms == 0.0


class TestRecordRetrieval:
    def test_increments_total(self, metrics):
        metrics.record_retrieval(source="pgvector", latency_ms=50.0)
        assert metrics.retrieval_total == 1

    def test_cache_hit_increments_counter(self, metrics):
        metrics.record_retrieval(source="pgvector", latency_ms=10.0, cache_hit=True)
        assert metrics.retrieval_cache_hits == 1
        assert metrics.retrieval_cache_misses == 0

    def test_cache_miss_increments_counter(self, metrics):
        metrics.record_retrieval(source="pgvector", latency_ms=50.0, cache_hit=False)
        assert metrics.retrieval_cache_misses == 1

    def test_json_fallback_tracked(self, metrics):
        metrics.record_retrieval(source="json_fallback", latency_ms=30.0)
        assert metrics.retrieval_fallback_json == 1

    def test_directory_fallback_tracked(self, metrics):
        metrics.record_retrieval(source="directory_fallback", latency_ms=20.0)
        assert metrics.retrieval_fallback_directory == 1

    def test_error_tracked(self, metrics):
        metrics.record_retrieval(source="error", latency_ms=0.0)
        assert metrics.retrieval_errors == 1


class TestRecordIngestion:
    def test_no_change_increments(self, metrics):
        metrics.record_ingestion("no_change")
        assert metrics.ingestion_total == 1
        assert metrics.ingestion_no_change == 1

    def test_updated_increments(self, metrics):
        metrics.record_ingestion("updated")
        assert metrics.ingestion_updated == 1

    def test_error_increments(self, metrics):
        metrics.record_ingestion("error")
        assert metrics.ingestion_errors == 1


class TestRecordDriftCheck:
    def test_stale_increments(self, metrics):
        metrics.record_drift_check("stale")
        assert metrics.drift_checks_total == 1
        assert metrics.drift_stale_found == 1

    def test_drifted_increments(self, metrics):
        metrics.record_drift_check("drifted")
        assert metrics.drift_drifted_found == 1

    def test_ok_increments_total_only(self, metrics):
        metrics.record_drift_check("ok")
        assert metrics.drift_checks_total == 1
        assert metrics.drift_stale_found == 0
        assert metrics.drift_drifted_found == 0


class TestRecordSatisfaction:
    def test_positive_increments(self, metrics):
        metrics.record_satisfaction(positive=True)
        assert metrics.satisfaction_total == 1
        assert metrics.satisfaction_positive == 1
        assert metrics.satisfaction_negative == 0

    def test_negative_increments(self, metrics):
        metrics.record_satisfaction(positive=False)
        assert metrics.satisfaction_negative == 1

    def test_rate_calculation(self, metrics):
        metrics.record_satisfaction(positive=True)
        metrics.record_satisfaction(positive=True)
        metrics.record_satisfaction(positive=False)
        d = metrics.to_dict()
        assert d["satisfaction"]["rate"] == 0.67


class TestToDict:
    def test_returns_all_sections(self, metrics):
        d = metrics.to_dict()
        assert "retrieval" in d
        assert "ingestion" in d
        assert "drift" in d
        assert "satisfaction" in d

    def test_latency_avg_calculated(self, metrics):
        metrics.record_retrieval(source="pgvector", latency_ms=100.0)
        metrics.record_retrieval(source="pgvector", latency_ms=200.0)
        d = metrics.to_dict()
        assert d["retrieval"]["latency_avg_ms"] == 150.0


class TestReset:
    def test_clears_all_counters(self, metrics):
        metrics.record_retrieval(source="pgvector", latency_ms=50.0)
        metrics.record_ingestion("updated")
        metrics.record_drift_check("stale")
        metrics.record_satisfaction(positive=True)
        metrics.reset()
        assert metrics.retrieval_total == 0
        assert metrics.ingestion_total == 0
        assert metrics.drift_checks_total == 0
        assert metrics.satisfaction_total == 0
        assert metrics.retrieval_latency_avg_ms == 0.0


class TestLatencyAvg:
    def test_avg_with_data(self, metrics):
        metrics.record_retrieval(source="pgvector", latency_ms=10.0)
        metrics.record_retrieval(source="pgvector", latency_ms=30.0)
        assert metrics.retrieval_latency_avg_ms == 20.0

    def test_avg_no_data(self, metrics):
        assert metrics.retrieval_latency_avg_ms == 0.0
