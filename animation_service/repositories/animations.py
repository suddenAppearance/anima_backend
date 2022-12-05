from sqlalchemy import select, delete

from models import Animation
from repositories.base import BaseRepository


class AnimationRepository(BaseRepository[Animation]):
    def create(self, animation: Animation):
        self.session.add(animation)
        await self.session.flush()

    def get_by_id(self, id: int) -> Animation | None:
        statement = select(Animation).filter(Animation.id == id)
        return await self.one_or_none(statement)

    def get_all_by_project_id(self, project_id: int) -> list[Animation]:
        statement = select(Animation).filter(Animation.project_id == project_id)
        return await self.all(statement)

    def delete_by_id(self, id: int) -> bool:
        statement = delete(Animation).filter(Animation.id == id)
        result = await self.session.execute(statement)
        return result.rowcount > 0
