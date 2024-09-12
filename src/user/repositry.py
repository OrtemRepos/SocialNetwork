import asyncio
import functools
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from uuid import UUID

from sqlalchemy import select

from src.auth.exceptions import UserAlreadyExists, UserNotExists
from src.auth.schema import UserCreate, UserRead
from src.auth.service import get_user_manager
from src.database import get_session, get_user_db
from src.models import User as UserTable
from src.user.service import User

get_async_session_context = asynccontextmanager(get_session)
get_user_db_context = asynccontextmanager(get_user_db)
get_user_manager_context = asynccontextmanager(get_user_manager)


def async_start(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@asynccontextmanager
async def get_async_session():
    async with get_async_session_context() as session:
        yield session


@asynccontextmanager
async def get_user_manager(self):
    session = get_async_session()
    async with (
        get_user_db_context(session) as user_db,
        get_user_manager_context(user_db) as user_manager,
    ):
        yield user_manager


class AbstractRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def add(self, user: User) -> User:
        raise NotImplementedError


class UserRepository(AbstractRepository):
    async def get_by_id(self, user_id: UUID):
        try:
            async with get_user_manager() as user_manager:
                user = await user_manager.get(user_id)
                print(f"User {user}")
        except UserNotExists:
            print(f"User {user_id} does not exist")

    @async_start
    async def get_by_email(self, email: str):
        try:
            async with get_user_manager() as user_manager:
                user = await user_manager.get_by_email(email)
                print(f"User {user}")
        except UserNotExists:
            print(f"User {email} does not exist")

    @async_start
    async def add(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_superuser: bool = False,
    ):
        try:
            async with get_user_manager() as user_manager:
                user = await user_manager.create(
                    UserCreate(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                        is_superuser=is_superuser,
                    )
                )
                print(f"User created {user}")
        except UserAlreadyExists:
            print(f"User {email} already exists")

    @async_start
    async def list(self):
        stmt = select(UserTable)
        async with get_async_session() as session:
            res = await session.execute(stmt)
        return [
            UserRead.model_validate(user, from_attributes=True)
            for user in res.scalars().all()
        ]


class FakeUserRepository(AbstractRepository):
    def __init__(self, list_user: list[User | None]):
        self.list_user = list_user

    def get_by_id(self, user_id: UUID) -> User | None:
        for user in self.list_user:
            if user.id == user_id:
                return user
        print(f"User {user_id=} does not exist")
        raise UserNotExists(f"User with {user_id=} does not exist")

    def get_by_email(self, email: str):
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
