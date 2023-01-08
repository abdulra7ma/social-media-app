import hashlib
import hmac

from pydantic import SecretStr

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: SecretStr):
    """Verifies a password by re-hashing it and comparing the result to the hashed password."""
    return (
        hmac.new(
            settings.SECRET_KEY.encode(),
            plain_password.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        == hashed_password
    )


def get_password_hash(password: str):
    """Hashes a password using HMAC and the secret key."""
    return hmac.new(
        settings.SECRET_KEY.encode(),
        password.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
