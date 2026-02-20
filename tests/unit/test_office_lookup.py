"""Tests for office_lookup skill."""

from src.core.skills.office_lookup import office_lookup, _OFICINAS, _GENERIC_FALLBACK


class TestOficinasLoaded:
    """Verify oficinas.json loads correctly."""

    def test_oficinas_loaded(self):
        assert len(_OFICINAS) > 0, "oficinas.json should load at least one city"

    def test_ten_cities_loaded(self):
        expected = {
            "madrid", "barcelona", "valencia", "sevilla", "bilbao",
            "zaragoza", "malaga", "alicante", "murcia", "palma de mallorca",
        }
        assert expected == set(_OFICINAS.keys())

    def test_each_city_has_three_tramites(self):
        expected_tramites = {"empadronamiento", "tarjeta_sanitaria", "imv"}
        for city, data in _OFICINAS.items():
            assert set(data.keys()) == expected_tramites, f"{city} missing tramites"


class TestOfficeLookup:
    """Test office_lookup function."""

    def test_exact_match_madrid_empadronamiento(self):
        result = office_lookup("madrid", "empadronamiento")
        assert result is not None
        assert "OAC" in result["oficina"] or "Atencion" in result["oficina"]
        assert "madrid" in result["direccion"].lower() or "Madrid" in result["direccion"]
        assert result["telefono"]
        assert result["cita_previa_url"].startswith("https://")

    def test_exact_match_barcelona_imv(self):
        result = office_lookup("barcelona", "imv")
        assert result is not None
        assert "INSS" in result["oficina"] or "Seguridad Social" in result["oficina"]
        assert result["cita_previa_url"].startswith("https://")

    def test_accent_normalization(self):
        result = office_lookup("Málaga", "empadronamiento")
        assert result is not None
        assert result != _GENERIC_FALLBACK

    def test_case_insensitive(self):
        result = office_lookup("MADRID", "empadronamiento")
        assert result is not None
        assert result != _GENERIC_FALLBACK

    def test_unknown_city_returns_generic(self):
        result = office_lookup("cuenca", "empadronamiento")
        assert result is not None
        assert result == _GENERIC_FALLBACK
        assert "060" in result["telefono"]

    def test_unknown_tramite_returns_generic(self):
        result = office_lookup("madrid", "tramite_inexistente")
        assert result is not None
        assert result == _GENERIC_FALLBACK

    def test_none_city_returns_none(self):
        result = office_lookup("", "empadronamiento")
        assert result is None

    def test_none_tramite_returns_first_available(self):
        result = office_lookup("madrid", None)
        assert result is not None
        assert result != _GENERIC_FALLBACK

    def test_palma_de_mallorca(self):
        result = office_lookup("palma de mallorca", "empadronamiento")
        assert result is not None
        assert result != _GENERIC_FALLBACK
        assert "Palma" in result["direccion"]

    def test_all_cities_have_valid_urls(self):
        for city, tramites in _OFICINAS.items():
            for tramite, info in tramites.items():
                assert info.get("cita_previa_url", "").startswith("https://"), (
                    f"{city}/{tramite} missing valid cita_previa_url"
                )
                assert info.get("sede_url", "").startswith("https://"), (
                    f"{city}/{tramite} missing valid sede_url"
                )

    def test_all_cities_have_required_fields(self):
        required = {"oficina", "direccion", "telefono", "horario", "cita_previa_url", "sede_url"}
        for city, tramites in _OFICINAS.items():
            for tramite, info in tramites.items():
                for field in required:
                    assert field in info, f"{city}/{tramite} missing field: {field}"
                    assert info[field], f"{city}/{tramite} empty field: {field}"
