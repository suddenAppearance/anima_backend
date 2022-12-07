from sqlalchemy import select, delete

from models import Animation
from repositories.base import BaseRepository


class AnimationsRepository(BaseRepository[Animation]):
    async def create(self, animation: Animation) -> Animation:
        self.session.add(animation)
        await self.session.flush()
        await self.session.refresh(animation)
        return animation

    async def get_all(self) -> list[Animation]:
        statement = select(Animation)
        return await self.all(statement)

    async def get_by_id(self, id: int) -> Animation | None:
        statement = select(Animation).filter(Animation.id == id)
        return await self.one_or_none(statement)

    async def get_all_by_project_id(self, project_id: int) -> list[Animation]:
        statement = select(Animation).filter(Animation.project_id == project_id)
        return await self.all(statement)

    async def delete_by_id(self, id: int) -> bool:
        statement = delete(Animation).filter(Animation.id == id)
        result = await self.session.execute(statement)
        return result.rowcount > 0
