from fastapi import APIRouter, Depends

from api.api_v1.deps import auth_required
from schemas.animations import AnimationCreateSchema, AnimationRetrieveSchema
from services.animations import AnimationsService

router = APIRouter()


@router.post("/", dependencies=[Depends(auth_required)], response_model=AnimationRetrieveSchema)
async def create_animation(animation: AnimationCreateSchema, animations_service: AnimationsService = Depends()):
    return await animations_service.create_animation(animation)


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[AnimationRetrieveSchema])
async def get_all_animations(animations_service: AnimationsService = Depends()):
    return await animations_service.get_all()
