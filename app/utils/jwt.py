from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from app.core.config import settings
import time


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "sub": settings.ACCESS_TOKEN_JWT_SUBJECT})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM],
        )
        return (
            decoded_token if decoded_token["exp"] >= time.time() else None
        )
    except (jwt.exceptions.PyJWTError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid Token")
