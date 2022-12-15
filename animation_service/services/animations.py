from models import Animation
from schemas.animations import AnimationCreateSchema, AnimationRetrieveSchema
from services.base import BaseService


class AnimationsService(BaseService):
    @property
    def repository(self):
        return self.animations_repository

    async def create_animation(self, animation: AnimationCreateSchema) -> AnimationRetrieveSchema:
        animation = await self.repository.create(Animation(**animation.dict(), author_id=self.request.user.sub))
        return AnimationRetrieveSchema.from_orm(animation)

    async def get_all(self) -> list[AnimationRetrieveSchema]:
        animations = await self.repository.get_all()
        return [AnimationRetrieveSchema.from_orm(animation) for animation in animations]

    async def get_by_project_id(self, project_id: int) -> list[AnimationRetrieveSchema]:
        animations = await self.repository.get_all_by_project_id(project_id=project_id)
        return [AnimationRetrieveSchema.from_orm(animation) for animation in animations]
