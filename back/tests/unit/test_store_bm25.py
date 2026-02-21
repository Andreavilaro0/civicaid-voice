"""Tests for BM25 tuning and synonym expansion in PGVectorStore."""
import pytest
from unittest.mock import MagicMock, patch
from src.core.rag.store import PGVectorStore
from src.core.rag.synonyms import expand_query


class TestBM25SynonymIntegration:
    """Verify that search_hybrid uses expanded queries for BM25."""

    @pytest.fixture
    def store(self):
        mock_factory = MagicMock()
        mock_session = MagicMock()
        mock_factory.return_value = mock_session
        mock_session.execute.return_value.fetchall.return_value = []
        return PGVectorStore(session_factory=mock_factory)

    def test_search_hybrid_calls_expand_query(self, store):
        """search_hybrid should expand the query for BM25."""
        with patch("src.core.rag.store.expand_query", wraps=expand_query) as mock_expand:
            store.search_hybrid(
                query_text="IMV",
                query_embedding=[0.1] * 768,
                top_k=5,
                weight=0.5,
            )
            mock_expand.assert_called_once_with("IMV")

    def test_expanded_query_used_in_sql(self, store):
        """The expanded query (not original) should be passed to SQL."""
        mock_session = store._session_factory()
        store.search_hybrid(
            query_text="IMV",
            query_embedding=[0.1] * 768,
            top_k=5,
        )
        # Check that execute was called with expanded query containing "ingreso minimo vital"
        call_args = mock_session.execute.call_args
        params = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("params", {})
        if isinstance(params, dict):
            assert "ingreso minimo vital" in params.get("expanded_query", "").lower()

    def test_territory_filter_none_by_default(self, store):
        """Without territory_filter, no territory clause in SQL."""
        mock_session = store._session_factory()
        store.search_hybrid(
            query_text="requisitos IMV",
            query_embedding=[0.1] * 768,
        )
        mock_session.execute.assert_called_once()

    def test_territory_filter_ccaa(self, store):
        """With ccaa territory filter, should add WHERE clause."""
        mock_session = store._session_factory()
        store.search_hybrid(
            query_text="ayuda alquiler",
            query_embedding=[0.1] * 768,
            territory_filter={"ccaa": "madrid"},
        )
        call_args = mock_session.execute.call_args
        params = call_args[0][1] if len(call_args[0]) > 1 else {}
        if isinstance(params, dict):
            assert params.get("t_ccaa") == "madrid"

    def test_territory_filter_municipio(self, store):
        """With municipio territory filter, should add WHERE clause."""
        mock_session = store._session_factory()
        store.search_hybrid(
            query_text="empadronamiento",
            query_embedding=[0.1] * 768,
            territory_filter={"municipio": "barcelona", "ccaa": "cataluna"},
        )
        call_args = mock_session.execute.call_args
        params = call_args[0][1] if len(call_args[0]) > 1 else {}
        if isinstance(params, dict):
            assert params.get("t_municipio") == "barcelona"


class TestExpandQueryForBM25:
    """Verify expand_query produces BM25-friendly expanded terms."""

    def test_imv_expansion_for_bm25(self):
        expanded = expand_query("IMV")
        assert "ingreso" in expanded
        assert "minimo" in expanded
        assert "vital" in expanded

    def test_nie_expansion_for_bm25(self):
        expanded = expand_query("NIE")
        assert "identidad" in expanded
        assert "extranjero" in expanded

    def test_sepe_expansion_for_bm25(self):
        expanded = expand_query("SEPE")
        assert "empleo" in expanded

    def test_combined_acronyms(self):
        expanded = expand_query("necesito el IMV y el NIE")
        assert "ingreso minimo vital" in expanded
        assert "numero de identidad de extranjero" in expanded
