from __future__ import annotations, annotations

from typing import Optional, AsyncIterator

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from app.db.base_class import Base


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(String)

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, post_id: int
    ) -> Optional[PostModel]:
        post = (
            await session.execute(select(cls).where(cls.id == post_id))
        ).first()

        return None if not post else post.PostModel

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[PostModel]:
        stream = await session.stream(select(cls).order_by(cls.id))
        async for row in stream:
            yield row.PostModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        user_id: int,
        content: str,
    ) -> PostModel:
        post = PostModel(user_id=user_id, content=content)
        session.add(post)
        await session.flush()

        # To fetch user
        new = await cls.read_by_id(session, post.id)

        if not new:
            raise RuntimeError()

        return new

    async def update(
        self, session: AsyncSession, user_id: int, content: str
    ) -> None:
        self.user_id = user_id
        self.content = content
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, post: PostModel) -> None:
        await session.delete(post)
        await session.flush()


class LikeModel(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    user_id = Column(Integer)

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, like_id: int
    ) -> Optional[LikeModel]:
        like = (
            await session.execute(select(cls).where(cls.id == like_id))
        ).first()

        return None if not like else like.LikeModel

    @classmethod
    async def read_all(
        cls, session: AsyncSession, post_id: int
    ) -> AsyncIterator[LikeModel]:
        stream = await session.stream(
            select(cls).where(cls.post_id == post_id)
        )

        async for row in stream:
            yield row.LikeModel

    @staticmethod
    async def count_likes_for_post(session: AsyncSession, post_id: int):
        query = (
            select([LikeModel.post_id, func.count(LikeModel.id)])
            .where(LikeModel.post_id == post_id)
            .group_by(LikeModel.post_id)
        )
        return await session.execute(query)

    @classmethod
    async def existing_like(
        cls, session: AsyncSession, post_id: int, user_id: int
    ):
        query = select(cls).where(
            cls.post_id == post_id, cls.user_id == user_id
        )
        like = (await session.execute(query)).first()
        return None if not like else like.LikeModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        user_id: int,
        post_id: int,
    ) -> LikeModel:
        like = LikeModel(user_id=user_id, post_id=post_id)
        session.add(like)
        await session.flush()

        # To fetch user
        new = await cls.read_by_id(session, like.id)

        if not new:
            raise RuntimeError()

        return new

    @classmethod
    async def delete(cls, session: AsyncSession, like: LikeModel) -> None:
        await session.delete(like)
        await session.flush()


class DislikeModel(Base):
    __tablename__ = "dislikes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    user_id = Column(Integer)

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, dislike_id: int
    ) -> Optional[DislikeModel]:
        dislike = (
            await session.execute(select(cls).where(cls.id == dislike_id))
        ).first()

        return None if not dislike else dislike.DislikeModel

    @staticmethod
    async def count_dislikes_for_post(session: AsyncSession, post_id: int):
        query = (
            select([DislikeModel.post_id, func.count(DislikeModel.id)])
            .where(DislikeModel.post_id == post_id)
            .group_by(DislikeModel.post_id)
        )
        return await session.execute(query)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        user_id: int,
        post_id: int,
    ) -> DislikeModel:
        dislike = DislikeModel(user_id=user_id, post_id=post_id)
        session.add(dislike)
        await session.flush()

        new = await cls.read_by_id(session, dislike.id)

        if not new:
            raise RuntimeError()

        return new

    @classmethod
    async def delete(
        cls, session: AsyncSession, dislike: DislikeModel
    ) -> None:
        # await session.delete(select(cls).where(cls.id == dislike.id))
        await session.delete(dislike)
        await session.flush()

    @classmethod
    async def existing_dislike(
        cls, session: AsyncSession, post_id: int, user_id: int
    ):
        query = select(cls).where(
            cls.post_id == post_id, cls.user_id == user_id
        )
        dislike = (await session.execute(query)).first()
        return None if not dislike else dislike.DislikeModel
