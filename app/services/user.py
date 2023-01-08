from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.session import get_session
from app.db_models.user import UserModel
from app.models.user import User


class UserService:
    def __init__(self, session: sessionmaker = None) -> None:
        self.async_session = session or get_session

    @staticmethod
    async def create(*, user: User, session) -> UserModel:
        new_user = await UserModel.create(session, **user.dict())
        return new_user
