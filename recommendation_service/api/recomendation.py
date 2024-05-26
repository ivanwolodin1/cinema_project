"""Endpoints for getting recommendation information."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from ..schemas.recomendation import RecommendationResponse
from ..services.recommendation import RecommendationService, get_rec_service

recommendation_router = APIRouter()


@recommendation_router.get(
    "/recommendation/{user_id}", response_model=RecommendationResponse
)
async def recommendation(
        user_id: UUID,
        rec_service: RecommendationService = Depends(get_rec_service)
):
    try:
        res = await rec_service.get_recommendations(user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    return RecommendationResponse(list_of_films=res.list_of_recommendations)
