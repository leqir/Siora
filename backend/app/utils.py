from __future__ import annotations
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from .config import get_settings

_signer: TimestampSigner | None = None


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
