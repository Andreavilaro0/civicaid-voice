"""Tests for observability module: RequestContext, thread-local storage, timing."""

import threading
from src.utils.observability import RequestContext, get_context, set_context, clear_context


def test_request_context_creation():
    """RequestContext generates a valid UUID request_id."""
    ctx = RequestContext()
    assert len(ctx.request_id) == 36
    assert ctx.request_id.count("-") == 4
    assert ctx.timings == {}
    assert ctx.start_time > 0


def test_timing_tracking():
    """add_timing records stage timings correctly."""
    ctx = RequestContext()
    ctx.add_timing("cache", 50)
    ctx.add_timing("llm", 200)
    ctx.add_timing("total", 260)
    assert ctx.timings == {"cache": 50, "llm": 200, "total": 260}


def test_to_dict():
    """to_dict serializes context correctly."""
    ctx = RequestContext()
    ctx.add_timing("cache", 42)
    d = ctx.to_dict()
    assert d["request_id"] == ctx.request_id
    assert d["timings"] == {"cache": 42}
    assert "start_time" in d


def test_context_thread_local():
    """set_context/get_context use thread-local storage."""
    ctx = RequestContext()
    set_context(ctx)
    assert get_context() is ctx

    # Different thread should not see the context
    other_ctx = []

    def _check():
        other_ctx.append(get_context())

    t = threading.Thread(target=_check)
    t.start()
    t.join()

    assert other_ctx[0] is None
    clear_context()
    assert get_context() is None


def test_clear_context():
    """clear_context removes context from thread-local."""
    ctx = RequestContext()
    set_context(ctx)
    assert get_context() is ctx
    clear_context()
    assert get_context() is None


def test_observability_flag_off(monkeypatch):
    """When OBSERVABILITY_ON=false, no crash occurs."""
    monkeypatch.setenv("OBSERVABILITY_ON", "false")
    # Re-import to pick up new env
    from src.core.config import Config
    cfg = Config()
    assert cfg.OBSERVABILITY_ON is False
    # Verify get_context returns None when nothing is set
    clear_context()
    assert get_context() is None
