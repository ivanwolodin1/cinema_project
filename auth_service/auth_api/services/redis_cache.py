import pickle
from abc import ABC, abstractmethod

from core.constants import EXPIRATION_CACHE_TIME
from db_connectors.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis


class AsyncCacheSearcher(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: int, expire: int, **kwargs):
        pass


class RedisCacheSearcher(AsyncCacheSearcher):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, **kwargs):
        res = await self.redis.get(pickle.dumps(key))
        return pickle.loads(res) if res else None

    async def set(self, key: str, value: str, expire: int, **kwargs):
        return await self.redis.set(
            pickle.dumps(key), pickle.dumps(value), EXPIRATION_CACHE_TIME
        )


async def get_redis_cache_searcher(
    redis: Redis = Depends(get_redis),
) -> RedisCacheSearcher:
    return RedisCacheSearcher(redis)
