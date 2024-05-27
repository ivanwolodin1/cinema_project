from functools import lru_cache

from core.elasticsearch_queries import (get_main_page_query,
                                        get_movies_by_person_id_query,
                                        get_pop_movies_by_genre_query,
                                        get_search_movies_query)
from fastapi import Depends
from models.film import Film
from services.elastic_searcher import AsyncDataStorage, get_es_searcher
from services.redis_cache import (AsyncCacheSearcher, cache_searcher,
                                  get_redis_cache_searcher)


class FilmService:
    def __init__(
        self,
        storage_searcher: AsyncDataStorage,
        searcher_cache: AsyncCacheSearcher,
    ):
        self.storage_searcher = storage_searcher
        self.cache_searcher = searcher_cache
        self.index = 'movies'

    @cache_searcher()
    async def get_all(self, page_number: int, page_size: int):
        response = await self.storage_searcher.search(
            index=self.index,
            body=get_main_page_query(page_number, page_size),
        )

        return [
            Film(
                id=hit['_source']['id'],
                title=hit['_source']['title'],
                imdb_rating=hit['_source']['imdb_rating'],
            )
            for hit in response['hits']['hits']
        ]

    @cache_searcher()
    async def get_films_by_person(self, person_id):
        movies = await self.storage_searcher.search(
            index=self.index,
            body=get_movies_by_person_id_query(person_id),
        )

        return [
            {
                'id': hit['_source']['id'],
                'title': hit['_source']['title'],
                'imdb_rating': hit['_source']['imdb_rating'],
            }
            for hit in movies['hits']['hits']
        ]

    @cache_searcher()
    async def search_movie(self, query: str, page_number: int, page_size: int):
        response = await self.storage_searcher.search(
            index=self.index,
            body=get_search_movies_query(query, page_number, page_size),
        )

        return [
            {
                'id': hit['_source']['id'],
                'title': hit['_source']['title'],
                'imdb_rating': hit['_source']['imdb_rating'],
            }
            for hit in response['hits']['hits']
        ]

    @cache_searcher()
    async def get_popular_movies_in_genre(self, genre_id: str):
        response = await self.storage_searcher.search(
            index=self.index,
            body=get_pop_movies_by_genre_query(genre_id),
        )
        return [
            {
                'id': hit['_source']['id'],
                'title': hit['_source']['title'],
                'imdb_rating': hit['_source']['imdb_rating'],
            }
            for hit in response['hits']['hits']
        ]

    @cache_searcher()
    async def get_by_id(self, index, doc_id):
        return await self.storage_searcher.get_by_id(index, doc_id)

    @cache_searcher()
    async def get_movies_interception(self, index, movies: list[str]):
        movies = await self.storage_searcher.get_interception(index, movies)
        return [
            {
                'id': hit['_source']['id'],
                'title': hit['_source']['title'],
            }
            for hit in movies['hits']['hits']
        ]

    @cache_searcher()
    async def get_movies_by_uuids(self, index, movies: list[str]):
        movies = await self.storage_searcher.get_movies_by_uuids(index, movies)
        return [hit['_source']['title'] for hit in movies['hits']['hits']]


@lru_cache()
def get_film_service(
    storage_searcher: AsyncDataStorage = Depends(get_es_searcher),
    searcher_cache: AsyncCacheSearcher = Depends(get_redis_cache_searcher),
) -> FilmService:
    return FilmService(storage_searcher, searcher_cache)
