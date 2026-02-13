"""Decorator to measure and log skill execution time, feeding into RequestContext."""

import time
import functools
import logging

logger = logging.getLogger("clara")


def timed(skill_name: str):
    """Decorator that logs execution time and records it in RequestContext."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_ms = int((time.time() - start) * 1000)
                logger.debug("[TIMING] %s OK %dms", skill_name, elapsed_ms)
                _record_timing(skill_name, elapsed_ms)
                return result
            except Exception:
                elapsed_ms = int((time.time() - start) * 1000)
                logger.debug("[TIMING] %s FAIL %dms", skill_name, elapsed_ms)
                _record_timing(skill_name, elapsed_ms)
                raise
        return wrapper
    return decorator


def _record_timing(skill_name: str, elapsed_ms: int) -> None:
    """Push skill timing into the current RequestContext if available."""
    try:
        from src.utils.observability import get_context
        ctx = get_context()
        if ctx:
            ctx.add_timing(skill_name, elapsed_ms)
    except Exception:
        pass  # observability is optional, never break the pipeline
