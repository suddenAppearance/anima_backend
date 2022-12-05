from models import Project
from repositories.projects import ProjectsRepository
from schemas.projects import ProjectCreateSchema, ProjectRetrieveSchema
from services.base import BaseService


class ProjectsService(BaseService):
    @property
    def repository(self) -> ProjectsRepository:
        return self.projects_repository

    async def create(self, project: ProjectCreateSchema):
        await self.repository.create(Project(**project.dict(), author_id=self.request.user.sub))

    async def get_all(self) -> list[ProjectRetrieveSchema]:
        return [ProjectRetrieveSchema.from_orm(project) for project in await self.repository.get_all()]

    async def get_by_id(self, id: int) -> ProjectRetrieveSchema | None:
        project = await self.repository.get_by_id(id)
        return ProjectRetrieveSchema.from_orm(project) if project else None