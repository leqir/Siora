from __future__ import annotations
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from .config import get_settings
import os


SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

signer = TimestampSigner(SECRET_KEY)
def signer() -> TimestampSigner:
    global _signer
    if _signer is None:
        _signer = TimestampSigner(get_settings().secret_key)
    return _signer


def sign_user_id(user_id: str) -> str:
    return signer().sign(user_id).decode()


def unsign_user_id(value: str, max_age_seconds: int = 60 * 60 * 24 * 30) -> str | None:
    try:
        return signer().unsign(value, max_age=max_age_seconds).decode()
    except (BadSignature, SignatureExpired):
        return None
def sign_user_id(user_id: str) -> str:
    """Sign a user ID using a timestamped signature."""
    return signer.sign(user_id.encode()).decode()

def verify_user_id(token: str) -> str:
    """Verify the signed user ID and return the original ID if valid."""
    try:
        value = signer.unsign(token, max_age=60 * 60 * 24 * 30)  # 30 days
        return value.decode()
    except (BadSignature, SignatureExpired):
        raise ValueError("Invalid or expired session token")
