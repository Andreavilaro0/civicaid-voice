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


def log_pipeline_result(request_id: str, from_number: str, source: str,
                        total_ms: int, fallback_reason: str = "") -> None:
    import hashlib
    user_hash = hashlib.sha256(from_number.encode()).hexdigest()[:12]
    _log_json(logging.INFO, "PIPELINE_RESULT",
              f"request_id={request_id} user={user_hash} source={source} total={total_ms}ms",
              request_id=request_id, user_id_hash=user_hash,
              provider=source, latency_ms=total_ms,
              fallback_reason=fallback_reason)


def log_memory(request_id: str, user_id_hash: str, backend: str,
               hit: bool, write: bool, size_bytes: int, latency_ms: int) -> None:
    _log_json(logging.INFO, "MEMORY",
              f"request_id={request_id} user={user_id_hash[:12]} backend={backend} hit={hit} write={write}",
              request_id=request_id, user_id_hash=user_id_hash[:12],
              memory_backend=backend, memory_hit=hit,
              memory_write=write, memory_size_bytes=size_bytes,
              latency_ms=latency_ms)


def log_retrieval(source: str, cache_hit: bool, latency_ms: float, procedure_id: str = "") -> None:
    """Log a RAG retrieval event."""
    _log_json(logging.INFO, "RAG_RETRIEVAL",
              f"source={source} cache_hit={cache_hit} latency_ms={latency_ms:.1f} procedure={procedure_id}",
              source=source, cache_hit=cache_hit, latency_ms=latency_ms,
              procedure_id=procedure_id)


def log_ingestion(source_id: str, status: str, chunks: int = 0, duration_ms: int = 0) -> None:
    """Log an ingestion event."""
    _log_json(logging.INFO, "RAG_INGESTION",
              f"source={source_id} status={status} chunks={chunks} duration_ms={duration_ms}",
              source_id=source_id, status=status, chunks=chunks,
              duration_ms=duration_ms)


def log_drift(procedure_id: str, status: str, staleness_days: int = 0) -> None:
    """Log a drift check event."""
    _log_json(logging.INFO, "RAG_DRIFT",
              f"procedure={procedure_id} status={status} staleness_days={staleness_days}",
              procedure_id=procedure_id, status=status,
              staleness_days=staleness_days)


def log_satisfaction(from_number: str, feedback: str, positive: bool) -> None:
    """Log user satisfaction feedback."""
    masked = from_number[:6] + "***" if len(from_number) >= 6 else from_number + "***"
    _log_json(logging.INFO, "USER_SATISFACTION",
              f"from={masked} feedback={feedback} positive={positive}",
              from_number_masked=masked, feedback=feedback, positive=positive)
