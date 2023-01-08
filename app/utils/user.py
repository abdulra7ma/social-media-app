from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import JWTBearer
from app.db.session import get_session
from app.selectors.user import get_user_by_id
from app.utils.jwt import decode_token


async def get_current_user(
    token: str = Depends(JWTBearer()),
    session: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    async with session.begin() as session:
        user = await get_user_by_id(user_id, session=session)

    if user is None:
        raise credentials_exception

    return user
