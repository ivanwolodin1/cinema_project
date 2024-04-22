from abc import abstractmethod
from datetime import datetime, timedelta
from functools import lru_cache
from time import time
from typing import Any, Dict, Optional

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from sqlalchemy import delete

from core.constants import EXPIRATION_CACHE_TIME
from core.exceptions import (
    AccessTokenExpired,
    InvalidTokenError,
    UserAuthenticationError,
)
from models.login_history import LoginHistory
from models.token import RefreshToken
from schemas.token import AuthTokens
from services.db_searcher import AsyncDb, get_db_searcher
from services.redis_cache import (
    AsyncCacheSearcher,
    get_redis_cache_searcher,
)
from services.register_service import UserCRUD, get_register_service


class TokenManager:
    @abstractmethod
    async def get_refresh_and_access_tokens(
            self, email: str, password: str
    ) -> Optional[AuthTokens]:
        pass

    @abstractmethod
    async def insert_login_history(self, user_id: int, device: str) -> None:
        pass

    @abstractmethod
    async def verify_token(self, access_token: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def revoke_token(self, user_id: int, access_token: str) -> int:
        pass


class TokenService(TokenManager):
    def __init__(
            self,
            user_crud: UserCRUD,
            authjwt: AuthJWT,
            db: AsyncDb,
            cacher: AsyncCacheSearcher,
    ) -> None:
        self.user_crud = user_crud
        self.authjwt = authjwt
        self.db = db
        self.cacher = cacher

    async def _insert_token(self, new_refresh_token: RefreshToken) -> None:
        async with self.db.get_session() as session:
            session.add(new_refresh_token)

    async def insert_login_history(self, user_id: int, device: str) -> None:
        login_history = LoginHistory(
            user_id=user_id, device=device, login_at=datetime.now()
        )

        async with self.db.get_session() as session:
            session.add(login_history)

    async def get_refresh_and_access_tokens(
            self, email: str, password: str
    ) -> Optional[AuthTokens]:
        user = await self.user_crud.authenticate_user(email, password)
        if not user:
            raise UserAuthenticationError()

        access_token = await self.authjwt.create_access_token(
            subject=user.email,
            expires_time=EXPIRATION_CACHE_TIME,
            user_claims={'role': user.role_id, 'uid': user.id},
        )
        refresh_token = await self.authjwt.create_refresh_token(
            subject=user.email
        )

        expires_at = datetime.now() + timedelta(days=30)
        new_refresh_token = RefreshToken(
            user_id=user.id, refresh_token=refresh_token, expires_at=expires_at
        )

        await self._insert_token(new_refresh_token)

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
        )

    async def verify_token(self, access_token: str) -> Dict[str, Any]:
        try:
            logout_token = await self.cacher.get(access_token)
            if logout_token:
                raise InvalidTokenError()

            token_data = await self.authjwt.get_raw_jwt(access_token)
            if time() > token_data.get('exp'):
                raise AccessTokenExpired()
            return token_data
        except:
            raise InvalidTokenError()

    async def revoke_token(self, user_id: int, access_token: str) -> int:
        async with self.db.get_session() as session:
            stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)
            res = await session.execute(stmt)
            await self.cacher.set(access_token, user_id, EXPIRATION_CACHE_TIME)
        return res


@lru_cache()
def get_token_service(
        user_crud: UserCRUD = Depends(get_register_service),
        authjwt: AuthJWT = Depends(),
        storage_searcher: AsyncDb = Depends(get_db_searcher),
        redis: AsyncCacheSearcher = Depends(get_redis_cache_searcher),
) -> TokenService:
    return TokenService(user_crud, authjwt, storage_searcher, redis)
