from models.like import LikeData
from motor.motor_asyncio import AsyncIOMotorClient


async def set_like(
    user_id: str,
    like_data: LikeData,
    db: AsyncIOMotorClient,
) -> str:
    collection = db['db_likes']['likes_collection']
    api_data = like_data.dict()
    movie_id = api_data.get('movie_id')
    movie = await collection.find_one({'_id': movie_id})

    if not movie:
        await collection.insert_one({'_id': movie_id, 'users': [user_id]})
        return 'Movie added, so does like'

    users = movie.get('users', [])
    if user_id in users:
        await collection.update_one(
            {'_id': movie_id},
            {'$pull': {'users': user_id}},
        )
        return 'Disliked'

    await collection.update_one(
        {'_id': movie_id},
        {'$addToSet': {'users': user_id}},
    )
    return 'Liked'


async def get_liked_users(movie_id: int, db: AsyncIOMotorClient) -> list:
    collection = db['db_likes']['likes_collection']

    movie = await collection.find_one({'_id': movie_id})
    if movie is None:
        return []
    liked_users = movie.get('users', [])
    res = []
    for user_id in liked_users:
        res.append(user_id)
    return res
