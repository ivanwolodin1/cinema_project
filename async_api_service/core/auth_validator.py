from functools import wraps
from http import HTTPStatus

import aiohttp
from core.config import AUTH_ROUTE
from fastapi import HTTPException


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        authorization_header = kwargs.get('authorization_header')
        if authorization_header is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Missing auth token',
            )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                AUTH_ROUTE,
                headers={
                    'accept': 'application/json',
                    'access-token': authorization_header,
                },
            ) as response:
                if response.status == HTTPStatus.OK:
                    return await func(*args, **kwargs)
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail='Authentication failed',
                )

    return wrapper
