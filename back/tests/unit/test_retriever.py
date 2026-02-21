"""Tests for the Retriever interface and JSONKBRetriever."""
import pytest
from src.core.retriever import Retriever, JSONKBRetriever, FallbackRetriever, get_retriever, reset_retriever
from src.core.models import KBContext


class TestRetrieverInterface:
    """Verify the abstract interface contract."""

    def test_retriever_is_abstract(self):
        with pytest.raises(TypeError):
            Retriever()

    def test_json_kb_retriever_is_retriever(self):
        r = JSONKBRetriever()
        assert isinstance(r, Retriever)


class TestJSONKBRetriever:
    """Test the keyword-matching retriever backed by JSON files."""

    def test_json_kb_retriever_finds_imv(self):
        r = JSONKBRetriever()
        result = r.retrieve("Quiero solicitar el IMV", "es")
        assert result is not None
        assert isinstance(result, KBContext)
        assert result.tramite == "imv"

    def test_json_kb_retriever_finds_empadronamiento(self):
        r = JSONKBRetriever()
        result = r.retrieve("Como me empadrono en Madrid", "es")
        assert result is not None
        assert result.tramite == "empadronamiento"

    def test_json_kb_retriever_no_match(self):
        r = JSONKBRetriever()
        result = r.retrieve("Cual es la capital de Francia", "es")
        assert result is None


class TestGetRetriever:
    """Test the factory function."""

    def test_get_retriever_returns_fallback_or_json(self):
        reset_retriever()
        r = get_retriever()
        reset_retriever()
        # With RAG_FALLBACK_CHAIN=true (default), returns FallbackRetriever
        # which wraps JSONKBRetriever as part of its chain
        assert isinstance(r, (FallbackRetriever, JSONKBRetriever))

    def test_get_retriever_returns_retriever(self):
        reset_retriever()
        r = get_retriever()
        reset_retriever()
        assert isinstance(r, Retriever)
