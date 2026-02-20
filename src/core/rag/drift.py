"""Drift detection — identify stale or changed procedures."""

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone

from src.core.config import config
from src.core.rag.migrator import _content_hash

logger = logging.getLogger(__name__)

_TRAMITES_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, "data", "tramites"
)


@dataclass
class DriftResult:
    """Result of a drift check for a single procedure."""

    procedure_id: str
    status: str  # "current", "stale", "drifted", "missing"
    staleness_days: int = 0
    staleness_score: float = 0.0  # 0.0=fresh, 1.0=very stale
    content_hash_match: bool = True
    detail: str = ""


class DriftDetector:
    """Detect content drift and staleness in procedure documents.

    Compares stored content hashes against source JSON files and
    computes staleness scores based on last_fetched_at timestamps.
    """

    def __init__(self, store):
        self.store = store

    def check_procedure(
        self,
        procedure_id: str,
        threshold_days: int = None,
    ) -> DriftResult:
        """Check drift for a single procedure.

        1. Get procedure from DB
        2. Load corresponding JSON from data/tramites/
        3. Compare content_hash
        4. Compute staleness score based on last_fetched_at
        """
        if threshold_days is None:
            threshold_days = config.RAG_STALENESS_THRESHOLD_DAYS

        # Get procedure from store
        proc = self.store.get_procedure(procedure_id)
        if not proc:
            return DriftResult(
                procedure_id=procedure_id,
                status="missing",
                detail="Procedure not found in database",
            )

        # Compute staleness
        staleness_days = 0
        staleness_score = 0.0
        last_fetched = proc.get("last_fetched_at")

        if last_fetched:
            if isinstance(last_fetched, str):
                try:
                    last_fetched = datetime.fromisoformat(last_fetched)
                except ValueError:
                    last_fetched = None

        if last_fetched:
            if last_fetched.tzinfo is None:
                last_fetched = last_fetched.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            delta = now - last_fetched
            staleness_days = delta.days
            staleness_score = min(1.0, staleness_days / threshold_days)
        else:
            # No fetch timestamp -> treat as very stale
            staleness_days = threshold_days
            staleness_score = 1.0

        # Try to compare content hash against source JSON
        content_hash_match = True
        source_json_path = self._find_source_json(procedure_id)

        if source_json_path:
            try:
                with open(source_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                source_hash = _content_hash(data)
                stored_hash = proc.get("content_hash", "")
                content_hash_match = source_hash == stored_hash
            except Exception as exc:
                logger.warning(
                    "Could not compare hash for %s: %s", procedure_id, exc,
                )

        # Determine status
        if not content_hash_match:
            status = "drifted"
            detail = "Content hash mismatch — source JSON has changed"
        elif staleness_score >= 1.0:
            status = "stale"
            detail = f"Last fetched {staleness_days} days ago (threshold: {threshold_days})"
        elif staleness_score > 0.5:
            status = "stale"
            detail = f"Approaching staleness: {staleness_days}/{threshold_days} days"
        else:
            status = "current"
            detail = f"Fresh: {staleness_days} days since last fetch"

        return DriftResult(
            procedure_id=procedure_id,
            status=status,
            staleness_days=staleness_days,
            staleness_score=round(staleness_score, 3),
            content_hash_match=content_hash_match,
            detail=detail,
        )

    def check_all(self, threshold_days: int = None) -> list[DriftResult]:
        """Check drift for all procedures in the store."""
        if threshold_days is None:
            threshold_days = config.RAG_STALENESS_THRESHOLD_DAYS

        results: list[DriftResult] = []

        # Get all procedure IDs
        procedure_ids = self._get_all_procedure_ids()
        if not procedure_ids:
            logger.info("No procedures found to check")
            return results

        for pid in procedure_ids:
            result = self.check_procedure(pid, threshold_days=threshold_days)
            results.append(result)

        current = sum(1 for r in results if r.status == "current")
        stale = sum(1 for r in results if r.status == "stale")
        drifted = sum(1 for r in results if r.status == "drifted")
        missing = sum(1 for r in results if r.status == "missing")
        logger.info(
            "Drift check: %d current, %d stale, %d drifted, %d missing",
            current, stale, drifted, missing,
        )
        return results

    def get_stale_procedures(
        self,
        threshold_days: int = None,
    ) -> list[DriftResult]:
        """Get only procedures that are stale or drifted."""
        if threshold_days is None:
            threshold_days = config.RAG_STALENESS_THRESHOLD_DAYS

        all_results = self.check_all(threshold_days=threshold_days)
        return [
            r for r in all_results
            if r.status in ("stale", "drifted", "missing")
        ]

    def _find_source_json(self, procedure_id: str) -> str | None:
        """Find a source JSON file that may correspond to a procedure ID."""
        tramites_dir = os.path.normpath(_TRAMITES_DIR)
        if not os.path.isdir(tramites_dir):
            return None

        # Try direct match first (procedure_id might contain the filename slug)
        for filename in os.listdir(tramites_dir):
            if not filename.endswith(".json"):
                continue
            name = os.path.splitext(filename)[0]
            # Check if the tramite name appears in the procedure_id
            if name in procedure_id or procedure_id in name:
                return os.path.join(tramites_dir, filename)

        return None

    def _get_all_procedure_ids(self) -> list[str]:
        """Get all procedure IDs from the store."""
        try:
            # Try the store's list method if available
            if hasattr(self.store, "list_procedure_ids"):
                return self.store.list_procedure_ids()

            # Fallback: scan tramites dir and derive IDs
            tramites_dir = os.path.normpath(_TRAMITES_DIR)
            if not os.path.isdir(tramites_dir):
                return []

            from src.core.rag.migrator import _map_to_procedure_doc
            ids = []
            for filename in sorted(os.listdir(tramites_dir)):
                if not filename.endswith(".json"):
                    continue
                path = os.path.join(tramites_dir, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    doc = _map_to_procedure_doc(data)
                    ids.append(doc["id"])
                except Exception:
                    continue
            return ids
        except Exception as exc:
            logger.warning("Failed to list procedure IDs: %s", exc)
            return []
