"""Decorator to measure and log skill execution time."""

import time
import functools
import logging

logger = logging.getLogger("clara")


def timed(skill_name: str):
    """Decorator that logs execution time of a skill function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_ms = int((time.time() - start) * 1000)
                logger.debug("[TIMING] %s OK %dms", skill_name, elapsed_ms)
                return result
            except Exception:
                elapsed_ms = int((time.time() - start) * 1000)
                logger.debug("[TIMING] %s FAIL %dms", skill_name, elapsed_ms)
                raise
        return wrapper
    return decorator
