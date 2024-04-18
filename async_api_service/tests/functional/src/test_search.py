from http import HTTPStatus

import pytest
from tests.functional.settings import test_settings
from tests.functional.utils.constants import (DOCS_NUMBER,
                                              GENRE_PERSON_TO_SEARCH,
                                              MOVIE_TITLE_TO_SEARCH,
                                              NONEXISTENT_SEARCH,
                                              PERSON_NUMBER)
from tests.functional.utils.index_mapping import utility_functions_by_index
from tests.functional.utils.perform_test import perform_test

MOVIES_INDEX = test_settings.es_index_movies
MOVIES_TEST_DATA = utility_functions_by_index[MOVIES_INDEX].get(
    'data_gen_function',
)()

PERSONS_INDEX = test_settings.es_index_persons
PERSON_TEST_DATA = utility_functions_by_index[PERSONS_INDEX].get(
    'data_gen_function',
)()


@pytest.mark.parametrize(
    'index, query, expected_status, expected_length, test_data',
    [
        (
            MOVIES_INDEX,
            {'url_param': 'search', 'query': MOVIE_TITLE_TO_SEARCH},
            HTTPStatus.OK,
            DOCS_NUMBER,
            MOVIES_TEST_DATA,
        ),
        (
            MOVIES_INDEX,
            {'url_param': 'search', 'query': NONEXISTENT_SEARCH},
            HTTPStatus.OK,
            0,
            MOVIES_TEST_DATA,
        ),
        (
            PERSONS_INDEX,
            {'url_param': 'search', 'query': GENRE_PERSON_TO_SEARCH},
            HTTPStatus.OK,
            PERSON_NUMBER,
            PERSON_TEST_DATA,
        ),
        (
            PERSONS_INDEX,
            {'url_param': 'search', 'query': NONEXISTENT_SEARCH},
            HTTPStatus.OK,
            0,
            PERSON_TEST_DATA,
        ),
    ],
)
@pytest.mark.asyncio
async def test_search(
    aiohttp_client_session,
    es_write_data,
    index,
    query,
    expected_status,
    expected_length,
    test_data,
):
    await perform_test(
        es_write_data,
        aiohttp_client_session,
        index,
        query,
        expected_status,
        expected_length,
        test_data,
    )
