"""Structured JSON logger with tagged prefixes for each pipeline stage."""

import json
import logging


class JSONFormatter(logging.Formatter):
    """Emit each log record as a single JSON line for easy parsing."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Attach structured extras if the caller passed them
        if hasattr(record, "json_fields"):
            entry.update(record.json_fields)
        return json.dumps(entry, ensure_ascii=False)


def _setup_logger() -> logging.Logger:
    """Configure the clara logger with JSON output to stdout."""
    _logger = logging.getLogger("clara")
    if not _logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        _logger.addHandler(handler)
        _logger.setLevel(logging.INFO)
        _logger.propagate = False
    return _logger


logger = _setup_logger()


def _log_json(level: int, tag: str, message: str, **fields) -> None:
    """Emit a log line with structured JSON fields attached."""
    record = logger.makeRecord(
        logger.name, level, "(logger)", 0, f"[{tag}] {message}", (), None,
    )
    record.json_fields = {"tag": tag, **fields}  # type: ignore[attr-defined]
    logger.handle(record)


def log_ack(from_number: str, input_type: str) -> None:
    _log_json(logging.INFO, "ACK", f"from={from_number} type={input_type}",
              from_number=from_number, input_type=input_type)


def log_cache(hit: bool, entry_id: str | None = None, ms: int = 0) -> None:
    if hit:
        _log_json(logging.INFO, "CACHE", f"HIT id={entry_id} {ms}ms",
                  hit=True, entry_id=entry_id, ms=ms)
    else:
        _log_json(logging.INFO, "CACHE", f"MISS {ms}ms",
                  hit=False, ms=ms)


def log_whisper(success: bool, duration_ms: int, text_preview: str = "") -> None:
    preview = text_preview[:60] + "..." if len(text_preview) > 60 else text_preview
    status = "OK" if success else "FAIL"
    _log_json(logging.INFO if success else logging.WARNING,
              "WHISPER", f"{status} {duration_ms}ms",
              success=success, duration_ms=duration_ms, preview=preview)


def log_llm(success: bool, duration_ms: int, source: str = "gemini") -> None:
    status = "OK" if success else "FAIL"
    _log_json(logging.INFO if success else logging.WARNING,
              "LLM", f"{status} {duration_ms}ms source={source}",
              success=success, duration_ms=duration_ms, source=source)


def log_rest(to_number: str, source: str, total_ms: int) -> None:
    _log_json(logging.INFO, "REST", f"Sent to={to_number} source={source} total={total_ms}ms",
              to_number=to_number, source=source, total_ms=total_ms)


def log_error(stage: str, error: str) -> None:
    _log_json(logging.ERROR, "ERROR", f"stage={stage} error={error}",
              stage=stage, error=error)


def log_observability(ctx) -> None:
    _log_json(logging.INFO, "OBS",
              f"request_id={ctx.request_id} timings={ctx.timings}",
              request_id=ctx.request_id, timings=ctx.timings)
