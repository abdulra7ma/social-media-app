from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db_models.post import PostModel


async def get_post_by_id(post_id: int, session: AsyncSession = None):
    stmt = select(PostModel).where(PostModel.id == post_id)
    return (await session.execute(stmt)).first()
