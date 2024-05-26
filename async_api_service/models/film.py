from pydantic import BaseModel


class Actor(BaseModel):
    id: str
    name: str


class Writer(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float
    # genre: str
    title: str
    # description: str
    # director: str
    # actors_names: list[str]
    # writers_names: list[str]
    # actors: list[Actor]
    # writers: list[Writer]
