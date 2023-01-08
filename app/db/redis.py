import asyncio
import aioredis
from app.core.config import settings


class RedisConnection:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True,
        )

    def is_connected(self):
        return True if self.redis else False

    async def get(self, key):
        return await self.redis.get(key) or 0

    async def get_set(self, key):
        return await self.redis.get(key) or []

    async def set(self, key, value):
        return await self.redis.set(key, value)

    async def incr(self, key):
        return await self.redis.incr(key)

    async def decr(self, key):
        if await self.redis.exists(key):
            if int(await self.get(key)) >= 1:
                return await self.redis.decr(key)
            return

    async def srem(self, key, value):
        return await self.redis.srem(key, value)
