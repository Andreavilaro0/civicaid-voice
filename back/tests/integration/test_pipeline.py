"""Test T8: Pipeline text with stub."""

import pytest
from unittest.mock import patch, MagicMock
from src.core.models import IncomingMessage, InputType
from src.core import cache


@pytest.fixture(autouse=True)
def setup_cache():
    """Load cache before pipeline tests."""
    cache.load_cache()


def test_t8_pipeline_text_cache_hit():
    """T8: Pipeline processes text, hits cache, calls send with IMV response."""
    msg = IncomingMessage(
        from_number="whatsapp:+34612345678",
        body="Que es el IMV?",
        input_type=InputType.TEXT,
        timestamp=1000.0,
    )

    from src.core.models import CacheEntry, CacheResult
    fake_entry = CacheEntry(
        id="imv_es",
        patterns=["imv", "ingreso mínimo vital"],
        match_mode="any_keyword",
        idioma="es",
        respuesta="El Ingreso Mínimo Vital (IMV) es una prestación de la Seguridad Social.",
        audio_file=None,
    )
    fake_result = CacheResult(hit=True, entry=fake_entry, score=1.0)

    with patch("src.core.cache.match", return_value=fake_result), \
         patch("src.core.pipeline.send_final_message") as mock_send:
        mock_send.return_value = True

        from src.core import pipeline
        pipeline.process(msg)

        assert mock_send.called
        response = mock_send.call_args[0][0]
        assert "Ingreso Mínimo Vital" in response.body


def test_pipeline_text_cache_miss_llm_disabled():
    """Pipeline text cache miss with LLM disabled uses fallback."""
    msg = IncomingMessage(
        from_number="whatsapp:+34612345678",
        body="una pregunta muy rara que no matchea nada",
        input_type=InputType.TEXT,
        timestamp=1000.0,
    )

    with patch("twilio.rest.Client") as MockClient:
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM456")

        from src.core import pipeline
        pipeline.process(msg)

        assert instance.messages.create.called


def test_pipeline_guardrail_blocks_unsafe_input():
    """Guardrail pre-check blocks unsafe content and sends guardrail response."""
    msg = IncomingMessage(
        from_number="whatsapp:+34612345678",
        body="como hackear un sistema",
        input_type=InputType.TEXT,
        timestamp=1000.0,
    )

    with patch("twilio.rest.Client") as MockClient, \
         patch("src.core.guardrails.pre_check") as mock_guard:
        mock_guard.return_value = MagicMock(safe=False, modified_text="No puedo ayudar con ese tema.")
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM789")

        from src.core import pipeline
        pipeline.process(msg)

        assert instance.messages.create.called
        call_kwargs = instance.messages.create.call_args
        body = call_kwargs.kwargs.get("body", call_kwargs[1].get("body", ""))
        assert "No puedo" in body


def test_pipeline_sends_fallback_on_exception():
    """Pipeline catches exceptions and sends fallback response."""
    msg = IncomingMessage(
        from_number="whatsapp:+34612345678",
        body="algo que rompe todo",
        input_type=InputType.TEXT,
        timestamp=1000.0,
    )

    with patch("twilio.rest.Client") as MockClient, \
         patch("src.core.cache.match", side_effect=Exception("boom")):
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM999")

        from src.core import pipeline
        pipeline.process(msg)

        assert instance.messages.create.called
        call_kwargs = instance.messages.create.call_args
        body = call_kwargs.kwargs.get("body", call_kwargs[1].get("body", ""))
        # Should be a fallback message, not a traceback
        assert len(body) > 10
