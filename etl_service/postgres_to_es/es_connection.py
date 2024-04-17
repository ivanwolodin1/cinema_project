from contextlib import contextmanager

from constants import ES_PORT
from elasticsearch import Elasticsearch

TIMEOUT = 300


@contextmanager
def open_elasticsearch_connection():
    with Elasticsearch(
        hosts=f'http://elasticsearch:{ES_PORT}/',
        request_timeout=TIMEOUT,
        max_retries=10,
        retry_on_timeout=True,
    ) as es:
        yield es
