from schemas.projects import ProjectCreateSchema, ProjectRetrieveSchema
from services.base import BaseService


class ProjectsService(BaseService):
    async def create_project(self, project: ProjectCreateSchema) -> ProjectRetrieveSchema:
        response = await self.project_service_gateway.create(project.dict())
        response.raise_for_status()
        return ProjectRetrieveSchema(**response.json())

    async def get_all_projects(self) -> list[ProjectRetrieveSchema]:
        response = await self.project_service_gateway.get_projects()
        response.raise_for_status()
        projects = response.json()
        for project in projects:
            user = self.keycloak.get_user_by_sub(project["author_id"])
            project["author"] = {
                "sub": user["id"],
                "first_name": user["firstName"],
                "last_name": user["lastName"],
                "email": user["email"]
            }

        return [ProjectRetrieveSchema(**project) for project in projects]
