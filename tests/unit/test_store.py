"""Tests for PGVectorStore."""

from unittest.mock import MagicMock

import pytest

from src.core.rag.chunker import ChunkData


@pytest.fixture
def mock_session():
    session = MagicMock()
    return session


@pytest.fixture
def mock_session_factory(mock_session):
    factory = MagicMock(return_value=mock_session)
    return factory


@pytest.fixture
def store(mock_session_factory):
    from src.core.rag.store import PGVectorStore

    return PGVectorStore(session_factory=mock_session_factory)


@pytest.fixture
def sample_doc_data():
    return {
        "id": "age-segsocial-imv",
        "nombre": "Ingreso Minimo Vital",
        "descripcion": "Prestacion economica",
        "organismo": "Seguridad Social",
        "source_url": "https://example.com",
        "source_type": "age",
        "idioma": "es",
        "keywords": ["imv"],
        "content_hash": "a" * 64,
        "word_count": 100,
        "completeness_score": 0.8,
    }


@pytest.fixture
def sample_chunks():
    return [
        ChunkData(
            content="Chunk one content",
            section_name="requisitos",
            heading_path="IMV > requisitos",
            token_count=10,
            chunk_index=0,
            metadata={"procedure_id": "age-segsocial-imv", "source_type": "age"},
        ),
        ChunkData(
            content="Chunk two content",
            section_name="documentos",
            heading_path="IMV > documentos",
            token_count=8,
            chunk_index=1,
            metadata={"procedure_id": "age-segsocial-imv", "source_type": "age"},
        ),
    ]


class TestInsertProcedure:
    """Tests for insert_procedure method."""

    def test_insert_new_procedure(self, store, mock_session, sample_doc_data, sample_chunks):
        mock_session.get.return_value = None  # No existing procedure

        stats = store.insert_procedure(sample_doc_data, sample_chunks)

        assert stats["procedure_id"] == "age-segsocial-imv"
        assert stats["chunks_inserted"] == 2
        assert stats["replaced"] is False
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    def test_insert_replaces_existing_procedure(self, store, mock_session, sample_doc_data, sample_chunks):
        existing = MagicMock()
        existing.id = "age-segsocial-imv"
        mock_session.get.return_value = existing

        stats = store.insert_procedure(sample_doc_data, sample_chunks)

        assert stats["replaced"] is True
        assert stats["chunks_inserted"] == 2
        mock_session.query.return_value.filter.return_value.delete.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_insert_rolls_back_on_error(self, store, mock_session, sample_doc_data, sample_chunks):
        mock_session.get.return_value = None
        mock_session.commit.side_effect = Exception("DB error")

        with pytest.raises(Exception, match="DB error"):
            store.insert_procedure(sample_doc_data, sample_chunks)

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


class TestSearchVector:
    """Tests for search_vector method."""

    def test_search_vector_returns_results(self, store, mock_session):
        mock_row = MagicMock()
        mock_row.id = "chunk-1"
        mock_row.procedure_id = "age-segsocial-imv"
        mock_row.section_name = "requisitos"
        mock_row.heading_path = "IMV > requisitos"
        mock_row.content = "Tener entre 23 y 65 anos"
        mock_row.token_count = 10
        mock_row.metadata = {"idioma": "es"}
        mock_row.score = 0.92

        mock_session.execute.return_value.fetchall.return_value = [mock_row]

        query_embedding = [0.1] * 768
        results = store.search_vector(query_embedding, top_k=5, threshold=0.7)

        assert len(results) == 1
        assert results[0]["chunk_id"] == "chunk-1"
        assert results[0]["procedure_id"] == "age-segsocial-imv"
        assert results[0]["score"] == 0.92
        assert results[0]["content"] == "Tener entre 23 y 65 anos"
        mock_session.close.assert_called_once()

    def test_search_vector_empty_when_below_threshold(self, store, mock_session):
        mock_session.execute.return_value.fetchall.return_value = []

        query_embedding = [0.0] * 768
        results = store.search_vector(query_embedding, top_k=5, threshold=0.99)

        assert results == []
        mock_session.close.assert_called_once()


class TestCountMethods:
    """Tests for count_procedures and count_chunks."""

    def test_count_procedures(self, store, mock_session):
        mock_session.query.return_value.count.return_value = 8

        count = store.count_procedures()

        assert count == 8
        mock_session.close.assert_called_once()

    def test_count_chunks(self, store, mock_session):
        mock_session.query.return_value.count.return_value = 42

        count = store.count_chunks()

        assert count == 42
        mock_session.close.assert_called_once()


class TestDeleteProcedure:
    """Tests for delete_procedure method."""

    def test_delete_existing_procedure(self, store, mock_session):
        mock_procedure = MagicMock()
        mock_session.get.return_value = mock_procedure

        result = store.delete_procedure("age-segsocial-imv")

        assert result is True
        mock_session.delete.assert_called_once_with(mock_procedure)
        mock_session.commit.assert_called_once()

    def test_delete_nonexistent_returns_false(self, store, mock_session):
        mock_session.get.return_value = None

        result = store.delete_procedure("nonexistent")

        assert result is False
        mock_session.delete.assert_not_called()


class TestGetProcedure:
    """Tests for get_procedure method."""

    def test_get_existing_procedure(self, store, mock_session):
        mock_proc = MagicMock()
        mock_proc.id = "age-segsocial-imv"
        mock_proc.nombre = "IMV"
        mock_proc.descripcion = "Desc"
        mock_proc.organismo = "SS"
        mock_proc.source_type = "age"
        mock_proc.idioma = "es"
        mock_proc.chunks = [MagicMock(), MagicMock()]
        mock_proc.created_at = MagicMock()
        mock_proc.created_at.isoformat.return_value = "2026-01-01T00:00:00"
        mock_proc.updated_at = MagicMock()
        mock_proc.updated_at.isoformat.return_value = "2026-01-01T00:00:00"
        mock_session.get.return_value = mock_proc

        result = store.get_procedure("age-segsocial-imv")

        assert result is not None
        assert result["id"] == "age-segsocial-imv"
        assert result["chunk_count"] == 2

    def test_get_nonexistent_returns_none(self, store, mock_session):
        mock_session.get.return_value = None

        result = store.get_procedure("nonexistent")

        assert result is None
