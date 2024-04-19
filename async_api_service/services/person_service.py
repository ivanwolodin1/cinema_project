from functools import lru_cache

from core.elasticsearch_queries import get_search_person_query
from fastapi import Depends
from services.elastic_searcher import AsyncDataStorage, get_es_searcher
from services.redis_cache import (AsyncCacheSearcher, cache_searcher,
                                  get_redis_cache_searcher)


class PersonService:
    def __init__(
        self,
        storage_searcher: AsyncDataStorage,
        searcher_cache: AsyncCacheSearcher,
    ):
        self.storage_searcher = storage_searcher
        self.cache_searcher = searcher_cache
        self.index = 'persons'

    @cache_searcher()
    async def search_person(
        self, query: str, page_number: int, page_size: int,
    ):
        response = await self.storage_searcher.search(
            index=self.index,
            body=get_search_person_query(query, page_number, page_size),
        )

        return [
            {
                'id': hit['_id'],
                'name': hit['_source']['name'],
                'films': hit['_source']['films'],
            }
            for hit in response['hits']['hits']
        ]

    @cache_searcher()
    async def get_by_id(self, index, doc_id):
        return await self.storage_searcher.get_by_id(index, doc_id)


@lru_cache()
def get_person_service(
    storage_searcher: AsyncDataStorage = Depends(get_es_searcher),
    searcher_cache: AsyncCacheSearcher = Depends(get_redis_cache_searcher),
) -> PersonService:
    return PersonService(storage_searcher, searcher_cache)
