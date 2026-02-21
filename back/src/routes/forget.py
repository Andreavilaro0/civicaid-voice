"""POST /forget — admin endpoint to delete a user's memory."""

from flask import Blueprint, request, jsonify
from src.core.config import config
from src.core.memory.user_hash import derive_user_id
from src.core.memory.store import get_store

forget_bp = Blueprint("forget", __name__)


@forget_bp.route("/forget", methods=["POST"])
def forget_user():
    """Force-forget a user. Requires FORGET_TOKEN in Authorization header."""
    if not config.FORGET_TOKEN:
        return jsonify({"error": "forget not configured"}), 403

    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {config.FORGET_TOKEN}":
        return jsonify({"error": "unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    phone = data.get("phone", "")
    if not phone:
        return jsonify({"error": "phone required"}), 400

    user_id = derive_user_id(phone, config.MEMORY_SECRET_SALT)
    store = get_store(config.MEMORY_BACKEND)
    store.forget(user_id)

    return jsonify({"status": "forgotten", "user_id_hash": user_id[:12]})
