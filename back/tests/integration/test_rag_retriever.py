"""Integration tests for RAG retriever. Requires Docker PG running."""

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
        with patch("src.core.rag.embedder._configured", True):
            yield mock_genai


@pytest.fixture()
def migrated_imv(clean_db, mock_embedder):
    """Migrate IMV into the database and return the procedure_id."""
    from src.core.rag.migrator import migrate_tramite
    from src.core.rag.store import PGVectorStore

    store = PGVectorStore()
    imv_path = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "data",
        "tramites",
        "imv.json",
    )
    stats = migrate_tramite(imv_path, store=store)
    return stats["procedure_id"]


def test_pgvector_retriever_returns_kbcontext(migrated_imv, mock_embedder):
    """PGVectorRetriever.retrieve() returns a valid KBContext."""
    from src.core.models import KBContext
    from src.core.retriever import PGVectorRetriever

    retriever = PGVectorRetriever()

    # Patch config thresholds to be very permissive for random embeddings
    with patch("src.core.retriever.config") as mock_config:
        mock_config.RAG_TOP_K = 5
        mock_config.RAG_HYBRID_WEIGHT = 0.5
        mock_config.RAG_SIMILARITY_THRESHOLD = 0.0  # Accept any score

        result = retriever.retrieve("que es el IMV ingreso minimo vital", "es")

    assert result is not None
    assert isinstance(result, KBContext)
    assert result.tramite == migrated_imv
    assert result.datos.get("nombre") is not None
    assert "Ingreso" in result.datos["nombre"]
    assert result.datos.get("descripcion") != ""
    assert result.fuente_url != ""


def test_pgvector_retriever_returns_none_below_threshold(migrated_imv, mock_embedder):
    """PGVectorRetriever returns None when score is below threshold."""
    from src.core.retriever import PGVectorRetriever

    retriever = PGVectorRetriever()

    # Set threshold impossibly high
    with patch("src.core.retriever.config") as mock_config:
        mock_config.RAG_TOP_K = 5
        mock_config.RAG_HYBRID_WEIGHT = 0.5
        mock_config.RAG_SIMILARITY_THRESHOLD = 99.0  # Impossible threshold

        result = retriever.retrieve("que es el IMV", "es")

    assert result is None


def test_fallback_to_json_retriever():
    """With RAG_ENABLED=false, get_retriever() returns JSONKBRetriever."""
    from src.core.retriever import JSONKBRetriever, get_retriever

    with patch("src.core.retriever.config") as mock_config:
        mock_config.RAG_ENABLED = False
        mock_config.RAG_DB_URL = ""

        retriever = get_retriever()

    assert isinstance(retriever, JSONKBRetriever)


def test_pgvector_retriever_selected_when_rag_enabled():
    """With RAG_ENABLED=true and RAG_DB_URL set, get_retriever() returns PGVectorRetriever."""
    from src.core.retriever import PGVectorRetriever, get_retriever

    with patch("src.core.retriever.config") as mock_config:
        mock_config.RAG_ENABLED = True
        mock_config.RAG_DB_URL = "postgresql://test:test@localhost:5432/test"

        retriever = get_retriever()

    assert isinstance(retriever, PGVectorRetriever)
