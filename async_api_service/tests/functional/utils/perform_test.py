from tests.functional.utils.index_mapping import utility_functions_by_index


async def perform_test(
    aiohttp_client_session,
    index,
    query,
    expected_status,
    expected_length,
    test_data,
):
    url = utility_functions_by_index[index].get('url') + query.pop('url_param')
    async with aiohttp_client_session.get(url=url, params=query) as response:
        assert response.status == expected_status
        body = await response.json()
        assert len(body) == expected_length or type(body) is dict
