"""Integration test for PGVectorRetriever with reranking pipeline."""

import pytest
from unittest.mock import patch, MagicMock
from src.core.models import KBContext


class TestPGVectorRetrieverPipeline:
    """Test the full retriever pipeline: territory -> search -> rerank -> context."""

    @pytest.fixture
    def mock_config(self):
        cfg = MagicMock()
        cfg.RAG_TOP_K = 5
        cfg.RAG_HYBRID_WEIGHT = 0.5
        cfg.RAG_SIMILARITY_THRESHOLD = 0.7
        cfg.RAG_RERANK_STRATEGY = "heuristic"
        cfg.RAG_GROUNDED_PROMPTING = True
        cfg.RAG_MAX_CHUNKS_IN_PROMPT = 4
        cfg.RAG_ENABLED = True
        cfg.RAG_DB_URL = "postgresql://test"
        return cfg

    @pytest.fixture
    def mock_search_results(self):
        return [
            {
                "chunk_id": "c1", "procedure_id": "age-segsocial-imv",
                "section_name": "requisitos", "heading_path": "IMV > requisitos",
                "content": "Para solicitar el IMV necesitas residencia legal",
                "token_count": 10, "metadata": {},
                "score": 0.85, "vector_score": 0.9, "bm25_score": 0.3,
                "rerank_score": 0.85,
            },
            {
                "chunk_id": "c2", "procedure_id": "age-segsocial-imv",
                "section_name": "descripcion", "heading_path": "IMV > descripcion",
                "content": "El Ingreso Minimo Vital es una prestacion",
                "token_count": 8, "metadata": {},
                "score": 0.82, "vector_score": 0.85, "bm25_score": 0.2,
                "rerank_score": 0.82,
            },
        ]

    @pytest.fixture
    def mock_procedure_data(self):
        return {
            "id": "age-segsocial-imv",
            "nombre": "Ingreso Minimo Vital",
            "descripcion": "Prestacion economica",
            "organismo": "Seguridad Social",
            "source_type": "age",
            "idioma": "es",
        }

    def _make_retriever_with_mocks(self, mock_config, mock_store):
        """Create a PGVectorRetriever without calling __init__ (avoids DB)."""
        from src.core.retriever import PGVectorRetriever
        retriever = PGVectorRetriever.__new__(PGVectorRetriever)
        retriever.store = mock_store
        return retriever

    def test_retrieve_returns_kbcontext_with_chunks(
        self, mock_config, mock_search_results, mock_procedure_data
    ):
        """Full pipeline should return KBContext with chunks_used populated."""
        mock_store = MagicMock()
        mock_store.search_hybrid.return_value = mock_search_results
        mock_store.get_procedure.return_value = mock_procedure_data

        retriever = self._make_retriever_with_mocks(mock_config, mock_store)

        mock_doc = MagicMock()
        mock_doc.source_url = "https://seg-social.es/imv"
        mock_doc.verified_at = None
        mock_doc.requisitos = ["residencia legal"]
        mock_doc.documentos_necesarios = None
        mock_doc.como_solicitar = None
        mock_doc.plazos = None
        mock_doc.keywords = ["imv"]

        with patch("src.core.config.config", mock_config), \
             patch("src.core.rag.territory.detect_territory", return_value=None), \
             patch("src.core.rag.embedder.embed_text", return_value=[0.1] * 768), \
             patch("src.core.rag.reranker.rerank", return_value=mock_search_results), \
             patch("src.core.rag.database.SessionLocal") as mock_sl:
            mock_session = MagicMock()
            mock_sl.return_value = mock_session
            mock_session.get.return_value = mock_doc

            result = retriever.retrieve("requisitos IMV", "es")

        assert result is not None
        assert isinstance(result, KBContext)
        assert result.tramite == "age-segsocial-imv"
        assert len(result.chunks_used) > 0
        assert result.chunks_used[0]["chunk_id"] == "c1"

    def test_retrieve_with_territory_detection(
        self, mock_config, mock_search_results, mock_procedure_data
    ):
        """Territory should be detected and passed to search."""
        territory = {"nivel": "municipal", "ccaa": "madrid", "municipio": "madrid"}

        mock_store = MagicMock()
        mock_store.search_hybrid.return_value = mock_search_results
        mock_store.get_procedure.return_value = mock_procedure_data

        retriever = self._make_retriever_with_mocks(mock_config, mock_store)

        mock_doc = MagicMock()
        mock_doc.source_url = "https://example.com"
        mock_doc.verified_at = None
        mock_doc.requisitos = None
        mock_doc.documentos_necesarios = None
        mock_doc.como_solicitar = None
        mock_doc.plazos = None
        mock_doc.keywords = None

        with patch("src.core.config.config", mock_config), \
             patch("src.core.rag.territory.detect_territory", return_value=territory), \
             patch("src.core.rag.embedder.embed_text", return_value=[0.1] * 768), \
             patch("src.core.rag.reranker.rerank", return_value=mock_search_results), \
             patch("src.core.rag.database.SessionLocal") as mock_sl:
            mock_session = MagicMock()
            mock_sl.return_value = mock_session
            mock_session.get.return_value = mock_doc

            retriever.retrieve("ayuda alquiler en Madrid", "es")

        # Verify territory was passed to search
        mock_store.search_hybrid.assert_called_once()
        call_kwargs = mock_store.search_hybrid.call_args
        assert call_kwargs.kwargs.get("territory_filter") == territory

    def test_retrieve_returns_none_below_threshold(self, mock_config):
        """Should return None if top score is below threshold."""
        low_results = [
            {"chunk_id": "c1", "procedure_id": "test", "section_name": "desc",
             "content": "text", "score": 0.3, "rerank_score": 0.3,
             "heading_path": "", "token_count": 5, "metadata": {},
             "vector_score": 0.3, "bm25_score": 0.1},
        ]

        mock_store = MagicMock()
        mock_store.search_hybrid.return_value = low_results

        retriever = self._make_retriever_with_mocks(mock_config, mock_store)

        with patch("src.core.config.config", mock_config), \
             patch("src.core.rag.territory.detect_territory", return_value=None), \
             patch("src.core.rag.embedder.embed_text", return_value=[0.1] * 768), \
             patch("src.core.rag.reranker.rerank", return_value=low_results):

            result = retriever.retrieve("query", "es")

        assert result is None

    def test_retrieve_returns_none_on_empty_results(self, mock_config):
        """Should return None if search returns empty."""
        mock_store = MagicMock()
        mock_store.search_hybrid.return_value = []

        retriever = self._make_retriever_with_mocks(mock_config, mock_store)

        with patch("src.core.config.config", mock_config), \
             patch("src.core.rag.territory.detect_territory", return_value=None), \
             patch("src.core.rag.embedder.embed_text", return_value=[0.1] * 768):

            result = retriever.retrieve("nonexistent query", "es")

        assert result is None

    def test_retrieve_handles_search_exception(self, mock_config):
        """Should return None and log on search error."""
        mock_store = MagicMock()

        retriever = self._make_retriever_with_mocks(mock_config, mock_store)

        with patch("src.core.config.config", mock_config), \
             patch("src.core.rag.territory.detect_territory", return_value=None), \
             patch("src.core.rag.embedder.embed_text", side_effect=Exception("embed fail")):

            result = retriever.retrieve("test query", "es")

        assert result is None


