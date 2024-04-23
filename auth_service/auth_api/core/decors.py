from typing import Callable

from fastapi import Depends, Header
from services.token_service import TokenManager, get_token_service


def roles_required(role_id: int) -> Callable:
    def decorator(func: Callable):
        async def wrapper(
            access_token: str = Header(None),
            token_manager: TokenManager = Depends(get_token_service),
        ):
            acc_token = await token_manager.verify_token(access_token)
            if acc_token.get('role') != role_id:
                return {'response': 'Not granted'}
            return await func()

        return wrapper

    return decorator
