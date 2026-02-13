"""Observability: request_id tracking, stage timings, JSON structured logs."""

import json
import threading
import uuid
import time
import logging
from dataclasses import dataclass, field

logger = logging.getLogger("clara")

_local = threading.local()


@dataclass
class RequestContext:
    """Per-request observability context."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)
    timings: dict = field(default_factory=dict)

    def add_timing(self, stage: str, ms: int) -> None:
        """Record timing for a pipeline stage."""
        self.timings[stage] = ms

    def to_dict(self) -> dict:
        """Serialize context for logging/export."""
        return {
            "request_id": self.request_id,
            "start_time": self.start_time,
            "timings": self.timings,
        }


def set_context(ctx: RequestContext) -> None:
    """Store RequestContext in thread-local storage."""
    _local.ctx = ctx


def get_context() -> RequestContext | None:
    """Retrieve RequestContext from thread-local storage."""
    return getattr(_local, "ctx", None)


def clear_context() -> None:
    """Remove RequestContext from thread-local storage."""
    _local.ctx = None


def init_app(app):
    """Register Flask before/after request hooks for observability."""
    from src.core.config import config

    @app.before_request
    def _obs_before():
        if config.OBSERVABILITY_ON:
            ctx = RequestContext()
            set_context(ctx)

    @app.after_request
    def _obs_after(response):
        if config.OBSERVABILITY_ON:
            ctx = get_context()
            if ctx:
                elapsed_ms = int((time.time() - ctx.start_time) * 1000)
                ctx.add_timing("http_total", elapsed_ms)
                # Emit structured JSON summary for the request
                summary = {
                    "tag": "OBS_SUMMARY",
                    "request_id": ctx.request_id,
                    "http_status": response.status_code,
                    "http_total_ms": elapsed_ms,
                    "timings": ctx.timings,
                }
                logger.info("[OBS] %s", json.dumps(summary, ensure_ascii=False))
            clear_context()
        return response
