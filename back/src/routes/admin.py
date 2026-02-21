"""Admin endpoints for RAG metrics, staleness, and satisfaction — protected by ADMIN_TOKEN."""

from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from src.core.config import config

admin_bp = Blueprint("admin", __name__)

# Module-level dicts for storing last ingestion / drift results
_last_ingestion = {"last_run": None, "stats": None}
_last_drift = {"last_run": None, "results": None}


def update_ingestion_status(stats: dict):
    """Called by ingestion scripts to record the last run result."""
    _last_ingestion["last_run"] = datetime.now(timezone.utc).isoformat()
    _last_ingestion["stats"] = stats


def update_drift_status(results: dict):
    """Called by drift scripts to record the last check result."""
    _last_drift["last_run"] = datetime.now(timezone.utc).isoformat()
    _last_drift["results"] = results


def _check_admin_token():
    """Verify ADMIN_TOKEN header. Returns error response or None if OK."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not config.ADMIN_TOKEN or token != config.ADMIN_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    return None


@admin_bp.route("/admin/rag-metrics", methods=["GET"])
def rag_metrics_endpoint():
    """Return RAG metrics as JSON."""
    auth_error = _check_admin_token()
    if auth_error:
        return auth_error
    from src.utils.rag_metrics import rag_metrics
    return jsonify(rag_metrics.to_dict())


@admin_bp.route("/admin/staleness", methods=["GET"])
def staleness_endpoint():
    """Return stale procedures.

    Requires RAG_ENABLED + RAG_DB_URL.
    Uses store.get_stale_procedures() if available, falls back to empty.
    """
    auth_error = _check_admin_token()
    if auth_error:
        return auth_error
    try:
        from src.core.rag.store import PGVectorStore
        store = PGVectorStore()
        threshold = request.args.get("days", config.RAG_STALENESS_THRESHOLD_DAYS, type=int)
        stale = store.get_stale_procedures(threshold)
        return jsonify({"stale_procedures": stale, "threshold_days": threshold})
    except Exception as e:
        return jsonify({
            "stale_procedures": [],
            "threshold_days": config.RAG_STALENESS_THRESHOLD_DAYS,
            "note": "Store not available",
            "error": str(e),
        })


@admin_bp.route("/admin/satisfaction", methods=["GET"])
def satisfaction_endpoint():
    """Return satisfaction metrics."""
    auth_error = _check_admin_token()
    if auth_error:
        return auth_error
    from src.utils.rag_metrics import rag_metrics
    total = rag_metrics.satisfaction_total
    pos = rag_metrics.satisfaction_positive
    return jsonify({
        "total": total,
        "positive": pos,
        "negative": rag_metrics.satisfaction_negative,
        "rate": round(pos / total, 2) if total > 0 else 0.0,
    })


@admin_bp.route("/admin/ingestion-status", methods=["GET"])
def ingestion_status_endpoint():
    """Return last ingestion result."""
    auth_error = _check_admin_token()
    if auth_error:
        return auth_error
    data = dict(_last_ingestion)
    if data["last_run"] is None:
        data["note"] = "No ingestion has been run yet"
    return jsonify(data)


@admin_bp.route("/admin/drift-status", methods=["GET"])
def drift_status_endpoint():
    """Return last drift check result."""
    auth_error = _check_admin_token()
    if auth_error:
        return auth_error
    data = dict(_last_drift)
    if data["last_run"] is None:
        data["note"] = "No drift check has been run yet"
    return jsonify(data)


@admin_bp.route("/admin/cache-stats", methods=["GET"])
def cache_stats_endpoint():
    """Return cache stats from FallbackRetriever's cache."""
    auth_error = _check_admin_token()
    if auth_error:
        return auth_error
    try:
        from src.core.retriever import FallbackRetriever
        # Try to get the cache from an existing FallbackRetriever instance
        # Build a temporary one to access cache stats
        retriever = FallbackRetriever()
        if retriever.cache:
            return jsonify(retriever.cache.stats())
        return jsonify({"note": "Cache not enabled (RAG_CACHE_ENABLED=false)"})
    except Exception as e:
        return jsonify({
            "note": "Cache not available",
            "error": str(e),
        })
