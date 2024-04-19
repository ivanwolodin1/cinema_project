from typing import Optional

from models.base import Base
from models.genre import Genre
from models.person import Person


class Film(Base):
    title: str
    description: str = ''
    imdb_rating: Optional[float] = None
    genre: list[Genre] = []
    actors: list[Person] = []
    directors: list[Person] = []
    writers: list[Person] = []
