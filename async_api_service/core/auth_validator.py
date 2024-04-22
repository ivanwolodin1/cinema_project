from functools import wraps

import aiohttp
from fastapi import HTTPException

from core.config import AUTH_ROUTE


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        authorization_header = kwargs.get('authorization_header')
        if authorization_header is None:
            raise HTTPException(status_code=401, detail="Missing auth token")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    AUTH_ROUTE,
                    headers={"accept": "application/json", "access-token": authorization_header}) as response:
                if response.status == 200:
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(status_code=401, detail="Authentication failed")
    return wrapper
