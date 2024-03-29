from uuid import UUID

from fastapi import APIRouter, Depends

from api.api_v1.deps import auth_required
from schemas.files import CompiledAnimationCreateSchema
from services.characters import AnimationService
from services.files import CompiledAnimationService

router = APIRouter()


@router.post("/{model_id:uuid}:animate/{animation_id:uuid}/", dependencies=[Depends(auth_required)])
async def animate_model(model_id: UUID, animation_id: UUID, service: AnimationService = Depends()):
    return await service.animate(model_id, animation_id)
