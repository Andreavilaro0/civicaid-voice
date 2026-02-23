"""Tests for system_prompt.py — multi-language tone injection and prompt building."""

from src.core.prompts.system_prompt import build_prompt, _LANGUAGE_TONES


class TestLanguageTones:
    """All 5 supported languages have tone rules."""

    def test_all_five_languages_present(self):
        for lang in ("es", "fr", "en", "pt", "ar"):
            assert lang in _LANGUAGE_TONES

    def test_es_tone_uses_tuteo(self):
        assert "Tutea" in _LANGUAGE_TONES["es"] or "tutea" in _LANGUAGE_TONES["es"].lower()

    def test_fr_tone_uses_vouvoiement(self):
        assert "Vouvoie" in _LANGUAGE_TONES["fr"] or "vouvoie" in _LANGUAGE_TONES["fr"].lower()

    def test_pt_tone_mentions_europeu(self):
        assert "europeu" in _LANGUAGE_TONES["pt"].lower()

    def test_en_tone_mentions_you(self):
        assert "you" in _LANGUAGE_TONES["en"].lower()

    def test_ar_tone_mentions_msa(self):
        tone = _LANGUAGE_TONES["ar"].lower()
        assert "estandar" in tone or "msa" in tone

    def test_each_tone_at_least_50_chars(self):
        for lang, tone in _LANGUAGE_TONES.items():
            assert len(tone) >= 50, f"{lang} tone too short: {len(tone)} chars"


class TestBuildPrompt:
    """build_prompt injects language, context, and memory correctly."""

    def test_es_prompt_contains_es_tone(self):
        result = build_prompt(language="es")
        assert "Tutea" in result or "tutea" in result.lower()

    def test_fr_prompt_contains_fr_tone(self):
        result = build_prompt(language="fr")
        assert "Vouvoie" in result or "vouvoie" in result.lower()

    def test_en_prompt_contains_en_tone(self):
        result = build_prompt(language="en")
        # EN tone: 'Use "you" (informal but respectful)'
        assert "informal but respectful" in result

    def test_pt_prompt_contains_pt_tone(self):
        result = build_prompt(language="pt")
        assert "europeu" in result.lower()

    def test_ar_prompt_contains_ar_tone(self):
        result = build_prompt(language="ar")
        assert "estandar" in result.lower() or "MSA" in result

    def test_unknown_language_falls_back_to_es(self):
        result = build_prompt(language="xx")
        assert "Tutea" in result or "tutea" in result.lower()

    def test_language_code_injected(self):
        result = build_prompt(language="fr")
        assert "IDIOMA DE RESPUESTA: fr" in result

    def test_kb_context_injected(self):
        result = build_prompt(kb_context="Informacion sobre el IMV")
        assert "Informacion sobre el IMV" in result

    def test_default_kb_context(self):
        result = build_prompt()
        assert "No hay contexto disponible" in result

    def test_chunks_block_injected(self):
        result = build_prompt(chunks_block="[C1] chunk data here")
        assert "[C1] chunk data here" in result

    def test_memory_profile_injected(self):
        result = build_prompt(memory_profile="nombre: Maria")
        assert "<memory_profile>" in result
        assert "nombre: Maria" in result

    def test_memory_summary_injected(self):
        result = build_prompt(memory_summary="Consulto sobre NIE")
        assert "<memory_summary>" in result
        assert "Consulto sobre NIE" in result

    def test_memory_case_injected(self):
        result = build_prompt(memory_case="caso abierto: empadronamiento")
        assert "<memory_case>" in result

    def test_no_memory_blocks_when_empty(self):
        result = build_prompt()
        # When no memory is provided, the MEMORIA DEL USUARIO section should not appear.
        # Note: the tag names appear in the SEGURIDAD instructions, so we check
        # that no actual XML-wrapped memory content block is injected.
        assert "MEMORIA DEL USUARIO" not in result
        assert "<memory_profile>\n" not in result
        assert "<memory_summary>\n" not in result
        assert "<memory_case>\n" not in result

    def test_prompt_contains_evi_pattern(self):
        result = build_prompt()
        assert "E-V-I" in result or "Empatizar" in result

    def test_prompt_contains_security_section(self):
        result = build_prompt()
        assert "SEGURIDAD" in result

    def test_prompt_contains_veracidad_section(self):
        result = build_prompt()
        assert "VERACIDAD" in result

    def test_prompt_mentions_clara(self):
        result = build_prompt()
        assert "Clara" in result
