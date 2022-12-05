from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from api.api_v1.deps import auth_required
from schemas.projects import ProjectCreateSchema, ProjectRetrieveSchema
from services.projects import ProjectsService

router = APIRouter()


@router.post("/", dependencies=[Depends(auth_required)], status_code=202)
async def create_project(project: ProjectCreateSchema, projects_service: ProjectsService = Depends()):
    await projects_service.create(project)
    return Response(status_code=202)


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[ProjectRetrieveSchema])
async def get_all_projects(projects_service: ProjectsService = Depends()):
    return await projects_service.get_all()


@router.get("/{id:int}/", response_model=ProjectRetrieveSchema)
async def get_project_by_id(id: int, project_service: ProjectsService = Depends()):
    project = await project_service.get_by_id(id)
    if not project:
        raise HTTPException(status_code=404, detail={"message": "Resource not found"})
    return project
