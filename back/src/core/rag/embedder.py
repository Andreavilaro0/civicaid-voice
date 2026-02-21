"""Gemini embedding wrapper with rate limiting and retry."""

import logging
import os
import time
from collections import deque

from google import genai

logger = logging.getLogger(__name__)

_MODEL = os.getenv("RAG_EMBEDDING_MODEL", "models/gemini-embedding-001")
_EMBEDDING_DIM = 768
_BATCH_SIZE = 10
_MAX_REQUESTS_PER_MINUTE = 100
_MAX_RETRIES = 3
_RETRY_DELAYS = (1, 2, 4)  # exponential backoff in seconds

# Module-level state for rate limiting
_request_timestamps: deque[float] = deque()
_client: genai.Client | None = None


def _ensure_configured() -> genai.Client:
    """Create the Gemini client once using GEMINI_API_KEY."""
    global _client
    if _client is not None:
        return _client
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")
    _client = genai.Client(api_key=api_key)
    return _client


def _rate_limit() -> None:
    """Sleep if we've exceeded the per-minute request limit."""
    now = time.monotonic()

    # Discard timestamps older than 60 seconds
    while _request_timestamps and _request_timestamps[0] < now - 60:
        _request_timestamps.popleft()

    if len(_request_timestamps) >= _MAX_REQUESTS_PER_MINUTE:
        sleep_time = 60 - (now - _request_timestamps[0])
        if sleep_time > 0:
            logger.info("Rate limit reached, sleeping %.1fs", sleep_time)
            time.sleep(sleep_time)

    _request_timestamps.append(time.monotonic())


def embed_text(text: str) -> list[float]:
    """Embed a single text, returns 768-dim vector.

    Args:
        text: Input text to embed.

    Returns:
        List of 768 floats representing the embedding vector.

    Raises:
        RuntimeError: If embedding fails after retries or returns wrong dimension.
    """
    client = _ensure_configured()

    last_error = None
    for attempt in range(_MAX_RETRIES):
        try:
            _rate_limit()
            result = client.models.embed_content(
                model=_MODEL,
                contents=text,
                config={"output_dimensionality": _EMBEDDING_DIM},
            )
            embedding = result.embeddings[0].values

            if len(embedding) != _EMBEDDING_DIM:
                raise RuntimeError(
                    f"Expected {_EMBEDDING_DIM}-dim embedding, got {len(embedding)}"
                )

            return embedding

        except Exception as exc:
            last_error = exc
            if attempt < _MAX_RETRIES - 1:
                delay = _RETRY_DELAYS[attempt]
                logger.warning(
                    "Embedding attempt %d failed (%s), retrying in %ds",
                    attempt + 1, exc, delay,
                )
                time.sleep(delay)

    raise RuntimeError(f"Embedding failed after {_MAX_RETRIES} attempts: {last_error}")


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts with rate limiting.

    Processes texts in batches of 10 to respect API rate limits.

    Args:
        texts: List of input texts to embed.

    Returns:
        List of embedding vectors, one per input text.

    Raises:
        RuntimeError: If any embedding fails after retries.
    """
    if not texts:
        return []

    embeddings: list[list[float]] = []

    for i in range(0, len(texts), _BATCH_SIZE):
        batch = texts[i : i + _BATCH_SIZE]
        logger.info(
            "Embedding batch %d-%d of %d texts",
            i + 1, min(i + _BATCH_SIZE, len(texts)), len(texts),
        )
        for text in batch:
            embedding = embed_text(text)
            embeddings.append(embedding)

    return embeddings
