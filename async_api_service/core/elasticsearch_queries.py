def get_pop_movies_by_genre_query(genre_id):
    return {
        'query': {
            'nested': {
                'path': 'genre',
                'query': {
                    'bool': {'must': [{'term': {'genre.id': genre_id}}]},
                },
            },
        },
    }


def get_search_movies_query(
    search_query: str,
    page_number: int,
    page_size: int,
):
    return {
        'query': {'match': {'title': search_query}},
        'from': (page_number - 1) * page_size,
        'size': page_size,
    }


def get_main_page_query(page_number: int, page_size: int):
    return {
        'size': page_size,
        'from': (page_number - 1) * page_size,
        'sort': [{'imdb_rating': {'order': 'desc'}}],
    }


def get_movies_by_person_id_query(person_id: str):
    return {
        'query': {
            'bool': {
                'should': [
                    {
                        'nested': {
                            'path': 'actors',
                            'query': {
                                'bool': {
                                    'must': [
                                        {'match': {'actors.id': person_id}},
                                    ],
                                },
                            },
                        },
                    },
                    {
                        'nested': {
                            'path': 'directors',
                            'query': {
                                'bool': {
                                    'must': [
                                        {'match': {'directors.id': person_id}},
                                    ],
                                },
                            },
                        },
                    },
                    {
                        'nested': {
                            'path': 'writers',
                            'query': {
                                'bool': {
                                    'must': [
                                        {'match': {'writers.id': person_id}},
                                    ],
                                },
                            },
                        },
                    },
                ],
            },
        },
    }


def get_search_person_query(
    search_query: str,
    page_number: int,
    page_size: int,
):
    return {
        'query': {'match': {'name': search_query}},
        'from': (page_number - 1) * page_size,
        'size': page_size,
    }


def get_interception_query(
        movies: list[str],
):
    return {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "title.raw": movies,
                        }
                    },
                    {
                        "match_all": {}
                    },
                ],
            },
        },
    }


def titles_by_uuid_query(
    movies: list[str],
):
    return {
        "query": {
            "ids": {
                "values": movies
                }
            }
        }


get_all_query: dict = {'query': {'match_all': {}}}
