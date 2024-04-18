import uuid

from tests.functional.utils.constants import (DOCS_NUMBER,
                                              GENRE_PERSON_TO_SEARCH,
                                              GENRES_NUMBER,
                                              MOVIE_TITLE_TO_SEARCH,
                                              PERSON_NUMBER)


def generate_es_movies_search_data():
    return [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genre': [],
            'title': MOVIE_TITLE_TO_SEARCH,
            'description': 'A computer hacker learns about the true nature of reality',
            'director': 'Lana Wachowski',
            'actors_names': 'Keanu Reeves, Carrie-Anne Moss',
            'writers_names': ['Lilly Wachowski', 'Lana Wachowski'],
            'actors': [
                {'id': str(uuid.uuid4()), 'name': 'Keanu Reeves'},
                {'id': str(uuid.uuid4()), 'name': 'Carrie-Anne Moss'},
            ],
            'writers': [
                {'id': str(uuid.uuid4()), 'name': 'Lilly Wachowski'},
                {'id': str(uuid.uuid4()), 'name': 'Lana Wachowski'},
            ],
        }
        for _ in range(DOCS_NUMBER)
    ]


def generate_es_persons_search_data():
    return [
        {'id': str(uuid.uuid4()), 'name': GENRE_PERSON_TO_SEARCH, 'films': []}
        for _ in range(PERSON_NUMBER)
    ]


def generate_es_genres_search_data():
    return [
        {'id': str(uuid.uuid4()), 'name': f'Genre {genre_num}'}
        for genre_num in range(GENRES_NUMBER)
    ]
