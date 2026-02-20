"""Tests for src/core/rag/directory.py — static directory and DirectoryRetriever."""

from src.core.rag.directory import DIRECTORY, DirectoryRetriever


# ---------------------------------------------------------------------------
# Directory contents
# ---------------------------------------------------------------------------

EXPECTED_TRAMITES = [
    "imv",
    "empadronamiento",
    "tarjeta_sanitaria",
    "nie_tie",
    "prestacion_desempleo",
    "ayuda_alquiler",
    "certificado_discapacidad",
    "justicia_gratuita",
]


class TestDirectoryContents:
    def test_directory_contains_all_8_tramites(self):
        for t in EXPECTED_TRAMITES:
            assert t in DIRECTORY, f"Missing tramite: {t}"
        assert len(DIRECTORY) == 8

    def test_each_tramite_has_required_fields(self):
        for tid, info in DIRECTORY.items():
            assert "nombre" in info, f"{tid} missing nombre"
            assert "descripcion" in info, f"{tid} missing descripcion"
            assert "organismo" in info, f"{tid} missing organismo"
            assert "fuente_url" in info, f"{tid} missing fuente_url"
            assert "keywords" in info, f"{tid} missing keywords"
            assert len(info["keywords"]) > 0, f"{tid} has empty keywords"

    def test_fuente_url_not_empty(self):
        for tid, info in DIRECTORY.items():
            assert info["fuente_url"], f"{tid} has empty fuente_url"


# ---------------------------------------------------------------------------
# DirectoryRetriever
# ---------------------------------------------------------------------------

class TestDirectoryRetriever:
    def setup_method(self):
        self.retriever = DirectoryRetriever()

    def test_retrieve_imv(self):
        result = self.retriever.retrieve("que es el imv", "es")
        assert result is not None
        assert result.tramite == "imv"
        assert result.fuente_url != ""

    def test_retrieve_empadronamiento(self):
        result = self.retriever.retrieve("como hacer el empadronamiento", "es")
        assert result is not None
        assert result.tramite == "empadronamiento"

    def test_retrieve_returns_kbcontext_with_fuente_url(self):
        result = self.retriever.retrieve("necesito el nie", "es")
        assert result is not None
        assert result.fuente_url.startswith("http")

    def test_retrieve_irrelevant_query_returns_none(self):
        result = self.retriever.retrieve("receta de tortilla de patatas", "es")
        assert result is None

    def test_keyword_matching_case_insensitive(self):
        result = self.retriever.retrieve("NECESITO EL IMV", "es")
        assert result is not None
        assert result.tramite == "imv"

    def test_all_8_tramites_retrievable(self):
        """Each tramite should be retrievable via at least one of its keywords."""
        queries = {
            "imv": "necesito el imv ingreso minimo",
            "empadronamiento": "como empadronarme en el padron",
            "tarjeta_sanitaria": "tarjeta sanitaria medico",
            "nie_tie": "necesito el nie extranjeria",
            "prestacion_desempleo": "cobrar paro desempleo sepe",
            "ayuda_alquiler": "ayuda alquiler vivienda piso",
            "certificado_discapacidad": "certificado discapacidad grado",
            "justicia_gratuita": "abogado gratis turno oficio",
        }
        for expected_id, query in queries.items():
            result = self.retriever.retrieve(query, "es")
            assert result is not None, f"No result for {expected_id} with query: {query}"
            assert result.tramite == expected_id, (
                f"Expected {expected_id}, got {result.tramite} for query: {query}"
            )

    def test_datos_contains_source_marker(self):
        result = self.retriever.retrieve("imv", "es")
        assert result is not None
        assert result.datos.get("source") == "directory_fallback"

    def test_verificado_is_false(self):
        """Directory results are not verified (minimal fallback)."""
        result = self.retriever.retrieve("imv", "es")
        assert result is not None
        assert result.verificado is False
