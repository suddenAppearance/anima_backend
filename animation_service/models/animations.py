from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Animation(Base):
    __tablename__ = "animation"

    id = Column(BigInteger, primary_key=True)

    title = Column(String(55))
    author_id = Column(UUID(as_uuid=True), index=True)
    project_id = Column(BigInteger, index=True)
    file_id = Column(UUID(as_uuid=True), index=True)

    created_at = Column(DateTime, server_default=func.now(), )
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
