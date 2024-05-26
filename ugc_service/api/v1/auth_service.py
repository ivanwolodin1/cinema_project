from core.utils import create_jwt_token
from crud.auth_service import get_current_user
from db.get_mongo import get_database
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from motor.motor_asyncio import AsyncIOMotorClient

auther = APIRouter()


@auther.post('/register', response_model=User)
async def register(user: User, db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['db_auth']['auth_collection']
    if await collection.find_one({'username': user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already registered',
        )

    hashed_password = user.password

    await collection.insert_one(
        {'username': user.username, 'hashed_password': hashed_password},
    )

    return user


@auther.post('/login')
async def login(user: User, db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['db_auth']['auth_collection']
    db_user = await collection.find_one({'username': user.username})

    if db_user is None or db_user['hashed_password'] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    token = create_jwt_token(user.username)
    return {'access_token': token, 'token_type': 'bearer'}


@auther.post('/protected')
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {'message': 'This is a protected route', 'user_id': current_user}
