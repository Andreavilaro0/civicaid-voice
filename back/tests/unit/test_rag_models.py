"""Tests for RAG SQLAlchemy models."""

import uuid

import pytest


# Patch pgvector and sqlalchemy before importing models
@pytest.fixture(autouse=True)
def _patch_vector():
    """Ensure pgvector Vector type doesn't need a real PG connection."""
    pass


class TestProcedureDoc:
    """Tests for the ProcedureDoc model."""

    def test_instantiation_with_required_fields(self):
        from src.core.rag.models import ProcedureDoc

        doc = ProcedureDoc(
            id="age-segsocial-imv",
            nombre="Ingreso Minimo Vital",
            descripcion="Prestacion economica contra la pobreza",
            organismo="Seguridad Social",
            source_url="https://seg-social.es/imv",
            source_type="age",
            idioma="es",
            keywords=["imv", "ingreso minimo"],
            content_hash="a" * 64,
            word_count=500,
            completeness_score=0.85,
        )
        assert doc.id == "age-segsocial-imv"
        assert doc.nombre == "Ingreso Minimo Vital"
        assert doc.descripcion == "Prestacion economica contra la pobreza"
        assert doc.organismo == "Seguridad Social"
        assert doc.source_url == "https://seg-social.es/imv"
        assert doc.source_type == "age"
        assert doc.idioma == "es"
        assert doc.keywords == ["imv", "ingreso minimo"]
        assert doc.content_hash == "a" * 64
        assert doc.word_count == 500
        assert doc.completeness_score == 0.85

    def test_optional_fields_default_to_none(self):
        from src.core.rag.models import ProcedureDoc

        doc = ProcedureDoc(
            id="test-doc",
            nombre="Test",
            descripcion="Desc",
            organismo="Org",
            source_url="https://example.com",
            source_type="age",
            idioma="es",
            keywords=[],
            content_hash="b" * 64,
            word_count=10,
            completeness_score=0.5,
        )
        assert doc.organismo_abrev is None
        assert doc.territorio_nivel is None
        assert doc.territorio_ccaa is None
        assert doc.territorio_municipio is None
        assert doc.canal is None
        assert doc.requisitos is None
        assert doc.documentos_necesarios is None
        assert doc.plazos is None
        assert doc.tasas is None
        assert doc.base_legal is None
        assert doc.tags is None
        assert doc.extracted_at is None
        assert doc.verified_at is None
        assert doc.verified_by is None


class TestChunk:
    """Tests for the Chunk model."""

    def test_chunk_instantiation(self):
        from src.core.rag.models import Chunk

        chunk = Chunk(
            id=str(uuid.uuid4()),
            procedure_id="age-segsocial-imv",
            section_name="requisitos",
            heading_path="IMV > requisitos",
            content="Tener entre 23 y 65 anos",
            token_count=10,
            chunk_index=0,
        )
        assert chunk.procedure_id == "age-segsocial-imv"
        assert chunk.section_name == "requisitos"
        assert chunk.heading_path == "IMV > requisitos"
        assert chunk.content == "Tener entre 23 y 65 anos"
        assert chunk.token_count == 10
        assert chunk.chunk_index == 0

    def test_chunk_with_embedding_vector(self):
        from src.core.rag.models import Chunk

        mock_embedding = [0.1] * 768
        chunk = Chunk(
            id="chunk-001",
            procedure_id="age-segsocial-imv",
            section_name="descripcion",
            heading_path="IMV > descripcion",
            content="Prestacion economica",
            token_count=5,
            embedding=mock_embedding,
            chunk_index=0,
            metadata_={"source_type": "age", "idioma": "es"},
        )
        assert chunk.embedding == mock_embedding
        assert len(chunk.embedding) == 768
        assert chunk.metadata_ == {"source_type": "age", "idioma": "es"}

    def test_chunk_embedding_defaults_to_none(self):
        from src.core.rag.models import Chunk

        chunk = Chunk(
            id="chunk-002",
            procedure_id="test",
            section_name="desc",
            content="text",
            token_count=1,
            chunk_index=0,
        )
        assert chunk.embedding is None


class TestSource:
    """Tests for the Source model."""

    def test_source_instantiation(self):
        from src.core.rag.models import Source

        source = Source(
            id="seg-social",
            name="Seguridad Social",
            url="https://seg-social.es",
            source_type="age",
            gov_tier="national",
        )
        assert source.id == "seg-social"
        assert source.name == "Seguridad Social"
        assert source.url == "https://seg-social.es"
        assert source.source_type == "age"
        assert source.gov_tier == "national"

    def test_source_defaults(self):
        from src.core.rag.models import Source

        source = Source(
            id="test-src",
            name="Test",
            url="https://example.com",
            source_type="local",
            gov_tier="municipal",
        )
        assert source.last_checked_at is None
        assert source.last_fetched_at is None
        assert source.metadata_ is None


class TestIngestionLog:
    """Tests for the IngestionLog model."""

    def test_ingestion_log_creation(self):
        from src.core.rag.models import IngestionLog

        log = IngestionLog(
            procedure_id="age-segsocial-imv",
            source_id="seg-social",
            action="insert",
            chunks_created=5,
            chunks_updated=0,
            duration_ms=1200,
        )
        assert log.procedure_id == "age-segsocial-imv"
        assert log.source_id == "seg-social"
        assert log.action == "insert"
        assert log.chunks_created == 5
        assert log.chunks_updated == 0
        assert log.duration_ms == 1200

    def test_ingestion_log_update_action(self):
        from src.core.rag.models import IngestionLog

        log = IngestionLog(
            procedure_id="age-segsocial-imv",
            action="update",
            chunks_created=0,
            chunks_updated=3,
        )
        assert log.action == "update"
        assert log.source_id is None
        assert log.duration_ms is None
