"""Retriever interface for Clara — abstracts KB lookup behind a common interface.
Current: JSONKBRetriever (keyword matching), PGVectorRetriever (hybrid search),
FallbackRetriever (chain with cache). Controlled by RAG_ENABLED / RAG_FALLBACK_CHAIN."""

import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

from src.core.models import KBContext

logger = logging.getLogger(__name__)


def _validate_source_url(ctx: KBContext) -> bool:
    """Check fuente_url against domain policy. Returns True if OK or validation off."""
    from src.core.config import config
    if not config.DOMAIN_VALIDATION_ON:
        return True
    url = ctx.fuente_url or ctx.datos.get("fuente_url", "")
    if not url:
        return True  # No URL to validate
    from src.core.domain_validator import is_domain_approved
    if not is_domain_approved(url):
        logger.warning(
            "Retriever rejected result for '%s': fuente_url domain not approved: %s",
            ctx.tramite, url,
        )
        return False
    return True


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        pass


class JSONKBRetriever(Retriever):
    """Wraps the existing kb_lookup as a Retriever implementation."""
    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        from src.core.skills.kb_lookup import kb_lookup
        result = kb_lookup(query, language)
        if result and not _validate_source_url(result):
            return None
        return result


class PGVectorRetriever(Retriever):
    """Hybrid BM25 + vector search with reranking and grounded context."""

    def __init__(self):
        from src.core.rag.store import PGVectorStore
        self.store = PGVectorStore()

    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        from src.core.config import config
        from src.core.rag.embedder import embed_text
        from src.core.rag.territory import detect_territory
        from src.core.rag.reranker import rerank

        try:
            # Step 1: Detect territory
            territory = detect_territory(query)
            if territory:
                logger.info("Territory detected: %s", territory)

            # Step 2: Embed query
            query_embedding = embed_text(query)

            # Step 3: Hybrid search (with synonym expansion + territory filter)
            results = self.store.search_hybrid(
                query_text=query,
                query_embedding=query_embedding,
                top_k=config.RAG_TOP_K,
                weight=config.RAG_HYBRID_WEIGHT,
                territory_filter=territory,
            )
        except Exception as exc:
            logger.error("PGVectorRetriever search failed: %s", exc)
            return None

        if not results:
            return None

        # Step 4: Rerank
        results = rerank(query, results, strategy=config.RAG_RERANK_STRATEGY)

        # Use rerank_score if available, else original score
        top_score = results[0].get("rerank_score", results[0].get("score", 0))
        if top_score < config.RAG_SIMILARITY_THRESHOLD:
            return None

        procedure_id = results[0]["procedure_id"]

        # Build datos dict from top procedure chunks
        procedure_chunks = [r for r in results if r["procedure_id"] == procedure_id]
        datos = self._build_datos(procedure_id, procedure_chunks)

        # Step 5: Build chunks_used for grounded prompting
        source_url = datos.get("fuente_url", "")
        chunks_used = [
            {
                "chunk_id": r.get("chunk_id", ""),
                "section_name": r.get("section_name", ""),
                "procedure_id": r.get("procedure_id", ""),
                "score": round(r.get("rerank_score", r.get("score", 0)), 4),
                "source_url": source_url,
                "content_preview": (r.get("content", ""))[:200],
            }
            for r in procedure_chunks[:config.RAG_MAX_CHUNKS_IN_PROMPT]
        ]

        ctx = KBContext(
            tramite=procedure_id,
            datos=datos,
            fuente_url=source_url,
            verificado=bool(datos.get("verified_at")),
            chunks_used=chunks_used,
        )
        if not _validate_source_url(ctx):
            return None
        return ctx

    def _build_datos(self, procedure_id: str, chunks: list[dict]) -> dict:
        """Reconstruct a datos dict compatible with the LLM context builder."""
        # Get procedure-level metadata from the store
        proc = self.store.get_procedure(procedure_id)
        datos: dict = {}

        if proc:
            datos["nombre"] = proc.get("nombre", "")
            datos["descripcion"] = proc.get("descripcion", "")
            datos["organismo"] = proc.get("organismo", "")

        # Get full procedure record for structured fields
        from src.core.rag.database import SessionLocal
        from src.core.rag.models import ProcedureDoc
        session = SessionLocal()
        try:
            doc = session.get(ProcedureDoc, procedure_id)
            if doc:
                datos["fuente_url"] = doc.source_url or ""
                datos["verified_at"] = doc.verified_at.isoformat() if doc.verified_at else None
                if doc.requisitos:
                    datos["requisitos"] = doc.requisitos
                if doc.documentos_necesarios:
                    datos["documentos"] = doc.documentos_necesarios
                if doc.como_solicitar:
                    datos["como_solicitar"] = doc.como_solicitar
                if doc.plazos:
                    datos["plazos"] = doc.plazos
                if doc.keywords:
                    datos["keywords"] = doc.keywords
        finally:
            session.close()

        # Add chunk content as supplementary context
        for chunk in chunks:
            section = chunk.get("section_name", "")
            if section and section not in datos:
                datos[section] = chunk["content"]

        return datos


