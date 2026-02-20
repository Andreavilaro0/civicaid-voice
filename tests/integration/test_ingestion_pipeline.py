"""Integration tests for ingestion pipeline — mock embedder, skip if no Docker."""

import json
import os
import tempfile

import pytest
from unittest.mock import MagicMock, patch

from src.core.rag.ingestion import IngestionPipeline, FetchResult

# Skip all tests if PG is not available (Docker dependency)
pytestmark = pytest.mark.skipif(
    not os.getenv("RAG_DB_URL"),
    reason="RAG_DB_URL not set — Docker/PG not available",
)


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
def tramite_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        for name in ["imv.json", "empadronamiento.json", "tarjeta_sanitaria.json"]:
            data = {
                "nombre": name.replace(".json", ""),
                "organismo": "Test Org",
                "descripcion": "Descripcion de prueba del tramite.",
                "keywords": ["test"],
                "requisitos": ["Ser residente"],
                "documentos": ["DNI"],
            }
            with open(os.path.join(tmpdir, name), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        yield tmpdir


class TestIngestionPipelineIntegration:
    @patch("src.core.rag.ingestion.config")
    @patch("src.core.rag.ingestion.embed_batch", return_value=[[0.1] * 768])
    @patch("src.core.rag.ingestion.chunk_procedure")
    def test_full_ingest_flow(
        self, mock_chunk, mock_embed, mock_config, pipeline, mock_store, tramite_dir,
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        mock_chunk_obj = MagicMock(content="c", metadata={})
        mock_chunk.return_value = [mock_chunk_obj]

        path = os.path.join(tramite_dir, "imv.json")
        result = pipeline.ingest_source(path)
        assert result.status in ("fetched", "updated")
        assert result.chunks_created >= 1
        mock_store.insert_procedure.assert_called_once()

    @patch("src.core.rag.ingestion.config")
    @patch("src.core.rag.ingestion.chunk_procedure")
    def test_dry_run_skips_db(
        self, mock_chunk, mock_config, pipeline, mock_store, tramite_dir,
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        mock_chunk.return_value = [MagicMock(content="c", metadata={})]

        path = os.path.join(tramite_dir, "imv.json")
        result = pipeline.ingest_source(path, dry_run=True)
        assert result.status in ("fetched", "updated")
        mock_store.insert_procedure.assert_not_called()

    @patch("src.core.rag.ingestion.config")
    @patch("src.core.rag.ingestion.embed_batch", return_value=[[0.1] * 768])
    @patch("src.core.rag.ingestion.chunk_procedure")
    def test_ingest_all_processes_multiple(
        self, mock_chunk, mock_embed, mock_config, pipeline, tramite_dir,
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        mock_chunk.return_value = [MagicMock(content="c", metadata={})]

        with patch("src.core.rag.ingestion._TRAMITES_DIR", tramite_dir):
            results = pipeline.ingest_all()
        assert len(results) == 3
        assert all(isinstance(r, FetchResult) for r in results)

    @patch("src.core.rag.ingestion.config")
    def test_hash_match_skips_reingestion(
        self, mock_config, pipeline, mock_store, tramite_dir,
    ):
        mock_config.RAG_INGESTION_ENABLED = True
        path = os.path.join(tramite_dir, "imv.json")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        from src.core.rag.migrator import _content_hash
        h = _content_hash(data)

        mock_store.get_procedure.return_value = {"content_hash": h}
        result = pipeline.ingest_source(path)
        assert result.status == "no_change"
        mock_store.insert_procedure.assert_not_called()
