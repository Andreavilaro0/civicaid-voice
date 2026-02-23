"""Tests for domain_validator — allowlist/blocklist enforcement."""

import pytest

from src.core.domain_validator import (
    DomainValidator,
    extract_urls,
    is_domain_approved,
    reset_validator,
)


@pytest.fixture(autouse=True)
def _reset():
    """Reset singleton between tests."""
    reset_validator()
    yield
    reset_validator()


# ------------------------------------------------------------------ #
# Test: 8 tramites fuente_url → all approved
# ------------------------------------------------------------------ #
class TestTramitesURLsApproved:
    """All 8 tramites fuente_url must pass validation."""

    @pytest.mark.parametrize(
        "tramite,url",
        [
            ("imv", "https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-8d06-4645-bde7-05374ee42ac7"),
            ("empadronamiento", "https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Estadistica/Padron-Municipal/"),
            ("tarjeta_sanitaria", "https://www.comunidad.madrid/servicios/salud/tarjeta-sanitaria"),
            ("prestacion_desempleo", "https://www.sepe.es/HomeSepe/prestaciones-desempleo/prestacion-contributiva.html"),
            ("nie_tie", "https://www.inclusion.gob.es/web/migraciones/informacion-util/tramites"),
            ("ayuda_alquiler", "https://www.mivau.gob.es/vivienda"),
            ("certificado_discapacidad", "https://www.comunidad.madrid/servicios/servicios-sociales/discapacidad"),
            ("justicia_gratuita", "https://www.mjusticia.gob.es/es/ciudadania/tramites/asistencia-juridica-gratuita"),
        ],
    )
    def test_tramite_url_approved(self, tramite, url):
        assert is_domain_approved(url), f"{tramite} URL should be approved: {url}"


# ------------------------------------------------------------------ #
# Test: 25 blocked domains → all rejected
# ------------------------------------------------------------------ #
class TestBlockedDomains:
    """All domains in blocklist.yaml must be rejected."""

    BLOCKED = [
        "loentiendo.com",
        "tramitalia.com",
        "emigralia.es",
        "parainmigrantes.info",
        "rankia.com",
        "asesorias.com",
        "supercontable.com",
        "forocoches.com",
        "burbuja.info",
        "reddit.com",
        "quora.com",
        "twitter.com",
        "facebook.com",
        "instagram.com",
        "tiktok.com",
        "es.wikipedia.org",
        "elpais.com",
        "elmundo.es",
        "20minutos.es",
        "tramitesygestiones.com",
        "extranjeria.info",
        "noticias.juridicas.com",
        "vlex.es",
    ]

    @pytest.mark.parametrize("domain", BLOCKED)
    def test_blocked_domain(self, domain):
        url = f"https://{domain}/some/page"
        assert not is_domain_approved(url), f"Should be blocked: {domain}"


# ------------------------------------------------------------------ #
# Test: Wildcard patterns (*.wordpress.com etc.) → rejected
# ------------------------------------------------------------------ #
class TestWildcardPatterns:
    """Wildcard blocked patterns must reject matching domains."""

    @pytest.mark.parametrize(
        "domain",
        [
            "myblog.wordpress.com",
            "tramites-espana.blogspot.com",
            "guia-imv.medium.com",
            "info-nie.notion.site",
        ],
    )
    def test_wildcard_blocked(self, domain):
        url = f"https://{domain}/article"
        assert not is_domain_approved(url), f"Wildcard should block: {domain}"


# ------------------------------------------------------------------ #
# Test: *.gob.es auto-allow → approved
# ------------------------------------------------------------------ #
class TestGobEsAutoAllow:
    """Any *.gob.es subdomain should be auto-approved."""

    @pytest.mark.parametrize(
        "domain",
        [
            "inclusion.gob.es",
            "sede.seg-social.gob.es",
            "mivau.gob.es",
            "newministry.gob.es",
            "deep.sub.domain.gob.es",
        ],
    )
    def test_gob_es_approved(self, domain):
        url = f"https://{domain}/page"
        assert is_domain_approved(url), f"*.gob.es should be auto-allowed: {domain}"


# ------------------------------------------------------------------ #
# Test: Unknown domain → rejected (default-reject policy)
# ------------------------------------------------------------------ #
class TestDefaultReject:
    """Domains not in allowlist and not *.gob.es should be rejected."""

    @pytest.mark.parametrize(
        "domain",
        [
            "random-site.com",
            "some-gestoria.es",
            "ayuda-nie.info",
            "tramites.org",
            "example.com",
        ],
    )
    def test_unknown_rejected(self, domain):
        url = f"https://{domain}/info"
        assert not is_domain_approved(url), f"Unknown domain should be rejected: {domain}"


# ------------------------------------------------------------------ #
# Test: Allowlist tiers (explicit domains)
# ------------------------------------------------------------------ #
class TestAllowlistTiers:
    """Explicitly listed domains from all tiers should be approved."""

    @pytest.mark.parametrize(
        "domain",
        [
            # Tier 1 AGE
            "administracion.gob.es",
            "boe.es",
            "seg-social.es",
            "sepe.es",
            "policia.es",
            "060.es",
            "iprem.es",
            # Tier 2 CCAA
            "comunidad.madrid",
            "juntadeandalucia.es",
            "euskadi.eus",
            "xunta.gal",
            # Tier 3 Municipal
            "madrid.es",
            "barcelona.cat",
            "sevilla.org",
        ],
    )
    def test_allowlist_approved(self, domain):
        url = f"https://{domain}/tramite"
        assert is_domain_approved(url), f"Allowlisted domain should be approved: {domain}"


# ------------------------------------------------------------------ #
# Test: Subdomain inheritance
# ------------------------------------------------------------------ #
class TestSubdomainInheritance:
    """Subdomains of allowed domains should be approved."""

    @pytest.mark.parametrize(
        "subdomain",
        [
            "sede.madrid.es",
            "sede.seg-social.gob.es",
            "ajuntament.barcelona.cat",
            "sede.sevilla.org",
        ],
    )
    def test_subdomain_approved(self, subdomain):
        url = f"https://{subdomain}/page"
        assert is_domain_approved(url), f"Subdomain should inherit approval: {subdomain}"


# ------------------------------------------------------------------ #
# Test: extract_urls helper
# ------------------------------------------------------------------ #
class TestExtractUrls:
    def test_extracts_multiple(self):
        text = "Visita https://www.seg-social.es/imv y también http://sepe.es/paro"
        urls = extract_urls(text)
        assert len(urls) == 2
        assert "https://www.seg-social.es/imv" in urls
        assert "http://sepe.es/paro" in urls

    def test_no_urls(self):
        assert extract_urls("Sin enlaces aqui") == []

    def test_url_with_query(self):
        text = "Ve a https://sede.madrid.es/portal?id=123&lang=es para más info"
        urls = extract_urls(text)
        assert len(urls) == 1
        assert "id=123" in urls[0]


# ------------------------------------------------------------------ #
# Test: Empty / invalid inputs
# ------------------------------------------------------------------ #
class TestEdgeCases:
    def test_empty_url(self):
        assert not is_domain_approved("")

    def test_none_like(self):
        assert not is_domain_approved("")

    def test_malformed_url(self):
        assert not is_domain_approved("not a url at all")

    def test_www_prefix_stripped(self):
        assert is_domain_approved("https://www.sepe.es/HomeSepe")

    def test_url_without_scheme(self):
        assert is_domain_approved("seg-social.es/wps/portal/something")
