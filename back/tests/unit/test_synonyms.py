"""Tests for synonym expansion and query normalization."""
from src.core.rag.synonyms import expand_query, normalize_query, SYNONYMS


class TestNormalizeQuery:
    def test_lowercases(self):
        assert normalize_query("HOLA MUNDO") == "hola mundo"

    def test_removes_accents(self):
        assert normalize_query("información básica") == "informacion basica"

    def test_combined(self):
        assert normalize_query("Ingreso Mínimo Vital") == "ingreso minimo vital"

    def test_empty_string(self):
        assert normalize_query("") == ""


class TestExpandQuery:
    def test_expands_imv(self):
        result = expand_query("quiero el IMV")
        assert "ingreso minimo vital" in result
        assert "imv" in result  # original kept

    def test_expands_nie(self):
        result = expand_query("como pido el NIE")
        assert "numero de identidad de extranjero" in result

    def test_expands_sepe(self):
        result = expand_query("SEPE")
        assert "servicio publico de empleo estatal" in result

    def test_expands_tsi(self):
        result = expand_query("TSI")
        assert "tarjeta sanitaria individual" in result

    def test_no_expansion_for_unknown(self):
        result = expand_query("hola buenos dias")
        assert result == "hola buenos dias"

    def test_multi_word_expansion(self):
        result = expand_query("necesito alquiler joven")
        # Verifies "alquiler joven" synonym expansion triggers
        assert "alquiler" in result
        assert "ayuda" in result
        assert "vivienda" in result

    def test_case_insensitive(self):
        result = expand_query("DNI")
        assert "documento nacional de identidad" in result

    def test_preserves_non_synonym_words(self):
        result = expand_query("requisitos imv en Madrid")
        assert "requisitos" in result
        assert "madrid" in result
        assert "ingreso minimo vital" in result


class TestSynonymsDict:
    def test_has_minimum_entries(self):
        assert len(SYNONYMS) >= 10

    def test_all_keys_lowercase(self):
        for key in SYNONYMS:
            assert key == key.lower(), f"Key '{key}' is not lowercase"

    def test_known_acronyms_present(self):
        required = ["imv", "nie", "tie", "sepe", "tsi", "dni"]
        for acronym in required:
            assert acronym in SYNONYMS, f"Missing acronym: {acronym}"
