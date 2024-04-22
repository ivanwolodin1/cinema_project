from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db_сonnectors.async_db import get_db


class AsyncDb(ABC):
    @abstractmethod
    async def get_session(self) -> AsyncSession:
        pass

    @abstractmethod
    async def execute_query(self, query) -> list:
        pass


class AsyncPostgres(AsyncDb):
    def __init__(self, async_session):
        self.async_session = async_session

    # вопрос ревьюеру!!
    # корректно ли мы закрываем соединение здесь?
    # почему если зайти в контейнер с ДБ, подключиться к базе
    # psql -h 127.0.0.1 -U app -d user_auth_database
    # и выполнить команду
    # SELECT sum(numbackends) FROM pg_stat_database;
    # эта команда никогда не покажет одно соединение?
    # их всегда будет больше, чем одно, при том, что ни один сервис не использует коннект
    #
    # второй вопрос, можно ли не использовать asynccontextmanager??
    # если да, то как?
    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        session = self.async_session()
        try:
            yield session
        finally:
            await session.commit()
            await session.close()

    async def execute_query(self, query) -> list:
        async with self.get_session() as session:
            result = await session.execute(query)
            return result.scalars().all()


async def get_db_searcher(
        db: AsyncDb = Depends(get_db),
) -> AsyncPostgres:
    return AsyncPostgres(db)
