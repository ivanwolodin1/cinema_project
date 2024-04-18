DOCS_NUMBER = 50
GENRES_NUMBER = 10
PERSON_NUMBER = 10

MOVIE_TITLE_TO_SEARCH = 'matrix'
NONEXISTENT_SEARCH = 'sjdkangfakdfjngsdfg'

GENRE_PERSON_TO_SEARCH = 'Tarantino'


ES_SEARCH_ERROR = 'Ошибка записи данных в Elasticsearch'
MOVIES_INDEX = 'movies'

ES_INDEX_SETTING = {
    'settings': {
        'refresh_interval': '1s',
        'analysis': {
            'filter': {
                'english_stop': {'type': 'stop', 'stopwords': '_english_'},
                'english_stemmer': {
                    'type': 'stemmer',
                    'language': 'english',
                },
                'english_possessive_stemmer': {
                    'type': 'stemmer',
                    'language': 'possessive_english',
                },
                'russian_stop': {'type': 'stop', 'stopwords': '_russian_'},
                'russian_stemmer': {
                    'type': 'stemmer',
                    'language': 'russian',
                },
            },
            'analyzer': {
                'ru_en': {
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'english_stop',
                        'english_stemmer',
                        'english_possessive_stemmer',
                        'russian_stop',
                        'russian_stemmer',
                    ],
                },
            },
        },
    },
}

ES_INDEX_MOVIES = {
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {'type': 'keyword'},
            'imdb_rating': {'type': 'float'},
            'genre': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                },
            },
            'title': {
                'type': 'text',
            },
            'description': {'type': 'text', 'analyzer': 'ru_en'},
            'director': {'type': 'text', 'analyzer': 'ru_en'},
            'actors_names': {'type': 'text', 'analyzer': 'ru_en'},
            'writers_names': {'type': 'text', 'analyzer': 'ru_en'},
            'actors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                    'name': {'type': 'text', 'analyzer': 'ru_en'},
                },
            },
            'writers': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                    'name': {'type': 'text', 'analyzer': 'ru_en'},
                },
            },
        },
    },
}

ES_INDEX_GENRES = {
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {'type': 'keyword'},
            'name': {'type': 'text'},
        },
    },
}

ES_INDEX_PERSONS = {
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {'type': 'keyword'},
            'name': {'type': 'text'},
            'films': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                    'roles': {'type': 'text'},
                },
            },
        },
    },
}

ES_INDEXES = {
    'movies': ES_INDEX_SETTING | ES_INDEX_MOVIES,
    'genres': ES_INDEX_SETTING | ES_INDEX_GENRES,
    'persons': ES_INDEX_SETTING | ES_INDEX_PERSONS,
}
