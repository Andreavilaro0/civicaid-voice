"""Tests for JSON to PG migration."""

import hashlib
import json
import os
from unittest.mock import MagicMock, patch

import pytest

from src.core.rag.migrator import (
    _content_hash,
    _count_words,
    _generate_id,
    _get_org_abbrev,
    _map_to_procedure_doc,
    _slugify,
)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMV_PATH = os.path.join(REPO, "data", "tramites", "imv.json")


@pytest.fixture
def imv_data():
    with open(IMV_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestSlugify:
    """Tests for _slugify helper."""

    def test_basic_slugify(self):
        assert _slugify("Ingreso Minimo Vital") == "ingreso-minimo-vital"

    def test_slugify_accents(self):
        result = _slugify("Ingreso Minimo Vital")
        assert result == "ingreso-minimo-vital"

    def test_slugify_special_chars(self):
        result = _slugify("NIE / TIE (Extranjeria)")
        assert "nie" in result
        assert "/" not in result
        assert "(" not in result


class TestOrgAbbrev:
    """Tests for _get_org_abbrev helper."""

    def test_known_org(self):
        assert _get_org_abbrev("Seguridad Social") == "SEGSOCIAL"

    def test_known_org_case_insensitive(self):
        assert _get_org_abbrev("seguridad social") == "SEGSOCIAL"

    def test_unknown_org_fallback(self):
        result = _get_org_abbrev("Ministerio Desconocido")
        assert result == "MD"


class TestGenerateId:
    """Tests for _generate_id."""

    def test_imv_id_format(self):
        generated = _generate_id("Seguridad Social", "Ingreso Minimo Vital")
        assert generated.startswith("age-")
        assert "segsocial" in generated
        assert "ingreso" in generated

    def test_id_is_lowercase_with_hyphens(self):
        generated = _generate_id("SEPE", "Prestacion Desempleo")
        assert generated == generated.lower()
        assert " " not in generated


class TestFieldMapping:
    """Tests for _map_to_procedure_doc field mapping."""

    def test_fuente_url_maps_to_source_url(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["source_url"] == imv_data["fuente_url"]

    def test_documentos_maps_to_documentos_necesarios(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert "documentos_necesarios" in doc
        assert isinstance(doc["documentos_necesarios"], list)
        assert len(doc["documentos_necesarios"]) > 0

    def test_nombre_preserved(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["nombre"] == imv_data["nombre"]

    def test_source_type_is_age(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["source_type"] == "age"

    def test_idioma_default_es(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["idioma"] == "es"

    def test_requisitos_copied(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["requisitos"] == imv_data["requisitos"]

    def test_como_solicitar_copied(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["como_solicitar"] == imv_data["como_solicitar"]

    def test_plazos_copied(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["plazos"] == imv_data["plazos"]


class TestContentHash:
    """Tests for _content_hash."""

    def test_hash_is_sha256(self, imv_data):
        h = _content_hash(imv_data)
        assert len(h) == 64, "SHA-256 hex digest should be 64 chars"
        assert all(c in "0123456789abcdef" for c in h)

    def test_hash_deterministic(self, imv_data):
        h1 = _content_hash(imv_data)
        h2 = _content_hash(imv_data)
        assert h1 == h2

    def test_hash_changes_with_data(self, imv_data):
        h1 = _content_hash(imv_data)
        modified = dict(imv_data)
        modified["nombre"] = "Modificado"
        h2 = _content_hash(modified)
        assert h1 != h2

    def test_hash_matches_manual_sha256(self):
        data = {"key": "value"}
        expected = hashlib.sha256(
            json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        assert _content_hash(data) == expected


class TestCompletenessScore:
    """Tests for completeness_score calculation."""

    def test_imv_completeness_above_zero(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["completeness_score"] > 0.0

    def test_imv_completeness_at_most_one(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert doc["completeness_score"] <= 1.0

    def test_completeness_is_ratio(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        score = doc["completeness_score"]
        # Score should be a decimal with at most 2 decimal places
        assert score == round(score, 2)


class TestWordCount:
    """Tests for _count_words."""

    def test_imv_word_count_positive(self, imv_data):
        count = _count_words(imv_data)
        assert count > 0

    def test_word_count_simple_dict(self):
        data = {"field": "one two three"}
        assert _count_words(data) == 3

    def test_word_count_list_values(self):
        data = {"items": ["one two", "three four five"]}
        assert _count_words(data) == 5

    def test_word_count_never_zero(self):
        data = {}
        count = _count_words(data)
        assert count >= 1, "word_count should be at least 1 (max(count, 1))"


class TestVerifiedMapping:
    """Tests for verified fields mapping."""

    def test_verified_imv_has_verified_at(self, imv_data):
        doc = _map_to_procedure_doc(imv_data)
        assert "verified_at" in doc
        assert doc["verified_by"] == "manual"

    def test_unverified_has_no_verified_at(self):
        data = {
            "nombre": "Test",
            "organismo": "Test Org",
            "descripcion": "desc",
            "keywords": [],
            "verificado": False,
        }
        doc = _map_to_procedure_doc(data)
        assert "verified_at" not in doc


class TestMigrateTramite:
    """Tests for migrate_tramite function using mocks."""

    @patch("src.core.rag.migrator.embed_batch")
    @patch("src.core.rag.migrator.chunk_procedure")
    def test_migrate_tramite_calls_store(self, mock_chunk, mock_embed):
        from src.core.rag.chunker import ChunkData
        from src.core.rag.migrator import migrate_tramite

        mock_chunk.return_value = [
            ChunkData(
                content="chunk text",
                section_name="requisitos",
                heading_path="IMV > requisitos",
                token_count=5,
                chunk_index=0,
                metadata={"procedure_id": "imv"},
            )
        ]
        mock_embed.return_value = [[0.1] * 768]

        mock_store = MagicMock()
        mock_store.insert_procedure.return_value = {
            "procedure_id": "age-segsocial-imv",
            "chunks_inserted": 1,
            "replaced": False,
        }

        stats = migrate_tramite(IMV_PATH, store=mock_store)

        assert stats["procedure_id"] == "age-segsocial-imv"
        assert stats["tramite"] == "imv"
        mock_store.insert_procedure.assert_called_once()
        mock_embed.assert_called_once()
