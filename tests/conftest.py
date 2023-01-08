import asyncio
from typing import Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import Settings, test_settings
from app.db.base import Base
from app.db.session import get_session
from app.main import app
from app.models.user import User
from app.services.user import UserService
from app.utils.password import get_password_hash

settings = Settings()


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def ac() -> Generator:
    async with AsyncClient(
        app=app, base_url="http://127.0.0.1:8000/api/v1/"
    ) as c:
        yield c

    await c.aclose()


@pytest.fixture(scope="function")
def setup_db() -> Generator:
    engine_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/"
    engine = create_engine(engine_url)
    conn = engine.connect()
    print("opened connection before test")
    conn.execute("commit")

    try:
        conn.execute(f"drop database {settings.POSTGRES_DB}")
        print("dropped database before test")
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    conn.execute("commit")

    print("created new database before test")

    conn.execute(f"create database {settings.POSTGRES_DB}")
    conn.close()

    print("closed database before test")

    yield

    conn = engine.connect()
    conn.execute("commit")

    try:
        # Terminate all sessions connected to the database
        engine.execute(
            text(
                f"SELECT pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{settings.POSTGRES_DB}';"
            )
        )
        conn.execute(text(f"DROP DATABASE {settings.POSTGRES_DB}"))
        print("dropped database after test")
    except SQLAlchemyError as e:
        print(e.code)
    finally:
        conn.close()
        print("closed connection after test")


@pytest.fixture(scope="function", autouse=True)
def setup_test_db(setup_db):
    engine = create_engine(f"{test_settings.DB_URI.replace('+asyncpg', '')}")

    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Dropped all dbs and created before session")
        yield
        Base.metadata.drop_all(engine)
        print("Dropped all dbs and created after session")


@pytest.fixture(scope="function")
async def session():
    async_engine = create_async_engine(
        f"{test_settings.DB_URI}", echo=False, poolclass=NullPool
    )

    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()

        AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
            class_=AsyncSession,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction:
                conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session

        # await async_session.rollback()
        await async_session.close()
        await conn.rollback()


@pytest.fixture(scope="function")
async def test_user(session: AsyncSession):
    user = User(
        email="test@mail.com",
        username="test",
        password=get_password_hash("password"),
    )
    return await UserService.create(user=user, session=session)
