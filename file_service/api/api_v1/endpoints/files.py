from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile

from api.api_v1.deps import auth_required
from schemas.files import FileInfoRetrieveSchema
from services.files import FileService

router = APIRouter()


@router.put("/", dependencies=[Depends(auth_required)], response_model=FileInfoRetrieveSchema)
async def upload_file(file: UploadFile, file_service: FileService = Depends()):
    return await file_service.create(file)


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[FileInfoRetrieveSchema])
async def get_all(file_service: FileService = Depends()):
    return await file_service.get_all()


@router.get("/{id:uuid}/")
async def get_file_info_by_id(id: UUID, file_service: FileService = Depends()):
    return await file_service.get_file_info_by_id(id)