class FallbackRetriever(Retriever):
    """Fallback chain: PGVector -> JSON keyword -> Directory.
    With optional response cache."""

    def __init__(self):
        from src.core.config import config

        self.retrievers: list[Retriever] = []
        self.cache = None

        # Build chain based on config
        if config.RAG_ENABLED and config.RAG_DB_URL:
            try:
                self.retrievers.append(PGVectorRetriever())
            except Exception as e:
                logger.warning("PGVectorRetriever init failed: %s", e)

        self.retrievers.append(JSONKBRetriever())

        # Directory is always last resort
        from src.core.rag.directory import DirectoryRetriever
        self.retrievers.append(DirectoryRetriever())

        # Init cache if enabled
        if config.RAG_CACHE_ENABLED:
            from src.core.rag.response_cache import ResponseCache
            redis_url = os.getenv("REDIS_URL", "")
            self.cache = ResponseCache(
                backend=config.RAG_CACHE_BACKEND,
                redis_url=redis_url,
                ttl=config.RAG_CACHE_TTL,
            )

    # Map retriever class names to metric source labels
    _SOURCE_MAP = {
        "PGVectorRetriever": "pgvector",
        "JSONKBRetriever": "json_fallback",
        "DirectoryRetriever": "directory_fallback",
    }

    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        """Try each retriever in order. Cache if enabled."""
        import time
        from src.core.config import config

        start = time.time()
        source = "error"
        cache_hit = False

        try:
            # Check cache first
            if self.cache:
                cached = self.cache.get(query, language)
                if cached:
                    logger.debug("Cache hit for query: %s", query[:50])
                    cache_hit = True
                    source = "pgvector"  # cache holds previous successful result
                    return cached

            # Try each retriever
            for retriever in self.retrievers:
                try:
                    result = retriever.retrieve(query, language)
                    if result:
                        if self.cache:
                            self.cache.put(query, language, result)
                        source = self._SOURCE_MAP.get(
                            type(retriever).__name__, "pgvector"
                        )
                        logger.debug(
                            "Retriever %s returned result for: %s",
                            type(retriever).__name__, query[:50],
                        )
                        return result
                except Exception as e:
                    logger.warning(
                        "Retriever %s failed: %s", type(retriever).__name__, e,
                    )
                    continue

            return None
        finally:
            if config.RAG_METRICS_ENABLED:
                latency_ms = (time.time() - start) * 1000
                from src.utils.rag_metrics import rag_metrics
                rag_metrics.record_retrieval(source, latency_ms, cache_hit)


_retriever_instance: Retriever | None = None


def get_retriever() -> Retriever:
    """Factory — returns singleton retriever based on config."""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = _build_retriever()
    return _retriever_instance


def _build_retriever() -> Retriever:
    """Build the active retriever. Called once."""
    from src.core.config import config
    if config.RAG_FALLBACK_CHAIN:
        logger.info("Using FallbackRetriever (RAG_FALLBACK_CHAIN=true)")
        return FallbackRetriever()
    if config.RAG_ENABLED and config.RAG_DB_URL:
        logger.info("Using PGVectorRetriever (RAG_ENABLED=true, RAG_DB_URL set)")
        return PGVectorRetriever()
    return JSONKBRetriever()


def reset_retriever() -> None:
    """Reset singleton (for testing only)."""
    global _retriever_instance
    _retriever_instance = None
