"""Tests for the reranker module."""
import pytest
from unittest.mock import patch
from src.core.rag.reranker import (
    rerank, _heuristic_rerank, _compute_heuristic_scores, _SECTION_KEYWORDS,
)


@pytest.fixture
def sample_results():
    return [
        {"chunk_id": "c1", "procedure_id": "imv", "section_name": "descripcion",
         "content": "El ingreso minimo vital es una prestacion", "score": 0.8},
        {"chunk_id": "c2", "procedure_id": "imv", "section_name": "requisitos",
         "content": "Para solicitar necesitas tener residencia legal", "score": 0.75},
        {"chunk_id": "c3", "procedure_id": "imv", "section_name": "documentos",
         "content": "Documentos necesarios: DNI, certificado de empadronamiento", "score": 0.7},
    ]


class TestRerank:
    def test_empty_results_returns_empty(self):
        assert rerank("test", []) == []

    def test_strategy_none_returns_original(self, sample_results):
        result = rerank("test", sample_results, strategy="none")
        assert result == sample_results

    def test_strategy_heuristic_adds_rerank_score(self, sample_results):
        result = rerank("requisitos IMV", sample_results, strategy="heuristic")
        assert all("rerank_score" in r for r in result)

    def test_strategy_heuristic_sorted_descending(self, sample_results):
        result = rerank("requisitos", sample_results, strategy="heuristic")
        scores = [r["rerank_score"] for r in result]
        assert scores == sorted(scores, reverse=True)

    def test_gemini_fallback_to_heuristic(self, sample_results):
        """When Gemini fails, should fall back to heuristic."""
        with patch("src.core.rag.reranker._gemini_rerank", side_effect=Exception("API error")):
            result = rerank("test", sample_results, strategy="gemini")
            assert all("rerank_score" in r for r in result)


class TestHeuristicRerank:
    def test_boosts_matching_section(self, sample_results):
        """Query about 'requisitos' should boost requisitos chunk."""
        result = _heuristic_rerank("cuales son los requisitos", sample_results)
        assert result[0]["section_name"] == "requisitos"

    def test_boosts_matching_documents(self, sample_results):
        """Query about 'documentos' should boost documentos_necesarios chunk."""
        # Fix section_name to match _SECTION_KEYWORDS key "documentos_necesarios"
        for r in sample_results:
            if r["section_name"] == "documentos":
                r["section_name"] = "documentos_necesarios"
        result = _heuristic_rerank("que documentos necesito llevar", sample_results)
        assert result[0]["section_name"] == "documentos_necesarios"

    def test_keyword_overlap_matters(self, sample_results):
        """Higher keyword overlap = higher score."""
        result = _heuristic_rerank("prestacion ingreso minimo vital", sample_results)
        # Description chunk has more keyword overlap
        assert result[0]["content"].startswith("El ingreso")


class TestComputeHeuristicScores:
    def test_returns_list_of_floats(self, sample_results):
        scores = _compute_heuristic_scores("test query", sample_results)
        assert len(scores) == len(sample_results)
        assert all(isinstance(s, float) for s in scores)

    def test_scores_in_valid_range(self, sample_results):
        scores = _compute_heuristic_scores("test", sample_results)
        assert all(0 <= s <= 1.0 for s in scores)

    def test_section_match_boosts_score(self):
        results = [
            {"section_name": "requisitos", "content": "algo", "score": 0.5},
            {"section_name": "descripcion", "content": "algo", "score": 0.5},
        ]
        scores = _compute_heuristic_scores("requisitos del tramite", results)
        assert scores[0] > scores[1]


class TestSectionKeywords:
    def test_has_expected_sections(self):
        expected = ["requisitos", "documentos_necesarios", "como_solicitar", "plazos"]
        for section in expected:
            assert section in _SECTION_KEYWORDS
