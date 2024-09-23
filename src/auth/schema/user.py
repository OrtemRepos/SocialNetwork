from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from src.schema.base import Base


class UserRead(Base):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime


class UserCreate(Base):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserUpdate(Base):
    email: EmailStr | None
    first_name: str | None
    last_name: str | None
    password: str | None
