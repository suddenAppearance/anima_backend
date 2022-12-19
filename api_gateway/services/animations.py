from schemas.animations import AnimationCreateSchema, AnimationRetrieveSchema
from services.base import BaseService


class AnimationsService(BaseService):
    async def create_animation(self, animation: AnimationCreateSchema) -> AnimationRetrieveSchema:
        response = await self.project_service_gateway.get_project_by_id(animation.project_id)
        response.raise_for_status()
        response = await self.file_service_gateway.get_file_by_id(animation.file_id)
        response.raise_for_status()

        response = await self.animation_service_gateway.create_animation(animation.dict())
        response.raise_for_status()
        animation = response.json()
        user = self.keycloak.get_user_by_sub(animation["author_id"])
        animation["author"] = {
            "sub": user["id"],
            "first_name": user["firstName"],
            "last_name": user["lastName"],
            "email": user["email"]
        }

        return AnimationRetrieveSchema(**animation)
