"""Tests T1-T3: Cache matching."""

from src.core.models import CacheEntry, InputType
from src.core.skills.cache_match import cache_match

ENTRIES = [
    CacheEntry(id="imv_es", patterns=["imv", "ingreso minimo"], match_mode="any_keyword", idioma="es", respuesta="IMV info...", audio_file="imv_es.mp3"),
    CacheEntry(id="empadronamiento_es", patterns=["empadron", "padron"], match_mode="any_keyword", idioma="es", respuesta="Empadronamiento info...", audio_file="empadronamiento_es.mp3"),
    CacheEntry(id="ahmed_empadronamiento_fr", patterns=["inscrire", "mairie", "empadron"], match_mode="any_keyword", idioma="fr", respuesta="Empadronamiento FR...", audio_file="ahmed_fr.mp3"),
    CacheEntry(id="saludo_es", patterns=["hola", "buenos dias"], match_mode="any_keyword", idioma="es", respuesta="Hola!", audio_file=None),
    CacheEntry(id="maria_carta_vision", patterns=[], match_mode="image_demo", idioma="any", respuesta="Veo un documento...", audio_file="maria_es.mp3"),
]


def test_t1_cache_match_keyword_exact():
    """T1: Cache match with exact keyword hit."""
    result = cache_match("Que es el IMV?", "es", InputType.TEXT, ENTRIES)
    assert result.hit is True
    assert result.entry is not None
    assert result.entry.id == "imv_es"


def test_t2_cache_match_no_match():
    """T2: Cache match with no match."""
    result = cache_match("Que tiempo hace?", "es", InputType.TEXT, ENTRIES)
    assert result.hit is False


def test_t3_cache_match_image_demo():
    """T3: Cache match for image in DEMO_MODE."""
    result = cache_match("", "es", InputType.IMAGE, ENTRIES)
    assert result.hit is True
    assert result.entry is not None
    assert result.entry.id == "maria_carta_vision"


def test_cache_match_french():
    """Cache match: French keywords match French entry."""
    result = cache_match("Comment m'inscrire a la mairie?", "fr", InputType.TEXT, ENTRIES)
    assert result.hit is True
    assert result.entry.id == "ahmed_empadronamiento_fr"


def test_cache_match_language_filter():
    """Cache match: Spanish query doesn't match French entry."""
    result = cache_match("inscrire mairie", "es", InputType.TEXT, ENTRIES)
    assert result.hit is False


def test_cache_match_empty_text():
    """Cache match: Empty text returns miss."""
    result = cache_match("", "es", InputType.TEXT, ENTRIES)
    assert result.hit is False
