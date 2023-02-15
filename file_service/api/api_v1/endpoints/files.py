from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, Query

from api.api_v1.deps import auth_required
from schemas.files import FileInfoRetrieveSchema, FileMetaTypeEnum, FileMetaRetrieveSchema
from services.files import FileService, FileMetaService

router = APIRouter()


@router.put("/", dependencies=[Depends(auth_required)], response_model=FileInfoRetrieveSchema)
async def upload_file(file: UploadFile, file_service: FileService = Depends()):
    return await file_service.create(file)


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[FileMetaRetrieveSchema])
async def get_all(file_meta_service: FileMetaService = Depends(), type: FileMetaTypeEnum = Query(...)):
    return await file_meta_service.get_full_by_type(type)


@router.get("/{id:uuid}/", response_model=FileMetaRetrieveSchema)
async def get_file_info_by_id(id: UUID, file_meta_service: FileMetaService = Depends()):
    return await file_meta_service.get_full_file(file_id=id)
