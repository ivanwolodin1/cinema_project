from http import HTTPStatus
import json

from crud.like_service import get_liked_users, set_like, fetch_all_likes
from db.get_mongo import get_database
from fastapi import APIRouter, Depends, Header
from models.like import LikeData
from motor.motor_asyncio import AsyncIOMotorClient
from utils.auth_validator import auth_required

liker = APIRouter()


@liker.get('/')
async def main_page():
    return {'status': 'ok'}


@liker.post('/set_like', status_code=HTTPStatus.CREATED)
@auth_required
async def set_like_or_dislike(
    like_data: LikeData,
    db: AsyncIOMotorClient = Depends(get_database),
    authorization_header: str = Header(None),
):
    user_id = "1"
    res = await set_like(user_id, like_data, db)
    if res is None:
        return {'message': 'Like is not added', 'status': 'Fail', 'res': None}
    return {'message': 'Like is added', 'status': 'Success', 'res': json.dumps(res)}


@liker.get('/get_likes_by_movie')
async def get_likes_by_movie(
    movie_id: int,
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await get_liked_users(movie_id, db)
    return {'status': 'Success', 'res': str(res)}


@liker.get('/fetch_likes_list')
async def fetch_likes_list(
    db: AsyncIOMotorClient = Depends(get_database),
):
    # TODO: защитить роут токеном
    res = await fetch_all_likes(db)
    
    return {'status': 'Success', 'res': str(res)}

