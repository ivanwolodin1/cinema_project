from uuid import UUID
from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    """Response for recommendation endpoint"""
    list_of_films: list[UUID]