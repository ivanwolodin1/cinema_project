from models.base import Base
from models.user import User
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String


class LoginHistory(Base):
    __tablename__ = 'login_history'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False
    )
    device = Column(String(50), nullable=False)
    login_at = Column(DateTime, nullable=False)


Index('login_user_id', LoginHistory.id)
