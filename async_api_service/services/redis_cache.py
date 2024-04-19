import pickle
from abc import ABC, abstractmethod
from functools import wraps

from core.constants import FILM_CACHE_EXPIRE_IN_SECONDS
from db.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis


class AsyncCacheSearcher(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, cache_value: str, expire: int, **kwargs):
        pass


class RedisCacheSearcher(AsyncCacheSearcher):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, **kwargs):
        return await self.redis.get(key)

    async def set(self, key: str, cache_value: str, expire: int, **kwargs):
        return await self.redis.set(key, cache_value, expire, **kwargs)


def cache_searcher():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            key = f'{self.__class__.__name__}:{func.__name__}:{pickle.dumps(args)}:{pickle.dumps(kwargs)}'
            try:
                cached_result = await self.cache_searcher.get(key)
            except Exception as retrieve_error:
                print(f'Error retrieving from cache: {retrieve_error}')
                cached_result = None

            if cached_result:
                return pickle.loads(cached_result)

            try:
                cached_value = await func(self, *args, **kwargs)
                await self.cache_searcher.set(key, pickle.dumps(cached_value), FILM_CACHE_EXPIRE_IN_SECONDS)
                return cached_value
            except Exception as store_error:
                print(f'Error storing to cache: {store_error}')
                return await func(self, *args, **kwargs)

        return wrapper

    return decorator


async def get_redis_cache_searcher(
    redis: Redis = Depends(get_redis),
) -> RedisCacheSearcher:
    return RedisCacheSearcher(redis)
