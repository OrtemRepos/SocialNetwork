import asyncio
import functools
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import UserAlreadyExists, UserNotExists
from src.auth.schema import UserRead
from src.models import User


def async_start(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


class UserRepository:
    async def get_by_id(
        self, session: AsyncSession, user_id: UUID
    ) -> User | None:
        try:
            user = await session.get(User, user_id)
            assert user is not None
            UserRead.model_validate(user, from_attributes=True)
            return user
        except UserNotExists:
            print(f"User {user_id} does not exist")
            return None

    @async_start
    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> User | None:
        try:
            stmt = select(User).where(User.email == email)  # type: ignore
            user = await session.execute(stmt)
            user_result = user.scalars().one()
            UserRead.model_validate(user_result, from_attributes=True)
            return user_result
        except UserNotExists:
            print(f"User {email} does not exist")
            return None

    @async_start
    async def add(
        self,
        session: AsyncSession,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_superuser: bool = False,
    ):
        try:
            session.add(
                User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    is_superuser=is_superuser,
                )
            )
        except UserAlreadyExists:
            print(f"User {email} already exists")

    @async_start
    async def list(self, session: AsyncSession) -> list[User]:
        stmt = select(User)
        session_result = await session.execute(stmt)
        user_list = [User(*user) for user in session_result.scalars().all()]  # type: ignore[misc]
        return user_list

    @async_start
    async def add_friend(
        self, session: AsyncSession, user_id: UUID, friend_id: UUID
    ):
        user = await self.get_by_id(session, user_id)
        friend = await self.get_by_id(session, friend_id)
        if user and friend:
            user.friend.add(friend)

    @async_start
    async def remove_friend(
        self, session: AsyncSession, user_id: UUID, friend_id: UUID
    ):
        user = await self.get_by_id(session, user_id)
        friend = await self.get_by_id(session, friend_id)
        if user and friend:
            user.friend.remove(friend)


class FakeUserRepository:
    def __init__(self, list_user: list[User]):
        self.list_user = list_user

    def get_by_id(self, user_id: UUID) -> User | None:
        for user in self.list_user:
            if user.id == user_id:
                return user
        print(f"User {user_id=} does not exist")
        raise UserNotExists(f"User with {user_id=} does not exist")

    def get_by_email(self, email: str) -> User | None:
        for user in self.list_user:
            if user.email == email:
                return user
        raise UserNotExists(f"User with {email=} does not exist")

    def add(self, user: User):
        if user.email not in [user.email for user in self.list_user]:
            self.list_user.append(user)
        else:
            raise UserAlreadyExists(f"User with {user.email=} already exists")

    def list(self):
        return self.list_user
