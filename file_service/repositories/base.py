from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

T = TypeVar('T')


class BaseRepository(Generic[T], ABC):
    prepared_statements = {}

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, meta: T) -> T:
        self.session.add(meta)
        await self.session.flush()
        await self.session.refresh(meta)
        return meta

    async def all(self, statement: Select, **params) -> list[T]:
        return (await self.session.execute(statement, **params)).scalars().all()

    async def one_or_none(self, statement: Select, **params) -> T | None:
        return (await self.session.execute(statement, **params)).scalars().one_or_none()

    async def first(self, statement: Select, **params) -> T | None:
        return (await self.session.execute(statement, **params)).scalars().first()
