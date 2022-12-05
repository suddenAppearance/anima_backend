from sqlalchemy import Column, BigInteger, String
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Animation(Base):
    __tablename__ = "animation"

    id = Column(BigInteger, primary_key=True)

    title = Column(String(55))
    author_id = Column(UUID(as_uuid=True))
    project_id = Column(BigInteger, index=True)
    minio_file_url = Column(String)

    created_at = Column(UUID)
    updated_at = Column(UUID)
