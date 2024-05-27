#!/usr/bin/env python3
# """Scheduler для обновления рекомендаций

# 1. запрос в UGC, предполагается, что ответ получается в виде:
#      userid: {'liked_movies': [..., ..., ...], 'disliked_movies': [..., ..., ...]}
# 2. далее по каждому пользователю отправляем запрос в GigaChat (Алексей )
# 3. затем сервис идет в AsyncAPI получает ответ в виде пересечения рекомендованных фильмов и тех, которые есть в ES
# 4. результат кладет в базу сервиса рекомендаций, фактически перезаписывая ее

# """

import asyncio
import aiohttp
import aiopg
import json

from giga import get_suggestion

UGC_API_URL = "http://like_service:8000/api/v1/likes/fetch_likes_list"
GIGACHAT_API_URL = "https://gigachat.example.com/get_recommendations"
ASYNC_API_URL_TITLE_BY_UUIDS = "http://asyncapi:8000/api/v1/films/fetch_titles_by_uuid"
ASYNC_API_URL_INTERSECTION = "http://asyncapi:8000/api/v1/films/find_intersection"
RECOMMENDATIONS_DB_CONFIG = {
    'host': 'postgres_recommendation',
    'port': 5433,
    'user': 'app',
    'password': '123qwe',
    'dbname': 'recsys_database'
}


async def fetch_ugc_data(session):
    async with session.get(UGC_API_URL) as response:
        data = await response.json()
        if data['status'] == 'Success':
            return json.loads(data['res'].replace("'", '"'))
        else:
            raise ValueError("Failed to fetch UGC data")


async def fetch_titles_by_uuid(session, movies_list):
    print(f'movies={movies_list}')
    async with session.post(ASYNC_API_URL_TITLE_BY_UUIDS, json=movies_list) as response:
        print(f'resp={response}')
        return await response.json()


async def fetch_intersection(session, gigachat_recommendations):
    async with session.post(ASYNC_API_URL_INTERSECTION, json=gigachat_recommendations) as response:
        return await response.json()


async def update_recommendations_db(pool, user_id, recommendations):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO recommendations (user_id, recommendations) VALUES (%s, %s) "
                              "ON CONFLICT (user_id) DO UPDATE SET recommendations = EXCLUDED.recommendations",
                              (user_id, recommendations))
            await conn.commit()


async def main():
    while True:
        print("Running fetching")
        pool = None
        try:
            async with aiohttp.ClientSession() as session:
                # TODO: использовать пагинацию, так как данных может быть много
                ugc_data = await fetch_ugc_data(session)
                pool = await aiopg.create_pool(**RECOMMENDATIONS_DB_CONFIG)
                for user_id, user_data in ugc_data.items():
                    movie_names = await fetch_titles_by_uuid(session, user_data.get('liked_movies'))
                    movies_liked_by_user = ', '.join(movie_names['data'])
                    suggested_by_giga_chat = get_suggestion(movies_liked_by_user)
                    if suggested_by_giga_chat:
                        intersection = await fetch_intersection(session, suggested_by_giga_chat)
                        await update_recommendations_db(pool, user_id, intersection)
        except Exception as e:
            print(e)
        finally:
            if pool is not None:
                pool.close()
                await pool.wait_closed()
        await asyncio.sleep(10)

if __name__ == '__main__':
    print("Starting scheduler")
    asyncio.run(main())
