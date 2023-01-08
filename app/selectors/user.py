from typing import Optional

from fastapi import Depends
from app.db.session import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db_models.user import UserModel


async def get_user_by_username(
    username: str, session: AsyncSession = None
) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.username == username)
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_user_by_id(user_id: int, session: AsyncSession = None):
    stmt = select(UserModel).where(UserModel.id == user_id)
    return (await session.execute(stmt)).scalar_one_or_none()
