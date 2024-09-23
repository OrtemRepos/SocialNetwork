from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exception.user import UserAlreadyExists, UserNotFoundException
from src.auth.schema.user import UserCreate, UserRead
from src.auth.util import get_password_hash
from src.logging_config import logger
from src.model import Friend, User


class UserRepository:
    async def get_by_id(
        self, session: AsyncSession, user_id: UUID
    ) -> User | None:
        try:
            user = await session.get(User, user_id)
            if user is None:
                raise UserNotFoundException(f"User {user_id} does not exist")
            UserRead.model_validate(user, from_attributes=True)
            return user
        except UserNotFoundException:
            logger.exception("User not found", user_id=user_id)
            return None
        except ValidationError:
            logger.exception("ValueError", user_id=user_id)
            return None

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> User | None:
        try:
            stmt = select(User).where(User.email == email)  # type: ignore
            user = await session.execute(stmt)
            if user is None:
                raise UserNotFoundException(f"User {email} does not exist")
            user_result = user.scalars().one()
            UserRead.model_validate(user_result, from_attributes=True)
            return user_result
        except UserNotFoundException:
            logger.exception("User not found", email=email)
            return None
        except ValidationError:
            logger.exception("ValueError", email=email)
            return None

    async def add(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> User | None:
        try:
            user = UserCreate(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user_model = User(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=get_password_hash(user.password),
            )
            session.add(user)
            await session.flush()
            UserRead.model_validate(user, from_attributes=True)
            return user_model
        except ValidationError:
            logger.exception("ValueError", user=user.__repr__())
            return None

    async def list(self, session: AsyncSession) -> list[User]:
        stmt = select(User)
        session_result = await session.execute(stmt)
        user_list = [User(*user) for user in session_result.scalars().all()]
        return user_list

    async def add_friend(
        self, session: AsyncSession, user_id: UUID, friend_id: UUID
    ):
        user = await self.get_by_id(session, user_id)
        friend = await self.get_by_id(session, friend_id)
        if user and friend:
            user.friends.append(friend)
            friend.friends.append(user)
            return True

    async def get_friend(
        self, user_id: UUID, friend_id: UUID, session: AsyncSession
    ) -> UserRead:
        user = await self.get_by_id(session, user_id)
        stmt = select(Friend).where(User.id == friend_id)
        return UserRead.model_validate(user, from_attributes=True)

    async def remove_friend(
        self, session: AsyncSession, user_id: UUID, friend_id: UUID
    ):
        user = await self.get_by_id(session, user_id)
        friend = await self.get_by_id(session, friend_id)
        if user and friend:
            pass


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
