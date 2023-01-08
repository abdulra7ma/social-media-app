from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import SQLAlchemyError
from .redis import RedisConnection

from app.core.config import settings

async_engine = create_async_engine(
    settings.DB_URI,
    pool_pre_ping=True,
    echo=settings.ECHO_SQL_STATEMENTS,
    future=True,
)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        pass
