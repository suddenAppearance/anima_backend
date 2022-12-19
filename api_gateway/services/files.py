from fastapi import UploadFile

from schemas.files import FileInfoRetrieveSchema
from services.base import BaseService


class FilesService(BaseService):
    async def upload_file(self, file: UploadFile) -> FileInfoRetrieveSchema:
        response = await self.file_service_gateway.upload_file(file)
        response.raise_for_status()
        file = response.json()
        user = self.keycloak.get_user_by_sub(file["author_id"])
        file["author"] = {
            "sub": user["id"],
            "first_name": user["firstName"],
            "last_name": user["lastName"],
            "email": user["email"]
        }

        return FileInfoRetrieveSchema(**file)

    async def get_all(self) -> list[FileInfoRetrieveSchema]:
        response = await self.file_service_gateway.get_all()
        response.raise_for_status()
        files = response.json()
        for file in files:
            user = self.keycloak.get_user_by_sub(file["author_id"])
            file["author"] = {
                "sub": user["id"],
                "first_name": user["firstName"],
                "last_name": user["lastName"],
                "email": user["email"]
            }

        return [FileInfoRetrieveSchema(**file) for file in files]
