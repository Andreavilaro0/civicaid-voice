"""Integration tests for RAG pipeline. Requires Docker PG running."""

import os
import random
from unittest.mock import patch

import pytest

# Skip all tests in this module if no DB available
pytestmark = pytest.mark.skipif(
    not os.getenv("RAG_DB_URL"),
    reason="RAG_DB_URL not set — need Docker PG running",
)


@pytest.fixture(scope="module")
def db_tables():
    """Create fresh tables for the test module, drop after."""
    from src.core.rag.database import engine
    from src.core.rag.models import Base

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture()
def clean_db(db_tables):
    """Truncate all rows between tests."""
    from sqlalchemy import text

    from src.core.rag.database import SessionLocal

    session = SessionLocal()
    try:
        session.execute(text("TRUNCATE chunks, procedure_docs CASCADE"))
        session.commit()
    finally:
        session.close()


@pytest.fixture()
def mock_embedder():
    """Mock embedder with deterministic fake vectors."""
    rng = random.Random(42)
    with patch("src.core.rag.embedder.genai") as mock_genai:

        def fake_embed(*args, **kwargs):
            return {"embedding": [rng.random() for _ in range(768)]}

        mock_genai.embed_content.side_effect = fake_embed
        # Also mark as configured so _ensure_configured is a no-op
        with patch("src.core.rag.embedder._configured", True):
            yield mock_genai


@pytest.fixture()
def store():
    """Fresh PGVectorStore instance."""
    from src.core.rag.store import PGVectorStore

    return PGVectorStore()


def _imv_json_path() -> str:
    """Absolute path to data/tramites/imv.json."""
    return os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "data",
        "tramites",
        "imv.json",
    )


def test_migrate_imv_creates_chunks(clean_db, mock_embedder, store):
    """Migrate imv.json and verify procedure + chunks exist in DB."""
    from src.core.rag.migrator import migrate_tramite

    stats = migrate_tramite(_imv_json_path(), store=store)

    assert stats["procedure_id"] is not None
    assert stats["chunks_inserted"] > 0
    assert stats["replaced"] is False
    assert stats["tramite"] == "imv"

    # Verify in DB
    assert store.count_procedures() == 1
    assert store.count_chunks() == stats["chunks_inserted"]

    # Verify procedure is retrievable
    proc = store.get_procedure(stats["procedure_id"])
    assert proc is not None
    assert "Ingreso" in proc["nombre"]
    assert proc["idioma"] == "es"


def test_search_imv_by_query(clean_db, mock_embedder, store):
    """After migration, vector search returns IMV chunks."""
    from src.core.rag.embedder import embed_text
    from src.core.rag.migrator import migrate_tramite

    stats = migrate_tramite(_imv_json_path(), store=store)

    # Search with a query embedding
    query_embedding = embed_text("ingreso minimo vital ayuda economica")
    results = store.search_vector(
        query_embedding=query_embedding,
        top_k=5,
        threshold=0.0,  # Low threshold since embeddings are random
    )

    assert len(results) > 0
    assert results[0]["procedure_id"] == stats["procedure_id"]
    assert results[0]["content"] != ""
    assert results[0]["score"] > 0


def test_hybrid_search_returns_results(clean_db, mock_embedder, store):
    """Hybrid search combines BM25 + vector and returns ranked results."""
    from src.core.rag.embedder import embed_text
    from src.core.rag.migrator import migrate_tramite

    migrate_tramite(_imv_json_path(), store=store)

    query_embedding = embed_text("requisitos para solicitar el IMV")
    results = store.search_hybrid(
        query_text="requisitos solicitar IMV ingreso minimo",
        query_embedding=query_embedding,
        top_k=5,
        weight=0.5,
    )

    assert len(results) > 0

    # Hybrid results should have all score components
    top = results[0]
    assert "score" in top
    assert "vector_score" in top
    assert "bm25_score" in top
    assert top["score"] > 0
    assert top["content"] != ""


def test_migrate_idempotent_replaces(clean_db, mock_embedder, store):
    """Running migration twice replaces procedure without errors."""
    from src.core.rag.migrator import migrate_tramite

    stats1 = migrate_tramite(_imv_json_path(), store=store)
    assert stats1["replaced"] is False

    stats2 = migrate_tramite(_imv_json_path(), store=store)
    assert stats2["replaced"] is True
    assert stats2["procedure_id"] == stats1["procedure_id"]

    # Still only 1 procedure
    assert store.count_procedures() == 1
