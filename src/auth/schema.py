import datetime
from typing import Annotated
from uuid import UUID

from fastapi_users import schemas
from pydantic import Field

first_name = Annotated[str, Field(min_length=2, max_length=20)]
last_name = Annotated[str, Field(min_length=1, max_length=20)]
password = Annotated[str, Field(min_length=8, max_length=64)]


class UserRead(schemas.BaseUser[UUID]):
    first_name: first_name
    last_name: last_name
    created_at: datetime.datetime
    update_at: datetime.datetime | None = None


class UserCreate(schemas.BaseUserCreate):
    first_name: first_name
    last_name: last_name


class UserUpdate(schemas.BaseUserUpdate):
    first_name: first_name
    last_name: last_name
