"""Tests for territory detection."""
from src.core.rag.territory import detect_territory, CCAA_MAP, CITY_MAP


class TestDetectTerritory:
    # "en <territory>" pattern
    def test_en_madrid_city(self):
        result = detect_territory("ayuda alquiler en Madrid")
        assert result is not None
        assert result["ccaa"] == "madrid"

    def test_en_barcelona(self):
        result = detect_territory("empadronamiento en Barcelona")
        assert result is not None
        assert result["municipio"] == "barcelona"
        assert result["ccaa"] == "cataluna"

    def test_en_andalucia_ccaa(self):
        result = detect_territory("tarjeta sanitaria en Andalucia")
        assert result is not None
        assert result["ccaa"] == "andalucia"
        assert result["nivel"] == "ccaa"

    # Single word detection
    def test_single_word_bilbao(self):
        result = detect_territory("tramites Bilbao")
        assert result is not None
        assert result["ccaa"] == "pais_vasco"
        assert result["municipio"] == "bilbao"

    def test_single_word_valencia(self):
        result = detect_territory("ayudas Valencia")
        assert result is not None

    # No territory
    def test_no_territory(self):
        result = detect_territory("que es el ingreso minimo vital")
        assert result is None

    def test_greeting_no_territory(self):
        result = detect_territory("hola buenos dias")
        assert result is None

    # Accent insensitive
    def test_accent_insensitive(self):
        result = detect_territory("tramites en Málaga")
        assert result is not None
        assert result["municipio"] == "malaga"

    # N-gram matching
    def test_multi_word_city(self):
        result = detect_territory("NIE en San Sebastian")
        assert result is not None
        assert result["ccaa"] == "pais_vasco"

    def test_multi_word_ccaa(self):
        result = detect_territory("ayudas en Pais Vasco")
        assert result is not None
        assert result["ccaa"] == "pais_vasco"

    # Municipal level
    def test_municipal_level(self):
        result = detect_territory("empadronamiento en Sevilla")
        assert result is not None
        assert result["nivel"] == "municipal"

    # Edge cases
    def test_case_insensitive(self):
        result = detect_territory("ALICANTE tramites")
        assert result is not None


class TestCCAAMap:
    def test_has_17_unique_ccaa(self):
        unique_ccaa = set(CCAA_MAP.values())
        assert len(unique_ccaa) >= 17

    def test_cataluna_aliases(self):
        assert CCAA_MAP.get("cataluna") == "cataluna"
        assert CCAA_MAP.get("catalunya") == "cataluna"


class TestCityMap:
    def test_has_major_cities(self):
        major = ["madrid", "barcelona", "sevilla", "valencia", "bilbao", "zaragoza"]
        for city in major:
            assert city in CITY_MAP, f"Missing city: {city}"

    def test_city_has_ccaa_and_municipio(self):
        for city, info in CITY_MAP.items():
            assert "ccaa" in info, f"City {city} missing ccaa"
            assert "municipio" in info, f"City {city} missing municipio"
