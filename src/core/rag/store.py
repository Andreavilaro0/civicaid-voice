"""PGVectorStore — CRUD and hybrid search over procedure chunks."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.core.rag.database import SessionLocal
from src.core.rag.models import Chunk, ProcedureDoc
from src.core.rag.synonyms import expand_query

logger = logging.getLogger(__name__)


class PGVectorStore:
    """Vector store backed by PostgreSQL + pgvector.

    Provides insert/search/delete operations for procedure documents
    and their embedded chunks. Supports pure vector search, hybrid
    (BM25 + vector) search, and metadata-filtered queries.
    """

    def __init__(self, session_factory=None):
        self._session_factory = session_factory or SessionLocal

    def _get_session(self) -> Session:
        return self._session_factory()

    # ── Insert / Delete ─────────────────────────────────────────────

    def insert_procedure(self, doc_data: dict, chunks: list) -> dict:
        """Insert a procedure and its chunks transactionally.

        If a procedure with the same id already exists, its existing
        chunks are deleted and replaced (upsert pattern).

        Args:
            doc_data: Dict with ProcedureDoc fields.
            chunks: List of ChunkData objects from the chunker.

        Returns:
            Dict with stats: procedure_id, chunks_inserted, replaced.
        """
        session = self._get_session()
        try:
            procedure_id = doc_data["id"]
            replaced = False

            # Check for existing procedure
            existing = session.get(ProcedureDoc, procedure_id)
            if existing:
                # Delete old chunks (cascade would handle it, but be explicit)
                session.query(Chunk).filter(
                    Chunk.procedure_id == procedure_id
                ).delete()
                # Update procedure fields
                for key, value in doc_data.items():
                    if hasattr(existing, key) and key != "id":
                        setattr(existing, key, value)
                existing.updated_at = datetime.now(timezone.utc)
                replaced = True
            else:
                procedure = ProcedureDoc(**doc_data)
                session.add(procedure)

            # Insert new chunks
            for chunk in chunks:
                db_chunk = Chunk(
                    id=str(uuid.uuid4()),
                    procedure_id=procedure_id,
                    section_name=chunk.section_name,
                    heading_path=chunk.heading_path,
                    content=chunk.content,
                    token_count=chunk.token_count,
                    embedding=chunk.metadata.get("embedding"),
                    chunk_index=chunk.chunk_index,
                    metadata_=chunk.metadata,
                )
                session.add(db_chunk)

            session.commit()

            stats = {
                "procedure_id": procedure_id,
                "chunks_inserted": len(chunks),
                "replaced": replaced,
            }
            logger.info(
                "Inserted procedure %s: %d chunks (replaced=%s)",
                procedure_id, len(chunks), replaced,
            )
            return stats

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_procedure(self, id: str) -> bool:
        """Delete a procedure and all its chunks.

        Returns:
            True if the procedure existed and was deleted, False otherwise.
        """
        session = self._get_session()
        try:
            procedure = session.get(ProcedureDoc, id)
            if not procedure:
                return False
            session.delete(procedure)  # cascade deletes chunks
            session.commit()
            logger.info("Deleted procedure %s", id)
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # ── Read ────────────────────────────────────────────────────────

    def get_procedure(self, id: str) -> dict | None:
        """Get a procedure by id with its chunks.

        Returns:
            Dict with procedure fields and chunk list, or None.
        """
        session = self._get_session()
        try:
            procedure = session.get(ProcedureDoc, id)
            if not procedure:
                return None
            return {
                "id": procedure.id,
                "nombre": procedure.nombre,
                "descripcion": procedure.descripcion,
                "organismo": procedure.organismo,
                "source_type": procedure.source_type,
                "idioma": procedure.idioma,
                "content_hash": procedure.content_hash,
                "last_fetched_at": procedure.last_fetched_at.isoformat() if procedure.last_fetched_at else None,
                "fetch_count": procedure.fetch_count or 0,
                "chunk_count": len(procedure.chunks),
                "created_at": procedure.created_at.isoformat() if procedure.created_at else None,
                "updated_at": procedure.updated_at.isoformat() if procedure.updated_at else None,
            }
        finally:
            session.close()

    def count_procedures(self) -> int:
        """Return total number of procedures."""
        session = self._get_session()
        try:
            return session.query(ProcedureDoc).count()
        finally:
            session.close()

    def count_chunks(self) -> int:
        """Return total number of chunks."""
        session = self._get_session()
        try:
            return session.query(Chunk).count()
        finally:
            session.close()

    # ── Vector Search ───────────────────────────────────────────────

    def search_vector(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        threshold: float = 0.7,
    ) -> list[dict]:
        """Cosine similarity search using pgvector <=> operator.

        Args:
            query_embedding: 768-dim query vector.
            top_k: Maximum results to return.
            threshold: Minimum cosine similarity score (0-1).

        Returns:
            List of dicts with chunk content, score, and metadata.
        """
        session = self._get_session()
        try:
            sql = text("""
                SELECT
                    c.id,
                    c.procedure_id,
                    c.section_name,
                    c.heading_path,
                    c.content,
                    c.token_count,
                    c.metadata,
                    1 - (c.embedding <=> :query) AS score
                FROM chunks c
                WHERE c.embedding IS NOT NULL
                  AND 1 - (c.embedding <=> :query) > :threshold
                ORDER BY score DESC
                LIMIT :top_k
            """)

            rows = session.execute(sql, {
                "query": str(query_embedding),
                "threshold": threshold,
                "top_k": top_k,
            }).fetchall()

            return [
                {
                    "chunk_id": row.id,
                    "procedure_id": row.procedure_id,
                    "section_name": row.section_name,
                    "heading_path": row.heading_path,
                    "content": row.content,
                    "token_count": row.token_count,
                    "metadata": row.metadata,
                    "score": float(row.score),
                }
                for row in rows
            ]
        finally:
            session.close()

    # ── Hybrid Search (BM25 + Vector) ──────────────────────────────

    def search_hybrid(
        self,
        query_text: str,
        query_embedding: list[float],
        top_k: int = 5,
        weight: float = 0.5,
        territory_filter: Optional[dict] = None,
    ) -> list[dict]:
        """Hybrid search combining BM25 (tsvector) and vector cosine.

        The combined score is:
            weight * vector_score + (1 - weight) * normalized_bm25_score

        BM25 scores are normalized by dividing by the max BM25 score
        in the result set.

        Args:
            query_text: Raw query string for BM25 matching.
            query_embedding: 768-dim query vector for cosine similarity.
            top_k: Maximum results to return.
            weight: Vector vs BM25 weight (0-1). Higher = more vector.
            territory_filter: Optional territory dict from detect_territory().

        Returns:
            List of dicts with chunk content, combined score, and sub-scores.
        """
        # Expand acronyms/synonyms for better BM25 recall
        expanded_query = expand_query(query_text)

        # Build territory WHERE clause — allow NULL (national procedures always match)
        territory_clause = ""
        territory_params: dict = {}
        if territory_filter:
            if territory_filter.get("municipio"):
                territory_clause = (
                    "AND (c.metadata->>'territorio_municipio' = :t_municipio "
                    "OR c.metadata->>'territorio_municipio' IS NULL)"
                )
                territory_params["t_municipio"] = territory_filter["municipio"]
            elif territory_filter.get("ccaa"):
                territory_clause = (
                    "AND (c.metadata->>'territorio_ccaa' = :t_ccaa "
                    "OR c.metadata->>'territorio_ccaa' IS NULL)"
                )
                territory_params["t_ccaa"] = territory_filter["ccaa"]

        session = self._get_session()
        try:
            # Step 1: Get candidates with both scores
            sql = text(f"""
                WITH scored AS (
                    SELECT
                        c.id,
                        c.procedure_id,
                        c.section_name,
                        c.heading_path,
                        c.content,
                        c.token_count,
                        c.metadata,
                        1 - (c.embedding <=> :query_embedding) AS vector_score,
                        ts_rank(
                            to_tsvector('spanish', p.nombre || ' ' || c.content),
                            plainto_tsquery('spanish', :expanded_query)
                        ) AS bm25_score
                    FROM chunks c
                    JOIN procedure_docs p ON p.id = c.procedure_id
                    WHERE c.embedding IS NOT NULL
                    {territory_clause}
                ),
                max_bm25 AS (
                    SELECT GREATEST(MAX(bm25_score), 0.0001) AS max_val
                    FROM scored
                ),
                combined AS (
                    SELECT
                        s.*,
                        :weight * s.vector_score
                        + (1.0 - :weight) * (s.bm25_score / m.max_val) AS combined_score
                    FROM scored s, max_bm25 m
                )
                SELECT *
                FROM combined
                ORDER BY combined_score DESC
                LIMIT :top_k
            """)

            params = {
                "query_embedding": str(query_embedding),
                "expanded_query": expanded_query,
                "weight": weight,
                "top_k": top_k,
                **territory_params,
            }
            rows = session.execute(sql, params).fetchall()

            return [
                {
                    "chunk_id": row.id,
                    "procedure_id": row.procedure_id,
                    "section_name": row.section_name,
                    "heading_path": row.heading_path,
                    "content": row.content,
                    "token_count": row.token_count,
                    "metadata": row.metadata,
                    "score": float(row.combined_score),
                    "vector_score": float(row.vector_score),
                    "bm25_score": float(row.bm25_score),
                }
                for row in rows
            ]
        finally:
            session.close()

    # ── Metadata Search ─────────────────────────────────────────────

    def search_metadata(self, filters: dict, limit: int = 50) -> list[dict]:
        """Pre-filter chunks by metadata fields.

        Supported filter keys: territorio, source_type, canal, idioma.
        Each maps to a JSONB field in chunk metadata or a procedure column.

        Args:
            filters: Dict of field -> value to filter on.
            limit: Maximum number of results to return.

        Returns:
            List of matching chunk dicts.
        """
        session = self._get_session()
        try:
            conditions = []
            params = {}

            supported_filters = {
                "source_type": "c.metadata->>'source_type' = :source_type",
                "idioma": "c.metadata->>'idioma' = :idioma",
                "territorio_nivel": "c.metadata->>'territorio_nivel' = :territorio_nivel",
                "territorio_ccaa": "c.metadata->>'territorio_ccaa' = :territorio_ccaa",
                "territorio_municipio": "c.metadata->>'territorio_municipio' = :territorio_municipio",
                "canal": "p.canal = :canal",
                "procedure_id": "c.procedure_id = :procedure_id",
            }

            for key, value in filters.items():
                if key in supported_filters:
                    conditions.append(supported_filters[key])
                    params[key] = value

            where_clause = " AND ".join(conditions) if conditions else "TRUE"

            sql = text(f"""
                SELECT
                    c.id,
                    c.procedure_id,
                    c.section_name,
                    c.heading_path,
                    c.content,
                    c.token_count,
                    c.metadata
                FROM chunks c
                JOIN procedure_docs p ON p.id = c.procedure_id
                WHERE {where_clause}
                ORDER BY c.procedure_id, c.chunk_index
                LIMIT :limit
            """)

            params["limit"] = limit
            rows = session.execute(sql, params).fetchall()

            return [
                {
                    "chunk_id": row.id,
                    "procedure_id": row.procedure_id,
                    "section_name": row.section_name,
                    "heading_path": row.heading_path,
                    "content": row.content,
                    "token_count": row.token_count,
                    "metadata": row.metadata,
                }
                for row in rows
            ]
        finally:
            session.close()

    # ── Staleness ──────────────────────────────────────────────────

    def get_stale_procedures(self, threshold_days: int = 90) -> list[dict]:
        """Return procedures with updated_at older than threshold_days."""
        session = self._get_session()
        try:
            sql = text("""
                SELECT
                    id,
                    nombre,
                    updated_at,
                    EXTRACT(DAY FROM (NOW() - updated_at))::int AS staleness_days
                FROM procedure_docs
                WHERE updated_at < NOW() - MAKE_INTERVAL(days => :threshold_days)
                ORDER BY updated_at ASC
            """)
            rows = session.execute(sql, {"threshold_days": threshold_days}).fetchall()
            return [
                {
                    "id": row.id,
                    "nombre": row.nombre,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                    "staleness_days": row.staleness_days or 0,
                }
                for row in rows
            ]
        finally:
            session.close()
