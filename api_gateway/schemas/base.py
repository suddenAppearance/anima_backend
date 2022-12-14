from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    sub: UUID


class UserInfo(User):
    email: EmailStr
    first_name: str
    last_name: str
