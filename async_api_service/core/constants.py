from models.film import Film
from models.genre import Genre
from models.person import Person

MODELS_BY_INDEX = {
    'movies': Film,
    'persons': Person,
    'genres': Genre,
}

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
