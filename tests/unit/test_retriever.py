"""Tests for the Retriever interface and JSONKBRetriever."""
import pytest
from src.core.retriever import Retriever, JSONKBRetriever, get_retriever
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
        result = r.retrieve("El tiempo en Barcelona hoy", "es")
        assert result is None


class TestGetRetriever:
    """Test the factory function."""

    def test_get_retriever_returns_json(self):
        r = get_retriever()
        assert isinstance(r, JSONKBRetriever)

    def test_get_retriever_returns_retriever(self):
        r = get_retriever()
        assert isinstance(r, Retriever)
