from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FriendRequest(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    msg: str | None = None

    model_config = ConfigDict(frozen=True)
