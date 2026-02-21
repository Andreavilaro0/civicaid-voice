"""Tests for grounded prompting — chunks in system prompt."""
import pytest
from src.core.prompts.system_prompt import build_prompt, SYSTEM_PROMPT
from src.core.skills.llm_generate import _build_grounded_context
from src.core.models import KBContext


class TestSystemPromptCitationRules:
    def test_citation_rules_in_prompt(self):
        assert "[C1]" in SYSTEM_PROMPT
        assert "CHUNKS RECUPERADOS" in SYSTEM_PROMPT or "chunks" in SYSTEM_PROMPT.lower()

    def test_chunks_block_placeholder(self):
        assert "{chunks_block}" in SYSTEM_PROMPT

    def test_build_prompt_includes_chunks_block(self):
        prompt = build_prompt(
            kb_context="test context",
            chunks_block="CHUNKS RECUPERADOS:\n[C1] test chunk",
        )
        assert "[C1] test chunk" in prompt

    def test_build_prompt_empty_chunks_block(self):
        prompt = build_prompt(kb_context="test context", chunks_block="")
        # The system prompt template mentions "CHUNKS RECUPERADOS" in citation rules,
        # but with an empty chunks_block, no actual chunk data appears after the placeholder.
        assert "[C1]" not in prompt or "CHUNKS RECUPERADOS:\n[C1]" not in prompt


class TestBuildGroundedContext:
    @pytest.fixture
    def kb_with_chunks(self):
        return KBContext(
            tramite="imv",
            datos={"nombre": "IMV"},
            fuente_url="https://example.com/imv",
            chunks_used=[
                {
                    "chunk_id": "c1",
                    "section_name": "requisitos",
                    "procedure_id": "age-imv",
                    "score": 0.92,
                    "source_url": "https://seg-social.es/imv",
                    "content_preview": "Para solicitar el IMV necesitas...",
                },
                {
                    "chunk_id": "c2",
                    "section_name": "documentos",
                    "procedure_id": "age-imv",
                    "score": 0.85,
                    "source_url": "https://seg-social.es/imv",
                    "content_preview": "Documentos necesarios: DNI...",
                },
            ],
        )

    def test_builds_numbered_chunks(self, kb_with_chunks):
        result = _build_grounded_context(kb_with_chunks)
        assert "[C1]" in result
        assert "[C2]" in result

    def test_includes_section_name(self, kb_with_chunks):
        result = _build_grounded_context(kb_with_chunks)
        assert "requisitos" in result
        assert "documentos" in result

    def test_includes_source_url(self, kb_with_chunks):
        result = _build_grounded_context(kb_with_chunks)
        assert "https://seg-social.es/imv" in result

    def test_includes_score(self, kb_with_chunks):
        result = _build_grounded_context(kb_with_chunks)
        assert "0.92" in result

    def test_includes_content_preview(self, kb_with_chunks):
        result = _build_grounded_context(kb_with_chunks)
        assert "Para solicitar el IMV" in result

    def test_empty_chunks_returns_empty(self):
        kb = KBContext(tramite="imv", chunks_used=[])
        result = _build_grounded_context(kb)
        assert result == ""

    def test_respects_max_chunks(self, kb_with_chunks):
        result = _build_grounded_context(kb_with_chunks, max_chunks=1)
        assert "[C1]" in result
        assert "[C2]" not in result


class TestKBContextChunksUsed:
    def test_chunks_used_default_empty(self):
        kb = KBContext(tramite="test")
        assert kb.chunks_used == []

    def test_chunks_used_populated(self):
        kb = KBContext(
            tramite="test",
            chunks_used=[{"chunk_id": "c1", "score": 0.9}],
        )
        assert len(kb.chunks_used) == 1
        assert kb.chunks_used[0]["score"] == 0.9
