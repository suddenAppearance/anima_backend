from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def all(self, statement: Select) -> list[T]:
        return (await self.session.execute(statement)).scalars().all()

    async def one_or_none(self, statement: Select) -> T | None:
        return (await self.session.execute(statement)).scalars().one_or_none()

    async def first(self, statement: Select) -> T | None:
        return (await self.session.execute(statement)).scalars().first()

