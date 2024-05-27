from sqlalchemy import Column, Integer, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID

from ..base import Base

JSONVariant = JSON().with_variant(JSONB(), "postgresql")


class Recommendation(Base):
    __tablename__ = "recommendations"

    user_id = Column(UUID, primary_key=True)
    list_of_recommendations = Column(JSONVariant)
