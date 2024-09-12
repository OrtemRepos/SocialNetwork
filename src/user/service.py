from datetime import datetime
from typing import Union

from fastapi_users.models import ID
from pydantic import EmailStr

from src.auth.schema import UserRead
from src.user.schema import FriendRequest
from user.exception import AlreadyFriend, AlreadySentRequest, NotFound


class User:
    def __init__(
        self, id: ID, first_name: str, last_name: str, email: EmailStr
    ):
        UserRead(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            created_at=datetime.now(),
        )
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._friend: set[User | None] = set()
        self._request: set[FriendRequest | None] = set()

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _add_friend(self, user: "User"):
        self._friend.add(user)
        user._friend.add(self)

    def remove_from_friend(self, user: "User") -> Union["User", None]:
        if user in self._friend:
            self._friend.remove(user)
            user._friend.remove(self)
            user.send_friendrequest(self)
            return user
        raise NotFound(f"User {user=} not in friend list")

    def send_friendrequest(
        self, user: "User", msg: str = None
    ) -> FriendRequest | None:
        if user in self._friend:
            raise AlreadyFriend(f"User {user=} already in friend list")
        request = FriendRequest(
            sender_id=self.id, receiver_id=user.id, msg=msg
        )

        if request in self.send_request:
            raise AlreadySentRequest("You have already sent a friend request")
        accept_request = FriendRequest(
            sender_id=user.id, receiver_id=self.id, msg=msg
        )

        if accept_request in self.receive_request:
            self._request.remove(accept_request)
            self._add_friend(user)
            return accept_request
        self._request.add(request)
        user._request.add(request)
        return request

    def reject_friendrequest(self, user: "User") -> FriendRequest | None:
        request = self.get_request(user)
        if request in self._request:
            self._request.remove(request)
            user._request.remove(request)
            return request

    def get_request(self, user: "User") -> FriendRequest | None:
        for request in self._request:
            if request.receiver_id == user.id or request.sender_id == user.id:
                return request
        raise NotFound(f"Request from {user=} not found")

    @property
    def send_request(self):
        return [
            request
            for request in self._request
            if request.sender_id == self.id
        ]

    @property
    def receive_request(self):
        return [
            request
            for request in self._request
            if request.receiver_id == self.id
        ]
