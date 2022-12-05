from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(BigInteger, primary_key=True)

    title = Column(String(55))
    description = Column(String(240))
    author_id = Column(UUID(as_uuid=True))

    created_at = Column(DateTime, server_default=func.now(),)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

