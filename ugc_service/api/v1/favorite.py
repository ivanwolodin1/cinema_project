from http import HTTPStatus

from crud.auth_service import get_current_user
from crud.favorite_service import add_favorite, get_favorites, remove_favorite
from db.get_mongo import get_database
from fastapi import APIRouter, Depends, HTTPException
from models.favorite import BookmarkData
from motor.motor_asyncio import AsyncIOMotorClient

favoriter = APIRouter()


@favoriter.post('/bookmark/add')
async def add_bookmark_endpoint(
    bookmark_data: BookmarkData,
    db: AsyncIOMotorClient = Depends(get_database),
):
    operation_status = await add_favorite(bookmark_data, db)
    return {'message': operation_status}


@favoriter.get('/bookmarks/')
async def get_bookmarks_endpoint(
    db: AsyncIOMotorClient = Depends(get_database),
    user_id: str = Depends(get_current_user),
):
    bookmarks = await get_favorites(user_id, db)
    return {'bookmarks': bookmarks}


@favoriter.delete('/bookmark/{movie_id}')
async def remove_bookmark_endpoint(
    movie_id: int,
    db: AsyncIOMotorClient = Depends(get_database),
    user_id: str = Depends(get_current_user),
):
    operation_status = await remove_favorite(user_id, movie_id, db)
    if operation_status == 'Bookmark not found':
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Bookmark not found',
        )
    return {'message': operation_status}
