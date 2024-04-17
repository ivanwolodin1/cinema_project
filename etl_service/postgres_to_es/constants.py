import os
from datetime import datetime

ES_INDEX_STRUCTURE = {
    'settings': {
        'refresh_interval': '1s',
        'analysis': {
            'filter': {
                'english_stop': {'type': 'stop', 'stopwords': '_english_'},
                'english_stemmer': {'type': 'stemmer', 'language': 'english'},
                'english_possessive_stemmer': {
                    'type': 'stemmer',
                    'language': 'possessive_english',
                },
                'russian_stop': {'type': 'stop', 'stopwords': '_russian_'},
                'russian_stemmer': {'type': 'stemmer', 'language': 'russian'},
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
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {'type': 'keyword'},
            'imdb_rating': {'type': 'float'},
            'genre': {'type': 'keyword'},
            'title': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {'raw': {'type': 'keyword'}},
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
ES_INDEX_NAME = 'movies'
ES_PORT = os.environ.get('ES_PORT')

SELECT_PERSONS = 'persons_select'
SELECT_MOVIES_BY_PERSONS = 'movies_by_persons_select'
SELECT_PERSONS_GENRES_FILM_WORKS_BY_MOVIES = (
    'persons_genres_film_works_by_movies_select'
)
SELECT_MOVIES_WITH_NO_PERSONS = 'movies_with_no_persons_select'

VERY_OLD_YEAR = 2009
VERY_OLD_MONTH = 10
VERY_OLD_DAY = 5
VERY_OLD_HOUR = 18
VERY_OLD_MINUTE = 0

LAST_MODIFIED_DATA = datetime(
    VERY_OLD_YEAR,
    VERY_OLD_MONTH,
    VERY_OLD_DAY,
    VERY_OLD_HOUR,
    VERY_OLD_MINUTE,
)

STATE_JSON_FILE_NAME = 'state.json'
STATE_JSON_KEY = 'last_sync'

ETL_LOG_FILENAME = 'etl.log'
LOGGER_ENCODING = 'utf-8'
LOGGER_NAME = 'es_uploader'
LOGGER_FORMAT = '%(asctime)s %(message)s'

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
}

EXCEPTION_ON_EXCEEDING_TRIES_LIMIT = 'Maximum number of attempts reached'
