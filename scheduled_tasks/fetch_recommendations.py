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


UGC_API_URL = "http://ugc:8003/get_user_data"
GIGACHAT_API_URL = "https://gigachat.example.com/get_recommendations"
ASYNC_API_URL = "http://asyncapi:8000/get_intersection"
RECOMMENDATIONS_DB_CONFIG = {
    'host': 'postgres_recommendation',
    'port': 5433,
    'user': 'app',
    'password': '123qwe',
    'dbname': 'recsys_database'
}


async def fetch_ugc_data(session):
    async with session.get(UGC_API_URL) as response:
        return await response.json()


async def fetch_gigachat_recommendations(session, user_id, user_data):
    # вставить сюда prompt
    async with session.post(GIGACHAT_API_URL, json={'user_id': user_id, 'user_data': user_data}) as response:
        return await response.json()


async def fetch_intersection(session, recommendations):
    async with session.post(ASYNC_API_URL, json={'recommendations': recommendations}) as response:
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
        try:
            async with aiohttp.ClientSession() as session:
                # TODO: использовать пагинацию, так как данных может быть
                ugc_data = await fetch_ugc_data(session)

                pool = await aiopg.create_pool(**RECOMMENDATIONS_DB_CONFIG)
                for user_id, user_data in ugc_data.items():
                    resp = fetch_gigachat_recommendations(session, user_id, user_data)
                    # parse response 
                    intersection = fetch_intersection(session, resp)
                    await update_recommendations_db(pool, user_id, intersection)

                pool.close()
                await pool.wait_closed()
        except:
            pass
        await asyncio.sleep(60)



asyncio.run(main())
