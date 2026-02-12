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

    with patch("twilio.rest.Client") as MockClient:
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM123")

        from src.core import pipeline
        pipeline.process(msg)

        assert instance.messages.create.called
        call_kwargs = instance.messages.create.call_args
        body = call_kwargs.kwargs.get("body", call_kwargs[1].get("body", ""))
        assert "Ingreso Mínimo Vital" in body


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
