from uuid import UUID

from sqlalchemy import select, delete, bindparam
from sqlalchemy.orm import selectinload

from models import File, FileMeta, CompiledAnimation
from repositories.base import BaseRepository


class FilesRepository(BaseRepository[File]):
    async def get_by_id(self, id: UUID) -> File | None:
        statement = select(File).filter(File.id == id)
        return await self.one_or_none(statement)

    async def get_all(self) -> list[File]:
        statement = select(File)
        return await self.all(statement)

    async def get_by_filename_and_author_id(self, filename: str, author_id: UUID) -> File | None:
        statement = select(File).filter(File.initial_filename == filename, File.author_id == author_id)
        return await self.one_or_none(statement)

    async def get_all_by_author_id(self, author_id: UUID) -> list[File]:
        statement = select(File).filter(File.author_id == author_id)
        return await self.all(statement)

    async def delete_by_id(self, id: UUID) -> bool:
        statement = delete(File).filter(File.id == id)
        result = await self.session.execute(statement)
        return result.rowcount > 0


class FileMetaRepository(BaseRepository[FileMeta]):
    class PreparedStatements:
        get_by_file_id = select(FileMeta).filter(FileMeta.file_id == bindparam("file_id"))
        get_by_type = select(FileMeta).filter(FileMeta.type == bindparam("type"))

    async def get_by_file_id(self, file_id: UUID, load_file: bool = False) -> FileMeta | None:
        return await self.one_or_none(
            self.PreparedStatements.get_by_file_id
            if not load_file
            else self.PreparedStatements.get_by_file_id.options(selectinload(FileMeta.file)),
            params={"file_id": file_id},
        )

    async def get_by_type(self, type: str, load_file: bool = False) -> list[FileMeta]:
        return await self.all(
            self.PreparedStatements.get_by_type
            if not load_file
            else self.PreparedStatements.get_by_type.options(selectinload(FileMeta.file)),
            params={"type": type},
        )


class CompiledAnimationRepository(BaseRepository[CompiledAnimation]):
    class PreparedStatements:
        get_by_model_id_and_animation_id = select(CompiledAnimation).filter(
            CompiledAnimation.model_id == bindparam("model_id"),
            CompiledAnimation.animation_id == bindparam("animation_id"),
        )

    async def get_by_model_id_and_animation_id(self, model_id: UUID, animation_id: UUID) -> CompiledAnimation | None:
        return await self.one_or_none(
            self.PreparedStatements.get_by_model_id_and_animation_id.options(selectinload(CompiledAnimation.file)),
            params={"model_id": model_id, "animation_id": animation_id},
        )
