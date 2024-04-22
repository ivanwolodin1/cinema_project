from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Optional

from core.exceptions import (
    DuplicateUserError,
    InvalidRoleError,
    UserAuthenticationError,
)
from core.utils import hash_password
from fastapi import Depends
from models.password import Password
from models.role import Role
from models.user import User
from passlib.hash import pbkdf2_sha256
from schemas.user import UserCreate
from services.db_searcher import AsyncDb, get_db_searcher
from sqlalchemy import select, update


class RegisterService(ABC):
    @abstractmethod
    async def create_user(self, email: str, password: str) -> UserCreate:
        pass

    @abstractmethod
    async def check_if_user_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[User]:
        pass


class UserCRUD(RegisterService):
    def __init__(self, db: AsyncDb):
        self.db = db

    async def _insert_user(self, email: str, role_id: int) -> User:
        new_user = User(email=email, role_id=role_id)
        async with self.db.get_session() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        return new_user

    async def _insert_password(self, user_id: int, password: str) -> None:
        p_hash = hash_password(password)
        new_password = Password(user_id=user_id, password_hash=p_hash)
        async with self.db.get_session() as session:
            session.add(new_password)

    async def check_if_user_exists(self, email: str) -> bool:
        async with self.db.get_session() as session:
            query_email = select(User).filter(User.email == email)
            result_email = await session.execute(query_email)

            return result_email.scalar() is not None

    async def check_if_role_exists(self, role_id: int) -> bool:
        async with self.db.get_session() as session:
            result = await session.execute(
                select(Role).where(Role.id == role_id)
            )
            return bool(result.scalar())

    async def create_user(
        self, email: str, password: str, role_id: int = 1
    ) -> User:
        if await self.check_if_user_exists(email):
            raise DuplicateUserError()

        if not await self.check_if_role_exists(role_id):
            raise InvalidRoleError()

        new_user = await self._insert_user(email, role_id)
        await self._insert_password(new_user.id, password)

        return new_user

    async def _update_user_email(self, user_id: int, new_email: str) -> User:
        async with self.db.get_session() as session:
            stmt = (
                update(User).where(User.id == user_id).values(email=new_email)
            )
            new_user = await session.execute(stmt)
            await session.commit()

        return new_user

    async def _update_user_password(
        self, user_id: int, new_pass: str
    ) -> Password:
        p_hash = hash_password(new_pass)
        async with self.db.get_session() as session:
            stmt = (
                update(Password)
                .where(Password.user_id == user_id)
                .values(password_hash=p_hash)
            )
            await session.execute(stmt)
            await session.commit()

    async def update_user_email(
        self, user_id: int, new_email: str, new_password: str
    ) -> User:
        if await self.check_if_user_exists(new_email):
            raise DuplicateUserError()

        upd_user = await self._update_user_email(user_id, new_email)
        await self._update_user_password(user_id, new_password)

        return upd_user

    async def authenticate_user(  # type: ignore
        self, email: str, password: str
    ) -> Optional[User]:  # type: ignore
        async with self.db.get_session() as session:
            query_user = select(User).filter(User.email == email)
            result_user = await session.execute(query_user)
            user = result_user.scalar()

            if user is None:
                raise UserAuthenticationError()

            query_password = select(Password).filter(
                Password.user_id == user.id
            )
            result_password = await session.execute(query_password)
            stored_password_hash = result_password.scalar()
            if stored_password_hash and pbkdf2_sha256.verify(
                password, stored_password_hash.password_hash
            ):
                return user


@lru_cache()
def get_register_service(
    storage_searcher: AsyncDb = Depends(get_db_searcher),
) -> UserCRUD:
    return UserCRUD(storage_searcher)
