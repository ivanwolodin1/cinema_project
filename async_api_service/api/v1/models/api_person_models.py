from typing import List
from uuid import UUID

from api.v1.models.api_base_model import Base


class Film(Base):
    id: UUID
    roles: List[str]


class PersonBase(Base):
    name: str


class Person(PersonBase):
    id: UUID
    name: str
    films: List[Film] = []
