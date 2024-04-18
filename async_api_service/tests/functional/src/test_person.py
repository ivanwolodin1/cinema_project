from http import HTTPStatus

import pytest
from tests.functional.settings import test_settings
from tests.functional.utils.index_mapping import utility_functions_by_index
from tests.functional.utils.perform_test import perform_test

INDEX = test_settings.es_index_persons
TEST_DATA = utility_functions_by_index[INDEX].get('data_gen_function')()
PERSON_ID = TEST_DATA[0]['id']


@pytest.mark.parametrize(
    'index, query, expected_status, expected_length',
    [
        (INDEX, {'url_param': PERSON_ID}, HTTPStatus.OK, 1),
        (INDEX, {'url_param': 'non_existing_id'}, HTTPStatus.NOT_FOUND, 1),
    ],
)
@pytest.mark.asyncio
async def test_person(
    aiohttp_client_session,
    index,
    query,
    expected_status,
    expected_length,
):
    await perform_test(
        aiohttp_client_session,
        index,
        query,
        expected_status,
        expected_length,
        TEST_DATA,
    )
