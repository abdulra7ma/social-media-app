from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

from app.db.base import Base
from .session import engine


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(_element, _compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
