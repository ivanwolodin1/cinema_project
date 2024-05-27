from models.review import ReviewData
from motor.motor_asyncio import AsyncIOMotorClient


async def add_review(
    review_data: ReviewData,
    user_id: str,
    db: AsyncIOMotorClient,
) -> str:
    collection = db['db_reviews']['reviews_collection']
    api_data = review_data.dict()
    movie_id = api_data.get('movie_id')
    review_text = api_data.get('review_text')

    await collection.update_one(
        {'_id': movie_id},
        {
            '$push': {
                'reviews': {'user_id': user_id, 'review_text': review_text},
            },
        },
        upsert=True,
    )
    return 'Review added/updated'


async def get_reviews(movie_id: int, db: AsyncIOMotorClient) -> list:
    collection = db['db_reviews']['reviews_collection']

    movie = await collection.find_one({'_id': movie_id})
    if movie is None:
        return []
    return movie.get('reviews', [])


async def delete_review(
    movie_id: int,
    user_id: str,
    db: AsyncIOMotorClient,
) -> str:
    collection = db['db_reviews']['reviews_collection']

    operation_res = await collection.update_one(
        {'_id': movie_id},
        {'$pull': {'reviews': {'user_id': user_id}}},
    )

    if operation_res.modified_count > 0:
        return 'Review deleted'
    return 'Review not found'
