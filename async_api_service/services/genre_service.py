from functools import lru_cache

from core.elasticsearch_queries import get_all_query
from fastapi import Depends
from services.elastic_searcher import AsyncDataStorage, get_es_searcher
from services.redis_cache import (AsyncCacheSearcher, cache_searcher,
                                  get_redis_cache_searcher)


class GenreService:
    def __init__(
        self,
        storage_searcher: AsyncDataStorage,
        searcher_cache: AsyncCacheSearcher,
    ):
        self.storage_searcher = storage_searcher
        self.cache_searcher = searcher_cache
        self.index = 'genres'

    @cache_searcher()
    async def get_all(self):
        all_queries = await self.storage_searcher.search(
            index=self.index, body=get_all_query,
        )

        return [
            {'id': hit['_source']['id'], 'name': hit['_source']['name']}
            for hit in all_queries['hits']['hits']
        ]

    @cache_searcher()
    async def get_by_id(self, index, doc_id):
        return await self.storage_searcher.get_by_id(index, doc_id)


@lru_cache()
def get_genre_service(
    storage_searcher: AsyncDataStorage = Depends(get_es_searcher),
    searcher_cache: AsyncCacheSearcher = Depends(get_redis_cache_searcher),
) -> GenreService:
    return GenreService(storage_searcher, searcher_cache)
