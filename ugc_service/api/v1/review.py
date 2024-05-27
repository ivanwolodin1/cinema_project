from http import HTTPStatus

from crud.reviews_service import add_review, delete_review, get_reviews
from db.get_mongo import get_database
from fastapi import APIRouter, Depends, HTTPException
from models.review import ReviewData
from motor.motor_asyncio import AsyncIOMotorClient

reviewer = APIRouter()


@reviewer.post('/review/add')
async def add_review_endpoint(
    review_data: ReviewData,
    db: AsyncIOMotorClient = Depends(get_database),
):
    user_id = 1
    operation_status = await add_review(review_data, user_id, db)
    return {'message': operation_status}


@reviewer.get('/review/{movie_id}')
async def get_reviews_endpoint(
    movie_id: int,
    db: AsyncIOMotorClient = Depends(get_database),
):
    reviews = await get_reviews(movie_id, db)
    if not reviews:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Reviews not found',
        )
    return {'reviews': reviews}


@reviewer.delete('/review/{movie_id}}')
async def delete_review_endpoint(
    movie_id: int,
    db: AsyncIOMotorClient = Depends(get_database),
):
    user_id = 1
    operation_status = await delete_review(movie_id, user_id, db)
    if operation_status == 'Review not found':
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Review not found',
        )
    return {'message': operation_status}
