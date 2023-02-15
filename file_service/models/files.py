from sqlalchemy import Column, func, String, DateTime, BigInteger, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

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

    meta: "FileMeta" = relationship("FileMeta", lazy="noload", back_populates="file", uselist=False)


class FileMeta(Base):
    __tablename__ = "file_meta"

    file_id = Column(ForeignKey("file.id", ondelete="CASCADE"), primary_key=True)
    title = Column(String)
    type = Column(String)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    file: "File" = relationship("File", lazy="noload", back_populates="meta", uselist=False)
