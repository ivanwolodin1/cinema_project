import aiohttp


async def fetch_recommendations(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://recommendation_service:8000/recommendation/{user_id}') as response:
            try:
                if response.status == 200:
                    return await response.json()
            except:
                return []
            