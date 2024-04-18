from typing import List
from uuid import UUID

from models.base import Base


class FilmRole(Base):
    id: UUID
    roles: List[str]


class Person(Base):
    id: UUID
    name: str
    films: list[FilmRole] = []
