import os

from pydantic_settings import BaseSettings
from tests.functional.utils.constants import ES_INDEXES


class TestSettings(BaseSettings):
    es_host: str = os.getenv('ELASTIC_HOST', 'http://etl_elasticsearch')
    es_port: int = int(os.getenv('ELASTIC_PORT', '9200'))
    es_max_tries: int = 10

    es_index_movies: str = os.getenv('INDEX_MOVIES', 'movies')
    es_index_persons: str = os.getenv('INDEX_PERSONS', 'persons')
    es_index_genres: str = os.getenv('INDEX_GENRES', 'genres')

    es_index_movies_mapping: dict = ES_INDEXES['movies']
    es_index_persons_mapping: dict = ES_INDEXES['persons']
    es_index_genres_mapping: dict = ES_INDEXES['genres']

    async_service_url: str = os.getenv('ASYNC_API_HOST', 'http://asyncapi')
    async_service_port: int = int(os.getenv('ASYNC_API_PORT', '8000'))

    redis_host: str = os.getenv('REDIS_HOST', 'http://redis')
    redis_port: int = int(os.getenv('REDIS_PORT', '6379'))
    redis_max_tries: int = 10


test_settings = TestSettings()
