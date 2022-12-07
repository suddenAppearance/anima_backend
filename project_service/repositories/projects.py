from sqlalchemy import select

from models import Project
from repositories.base import BaseRepository


class ProjectsRepository(BaseRepository[Project]):
    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def get_by_id(self, id: int) -> Project | None:
        statement = select(Project).filter(Project.id == id)
        return await self.one_or_none(statement)

    async def get_all(self) -> list[Project]:
        statement = select(Project)
        return await self.all(statement)
