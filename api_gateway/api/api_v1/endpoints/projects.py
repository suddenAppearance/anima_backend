from fastapi import APIRouter, Depends

from api.api_v1.deps import auth_required
from schemas.projects import ProjectCreateSchema, ProjectRetrieveSchema
from services.projects import ProjectsService

router = APIRouter()


@router.post("/", dependencies=[Depends(auth_required)], response_model=ProjectRetrieveSchema)
async def create_project(project: ProjectCreateSchema, projects_service: ProjectsService = Depends()):
    return await projects_service.create_project(project)


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[ProjectRetrieveSchema])
async def get_all_projects(projects_service: ProjectsService = Depends()):
    return await projects_service.get_all_projects()
