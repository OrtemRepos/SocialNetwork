import datetime
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[UUID]):
    first_name: str = Field(repr=True)
    last_name: str = Field(repr=True)
    email: str = Field(repr=True)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    update_at: datetime.datetime | None = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(repr=True)
    last_name: str = Field(repr=True)
    email: EmailStr = Field(repr=True)
    password: str = Field(repr=True)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str = Field(repr=True)
    last_name: str = Field(repr=True)
    password: str = Field(repr=True, default=None)
    email: EmailStr = Field(repr=True, default=None)
    is_active: bool = None
    is_superuser: bool = None
    is_verified: bool = None
