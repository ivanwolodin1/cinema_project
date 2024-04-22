from typing import Callable

from fastapi import Header, Depends

from services.token_service import get_token_service, TokenManager


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
