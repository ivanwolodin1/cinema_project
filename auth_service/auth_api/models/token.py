from models.base import Base
from models.user import User
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.sql import func


class RefreshToken(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False
    )
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


Index('refresh_token_id', RefreshToken.id)
