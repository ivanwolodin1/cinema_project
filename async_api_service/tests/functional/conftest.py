import asyncio

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from tests.functional.settings import test_settings
from tests.functional.utils.constants import ES_SEARCH_ERROR
from tests.functional.utils.helpers import prepare_bulk_query


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    elasticsearch_client = AsyncElasticsearch(
        hosts=f'{test_settings.es_host}:{test_settings.es_port}',
        verify_certs=False,
    )
    yield elasticsearch_client
    await elasticsearch_client.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client):
    async def inner(index, index_structure, es_data):
        bulk_query = prepare_bulk_query(index, es_data)
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(index=index, **index_structure)
        updated, errors = await async_bulk(
            client=es_client, actions=bulk_query, refresh='wait_for',
        )
        if errors:
            raise Exception(ES_SEARCH_ERROR)

    return inner


@pytest_asyncio.fixture(name='aiohttp_client_session', scope='session')
async def aiohttp_client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
