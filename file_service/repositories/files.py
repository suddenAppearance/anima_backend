from uuid import UUID

from sqlalchemy import select, delete

from models import File
from repositories.base import BaseRepository


class FilesRepository(BaseRepository[File]):
    async def create(self, file: File) -> File:
        self.session.add(file)
        await self.session.flush()
        await self.session.refresh(file)
        return file

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
