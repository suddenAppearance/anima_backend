from fastapi import APIRouter, Depends, Query, UploadFile

from api.api_v1.deps import auth_required
from schemas.files import FileMetaRetrieveSchema, FileMetaCreateSchema
from services.file_service import FileService

router = APIRouter()


@router.get("/", dependencies=[Depends(auth_required)], response_model=list[FileMetaRetrieveSchema])
async def get_files(service: FileService = Depends(), type: str = Query(...)):
    return await service.get_files(type)


@router.put("/", dependencies=[Depends(auth_required)])
async def upload_file(file: UploadFile, service: FileService = Depends()):
    return await service.upload_file(file)


@router.post("/", dependencies=[Depends(auth_required)])
async def create_file_meta(meta: FileMetaCreateSchema, service: FileService = Depends()):
    return await service.create_meta(meta)
