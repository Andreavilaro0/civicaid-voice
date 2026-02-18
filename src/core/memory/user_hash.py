"""Derive stable, non-reversible user_id_hash from phone number."""
import hashlib


def derive_user_id(phone: str, salt: str) -> str:
    """SHA256(phone + salt) -> 64-char hex string. Never persist phone."""
    return hashlib.sha256(f"{phone}{salt}".encode("utf-8")).hexdigest()
