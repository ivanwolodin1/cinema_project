import uuid
from functools import lru_cache
from typing import List, Optional

from core.exceptions import RoleAlreadyExist, RoleNotFound, UserNotFound
from fastapi import Depends
from models.role import Role
from models.user import User
from services.db_searcher import AsyncDb, get_db_searcher
from sqlalchemy import delete, select, update


class RoleService:
    def __init__(self, db_searcher: AsyncDb):
        self.db_searcher = db_searcher

    async def get_roles(self) -> List[Role]:
        result = await self.db_searcher.execute_query(select(Role))
        return result

    async def get_role_by_id(self, role_id: int) -> Role:
        async with self.db_searcher.get_session() as session:
            result = await session.execute(
                select(Role).where(Role.id == role_id)
            )
            role_found = result.scalars().first()
            if role_found is None:
                raise RoleNotFound()
            return role_found

    async def get_role_by_name(self, name: str) -> Role:
        async with self.db_searcher.get_session() as session:
            result = await session.execute(
                select(Role).where(Role.name == name)
            )
            found = result.scalars().first()
            if found:
                raise RoleAlreadyExist()
            return found

    async def create_role(self, name: str) -> Optional[Role]:
        async with self.db_searcher.get_session() as session:
            if await self.get_role_by_name(name=name):
                return None
            role = Role(name=name)
            session.add(role)
            await session.commit()
            return role

    async def change_name(self, role_id: int, new_name: str) -> Optional[Role]:
        if not await self.get_role_by_id(role_id=role_id):
            return None
        async with self.db_searcher.get_session() as session:
            stmt = update(Role).where(Role.id == role_id).values(name=new_name)
            await session.execute(stmt)
            await session.commit()
            role = await self.get_role_by_id(role_id)
            return role

    async def delete_role(self, role_id: uuid.UUID) -> bool:
        async with self.db_searcher.get_session() as session:
            result = await session.execute(
                delete(Role).where(Role.id == role_id)
            )
            await session.commit()
            return bool(result)

    async def set_user_role(self, username: str, role_id: int) -> User:
        async with self.db_searcher.get_session() as session:
            await session.execute(
                update(User)
                .where(User.username == username)
                .values(role_id=role_id)
            )
            await session.commit()
            result = await session.execute(
                select(User).where(User.username == username)
            )
            found = result.scalars().first()
            if found is None:
                raise UserNotFound()
            return found

    async def delete_user_role(self, username: str) -> User:
        async with self.db_searcher.get_session() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            found = result.scalars().first()
            if found is None:
                raise UserNotFound()
            # TODO: убрать захардкоженную role_id
            await session.execute(
                update(User).where(User.username == username).values(role_id=2)
            )
            await session.commit()
            return found


@lru_cache()
def get_role_service(
    storage_searcher: AsyncDb = Depends(get_db_searcher),
) -> RoleService:
    return RoleService(storage_searcher)
