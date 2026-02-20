"""Unit tests for src/core/rag/ingestion.py — IngestionPipeline."""

import json
import os
import tempfile

import pytest
from unittest.mock import MagicMock, patch

from src.core.rag.ingestion import FetchResult, IngestionPipeline


@pytest.fixture
def mock_store():
    store = MagicMock()
    store.get_procedure.return_value = None
    store.insert_procedure.return_value = None
    store.update_fetch_timestamp.return_value = None
    store._get_session.return_value = MagicMock()
    return store


@pytest.fixture
def pipeline(mock_store):
    return IngestionPipeline(mock_store)


@pytest.fixture
def sample_tramite_file():
    data = {
        "nombre": "Test Tramite",
        "organismo": "Seguridad Social",
        "descripcion": "Una descripcion de prueba para el tramite.",
        "keywords": ["test", "prueba"],
        "requisitos": ["Ser mayor de edad"],
        "documentos": ["DNI", "Certificado"],
        "como_solicitar": [{"via": "Online", "detalle": "Sede electronica"}],
        "fuente_url": "https://example.com",
    }
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False)
        path = f.name
    yield path
    os.unlink(path)


class TestFetchResultDataclass:
    def test_fields_exist(self):
        r = FetchResult(source_id="test", status="fetched")
        assert r.source_id == "test"
        assert r.status == "fetched"
        assert r.content_hash == ""
        assert r.error == ""
        assert r.chunks_created == 0
        assert r.duration_ms == 0

    def test_custom_values(self):
        r = FetchResult(
            source_id="s1", status="error", error="boom", chunks_created=5
        )
        assert r.error == "boom"
        assert r.chunks_created == 5


class TestIngestionPipelineInit:
    def test_creates_with_store(self, mock_store):
        p = IngestionPipeline(mock_store)
        assert p.store is mock_store


class TestIngestSource:
    @patch("src.core.rag.ingestion.config")
    @patch("src.core.rag.ingestion.embed_batch", return_value=[[0.1] * 768])
    @patch("src.core.rag.ingestion.chunk_procedure")
    def test_valid_json_ingests(
        self, mock_chunk, mock_embed, mock_config, pipeline, mock_store, sample_tramite_file
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        mock_chunk_obj = MagicMock()
        mock_chunk_obj.content = "test content"
        mock_chunk_obj.metadata = {}
        mock_chunk.return_value = [mock_chunk_obj]

        result = pipeline.ingest_source(sample_tramite_file)
        assert result.status in ("fetched", "updated")
        assert result.chunks_created == 1
        mock_store.insert_procedure.assert_called_once()

    @patch("src.core.rag.ingestion.config")
    @patch("src.core.rag.ingestion.chunk_procedure")
    def test_dry_run_no_db_writes(
        self, mock_chunk, mock_config, pipeline, mock_store, sample_tramite_file
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        mock_chunk.return_value = [MagicMock(content="x", metadata={})]

        result = pipeline.ingest_source(sample_tramite_file, dry_run=True)
        assert result.status in ("fetched", "updated")
        mock_store.insert_procedure.assert_not_called()

    @patch("src.core.rag.ingestion.config")
    def test_missing_file_returns_error(self, mock_config, pipeline):
        mock_config.RAG_INGESTION_ENABLED = True
        result = pipeline.ingest_source("/nonexistent/path.json")
        assert result.status == "error"
        assert "not found" in result.error.lower()

    @patch("src.core.rag.ingestion.config")
    def test_invalid_json_returns_error(self, mock_config, pipeline):
        mock_config.RAG_INGESTION_ENABLED = True
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("{bad json")
            path = f.name
        try:
            result = pipeline.ingest_source(path)
            assert result.status == "error"
            assert "invalid json" in result.error.lower()
        finally:
            os.unlink(path)

    @patch("src.core.rag.ingestion.config")
    def test_content_hash_no_change(
        self, mock_config, pipeline, mock_store, sample_tramite_file
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        # First call to compute the hash
        with open(sample_tramite_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        from src.core.rag.migrator import _content_hash, _map_to_procedure_doc
        expected_hash = _content_hash(data)
        _map_to_procedure_doc(data)

        mock_store.get_procedure.return_value = {"content_hash": expected_hash}
        result = pipeline.ingest_source(sample_tramite_file)
        assert result.status == "no_change"

    @patch("src.core.rag.ingestion.config")
    def test_ingestion_disabled_returns_error(self, mock_config, pipeline, sample_tramite_file):
        mock_config.RAG_INGESTION_ENABLED = False
        result = pipeline.ingest_source(sample_tramite_file)
        assert result.status == "error"
        assert "INGESTION_ENABLED" in result.error


class TestIngestAll:
    @patch("src.core.rag.ingestion.config")
    def test_nonexistent_dir_returns_empty(self, mock_config, pipeline):
        mock_config.RAG_INGESTION_ENABLED = True
        with patch("src.core.rag.ingestion._TRAMITES_DIR", "/nonexistent/dir"):
            results = pipeline.ingest_all()
        assert results == []

    @patch("src.core.rag.ingestion.config")
    @patch("src.core.rag.ingestion.embed_batch", return_value=[[0.1] * 768])
    @patch("src.core.rag.ingestion.chunk_procedure")
    def test_processes_json_files(
        self, mock_chunk, mock_embed, mock_config, pipeline
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        mock_chunk_obj = MagicMock(content="c", metadata={})
        mock_chunk.return_value = [mock_chunk_obj]

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create 2 sample JSONs
            for name in ["a.json", "b.json"]:
                with open(os.path.join(tmpdir, name), "w") as f:
                    json.dump(
                        {"nombre": name, "organismo": "Test", "descripcion": "d", "keywords": []},
                        f,
                    )
            with patch("src.core.rag.ingestion._TRAMITES_DIR", tmpdir):
                results = pipeline.ingest_all()
            assert len(results) == 2
