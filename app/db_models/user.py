from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    fullname = Column(String)
    email = Column(String)
    location = Column(String)
    company = Column(String)

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, user_id: int
    ) -> Optional[UserModel]:
        return (
            await session.execute(select(cls).where(cls.id == user_id))
        ).scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        username: str,
        password: str,
        email: str,
        fullname: str = None,
        company: str = None,
        location: str = None,
    ) -> UserModel:
        user = UserModel(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            company=company,
            location=location,
        )
        session.add(user)
        await session.flush()

        # To fetch user
        new = await cls.read_by_id(session, user.id)
        if not new:
            raise RuntimeError()
        return new

    async def update(
        self, session: AsyncSession, username: int, password: str
    ) -> None:
        self.username = username
        self.password = password
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, user: UserModel) -> None:
        await session.delete(user)
        await session.flush()
