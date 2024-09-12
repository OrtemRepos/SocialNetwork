from fastapi_users.models import ID
from pydantic import BaseModel, ConfigDict


class FriendRequest(BaseModel):
    sender_id: ID
    receiver_id: ID
    msg: str | None = None

    model_config = ConfigDict(frozen=True)
