# Observability Layer

## Overview

Clara includes a lightweight observability layer that assigns a unique `request_id` to every incoming request, tracks stage timings through the pipeline, and logs structured observability data. An optional OpenTelemetry (OTEL) export stub is included for future integration.

## Request ID Flow

```
Twilio POST /webhook
    |
    v
Flask before_request hook
    -> Creates RequestContext(request_id=uuid4)
    -> Stores in threading.local()
    |
    v
webhook() handler
    -> Reads ctx from thread-local
    -> Sets msg.request_id = ctx.request_id
    |
    v
pipeline.process(msg) [background thread]
    -> Reads ctx via get_context()
    -> Records stage timings via ctx.add_timing()
    -> Logs [OBS] request_id=... timings=...
    |
    v
Flask after_request hook
    -> Records http_total timing
    -> Logs final [OBS] line
    -> Clears thread-local context
```

## Stage Timings

The pipeline records the following timing stages (in milliseconds):

| Stage | Where | Description |
|-------|-------|-------------|
| `cache` | pipeline.py | Time to cache lookup + response |
| `total` | pipeline.py | Total pipeline processing time |
| `http_total` | after_request | Total HTTP request-response time |

## Feature Flags

| Flag | Env Var | Default | Effect |
|------|---------|---------|--------|
| OBSERVABILITY_ON | `OBSERVABILITY_ON` | `true` | Enables request_id generation, timing tracking, and [OBS] log lines |
| OTEL_ENDPOINT | `OTEL_ENDPOINT` | `""` (empty) | When set, logs a TODO stub for OTEL export |

## Configuration

```bash
# Enable observability (default)
export OBSERVABILITY_ON=true

# Disable observability
export OBSERVABILITY_ON=false

# Enable OTEL export stub
export OTEL_ENDPOINT=http://localhost:4317
```

## Log Format

Observability log lines use the `[OBS]` prefix:

```
12:34:56 INFO [OBS] request_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890 timings={'cache': 12, 'total': 15}
```

## Module: src/utils/observability.py

### Classes

- **RequestContext**: Dataclass with `request_id`, `start_time`, `timings` dict, `add_timing()`, `to_dict()`

### Functions

- **set_context(ctx)**: Store RequestContext in thread-local storage
- **get_context()**: Retrieve RequestContext (returns None if not set)
- **clear_context()**: Remove context from thread-local
- **init_app(app)**: Register Flask before/after request hooks

## Tests

Tests are in `tests/unit/test_observability.py`:

- `test_request_context_creation` -- UUID generation and defaults
- `test_timing_tracking` -- add_timing records correctly
- `test_to_dict` -- serialization
- `test_context_thread_local` -- thread isolation
- `test_clear_context` -- cleanup
- `test_observability_flag_off` -- no crash when disabled

## Future: OpenTelemetry Integration

When `OTEL_ENDPOINT` is set, the system currently logs a stub message. To implement full OTEL export:

1. Install `opentelemetry-sdk` and `opentelemetry-exporter-otlp`
2. Replace the stub in `observability.py` `_obs_after` with actual span creation
3. Map `RequestContext.timings` to OTEL span attributes
4. Export to the configured `OTEL_ENDPOINT`
