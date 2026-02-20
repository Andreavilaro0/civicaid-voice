"""Thread-safe RAG metrics collector for Clara pipeline observability."""

import threading
from dataclasses import dataclass, field


@dataclass
class RAGMetrics:
    """Thread-safe RAG metrics collector.

    All counter updates are protected by a threading.Lock to ensure
    correctness under concurrent access from Flask request threads.
    """

    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    # Retrieval metrics
    retrieval_total: int = 0
    retrieval_cache_hits: int = 0
    retrieval_cache_misses: int = 0
    retrieval_fallback_json: int = 0
    retrieval_fallback_directory: int = 0
    retrieval_errors: int = 0
    retrieval_latency_sum_ms: float = 0.0
    retrieval_latency_count: int = 0

    # Ingestion metrics
    ingestion_total: int = 0
    ingestion_no_change: int = 0
    ingestion_updated: int = 0
    ingestion_errors: int = 0

    # Drift metrics
    drift_checks_total: int = 0
    drift_stale_found: int = 0
    drift_drifted_found: int = 0

    # Satisfaction
    satisfaction_total: int = 0
    satisfaction_positive: int = 0
    satisfaction_negative: int = 0

    def record_retrieval(self, source: str, latency_ms: float, cache_hit: bool = False):
        """Record a retrieval event.

        Args:
            source: Retrieval source — "pgvector", "json_fallback", "directory_fallback", "error".
            latency_ms: Time taken for the retrieval in milliseconds.
            cache_hit: Whether the result came from cache.
        """
        with self._lock:
            self.retrieval_total += 1
            self.retrieval_latency_sum_ms += latency_ms
            self.retrieval_latency_count += 1

            if cache_hit:
                self.retrieval_cache_hits += 1
            else:
                self.retrieval_cache_misses += 1

            if source == "json_fallback":
                self.retrieval_fallback_json += 1
            elif source == "directory_fallback":
                self.retrieval_fallback_directory += 1
            elif source == "error":
                self.retrieval_errors += 1

    def record_ingestion(self, status: str):
        """Record an ingestion event.

        Args:
            status: One of "no_change", "updated", "error".
        """
        with self._lock:
            self.ingestion_total += 1
            if status == "no_change":
                self.ingestion_no_change += 1
            elif status == "updated":
                self.ingestion_updated += 1
            elif status == "error":
                self.ingestion_errors += 1

    def record_drift_check(self, status: str):
        """Record a drift check.

        Args:
            status: One of "stale", "drifted", "ok".
        """
        with self._lock:
            self.drift_checks_total += 1
            if status == "stale":
                self.drift_stale_found += 1
            elif status == "drifted":
                self.drift_drifted_found += 1

    def record_satisfaction(self, positive: bool):
        """Record user satisfaction feedback.

        Args:
            positive: True for positive feedback, False for negative.
        """
        with self._lock:
            self.satisfaction_total += 1
            if positive:
                self.satisfaction_positive += 1
            else:
                self.satisfaction_negative += 1

    @property
    def retrieval_latency_avg_ms(self) -> float:
        """Average retrieval latency in ms, or 0.0 if no data."""
        with self._lock:
            if self.retrieval_latency_count == 0:
                return 0.0
            return self.retrieval_latency_sum_ms / self.retrieval_latency_count

    def to_dict(self) -> dict:
        """Export all metrics as a dict (snapshot under lock)."""
        with self._lock:
            avg_latency = (
                self.retrieval_latency_sum_ms / self.retrieval_latency_count
                if self.retrieval_latency_count > 0
                else 0.0
            )
            return {
                "retrieval": {
                    "total": self.retrieval_total,
                    "cache_hits": self.retrieval_cache_hits,
                    "cache_misses": self.retrieval_cache_misses,
                    "fallback_json": self.retrieval_fallback_json,
                    "fallback_directory": self.retrieval_fallback_directory,
                    "errors": self.retrieval_errors,
                    "latency_avg_ms": round(avg_latency, 1),
                    "latency_count": self.retrieval_latency_count,
                },
                "ingestion": {
                    "total": self.ingestion_total,
                    "no_change": self.ingestion_no_change,
                    "updated": self.ingestion_updated,
                    "errors": self.ingestion_errors,
                },
                "drift": {
                    "total": self.drift_checks_total,
                    "stale_found": self.drift_stale_found,
                    "drifted_found": self.drift_drifted_found,
                },
                "satisfaction": {
                    "total": self.satisfaction_total,
                    "positive": self.satisfaction_positive,
                    "negative": self.satisfaction_negative,
                    "rate": round(
                        self.satisfaction_positive / self.satisfaction_total, 2
                    )
                    if self.satisfaction_total > 0
                    else 0.0,
                },
            }

    def reset(self):
        """Reset all counters to zero (for testing)."""
        with self._lock:
            self.retrieval_total = 0
            self.retrieval_cache_hits = 0
            self.retrieval_cache_misses = 0
            self.retrieval_fallback_json = 0
            self.retrieval_fallback_directory = 0
            self.retrieval_errors = 0
            self.retrieval_latency_sum_ms = 0.0
            self.retrieval_latency_count = 0
            self.ingestion_total = 0
            self.ingestion_no_change = 0
            self.ingestion_updated = 0
            self.ingestion_errors = 0
            self.drift_checks_total = 0
            self.drift_stale_found = 0
            self.drift_drifted_found = 0
            self.satisfaction_total = 0
            self.satisfaction_positive = 0
            self.satisfaction_negative = 0


# Singleton — import this everywhere
rag_metrics = RAGMetrics()
