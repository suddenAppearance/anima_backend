from uuid import UUID

from fastapi import APIRouter, Depends

from services.characters import AnimationService

router = APIRouter()


@router.post("/{model_id:uuid}:animate/{animation_id:uuid}/")
async def animate_model(model_id: UUID, animation_id: UUID, service: AnimationService = Depends()):
    return await service.animate(model_id, animation_id)
