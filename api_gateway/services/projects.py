from schemas.projects import ProjectCreateSchema, ProjectRetrieveSchema, ProjectDetailRetrieveSchema
from services.base import BaseService


class ProjectsService(BaseService):
    async def create_project(self, project: ProjectCreateSchema) -> ProjectRetrieveSchema:
        response = await self.project_service_gateway.create(project.dict())
        response.raise_for_status()
        project = response.json()
        user = self.keycloak.get_user_by_sub(project["author_id"])
        project["author"] = {
            "sub": user["id"],
            "first_name": user["firstName"],
            "last_name": user["lastName"],
            "email": user["email"]
        }
        return ProjectRetrieveSchema(**project)

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

    async def get_project_by_id(self, id: int) -> ProjectDetailRetrieveSchema:
        response = await self.project_service_gateway.get_project_by_id(id)
        response.raise_for_status()
        project = response.json()
        user = self.keycloak.get_user_by_sub(project["author_id"])
        project["author"] = {
            "sub": user["id"],
            "first_name": user["firstName"],
            "last_name": user["lastName"],
            "email": user["email"]
        }
        response = await self.animation_service_gateway.get_animations_by_project_id(project_id=project["id"])
        response.raise_for_status()
        animations = response.json()
        project["animations"] = animations
        return ProjectDetailRetrieveSchema(**project)
