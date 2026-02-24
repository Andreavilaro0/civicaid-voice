"""In-memory conversation history store for multi-turn Gemini sessions.

Key = session_id (web) or phone_number (WhatsApp).
Stores last MAX_MESSAGES turns per session with TTL-based cleanup.
"""

import time
import threading
from collections import deque

_conversations: dict[str, dict] = {}  # {key: {"messages": deque, "last_activity": float}}
_conv_lock = threading.Lock()
MAX_MESSAGES = 10   # Last 10 turns (5 user + 5 model)
TTL_SECONDS = 1800  # 30 min inactivity -> delete


def add_message(session_key: str, role: str, content: str) -> None:
    """Add a message to the conversation history."""
    with _conv_lock:
        if session_key not in _conversations:
            _conversations[session_key] = {
                "messages": deque(maxlen=MAX_MESSAGES),
                "last_activity": time.time(),
            }
        _conversations[session_key]["messages"].append({
            "role": role,
            "content": content,
        })
        _conversations[session_key]["last_activity"] = time.time()


def get_history(session_key: str) -> list[dict]:
    """Get conversation history as list of {role, content} dicts."""
    with _conv_lock:
        entry = _conversations.get(session_key)
        if not entry:
            return []
        entry["last_activity"] = time.time()
        return list(entry["messages"])


def clear_history(session_key: str) -> None:
    """Clear conversation history for a session."""
    with _conv_lock:
        _conversations.pop(session_key, None)


def touch_session(session_key: str) -> None:
    """Update last_activity timestamp without adding a message."""
    with _conv_lock:
        entry = _conversations.get(session_key)
        if entry:
            entry["last_activity"] = time.time()


def _cleanup_stale() -> None:
    """Remove sessions that have been inactive for longer than TTL_SECONDS."""
    while True:
        time.sleep(300)  # Run every 5 minutes
        now = time.time()
        with _conv_lock:
            stale_keys = [
                k for k, v in _conversations.items()
                if now - v["last_activity"] > TTL_SECONDS
            ]
            for k in stale_keys:
                del _conversations[k]


def start_cleanup_thread() -> None:
    """Start background thread that periodically cleans stale sessions."""
    t = threading.Thread(target=_cleanup_stale, daemon=True)
    t.start()