class TestGetRetriever:
    """Tests for get_retriever factory."""

    def test_returns_retriever_when_rag_disabled(self):
        from src.core.retriever import JSONKBRetriever, FallbackRetriever, reset_retriever

        mock_cfg = MagicMock()
        mock_cfg.RAG_ENABLED = False
        mock_cfg.RAG_DB_URL = ""
        mock_cfg.RAG_FALLBACK_CHAIN = True

        with patch("src.core.config.config", mock_cfg):
            from src.core.retriever import get_retriever
            reset_retriever()
            retriever = get_retriever()
            reset_retriever()
            # With RAG_FALLBACK_CHAIN=true, returns FallbackRetriever
            assert isinstance(retriever, (FallbackRetriever, JSONKBRetriever))

    def test_returns_json_when_no_db_url(self):
        from src.core.retriever import JSONKBRetriever, FallbackRetriever, reset_retriever

        mock_cfg = MagicMock()
        mock_cfg.RAG_ENABLED = True
        mock_cfg.RAG_DB_URL = ""
        mock_cfg.RAG_FALLBACK_CHAIN = True

        with patch("src.core.config.config", mock_cfg):
            from src.core.retriever import get_retriever
            reset_retriever()
            retriever = get_retriever()
            reset_retriever()
            # With RAG_FALLBACK_CHAIN=true (default), returns FallbackRetriever
            assert isinstance(retriever, (FallbackRetriever, JSONKBRetriever))
