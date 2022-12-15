from fastapi import APIRouter, Depends, Query

from api.api_v1.deps import auth_required
from schemas.animations import AnimationCreateSchema, AnimationRetrieveSchema
from services.animations import AnimationsService

router = APIRouter()


@router.post("/", dependencies=[Depends(auth_required)], response_model=AnimationRetrieveSchema)
async def create_animation(animation: AnimationCreateSchema, animations_service: AnimationsService = Depends()):
    return await animations_service.create_animation(animation)


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[AnimationRetrieveSchema])
async def get_all_animations(
    project_id: int | None = Query(None, description="Фильтр по проекту"),
    animations_service: AnimationsService = Depends(),
):
    if project_id is None:
        return await animations_service.get_all()
    else:
        return await animations_service.get_by_project_id(project_id)
