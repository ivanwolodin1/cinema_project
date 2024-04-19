from tests.functional.settings import test_settings
from tests.functional.test_data.es_mapping import (
    generate_es_genres_search_data, generate_es_movies_search_data,
    generate_es_persons_search_data)

utility_functions_by_index = {
    test_settings.es_index_movies: {
        'es_index_structure': test_settings.es_index_movies_mapping,
        'data_gen_function': generate_es_movies_search_data,
        'url': f'{test_settings.async_service_url}:{test_settings.async_service_port}'
        + '/api/v1/films/',
    },
    test_settings.es_index_persons: {
        'es_index_structure': test_settings.es_index_persons_mapping,
        'data_gen_function': generate_es_persons_search_data,
        'url': f'{test_settings.async_service_url}:{test_settings.async_service_port}'
        + '/api/v1/persons/',
    },
    test_settings.es_index_genres: {
        'es_index_structure': test_settings.es_index_genres_mapping,
        'data_gen_function': generate_es_genres_search_data,
        'url': f'{test_settings.async_service_url}:{test_settings.async_service_port}'
        + '/api/v1/genres/',
    },
}
