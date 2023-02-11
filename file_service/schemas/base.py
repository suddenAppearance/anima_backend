from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    sub: UUID


class MinioBuckets(str, Enum):
    USERS_FILES = "usersfiles"
