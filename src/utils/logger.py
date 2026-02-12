"""Structured logger with tagged prefixes for each pipeline stage."""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("clara")


def log_ack(from_number: str, input_type: str) -> None:
    logger.info("[ACK] from=%s type=%s", from_number, input_type)


def log_cache(hit: bool, entry_id: str | None = None, ms: int = 0) -> None:
    if hit:
        logger.info("[CACHE] HIT id=%s %dms", entry_id, ms)
    else:
        logger.info("[CACHE] MISS %dms", ms)


def log_whisper(success: bool, duration_ms: int, text_preview: str = "") -> None:
    preview = text_preview[:60] + "..." if len(text_preview) > 60 else text_preview
    if success:
        logger.info('[WHISPER] OK %dms "%s"', duration_ms, preview)
    else:
        logger.warning("[WHISPER] FAIL %dms", duration_ms)


def log_llm(success: bool, duration_ms: int, source: str = "gemini") -> None:
    if success:
        logger.info("[LLM] OK %dms source=%s", duration_ms, source)
    else:
        logger.warning("[LLM] FAIL %dms source=%s", duration_ms, source)


def log_rest(to_number: str, source: str, total_ms: int) -> None:
    logger.info("[REST] Sent to=%s source=%s total=%dms", to_number, source, total_ms)


def log_error(stage: str, error: str) -> None:
    logger.error("[ERROR] stage=%s error=%s", stage, error)


def log_observability(ctx) -> None:
    logger.info("[OBS] request_id=%s timings=%s", ctx.request_id, ctx.timings)
