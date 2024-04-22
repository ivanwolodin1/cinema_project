from fastapi import APIRouter, Depends, Header
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from core.constants import ADMIN_ROLE_ID, AUTHENTICATED_USER_ROLE_ID
from models.login_history import LoginHistory
from schemas.login_history import LoginHistoryDto
from schemas.user import UserUpdate
from services.db_searcher import AsyncPostgres, get_db_searcher
from services.register_service import UserCRUD, get_register_service
from services.token_service import TokenManager, get_token_service

protected_router = APIRouter()


@protected_router.post('/admin_route')
async def admin_route(
        access_token: str = Header(None),
        token_manager: TokenManager = Depends(get_token_service),
):
    acc_token = await token_manager.verify_token(access_token)
    if acc_token.get('role') == ADMIN_ROLE_ID:
        return {
            'access_token': acc_token,
        }


@protected_router.post('/authenticate_user_route')
async def authenticate_user_route(
        access_token: str = Header(None),
        token_manager: TokenManager = Depends(get_token_service),
):
    acc_token = await token_manager.verify_token(access_token)
    if acc_token.get('role') == AUTHENTICATED_USER_ROLE_ID:
        return {
            'access_token': acc_token,
        }


@protected_router.post('/login_history', response_model=Page[LoginHistoryDto])
async def login_history(
        access_token: str = Header(None),
        token_manager: TokenManager = Depends(get_token_service),
        db: AsyncPostgres = Depends(get_db_searcher),
):
    acc_token = await token_manager.verify_token(access_token)
    user_id = acc_token.get('uid')
    result = await paginate(
        db.async_session(),
        (
            select(LoginHistory)
            .where(LoginHistory.user_id == user_id)
            .order_by(LoginHistory.login_at)
        )
    )
    return result


@protected_router.post('/update_account')
async def update_account(
        user_data: UserUpdate,
        access_token: str = Header(None),
        token_manager: TokenManager = Depends(get_token_service),
        register_service: UserCRUD = Depends(get_register_service),
):
    acc_token = await token_manager.verify_token(access_token)

    user_id = acc_token.get('uid')
    upd_user = await register_service.update_user_email(
        user_id=user_id,
        new_email=user_data.email,
        new_password=user_data.password,
    )
    return {'update_user': upd_user}


@protected_router.post('/logout')
async def logout(
        access_token: str = Header(None),
        token_manager: TokenManager = Depends(get_token_service),
):
    acc_token = await token_manager.verify_token(access_token)

    user_id = acc_token.get('uid')
    delete_token = await token_manager.revoke_token(user_id, access_token)
    return {'logout': delete_token}


add_pagination(protected_router)
