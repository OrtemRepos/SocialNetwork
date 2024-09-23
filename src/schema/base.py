from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    created_at: datetime | None = None
    update_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    status: Literal["success", "fail"] = "success"

    model_config = ConfigDict(from_attributes=True)


class HTTPResponse(BaseResponse):
    detail: list | None = None
