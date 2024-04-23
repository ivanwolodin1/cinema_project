from models.base import Base
from models.user import User
from sqlalchemy import Column, ForeignKey, Index, Integer, String


class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False
    )
    password_hash = Column(String, nullable=False)


Index('user_id', Password.id)
