"""Automated ingestion pipeline for tramite JSON files."""

import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import yaml

from src.core.config import config
from src.core.rag.chunker import chunk_procedure
from src.core.rag.embedder import embed_batch
from src.core.rag.migrator import _content_hash, _map_to_procedure_doc

logger = logging.getLogger(__name__)

_TRAMITES_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, "data", "tramites"
)
_REGISTRY_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, os.pardir,
    "data", "sources", "registry.yaml",
)


@dataclass
class FetchResult:
    """Result of ingesting a single source."""

    source_id: str
    status: str  # "fetched", "no_change", "updated", "error"
    content_hash: str = ""
    error: str = ""
    chunks_created: int = 0
    duration_ms: int = 0


class IngestionPipeline:
    """Ingest tramite JSON files into the PGVector store.

    Computes content hashes to detect changes, re-chunks and re-embeds
    only when content has actually changed, and logs each operation.
    """

    def __init__(self, store):
        self.store = store

    def ingest_source(self, source_path: str, dry_run: bool = False) -> FetchResult:
        """Ingest a single tramite JSON file.

        1. Load JSON from source_path
        2. Compute content_hash (SHA256 of normalized JSON)
        3. Check if content_hash matches existing procedure
        4. If no_change -> return early
        5. If new/changed -> chunk -> embed -> upsert
        """
        if not config.RAG_INGESTION_ENABLED and not dry_run:
            return FetchResult(
                source_id=source_path,
                status="error",
                error="RAG_INGESTION_ENABLED is false",
            )

        start_ms = time.monotonic()
        source_id = os.path.splitext(os.path.basename(source_path))[0]

        try:
            with open(source_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return FetchResult(
                source_id=source_id,
                status="error",
                error=f"File not found: {source_path}",
            )
        except json.JSONDecodeError as exc:
            return FetchResult(
                source_id=source_id,
                status="error",
                error=f"Invalid JSON: {exc}",
            )

        content_hash = _content_hash(data)
        doc_data = _map_to_procedure_doc(data)
        procedure_id = doc_data["id"]

        # Check for existing procedure with same hash
        existing = self.store.get_procedure(procedure_id)
        if existing and existing.get("content_hash") == content_hash:
            elapsed = int((time.monotonic() - start_ms) * 1000)
            logger.info("No change for %s (hash match)", source_id)
            return FetchResult(
                source_id=source_id,
                status="no_change",
                content_hash=content_hash,
                duration_ms=elapsed,
            )

        if dry_run:
            chunks = chunk_procedure(doc_data)
            elapsed = int((time.monotonic() - start_ms) * 1000)
            status = "updated" if existing else "fetched"
            logger.info(
                "[DRY RUN] Would %s %s: %d chunks",
                status, source_id, len(chunks),
            )
            return FetchResult(
                source_id=source_id,
                status=status,
                content_hash=content_hash,
                chunks_created=len(chunks),
                duration_ms=elapsed,
            )

        # Chunk
        chunks = chunk_procedure(doc_data)

        # Embed
        texts = [c.content for c in chunks]
        embeddings = embed_batch(texts)
        for chunk, embedding in zip(chunks, embeddings):
            chunk.metadata["embedding"] = embedding

        # Upsert (store.insert_procedure handles delete-old + insert-new)
        doc_data["last_fetched_at"] = datetime.now(timezone.utc)
        self.store.insert_procedure(doc_data, chunks)

        # Update fetch timestamp
        try:
            self.store.update_fetch_timestamp(procedure_id)
        except AttributeError:
            pass  # method may not exist yet

        # Log ingestion
        self._log_ingestion(
            procedure_id=procedure_id,
            action="update" if existing else "insert",
            chunks_created=len(chunks),
            start_ms=start_ms,
        )

        elapsed = int((time.monotonic() - start_ms) * 1000)
        status = "updated" if existing else "fetched"
        logger.info(
            "Ingested %s: status=%s, chunks=%d, %dms",
            source_id, status, len(chunks), elapsed,
        )
        return FetchResult(
            source_id=source_id,
            status=status,
            content_hash=content_hash,
            chunks_created=len(chunks),
            duration_ms=elapsed,
        )

    def ingest_from_registry(
        self,
        tier: str = "p0",
        max_sources: int = 50,
        dry_run: bool = False,
    ) -> list[FetchResult]:
        """Ingest sources listed in registry.yaml by tier/priority.

        Falls back to data/tramites/*.json if registry is unavailable.
        """
        registry_path = os.path.normpath(_REGISTRY_PATH)
        if os.path.exists(registry_path):
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    registry = yaml.safe_load(f)
                sources = registry.get("sources", [])
                filtered = [
                    s for s in sources
                    if s.get("priority", "").lower() == tier.lower()
                ][:max_sources]
                if filtered:
                    logger.info(
                        "Registry: %d sources for tier %s",
                        len(filtered), tier,
                    )
                    # Map registry entries to local JSON paths
                    results = []
                    tramites_dir = os.path.normpath(_TRAMITES_DIR)
                    for source in filtered:
                        # Try to find matching JSON in tramites dir
                        for json_file in os.listdir(tramites_dir):
                            if json_file.endswith(".json"):
                                path = os.path.join(tramites_dir, json_file)
                                results.append(
                                    self.ingest_source(path, dry_run=dry_run)
                                )
                                if len(results) >= max_sources:
                                    break
                        if len(results) >= max_sources:
                            break
                    return results
            except Exception as exc:
                logger.warning(
                    "Failed to read registry, falling back: %s", exc,
                )

        # Fallback: ingest all tramite JSONs
        return self.ingest_all(dry_run=dry_run)

    def ingest_all(self, dry_run: bool = False) -> list[FetchResult]:
        """Ingest all JSON files from data/tramites/."""
        tramites_dir = os.path.normpath(_TRAMITES_DIR)
        results: list[FetchResult] = []

        if not os.path.isdir(tramites_dir):
            logger.warning("Tramites directory not found: %s", tramites_dir)
            return results

        json_files = sorted(
            f for f in os.listdir(tramites_dir) if f.endswith(".json")
        )
        logger.info("Ingesting %d tramite files", len(json_files))

        for filename in json_files:
            path = os.path.join(tramites_dir, filename)
            result = self.ingest_source(path, dry_run=dry_run)
            results.append(result)

        fetched = sum(1 for r in results if r.status == "fetched")
        updated = sum(1 for r in results if r.status == "updated")
        unchanged = sum(1 for r in results if r.status == "no_change")
        errors = sum(1 for r in results if r.status == "error")
        logger.info(
            "Ingestion complete: %d fetched, %d updated, %d unchanged, %d errors",
            fetched, updated, unchanged, errors,
        )
        return results

    def _log_ingestion(
        self,
        procedure_id: str,
        action: str,
        chunks_created: int,
        start_ms: float,
    ) -> None:
        """Log ingestion event to ingestion_log table."""
        elapsed = int((time.monotonic() - start_ms) * 1000)
        try:
            from src.core.rag.models import IngestionLog
            session = self.store._get_session()
            try:
                log_entry = IngestionLog(
                    procedure_id=procedure_id,
                    action=action,
                    chunks_created=chunks_created,
                    chunks_updated=0,
                    duration_ms=elapsed,
                )
                session.add(log_entry)
                session.commit()
            except Exception:
                session.rollback()
                logger.warning(
                    "Failed to write ingestion log for %s", procedure_id,
                )
            finally:
                session.close()
        except Exception:
            logger.warning("Could not log ingestion for %s", procedure_id)
