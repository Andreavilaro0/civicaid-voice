"""Reranking module — Gemini-based and heuristic reranking for RAG results."""

import logging
import os
import re
import time
from collections import deque

logger = logging.getLogger(__name__)

# Rate limiting shared with embedder (100 req/min budget)
_MAX_REQUESTS_PER_MINUTE = 100
_request_timestamps: deque[float] = deque()

# Section keyword mappings for heuristic reranker
_SECTION_KEYWORDS: dict[str, list[str]] = {
    "requisitos": ["requisitos", "necesito", "quien puede"],
    "documentos_necesarios": ["documentos", "papeles", "que necesito llevar"],
    "como_solicitar": ["como", "solicitar", "pedir", "tramitar"],
    "plazos": ["plazo", "cuando", "fecha"],
    "donde_solicitar": ["donde", "oficina", "sede"],
    "descripcion": ["que es", "descripcion", "informacion"],
}


def _rate_limit() -> None:
    """Sleep if we've exceeded the per-minute request limit."""
    now = time.monotonic()

    while _request_timestamps and _request_timestamps[0] < now - 60:
        _request_timestamps.popleft()

    if len(_request_timestamps) >= _MAX_REQUESTS_PER_MINUTE:
        sleep_time = 60 - (now - _request_timestamps[0])
        if sleep_time > 0:
            logger.info("Reranker rate limit reached, sleeping %.1fs", sleep_time)
            time.sleep(sleep_time)

    _request_timestamps.append(time.monotonic())


def rerank(
    query: str,
    results: list[dict],
    strategy: str = "gemini",
) -> list[dict]:
    """Rerank RAG results using the specified strategy.

    Args:
        query: The user query string.
        results: List of result dicts from hybrid search.
        strategy: One of "none", "gemini", or "heuristic".

    Returns:
        Same result dicts with added "rerank_score" key, sorted descending.
    """
    if not results:
        return results

    if strategy == "none":
        return results

    if strategy == "heuristic":
        return _heuristic_rerank(query, results)

    # Default: gemini with heuristic fallback
    try:
        return _gemini_rerank(query, results)
    except Exception as exc:
        logger.warning(
            "Gemini rerank failed (%s), falling back to heuristic", exc
        )
        return _heuristic_rerank(query, results)


def _gemini_rerank(query: str, results: list[dict]) -> list[dict]:
    """Score each result using Gemini Flash for relevance.

    Calls Gemini once per result to get a 0-10 relevance score.
    Falls back to heuristic scoring for individual results where
    the Gemini response is non-numeric.

    Args:
        query: The user query string.
        results: List of result dicts.

    Returns:
        Results with rerank_score added, sorted by rerank_score DESC.
    """
    from google import genai

    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    # Pre-compute heuristic scores as fallback for individual failures
    heuristic_scores = _compute_heuristic_scores(query, results)

    for i, result in enumerate(results):
        _rate_limit()

        prompt = (
            "Rate the relevance of the following passage to the query "
            "on a scale of 0-10. Respond with ONLY a single integer number.\n\n"
            f"Query: {query}\n\n"
            f"Passage: {result['content']}\n\n"
            "Relevance score:"
        )

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash", contents=prompt
            )
            score_text = response.text.strip()
            match = re.search(r"\d+", score_text)
            if match:
                gemini_score = min(int(match.group()), 10)
                result["rerank_score"] = gemini_score / 10.0
            else:
                logger.warning(
                    "Non-numeric Gemini response for chunk %s: '%s', using heuristic",
                    result.get("chunk_id", "?"),
                    score_text,
                )
                result["rerank_score"] = heuristic_scores[i]
        except Exception as exc:
            logger.warning(
                "Gemini scoring failed for chunk %s (%s), using heuristic",
                result.get("chunk_id", "?"),
                exc,
            )
            result["rerank_score"] = heuristic_scores[i]

    results.sort(key=lambda r: r["rerank_score"], reverse=True)
    return results


def _heuristic_rerank(query: str, results: list[dict]) -> list[dict]:
    """Rerank using keyword and section matching heuristics.

    Scoring (0-10 scale, normalized to 0-1):
        - Section match: 0-3 points
        - Keyword overlap: 0-3 points
        - Original score pass-through: 0-4 points

    Args:
        query: The user query string.
        results: List of result dicts.

    Returns:
        Results with rerank_score added, sorted by rerank_score DESC.
    """
    scores = _compute_heuristic_scores(query, results)
    for result, score in zip(results, scores):
        result["rerank_score"] = score

    results.sort(key=lambda r: r["rerank_score"], reverse=True)
    return results


def _compute_heuristic_scores(query: str, results: list[dict]) -> list[float]:
    """Compute heuristic scores for a list of results.

    Returns a list of float scores (0-1 range) aligned with results.
    """
    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 2]

    scores: list[float] = []

    for result in results:
        # (a) Section match: 0-3 points
        section_score = 0.0
        section_name = (result.get("section_name") or "").lower()
        for target_section, keywords in _SECTION_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords):
                if target_section in section_name:
                    section_score = 3.0
                    break

        # (b) Keyword overlap: 0-3 points
        keyword_score = 0.0
        if query_words:
            content_lower = (result.get("content") or "").lower()
            matches = sum(1 for w in query_words if w in content_lower)
            keyword_score = (matches / len(query_words)) * 3.0

        # (c) Original score pass-through: 0-4 points
        original_score = result.get("score", 0.0)
        original_bonus = min(original_score, 1.0) * 4.0

        raw_score = section_score + keyword_score + original_bonus
        scores.append(min(raw_score, 10.0) / 10.0)

    return scores
