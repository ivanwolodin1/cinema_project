from typing import Optional

from fastapi import APIRouter, Depends, Header
from schemas.token import TokenResponse
from schemas.user import UserAuthentication, UserCreate, UserResponse
from services.register_service import UserCRUD, get_register_service
from services.token_service import TokenManager, get_token_service

router = APIRouter()


@router.get('/')
async def get():
    return {'status': 'ok'}


@router.post('/sign_up', response_model=UserResponse)
async def sign_up(
    user_data: UserCreate,
    register_service: UserCRUD = Depends(get_register_service),
):
    new_user = await register_service.create_user(
        email=user_data.email,
        password=user_data.password,
        role_id=user_data.role_id,
    )
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
    )


@router.post('/sign_in', response_model=TokenResponse)
async def sign_in(
    user_data: UserAuthentication,
    token_manager: TokenManager = Depends(get_token_service),
    user_agent: Optional[str] = Header(None),
):
    data = await token_manager.get_refresh_and_access_tokens(
        user_data.email, user_data.password
    )
    await token_manager.insert_login_history(data.user_id, user_agent)
    return TokenResponse(
        access_token=data.access_token,
        refresh_token=data.refresh_token,
    )
