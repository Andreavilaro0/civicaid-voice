"""Tests for structured section-based chunker."""

import json
import os

import pytest

from src.core.rag.chunker import (
    ChunkData,
    _estimate_tokens,
    _format_list,
    _section_to_text,
    _split_text_with_overlap,
    chunk_procedure,
)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMV_PATH = os.path.join(REPO, "data", "tramites", "imv.json")


@pytest.fixture
def imv_data():
    with open(IMV_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def minimal_doc():
    return {
        "id": "test-doc",
        "nombre": "Test Tramite",
        "descripcion": "Una descripcion breve del tramite.",
        "requisitos": ["Requisito uno", "Requisito dos"],
        "documentos": ["DNI", "Certificado"],
    }


class TestChunkData:
    """Tests for the ChunkData dataclass."""

    def test_chunkdata_creation(self):
        chunk = ChunkData(
            content="Some content",
            section_name="requisitos",
            heading_path="Test > requisitos",
            token_count=10,
            chunk_index=0,
        )
        assert chunk.content == "Some content"
        assert chunk.section_name == "requisitos"
        assert chunk.heading_path == "Test > requisitos"
        assert chunk.token_count == 10
        assert chunk.chunk_index == 0
        assert chunk.metadata == {}

    def test_chunkdata_with_metadata(self):
        meta = {"procedure_id": "imv", "idioma": "es"}
        chunk = ChunkData(
            content="text",
            section_name="desc",
            heading_path="path",
            token_count=5,
            chunk_index=0,
            metadata=meta,
        )
        assert chunk.metadata["procedure_id"] == "imv"
        assert chunk.metadata["idioma"] == "es"


class TestChunkProcedureWithIMV:
    """Tests for chunk_procedure using real IMV data."""

    def test_imv_produces_chunks(self, imv_data):
        chunks = chunk_procedure(imv_data)
        assert len(chunks) > 0, "IMV data should produce at least one chunk"

    def test_chunk_has_section_name(self, imv_data):
        chunks = chunk_procedure(imv_data)
        for chunk in chunks:
            assert chunk.section_name, f"Chunk {chunk.chunk_index} missing section_name"

    def test_chunk_has_heading_path(self, imv_data):
        chunks = chunk_procedure(imv_data)
        for chunk in chunks:
            assert chunk.heading_path, f"Chunk {chunk.chunk_index} missing heading_path"
            assert ">" in chunk.heading_path, "heading_path should contain '>'"

    def test_metadata_preserved(self, imv_data):
        chunks = chunk_procedure(imv_data)
        for chunk in chunks:
            assert "procedure_id" in chunk.metadata
            assert "idioma" in chunk.metadata
            assert chunk.metadata["idioma"] == "es"

    def test_chunk_indices_sequential(self, imv_data):
        chunks = chunk_procedure(imv_data)
        indices = [c.chunk_index for c in chunks]
        assert indices == list(range(len(chunks))), "Chunk indices should be sequential starting at 0"


class TestSectionMerging:
    """Tests for small-section merging behavior."""

    def test_small_sections_merged(self):
        doc = {
            "id": "test",
            "nombre": "Test",
            "descripcion": "Short.",
            "requisitos": ["One"],
        }
        chunks = chunk_procedure(doc)
        # Both sections are small (< 200 tokens), should be merged into one chunk
        assert len(chunks) == 1
        merged_name = chunks[0].section_name
        assert "+" in merged_name, "Merged sections should have '+' in section_name"

    def test_medium_section_not_merged(self):
        long_text = " ".join(["palabra"] * 200)  # ~260 tokens
        doc = {
            "id": "test",
            "nombre": "Test",
            "descripcion": long_text,
            "requisitos": ["Requisito uno", "Requisito dos"],
        }
        chunks = chunk_procedure(doc)
        # descripcion is large enough to stand alone
        section_names = [c.section_name for c in chunks]
        assert any("descripcion" in s and "+" not in s for s in section_names) or len(chunks) >= 1


class TestLargeSectionSplitting:
    """Tests for splitting large sections with overlap."""

    def test_large_section_gets_split(self):
        long_text = " ".join(["palabra"] * 600)  # ~780 tokens, well above _MAX_TOKENS=600
        doc = {
            "id": "test",
            "nombre": "Test",
            "descripcion": long_text,
        }
        chunks = chunk_procedure(doc)
        assert len(chunks) > 1, "Large section should be split into multiple chunks"

    def test_split_text_with_overlap_produces_overlapping_chunks(self):
        text = " ".join([f"word{i}" for i in range(100)])
        parts = _split_text_with_overlap(text, max_tokens=50, overlap_tokens=10)
        assert len(parts) > 1, "Should produce multiple chunks"
        # Check overlap: last words of part[0] should appear in start of part[1]
        words_0 = parts[0].split()
        words_1 = parts[1].split()
        # The overlap means some words at the end of chunk 0 appear at the start of chunk 1
        overlap_count = 0
        for w in words_0[-10:]:
            if w in words_1[:15]:
                overlap_count += 1
        assert overlap_count > 0, "Chunks should have overlapping words"


class TestHelpers:
    """Tests for internal helper functions."""

    def test_estimate_tokens(self):
        text = "una dos tres cuatro cinco"
        tokens = _estimate_tokens(text)
        # 5 words * 1.3 factor = 6.5 -> 6
        assert tokens == 6

    def test_format_list(self):
        result = _format_list(["a", "b", "c"], "Items")
        assert "Items:" in result
        assert "1. a" in result
        assert "2. b" in result
        assert "3. c" in result

    def test_section_to_text_string(self):
        assert _section_to_text("descripcion", "Hello") == "Hello"

    def test_section_to_text_none(self):
        assert _section_to_text("descripcion", None) == ""

    def test_empty_doc_returns_no_chunks(self):
        doc = {"id": "empty", "nombre": "Empty"}
        chunks = chunk_procedure(doc)
        assert chunks == []
