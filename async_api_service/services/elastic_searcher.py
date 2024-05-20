from abc import ABC, abstractmethod

from core.constants import MODELS_BY_INDEX
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends


class AsyncDataStorage(ABC):
    @abstractmethod
    async def search(self, index: str, body: str):
        pass

    @abstractmethod
    async def get_by_id(self, index: str, doc_id: str):
        pass


class ElasticSearcher(AsyncDataStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index: str, doc_id: str) -> dict | None:
        try:
            doc = await self.elastic.get(index=index, id=doc_id)
        except NotFoundError:
            return None

        return MODELS_BY_INDEX[index](**doc['_source'])

    async def search(self, index: str, body: str):
        return await self.elastic.search(
            index=index,
            body=body,
        )

    async def get_interception(self, index: str, movies: list[str]):
        ...


async def get_es_searcher(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticSearcher:
    return ElasticSearcher(elastic)
