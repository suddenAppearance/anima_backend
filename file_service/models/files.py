from sqlalchemy import Column, func, String, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class File(Base):
    __tablename__ = "file"
    __table_args__ = (UniqueConstraint("author_id", "initial_filename", name="file_author_filename_uc"),)

    #  get_random_uuid() only PostgreSQL 13+
    id = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid(), primary_key=True)

    author_id = Column(UUID(as_uuid=True), index=True)
    bucket_name = Column(String)
    minio_path = Column(String)
    initial_filename = Column(String)
    size = Column(BigInteger)
    hash = Column(String)

    created_at = Column(DateTime, server_default=func.now())
