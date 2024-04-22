from sqlalchemy import Column, Integer, String

from models.base import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
