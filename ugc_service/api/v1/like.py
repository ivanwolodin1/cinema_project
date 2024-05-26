from http import HTTPStatus

from crud.auth_service import get_current_user
from crud.like_service import get_liked_users, set_like
from db.get_mongo import get_database
from fastapi import APIRouter, Depends
from models.like import LikeData
from motor.motor_asyncio import AsyncIOMotorClient

liker = APIRouter()


@liker.get('/')
async def main_page():
    return {'status': 'ok'}


@liker.post('/set_like', status_code=HTTPStatus.CREATED)
async def set_like_or_dislike(
    like_data: LikeData,
    db: AsyncIOMotorClient = Depends(get_database),
    user_id: str = Depends(get_current_user),
):
    res = await set_like(user_id, like_data, db)
    if res is None:
        return {'message': 'Like is not added', 'status': 'Fail', 'res': None}
    return {'message': 'Like is added', 'status': 'Success', 'res': res}


@liker.get('/get_likes_by_movie')
async def get_likes_by_movie(
    movie_id: int,
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await get_liked_users(movie_id, db)
    return {'status': 'Success', 'res': str(res)}
