from models.favorite import BookmarkData
from motor.motor_asyncio import AsyncIOMotorClient


async def add_favorite(
    bookmark_data: BookmarkData,
    db: AsyncIOMotorClient,
) -> str:
    collection = db['db_favorites']['favorites_collection']
    api_data = bookmark_data.dict()
    user_id = api_data.get('user_id')
    movie_id = api_data.get('movie_id')

    await collection.update_one(
        {'user_id': user_id},
        {'$addToSet': {'movies': movie_id}},
        upsert=True,
    )
    return 'Favorite added'


async def get_favorites(user_id: str, db: AsyncIOMotorClient) -> list:
    collection = db['db_favorites']['favorites_collection']

    favorites = await collection.find_one({'user_id': user_id})
    if favorites is None:
        return []
    return favorites.get('movies', [])


async def remove_favorite(
    user_id: str,
    movie_id: int,
    db: AsyncIOMotorClient,
) -> str:
    collection = db['db_favorites']['favorites_collection']

    res = await collection.update_one(
        {'user_id': user_id},
        {'$pull': {'movies': movie_id}},
    )

    if res.modified_count > 0:
        return 'Favorite removed'
    return 'Favorite not found'
